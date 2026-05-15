"""
Cross-check our implementation against Heim's Anhang B canonical values
(J0032 pp.41-43).

Heim's Anhang B tabulates:
  - canonical η, η_{1,1}, η_{1,2}, η_{2,2}, θ, θ_{1,1}, θ_{1,2}, θ_{2,2}
  - α_+, α_-
  - Q_i, B, H, A for k = 1 and k = 2
  - N_1(k,q) ... N_6(k,q) for (k,q) ∈ {(1,0), (1,1), (2,0), (2,1), (2,2)}
  - per-particle a_1, a_2, a_3, W_{N=0} for the 21 ground states

We compute each of these via our code and report agreement / disagreement.
"""

from __future__ import annotations

from math import comb, exp, sqrt

import formulae as fm
from constants import (alpha_fine_structure, alpha_minus, alpha_plus, eta,
                        mass_element, theta)


# Heim's canonical values from Anhang B
HEIM_ANHANG_B = {
    # Page 41 — symbol values
    "η":            0.98998964,
    "η_1,1":        0.98756399,
    "η_1,2":        0.98516776,
    "η_2,2":        0.84242385,
    "θ":            7.93991266,
    "θ_1,1":        7.92534503,
    "θ_1,2":        7.91095114,
    "θ_2,2":        7.04779227,
    "α_+":          0.01832211,
    "α_-":          0.00812835,
}

# Q_i, B, H, A per k
HEIM_QHBA = {
    1: {"Q_n": 3,  "Q_m": 3,  "Q_p": 2,  "Q_σ": 1,  "B": 27, "H": 9,
        "A": 2787.59025432},
    2: {"Q_n": 24, "Q_m": 31, "Q_p": 34, "Q_σ": 15, "B": 26, "H": 104,
        "A": 14727.57867072},
}

# N_i(k, q) — page 42
HEIM_NI = {
    "N_1(1,1)":   0.99688127,
    "N_1(1,0)":   1.0,
    "N_1(2,1)":   0.99627809,
    "N_1(2,0)":   1.0,
    "N_1(2,2)":   0.95891826,
    "N_2(1,1)":   0.67506174,
    "N_2(1,0)":   0.66666667,
    "N_2(2,1)":   0.67670370,
    "N_2(2,0)":   0.66666667,
    "N_2(2,2)":   0.79136728,
    "N_3(1,1)":   1.95731764,
    "N_3(1,0)":   2.0,
    "N_3(2,1)":   2.59881924,
    "N_3(2,0)":   2.71828183,    # = e (Euler)
    "N_3(2,2)":   2.12190443,
    "N_4(1,1)":   4.0,
    "N_4(1,0)":   4.0,
    "N_4(2,1)":   4.0,
    "N_4(2,0)":   2.0,
    "N_4(2,2)":   6.0,
    "N_5(1,1)":   1.15773470,
    "N_5(1,0)":   1.15773470,
    "N_5(2,1)":   1.73247496,
    "N_5(2,0)":   1.15773470,
    "N_5(2,2)":   76.73214581,
    "N_6(1,1)":   0.00000164,
    "N_6(1,0)":   0.00000164,
    "N_6(2,1)":   0.02518725,
    "N_6(2,0)":  -0.10493009,
    "N_6(2,2)":   0.15580107,
}

# Per-particle W_{N=0} (page 43)
HEIM_W = {
    "e⁻":    38.70294226,
    "μ⁻":    2830.26324345,
    "π±":    3514.46294316,
    "K⁺":    8857.95769020,
    "e₀":    38.51308957,
    "π⁰":    3419.16217346,
    "K⁰":    9332.35821820,
    "η":     9905.00599107,
    "p":     14792.56308050,
    "Σ⁺":    18124.03136129,
    "Σ⁻":    18183.30294347,
    "Ξ⁻":    18998.73451193,
    "Ω⁻":    23157.61451004,
    "o⁺⁺":   18115.38391620,   # Δ⁺⁺
    "o⁺":    18467.56082305,   # Δ⁺
    "o⁻":    18448.51703290,   # Δ⁻
    "n":     14828.61089116,
    "Λ":     16827.97671482,
    "Σ⁰":    18179.59733741,
    "Ξ⁰":    18990.08927597,
    "o⁰":    18508.94119539,   # Δ⁰
}

# Mapping particle → (eps, k, P, Q, kap, q_x) for calc_W (from TABLE_I)
HEIM_PARTICLE_PARAMS = {
    "e⁻":   (1, 1, 1, 1, 0, -1),
    "e₀":   (1, 1, 1, 1, 0,  0),
    "μ⁻":   (1, 1, 1, 1, 1, -1),
    "η":    (1, 1, 0, 0, 0,  0),
    "K⁺":   (1, 1, 1, 0, 1,  1),
    "K⁰":   (1, 1, 1, 0, 1,  0),
    "π±":   (1, 1, 2, 0, 0,  1),
    "π⁰":   (1, 1, 2, 0, 0,  0),
    "Λ":    (1, 2, 0, 1, 0,  0),
    "Ω⁻":   (1, 2, 0, 3, 0, -1),
    "p":    (1, 2, 1, 1, 0,  1),
    "n":    (1, 2, 1, 1, 0,  0),
    "Ξ⁻":   (1, 2, 1, 1, 1, -1),
    "Ξ⁰":   (1, 2, 1, 1, 1,  0),
    "Σ⁺":   (1, 2, 2, 1, 0,  1),
    "Σ⁰":   (1, 2, 2, 1, 0,  0),
    "Σ⁻":   (1, 2, 2, 1, 0, -1),
    "o⁺⁺":  (1, 2, 3, 3, 0,  2),
    "o⁺":   (1, 2, 3, 3, 0,  1),
    "o⁰":   (1, 2, 3, 3, 0,  0),
    "o⁻":   (1, 2, 3, 3, 0, -1),
}


def check(label, computed, expected, tol=1e-6):
    diff = abs(computed - expected)
    rel = diff / abs(expected) if expected != 0 else diff
    if diff < tol or rel < tol:
        status = "✓"
    elif diff < tol * 100 or rel < 1e-4:
        status = "≈"
    else:
        status = "✗"
    print(f"  {label:<14} computed = {computed:>16.10g}  "
          f"Heim = {expected:>16.10g}  Δ = {diff:>10.3g}  {status}")


def main():
    print("=" * 90)
    print(" Anhang B cross-check: our code vs Heim's published canonical values")
    print("=" * 90)

    # 1. η, θ, α
    print()
    print("1. Canonical η, θ, α values (J0032 p.41)")
    print("   " + "-" * 60)
    eta00 = eta(1, 0)
    check("η",      eta00,         HEIM_ANHANG_B["η"])
    check("η_1,1",  eta(1, 1),     HEIM_ANHANG_B["η_1,1"])
    check("η_1,2",  eta(1, 2),     HEIM_ANHANG_B["η_1,2"])
    check("η_2,2",  eta(2, 2),     HEIM_ANHANG_B["η_2,2"])
    check("θ",      theta(eta00),  HEIM_ANHANG_B["θ"])
    check("θ_1,1",  theta(eta(1, 1)), HEIM_ANHANG_B["θ_1,1"])
    check("θ_1,2",  theta(eta(1, 2)), HEIM_ANHANG_B["θ_1,2"])
    check("θ_2,2",  theta(eta(2, 2)), HEIM_ANHANG_B["θ_2,2"])
    th = theta(eta00)
    check("α_+",    alpha_plus(eta00, th),  HEIM_ANHANG_B["α_+"])
    check("α_-",    alpha_minus(eta00, th), HEIM_ANHANG_B["α_-"])

    # 2. Q, B, H, A per k
    print()
    print("2. Q_i, B, H, A (J0032 p.41)")
    print("   " + "-" * 60)
    for k in (1, 2):
        I = fm.calc_Q(k)
        H = sum(I)
        B = 3.0 * H / (k * k * (2 * k - 1))
        # A from (12a): A = 8·g·H / (2 − k + 8·H·(k − 1))
        # g from (12c):
        eta00 = eta(1, 0)
        g = (I[0] ** 3 + I[1] ** 2
             + I[2] * exp(k - 1) / k
             + exp((1.0 - 2 * k) / 3.0)
             - (k - 1) * H)
        A = 8.0 * g * H / (2.0 - k + 8.0 * H * (k - 1))
        print(f"  k={k}:")
        check(f"  Q_n",  I[0], HEIM_QHBA[k]["Q_n"])
        check(f"  Q_m",  I[1], HEIM_QHBA[k]["Q_m"])
        check(f"  Q_p",  I[2], HEIM_QHBA[k]["Q_p"])
        check(f"  Q_σ",  I[3], HEIM_QHBA[k]["Q_σ"])
        check(f"  B",    B,    HEIM_QHBA[k]["B"])
        check(f"  H",    H,    HEIM_QHBA[k]["H"])
        check(f"  A",    A,    HEIM_QHBA[k]["A"])

    # 3. N_i(k, q)
    print()
    print("3. N_i(k, q) (J0032 p.42)")
    print("   " + "-" * 60)
    for k in (1, 2):
        I = fm.calc_Q(k)
        for q in (0, 1, 2):
            if (k, q) == (1, 2):  # not in Heim's table
                continue
            N = fm.calc_N(k, q, I)
            for i in range(6):
                key = f"N_{i+1}({k},{q})"
                if key in HEIM_NI:
                    check(key, N[i], HEIM_NI[key])

    # 4. W_{N=0} per particle
    print()
    print("4. W_{N=0} per ground-state particle (J0032 p.43)")
    print("   " + "-" * 60)
    for name, params in HEIM_PARTICLE_PARAMS.items():
        eps, k, P, Q, kap, q_x = params
        I = fm.calc_Q(k)
        W = fm.calc_W(eps, k, P, Q, kap, q_x, I)
        if name in HEIM_W:
            check(name, W, HEIM_W[name], tol=1e-4)


if __name__ == "__main__":
    main()
