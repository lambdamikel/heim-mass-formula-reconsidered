"""
Probe the *functional form* of Heim's η:

    η(q, k) = (π^A / (π^A + (B + k)·q^C))^D     with default (A, B, C, D) = (4, 4, 4, 1/4)

If the loss has a sharp minimum at the published values, the form is
strongly constrained — i.e. η is not just one of many shapes that would
work. If the minima are flat or in unexpected places, η was effectively
hand-tuned in functional form.
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
# Parameterised eta
# ---------------------------------------------------------------------------
PI = math.pi


def make_eta(A: float, B: float, C: float, D: float):
    """Return η(q, k) with custom parameters."""
    def eta(q, k):
        denom = PI ** A + (B + k) * q ** C
        if denom <= 0:
            raise ValueError("denom <= 0")
        return (PI ** A / denom) ** D
    return eta


def patch_eta(eta_fn):
    original = const_mod.eta
    const_mod.eta = eta_fn
    const_mod.query_eta = eta_fn
    formulae._eta = eta_fn
    return original


def restore_eta(original):
    const_mod.eta = original
    const_mod.query_eta = original
    formulae._eta = original


def total_loss() -> float:
    return sum(
        ((p.mass_mev - p.m_exp_mev) / p.m_exp_mev) ** 2
        for p in REFERENCE_PARTICLES if p.m_exp_mev > 0
    )


# ---------------------------------------------------------------------------
# Sweep one parameter
# ---------------------------------------------------------------------------

def sweep_param(param_name: str, values: np.ndarray, defaults: dict) -> np.ndarray:
    """Return array of losses, one per value."""
    losses = []
    for v in values:
        kwargs = dict(defaults)
        kwargs[param_name] = float(v)
        try:
            eta_fn = make_eta(**kwargs)
            saved = patch_eta(eta_fn)
            try:
                losses.append(total_loss())
            except (ValueError, OverflowError, ZeroDivisionError):
                losses.append(float("nan"))
            finally:
                restore_eta(saved)
        except (ValueError, OverflowError, ZeroDivisionError):
            losses.append(float("nan"))
    return np.array(losses)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    outdir = Path(__file__).parent / "plots"
    outdir.mkdir(exist_ok=True)

    defaults = dict(A=4.0, B=4.0, C=4.0, D=0.25)

    # Sanity: with defaults, loss should equal Heim baseline
    saved = patch_eta(make_eta(**defaults))
    baseline = total_loss()
    restore_eta(saved)
    print(f"Baseline loss with reconstructed η defaults: {baseline:.6e}")
    print(f"  RMS rel err = {math.sqrt(baseline/20)*100:.4f} %")
    print()

    # Sweep configurations: param → (range, n_points, default)
    sweeps = {
        "A": (np.linspace(2.0, 6.0, 401), 4.0, "exponent on π in numerator/denom"),
        "B": (np.linspace(0.0, 10.0, 401), 4.0, "constant in (B + k)"),
        "C": (np.linspace(1.0, 8.0, 401), 4.0, "exponent on q"),
        "D": (np.linspace(0.05, 1.0, 401), 0.25, "outer exponent"),
    }

    results = {}
    for param, (values, default, desc) in sweeps.items():
        losses = sweep_param(param, values, defaults)
        results[param] = (values, losses, default, desc)

        valid = ~np.isnan(losses)
        if not np.any(valid):
            print(f"--- {param} : all evaluations failed ---\n")
            continue
        vL = losses[valid]
        vF = values[valid]
        i_min = int(np.argmin(vL))
        L_min = vL[i_min]
        f_min = vF[i_min]

        # baseline at the default
        idx_default = int(np.argmin(np.abs(values - default)))
        L_at_default = losses[idx_default]

        # tolerances: factor change to double the loss
        # find first crossing > 2·L_at_default to either side of default
        L_thresh = 2.0 * L_at_default
        above = np.where(vF > default)[0]
        below = np.where(vF < default)[0]
        f_double_pos = None
        f_double_neg = None
        for i in above:
            if vL[i] > L_thresh:
                f_double_pos = vF[i]
                break
        for i in below[::-1]:
            if vL[i] > L_thresh:
                f_double_neg = vF[i]
                break

        print(f"--- {param} ({desc}) ---")
        print(f"  Heim default       : {default}")
        print(f"  loss at default    : {L_at_default:.4e}")
        print(f"  empirical minimum  : {param} = {f_min:.4f}, loss = {L_min:.4e}")
        if f_double_pos is not None:
            print(f"  loss doubles at {param} = {f_double_pos:.4f}  (above default)")
        else:
            print(f"  loss never doubles above default in sweep")
        if f_double_neg is not None:
            print(f"  loss doubles at {param} = {f_double_neg:.4f}  (below default)")
        else:
            print(f"  loss never doubles below default in sweep")
        print(f"  failed evaluations : {(~valid).sum()} of {len(values)}")
        print()

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    for ax, (param, (values, losses, default, desc)) in zip(axes.flat, results.items()):
        valid = ~np.isnan(losses)
        ax.plot(values[valid], losses[valid], lw=1.5)
        ax.axvline(default, color="C1", ls="--", lw=1, label=f"Heim default = {default}")
        if np.any(valid):
            i_min = int(np.argmin(losses[valid]))
            ax.axvline(values[valid][i_min], color="C2", ls=":", lw=1,
                       label=f"min @ {values[valid][i_min]:.3f}")
        ax.set_yscale("log")
        ax.set_xlabel(f"parameter {param}: {desc}")
        ax.set_ylabel(r"$\Sigma\,(\Delta m / m_{\mathrm{exp}})^2$")
        ax.set_title(f"η functional sensitivity: {param}")
        ax.grid(True, which="both", ls=":", alpha=0.4)
        ax.legend(fontsize=9)

    fig.suptitle(
        r"Probing the functional form of $\eta(q,k) = (\pi^A / (\pi^A + (B+k)q^C))^D$",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(outdir / "sensitivity_eta_form.png", dpi=140)
    print(f"Plot saved → {outdir / 'sensitivity_eta_form.png'}")


if __name__ == "__main__":
    main()
