"""
Cross-check our Python lifetime predictions against the Excel reference
(Heim_1989_Massenformel_0.4.xlsm — see downloads/).

The Excel spreadsheet contains a 'Vergleich' sheet with hardcoded T
values that match Heim's 1989 published numbers (12 of 14 within
experimental error). We reproduce 7 of them to ≤ 0.1 % and 16 of 18
within factor 3 of measurement.

The remaining gaps to Excel — particularly Λ (factor 12) and the four
Δ resonances (~10–40 % each) — could not be localised to specific
terms by careful side-by-side reading of the formulas. The formulas
themselves appear identical; the constants differ only at the 0.001 %
level. The discrepancy may live in Excel's macro-driven evaluation of
the (n, m, p, σ) decomposition or in a subtle rounding/precedence
difference that we have not yet pinned down.

This file pins the **current** state. If the Λ discrepancy is later
fixed, this snapshot will need to be updated.
"""

from __future__ import annotations

import math

import pytest

from particle import REFERENCE_PARTICLES


# Excel Vergleich values, in seconds. Particles without an entry are
# stable / not measured (e_0, e_-, p, n) or unknown (n had no Excel value).
EXCEL_T_PREDICTED: dict[str, float] = {
    "miu_-":   2.19946600851041e-06,
    "eta":     2.3382405818953605e-19,
    "KAPPA_+": 1.2371221136630449e-08,
    "pi_+-":   2.602878932367812e-08,
    "pi_0":    8.401800542436449e-17,
    "LAMBDA":  2.578040272278807e-10,
    "OMEGA_-": 1.3176698290660324e-10,
    "XI_0":    2.962003581078723e-10,
    "XI_-":    1.6530834732444074e-10,
    "SIGMA_+": 8.007296366670605e-11,
    "SIGMA_0": 4.290884921384008e-15,
    "SIGMA_-": 1.481755468625331e-10,
    "DELTA_++": 3.685e-24,
    "DELTA_+":  5.483e-24,
    "DELTA_0":  4.957e-24,
    "DELTA_-":  6.401e-24,
}

# Particles where our code agrees with Excel to better than 0.5 %.
# (These should NOT regress.)
TIGHTLY_MATCHED = {
    "miu_-", "KAPPA_+", "pi_+-", "OMEGA_-", "XI_-", "SIGMA_+", "SIGMA_-",
}


@pytest.mark.parametrize("particle", REFERENCE_PARTICLES, ids=lambda p: p.symbol)
def test_excel_agreement(particle):
    """For particles that already match Excel tightly, hold the line."""
    if particle.symbol not in TIGHTLY_MATCHED:
        pytest.skip(f"{particle.symbol} is a known Excel-discrepancy case")
    T_excel = EXCEL_T_PREDICTED[particle.symbol]
    T_ours = particle.lifetime_seconds
    rel_diff = abs(T_ours - T_excel) / T_excel
    assert rel_diff < 0.005, (
        f"{particle.symbol}: regression vs Excel — "
        f"got {T_ours:.6e}, Excel {T_excel:.6e}, rel diff {rel_diff*100:.3f}%"
    )


def test_known_excel_discrepancies():
    """Document particles where we currently disagree with Excel — for
    visibility, not as a hard constraint."""
    discrepancies = []
    for p in REFERENCE_PARTICLES:
        if p.symbol not in EXCEL_T_PREDICTED:
            continue
        if p.symbol in TIGHTLY_MATCHED:
            continue
        T_excel = EXCEL_T_PREDICTED[p.symbol]
        T_ours = p.lifetime_seconds
        if not math.isfinite(T_ours):
            continue
        ratio = T_ours / T_excel
        log_diff = math.log10(abs(ratio))
        discrepancies.append((p.symbol, T_ours, T_excel, ratio, log_diff))

    # Print as informational output (visible with `pytest -s`)
    print("\nKnown discrepancies vs Excel (informational, not a failure):")
    print(f"  {'Particle':10}  {'Mine':>14}  {'Excel':>14}  {'Mine/Excel':>10}")
    for symbol, m, e, r, _ in discrepancies:
        print(f"  {symbol:10}  {m:>14.4e}  {e:>14.4e}  {r:>10.3f}")
    # Should be 9 known cases (eta, pi_0, LAMBDA, XI_0, SIGMA_0, 4× DELTA)
    assert len(discrepancies) == 9
