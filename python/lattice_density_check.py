"""
Lattice density check at Heim's 21 ground-state mass points.

See LATTICE_DENSITY_PREREGISTRATION.md for the protocol.
The pre-registered metric: for each precision tier T, count
(n, m, p, σ) tuples whose predicted mass lies within T of Heim's
target mass, then report the median count across the 19 well-
behaved particles.

This tells us at which precision tier Heim's lattice transitions
from sparse (median ≤ 2 — his tuple uniquely close) to dense
(median ≫ 1 — many alternatives).

Output: python/lattice_density_results.txt.
"""

from __future__ import annotations

import math
from math import fabs
from statistics import median

import formulae as fm
from constants import (KG_TO_MEV, alpha_minus, alpha_plus, eta, mass_element,
                       theta)
from particle import REFERENCE_PARTICLES


# Precision tiers (in MeV).  Order matters — bands are progressively wider.
TIERS_MEV = [
    ("2 eV",   2e-6),
    ("100 eV", 1e-4),
    ("1 keV",  1e-3),
    ("10 keV", 1e-2),
    ("100 keV",1e-1),
    ("1 MeV",  1.0),
    ("10 MeV", 10.0),
]


def count_close_tuples(eps: int, k: int, P: int, Q: int, kap: int, q_x: float,
                        M_target_MeV: float,
                        K_n_max=60, K_m_max=70, K_p_max=70, K_sig_max=40):
    """Enumerate all (n, m, p, σ) tuples reachable in the sector
    (ε, k, P, Q, κ, q) under Heim's exhaustion ordering.  Return:

    {
      "rank1_dM_MeV":    smallest |M_pred − M_target|,
      "rank2_dM_MeV":    second-smallest |M_pred − M_target|,
      "tier_counts":     dict from tier-label → count of tuples within that tier,
      "n_total":         total number of reachable tuples in this sector,
    }
    """
    q = fabs(q_x)
    eta00 = eta(1, 0)
    th = theta(eta00)
    a_p = alpha_plus(eta00, th)
    a_m = alpha_minus(eta00, th)
    mu = mass_element()
    mu_ap_MeV = mu * a_p * KG_TO_MEV
    qterm_MeV = 4 * q * mu * a_m * KG_TO_MEV
    I = fm.calc_Q(k)
    N = fm.calc_N(k, q, I)
    a1 = N[0]
    a2 = 1.5 * N[1]
    a3 = 0.5 * N[2]
    Q_n, Q_m, Q_p, Q_sig = I

    S = ((I[0] * (I[0] + 1))**2 * N[0]
         + I[1] * (2*I[1]**2 + 3*I[1] + 1) * N[1]
         + I[2] * (I[2] + 1) * N[2]
         + 4 * I[3])
    PHI = P * (-1)**(P+Q) * (P+Q) * N[4] + Q * (P+1) * N[5]

    tier_counts = {label: 0 for label, _ in TIERS_MEV}
    rank1 = math.inf
    rank2 = math.inf
    n_total = 0

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
                bracket_no_sig = (K_piece_n + K_piece_m + K_piece_p + S
                                   + F_piece_n + F_piece_m + F_piece_p + PHI)
                for K_sig in range(Q_sig + 1, K_sig_max + 1):
                    sig_ = K_sig - 1 - Q_sig
                    bracket = bracket_no_sig + 4 * sig_
                    M_MeV = mu_ap_MeV * bracket + qterm_MeV
                    if M_MeV <= 0:
                        continue
                    n_total += 1
                    dM = abs(M_MeV - M_target_MeV)
                    if dM < rank1:
                        rank2 = rank1
                        rank1 = dM
                    elif dM < rank2:
                        rank2 = dM
                    for label, T in TIERS_MEV:
                        if dM <= T:
                            tier_counts[label] += 1

    return {
        "rank1_dM_MeV": rank1,
        "rank2_dM_MeV": rank2,
        "tier_counts": tier_counts,
        "n_total": n_total,
    }


def classify_tier(median_count: float) -> str:
    if median_count <= 2:
        return "sparse"
    if median_count <= 10:
        return "moderately dense"
    return "dense"


def main():
    print("=" * 110)
    print(" Lattice density check at Heim's 21 ground-state mass points")
    print(" Pre-registration: LATTICE_DENSITY_PREREGISTRATION.md")
    print("=" * 110)

    # Exclude e_0 (neutral electron, no measured counterpart, target mass = 0)
    # and the two Heim-self-inconsistent Δ outliers (Δ⁺⁺ and Δ⁰) per pre-reg.
    excluded_names = {"e_0", "DELTA_++", "DELTA_0"}

    results = []
    for p in REFERENCE_PARTICLES:
        if p.symbol in excluded_names:
            continue
        # Use Heim's *predicted* mass as the target — this IS Heim's intended
        # Tabelle II value (we verified ≤ 2 eV against published values).
        M_target = p.mass_mev
        q_x = p.charge
        info = count_close_tuples(
            p.eps, p.k, p.P, p.Q, p.kap, q_x, M_target
        )
        results.append((p.symbol, M_target, info))

    print()
    print(f"  {'particle':<10} {'M_target':>14}  {'rank1 [MeV]':>14}  {'rank2 [MeV]':>14}  "
          f"{'n_total':>8}    counts within tier")
    print(f"  {'-'*10} {'-'*14}  {'-'*14}  {'-'*14}  {'-'*8}    -------------------")
    for name, M, info in results:
        tc = info["tier_counts"]
        tier_str = " ".join(f"{label}:{tc[label]}" for label, _ in TIERS_MEV)
        rank1_str = f"{info['rank1_dM_MeV']:.3e}" if info["rank1_dM_MeV"] != math.inf else "-"
        rank2_str = f"{info['rank2_dM_MeV']:.3e}" if info["rank2_dM_MeV"] != math.inf else "-"
        print(f"  {name:<10} {M:>14.7f}  {rank1_str:>14}  {rank2_str:>14}  "
              f"{info['n_total']:>8}    {tier_str}")

    # Compute median count per tier
    print()
    print("=" * 110)
    print(" Pre-registered metric: median count of close tuples per precision tier")
    print("=" * 110)
    print(f"  (n = {len(results)} particles)")
    print()
    print(f"  {'tier':<10}  {'median':>8}  {'min':>6}  {'max':>6}  {'classification':<20}")
    print(f"  {'-'*10}  {'-'*8}  {'-'*6}  {'-'*6}  {'-'*20}")
    tier_medians = {}
    for label, T in TIERS_MEV:
        counts = [info["tier_counts"][label] for _, _, info in results]
        m = median(counts)
        cls = classify_tier(m)
        tier_medians[label] = (m, cls)
        print(f"  {label:<10}  {m:>8.1f}  {min(counts):>6}  {max(counts):>6}  {cls:<20}")

    # Determine where the lattice transitions to "dense"
    first_dense_tier = None
    for label, T in TIERS_MEV:
        _, cls = tier_medians[label]
        if cls == "dense":
            first_dense_tier = label
            break

    print()
    print("=" * 110)
    print(" VERDICT (pre-registered tiers, not modified after run)")
    print("=" * 110)
    print(f"  First tier where lattice becomes DENSE (median count ≥ 10):  "
          f"{first_dense_tier if first_dense_tier else '(none — sparse at all tested tiers)'}")
    print()
    if first_dense_tier is None:
        print("  → Heim's lattice is sparse all the way to 10 MeV.  Even PDG-level")
        print("    agreement (~10 MeV) is *not* slot-density-aided.  This would CONFLICT")
        print("    with the post-1989 test result, which would need re-examination.")
    elif first_dense_tier == "2 eV":
        print("  → Heim's lattice is dense even at 2 eV.")
        print("    The intra-Heim Tabelle II reproduction is ALSO slot-density-aided.")
        print("    The 'self-consistency at ≤2 eV' anchor collapses; only η-derivation")
        print("    and α-from-formula remain as un-slot-density anchors.")
    elif first_dense_tier in ("100 eV", "1 keV", "10 keV", "100 keV"):
        print(f"  → Heim's lattice becomes dense at {first_dense_tier}.")
        print("    Intra-Heim ≤2 eV match is *structural* (lattice sparse at that")
        print("    precision); PDG agreement at 10 keV–1 MeV is slot-density-aided.")
        print("    The structural anchor 'Tabelle II reproduction at ≤2 eV' SURVIVES.")
        print("    Consistent with the post-1989 test.")
    elif first_dense_tier in ("1 MeV", "10 MeV"):
        print(f"  → Heim's lattice becomes dense at {first_dense_tier}.")
        print("    Intra-Heim consistency AND much of the PDG-percent match is")
        print("    structural; only the very-loose PDG comparison is slot-density.")
        print("    Would partially walk back the post-1989 falsification severity.")


if __name__ == "__main__":
    main()
