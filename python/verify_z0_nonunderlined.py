"""
Re-verification of Heim's z=0 claim, restricted to non-underlined entries.

Per J0032 p.27a, underlined N̄ entries are "single-process" resonances
not satisfying eq. (14d) and not covered by eqs. (14a, 14b).  The
non-underlined N entries are the ones Heim's z=0 approximation
applies to with stated < 0.1 MeV error.

This script filters our existing verification (commit df86c7c) by
underline status from `underline_status.py` and reports the corrected
pass rates.
"""

from __future__ import annotations

import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np

import formulae as fm
from anregung_ab_initio import predict as predict_anregung
from pdg_j_lookup import MESON_PDG_J, BARYON_PDG_J
from resonance_consistency_baryons import implied_w_k2
from resonance_wscan_baryons import expand_to_states
from g_tables import (TABLE_IV_MESONS_K1, TABLE_V_a_BARYONS_K2,
                      TABLE_V_b_BARYONS_K2, TABLE_V_c_BARYONS_K2_SIGMA)
from resonance_z0_classify_k1 import (expand_meson_states,
                                        expand_meson_pub_N,
                                        CACHE as MESON_CACHE)
from underline_status import is_underlined

BARYON_CACHE = Path(__file__).parent / "baryon_candidates_cache.pkl"


def Q_ground(base):
    if base in BARYON_PDG_J:
        return BARYON_PDG_J[base].Q_ground
    if base in MESON_PDG_J:
        return MESON_PDG_J[base].Q_ground
    return None


def main():
    print("=" * 100)
    print(" z=0 verification restricted to NON-UNDERLINED entries")
    print(" (per Heim J0032 p.27a: only non-underlined N's are stepwise z=0)")
    print("=" * 100)
    print()

    # Load caches
    with open(BARYON_CACHE, "rb") as f:
        bary_cands = pickle.load(f)
    with open(MESON_CACHE, "rb") as f:
        mes_cands = pickle.load(f)
    print(f"Baryons: {len(bary_cands)}, Mesons: {len(mes_cands)} candidates")

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

    def evaluate(label, P, qx, M_t, KB_t, N_idx, k, cands):
        base = label.replace("⁻", "").replace("⁰", "").replace("⁺", "").replace("±", "")
        Q0 = Q_ground(base)
        if Q0 is None:
            return None
        I = I_k1 if k == 1 else I_k2
        Nconst = get_Nconst(k, qx)
        cand_list = [c for c in cands.get(label, []) if c["Q"] == Q0]
        if not cand_list:
            return None
        best_c = min(cand_list, key=lambda c: c["dM"])
        nmps = best_c["nmps"]
        dM = best_c["dM"]
        dKB = best_c["dKB"]
        w = implied_w_k2(nmps, I, Nconst, k=k)
        best_df = None
        best_kap = None
        best_finfo = None
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
                best_finfo = (f_imp, f_pred)
        if best_df is None:
            return None
        return {"Q0": Q0, "kap": best_kap, "nmps": nmps, "dM": dM, "dKB": dKB,
                "f_imp": best_finfo[0], "f_pred": best_finfo[1], "df": best_df}

    # Mesons
    meson_pub_N = expand_meson_pub_N()
    meson_states = expand_meson_states()
    print()
    print("=== k=1 mesons (non-underlined only) ===")
    print(f"  {'symbol':<14} {'P':>2} {'qx':>3} {'N':>4} "
          f"{'Q₀':>3} {'κ':>3} {'ΔM':>9} {'ΔKB':>5} {'|Δf|':>9}  verdict")
    print("  " + "-" * 96)

    mes_pass = 0
    mes_fail = 0
    mes_uncovered = 0
    for label, P, qx, M_t, KB_t in meson_states:
        if is_underlined(label):
            continue
        if is_underlined(label) is None:
            mes_uncovered += 1
            continue
        N_idx = meson_pub_N.get(label)
        if N_idx is None:
            continue
        r = evaluate(label, P, qx, M_t, KB_t, N_idx, 1, mes_cands)
        if r is None:
            print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d}  -- no candidate")
            mes_fail += 1
            continue
        passes = (r["dM"] < 0.1 and r["df"] < 0.05)
        verdict = "PASS" if passes else "FAIL"
        print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d} "
              f"{r['Q0']:>3} {r['kap']:>3} "
              f"{r['dM']:>+9.4f} {r['dKB']:>+5.2f} {r['df']:>9.4f}  {verdict}")
        if passes:
            mes_pass += 1
        else:
            mes_fail += 1

    print()
    print(f"  Mesons (non-underlined): {mes_pass} pass / {mes_fail} fail")

    # Baryons
    baryon_pub_N = {}
    for tbl in (TABLE_V_a_BARYONS_K2, TABLE_V_b_BARYONS_K2,
                TABLE_V_c_BARYONS_K2_SIGMA):
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

    print()
    print("=== k=2 baryons (non-underlined only) ===")
    print(f"  {'symbol':<14} {'P':>2} {'qx':>3} {'N':>4} "
          f"{'Q₀':>3} {'κ':>3} {'ΔM':>9} {'ΔKB':>5} {'|Δf|':>9}  verdict")
    print("  " + "-" * 96)

    bary_pass = 0
    bary_fail = 0
    bary_uncovered = 0
    bary_fail_breakdown = defaultdict(int)
    for label, P, qx, M_t, KB_t in baryon_states:
        if is_underlined(label):
            continue
        if is_underlined(label) is None:
            bary_uncovered += 1
            continue
        N_idx = baryon_pub_N.get(label)
        if N_idx is None:
            continue
        r = evaluate(label, P, qx, M_t, KB_t, N_idx, 2, bary_cands)
        if r is None:
            print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d}  -- no candidate")
            bary_fail += 1
            bary_fail_breakdown["no candidate"] += 1
            continue
        passes = (r["dM"] < 0.1 and r["df"] < 0.05)
        verdict = "PASS" if passes else "FAIL"
        print(f"  {label:<14} {P:>2} {qx:>+3d} {N_idx:>4d} "
              f"{r['Q0']:>3} {r['kap']:>3} "
              f"{r['dM']:>+9.4f} {r['dKB']:>+5.2f} {r['df']:>9.4f}  {verdict}")
        if passes:
            bary_pass += 1
        else:
            bary_fail += 1
            if r["dM"] >= 0.1 and r["df"] >= 0.05:
                bary_fail_breakdown["both fail"] += 1
            elif r["dM"] >= 0.1:
                bary_fail_breakdown["ΔM ≥ 0.1"] += 1
            else:
                bary_fail_breakdown["|Δf| ≥ 0.05"] += 1

    print()
    print(f"  Baryons (non-underlined): {bary_pass} pass / {bary_fail} fail")
    print(f"    Fail breakdown: {dict(bary_fail_breakdown)}")

    print()
    print("=" * 100)
    print(" FINAL VERDICT on Heim's z=0 claim (J0032 p.27a, restricted to non-underlined):")
    print("=" * 100)
    total = mes_pass + mes_fail + bary_pass + bary_fail
    total_pass = mes_pass + bary_pass
    print(f"  Pass rate: {total_pass}/{total} = {100*total_pass/total if total else 0:.1f} %")
    print(f"  Mesons:  {mes_pass}/{mes_pass + mes_fail}")
    print(f"  Baryons: {bary_pass}/{bary_pass + bary_fail}")


if __name__ == "__main__":
    main()
