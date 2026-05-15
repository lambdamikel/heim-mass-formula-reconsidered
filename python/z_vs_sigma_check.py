"""
Test whether σ in Heim's matched (n, m, p, σ) decomposition encodes
z(N) = (Q(N) - Q(N=0))/2 = (2·J_PDG - Q_ground)/2.

Hypothesis: if Heim's σ is a separate angular-momentum quantum number,
then σ might track z directly (e.g., σ ≡ z + const).  If so we'd
have closed Heim's open question without any external function.

Loads matched (n, m, p, σ) from baryon_reproduction_results.txt, joins
with PDG-J table from pdg_j_lookup.py, and tabulates (z, σ) per state.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from pdg_j_lookup import MESON_PDG_J, BARYON_PDG_J, z_value

LOG = Path(__file__).parent / "baryon_reproduction_results.txt"
LINE_RE = re.compile(
    r"^\s+(?P<label>\S+)\s+\d+\s+[+-]\d+\s+[\d.]+\s+-?\d+\s+\d+\s+"
    r"\((?P<n>-?\d+),\s*(?P<m>-?\d+),\s*(?P<p>-?\d+),\s*(?P<sig>-?\d+)\)"
)


def load_matched_nmps():
    out = {}
    with open(LOG) as fh:
        for line in fh:
            m = LINE_RE.match(line)
            if not m:
                continue
            label = m.group("label")
            # strip charge superscripts to map to the PDG table
            base = (label.replace("⁻", "").replace("⁰", "")
                          .replace("⁺", "").replace("±", ""))
            nmps = (int(m.group("n")), int(m.group("m")),
                    int(m.group("p")), int(m.group("sig")))
            out[label] = (base, nmps)
    return out


def main():
    nmps_table = load_matched_nmps()
    print(f"Loaded {len(nmps_table)} matched states")
    print()
    print(f"  {'symbol':<14}  {'(n,m,p,σ)':<24}  {'σ':>4}  "
          f"{'z':>3}  {'σ-z':>5}  {'conf':<8}")
    print("  " + "-" * 70)
    by_family = defaultdict(list)
    for label, (base, nmps) in nmps_table.items():
        z = z_value(base, BARYON_PDG_J)
        if z is None:
            z = z_value(base, MESON_PDG_J)
        if z is None:
            continue
        if base in BARYON_PDG_J:
            conf = BARYON_PDG_J[base].confidence
        elif base in MESON_PDG_J:
            conf = MESON_PDG_J[base].confidence
        else:
            conf = "?"
        if conf not in ("PDG", "approx"):
            continue
        sig = nmps[3]
        sig_minus_z = sig - z
        if base.startswith("Λ"):  fam = "Λ*"
        elif base.startswith("N("): fam = "N*"
        elif base.startswith("Ξ"): fam = "Ξ*"
        elif base.startswith("Δ"): fam = "Δ*"
        elif base.startswith("Σ"): fam = "Σ*"
        else: fam = "?"
        by_family[fam].append((label, nmps, sig, z, conf))
        print(f"  {label:<14}  {str(nmps):<24}  {sig:>+4d}  "
              f"{z:>+3d}  {sig_minus_z:>+5d}  {conf:<8}")

    print()
    print("=" * 70)
    print(" σ ↔ z correlation per family:")
    print("=" * 70)
    import numpy as np
    for fam in sorted(by_family.keys()):
        items = by_family[fam]
        if len(items) < 3:
            continue
        sig_arr = np.array([s for _, _, s, _, _ in items], dtype=float)
        z_arr = np.array([z for _, _, _, z, _ in items], dtype=float)
        # linear fit σ = a·z + b
        a, b = np.polyfit(z_arr, sig_arr, 1)
        rmse = float(np.sqrt(np.mean((sig_arr - (a*z_arr + b))**2)))
        # correlation coefficient
        if len(sig_arr) > 1:
            corr = float(np.corrcoef(sig_arr, z_arr)[0, 1])
        else:
            corr = float("nan")
        print(f"  {fam:<6} n={len(items):>3}  "
              f"corr(σ, z) = {corr:+.3f}   σ ≈ {a:+.3f}·z {b:+.3f}  "
              f"RMSE={rmse:.2f}")


if __name__ == "__main__":
    main()
