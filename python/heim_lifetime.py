"""
Run Heim's 1989 lifetime formula on the reference particle list and
print a comparison table against PDG measurements.

⚠ The lifetime implementation has not been verified against an upstream
reference — see lifetime.py docstring. Negative T or large discrepancies
(>3 orders of magnitude) likely indicate transcription errors in the
implementation of [B54]/[B55] or limitations of the formula itself.
"""

from __future__ import annotations

from math import isfinite, log10

from particle import REFERENCE_PARTICLES


def fmt(x: float) -> str:
    """Format a float compactly across many orders of magnitude."""
    if not isfinite(x):
        return "       inf      " if x > 0 else "      -inf      "
    if abs(x) < 1e-50:
        return "      ~0        "
    return f"{x:>+15.4e}"


def main() -> None:
    print()
    print("=" * 92)
    print(" Heim 1989 lifetime predictions vs. PDG measurements")
    print("=" * 92)
    print(
        f" {'particle':18}  q  {'T_predicted [s]':>16} {'T_measured [s]':>16} "
        f"{'log10(T_p/T_e)':>14}  notes"
    )
    print("-" * 92)

    n_negative = 0
    n_zero = 0
    n_close = 0       # |log err| < 0.5
    n_moderate = 0    # |log err| < 2
    n_far = 0         # |log err| ≥ 2
    n_no_exp = 0

    for p in REFERENCE_PARTICLES:
        T = p.lifetime_seconds
        q = round(p.charge)

        if T < 0:
            n_negative += 1
            note = "negative — sign issue / transcription"
        elif T == 0.0:
            n_zero += 1
            note = "zero — F·y vanishes (precision?)"
        else:
            note = ""

        if p.t_exp_sec > 0 and isfinite(T) and T > 0:
            log_err = log10(T / p.t_exp_sec)
            err_str = f"{log_err:+.2f}"
            ae = abs(log_err)
            if ae < 0.5:
                n_close += 1
            elif ae < 2.0:
                n_moderate += 1
            else:
                n_far += 1
        elif p.t_exp_sec == 0:
            err_str = "      "
            note = note or "stable / unknown"
            n_no_exp += 1
        else:
            err_str = "  ?   "

        T_exp_str = f"{p.t_exp_sec:>+15.4e}" if p.t_exp_sec else "       —       "

        print(
            f" {p.symbol:18} {q:+d}  {fmt(T):>16} {T_exp_str} "
            f"{err_str:>14}  {note}"
        )

    print("-" * 92)

    n_measured = sum(1 for p in REFERENCE_PARTICLES if p.t_exp_sec > 0)
    print(f" Particles with measured lifetime:   {n_measured}")
    print(f" Predictions within factor 3   (log err < 0.5):  {n_close}")
    print(f" Predictions within factor 100 (log err < 2.0):  {n_moderate}")
    print(f" Predictions off by ≥ 100x:                       {n_far}")
    print(f" Negative T (formula sign issue):                 {n_negative}")
    print(f" Zero T (numerical / formula limit):              {n_zero}")
    print()
    print(" Caveats:")
    print(" - This is a fresh implementation of [B47]–[B57] with no upstream")
    print("   bit-identical reference (Gildish 2006 and HeimGroup C# cover")
    print("   masses only). Discrepancies probably indicate transcription")
    print("   errors in the long b_1 / b_2 expressions, ambiguities in the")
    print("   1989 source typography, or convention issues (sign/abs).")
    print(" - The Σ_0 decays electromagnetically (→ Λγ); the formula")
    print("   appears to predict only weak-channel lifetimes and so misses")
    print("   Σ_0 by ~12 orders of magnitude.")
    print(" - The Δ resonances decay strongly via Δ → Nπ; the formula's")
    print("   F-factor vanishes for P=3, suggesting these states are")
    print("   outside the formula's intended scope.")
    print()


if __name__ == "__main__":
    main()
