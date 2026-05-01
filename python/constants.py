"""
Physical constants and Heim-theory auxiliary functions.

Port of constant.{h,c} from Eli Gildish's 2006 C implementation, with
cross-references to "Heim's Mass Formula (1989), IGW Innsbruck 2002/2003"
[F_1989_en.pdf], cited as [1989].

The auxiliary functions η, θ, α_±, α (fine structure), and μ provide the
dimensionless scaffolding that the mass formula in `formulae.py` operates
on. None of these depends on a particle's quantum numbers.
"""

from __future__ import annotations

from math import e, pi, sqrt

# ---------------------------------------------------------------------------
# Physical constants — switchable mode
# ---------------------------------------------------------------------------
#
# Two modes are supported:
#
#   "legacy_2006"  (default)  CODATA-2006-era values, matching the
#                             C reference implementation by Eli Gildish.
#                             Use this for bit-identical reproduction.
#
#   "codata_2022"             Current CODATA values (NIST 2022 edition,
#                             which is identical to the post-2019 SI
#                             redefinition for h, e, c, k_B, N_A — those
#                             are now defined exact).
#
# Switch modes with `set_constants_mode("codata_2022")` BEFORE constructing
# Particle objects or running the formula. Re-importing the module is not
# required.
#
# Numerical effect: masses change by O(10⁻⁵) — i.e., much smaller than
# Heim's quoted accuracy. The two modes therefore give predictions that
# agree to ~5 decimal places. This is the right behaviour: the formula's
# essential content lives in geometry, not in tiny constant updates.

_CONSTANT_MODES = {
    "legacy_2006": {
        # Values frozen at the C-reference implementation (Eli Gildish 2006)
        "C_LIGHT":           299_792_458.0,         # m/s, defined exact
        "G":                 6.6742e-11,            # m³·kg⁻¹·s⁻²
        "ELEMENTARY_CHARGE": 1.60217653e-19,        # C
        "H_PLANCK":          6.6260693e-34,         # J·s
        "KG_TO_MEV":         5.609588357e+29,       # kg → MeV/c²
    },
    "codata_2022": {
        # Current best NIST CODATA values. Note: c, h, e, k_B, N_A are
        # exact since the 2019 SI redefinition; G has 22 ppm uncertainty.
        "C_LIGHT":           299_792_458.0,         # m/s, defined exact
        "G":                 6.67430e-11,           # m³·kg⁻¹·s⁻² (uncertainty 0.00015e-11)
        "ELEMENTARY_CHARGE": 1.602176634e-19,       # C, defined exact
        "H_PLANCK":          6.62607015e-34,        # J·s, defined exact
        "KG_TO_MEV":         1.0 / 1.78266192e-30,  # exact derived: 1/(MeV/c² in kg)
    },
}

C_LIGHT: float
G: float
ELEMENTARY_CHARGE: float
H_PLANCK: float
H_BAR: float
KG_TO_MEV: float

MU_0: float
EPS_0: float

_active_mode = "legacy_2006"


def set_constants_mode(mode: str) -> None:
    """
    Set the physical-constant set used by the Heim mass and lifetime
    formulas. Must be called before computing any particle properties
    (or call it and then re-evaluate as needed; constants are read at
    call time, not at import time).
    """
    global C_LIGHT, G, ELEMENTARY_CHARGE, H_PLANCK, H_BAR, KG_TO_MEV
    global MU_0, EPS_0, _active_mode

    if mode not in _CONSTANT_MODES:
        raise ValueError(
            f"Unknown constants mode: {mode!r}. "
            f"Available: {list(_CONSTANT_MODES)}"
        )
    vals = _CONSTANT_MODES[mode]
    C_LIGHT           = vals["C_LIGHT"]
    G                 = vals["G"]
    ELEMENTARY_CHARGE = vals["ELEMENTARY_CHARGE"]
    H_PLANCK          = vals["H_PLANCK"]
    KG_TO_MEV         = vals["KG_TO_MEV"]
    H_BAR             = 0.5 * H_PLANCK / pi
    MU_0              = 4.0e-7 * pi
    EPS_0             = 1.0 / MU_0 / (C_LIGHT * C_LIGHT)
    _active_mode      = mode


def get_constants_mode() -> str:
    """Return the currently active constants mode."""
    return _active_mode


# Initialise to legacy_2006 (preserves bit-equality with the C reference).
set_constants_mode("legacy_2006")

S_0: float = 1.0                        # m, gauge length


# ---------------------------------------------------------------------------
# Heim-theory auxiliary functions
# ---------------------------------------------------------------------------

def eta(q: float, k: int) -> float:
    """
    η(q, k) — auxiliary function from 1982 eq. (I).

        η(q, k) = ⁴√(π⁴ / (π⁴ + (4 + k)·q⁴))

    Properties:
      • η(0, k) = 1                           (zero-charge limit)
      • η(1, 0) ≈ 0.98999  (the canonical "η")
      • η(1, 1) ≈ 0.98770
      • η(1, 2) ≈ 0.98519

    The (4 + k) coefficient and the quartic q-dependence are not derived
    in any publicly available Heim manuscript — they appear as a definition.
    """
    return (pi**4 / (pi**4 + (4.0 + k) * q**4)) ** 0.25


def theta(eta_val: float) -> float:
    """
    θ(η) — auxiliary, from 1982 eq. (I):  θ = 5η + 2√η + 1.
    For η ≈ 0.99: θ ≈ 7.94.
    """
    return 5.0 * eta_val + 2.0 * sqrt(eta_val) + 1.0


def alpha_plus(eta_val: float, theta_val: float) -> float:
    """
    α₊ from [B4]:

        α₊ = (⁶√η / η²) · ( 1 − θ · √(2η) · [2(1 − √η) / (η·(1 + √η))]² ) − 1

    Note: pow(η, -11/6) = ⁶√η / η².  For η ≈ 0.99: α₊ ≈ 0.0183.
    """
    return (
        eta_val ** (-11.0 / 6.0)
        * (
            1.0
            - theta_val
            * sqrt(2.0 * eta_val)
            * ((2.0 * (1.0 - sqrt(eta_val))) / (eta_val * (1.0 + sqrt(eta_val)))) ** 2
        )
        - 1.0
    )


def alpha_minus(eta_val: float, theta_val: float) -> float:
    """
    α₋ from [B4]:  α₋ = (α₊ + 1)·η − 1.

    For η ≈ 0.99 and α₊ ≈ 0.0183:  α₋ ≈ 0.00813.
    α₋ enters the mass formula [B3] as the "+ 4·q·α₋" charge correction.
    """
    return eta_val * (alpha_plus(eta_val, theta_val) + 1.0) - 1.0


def alpha_fine_structure() -> float:
    """
    Sommerfeld fine-structure constant α, derived purely from η and θ
    via [B58]–[B62]:

        α · √(1 − α²) = (9·θ / (2π)⁵) · (1 − C')                          [B58]
        1 − C' = 1 − √η₁₁ √η₁₂ / [(1 + √η₁₁)(1 + √η₁₂)] · (… - simplified)

    The implementation here matches the C `query_alpha`. The smaller positive
    root of the quadratic in α² is taken.

    Returns α ≈ 0.00729735…  (i.e. 1/α ≈ 137.0360, agreeing with experiment
    to ~5 decimal digits).
    """
    eta00 = eta(1, 0)
    eta11 = eta(1, 1)
    eta12 = eta(1, 2)
    th = theta(eta00)

    a1 = sqrt(eta11) * (1 - sqrt(eta11)) / (1 + sqrt(eta11))
    a2 = sqrt(eta12) * (1 - sqrt(eta12)) / (1 + sqrt(eta12))

    cst = 9.0 * th * (1 - a1 * a2) / (2.0 * pi) ** 5

    # Solve  α·√(1 − α²) = cst  for α (smaller positive root)
    return sqrt(0.5 * (1.0 - sqrt(1.0 - 4.0 * cst**2)))


def mass_element() -> float:
    """
    The mass element μ in kilograms — pure-geometric mass scale built from
    G, ℏ, c (and gauge length s₀ = 1 m):

        μ = π^(1/4) · (3π·G·ℏ·s₀)^(1/3) · √(ℏ / (3·c·G)) / s₀

    Numerical value: μ ≈ 2.259·10⁻³¹ kg ≈ 0.248·m_e.
    """
    return (
        pi ** (1.0 / 4.0)
        * (3.0 * pi * G * H_BAR * S_0) ** (1.0 / 3.0)
        * sqrt(H_BAR / (3.0 * C_LIGHT * G))
        / S_0
    )


# ---------------------------------------------------------------------------
# Convenience aliases — mirror the C "query_*" naming for direct comparison.
# ---------------------------------------------------------------------------

query_eta = eta
query_tet = theta
query_alp_p = alpha_plus
query_alp_n = alpha_minus
query_alpha = alpha_fine_structure
query_miu = mass_element


__all__ = [
    "C_LIGHT", "G", "ELEMENTARY_CHARGE", "H_PLANCK", "H_BAR",
    "MU_0", "EPS_0", "S_0", "KG_TO_MEV",
    "set_constants_mode", "get_constants_mode",
    "eta", "theta", "alpha_plus", "alpha_minus",
    "alpha_fine_structure", "mass_element",
    "query_eta", "query_tet", "query_alp_p", "query_alp_n",
    "query_alpha", "query_miu",
]
