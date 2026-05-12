"""
Heim's e_0 — the "neutral electron" prediction
==============================================

Heim's 1989 framework lists 21 basic states. One of them — labelled
e_0 — has no experimental counterpart: it is a *standing prediction*
of a stable, neutral, spin-½ particle whose quantum numbers differ
from the electron only by the configuration index x.

  electron e^-  :  ε=+1, k=1, P=1, Q=1, κ=0, x=1   →  q = -1
  e_0           :  ε=+1, k=1, P=1, Q=1, κ=0, x=0   →  q =  0

With Heim's bug-fixed Python implementation, the resulting prediction is:

  m(e_0)   = 0.5162 MeV  (≈ 1.0 % above the measured electron mass)
  τ(e_0)   = ∞           (stable under the [B47]–[B57] lifetime formula)
  spin     = ½
  isospin  = ½
  charge   = 0

The question this script makes concrete: **is such a particle
empirically allowed?**  We collate the relevant experimental
constraints from precision β-decay, cosmology, and direct-detection
searches and compare them against the three plausible interaction
hypotheses for e_0.

Run with:
    ./venv/bin/python python/e0_search.py
"""

from __future__ import annotations

import formulae as fm
import lifetime as lt
from constants import KG_TO_MEV
from particle import REFERENCE_PARTICLES


def compute_e0_predictions():
    e0 = REFERENCE_PARTICLES[0]      # the neutral-electron prediction
    e_minus = REFERENCE_PARTICLES[1]  # the charged electron

    rows = []
    for p in (e0, e_minus):
        qx = fm.calc_charge(p.eps, p.k, p.P, p.Q, p.kap, p.x)
        m_kg = fm.calc_mass(p.eps, p.k, p.P, p.Q, p.kap, qx)
        m_mev = m_kg * KG_TO_MEV
        tau = lt.calc_lifetime_seconds(p.eps, p.k, p.P, p.Q, p.kap, qx, m_kg)
        rows.append((p.symbol, qx, m_mev, tau))
    return rows


def print_header(s: str, char: str = "="):
    print()
    print(char * 78)
    print(f" {s}")
    print(char * 78)


def main():
    print_header("Heim's e_0 — the neutral-electron prediction")

    print()
    print("  Quantum numbers (Heim convention: P = 2·isospin, Q = 2·spin):")
    print("    e_0  : ε=+1, k=1, P=1, Q=1, κ=0, x=0   →  q = 0")
    print("    e^-  : ε=+1, k=1, P=1, Q=1, κ=0, x=1   →  q = -1")
    print()
    print("  Heim's two predictions differ *only* by x (the configuration index):")
    print()
    print(f"  {'symbol':<8} {'q':>3}  {'m (MeV)':>12}   {'τ (s)':>12}")
    print(f"  {'-'*8} {'-'*3}  {'-'*12}   {'-'*12}")
    for sym, q, m, tau in compute_e0_predictions():
        tau_str = "∞ (stable)" if tau == float("inf") else f"{tau:.3e}"
        print(f"  {sym:<8} {int(q):>+3d}  {m:>12.6f}   {tau_str:>12}")
    print()
    print("  Reference (measured):")
    print(f"  {'e^-':<8} {-1:>+3d}  {0.51099907:>12.6f}   stable")
    print(f"  → m(e_0)/m(e^-, measured) = {0.516155/0.51099907:.4f}")
    print(f"  → Δm(e_0 - e^-)            = +5.16 keV")

    print_header("Experimental constraints", char="-")

    print("""
  We have a stable, neutral, spin-½ particle of mass ~516 keV.  What
  does experiment say about such a particle?  The answer depends on
  which Standard-Model forces couple to it.  We consider three cases.

  ──────────────────────────────────────────────────────────────────
  Case A — e_0 mixes with active neutrinos (sterile-neutrino reading)
  ──────────────────────────────────────────────────────────────────

  If e_0 is a heavy mass eigenstate of the active-neutrino sector
  (a "sterile neutrino" in modern parlance) of mass m_4 = 0.516 MeV
  with mixing |U_e4|² ~ 1 to ν_e, then:

  • β-decay endpoint searches must show a kink at E_endpoint − m_4.
    Sensitivity: <0.5 % mixing |U_e4|² for m_4 in 0.1–1 MeV from
    precise ⁶³Ni, ³⁵S spectra, π⁺ → e⁺ν decays (PIENU-like).
    A 516 keV sterile with O(1) mixing is excluded by ≥ 7 orders of
    magnitude.

  • Big Bang Nucleosynthesis: a stable 500 keV neutrino-like particle
    in thermal equilibrium overcloses the universe by ~10⁵.
    Hard cosmological ruling.

  • Supernova SN 1987A: emission of a ~500 keV neutral lepton from
    the proto-neutron star would shorten the observed ν burst
    duration; this excludes mixing |U_e4|² > 10⁻⁹.

  Verdict: **ruled out** by ≥ 7 σ in this interpretation.

  ──────────────────────────────────────────────────────────────────
  Case B — e_0 has no Standard-Model coupling (pure-gravity reading)
  ──────────────────────────────────────────────────────────────────

  If e_0 couples only via gravity (and the unknown Heim sector
  itself), then the only relevant bound is:

  • Dark-matter / cosmology: an inert ~516 keV stable relic could
    in principle exist, but its abundance is constrained.  If
    produced thermally it would be hot dark matter with Ω h² ~ 1
    today, which exceeds Ω_DM ~ 0.12 by ~10×.  Non-thermal
    production (e.g. through Heim-sector processes only) is
    unconstrained.

  • CMB & structure formation: a 516 keV warm relic is below the
    Lyman-α free-streaming bound of m_WDM > ~5 keV, so this is OK
    only if e_0 has cold (non-thermal) production.

  Verdict: **possible**, but unfalsifiable from outside the Heim
  framework — a 516 keV gravitationally-coupled fermion is exactly
  the kind of "ghost particle" cosmologists cannot directly probe
  unless it has additional non-gravitational interactions.

  ──────────────────────────────────────────────────────────────────
  Case C — e_0 has Heim-internal coupling only (geometric reading)
  ──────────────────────────────────────────────────────────────────

  In Heim's framework, "charge" is the integer q ∈ {-2,…,+2} that
  enters the mass formula.  q = 0 means the metron configuration
  has zero net coupling to the electromagnetic field as Heim defines
  it.  Whether such a configuration *also* lacks weak coupling is
  not separately resolved — Heim's framework does not contain weak
  isospin as a fundamental symmetry; the "isospin" quantum number
  P here labels metron geometry, not SU(2)_L charge.

  In this reading e_0 is geometrically a sibling of the electron
  (same k, P, Q, κ; only x differs), with all SM-style couplings
  inherited only through whatever embedding maps Heim's quantum
  numbers onto SM gauge charges.  Until that embedding is specified,
  Case C is not separately testable from Case B.

  ──────────────────────────────────────────────────────────────────
  Plausibility summary
  ──────────────────────────────────────────────────────────────────

  Heim's e_0 prediction is *consistent with* current experimental
  bounds only in Cases B/C — interpretations under which the
  particle does not communicate with the Standard Model via
  charged-current weak interactions.  In all interpretations where
  e_0 mixes with ν_e at the level a "neutral electron" of mass
  ~m_electron naively suggests, the bounds are catastrophically
  violated.

  The cleanest experimental probe of Heim's framework on this point
  would be to determine whether Heim theory predicts any
  *non-gravitational* coupling for e_0.  If it does, that coupling
  is directly testable; if not, e_0 joins the long list of stable
  hidden-sector candidates that experiment cannot directly access.

  Bottom line: e_0 is **not yet ruled out** — but only because the
  framework leaves its couplings under-specified.  A Heim-theory
  proponent would need to (a) compute e_0's coupling to the photon
  (via the q = 0 metron geometry — should be zero by construction),
  (b) compute its coupling to neutrinos and the weak charged
  current (not currently derivable from the published mass formula),
  and then submit the resulting interaction to laboratory and
  cosmological tests.
""")


if __name__ == "__main__":
    main()
