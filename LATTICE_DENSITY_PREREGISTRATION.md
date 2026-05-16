# Pre-registered test: Lattice density at Heim's 21 ground-state mass points

**Written before the scan was run.**  Date: 2026-05-16.

## Question

The pre-registered post-1989 slot-density test (`POST_1989_PREREGISTRATION.md`,
falsified at moderate tier, see `python/post_1989_test_results.txt`)
showed that Heim's integer lattice is dense enough at the **~1 %**
precision tier that random masses with random (P, Q, q) find slots
56 % of the time.

The post-1989 result re-framed *PDG agreement at 0.01–1 %* as
ambiguous evidence.  But it did not directly address Heim's
**intra-Tabelle II ≤ 2 eV reproduction** — that's a vastly tighter
precision tier (≈ 2 ppb of a proton mass, six orders of magnitude
finer than the post-1989 1 % threshold).

The question now: **at what precision tier is Heim's lattice still
sparse enough that the chosen tuple is uniquely close?**

If the lattice is sparse at 2 eV (only Heim's tuple lands within
2 eV of his target), then the intra-table reproduction is structural
— the algorithm uniquely picks the right tuple given the quantum
numbers.

If the lattice is dense even at 2 eV (many tuples cluster within
2 eV), then even the intra-table consistency is slot-density-aided.

A side question: what is the lattice density at the 1 % PDG-precision
tier (~10 keV to ~10 MeV for typical particles)?  This sharpens the
post-1989 finding from "≥ 50 % chance hits" to a quantitative
density profile.

## Method (pre-registered)

For each of Heim's 19 well-behaved ground states (the two Δ outliers
o⁺⁺ and o⁰ are excluded because their Tabelle I ↔ II self-inconsistency
makes "Heim's chosen tuple" ambiguous — see Open Q 1b):

  1. Compute Heim's target mass `M_target` from his published Tabelle II
     value (8-decimal MeV).
  2. Enumerate ALL (n, m, p, σ) tuples in the sector
     (ε, k, P, Q, κ, q) with `K_n ≤ 60, K_m ≤ 70, K_p ≤ 70, K_σ ≤ 40`
     (same limits as `resonance_wscan_baryons.py` and
     `post_1989_test.py`).
  3. For each tuple, compute predicted mass.
  4. Sort by `|M_pred − M_target|`.
  5. Record:
     - rank-1 distance (this should be Heim's tuple, ≤ 2 eV)
     - rank-2 distance (the next-closest alternative tuple)
     - count of tuples within each of these precision tiers:
         `{2 eV, 100 eV, 1 keV, 10 keV, 100 keV, 1 MeV, 10 MeV}`

## Acceptance criteria (pre-registered)

For each tier T, compute the *median* tuple-count-within-T across the
19 particles.  This gives a profile: at what precision the lattice
transitions from sparse (median 1, only Heim's tuple) to dense
(median ≫ 1, many alternatives).

**Pre-registered interpretation rules**:

- **Tier "intra-Heim verified structural"**: lattice is *sparse* at this
  precision (median count ≤ 2) — Heim's tuple is essentially the unique
  close match.
- **Tier "lattice contributes"**: lattice is *moderately dense* (median
  count 3–10) — Heim's chosen tuple is one of a small finite set.
- **Tier "lattice dominates"**: lattice is *dense* (median count ≥ 10)
  — the apparent reproduction at this precision is largely a lattice
  density effect.

The verdict for the "intra-Heim ≤ 2 eV match is structural" claim is
classified by which tier hits "lattice dominates":

  - If "lattice dominates" hit at ≤ 2 eV:
      **intra-Heim consistency is also slot-density**
      — the strong-anchor status of "Tabelle II at ≤ 2 eV" collapses.
  - If "lattice dominates" hit between 2 eV and 1 MeV (typical PDG range):
      **intra-Heim consistency is structural, PDG agreement is slot-density**
      — confirms the post-1989 finding and preserves the intra-Heim anchor.
  - If "lattice dominates" hit above 1 MeV only:
      **even PDG agreement is more structural than the post-1989 test suggested**
      — surprising; would require re-examination of the post-1989 protocol
      (most likely the post-1989 result is dominated by very-low-Q wide
      sectors that don't represent typical ground-state sectors).

## Pre-registration commitment

- The tier definitions above are fixed.
- All 19 particles will be reported (no cherry-picking).
- K-limits match `post_1989_test.py` and `resonance_wscan_baryons.py`.
- Script `python/lattice_density_check.py` and raw output
  `python/lattice_density_results.txt` will be committed together.
- Interpretation rules above are not modified after the run.
