"""
Cross-check: Heim's published (n, m, p, σ) values from G-Tabelle I
vs the values our Python port computes via the greedy decomposition.

In Heim's scheme (n, m, p, σ) are *input* quantum numbers, listed
explicitly per particle in G-Tabelle I (the ground-state QN table).
In our port (formulae.calc_n) they are *output* values, computed
from the structure weight W via a greedy algorithm
([B40]-[B46] of the IGW Innsbruck restatement).

If the two agree for all 21 reference particles, the greedy
algorithm correctly reproduces Heim's intended decomposition.

If they disagree on the electron and electron-only, that explains
the standing 0.79 % electron-mass discrepancy (Heim 1989: 0.51100
MeV; our port: 0.50694 MeV).

This script was surfaced by the May 2026 source-audit conversation
with Joel (Heim-Theory Discord) and is the simplest diagnostic
that maps directly to Open Question #1 in the README.

Run with:
    ./venv/bin/python python/nmps_cross_check.py
"""

from __future__ import annotations

from math import fabs

import formulae as fm
from g_tables import TABLE_I_GROUND_STATES, TableI
from particle import REFERENCE_PARTICLES


# --------------------------------------------------------------------
# Map Heim's Tabelle-I labels to our REFERENCE_PARTICLES entries.
# Our (eps, k, P, Q, kap, x) parameter "x" enumerates members within
# a multiplet (e.g. Σ⁺ has x=0, Σ⁰ x=1, Σ⁻ x=2 in our scheme).
# Heim's table lists them with explicit εq_x charge, which lets us
# match unambiguously.
# --------------------------------------------------------------------

# Build a (k, P, Q, kap, eq_x) → Heim TableI row index
HEIM_BY_KEY: dict[tuple[int, int, int, int, int], TableI] = {}
for row in TABLE_I_GROUND_STATES:
    key = (row.k, row.P, row.Q, row.R, row.eq_x)
    HEIM_BY_KEY[key] = row


def heim_for(eps: int, k: int, P: int, Q: int, kap: int, qx: int) -> TableI | None:
    """Look up Heim's Tabelle-I row given our (eps, k, P, Q, kap, qx).
    ε just flips overall sign; we treat ε=+1 as canonical."""
    if eps == -1:
        # antiparticle — same row, sign-flipped charge
        return HEIM_BY_KEY.get((k, P, Q, kap, -qx))
    return HEIM_BY_KEY.get((k, P, Q, kap, qx))


def compute_nmps(p) -> tuple[int, int, int, int]:
    """Run our greedy decomposition for one particle. Returns
    (n, m, p, σ)."""
    qx = fm.calc_charge(p.eps, p.k, p.P, p.Q, p.kap, p.x)
    q  = fabs(qx)
    I  = fm.calc_Q(p.k)
    N  = fm.calc_N(p.k, q, I)
    W  = fm.calc_W(p.eps, p.k, p.P, p.Q, p.kap, qx, I)
    nmps = fm.calc_n(p.k, I, N, W)
    return nmps, qx


def main():
    print("=" * 110)
    print(" Heim's (n, m, p, σ) — Tabelle I (input) vs Python port greedy decomposition (output)")
    print("=" * 110)
    print()
    print(f"  {'Heim particle':<14} {'our entry':<22} "
          f"{'(n,m,p,σ) Heim':<22} {'(n,m,p,σ) ours':<22}  match")
    print("  " + "-" * 100)

    all_match = True
    n_total, n_match = 0, 0
    for p in REFERENCE_PARTICLES:
        # Compute our (n, m, p, σ) and integer charge
        ours, qx = compute_nmps(p)
        qx_int = int(round(qx))

        # Look up Heim's row
        heim = heim_for(p.eps, p.k, p.P, p.Q, p.kap, qx_int)
        if heim is None:
            print(f"  (no Heim row)   {p.symbol:<22} "
                  f"{'-':<22} {ours!r:<22}  ?")
            continue

        heim_nmps = (heim.n, heim.m, heim.p, heim.sigma)
        ok = (heim_nmps == tuple(ours))
        marker = "✓" if ok else "✗"
        n_total += 1
        if ok:
            n_match += 1
        else:
            all_match = False
        print(f"  {heim.symbol:<14} {p.symbol:<22} "
              f"{str(heim_nmps):<22} {str(tuple(ours)):<22}  {marker}")

    print("  " + "-" * 100)
    print(f"  {n_match} / {n_total} ground-state (n, m, p, σ) tuples match.")
    print()

    if all_match:
        print("=" * 110)
        print(" ✓ ALL MATCH: the greedy decomposition correctly reproduces Heim's listed")
        print("   quantum numbers across all 21 ground states. The 0.79 % electron-mass")
        print("   discrepancy must originate elsewhere — likely in calc_W, calc_phi, or")
        print("   the M = μ·α₊·(K + S + F + Φ + 4qα₋) assembly itself.")
        print("=" * 110)
    else:
        print("=" * 110)
        print(" ✗ MISMATCH found. The mismatched rows are candidate locations for the")
        print("   unidentified third upstream-inherited transcription bug (Open Question")
        print("   #1 in the README). Each mismatch tells us:")
        print()
        print("     - Either Heim's listed (n, m, p, σ) is the correct ground-truth and")
        print("       our calc_n / calc_W chain produces wrong values for this particle;")
        print("     - Or our W is correct and Heim's listed values are from a different")
        print("       decomposition rule than the one we implemented from [B40]-[B46].")
        print()
        print("   Either way, the row pinpoints where to look. Recommended next step:")
        print("   for each mismatched particle, print W, N_1..N_6, Q_n..Q_σ, and the")
        print("   greedy-step intermediates to determine which of the two scenarios is")
        print("   active.")
        print("=" * 110)


if __name__ == "__main__":
    main()
