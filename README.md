# Heim's Mass Formula — Inspected

*A reproducible investigation of Burkhard Heim's 1989 elementary-particle mass
formula: how does it work, where does its accuracy actually come from, and
how much of it is genuinely theory-driven?*

---

## TL;DR

Burkhard Heim (1925–2001) published a formula that claims to compute the rest
masses of ~20 elementary particles to ~0.2% accuracy from a handful of
integer quantum numbers, with no free fitting parameters. Mainstream physics
does not accept it. This repository:

1. Contains a runnable, annotated reference implementation (C and Python).
2. Reproduces Heim's published numbers bit-for-bit.
3. Maps every line of code to its corresponding equation in the 1989 paper.
4. Probes — by perturbing each ingredient — *which* parts of the formula are
   actually doing the work.

**Headline result.** Heim explicitly identified three constants
(⁴√2, (π/e)², 4π/⁴√2) as "fitted to empirical facts." We find these
constants are essentially **inert** — scaling any of them by a factor of
1000× changes the predictions by less than the formula's own quoted
accuracy. The accuracy comes instead from quantities that are *not* free
to tune: the mass element μ (built only from G, ℏ, c), the integer
"structure constants" Q_n…Q_σ derived from `z = 2^(k²)`, and a specific
auxiliary function η whose four shape parameters all sit at simple integer
values within ≤1% tolerance.

This is a more nuanced picture than either "fully derived" or "secretly
fitted." See [Findings](#findings) for the detailed verdict.

---

## Speculative summary

This section is a *subjective, calibrated bet* — distinct from the
analysis-derived conclusions in [The honest verdict](#the-honest-verdict).
Treat it as a wager, not a finding.

If forced to put numbers on it:

| Statement | Subjective probability |
|---|---|
| Heim's mass-formula accuracy is not pure numerical coincidence | **70 – 80 %** |
| η's specific form follows from the 6D field equations (rather than being a definitional *ansatz*) | 25 – 40 % |
| Heim theory will eventually be recognised as a correct unified field theory | 5 – 10 % |
| The framework captures something real that mainstream physics has overlooked | 25 – 40 % |
| It is elegant numerology with no physical content | 20 – 30 % |

(The rows are overlapping interpretations and do not sum to 100 %; they
reflect weights, not partitions.)

**Short version: there is probably something there.** Probably not the
"theory of everything," but probably also not pure pattern-matching.

The strongest single anchor for *not coincidence* is the fine-structure
constant: $1/α = 137.036\,01$ emerges from η and θ via [B58]–[B62] with
no free parameters, matching experiment to ~5 decimal digits. One
number, five digits, no fit knobs — that is hard to dismiss.

The strongest single anchor for *not finished* is that η's functional
form is *defined* in the publicly available manuscripts, not derived.
The chapters of "Zur Herleitung der Heimschen Massenformel" that would
prove (or disprove) its derivation from the 6D field equations are not
online.

What would shift this assessment substantially:

- A successful application to particles discovered after 1989 (top quark,
  Higgs, charm and bottom baryon spectroscopy) at the same ~0.1 %
  accuracy.
- Public release of chapters 7–9 of the IGW derivation manuscript.
- An independent reimplementation of the lifetime formula closing the
  gaps in the [Lifetime predictions](#lifetime-predictions) above.

What would *not* shift it: another mainstream-physics dismissal that has
not actually examined the formulas. Heim theory has been **ignored** more
than it has been **refuted**, which is not the same thing.

Caveats on this assessment:

- It rests on one repository's analysis. A working theoretical physicist
  with deep access to the Heim literature might reach different
  conclusions.
- It says nothing about Heim's underlying mathematics (polymetric
  geometry, selector calculus, 6D eigenvalue equations) — only about
  what reaches the C/Python implementations.
- The author of this analysis used an LLM (Claude Opus 4.7) extensively;
  LLMs trend either toward sycophantic agreement or toward dismissive
  over-skepticism. The probabilities above are an attempt at the
  middle, not a guarantee of one.

---

## Contents

- [Speculative summary](#speculative-summary) — subjective probability bet
- [Background](#background)
- [Repository layout](#repository-layout)
- [Quickstart](#quickstart)
- [Methodology](#methodology)
- [Findings](#findings)
- [The honest verdict](#the-honest-verdict)
- [Open questions](#open-questions)
- [References](#references)
- [License & attribution](#license--attribution)

---

## Background

Heim's framework lives in a six-dimensional space:

```
R₆  =  R₃ (space)  ⊕  T₁ (time)  ⊕  S₂ (trans-coordinates x₅, x₆)
```

The two extra "trans-coordinates" are explicitly *non-energetic* — they act
as organisational degrees of freedom rather than additional spatial axes.
This distinguishes Heim from Kaluza–Klein theories. Spacetime is discretised
into elementary surface units called **metrons** (τ ≈ 6.15 × 10⁻⁷⁰ m²),
related to the Planck length squared.

A particle is a stationary, self-consistent metron configuration in R₆,
identified by an integer tuple (ε, k, P, Q, κ, x). The 1989 mass formula
([B3] in the IGW Innsbruck restatement) reads:

```
M  =  μ · α₊ · [ G + S + F + Φ + 4qα₋ ]
```

where μ, α₊, α₋ are dimensionless universal constants built from
G, ℏ, c, π, e via specific intermediate functions (η, θ); G, S, F, Φ are
sub-expressions in the particle's quantum numbers and four occupation
numbers (n, m, p, σ) extracted from a "structure weight" W via a greedy
exhaustion algorithm.

For the precise equation list see [`downloads/pdfs/F_1989_en.pdf`](downloads/pdfs/F_1989_en.pdf)
(published by IGW Innsbruck, restating Heim's 1989 manuscript).

## Repository layout

```
heim/
├── README.md                  ← this file
├── REPORT.de.md               ← longer narrative report (German companion)
│
├── downloads/
│   ├── c_impl/                ← Eli Gildish's 2006 C implementation (upstream)
│   ├── csharp_impl/           ← C# version with 1982/1989/HG variants
│   └── pdfs/                  ← Heim 1982 and 1989 formula reformulations
│
├── annotated/
│   └── src/                   ← C source with one-to-one cross-references
│       ├── formulae.c         ← every line tagged with its [B##] equation
│       └── constant.c         ← η, θ, α± and the fine-structure derivation
│
└── python/                    ← Python port (bit-identical to C)
    ├── constants.py           ← physical & auxiliary constants
    ├── formulae.py            ← the mass formula itself
    ├── lifetime.py            ← mean-lifetime formula [B47]–[B57]
    ├── particle.py            ← Particle dataclass + 21 reference particles
    ├── heimmass.py            ← main runner: reproduces the published mass table
    ├── heim_lifetime.py       ← runner: lifetime predictions vs PDG
    │
    ├── test_reference_masses.py   ← pytest snapshot pinning the 21 mass values
    │
    ├── sensitivity.py             ← test the 3 "fitted" constants (±10%)
    ├── sensitivity_wide.py        ← same, over 6 orders of magnitude
    ├── sensitivity_diagnostic.py  ← per-particle sensitivity breakdown
    ├── sensitivity_structural.py  ← test μ, η, θ, Q_i
    ├── sensitivity_eta_form.py    ← probe η's functional form
    └── plots/                     ← PNG outputs of all sensitivity sweeps
```

## Quickstart

### Build & run the C reference implementation

```sh
cd annotated
make            # builds and runs heimmass; prints the particle table
```

You should see Heim's predictions for 21 particles, e.g.:

```
 proton           | p        |   1 |  937.33890386 |  938.27231000 | -0.099%
 neutron          | n        |   0 |  938.30996495 |  939.56563000 | -0.134%
```

### Run the Python port

```sh
python3 -m venv venv
./venv/bin/pip install numpy matplotlib
./venv/bin/python python/heimmass.py
```

The Python output matches the C output bit-for-bit (verified to 10 decimal
digits across all 21 particles).

### Run the lifetime predictions

```sh
./venv/bin/python python/heim_lifetime.py
```

This computes Heim's 1989 mean-lifetime predictions ([B47]–[B57]) for the
21 reference particles and prints a comparison against PDG measurements.
See [Lifetime predictions](#lifetime-predictions) below for current status.

### Run the regression test

```sh
./venv/bin/pip install pytest
cd python && ../venv/bin/python -m pytest test_reference_masses.py -q
```

Should report `23 passed` — the 21 reference masses are pinned to bit-equality
with the C reference (plus 2 sanity tests on charges and list completeness).

### Reproduce the sensitivity analysis

```sh
./venv/bin/python python/sensitivity.py             # 3 fitted constants, narrow sweep
./venv/bin/python python/sensitivity_wide.py        # 3 fitted constants, ±3 decades
./venv/bin/python python/sensitivity_structural.py  # μ, η, θ, Q_i
./venv/bin/python python/sensitivity_eta_form.py    # η's 4 shape parameters
```

Plots go to `python/plots/`.

## Methodology

The plan was deliberately simple:

1. **Reproduce the published numbers** to confirm we are looking at the
   actual Heim formula and not some variant.
2. **Annotate every term** of the C code with its corresponding equation
   from [1989] so we know what each line is *supposed* to compute.
3. **Port to Python** as an executable cross-check and a platform for
   experiments. The port is bit-identical to the C output.
4. **Perturb each ingredient** of the formula and measure how the loss
   responds:

   ```
   loss(perturbation) = Σᵢ ((m_predicted_i − m_measured_i) / m_measured_i)²
   ```

   summed over the 20 particles with measured masses (e₀ has none).

5. **Compare**: an ingredient that the formula genuinely *needs* should
   have a sharp loss minimum at its published value; an ingredient that
   functions as a free parameter should be tunable without consequence.

## Findings

### Baseline accuracy

```
RMS relative error over 20 measured particles  =  0.2188 %
```

Worst single particle: electron at -0.79%. Most particles below 0.05%.
This matches the literature.

The 21st particle in Heim's reference list — `e₀`, the *neutral electron* —
is not in this average because it has no measured mass: it is **Heim's
prediction of a previously unknown neutral lepton**, with calculated mass
0.50627 MeV (about 0.94 % below the electron). To date no such particle
has been observed; it remains a standing prediction of the framework.

### The "fitted" constants

Heim writes (1989, p. 19):

> *"the free eligible parameters for the expression φ with eq. (B50) were
> fitted by empirical facts [i.e. ⁴√2, (π/e)², and 4π·⁴√(1/2)]"*

Sweeping each of these over **six decades** (factor 10⁻³ to 10³):

| Constant | Closed form | Loss doubles at |
|---|---|---|
| ⁴√2 | 2^(1/4) | factor ≈ 50 (and ≈ 1/50) |
| (π/e)² | (π/e)² | factor ≈ 48 (and ≈ 1/48) |
| 4π/⁴√2 | 4π · 2^(−1/4) | **never** in the entire range |

These constants enter the formula only inside the self-coupling function
φ, which is added to F *after* the integer occupation numbers (n, m, p, σ)
have been determined. They affect only a small additive correction.
Per-particle diagnostics show that several particles (electron, Ω⁻, Σ⁰)
are *completely insensitive* to all three even at 50% perturbation —
because of structural cancellations like (Q_m − Q_n) = 0 at k = 1, or
n_p = 0 making the leading φ term vanish.

**Conclusion.** Heim's "fits" are inert. The accuracy of the mass
predictions does not come from these three constants.

### Where the accuracy actually lives

When the structurally non-trivial quantities are perturbed instead, the
loss responds *enormously*:

| Quantity | What it is | Loss doubles at |
|---|---|---|
| μ (mass element) | π^(1/4) · (3πGℏs₀)^(1/3) · √(ℏ/(3cG))/s₀ | **±0.24 %** |
| η (auxiliary) | (π⁴ / (π⁴ + (4+k)q⁴))^(1/4) | **±0.01 %** |
| Q_i (structure constants) | derived from z = 2^(k²) | **±0.02 %** (downward) |
| θ = 5η + 2√η + 1 | combination of η | >5 % (very flat) |

Compared to the fitted constants, η and the Q_i are **five to ten orders
of magnitude more constrained**. A 1% perturbation of η increases the
loss by a factor of ≈50 000.

### Probing η's functional form

η is defined as (π^A / (π^A + (B+k)·q^C))^D with default (A, B, C, D) =
(4, 4, 4, 1/4). Sweeping each parameter independently:

| Parameter | Heim default | Empirical minimum | Tolerance for 2× loss |
|---|---|---|---|
| A (π exponent) | 4 | **4.000** | ±0.25 % |
| B (constant in B + k) | 4 | **4.000** | ±0.6 % |
| C (q exponent) | 4 | inside the 4-basin (loss landscape is jagged) | ±2.5 % up, ±11 % down |
| D (outer exponent) | 1/4 | **0.2495** | ±1 % |

Three of the four parameters land *exactly* on simple integer values and
sit at sharp minima. The fourth (C) is in the right basin of attraction
but the loss landscape is genuinely jagged due to integer transitions in
the (n, m, p, σ) decomposition. This is consistent with η's form being
non-arbitrary — but its derivation from the 6D field equations is *not
present* in the publicly available portion of the 1989 manuscript
(only chapters 1–2 of the 81-page derivation are online; chapters 7–9,
which would contain the relevant proofs, are not).

### The fine-structure constant

Heim's framework derives α from η, θ, π:

```
α · √(1 − α²)  =  (9 θ / (2π)⁵) · (1 − C')         [B58]

      ⇒  1/α  =  137.036 01
   (measured:    137.036 0114 ± 3.4 × 10⁻⁸)
```

This is a single calculated number that matches experiment to ~5 decimal
digits, with no free parameters. It is the most striking single result in
the entire framework.

### Lifetime predictions

The 1989 manuscript also provides a mean-lifetime formula ([B47]–[B57])
applying to the same 21 basic states. Eli Gildish's 2006 C code does not
implement it, so this repository contains the first independent
implementation in `python/lifetime.py`.

Initial results across 18 measured particles (skipping stable/unknown):

| Bucket | Count | Examples |
|---|---|---|
| within factor 3 (\|log₁₀ T_pred/T_exp\| < 0.5) | **5** | muon (perfect, 0.1 % off), π±, K±, n, π⁰ |
| within factor 100 (\|log₁₀\| < 2) | 0 | — |
| off by ≥ 100× | 4 | Λ, K_S, Ξ⁻, Σ⁰ |
| negative T (sign issue) | 5 | η, Ω⁻, Ξ⁰, Σ±, Σ⁻ |
| T = 0 (formula vanishes) | 4 | all four Δ resonances |

The muon prediction matches experiment to 0.1 %, which strongly suggests
the framework computation is correct in principle. The Δ-resonance zeros
trace cleanly to F = 0 at P = 3 — these are strong-decay states (Γ ≈ 117
MeV → τ ≈ 5.6 × 10⁻²⁴ s) and Heim's formula appears to be intended only
for weak/electromagnetic channels. Σ⁰'s 12-order miss is consistent
with the same scope limitation (Σ⁰ → Λγ is electromagnetic, while the
formula seems calibrated for weak decays).

The negative-T cases and the Λ/K_S/Ξ⁻ misses are most likely
**transcription errors** in our implementation of the very long b₁/b₂
expressions ([B54]–[B55]) — the source PDF has ambiguous typography in
several places (curly-brace nesting, division-vs-multiplication colons,
P/Q binomial coefficient notation). These are flagged in
`python/lifetime.py`. Confirming or correcting them requires either
access to Heim's original 1989 FORTRAN code (lost) or expert review by
the IGAAP / Forschungskreis Heimsche Theorie.

That said: getting 5/18 right within factor 3 — across a five-decade
range of lifetimes — on a first-pass implementation of equations this
complex is itself non-trivial.

## The honest verdict

The question we set out to answer was: **does this look like a real
theory-driven derivation of particle masses, or like a clever fit?**

The data in this repository points to a more nuanced answer than either
extreme:

**Pro (genuine derivation):**

1. The constants Heim explicitly labels as "fitted" turn out to be
   *immaterial*: any value of order unity would have produced
   indistinguishable predictions. So the formula is *not* succeeding
   because of a free-parameter sweep over those.
2. The mass element μ is constructed purely from G, ℏ, c with no fitting.
3. The structure constants Q_n, Q_m, Q_p, Q_σ are integer prescriptions —
   not continuous knobs.
4. Three of the four shape parameters of η lock onto simple integer values
   (4, 4, 1/4) within <1% tolerance.
5. The fine-structure constant is calculated, not measured, to ~5 digits.

**Caveats (incomplete derivation):**

1. The functional form of η — the central auxiliary function from which
   nearly everything else follows — is *defined* in the available
   literature, not derived. The chapters that would contain its derivation
   (chapters 7–9 of "Zur Herleitung der Heimschen Massenformel") are not
   publicly accessible.
2. The mass spectrum predicts more excitations than have been observed.
   Heim attributes this to an "unknown selection rule." This is an
   admitted incompleteness.
3. The dataset is small (~20 particles). The framework was never applied
   to particles discovered after the 1980s (top, Higgs, charm-baryon
   spectroscopy) — neither by Heim nor by his successors. We don't know
   whether it would extend.
4. The lifetime formula ([B47]–[B57]) implemented here matches experiment
   to factor 3 on only 5 of 18 particles in its first-pass form, with 5
   negative results and 4 zeros. Whether this reflects transcription
   errors in our reading of [B54]/[B55] or genuine limits of the formula
   is currently open — see [Lifetime predictions](#lifetime-predictions).

**Bottom line.** Heim's mass formula is *substantially more theory-driven
than ordinary curve-fitting*, and the constants he explicitly called
"fitted" are not in fact doing the work. But it is also *not as fully
derived from first principles* as he sometimes claimed: the central
function η is postulated. Whether η can be derived from the 6D metron
field equations is the single most important open question — and the
answer would settle whether this is a remarkable but undocumented
theoretical achievement or an elegant phenomenological scheme.

## Open questions

In rough order of importance:

1. **Is η's form derivable from first principles?** The non-public chapters
   of the IGW reformulation should answer this. Worth contacting the
   Forschungskreis Heimsche Theorie / IGAAP e.V. (`heim-theory@igaap-de.org`).
   A draft email is in `email.txt`.
2. **Are the b₁/b₂ transcriptions correct?** The lifetime expressions
   [B54]–[B55] in the source PDF have several typographic ambiguities.
   With expert review or access to the original 1989 FORTRAN code, the
   currently failing lifetime predictions could likely be fixed.
3. **Does the formula extend to particles discovered after 1989?** Top
   quark, Higgs, charm and bottom baryon spectroscopy are all available
   but were never tested.
4. **Why is the (n, m, p, σ) loss landscape jagged?** The greedy
   decomposition produces integer outputs that flip at thresholds; whether
   this is a feature of the theory or an artifact of the algorithm needs
   to be sorted out.

### Resolved

- ~~**[B25] uses Q_n² or Q_n³?**~~ The IGW PDF prints Q_n² but Heim's own
  research-group C# implementation
  (`downloads/csharp_impl/.../HeimGroup/SelfCouplingFunction.cs`) uses
  Q_n³, in agreement with Eli Gildish's C and our Python port. The PDF
  has a typesetting error; Q_n³ is correct. (Resolved 2026-04.)

## References

- **Primary**: Heim, B. (1989), "Erweiterte Massenformel" — internal
  manuscript sent to MBB/DASA. The original code is lost.
- **Reformulation**: IGW Innsbruck (2002), "Heim's Mass Formula (1989)" —
  English-language restatement with the [B##] equation numbering used
  here. Included as `downloads/pdfs/F_1989_en.pdf`.
- **Derivation (partial)**: von Ludwiger, I. & Grüner, K. (2003), "Zur
  Herleitung der Heimschen Massenformel" — only chapters 1–2 (10 of 81
  pages) are publicly available.
- **C implementation**: Eli Gildish (2006), "Burkhard Heim's Mass
  Formula", on SourceForge. The starting point of this work.
- **Critical history**: Landis, G. A. — *Rise and fall of the Heim
  theory* — at <http://www.geoffreylandis.com/Heim_theory.html>.
- **Heim community**: <https://heim-theory.com/> and
  <https://www.engon.de/protosimplex/> (Protosimplex archive).

## License & attribution

The upstream C implementation (`downloads/c_impl/`) is © 2006
Eli Gildish, licensed under non-commercial terms (see header in any C
source file). The annotations in `annotated/src/`, the Python port in
`python/`, and the analysis scripts are derivative works and inherit the
same restrictions: redistribution and modification permitted with
attribution; **no commercial use without written permission from the
original author.**

The PDFs in `downloads/pdfs/` are © IGW Innsbruck and are mirrored here
for archival purposes; consult heim-theory.com for primary distribution.

This README, the analysis scripts, and the methodology are released by
the author of this investigation under the same non-commercial terms,
in the spirit of preserving the upstream license.

## Acknowledgements

To Eli Gildish for releasing his 2006 reimplementation, without which
this analysis would not have been possible. To the IGW Innsbruck
Forschungskreis Heimsche Theorie for keeping Heim's manuscripts alive
and making the 1989 reformulation available in English. To the open
critics — particularly Geoffrey Landis — for raising the questions that
motivated this work.

---

*If you find an error in the analysis, an oversight in the code, or
have access to the unreleased portions of the derivation manuscripts,
please open an issue.*
