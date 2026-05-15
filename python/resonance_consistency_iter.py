"""
Iterative Q-disambiguation via per-sector Anregerkurve consistency.

Approach:
  1. Run scan_all_candidates() to get ALL Q-candidates per state
     (one per Q ∈ {1, 3, 5, 7, 9} where W_0 is non-degenerate).
  2. Initial Q assignment: best (dM, dKB) score per state.
  3. Per (P, Q, qx) sector, fit Anregerkurve f(N) = a·N/(N+1) + b·N
     to the assigned states.
  4. For each state with > 1 candidate Q: re-rank candidates by
     score + λ·|f_imp − f_fit_at_N| where the second term measures
     deviation from the fitted sector curve.
  5. Iterate 3-4 until assignments stabilise.
"""

from __future__ import annotations

import pickle
from collections import defaultdict
from math import exp
from pathlib import Path

import numpy as np

import formulae as fm
from g_tables import (TABLE_V_a_BARYONS_K2, TABLE_V_b_BARYONS_K2,
                      TABLE_V_c_BARYONS_K2_SIGMA)
from resonance_wscan_baryons import expand_to_states, scan_all_candidates
from resonance_consistency_baryons import (collect_published_N,
                                            fit_anregung, implied_w_k2)

CACHE = Path(__file__).parent / "baryon_candidates_cache.pkl"


def get_W0(P, Q, qx, I):
    """Min over κ of calc_W (positive values only).  Returns None if both
    κ give non-positive."""
    vals = [fm.calc_W(1, 2, P, Q, kap, qx, I) for kap in (0, 1)]
    vals = [(kap, w) for kap, w in enumerate(vals) if w > 0]
    if not vals:
        return None
    return min(vals, key=lambda kv: kv[1])


def main():
    import sys
    print("=" * 92)
    print(" Iterative Q-disambiguation via Anregerkurve consistency")
    print("=" * 92)
    print()

    all_states = (expand_to_states(TABLE_V_a_BARYONS_K2)
                   + expand_to_states(TABLE_V_b_BARYONS_K2)
                   + expand_to_states(TABLE_V_c_BARYONS_K2_SIGMA))
    pub_N = collect_published_N(all_states)
    I = fm.calc_Q(2)
    Nconst_q0 = fm.calc_N(2, 0, I)
    Nconst_q1 = fm.calc_N(2, 1, I)

    # Step 1: get all Q-candidates per state (cached)
    if CACHE.exists() and "--rescan" not in sys.argv:
        print(f"Loading cached candidates from {CACHE.name} ...")
        with open(CACHE, "rb") as f:
            cands = pickle.load(f)
    else:
        print("Running full scan_all_candidates (≈ 5 min) ...")
        cands = scan_all_candidates(all_states)
        with open(CACHE, "wb") as f:
            pickle.dump(cands, f)
        print(f"  saved to {CACHE.name}")

    print(f"  {len(cands)} states with at least one candidate")
    multi_q_count = sum(1 for v in cands.values() if len(v) > 1)
    print(f"  {multi_q_count} states with > 1 Q candidate (ambiguous)")
    single_q_count = len(cands) - multi_q_count
    print(f"  {single_q_count} states with single Q candidate (locked)")

    # Step 2: initial assignment — best (dM, dKB) per state
    assignment = {}     # label → candidate dict
    for label, candidate_list in cands.items():
        best = min(candidate_list, key=lambda c: c["score"])
        assignment[label] = best

    def sector_anregung_fits():
        sectors = defaultdict(list)
        for label, c in assignment.items():
            N_idx = pub_N.get(label)
            if N_idx is None:
                continue
            sectors[(c["P"], c["Q"], c["qx"])].append((N_idx, label, c))
        fits = {}
        for key, entries in sectors.items():
            if len(entries) < 2:
                continue
            P_, Q_, qx = key
            Nconst = Nconst_q0 if qx == 0 else Nconst_q1
            N_np = np.array([e[0] for e in entries], dtype=float)
            w_np = np.array([implied_w_k2(e[2]["nmps"], I, Nconst)
                              for e in entries])
            # Try both κ and pick the one with smaller max-residual.
            best = None
            for kap in (0, 1):
                W0 = fm.calc_W(1, 2, P_, Q_, kap, qx, I)
                if W0 <= 0 or not np.isfinite(W0):
                    continue
                f_arr = w_np / W0 - 1.0
                try:
                    a, b, _ = fit_anregung(N_np, f_arr)
                except Exception:
                    continue
                max_r = float(np.max(np.abs(
                    f_arr - (a * N_np / (N_np + 1.0) + b * N_np))))
                if best is None or max_r < best["max_resid"]:
                    best = {"a": a, "b": b, "W0": W0, "kap": kap,
                            "n": len(entries), "max_resid": max_r}
            if best is None:
                continue
            fits[key] = best
        return fits

    def total_inconsistency(fits):
        total = 0.0
        for label, c in assignment.items():
            key = (c["P"], c["Q"], c["qx"])
            if key not in fits:
                continue
            N_idx = pub_N.get(label)
            if N_idx is None:
                continue
            Nconst = Nconst_q0 if c["qx"] == 0 else Nconst_q1
            w = implied_w_k2(c["nmps"], I, Nconst)
            f_imp = w / fits[key]["W0"] - 1.0
            a, b = fits[key]["a"], fits[key]["b"]
            f_fit = a * N_idx / (N_idx + 1.0) + b * N_idx
            total += abs(f_imp - f_fit)
        return total

    LAMBDA = 200.0     # weight of Anregerkurve consistency in re-ranking
    print()
    print("Step 3-4: iterating assignment until stable...")
    for iteration in range(10):
        fits = sector_anregung_fits()
        incons = total_inconsistency(fits)
        print(f"  Iter {iteration}: {len(fits)} sectors fitted, "
              f"total inconsistency = {incons:.4f}")
        # Re-evaluate Q assignment for ambiguous states
        changed = 0
        for label, candidate_list in cands.items():
            if len(candidate_list) <= 1:
                continue
            N_idx = pub_N.get(label)
            if N_idx is None:
                continue
            best_c = None
            best_score = 1e18
            for c in candidate_list:
                Nconst = Nconst_q0 if c["qx"] == 0 else Nconst_q1
                key = (c["P"], c["Q"], c["qx"])
                if key in fits:
                    w = implied_w_k2(c["nmps"], I, Nconst)
                    f_imp = w / fits[key]["W0"] - 1.0
                    a, b = fits[key]["a"], fits[key]["b"]
                    f_fit = a * N_idx / (N_idx + 1.0) + b * N_idx
                    df = abs(f_imp - f_fit)
                else:
                    df = 1.0    # large penalty for "lone state" sectors
                combined = c["score"] + LAMBDA * df
                if combined < best_score:
                    best_score = combined
                    best_c = c
            if best_c is None or best_c["Q"] == assignment[label]["Q"]:
                continue
            assignment[label] = best_c
            changed += 1
        print(f"           changed Q for {changed} states")
        if changed == 0:
            print("           converged.")
            break

    # Final report
    fits = sector_anregung_fits()
    print()
    print("=" * 92)
    print(f"Final per-sector consistency ({len(fits)} sectors):")
    print("=" * 92)
    print(f"  {'Sector':<22} {'#':>3}  {'κ':>3}  {'W_0':>10}  "
          f"{'a':>10}  {'b':>10}  {'max |Δf|':>10}")
    print("  " + "-" * 78)
    for key in sorted(fits.keys()):
        f = fits[key]
        P_, Q_, qx = key
        label = f"P={P_} Q={Q_} q={qx:+d}"
        print(f"  {label:<22} {f['n']:>3}  {f['kap']:>3}  "
              f"{f['W0']:>10.3g}  {f['a']:>+10.4f}  {f['b']:>+10.4f}  "
              f"{f['max_resid']:>10.3e}")
    print()

    # Q distribution
    from collections import Counter
    q_dist = Counter(c["Q"] for c in assignment.values())
    print(f"  Final Q distribution: {dict(sorted(q_dist.items()))}")

    # Save final assignment as a text table
    print()
    print("Final per-state assignment (sorted by family):")
    fams = defaultdict(list)
    for s in all_states:
        label, P, qx, M_t, KB_t = s
        if label not in assignment:
            continue
        sym0 = label.lstrip().replace("⁻", "").replace("⁰", "").replace("⁺", "").replace("±", "")
        if "Λ" in sym0:
            fam = "Λ*"
        elif "N(" in sym0:
            fam = "N*"
        elif "Ξ" in sym0:
            fam = "Ξ*"
        elif "Δ" in sym0:
            fam = "Δ*"
        elif "Σ" in sym0:
            fam = "Σ*"
        else:
            fam = "?"
        fams[fam].append((label, P, qx, M_t, KB_t))

    n_kb_exact = 0
    n_m_05 = 0
    n_m_2 = 0
    for fam in ("Λ*", "N*", "Ξ*", "Δ*", "Σ*"):
        items = fams[fam]
        print()
        print(f"  --- {fam} ({len(items)}) ---")
        print(f"  {'symbol':<14} {'P':>2} {'qx':>3}  {'M_t':>10}  {'K_B':>5}  "
              f"{'Q':>3}  {'(n,m,p,σ)':<22}  {'Δ_M':>9}  {'Δ_KB':>6}")
        for label, P, qx, M_t, KB_t in items:
            c = assignment[label]
            dM = c["M_MeV"] - M_t
            dKB = c["K_B"] - KB_t
            if abs(dKB) < 0.5:
                n_kb_exact += 1
            if abs(dM) < 0.5:
                n_m_05 += 1
            if abs(dM) < 2.0:
                n_m_2 += 1
            print(f"  {label:<14} {P:>2} {qx:>+3d}  {M_t:>10.4f}  {KB_t!s:>5}  "
                  f"{c['Q']:>3}  {str(c['nmps']):<22}  "
                  f"{dM:>+9.4f}  {dKB:>+6.2f}")

    print()
    print(f"OVERALL: K_B≈exact {n_kb_exact}/{len(assignment)}, "
          f"Δ_M<0.5 MeV {n_m_05}/{len(assignment)}, "
          f"Δ_M<2 MeV {n_m_2}/{len(assignment)}")


if __name__ == "__main__":
    main()
