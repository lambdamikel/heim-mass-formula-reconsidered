"""
Regression test: lock the 21 reference particle masses to the canonical
output of the Python port.

Update history:
  - 2026-04-29: pinned to Eli Gildish 2006 C reference output, after
                fixing two upstream-inherited transcription bugs in
                calc_N (missing *q factor) and calc_a (wrong y-nesting).
  - 2026-05-14: pinned to the J0060-corrected B3 form (default).
                Heim's primary manuscript J0060 (Synmetronik Band IV)
                gives M_q = q·μ_- = 4qμα_- explicitly (eq. 192 + p. 709),
                outside the μα_+ multiplication.  The IGW-Innsbruck 2003
                restatement [B3] = "+4qα_-" inside the bracket is
                missing a /α_+ factor and was the source of the 0.79 %
                electron-mass discrepancy.  With the correction:
                  electron:  -0.002 % off measurement (was -0.79 %)
                  muon:      -0.002 % off (was -0.005 %)
                  proton:    -0.002 % off (was -0.003 %)
                Bit-equality with the C reference is preserved only
                when formulae.LEGACY_B3_FORM = True (see commit
                message for source pointers).

Any future change to the Python port that breaks this test must be
reviewed against Heim's J0060 manuscript and the published Tabelle II
values in G_Ausgewaehlte_Ergebnisse.pdf.

Run:  pytest python/test_reference_masses.py
  or: python -m pytest test_reference_masses.py   (from the python/ dir)
"""

from __future__ import annotations

import pytest

from particle import REFERENCE_PARTICLES


# Frozen snapshot of the 21 mass predictions in MeV/c² as produced by
# the canonical Python port (J0060-corrected B3 form, LEGACY_B3_FORM=False).
# These values match Heim's published Tabelle II to <= 30 ppm overall
# and to <= 2 eV with heim_1989 constants.
REFERENCE_MASSES_MEV: dict[str, float] = {
    "e_0":      0.51615513,
    "e_-":      0.51098822,
    "miu_-":  105.65634128,
    "eta":    548.78369542,
    "KAPPA_+": 493.69956168,
    "KAPPA_0": 497.70819066,
    "pi_+-":  139.56421834,
    "pi_0":   134.95602561,
    "LAMBDA":1115.56659651,
    "OMEGA_-":1672.12543330,
    "p":      938.25167338,
    "n":      939.54540401,
    "XI_0":  1314.86293703,
    "XI_-":  1321.25394409,
    "SIGMA_+":1189.33870868,
    "SIGMA_0":1192.44246612,
    "SIGMA_-":1197.26880554,
    "DELTA_++":1234.44239668,
    "DELTA_+":1234.57307449,
    "DELTA_0":1235.13841791,
    "DELTA_-":1229.95869976,
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
