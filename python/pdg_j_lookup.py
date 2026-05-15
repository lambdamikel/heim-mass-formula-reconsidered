"""
PDG J (total angular momentum) lookup for the 23 mesonic resonances of
G-Tabelle IV and the 76 baryonic resonances of G-Tabellen V_{a,b,c}.

Values from Particle Data Group reviews (most recent: PDG 2024 for
well-established resonances, older editions for some that PDG has
dropped or merged).  Where the Heim label maps unambiguously onto a
PDG resonance, the J is given with `confidence = "PDG"`.  Where the
mapping is approximate (mass-window match within ± 30 MeV but no exact
PDG name), `confidence = "approx"`.  Where the Heim label has no
clean PDG counterpart, `confidence = "guess"`.

For each entry we also list Q(N=0) — the ground-state Q of the family
the resonance is an excitation of:

  family   ground particle        Q(N=0)
  -------  ---------------------  ------
  ε        (η — isoscalar)        0
  K*       K (kaon, J=0)          0
  ρ/π fam  π (J=0)                0
  ω/φ fam  isoscalar vector mes   2 (taking ω/φ as their own "ground")
  Λ        Λ(1116) J=1/2          1
  N*       p/n nucleon J=1/2      1
  Ξ*       Ξ J=1/2                1
  Σ*       Σ J=1/2                1
  Δ*       Δ(1232) J=3/2          3

z(N) per Heim eq. 14c is then  (Q_PDG − Q(N=0)) / 2  where Q_PDG = 2·J.
"""

from __future__ import annotations

from typing import NamedTuple


class PDGEntry(NamedTuple):
    heim_label: str
    pdg_J: float | None         # None = unknown / unmatched
    Q_ground: int               # Heim Q(N=0) for the family
    confidence: str             # "PDG" / "approx" / "guess" / "none"
    pdg_name: str | None = None
    note: str = ""


# k=1 mesonic resonances (G-Tabelle IV)
MESON_PDG_J: dict[str, PDGEntry] = {
    "ε":         PDGEntry("ε",        0,   0, "approx",  "f₀(500)?",      "broad scalar; PDG f₀(500)"),
    "ω(783)":    PDGEntry("ω(783)",   1,   2, "PDG",     "ω(782)",        ""),
    "η'(958)":   PDGEntry("η'(958)",  0,   0, "PDG",     "η'(958)",       ""),
    "S*(993)":   PDGEntry("S*(993)",  0,   0, "PDG",     "f₀(980)",       ""),
    "Φ(1019)":   PDGEntry("Φ(1019)",  1,   2, "PDG",     "φ(1020)",       ""),
    "f(1270)":   PDGEntry("f(1270)",  2,   0, "PDG",     "f₂(1270)",      ""),
    "D(1285)":   PDGEntry("D(1285)",  1,   0, "PDG",     "f₁(1285)",      ""),
    "E(1420)":   PDGEntry("E(1420)",  1,   0, "PDG",     "f₁(1420)/η(1405)", "old E meson"),
    "f'(1514)":  PDGEntry("f'(1514)", 2,   0, "PDG",     "f₂'(1525)",     ""),
    "ω(1675)":   PDGEntry("ω(1675)",  3,   2, "PDG",     "ω₃(1670)",      ""),
    "K*(892)":   PDGEntry("K*(892)",  1,   0, "PDG",     "K*(892)",       "z=1 (J=1 over K J=0)"),
    "K_A(1240)": PDGEntry("K_A(1240)",1,   0, "PDG",     "K₁(1270)/K₁(1400)", "axial K"),
    "K*(1420)":  PDGEntry("K*(1420)", 2,   0, "PDG",     "K*₂(1430)",     ""),
    "L(1770)":   PDGEntry("L(1770)",  2,   0, "approx",  "K₂(1770)",      ""),
    "ρ(770)":    PDGEntry("ρ(770)",   1,   0, "PDG",     "ρ(770)",        ""),
    "δ(970)":    PDGEntry("δ(970)",   0,   0, "PDG",     "a₀(980)",       ""),
    "A1(1100)":  PDGEntry("A1(1100)", 1,   0, "PDG",     "a₁(1260)",      ""),
    "B(1235)":   PDGEntry("B(1235)",  1,   0, "PDG",     "b₁(1235)",      ""),
    "A2(1310)":  PDGEntry("A2(1310)", 2,   0, "PDG",     "a₂(1320)",      ""),
    "F1(1540)":  PDGEntry("F1(1540)", 1,   0, "approx",  "?",             "older catalog"),
    "ρ'(1600)":  PDGEntry("ρ'(1600)", 1,   0, "PDG",     "ρ(1700)",       ""),
    "A3(1640)":  PDGEntry("A3(1640)", 2,   0, "approx",  "π₂(1670)?",     "older A3"),
    "g(1680)":   PDGEntry("g(1680)",  3,   0, "PDG",     "ρ₃(1690)",      ""),
}


# k=2 baryon resonances (V_a, V_b, V_c)
BARYON_PDG_J: dict[str, PDGEntry] = {
    # Λ family — Q(N=0) = 1
    "Λ(1330)":   PDGEntry("Λ(1330)",  None,  1, "none",    None,            "no clean PDG match"),
    "Λ(1405)":   PDGEntry("Λ(1405)",  0.5,   1, "PDG",     "Λ(1405)",       "S₀₁"),
    "Λ(1520)":   PDGEntry("Λ(1520)",  1.5,   1, "PDG",     "Λ(1520)",       "D₀₃"),
    "Λ(1670)":   PDGEntry("Λ(1670)",  0.5,   1, "PDG",     "Λ(1670)",       "S₀₁"),
    "Λ(1690)":   PDGEntry("Λ(1690)",  1.5,   1, "PDG",     "Λ(1690)",       "D₀₃"),
    "Λ(1750)":   PDGEntry("Λ(1750)",  0.5,   1, "approx",  "Λ(1800)?",      ""),
    "Λ(1815)":   PDGEntry("Λ(1815)",  2.5,   1, "PDG",     "Λ(1820)",       "F₀₅"),
    "Λ(1830)":   PDGEntry("Λ(1830)",  2.5,   1, "PDG",     "Λ(1830)",       "D₀₅"),
    "Λ(1860)":   PDGEntry("Λ(1860)",  1.5,   1, "approx",  "Λ(1890)?",      "P₀₃"),
    "Λ(1870)":   PDGEntry("Λ(1870)",  0.5,   1, "approx",  "Λ(1810)?",      "P₀₁"),
    "Λ(2010)":   PDGEntry("Λ(2010)",  None,  1, "none",    None,            ""),
    "Λ(2020)":   PDGEntry("Λ(2020)",  3.5,   1, "approx",  "Λ(2020)?",      "F₀₇ unestablished"),
    "Λ(2100)":   PDGEntry("Λ(2100)",  3.5,   1, "PDG",     "Λ(2100)",       "G₀₇"),
    "Λ(2110)":   PDGEntry("Λ(2110)",  2.5,   1, "PDG",     "Λ(2110)",       "F₀₅"),
    "Λ(2350)":   PDGEntry("Λ(2350)",  4.5,   1, "PDG",     "Λ(2350)",       "H₀₉"),
    "Λ(2585)":   PDGEntry("Λ(2585)",  None,  1, "guess",   "Λ(2585)?",      "very heavy"),
    # N* family — Q(N=0) = 1
    "N(1470)":   PDGEntry("N(1470)",  0.5,   1, "PDG",     "N(1440) Roper", "P₁₁"),
    "N(1520)":   PDGEntry("N(1520)",  1.5,   1, "PDG",     "N(1520)",       "D₁₃"),
    "N(1535)":   PDGEntry("N(1535)",  0.5,   1, "PDG",     "N(1535)",       "S₁₁"),
    "N(1670)":   PDGEntry("N(1670)",  0.5,   1, "PDG",     "N(1650)",       "S₁₁(1650)"),
    "N(1688)":   PDGEntry("N(1688)",  2.5,   1, "PDG",     "N(1680)",       "F₁₅"),
    "N(1700)":   PDGEntry("N(1700)",  1.5,   1, "PDG",     "N(1700)",       "D₁₃(1700)"),
    "N(1770)":   PDGEntry("N(1770)",  0.5,   1, "PDG",     "N(1710)",       "P₁₁"),
    "N(1780)":   PDGEntry("N(1780)",  1.5,   1, "PDG",     "N(1720)",       "P₁₃"),
    "N(1810)":   PDGEntry("N(1810)",  0.5,   1, "approx",  "N(1900)?",      "P₁₁"),
    "N(1990)":   PDGEntry("N(1990)",  3.5,   1, "PDG",     "N(1990)",       "F₁₇"),
    "N(2000)":   PDGEntry("N(2000)",  2.5,   1, "approx",  "N(2000)",       "F₁₅"),
    "N(2040)":   PDGEntry("N(2040)",  1.5,   1, "approx",  "N(2080)?",      "D₁₃"),
    "N(2100)":   PDGEntry("N(2100)",  0.5,   1, "PDG",     "N(2100)",       "P₁₁"),
    "N(2190)":   PDGEntry("N(2190)",  3.5,   1, "PDG",     "N(2190)",       "G₁₇"),
    "N(2220)":   PDGEntry("N(2220)",  4.5,   1, "PDG",     "N(2220)",       "H₁₉"),
    "N(2650)":   PDGEntry("N(2650)",  None,  1, "guess",   None,            ""),
    "N(3030)":   PDGEntry("N(3030)",  None,  1, "none",    None,            ""),
    "N(3245)":   PDGEntry("N(3245)",  None,  1, "none",    None,            ""),
    "N(3690)":   PDGEntry("N(3690)",  None,  1, "none",    None,            ""),
    "N(3755)":   PDGEntry("N(3755)",  None,  1, "none",    None,            ""),
    # Ξ* family — Q(N=0) = 1
    "Ξ(1530)":   PDGEntry("Ξ(1530)",  1.5,   1, "PDG",     "Ξ(1530)",       ""),
    "Ξ(1630)":   PDGEntry("Ξ(1630)",  None,  1, "guess",   None,            "tentative"),
    "Ξ(1820)":   PDGEntry("Ξ(1820)",  1.5,   1, "PDG",     "Ξ(1820)",       ""),
    "Ξ(1940)":   PDGEntry("Ξ(1940)",  None,  1, "guess",   None,            ""),
    "Ξ(2030)":   PDGEntry("Ξ(2030)",  2.5,   1, "approx",  "Ξ(2030)?",      ""),
    "Ξ(2250)":   PDGEntry("Ξ(2250)",  None,  1, "guess",   None,            ""),
    "Ξ(2500)":   PDGEntry("Ξ(2500)",  None,  1, "guess",   None,            ""),
    # Δ* family — Q(N=0) = 3
    "Δ(1650)":   PDGEntry("Δ(1650)",  0.5,   3, "PDG",     "Δ(1620)?",      "S₃₁"),
    "Δ(1670)":   PDGEntry("Δ(1670)",  1.5,   3, "PDG",     "Δ(1700)",       "D₃₃"),
    "Δ(1690)":   PDGEntry("Δ(1690)",  None,  3, "guess",   None,            ""),
    "Δ(1890)":   PDGEntry("Δ(1890)",  2.5,   3, "PDG",     "Δ(1905)",       "F₃₅"),
    "Δ(1900)":   PDGEntry("Δ(1900)",  0.5,   3, "PDG",     "Δ(1910)",       "P₃₁"),
    "Δ(1910)":   PDGEntry("Δ(1910)",  2.5,   3, "PDG",     "Δ(1905)",       "F₃₅ alt"),
    "Δ(1950)":   PDGEntry("Δ(1950)",  3.5,   3, "PDG",     "Δ(1950)",       "F₃₇"),
    "Δ(1960)":   PDGEntry("Δ(1960)",  None,  3, "guess",   None,            ""),
    "Δ(2160)":   PDGEntry("Δ(2160)",  None,  3, "guess",   None,            ""),
    "Δ(2420)":   PDGEntry("Δ(2420)",  5.5,   3, "PDG",     "Δ(2420)",       "H₃,₁₁"),
    "Δ(2850)":   PDGEntry("Δ(2850)",  None,  3, "none",    None,            ""),
    "Δ(3230)":   PDGEntry("Δ(3230)",  None,  3, "none",    None,            ""),
    # Σ* family — Q(N=0) = 1
    "Σ(1385)":   PDGEntry("Σ(1385)",  1.5,   1, "PDG",     "Σ(1385)",       ""),
    "Σ(1440)":   PDGEntry("Σ(1440)",  None,  1, "guess",   None,            ""),
    "Σ(1480)":   PDGEntry("Σ(1480)",  None,  1, "guess",   None,            ""),
    "Σ(1620)":   PDGEntry("Σ(1620)",  0.5,   1, "approx",  "Σ(1620)?",      "S-wave"),
    "Σ(1670)":   PDGEntry("Σ(1670)",  1.5,   1, "PDG",     "Σ(1670)",       "D₁₃"),
    "Σ(1690)":   PDGEntry("Σ(1690)",  None,  1, "guess",   None,            ""),
    "Σ(1750)":   PDGEntry("Σ(1750)",  0.5,   1, "PDG",     "Σ(1750)",       "S₁₁"),
    "Σ(1765)":   PDGEntry("Σ(1765)",  2.5,   1, "PDG",     "Σ(1775)",       "D₁₅"),
    "Σ(1840)":   PDGEntry("Σ(1840)",  None,  1, "guess",   None,            ""),
    "Σ(1880)":   PDGEntry("Σ(1880)",  0.5,   1, "PDG",     "Σ(1880)",       "P₁₁"),
    "Σ(1915)":   PDGEntry("Σ(1915)",  2.5,   1, "PDG",     "Σ(1915)",       "F₁₅"),
    "Σ(1940)":   PDGEntry("Σ(1940)",  1.5,   1, "approx",  "Σ(1940)",       "D₁₃"),
    "Σ(2000)":   PDGEntry("Σ(2000)",  0.5,   1, "approx",  "Σ(2000)?",      "S₁₁"),
    "Σ(2030)":   PDGEntry("Σ(2030)",  3.5,   1, "PDG",     "Σ(2030)",       "F₁₇"),
    "Σ(2070)":   PDGEntry("Σ(2070)",  None,  1, "guess",   None,            ""),
    "Σ(2080)":   PDGEntry("Σ(2080)",  1.5,   1, "approx",  "Σ(2080)?",      ""),
    "Σ(2100)":   PDGEntry("Σ(2100)",  3.5,   1, "PDG",     "Σ(2100)",       "G₁₇ candidate"),
    "Σ(2250)":   PDGEntry("Σ(2250)",  None,  1, "guess",   None,            ""),
    "Σ(2455)":   PDGEntry("Σ(2455)",  None,  1, "guess",   None,            ""),
    "Σ(2620)":   PDGEntry("Σ(2620)",  None,  1, "guess",   None,            ""),
    "Σ(3000)":   PDGEntry("Σ(3000)",  None,  1, "none",    None,            ""),
}


def z_value(heim_label: str, table: dict[str, PDGEntry] = None) -> int | None:
    """Return z(N) = J·2 − Q(N=0) for a Heim resonance, or None if unknown."""
    if table is None:
        table = {**MESON_PDG_J, **BARYON_PDG_J}
    if heim_label not in table:
        return None
    e = table[heim_label]
    if e.pdg_J is None:
        return None
    return int(round(e.pdg_J * 2 - e.Q_ground)) // 2


def main():
    print("=" * 80)
    print(" PDG-J lookup for Heim resonances")
    print("=" * 80)
    print()
    print("--- mesons (k=1) ---")
    print(f"  {'Heim label':<12} {'PDG name':<16} {'J':>5}  Q₀  z  conf")
    print("  " + "-" * 54)
    for sym, e in MESON_PDG_J.items():
        z = z_value(sym)
        z_str = f"{z:+d}" if z is not None else "—"
        J_str = f"{e.pdg_J}" if e.pdg_J is not None else "—"
        pdg = e.pdg_name or "—"
        print(f"  {sym:<12} {pdg:<16} {J_str:>5}  {e.Q_ground}  "
              f"{z_str:>3}  {e.confidence}")

    print()
    print("--- baryons (k=2) ---")
    print(f"  {'Heim label':<12} {'PDG name':<20} {'J':>5}  Q₀  z  conf")
    print("  " + "-" * 60)
    for sym, e in BARYON_PDG_J.items():
        z = z_value(sym)
        z_str = f"{z:+d}" if z is not None else "—"
        J_str = f"{e.pdg_J}" if e.pdg_J is not None else "—"
        pdg = e.pdg_name or "—"
        print(f"  {sym:<12} {pdg:<20} {J_str:>5}  {e.Q_ground}  "
              f"{z_str:>3}  {e.confidence}")

    # Summary
    print()
    n_PDG = sum(1 for e in {**MESON_PDG_J, **BARYON_PDG_J}.values()
                if e.confidence == "PDG")
    n_approx = sum(1 for e in {**MESON_PDG_J, **BARYON_PDG_J}.values()
                   if e.confidence == "approx")
    n_guess = sum(1 for e in {**MESON_PDG_J, **BARYON_PDG_J}.values()
                  if e.confidence in ("guess", "none"))
    total = n_PDG + n_approx + n_guess
    print(f"  Total entries: {total}")
    print(f"    PDG-clean:   {n_PDG}")
    print(f"    approx:      {n_approx}")
    print(f"    guess/none:  {n_guess}")


if __name__ == "__main__":
    main()
