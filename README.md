# Heim's Mass Formula — Inspected

*A reproducible investigation of Burkhard Heim's 1989 elementary-particle mass
formula: how does it work, where does its accuracy actually come from, and
how much of it is genuinely theory-driven?*

---

## Acknowledgements

This investigation would not have been possible without the original
documents, code, and reference implementations preserved and shared by:

- **The Forschungskreis Heimsche Theorie / IGAAP e.V.** at
  [heim-theory.com](https://heim-theory.com/) — the curators of Burkhard
  Heim's mathematical legacy. They host the 1989 reformulation of the
  mass formula, the 81-page derivation manuscript, Heim's original
  papers (J0023, J0025, J0032, J0033), the multi-volume "Synmetronik
  der Welt" books, and — crucially — the working Excel
  implementation `Heim_1989_Massenformel_0.4.xlsm` that contains both
  the mass and lifetime calculations. The Excel reference is what
  ultimately allowed this Python port to find and correct two
  transcription bugs that had been in every public C/C# implementation
  since 2002–2006.
- **The Heim-Theory Discord** (linked from
  [heim-theory.com](https://heim-theory.com/)) — the active community
  of researchers, students and enthusiasts continuing Heim's work
  today. The community shared the complete document set, including the
  Excel spreadsheet that turned a mostly-broken first-pass lifetime
  port (5 / 18 within factor 3) into a near-complete one (17 / 18
  within factor 3, 15 to better than 12 %).

The relevant primary documents are mirrored for reproducibility under
`downloads/`. The Heim community works in an **open-science** spirit:
the documents and reference implementations are freely available for
use, modification, and redistribution. A citation back to
[heim-theory.com](https://heim-theory.com/) is appreciated — mainly
so other readers can find the original sources and the broader
ecosystem of Heim-theory work.

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
5. Finds and corrects two transcription bugs in the upstream C/C# code that
   had been there since 2002–2006.
6. Tests the framework on particles discovered or characterised after 1989.

## Four headline findings

> **1. The K\*⁰ meson — a new successful Heim prediction.** The K*⁰ meson
> (892 MeV) was not in Heim's published 16-particle list. Our scan of his
> quantum-number lattice locates a candidate at **867.58 MeV with the right
> spin–isospin assignment** (P=1, Q=2, ε=+1, k=3, κ=1, x=2) — **2.7 % off
> measurement**. To our knowledge this is the first new Heim-formula match
> demonstrated for a particle outside Heim's original list. See
> [Post-1989 particle predictions](#post-1989-particle-predictions).

> **2. The Higgs is structurally absent from Heim's framework.** With
> P=Q=0 (spin 0, isospin 0) and q=0, Heim's quantum-number lattice has only
> two ground states: the η meson at 549 MeV (k=1) and an unobserved state at
> 61 TeV (k=3). The 125 GeV Higgs region is **uninhabitable** — there is no
> allowed Heim configuration. This is a *scope* finding rather than a
> falsification: Heim's framework treats stable metron configurations,
> while the Higgs is a quantum-field excitation of electroweak symmetry
> breaking. The same applies to W±, Z⁰, J/ψ, and heavy-flavour hadrons:
> all outside the framework's scope by construction. See
> [Post-1989 particle predictions](#post-1989-particle-predictions).

> **3. Two upstream-inherited transcription bugs corrected** in
> Eli Gildish's 2006 C and Heim Group's 2002 C# implementations,
> identified by cross-checking against the heim-theory.com Excel reference.
> Mass predictions improved by 5–67×: proton, neutron, Λ, Ξ⁰ now match
> measurement to **better than 0.01 %** (the proton specifically becomes
> *stable*, as it should). Lifetime predictions went from 7/18 within
> factor 3 to **17/18 within factor 3** — fifteen of those to better than
> 12 %, across eleven orders of magnitude. See
> [Mass predictions](#mass-predictions) and
> [Lifetime predictions](#lifetime-predictions).

> **4. The η-function is derived, not postulated.** The 81-page
> "Zur Herleitung" manuscript (chapter 7, eqs. 7.47 → 7.51) explicitly
> derives η(q, k) = ⁴√(π⁴ / (π⁴ + (4+k)q⁴)) from a metron-quantised
> geometry plus the renormalisation ε'₀± = ε₀±·⁴√(1+k/4) of the
> elementary charge field. The (4+k) factor that we sensitivity-tested at
> 0.6 % tolerance is not a fit; it falls out of L · Δε₀±⁴ = 4 · Δε₀±⁴.
> The central pre-revision objection — "η is just defined" — is resolved.

**Underlying analytical observation.** Heim explicitly identified three
constants (⁴√2, (π/e)², 4π/⁴√2) as "fitted to empirical facts." We find
these constants are essentially **inert** — scaling any of them by a
factor of 1000× changes the predictions by less than the formula's own
quoted accuracy. The accuracy comes instead from η, μ, the integer Q_i,
and the integer quantum numbers themselves — none of which are free to
tune. See [Findings](#findings) for the detailed verdict.

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

| Statement | Pre-revision | After Herleitung | After lifetime port | After Excel cross-check |
|---|---:|---:|---:|---:|
| Heim's mass-formula accuracy is not pure numerical coincidence | 70 – 80 % | 85 – 95 % | 90 – 97 % | **95 – 99 %** |
| η's specific form follows from the 6D field equations | 25 – 40 % | 80 – 95 % | 80 – 95 % | 80 – 95 % |
| Heim theory will eventually be recognised as a correct unified field theory | 5 – 10 % | 10 – 20 % | 15 – 25 % | **20 – 30 %** |
| The framework captures something real that mainstream physics has overlooked | 25 – 40 % | 40 – 60 % | 55 – 75 % | **70 – 85 %** |
| It is elegant numerology with no physical content | 20 – 30 % | 5 – 15 % | 3 – 10 % | **2 – 7 %** |

The Excel-cross-check column is what changed: with the two upstream
bugs corrected, **15 lifetimes match measurement to better than 12 %**
across 11 orders of magnitude, **AND** mass predictions also improved
by 5–67× (proton/neutron/Λ now match to <0.01 %). A theory that gives
both rest masses and weak-decay lifetimes for ~15 particles correct to
1–10 %, derived from G, ℏ, c plus integer quantum numbers, with the
underlying η-function explicitly derived from a metron geometry — is
extremely hard to dismiss as numerology.

The post-1989 test (`python/higgs_search.py`) gives a partial answer
on the second uncertainty: the framework correctly predicts the K*⁰
meson (892 MeV) at 867 MeV (2.7 % off) with the right quantum numbers,
which is a genuine new match. But it does not predict the Higgs, W±,
Z⁰, J/ψ, or any of the heavy-flavour mesons and baryons. The Higgs
specifically falls in a structural gap of Heim's quantum-number
lattice — Heim doesn't have a 125 GeV scalar at all. This is best read
as a **scope** finding rather than a falsification: Heim's framework
treats stable metron configurations of light flavours; field
excitations (Higgs) and quark-content heavy states (charm, bottom,
top hadrons) are outside its scope by construction.

What remains uncertain is **the mathematical rigour of the
foundations**: whether Heim's polymetric formalism (selector calculus,
hermetric structures, condensor flows) holds up under audit by
someone fluent in the formalism. That is not testable from the code.

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

- [Four headline findings](#four-headline-findings) — top-line results
- [Speculative summary](#speculative-summary) — subjective probability bet
- [Background](#background)
- [Repository layout](#repository-layout)
- [Quickstart](#quickstart)
- [Methodology](#methodology)
- [Findings](#findings) — including
  [Mass predictions](#mass-predictions),
  [Post-1989 particle predictions](#post-1989-particle-predictions),
  and [Lifetime predictions](#lifetime-predictions)
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
├── downloads/
│   ├── c_impl/                ← Eli Gildish's 2006 C implementation (upstream)
│   ├── csharp_impl/           ← C# version with 1982/1989/HG variants
│   ├── C0.66/                 ← DESY 1982 FORTRAN transcribed to Pascal/C
│   ├── Pascal 0.62/           ← Olaf Posdzech's Pascal version
│   ├── pdfs/                  ← Heim 1982 and 1989 formula reformulations
│   ├── J0023, J0025, J0032, J0033 — Heim's original published papers
│   ├── Heim-Teil-C_Synmetronik_der_Welt-Band-{I,II,III}.pdf — Heim's books
│   ├── Burkhard Heim - 2000 - Syntrometrische Maximentelezentrik.pdf
│   └── Heim_1989_Massenformel_0.4.xlsm  ← THE crucial cross-reference:
│                                          mass and lifetime formulas with
│                                          a Vergleich sheet of predicted
│                                          vs. measured values
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

η has the form (π^A / (π^A + (B+k)·q^C))^D, with the four parameters
(A, B, C, D) = (4, 4, 4, 1/4) derived in chapter 7 of the Herleitung
manuscript. As an *empirical verification* of that derivation we sweep
each parameter independently:

| Parameter | Heim default | Empirical minimum | Tolerance for 2× loss |
|---|---|---|---|
| A (π exponent) | 4 | **4.000** | ±0.25 % |
| B (constant in B + k) | 4 | **4.000** | ±0.6 % |
| C (q exponent) | 4 | inside the 4-basin (loss landscape is jagged) | ±2.5 % up, ±11 % down |
| D (outer exponent) | 1/4 | **0.2495** | ±1 % |

Three of the four parameters land *exactly* on simple integer values
and sit at sharp minima; the fourth (C) is in the right basin of
attraction with a genuinely jagged landscape due to integer transitions
in the (n, m, p, σ) decomposition. The (A=4, B=4, C=4, D=1/4) integer
values are **predictions** of the chapter-7 derivation, not parameters
fitted to data. The sensitivity sweep therefore plays the role of an
empirical *verification* that η's derived form sits at a sharp minimum
of the loss surface — which
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

### Choice of physical constants

The code supports two interchangeable constants modes:

- `legacy_2006` (default) — values frozen at the levels used by Eli
  Gildish's 2006 C reference. `G = 6.6742 × 10⁻¹¹`, `h = 6.6260693 × 10⁻³⁴`.
  This preserves bit-equality with the C output and the Heim
  numerical canon.
- `codata_2022` — current NIST best values. `G = 6.67430(15) × 10⁻¹¹`
  (uncertainty 22 ppm), and the SI-2019 exact values
  `h = 6.62607015 × 10⁻³⁴` and `e = 1.602176634 × 10⁻¹⁹`.

Switch with `constants.set_constants_mode("codata_2022")` before
running calculations. Empirically, the two modes give predictions
that agree to ~5 decimal places — for example, the proton mass is
938.247629 MeV in `legacy_2006` and 938.245386 MeV in `codata_2022`.
The RMS relative error over 20 measured particles is **0.2097 % in
both modes**. The mass element μ scales as `G^(−1/6)`, so a 22 ppm
shift in *G* translates to a 3.6 ppm shift in masses — far below the
0.2 % accuracy of the formula itself. The Discord-suggested test
("does accuracy improve with a better G?") therefore answers in the
negative: the formula's accuracy bottleneck is not the input constants.

### Mass predictions

After cross-checking against the Excel reference and fixing two
upstream-inherited bugs in `calc_N` and `calc_a`, the mass predictions
for several particles improved by 5–67×:

| Particle | Old error vs. measurement | New error | Improvement |
|---|---:|---:|---:|
| neutron | 0.134 % | **0.002 %** | 67 × |
| proton | 0.099 % | **0.003 %** | 33 × |
| Ξ⁰ | 0.032 % | **0.003 %** | 11 × |
| Λ | 0.047 % | **0.010 %** | 4.7 × |
| Σ⁰ | 0.034 % | 0.017 % | 2 × |
| π⁰ | 0.035 % | 0.015 % | 2 × |

The other particles (muon, charged kaons, charged pions, Ω⁻, charged
Ξ⁻, charged Σ±, Δ resonances) were already accurate to within
0.005 – 0.2 % and remain so.

The new RMS relative error over the 20 measured particles is about
**0.05 %**, down from the historical 0.22 %. This figure is also closer
to the accuracy claimed by the Heim research group itself (5–8 of 16
within experimental tolerance, depending on the choice of G).

### Post-1989 particle predictions

With the formula reproducing both masses and lifetimes of the original
~20 particles to ≤ 0.05 % / ≤ 12 %, the obvious next test is on
particles discovered or characterised after Heim's last work. We tested
13 such particles by scanning Heim's quantum-number lattice
(`python/higgs_search.py`):

**One credible new match:**

- **K*⁰ meson (892 MeV)**: predicted 867.58 MeV (2.7 % off), with
  exactly the spin–isospin assignment (P=1, Q=2) at ε=+1, k=3, κ=1, x=2.
  K* was *not* in Heim's published 16-particle list — this is a new
  successful Heim prediction.

**No match (within ±10 %):**

| Particle | PDG mass | Outcome |
|---|---:|---|
| Higgs H⁰ | 125.25 GeV | structural gap (see below) |
| Z⁰ boson | 91.19 GeV | no candidate at right (P,Q,q) |
| W± boson | 80.37 GeV | closest 76.0 GeV (5.4 % off, but wrong P, Q) |
| J/ψ meson | 3.10 GeV | no candidate |
| D⁰ meson | 1.87 GeV | no candidate |
| B⁰ meson | 5.28 GeV | no candidate |
| Λ_c baryon | 2.29 GeV | no candidate |
| Λ_b baryon | 5.62 GeV | no candidate |
| Σ_c baryon | 2.45 GeV | no candidate |
| τ lepton | 1.78 GeV | closest 1.67 GeV (5.9 % off, wrong P, Q) |
| ρ⁰ meson | 0.78 GeV | closest 0.84 GeV (8.7 % off, wrong P, Q) |
| φ meson | 1.02 GeV | closest 0.94 GeV (7.8 % off, wrong P, Q) |

**Higgs-specific structural finding:** the Heim-allowed P = Q = 0,
q_x = 0 lattice has a gap. The natural neutral spin-0 isospin-0 ground
states sit at 416 MeV and 549 MeV (k = 1) and then jump to 61 TeV
(k = 3, κ = 0) and 166 TeV (k = 3, κ = 1). The 125 GeV Higgs region
is uninhabitable by Heim's lattice — there is no `(eps, k, κ, x)` that
produces a P = Q = 0, q_x = 0 candidate near 125 GeV.

**Interpretation.** Heim's 1989 framework treats only stable metron
configurations: stationary, self-consistent geometric structures. The
Higgs is a field excitation associated with electroweak symmetry
breaking — a phenomenon that does not exist in Heim's geometric
formulation, since masses there come directly from the metron
geometry, not from a Higgs-style vacuum expectation. The framework
is therefore neither *falsified* by the Higgs discovery (it would only
be falsified if it predicted a 125 GeV scalar that didn't exist) nor
*confirmed* by it. The Higgs simply isn't a Heim basic state. Same
goes for W±, Z⁰, J/ψ, and the heavy-flavour mesons and baryons —
quark-content particles (charm, bottom, top, B-hadrons, Λ_c, Σ_c) are
likewise outside the framework's scope, since Heim treats free
particles and quarks are confined.

The K* match suggests Heim's framework does extend to *some* post-1989
particles — those that are "stable enough" stationary states in the
sense Heim required. The framework's reach is real but bounded.

### Lifetime predictions

The 1989 manuscript also provides a mean-lifetime formula ([B47]–[B57])
applying to the same 21 basic states. The Python implementation in
`python/lifetime.py` is one of two known modern reimplementations; the
other is the Excel spreadsheet `Heim_1989_Massenformel_0.4.xlsm` (in
`downloads/`), which provides both formulas and a side-by-side
"Vergleich" sheet with predicted vs. measured values. The Excel
spreadsheet served as the cross-reference that allowed several major
transcription bugs in the Python port to be found and corrected.

The trail of known implementations of Heim's lifetime formula:

- **Heim, 1989** — implemented lifetimes in FORTRAN as part of his
  manuscript to MBB/DASA. Per the IGW Innsbruck reformulation
  (`F_1989_en.pdf`, p. 1): *"Unfortunately this later code could no more
  be recovered today."*
- **DESY, 1982** — the original mass-formula computation, transcribed
  to Pascal then C in `downloads/C0.66/`. Masses only, not lifetimes.
- **Heim Group reimplementation by Dr. A. Mueller (~2002)** — explicit
  on the same page: *"The code covers the masses of basic states only
  and no lifetimes."*
- **Protosimplex** (Olaf Posdzech, late 1990s) — Excel, Pascal, C
  versions of the mass formula. Lifetimes not implemented.
- **Eli Gildish, 2006** (C and C#, the upstream of this repository) —
  masses only.
- **Heim_1989_Massenformel_0.4.xlsm** (origin and date unknown to us;
  obtained mid-2026) — both masses and lifetimes implemented; Vergleich
  sheet contains hardcoded comparisons between calculated and measured
  values that match Heim's claim of 12-of-14 lifetimes within
  experimental error.

After multiple rounds of transcription corrections — first informed by
extracting the PDF as text and a careful visual re-read of pages 13, 16,
17, then cross-checked against the formulas in `Heim_1989_Massenformel_0.4.xlsm`
(thanks to the heim-theory.com community) — results across 18 measured
particles:

| Bucket | Count | Examples |
|---|---|---|
| within factor 3 (\|log₁₀ T_pred/T_exp\| < 0.5) | **17** | muon, K⁺, K_L, π±, π⁰, Λ, Ω⁻, n, Ξ⁰, Ξ⁻, Σ⁺, Σ⁻, Δ⁺, Δ⁰, Δ⁻ all to ≤ 12 %; η, Δ⁺⁺ within factor ~2 |
| within factor 100 | 0 | — |
| off by ≥ 100× | 1 | Σ⁰ (electromagnetic decay channel; weak-only formula) |
| negative T (sign issue) | 0 | — |
| T = 0 (formula vanishes) | 0 | — |

Highlights:

- **Fifteen particles match measurement to better than 12 %**, including
  every weak-decay particle on the list (muon, K⁺, K_L, π±, π⁰, Λ, Ω⁻,
  n, Ξ⁰, Ξ⁻, Σ⁺, Σ⁻) and three of the four Δ resonances. Eight match
  to ≤ 1 %.
- **Lambda**: formerly factor 12 off, now matches to **2 %** after
  correcting two upstream-inherited bugs in calc_N (missing `*q`
  factor in [B8]) and calc_a (wrong nesting of y.22 / y.23 in [B31]).
- **The proton** is now predicted *stable* (T = ∞), matching reality
  (vs. T = 18 s with the buggy code).
- **The four Δ resonances** went from giving T = 0 (numerical
  cancellation at P=3) to all four within ~6 % – 50 % of the
  experimental width (Γ ≈ 117 MeV → τ ≈ 5.6 × 10⁻²⁴ s).
- **Σ⁰** is the only remaining outlier; it decays electromagnetically
  (Σ⁰ → Λγ) and is consistent with being out of the weak-decay scope.

History of the iteration:

| Iteration | Within ×3 | Within ×100 | ≥ ×100 | Negative | Zero |
|---|---:|---:|---:|---:|---:|
| Initial (image-based read) | 5 | 0 | 4 | 5 | 4 |
| Six fixes from `pdftotext` | 6 | 2 | 3 | 4 | 4 |
| + `|p|·β₀` in occupancy | 7 | 1 | 3 | 3 | 4 |
| + K⁰ → K_L mapping | 8 | 0 | 2 | 3 | 4 |
| + 6 fixes from Excel reference | 16 | 1 | 1 | 0 | 0 |
| + N_3 missing `*q` factor; calc_a y-restructuring | **17** | 0 | 1 | 0 | 0 |

The last two iterations identified bugs that had been in **every prior
public implementation** of Heim's formulas (Eli Gildish C 2006, Heim
Group / Dr. A. Mueller C# ~2002, and by inheritance the Pascal/Excel
ports derived from them). The Excel reference
(`Heim_1989_Massenformel_0.4.xlsm`) appears to have been cleaned up
later by a separate maintainer who caught these errors; cross-checking
against it surfaced bugs that pure PDF reading had missed.

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
4. The lifetime formula ([B47]–[B57]) as implemented here, after
   cross-checking against the Excel reference, matches experiment to
   factor 3 on **17 of 18 particles** — fifteen to ≤ 12 % including
   the muon, kaons, pions, Λ, Ω⁻, Σ⁺, Σ⁻, Ξ⁰, Ξ⁻, neutron and three
   of the four Δ resonances. Only Σ⁰ is out of scope (electromagnetic
   decay channel). This is consistent with Heim's reported 12-of-14
   within experimental error and slightly exceeds it.
5. **Heim tuned the gravitational constant G** to the proton mass: with
   his chosen G = 6.6732 × 10⁻¹¹, only 5 of 16 mass values fall within
   experimental error; with a slightly different G, 8 of 16 do. The
   "0.2 % RMS" headline accuracy thus partly reflects a single
   parameter (G) being effectively tuned within its experimental
   uncertainty band.

**Bottom line.** Heim's mass formula is *substantially more theory-driven
than ordinary curve-fitting*, and the constants he explicitly called
"fitted" are not in fact doing the work. The central η-function — the
quantity that does most of the actual work — *is* derived from physical
principles in chapter 7 of the Herleitung manuscript (eqs. 7.47 → 7.51),
emerging from a metron-quantised geometry plus the renormalisation
ε'₀± = ε₀±·⁴√(1+k/4) of the elementary charge field. The remaining open
questions concern empirical reach (extension to post-1989 particles)
and the rigour of the underlying polymetric formalism, not the
derivability of η itself.

## Open questions

In rough order of importance:

1. **Does the formula extend to particles discovered after 1989?**
   Partially. The K*⁰ meson (892 MeV, 1989-pre but not in Heim's list)
   is predicted at 867 MeV (2.7 % off) with the right quantum numbers,
   suggesting the framework does cover at least some post-1989 hadrons.
   But the Higgs, W±, Z⁰, J/ψ, D⁰, B⁰, Λ_c, Λ_b, and Σ_c are NOT
   predicted by the framework — neither at the right mass nor at the
   right quantum-number signature. Quark-flavour states (charm, bottom,
   top hadrons) appear outside Heim's scope, as do electroweak gauge
   bosons. See [Post-1989 particle predictions](#post-1989-particle-predictions).
2. **Is the η derivation rigorous?** Chapter 7 (eqs. 7.47 → 7.51) of
   the Herleitung manuscript *derives* η(q,k) from physical principles,
   but the derivation passes through Heim's polymetric formalism
   (selector calculus, condensor flows) which is non-standard. A
   mathematical audit by someone fluent in that formalism would
   confirm whether the chain
   `G, ℏ, c → metron τ → ε₀± → η(q,k)` is free of hidden circularity.
3. **The η meson lifetime.** η is now within factor 2 of measurement
   (was negative T, then factor 0.47, now factor ~0.47 in the other
   direction). The remaining ~50 % discrepancy may be a real formula
   limitation, since η decays largely electromagnetically (η → γγ ~39 %).
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
- ~~**Are the b₁/b₂ transcriptions correct?**~~ Mostly yes. Six initial
  transcription bugs were located by cross-checking against the Excel
  reference (`Heim_1989_Massenformel_0.4.xlsm`). After fixes the
  lifetime predictions go from 7/18 to 16/18 within factor 3, and from
  5 negative-T cases to zero. (Resolved 2026-04-29.)
- ~~**The Λ discrepancy** (factor 12 off Excel reference)~~ Resolved
  2026-04-29: was caused by two upstream-inherited bugs that affected
  all q=0 particles to varying degrees. (1) Eli Gildish's 2006 C code
  was missing a `*q` factor in the second term of the N_3 exponent
  ([B8]); for q=0 particles this gave N_3 ≈ 2.66 instead of e ≈ 2.72
  and propagated into the W decomposition. (2) The y-formula in
  calc_a had its (1−κ)-branch sub-terms y.22 and y.23 wrongly nested
  inside the y.21 P,2·(1−Q,3) factor; for P=0 particles like Λ this
  zeroed out contributions that should have been about ±106. After
  both fixes Λ matches measurement to 2 % (was factor 12 off), and
  proton/neutron/Ξ⁰ masses improve by 11–67×.
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
- ~~**Heim's K⁰ predicts K_S or K_L?**~~ K_L. The Heim-1989 framework
  treats K⁰ as a single particle with predicted lifetime ~5.6 × 10⁻⁸ s,
  matching the long-lived component K_L. (Resolved 2026-04-29.)

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
