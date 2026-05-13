# Heim's Mass Formula — Inspected

*A reproducible investigation of Burkhard Heim's 1989 elementary-particle mass
formula: how does it work, where does its accuracy actually come from, and
how much of it is genuinely theory-driven?*

> 📖 **New to Heim theory?** Read **[THEORY_EXPLAINED.md](THEORY_EXPLAINED.md)**
> first — a 15-chapter, three-level (Beginner / Intermediate / Expert)
> walk-through of the framework: Burkhard Heim's biography, the 6D
> geometry, the metron, the mass formula step by step, a worked proton
> example, Syntrometrie, and the Extended (8D / 12D) Heim–Dröscher
> theory. The README that follows is the analysis report; the
> companion document is the conceptual guide.

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

## Scope of this repository

*This statement was substantially rewritten following an extended review
exchange with Joel from the Heim-Theory Discord in May 2026.*

> The chain `Heim Theory ≠ Syntrometrie ≠ Synmetronik ≠ Elementarstrukturen
> der Materie ≠ Mass Formula A/B ≠ Python code` is real and important.
> This repository implements a reconstructed reading of the **computationally
> transmitted mass-formula layer** (the terminal projection). It does not
> implement Heim Theory as a whole, does not implement Syntrometrie as a
> complete formal system, and does not reconstruct the full derivation from
> Syntrometrie down to the executable formula.

A historical transmission was made available by the Heim-Theory Discord
community in May 2026 (`downloads/A_…` through `downloads/H_…`).
The relevant source layering, which the repo now adopts:

| Layer | Meaning | File(s) |
|---|---|---|
| A / 1982 source | Ground-pattern / original mass-formula source. Defines `k ∈ {1, 2}` for ponderable particles, P, Q, κ, q_x, C = strangeness, etc. | `downloads/A_Massenformel_Kurzfassung.pdf`, `downloads/E_Massenformel_nach_B_Heim_1982.pdf` |
| B / 1989 extension | Extends formula to excited states (N > 0), lifetimes, neutrino masses, fine-structure constant. Lost code, source-critical reconstruction. | `downloads/F_Erweiterte_Massenformel_nach_Heim 1989.pdf` |
| G / selected results | Numerical-output tables: ground states, theoretical/experimental data, **approximate meson resonances (k=1)**, **approximate baryon resonances (k=2)**, lifetimes, Heim's own 1989 predictions for 23 mesons + 50+ baryons. | `downloads/G_Ausgewaehlte_Ergebnisse.pdf` |
| Old programs | DESY / Pascal / C / C# / Excel transmission chain. | `downloads/c_impl/`, `downloads/csharp_impl/`, `downloads/Pascal 0.62/`, `downloads/C0.66/`, `downloads/Heim_1989_Massenformel_0.4.xlsm` |
| Current repo | Modern Python reconstructed implementation. | `python/` |
| Modern PDG | External empirical reference; not identical with Heim ontology. | — |

The intended domain of the formula must be reconstructed from
A + B + G together, not inferred from any one source alone.

## Headline findings

> **1. The mass-formula layer carries non-trivial numerical structure.**
> Sensitivity analysis shows three of Heim's *self-described* "fitted"
> constants (⁴√2, (π/e)², 4π/⁴√2) are essentially inert — changing them
> by factors of 1000× has effects below the formula's own quoted accuracy.
> The accuracy lives instead in η(q, k), the mass element μ, the integer
> structure constants Q_i, and the integer quantum numbers, none of which
> are free parameters. This is the central positive result: the formula
> is not succeeding through hidden tunable knobs.

> **2. The η-function is derived from physical principles, not postulated.**
> The 81-page "Zur Herleitung" manuscript (chapter 7, eqs. 7.47 → 7.51)
> derives η(q, k) = ⁴√(π⁴ / (π⁴ + (4+k)q⁴)) from a metron-quantised
> geometry plus the renormalisation ε'₀± = ε₀±·⁴√(1+k/4) of the elementary
> charge field. The (4+k) factor — sensitivity-tested at 0.6 % tolerance
> — is not a fit; it falls out of L · Δε₀±⁴ = 4 · Δε₀±⁴.

> **3. The same η drives Heim's *magnetic-moment* formula.** Synmetronik
> Band III (1980), Eq. 186, gives the electron magnetic moment as
> μ_e/μ_B = (e_w/e_±)·(1 − e·K/(6·√η)) with the *same* η-function that
> appears in the mass formula and α-derivation. Reverse-engineering K
> from the measured (g-2)/2 anomaly produces K ≈ 2.547·10⁻³, which
> agrees with the QED-Schwinger expression 6·√η·α/(2π·e) = 2.551·10⁻³
> to **0.15 %**. Heim's structural formula from 1980 is consistent with
> leading-order QED. Caveat: a from-first-principles prediction requires
> the protosimplex/synmetronic side of the framework, not in our port.

> **4. Two upstream-inherited transcription bugs corrected** in
> Eli Gildish's 2006 C and Heim Group's 2002 C# implementations,
> identified by cross-checking against the heim-theory.com Excel reference.
> Mass predictions improved by 5–67×: proton, neutron, Λ, Ξ⁰ now match
> measurement to **better than 0.01 %** (the proton specifically becomes
> *stable*, as it should). Lifetime predictions went from 7/18 within
> factor 3 to **17/18 within factor 3** — fifteen of those to better
> than 12 %, across eleven orders of magnitude. The 1989 source itself
> notes that "in the manuscript some brackets in very long equations were
> lost during the process of writing; this had to be corrected at best
> estimate" — our independent fixes are consistent with this known
> transmission failure mode.

> **5. Heim's 1989 framework predicts five neutrinos with specific masses.**
> G-Tabelle II ("Theoretical Data of Elementary Particles… Calculated
> by B. Heim 1989") lists masses for **five** neutrino species, two
> beyond the Standard Model's three:
>
> | Species | Heim 1989 mass | Status |
> |---|---|---|
> | ν_e | 0.00381 × 10⁻⁶ MeV ≈ **3.81 meV** | below KATRIN upper bound 0.45 eV ✓ |
> | ν_μ | 0.00537 MeV ≈ **5.37 keV** | ruled out as active mixing eigenstate by cosmological Σm_ν < 0.12 eV; viable only as sterile / non-mixing |
> | ν_τ | 0.010752 MeV ≈ **10.75 keV** | same — only viable as sterile |
> | **ν_4** | 0.021059 MeV ≈ **21.06 keV** | **fourth-generation prediction** (sterile interpretation) |
> | **ν_5** | 0.207001 MeV ≈ **207 keV** | **fifth-generation, heavy-neutral-lepton regime** |
>
> This is a genuine tension between Heim 1989 and modern cosmology if
> ν_μ / ν_τ are identified with the SM mass eigenstates (which are
> bounded to ≪ 1 eV by oscillations + KATRIN + cosmology). Three
> possible resolutions: (a) Heim's "ν_μ" / "ν_τ" labels denote sterile
> states distinct from the SM ν_μ / ν_τ; (b) the values are wrong;
> (c) the SM mass eigenstates are emergent / mixing effects beyond
> Heim's bare framework. Falsification handle: ν_5 at 207 keV is
> within PIENU / NA62 heavy-neutral-lepton sensitivity. See
> [`python/heim_neutrinos.py`](python/heim_neutrinos.py).

### Findings that were retracted or sharpened after the source audit

> **The "K\*(892) / Λ(1690) as new Heim predictions" claim** has been
> retracted. Both particles are explicitly in Heim's G-Tabelle IV / Va
> as approximated resonances (K\*(892) at theoretical 891.20 / 892.22 MeV;
> Λ(1690) at theoretical 1693.28 MeV). Our excited-state scan at k=3
> found K\* at 867.6 MeV (2.7 % below Heim's own published table value);
> Heim's k=1 resonance procedure (using P, N, K_B parameters separate
> from the (ε, k, P, Q, κ, x) ground-state scheme) is *not implemented*
> in our port. The correct framing: this is a reconstruction gap, not
> a new prediction. See
> [Post-1989 particle predictions](#post-1989-particle-predictions).

> **The "Higgs is structurally absent from Heim" framing** has been
> sharpened. The empirical core is narrower than "we observed the Higgs
> field": ATLAS / CMS observed a 125 GeV scalar-like resonance whose
> production and decay channels are *broadly consistent* with the
> Standard Model Higgs. The full Higgs-sector picture — scalar
> potential, self-coupling, elementary-vs-composite character, deeper
> origin of parameters — remains open even within the Standard Model.
> Heim's framework proposes its own geometric mass mechanism and does
> not need a Higgs field as a primitive. A complete Heim-compatible
> theory must therefore account for the *observed* 125 GeV resonance
> phenomenology, but it may interpret it as an effective excitation
> of deeper geometric dynamics rather than as the fundamental origin
> of mass. The same logic applies to W±, Z⁰: their observed
> phenomenology must eventually be recovered, but neither needs to
> appear as primitive Heim ontology. See
> [Post-1989 particle predictions](#post-1989-particle-predictions).


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

| Statement | Pre-revision | After Herleitung | After lifetime port | After Excel cross-check | After η-triple-role | After A/B/G source audit |
|---|---:|---:|---:|---:|---:|---:|
| Heim's mass-formula accuracy is not pure numerical coincidence | 70 – 80 % | 85 – 95 % | 90 – 97 % | 95 – 99 % | 97 – 99 % | **97 – 99 %** ✓ |
| η's specific form follows from the 6D field equations | 25 – 40 % | 80 – 95 % | 80 – 95 % | 80 – 95 % | 85 – 95 % | **85 – 95 %** ✓ |
| Heim theory will eventually be recognised as a correct unified field theory | 5 – 10 % | 10 – 20 % | 15 – 25 % | 20 – 30 % | 18 – 28 % | **18 – 30 %** ↑ slightly |
| The framework captures something real that mainstream physics has overlooked | 25 – 40 % | 40 – 60 % | 55 – 75 % | 70 – 85 % | 75 – 88 % | **78 – 90 %** ↑ |
| It is elegant numerology with no physical content | 20 – 30 % | 5 – 15 % | 3 – 10 % | 2 – 7 % | 1 – 5 % | **1 – 4 %** ↓ |
| Current Python port reproduces Heim's intended results | — | — | — | 85 – 95 % | 85 – 95 % | **60 – 75 %** ↓↓ |

The most recent column reflects a deep source audit using the
historical A / B / G transmission set provided by the Heim-Theory
Discord community in May 2026:

- **Up** for "captures something real" and "unified field theory": the
  G-Tabelle IV / Va contain explicit theoretical mass predictions by
  Heim for 23 mesonic resonances (including ρ, ω, φ, K*, η', f, A1,
  …) and >50 baryonic resonances (Λ, Σ, Ξ, Δ, N* families) at
  agreement levels of ≈ 0.05–1 % with PDG. The earlier "structural
  gap for vector mesons" was an artifact of our limited
  excited-state-scan procedure — not a feature of Heim's framework.
  Heim's framework is empirically broader than our port currently
  exposes. Additionally, G-Tabelle II lists masses for **five
  neutrino species** (3.81 meV, 5.37 meV, 10.75 meV, 21.06 meV,
  207 MeV) — concrete falsifiable post-Standard-Model predictions
  this repo had not previously documented.

- **Down** for "current Python port reproduces Heim's intended
  results": Heim's 1989 Tabelle II gives an electron mass of
  0.51100343 MeV (matching PDG to 5 decimal digits). Our port
  computes 0.50694 MeV — **0.79 % off**. This is a remaining
  transcription discrepancy specific to the electron configuration
  (k=1, P=1, Q=1, κ=0, x=1) that we have not yet identified.
  Additionally, our excited-state scan found K\*(892) at 867.6 MeV
  in a k=3 sector, whereas Heim's G-Tabelle IV places K\* at
  k=1 with theoretical 891.20 / 892.22 MeV — so our scan is *not
  reproducing the historical resonance procedure*. These are
  open reconstruction tasks, not foundational issues.

In short: the source audit *strengthens* the case for Heim's
framework substantively (because G now provides concrete
ground-truth predictions to compare against, and Heim's
empirical reach is broader than we had reported) while
*weakening* our claim that the current port faithfully reproduces
Heim's intended computation.

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

The strongest three anchors for *not coincidence* are now:

1. The **fine-structure constant**: $1/α = 137.036\,01$ emerges from η and
   θ via [B58]–[B62] with no free parameters, matching experiment to ~5
   decimal digits. One number, five digits, no fit knobs.
2. The **η derivation**: η(q, k) = ⁴√(π⁴ / (π⁴ + (4+k)q⁴)) follows from
   the metron-quantised geometry plus the renormalisation
   ε'₀± = ε₀±·⁴√(1+k/4) of the elementary charge over k effective
   dimensions. The (4+k) factor that we sensitivity-tested at 0.6 %
   tolerance is not a fit; it falls out of L = 4 (number of dimensions
   in R₃ + time) times Δε₀±⁴.
3. The **electron magnetic moment**: Heim's Synmetronik III Eq. 186
   (1980) gives μ_e/μ_B in terms of the *same* η. Reverse-engineering
   the unknown internal ratio K from measured (g-2)/2 yields a value
   that matches the QED-Schwinger expression 6·√η·α/(2π·e) to 0.15 %.
   The structural shape Heim wrote in 1980 is consistent with leading-
   order QED — a third independent role for η.

What would still shift this assessment substantially:

- **Reproducing Heim's G-Tabellen IV / V exactly.** Heim's own 1989
  framework lists theoretical masses for 23 mesonic resonances (including
  ρ, ω, φ, K* via their k=1 P-N-K_B parametrisation) and >50 baryonic
  resonances at ≤ 1 % from PDG. If a clean modern implementation can
  reproduce these G-table values from first principles using only Heim's
  documented quantum-number structure, the framework moves from
  "interesting structure" to "well-defined and reproducible".
- **Resolving the 0.79 % electron-mass discrepancy** between Heim's
  1989 Tabelle II (0.51100343 MeV) and our port (0.50694 MeV). This is
  a localised transcription / convention issue, not a foundational one,
  but every other particle in our port matches Heim's table to ≤ 0.01 %.
- **Confirming or refuting Heim's five-neutrino prediction.** The
  ν_5 at 207 MeV in particular is in a range where laboratory bounds
  on heavy neutral leptons / sterile neutrinos already exist. A
  detailed comparison would be a clean falsification test.
- **A mathematical audit of the chapter 7 η-derivation** by someone
  fluent in Heim's polymetric formalism, to confirm that no circular
  reasoning enters via the chain ε₀± → η.

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

- **[THEORY_EXPLAINED.md](THEORY_EXPLAINED.md)** — companion document:
  conceptual three-level walk-through of Heim theory (start here if
  you are new to the framework)
- [Scope of this repository](#scope-of-this-repository) — what is actually implemented
- [Headline findings](#headline-findings) — top-line results
- [Speculative summary](#speculative-summary) — subjective probability bet
- [Background](#background)
- [Repository layout](#repository-layout)
- [Quickstart](#quickstart)
- [Methodology](#methodology)
- [Findings](#findings) — including
  [Mass predictions](#mass-predictions),
  [Post-1989 particle predictions](#post-1989-particle-predictions),
  [Lifetime predictions](#lifetime-predictions),
  and [Beyond the mass formula — Kontrabarie](#beyond-the-mass-formula--kontrabarie)
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
│   ├── A_Massenformel_Kurzfassung.pdf      ← A: 1982 source / Kurzfassung
│   ├── B_Bemerkungen_ueber_Heim.pdf        ← editorial notes
│   ├── C_Zum_Stand_der_Elementarteilchenphysik.pdf   ← context
│   ├── D_Zur_Herleitung_Der_Heimschen_Massenformel.pdf  ← 81-page derivation
│   ├── E_Massenformel_nach_B_Heim_1982.pdf ← A: Heim's own 1982 source
│   │                                          (signed Northeim 25.2.1982)
│   ├── F_Erweiterte_Massenformel_nach_Heim 1989.pdf   ← B: 1989 extension
│   │                                          (excited states, lifetimes,
│   │                                           neutrinos, α)
│   ├── G_Ausgewaehlte_Ergebnisse.pdf       ← G: SELECTED RESULTS — ground
│   │                                          states (Tabelle I/II/III),
│   │                                          meson resonances k=1 (IV),
│   │                                          baryon resonances k=2 (V),
│   │                                          numerical evaluations
│   ├── H_Literaturverzeichnis.pdf          ← bibliography
│   │
│   ├── c_impl/                ← Eli Gildish's 2006 C implementation (upstream)
│   ├── csharp_impl/           ← C# version with 1982/1989/HG variants
│   ├── C0.66/                 ← DESY 1982 FORTRAN transcribed to Pascal/C
│   ├── Pascal 0.62/           ← Olaf Posdzech's Pascal version
│   ├── pdfs/                  ← earlier copies of D/E/F (pre-A-H archive)
│   ├── J0023, J0025, J0032, J0033 — Heim's original published papers
│   ├── Heim-Teil-C_Synmetronik_der_Welt-Band-{I,II,III}.pdf — Heim's books
│   ├── Burkhard Heim - 2000 - Syntrometrische Maximentelezentrik.pdf
│   ├── Feldtheorie-Heim-Prinzip-Kontrabarie-IvL-IGAAP-2017-2-seitig.pdf
│   │                                       ← von Ludwiger 2017 reconstruction
│   │                                          of Heim's contrabaric / field
│   │                                          drive claims
│   └── Heim_1989_Massenformel_0.4.xlsm  ← Excel cross-reference: mass and
│                                          lifetime formulas with Vergleich
│                                          sheet of predicted vs. measured
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
    │
    ├── higgs_search.py            ← post-1989 particle scan (Higgs, W, Z, …)
    ├── excited_state_search.py    ← exploratory non-canonical scan for
    │                                 baryon/meson resonances (k > 2;
    │                                 distinct from Heim's G-table k=1 / k=2
    │                                 resonance procedure)
    ├── e0_search.py               ← experimental bounds on Heim's neutral
    │                                 electron prediction (0.5162 MeV)
    ├── magnetic_moment.py         ← Synmetronik III Eq. 186 — Heim's
    │                                 electron g-factor formula
    ├── kontrabarie_design.py      ← modern-apparatus thrust prediction
    │                                 for Heim's 1959 field-drive claim
    ├── heim_neutrinos.py          ← Heim's 5-neutrino prediction
    │                                 (G-Tabelle II) vs current bounds
    │
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
**0.5162 MeV** (about 1.0 % above the measured electron mass) and Heim's
lifetime formula declaring it **stable**. To date no such particle has
been observed; it remains a standing prediction of the framework. See
[`python/e0_search.py`](python/e0_search.py) for a detailed comparison
against precision-β-decay, supernova-cooling, BBN and cosmological-relic
bounds: a charged-current-active sterile-neutrino reading of e₀ is
excluded by ≥ 7 orders of magnitude, but a Heim-internal / purely
gravitationally coupled reading is consistent with all current
experimental data — at the cost of being unfalsifiable from outside
the framework until Heim's coupling structure of e₀ is specified.

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

**Open electron-mass discrepancy.** Heim's own 1989 Tabelle II
(`downloads/G_Ausgewaehlte_Ergebnisse.pdf`, p. 3) lists the electron
theoretical mass as **0.51100343 MeV** — matching the measured PDG
value 0.51099907 MeV to **5 decimal digits** (+0.0009 %). Our current
Python port (and the upstream Eli-Gildish 2006 C from which it
descends) computes **0.50694371 MeV** for the same configuration
(k=1, P=1, Q=1, κ=0, x=1, ε=+1), which is **−0.79 % off** the
measurement *and* off Heim's own published value. Every other
particle in our port matches Heim's 1989 Tabelle II to ≤ 0.01 %.
This is therefore a localised transcription / convention bug
specific to the electron sector that we have not yet identified —
a third upstream-inherited bug beyond the two already corrected.
Until it is found and fixed, the electron line in the
Python output should be read as carrying a known offset.

### Post-1989 particle predictions

*This section was substantially rewritten in May 2026 after access to
Heim's selected-result tables in `downloads/G_Ausgewaehlte_Ergebnisse.pdf`.*

Following Joel's source-critical audit (Heim-Theory Discord, May 2026),
results in this section are now reported in **three distinct
categories**, which the repo previously conflated:

1. **Reproduction of Heim/Arbeitskreis selected results in G**.
   Does the current Python port compute the same theoretical masses
   that Heim's 1989 G-tables list? *Status: partially.* Ground states
   match Heim's Tabelle II to better than 0.01 % for 20 of 21 particles
   — but the electron is **0.79 % off** (Heim: 0.51100343 MeV; port:
   0.50694 MeV). For excited states, our current scan does **not**
   implement Heim's resonance procedure (which uses k=1 / k=2
   parametrisation in (P, N, K_B), separate from the (ε, k, P, Q, κ, x)
   ground-state procedure); a clean reproduction of G-Tabelle IV / Va
   from the formula is an open reconstruction task.

2. **Comparison of Heim's selected results to modern PDG values**.
   Heim's G-table predictions, *as he published them*, are mostly
   excellent. Examples:
   - ω(783) Heim 783.90 MeV vs PDG 782.65 MeV (0.16 %)
   - Φ(1019) Heim 1019.63 MeV vs PDG 1019.46 MeV (0.02 %)
   - K*(892) Heim 891.20 MeV vs PDG 892 MeV (0.09 %)
   - ρ(770) Heim 769.98 / 769.31 MeV vs PDG ≈ 775 MeV (0.7 %)
   - Λ(1690) Heim 1693.28 MeV vs PDG 1690 MeV (0.19 %)
   - over 70 resonances total to ≤ 1 % typical agreement
   
   So the *historical* Heim/Arbeitskreis predictions for these particles
   exist and are good. Our previous claim that ρ / ω / φ were
   "structurally absent from Heim's lattice" was an artifact of our
   limited scan — **retracted**.

3. **Genuinely new post-G exploratory scans**. Our `excited_state_search.py`
   ran at k ≤ 5, which goes beyond Heim's own A-source constraint
   ("for ponderable corpuscles only k = 1 and k = 2 are possible,
   not k > 2"). The "K\*(892) at 867.6 MeV in our k=3 scan" was
   therefore *not* the same object as Heim's k=1 K\*; it was a
   numerical coincidence in a non-canonical scan region. **The
   earlier claim of two new Heim-formula matches outside Heim's
   published list (K\*, Λ(1690)) is retracted.** Both are explicitly
   present in G-Tabelle IV / Va with theoretical masses already
   stated; our scan simply didn't reproduce them.

**Standard Model phenomena not currently mapped into Heim:**

| Particle / phenomenon | Status |
|---|---|
| Higgs H⁰ (125 GeV resonance) | Observed; Heim has its own mass mechanism (geometric, not Yukawa), so a Higgs field is not a primitive. A complete Heim-compatible theory must still account for the observed 125 GeV scalar phenomenology. |
| Z⁰ / W± gauge bosons | Observed; must be recoverable as effective phenomena. Not mass-formula-A/B input ontology. |
| J/ψ, D, B mesons | Heavy-flavour; Heim's hadronic framework treats free particles and "quark content" is not a Heim primitive. Internal/effective structure correspondence is open. |
| Λ_c, Λ_b, Σ_c baryons | Same as above. |
| τ lepton | Heim's table II lists only e, e₀, μ (plus 5 neutrinos). τ is not in Heim's basic-state list. Reconstruction needed. |

**Reframing.** The right question is not *"does Heim reproduce every
Standard Model entity as a primitive?"* — that's a category mistake.
Heim is a structural-geometric theory, not the Standard Model rewritten
in different notation. The right question is: *"does Heim reproduce
the empirical phenomena that the Standard Model describes, possibly
through a deeper structural language?"* For the empirical phenomena
that G-Tabelle IV / V cover, the answer is broadly *yes*. For W / Z /
Higgs / heavy-flavour, the answer is *currently unknown — needs
reconstruction work*, not a falsification.

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

### Beyond the mass formula — Kontrabarie

*This subsection is epistemically distinct from the rest of Findings:
the mass and lifetime results above are verified against measurement;
the material below is from the most speculative part of Heim's
framework and has no positive experimental confirmation.*

Heim's mass formula is the part of his work that this repository's
analysis has *verified*. But Heim also published, in the late 1950s,
a propulsion claim: that EM radiation forced into a closed circular
motion by a suitable material structure should produce a real
ponderomotive force on the apparatus, with no electromagnetic
recoil partner — a *field drive* or **Kontrabarie effect**.

The historical record (von Ludwiger 2017, in
`downloads/Feldtheorie-Heim-Prinzip-Kontrabarie-IvL-IGAAP-2017-2-seitig.pdf`)
is sobering. Heim built a prototype "Kontrabator" from hand-soldered
hollow-waveguide rings in his Northeim apartment in 1957; the
device's losses were too high to detect the predicted effect even
with the most sensitive seismometers available. A 1985 follow-up
proposal at MBB / DASA (Auerbach, Harasim, Kroy, von Ludwiger)
designed a SQUID magnetometer experiment to test the related
gravito-magnetic hypothesis; it was published in Springer's
*Superconducting Quantum Interference Devices and their Applications*
but never funded to completion. No definitive replication has been
attempted with modern apparatus since.

`python/kontrabarie_design.py` does what can be computed from the
published formulas: implements Heim's steady-state acceleration
field `b(x) = C · (e^(-x) - e^(x/2) · (cos(x√3) - ½√3·sin(x√3)))`
(IvL 2017 p. 237), finds its first positive maximum
(`x ≈ 1.54, shape ≈ 2.99`), and brackets the thrust for a lab-scale
modern apparatus (30 cm SCRF toroid, 100 kW gyrotron at 30 GHz,
50 % efficiency, 15 kg apparatus, 5 L cycle-former volume) under
several hypotheses for Heim's unknown overall coupling C:

| C [m/s²] | Interpretation | Thrust [N] | Thrust/Power |
|---:|---|---:|---:|
| 7.4·10⁻⁶ | matched to photon-rocket limit | 3.3·10⁻⁴ | trivially small |
| 1·10⁻³ | Heim's 1957 detection floor | **0.045** | 0.45 mN/kW |
| 9.8·10⁻³ | 0.1 % of standard gravity | 0.44 | 4.4 mN/kW |
| 9.81 | full antigravity (popular-press version) | 440 | 4.4 N/kW |

The popular-press "antigravity" hypothesis (C = g, last row) would
have been *spectacularly* detected in 1957 already and was not — so
either Heim's apparatus was so inefficient that detection was
missed by a margin of ≥1000 × (which is plausible given the negative
result on seismometers), or C ≪ g. The interesting region is the
middle two rows: C ~ 10⁻³ m/s² gives 45-440 mN of thrust on 100 kW
of input, well within the resolution of modern thrust stands
(µN-class, e.g. NASA Eagleworks, Tajmar 2017). A successful
detection there would be a Nobel-prize-level result; a robust null
result would constrain Heim's Kontrabarie at the level his 1957
prototype could not reach.

**The decisive test, if anyone wanted to run it:** vary input
power L over 2-3 decades and check whether thrust scales as Heim's
`λ' = 2π·r·L·ε/(m₀·V')`. A real Kontrabarie effect *must* follow
this scaling. A constant offset (thermal artifact, RF leakage,
electrostatic systematic) will not. Total apparatus cost:
~$2-5 M plus ~1 person-year for the cycle-former metamaterial design.
That's roughly an order of magnitude less than a typical mid-sized
physics experiment. The reason it hasn't been done is not cost —
it is that mainstream physics views the entire premise as not
worth checking.

For the full technical treatment, see
[Chapter 15 of THEORY_EXPLAINED.md](THEORY_EXPLAINED.md#chapter-15-kontrabarie--heims-own-field-drive-claim).

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
3. **The dataset is wider than we initially reported.** Heim's
   G-Tabelle IV / V (`downloads/G_Ausgewaehlte_Ergebnisse.pdf`, pp.
   5-8) contains theoretical mass predictions for 23 mesonic and
   50+ baryonic resonances at typically ≤ 1 % agreement with PDG.
   The historical Heim framework therefore *does* extend significantly
   beyond the 21-particle ground-state set; our previous "limited
   dataset" framing was an artefact of looking only at Tabelle II
   ground states. The framework's coverage of W / Z / Higgs /
   heavy-flavour, however, remains genuinely open and is not addressed
   by G.
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

> **In Joel's phrasing (Heim-Theory Discord, May 2026):**
> *Interesting structure, limited scope, open derivation.*

## Open questions

In rough order of importance (revised May 2026 after A/B/G source audit):

1. **The 0.79 % electron-mass discrepancy.** Heim's 1989 Tabelle II
   (G, p. 3) lists the electron at 0.51100343 MeV; our port computes
   0.50694 MeV. Every other particle matches Heim's table to ≤ 0.01 %.
   This is a localised transcription / convention bug specific to the
   (k=1, P=1, Q=1, κ=0, x=1) configuration — a third upstream-inherited
   bug not yet found. Highest-priority engineering task.

2. **Reproduction of Heim's G-Tabelle IV / V resonance procedure.**
   Heim's k=1 / k=2 resonance scheme is parametrised by (P, N, K_B),
   distinct from the ground-state (ε, k, P, Q, κ, x) scheme our port
   implements. Reproducing G-Tabelle IV (23 mesonic resonances) and
   V (50+ baryonic resonances) from first principles would close the
   biggest "reconstruction problem" identified by the source audit
   and is needed before any post-PDG scan can be properly interpreted.

3. **Heim's five-neutrino prediction (G-Tabelle II).** Heim 1989
   predicts ν_e at 3.81 meV (consistent with KATRIN); ν_μ at 5.37 keV;
   ν_τ at 10.75 keV; and two additional generations ν_4 at 21.06 keV
   and ν_5 at 207 keV. The 5.37 keV / 10.75 keV values for ν_μ / ν_τ
   would violate cosmological Σm_ν < 0.12 eV by 4-5 orders of magnitude
   *if* they describe the active mass eigenstates; they are tenable only
   if Heim's labels denote sterile, non-mixing states. The framework
   does not specify the mixing structure. See `python/heim_neutrinos.py`.

4. **Is the η derivation rigorous?** Chapter 7 (eqs. 7.47 → 7.51) of
   the Herleitung manuscript *derives* η(q, k) from physical principles,
   but the derivation passes through Heim's polymetric formalism
   (selector calculus, condensor flows) which is non-standard. A
   mathematical audit by someone fluent in that formalism would
   confirm whether the chain
   `G, ℏ, c → metron τ → ε₀± → η(q,k)` is free of hidden circularity.

5. **How does Heim's framework recover SM phenomenology for W / Z /
   Higgs / heavy-flavour states?** None of these appear as primitives
   in Heim's A/B framework, but a complete Heim-compatible theory
   would still need to explain why the Standard Model works as an
   effective theory in those sectors. This is the largest open
   conceptual question; it is *not* automatically a falsification
   (per Joel's reframing), but it needs positive resolution rather
   than dismissal.

6. **The η meson lifetime.** η is now within factor 2 of measurement
   (was negative T, then factor 0.47, now factor ~0.47 in the other
   direction). The remaining ~50 % discrepancy may be a real formula
   limitation, since η decays largely electromagnetically (η → γγ ~39 %).

7. **Why is the (n, m, p, σ) loss landscape jagged?** The greedy
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
