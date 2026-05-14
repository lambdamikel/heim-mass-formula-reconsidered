"""
Heim's predicted charge-doublet mass splittings — a new falsifiable test.
=========================================================================

Heim's G-Tabelle IV (the k=1 mesonic resonance list) gives 13 entries
parametrised as charge doublets:

  4 K-family doublets (P = 1, isospin 1/2):  K*(892), K_A(1240),
                                              K*(1420), L(1770)
  9 ρ-family entries  (P = 2, isospin 1):     ρ(770), δ(970), A1(1100),
                                              B(1235), A2(1310), F1(1540),
                                              ρ'(1600), A3(1640), g(1680)

Each entry has *two* values for (N, K_B, mass) — one for each member
of the charge doublet (neutral vs charged, in some convention not
explicit in the IGW Innsbruck source).  Heim's two members differ
*substantially* in (N, K_B), and the resulting mass splittings range
from 0.2 to 10 MeV.

This is a CONCRETE FALSIFIABLE PREDICTION that has, to our knowledge,
never been systematically extracted from Heim's tables and tested
against PDG measurements.  The 4·q·α₋ charge-correction term in
Heim's mass formula contributes only ~0.1 keV — far below the
observed splittings.  So Heim's predicted MeV-scale splittings come
*entirely* from the (N, K_B) assignment rule, which is itself not
explained in the published material.

This script:

  1. Extracts all 13 doublet splittings from g_tables.TABLE_IV_MESONS_K1.
  2. Compares them to PDG-2024 charge-doublet mass differences.
  3. Computes the trivial 4·q·α₋ contribution from Heim's formula
     as a sanity check.
  4. Identifies the falsification handle: a real test of Heim's
     framework would resolve whether the predicted splitting pattern
     matches the measured one.

Run with:
    ./venv/bin/python python/doublet_splittings.py
"""

from __future__ import annotations

import formulae as fm
from constants import (KG_TO_MEV, alpha_minus, alpha_plus, eta, mass_element,
                       theta)
from g_tables import TABLE_IV_MESONS_K1


# --------------------------------------------------------------------
# PDG-2024 charge-doublet mass differences, in MeV.
# Sign convention: Δm = m(neutral) − m(charged), in MeV.
# "—" = no clean separation in PDG.
#
# K-family: K*⁰ / K*±, K_1⁰ / K_1±, etc.
# ρ-family: ρ⁰ / ρ±, δ → a₀(980)⁰ / a₀(980)±, A1 → a₁(1260)⁰ / a₁(1260)±, etc.
# Many of Heim's labels predate the modern PDG nomenclature; mappings
# below follow the PDG meson-table conventions.
# --------------------------------------------------------------------

PDG_SPLITTINGS = {
    # K-family
    "K*(892)":   ("K*(892)",      895.55, 891.67),   # K*⁰ vs K*±
    "K_A(1240)": ("K₁(1270)",     1272.0, 1272.0),   # K₁(1270)⁰ vs ±  (no measured splitting)
    "K*(1420)": ("K*₂(1430)",    1432.4, 1427.3),   # tensor K*₂(1430)
    "L(1770)":  ("K₂(1770)",     1773.0, 1773.0),   # K₂(1770), no clean splitting

    # ρ-family (Heim labels → modern PDG)
    "ρ(770)":   ("ρ(770)",        775.26, 775.11),  # ρ⁰ vs ρ±
    "δ(970)":   ("a₀(980)",       980.0, 980.0),    # roughly degenerate
    "A1(1100)": ("a₁(1260)",      1230, 1230),
    "B(1235)":  ("b₁(1235)",      1229.5, 1229.5),
    "A2(1310)": ("a₂(1320)",      1318.2, 1318.2),
    "F1(1540)": ("(no clean PDG match)", None, None),
    "ρ'(1600)": ("ρ(1450)/(1700)", None, None),     # PDG splits these
    "A3(1640)": ("(no clean PDG match)", None, None),
    "g(1680)":  ("ρ(1700)",       None, None),
}


def heim_charge_correction_MeV(q1: int, q2: int) -> float:
    """The pure 4·q·α₋ correction in Heim's mass formula gives a mass
    difference of mu·α₊·4·(q1-q2)·α₋ between two charge states.
    Returns the MeV-scale difference for one unit of charge change."""
    eta00 = eta(1, 0)
    th = theta(eta00)
    a_p = alpha_plus(eta00, th)
    a_m = alpha_minus(eta00, th)
    mu = mass_element()
    dM_kg = mu * a_p * 4.0 * (q1 - q2) * a_m
    return dM_kg * KG_TO_MEV


def main():
    print("=" * 92)
    print(" Heim's charge-doublet mass splittings — G-Tabelle IV vs PDG-2024")
    print("=" * 92)

    print(f"""
Heim's 4·q·α₋ contribution to mass splitting:
    Δm(q=+1 → q=−1) = μ·α₊·4·(2)·α₋
                    = {heim_charge_correction_MeV(+1, -1):+.4e} MeV
                    ≈ {heim_charge_correction_MeV(+1, -1)*1000:.3f} keV

So the naive charge correction is ~0.1 keV.  The observed and
Heim-predicted splittings are *4 orders of magnitude larger* —
meaning they come from the (N, K_B) assignment difference, NOT
from the 4·q·α₋ term.
""")

    print("=" * 92)
    print(" Doublet table")
    print("=" * 92)
    print()
    print(f"  {'Heim particle':<14} {'modern PDG label':<22} "
          f"{'|Δm_Heim|':>10} {'|Δm_PDG|':>10}   verdict")
    print("  " + "-" * 80)

    sum_heim, sum_pdg, n_compared = 0.0, 0.0, 0

    for r in TABLE_IV_MESONS_K1:
        if not isinstance(r.mass_MeV, tuple):
            continue
        dm_heim = r.mass_MeV[0] - r.mass_MeV[1]
        info = PDG_SPLITTINGS.get(r.symbol, (None, None, None))
        if info[1] is None or info[2] is None:
            verdict = f"(no clean PDG number — {info[0]})" if info[0] else "(no PDG mapping)"
            print(f"  {r.symbol:<14} {info[0] or '—':<22} "
                  f"{abs(dm_heim):>10.4f} {'—':>10}   {verdict}")
            continue
        dm_pdg = info[1] - info[2]
        ratio = abs(dm_heim) / max(abs(dm_pdg), 0.01)
        if abs(dm_pdg) < 0.1:
            verdict = f"PDG ≈ 0 ({dm_pdg:+.2f}); Heim: {dm_heim:+.2f}"
        else:
            verdict = f"Heim/PDG = {ratio:.2f}× (Heim {dm_heim:+.2f}, PDG {dm_pdg:+.2f})"
        print(f"  {r.symbol:<14} {info[0]:<22} "
              f"{abs(dm_heim):>10.4f} {abs(dm_pdg):>10.4f}   {verdict}")
        sum_heim += abs(dm_heim)
        sum_pdg += abs(dm_pdg)
        n_compared += 1

    print()
    print(f"  Total |Δm| across {n_compared} comparable doublets:")
    print(f"    Heim sum:  {sum_heim:.3f} MeV")
    print(f"    PDG sum:   {sum_pdg:.3f} MeV")
    print(f"    Heim/PDG:  {sum_heim/max(sum_pdg,0.001):.2f}×")

    print()
    print("=" * 92)
    print(" Pattern observations")
    print("=" * 92)
    print("""
1. K-family monotonic growth.
   Heim's K-family splittings rise monotonically with mass:
       K*(892):    1.03 MeV
       K_A(1240):  1.14 MeV
       K*(1420):   5.73 MeV
       L(1770):   10.23 MeV
   PDG data (K*⁰ - K*±):
       K*(892):    3.88 MeV
       K₁(1270):   ≈ 0
       K*₂(1430):  5.10 MeV
       K₂(1770):   ≈ 0
   So Heim correctly predicts ~5 MeV scale splittings for the
   K*-tensor family but *over-predicts* for the K₁ axial mesons by
   factor > 10.  This is a sharp falsifiable pattern.

2. ρ-family has very small splittings in PDG (sub-MeV for all states
   that have clean charged-vs-neutral data).  Heim predicts mostly
   sub-MeV but with three outliers above 3 MeV: δ(970)=2.82,
   A3(1640)=3.05, g(1680)=7.37.  The g(1680) prediction at 7.4 MeV
   is the most striking — PDG ρ(1700) has no measured charge
   splitting at that scale.

3. Two negative Heim Δm values (K*(892), ρ'(1600)) suggest one
   member of the doublet is consistently *heavier* than the other,
   and Heim's convention has the "heavier" member listed in
   different positions.  Without the original IGW Innsbruck notes
   it is not possible to definitively map "first value" vs "second
   value" to "neutral" vs "charged".

4. Falsification handle.
   A clean test of Heim's framework on this data would be:

     (a) Resolve Heim's charge convention by cross-referencing
         G-Tabelle I (ground-state quantum numbers) where charge is
         explicit.
     (b) Compare signs of Heim's Δm vs PDG signs across all 13
         doublets.  Currently we cannot do this confidently.
     (c) Once signs are resolved, compute the χ² of Heim vs PDG.
         If χ²/dof ≪ 1, the prediction is confirmed.  If χ²/dof
         » 1, the prediction is falsified at a specific magnitude.

5. New prediction extraction.
   To our knowledge no published Heim-theory paper, IGW Innsbruck
   report, or third-party analysis has extracted the 13-entry
   charge-doublet splitting prediction from G-Tabelle IV and
   compared it systematically to PDG.  This script is therefore
   the first time these specific 13 numbers have been treated as a
   joint Heim prediction with associated falsifiability.
""")


if __name__ == "__main__":
    main()
