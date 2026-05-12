"""
Excited-state search: do Heim's quantum-number lattice and configuration
index x reproduce observed baryon and meson resonances?

Heim's 21 reference particles span only the ground states of light
hadrons.  But the same mass formula is in principle valid for any
allowed integer tuple (ε, k, P, Q, κ, x).  Many well-established
post-1965 resonances (the N* nucleon excitations, the Δ excited
states, Λ*, Σ*, Ξ*, ρ, ω, η', φ, the K* family, the f/a/b/h
mesons, …) were known in 1989 but were *not* placed by Heim into
his published table.  This script asks: does the formula find them
anyway, at the right (P, Q, |q|)?

For each PDG resonance, we scan the (ε, k, κ, x) lattice with the
*required* P (= 2·isospin) and Q (= 2·spin) and report:

  - exact-charge, exact-(P,Q) matches within ±2% and ±10%
  - the next-closest mass at the correct (P, Q, |q|), if any
  - the K* control match (already known to be 2.7 % off)

The full PDG list of light-flavour resonances (no charm/bottom) up
to ~2.5 GeV is used.  Heavy-flavour states (J/ψ, D, B, Λ_c, …) are
deliberately excluded — earlier work showed those are outside the
framework's scope.

Run with:
    ./venv/bin/python python/excited_state_search.py
"""

from __future__ import annotations

import formulae as fm
from constants import KG_TO_MEV
from math import isfinite


# --------------------------------------------------------------------
# Targets — PDG well-established light-flavour resonances, in MeV.
# Format: (name, mass MeV, |charge|, J (spin), I (isospin), note)
# Spin and isospin in physical units (not Heim's P,Q!).
# --------------------------------------------------------------------

TARGETS_MESONS = [
    # ---- Light unflavoured mesons
    ("ρ(770)",        775,  1, 1,    1,    "vector"),
    ("ρ(770)⁰",       775,  0, 1,    1,    "vector"),
    ("ω(782)",        783,  0, 1,    0,    "vector"),
    ("η′(958)",       958,  0, 0,    0,    "pseudoscalar"),
    ("f₀(980)",       990,  0, 0,    0,    "scalar"),
    ("a₀(980)⁰",      980,  0, 0,    1,    "scalar"),
    ("a₀(980)±",      980,  1, 0,    1,    "scalar"),
    ("φ(1020)",      1019,  0, 1,    0,    "vector ss̄"),
    ("h₁(1170)",     1170,  0, 1,    0,    "axial"),
    ("b₁(1235)",     1230,  1, 1,    1,    "axial"),
    ("a₁(1260)",     1230,  1, 1,    1,    "axial"),
    ("f₂(1270)",     1275,  0, 2,    0,    "tensor"),
    ("f₁(1285)",     1282,  0, 1,    0,    "axial"),
    ("η(1295)",      1294,  0, 0,    0,    "pseudoscalar"),
    ("π(1300)",      1300,  1, 0,    1,    "radial π exc."),
    ("a₂(1320)",     1318,  1, 2,    1,    "tensor"),
    # ---- Strange mesons
    ("K*(892)",       892,  0, 1,    0.5,  "vector"),     # ← known match
    ("K*(892)±",      892,  1, 1,    0.5,  "vector"),
    ("K₁(1270)",     1272,  1, 1,    0.5,  "axial"),
    ("K₁(1400)",     1403,  1, 1,    0.5,  "axial"),
    ("K*(1410)",     1414,  1, 1,    0.5,  "vector"),
    ("K₀*(1430)",    1425,  1, 0,    0.5,  "scalar"),
    ("K₂*(1430)",    1432,  1, 2,    0.5,  "tensor"),
]

TARGETS_BARYONS = [
    # ---- Nucleon excitations
    ("N(1440)",      1440,  1, 0.5,  0.5,  "Roper"),
    ("N(1520)",      1520,  1, 1.5,  0.5,  ""),
    ("N(1535)",      1535,  1, 0.5,  0.5,  ""),
    ("N(1650)",      1655,  1, 0.5,  0.5,  ""),
    ("N(1680)",      1685,  1, 2.5,  0.5,  ""),
    ("N(1720)",      1720,  1, 1.5,  0.5,  ""),
    # ---- Δ excitations (beyond the 1232)
    ("Δ(1600)",      1600,  1, 1.5,  1.5,  ""),
    ("Δ(1620)",      1630,  1, 0.5,  1.5,  ""),
    ("Δ(1700)",      1700,  1, 1.5,  1.5,  ""),
    ("Δ(1905)",      1880,  1, 2.5,  1.5,  ""),
    # ---- Λ excitations
    ("Λ(1405)",      1405,  0, 0.5,  0,    "narrow"),
    ("Λ(1520)",      1520,  0, 1.5,  0,    ""),
    ("Λ(1670)",      1670,  0, 0.5,  0,    ""),
    ("Λ(1690)",      1690,  0, 1.5,  0,    ""),
    # ---- Σ excitations
    ("Σ(1385)",      1385,  1, 1.5,  1,    ""),
    ("Σ(1660)",      1660,  1, 0.5,  1,    ""),
    ("Σ(1670)",      1670,  1, 1.5,  1,    ""),
    ("Σ(1775)",      1775,  1, 2.5,  1,    ""),
    # ---- Ξ excitations
    ("Ξ(1530)",      1530,  0, 1.5,  0.5,  ""),
    ("Ξ(1690)",      1690,  0, 0.5,  0.5,  ""),
    ("Ξ(1820)",      1820,  0, 1.5,  0.5,  ""),
]


# --------------------------------------------------------------------
# Lattice scanner — generate every (ε, k, P, Q, κ, x) with finite
# mass and integer charge in {-2..+2}.
# --------------------------------------------------------------------

def scan_all(k_range=range(1, 5), x_range=range(0, 8),
             P_range=range(0, 7), Q_range=range(0, 7)):
    out = []
    for eps in (1, -1):
        for k in k_range:
            for P in P_range:
                for Q in Q_range:
                    for kap in (0, 1):
                        for x in x_range:
                            try:
                                qx = fm.calc_charge(eps, k, P, Q, kap, x)
                            except Exception:
                                continue
                            qx_int = round(qx)
                            if abs(qx - qx_int) > 0.01 or abs(qx_int) > 2:
                                continue
                            try:
                                m_kg = fm.calc_mass(eps, k, P, Q, kap, qx)
                                m_mev = m_kg * KG_TO_MEV
                            except Exception:
                                continue
                            if isfinite(m_mev) and 0 < m_mev < 5e3:
                                out.append((eps, k, P, Q, kap, x, qx_int, m_mev))
    return out


def heim_PQ(spin: float, isospin: float):
    return int(round(2 * isospin)), int(round(2 * spin))


def find_best_match(candidates, m_target, abs_q, P_req, Q_req, tol):
    """Return the *closest mass* candidate with the right (P, Q, |q|)
    within fractional tolerance `tol`, or None."""
    best = None
    for c in candidates:
        eps, k, P, Q, kap, x, qx, m = c
        if P != P_req or Q != Q_req:
            continue
        if abs(qx) != abs_q:
            continue
        if abs(m - m_target) / m_target > tol:
            continue
        if best is None or abs(m - m_target) < abs(best[7] - m_target):
            best = c
    return best


def main():
    print("=" * 92)
    print(" Excited-state search — does Heim's lattice cover known light-flavour resonances?")
    print("=" * 92)

    # Wider lattice than higgs_search.py: include k up to 5 and x up to 11,
    # which encompasses the regime where Heim's later (post-1989) work
    # placed several un-published candidate states.
    candidates = scan_all(k_range=range(1, 6), x_range=range(0, 12))
    print(f"\nLattice: ε∈±1, k∈{{1..5}}, P∈{{0..6}}, Q∈{{0..6}}, κ∈{{0,1}}, "
          f"x∈{{0..11}}, |q|≤2")
    print(f"Generated {len(candidates):,} integer-charge candidates < 5 GeV\n")

    for label, targets in (("MESONS", TARGETS_MESONS),
                           ("BARYONS", TARGETS_BARYONS)):
        print()
        print("-" * 86)
        print(f"  {label}")
        print("-" * 86)
        print(f"{'Particle':<14} {'PDG':>6} {'|q|':>3}  "
              f"{'P':>2} {'Q':>2}  "
              f"{'best ≤10%':>11}  "
              f"{'err':>6}   "
              f"{'note':<28}")
        print("-" * 86)
        n_match2, n_match10, n_total = 0, 0, 0
        for name, m_t, q, J, I, note in targets:
            P_req, Q_req = heim_PQ(J, I)
            best10 = find_best_match(candidates, m_t, q, P_req, Q_req, 0.10)
            best2  = find_best_match(candidates, m_t, q, P_req, Q_req, 0.02)
            n_total += 1
            if best2 is not None:
                n_match2 += 1
            if best10 is not None:
                n_match10 += 1
                eps_b, k_b, _, _, kap_b, x_b, _, m_pred = best10
                err_pct = (m_pred - m_t) / m_t * 100
                tag = "★" if best2 is not None else " "
                qnstr = f"ε={eps_b:+d} k={k_b} κ={kap_b} x={x_b}"
                print(f"{name:<14} {m_t:>6} {q:>3}  "
                      f"{P_req:>2} {Q_req:>2}  "
                      f"{m_pred:>9.1f} {tag}  "
                      f"{err_pct:>+5.1f}%   "
                      f"{qnstr:<28}")
            else:
                print(f"{name:<14} {m_t:>6} {q:>3}  "
                      f"{P_req:>2} {Q_req:>2}  "
                      f"{'  —':>11}  "
                      f"{'    —':>6}   "
                      f"{'(no candidate)':<28}")
        print("-" * 86)
        print(f"  {label}: {n_match2}/{n_total} within ±2%, "
              f"{n_match10}/{n_total} within ±10%")

    print()
    print("=" * 92)
    print(" Interpretation")
    print("=" * 92)
    print("""
Three structural observations:

1. NEW ±2% match: Λ(1690) at 1666 MeV (-1.4%) with ε=-1, k=2, κ=0, x=1
   at the correct (P=0, Q=3, q=0).  Joins K*(892) as a second
   independently obtained Heim prediction outside his published 16-21.

2. The Heim lattice CLUSTERS multiple PDG resonances onto one state:

     N(1520), N(1720) → both → 1671 MeV at (P=1, Q=3, q=1, k=2)
     Δ(1600), Δ(1700) → both → 1647 MeV at (P=3, Q=3, q=1, k=2)
     Λ(1520), Λ(1690) → both → 1666 MeV at (P=0, Q=3, q=0, k=2)
     Ξ(1530), Ξ(1820) → both → 1665 MeV at (P=1, Q=3, q=0, k=2)

   In each case Heim's framework places ONE state where the PDG
   resolves TWO.  This is consistent with the quark-model view that
   the PDG pair are radial/orbital partners with the same quantum
   numbers — a distinction Heim's lattice does not encode through
   (P, Q, κ, x) at k = 2.  Either:
     (a) Heim's framework is genuinely incomplete and is missing the
         excitation degree of freedom that distinguishes the two; or
     (b) one of each PDG pair is mis-assigned and the other is the
         "true" Heim state.

3. The light VECTOR MESON sector (ρ, ω, φ; Q = 2 with low isospin)
   has NO Heim candidate within ±10 % of measurement.  The Heim
   lattice produces no isospin-(0,1) spin-1 meson near 770-1020 MeV.
   This is a sharp prediction in the *wrong* direction — these
   particles obviously exist.  Possible readings:

     • Heim's framework treats only "metron-stationary" states and
       the ρ/ω/φ are not stationary in that sense (their hadronic
       widths Γ ~ 5-150 MeV are large enough that they are arguably
       not on the same footing as the pseudoscalar mesons π/K/η,
       whose widths are 5-12 orders of magnitude smaller).
     • Or: the framework is simply silent on vector mesons, in
       parallel with its silence on the electroweak gauge bosons.

The K* match — which IS a Q = 2 vector — sits at the strange-quark
boundary (P = 1, |q| = 1) where the lattice transitions through one
of its first non-trivial cells.  Why it works for K* but not for ρ
or ω is not obvious from the geometry alone.

What this scan does NOT do:
  - It does not enumerate which observed resonance is a "radial
    excitation" vs. an "orbital excitation" in the SM quark-model
    sense.  Heim's framework lacks the quark-model concept of radial
    excitation; what the configuration index x labels physically is
    not the same thing as a radial node count.
  - It does not test selection rules.  Heim noted (1989, p. 14) an
    unfinished selection rule that would prune the lattice down to
    only the observed states.  Without it the lattice generates
    states with no observed counterpart, and the obvious question
    "where are these extra states?" remains open.
""")


if __name__ == "__main__":
    main()
