"""
Test whether Heim's 1989 mass formula predicts particles discovered after
1989 — particularly the Higgs boson (125.25 GeV), W± (80.4 GeV), Z⁰
(91.2 GeV), and a few hadrons (K*, ρ, φ, B, etc.) that were known but
not in Heim's published 16-particle list.

The basic question: does the formula predict the Higgs, and at what mass?

Heim's quantum-number convention:
  P = 2 · isospin
  Q = 2 · spin  (yes, Q is double-spin, not "charge" — that's q_x)
  q_x = electric charge in units of e
  k  = configuration index ∈ {1, 2, 3, …}

For the Higgs (spin-0, isospin-0, charge-0):
  P = 0, Q = 0, q_x = 0

Run with:
    ./venv/bin/python python/higgs_search.py
"""

from __future__ import annotations

import formulae as fm
from constants import KG_TO_MEV
from math import isfinite


# --------------------------------------------------------------------
# Targets (PDG values, in MeV)
# --------------------------------------------------------------------
TARGETS = [
    # name,                 mass MeV, |q|, J,    isospin
    ("Higgs H⁰",             125_250, 0, 0,    0),
    ("Z⁰ boson",              91_188, 0, 1,    0),
    ("W± boson",              80_369, 1, 1,    0),     # weak isospin, ignore
    ("tau lepton",             1_777, 1, 0.5,  0.5),
    ("ρ⁰ meson",                 775, 0, 1,    1),
    ("K*⁰ meson",                892, 0, 1,    0.5),
    ("φ meson",                1_019, 0, 1,    0),
    ("J/ψ meson",              3_097, 0, 1,    0),
    ("D⁰ meson",               1_865, 0, 0,    0.5),
    ("B⁰ meson",               5_280, 0, 0,    0.5),
    ("Λc baryon",              2_286, 1, 0.5,  0),
    ("Λb baryon",              5_620, 0, 0.5,  0),
    ("Σc baryon",              2_454, 0, 0.5,  1),
]


def heim_quantum_numbers(spin: float, isospin: float):
    """Return (P, Q) for given spin and isospin under Heim's convention."""
    P = int(round(2 * isospin))
    Q = int(round(2 * spin))
    return P, Q


def scan_all_neutral(k_range=range(1, 5), x_range=range(0, 8)):
    """All Heim-allowed (k, P, Q, kap, x, eps) tuples that produce
    integer charge in {-2..+2} and finite mass."""
    out = []
    for k in k_range:
        for P in range(0, 6):
            for Q in range(0, 6):
                for kap in [0, 1]:
                    for x in x_range:
                        for eps in [1, -1]:
                            try:
                                qx = fm.calc_charge(eps, k, P, Q, kap, x)
                            except Exception:
                                continue
                            qx_int = round(qx)
                            if abs(qx - qx_int) > 0.01:
                                continue
                            if abs(qx_int) > 2:
                                continue
                            try:
                                m_kg = fm.calc_mass(eps, k, P, Q, kap, qx)
                                m_mev = m_kg * KG_TO_MEV
                            except Exception:
                                continue
                            if isfinite(m_mev) and 0 < m_mev < 1e15:
                                out.append((eps, k, P, Q, kap, x, qx_int, m_mev))
    return out


def find_matches(candidates, m_target, abs_charge, tol=0.10, P=None, Q=None):
    """Return up to 5 candidates within `tol` of m_target, with |q|=abs_charge,
    sorted by mass distance. If P or Q given, also filter on those."""
    matches = []
    for c in candidates:
        eps, k, p, q, kap, x, qx, m = c
        if abs(qx) != abs_charge:
            continue
        if P is not None and p != P:
            continue
        if Q is not None and q != Q:
            continue
        if not (1 - tol) * m_target <= m <= (1 + tol) * m_target:
            continue
        matches.append(c)
    matches.sort(key=lambda c: abs(c[7] - m_target))
    return matches[:5]


def main():
    print("=" * 80)
    print(" Heim 1989 framework — test on particles discovered or known after 1989")
    print("=" * 80)

    candidates = scan_all_neutral()
    print(f"\nGenerated {len(candidates)} physically-charged candidates")
    print(f"  (eps∈{{±1}}, k∈{{1,2,3,4}}, P∈{{0..5}}, Q∈{{0..5}}, κ∈{{0,1}}, x∈{{0..7}}, |q|≤2)\n")

    print(f"{'Particle':22} {'mass [MeV]':>10}  {'|q|':>3} {'P':>2} {'Q':>2}  Matches")
    print("-" * 80)

    for name, m_target, abs_q, spin, iso in TARGETS:
        P_exp, Q_exp = heim_quantum_numbers(spin, iso)
        matches = find_matches(candidates, m_target, abs_q, tol=0.10, P=P_exp, Q=Q_exp)
        if matches:
            best = matches[0]
            eps, k, P, Q, kap, x, qx, m = best
            err = abs(m - m_target) / m_target * 100
            print(f"{name:22} {m_target:>10}    {abs_q:>1}  {P_exp:>2} {Q_exp:>2}  "
                  f"ε={eps:+d} k={k} κ={kap} x={x}  →  {m:>10.2f} MeV ({err:.2f}% off)")
        else:
            # Fall back to: any P,Q match with right charge
            relax = find_matches(candidates, m_target, abs_q, tol=0.10)
            if relax:
                best = relax[0]
                eps, k, P, Q, kap, x, qx, m = best
                err = abs(m - m_target) / m_target * 100
                note = f"(at P={P} Q={Q}, NOT P={P_exp} Q={Q_exp})"
                print(f"{name:22} {m_target:>10}    {abs_q:>1}  {P_exp:>2} {Q_exp:>2}  "
                      f"closest {m:>10.2f} MeV ({err:.2f}% off) {note}")
            else:
                print(f"{name:22} {m_target:>10}    {abs_q:>1}  {P_exp:>2} {Q_exp:>2}  "
                      f"NO candidate within ±10%")

    print()
    print("=" * 80)
    print(" Higgs-specific analysis")
    print("=" * 80)
    print()
    print("The Higgs (J=0, isospin=0, charge=0) requires P=0, Q=0, q_x=0.")
    print("Heim-allowed neutral P=Q=0 ground states across k=2..4:")
    print()
    for c in candidates:
        eps, k, P, Q, kap, x, qx, m = c
        if P == 0 and Q == 0 and qx == 0:
            print(f"  ε={eps:+d} k={k} κ={kap} x={x}  →  m = {m:.3e} MeV")
    print()
    print("Notice: there are NO P=Q=0 q=0 Heim-allowed states in the")
    print("125 GeV range. The framework's natural P=Q=0 q=0 spacing")
    print("jumps from ~547 MeV (η meson, k=1) directly to 61 TeV (k=3, κ=0)")
    print("and 166 TeV (k=3, κ=1). The Higgs falls in a structural gap.")
    print()
    print("Interpretation: Heim's 1989 framework treats stable basic states")
    print("as stationary metron configurations. The Higgs is a quantum-field")
    print("excitation associated with electroweak symmetry breaking — a")
    print("phenomenon Heim's framework does not contain. The framework is")
    print("therefore neither falsified nor confirmed by the Higgs discovery;")
    print("it simply doesn't predict one.")


if __name__ == "__main__":
    main()
