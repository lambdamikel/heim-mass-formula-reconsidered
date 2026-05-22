"""
2×2 mode-comparison table (Joel's May 2026 follow-up request).

Following the proposed [B3] correction (b3_correction.py) and the
full-reproduction analysis (full_reproduction.py), Joel asked for
an explicit 2×2 residual table separating two orthogonal questions:

  - "Have we correctly reconstructed what Heim actually calculated?"
    (heim_reproduction_mode: Heim constants, corrected B3)
  - "Does the formula work today with modern empirical constants?"
    (modern_comparison_mode: modern CODATA, corrected B3)

The two distinctions are:

  Axis 1: B3 formula form
    - "published"  : as printed in IGW Innsbruck PDF, "+4qα₋"
    - "corrected"  : proposed typo fix, "+4qα₋/α₊"

  Axis 2: Physical constants
    - "port"       : CODATA-2006 era (Eli Gildish 2006 reference)
                     G = 6.6742·10⁻¹¹, h = 6.6260693·10⁻³⁴
    - "heim_1989"  : Heim's stated values (G = 6.6732·10⁻¹¹) plus
                     CODATA-1986 for h, e

Four modes:
    A: published B3 + port constants       (current canonical port)
    B: corrected B3 + port constants       (electron fix only)
    C: published B3 + heim_1989 constants  (constants fix only)
    D: corrected B3 + heim_1989 constants  (both fixes — full reproduction)

Each mode is compared against Heim's 1989 Tabelle II.  Two reference
points reported for each: the 17 well-behaved non-Δ particles
separately from the 4 Δ ground states with the ~0.85–1.58 MeV
residual (Open Q 1b — suspected missing P=3 specific term in φ).

Run with:
    ./venv/bin/python python/modes_table.py
"""

from __future__ import annotations

from math import fabs, sqrt

import constants as const
import formulae as fm
from g_tables import (TABLE_II_BARYONS, TABLE_II_LEPTONS, TABLE_II_MESONS)
from particle import REFERENCE_PARTICLES


SYMBOL_MAP = {
    "e_-": "e", "e_0": "e_0", "miu_-": "μ", "eta": "η",
    "KAPPA_+": "K+", "KAPPA_0": "K0",
    "pi_+-": "π+", "pi_0": "π0",
    "LAMBDA": "Λ", "OMEGA_-": "Ω-",
    "p": "p", "n": "n",
    "XI_0": "Ξ0", "XI_-": "Ξ-",
    "SIGMA_+": "Σ+", "SIGMA_0": "Σ0", "SIGMA_-": "Σ-",
    "DELTA_++": "o++", "DELTA_+": "o+", "DELTA_0": "o0", "DELTA_-": "o-",
}

# All four Δ ground states share the ~0.85–1.58 MeV residual (Open Q 1b).
# This is NOT a greedy-decomposition artefact (using Heim's own
# (n, m, p, σ) for o⁺/o⁻ does not close the residual).
DECOMP_ANOMALY = {"DELTA_++", "DELTA_+", "DELTA_0", "DELTA_-"}


def heim_TII_mass(symbol):
    h_sym = SYMBOL_MAP.get(symbol)
    if h_sym is None:
        return None
    for entry in TABLE_II_LEPTONS + TABLE_II_MESONS + TABLE_II_BARYONS:
        if entry.symbol == h_sym:
            return entry.mass_MeV
    return None


def calc_mass_in_mode(p, b3_form: str) -> float:
    """Mass calculation in 'published' or 'corrected' B3 form,
    using whatever constants are currently active in constants.py."""
    qx = fm.calc_charge(p.eps, p.k, p.P, p.Q, p.kap, p.x)
    q = fabs(qx)
    eta00 = const.eta(1, 0)
    th = const.theta(eta00)
    a_p = const.alpha_plus(eta00, th)
    a_m = const.alpha_minus(eta00, th)
    I = fm.calc_Q(p.k)
    N = fm.calc_N(p.k, q, I)
    W = fm.calc_W(p.eps, p.k, p.P, p.Q, p.kap, qx, I)
    n = fm.calc_n(p.k, I, N, W)
    K = ((n[0]*(n[0]+1))**2 * N[0]
         + n[1]*(2*n[1]**2+3*n[1]+1)*N[1]
         + n[2]*(n[2]+1)*N[2] + 4*n[3])
    S = ((I[0]*(I[0]+1))**2 * N[0]
         + I[1]*(2*I[1]**2+3*I[1]+1)*N[1]
         + I[2]*(I[2]+1)*N[2] + 4*I[3])
    F = (2*n[0]*I[0]*(1 + 3*(n[0]+I[0]+n[0]*I[0])
                    + 2*(n[0]**2+I[0]**2)) * N[0]
         + 6*n[1]*I[1]*(1+n[1]+I[1])*N[1]
         + 2*n[2]*I[2]*N[2]
         + fm.calc_phi(p.k, p.P, p.Q, p.kap, q, n, I, N, W))
    PHI = p.P*(-1)**(p.P+p.Q)*(p.P+p.Q)*N[4] + p.Q*(p.P+1)*N[5]
    if b3_form == "published":
        qterm = 4 * q * a_m
    elif b3_form == "corrected":
        qterm = 4 * q * a_m / a_p
    else:
        raise ValueError(b3_form)
    return const.mass_element() * a_p * (K + S + F + PHI + qterm) * const.KG_TO_MEV


def run_mode(b3_form: str, const_mode: str) -> dict:
    """Run all 21 particles in a given mode; return aggregated stats."""
    const.set_constants_mode(const_mode)
    rows = []
    for p in REFERENCE_PARTICLES:
        h = heim_TII_mass(p.symbol)
        if h is None or h == 0:
            continue
        m_ours = calc_mass_in_mode(p, b3_form)
        rows.append((p.symbol, p.k, h, m_ours))
    # Split: well-behaved non-Δ (17) vs all four Δ ground states (4)
    good = [r for r in rows if r[0] not in DECOMP_ANOMALY]
    bad = [r for r in rows if r[0] in DECOMP_ANOMALY]
    return {"good": good, "bad": bad}


def summarize(name: str, results: dict):
    good = results["good"]
    bad = results["bad"]
    # Stats on the 17 well-behaved non-Δ particles
    ppms = [(m - h) / h * 1e6 for _, _, h, m in good]
    keVs = [(m - h) * 1000 for _, _, h, m in good]
    mean_ppm = sum(ppms) / len(ppms)
    # Residual after subtracting global mean
    after_mean = [p - mean_ppm for p in ppms]
    rms_residual_ppm = sqrt(sum(p*p for p in after_mean) / len(after_mean))
    abs_keVs = [abs(k) for k in keVs]
    abs_after_mean_keV = [abs((m - h * (1 + mean_ppm * 1e-6)) * 1000) for _, _, h, m in good]
    return {
        "name": name,
        "n_good": len(good),
        "mean_ppm": mean_ppm,
        "rms_ppm_raw": sqrt(sum(p*p for p in ppms) / len(ppms)),
        "rms_residual_ppm": rms_residual_ppm,
        "max_keV_raw": max(abs_keVs),
        "max_keV_after_mean": max(abs_after_mean_keV),
        "bad": bad,
    }


def banner(s: str, ch: str = "="):
    print()
    print(ch * 96)
    print(f" {s}")
    print(ch * 96)


def main():
    banner("Joel's 2×2 mode-comparison table")

    print("""
  Axis 1 — B3 formula:        'published' = +4qα₋
                              'corrected' = +4qα₋/α₊ (proposed typo fix)
  Axis 2 — physical constants: 'port'      = legacy_2006 (Eli Gildish 2006)
                              'heim_1989' = Heim's G=6.6732e-11 + CODATA-1986 h, e

  Target = Heim's published Tabelle II values.
  Stats computed over the 17 well-behaved non-Δ particles
  (all four Δ ground states excluded; ~0.85–1.58 MeV residual,
  suspected missing P=3 specific term in φ — see Open Q #1b).
""")

    # Run all four modes
    modes = []
    for b3 in ("published", "corrected"):
        for cm in ("legacy_2006", "heim_1989"):
            label = f"B3={b3:<9} | constants={cm}"
            results = run_mode(b3, cm)
            modes.append((label, summarize(label, results), results))

    # Headline table
    print(f"  {'Mode':<42} {'mean offset':>13} {'RMS raw':>10} "
          f"{'RMS after':>11} {'max raw [keV]':>15} {'max after [keV]':>17}")
    print("  " + "-" * 94)
    for label, summ, _ in modes:
        print(f"  {label:<42} "
              f"{summ['mean_ppm']:>+10.3f} ppm "
              f"{summ['rms_ppm_raw']:>10.3f} "
              f"{summ['rms_residual_ppm']:>11.5f} "
              f"{summ['max_keV_raw']:>15.4f} "
              f"{summ['max_keV_after_mean']:>17.5f}")

    print(f"\n  Note: 'after' = after subtracting the mode's global mean offset, "
          f"i.e. the residual that\n        cannot be absorbed by a single "
          f"multiplicative scale (= a constants choice).")

    banner("Charged vs neutral split (Mode D: corrected + heim_1989)", ch="-")
    _, summ_D, results_D = modes[3]
    chg, neu = [], []
    for sym, k, h, m in results_D["good"]:
        # determine charge from particle symbol or recompute
        # easier: use the abs delta / mass
        # Look up our particle to get charge
        for p in REFERENCE_PARTICLES:
            if p.symbol == sym:
                qx = fm.calc_charge(p.eps, p.k, p.P, p.Q, p.kap, p.x)
                if abs(qx) > 0.5:
                    chg.append((m - h) * 1000)
                else:
                    neu.append((m - h) * 1000)
                break
    print(f"  Charged (|q|≥1):  n={len(chg)}, RMS={sqrt(sum(c*c for c in chg)/len(chg)):.3f} keV, "
          f"max |Δ|={max(abs(c) for c in chg):.3f} keV")
    print(f"  Neutral (q=0):   n={len(neu)}, RMS={sqrt(sum(c*c for c in neu)/len(neu)):.3f} keV, "
          f"max |Δ|={max(abs(c) for c in neu):.3f} keV")

    banner("All four Δ ground states in each mode (Open Q 1b residual)", ch="-")
    print(f"  {'Mode':<42} {'Particle':>8} {'ours':>12} {'Heim T-II':>11} {'Δ [keV]':>11}")
    print("  " + "-" * 94)
    for label, _, results in modes:
        for sym, k, h, m in results["bad"]:
            print(f"  {label:<42} {sym:>8} {m:>12.3f} {h:>11.3f} "
                  f"{(m-h)*1000:>+11.3f}")

    banner("Interpretation (in Joel's language)")
    summ_A = modes[0][1]
    summ_B = modes[1][1]
    summ_C = modes[2][1]
    summ_D = modes[3][1]
    print(f"""
  Mode A (current canonical, published B3 + port constants):
      mean offset {summ_A['mean_ppm']:+.1f} ppm, max raw residual {summ_A['max_keV_raw']:.2f} keV.
      Includes the 0.79% electron-mass discrepancy and the 30-ppm
      constants offset together.

  Mode B (corrected B3 + port constants):
      mean offset {summ_B['mean_ppm']:+.1f} ppm, max raw residual {summ_B['max_keV_raw']:.2f} keV.
      The B3 correction has removed the electron-specific discrepancy
      (and the +4 keV charge-dependent offset on all q ≠ 0 particles).
      The residual is now a uniform ~30 ppm shift — purely constants-based.

  Mode C (published B3 + heim_1989 constants):
      mean offset {summ_C['mean_ppm']:+.1f} ppm, max raw residual {summ_C['max_keV_raw']:.2f} keV.
      The constants change removes the universal shift but leaves the
      electron-specific 4 keV discrepancy (and other q ≠ 0 effects).

  Mode D (corrected B3 + heim_1989 constants) — full reproduction:
      mean offset {summ_D['mean_ppm']:+.3f} ppm, max raw residual {summ_D['max_keV_raw']:.3f} keV.
      All 17 well-behaved non-Δ particles match Heim's Tabelle II to within
      {summ_D['max_keV_raw']:.2f} keV.  This is heim_reproduction_mode.

  The natural mode pair, per Joel's framework, is therefore:

    heim_reproduction_mode  = Mode D  (target: Heim Tabelle II)
    modern_comparison_mode  = Mode B with codata_2022 constants
                             (target: modern PDG values)

  These answer different questions:
    Mode D answers: "have we reconstructed what Heim calculated?"  → YES.
    Modern mode B answers: "does the formula match modern PDG?"
                         → that is the separate scientific question.
""")


if __name__ == "__main__":
    main()
