"""
Ab initio prediction of the Anregerfunktion coefficients (a, b) from
J0032 eqs. 14, 14a, 14a₁, 14b, 14b₁ (+ p.15a correction).

J0032 ("Ausgewählte Ergebnisse einer einheitlichen Quantenfeldtheorie der
Materie und Gravitation", Burkhard Heim 1973, pages 14-16) gives:

    f(N) = a · N/(N+1) + b · N                                      (14)

with two pairs of coupled equations defining (a, T) and (b, C):

    T · a · η²_qk · √η_qk
      = (P²/(k·ω))·(ω - k·(ω - c))
      + (k - 1)·(π/4·C(P,3) - η_{1,1}·C(P,2))                       (14a)

    (T - 1) / κ                                       [κ = Spiegel-isospin]
      = 4α·(B + k + 1)/(1 - α²)·(1 + 5α²)/(1 - 5α²)
      - 2·(3α/(4π))²
      - q·(π/2 - 1 - α²·π·e·(1 + √η)/(2·κ·(1 - 6α²)))               (14a₁)

    2·(b + C)·η²_qk·√η_qk
      = α·ϑ/8·(P² + 1)·[
            (1 + √η)/2 · (1 + η_{1,1}·η_{1,2}·(c/ω)·C(P,3)·(k - 1))
          + (k - 1)·(ϑ_{1,2}/ϑ - 8·C(P,2)/(P² + 1))
        ]                                                            (14b)

    C - 2·e·κ·q/η²·(2 - k)·(1 - η)²
      = π·(1 - √η)²·[
            1
          + √π·(k - 1)
          + P/k³·(3/e + q·(8 + η_qk)
                  + 4π·e/√η·(1 - κ)·(1 - q·3π/(5·e·η_qk)))
          - 2·(k - 1)·C(P,2)·(3 - P)·(2·e·(η + η_qk)
                                       + π·e/(3·√η)·ε·q_κ)
          + 8π·e/√η·κ·(k - 1)·(e/√η - q/√e)
        ]                                                            (14b₁)

with:
  α     — Sommerfeld fine-structure constant ≈ 1/137.036
  e     — Euler's number 2.71828...
  η, ϑ  — canonical η_{1,0}, ϑ = ϑ(η_{1,0})  (NOT state-specific)
  η_qk  — state-specific η evaluated at (q, k)
  η_{1,1}, η_{1,2}     — η at (q=1, k=1) and (q=1, k=2)
  ϑ_{1,2}              — ϑ evaluated at η_{1,2}
  ω, c  — abstract constants with 3·ω = 4·c (only ratio c/ω = 3/4 matters)
  B     — = 3·H / (k²·(2k - 1))      [J0032 eq. 13b]
  H     — = Q_n + Q_m + Q_p + Q_σ    [J0032 eq. 12b]
  P, Q  — state quantum numbers (P = 2·isospin, Q = 2·spin)
  κ     — Spiegelisospin ∈ {0, 1}        (= chi/X in the manuscript)
  q     — state charge (= |εq_x| in formulae.py; we use |q_x| here)
  q_κ   — = ε·q (signed charge)
  ε     — = ±1 sign of the R₄± structure (from J0032 eq. 10)

For κ = 0, eq. 14a₁ has 1/κ on the LHS — we take the limit T = 1
(the leading 4α(B+k+1) term, when multiplied by κ→0, vanishes).
"""

from __future__ import annotations

from math import comb, e as E, pi, sqrt

import formulae as fm
from constants import alpha_fine_structure as _alpha, eta as _eta, theta as _theta


# Constants
ALPHA = _alpha()
EULER = E

# c/ω ratio from (8c₁): 3·ω = 4·c
C_OVER_OMEGA = 3.0 / 4.0


def _binom(n, k):
    if n < 0 or k < 0 or k > n:
        return 0
    return comb(n, k)


def predict_T(k: int, P: int, kap: int, q: float, B: float) -> float:
    """Solve (14a₁) for T."""
    if kap == 0:
        # Take the limit κ → 0: T = 1 (the κ-multiplied terms vanish).
        return 1.0
    alpha = ALPHA
    eta00 = _eta(1, 0)
    sqrt_eta = sqrt(eta00)
    # (T - 1) / κ = 4α(B+k+1)/(1-α²)·(1+5α²)/(1-5α²)
    #               - 2·(3α/(4π))²
    #               - q·(π/2 - 1 - α²·π·e·(1+√η) / (2·κ·(1 - 6α²)))
    term1 = 4.0 * alpha * (B + k + 1) / (1.0 - alpha**2) * (
        (1.0 + 5.0 * alpha**2) / (1.0 - 5.0 * alpha**2)
    )
    term2 = -2.0 * (3.0 * alpha / (4.0 * pi)) ** 2
    term3 = -q * (
        pi / 2 - 1
        - alpha**2 * pi * EULER * (1.0 + sqrt_eta) / (2.0 * kap * (1.0 - 6.0 * alpha**2))
    )
    return 1.0 + kap * (term1 + term2 + term3)


def predict_a(k: int, P: int, kap: int, q: float, B: float) -> float:
    """Compute a from (14a) given T."""
    T = predict_T(k, P, kap, q, B)
    # η_qk at state's (q, k); η_{1,1} = η at q=1, k=1
    eta_qk = _eta(q, k)
    eta_11 = _eta(1, 1)
    # RHS of (14a)
    omega_factor = 1.0 / k  # we will use ω and (ω - k(ω-c)) / (kω) = (1 - (k-1)(1-c/ω))/k
    # (P²/(kω))·(ω - k·(ω-c)) = (P²·/(kω))·(ω(1-k) + kc) = P²·(1-k+kc/ω)/k
    #                          = P²·(1 - (k-1)(1-c/ω))/k
    pterm = P**2 * (1.0 - (k - 1) * (1.0 - C_OVER_OMEGA)) / k
    crossterm = (k - 1) * (pi / 4.0 * _binom(P, 3) - eta_11 * _binom(P, 2))
    rhs = pterm + crossterm
    return rhs / (T * eta_qk**2 * sqrt(eta_qk))


def predict_C(k: int, P: int, kap: int, q: float, eps: int = 1) -> float:
    """Compute C from (14b₁) inclusive of the p.15a correction."""
    eta00 = _eta(1, 0)
    eta_qk = _eta(q, k)
    sqrt_eta = sqrt(eta00)

    # P/k³ inner bracket
    inner_Pk3 = (3.0 / EULER + q * (8.0 + eta_qk)
                 + 4.0 * pi * EULER / sqrt_eta * (1.0 - kap)
                 * (1.0 - q * 3.0 * pi / (5.0 * EULER * eta_qk)))

    # Big bracket of (14b₁)
    q_kap = eps * q   # signed charge
    bracket = (1.0
                + sqrt(pi) * (k - 1)
                + P / k**3 * inner_Pk3
                - 2.0 * (k - 1) * _binom(P, 2) * (3 - P) * (
                    2.0 * EULER * (eta00 + eta_qk)
                    + pi * EULER / (3.0 * sqrt_eta) * q_kap
                )
                + 8.0 * pi * EULER / sqrt_eta * kap * (k - 1)
                  * (EULER / sqrt_eta - q / sqrt(EULER))
                )

    C_lhs_uncorrected = pi * (1.0 - sqrt_eta) ** 2 * bracket
    # p.15a correction: C_LHS has additional -2·e·κ·q/η²·(2-k)·(1-η)²
    # so C (the standalone quantity) = C_LHS_uncorrected + the additive term
    correction = 2.0 * EULER * kap * q / eta00**2 * (2 - k) * (1.0 - eta00) ** 2
    return C_lhs_uncorrected + correction


def predict_b(k: int, P: int, kap: int, q: float, B: float) -> float:
    """Compute b from (14b) given C."""
    C = predict_C(k, P, kap, q)
    eta00 = _eta(1, 0)
    eta_qk = _eta(q, k)
    eta_11 = _eta(1, 1)
    eta_12 = _eta(1, 2)
    theta = _theta(eta00)
    theta_12 = _theta(eta_12)
    # RHS of (14b)
    inner = (
        (1.0 + sqrt(eta00)) / 2.0
        * (1.0 + eta_11 * eta_12 * C_OVER_OMEGA * _binom(P, 3) * (k - 1))
        + (k - 1) * (theta_12 / theta - 8.0 * _binom(P, 2) / (P**2 + 1))
    )
    rhs = ALPHA * theta / 8.0 * (P**2 + 1) * inner
    bplusC = rhs / (2.0 * eta_qk**2 * sqrt(eta_qk))
    return bplusC - C


def predict(k: int, P: int, Q: int, kap: int, q_x: float) -> tuple[float, float]:
    """Return predicted (a, b) for the Anregerkurve in sector (k, P, Q, κ, q)."""
    q = abs(q_x)
    I = fm.calc_Q(k)
    H = sum(I)
    B = 3.0 * H / (k**2 * (2 * k - 1))
    a = predict_a(k, P, kap, q, B)
    b = predict_b(k, P, kap, q, B)
    return a, b


def main():
    print("=" * 80)
    print(" Ab initio Anregerfunktion (a, b) predictions vs back-fit")
    print("=" * 80)

    # k=1 mesonic sectors with back-fitted values from
    # resonance_consistency.py (May 2026):
    K1_FITS = [
        # (label, P, Q, κ, q, a_fit, b_fit, n_entries)
        ("(P=0, Q=0)",      0, 0, 1, 0, +0.286,  +0.0045, 3),
        ("(P=0, Q=2)",      0, 2, 1, 0, +13.19,  +0.0484, 4),
        ("(P=1, Q=2)",      1, 2, 1, 0, +14.78,  +0.0722, 2),
        ("(P=1, Q=4)",      1, 4, 1, 0, +91.02,  +0.4526, 2),
        ("(P=2, Q=2)",      2, 2, 1, 0, +35.43,  +0.107,  5),
        ("(P=2, Q=4)",      2, 4, 1, 0, +212.7,  +0.6573, 2),
    ]

    # k=2 baryon sectors with back-fitted values from
    # resonance_consistency_iter.py (May 2026, post-eta-fix):
    K2_FITS = [
        # (label, P, Q, κ, q, a_fit, b_fit, n_entries)
        ("(P=0, Q=1, q= 0)", 0, 1, 0, 0, -0.0001, +0.0070, 12),
        ("(P=0, Q=5, q= 0)", 0, 5, 0, 0, -0.7954, +0.0009, 4),
        ("(P=2, Q=1, q=-1)", 2, 1, 0, 1, +0.0244, +0.0073, 16),
        ("(P=2, Q=3, q=-1)", 2, 3, 0, 1, -1.0354, +0.0185, 2),
        ("(P=3, Q=1, q= 0)", 3, 1, 1, 0, -1.0198, +0.0001, 4),
        ("(P=3, Q=5, q= 0)", 3, 5, 0, 0, -0.9961, +0.0000, 8),
    ]

    print()
    print("--- k=1 (mesonic resonances) ---")
    print(f"  {'Sector':<14} {'#':>3}  "
          f"{'a_fit':>10}  {'a_pred':>10}  {'Δa':>10}  "
          f"{'b_fit':>10}  {'b_pred':>10}  {'Δb':>10}")
    print("  " + "-" * 90)
    for label, P, Q, kap, q, a_fit, b_fit, n in K1_FITS:
        a_pred, b_pred = predict(1, P, Q, kap, q)
        print(f"  {label:<14} {n:>3}  "
              f"{a_fit:>+10.4f}  {a_pred:>+10.4f}  {a_fit - a_pred:>+10.3e}  "
              f"{b_fit:>+10.4f}  {b_pred:>+10.4f}  {b_fit - b_pred:>+10.3e}")

    print()
    print("--- k=2 (baryonic resonances) ---")
    print(f"  {'Sector':<18} {'#':>3}  "
          f"{'a_fit':>10}  {'a_pred':>10}  {'Δa':>10}  "
          f"{'b_fit':>10}  {'b_pred':>10}  {'Δb':>10}")
    print("  " + "-" * 92)
    for label, P, Q, kap, q, a_fit, b_fit, n in K2_FITS:
        a_pred, b_pred = predict(2, P, Q, kap, q)
        print(f"  {label:<18} {n:>3}  "
              f"{a_fit:>+10.4f}  {a_pred:>+10.4f}  {a_fit - a_pred:>+10.3e}  "
              f"{b_fit:>+10.4f}  {b_pred:>+10.4f}  {b_fit - b_pred:>+10.3e}")


if __name__ == "__main__":
    main()
