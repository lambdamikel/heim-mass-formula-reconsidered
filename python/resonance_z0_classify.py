"""
Z=0 branch classification — re-rank candidates by ab initio f(N) prediction.

Per Heim J0032 p.15: f(N) coefficients (a, b) from eqs. 14a-14b₁ depend
only on (k, P, q, κ), NOT on Q.  Q can change with N via Q(N) = Q(N=0)
+ 2·z(N) where z(N) "noch völlig unbekannt" (eq. 14c).  The ab initio
(a, b) is the prediction for the *z=0 branch* — Q stays at its ground
value through the excitation tower.

Strategy:
  1. For each state, get all (Q, nmps) candidates with K_B-exact and
     mass-within-tol.
  2. For each candidate, compute implied f_imp = w/W_0(P, Q, κ, q) − 1
     for κ ∈ {0, 1}.
  3. Compute predicted f_pred(N) = a_pred·N/(N+1) + b_pred·N from the
     ab initio formula at (k, P, q, κ).
  4. Score each (Q, κ) by mass+K_B match plus |f_imp − f_pred|.
  5. The best (Q, κ) per state — if Δf is small — is the z=0 branch
     assignment.  States where no candidate fits f_pred within
     tolerance are flagged as z≠0 branch.
"""

from __future__ import annotations

import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np

import formulae as fm
from g_tables import (TABLE_V_a_BARYONS_K2, TABLE_V_b_BARYONS_K2,
                      TABLE_V_c_BARYONS_K2_SIGMA)
from resonance_wscan_baryons import expand_to_states, scan_all_candidates
from resonance_consistency_baryons import (collect_published_N,
                                            implied_w_k2)
from anregung_ab_initio import predict as predict_anregung

CACHE = Path(__file__).parent / "baryon_candidates_cache.pkl"


def get_W0(P, Q, qx, kap, k, I):
    W0 = fm.calc_W(1, k, P, Q, kap, qx, I)
    return W0 if W0 > 0 and np.isfinite(W0) else None


def main():
    import sys
    print("=" * 92)
    print(" Z=0 branch classification via ab initio (a, b) prediction")
    print("=" * 92)
    print()

    all_states = (expand_to_states(TABLE_V_a_BARYONS_K2)
                   + expand_to_states(TABLE_V_b_BARYONS_K2)
                   + expand_to_states(TABLE_V_c_BARYONS_K2_SIGMA))
    pub_N = collect_published_N(all_states)
    I = fm.calc_Q(2)
    Nconst_q0 = fm.calc_N(2, 0, I)
    Nconst_q1 = fm.calc_N(2, 1, I)

    # Load candidates
    if CACHE.exists() and "--rescan" not in sys.argv:
        print(f"Loading candidates from {CACHE.name} ...")
        with open(CACHE, "rb") as f:
            cands = pickle.load(f)
    else:
        print("Running scan_all_candidates...")
        cands = scan_all_candidates(all_states)
        with open(CACHE, "wb") as f:
            pickle.dump(cands, f)
    print(f"  loaded {len(cands)} states")

    # For each state: pick best (Q, κ) by combined mass + K_B + |Δf|
    LAMBDA = 50.0     # weight of f-mismatch term

    print()
    print(f"  {'symbol':<14} {'P':>2} {'qx':>3} {'N':>4} {'M_t':>10} {'KB':>4}  "
          f"{'Q*':>3} {'κ*':>3}  {'f_imp':>8} {'f_pred':>8} {'|Δf|':>8}  "
          f"{'class':>6}")
    print("  " + "-" * 96)

    Z0_THRESHOLD = 0.05    # |Δf| > 5% → z≠0
    classifications = defaultdict(list)   # 'z0' | 'z!=0' → list of records

    for state in all_states:
        label, P, qx, M_t, KB_t = state
        if label not in cands or not cands[label]:
            continue
        N_idx = pub_N.get(label)
        if N_idx is None:
            continue
        Nconst = Nconst_q0 if qx == 0 else Nconst_q1
        q_abs = abs(qx)

        best = None
        best_score = 1e18
        for c in cands[label]:
            Q = c["Q"]
            nmps = c["nmps"]
            dM = abs(c["M_MeV"] - M_t)
            dKB = abs(c["K_B"] - KB_t)
            w = implied_w_k2(nmps, I, Nconst)
            for kap in (0, 1):
                W0 = get_W0(P, Q, qx, kap, 2, I)
                if W0 is None or W0 > 1e8:
                    continue
                f_imp = w / W0 - 1.0
                a_pred, b_pred = predict_anregung(2, P, Q, kap, qx)
                f_pred = a_pred * N_idx / (N_idx + 1.0) + b_pred * N_idx
                df = abs(f_imp - f_pred)
                score = dM + 100 * max(0, dKB - 0.5) + LAMBDA * df
                if score < best_score:
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
              f"{Q:>3} {kap:>3}  {f_imp:>+8.4f} {f_pred:>+8.4f} {df:>8.4f}  "
              f"{klass:>6}")

    print()
    print(f"  Classifications:")
    for klass in sorted(classifications.keys()):
        items = classifications[klass]
        print(f"    {klass}: {len(items)} states")

    # Group z=0 states by (P, q, kap) and verify each sub-set fits a single
    # (a_pred, b_pred) curve.
    print()
    print("z=0 branch sectors (predicted (a, b) per sector):")
    z0_by_sector = defaultdict(list)
    for r in classifications["z=0"]:
        label, P, qx, N_idx, M_t, KB_t, Q, kap, nmps, f_imp, f_pred, df, dM, dKB = r
        z0_by_sector[(P, qx, kap)].append(r)
    for key in sorted(z0_by_sector.keys()):
        items = z0_by_sector[key]
        if len(items) < 2:
            continue
        P, qx, kap = key
        # Compute predicted (a, b) for this sector — Q doesn't matter
        a_pred, b_pred = predict_anregung(2, P, items[0][6], kap, qx)
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
