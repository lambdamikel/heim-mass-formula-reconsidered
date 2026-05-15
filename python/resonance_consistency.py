"""
Anregerfunktion consistency check for the matched (n,m,p,σ) configs.

For each Tabelle IV entry matched in resonance_wscan.py we re-derive the
implied w and check whether f(N) = w/W_0 - 1 fits f(N) = a·N/(N+1) + b·N
within each (P, Q, κ) sector.

If our matched configs really are Heim's assignments, the implied f(N)
across entries in one sector should lie on a smooth 2-parameter curve.
If residuals are large, the matches are accidental (degenerate (M, K_B)
matches in a 2.4M-config space).
"""

from __future__ import annotations

from collections import defaultdict
from math import exp

import numpy as np

import formulae as fm
from g_tables import TABLE_IV_MESONS_K1
from resonance_wscan import match_sector


SECTORS = {
    "ε":         (0, 0, 0),
    "ω(783)":    (0, 2, 0),
    "η'(958)":   (0, 0, 0),
    "S*(993)":   (0, 0, 0),
    "Φ(1019)":   (0, 2, 0),
    "f(1270)":   (0, 4, 0),
    "D(1285)":   (0, 2, 0),
    "E(1420)":   (0, 2, 0),
    "f'(1514)":  (0, 4, 0),
    "ω(1675)":   (0, 6, 0),
    "K*(892)":   (1, 2, 0),
    "K_A(1240)": (1, 2, 0),
    "K*(1420)":  (1, 4, 0),
    "L(1770)":   (1, 4, 0),
    "ρ(770)":    (2, 2, 0),
    "δ(970)":    (2, 0, 0),
    "A1(1100)":  (2, 2, 0),
    "B(1235)":   (2, 2, 0),
    "A2(1310)":  (2, 4, 0),
    "F1(1540)":  (2, 2, 0),
    "ρ'(1600)":  (2, 2, 0),
    "A3(1640)":  (2, 4, 0),
    "g(1680)":   (2, 6, 0),
}


def implied_w(nmps, I, N_const, k):
    """J0032 eq. 11 lhs.  w_3 from σ via geometric mean of bracket."""
    n_, m_, p_, sig_ = nmps
    Q_n, Q_m, Q_p, Q_sig = I
    a1 = N_const[0]
    a2 = 1.5 * N_const[1]
    a3 = 0.5 * N_const[2]
    beta = (2 * k - 1) / (3.0 * Q_sig) if Q_sig != 0 else 1.0
    K_sig = sig_ + 1 + Q_sig
    w3_lo = exp(-beta * K_sig)
    w3_hi = exp(-beta * (K_sig - 1))
    w3 = (w3_lo * w3_hi) ** 0.5
    return ((n_ + Q_n) ** 3 * a1
            + (m_ + Q_m) ** 2 * a2
            + (p_ + Q_p) * a3
            + w3)


def fit_anregung(N_arr, f_arr):
    """LSQ fit f = a·N/(N+1) + b·N.  Returns (a, b, f_pred)."""
    A = np.column_stack([N_arr / (N_arr + 1.0), N_arr])
    coefs, _, _, _ = np.linalg.lstsq(A, f_arr, rcond=None)
    a, b = coefs
    f_pred = a * N_arr / (N_arr + 1.0) + b * N_arr
    return a, b, f_pred


def main():
    print("=" * 90)
    print(" Anregerfunktion consistency check")
    print("=" * 90)
    print()

    # Build sector groupings
    sector_targets = defaultdict(list)
    target_data = {}
    for r in TABLE_IV_MESONS_K1:
        if r.symbol not in SECTORS:
            continue
        P_, Q_, q_neu = SECTORS[r.symbol]
        if isinstance(r.mass_MeV, tuple):
            M_t, KB_t = r.mass_MeV[0], r.K_B[0]
        else:
            M_t, KB_t = r.mass_MeV, r.K_B
        N_idx = r.N[0] if isinstance(r.N, tuple) else r.N
        sector_targets[(P_, Q_, q_neu)].append((r.symbol, M_t, KB_t))
        target_data[r.symbol] = (M_t, KB_t, N_idx, P_, Q_, q_neu)

    print("Step 1: Re-running config-matching (this took ~6 min last time)...")
    matched = {}
    for (P_, Q_, q_neu), tgts in sector_targets.items():
        # κ does not affect (M, K_B) for resonances (φ omitted), so just κ=0.
        m = match_sector(1, P_, Q_, 0, q_neu, tgts)
        matched.update(m)
        print(f"  done: P={P_} Q={Q_} q={q_neu} ({len(tgts)} entries)")

    # Build per-sector list of (N, sym, nmps, w_implied)
    sector_entries = defaultdict(list)
    I = fm.calc_Q(1)
    N_const = fm.calc_N(1, 0, I)
    for sym, m in matched.items():
        if m is None:
            continue
        M_t, KB_t, N_idx, P_, Q_, q_neu = target_data[sym]
        w = implied_w(m["nmps"], I, N_const, 1)
        sector_entries[(P_, Q_, q_neu)].append((N_idx, sym, m["nmps"], w))

    # Summary table
    print()
    print(f"  {'Sector':<22} {'#entries':>9}  {'κ':>3}  "
          f"{'W_0':>10}  {'a':>10}  {'b':>10}  {'max |Δf|':>10}")
    print("  " + "-" * 82)
    fit_results = {}
    for key, entries in sorted(sector_entries.items()):
        if len(entries) < 2:
            continue
        P_, Q_, q_neu = key
        entries.sort()
        N_np = np.array([e[0] for e in entries], dtype=float)
        w_np = np.array([e[3] for e in entries], dtype=float)
        best = None
        for kap in (0, 1):
            W0 = fm.calc_W(1, 1, P_, Q_, kap, q_neu, I)
            if W0 <= 0:
                continue
            f_arr = w_np / W0 - 1.0
            a, b, f_pred = fit_anregung(N_np, f_arr)
            max_r = float(np.max(np.abs(f_arr - f_pred)))
            if best is None or max_r < best[0]:
                best = (max_r, kap, W0, a, b)
        if best is None:
            print(f"  P={P_} Q={Q_} q={q_neu:<14} {len(entries):>9}  (W_0≤0)")
            continue
        max_r, kap, W0, a, b = best
        fit_results[key] = best
        label = f"P={P_} Q={Q_} q={q_neu}"
        print(f"  {label:<22} {len(entries):>9}  {kap:>3}  "
              f"{W0:>10.3g}  {a:>+10.3f}  {b:>+10.4f}  {max_r:>10.3e}")

    print()
    print("=" * 90)
    print("Detail per sector (entries sorted by published N):")
    print("=" * 90)
    for key, entries in sorted(sector_entries.items()):
        if len(entries) < 2 or key not in fit_results:
            continue
        P_, Q_, q_neu = key
        max_r, kap, W0, a, b = fit_results[key]
        entries.sort()
        print()
        print(f"  Sector (P={P_}, Q={Q_}, q={q_neu})  κ={kap}  W_0={W0:.4g}")
        print(f"  fitted f(N) = {a:+.4f}·N/(N+1) {b:+.4f}·N")
        print(f"    {'N':>5}  {'symbol':<12} {'(n,m,p,σ)':<20} "
              f"{'w_implied':>11}  {'f_implied':>11}  {'f_fit':>11}  {'Δf':>11}")
        for (N_idx, sym, nmps, w) in entries:
            f_imp = w / W0 - 1.0
            f_fit = a * N_idx / (N_idx + 1.0) + b * N_idx
            print(f"    {N_idx:>5}  {sym:<12} {str(nmps):<20} "
                  f"{w:>11.4g}  {f_imp:>+11.4g}  {f_fit:>+11.4g}  "
                  f"{f_imp - f_fit:>+11.3e}")


if __name__ == "__main__":
    main()
