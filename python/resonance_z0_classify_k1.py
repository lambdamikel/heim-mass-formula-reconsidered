"""
Z=0 branch classification for k=1 mesonic resonances (G-Tabelle IV).

Same logic as resonance_z0_classify.py (which did k=2 baryons) but for
the 23 mesonic entries.

Per Heim J0032: f(N) = a·N/(N+1) + b·N with (a, b) from eqs. 14a-14b₁
depending only on (k, P, q, κ) — NOT on Q.  The Q value per state
is part of an excitation tower Q(N) = Q(N=0) + 2·z(N) where z(N)
is unknown.  Only the z=0 branch should match the ab initio prediction.

Mesonic Q = 2·J with J integer, so Q ∈ {0, 2, 4, 6, 8}.
"""

from __future__ import annotations

import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np

import formulae as fm
from g_tables import TABLE_IV_MESONS_K1
from resonance_wscan_baryons import match_sector_k2
from resonance_consistency_baryons import implied_w_k2
from anregung_ab_initio import predict as predict_anregung

CACHE = Path(__file__).parent / "meson_candidates_cache.pkl"


def expand_meson_states():
    """Each Tabelle IV entry → list of (label, P, qx, M_t, KB_t).
    Singlets become 1 state, doublets 2 states (neutral and charged)."""
    out = []
    for r in TABLE_IV_MESONS_K1:
        sym = r.symbol
        P = r.P
        if isinstance(r.mass_MeV, tuple):
            # doublet (neutral, charged)
            out.append((f"{sym}⁰", P, 0, r.mass_MeV[0], r.K_B[0]))
            out.append((f"{sym}±", P, 1, r.mass_MeV[1], r.K_B[1]))
        else:
            out.append((sym, P, 0, r.mass_MeV, r.K_B))
    return out


def expand_meson_pub_N():
    out = {}
    for r in TABLE_IV_MESONS_K1:
        sym = r.symbol
        if isinstance(r.N, tuple):
            out[f"{sym}⁰"] = r.N[0]
            out[f"{sym}±"] = r.N[1]
        else:
            out[sym] = r.N
    return out


def scan_candidates_k1(states, K_n_max=32, K_m_max=32,
                        K_p_max=48, K_sig_max=32, W0_max=1e8):
    """For each meson state, gather all (Q, nmps) candidates from k=1
    sector scans.  Q ∈ {0, 2, 4, 6, 8}, κ-independent (mass and K_B
    don't depend on κ for excited states)."""
    Q_candidates = [0, 2, 4, 6, 8]
    I = fm.calc_Q(1)
    by_sector = defaultdict(list)
    for s in states:
        label, P, qx, M_t, KB_t = s
        by_sector[(P, qx)].append((label, M_t, KB_t))

    results = defaultdict(list)
    for (P, qx), tgts in sorted(by_sector.items()):
        for Q in Q_candidates:
            valids = [fm.calc_W(1, 1, P, Q, kap, qx, I) for kap in (0, 1)]
            valids = [w for w in valids if w > 0]
            if not valids:
                continue
            W0_min = min(valids)
            if W0_min > W0_max:
                continue
            print(f"  P={P} q={qx:+d} Q={Q}: {len(tgts)} targets "
                  f"(W_0 = {W0_min:.2e})", flush=True)
            m = match_sector_k2(P, Q, qx, tgts,
                                K_n_max=K_n_max, K_m_max=K_m_max,
                                K_p_max=K_p_max, K_sig_max=K_sig_max, k=1)
            for label, mtch in m.items():
                if mtch is None:
                    continue
                M_t, KB_t = next(
                    (M, K) for (lbl, M, K) in tgts if lbl == label)
                dM = abs(mtch["M_MeV"] - M_t)
                dKB = abs(mtch["K_B"] - KB_t)
                score = dM + 100 * max(0, dKB - 0.5)
                results[label].append({
                    **mtch, "Q": Q, "score": score,
                    "P": P, "qx": qx, "M_t": M_t, "KB_t": KB_t,
                    "dM": dM, "dKB": dKB,
                })
    return dict(results)


def get_W0(P, Q, qx, kap, k, I):
    W0 = fm.calc_W(1, k, P, Q, kap, qx, I)
    return W0 if W0 > 0 and np.isfinite(W0) else None


def main():
    import sys
    print("=" * 92)
    print(" Z=0 branch classification for k=1 mesonic resonances")
    print("=" * 92)
    print()

    all_states = expand_meson_states()
    pub_N = expand_meson_pub_N()
    print(f"  {len(all_states)} meson states")
    I = fm.calc_Q(1)
    Nconst_q0 = fm.calc_N(1, 0, I)
    Nconst_q1 = fm.calc_N(1, 1, I)

    if CACHE.exists() and "--rescan" not in sys.argv:
        print(f"Loading cached candidates from {CACHE.name} ...")
        with open(CACHE, "rb") as f:
            cands = pickle.load(f)
    else:
        print("Running scan_candidates_k1 ...")
        cands = scan_candidates_k1(all_states)
        with open(CACHE, "wb") as f:
            pickle.dump(cands, f)
    print(f"  {len(cands)} states have ≥ 1 candidate")

    LAMBDA = 50.0
    Z0_THRESHOLD = 0.05

    print()
    print(f"  {'symbol':<14} {'P':>2} {'qx':>3} {'N':>4} {'M_t':>10} {'KB':>4}  "
          f"{'Q*':>3} {'κ*':>3}  {'f_imp':>10} {'f_pred':>10} {'|Δf|':>10}  "
          f"{'class':>6}")
    print("  " + "-" * 96)
    classifications = defaultdict(list)

    for state in all_states:
        label, P, qx, M_t, KB_t = state
        if label not in cands:
            continue
        N_idx = pub_N.get(label)
        if N_idx is None:
            continue
        Nconst = Nconst_q0 if qx == 0 else Nconst_q1

        # First pass: only consider candidates with dM < dM_max, dKB < dKB_max.
        # Among those, pick smallest df.  This avoids false z=0 from coincidental
        # f-match at large mass error.
        dM_max = 1.0      # MeV
        dKB_max = 0.6
        best = None
        best_df = 1e18
        for c in cands[label]:
            Q = c["Q"]
            nmps = c["nmps"]
            dM = c["dM"]
            dKB = c["dKB"]
            if dM > dM_max or dKB > dKB_max:
                continue
            w = implied_w_k2(nmps, I, Nconst, k=1)
            for kap in (0, 1):
                W0 = get_W0(P, Q, qx, kap, 1, I)
                if W0 is None or W0 > 1e8:
                    continue
                f_imp = w / W0 - 1.0
                a_pred, b_pred = predict_anregung(1, P, Q, kap, qx)
                f_pred = a_pred * N_idx / (N_idx + 1.0) + b_pred * N_idx
                df = abs(f_imp - f_pred)
                if df < best_df:
                    best_df = df
                    best = (Q, kap, nmps, f_imp, f_pred, df, dM, dKB)
        # If no candidate fits dM/dKB tolerance, fall back to best dM regardless of df.
        best_score = 1e18
        if best is None:
            for c in cands[label]:
                Q = c["Q"]
                nmps = c["nmps"]
                dM = c["dM"]
                dKB = c["dKB"]
                w = implied_w_k2(nmps, I, Nconst, k=1)
                for kap in (0, 1):
                    W0 = get_W0(P, Q, qx, kap, 1, I)
                    if W0 is None or W0 > 1e8:
                        continue
                    f_imp = w / W0 - 1.0
                    a_pred, b_pred = predict_anregung(1, P, Q, kap, qx)
                    f_pred = a_pred * N_idx / (N_idx + 1.0) + b_pred * N_idx
                    df = abs(f_imp - f_pred)
                    score = dM + 100 * max(0, dKB - 0.5)
                    if best is None or score < best_score:
                        best_score = score
                        best = (Q, kap, nmps, f_imp, f_pred, df, dM, dKB)
        if best is None:
            continue
        Q, kap, nmps, f_imp, f_pred, df, dM, dKB = best
        klass = "z=0" if df < Z0_THRESHOLD else "z≠0"
        classifications[klass].append((label, P, qx, N_idx, M_t, KB_t,
                                         Q, kap, nmps, f_imp, f_pred, df,
                                         dM, dKB))
        print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d} {M_t:>10.4f} {KB_t!s:>4}  "
              f"{Q:>3} {kap:>3}  {f_imp:>+10.4f} {f_pred:>+10.4f} {df:>10.4f}  "
              f"{klass:>6}")

    print()
    for klass in sorted(classifications.keys()):
        print(f"  {klass}: {len(classifications[klass])} states")

    print()
    print("z=0 branch sectors:")
    z0_by_sector = defaultdict(list)
    for r in classifications["z=0"]:
        label, P, qx, N_idx, M_t, KB_t, Q, kap, nmps, f_imp, f_pred, df, dM, dKB = r
        z0_by_sector[(P, qx, kap)].append(r)
    for key in sorted(z0_by_sector.keys()):
        items = z0_by_sector[key]
        if len(items) < 1:
            continue
        P, qx, kap = key
        a_pred, b_pred = predict_anregung(1, P, items[0][6], kap, qx)
        df_max = max(r[11] for r in items)
        print(f"  P={P} q={qx:+d} κ={kap}  ({len(items)} states)  "
              f"a_pred={a_pred:+.4f}  b_pred={b_pred:+.4f}  max |Δf|={df_max:.4f}")
        for r in sorted(items, key=lambda r: r[3]):
            label, _, _, N_idx, M_t, _, Q, _, nmps, f_imp, f_pred, df, dM, _ = r
            print(f"    {label:<14} N={N_idx:>4d}  Q={Q}  M={M_t:>8.3f}"
                  f"  f_imp={f_imp:+.4f}  f_pred={f_pred:+.4f}  Δf={df:+.4f}"
                  f"  ΔM={dM:.3f}")


if __name__ == "__main__":
    main()
