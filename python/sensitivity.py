"""
Sensitivity analysis of the three empirically fitted constants in Heim's
1989 mass formula.

Per Heim (1989, p. 19): "the free eligible parameters for the expression φ
with eq. (B50) were fitted by empirical facts [i.e. ⁴√2, (π/e)², and
4π·⁴√(1/2)]."

This script tests whether those values actually sit at — or near — a local
minimum of the total mass-prediction error. If "yes": the empirical fit was
good. If "no": the published values are not even locally optimal, which
would suggest they were chosen for aesthetic reasons (closed-form geometric
expressions) rather than as the true error minimum.

The loss function is the sum of squared relative errors across the 20
particles with measured masses (e_0 has no measured mass and is skipped).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import formulae
from particle import REFERENCE_PARTICLES


# ---------------------------------------------------------------------------
# Constants under test
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FittedConstant:
    """A constant scheduled for sensitivity sweep."""
    attr: str          # attribute name in `formulae` module
    label: str         # short human label
    expression: str    # closed-form expression in [1989]
    original: float    # the published value


FITTED = [
    FittedConstant("FOURTH_ROOT_2",     "⁴√2",      "2^(1/4)",
                   formulae.FOURTH_ROOT_2),
    FittedConstant("PI_OVER_E_SQR",     "(π/e)²",   "(π/e)²",
                   formulae.PI_OVER_E_SQR),
    FittedConstant("FOUR_PI_OVER_4RT2", "4π/⁴√2",   "4π · 2^(−1/4)",
                   formulae.FOUR_PI_OVER_4RT2),
]


# ---------------------------------------------------------------------------
# Loss function
# ---------------------------------------------------------------------------

MEASURED_PARTICLES = [p for p in REFERENCE_PARTICLES if p.m_exp_mev > 0]


def total_loss() -> float:
    """
    Sum of squared relative errors across all measured particles.

    Returns the loss with the *currently configured* fitted constants in
    `formulae` (so callers should set those before invoking).
    """
    total = 0.0
    for p in MEASURED_PARTICLES:
        rel = (p.mass_mev - p.m_exp_mev) / p.m_exp_mev
        total += rel * rel
    return total


def loss_at(constant_attr: str, value: float) -> float:
    """Compute total loss while temporarily setting `formulae.<attr> = value`."""
    saved = getattr(formulae, constant_attr)
    setattr(formulae, constant_attr, value)
    try:
        return total_loss()
    finally:
        setattr(formulae, constant_attr, saved)


def loss_at_factor(constant: FittedConstant, factor: float) -> float:
    """Loss when `constant` is scaled by `factor` from its original value."""
    return loss_at(constant.attr, constant.original * factor)


# ---------------------------------------------------------------------------
# 1D sweep
# ---------------------------------------------------------------------------

def sweep_one(
    constant: FittedConstant, span: float = 0.1, n: int = 201
) -> tuple[np.ndarray, np.ndarray]:
    """
    Sweep one constant from (1 − span) to (1 + span) in `n` steps.

    Returns (factors, losses) as numpy arrays.
    """
    factors = np.linspace(1.0 - span, 1.0 + span, n)
    losses = np.array([loss_at_factor(constant, float(f)) for f in factors])
    return factors, losses


def find_minimum(factors: np.ndarray, losses: np.ndarray) -> tuple[float, float]:
    """Return (factor, loss) at the discrete minimum of the sweep."""
    i = int(np.argmin(losses))
    return float(factors[i]), float(losses[i])


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def baseline_report() -> None:
    """Print the loss at the published Heim values (factor = 1.0)."""
    L = total_loss()
    print(f"Baseline (Heim 1989 published values):")
    print(f"  Σ(Δ/m_exp)² = {L:.6e}")
    print(f"  RMS relative error = {math.sqrt(L / len(MEASURED_PARTICLES)) * 100:.4f}%")
    print()


def sweep_report(constant: FittedConstant, span: float = 0.1, n: int = 201) -> dict:
    """Run a single sweep and print + return the summary."""
    factors, losses = sweep_one(constant, span, n)
    f_min, L_min = find_minimum(factors, losses)
    L_baseline = loss_at_factor(constant, 1.0)

    print(f"--- {constant.label}  (= {constant.expression} ≈ {constant.original:.6f}) ---")
    print(f"  Heim value      :  factor = 1.0      loss = {L_baseline:.6e}")
    print(f"  Empirical min   :  factor = {f_min:.6f}  loss = {L_min:.6e}")
    if abs(f_min - 1.0) < (factors[1] - factors[0]) * 0.6:
        verdict = "✓ Heim's value sits at the discrete minimum (within sweep resolution)."
    elif L_baseline < L_min * 1.001:
        verdict = "≈ Heim's value is within 0.1 % of the empirical minimum (effectively optimal)."
    else:
        improvement = (L_baseline - L_min) / L_baseline * 100
        verdict = f"⚠ Empirical min beats Heim's by {improvement:.2f} % at factor {f_min:.4f}."
    print(f"  Verdict         :  {verdict}")
    print()

    return {
        "label": constant.label,
        "factors": factors,
        "losses": losses,
        "f_min": f_min,
        "L_min": L_min,
        "L_baseline": L_baseline,
    }


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_sweeps(results: list[dict], outpath: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    for ax, res in zip(axes, results):
        ax.plot(res["factors"], res["losses"], lw=1.5)
        ax.axvline(1.0, color="C1", lw=1, ls="--", label=f"Heim: f=1")
        ax.axvline(res["f_min"], color="C2", lw=1, ls=":", label=f"min: f={res['f_min']:.4f}")
        ax.set_yscale("log")
        ax.set_xlabel(f"scaling factor for {res['label']}")
        ax.set_title(res["label"])
        ax.grid(True, which="both", ls=":", alpha=0.4)
        ax.legend(fontsize=8, loc="upper left")
    axes[0].set_ylabel(r"$\Sigma_{i}\,(\Delta m_i / m_{i,\mathrm{exp}})^2$")
    fig.suptitle(
        "Sensitivity of total mass error to Heim's three fitted constants  "
        "(20 particles, sweep ±10 %)",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(outpath, dpi=140)
    print(f"Plot saved → {outpath}")


# ---------------------------------------------------------------------------
# Joint scan (2D heatmap of any two constants)
# ---------------------------------------------------------------------------

def joint_scan(
    c1: FittedConstant, c2: FittedConstant, span: float = 0.05, n: int = 41
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """2D scan: factor1 × factor2.  Returns (F1, F2, L)."""
    f = np.linspace(1.0 - span, 1.0 + span, n)
    F1, F2 = np.meshgrid(f, f, indexing="xy")
    L = np.zeros_like(F1)

    saved1 = getattr(formulae, c1.attr)
    saved2 = getattr(formulae, c2.attr)
    try:
        for i in range(n):
            for j in range(n):
                setattr(formulae, c1.attr, c1.original * F1[i, j])
                setattr(formulae, c2.attr, c2.original * F2[i, j])
                L[i, j] = total_loss()
    finally:
        setattr(formulae, c1.attr, saved1)
        setattr(formulae, c2.attr, saved2)
    return F1, F2, L


def plot_joint(
    c1: FittedConstant,
    c2: FittedConstant,
    F1: np.ndarray,
    F2: np.ndarray,
    L: np.ndarray,
    outpath: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    cs = ax.contourf(F1, F2, np.log10(L), levels=24, cmap="viridis")
    ax.contour(F1, F2, np.log10(L), levels=12, colors="white", linewidths=0.4, alpha=0.5)
    ax.plot(1.0, 1.0, "rx", ms=12, mew=2, label="Heim (1, 1)")
    i, j = np.unravel_index(np.argmin(L), L.shape)
    ax.plot(F1[i, j], F2[i, j], "g*", ms=14, label=f"min ({F1[i,j]:.3f}, {F2[i,j]:.3f})")
    ax.set_xlabel(f"factor for {c1.label}")
    ax.set_ylabel(f"factor for {c2.label}")
    ax.set_title(f"Joint sensitivity: {c1.label} × {c2.label}\nlog₁₀ Σ(Δ/m)²")
    ax.legend()
    fig.colorbar(cs, ax=ax, label=r"log$_{10}$ loss")
    fig.tight_layout()
    fig.savefig(outpath, dpi=140)
    print(f"Plot saved → {outpath}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    outdir = Path(__file__).parent / "plots"
    outdir.mkdir(exist_ok=True)

    print("=" * 78)
    print("Heim 1989 mass-formula — sensitivity to fitted constants")
    print("=" * 78)
    print(f"Particle set: {len(MEASURED_PARTICLES)} particles with measured mass")
    print()

    baseline_report()

    print("-" * 78)
    print("1D sweeps (each constant individually, ±10 %, 201 points)")
    print("-" * 78)
    print()
    results = [sweep_report(c, span=0.10, n=201) for c in FITTED]

    plot_sweeps(results, outdir / "sensitivity_1d.png")

    print()
    print("-" * 78)
    print("2D joint scan (all pairs, ±5 %, 41×41 grid)")
    print("-" * 78)
    print()

    pairs = [(0, 1), (0, 2), (1, 2)]
    for i, j in pairs:
        c1, c2 = FITTED[i], FITTED[j]
        F1, F2, L = joint_scan(c1, c2, span=0.05, n=41)
        i_min, j_min = np.unravel_index(np.argmin(L), L.shape)
        L_at_heim = L[L.shape[0] // 2, L.shape[1] // 2]
        print(
            f"{c1.label} × {c2.label}: "
            f"min at ({F1[i_min, j_min]:.4f}, {F2[i_min, j_min]:.4f}), "
            f"loss = {L[i_min, j_min]:.4e};   "
            f"Heim baseline = {L_at_heim:.4e}"
        )
        plot_joint(c1, c2, F1, F2, L,
                   outdir / f"sensitivity_2d_{c1.attr}_{c2.attr}.png")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
