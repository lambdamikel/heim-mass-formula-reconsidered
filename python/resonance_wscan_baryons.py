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
    eta00 = eta(2, q)            # k=2 has its own η
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

    best = {tid: None for tid, _, _ in targets}
    best_score = {tid: (1e18,) for tid, _, _ in targets}

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
                for K_sig in range(1, K_sig_max + 1):
                    sig_ = K_sig - 1 - Q_sig
                    bracket = bracket_no_sig + 4 * sig_
                    M_MeV = mu_ap_MeV * bracket + qterm_MeV
                    K_B = L_sigma - sig_
                    for tid, M_t, KB_t in targets:
                        dM = abs(M_MeV - M_t)
                        dKB = abs(K_B - KB_t)
                        # Combined score: prefer small dM, penalize dKB > 1
                        score = (dM + 100 * max(0, dKB - 0.5),)
                        if score < best_score[tid]:
                            best_score[tid] = score
                            best[tid] = {
                                "K": (K_n, K_m, K_p, K_sig),
                                "nmps": (n_, m_, p_, sig_),
                                "M_MeV": M_MeV,
                                "K_B": K_B,
                                "Q": Q,
                            }
    return best


def main():
    print("=" * 92)
    print(" G-Tabellen V_a-V_c reproduction (k=2) — Λ* singlets first pass")
    print("=" * 92)
    print()

    # All Λ* entries (P=0, isospin singlet, q=0).  16 entries total
    # (7 in V_a + 9 in V_b).
    lambda_entries = [
        r for r in TABLE_V_a_BARYONS_K2 if r.symbol.startswith("Λ")
    ] + [
        r for r in TABLE_V_b_BARYONS_K2 if r.symbol.startswith("Λ")
    ]
    print(f"  {len(lambda_entries)} Λ* entries (P=0, q=0)")

    # Per-entry: try Q ∈ {1, 3, 5, 7, 9, 11} (J ∈ {1/2, 3/2, 5/2, 7/2, 9/2, 11/2})
    Q_candidates = [1, 3, 5, 7, 9, 11]
    P_, q_x = 0, 0
    print()

    all_results = []
    for Q_try in Q_candidates:
        print(f"  Scanning Q={Q_try}...", flush=True)
        targets = [(r.symbol, r.mass_MeV, r.K_B) for r in lambda_entries]
        matches = match_sector_k2(P_, Q_try, q_x, targets,
                                   K_n_max=50, K_m_max=70,
                                   K_p_max=100, K_sig_max=50)
        for sym, m in matches.items():
            if m is None:
                continue
            r = next(rr for rr in lambda_entries if rr.symbol == sym)
            all_results.append((sym, r, m))

    # For each symbol, pick best Q match (combined score)
    best_per_sym = {}
    for sym, r, m in all_results:
        dM = abs(m["M_MeV"] - r.mass_MeV)
        dKB = abs(m["K_B"] - r.K_B)
        score = dM + 100 * max(0, dKB - 0.5)
        if sym not in best_per_sym or score < best_per_sym[sym][3]:
            best_per_sym[sym] = (r, m, m["Q"], score)

    print()
    print(f"  {'Symbol':<12} {'M_heim':>10} {'N':>5} {'K_B':>5}  "
          f"{'best Q':>6}  {'(n,m,p,σ)':<22}  {'Δ_M':>9}  {'Δ_KB':>5}")
    print("  " + "-" * 90)
    n_kb_exact = 0
    n_mass_05 = 0
    n_mass_2 = 0
    for r in lambda_entries:
        if r.symbol not in best_per_sym:
            print(f"  {r.symbol:<12} {r.mass_MeV:>10.4f} {r.N!s:>5} {r.K_B!s:>5}  (no match)")
            continue
        _, m, Q_b, _ = best_per_sym[r.symbol]
        dM = m["M_MeV"] - r.mass_MeV
        dKB = round(m["K_B"]) - r.K_B
        if dKB == 0:
            n_kb_exact += 1
        if abs(dM) < 0.5:
            n_mass_05 += 1
        if abs(dM) < 2.0:
            n_mass_2 += 1
        print(f"  {r.symbol:<12} {r.mass_MeV:>10.4f} {r.N!s:>5} {r.K_B!s:>5}  "
              f"{Q_b:>6}  {str(m['nmps']):<22}  {dM:>+9.4f}  {dKB:>+5d}")
    print()
    print(f"  K_B exact: {n_kb_exact}/{len(lambda_entries)}")
    print(f"  Mass within 0.5 MeV: {n_mass_05}/{len(lambda_entries)}")
    print(f"  Mass within 2.0 MeV: {n_mass_2}/{len(lambda_entries)}")


if __name__ == "__main__":
    main()
