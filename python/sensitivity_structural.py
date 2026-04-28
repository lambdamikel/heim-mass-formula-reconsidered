"""
Sensitivity of the mass formula to the *structural* quantities:
    μ  — the mass element  (sets the overall scale)
    η  — the auxiliary function  (enters everywhere via α±, α, N_i, …)
    θ  — derived from η, but also a scaling input itself
    Q_i — the four "structure constants" (Q_n, Q_m, Q_p, Q_σ) per k

Compare directly with the previous sensitivity result for the three
"fitted" constants (⁴√2, (π/e)², 4π/⁴√2): if those structural quantities
respond sharply where the fitted constants don't, the bulk of Heim's
predictive accuracy comes from structure, not from fits.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import constants as const_mod
import formulae
from particle import REFERENCE_PARTICLES


# ---------------------------------------------------------------------------
# Loss
# ---------------------------------------------------------------------------

def total_loss() -> float:
    return sum(
        ((p.mass_mev - p.m_exp_mev) / p.m_exp_mev) ** 2
        for p in REFERENCE_PARTICLES if p.m_exp_mev > 0
    )


# ---------------------------------------------------------------------------
# Helpers — monkey-patch auxiliary functions in `constants` AND `formulae`
# (formulae imports them by name, so patching only constants is not enough).
# ---------------------------------------------------------------------------

def patch_eta(factor: float):
    original = const_mod.eta
    patched = lambda q, k: original(q, k) * factor
    const_mod.eta = patched
    const_mod.query_eta = patched
    formulae._eta = patched
    return original


def restore_eta(original):
    const_mod.eta = original
    const_mod.query_eta = original
    formulae._eta = original


def patch_theta(factor: float):
    original = const_mod.theta
    patched = lambda eta_val: original(eta_val) * factor
    const_mod.theta = patched
    const_mod.query_tet = patched
    formulae._theta = patched
    return original


def restore_theta(original):
    const_mod.theta = original
    const_mod.query_tet = original
    formulae._theta = original


def patch_miu(factor: float):
    original = const_mod.mass_element
    patched = lambda: original() * factor
    const_mod.mass_element = patched
    const_mod.query_miu = patched
    formulae.mass_element = patched
    return original


def restore_miu(original):
    const_mod.mass_element = original
    const_mod.query_miu = original
    formulae.mass_element = original


def patch_calcQ(factor: float):
    """Scale all four Q_n, Q_m, Q_p, Q_σ by `factor`. Truncates to int."""
    original = formulae.calc_Q
    def patched(k):
        a, b, c, d = original(k)
        return (int(a * factor), int(b * factor), int(c * factor), int(d * factor))
    formulae.calc_Q = patched
    return original


def restore_calcQ(original):
    formulae.calc_Q = original


# ---------------------------------------------------------------------------
# Sweep machinery
# ---------------------------------------------------------------------------

def sweep_with_patcher(patch_fn, restore_fn, factors):
    losses = []
    for f in factors:
        original = patch_fn(float(f))
        try:
            losses.append(total_loss())
        except (ValueError, OverflowError, ZeroDivisionError):
            losses.append(float("nan"))
        finally:
            restore_fn(original)
    return np.array(losses)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def report(label: str, factors: np.ndarray, losses: np.ndarray, baseline: float):
    valid = ~np.isnan(losses)
    if not np.any(valid):
        print(f"--- {label} : ALL EVALUATIONS FAILED ---")
        return

    vL, vF = losses[valid], factors[valid]
    i_min = int(np.argmin(vL))
    L_min = vL[i_min]
    f_min = vF[i_min]

    # local sensitivity: how does loss change at f=1 ± 1%?
    near_1_pct_idx = np.argmin(np.abs(factors - 1.01))
    L_at_1_01 = losses[near_1_pct_idx]

    # how far from 1.0 to double the loss?
    f_double_pos = None
    f_double_neg = None
    above_1 = factors > 1.0
    below_1 = factors < 1.0
    pos_double = np.where((losses > 2 * baseline) & above_1)[0]
    neg_double = np.where((losses > 2 * baseline) & below_1)[0]
    if len(pos_double) > 0:
        f_double_pos = factors[pos_double[0]]
    if len(neg_double) > 0:
        f_double_neg = factors[neg_double[-1]]

    print(f"--- {label} ---")
    print(f"  baseline (f=1)       : loss = {baseline:.4e}")
    print(f"  empirical min        : factor {f_min:.4f}, loss = {L_min:.4e}")
    print(f"  loss at f=1.01       : {L_at_1_01:.4e}  (change {(L_at_1_01-baseline)/baseline*100:+.4f} %)")
    if f_double_pos is not None:
        print(f"  loss doubles at f>1  : factor {f_double_pos:.4f}")
    else:
        print(f"  loss never doubles for f>1 in sweep")
    if f_double_neg is not None:
        print(f"  loss doubles at f<1  : factor {f_double_neg:.4f}")
    else:
        print(f"  loss never doubles for f<1 in sweep")
    print(f"  failed evaluations   : {(~valid).sum()} of {len(factors)}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    outdir = Path(__file__).parent / "plots"
    outdir.mkdir(exist_ok=True)

    baseline = total_loss()
    print(f"Baseline loss: {baseline:.4e}  (RMS rel err = {math.sqrt(baseline/20)*100:.4f} %)")
    print()

    # μ — narrow range, since it scales masses linearly
    factors_narrow = np.linspace(0.99, 1.01, 401)
    # η, θ — moderately narrow (η ≈ 0.99, so factor > 1.01 makes η > 1 → broken sqrt)
    factors_eta_th = np.linspace(0.95, 1.005, 401)
    # Q_i — wider, since they're large integers
    factors_Q = np.linspace(0.95, 1.05, 401)

    print("=" * 78)
    print("Structural-quantity sensitivity")
    print("=" * 78)
    print()

    sweeps = []

    # μ
    L = sweep_with_patcher(patch_miu, restore_miu, factors_narrow)
    report("μ (mass element)", factors_narrow, L, baseline)
    sweeps.append(("μ", factors_narrow, L))

    # η — careful, η ≈ 0.99, scaling > 1.01 → η > 1 → math errors
    L = sweep_with_patcher(patch_eta, restore_eta, factors_eta_th)
    report("η (auxiliary function)", factors_eta_th, L, baseline)
    sweeps.append(("η", factors_eta_th, L))

    # θ
    factors_theta = np.linspace(0.95, 1.05, 401)
    L = sweep_with_patcher(patch_theta, restore_theta, factors_theta)
    report("θ (= 5η + 2√η + 1)", factors_theta, L, baseline)
    sweeps.append(("θ", factors_theta, L))

    # Q_i
    L = sweep_with_patcher(patch_calcQ, restore_calcQ, factors_Q)
    report("Q_n, Q_m, Q_p, Q_σ (uniform scale)", factors_Q, L, baseline)
    sweeps.append(("Q_i", factors_Q, L))

    # ---------------------------------------------------------------
    # Plots
    # ---------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    for ax, (label, factors, losses) in zip(axes.flat, sweeps):
        valid = ~np.isnan(losses)
        ax.plot(factors[valid], losses[valid], lw=1.5)
        ax.axhline(baseline, color="C1", ls="--", lw=1, label="Heim baseline")
        ax.axvline(1.0, color="C1", ls=":", lw=1)
        ax.set_yscale("log")
        ax.set_xlabel(f"scaling factor for {label}")
        ax.set_ylabel(r"$\Sigma\,(\Delta m / m_{\mathrm{exp}})^2$")
        ax.set_title(f"{label} — sensitivity")
        ax.grid(True, which="both", ls=":", alpha=0.4)
        ax.legend(fontsize=9)

    fig.suptitle(
        "Structural sensitivity: μ, η, θ, Q_i — compare with the flat sweeps "
        "for the 3 fitted constants",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(outdir / "sensitivity_structural.png", dpi=140)
    print(f"Plot saved → {outdir / 'sensitivity_structural.png'}")


if __name__ == "__main__":
    main()
