"""
Main runner — Python port of heimmass.c.

Computes the Heim-1989 predictions for the reference particle list and
prints a comparison table against measured masses.
"""

from __future__ import annotations

from particle import REFERENCE_PARTICLES


def print_results(particles=REFERENCE_PARTICLES) -> None:
    print()
    print(" === particles ===============================================================")
    print(" =============================================================================")
    print(" name               | symbol   | q_x | m_the   [Mev] | m_exp   [Mev] | error %")
    print(" -----------------------------------------------------------------------------")

    for p in particles:
        q = round(p.charge)
        if p.m_exp_mev > 0:
            err = f"{p.error_percent:+.3f}%"
            exp = f"{p.m_exp_mev:13.8f}"
        else:
            err = "       "
            exp = " " * 13

        print(
            f" {p.name:18} | {p.symbol:8} | {q:3d} | "
            f"{p.mass_mev:13.8f} | {exp} | {err}"
        )

    print(" =============================================================================")


if __name__ == "__main__":
    print_results()
