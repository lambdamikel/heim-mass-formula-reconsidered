"""
Heim's five-neutrino prediction from G-Tabelle II.
==================================================

The historical Heim/Arbeitskreis transmission set
(`downloads/G_Ausgewaehlte_Ergebnisse.pdf`, Tabelle II, page 3,
"Theoretical Data of Elementary Particles … Calculated by B. Heim
1989") lists rest masses for **five** neutrino species — three with
Standard-Model partners (ν_e, ν_μ, ν_τ) and two additional ones
without Standard-Model counterparts (ν_4, ν_5).

This script:

  1. Lists the Heim 1989 theoretical values.
  2. Compares them against modern experimental upper bounds:
       - KATRIN (electron-neutrino mass)
       - Accelerator constraints on ν_μ, ν_τ
       - Beta-decay endpoint searches on heavy sterile neutrinos
       - PIENU / PIPENU on heavy neutral leptons in 50-400 MeV range
  3. Identifies which Heim predictions are currently consistent,
     in tension, or already ruled out.

This is a concrete, falsifiable Heim-framework prediction that the
README had not previously documented.  It was surfaced during a
May 2026 source audit triggered by Joel's Discord review.

Run with:
    ./venv/bin/python python/heim_neutrinos.py
"""

from __future__ import annotations


# --------------------------------------------------------------------
# Heim 1989 — G-Tabelle II values (in MeV)
# --------------------------------------------------------------------
# Source: downloads/G_Ausgewaehlte_Ergebnisse.pdf, page 3,
# Tabelle II "Theoretical Data of Elementary Particles
# with Mean Lives > 10^-16 sec Calculated by B. Heim 1989".

HEIM_NEUTRINOS = [
    # (name,  Heim mass MeV,        spin, baryon#, status_note)
    # IMPORTANT: G-Tabelle II uses MeV throughout. The "× 10⁻⁶" notation
    # appears only on the ν_e row, NOT on ν_μ..ν_5. So:
    #   ν_e = 0.00381 × 10⁻⁶ MeV = 3.81e-9 MeV = 3.81 meV
    #   ν_μ = 0.00537      MeV  = 5.37e-3 MeV = 5.37 keV
    #   ν_τ = 0.010752     MeV  = 10.75 keV
    #   ν_4 = 0.021059     MeV  = 21.06 keV
    #   ν_5 = 0.207001     MeV  = 207.0 keV
    ("ν_e",   3.81e-9,    0.5, 0, "matches SM electron neutrino label"),
    ("ν_μ",   5.37e-3,    0.5, 0, "Heim's muon-neutrino label; "
                                  "in tension with cosmology if mixing"),
    ("ν_τ",   10.752e-3,  0.5, 0, "Heim's tau-neutrino label; "
                                  "in tension with cosmology if mixing"),
    ("ν_4",   21.059e-3,  0.5, 0, "FOURTH-GENERATION — no SM counterpart"),
    ("ν_5",   207.001e-3, 0.5, 0, "FIFTH-GENERATION — heavy neutral lepton"),
]


# --------------------------------------------------------------------
# Experimental bounds (2026)
# --------------------------------------------------------------------
# All bounds in MeV.  "<x" = upper bound on rest mass.

BOUNDS = [
    # (regime, upper_bound_MeV, source)
    ("ν_e direct (KATRIN 2024)",            0.45e-6,   "KATRIN tritium β-decay endpoint"),
    ("ν_e cosmological (Planck 2018+BAO)",  0.12e-6,   "ΣΣm_ν < 0.12 eV (95 % CL)"),
    ("ν_μ direct (PSI π→μν)",               0.19,      "0.19 MeV upper bound"),
    ("ν_τ direct (ALEPH τ→5πν)",            18.2,      "18.2 MeV upper bound"),
    # Heavy neutral lepton searches:
    ("HNL 1-450 MeV (PIENU π→eν)",          0.005,     "|U_e4|² ≲ 10⁻⁵ for m_4 ~ 50-130 MeV"),
    ("HNL 50-300 MeV (NA62 K→eν)",          0.001,     "|U_e4|² ≲ 10⁻⁶ for m_4 ~ 100 MeV"),
    ("HNL > 200 MeV (T2K, NA62)",           0.001,     "|U_e4|² ≲ 10⁻⁷ for m_4 ~ 200-400 MeV"),
]


def banner(s: str, ch: str = "="):
    print()
    print(ch * 78)
    print(f" {s}")
    print(ch * 78)


def evaluate_status(name: str, m_MeV: float) -> str:
    """Roughly classify each Heim neutrino against current bounds."""
    m_eV = m_MeV * 1e6
    if m_eV < 1.0:           # sub-eV
        return ("consistent with KATRIN 2024 upper bound (0.45 eV); "
                "below cosmological Σm_ν < 0.12 eV when treated alone.")
    if m_eV < 1e3:           # 1 eV to 1 keV
        return ("active-flavour interpretation RULED OUT by cosmological "
                "Σm_ν < 0.12 eV.  Only viable as a sterile / non-mixing "
                "state, in which case standard cosmology bounds do not apply "
                "directly.")
    if m_eV < 1e6:           # 1 keV to 1 MeV
        return ("keV-scale neutral lepton regime.  Heim's PSI direct bound "
                "(0.19 MeV for ν_μ) is satisfied numerically, but the "
                "cosmological bound Σm_ν < 0.12 eV is violated by >10⁴× if "
                "this state mixes appreciably with the active sector.  "
                "As a sterile/dark state it is constrained instead by "
                "X-ray decay searches (e.g. INTEGRAL, NuSTAR) and "
                "structure-formation bounds.  Status depends on whether "
                "Heim's framework gives it active mixing.")
    return ("> 1 MeV regime — heavy neutral leptons searched intensively; "
            "current bounds on |U|² are ≲ 10⁻⁶ in this mass window.  "
            "Status depends on Heim's (unspecified) mixing structure.")


def main():
    banner("Heim 1989 — five-neutrino prediction (G-Tabelle II)")
    print()
    print(f"  {'name':<7} {'Heim mass [MeV]':>18}  {'note':<60}")
    print("  " + "-" * 88)
    for name, m, J, B, note in HEIM_NEUTRINOS:
        print(f"  {name:<7} {m:>18.4e}  {note:<60}")
    print()
    print("  Spin: all ½. Baryon number: 0. Predicted as stable (mean life > 10⁻¹⁶ s).")
    print()

    banner("Current experimental bounds (2026 snapshot)", ch="-")
    print()
    print(f"  {'regime':<42} {'upper bound [MeV]':>20}  {'source':<35}")
    print("  " + "-" * 100)
    for regime, ub, source in BOUNDS:
        print(f"  {regime:<42} {ub:>20.4e}  {source:<35}")
    print()

    banner("Per-prediction status", ch="-")
    for name, m, J, B, note in HEIM_NEUTRINOS:
        # m is in MeV. 1 MeV = 1e6 eV = 1e3 keV = 1e9 meV.
        m_eV  = m * 1e6
        m_meV = m * 1e9
        print()
        if m < 1e-3:                       # sub-keV: report in eV / meV
            print(f"  {name}  (Heim 1989 = {m_eV:.4g} eV "
                  f"= {m_meV:.4g} meV)")
        elif m < 1.0:                      # keV-to-near-MeV
            print(f"  {name}  (Heim 1989 = {m*1e3:.4f} keV "
                  f"= {m:.4f} MeV)")
        else:
            print(f"  {name}  (Heim 1989 = {m:.4f} MeV)")
        print(f"    note  : {note}")
        print(f"    status: {evaluate_status(name, m)}")

    banner("Summary")
    print("""
  Heim 1989 predicts five neutrino species (with the unit reading
  ν_e = 0.00381 × 10⁻⁶ MeV vs. the others without ×10⁻⁶ scaling, taken
  at face value from G-Tabelle II):

    ν_e  ≈   3.81 meV   — consistent with KATRIN, below cosmological sum
    ν_μ  ≈   5.37 keV   — RULED OUT as active-flavour eigenstate by
                          cosmological Σm_ν < 0.12 eV; only viable as a
                          sterile / non-mixing state
    ν_τ  ≈  10.75 keV   — same — RULED OUT as active eigenstate, viable
                          only as sterile / non-mixing
    ν_4  ≈  21.06 keV   — new prediction; sterile interpretation OK,
                          active interpretation ruled out
    ν_5  ≈ 207    keV   — new prediction; heavy neutral lepton regime,
                          tightly constrained by PIENU / NA62 IF mixing

  This is a genuinely substantial tension between Heim 1989 and modern
  data: Heim's ν_μ and ν_τ labels carry masses of 5 keV and 11 keV, but
  PDG-2024 active-neutrino bounds (from oscillation experiments + KATRIN
  + cosmology) cap all three active neutrino mass eigenstates at well
  below 1 eV total.

  Three plausible resolutions:

    (a) Heim's "ν_μ", "ν_τ" labels denote DIFFERENT physical states than
        the SM ν_μ, ν_τ — they are sterile, non-mixing geometric
        objects.  The SM neutrinos are then either covered by ν_e alone
        and additional ones we have not identified, or are not in
        G-Tabelle II at all.

    (b) Heim's framework gives the wrong values for ν_μ / ν_τ.  This
        would be a genuine failure of the framework on a quantitative
        prediction.

    (c) Heim's framework gives correct GEOMETRIC mass scales but the
        empirical "observed mass eigenstates" are emergent / mixing
        effects from interaction with the Standard-Model field content
        that Heim's bare framework does not include.

  None of these has been worked through in the published Heim literature
  we have access to.  This script does NOT adjudicate the question; it
  documents that the prediction exists, raises the tension explicitly,
  and lists the three resolution paths.

  Falsification handle: the ν_5 at 207 keV is the most directly testable
  Heim prediction.  PIENU and NA62 already constrain heavy-neutral-lepton
  mixing in this mass range to |U|² ≲ 10⁻⁶.  Heim's framework does not
  explicitly fix the mixing-matrix elements for these extra generations,
  so the prediction is currently underconstrained — but a Heim-positive
  theory would need to either demonstrate consistency with these
  experimental bounds, or specify (b) above.
""")


if __name__ == "__main__":
    main()
