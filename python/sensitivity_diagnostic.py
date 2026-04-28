"""
Diagnostic: which particles are actually sensitive to each fitted constant?

The first sensitivity scan revealed that the loss is almost flat (Δ ~ 10⁻⁹
out of 10⁻⁵) under ±10 % perturbations of the three fitted constants. This
script localises the effect particle-by-particle to find out where —
if anywhere — those constants matter.
"""

from __future__ import annotations

import formulae
from particle import REFERENCE_PARTICLES


CONSTANTS = [
    ("FOURTH_ROOT_2",     "⁴√2"),
    ("PI_OVER_E_SQR",     "(π/e)²"),
    ("FOUR_PI_OVER_4RT2", "4π/⁴√2"),
]

PERTURBATION = 0.5   # multiply by this factor (so 50% = drastic change)


def mass_at(particle, attr, factor):
    saved = getattr(formulae, attr)
    setattr(formulae, attr, saved * factor)
    try:
        return particle.mass_mev
    finally:
        setattr(formulae, attr, saved)


def main():
    measured = [p for p in REFERENCE_PARTICLES if p.m_exp_mev > 0]

    print("Per-particle sensitivity to each fitted constant")
    print("(comparing default vs. ×0.5 — i.e., halve the constant)")
    print()
    header = f"{'particle':12} {'baseline':>14}"
    for _, label in CONSTANTS:
        header += f" {'Δ ' + label:>16}"
    header += f" {'most-sensitive':>16}"
    print(header)
    print("-" * len(header))

    for p in measured:
        baseline = p.mass_mev
        deltas = []
        for attr, label in CONSTANTS:
            perturbed = mass_at(p, attr, PERTURBATION)
            delta_rel = (perturbed - baseline) / baseline
            deltas.append((label, delta_rel))

        most = max(deltas, key=lambda kv: abs(kv[1]))[0]
        row = f"{p.symbol:12} {baseline:14.6f}"
        for _, d in deltas:
            row += f"   {d*100:+10.4f}%   " if abs(d) > 1e-10 else "       (zero)    "
        row += f" {most:>16}"
        print(row)


if __name__ == "__main__":
    main()
