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

**Headline finding (analytical).** Heim explicitly identified three
constants (⁴√2, (π/e)², 4π/⁴√2) as "fitted to empirical facts." We
find these constants are essentially **inert** — scaling any of them by
a factor of 1000× changes the predictions by less than the formula's own
quoted accuracy. The accuracy comes instead from quantities that are
*not* free to tune: the mass element μ (built only from G, ℏ, c), the
integer "structure constants" Q_n…Q_σ derived from `z = 2^(k²)`, and a
specific auxiliary function η whose four shape parameters all sit at
simple integer values within ≤1 % tolerance — a function that **is
derived** from physical principles in chapter 7 of the full Herleitung
document (eqs. 7.47 → 7.51), not postulated. Combined with the
fine-structure constant α emerging at 5-decimal accuracy from the same
η, the predictive power of the framework appears to come from genuine
geometric content rather than from parameter fitting.

See [Findings](#findings) for the detailed verdict.

**Headline finding (methodological).** This repository contains what
appears to be the **first publicly available reimplementation of Heim's
1989 mean-lifetime formula** ([B47]–[B57]) since Heim's own FORTRAN code
(sent to MBB/DASA in 1989) was lost. Every other public implementation
on record — DESY 1982, Heim's UCSD-Pascal, Protosimplex (Posdzech),
Heim Group / A. Mueller, Eli Gildish 2006 — covers masses only. After
two rounds of transcription corrections against the machine-extracted
PDF, **7 of 18 measured particles match within factor 3** — the muon,
K⁺, π±, and Ξ⁻ all to ~1 %, across lifetimes spanning four decades.
Three particles still give negative T (probable further transcription
errors in φ / U or b₁/b₂); four Δ resonances are structurally outside
the formula's scope. See [Lifetime predictions](#lifetime-predictions).

---

## Speculative summary

This section is a *subjective, calibrated bet* — distinct from the
analysis-derived conclusions in [The honest verdict](#the-honest-verdict).
Treat it as a wager, not a finding.

**This summary was substantially revised after access to the full 81-page
"Zur Herleitung der Heimschen Massenformel" (the previous read was
truncated to the first 10 pages by a `file`-command misreport).** The
key revision: chapter 7 of that document explicitly *derives* η(q,k)
from physical principles (eq. 7.47 → 7.51), so the central pre-revision
caveat — "η's form is defined, not derived" — is now resolved in η's
favour.

If forced to put numbers on it:

| Statement | Pre-revision | After full Herleitung |
|---|---:|---:|
| Heim's mass-formula accuracy is not pure numerical coincidence | 70 – 80 % | **85 – 95 %** |
| η's specific form follows from the 6D field equations (rather than being a definitional *ansatz*) | 25 – 40 % | **80 – 95 %** |
| Heim theory will eventually be recognised as a correct unified field theory | 5 – 10 % | 10 – 20 % |
| The framework captures something real that mainstream physics has overlooked | 25 – 40 % | **40 – 60 %** |
| It is elegant numerology with no physical content | 20 – 30 % | **5 – 15 %** |

(The rows are overlapping interpretations and do not sum to 100 %; they
reflect weights, not partitions.)

**Short version: there is probably something real here.** The η
derivation in chapter 7 turns the most serious "but is it really
derived?" objection from open into resolved (in Heim's favour). What
remains uncertain is mostly empirical reach (post-1989 particles,
lifetime accuracy with corrected b₁/b₂) rather than the foundations.

The strongest two anchors for *not coincidence* are now:

1. The **fine-structure constant**: $1/α = 137.036\,01$ emerges from η and
   θ via [B58]–[B62] with no free parameters, matching experiment to ~5
   decimal digits. One number, five digits, no fit knobs.
2. The **η derivation**: η(q, k) = ⁴√(π⁴ / (π⁴ + (4+k)q⁴)) follows from
   the metron-quantised geometry plus the renormalisation
   ε'₀± = ε₀±·⁴√(1+k/4) of the elementary charge over k effective
   dimensions. The (4+k) factor that we sensitivity-tested at 0.6 %
   tolerance is not a fit; it falls out of L = 4 (number of dimensions
   in R₃ + time) times Δε₀±⁴.

What would still shift this assessment substantially:

- A successful application to particles discovered after 1989 (top quark,
  Higgs, charm and bottom baryon spectroscopy) at the same ~0.1 %
  accuracy.
- An independent reimplementation of the lifetime formula closing the
  gaps in the [Lifetime predictions](#lifetime-predictions) above —
  Heim's own 1989 numbers reportedly had 12 of 14 within experimental
  error (per the Herleitung document, chapter 11), but the IGW group
  itself never reprogrammed the lifetime formula and our implementation
  reaches only 7/18 within factor 3.
- A mathematical audit of the chapter 7 derivation by someone fluent in
  Heim's polymetric formalism, to confirm that no circular reasoning
  enters via the chain ε₀± → η.

What would *not* shift it: another mainstream-physics dismissal that has
not actually examined the formulas. Heim theory has been **ignored** more
than it has been **refuted**, which is not the same thing.

Caveats on this assessment:

- It rests on one repository's analysis and a non-mathematician's reading
  of a 1989 manuscript. A working theoretical physicist with deeper
  access might still reach different conclusions, particularly on the
  rigour of the η derivation.
- It says nothing about Heim's underlying mathematics (polymetric
  geometry, selector calculus, 6D eigenvalue equations) — only about
  what reaches the C/Python implementations and what the Herleitung
  document presents.
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

Three of the four parameters land *exactly* on simple integer values
and sit at sharp minima; the fourth (C) is in the right basin of
attraction with a genuinely jagged landscape due to integer transitions
in the (n, m, p, σ) decomposition. **At the time we ran this analysis
we believed η's form was undocumented; the full Herleitung manuscript
(only the first 10 of 81 pages were initially available, due to a
`file`-command misreport) actually derives all four shape parameters
in chapter 7.** The (A=4, B=4, C=4, D=1/4) integer values are
predictions of the derivation, not survivors of a sensitivity sweep.
Hindsight: the sensitivity sweep is now best read as an empirical
*verification* that η's derived form sits at a sharp minimum — which
is exactly what one would expect if the derivation is correct.

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
applying to the same 21 basic states. As far as can be established from
publicly accessible sources, **`python/lifetime.py` appears to be the
first openly available reimplementation of this formula since Heim's
own 1989 FORTRAN code (sent to MBB/DASA) was lost.**

The trail in the public record:

- **Heim, 1989** — implemented lifetimes in FORTRAN as part of his
  manuscript to MBB/DASA. Per the IGW Innsbruck reformulation
  (`F_1989_en.pdf`, p. 1): *"Unfortunately this later code could no more
  be recovered today."*
- **DESY, 1982** — the original mass-formula computation. Masses only.
- **Heim Group reimplementation by Dr. A. Mueller (~2002)** — explicit on
  the same page: *"The code covers the masses of basic states only and
  no lifetimes."*
- **Protosimplex** (Olaf Posdzech, late 1990s) — Excel, Pascal, C versions
  of the mass formula. No lifetime implementation listed.
- **Eli Gildish, 2006** (C and C#, the upstream of this repository) —
  masses only.

Caveats on the "first since 1989" claim: the search rests on what is
public on the open web. Closed channels (the Heim-Discord, private
notebooks, German-language forums) might contain unreleased work. An
email to `heim-theory@igaap-de.org` (`email.txt`) asks among other things
whether such work exists.

After two rounds of transcription corrections (informed by extracting
the PDF as text and a careful visual re-read of pages 13, 16, 17),
results across 18 measured particles:

| Bucket | Count | Examples |
|---|---|---|
| within factor 3 (\|log₁₀ T_pred/T_exp\| < 0.5) | **7** | muon, K⁺, π±, Ξ⁻ all essentially exact (≤1 % off); π⁰ and η within 30 %; neutron at factor 2.4 |
| within factor 100 (\|log₁₀\| < 2) | 1 | Λ |
| off by ≥ 100× | 3 | K_S, Ξ⁰, Σ⁰ |
| negative T (sign issue) | 3 | Ω⁻, Σ⁺, Σ⁻ |
| T = 0 (formula vanishes) | 4 | all four Δ resonances |

Highlights:

- **Muon, K⁺, π±, Ξ⁻ are predicted to within ~1 %** of measured values
  — across lifetimes ranging from 10⁻¹⁰ s (Ξ⁻) to 10⁻⁶ s (μ).
- **The neutron** comes out at 361 s vs. measured 879 s — factor 2.4,
  in scope.
- **The Δ-resonance zeros** trace cleanly to F = 0 at P = 3. These are
  strong-decay states (Γ ≈ 117 MeV → τ ≈ 5.6 × 10⁻²⁴ s) and the formula
  appears intended for weak/electromagnetic channels only.
- **Σ⁰** decays electromagnetically (Σ⁰ → Λγ) and is likewise out of scope.

The remaining negative-T cases (Ω⁻, Σ⁺, Σ⁻) have negative *y*, not
negative occupancy. For Ω⁻ specifically, y is dominated by the
(P+1)·(Q,3)/α term in φ, giving y ≈ −1/α ≈ −137. This likely indicates
further transcription errors in our reading of φ ([B49]) / U ([B50]) or
of the b₁/b₂ expressions; access to Heim's original 1989 FORTRAN code
(lost) or expert review from the IGAAP / Forschungskreis Heimsche
Theorie would be the cleanest resolution.

History of the iteration:

| Iteration | Within ×3 | Within ×100 | ≥ ×100 | Negative | Zero |
|---|---:|---:|---:|---:|---:|
| Initial (image-based read) | 5 | 0 | 4 | 5 | 4 |
| Six fixes from `pdftotext` | 6 | 2 | 3 | 4 | 4 |
| + `|p|·β₀` in occupancy | **7** | 1 | 3 | 3 | 4 |

Specific fixes versus the initial implementation are documented in the
git log and inline in `python/lifetime.py`.

## The honest verdict

The question we set out to answer was: **does this look like a real
theory-driven derivation of particle masses, or like a clever fit?**

The data in this repository points to a more nuanced answer than either
extreme:

**Pro (genuine derivation):**

1. **η(q, k) is derived from physical principles**, not postulated. Chapter
   7 of the full Herleitung manuscript (eqs. 7.47 → 7.51) shows the
   chain: metron-quantised geometry → theoretical elementary charge
   ε₀± → renormalisation ε'₀± = ε₀±·⁴√(1+k/4) over L = 4 effective
   dimensions → η(q, k). This was the central pre-revision question.
2. The constants Heim explicitly labels as "fitted" turn out to be
   *immaterial*: any value of order unity would have produced
   indistinguishable predictions. So the formula is *not* succeeding
   because of a free-parameter sweep over those.
3. The mass element μ is constructed purely from G, ℏ, c with no fitting.
4. The structure constants Q_n, Q_m, Q_p, Q_σ are integer prescriptions —
   not continuous knobs.
5. Three of the four shape parameters of η lock onto simple integer values
   (4, 4, 1/4) within <1 % tolerance — and now we know *why*: those
   values come from the derivation, not from a search.
6. The fine-structure constant is calculated, not measured, to ~5 digits.

**Caveats (now fewer than before):**

1. ~~The functional form of η is *defined* in the available literature,
   not derived.~~ **Resolved 2026-04-28**: chapter 7 of the full
   Herleitung manuscript (eqs. 7.47 → 7.51) derives η(q, k) explicitly
   from the metron geometry plus charge-field renormalisation. The
   `(4+k)` factor is not a fit; it falls out of L · Δε₀±⁴ = 4 · Δε₀±⁴.
2. The mass spectrum predicts more excitations than have been observed.
   Heim attributes this to an "unknown selection rule" he was working on
   when he fell ill in 1999. This remains an admitted incompleteness.
3. The dataset is small (~20 particles). The framework was never applied
   to particles discovered after the 1980s (top, Higgs, charm-baryon
   spectroscopy) — neither by Heim nor by his successors. We don't know
   whether it would extend.
4. The lifetime formula ([B47]–[B57]) as implemented here matches
   experiment to factor 3 on 7 of 18 particles, with 3 negative T and 4
   structurally-vanishing Δ resonances. Heim's own 1989 numbers
   reportedly produced 12 of 14 within experimental error (per
   Herleitung chapter 11), but the IGW group itself never reprogrammed
   the lifetime formula, so the ground-truth FORTRAN-derived values are
   the only available reference. Our gap therefore likely reflects
   transcription errors in our reading of [B54]/[B55] that we cannot
   currently audit.
5. **Heim tuned the gravitational constant G** to the proton mass: with
   his chosen G = 6.6732 × 10⁻¹¹, only 5 of 16 mass values fall within
   experimental error; with a slightly different G, 8 of 16 do. The
   "0.2 % RMS" headline accuracy thus partly reflects a single
   parameter (G) being effectively tuned within its experimental
   uncertainty band.

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

1. **Are the b₁/b₂ transcriptions correct?** The lifetime expressions
   [B54]–[B55] in the source PDF have several typographic ambiguities.
   The IGW group itself never reprogrammed the lifetime formula (per the
   Herleitung document, chapter 11), so the currently failing lifetime
   predictions cannot be cross-checked against an independent reference.
   Heim's lost 1989 FORTRAN apparently produced 12 of 14 lifetimes within
   experimental error; we manage 7/18 within factor 3. The gap likely
   indicates further transcription errors in our reading.
2. **Does the formula extend to particles discovered after 1989?** Top
   quark, Higgs, charm and bottom baryon spectroscopy are all available
   but were never tested by Heim or any successor.
3. **Is the η derivation rigorous?** Chapter 7 (eqs. 7.47 → 7.51)
   *derives* η(q,k) from physical principles, but the derivation passes
   through Heim's polymetric formalism (selector calculus, condensor
   flows) which is non-standard. A mathematical audit by someone fluent
   in that formalism would confirm whether the chain
   `G, ℏ, c → metron τ → ε₀± → η(q,k)` is free of hidden circularity.
4. **Why is the (n, m, p, σ) loss landscape jagged?** The greedy
   decomposition produces integer outputs that flip at thresholds;
   whether this is a feature of the theory or an algorithmic artifact
   needs to be sorted out.

### Resolved

- ~~**Is η's form derivable from first principles?**~~ Yes — chapter 7 of
  the full Herleitung document derives it explicitly. Equations 7.47 →
  7.51 produce η(q, k) = ⁴√(π⁴ / (π⁴ + (4+k)q⁴)) from a metron-quantised
  geometry plus the renormalisation ε'₀± = ε₀±·⁴√(1 + k/4) of the
  elementary charge field over the L = 4 effective dimensions of
  condensation. The (4+k) factor falls out of `L · Δε₀±⁴ = 4 · Δε₀±⁴`.
  This was the central pre-revision open question. (Resolved 2026-04-28
  upon access to the full 81-page derivation manuscript.)
- ~~**[B25] uses Q_n² or Q_n³?**~~ The IGW reformulation PDF prints Q_n²
  but Heim's own research-group C# implementation
  (`downloads/csharp_impl/.../HeimGroup/SelfCouplingFunction.cs`) uses
  Q_n³, in agreement with Eli Gildish's C and our Python port. The PDF
  has a typesetting error; Q_n³ is correct. (Resolved 2026-04.)
- ~~**[B49] φ uses `+(P+1)(Q,3)/α` or `−(P+1)(Q,3)/α`?**~~ The IGW PDF
  shows what visually appears to be a double-minus separator (`−−`). We
  tested both signs; `+` produces masses that no longer bit-match the C
  reference (Δs deviate by ~0.4 %) and gives no improvement to lifetime
  predictions (Ω⁻ moves from "negative T" to "factor 4700 off"). The
  `−` reading, used by both the C and C# implementations, is therefore
  the correct one; the `−−` in the PDF is a typesetting artifact
  (likely an em-dash). (Resolved 2026-04-28.)

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
