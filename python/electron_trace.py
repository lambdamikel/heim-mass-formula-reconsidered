"""
Per-term trace of the electron mass calculation — diagnostic for the
0.79 % electron-mass discrepancy (Open Question #1).

After the May 2026 (n, m, p, σ) cross-check ruled out the greedy
decomposition (see python/nmps_cross_check.py), the bug must live
in calc_W, calc_phi, or the final mass-assembly
    M = μ · α_+ · (K + S + F + Φ + 4 q α_-).
This script decomposes both e_0 (q=0, σ=1) and e_- (q=1, σ=0) into
the five constituent pieces and identifies *which piece* carries
the missing 1.72-unit contribution that would bring our e_- value
up to Heim's published 0.51100343 MeV.

Run with:
    ./venv/bin/python python/electron_trace.py
"""

from __future__ import annotations

from math import fabs

import formulae as fm
from constants import (KG_TO_MEV, alpha_minus, alpha_plus, eta, mass_element,
                       theta)


CONFIGS = [
    # (name, eps, k, P, Q, kap, x, heim_published_MeV)
    ("e_0", 1, 1, 1, 1, 0, 0, 0.51617049),   # Heim G-Tabelle II
    ("e_-", 1, 1, 1, 1, 0, 1, 0.51100343),   # Heim G-Tabelle II
]


def trace(name, eps, k, P, Q, kap, x, heim_MeV):
    q_x = fm.calc_charge(eps, k, P, Q, kap, x)
    q = fabs(q_x)

    eta00 = eta(1, 0)
    th = theta(eta00)
    a_p = alpha_plus(eta00, th)
    a_m = alpha_minus(eta00, th)
    mu = mass_element()
    mu_alpha_p_MeV = mu * a_p * KG_TO_MEV       # MeV per bracket unit

    I = fm.calc_Q(k)
    N = fm.calc_N(k, q, I)
    W = fm.calc_W(eps, k, P, Q, kap, q_x, I)
    nmps = fm.calc_n(k, I, N, W)
    phi_val = fm.calc_phi(k, P, Q, kap, q, nmps, I, N, W)

    K = ((nmps[0] * (nmps[0] + 1)) ** 2 * N[0]
         + nmps[1] * (2 * nmps[1] ** 2 + 3 * nmps[1] + 1) * N[1]
         + nmps[2] * (nmps[2] + 1) * N[2] + 4 * nmps[3])
    S = ((I[0] * (I[0] + 1)) ** 2 * N[0]
         + I[1] * (2 * I[1] ** 2 + 3 * I[1] + 1) * N[1]
         + I[2] * (I[2] + 1) * N[2] + 4 * I[3])
    F = (2 * nmps[0] * I[0] *
         (1 + 3 * (nmps[0] + I[0] + nmps[0] * I[0])
          + 2 * (nmps[0] ** 2 + I[0] ** 2)) * N[0]
         + 6 * nmps[1] * I[1] * (1 + nmps[1] + I[1]) * N[1]
         + 2 * nmps[2] * I[2] * N[2] + phi_val)
    PHI = P * (-1) ** (P + Q) * (P + Q) * N[4] + Q * (P + 1) * N[5]
    qterm = 4 * q * a_m

    bracket = K + S + F + PHI + qterm
    M_ours_MeV = mu_alpha_p_MeV * bracket

    return {
        "name": name, "q_x": q_x, "q": q, "nmps": nmps,
        "K": K, "S": S, "F": F, "PHI": PHI, "qterm": qterm,
        "bracket": bracket, "mu_alpha_p_MeV": mu_alpha_p_MeV,
        "M_ours": M_ours_MeV, "M_heim": heim_MeV,
        "bracket_heim": heim_MeV / mu_alpha_p_MeV,
    }


def main():
    print("=" * 86)
    print(" Electron mass discrepancy — per-term decomposition")
    print("=" * 86)

    results = [trace(*c) for c in CONFIGS]

    print(f"\n  μ · α_+ = {results[0]['mu_alpha_p_MeV']:.10f} MeV per bracket unit")
    print(f"  η(1, 0) = {eta(1, 0):.10f}")
    print(f"  α_+    = {alpha_plus(eta(1,0), theta(eta(1,0))):.10e}")
    print(f"  α_-    = {alpha_minus(eta(1,0), theta(eta(1,0))):.10e}")
    print()

    print(f"  {'Term':<12} {'e_0 (q=0)':>14}  {'e_- (q=1)':>14}  {'Δ (e_- - e_0)':>16}")
    print("  " + "-" * 60)
    for k_ in ["K", "S", "F", "PHI", "qterm", "bracket"]:
        v0 = results[0][k_]
        v1 = results[1][k_]
        delta = v1 - v0
        print(f"  {k_:<12} {v0:>14.6f}  {v1:>14.6f}  {delta:>+16.6f}")

    print(f"  {'M (MeV)':<12} {results[0]['M_ours']:>14.6f}  "
          f"{results[1]['M_ours']:>14.6f}  "
          f"{(results[1]['M_ours']-results[0]['M_ours'])*1000:>+14.4f} keV")
    print()

    print("=" * 86)
    print(" Vs Heim's published Tabelle II values")
    print("=" * 86)
    for r in results:
        print(f"\n  {r['name']}:")
        print(f"    Our M:         {r['M_ours']:.6f} MeV")
        print(f"    Heim T-II:     {r['M_heim']:.6f} MeV")
        print(f"    Δ (ours - H):  {(r['M_ours'] - r['M_heim'])*1000:+.4f} keV "
              f"({(r['M_ours']/r['M_heim'] - 1)*100:+.4f} %)")
        print(f"    Heim's implied bracket: {r['bracket_heim']:.4f}")
        print(f"    Our   bracket:          {r['bracket']:.4f}")
        print(f"    Bracket gap (Heim-ours): {r['bracket_heim']-r['bracket']:+.4f}")

    print()
    print("=" * 86)
    print(" Diagnosis")
    print("=" * 86)

    d_M_ours = results[1]['M_ours'] - results[0]['M_ours']
    d_M_heim = results[1]['M_heim'] - results[0]['M_heim']
    d_br_ours = results[1]['bracket'] - results[0]['bracket']
    d_br_heim = results[1]['bracket_heim'] - results[0]['bracket_heim']
    print(f"""
  Δ(e_- − e_0) according to our port:  {d_M_ours*1000:+.4f} keV  (bracket {d_br_ours:+.4f})
  Δ(e_- − e_0) according to Heim:      {d_M_heim*1000:+.4f} keV  (bracket {d_br_heim:+.4f})
  Gap in ΔΣ:                           {d_br_ours - d_br_heim:+.4f}

  e_0 matches Heim exactly.  e_- is too LIGHT in our port by
  {abs(results[1]['M_ours']-results[1]['M_heim'])*1000:.2f} keV.

  Within our decomposition, going from e_0 to e_- changes only:
    K: +4 → 0           (because σ goes 1 → 0)              ← -4.000
    S: barely changes (η-dependence of N_1..N_3)            ←  -0.00005
    4qα_-: 0 → +0.0325  (the charge correction)             ← +0.0325
  Net: ΔΣ = -3.97 units → ΔM = -9.21 keV.

  Heim says ΔM (e_- − e_0) should only be -5.17 keV → ΔΣ = -2.23.

  So the +4·n[3] term in the K-piece carries too much weight here
  relative to Heim's framework, OR there is an additional q-dependent
  term in [B3] that we do not implement and that adds +1.72 units
  for q ≠ 0 charged states.

  Two concrete diagnostic next steps:
    (a) Re-read the IGW Innsbruck restatement of [B3] (the K-piece
        in formulae.calc_mass corresponds to the "G_underline" of
        the 1989 manuscript) and verify the σ-coefficient is "4",
        not something like "4·η_qk" or "4·(1-q·something)".
    (b) Check whether [B5]'s F-piece or [B6]'s Φ-piece has a
        q-dependent term we are dropping for the special case
        n=(0,0,0,0).  Currently F=0 trivially because the
        (n[0]·I[0]), (n[1]·I[1]), (n[2]·I[2]) cross-terms all
        vanish at the ground-bound — but a φ-contribution for
        charged ground-state leptons might still be non-trivial.
""")


if __name__ == "__main__":
    main()
