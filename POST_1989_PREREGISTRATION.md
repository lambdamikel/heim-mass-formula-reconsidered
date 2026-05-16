# Pre-registered test: Heim 1989 vs. post-1989 particle physics

**Written before the scan was run. Acceptance / falsification thresholds
are set here and not modified afterwards.**

Date written: 2026-05-16

## Question

Heim's 1989 framework predicts every elementary particle mass as a tuple
of small integers (k, P, Q, κ, q, eps, x) plus the resonance excitation
indices (n, m, p, σ). If the framework is *substantively* describing
real mass quantisation, then particles discovered after 1989 (or known
but not in Heim's published 21-particle / 168-resonance tables) should
also fit naturally into Heim's integer scheme — at the *right* quantum
numbers, not just "some slot somewhere".

If they don't, the framework is shown to be a 1989-snapshot result that
does not extrapolate, which is much weaker evidence for it being real
physics.

## Targets

We compile a target list from PDG. Each target gets independent assigned
quantum numbers (P = 2·isospin, Q = 2·spin, q = charge in units of e)
based on the experimental PDG values *before* the scan is run.

### Tier 1 — should have been known to Heim (pre-1989 discoveries)

These particles existed and had measured masses by 1989. If Heim's
framework had been complete, he *could* have included them. Failure
to slot them is strong evidence that the published scheme is
incomplete.

  | Particle    | Mass (MeV)  | J (spin) | I (isospin) | q | Discovery |
  |-------------|------------:|---------:|------------:|--:|----------:|
  | τ (tau)     |     1776.86 | 1/2      | 1/2         | ±1| 1975      |
  | J/ψ         |     3096.90 | 1        | 0           | 0 | 1974      |
  | ψ(2S)       |     3686.10 | 1        | 0           | 0 | 1974      |
  | Υ (1S)      |     9460.30 | 1        | 0           | 0 | 1977      |
  | D⁰          |     1864.84 | 0        | 1/2         | 0 | 1976      |
  | D±          |     1869.66 | 0        | 1/2         |±1 | 1976      |
  | D_s±        |     1968.35 | 0        | 0           |±1 | 1983      |
  | B⁰/B±       |     5279.4  | 0        | 1/2         | 0/±1 | 1983 |
  | W±          |    80369    | 1        | 0 (weak)    |±1 | 1983      |
  | Z⁰          |    91188    | 1        | 0 (weak)    | 0 | 1983      |
  | Λ_c⁺        |     2286.5  | 1/2      | 0           |±1 | 1976      |

### Tier 2 — post-1989 discoveries

Heim could not have known these masses. They are clean extrapolations.

  | Particle    | Mass (MeV)  | J     | I    | q | Discovery |
  |-------------|------------:|------:|-----:|--:|----------:|
  | t (top)     |   172570    | 1/2   | 1/2  |±2/3| 1995     |
  | H⁰ (Higgs)  |   125250    | 0     | 0    | 0  | 2012     |
  | B_s         |     5366.93 | 0     | 0    | 0  | 1992     |
  | B_c         |     6274.47 | 0     | 0    |±1  | 1998     |
  | Σ_c         |     2453.97 | 1/2   | 1    | 0  | 1990s    |
  | Ξ_c         |     2467.71 | 1/2   | 1/2  | 0/±1| 1980s/90s |
  | Λ_b         |     5619.60 | 1/2   | 0    | 0  | 1992     |
  | Σ_b         |     5810.56 | 1/2   | 1    |±1  | 2007     |
  | Ω_b         |     6045.20 | 1/2   | 0    |±1  | 2008     |

We treat heavy quarks (c at 1.27 GeV, b at 4.18 GeV, t at 172.6 GeV) as
constituent-mass targets rather than free-particle targets — Heim's
framework describes *observable* particles, and free quarks are not
observable. They are NOT counted in the main tally; just noted for
reference.

## Scan procedure (pre-registered)

For each target (target_mass, q, J, I):

1. **Quantum number assignment**: P_target = round(2·I), Q_target = round(2·J).

2. **Sector scan**: enumerate every (eps, k, P, Q, kap, x) with
     - eps ∈ {+1, −1}
     - k ∈ {1, 2}
     - P ∈ {0, 1, …, 6}
     - Q ∈ {0, 1, …, 6}
     - κ ∈ {0, 1}
     - x ∈ {0, 1, …, 8}
     - charge q produced by calc_charge equals target q
     - **(P, Q) == (P_target, Q_target)** ← strict quantum-number match required
     - mass formula returns a finite positive value

3. **Resonance enumeration** within each matching sector:
     - for each ground state, enumerate (n, m, p, σ) tuples satisfying
       Heim's exhaustion condition (J0032 eq. 16) up to N ≤ 25
     - compute mass for each tuple
     - keep best match to target_mass

4. **Match outcome** per target:
     - **strict match**:   |Δm/m| ≤ 1 %, at correct (P, Q)
     - **moderate match**: |Δm/m| ≤ 3 %, at correct (P, Q)
     - **relaxed match**:  |Δm/m| ≤ 10 %, at correct (P, Q)
     - **wrong-QN match**: best mass match within 10 %, but wrong (P, Q)
     - **no match**:       nothing within 10 %

## Background / chance-rate estimate (pre-registered)

To avoid declaring victory just because there are many Heim states per
mass decade, we estimate the chance-hit rate:

  - Generate 50 *random* target masses uniformly in log-space over
    [100 MeV, 200 GeV], with random (P, Q) drawn from the same
    distribution as the real targets.
  - Run the identical scan procedure (steps 1–4) on each.
  - Compute the per-target chance-hit rate at each match tier.

Signal rate is "interesting" only if it exceeds background by ≥ 2×.

## Acceptance / falsification criteria (pre-registered)

We classify the overall outcome into one of four buckets, decided
*before* the scan runs:

  **STRONG CONFIRMATION** (Heim extends beyond 1989):
    - ≥ 6 of 11 Tier-1 targets match at strict (≤ 1 %) with correct
      (P, Q), AND background strict-match rate ≤ 25 % of signal rate.

  **MODERATE CONFIRMATION** (Heim partially extends):
    - ≥ 4 of 11 Tier-1 targets at moderate (≤ 3 %) with correct (P, Q),
      AND signal/background ratio ≥ 2× at moderate tier.

  **NULL RESULT** (framework is 1989-bounded):
    - < 4 of 11 Tier-1 at moderate, OR signal/background ratio < 2× at
      moderate tier.

  **FALSIFICATION** (worse than chance):
    - Signal rate ≤ background rate at moderate tier on Tier-1 sample.

For Tier 2 (truly post-1989) we report results but do not assign
acceptance buckets to them — these are exploratory.

## What this test cannot do

  - It cannot test particles whose quantum numbers don't fit Heim's
    convention (top, Higgs at "weak isospin" rather than strong).
    Their results are reported for record but not used in scoring.
  - It cannot account for an unknown selection rule (Heim's
    "Auswahlregel"); a missing match could mean either "the framework
    doesn't predict this" or "the framework predicts but the rule
    forbids this state".
  - It cannot distinguish between "wrong framework" and "wrong (n, m,
    p, σ) enumeration bound" if N=25 is too small.

## Pre-registration commitment

  - Acceptance criteria above will not be modified after the scan runs.
  - All Tier-1 targets in the list above will be reported.
  - Background scan size (50 random) is fixed.
  - The script `python/post_1989_test.py` will be committed and run;
    output captured to `python/post_1989_test_results.txt`.
  - If a particle slips through with a fishy fit (e.g. only with
    extreme (n, m, p, σ) values), it will be flagged, not silently
    counted.
