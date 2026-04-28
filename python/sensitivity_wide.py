"""
Wide-range sweep — does the loss EVER respond strongly to the fitted constants?
Tries factors from 10⁻³ up to 10³ on a log scale.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import formulae
from particle import REFERENCE_PARTICLES


CONSTANTS = [
    ("FOURTH_ROOT_2",     "⁴√2",    formulae.FOURTH_ROOT_2),
    ("PI_OVER_E_SQR",     "(π/e)²", formulae.PI_OVER_E_SQR),
    ("FOUR_PI_OVER_4RT2", "4π/⁴√2", formulae.FOUR_PI_OVER_4RT2),
]


def total_loss():
    return sum(
        ((p.mass_mev - p.m_exp_mev) / p.m_exp_mev) ** 2
        for p in REFERENCE_PARTICLES if p.m_exp_mev > 0
    )


def loss_at(attr, value):
    saved = getattr(formulae, attr)
    setattr(formulae, attr, value)
    try:
        return total_loss()
    finally:
        setattr(formulae, attr, saved)


def wide_sweep(attr, original, log_span=3.0, n=301):
    """Sweep `attr` on a log scale: factor ∈ [10⁻³ … 10³]."""
    factors = np.logspace(-log_span, log_span, n)
    losses = []
    failures = 0
    for f in factors:
        try:
            losses.append(loss_at(attr, original * f))
        except (ValueError, OverflowError, ZeroDivisionError):
            losses.append(float("nan"))
            failures += 1
    return factors, np.array(losses), failures


def main():
    outdir = Path(__file__).parent / "plots"
    outdir.mkdir(exist_ok=True)

    baseline = total_loss()
    print(f"Baseline loss: {baseline:.4e}  (RMS rel err = {math.sqrt(baseline/20)*100:.4f} %)")
    print()

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    for ax, (attr, label, original) in zip(axes, CONSTANTS):
        factors, losses, fails = wide_sweep(attr, original)
        valid = ~np.isnan(losses)
        ax.semilogx(factors[valid], losses[valid], lw=1.4)
        ax.axhline(baseline, color="C1", ls="--", lw=1, label="Heim baseline")
        ax.axvline(1.0, color="C1", ls=":", lw=1)
        ax.set_yscale("log")
        ax.set_xlabel(f"factor for {label}")
        ax.set_title(f"{label} — wide sweep")
        ax.grid(True, which="both", ls=":", alpha=0.4)
        ax.legend(fontsize=8)

        # Report
        valid_losses = losses[valid]
        valid_factors = factors[valid]
        i_min = int(np.argmin(valid_losses))
        L_min = valid_losses[i_min]
        f_min = valid_factors[i_min]
        L_at_1 = losses[len(factors) // 2]  # factor=1 is at midpoint of log scale
        # …or more reliably:
        L_at_1 = loss_at(attr, original)

        # Where does the loss double? (a measure of "how bad before broken")
        twox = np.where(valid_losses > 2 * L_at_1)[0]
        f_double = valid_factors[twox[0]] if len(twox) > 0 else None

        print(f"--- {label} ---")
        print(f"  Heim value (factor 1)  : loss = {L_at_1:.4e}")
        print(f"  Empirical min          : factor {f_min:.4f}, loss = {L_min:.4e}")
        if f_double is not None:
            print(f"  Loss doubles at factor : {f_double:.4f}  (or its reciprocal ~{1/f_double:.4f})")
        else:
            print(f"  Loss never doubles in [{factors[0]:.0e}, {factors[-1]:.0e}]")
        print(f"  NaN/exceptions         : {fails} of {len(factors)}")
        print()

    axes[0].set_ylabel(r"$\Sigma\,(\Delta m / m_{\mathrm{exp}})^2$")
    fig.suptitle(
        "Wide-range sensitivity: factors 10⁻³ to 10³ (log scale)",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(outdir / "sensitivity_wide.png", dpi=140)
    print(f"Plot saved → {outdir / 'sensitivity_wide.png'}")


if __name__ == "__main__":
    main()
