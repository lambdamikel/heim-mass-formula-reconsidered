"""
Anregerfunktion consistency check for k=2 baryon resonances.

Same logic as resonance_consistency.py (which did k=1 mesons):
  1. Re-run the config-matching for all 145 baryon states.
  2. Group by matched (P, Q_best, q_x) sector.
  3. For each group with ≥ 2 states, compute implied w from
     J0032 eq. 11 and check whether (N_published, f_implied = w/W_0 - 1)
     pairs lie on an Anregerkurve f(N) = a·N/(N+1) + b·N.

Strong consistency (max |Δf| ≪ 1) → matched configs are likely Heim's
actual decompositions, not accidental (M, K_B) hits.  Weak
consistency → matches may be spurious.
"""

from __future__ import annotations

import re
from collections import defaultdict
from math import exp
from pathlib import Path

import numpy as np

import formulae as fm
from g_tables import (TABLE_V_a_BARYONS_K2, TABLE_V_b_BARYONS_K2,
                      TABLE_V_c_BARYONS_K2_SIGMA)
from resonance_wscan_baryons import (expand_to_states, match_sector_k2,
                                      scan_all)


CACHED_LOG = Path(__file__).parent / "baryon_reproduction_results.txt"
LINE_RE = re.compile(
    r"^\s+(?P<label>\S+)\s+(?P<P>\d+)\s+(?P<qx>[+-]\d+)\s+"
    r"(?P<M>[\d.]+)\s+(?P<KB>-?\d+)\s+(?P<Q>\d+)\s+"
    r"\((?P<n>-?\d+),\s*(?P<m>-?\d+),\s*(?P<p>-?\d+),\s*(?P<sig>-?\d+)\)"
)


def load_results_from_log(path=CACHED_LOG):
    """Parse the per-entry table emitted by resonance_wscan_baryons.py
    into a results dict {label → match info}."""
    out = {}
    with open(path) as fh:
        for line in fh:
            m = LINE_RE.match(line)
            if not m:
                continue
            label = m.group("label")
            out[label] = {
                "P": int(m.group("P")),
                "qx": int(m.group("qx")),
                "M_t": float(m.group("M")),
                "KB_t": int(m.group("KB")),
                "Q": int(m.group("Q")),
                "nmps": (int(m.group("n")), int(m.group("m")),
                         int(m.group("p")), int(m.group("sig"))),
            }
    return out


def implied_w_k2(nmps, I, N_const, k=2):
    """J0032 eq. 11 lhs at k=2.  w_3 = geometric mean of bracket."""
    n_, m_, p_, sig_ = nmps
    Q_n, Q_m, Q_p, Q_sig = I
    a1 = N_const[0]
    a2 = 1.5 * N_const[1]
    a3 = 0.5 * N_const[2]
    beta = (2 * k - 1) / (3.0 * Q_sig) if Q_sig != 0 else 1.0
    K_sig = sig_ + 1 + Q_sig
    w3_lo = exp(-beta * K_sig)
    w3_hi = exp(-beta * max(K_sig - 1, 0))
    w3 = (w3_lo * w3_hi) ** 0.5
    return ((n_ + Q_n) ** 3 * a1
            + (m_ + Q_m) ** 2 * a2
            + (p_ + Q_p) * a3
            + w3)


def fit_anregung(N_arr, f_arr):
    A = np.column_stack([N_arr / (N_arr + 1.0), N_arr])
    coefs, _, _, _ = np.linalg.lstsq(A, f_arr, rcond=None)
    a, b = coefs
    f_pred = a * N_arr / (N_arr + 1.0) + b * N_arr
    return a, b, f_pred


def collect_published_N(states_with_pub_N):
    """Map state-label → published N (excitation index)."""
    out = {}
    for tbl in (TABLE_V_a_BARYONS_K2, TABLE_V_b_BARYONS_K2,
                TABLE_V_c_BARYONS_K2_SIGMA):
        for r in tbl:
            if isinstance(r.N, tuple):
                # Tuples are (neutral, charged) or (-, 0, +)
                ncols = len(r.N)
                if ncols == 2:
                    out[f"{r.symbol}⁰"] = r.N[0]
                    out[f"{r.symbol}±"] = r.N[1]
                elif ncols == 3:
                    out[f"{r.symbol}⁻"] = r.N[0]
                    out[f"{r.symbol}⁰"] = r.N[1]
                    out[f"{r.symbol}⁺"] = r.N[2]
            else:
                out[r.symbol] = r.N
    return out


def main():
    import sys
    print("=" * 92)
    print(" Anregerfunktion consistency check for k=2 baryons")
    print("=" * 92)
    print()

    use_cache = "--rescan" not in sys.argv and CACHED_LOG.exists()
    if use_cache:
        print(f"Step 1: loading cached matches from {CACHED_LOG.name} ...")
        results_cached = load_results_from_log()
        print(f"  loaded {len(results_cached)} matches")
    else:
        print("Step 1: re-running config matching (≈ 7 min)...")
        all_states = (expand_to_states(TABLE_V_a_BARYONS_K2)
                       + expand_to_states(TABLE_V_b_BARYONS_K2)
                       + expand_to_states(TABLE_V_c_BARYONS_K2_SIGMA))
        results = scan_all(all_states)
        results_cached = {}
        for label, (mtch, score, Q_b, M_t, KB_t) in results.items():
            if mtch is None:
                continue
            results_cached[label] = {
                "P": next(s[1] for s in all_states if s[0] == label),
                "qx": next(s[2] for s in all_states if s[0] == label),
                "M_t": M_t, "KB_t": KB_t, "Q": Q_b,
                "nmps": mtch["nmps"],
            }

    all_states = (expand_to_states(TABLE_V_a_BARYONS_K2)
                   + expand_to_states(TABLE_V_b_BARYONS_K2)
                   + expand_to_states(TABLE_V_c_BARYONS_K2_SIGMA))
    pub_N = collect_published_N(all_states)

    print()
    print("Step 2: grouping by (P, Q_best, q_x) sector...")

    # Build {(P, Q, qx) → list of (label, N, nmps, M_t, KB_t)}
    sector_data = defaultdict(list)

    for label, info in results_cached.items():
        N_idx = pub_N.get(label)
        if N_idx is None:
            continue
        sector_data[(info["P"], info["Q"], info["qx"])].append(
            (N_idx, label, info["nmps"], info["M_t"], info["KB_t"]))

    I = fm.calc_Q(2)
    Nconst_q0 = fm.calc_N(2, 0, I)
    Nconst_q1 = fm.calc_N(2, 1, I)

    print()
    print(f"  {'Sector':<26} {'#':>3}  {'κ':>3}  {'W_0':>10}  "
          f"{'a':>10}  {'b':>10}  {'max |Δf|':>10}")
    print("  " + "-" * 78)

    overall_fits = {}
    for key, entries in sorted(sector_data.items()):
        if len(entries) < 2:
            continue
        P_, Q_, qx = key
        Nconst = Nconst_q0 if qx == 0 else Nconst_q1
        entries.sort()
        N_np = np.array([e[0] for e in entries], dtype=float)
        w_np = np.array([implied_w_k2(e[2], I, Nconst) for e in entries])

        best = None
        for kap in (0, 1):
            W0 = fm.calc_W(1, 2, P_, Q_, kap, qx, I)
            if W0 <= 0 or not np.isfinite(W0):
                continue
            f_arr = w_np / W0 - 1.0
            try:
                a, b, f_pred = fit_anregung(N_np, f_arr)
            except Exception:
                continue
            max_r = float(np.max(np.abs(f_arr - f_pred)))
            if best is None or max_r < best[0]:
                best = (max_r, kap, W0, a, b)
        if best is None:
            print(f"  P={P_} Q={Q_:>2} q={qx:+d:<2}  {len(entries):>3}  "
                  f"(no valid W_0)")
            continue
        max_r, kap, W0, a, b = best
        overall_fits[key] = best
        label = f"P={P_} Q={Q_} q={qx:+d}"
        print(f"  {label:<26} {len(entries):>3}  {kap:>3}  "
              f"{W0:>10.3g}  {a:>+10.3f}  {b:>+10.4f}  {max_r:>10.3e}")

    print()
    print("=" * 92)
    print("Per-sector detail (groups with ≥ 3 entries — most informative):")
    print("=" * 92)
    for key, entries in sorted(sector_data.items()):
        if len(entries) < 3 or key not in overall_fits:
            continue
        P_, Q_, qx = key
        max_r, kap, W0, a, b = overall_fits[key]
        Nconst = Nconst_q0 if qx == 0 else Nconst_q1
        entries.sort()
        print()
        print(f"  Sector (P={P_}, Q={Q_}, q={qx:+d})  κ={kap}  "
              f"W_0={W0:.4g}")
        print(f"  fitted f(N) = {a:+.4f}·N/(N+1) {b:+.4f}·N")
        print(f"    {'N':>5}  {'label':<14} {'(n,m,p,σ)':<22} "
              f"{'w':>11}  {'f_imp':>10}  {'f_fit':>10}  {'Δf':>10}")
        for N_idx, label, nmps, M_t, KB_t in entries:
            w = implied_w_k2(nmps, I, Nconst)
            f_imp = w / W0 - 1.0
            f_fit = a * N_idx / (N_idx + 1.0) + b * N_idx
            print(f"    {N_idx:>5}  {label:<14} {str(nmps):<22} "
                  f"{w:>11.4g}  {f_imp:>+10.3g}  {f_fit:>+10.3g}  "
                  f"{f_imp - f_fit:>+10.3e}")


if __name__ == "__main__":
    main()
