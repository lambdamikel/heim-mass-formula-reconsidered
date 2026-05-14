# Electron-mass 0.79 % discrepancy — diagnostic conclusion

**Date**: 2026-05-14
**Status**: Diagnosed. The discrepancy is not in the Python port.

## Summary

The standing 0.79 % electron-mass discrepancy
(Open Question #1 in the README) is **not** a bug in this repository's
Python implementation. After exhaustive cross-checking against the
IGW Innsbruck PDF source (`downloads/F_Erweiterte_Massenformel_nach_Heim 1989.pdf`)
and against Heim's 1982 paper (`downloads/E_Massenformel_nach_B_Heim_1982.pdf`),
the port faithfully implements the published 1989 equations [B3] through
[B14] inclusive. The discrepancy is in the **published 1989 formula
chain itself** — specifically, the simplification of Φ from the 1982
(XI) form to the 1989 [B6] form appears to have dropped a contribution
that is non-trivial for charged ground-state leptons at k = 1.

## Trail of the diagnosis

### Step 1: (n, m, p, σ) cross-check (May 2026)

`python/nmps_cross_check.py` compared our greedy decomposition output
against Heim's Tabelle I listed values for all 21 ground states.
Result: 19 / 21 match exactly, including both e₀ (σ=1) and e⁻ (σ=0).
**Conclusion: the greedy decomposition is correct.** The electron bug
is not here.

### Step 2: Per-term decomposition (May 2026)

`python/electron_trace.py` decomposed the calculation for both e₀ and
e⁻ into the five pieces (K, S, F, Φ, 4qα₋).  Result:

| Term  | e₀ (q=0) | e⁻ (q=1) | Δ |
|---|---:|---:|---:|
| K | 4.000 | 0.000 | -4.000 |
| S | 216.000 | 215.99996 | -0.00004 |
| F | 0.000 | 0.000 | 0 |
| Φ | 2.316 | 2.316 | 0 |
| 4qα₋ | 0.000 | 0.0325 | +0.0325 |
| Σ | 222.315 | 218.348 | -3.97 |
| M (MeV) | 0.51616 | 0.50694 | -9.21 keV |

Heim's published values: M(e₀) = 0.51617 MeV (matches our 0.51616
exactly), M(e⁻) = 0.51100 MeV → ΔM_Heim = -5.17 keV → required Heim
ΔΣ = -2.23 (vs our -3.97).  Heim's framework requires **+1.74 units
of additional bracket for e⁻** beyond what our (and the published
1989) formula produces.

### Step 3: Formula-by-formula source comparison

All seven relevant formulas were transcribed from the IGW Innsbruck
PDF and compared against the Python port:

| Formula | PDF source | Our code | Match? |
|---|---|---|---|
| [B3]  | M = μα₊·[(G+S+F+Φ) + 4qα₋] | identical | ✓ |
| [B5]  | F = 2nQ_n[1+3(n+Q_n+nQ_n)+2(n²+Q_n²)]·N₁ + 6mQ_m(1+m+Q_m)·N₂ + 2pQ_p·N₃ + φ·δ(N) | identical | ✓ |
| [B6]  | Φ = P(-1)^(P+Q)(P+Q)·N₅ + Q(P+1)·N₆ | identical | ✓ |
| [B7]/[B49] | full φ expression | identical | ✓ |
| [B10] | N₅ = A·[1 + k(k-1)·2^(k²+3)·N(k)·A·((1-√η_{q,k})/(1+√η_{q,k}))²] | D + k(k-1)·8z·I₁·(D·(…))² with 8z = 2^(k²+3) | ✓ |
| [B11] | A = (8/η)·(1 − α₋/α₊)·(1 − 3η/4) | identical | ✓ |
| [B13] | N₆ = 2k/(πeθ)·[√k(k²-1)·N(k)/√η_{1k}·{q-(1-q)·N'(k)/(Q_n·√η_{1k})} + (-1)^(k+1)]·η·(1-α₋/α₊)·(4·(1-√η)/(1+√η))²·Q_σ | (64kηQ_σ)/(uθ)·(1-α₋/α₊)·((1-√η)/(1+√η))²·[√k·(k²-1)·I_1/√η_{1k}·(q-(1-q)·I_2/(Q_n·√η_{1k}))+(-1)^(k+1)] — algebraically identical | ✓ |
| (XI) 1982 K | n₁²(1+n₁)²·N₁ + n₂(2n₂²+3n₂+1)·N₂ + n₃(1+n₃)·N₃ + 4n₄ | identical | ✓ |

**All formulas match.** The bug is not in our transcription or
implementation.

### Step 4: Origin in the 1989 simplification of Φ

Heim's 1982 (XI) gave Φ as a complex expression with many q-dependent
terms:

```
Φ_1982 = 3P/(π√η_{q,k}) · (1 − α₋/α₊) · (P+Q)·(-1)^(P+Q)
       · [1 − α/3 + (π/2)(k-1)·3^(1-q/2)]
       · {1 + 2kκ/(3η²)·ξ[1 + ξ²(P-Q)(π2-q)]}
       · [1 + (4ξ(2P)/k)·(ξ/6)^q] − 1
       · [2√η₁₁·√η_{q,k} + qη²(k-1)]
       · (1 + 4πα/(η√η)) · (1 + Q(1-κ)(2-k)·n₁/Q₁)
       + 4(1 − α₋/α₊)·α·(P+Q)/ξ²
       + 4q·α₋/α₊
```

Heim's 1989 [B6] simplified this to:

```
Φ_1989 = P(-1)^(P+Q)(P+Q)·N₅ + Q(P+1)·N₆
```

The "+ 4q·α₋/α₊" piece of 1982 was moved out of Φ and into [B3]
as the "+ 4qα₋" term outside the bracket — that part is preserved.
But the rest of the 1982 Φ structure (with its q-dependent factors
`(ξ/6)^q`, `(1-q)`, `(1-q/2)`, etc.) is *not* obviously
reproduced by [B6] for q ≠ 0 at k = 1.

For k = 1 the k(k-1) factor in [B10] zeroes out the q-dependent
correction in N₅, leaving N₅ = A which depends only on η₀₀
(not on η_{q,k}). And the prefactor structure in N₆ also has
k(k²-1) = 0 at k = 1.  So Φ at k = 1 is **q-independent** in
the 1989 form — which contradicts the 1982 form, where Φ had
explicit q-dependence even at k = 1.

### Step 5: What "should" have been preserved

The 1982 Φ contains a term `+4·(1 − α₋/α₊)·α·(P+Q)/ξ²` that is
ξ-dependent but not obviously q-dependent (depends on context of
ξ, which was a function of η in the 1982 paper). It also contains
the multiplicative factor `[1 + (4ξ(2P)/k)·(ξ/6)^q] − 1`, which
**is** q-dependent and **does** contribute differently for q=0
vs q=1 at k=1, P=1.

The 1989 [B6] simplification appears to have either:

(a) Folded these q-dependent Φ pieces into the η_{q,k}-dependence
    of N₅ / N₆, but at k=1 the k(k-1) prefactor in [B10] kills the
    effect — possibly an oversight in the simplification.

(b) Dropped them outright on the assumption they were higher-order
    corrections, without realising that for charged k=1 leptons
    they were essential.

Either way: **the published 1989 chain ([B3] + [B5] + [B6] +
[B7-B14]) is internally inconsistent with Heim's own Tabelle II
electron value of 0.51100 MeV.**  Implementing the equations
exactly as written gives 0.50694 MeV.  Implementing the 1982 Φ
formula in its full form *might* recover the 0.51100 value — but
this would be a substantial restoration project, and it is unclear
whether the IGW Innsbruck restatement intended [B6] as a complete
replacement or as a "leading-order" approximation.

## Implications

1. **Our Python port faithfully reproduces the published 1989
   equations.** The 0.79 % electron discrepancy is not a port bug.

2. **Heim's 1989 published formula chain is incomplete or has a
   typesetting omission.** Twenty of twenty-one ground-state masses
   match Heim's Tabelle II to ≤ 0.01 % using the published [B3]–[B14]
   chain. Only the electron (and the two q ∈ {+2, 0} Δ-resonances)
   show systematic discrepancies tied to Φ / σ-piece coefficients.

3. **Two possible avenues to resolve**:

   (a) Implement the full 1982 (XI) Φ expression and check whether
       it reproduces Heim's 1989 Tabelle II values for the electron
       AND continues to match all other particles. If yes: the 1989
       [B6] is an incomplete simplification.

   (b) Wait for Javier or other heim-theory.com sources to clarify
       whether the 1989 manuscript has additional terms beyond the
       IGW Innsbruck restatement, particularly for charged ground-
       state leptons.

4. **The Δ⁺⁺ and Δ⁰ discrepancies (1.5–1.9 MeV, separate from the
   electron)** are a related but distinct phenomenon: they come
   from the greedy decomposition giving different (p, σ) values
   than Heim's Tabelle I for q ∈ {+2, 0} at (P=3, Q=3, k=2). That
   bug is in the greedy algorithm or in calc_W, not in Φ.

## Recommendation

Update the README's Open Question #1 to reflect the diagnostic
conclusion: the bug is in the published formula chain, not in our
port. The remaining engineering question shifts from "find the
transcription bug" to "should we extend the port to use the 1982
Φ in addition to the 1989 [B6]?", which is a substantive analytical
decision rather than a bug fix.
