"""
Test the calc_n decomposition for the Δ family.

Hypothesis: our greedy exhaustion picks different (p, σ) than Heim's
Tabelle I publishes.  Check what our calc_n gives for each Δ ground
state and compare to Heim's listed values.

If both correspond to the SAME W via the inverse-substitution
(11) check, that confirms the formula admits multiple solutions
and Heim picked a non-greedy one.
"""

from __future__ import annotations

from math import exp

import formulae as fm
from constants import (KG_TO_MEV, alpha_minus, alpha_plus, eta, mass_element,
                       theta)


# Heim's Tabelle I (n, m, p, σ) for Δ family (k=2)
HEIM_DELTA = {
    "o⁺⁺": (1, 2, 3, 3, 0, +2, (2, 1, 9, 4)),       # (eps, k, P, Q, κ, q_x, (n,m,p,σ))
    "o⁺":  (1, 2, 3, 3, 0, +1, (2, -1, -1, -6)),
    "o⁰":  (1, 2, 3, 3, 0,  0, (2, -1, -10, 2)),
    "o⁻":  (1, 2, 3, 3, 0, -1, (2, -1, -16, -15)),
}

# Heim's Tabelle II masses (J0032 p.39)
HEIM_MASS = {
    "o⁺⁺": 1236.02333225,
    "o⁺":  1235.99646406,
    "o⁰":  1235.99143567,
    "o⁻":  1231.20485197,
}


def compute_w(nmps, I, N, k):
    """J0032 eq. 11 LHS: w = (n+Q_n)³·α_1 + (m+Q_m)²·α_2 + (p+Q_p)·α_3
    + exp(-β·K_σ).  Returns w."""
    n, m, p, sig = nmps
    Q_n, Q_m, Q_p, Q_sig = I
    a1 = N[0]
    a2 = 1.5 * N[1]
    a3 = 0.5 * N[2]
    K_sig = sig + 1 + Q_sig
    beta = (2 * k - 1) / (3.0 * Q_sig) if Q_sig != 0 else 1.0
    return ((n + Q_n) ** 3 * a1
            + (m + Q_m) ** 2 * a2
            + (p + Q_p) * a3
            + exp(-beta * K_sig))


def mass_from_nmps(nmps, P, Q, kap, q_x, I, N, k, include_phi=True, W=None):
    """Compute mass from explicit (n, m, p, σ) using J0060-corrected form."""
    q = abs(q_x)
    eta00 = eta(1, 0)
    th = theta(eta00)
    a_p = alpha_plus(eta00, th)
    a_m = alpha_minus(eta00, th)
    mu = mass_element()
    n_, m_, p_, sig_ = nmps
    if W is None:
        W = compute_w(nmps, I, N, k)
    K_mass = ((n_ * (n_ + 1))**2 * N[0]
              + m_ * (2*m_**2 + 3*m_ + 1) * N[1]
              + p_ * (p_ + 1) * N[2]
              + 4 * sig_)
    S = ((I[0] * (I[0] + 1))**2 * N[0]
         + I[1] * (2*I[1]**2 + 3*I[1] + 1) * N[1]
         + I[2] * (I[2] + 1) * N[2]
         + 4 * I[3])
    F_cross = (2*n_*I[0]*(1 + 3*(n_+I[0]+n_*I[0]) + 2*(n_**2 + I[0]**2)) * N[0]
               + 6*m_*I[1]*(1+m_+I[1]) * N[1]
               + 2*p_*I[2] * N[2])
    PHI = P * (-1)**(P+Q) * (P+Q) * N[4] + Q * (P+1) * N[5]
    if include_phi:
        phi_val = fm.calc_phi(k, P, Q, kap, q, nmps, I, N, W)
        F = F_cross + phi_val
    else:
        F = F_cross
    M_kg = mu * a_p * (K_mass + S + F + PHI) + 4 * q * mu * a_m
    return M_kg * KG_TO_MEV


def main():
    print("=" * 95)
    print(" Δ family: Heim's published (n, m, p, σ) vs our greedy decomposition")
    print("=" * 95)
    print()

    print(f"  {'Particle':<8} {'Heim (n,m,p,σ)':<22} {'Heim w':>10}  "
          f"{'Our calc_n':<22} {'Our w':>10}  {'Δw':>10}")
    print("  " + "-" * 90)

    for name, params in HEIM_DELTA.items():
        eps, k, P, Q, kap, q_x, heim_nmps = params
        I = fm.calc_Q(k)
        q = abs(q_x)
        N = fm.calc_N(k, q, I)
        # Our W_{N=0}
        W0 = fm.calc_W(eps, k, P, Q, kap, q_x, I)
        # Our greedy decomposition
        our_nmps = fm.calc_n(k, I, N, W0)
        # w from each (n, m, p, σ) via eq. 11
        heim_w = compute_w(heim_nmps, I, N, k)
        our_w = compute_w(our_nmps, I, N, k)
        print(f"  {name:<8} {str(heim_nmps):<22} {heim_w:>10.4f}  "
              f"{str(our_nmps):<22} {our_w:>10.4f}  "
              f"{heim_w - our_w:>10.4f}")

    print()
    print("=" * 95)
    print(" Masses computed from each (n, m, p, σ) choice")
    print("=" * 95)
    print()
    print(f"  {'Particle':<8} {'Heim mass':>12}  {'Our (greedy)':>14}  "
          f"{'Heim-nmps mass':>16}  {'Δ Heim-our':>10}")
    print("  " + "-" * 80)

    for name, params in HEIM_DELTA.items():
        eps, k, P, Q, kap, q_x, heim_nmps = params
        I = fm.calc_Q(k)
        q = abs(q_x)
        N = fm.calc_N(k, q, I)
        W0 = fm.calc_W(eps, k, P, Q, kap, q_x, I)
        our_nmps = fm.calc_n(k, I, N, W0)
        # Use heimmass.py logic — must go via calc_mass which does calc_n internally
        from formulae import calc_mass
        our_mass_kg = calc_mass(eps, k, P, Q, kap, q_x)
        our_mass = our_mass_kg * KG_TO_MEV
        # Mass from Heim's published nmps directly
        heim_mass_calc = mass_from_nmps(heim_nmps, P, Q, kap, q_x, I, N, k)
        target = HEIM_MASS[name]
        print(f"  {name:<8} {target:>12.6f}  {our_mass:>14.6f}  "
              f"{heim_mass_calc:>16.6f}  {target - our_mass:>+10.4f}")


if __name__ == "__main__":
    main()
