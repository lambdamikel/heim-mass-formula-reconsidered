"""
Pre-registered test: Heim 1989 vs. post-1989 particle physics.

See POST_1989_PREREGISTRATION.md for the protocol.  This script
implements steps 1-4 + the random-background scan.  Acceptance
criteria are evaluated against pre-registered thresholds.

Output goes to python/post_1989_test_results.txt.
"""

from __future__ import annotations

import math
import random
from math import fabs

import formulae as fm
from constants import (KG_TO_MEV, alpha_minus, alpha_plus, eta, mass_element,
                       theta)


# Tier 1 targets — pre-1989 discoveries (Heim could have known)
# (name, mass_MeV, |q|, P_target=2I, Q_target=2J)
TIER_1 = [
    ("tau (τ)",       1776.86, 1, 1, 1),   # I=1/2, J=1/2
    ("J/psi",         3096.90, 0, 0, 2),   # I=0,   J=1
    ("psi(2S)",       3686.10, 0, 0, 2),
    ("Upsilon(1S)",   9460.30, 0, 0, 2),
    ("D0",            1864.84, 0, 1, 0),   # I=1/2, J=0
    ("D+",            1869.66, 1, 1, 0),
    ("Ds+",           1968.35, 1, 0, 0),
    ("B0",            5279.66, 0, 1, 0),
    ("B+",            5279.34, 1, 1, 0),
    ("W boson",      80369.0,  1, 0, 2),   # weak isospin treated as 0
    ("Z boson",      91188.0,  0, 0, 2),
    ("Lambda_c+",     2286.46, 1, 0, 1),
]

# Tier 2 — post-1989 (exploratory, reported but not scored)
TIER_2 = [
    ("top quark",   172570.0,  1, 1, 1),   # constituent value, exploratory
    ("Higgs H0",    125250.0,  0, 0, 0),   # spin-0, isospin-0
    ("Bs0",           5366.93, 0, 0, 0),
    ("Bc+",           6274.47, 1, 0, 0),
    ("Sigma_c++",     2453.97, 2, 2, 1),
    ("Sigma_c0",      2453.75, 0, 2, 1),
    ("Xi_c+",         2467.71, 1, 1, 1),
    ("Lambda_b0",     5619.60, 0, 0, 1),
    ("Sigma_b+",      5810.56, 1, 2, 1),
    ("Omega_b-",      6045.20, 1, 0, 1),
]


# Note: Tier-1 has 12 entries (we added D0/D+ split, B0/B+ split as the
# pre-registration suggested "D⁰/±" and "B⁰/±" as single rows).  We score
# them as 12 entries against the same thresholds, treating "≥6/11" in the
# pre-registration as the floor.


def best_match_in_sector(k: int, P: int, Q: int, kap: int, q_x: float,
                          target_mass: float,
                          K_n_max=60, K_m_max=70, K_p_max=70, K_sig_max=40):
    """Enumerate (n,m,p,σ) tuples reachable in this sector under
    Heim's exhaustion ordering, return best mass match to target_mass.

    K-limits match resonance_wscan_baryons.py (Heim's working range).
    Returns dict with keys M_MeV, K_B, nmps, K, dM_pct, or None if the
    sector itself returns an invalid base.
    """
    q = fabs(q_x)
    try:
        eta00 = eta(1, 0)
        th = theta(eta00)
        a_p = alpha_plus(eta00, th)
        a_m = alpha_minus(eta00, th)
        mu = mass_element()
        mu_ap_MeV = mu * a_p * KG_TO_MEV
        qterm_MeV = 4 * q * mu * a_m * KG_TO_MEV
        I = fm.calc_Q(k)
        N = fm.calc_N(k, q, I)
    except Exception:
        return None
    a1 = N[0]
    a2 = 1.5 * N[1]
    a3 = 0.5 * N[2]
    Q_n, Q_m, Q_p, Q_sig = I

    S = ((I[0] * (I[0] + 1))**2 * N[0]
         + I[1] * (2*I[1]**2 + 3*I[1] + 1) * N[1]
         + I[2] * (I[2] + 1) * N[2]
         + 4 * I[3])
    PHI = P * (-1)**(P+Q) * (P+Q) * N[4] + Q * (P+1) * N[5]

    best_dM = math.inf
    best = None

    # Mass grows monotonically with each K — once we're above target by 2× we
    # can stop the inner sigma loop (it only adds to mass).
    stop_threshold = target_mass * 2.0

    for K_n in range(Q_n + 1, K_n_max + 1):
        n_ = K_n - 1 - Q_n
        K_piece_n = (n_ * (n_ + 1))**2 * N[0]
        F_piece_n = 2*n_*I[0]*(1 + 3*(n_+I[0]+n_*I[0]) + 2*(n_**2 + I[0]**2)) * N[0]
        w1_max = a1 * (3 * K_n * K_n - 3 * K_n + 1)
        Km_struct = int((w1_max / a2) ** 0.5) + 2 if a2 > 0 else K_m_max
        Km_top = min(Km_struct, K_m_max)
        for K_m in range(Q_m + 1, Km_top + 1):
            m_ = K_m - 1 - Q_m
            if a2 > 0 and (K_m - 1) ** 2 * a2 >= w1_max:
                continue
            K_piece_m = m_ * (2*m_**2 + 3*m_ + 1) * N[1]
            F_piece_m = 6*m_*I[1]*(1+m_+I[1]) * N[1]
            w2_max_in_Km = a2 * (2 * K_m - 1) if a2 > 0 else 0
            w2_max_from_w1 = w1_max - (K_m - 1) ** 2 * a2
            w2_max = min(w2_max_in_Km, w2_max_from_w1) if a2 > 0 else w1_max
            Kp_struct = int(w2_max / a3) + 2 if a3 > 0 else K_p_max
            Kp_top = min(Kp_struct, K_p_max)
            for K_p in range(Q_p + 1, Kp_top + 1):
                p_ = K_p - 1 - Q_p
                if a3 > 0 and (K_p - 1) * a3 >= w2_max:
                    continue
                K_piece_p = p_ * (p_ + 1) * N[2]
                F_piece_p = 2*p_*I[2] * N[2]
                L_sigma = 0.5 * N[2] * (p_ + I[2]) - I[3]
                bracket_no_sig = (K_piece_n + K_piece_m + K_piece_p + S
                                   + F_piece_n + F_piece_m + F_piece_p + PHI)
                M_no_sig = mu_ap_MeV * bracket_no_sig + qterm_MeV
                if M_no_sig > stop_threshold:
                    # mass only grows with sigma — skip this K_p, but other K_p
                    # at the same K_m might give lower mass via different L_sigma
                    # contribution... actually L_sigma doesn't enter mass, so
                    # we can break out of the K_p loop here.
                    break
                for K_sig in range(Q_sig + 1, K_sig_max + 1):
                    sig_ = K_sig - 1 - Q_sig
                    bracket = bracket_no_sig + 4 * sig_
                    M_MeV = mu_ap_MeV * bracket + qterm_MeV
                    if M_MeV <= 0:
                        continue
                    dM = abs(M_MeV - target_mass)
                    if dM < best_dM:
                        best_dM = dM
                        best = {
                            "K": (K_n, K_m, K_p, K_sig),
                            "nmps": (n_, m_, p_, sig_),
                            "M_MeV": M_MeV,
                            "K_B": L_sigma - sig_,
                            "dM_pct": dM / target_mass * 100.0,
                        }
                    if M_MeV > stop_threshold:
                        break
    return best


def scan_target(target_mass, target_q, target_P, target_Q,
                K_n_max=60, K_sig_max=40):
    """Try every (eps, k, kap, x) sector that produces target charge and
    target (P, Q).  Return best overall mass match."""
    best = None
    for eps in (+1, -1):
        for k in (1, 2):
            for kap in (0, 1):
                for x in range(0, 9):
                    try:
                        qx = fm.calc_charge(eps, k, target_P, target_Q, kap, x)
                    except Exception:
                        continue
                    qx_int = round(qx)
                    if abs(qx - qx_int) > 0.01:
                        continue
                    if abs(qx_int) != target_q:
                        continue
                    match = best_match_in_sector(
                        k, target_P, target_Q, kap, float(qx_int),
                        target_mass, K_n_max, K_sig_max
                    )
                    if match is None:
                        continue
                    if best is None or match["dM_pct"] < best["dM_pct"]:
                        best = dict(match)
                        best["eps"] = eps
                        best["k"] = k
                        best["P"] = target_P
                        best["Q"] = target_Q
                        best["kap"] = kap
                        best["x"] = x
                        best["q_x"] = qx_int
    return best


def classify(dM_pct):
    if dM_pct is None:
        return "no_match"
    if dM_pct <= 1.0:
        return "strict"
    if dM_pct <= 3.0:
        return "moderate"
    if dM_pct <= 10.0:
        return "relaxed"
    return "no_match"


def run_targets(targets, label):
    rows = []
    print(f"\n{'='*100}")
    print(f" {label}")
    print(f"{'='*100}")
    print(f"  {'particle':<14} {'target [MeV]':>14}  q  P  Q  → "
          f"{'best [MeV]':>14}  {'Δ%':>7}  {'tier':<10} (ε,k,κ,x,nmps)")
    print(f"  {'-'*98}")
    for name, m, q, P, Q in targets:
        best = scan_target(m, q, P, Q)
        if best is None:
            row_tier = "no_match"
            print(f"  {name:<14} {m:>14.2f}  {q:<2} {P:<2} {Q:<2}  → "
                  f"{'no sector':>14}    {'-':>7}  {row_tier:<10}")
        else:
            row_tier = classify(best["dM_pct"])
            print(f"  {name:<14} {m:>14.2f}  {q:<2} {P:<2} {Q:<2}  → "
                  f"{best['M_MeV']:>14.2f}  {best['dM_pct']:>6.2f}%  "
                  f"{row_tier:<10} "
                  f"(ε={best['eps']:+d} k={best['k']} κ={best['kap']} "
                  f"x={best['x']} nmps={best['nmps']})")
        rows.append((name, m, q, P, Q, best, row_tier))
    return rows


def tally(rows):
    cnt = {"strict": 0, "moderate": 0, "relaxed": 0, "no_match": 0}
    for *_, tier in rows:
        cnt[tier] = cnt.get(tier, 0) + 1
    cnt["moderate_or_better"] = cnt["strict"] + cnt["moderate"]
    cnt["relaxed_or_better"] = cnt["moderate_or_better"] + cnt["relaxed"]
    return cnt


def background_scan(n_samples=50, seed=20260516):
    """Generate n random (mass, q, P, Q) targets log-uniform in mass over
    [100 MeV, 200 GeV], run the same scan.  Pre-registered: seed fixed."""
    rng = random.Random(seed)
    samples = []
    print(f"\n{'='*100}")
    print(f" BACKGROUND SCAN: {n_samples} random (mass, P, Q, q) — log-uniform [100 MeV, 200 GeV]")
    print(f"{'='*100}")
    for i in range(n_samples):
        log_m = rng.uniform(math.log10(100.0), math.log10(200_000.0))
        m = 10.0 ** log_m
        # P, Q drawn uniformly to match the rough range of the real targets
        P = rng.randint(0, 4)
        Q = rng.randint(0, 4)
        q = rng.choice([0, 0, 0, 1, 1, 2])  # match real-target charge distribution
        best = scan_target(m, q, P, Q)
        tier = classify(best["dM_pct"]) if best else "no_match"
        samples.append((f"rand_{i:02d}", m, q, P, Q, best, tier))
    cnt = tally(samples)
    print(f"  Background tally (n={n_samples}):")
    print(f"    strict   ≤ 1%:  {cnt['strict']:>2}  ({100*cnt['strict']/n_samples:.1f}%)")
    print(f"    moderate ≤ 3%:  {cnt['moderate']:>2}  ({100*cnt['moderate']/n_samples:.1f}%)")
    print(f"    relaxed  ≤10%:  {cnt['relaxed']:>2}  ({100*cnt['relaxed']/n_samples:.1f}%)")
    print(f"    moderate-or-better:  {cnt['moderate_or_better']:>2}  "
          f"({100*cnt['moderate_or_better']/n_samples:.1f}%)")
    print(f"    no match  >10%: {cnt['no_match']:>2}")
    return samples, cnt


def evaluate_acceptance(t1_cnt, bg_cnt, n_t1, n_bg):
    """Apply pre-registered acceptance criteria.

    Strong:    ≥6/11 strict + bg strict-rate ≤ 25% of signal strict-rate
    Moderate:  ≥4/11 moderate-or-better + signal/bg ≥ 2× at moderate tier
    Null:      <4/11 moderate, OR signal/background <2× at moderate tier
    Falsified: signal ≤ background at moderate tier
    """
    sig_strict_rate = t1_cnt["strict"] / n_t1
    sig_mod_rate    = t1_cnt["moderate_or_better"] / n_t1
    bg_strict_rate  = bg_cnt["strict"] / n_bg
    bg_mod_rate     = bg_cnt["moderate_or_better"] / n_bg

    print(f"\n{'='*100}")
    print(f" ACCEPTANCE / FALSIFICATION (pre-registered)")
    print(f"{'='*100}")
    print(f"  Tier-1 signal:")
    print(f"    strict        ≤ 1%:  {t1_cnt['strict']} / {n_t1}  = {100*sig_strict_rate:.1f}%")
    print(f"    moderate-or-better: {t1_cnt['moderate_or_better']} / {n_t1}  = {100*sig_mod_rate:.1f}%")
    print(f"  Background:")
    print(f"    strict        ≤ 1%:  {bg_cnt['strict']} / {n_bg}  = {100*bg_strict_rate:.1f}%")
    print(f"    moderate-or-better: {bg_cnt['moderate_or_better']} / {n_bg}  = {100*bg_mod_rate:.1f}%")

    sb_strict = sig_strict_rate / bg_strict_rate if bg_strict_rate > 0 else float("inf")
    sb_mod    = sig_mod_rate    / bg_mod_rate    if bg_mod_rate    > 0 else float("inf")
    print(f"  Signal / Background ratios:")
    print(f"    strict tier:        {sb_strict:.2f}×")
    print(f"    moderate tier:      {sb_mod:.2f}×")

    print(f"\n  Bucket decision (criteria fixed before scan):")

    strong = (t1_cnt["strict"] >= 6 and bg_strict_rate <= 0.25 * sig_strict_rate)
    moderate = (t1_cnt["moderate_or_better"] >= 4 and sb_mod >= 2.0)
    falsified = (sig_mod_rate <= bg_mod_rate)

    if strong:
        verdict = "STRONG CONFIRMATION — Heim extrapolates beyond 1989"
    elif moderate:
        verdict = "MODERATE CONFIRMATION — Heim partially extrapolates"
    elif falsified:
        verdict = "FALSIFICATION — signal at or below chance"
    else:
        verdict = "NULL RESULT — framework appears 1989-bounded"

    print(f"\n  >>> {verdict}")
    return verdict


def main():
    print(f"\n{'#'*100}")
    print(f"# Heim 1989 framework — post-1989 particle slot test")
    print(f"# Pre-registration: POST_1989_PREREGISTRATION.md (committed 181110c)")
    print(f"{'#'*100}")

    t1_rows = run_targets(TIER_1, "TIER 1 — pre-1989 discoveries (scored)")
    t1_cnt  = tally(t1_rows)
    print(f"\n  Tier-1 tally (n={len(TIER_1)}):")
    print(f"    strict   ≤ 1%:  {t1_cnt['strict']}")
    print(f"    moderate ≤ 3%:  {t1_cnt['moderate']}")
    print(f"    relaxed  ≤10%:  {t1_cnt['relaxed']}")
    print(f"    moderate-or-better: {t1_cnt['moderate_or_better']}")
    print(f"    no match  >10%: {t1_cnt['no_match']}")

    t2_rows = run_targets(TIER_2, "TIER 2 — post-1989 (exploratory, not scored)")
    t2_cnt  = tally(t2_rows)
    print(f"\n  Tier-2 tally (n={len(TIER_2)}, exploratory):")
    print(f"    strict / moderate / relaxed / no_match: "
          f"{t2_cnt['strict']} / {t2_cnt['moderate']} / {t2_cnt['relaxed']} / {t2_cnt['no_match']}")

    bg_rows, bg_cnt = background_scan(n_samples=50)

    evaluate_acceptance(t1_cnt, bg_cnt, len(TIER_1), 50)


if __name__ == "__main__":
    main()
