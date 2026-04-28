"""
Heim 1989 mean-lifetime formula for elementary basic states.

Implements equations [B47]–[B57] of the IGW Innsbruck reformulation
(file `downloads/pdfs/F_1989_en.pdf`). These compute T = mean lifetime
in seconds, as a function of the same six integer quantum numbers
(eps, k, P, Q, kap, x) that determine the mass.

⚠ This is a fresh implementation with no upstream reference to verify
against — Eli Gildish's C/C# port covers only masses. Therefore the
formulas here are transcribed *literally* from the PDF, with each line
tagged by its [B##]; any disagreement with experiment most likely
indicates either a transcription error here or an ambiguity in the
1989 source text. Known typography ambiguities are flagged in the
comments below.

For the basic state (N = 0), δ = 1 and T_N = 0, so T equals the right-hand
side of [B47] directly. Excited states (N > 0) are not implemented.
"""

from __future__ import annotations

from math import comb, fabs, pi, sqrt

from constants import (
    C_LIGHT, H_PLANCK,
    eta as _eta, theta as _theta,
    alpha_plus, alpha_minus, alpha_fine_structure,
)
import constants as const_mod
import formulae

# Use module-level lookups so monkey-patches (sensitivity scripts) are honoured.
# We deliberately reach through `formulae` for FOURTH_ROOT_2 etc. because that
# is where the perturbation harness expects them to live.


# ---------------------------------------------------------------------------
# Strangeness / structure-distributor C — used in [B52]–[B55]
# ---------------------------------------------------------------------------

def calc_C(eps: int, k: int, P: int, Q: int, kap: int) -> float:
    """
    The structure-distributor C from [B2] (mass-formula chapter), already
    divided by k as required by the [1989] introduction note. This is the
    same C that appears unchanged in [B52]–[B55].
    """
    alp_P = pi * Q * (kap + comb(P, 2))
    alp_Q = pi * Q * (Q * (k - 1) + comb(P, 2))
    eps_P = eps * _eta_local_cos(alp_P)
    eps_Q = eps * _eta_local_cos(alp_Q)
    return 2.0 * (eps_P * P + eps_Q * Q) * (k + kap - 1) / (k * (1 + kap))


def _eta_local_cos(x):
    # Kept as a thin wrapper so future tracing/inspection can hook here.
    from math import cos
    return cos(x)


# ---------------------------------------------------------------------------
# β₀ — [B56]
# ---------------------------------------------------------------------------

def beta_0() -> float:
    """β₀ = (2α / (πe)) · ((1 − √η) / (1 + √η))²    [B56]"""
    eta00 = _eta(1, 0)
    alpha = alpha_fine_structure()
    from math import e as euler_e
    return (
        2.0 * alpha / (pi * euler_e)
        * ((1.0 - sqrt(eta00)) / (1.0 + sqrt(eta00))) ** 2
    )


# ---------------------------------------------------------------------------
# D — [B57]
# ---------------------------------------------------------------------------

def calc_D(eps: int, P: int, q_x: float) -> float:
    """
    D = [1 + 4q²(q−1)(2q+1)]^(−1) · η · β₀ · (1−√η)⁴ · P^(2+εq) ·
        (P−1)^((q−1)q/2) / (3√2)                                  [B57]

    For q = 0: factor = 1, exponent on P = 2, exponent on (P−1) = 0
    For q = 1: factor = 1, exponent on P = 2+ε, exponent on (P−1) = 0
    For q = 2: factor = 1/81, exponent on P = 2+2ε, exponent on (P−1) = 1
    """
    q = fabs(q_x)
    eta00 = _eta(1, 0)
    b0 = beta_0()

    inv_factor = 1.0 + 4.0 * q * q * (q - 1) * (2.0 * q + 1.0)
    p_exp = 2.0 + eps * q
    pm1_exp = (q - 1) * q / 2.0

    # Handle P=0 with non-zero exponent gracefully (zero^0 = 1 by Python convention)
    p_term = P ** p_exp if P != 0 else (1.0 if p_exp == 0 else 0.0)
    pm1_term = (P - 1) ** pm1_exp if P != 1 else (1.0 if pm1_exp == 0 else 0.0)

    return (
        (1.0 / inv_factor)
        * eta00
        * b0
        * (1.0 - sqrt(eta00)) ** 4
        * p_term
        * pm1_term
        / (3.0 * sqrt(2.0))
    )


# ---------------------------------------------------------------------------
# F — [B52]
# ---------------------------------------------------------------------------

def calc_F(eps: int, k: int, P: int, Q: int, kap: int, q_x: float) -> float:
    """
    F = 1 − (1/3)(1−q)(P−1)²(3−P)·(1 + P + Q − εCP/2)·(1 + β₀·(−1)^k)
        − (P,3)·(1 + D)                                                [B52]
    """
    q = fabs(q_x)
    C = calc_C(eps, k, P, Q, kap)
    D = calc_D(eps, P, q_x)
    b0 = beta_0()

    # [B52]: F = 1 - (1/3)(1-q)(P-1)²(3-P)·(1 + P − Q − εCP/2)·(1 + β_0(−1)^k)
    #            − (P,3)(1 + D)
    # NB: (1 + P − Q − εCP/2), with MINUS Q. Earlier had +Q from a misread.
    return (
        1.0
        - (1.0 / 3.0)
        * (1.0 - q)
        * (P - 1) ** 2
        * (3 - P)
        * (1.0 + P - Q - eps * C * P / 2.0)
        * (1.0 + b0 * ((-1) ** k))
        - comb(P, 3) * (1.0 + D)
    )


# ---------------------------------------------------------------------------
# s — [B53]
# ---------------------------------------------------------------------------

def calc_s(eps: int, k: int, P: int, Q: int, kap: int) -> float:
    """
    s = 2 − k + εC + (2kQ − κP) + (Q,3)·(1/k)·(P−1)(P−2)(P−3)        [B53]

    Note: only s mod 2 matters in [B48] (it appears as (−1)^s).
    For our reference particles with P ≤ 3, the trailing
    (P−1)(P−2)(P−3) factor is always zero.
    """
    C = calc_C(eps, k, P, Q, kap)
    return (
        2 - k
        + eps * C
        + (2 * k * Q - kap * P)
        + comb(Q, 3) * (1.0 / k) * (P - 1) * (P - 2) * (P - 3)
    )


# ---------------------------------------------------------------------------
# b₁ — [B54]
# ---------------------------------------------------------------------------

def calc_b1(
    eps: int, k: int, P: int, Q: int, kap: int, q_x: float, I, B: float
) -> float:
    """
    b₁ = [P{7 + 6(1−q)(C − (P,2)) − 2q(1 − (P,2))} + κQ(3Z−1)·B + 1]·(2−k)
         + (1/2)(1−κ)·{(q − εq_x − 2)·Q + εCP + 2(P+1)
                       − (1−q)·P(P−3) / (1 + P(P²−1))·(4B − 6 + P)}·(k−1)
         − (P,3)·(q − εq_x)                                              [B54]

    Z from [B51] = k + P + Q + κ.
    """
    q = fabs(q_x)
    C = calc_C(eps, k, P, Q, kap)
    Z = k + P + Q + kap
    P2 = comb(P, 2)
    P3 = comb(P, 3)

    # [B54] first bracket: [P·{…} + κQ·{(3Z−1)B + 1}]·(2−k)
    # The "+1" is INSIDE the κQ braces, so the inner factor is κQ·((3Z−1)B + 1)
    # = κQ(3Z−1)B + κQ. Earlier had "+1" outside the braces.
    term_first = (
        P * (7 + 6 * (1 - q) * (C - P2) - 2 * q * (1 - P2))
        + kap * Q * ((3 * Z - 1) * B + 1)
    ) * (2 - k)

    # Avoid division by zero when 1 + P(P²−1) = 0 (P = 0 → 1; P = 1 → 1; P = 2 → 7;
    # but for any plausible P, this factor is positive)
    denom = 1 + P * (P * P - 1)
    inner = (
        (q - eps * q_x - 2) * Q
        + eps * C * P
        + 2 * (P + 1)
        - (1 - q) * P * (P - 3) / denom * (4 * B - 6 + P)
    )
    term_second = 0.5 * (1 - kap) * inner * (k - 1)

    term_third = -P3 * (q - eps * q_x)

    return term_first + term_second + term_third


# ---------------------------------------------------------------------------
# b₂ — [B55]
# ---------------------------------------------------------------------------

def calc_b2(
    eps: int, k: int, P: int, Q: int, kap: int, q_x: float, I, B: float, H: float
) -> float:
    """
    b₂ — eq. [B55]. Verbose; transcribed line by line from the PDF.

    Ambiguities flagged inline.
    """
    from math import e as euler_e
    q = fabs(q_x)
    C = calc_C(eps, k, P, Q, kap)
    eta00 = _eta(1, 0)
    eta22 = _eta(2, 2)
    P2 = comb(P, 2)
    P3 = comb(P, 3)

    # Line 1:  B(5B+3) + (2H−3)/(P+1)
    line1 = B * (5 * B + 3) + (2 * H - 3) / (P + 1)

    # Line 2:  C^k · {B·(3B + 2(H+1)) + H + 1/2} · (1 − q)
    # Earlier (image-based) read had three errors here: (·H instead of +H),
    # (+H/2 instead of +1/2), and (+3 instead of nothing). Machine-extracted
    # PDF text shows: "Ck{B( 3B+2(H+1)) + H + ½}(1 - q)".
    line2 = (C ** k) * (B * (3 * B + 2 * (H + 1)) + H + 0.5) * (1 - q)

    # Line 3:  − Q · {B(2(B+H) − 1) + H/2 + 3}
    line3 = -Q * (B * (2 * (B + H) - 1) + H / 2 + 3)

    # Line 4:  + κq · {B(3B+1) − 5/2} · (k − Q)
    line4 = kap * q * (B * (3 * B + 1) - 5.0 / 2.0) * (k - Q)

    # Line 5:  − (P,2)·P²(P+Q)²·[8B + 1 − {5B − (2H+1)·(1 + 2(P,3) − Q) + 2}·q]
    bracket5 = 8 * B + 1 - (5 * B - (2 * H + 1) * (1 + 2 * P3 - Q) + 2) * q
    line5 = -P2 * P * P * (P + Q) ** 2 * bracket5

    # Line 6:  − (P,2)·H·(1 − q)
    line6 = -P2 * H * (1 - q)

    # Line 7:  − (B − 3/4)² · (P−1)(P−2)(P−3) · (−1)^(k−1)
    line7 = -((B - 0.75) ** 2) * (P - 1) * (P - 2) * (P - 3) * ((-1) ** (k - 1))

    # Line 8:  + (Q − q)(1 − q + Bq) · {3(H+B) + π·e/η − q/4} · (P+1)³ · (k−1)
    line8 = (
        (Q - q)
        * (1 - q + B * q)
        * (3 * (H + B) + pi * euler_e / eta00 - q / 4)
        * (P + 1) ** 3
        * (k - 1)
    )

    # Line 9:  + κ · {  (−1)^(1−q) · [7HB + 3(H+B) − 5/2 + (1−q){H(3B−4) + B+7/2}]·(k−1)
    # Earlier had (-1)^q, which is the negation of the correct expression
    # for q ∈ {0, 1, 2}. Now corrected to (-1)^(1−q).
    qi = int(round(q))
    line9_a = (
        ((-1) ** (1 - qi))
        * (
            7 * H * B
            + 3 * (H + B)
            - 5.0 / 2.0
            + (1 - q) * (H * (3 * B - 4) + B + 3.5)
        )
        * (k - 1)
    )

    # Line 10:  + Q(P,2) · { (2−q)(1+εq_x)·[B/(2(H+2)) + 3/4]
    #                       + (5/2)·HB + 3H − (B+5)/(P+1) }   }
    # Machine-extracted text confirms the bracket is [B/2(H+2) + ¾],
    # i.e. B/(2(H+2)) PLUS 3/4 (not B over the whole "2(H+2) + 3/4").
    # Earlier reading grouped 3/4 into the denominator — corrected.
    line9_b = (
        Q * P2 * (
            (2 - q) * (1 + eps * q_x) * (B / (2 * (H + 2)) + 0.75)
            + (5.0 / 2.0) * H * B
            + 3 * H
            - (B + 5) / (P + 1)
        )
    )
    line9 = kap * (line9_a + line9_b)

    # Line 11:  − (5/2) · H² · (P,3) · {q · (1 + π/3 · (2−q) · η₂,₂)·B − (2−q)(1−q)}
    line11 = (
        -(5.0 / 2.0)
        * H * H
        * P3
        * (q * (1.0 + pi / 3.0 * (2 - q) * eta22) * B - (2 - q) * (1 - q))
    )

    return line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9 + line11


# ---------------------------------------------------------------------------
# y — [B48]
# ---------------------------------------------------------------------------

def calc_y(
    eps: int, k: int, P: int, Q: int, kap: int, q_x: float,
    phi: float, W: float, I, H: float, B: float
) -> float:
    """
    y = F · [φ + (−1)^s · (1 + φ) · (b₁ + b₂ / W_(N=0))]                [B48]
    """
    F = calc_F(eps, k, P, Q, kap, q_x)
    s = calc_s(eps, k, P, Q, kap)
    b1 = calc_b1(eps, k, P, Q, kap, q_x, I, B)
    b2 = calc_b2(eps, k, P, Q, kap, q_x, I, B, H)

    sign_s = (-1.0) ** int(round(s))    # only parity matters

    return F * (phi + sign_s * (1.0 + phi) * (b1 + b2 / W))


# ---------------------------------------------------------------------------
# T — [B47]   the lifetime itself, in seconds
# ---------------------------------------------------------------------------

def calc_lifetime_seconds(
    eps: int, k: int, P: int, Q: int, kap: int, q_x: float, mass_kg: float
) -> float:
    """
    Mean lifetime T (basic state, N = 0) in seconds, per [B47]:

        T = 192·h·H·y / [M·c²·η₂,₂·(1−√η)²·(1−√η₁,₁)²·(1−√η₁,₂)² ·
                          (H + n + m + p + σ) · (n + |m| + |p|·β₀)]

    Returns +∞ if (n + |m| + |p|·β₀) = 0 (the case for stable basic states
    such as the proton and electron).
    """
    eta00 = _eta(1, 0)
    eta11 = _eta(1, 1)
    eta12 = _eta(1, 2)
    eta22 = _eta(2, 2)
    b0 = beta_0()

    I = formulae.calc_Q(k)                                 # Q_n, Q_m, Q_p, Q_σ
    H = sum(I)                                             # [B24]
    Bk = 3.0 * H / (k * k * (2.0 * k - 1.0))               # [B28]
    N = formulae.calc_N(k, fabs(q_x), I)                    # N_1..N_6
    W = formulae.calc_W(eps, k, P, Q, kap, q_x, I)          # W_(N=0)
    n = formulae.calc_n(k, I, N, W)                        # (n, m, p, σ)
    phi = formulae.calc_phi(k, P, Q, kap, q_x, n, I, N, W)  # self-coupling

    y = calc_y(eps, k, P, Q, kap, q_x, phi, W, I, H, Bk)

    # Denominator factors
    eta_factor = (
        eta22
        * (1.0 - sqrt(eta00)) ** 2
        * (1.0 - sqrt(eta11)) ** 2
        * (1.0 - sqrt(eta12)) ** 2
    )
    sum_HQn = H + n[0] + n[1] + n[2] + n[3]
    # [B47]:  (n + m + p·β_0)  — note: NO absolute values around m, p.
    # An earlier reading had |m|, |p|·β_0 (from a misread of the visual
    # PDF rendering); the machine-extracted text confirms plain n + m + p·β_0.
    occupancy = n[0] + n[1] + n[2] * b0

    if occupancy == 0.0:
        return float("inf")

    return (
        192.0 * H_PLANCK * H * y
        / (mass_kg * C_LIGHT * C_LIGHT * eta_factor * sum_HQn * occupancy)
    )


__all__ = [
    "calc_C", "beta_0", "calc_D", "calc_F", "calc_s",
    "calc_b1", "calc_b2", "calc_y", "calc_lifetime_seconds",
]
