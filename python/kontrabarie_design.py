"""
Modern Kontrabator design — thrust prediction from Heim's 1959 formulas.
========================================================================

Heim's "Prinzip der dynamischen Kontrabarie" (Flugkörper 1959, IvL
reconstruction 2017) describes a propulsion device — the "Kontrabator"
— that converts circulating electromagnetic radiation into a
ponderomotive force via the cross-coupling terms of the gravito-EM
energy-density tensor (m=2 gravito-electric, m=3 gravito-magnetic
components in Heim's framework — see THEORY_EXPLAINED.md ch. 15).

This script does what is computable from Heim's published formulas:

  1. Implements the steady-state acceleration field b(x) from
     IvL 2017 p. 237, finds its peak value as a pure number.
  2. Defines a modern apparatus spec (radius, mass, transformer
     volume, input power, efficiency) using components available
     today rather than the 1957 hand-soldered hollow-ring prototype.
  3. Computes the dimensionless parameter x and the corresponding
     acceleration b(x) in units of Heim's unknown coupling
     constant C.
  4. Brackets the resulting thrust between two reference values:
       LOWER  — pure-photon-rocket limit F = L/c (no Heim effect)
       UPPER  — "Heim taken at face value" with C set to make
               the 1957 negative result an upper bound only.
  5. Lists what experimental upgrades over Heim 1957 would be
     needed to detect the predicted effect, IF it exists.

This is a PARAMETRIC prediction.  The overall scale C of Heim's
acceleration formula is not derivable from anything in our current
Python port — it depends on the protosimplex/synmetronic structure
quantities described in Synmetronik Band III chapters 7-8 which
have never been implemented.  Anyone wanting to close that gap
would have to port those chapters first.

Run with:
    ./venv/bin/python python/kontrabarie_design.py
"""

from __future__ import annotations

from math import cos, exp, pi, sin, sqrt


def _golden_section_max(f, a: float, b: float, tol: float = 1e-8):
    """Pure-Python golden-section maximisation, no scipy dependency."""
    phi = (sqrt(5.0) - 1.0) / 2.0
    c = b - phi * (b - a)
    d = a + phi * (b - a)
    while abs(b - a) > tol:
        if f(c) > f(d):
            b = d
        else:
            a = c
        c = b - phi * (b - a)
        d = a + phi * (b - a)
    x = 0.5 * (a + b)
    return x, f(x)


# ----------------------------------------------------------------------
# 1.  Heim's steady-state acceleration shape function
# ----------------------------------------------------------------------
#
# IvL 2017 p. 237, last equation block:
#
#       b(x) = C · ( e^(-x) − e^(x/2) · (cos(x·√3) − (1/2)·√3·sin(x·√3)) )
#
# where x = ∛λ' is a dimensionless parameter determined by the apparatus
# spec, and C is an overall acceleration scale set by Heim's
# polymetric formalism (not derivable from the IvL paper alone).
#
# The dimensionless function shape(x) below has the property:
#   shape(0) = 1 - 1 = 0       (no excitation, no acceleration)
#   shape(x) grows for moderate x, then oscillates/decays
#   The first positive maximum is the operating point of the device.


def shape(x: float) -> float:
    """The bracketed dimensionless factor of Heim's b(x)."""
    return (
        exp(-x)
        - exp(x / 2.0) * (cos(x * sqrt(3.0)) - 0.5 * sqrt(3.0) * sin(x * sqrt(3.0)))
    )


def find_first_maximum() -> tuple[float, float]:
    """Locate the first positive maximum of shape(x) for x > 0."""
    return _golden_section_max(shape, 0.0, 4.0)


# ----------------------------------------------------------------------
# 2.  Apparatus spec — modern components
# ----------------------------------------------------------------------
#
# Heim's 1957 prototype used hand-soldered hollow-ring waveguides ~17 cm
# in diameter, fed by a magnetron at radar frequencies (~3 GHz).  The
# components had ohmic loss ~50 dB/m, making any sub-percent efficiency
# transformation undetectable even by sensitive seismometers.
#
# Modern equivalents:
#
#   superconducting RF cavities  (CERN / SLAC / DESY style):
#       Q > 10^10, loss < 0.001 dB/m at GHz frequencies
#       limit: thermal at ~2 K, accelerating gradient ~50 MV/m
#
#   high-power millimetre-wave gyrotrons:
#       ITER-class: 1 MW CW at 170 GHz
#       lab-scale: 10 kW CW at 30-100 GHz
#
#   precision force balance / laser interferometric detection:
#       1957: seismometer floor ~10 µm
#       2026: torsion-pendulum thrust stands resolve 1 µN at 1 MW
#             (NASA Eagleworks chamber, Tajmar 2017 setup, etc.)
#
#   structured photonic crystals for the "cycle former":
#       1957: Heim guessed at cyclic polymers; never built them
#       2026: photonic-crystal whispering-gallery resonators
#             (sapphire, silicon), gyrotropic metamaterials


APPARATUS = {
    "name":             "Heim 2026 lab-scale Kontrabator",
    "radius_m":         0.30,         # 30 cm ring radius
    "transformer_V_m3": 0.0050,       # 5 L active volume of cycle former
    "mass_kg":          15.0,         # apparatus mass (cavity + cycle former)
    "input_power_W":    100_000.0,    # 100 kW CW gyrotron — accessible today
    "efficiency":       0.5,          # 50 % power actually transformed
                                      # (Heim guessed at <1 % for his 1957 unit)
    "frequency_GHz":    30.0,         # mid-millimetre-wave band
    "Q_factor":         1e9,          # superconducting cavity quality factor
}


def heim_lambda_prime(spec: dict) -> float:
    """
    Heim's reduced parameter λ' = 2π · r · L · ε / (m₀ · V').  In
    IvL 2017 this combination is written as if dimensionless, but
    dimensional analysis gives [m³·kg⁻¹·s⁻³] = [W·s³/(kg·m²)] — i.e.
    Heim's published formulas drop an implicit time scale that
    converts λ' into a dimensionless ratio.  That conversion factor
    is part of the protosimplex/synmetronic apparatus that we do not
    have implemented.  We therefore report the SHAPE-function peak
    independently of the absolute scale: the operator tunes the
    apparatus parameters until the dimensionless x sits at the
    first maximum of shape(x), and the resulting thrust is
    F = m₀·C·shape(x_peak).
    """
    r   = spec["radius_m"]
    L   = spec["input_power_W"]
    eps = spec["efficiency"]
    m0  = spec["mass_kg"]
    Vp  = spec["transformer_V_m3"]
    return 2.0 * pi * r * L * eps / (m0 * Vp)


# ----------------------------------------------------------------------
# 3.  Bracket the resulting thrust between two reference values
# ----------------------------------------------------------------------

def photon_rocket_thrust(power_W: float) -> float:
    """Pure photon-rocket limit: F = L / c.  This is a HARD lower bound
    on any propellantless-radiation-driven thrust; Heim claims to do
    much better, but no device should do worse than this."""
    return power_W / 299_792_458.0


def standard_GR_gravitomagnetic_thrust(spec: dict) -> float:
    """
    Standard general relativity says gravito-magnetic effects from
    moving EM energy density scale as G/c⁴ · L / r.  This is the
    "no new physics" prediction — what one gets by treating the
    Kontrabator with conventional GR.  It is many orders of magnitude
    below the photon limit.
    """
    G = 6.674e-11
    c = 299_792_458.0
    L = spec["input_power_W"]
    r = spec["radius_m"]
    # Frame-dragging-type coupling: F ~ G · U_em / c² × geometric factor
    return G * L / (c**4 * r) * spec["mass_kg"]


def heim_face_value_thrust(spec: dict, C_ms2: float,
                           shape_factor: float) -> float:
    """
    Heim's predicted thrust:  F = m₀ · b(x) = m₀ · C · shape(x).
    We assume the apparatus is tuned to the first peak of shape(x);
    shape_factor passed in is shape(x_peak).
    """
    return spec["mass_kg"] * C_ms2 * shape_factor


# ----------------------------------------------------------------------
# 4.  Output
# ----------------------------------------------------------------------

def banner(s: str, ch: str = "=") -> None:
    print()
    print(ch * 78)
    print(f" {s}")
    print(ch * 78)


def main():
    banner("Modern Kontrabator — Heim 1959 / IvL 2017 thrust prediction")

    x_peak, shape_peak = find_first_maximum()
    print(f"""
  Heim's steady-state acceleration field (IvL 2017 p. 237):

      b(x) = C · ( e^(-x) − e^(x/2) · (cos(x·√3) − (½)·√3·sin(x·√3)) )

  Numerical properties of the dimensionless bracket:

    First positive maximum at  x  ≈ {x_peak:.4f}
    Peak shape value          shape(x_peak) ≈ {shape_peak:.4f}
    shape(0) = 0  (no excitation, no thrust — consistency check)
""")

    banner("Apparatus spec — modern lab-scale components", ch="-")
    for k, v in APPARATUS.items():
        if isinstance(v, str):
            print(f"  {k:<24} {v}")
        elif isinstance(v, float) and (abs(v) < 1e-3 or abs(v) > 1e6):
            print(f"  {k:<24} {v:.3e}")
        else:
            print(f"  {k:<24} {v}")

    lam_p = heim_lambda_prime(APPARATUS)
    print(f"""
  Heim's λ' = 2π·r·L·ε/(m₀·V') = {lam_p:.4e}   (dimensions of W·s³/(kg·m²);
                                                Heim wrote it as if pure number).

  Operating-point assumption: the apparatus is geometrically tuned so
  that x sits at the first positive peak of shape(x) — i.e. at x ≈
  {x_peak:.4f}, where shape(x) attains its maximum value {shape_peak:.4f}.
  Tuning is achieved by adjusting r, L, V' and frequency until the
  device's natural dimensionless parameter lands on this peak.
""")

    banner("Thrust bracketing", ch="-")

    F_photon = photon_rocket_thrust(APPARATUS["input_power_W"])
    F_GR     = standard_GR_gravitomagnetic_thrust(APPARATUS)

    print(f"""
  LOWER BOUND — pure photon rocket:
    F = L / c = {APPARATUS["input_power_W"]:.2e} W / {299_792_458.0:.0f} m/s
            ≈ {F_photon:.4e} N
    Specific impulse: ~10⁵ s (best of any propellantless drive)
    — every electromagnetic radiation source produces at least this.

  REFERENCE — standard GR gravito-magnetic effect:
    F ≈ G·L·m / (c⁴·r) ≈ {F_GR:.4e} N
    — what conventional general relativity predicts.  Forty-plus
    orders of magnitude below detectability.

  HEIM PREDICTION — F = m₀ · C · shape(x_peak):
    Parametric in the unknown coupling scale C (units: m/s²).
    At the apparatus's first-maximum operating point, shape(x) ≈ {shape_peak:.4f}.
""")

    # We compute thrust under several hypotheses for what C might be:
    photon_C = F_photon / (APPARATUS["mass_kg"] * shape_peak)
    hypotheses = [
        ("matched to photon limit",
         photon_C,
         "C set so Heim-predicted thrust equals the photon-rocket limit"),
        ("Heim 1957 detection floor",
         1e-3,
         "C set so Heim's 1957 prototype just barely failed to detect "
         "(seismometer floor ~µm displacement)"),
        ("0.1 % of standard gravity",
         9.81e-3,
         "C ≈ g/1000 — 'noticeable' on a precision force balance"),
        ("equal to standard gravity",
         9.81,
         "C ≈ g — would lift the apparatus against Earth gravity, the "
         "popular-press version of 'antigravity'"),
    ]

    print("  Thrust at the apparatus's first-maximum operating point, "
          "for various C:")
    print()
    print(f"    {'hypothesis':<35} {'C [m/s²]':>12}   {'F [N]':>12}   "
          f"{'F/L [N/kW]':>11}")
    print(f"    {'-'*35} {'-'*12}   {'-'*12}   {'-'*11}")
    for name, C, _expl in hypotheses:
        F = heim_face_value_thrust(APPARATUS, C, shape_peak)
        F_per_kW = F / (APPARATUS["input_power_W"] / 1000.0)
        print(f"    {name:<35} {C:>12.3e}   {F:>12.4e}   {F_per_kW:>11.4f}")

    F_modest = heim_face_value_thrust(APPARATUS, 1e-3, shape_peak)
    F_photon_match = heim_face_value_thrust(APPARATUS, photon_C, shape_peak)
    print(f"""
  Reading the table:
    • Anything in the "C ≥ 1 m/s²" row would have been spectacularly
      detected in 1957 already.  The fact that it WASN'T tells us
      C ≪ 1 m/s² (or the effect doesn't exist).
    • C ≈ 10⁻³ m/s² (Heim's 1957 detection floor) gives ~{F_modest*1000:.1f} mN
      at 100 kW input.  This is well within reach of a modern thrust
      stand (~µN sensitivity).  A successful detection here would be
      a Nobel-prize-level result.
    • C ≈ {photon_C:.2e} m/s² (matching the photon-rocket limit) gives
      ~{F_photon_match*1e6:.2f} µN — indistinguishable from the trivial photon thrust.
""")

    banner("Modern Kontrabator design recommendations", ch="-")
    print("""
  If anyone genuinely wanted to test this:

  1. Replace Heim's hand-soldered hollow rings with a superconducting
     niobium toroidal cavity (RF Q > 10⁹).  Single-cell or 9-cell
     ILC-style technology, scaled to ring topology.  Loss budget at
     30 GHz: ~10⁻⁵ of input power per round trip vs. Heim's ~1
     round-trip loss.

  2. Drive with a 100 kW CW gyrotron at ~30 GHz (commercially
     available; lab-scale).  Heim's 1957 magnetron was ~10 kW pulsed.

  3. Force the EM mode into a closed loop using a chiral / gyrotropic
     metamaterial inner liner, designed to satisfy Heim's
     rot rot · F = 0 condition (the "cycle former" he envisioned in
     cyclic polymers).  This is the part where Heim's prescription
     is least specific — modern photonic-crystal design tools can
     enumerate candidate structures, but verifying that any one of
     them implements Heim's exact operator algebra is nontrivial.

  4. Mount on a NASA-Eagleworks-style torsion-pendulum thrust stand
     in vacuum, ≤ 10⁻⁶ Torr.  Sensitivity 1 µN.  Use null-result
     control runs (gyrotron on but cavity detuned) to subtract
     systematic effects (thermal, EM-leakage, electrostatic).

  5. Vary input power L over 2–3 decades and verify that thrust
     scales as predicted by Heim's λ' = 2π·r·L·ε/(m₀·V').  This is
     the falsification test: a real Heim effect must follow this
     scaling.  A constant offset (artifact) will not.

  Total cost: ~$2-5 million for the apparatus, plus ~1 person-year
  to design the cycle-former metamaterial.  Less than a typical
  small physics experiment.  The reason it hasn't been done is not
  cost — it's that mainstream physics views the entire premise as
  not worth checking.

  This script will not run that experiment for you, but it is
  enough to know:
    • What to build.
    • What to measure.
    • How to read the result.
""")


if __name__ == "__main__":
    main()
