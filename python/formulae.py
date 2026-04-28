"""
Heim's 1989 mass formula — Python port of Eli Gildish's 2006 C implementation.

All function semantics, intermediate variables and numerical conventions
mirror the C reference (`/home/mike/claude/heim/annotated/src/formulae.c`).
Cross-references in [B##] form point to "Heim's Mass Formula (1989), IGW
Innsbruck 2002/2003" (file F_1989_en.pdf), cited as [1989].

Key indexing note: the C code uses 1-based arrays (via the pointer-minus-1
trick). This port uses Python's natural 0-based indexing, so the mapping is

      C: I[1..4]  ↔  Python: I[0..3]   (Q_n, Q_m, Q_p, Q_σ)
      C: N[1..6]  ↔  Python: N[0..5]   (N_1 .. N_6)
      C: a[1..3]  ↔  Python: a[0..2]   (a_1, a_2, a_3)
      C: n[1..4]  ↔  Python: n[0..3]   (n, m, p, σ)

Variable name mapping (code → [1989] → meaning):
      eps      ε        time-helicity sign, ±1
      k        k        metrical/configuration index
      P        P        double iso-spin (P = 2 s)
      Q        Q        double angular momentum (Q = 2 J)
      kap      κ        doublet indicator, ∈ {0, 1}
      x        x        iso-spin multiplet identifier
      q_x      ε·q      signed elementary charge, q = |q_x|
      I        Q_n,…,Q_σ  four "structure constants" (eq. X of 1982)
      N        N_1..N_6   the "N-functions" (1982 eq. IX + [B8..B14])
      W        W_(N=0)    zone-occupation weight [B22]

EMPIRICALLY FITTED CONSTANTS (per Heim 1989, p. 19):
      ⁴√2       FOURTH_ROOT_2     in `calc_phi` / U-term in [B7]/[B50]
      (π/e)²    PI_OVER_E_SQR     in `calc_phi` / second additive piece [B7]
      4π/⁴√2    FOUR_PI_OVER_4RT2 in U / coefficient in [B50]
"""

from __future__ import annotations

from math import comb, cos, exp, fabs, log, pi, sqrt
from typing import Sequence

from constants import (
    eta as _eta,
    theta as _theta,
    alpha_plus, alpha_minus,
    alpha_fine_structure, mass_element,
)

# ---------------------------------------------------------------------------
# Empirically fitted constants from [1989] §5 ("concluding remarks", p. 19)
# ---------------------------------------------------------------------------
FOURTH_ROOT_2: float = 2.0 ** (1.0 / 4.0)               # ⁴√2          [FITTED #1]
PI_OVER_E_SQR: float = (pi / 2.718281828459045235) ** 2  # (π/e)²       [FITTED #2]
# We use a literal e value matching C's `exp(1.0)` to stay byte-identical.
import math as _m
_E_C = _m.exp(1.0)
PI_OVER_E_SQR = (pi / _E_C) ** 2
FOUR_PI_OVER_4RT2: float = 4.0 * pi / FOURTH_ROOT_2     # 4π/⁴√2       [FITTED #3]


# ---------------------------------------------------------------------------
# calc_charge — [B2], with α_Q from [B1]
# ---------------------------------------------------------------------------

def calc_charge(eps: int, k: int, P: int, Q: int, kap: int, x: int) -> float:
    """
    Electric charge quantum number from quantum numbers (eps, k, P, Q, kap, x).
    Implements [B2]:
        q_x = ½ · [ (P − 2x) · (1 − Q·κ·(2−k))
                   + ε · (k − 1 − Q·(1+κ)·(2−k))
                   + C ]
    with C derived from α_Q [B1] applied to both P and Q.

    Note: [B2] in the [1989] PDF reads "(P − 2x + 2)" while this code uses
    "(P − 2x)" — the multiplet-identifier x convention differs.
    """
    # α_P, α_Q angles — variant of [B1]: α_Q = π Q [Q + (P/2)]
    alp_P = pi * Q * (kap + comb(P, 2))
    alp_Q = pi * Q * (Q * (k - 1) + comb(P, 2))

    eps_P = eps * cos(alp_P)
    eps_Q = eps * cos(alp_Q)

    # Structure-distributor C ("strangeness" in [1989], divided by k)
    C = 2.0 * (eps_P * P + eps_Q * Q) * (k + kap - 1) / (k * (1 + kap))

    return (
        (P - 2.0 * x) * (1.0 - Q * kap * (2.0 - k))
        + eps * (k - 1.0 - Q * (1.0 + kap) * (2.0 - k))
        + C
    ) / 2.0


# ---------------------------------------------------------------------------
# calc_Q — Q_n, Q_m, Q_p, Q_σ  (eq. X of 1982; not redefined in [1989])
# ---------------------------------------------------------------------------

def calc_Q(k: int) -> tuple[int, int, int, int]:
    """
    Four "structure constants" depending only on k (z = 2^(k²)):
        Q_n = 3·z / 2
        Q_m = 2·z − 1
        Q_p = 2·(z + (−1)^k)
        Q_σ = z − 1

    For k=1: z=2  → (3, 3, 2, 1).
    For k=2: z=16 → (24, 31, 34, 15).
    """
    z = int(2.0 ** (k**2))
    Qn = 3 * z // 2
    Qm = 2 * z - 1
    Qp = 2 * (z + (-1) ** k)
    Qsig = z - 1
    return Qn, Qm, Qp, Qsig


# ---------------------------------------------------------------------------
# calc_N — N_1, N_2 (1982 eq. IX); N_3..N_6 ([B8]..[B14])
# ---------------------------------------------------------------------------

def calc_N(
    k: int, q: float, I: Sequence[int]
) -> tuple[float, float, float, float, float, float]:
    """
    Six functions of (k, q):
      N_1, N_2 — from 1982 eq. (IX), unchanged in 1989
      N_3      — [B8]
      N_4      — [B9]
      N_5      — [B10] using A [B11], N(k) [B12]
      N_6      — [B13] using N'(k) [B14]
    """
    eta00 = _eta(1, 0)
    eta_1k = _eta(1, k)
    eta_q1 = _eta(q, 1)
    eta_qk = _eta(q, k)
    th = _theta(eta00)
    th_q1 = _theta(eta_q1)
    alp_p = alpha_plus(eta00, th)
    alp_n = alpha_minus(eta00, th)

    z = 2.0 ** (k**2)
    u = 2.0 * pi * _E_C  # u = 2πe in [B8]

    H = sum(I)                               # H ≡ Q_n+Q_m+Q_p+Q_σ  [B24]
    I_1 = H + 0.5 * z * k * (-1) ** k        # ≈ N(k)  [B12]
    I_2 = H - 2.0 * k - 1.0                  # ≈ N'(k) [B14]

    # D = A from [B11]
    D = (8.0 / eta00) * (1.0 - alp_n / alp_p) * (1.0 - 3.0 * eta00 / 4.0)

    # N_1 — 1982 eq.(IX):  ½(1 + √η_qk)
    N1 = 0.5 * (1.0 + sqrt(eta_qk))

    # N_2 — 1982 eq.(IX):  2 / (3·η_qk)
    N2 = 2.0 / (3.0 * eta_qk)

    # N_3 — [B8]. N_3 = (2/k) · exp[…]
    N3 = exp(
        (k - 1.0)
        * (
            1.0
            - pi
            * ((1.0 - eta_qk) / (1.0 + sqrt(eta_q1)))
            * (
                1.0
                - u * (eta_q1 / th_q1) * (1.0 - alp_n / alp_p) * (1.0 - sqrt(eta00)) ** 2
            )
        )
        - (
            4.0
            / (3.0 * u)
            * (1.0 - sqrt(eta00)) ** 2
            * ((1.5 * u**2 / th) * (1.0 + sqrt(eta_q1)) / (1.0 - eta00) - 1.0)
        )
    ) * (2.0 / k)

    # N_4 — [B9]:  (4/k)·[1 + q·(k − 1)]
    N4 = 4.0 * (1.0 + q * (k - 1.0)) / k

    # N_5 — [B10] with D = A [B11]
    N5 = D + k * (k - 1.0) * 8.0 * z * I_1 * (
        D * (1.0 - sqrt(eta_qk)) / (1.0 + sqrt(eta_qk))
    ) ** 2

    # N_6 — [B13] with I_2 = N'(k) [B14], I_1 the N(k)-analog
    N6 = (
        (64.0 * k * eta00 * I[3])
        / (u * th)
        * (1.0 - alp_n / alp_p)
        * ((1.0 - sqrt(eta00)) / (1.0 + sqrt(eta00))) ** 2
        * (
            sqrt(k)
            * (k * k - 1.0)
            * I_1
            / sqrt(eta_1k)
            * (q - (1.0 - q) * I_2 / (I[0] * sqrt(eta_1k)))
            + (-1) ** (k + 1)
        )
    )

    return N1, N2, N3, N4, N5, N6


# ---------------------------------------------------------------------------
# calc_a — combinatorial coefficients a_1, a_2, a_3
# ---------------------------------------------------------------------------

def calc_a(
    eps: int,
    k: int,
    P: int,
    Q: int,
    kap: int,
    q_x: float,
    I: Sequence[int],
) -> tuple[float, float, float]:
    """
    Combinatorial coefficients used inside W [B22] via x [B27]:
        a_1 = [B30]
        a_2 = [B29]
        a_3 = [B31]
    "Y" below is the y'·2B bracket inside [B31].
    """
    q = fabs(q_x)
    eta00 = _eta(1, 0)
    H = sum(I)                                       # H [B24]
    B = 3.0 * H / (k * k * (2.0 * k - 1.0))          # B [B28]

    P2 = comb(P, 2)
    P3 = comb(P, 3)
    Q3 = comb(Q, 3)

    # a_1 — [B30]
    a1 = (
        1.0
        + B
        + k * (Q * Q + 1.0) * Q3
        - kap
        * ((B - 1.0) * (2.0 - k) - 3.0 * (P - Q) * (H - 2.0 * (1.0 + q)) + 1.0)
        - (1 - kap)
        * (
            (2.0 - k) * (3.0 * (2.0 - q) * P2 - Q * (3.0 * (P + Q) + q))
            + (k - 1.0)
            * (
                k * (P + 1.0) * P2
                + (1.0 + (B / k) * (k + P - Q)) * (1.0 - P2) * (1.0 - Q3)
                - q * (1.0 - q) * Q3
            )
        )
    )

    # a_2 — [B29]
    a2 = (
        B * (1.0 - Q3 * (1.0 - P3))
        + (6.0 / k)
        - kap
        * (
            0.5 * Q * (B - 7.0 * k)
            - (3.0 * q - 1.0) * (k - 1.0)
            + 0.5 * (P - Q) * (4.0 + (B + 1.0) * (1.0 - q))
        )
        - (1 - kap)
        * (
            (2.0 - k)
            * (
                P * (0.5 * B + q + 2.0)
                - Q * (0.5 * B + 1.0 - 4.0 * (1.0 + 4.0 * q))
            )
            + (k - 1.0)
            * (1.0 - Q3)
            * (
                0.25 * (B - 2.0) * (1.0 + 1.5 * (P - Q))
                - 0.5 * B * (1 - q)
                - P2
                * (
                    (2.0 - eps * q_x)
                    * (0.5 * (B + q - eps * q_x) + 3.0 * eps * q_x)
                    - 0.25 * (B + 2.0) * (1.0 - q)
                )
            )
            - P3
            * (
                2.0 * (1.0 + eps * q_x)
                + 0.5 * (2.0 - q) * (3.0 * (1.0 - q) + eps * q_x - q)
                - 0.25 * q * (1.0 - q) * (B - 4.0)
                - 0.25 * (B - 2.0)
                + 0.5 * B * (1.0 - q)
            )
        )
    )

    # Y — y'·2B inside [B31]
    Y = (
        kap
        * (
            (sqrt(eta00) / k)
            * (
                4.0 * (2.0 - sqrt(eta00))
                - pi * _E_C * sqrt(eta00) * (1.0 - eta00)
            )
            * (k + _E_C * sqrt(eta00) * (k - 1.0))
            + 5.0 * (1.0 - q) * (4.0 * B + P + Q) / (2.0 * k + (-1) ** k)
        )
        + (1 - kap)
        * (
            (P - 1.0) * (P - 2.0) * (2.0 / (k * k) * (H + 2.0) + 0.5 * (2.0 - k) / pi)
            + P2
            * (1.0 - Q3)
            * (
                0.5 * q * B * (B + 2.0 * (P - Q))
                + (k - 1)
                * (
                    P * (P + 2.0) * B
                    + (P + 1.0) ** 2
                    - q
                    * (1.0 + eps * q_x)
                    * (
                        k * (P * P + 1.0) * (B + 2.0)
                        + 0.25 * (P * P + P + 1.0)
                    )
                    - q * (1.0 - eps * q_x) * (B + P * P + 1.0)
                )
                + (
                    (P - Q) * (H + 2.0)
                    + P
                    * (
                        5.0 * B * (1.0 + q) * Q
                        + k
                        * (k - 1.0)
                        * (
                            k * (P + Q) ** 2 * (H + 3.0 * k + 1.0) * (1.0 - q)
                            - 0.5 * (B + 6.0 * k)
                        )
                    )
                )
                * (1.0 - P2)
                * (1.0 - Q3)
                + P3
                * (2.0 - q)
                * Q
                * (
                    eps * q_x * (B + 2.0 * Q + 1.0)
                    + (0.5 * q / k) * (1.0 - eps * q_x) * (2.0 * k + 1.0)
                    + (1.0 - q) * (Q * Q + 2.0 * B + 1.0)
                )
            )
        )
    )

    Y = 0.5 * Y / B

    # a_3 — [B31]
    a3 = (4.0 * B * Y / (Y + 1)) - (1.0 / (B + 4.0))

    return a1, a2, a3


# ---------------------------------------------------------------------------
# calc_W — W_(N=0) from [B22]
# ---------------------------------------------------------------------------

def calc_W(
    eps: int,
    k: int,
    P: int,
    Q: int,
    kap: int,
    q_x: float,
    I: Sequence[int],
) -> float:
    """
    Zone-occupation weight W_(N=0) — [B22]:
        W = A · e^x · (1 − η)^L
            + (P − Q)·(1 − (P 2))·(1 − (Q 3))·(1 − √η)²·√2
    with A [B23], L [B26], x [B27], B [B28].
    """
    eta00 = _eta(1, 0)
    P2 = comb(P, 2)
    Q3 = comb(Q, 3)

    H = sum(I)                                             # H [B24]

    # g [B25] — uses I[0]^3 (Q_n^3). The IGW Innsbruck PDF prints "Q_n^2"
    # in [B25], but Heim's own research-group C# code uses Q_n^3 (verified
    # in downloads/csharp_impl/.../HeimGroup/SelfCouplingFunction.cs).
    # The PDF has a typesetting error; Q_n^3 is the correct exponent.
    g = (
        I[0] ** 3.0
        + I[1] ** 2.0
        + I[2] * exp(k - 1.0) / k
        + exp((1.0 - 2.0 * k) / 3.0)
        - (k - 1.0) * H
    )

    A = 8.0 * g * H / (2.0 - k + 8 * H * (k - 1.0))        # A [B23]
    B = 3.0 * H / (k * k * (2.0 * k - 1.0))                # B [B28]

    a = calc_a(eps, k, P, Q, kap, q_x, I)

    # x [B27]: (1 − Q − (P 2))·(2 − k) + (1/4B)·[a_1 + (k³/4H)·(a_2 + a_3/4B)]
    X = (2.0 - k) * (1 - Q - P2) + (
        a[0] + k**3.0 * (a[1] + a[2] / (4.0 * B)) / (4.0 * H)
    ) / (4.0 * B)

    # W [B22], L = Q·(1 − κ)·(2 − k) [B26]
    return A * exp(X) * (1.0 - eta00) ** (Q * (1.0 - kap) * (2.0 - k)) + sqrt(2.0) * (
        P - Q
    ) * (1.0 - P2) * (1.0 - Q3) * (1.0 - sqrt(eta00)) ** 2


# ---------------------------------------------------------------------------
# calc_n — exhaustion algorithm of [B40..B46]
# ---------------------------------------------------------------------------

def calc_n(
    k: int, I: Sequence[int], N: Sequence[float], W: float
) -> tuple[int, int, int, int]:
    """
    Greedy decomposition of W into the four occupation numbers (n, m, p, σ).
    Implements [B42]–[B46]:

        K_n = ⌊(W/α₁)^(1/3)⌋
        K_m = ⌊√(w₁/α₂)⌋
        K_p = ⌊w₂/α₃⌋
        K_σ from exponential remainder
        n = K_n − Q_n, m = K_m − Q_m, p = K_p − Q_p, σ = K_σ − Q_σ

    α₁ = N_1, α₂ = (3/2)·N_2, α₃ = (1/2)·N_3.
    """
    K = [0, 0, 0, 0]
    w = [0.0, 0.0, 0.0, 0.0]
    alp = [N[0], N[1] * 1.5, N[2] * 0.5]                   # α_1, α_2, α_3

    # Step 1 — cubic [B42]
    w[0] = W
    K[0] = int((w[0] / alp[0]) ** (1.0 / 3.0) + 0.01)

    # Step 2 — quadratic [B43]
    w[1] = w[0] - alp[0] * K[0] ** 3.0
    K[1] = int(sqrt(w[1] / alp[1]) + 0.01)

    # Step 3 — linear [B44]
    w[2] = w[1] - alp[1] * K[1] ** 2.0
    K[2] = int(w[2] / alp[2] + 0.01)

    # Step 4 — exponential remainder [B45], β = (2k − 1)/(3·Q_σ)
    w[3] = w[2] - alp[2] * K[2]

    if w[3] <= 0.0:
        K[3] = int(alp[2] * K[2] + 0.01)
    elif w[3] > 1.0:
        K[3] = int(-3.0 * I[3] * log(w[3]) / (2.0 * k - 1.0) + 0.01)
        K[2] -= 1
        K[3] += int(alp[2] * K[2])
    else:
        K[3] = int(-3.0 * I[3] * log(w[3]) / (2.0 * k - 1.0) + 0.01)

    # [B46]:  n_i = K_i − Q_i  (the "−1" is absorbed into the K-shift)
    return K[0] - I[0], K[1] - I[1], K[2] - I[2], K[3] - I[3]


# ---------------------------------------------------------------------------
# calc_phi — self-coupling φ from [B7] / [B49] (contains all 3 fitted constants)
# ---------------------------------------------------------------------------

def calc_phi(
    k: int,
    P: int,
    Q: int,
    kap: int,
    q_x: float,
    n: Sequence[int],
    I: Sequence[int],
    N: Sequence[float],
    W: float,
) -> float:
    """
    Self-coupling function φ from [B7] / [B49]:

        φ = [N_4·p² / (1+p²)] · [(σ + Q_σ) / √(1 + σ²)] · [⁴√2 − 4·B·U·W^(−1)]
            + P·(P − 2)²·(1 + κ·(1−q)/(2αθ))·(π/e)²·√η_12·(Q_m − Q_n)
            − (P + 1)·(Q 3) / α

    with U from [B50]:

        U = 2^Z · [P² + (3/2)(P−Q) + P(1−q) + 4κB(1−Q)/(3−2q)
                   + (k−1){P + 2Q − (4π/⁴√2)·(P−Q)·(1−q)}] · η_qk^(−2)

    and Z = k + P + Q + κ from [B51].

    ⚠ Contains all three EMPIRICALLY FITTED constants:
         FOURTH_ROOT_2  (⁴√2)         [FITTED #1]
         PI_OVER_E_SQR  ((π/e)²)      [FITTED #2]
         FOUR_PI_OVER_4RT2 (4π/⁴√2)   [FITTED #3]
    """
    q = fabs(q_x)
    alpha = alpha_fine_structure()
    eta12 = _eta(1, 2)
    eta_qk = _eta(q, k)
    th = _theta(_eta(1, 0))

    H = sum(I)
    B = 3.0 * H / (k * k * (2.0 * k - 1.0))

    # U — [B50]; Z = k + P + Q + κ from [B51]
    U = (
        P * P
        + 1.5 * (P - Q)
        + P * (1.0 - q)
        + (1.0 - Q) * 4.0 * kap * B / (3.0 - 2.0 * q)
        + (k - 1.0)
        * (
            P
            + 2.0 * Q
            - FOUR_PI_OVER_4RT2          # [FITTED #3]: 4π/⁴√2
            * (P - Q)
            * (1.0 - q)
        )
    ) * 2.0 ** (k + P + Q + kap) / (eta_qk * eta_qk)

    # φ — three additive pieces of [B7]
    return (
        (n[2] * n[2] * N[3])
        / (1.0 + n[2] * n[2])
        * (n[3] + I[3])
        / sqrt(1.0 + n[3] * n[3])
        * (FOURTH_ROOT_2 - 4.0 * B * U / W)   # [FITTED #1]: ⁴√2
        - (P + 1) * comb(Q, 3) / alpha
        + P
        * (P - 2.0) ** 2
        * (I[1] - I[0])
        * sqrt(eta12)
        * (1.0 + kap * (1.0 - q) / (2.0 * alpha * th))
        * PI_OVER_E_SQR                       # [FITTED #2]: (π/e)²
    )


# ---------------------------------------------------------------------------
# calc_mass — main mass formula M = [B3]  (returns kg)
# ---------------------------------------------------------------------------

def calc_mass(eps: int, k: int, P: int, Q: int, kap: int, q_x: float) -> float:
    """
    Particle rest mass from quantum numbers, in kilograms.

    M = μ · α_+ · [(G_underline + S + F + Φ) + 4·q·α_-]                   [B3]

    where:
        G_underline (called "K" in the upstream code) — same shape as S but
                    with n,m,p,σ instead of Q_n,Q_m,Q_p,Q_σ
        S          — uses Q_n,…,Q_σ; depends only on k
        F          — cross terms n_i·Q_i + φ (self-coupling)              [B5]
        Φ          — P·(−1)^(P+Q)·(P+Q)·N_5 + Q·(P+1)·N_6                  [B6]

    The "+ 4·q·α_-" is the principal addition of 1989 over 1982.
    """
    q = fabs(q_x)
    eta00 = _eta(1, 0)
    th = _theta(eta00)

    I = calc_Q(k)                                   # Q_n, Q_m, Q_p, Q_σ
    N = calc_N(k, q, I)                              # N_1..N_6
    W = calc_W(eps, k, P, Q, kap, q_x, I)            # W_(N=0) [B22]
    n = calc_n(k, I, N, W)                           # (n, m, p, σ) [B40-B46]

    # K = "occupation contribution" — G_underline shape with n_i
    K = (
        (n[0] * (n[0] + 1.0)) ** 2.0 * N[0]
        + n[1] * (2.0 * n[1] ** 2 + 3.0 * n[1] + 1.0) * N[1]
        + n[2] * (n[2] + 1.0) * N[2]
        + 4.0 * n[3]
    )

    # S = "structure-constant contribution" — same shape with I_i
    S = (
        (I[0] * (I[0] + 1.0)) ** 2.0 * N[0]
        + I[1] * (2.0 * I[1] ** 2 + 3.0 * I[1] + 1.0) * N[1]
        + I[2] * (I[2] + 1.0) * N[2]
        + 4.0 * I[3]
    )

    # F — [B5]: cross terms + self-coupling φ
    F = (
        2.0
        * n[0]
        * I[0]
        * (
            1.0
            + 3.0 * (n[0] + I[0] + n[0] * I[0])
            + 2.0 * (n[0] ** 2 + I[0] ** 2)
        )
        * N[0]
        + 6.0 * n[1] * I[1] * (1.0 + n[1] + I[1]) * N[1]
        + 2.0 * n[2] * I[2] * N[2]
        + calc_phi(k, P, Q, kap, q, n, I, N, W)
    )

    # Φ — [B6]: capital-Phi piece, distinct from φ
    PHI = P * (-1) ** (P + Q) * (P + Q) * N[4] + Q * (P + 1) * N[5]

    return (
        mass_element()
        * alpha_plus(eta00, th)
        * (K + S + F + PHI + 4.0 * q * alpha_minus(eta00, th))
    )


__all__ = [
    "FOURTH_ROOT_2", "PI_OVER_E_SQR", "FOUR_PI_OVER_4RT2",
    "calc_charge", "calc_Q", "calc_N", "calc_a", "calc_W",
    "calc_n", "calc_phi", "calc_mass",
]
