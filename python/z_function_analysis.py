"""
Empirical analysis of Heim's unknown z(N) integer function.

J0032 eq. 14c:  Q(N) = Q(N=0) + 2·z(N)
J0032 p.15:    "Hierin ist jedoch die ganzzahlige Beziehung z(N)
                noch völlig unbekannt."

Using PDG J for each Heim resonance (pdg_j_lookup.py) we can compute
the empirical z value per state and look for patterns vs N.

Heim groups Tabellen IV / V_{a,b,c} by particle family.  Per family
(Λ, N*, Ξ*, Σ*, Δ*, ε, K*, ρ, …) we have a sequence of (N, z) pairs.
We tabulate per-family, check monotonicity in N, look for simple
functional forms (linear, stepwise, etc.).
"""

from __future__ import annotations

from collections import defaultdict

from g_tables import (TABLE_IV_MESONS_K1, TABLE_V_a_BARYONS_K2,
                      TABLE_V_b_BARYONS_K2, TABLE_V_c_BARYONS_K2_SIGMA)
from pdg_j_lookup import (MESON_PDG_J, BARYON_PDG_J, z_value)


def get_N(entry, charge=None):
    """Return the published N index from a TableIV/V entry."""
    if isinstance(entry.N, tuple):
        # doublet (neutral, charged)  or triplet (-, 0, +)
        if len(entry.N) == 2:
            return entry.N[0] if charge == 0 else entry.N[1]
        elif len(entry.N) == 3:
            # (Σ⁻, Σ⁰, Σ⁺) → charge -1, 0, +1
            idx = {-1: 0, 0: 1, 1: 2}[charge]
            return entry.N[idx]
    return entry.N


def family_of(sym: str) -> str:
    if sym.startswith("Λ"): return "Λ*"
    if sym.startswith("N("):  return "N*"
    if sym.startswith("Ξ"): return "Ξ*"
    if sym.startswith("Δ"): return "Δ*"
    if sym.startswith("Σ"): return "Σ*"
    if sym.startswith("K"):  return "K*"
    if sym.startswith("ρ"):  return "ρ*"
    if any(sym.startswith(c) for c in "ωΦϕ"):  return "ω/φ"
    if any(sym.startswith(c) for c in "εη'f'fS*ED"):  return "ε family"
    if any(sym.startswith(c) for c in "AB"): return "A/B mesons"
    if sym.startswith("δ") or sym.startswith("g"): return "ε family"
    return "?"


def main():
    print("=" * 80)
    print(" Empirical z(N) per Heim family")
    print("=" * 80)
    print()

    # Build family → list of (N, z, sym, confidence)
    by_family = defaultdict(list)

    # Mesons (use neutral N for doublets)
    for r in TABLE_IV_MESONS_K1:
        sym = r.symbol
        if sym not in MESON_PDG_J:
            continue
        N_neu = get_N(r, charge=0)
        z = z_value(sym, MESON_PDG_J)
        fam = family_of(sym)
        conf = MESON_PDG_J[sym].confidence
        by_family[fam].append((N_neu, z, sym, conf))

    # Baryons (use neutral N for doublets, central N for triplets)
    for tbl in (TABLE_V_a_BARYONS_K2, TABLE_V_b_BARYONS_K2,
                TABLE_V_c_BARYONS_K2_SIGMA):
        for r in tbl:
            sym = r.symbol
            if sym not in BARYON_PDG_J:
                continue
            N_neu = get_N(r, charge=0)
            z = z_value(sym, BARYON_PDG_J)
            fam = family_of(sym)
            conf = BARYON_PDG_J[sym].confidence
            by_family[fam].append((N_neu, z, sym, conf))

    # Output per family, sorted by N
    for fam in sorted(by_family.keys()):
        entries = sorted(by_family[fam], key=lambda x: (x[0] if x[0] is not None else 0))
        print(f"\n--- {fam} ({len(entries)} entries) ---")
        print(f"  {'N':>5}  {'z':>4}  {'symbol':<14}  conf")
        for N_, z_, sym, conf in entries:
            z_str = f"{z_:+d}" if z_ is not None else "—"
            N_str = f"{N_:>5}" if N_ is not None else "—".rjust(5)
            print(f"  {N_str}  {z_str:>4}  {sym:<14}  {conf}")

    # Pattern check: is z monotonic in N per family?
    print()
    print("=" * 80)
    print(" Monotonicity check (does z grow with N within a family?)")
    print("=" * 80)
    for fam in sorted(by_family.keys()):
        entries = [(N, z) for N, z, sym, conf in by_family[fam]
                    if z is not None and N is not None
                    and conf in ("PDG", "approx")]
        entries.sort()
        if len(entries) < 3:
            continue
        violations = sum(1 for i in range(len(entries) - 1)
                          if entries[i+1][1] < entries[i][1])
        z_values = [z for _, z in entries]
        print(f"  {fam:<12} n={len(entries):>3}  "
              f"z range: [{min(z_values)}, {max(z_values)}]  "
              f"monotonicity violations: {violations}/{len(entries)-1}")

    # Pattern check: z as a function of N — linear fit?
    print()
    print("=" * 80)
    print(" Linear fit z = a·N + b per family (PDG-only entries)")
    print("=" * 80)
    import numpy as np
    for fam in sorted(by_family.keys()):
        entries = [(N, z) for N, z, sym, conf in by_family[fam]
                    if z is not None and N is not None
                    and conf == "PDG"]
        if len(entries) < 3:
            continue
        N_arr = np.array([e[0] for e in entries], dtype=float)
        z_arr = np.array([e[1] for e in entries], dtype=float)
        if len(N_arr) == 0:
            continue
        a, b = np.polyfit(N_arr, z_arr, 1)
        z_pred = a * N_arr + b
        rmse = float(np.sqrt(np.mean((z_arr - z_pred) ** 2)))
        print(f"  {fam:<12} n={len(entries):>3}  "
              f"z = {a:+.4f}·N {b:+.4f}  RMSE={rmse:.2f}")


if __name__ == "__main__":
    main()
