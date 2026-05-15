"""
G-Tabelle IV reproduction by K-configuration enumeration.

For each k=1 mesonic-resonance sector (P, Q, κ, q), enumerate all
plausible (K_n, K_m, K_p, K_σ) configurations and compute the mass +
K_B for each.  Then for each Tabelle IV entry, find the configuration
matching its published mass AND K_B.

The mapping (K_n, K_m, K_p, K_σ) → (n, m, p, σ) is from J0032 eq. 16a-d:
    n = K_n − 1 − Q_n
    m = K_m − 1 − Q_m
    p = K_p − 1 − Q_p
    σ = K_σ − 1 − Q_σ

And the bandwidth K_B per J0032 eq. 14e:
    K_B = L_σ(p) − σ
where L_σ(p) = N_3·(p + Q_p)/2 − Q_σ per eq. 9d.

This script does the enumeration in a focused way:
  - Restrict K_n etc. to a reasonable maximum (covers up to N~500)
  - For each Tabelle IV entry, find K configs with matching mass (±1 MeV)
    and matching K_B
  - Report sector inferences

Run with:
    ./venv/bin/python python/resonance_enumerate.py
"""

from __future__ import annotations

from math import fabs

import formulae as fm
from constants import (KG_TO_MEV, alpha_minus, alpha_plus, eta, mass_element,
                       theta)
from g_tables import TABLE_IV_MESONS_K1


def enumerate_sector(k: int, P: int, Q: int, kap: int, q_x: int,
                      K_max_n: int = 32, K_max_m: int = 32,
                      K_max_p: int = 48, K_max_sig: int = 32):
    """Enumerate (K_n, K_m, K_p, K_σ) configurations and compute mass,
    K_B for each.  Return list of dicts."""
    q = fabs(q_x)
    eta00 = eta(1, 0)
    th = theta(eta00)
    a_p = alpha_plus(eta00, th)
    a_m = alpha_minus(eta00, th)
    mu = mass_element()

    I = fm.calc_Q(k)
    N = fm.calc_N(k, q, I)

    # Pre-compute the bracket pieces that don't depend on (n, m, p, σ)
    # i.e., S, Φ, and the constant prefactors.
    S = ((I[0] * (I[0] + 1))**2 * N[0]
         + I[1] * (2*I[1]**2 + 3*I[1] + 1) * N[1]
         + I[2] * (I[2] + 1) * N[2]
         + 4 * I[3])
    PHI = P * (-1)**(P+Q) * (P+Q) * N[4] + Q * (P+1) * N[5]
    mu_ap_kgmeV = mu * a_p * KG_TO_MEV
    qterm_MeV = 4 * q * mu * a_m * KG_TO_MEV    # outside the μα_+ multiplication

    out = []
    for K_n in range(1, K_max_n + 1):
        n = K_n - 1 - I[0]
        K_piece_n = (n * (n + 1)) ** 2 * N[0]
        F_piece_n_lookahead = 2 * n * I[0] * (
            1 + 3*(n + I[0] + n*I[0]) + 2*(n*n + I[0]*I[0])
        ) * N[0]

        for K_m in range(1, K_max_m + 1):
            m = K_m - 1 - I[1]
            K_piece_m = m * (2*m*m + 3*m + 1) * N[1]
            F_piece_m = 6 * m * I[1] * (1 + m + I[1]) * N[1]

            for K_p in range(1, K_max_p + 1):
                p = K_p - 1 - I[2]
                K_piece_p = p * (p + 1) * N[2]
                F_piece_p = 2 * p * I[2] * N[2]

                # L_σ(p) per eq. 9d.  Must be ≥ 0 for any σ-occupation to fit.
                L_sigma = 0.5 * N[2] * (p + I[2]) - I[3]

                for K_sig in range(1, K_max_sig + 1):
                    sig = K_sig - 1 - I[3]
                    K_piece_sig = 4 * sig

                    K_total = K_piece_n + K_piece_m + K_piece_p + K_piece_sig
                    F = F_piece_n_lookahead + F_piece_m + F_piece_p
                    # φ = 0 for excited states (which is the case for resonances)

                    bracket = K_total + S + F + PHI
                    M_MeV = mu_ap_kgmeV * bracket + qterm_MeV

                    K_B = L_sigma - sig

                    out.append({
                        "K": (K_n, K_m, K_p, K_sig),
                        "nmps": (n, m, p, sig),
                        "M_MeV": M_MeV,
                        "K_B": K_B,
                        "L_sigma": L_sigma,
                    })
    return out


def find_match(configs, M_target, K_B_target, tol_M=1.0, tol_KB=2):
    """Find configs matching (mass, K_B) within tolerances.
    Returns list of matches sorted by mass distance."""
    matches = []
    for c in configs:
        if abs(c["M_MeV"] - M_target) > tol_M:
            continue
        if abs(c["K_B"] - K_B_target) > tol_KB:
            continue
        matches.append(c)
    matches.sort(key=lambda c: (abs(c["M_MeV"] - M_target), abs(c["K_B"] - K_B_target)))
    return matches


def main():
    print("=" * 90)
    print(" G-Tabelle IV reproduction by K-configuration enumeration")
    print("=" * 90)
    print()

    # Spin and isospin assignments for each entry
    # Format: (P, Q, q_x_neutral, q_x_charged_or_None)
    # P = 2·isospin per Heim convention.
    # Q = 2·spin per Heim convention.
    SECTORS = {
        "ε":         (0, 0, 0, None),    # isospin 0, spin 0
        "ω(783)":    (0, 2, 0, None),    # isospin 0, spin 1
        "η'(958)":   (0, 0, 0, None),
        "S*(993)":   (0, 0, 0, None),
        "Φ(1019)":   (0, 2, 0, None),
        "f(1270)":   (0, 4, 0, None),
        "D(1285)":   (0, 2, 0, None),
        "E(1420)":   (0, 2, 0, None),
        "f'(1514)":  (0, 4, 0, None),
        "ω(1675)":   (0, 6, 0, None),    # spin 3
        "K*(892)":   (1, 2, 0, 1),       # isospin 1/2, spin 1 — doublet
        "K_A(1240)": (1, 2, 0, 1),
        "K*(1420)":  (1, 4, 0, 1),       # spin 2
        "L(1770)":   (1, 4, 0, 1),
        "ρ(770)":    (2, 2, 0, 1),       # isospin 1, spin 1 (ρ⁰/ρ±)
        "δ(970)":    (2, 0, 0, 1),       # spin 0
        "A1(1100)":  (2, 2, 0, 1),
        "B(1235)":   (2, 2, 0, 1),
        "A2(1310)":  (2, 4, 0, 1),
        "F1(1540)":  (2, 2, 0, 1),
        "ρ'(1600)":  (2, 2, 0, 1),
        "A3(1640)":  (2, 4, 0, 1),
        "g(1680)":   (2, 6, 0, 1),
    }

    # Cache per (P, Q, κ, q) sector
    sector_cache = {}
    def get_sector(P, Q, kap, q_x):
        key = (P, Q, kap, q_x)
        if key not in sector_cache:
            print(f"  Enumerating sector (P={P}, Q={Q}, κ={kap}, q={q_x})...", flush=True)
            sector_cache[key] = enumerate_sector(1, P, Q, kap, q_x)
        return sector_cache[key]

    print()
    print(f"  {'Particle':<12} {'P':>2} {'Q':>2}  {'M_heim':>10}  {'N':>6} {'K_B':>5}  "
          f"{'best match':<30}  {'Δ_M':>8}")
    print("  " + "-" * 86)

    for r in TABLE_IV_MESONS_K1:
        if r.symbol not in SECTORS:
            continue
        P_, Q_, q_neu, q_chg = SECTORS[r.symbol]

        # Determine target mass and K_B (use neutral form for now)
        if isinstance(r.mass_MeV, tuple):
            M_target = r.mass_MeV[0]   # neutral
            N_target = r.N[0]
            KB_target = r.K_B[0]
            q_x = q_neu
        else:
            M_target = r.mass_MeV
            N_target = r.N
            KB_target = r.K_B
            q_x = q_neu

        # Try both κ = 0 and κ = 1
        best_match = None
        best_diff = float("inf")
        for kap in (0, 1):
            configs = get_sector(P_, Q_, kap, q_x)
            matches = find_match(configs, M_target, KB_target, tol_M=2.0, tol_KB=3)
            if matches:
                c = matches[0]
                diff = abs(c["M_MeV"] - M_target)
                if diff < best_diff:
                    best_diff = diff
                    best_match = (kap, c)

        if best_match is None:
            print(f"  {r.symbol:<12} {P_:>2} {Q_:>2}  {M_target:>10.4f}  "
                  f"{N_target!s:>6} {KB_target!s:>5}  {'(no match within tol)':<30}  "
                  f"{'—':>8}")
        else:
            kap, c = best_match
            tag = f"κ={kap} K={c['K']} K_B={int(c['K_B'])}"
            print(f"  {r.symbol:<12} {P_:>2} {Q_:>2}  {M_target:>10.4f}  "
                  f"{N_target!s:>6} {KB_target!s:>5}  {tag:<30}  "
                  f"{best_diff:>+8.4f}")

    print()
    print("Cache sizes:", {k: len(v) for k, v in sector_cache.items()})


if __name__ == "__main__":
    main()
