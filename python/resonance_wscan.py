"""
G-Tabelle IV reproduction via streaming reachability enumeration.

Per sector (P, Q, κ, q), enumerate (K_n, K_m, K_p, K_σ) reachable by some
w under the J0032 exhaustion ordering, computing each config's (mass, K_B)
on the fly and matching against the relevant Tabelle IV targets without
materialising the full config list.
"""

from __future__ import annotations

from collections import defaultdict
from math import fabs

import formulae as fm
from constants import (KG_TO_MEV, alpha_minus, alpha_plus, eta, mass_element,
                       theta)
from g_tables import TABLE_IV_MESONS_K1


def match_sector(k, P, Q, kap, q_x, targets, K_n_max=40, K_sig_max=40):
    """Enumerate reachable configs for a sector; for each target
    (idx, M_target, KB_target), keep the best (smallest dKB, then dM) match.

    targets: list of (target_id, M_target, KB_target)
    Returns: dict {target_id: best_match_dict_or_None}
    """
    q = fabs(q_x)
    eta00 = eta(1, 0)
    th = theta(eta00)
    a_p = alpha_plus(eta00, th)
    a_m = alpha_minus(eta00, th)
    mu = mass_element()
    mu_ap_MeV = mu * a_p * KG_TO_MEV
    qterm_MeV = 4 * q * mu * a_m * KG_TO_MEV

    I = fm.calc_Q(k)
    N = fm.calc_N(k, q, I)
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
    best_score = {tid: (1e9, 1e9) for tid, _, _ in targets}

    for K_n in range(Q_n + 1, K_n_max + 1):
        n_ = K_n - 1 - Q_n
        K_piece_n = (n_ * (n_ + 1))**2 * N[0]
        F_piece_n = 2*n_*I[0]*(1 + 3*(n_+I[0]+n_*I[0]) + 2*(n_**2 + I[0]**2)) * N[0]
        w1_max = a1 * (3 * K_n * K_n - 3 * K_n + 1)
        K_m_max = int((w1_max / a2) ** 0.5) + 2
        for K_m in range(Q_m + 1, K_m_max + 1):
            m_ = K_m - 1 - Q_m
            if (K_m - 1) ** 2 * a2 >= w1_max:
                continue
            K_piece_m = m_ * (2*m_**2 + 3*m_ + 1) * N[1]
            F_piece_m = 6*m_*I[1]*(1+m_+I[1]) * N[1]
            w2_max_in_Km = a2 * (2 * K_m - 1)
            w2_max_from_w1 = w1_max - (K_m - 1) ** 2 * a2
            w2_max = min(w2_max_in_Km, w2_max_from_w1)
            K_p_max = int(w2_max / a3) + 2
            for K_p in range(Q_p + 1, K_p_max + 1):
                p_ = K_p - 1 - Q_p
                if (K_p - 1) * a3 >= w2_max:
                    continue
                K_piece_p = p_ * (p_ + 1) * N[2]
                F_piece_p = 2*p_*I[2] * N[2]
                L_sigma = 0.5 * N[2] * (p_ + I[2]) - I[3]
                # Mass prefix without K_sig contribution:
                bracket_no_sig = (K_piece_n + K_piece_m + K_piece_p + S
                                   + F_piece_n + F_piece_m + F_piece_p + PHI)
                for K_sig in range(Q_sig + 1, K_sig_max + 1):
                    sig_ = K_sig - 1 - Q_sig
                    bracket = bracket_no_sig + 4 * sig_
                    M_MeV = mu_ap_MeV * bracket + qterm_MeV
                    K_B = L_sigma - sig_

                    for tid, M_t, KB_t in targets:
                        dM = abs(M_MeV - M_t)
                        dKB = abs(K_B - KB_t)
                        score = (dKB, dM)
                        if score < best_score[tid]:
                            best_score[tid] = score
                            best[tid] = {
                                "K": (K_n, K_m, K_p, K_sig),
                                "nmps": (n_, m_, p_, sig_),
                                "M_MeV": M_MeV,
                                "K_B": K_B,
                            }
    return best


def main():
    print("=" * 90)
    print(" G-Tabelle IV reproduction — streaming reachability enumeration")
    print("=" * 90)
    print()

    SECTORS = {
        "ε":         (0, 0, 0),
        "ω(783)":    (0, 2, 0),
        "η'(958)":   (0, 0, 0),
        "S*(993)":   (0, 0, 0),
        "Φ(1019)":   (0, 2, 0),
        "f(1270)":   (0, 4, 0),
        "D(1285)":   (0, 2, 0),
        "E(1420)":   (0, 2, 0),
        "f'(1514)":  (0, 4, 0),
        "ω(1675)":   (0, 6, 0),
        "K*(892)":   (1, 2, 0),
        "K_A(1240)": (1, 2, 0),
        "K*(1420)":  (1, 4, 0),
        "L(1770)":   (1, 4, 0),
        "ρ(770)":    (2, 2, 0),
        "δ(970)":    (2, 0, 0),
        "A1(1100)":  (2, 2, 0),
        "B(1235)":   (2, 2, 0),
        "A2(1310)":  (2, 4, 0),
        "F1(1540)":  (2, 2, 0),
        "ρ'(1600)":  (2, 2, 0),
        "A3(1640)":  (2, 4, 0),
        "g(1680)":   (2, 6, 0),
    }

    # Group targets by sector
    sector_targets = defaultdict(list)   # key: (P, Q, q_x) → list of (sym, M, KB)
    target_data = {}                     # sym → (M, KB, P, Q)
    for r in TABLE_IV_MESONS_K1:
        if r.symbol not in SECTORS:
            continue
        P_, Q_, q_neu = SECTORS[r.symbol]
        if isinstance(r.mass_MeV, tuple):
            M_t = r.mass_MeV[0]
            KB_t = r.K_B[0]
        else:
            M_t = r.mass_MeV
            KB_t = r.K_B
        sector_targets[(P_, Q_, q_neu)].append((r.symbol, M_t, KB_t))
        target_data[r.symbol] = (M_t, KB_t, P_, Q_)

    # Results: sym → list of (kap, best_match) for κ ∈ {0,1}
    results = {sym: {} for sym in target_data}
    for (P_, Q_, q_neu), tgts in sector_targets.items():
        for kap in (0, 1):
            print(f"  Enumerating (P={P_}, Q={Q_}, κ={kap}, q={q_neu}) "
                  f"for {len(tgts)} target(s)...", flush=True)
            matches = match_sector(1, P_, Q_, kap, q_neu, tgts)
            for sym, m in matches.items():
                results[sym][kap] = m

    print()
    print(f"  {'Particle':<12} {'P':>2} {'Q':>2}  {'M_heim':>10}  {'K_B':>5}  "
          f"{'best (κ, nmps, K_B)':<42}  {'Δ_M':>9} {'Δ_KB':>5}")
    print("  " + "-" * 92)
    n_exact_KB = 0
    n_within_05 = 0

    for r in TABLE_IV_MESONS_K1:
        if r.symbol not in results:
            continue
        M_t, KB_t, P_, Q_ = target_data[r.symbol]
        # Pick best κ
        best = None
        best_score = None
        best_kap = None
        for kap, m in results[r.symbol].items():
            if m is None:
                continue
            score = (abs(m["K_B"] - KB_t), abs(m["M_MeV"] - M_t))
            if best_score is None or score < best_score:
                best_score = score
                best = m
                best_kap = kap
        if best is None:
            print(f"  {r.symbol:<12} {P_:>2} {Q_:>2}  {M_t:>10.4f}  "
                  f"{KB_t!s:>5}  (no match)")
            continue
        if int(best["K_B"]) == KB_t:
            n_exact_KB += 1
        if abs(best["M_MeV"] - M_t) < 0.5:
            n_within_05 += 1
        tag = f"κ={best_kap} {best['nmps']} K_B={int(best['K_B'])}"
        print(f"  {r.symbol:<12} {P_:>2} {Q_:>2}  {M_t:>10.4f}  "
              f"{KB_t!s:>5}  {tag:<42}  "
              f"{best['M_MeV']-M_t:>+9.4f} {int(best['K_B'])-KB_t:>+5d}")

    print()
    print(f"  Exact K_B match: {n_exact_KB}/{len(target_data)}")
    print(f"  Mass within 0.5 MeV: {n_within_05}/{len(target_data)}")


if __name__ == "__main__":
    main()
