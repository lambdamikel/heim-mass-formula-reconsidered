"""
G-Tabellen V_a-V_c reproduction (baryonic resonances at k=2).

Same J0032 exhaustion procedure as resonance_wscan.py, but with k=2.
Two important differences from k=1:

  1. Q_i are much larger:  (Q_n, Q_m, Q_p, Q_σ) = (24, 31, 34, 15) for k=2
     vs (3, 3, 2, 1) for k=1.  This means the K_x indices in the
     exhaustion can produce *negative* (n, m, p, σ) — and Heim's
     published Tabelle I shows that ground-state baryons do use
     negative quantum numbers (e.g. Λ has σ = -11; Σ⁰ has m = -7,
     p = -14; Ω⁻ has σ = -15).  K_x ≥ 1 in our enumeration.

  2. N_3 = e (= 2.718...) for k=2 q=0, vs 2 for k=1.  This affects
     K_B = N_3·(p+Q_p)/2 - Q_σ - σ — meaning K_B is no longer integer
     in general, and reachable K_B values are dense but not aligned
     with arbitrary published integers.

Starts with the simplest sub-case: Λ* singlets (P=0, q=0), 16 entries.
After that, scales to N*, Ξ* doublets (P=1), Σ* triplets (P=2), Δ* (P=3).

Baryon spin J is half-integer, so Q = 2·J is odd. We scan Q ∈ {1,3,5,7,9,11}
per entry and pick the best combined (mass + K_B-penalty) score.
"""

from __future__ import annotations

from collections import defaultdict
from math import fabs

import numpy as np

import formulae as fm
from constants import (KG_TO_MEV, alpha_minus, alpha_plus, eta, mass_element,
                       theta)
from g_tables import (TABLE_V_a_BARYONS_K2, TABLE_V_b_BARYONS_K2,
                      TABLE_V_c_BARYONS_K2_SIGMA)


def match_sector_k2(P, Q, q_x, targets,
                     K_n_max=60, K_m_max=70, K_p_max=70, K_sig_max=40):
    """Stream-enumerate reachable (K_n,K_m,K_p,K_σ) configs at k=2.
    Match each target (id, M_t, KB_t) by smallest (dKB, dM) tuple."""
    q = fabs(q_x)
    # Canonical η_{1,0} ≈ 0.990, same as calc_mass uses for α_+, α_-.
    # The earlier `eta(2, q)` call here was a bug — it gave η ≈ 0.881 and
    # α_+ ≈ 0.198 (vs canonical α_+ ≈ 0.018), making the bracket size
    # roughly 10× too small.  The matched (n, m, p, σ) under that bug
    # were self-consistent in mass + K_B but NOT Heim's actual
    # decompositions.
    eta00 = eta(1, 0)
    th = theta(eta00)
    a_p = alpha_plus(eta00, th)
    a_m = alpha_minus(eta00, th)
    mu = mass_element()
    mu_ap_MeV = mu * a_p * KG_TO_MEV
    qterm_MeV = 4 * q * mu * a_m * KG_TO_MEV

    I = fm.calc_Q(2)
    N = fm.calc_N(2, q, I)
    a1 = N[0]
    a2 = 1.5 * N[1]
    a3 = 0.5 * N[2]
    Q_n, Q_m, Q_p, Q_sig = I

    S = ((I[0] * (I[0] + 1))**2 * N[0]
         + I[1] * (2*I[1]**2 + 3*I[1] + 1) * N[1]
         + I[2] * (I[2] + 1) * N[2]
         + 4 * I[3])
    PHI = P * (-1)**(P+Q) * (P+Q) * N[4] + Q * (P+1) * N[5]

    n_targets = len(targets)
    target_M = np.array([t[1] for t in targets], dtype=float)
    target_KB = np.array([t[2] for t in targets], dtype=float)

    best_score = np.full(n_targets, 1e18, dtype=float)
    best = [None] * n_targets

    # Pre-compute K_sig array contributions (vectorised over K_sig)
    K_sig_arr = np.arange(1, K_sig_max + 1)
    sig_arr = K_sig_arr - 1 - Q_sig
    sig_contrib = 4.0 * sig_arr           # contributes to K_mass

    for K_n in range(1, K_n_max + 1):
        n_ = K_n - 1 - Q_n
        K_piece_n = (n_ * (n_ + 1))**2 * N[0]
        F_piece_n = 2*n_*I[0]*(1 + 3*(n_+I[0]+n_*I[0]) + 2*(n_**2 + I[0]**2)) * N[0]
        w1_max = a1 * (3 * K_n * K_n - 3 * K_n + 1)
        K_m_lim = min(K_m_max, int((w1_max / a2) ** 0.5) + 2)
        for K_m in range(1, K_m_lim + 1):
            m_ = K_m - 1 - Q_m
            if (K_m - 1) ** 2 * a2 >= w1_max:
                continue
            K_piece_m = m_ * (2*m_**2 + 3*m_ + 1) * N[1]
            F_piece_m = 6*m_*I[1]*(1+m_+I[1]) * N[1]
            w2_max_in_Km = a2 * (2 * K_m - 1)
            w2_max_from_w1 = w1_max - (K_m - 1) ** 2 * a2
            w2_max = min(w2_max_in_Km, w2_max_from_w1)
            K_p_lim = min(K_p_max, int(w2_max / a3) + 2)
            for K_p in range(1, K_p_lim + 1):
                p_ = K_p - 1 - Q_p
                if (K_p - 1) * a3 >= w2_max:
                    continue
                K_piece_p = p_ * (p_ + 1) * N[2]
                F_piece_p = 2*p_*I[2] * N[2]
                L_sigma = 0.5 * N[2] * (p_ + I[2]) - I[3]
                bracket_no_sig = (K_piece_n + K_piece_m + K_piece_p + S
                                   + F_piece_n + F_piece_m + F_piece_p + PHI)
                bracket_arr = bracket_no_sig + sig_contrib    # (K_sig_max,)
                M_arr = mu_ap_MeV * bracket_arr + qterm_MeV
                KB_arr = L_sigma - sig_arr
                # Vectorise over (targets × K_sig): shape (T, K_sig_max)
                dM_grid = np.abs(M_arr[None, :] - target_M[:, None])
                dKB_grid = np.abs(KB_arr[None, :] - target_KB[:, None])
                score_grid = dM_grid + 100.0 * np.maximum(0.0, dKB_grid - 0.5)
                argmin = np.argmin(score_grid, axis=1)
                best_score_this = score_grid[np.arange(n_targets), argmin]
                better = best_score_this < best_score
                for ti in np.nonzero(better)[0]:
                    s_idx = int(argmin[ti])
                    K_sig = int(K_sig_arr[s_idx])
                    sig_ = int(sig_arr[s_idx])
                    M_MeV = float(M_arr[s_idx])
                    K_B = float(KB_arr[s_idx])
                    best_score[ti] = best_score_this[ti]
                    best[ti] = {
                        "K": (K_n, K_m, K_p, K_sig),
                        "nmps": (n_, m_, p_, sig_),
                        "M_MeV": M_MeV,
                        "K_B": K_B,
                        "Q": Q,
                    }
    # Convert back to dict keyed by target id
    return {targets[i][0]: best[i] for i in range(n_targets)}


def expand_to_states(entries):
    """Expand each entry (singlet, doublet, triplet) into (label, P, q_x,
    M_target, KB_target) tuples."""
    out = []
    for r in entries:
        sym = r.symbol
        P = r.P
        if isinstance(r.mass_MeV, tuple):
            ncols = len(r.mass_MeV)
            if ncols == 2:
                q_xs = [0, 1]
                labels = [f"{sym}⁰", f"{sym}±"]
            elif ncols == 3:
                q_xs = [-1, 0, +1]
                labels = [f"{sym}⁻", f"{sym}⁰", f"{sym}⁺"]
            else:
                continue
            for i, qx in enumerate(q_xs):
                out.append((labels[i], P, qx, r.mass_MeV[i], r.K_B[i]))
        else:
            out.append((sym, P, 0, r.mass_MeV, r.K_B))
    return out


def scan_all_candidates(states, K_n_max=50, K_m_max=70, K_p_max=100,
                          K_sig_max=50, W0_max=1e8):
    """Like scan_all, but returns ALL Q-candidates per state, not just
    the best.  Returned dict maps label → list of dicts (one per Q)."""
    Q_candidates = [1, 3, 5, 7, 9]
    I = fm.calc_Q(2)
    by_sector = defaultdict(list)
    for s in states:
        label, P, qx, M_t, KB_t = s
        by_sector[(P, qx)].append((label, M_t, KB_t))

    results = defaultdict(list)
    for (P, qx), tgts in sorted(by_sector.items()):
        for Q in Q_candidates:
            W0_min_kap = 0
            valids = [fm.calc_W(1, 2, P, Q, kap, qx, I) for kap in (0, 1)]
            valids = [w for w in valids if w > 0]
            if not valids:
                continue
            W0_min_kap = min(valids)
            if W0_min_kap > W0_max:
                continue
            targets = [(label, M_t, KB_t) for (label, M_t, KB_t) in tgts]
            print(f"  P={P} q={qx:+d} Q={Q}: {len(targets)} targets "
                  f"(W_0 = {W0_min_kap:.2e})", flush=True)
            m = match_sector_k2(P, Q, qx, targets, K_n_max=K_n_max,
                                K_m_max=K_m_max, K_p_max=K_p_max,
                                K_sig_max=K_sig_max)
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


def scan_all(states, K_n_max=50, K_m_max=70, K_p_max=100, K_sig_max=50,
              W0_max=1e8):
    """For each state (label, P, q_x, M_t, KB_t), scan Q ∈ {1,3,5,7,9}
    and find best match.  Skip (P, Q, κ, q) sectors where W_0 (eq. B22)
    is > W0_max — those produce f_implied ≈ −1 trivially and make
    the per-sector Anregerkurve check degenerate."""
    # Q = 2·J for baryons; J ∈ {1/2, 3/2, ..., 9/2} covers all
    # well-identified PDG baryon resonances.  Q = 11 (J = 11/2) excluded.
    Q_candidates = [1, 3, 5, 7, 9]

    I = fm.calc_Q(2)
    by_sector = defaultdict(list)
    for s in states:
        label, P, qx, M_t, KB_t = s
        by_sector[(P, qx)].append((label, M_t, KB_t))

    results = {}   # label → (Q_best, dict)
    for (P, qx), tgts in sorted(by_sector.items()):
        for Q in Q_candidates:
            # Reject sectors where W_0 diverges (= calc_W is huge for some
            # (P, Q, κ, q) at k=2 — those entries are ranking degeneracies).
            W0_min_kap = min(
                fm.calc_W(1, 2, P, Q, kap, qx, I) for kap in (0, 1)
                if fm.calc_W(1, 2, P, Q, kap, qx, I) > 0
            ) if any(fm.calc_W(1, 2, P, Q, kap, qx, I) > 0
                     for kap in (0, 1)) else 0
            if W0_min_kap > W0_max or W0_min_kap == 0:
                print(f"  Sector P={P} q={qx:+d} Q={Q}: W_0 = "
                      f"{W0_min_kap:.2e} (>{W0_max:.0e} or 0) — skipped",
                      flush=True)
                continue
            targets = [(label, M_t, KB_t) for (label, M_t, KB_t) in tgts]
            print(f"  Sector P={P} q={qx:+d} Q={Q}: {len(targets)} targets "
                  f"(W_0 = {W0_min_kap:.2e})", flush=True)
            m = match_sector_k2(P, Q, qx, targets, K_n_max=K_n_max,
                                K_m_max=K_m_max, K_p_max=K_p_max,
                                K_sig_max=K_sig_max)
            for label, mtch in m.items():
                if mtch is None:
                    continue
                M_t, KB_t = next(
                    (M, K) for (lbl, M, K) in tgts if lbl == label)
                dM = abs(mtch["M_MeV"] - M_t)
                dKB = abs(mtch["K_B"] - KB_t)
                score = dM + 100 * max(0, dKB - 0.5)
                if (label not in results
                        or results[label][1] > score):
                    results[label] = (mtch, score, Q, M_t, KB_t)
    return results


def main():
    print("=" * 100)
    print(" G-Tabellen V_a-V_c reproduction (k=2) — all baryonic resonances")
    print("=" * 100)
    print()

    # All entries from V_a, V_b, V_c
    all_states = (expand_to_states(TABLE_V_a_BARYONS_K2)
                   + expand_to_states(TABLE_V_b_BARYONS_K2)
                   + expand_to_states(TABLE_V_c_BARYONS_K2_SIGMA))
    # Group by family for reporting
    families = defaultdict(list)
    for s in all_states:
        label = s[0]
        if label.startswith("N"):
            fam = "N*"
        elif label.startswith("Λ"):
            fam = "Λ*"
        elif label.startswith("Ξ"):
            fam = "Ξ*"
        elif label.startswith("Δ"):
            fam = "Δ*"
        elif label.startswith("Σ"):
            fam = "Σ*"
        else:
            fam = "?"
        families[fam].append(s)
    for fam, fs in sorted(families.items()):
        print(f"  {fam}: {len(fs)} states")
    print(f"  TOTAL: {len(all_states)} baryonic resonance states")
    print()

    results = scan_all(all_states)

    # Report per family
    for fam in ("Λ*", "N*", "Ξ*", "Δ*", "Σ*"):
        fs = families[fam]
        print()
        print(f"--- {fam} family ({len(fs)} states) ---")
        print(f"  {'Symbol':<12} {'P':>2} {'q_x':>4} {'M_heim':>10} {'K_B':>6}  "
              f"{'Q':>3}  {'(n,m,p,σ)':<22}  {'Δ_M':>9}  {'Δ_KB':>6}")
        n_kb05 = 0
        n_m05 = 0
        n_m2 = 0
        for (label, P, qx, M_t, KB_t) in fs:
            if label not in results:
                print(f"  {label:<12} {P:>2} {qx:>+4d} {M_t:>10.4f} {KB_t:>6}  (none)")
                continue
            mtch, _, Q_b, _, _ = results[label]
            dM = mtch["M_MeV"] - M_t
            dKB = mtch["K_B"] - KB_t
            if abs(dKB) < 0.5:
                n_kb05 += 1
            if abs(dM) < 0.5:
                n_m05 += 1
            if abs(dM) < 2.0:
                n_m2 += 1
            print(f"  {label:<12} {P:>2} {qx:>+4d} {M_t:>10.4f} {KB_t:>6}  "
                  f"{Q_b:>3}  {str(mtch['nmps']):<22}  "
                  f"{dM:>+9.4f}  {dKB:>+6.2f}")
        print(f"  Summary {fam}: K_B≈exact {n_kb05}/{len(fs)}, "
              f"Δ_M<0.5 MeV {n_m05}/{len(fs)}, Δ_M<2 MeV {n_m2}/{len(fs)}")


if __name__ == "__main__":
    main()
