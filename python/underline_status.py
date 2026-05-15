"""
Per-entry underline status for Heim's G-Tabellen IV / V_{a,b,c}.

Per J0032 p.27a:

  "Die N-Angaben der dritten Spalte unterscheiden zwischen N und N̄,
   wobei die Unterstreichung bedeutet, daß es sich um einen Term
   handelt, welcher der Beziehung (14d) nicht genügt."

J0032 p.15a clarifies: underlined N̄ entries are "single-process"
resonances — not stepwise (z=0) excitations.  Non-underlined N
entries are stepwise excitations expected to satisfy eqs. (14a, 14b).

This module records, per entry and per charge state, whether the
manuscript shows the N value underlined.

Transcribed from the manuscript images (J0032 pp.40a, 40b, 40c, 40d
and J0033 equivalent).  Where the underline is ambiguous in the
scan, marked with `?`.
"""

from __future__ import annotations

# Format: {label: bool_or_None}
# True  = underlined (single-process, not stepwise)
# False = not underlined (stepwise excitation, should fit (14a, 14b))
# None  = uncertain / unreadable in scan

# Tabelle IV (k=1 mesons).  Doublets/triplets have charged variants
# tracked via "⁰" (neutral) and "±" (charged) suffixes — these may
# have different underline status.

MESON_UNDERLINED: dict[str, bool] = {
    "ε":         False,
    "ω(783)":    False,
    "η'(958)":   True,
    "S*(993)":   True,
    "Φ(1019)":   False,
    "f(1270)":   True,
    "D(1285)":   True,
    "E(1420)":   False,
    "f'(1514)":  True,
    "ω(1675)":   False,
    # doublets — record neutral (N) and charged (N±) separately
    "K*(892)⁰":     True,
    "K*(892)±":     False,
    "K_A(1240)⁰":   True,
    "K_A(1240)±":   True,
    "K*(1420)⁰":    False,
    "K*(1420)±":    False,
    "L(1770)⁰":     False,
    "L(1770)±":     False,
    "ρ(770)⁰":      False,
    "ρ(770)±":      False,
    "δ(970)⁰":      False,
    "δ(970)±":      False,
    "A1(1100)⁰":    False,
    "A1(1100)±":    False,
    "B(1235)⁰":     True,
    "B(1235)±":     True,
    "A2(1310)⁰":    False,
    "A2(1310)±":    False,
    "F1(1540)⁰":    True,
    "F1(1540)±":    True,
    "ρ'(1600)⁰":    False,
    "ρ'(1600)±":    False,
    "A3(1640)⁰":    True,
    "A3(1640)±":    True,
    "g(1680)⁰":     False,
    "g(1680)±":     False,
}


# Tabellen V, V_a (k=2: N*, Λ*, Ξ*, Δ*).  Doublets in (N⁰, N±) format.

BARYON_UNDERLINED: dict[str, bool] = {
    # N* family — N⁰ first, N± second
    "N(1470)⁰":   False,  "N(1470)±":   False,
    "N(1520)⁰":   False,  "N(1520)±":   False,
    "N(1535)⁰":   True,   "N(1535)±":   False,
    "N(1670)⁰":   False,  "N(1670)±":   False,
    "N(1688)⁰":   False,  "N(1688)±":   False,
    "N(1770)⁰":   False,  "N(1770)±":   False,
    "N(1780)⁰":   True,   "N(1780)±":   False,
    "N(1810)⁰":   True,   "N(1810)±":   False,
    "N(1990)⁰":   True,   "N(1990)±":   False,
    "N(2000)⁰":   True,   "N(2000)±":   True,
    "N(2040)⁰":   True,   "N(2040)±":   False,
    "N(2100)⁰":   False,  "N(2100)±":   False,
    "N(2190)⁰":   False,  "N(2190)±":   False,
    "N(2220)⁰":   False,  "N(2220)±":   False,
    "N(2650)⁰":   True,   "N(2650)±":   False,
    "N(3030)⁰":   True,   "N(3030)±":   False,
    "N(3245)⁰":   False,  "N(3245)±":   False,
    "N(3690)⁰":   True,   "N(3690)±":   False,
    "N(3755)⁰":   False,  "N(3755)±":   False,
    "N(1700)⁰":   False,  "N(1700)±":   True,
    # Λ* family — singlets (no charge variants)
    "Λ(1330)":    True,
    "Λ(1405)":    False,
    "Λ(1520)":    False,
    "Λ(1670)":    False,
    "Λ(1690)":    False,
    "Λ(1750)":    False,
    "Λ(1815)":    True,
    "Λ(1830)":    True,
    "Λ(1860)":    True,
    "Λ(1870)":    True,
    "Λ(2010)":    True,
    "Λ(2020)":    False,
    "Λ(2100)":    False,
    "Λ(2110)":    False,
    "Λ(2350)":    True,
    "Λ(2585)":    True,
    # Ξ* family — doublet
    "Ξ(1530)⁰":   True,   "Ξ(1530)±":   False,
    "Ξ(1630)⁰":   False,  "Ξ(1630)±":   False,
    "Ξ(1820)⁰":   True,   "Ξ(1820)±":   True,
    "Ξ(1940)⁰":   False,  "Ξ(1940)±":   False,
    "Ξ(2030)⁰":   True,   "Ξ(2030)±":   True,
    "Ξ(2250)⁰":   False,  "Ξ(2250)±":   False,
    "Ξ(2500)⁰":   False,  "Ξ(2500)±":   False,
    # Δ* family — singlets in Heim's table
    "Δ(1650)":    True,
    "Δ(1670)":    True,
    "Δ(1690)":    True,
    "Δ(1890)":    False,
    "Δ(1900)":    False,
    "Δ(1910)":    True,
    "Δ(1950)":    False,
    "Δ(1960)":    True,
    "Δ(2160)":    False,
    "Δ(2420)":    True,
    "Δ(2850)":    False,
    "Δ(3230)":    False,
    # Σ* family triplets — (Σ⁻, Σ⁰, Σ⁺) tuple order in g_tables.
    # Manuscript prints "(N)_+ N (N)_-" so:
    #   our Σ⁻ ↔ "(N)_-" (last column)
    #   our Σ⁰ ↔ middle (no parens, no subscript)
    #   our Σ⁺ ↔ "(N)_+" (first column)
    # Underline by charge:
    "Σ(1385)⁻":  True,   "Σ(1385)⁰":  False,  "Σ(1385)⁺":  True,
    "Σ(1440)⁻":  True,   "Σ(1440)⁰":  False,  "Σ(1440)⁺":  True,
    "Σ(1480)⁻":  True,   "Σ(1480)⁰":  False,  "Σ(1480)⁺":  True,
    "Σ(1620)⁻":  True,   "Σ(1620)⁰":  False,  "Σ(1620)⁺":  True,
    "Σ(1670)⁻":  False,  "Σ(1670)⁰":  False,  "Σ(1670)⁺":  False,
    "Σ(1690)⁻":  False,  "Σ(1690)⁰":  False,  "Σ(1690)⁺":  False,
    "Σ(1750)⁻":  False,  "Σ(1750)⁰":  False,  "Σ(1750)⁺":  True,
    "Σ(1765)⁻":  True,   "Σ(1765)⁰":  False,  "Σ(1765)⁺":  True,
    "Σ(1840)⁻":  True,   "Σ(1840)⁰":  False,  "Σ(1840)⁺":  True,
    "Σ(1880)⁻":  False,  "Σ(1880)⁰":  True,   "Σ(1880)⁺":  False,
    "Σ(1915)⁻":  False,  "Σ(1915)⁰":  False,  "Σ(1915)⁺":  False,
    "Σ(1940)⁻":  False,  "Σ(1940)⁰":  False,  "Σ(1940)⁺":  False,
    "Σ(2000)⁻":  True,   "Σ(2000)⁰":  False,  "Σ(2000)⁺":  True,
    "Σ(2030)⁻":  False,  "Σ(2030)⁰":  False,  "Σ(2030)⁺":  True,
    "Σ(2070)⁻":  True,   "Σ(2070)⁰":  False,  "Σ(2070)⁺":  True,
    "Σ(2080)⁻":  True,   "Σ(2080)⁰":  False,  "Σ(2080)⁺":  True,
    "Σ(2100)⁻":  True,   "Σ(2100)⁰":  False,  "Σ(2100)⁺":  True,
    "Σ(2250)⁻":  False,  "Σ(2250)⁰":  False,  "Σ(2250)⁺":  False,
    "Σ(2455)⁻":  False,  "Σ(2455)⁰":  False,  "Σ(2455)⁺":  True,
    "Σ(2620)⁻":  False,  "Σ(2620)⁰":  False,  "Σ(2620)⁺":  True,
    "Σ(3000)⁻":  True,   "Σ(3000)⁰":  False,  "Σ(3000)⁺":  True,
}


def is_underlined(label: str) -> bool | None:
    """Return True/False/None per underline_status table."""
    if label in MESON_UNDERLINED:
        return MESON_UNDERLINED[label]
    if label in BARYON_UNDERLINED:
        return BARYON_UNDERLINED[label]
    return None


def main():
    print("=" * 70)
    print(" Underline status per Heim entry (J0032 Tabellen IV, V, V_a, V_b)")
    print("=" * 70)

    mes_underlined = sum(1 for v in MESON_UNDERLINED.values() if v)
    mes_not = sum(1 for v in MESON_UNDERLINED.values() if v is False)
    print(f"\n  Mesons (Tabelle IV): {len(MESON_UNDERLINED)} total")
    print(f"    Underlined (N̄, single-process):   {mes_underlined}")
    print(f"    Non-underlined (N, stepwise z=0): {mes_not}")

    bary_underlined = sum(1 for v in BARYON_UNDERLINED.values() if v)
    bary_not = sum(1 for v in BARYON_UNDERLINED.values() if v is False)
    print(f"\n  Baryons (Tabellen V, V_a, V_b): {len(BARYON_UNDERLINED)} total")
    print(f"    Underlined:     {bary_underlined}")
    print(f"    Non-underlined: {bary_not}")

    print()
    print("  Total non-underlined entries (z=0 stepwise candidates):",
          mes_not + bary_not)
    print("  Total underlined entries (single-process):",
          mes_underlined + bary_underlined)


if __name__ == "__main__":
    main()
