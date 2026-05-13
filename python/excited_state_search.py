"""
Excited-state EXPLORATORY scan (non-canonical) — see caveats below.
==================================================================

⚠️  EPISTEMIC CAVEAT (added May 2026 after source audit) ⚠️

This script implements an EXPLORATORY scan over (ε, k, P, Q, κ, x) with
k up to 5 and x up to 11.  After review by Joel (Heim-Theory Discord)
and inspection of Heim's actual source documents A_…, E_…, F_…, G_…
in `downloads/`, the following must be stated up front:

  1. Heim's 1982 A-source (E_Massenformel_nach_B_Heim_1982.pdf) is
     explicit: "For ponderable corpuscles only k = 1 and k = 2 are
     possible, not k > 2."  Any scan at k > 2 is therefore producing
     states that lie OUTSIDE Heim's intended canonical ontology for
     ground states.

  2. Heim's G-Tabelle IV (page 5 of G_Ausgewaehlte_Ergebnisse.pdf)
     lists 23 mesonic resonances at k=1 with theoretical masses,
     including ρ, ω, φ, K*, η', f, A1, B, A2, F1, ρ', A3, g, etc.

  3. Heim's G-Tabelle V (pages 6-8) lists 50+ baryonic resonances at
     k=2 including N*, Δ*, Λ*, Σ*, Ξ* families.

  4. Heim's resonance procedure uses (P, N, K_B) parameters distinct
     from the (ε, k, P, Q, κ, x) ground-state procedure.  This script
     does NOT implement Heim's resonance procedure — it instead
     extends the ground-state procedure into non-canonical (k > 2)
     territory.

Consequences:

  - The K*(892) "match at k=3" reported by an earlier run of this
    script is NOT the same object as Heim's k=1 K* in G-Tabelle IV
    (theoretical 891.20 / 892.22 MeV).  It is a numerical coincidence
    in a non-canonical scan region.

  - The Λ(1690) "match at k=2" is in Heim's G-Tabelle Va as a k=2
    baryon resonance with theoretical 1693.28 MeV (P=0, N=55, K_B=61).
    Our scan finds it at 1666 MeV, which is 1.6 % off Heim's published
    value.  So our scan is not reproducing Heim's resonance procedure
    even within the canonical k=2 region.

  - The earlier "vector mesons ρ/ω/φ structurally absent from Heim's
    lattice" claim is RETRACTED.  These particles are explicitly in
    G-Tabelle IV with masses matching PDG to 0.02–0.7 %.

What this script still does:

  - It enumerates the (ε, k, P, Q, κ, x) lattice up to k=5 and reports
    where modern PDG resonances land at the correct (P=2·isospin,
    Q=2·spin, |q|) signature.

  - It separates the result into three categories:
      (i)  k ≤ 2 (canonical Heim ground-state region)
      (ii) k > 2 (NON-CANONICAL — exploratory only)

  - It documents which observed resonances Heim's PUBLISHED tables
    cover (these are not "new predictions" but rediscoveries of
    G-table entries the implementation does not yet reproduce
    exactly).

Anyone wanting to make new claims about Heim's reach should FIRST
implement the (P, N, K_B) resonance procedure properly and reproduce
G-Tabelle IV and V from the formula — that is a separate
reconstruction task that this script does not undertake.

Run with:
    ./venv/bin/python python/excited_state_search.py
"""

from __future__ import annotations

import formulae as fm
from constants import KG_TO_MEV
from math import isfinite


# --------------------------------------------------------------------
# Targets — PDG well-established light-flavour resonances, in MeV.
# Format: (name, mass MeV, |charge|, J (spin), I (isospin), note)
# Spin and isospin in physical units (not Heim's P,Q!).
# --------------------------------------------------------------------

TARGETS_MESONS = [
    # ---- Light unflavoured mesons
    ("ρ(770)",        775,  1, 1,    1,    "vector"),
    ("ρ(770)⁰",       775,  0, 1,    1,    "vector"),
    ("ω(782)",        783,  0, 1,    0,    "vector"),
    ("η′(958)",       958,  0, 0,    0,    "pseudoscalar"),
    ("f₀(980)",       990,  0, 0,    0,    "scalar"),
    ("a₀(980)⁰",      980,  0, 0,    1,    "scalar"),
    ("a₀(980)±",      980,  1, 0,    1,    "scalar"),
    ("φ(1020)",      1019,  0, 1,    0,    "vector ss̄"),
    ("h₁(1170)",     1170,  0, 1,    0,    "axial"),
    ("b₁(1235)",     1230,  1, 1,    1,    "axial"),
    ("a₁(1260)",     1230,  1, 1,    1,    "axial"),
    ("f₂(1270)",     1275,  0, 2,    0,    "tensor"),
    ("f₁(1285)",     1282,  0, 1,    0,    "axial"),
    ("η(1295)",      1294,  0, 0,    0,    "pseudoscalar"),
    ("π(1300)",      1300,  1, 0,    1,    "radial π exc."),
    ("a₂(1320)",     1318,  1, 2,    1,    "tensor"),
    # ---- Strange mesons
    ("K*(892)",       892,  0, 1,    0.5,  "vector"),     # ← known match
    ("K*(892)±",      892,  1, 1,    0.5,  "vector"),
    ("K₁(1270)",     1272,  1, 1,    0.5,  "axial"),
    ("K₁(1400)",     1403,  1, 1,    0.5,  "axial"),
    ("K*(1410)",     1414,  1, 1,    0.5,  "vector"),
    ("K₀*(1430)",    1425,  1, 0,    0.5,  "scalar"),
    ("K₂*(1430)",    1432,  1, 2,    0.5,  "tensor"),
]

TARGETS_BARYONS = [
    # ---- Nucleon excitations
    ("N(1440)",      1440,  1, 0.5,  0.5,  "Roper"),
    ("N(1520)",      1520,  1, 1.5,  0.5,  ""),
    ("N(1535)",      1535,  1, 0.5,  0.5,  ""),
    ("N(1650)",      1655,  1, 0.5,  0.5,  ""),
    ("N(1680)",      1685,  1, 2.5,  0.5,  ""),
    ("N(1720)",      1720,  1, 1.5,  0.5,  ""),
    # ---- Δ excitations (beyond the 1232)
    ("Δ(1600)",      1600,  1, 1.5,  1.5,  ""),
    ("Δ(1620)",      1630,  1, 0.5,  1.5,  ""),
    ("Δ(1700)",      1700,  1, 1.5,  1.5,  ""),
    ("Δ(1905)",      1880,  1, 2.5,  1.5,  ""),
    # ---- Λ excitations
    ("Λ(1405)",      1405,  0, 0.5,  0,    "narrow"),
    ("Λ(1520)",      1520,  0, 1.5,  0,    ""),
    ("Λ(1670)",      1670,  0, 0.5,  0,    ""),
    ("Λ(1690)",      1690,  0, 1.5,  0,    ""),
    # ---- Σ excitations
    ("Σ(1385)",      1385,  1, 1.5,  1,    ""),
    ("Σ(1660)",      1660,  1, 0.5,  1,    ""),
    ("Σ(1670)",      1670,  1, 1.5,  1,    ""),
    ("Σ(1775)",      1775,  1, 2.5,  1,    ""),
    # ---- Ξ excitations
    ("Ξ(1530)",      1530,  0, 1.5,  0.5,  ""),
    ("Ξ(1690)",      1690,  0, 0.5,  0.5,  ""),
    ("Ξ(1820)",      1820,  0, 1.5,  0.5,  ""),
]


# --------------------------------------------------------------------
# Lattice scanner — generate every (ε, k, P, Q, κ, x) with finite
# mass and integer charge in {-2..+2}.
# --------------------------------------------------------------------

def scan_all(k_range=range(1, 5), x_range=range(0, 8),
             P_range=range(0, 7), Q_range=range(0, 7)):
    out = []
    for eps in (1, -1):
        for k in k_range:
            for P in P_range:
                for Q in Q_range:
                    for kap in (0, 1):
                        for x in x_range:
                            try:
                                qx = fm.calc_charge(eps, k, P, Q, kap, x)
                            except Exception:
                                continue
                            qx_int = round(qx)
                            if abs(qx - qx_int) > 0.01 or abs(qx_int) > 2:
                                continue
                            try:
                                m_kg = fm.calc_mass(eps, k, P, Q, kap, qx)
                                m_mev = m_kg * KG_TO_MEV
                            except Exception:
                                continue
                            if isfinite(m_mev) and 0 < m_mev < 5e3:
                                out.append((eps, k, P, Q, kap, x, qx_int, m_mev))
    return out


def heim_PQ(spin: float, isospin: float):
    return int(round(2 * isospin)), int(round(2 * spin))


def find_best_match(candidates, m_target, abs_q, P_req, Q_req, tol,
                    k_max=None):
    """Return the *closest mass* candidate with the right (P, Q, |q|)
    within fractional tolerance `tol`, or None.  If k_max is given,
    only consider candidates with k <= k_max."""
    best = None
    for c in candidates:
        eps, k, P, Q, kap, x, qx, m = c
        if k_max is not None and k > k_max:
            continue
        if P != P_req or Q != Q_req:
            continue
        if abs(qx) != abs_q:
            continue
        if abs(m - m_target) / m_target > tol:
            continue
        if best is None or abs(m - m_target) < abs(best[7] - m_target):
            best = c
    return best


def main():
    print("=" * 92)
    print(" EXPLORATORY excited-state scan — see top-of-file caveats")
    print("=" * 92)
    print("""
  This scan extends Heim's ground-state procedure to non-canonical
  k > 2 territory.  Heim's actual G-Tabelle IV / V resonance procedure
  uses (P, N, K_B) parameters and is NOT reproduced here.  Results
  in the (k > 2) section should be read as exploratory only — they
  are not the same objects as Heim's published resonances.
""")

    # Wider lattice than higgs_search.py: include k up to 5 and x up to 11.
    candidates = scan_all(k_range=range(1, 6), x_range=range(0, 12))
    print(f"Lattice: ε∈±1, k∈{{1..5}}, P∈{{0..6}}, Q∈{{0..6}}, κ∈{{0,1}}, "
          f"x∈{{0..11}}, |q|≤2")
    print(f"Generated {len(candidates):,} integer-charge candidates < 5 GeV")
    print("\nCanonical-region (k ≤ 2) matches and non-canonical (k > 2) "
          "matches are tagged separately.\n")

    for label, targets in (("MESONS", TARGETS_MESONS),
                           ("BARYONS", TARGETS_BARYONS)):
        print()
        print("-" * 86)
        print(f"  {label}")
        print("-" * 86)
        print(f"{'Particle':<14} {'PDG':>6} {'|q|':>3}  "
              f"{'P':>2} {'Q':>2}  "
              f"{'best ≤10%':>11}  "
              f"{'err':>6}   "
              f"{'note':<28}")
        print("-" * 86)
        n_match2, n_match10, n_total = 0, 0, 0
        for name, m_t, q, J, I, note in targets:
            P_req, Q_req = heim_PQ(J, I)
            best10 = find_best_match(candidates, m_t, q, P_req, Q_req, 0.10)
            best2  = find_best_match(candidates, m_t, q, P_req, Q_req, 0.02)
            n_total += 1
            if best2 is not None:
                n_match2 += 1
            if best10 is not None:
                n_match10 += 1
                eps_b, k_b, _, _, kap_b, x_b, _, m_pred = best10
                err_pct = (m_pred - m_t) / m_t * 100
                tag = "★" if best2 is not None else " "
                region = "CANON" if k_b <= 2 else "EXPL "
                qnstr = f"ε={eps_b:+d} k={k_b} κ={kap_b} x={x_b}"
                print(f"{name:<14} {m_t:>6} {q:>3}  "
                      f"{P_req:>2} {Q_req:>2}  "
                      f"{m_pred:>9.1f} {tag}  "
                      f"{err_pct:>+5.1f}%   "
                      f"[{region}] {qnstr:<22}")
            else:
                print(f"{name:<14} {m_t:>6} {q:>3}  "
                      f"{P_req:>2} {Q_req:>2}  "
                      f"{'  —':>11}  "
                      f"{'    —':>6}   "
                      f"{'(no candidate)':<28}")
        print("-" * 86)
        print(f"  {label}: {n_match2}/{n_total} within ±2%, "
              f"{n_match10}/{n_total} within ±10%")

    print()
    print("=" * 92)
    print(" Interpretation (revised May 2026 after A/B/G source audit)")
    print("=" * 92)
    print("""
THE EARLIER VERSION OF THIS SECTION CLAIMED:

  - "NEW ±2% match: Λ(1690) at 1666 MeV — a second Heim prediction
    outside the published list, joining K*(892)."
  - "Vector mesons ρ/ω/φ are structurally absent from Heim's lattice."

BOTH CLAIMS ARE RETRACTED.  The source audit using
G_Ausgewaehlte_Ergebnisse.pdf shows:

  - K*(892) and Λ(1690) are EXPLICITLY in Heim's published tables:
      K*(892) in G Tabelle IV (page 5, k=1 mesonic resonance):
              theoretical mass 891.20 / 892.22 MeV (neutral / charged)
              parametrised by (P=1, N=23(11), K_B=29(3))
      Λ(1690) in G Tabelle Va (page 6, k=2 baryonic resonance):
              theoretical mass 1693.28 MeV
              parametrised by (P=0, N=55, K_B=61)
    Our scan's "hits" are at 867.6 MeV (K* at k=3, NON-CANONICAL)
    and 1666 MeV (Λ at k=2, within canon but off Heim's own value
    by 1.6 %).  In neither case is this a NEW prediction.

  - ρ/ω/φ are also EXPLICITLY in G Tabelle IV at k=1:
      ω(783):    P=0, N=64,  K_B=51,  theoretical mass 783.90 MeV
      Φ(1019):   P=0, N=153, K_B=63,  theoretical mass 1019.63 MeV
      ρ(770):    P=2, N=8(5), K_B=30(34), theoretical 769.98(769.31) MeV
    The "vector meson gap" observation was an artifact of this scan
    failing to implement Heim's (P, N, K_B) k=1 resonance procedure.

WHAT THE SCAN ACTUALLY SHOWS (correctly):

  - The scan currently has TWO scan regions:
      CANON (k ≤ 2): Heim's intended ground-state ontology per
                     A-source ("only k=1 and k=2 are possible for
                     ponderable corpuscles").
      EXPL  (k > 2): non-canonical territory outside Heim's
                     documented domain.

  - Within the CANON region the scan can detect ground-state matches
    but does NOT reproduce Heim's separate resonance procedure.

  - Within the EXPL region the scan generates states with no
    canonical interpretation in Heim's framework.

CONCLUSION: This script can no longer be used as evidence for "new
Heim predictions outside the published list."  To make claims of
that kind one would have to implement Heim's actual k=1 / k=2
resonance procedure using (P, N, K_B) parameters and reproduce
G-Tabelle IV / V from first principles; that is a separate
reconstruction task.  See README "Beyond the mass formula"
discussion and Open Questions #2.""")


if __name__ == "__main__":
    main()
