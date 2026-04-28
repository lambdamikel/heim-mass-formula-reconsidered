"""
Regression test: lock the 21 reference particle masses to the values
produced by Eli Gildish's 2006 C reference implementation.

Any future change to the Python port that breaks this test must be
reviewed against the C reference (via `cd annotated && make`).

Run:  pytest python/test_reference_masses.py
  or: python -m pytest test_reference_masses.py   (from the python/ dir)
"""

from __future__ import annotations

import pytest

from particle import REFERENCE_PARTICLES


# Frozen snapshot of the 21 mass predictions in MeV/c², as produced by
# both the C reference (annotated/heimmass) and this Python port. These
# values match Heim's published figures via Eli Gildish's 2006
# reimplementation.
REFERENCE_MASSES_MEV: dict[str, float] = {
    "e_0":      0.50627181,
    "e_-":      0.50694371,
    "miu_-":  105.65229677,
    "eta":    548.62899518,
    "KAPPA_+": 493.69551717,
    "KAPPA_0": 497.69173794,
    "pi_+-":  139.56017382,
    "pi_0":   134.92903040,
    "LAMBDA":1116.21187996,
    "OMEGA_-":1672.12138879,
    "p":      937.33890386,
    "n":      938.30996495,
    "XI_0":  1314.47953670,
    "XI_-":  1321.24989957,
    "SIGMA_+":1189.33466416,
    "SIGMA_0":1192.23763970,
    "SIGMA_-":1197.26476102,
    "DELTA_++":1234.44268176,
    "DELTA_+":1234.73522847,
    "DELTA_0":1235.79291876,
    "DELTA_-":1229.21247787,
}


@pytest.mark.parametrize("particle", REFERENCE_PARTICLES, ids=lambda p: p.symbol)
def test_mass_matches_reference(particle):
    """Each particle's predicted mass must match the C reference to 8
    decimal digits."""
    expected = REFERENCE_MASSES_MEV[particle.symbol]
    actual = particle.mass_mev
    assert actual == pytest.approx(expected, abs=1e-7), (
        f"{particle.symbol}: got {actual:.10f}, expected {expected:.10f}"
    )


def test_all_21_particles_present():
    """Sanity: the reference list still has exactly 21 particles."""
    assert len(REFERENCE_PARTICLES) == 21
    assert len(REFERENCE_MASSES_MEV) == 21


def test_charge_predictions():
    """Predicted electric charges must match the integer quantum number
    expected from each particle's name (rounded)."""
    expected = {
        "e_0": 0, "e_-": -1, "miu_-": -1,
        "eta": 0, "KAPPA_+": 1, "KAPPA_0": 0,
        "pi_+-": 1, "pi_0": 0,
        "LAMBDA": 0, "OMEGA_-": -1,
        "p": 1, "n": 0,
        "XI_0": 0, "XI_-": -1,
        "SIGMA_+": 1, "SIGMA_0": 0, "SIGMA_-": -1,
        "DELTA_++": 2, "DELTA_+": 1, "DELTA_0": 0, "DELTA_-": -1,
    }
    for p in REFERENCE_PARTICLES:
        assert round(p.charge) == expected[p.symbol], (
            f"{p.symbol}: charge {p.charge:+.4f} → rounded {round(p.charge)}, "
            f"expected {expected[p.symbol]}"
        )
