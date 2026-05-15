"""
Reproduction of Heim's G-Tabelle IV mesonic resonances (k=1) via the
excitation procedure of J0032 ("Ausgewählte Ergebnisse einer einheitlichen
Quantenfeldtheorie der Materie und Gravitation", Burkhard Heim 1973).

Following the May 2026 reading of J0032, the resonance procedure is:

  Auswahlregel (J0032 eq. 11):
    (n+Q_n)³·α_1 + (m+Q_m)²·α_2 + (p+Q_p)·α_3 +
       exp[-(2k-1)/(3·Q_σ)·(σ+Q_σ)]
    = W_{N=0} · (1 + f(N))                ≡ w

  with α_1 = N_1, 2α_2 = 3N_2, 2α_3 = N_3      (J0032 eq. 11a)

  Anregerfunktion (J0032 eq. 14):
    f(N) = a · N/(N+1) + b · N

  with a, b sector-dependent constants from extremely complex
  expressions (J0032 eqs. 14a–14b_1).

  Exhaustionsverfahren (J0032 eq. 16, = our existing greedy):
    K_n: max K with w − K³·α_1 ≥ 0    →  n = K_n − 1 − Q_n
    K_m: similar with α_2             →  m = K_m − 1 − Q_m
    K_p: similar with α_3             →  p = K_p − 1 − Q_p
    K_σ: w_3 − exp(−βK) ≤ 0 with 3βQ_σ = 2k−1  →  σ = K_σ − 1 − Q_σ

  Bandwidth (J0032 eq. 14e):
    K_B = L_(σ)(p_N) − σ_N
    where L_(σ)(p) = N_3·(p+Q_p)/2 − Q_σ         (eq. 9d)

  Mass formula (J0032 eq. 4):
    M = μ · ((G + S + F + φ)·α_+ + 4q·α_-)
    with φ = 0 for N > 0                          (eq. 5e_2)

This script:

  1. Implements the J0032 procedure as `calc_resonance(eps, k, P, Q, kap, q_x, N, f)`
     that takes f directly as a numerical parameter.

  2. For each entry of G-Tabelle IV, back-solves the required f value
     to reproduce Heim's published mass and K_B.

  3. Reports the inferred (a, b) per sector (groups of entries sharing
     the same k, P, Q, κ, q).

  4. Identifies which Tabelle-IV entries can be back-solved cleanly,
     and where the existing infrastructure breaks down (typically
     because we don't yet know the sector's Q assignment).

Implementing the f(N) formula from first principles (eqs. 14a-14b_1)
is a substantial additional task; this script's back-solving lays the
groundwork for that.

Run with:
    ./venv/bin/python python/resonance_reproduction.py
"""

from __future__ import annotations

from math import exp, fabs

import formulae as fm
from constants import (KG_TO_MEV, alpha_minus, alpha_plus, eta, mass_element,
                       theta)
from g_tables import TABLE_IV_MESONS_K1


def calc_alphas_excitation(k: int, q: float):
    """The α_1, α_2, α_3 from J0032 eq. 11a in terms of N_1, N_2, N_3."""
    I = fm.calc_Q(k)
    N = fm.calc_N(k, q, I)
    alpha_1 = N[0]               # = N_1
    alpha_2 = 1.5 * N[1]         # = 3 N_2 / 2
    alpha_3 = 0.5 * N[2]         # = N_3 / 2
    return alpha_1, alpha_2, alpha_3, N, I


def exhaustion(w: float, I, N, k: int):
    """J0032 eq. 16 Exhaustionsverfahren. Given w (= rhs of eq. 11),
    return (K_n, K_m, K_p, K_σ, n, m, p, σ).

    Per Heim's J0032 p. 17: each K_x is the FIRST value of K where the
    sign of (residual − next-term) changes.  Then n = K_n − 1 − Q_n etc.
    per (16a-d).

    For K_n, K_m, K_p the residual starts positive and decreases with K;
    sign change is from "≥ 0" to "< 0".
    For K_σ the form is w_3 − exp(−βK), which starts negative (since
    exp(−βK) starts close to 1 for small K and w_3 ∈ (0, α_3)) and
    increases with K; sign change is from "≤ 0" to "> 0".
    """
    alpha_1 = N[0]                  # = N_1     (J0032 eq. 11a)
    alpha_2 = 1.5 * N[1]            # = 3 N_2 / 2
    alpha_3 = 0.5 * N[2]            # = N_3 / 2

    # K_n: smallest K with w − K³·α_1 < 0
    K = 1
    while w - K**3 * alpha_1 >= 0 and K < 10000:
        K += 1
    K_n = K
    w1 = w - (K_n - 1) ** 3 * alpha_1     # residual after K_n step

    # K_m: smallest K with w_1 − K²·α_2 < 0
    K = 1
    while w1 - K**2 * alpha_2 >= 0 and K < 10000:
        K += 1
    K_m = K
    w2 = w1 - (K_m - 1) ** 2 * alpha_2

    # K_p: smallest K with w_2 − K·α_3 < 0
    K = 1
    while w2 - K * alpha_3 >= 0 and K < 10000:
        K += 1
    K_p = K
    w3 = w2 - (K_p - 1) * alpha_3

    # K_σ: smallest K with w_3 − exp(−βK) > 0   (3βQ_σ = 2k − 1)
    Q_sig = I[3]
    beta = (2 * k - 1) / (3.0 * Q_sig) if Q_sig != 0 else 1.0
    K = 1
    while w3 - exp(-beta * K) <= 0 and K < 10000:
        K += 1
    K_sig = K

    # Convert K's to (n, m, p, σ) via (16a-d):  x = K_x − 1 − Q_x
    n = K_n - 1 - I[0]
    m = K_m - 1 - I[1]
    p = K_p - 1 - I[2]
    sig = K_sig - 1 - I[3]

    return K_n, K_m, K_p, K_sig, n, m, p, sig


def calc_resonance(eps, k, P, Q, kap, q_x, N_excit, f_value):
    """Compute mass and (n,m,p,σ), K_B for a given excitation.

    f_value is the numerical value of f(N) — to be supplied by the
    caller (either back-solved or computed from a, b)."""
    q = fabs(q_x)
    eta00 = eta(1, 0)
    th = theta(eta00)
    a_p = alpha_plus(eta00, th)
    a_m = alpha_minus(eta00, th)

    I = fm.calc_Q(k)
    N = fm.calc_N(k, q, I)
    W0 = fm.calc_W(eps, k, P, Q, kap, q_x, I)   # ground-state W per [B22]
    w = W0 * (1.0 + f_value)                     # J0032 eq. 11

    K_n, K_m, K_p, K_sig, n_, m_, p_, sig_ = exhaustion(w, I, N, k)
    nmps = (n_, m_, p_, sig_)

    # Compute mass.  For ground states (N_excit = 0, f_value = 0), φ
    # contributes per J0032 eq. 5e_2 (δ(0) = 1); for excited states
    # (N_excit > 0), δ(N) = 0 → φ = 0.
    is_ground = (N_excit == 0)

    K_mass = ((nmps[0] * (nmps[0] + 1))**2 * N[0]
              + nmps[1] * (2*nmps[1]**2 + 3*nmps[1] + 1) * N[1]
              + nmps[2] * (nmps[2] + 1) * N[2]
              + 4 * nmps[3])
    S = ((I[0] * (I[0] + 1))**2 * N[0]
         + I[1] * (2*I[1]**2 + 3*I[1] + 1) * N[1]
         + I[2] * (I[2] + 1) * N[2]
         + 4 * I[3])
    F_cross = (2*nmps[0]*I[0]*(1 + 3*(nmps[0]+I[0]+nmps[0]*I[0])
                              + 2*(nmps[0]**2 + I[0]**2)) * N[0]
               + 6*nmps[1]*I[1]*(1+nmps[1]+I[1]) * N[1]
               + 2*nmps[2]*I[2]*N[2])
    if is_ground:
        phi_val = fm.calc_phi(k, P, Q, kap, q, nmps, I, N, W0)
        F = F_cross + phi_val
    else:
        F = F_cross

    PHI = P * (-1)**(P+Q) * (P+Q) * N[4] + Q * (P+1) * N[5]

    # J0060-corrected mass formula (J0032 eq. 4 = the same form):
    #   M = μ · ((G + S + F + φ)·α_+ + 4q·α_-)
    M_kg = mass_element() * ((K_mass + S + F + PHI) * a_p + 4*q*a_m)
    M_MeV = M_kg * KG_TO_MEV

    # Bandwidth K_B per (14e) with L_σ from (9d)
    L_sigma = 0.5 * N[2] * (p_ + I[2]) - I[3]    # eq. 9d: 2L_σ = N_3(p+Q_p) − 2Q_σ → L_σ = N_3(p+Q_p)/2 − Q_σ
    K_B = L_sigma - sig_

    return {
        "w": w,
        "nmps": nmps,
        "K_indices": (K_n, K_m, K_p, K_sig),
        "K_B": K_B,
        "L_sigma": L_sigma,
        "M_MeV": M_MeV,
    }


def back_solve_f(eps, k, P, Q, kap, q_x, M_target, f_range=(-0.5, 50, 0.0001)):
    """Find f such that calc_resonance produces M_target (within 0.01 MeV)."""
    best_f, best_diff = None, float("inf")
    f_min, f_max, f_step = f_range
    f = f_min
    while f < f_max:
        try:
            r = calc_resonance(eps, k, P, Q, kap, q_x, 0, f)
            diff = abs(r["M_MeV"] - M_target)
            if diff < best_diff:
                best_diff = diff
                best_f = f
        except (ValueError, OverflowError, ZeroDivisionError):
            pass
        f += f_step
    return best_f, best_diff


def main():
    print("=" * 86)
    print(" Resonance reproduction — back-solving f for G-Tabelle IV entries")
    print("=" * 86)
    print()
    print("J0032 eq. 4 + eq. 11: M = μ·((G+S+F)·α_+ + 4q·α_-) for w = W₀·(1+f(N))")
    print("Strategy: for each Tabelle IV entry with k=1 and assumed (P, Q, q, κ),")
    print("back-solve the f value that reproduces Heim's published mass.")
    print()

    # For each Tabelle IV entry, try plausible (P, Q, κ, q) assignments and
    # back-solve f.  P is given in the table.  Q (spin·2) and q must be
    # inferred from the particle name / known properties.
    # We focus on the cleanest cases first.

    # Spin assignments (J value, from PDG):
    SPIN = {
        "ε":         0,    "ω(783)":    1,
        "η'(958)":   0,    "S*(993)":   0,
        "Φ(1019)":   1,    "f(1270)":   2,
        "D(1285)":   1,    "E(1420)":   1,
        "f'(1514)":  2,    "ω(1675)":   3,
        "K*(892)":   1,    "K_A(1240)": 1,
        "K*(1420)":  2,    "L(1770)":   2,
        "ρ(770)":    1,    "δ(970)":    0,
        "A1(1100)":  1,    "B(1235)":   1,
        "A2(1310)":  2,    "F1(1540)":  1,
        "ρ'(1600)":  1,    "A3(1640)":  2,
        "g(1680)":   3,
    }

    print(f"  {'Particle':<12} {'P':>2} {'Q':>2} {'q':>2}  {'M (Heim)':>10}  "
          f"{'best f':>10}  {'diff [MeV]':>12}")
    print("  " + "-" * 74)

    for r in TABLE_IV_MESONS_K1:
        if isinstance(r.mass_MeV, tuple):
            M = r.mass_MeV[0]    # neutral form
            q_x = 0
        else:
            M = r.mass_MeV
            q_x = 0     # P = 0 isospin singlets are neutral
        Q = 2 * SPIN.get(r.symbol, 1)    # double-spin

        # Try κ = 0 first (singlet); for P=1 we'll need κ=1 too.
        best_f, best_diff = back_solve_f(1, 1, r.P, Q, 0, q_x, M)
        if best_f is None or best_diff > 1.0:
            # Try κ=1
            best_f_k1, best_diff_k1 = back_solve_f(1, 1, r.P, Q, 1, q_x, M)
            if best_diff_k1 < best_diff:
                best_f, best_diff = best_f_k1, best_diff_k1

        print(f"  {r.symbol:<12} {r.P:>2} {Q:>2} {q_x:>2}  {M:>10.4f}  "
              f"{best_f if best_f is not None else float('nan'):>10.4f}  "
              f"{best_diff:>12.4f}")


if __name__ == "__main__":
    main()
