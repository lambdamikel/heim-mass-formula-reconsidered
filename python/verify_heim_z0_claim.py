"""
Verify Heim's claim (J0032 p.27a) that Tabellen IV and V_{a,b,c} are
assembled under the approximative assumption z(N) = 0 with approximation
error under 0.1 MeV, EXCEPT for three explicitly named entries:
ω(783) and η'(958) for k=1, and N(1688) for k=2.

Approach:
  For each Heim entry:
    1. Use Q = Q(N=0) per family (the z=0 ground-state spin).
    2. Find best-fit (n, m, p, σ) configuration under K_B-exact and
       Δ_M-minimised criteria.
    3. Compute implied f_imp = w / W_0(P, Q(N=0), κ, q) - 1.
    4. Compare to f_pred from ab-initio (a, b).
    5. If both Δ_M < 0.1 MeV AND |Δf| < some tolerance, entry confirms
       Heim's z=0 claim.

Output: per-entry verdict.  Cross-reference Heim's named exceptions.
"""

from __future__ import annotations

import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np

import formulae as fm
from g_tables import (TABLE_IV_MESONS_K1, TABLE_V_a_BARYONS_K2,
                      TABLE_V_b_BARYONS_K2, TABLE_V_c_BARYONS_K2_SIGMA)
from anregung_ab_initio import predict as predict_anregung
from pdg_j_lookup import MESON_PDG_J, BARYON_PDG_J
from resonance_consistency_baryons import implied_w_k2
from resonance_wscan_baryons import expand_to_states, scan_all_candidates
from resonance_z0_classify_k1 import (expand_meson_states,
                                        expand_meson_pub_N,
                                        scan_candidates_k1,
                                        CACHE as MESON_CACHE)

BARYON_CACHE = Path(__file__).parent / "baryon_candidates_cache.pkl"

# Heim's named exceptions (J0032 p.27a)
HEIM_EXCEPTIONS = {"ω(783)", "η'(958)", "N(1688)"}


def load_or_scan_baryons():
    if BARYON_CACHE.exists():
        with open(BARYON_CACHE, "rb") as f:
            return pickle.load(f)
    states = (expand_to_states(TABLE_V_a_BARYONS_K2)
              + expand_to_states(TABLE_V_b_BARYONS_K2)
              + expand_to_states(TABLE_V_c_BARYONS_K2_SIGMA))
    out = scan_all_candidates(states)
    with open(BARYON_CACHE, "wb") as f:
        pickle.dump(out, f)
    return out


def load_or_scan_mesons():
    if MESON_CACHE.exists():
        with open(MESON_CACHE, "rb") as f:
            return pickle.load(f)
    states = expand_meson_states()
    out = scan_candidates_k1(states)
    with open(MESON_CACHE, "wb") as f:
        pickle.dump(out, f)
    return out


def main():
    print("=" * 100)
    print(" Heim z=0 claim verification (J0032 p.27a)")
    print("=" * 100)
    print()
    print("Heim's claim: Tabellen IV (k=1) and V_{a,b,c} (k=2) assembled under")
    print("z(N) = 0 approximation, error < 0.1 MeV.  Named exceptions:")
    print("  ω(783) and η'(958) for k=1; N(1688) for k=2.")
    print()

    # Q(N=0) per family — from ground-state J values (PDG_J_LOOKUP)
    # All baryons have J=1/2 ground state (Q=1) except Δ family (J=3/2, Q=3)
    # All mesons in Heim's Tabelle IV are excitations of J=0 ground states (Q=0)
    # or J=1 vector mesons (Q=2 for ω/φ class).  Use the lookup's Q_ground.

    bary_cands = load_or_scan_baryons()
    mes_cands = load_or_scan_mesons()
    print(f"Loaded {len(bary_cands)} baryon candidates, {len(mes_cands)} meson candidates")

    I_k1 = fm.calc_Q(1)
    I_k2 = fm.calc_Q(2)
    Nconst_k1_q0 = fm.calc_N(1, 0, I_k1)
    Nconst_k1_q1 = fm.calc_N(1, 1, I_k1)
    Nconst_k2_q0 = fm.calc_N(2, 0, I_k2)
    Nconst_k2_q1 = fm.calc_N(2, 1, I_k2)

    def get_Nconst(k, qx):
        if k == 1:
            return Nconst_k1_q0 if qx == 0 else Nconst_k1_q1
        return Nconst_k2_q0 if qx == 0 else Nconst_k2_q1

    def Q_ground(label):
        if label in BARYON_PDG_J:
            return BARYON_PDG_J[label].Q_ground
        if label in MESON_PDG_J:
            return MESON_PDG_J[label].Q_ground
        return None

    def pub_N(entry, charge=0):
        if isinstance(entry.N, tuple):
            if len(entry.N) == 2:
                return entry.N[0] if charge == 0 else entry.N[1]
            elif len(entry.N) == 3:
                idx = {-1: 0, 0: 1, 1: 2}[charge]
                return entry.N[idx]
        return entry.N

    # Find best candidate at Q = Q(N=0) per state
    def evaluate(label, P, qx, M_t, KB_t, N_idx, k, cands):
        # Find Q_ground
        base = label.replace("⁻", "").replace("⁰", "").replace("⁺", "").replace("±", "")
        Q0 = Q_ground(base)
        if Q0 is None:
            return None
        # Search candidates at this Q only
        I = I_k1 if k == 1 else I_k2
        Nconst = get_Nconst(k, qx)
        cand_list = [c for c in cands.get(label, []) if c["Q"] == Q0]
        if not cand_list:
            return {"reason": f"no candidate at Q={Q0}", "Q_ground": Q0}
        # Pick smallest dM among Q=Q0 candidates
        best_c = min(cand_list, key=lambda c: c["dM"])
        nmps = best_c["nmps"]
        dM = best_c["dM"]
        dKB = best_c["dKB"]
        # Compute f_imp under both κ and pick best fit to ab-initio prediction
        w = implied_w_k2(nmps, I, Nconst, k=k)
        best_df = None
        best_kap = None
        best_f = None
        for kap in (0, 1):
            W0 = fm.calc_W(1, k, P, Q0, kap, qx, I)
            if W0 <= 0 or not np.isfinite(W0) or W0 > 1e8:
                continue
            f_imp = w / W0 - 1.0
            a_pred, b_pred = predict_anregung(k, P, Q0, kap, qx)
            f_pred = a_pred * N_idx / (N_idx + 1.0) + b_pred * N_idx
            df = abs(f_imp - f_pred)
            if best_df is None or df < best_df:
                best_df = df
                best_kap = kap
                best_f = (f_imp, f_pred)
        if best_df is None:
            return {"reason": "no valid W_0 at Q=Q_ground", "Q_ground": Q0,
                    "dM": dM, "dKB": dKB, "nmps": nmps}
        return {"Q_ground": Q0, "kap": best_kap, "nmps": nmps,
                "dM": dM, "dKB": dKB,
                "f_imp": best_f[0], "f_pred": best_f[1], "df": best_df}

    # Mesons
    print()
    print("=== k=1 mesonic resonances ===")
    print(f"  {'symbol':<14} {'P':>2} {'qx':>3} {'N':>4} "
          f"{'Q₀':>3} {'κ':>3} {'ΔM':>9} {'ΔKB':>5} {'|Δf|':>9}  verdict")
    print("  " + "-" * 90)
    meson_pub_N = expand_meson_pub_N()
    meson_states = expand_meson_states()
    pass_meson = []
    fail_meson = []
    for label, P, qx, M_t, KB_t in meson_states:
        N_idx = meson_pub_N.get(label)
        if N_idx is None:
            continue
        r = evaluate(label, P, qx, M_t, KB_t, N_idx, 1, mes_cands)
        base = label.replace("⁻", "").replace("⁰", "").replace("⁺", "").replace("±", "")
        is_exception = base in HEIM_EXCEPTIONS
        if r is None:
            print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d}  -- no Q_ground --")
            continue
        if "reason" in r:
            verdict = "NO-FIT"
            print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d} "
                  f"{r['Q_ground']:>3}        ({r['reason']})  "
                  f"{'(exception)' if is_exception else 'FAIL'}")
            fail_meson.append((label, "no W_0"))
            continue
        passes = (r["dM"] < 0.1 and r["df"] < 0.05)
        verdict = "PASS" if passes else ("EXCEPTION" if is_exception else "FAIL")
        print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d} "
              f"{r['Q_ground']:>3} {r['kap']:>3} "
              f"{r['dM']:>+9.4f} {r['dKB']:>+5.2f} {r['df']:>9.4f}  {verdict}")
        (pass_meson if passes else fail_meson).append((label, r))

    print()
    print(f"  Mesons: {len(pass_meson)} pass / {len(fail_meson)} fail")

    # Baryons
    print()
    print("=== k=2 baryonic resonances ===")
    print(f"  {'symbol':<14} {'P':>2} {'qx':>3} {'N':>4} "
          f"{'Q₀':>3} {'κ':>3} {'ΔM':>9} {'ΔKB':>5} {'|Δf|':>9}  verdict")
    print("  " + "-" * 90)
    baryon_pub_N = {}
    for tbl in (TABLE_V_a_BARYONS_K2, TABLE_V_b_BARYONS_K2, TABLE_V_c_BARYONS_K2_SIGMA):
        for r in tbl:
            if isinstance(r.N, tuple):
                if len(r.N) == 2:
                    baryon_pub_N[f"{r.symbol}⁰"] = r.N[0]
                    baryon_pub_N[f"{r.symbol}±"] = r.N[1]
                elif len(r.N) == 3:
                    baryon_pub_N[f"{r.symbol}⁻"] = r.N[0]
                    baryon_pub_N[f"{r.symbol}⁰"] = r.N[1]
                    baryon_pub_N[f"{r.symbol}⁺"] = r.N[2]
            else:
                baryon_pub_N[r.symbol] = r.N

    baryon_states = (expand_to_states(TABLE_V_a_BARYONS_K2)
                      + expand_to_states(TABLE_V_b_BARYONS_K2)
                      + expand_to_states(TABLE_V_c_BARYONS_K2_SIGMA))
    pass_bary = []
    fail_bary = []
    for label, P, qx, M_t, KB_t in baryon_states:
        N_idx = baryon_pub_N.get(label)
        if N_idx is None:
            continue
        r = evaluate(label, P, qx, M_t, KB_t, N_idx, 2, bary_cands)
        base = label.replace("⁻", "").replace("⁰", "").replace("⁺", "").replace("±", "")
        is_exception = base in HEIM_EXCEPTIONS
        if r is None:
            continue
        if "reason" in r:
            print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d} "
                  f"{r['Q_ground']:>3}        ({r['reason']})  "
                  f"{'(exception)' if is_exception else 'FAIL'}")
            fail_bary.append((label, "no W_0"))
            continue
        passes = (r["dM"] < 0.1 and r["df"] < 0.05)
        verdict = "PASS" if passes else ("EXCEPTION" if is_exception else "FAIL")
        print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d} "
              f"{r['Q_ground']:>3} {r['kap']:>3} "
              f"{r['dM']:>+9.4f} {r['dKB']:>+5.2f} {r['df']:>9.4f}  {verdict}")
        (pass_bary if passes else fail_bary).append((label, r))

    print()
    print(f"  Baryons: {len(pass_bary)} pass / {len(fail_bary)} fail")

    # Cross-reference: who fails vs Heim's named exceptions?
    print()
    print("=== Cross-reference with Heim's named exceptions ===")
    failed_labels = {l for l, _ in fail_meson + fail_bary}
    print(f"  Heim's named exceptions: {sorted(HEIM_EXCEPTIONS)}")
    print(f"  Our failed entries (subset shown):")
    expected_fails = set()
    surprise_fails = set()
    for lab in failed_labels:
        base = lab.replace("⁻", "").replace("⁰", "").replace("⁺", "").replace("±", "")
        if base in HEIM_EXCEPTIONS:
            expected_fails.add(lab)
        else:
            surprise_fails.add(lab)
    print(f"    expected (Heim-named): {sorted(expected_fails)}")
    print(f"    additional fails:      {len(surprise_fails)} entries")
    if len(surprise_fails) < 20:
        for lab in sorted(surprise_fails):
            print(f"      {lab}")


if __name__ == "__main__":
    main()
