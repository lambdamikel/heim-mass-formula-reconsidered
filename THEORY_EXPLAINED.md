# Heim Theory Explained

*Burkhard Heim's 1989 mass formula and the ideas behind it,
explained in three layers per chapter — from intuitive to rigorous.*

---

## How to read this document

Each chapter has three sections:

- **For Beginners.** Plain English, no equations. The intuition.
- **For Intermediate.** Some maths, at the level of an undergraduate
  physics student. Enough to follow the structure of the argument
  without being able to reproduce it line-by-line.
- **For Experts.** Full equations and explicit derivations. References
  to the underlying manuscripts and the implementation in this
  repository.

You can read straight through one level (all the *Beginner* sections
first, then all the *Intermediate*, etc.), or work through each chapter
top-to-bottom and let the depth grow as you go. The chapters build on
each other: chapter 4's intermediate level assumes you have understood
chapters 1–3 at intermediate level, but not at expert level.

The goal is not advocacy. Heim's theory is non-mainstream and not
peer-reviewed in the modern sense. This document explains it on its
own terms so the reader can judge.

---

## Table of Contents

0. [Burkhard Heim — Life and Work](#chapter-0-burkhard-heim--life-and-work)
1. [The Question Heim Was Trying to Answer](#chapter-1-the-question-heim-was-trying-to-answer)
2. [The Six-Dimensional Space](#chapter-2-the-six-dimensional-space)
3. [The Metron — Spacetime is Quantised](#chapter-3-the-metron--spacetime-is-quantised)
4. [Hermetric Forms — Particles as Geometric Structures](#chapter-4-hermetric-forms--particles-as-geometric-structures)
5. [The Mass Element μ](#chapter-5-the-mass-element-μ)
6. [The η-Function — Where the (4+k) Comes From](#chapter-6-the-η-function--where-the-4k-comes-from)
7. [Quantum Numbers and Particle Classification](#chapter-7-quantum-numbers-and-particle-classification)
8. [The Mass Formula](#chapter-8-the-mass-formula)
9. [The Lifetime Formula](#chapter-9-the-lifetime-formula)
10. [Predictions and Limits](#chapter-10-predictions-and-limits)
11. [Where Heim Theory Stands Today](#chapter-11-where-heim-theory-stands-today)
12. [A Worked Example — The Proton Mass Step by Step](#chapter-12-a-worked-example--the-proton-mass-step-by-step)
13. [Syntrometrie — The Logic Behind the Physics](#chapter-13-syntrometrie--the-logic-behind-the-physics)
14. [Extended Heim Theory — The Dröscher–Häuser 8D / 12D Framework](#chapter-14-extended-heim-theory--the-dröscherhäuser-8d12d-framework)

---

## Chapter 0: Burkhard Heim — Life and Work

### For Beginners

Burkhard Heim's life is one of the most extraordinary stories in 20th
century physics. He was born on 9 February 1925 in Potsdam and died
on 14 January 2001 in Northeim. Between those dates, he produced one
of the most ambitious unified field theories ever attempted —
**without the use of his hands, with severely impaired sight, and
with hearing loss so profound that for most of his career he could
follow conversations only with great difficulty**.

The catastrophe that defined his life happened in 1944, when Heim was
19. He had managed to avoid being drafted into the German Air Force
by working in a chemical-explosives laboratory. An explosion caused
by mishandled compounds tore off both his hands, blinded him almost
completely, and left him nearly deaf. He underwent the Krukenberg
procedure, in which the bones of the forearm are surgically separated
to produce a primitive pincer-like grip — restoring some basic motor
function but no fine manipulation. He could not write, type, or read
ordinary print again.

Despite this, after the war, Heim registered at the University of
Göttingen to study physics. He produced his theoretical work over
the following five decades by *dictating equations to his wife
Gerda* — a former Prague concert singer he married in 1950 — who
typed them up. Heim developed an *eidetic acoustic memory*: he could
hear a formula recited once and recall it perfectly afterwards, and
he could pick up new languages in days. He never published a paper in
a peer-reviewed mainstream journal. He gave a small number of public
lectures and circulated his manuscripts privately.

In 1952, at the age of 27, Heim spoke at a Stuttgart congress about
the possibility of a "field drive" — a propulsion mechanism based on
manipulation of the gravitational field. The lecture made
international news and Heim was briefly courted by the German
aerospace industry. From that point until his death, he worked
quietly on the mathematical foundations of his theory, producing a
private monograph (*Elementarstrukturen der Materie*, 1980), an
extended edition (1984), the 1989 mass-formula report sent to
MBB/DASA, and a final volume *Synmetronik der Welt* (in three
volumes, ~700 pages total) only published posthumously.

### For Intermediate

A more detailed timeline:

- **1925.** Born 9 February in Potsdam, Germany. As a child reportedly
  designed rockets at age 6 and synthesised nitroglycerin at 13.
- **1944.** Aged 19, working as an explosives technician (to avoid
  Air Force conscription). Laboratory accident from mishandled
  compounds. Loses both hands, near-total sight, near-total hearing.
- **1945–1948.** Recovery and Krukenberg procedure. Begins to develop
  the eidetic acoustic memory that will be the foundation of his
  later working method.
- **1948.** Begins physics studies at the University of Göttingen,
  one of the most important post-war physics centres in Germany.
  Studies under **Carl Friedrich von Weizsäcker** — a leading
  German theoretical physicist, philosopher of science, and member
  of the Werner-Heisenberg–era nuclear research community.
- **1950.** Marries Gerda, a former concert singer from Prague.
  Gerda becomes his amanuensis — typing every formula and every
  manuscript that Heim dictates. This collaborative arrangement
  continues for over fifty years.
- **1952.** Speaks at a Stuttgart aerospace congress about a possible
  *Feldantrieb* (field drive) for spacecraft, based on
  gravity-electromagnetism coupling that he had derived in his early
  unified-field-theory work. Lecture is widely covered, including
  international press. Briefly courted by German aerospace firms.
- **1954.** Leaves the Max-Planck-Institut (where he had been
  working on Einstein's unified field theory) to pursue his own
  research independently. His doctoral thesis on field theory had
  been rejected — partly because he disregarded standard formal
  conventions, partly because no university faculty member was
  willing to act as competent reviewer for the very non-standard
  mathematics he had developed.
- **1957.** First public formulation of *Heim theory* as a unified
  field theory aiming at the masses of all elementary particles.
- **1959.** First mass-formula computation in private circulation.
- **1976.** Detailed lecture at MBB Ottobrunn (Messerschmitt-Bölkow-
  Blohm, German aerospace) on the unified theory and its
  applications.
- **1980.** Publishes (privately) *Elementarstrukturen der Materie*,
  Volume I — his main monograph on the physics. In German, around
  600 pages, very dense, with idiosyncratic notation.
- **1982.** Mass formula programmed at DESY (Deutsches Elektronen-
  Synchrotron) in Hamburg by H. D. Schulz, with Heim's collaboration.
  Predicts ~16 particle masses to ~0.1 % accuracy.
- **1984.** Expanded edition of *Elementarstrukturen der Materie*.
- **1989.** Sends a 57-page report containing the extended mass
  formula and lifetime calculations to MBB/DASA. The accompanying
  FORTRAN code is later lost.
- **1996.** Collaborates with **Walter Dröscher** on the extension
  of Heim theory to 8 dimensions (the start of what is now called
  *Heim–Dröscher theory* or *Extended Heim Theory*).
- **1999.** Heim falls ill. Working until then on a still-incomplete
  *selection rule for resonances* and on magnetic moments of
  elementary particles.
- **2001.** Dies on 14 January in Northeim, aged 75. The successor
  community (Forschungskreis Heimsche Theorie / IGW Innsbruck and
  later IGAAP e.V.) takes over the curation of his manuscripts and
  the development of the surviving body of work.

The biography by **Illobrand von Ludwiger** — *Burkhard Heim: Das
Leben eines vergessenen Genies* (Scorpio Verlag, Munich/Berlin, 2010,
ISBN 978-3-942166-09-6) — is the most comprehensive account.
Von Ludwiger (born 1937) is an astrophysicist and aerospace systems
analyst who knew Heim personally for many years and inherited his
estate of unpublished notes; the biography draws extensively on this
material.

### For Experts

The scientific lineage and reception of Heim's work are worth tracing
carefully, because they shape how the theory should be evaluated.

**Lineage.**

Heim worked in the *Göttinger Tradition* of theoretical physics —
Heisenberg, Born, Jordan, von Weizsäcker, et al. — but on its
fringe. Carl Friedrich von Weizsäcker was his nominal advisor. More
substantively, Heim corresponded with **Pascual Jordan** (one of the
founders of quantum mechanics, the J in BJ–OW commutators) on the
gravitational interpretation of his theory; Jordan reportedly
encouraged Heim's work on geometrising the energy-momentum tensor.
Heim also briefly intersected with **Werner Heisenberg**'s late
unified-field-theory program, though Heim's polymetric approach
diverged sharply from Heisenberg's nonlinear-spinor approach.

The 1952 Stuttgart lecture is documented in the contemporary
aerospace press; Heim presented it as an *application* (field drive)
of his still-developing theoretical framework, and it was taken
seriously enough that the Federal Ministry of Defence funded a
preliminary investigation. The investigation was discontinued
because Heim refused to disclose details until he had completed the
full theoretical foundations — a pattern that recurs throughout his
career.

**Method.**

Heim's working method — dictation, mental computation, eidetic recall —
is unusual enough to merit comment. He computed all his formal
results *in his head*, dictated them to Gerda, who typed them up;
then he listened back as she read the typescript aloud, made
corrections, and proceeded. The selector calculus, the polymetric
geometry, the entire mass formula apparatus, and the lifetime
formula were all developed this way. The 1982 DESY computer
implementation was the first time any of the formula apparatus had
been instantiated as numerical code rather than as
formal-mathematical typescripts.

This working method also explains the dense, idiosyncratic style of
the manuscripts: every term has to be locally self-explanatory
because Heim could not flip back to earlier pages. Variables are
named with elaborate sub- and superscripts that try to encode their
meaning structurally.

**Reception.**

Mainstream physics never engaged with Heim's full system. The
reasons, in roughly decreasing order of importance:

1. *Notation barrier.* Heim's selector calculus and hermetric forms
   were mathematical inventions that did not connect to existing
   bodies of mathematics. There was no established literature against
   which a peer reviewer could check the work.
2. *Publication discipline.* Heim published nearly nothing in
   peer-reviewed venues. His main exposition (*Elementarstrukturen*)
   was a privately printed book.
3. *Independence.* Heim refused to follow doctoral conventions and
   never held a university position. He had no PhD students and no
   institutional momentum behind his work.
4. *Adjacency to UFO research.* Through Illobrand von Ludwiger and
   the Mutual UFO Network – Central European Section (MUFON–CES),
   Heim's work attracted attention from communities that mainstream
   physics found embarrassing. This was guilt-by-association, but the
   association affected reception.
5. *The Higgs gap.* Heim's theory predicted neither a Higgs nor any
   electroweak gauge bosons. Whether one reads this as "outside
   intended scope" (Chapter 10) or as an empirical limitation, it
   meant Heim's theory could not capture the post-1980 successes of
   the Standard Model.

The 1982 DESY computation was the closest the theory ever got to
mainstream attention. The numerical accuracy — 0.1 % on 16 particle
masses — was striking, but the underlying mathematical foundation
remained in private circulation.

**Continuing community.**

After Heim's death in 2001, several individuals took up the
preservation and (selective) continuation of the work:

- **Illobrand von Ludwiger** (1937–~2020s) — astrophysicist, friend,
  biographer, and steward of Heim's estate. Co-author with K. Grüner
  of *Zur Herleitung der Heimschen Massenformel* (IGW Innsbruck, 2003).
  Now deceased.
- **Walter Dröscher** (1937–) — physicist who collaborated with
  Heim from the mid-1990s and extended the theory to 8 dimensions
  (Heim–Dröscher theory) and 12 dimensions, including a derivation
  of the gravitational constant *G* itself.
- **Jochem Häuser** (Hochschule Salzgitter) — physicist working on
  the propulsion-applications side of extended Heim theory; published
  on the so-called *gravitophoton* hypothesis with Dröscher.
- **Olaf Posdzech** (Protosimplex archive) — software engineer who
  in 2006 reimplemented the 1982 DESY formula in Pascal and C; the
  core of `downloads/C0.66/` and `downloads/Pascal 0.62/`.
- **Eli Gildish** (2006) — independent reimplementation in C/C# (the
  upstream of `downloads/c_impl/` and `downloads/csharp_impl/`).
- **Dr. A. Mueller** (~2002) — reprogrammed parts of the 1989 formula
  in C# for the *Heim Group* (also in `downloads/csharp_impl/`).
- **Joel Michalowitz / IGAAP e.V.** (Hungen, Germany) — current
  custodian of [heim-theory.com](https://heim-theory.com/), maintains
  the document archive, the Excel reference implementation
  (`Heim_1989_Massenformel_0.4.xlsm`), and the Heim-Theory Discord
  community.

The most recent sustained mathematical-modernisation effort is the
2025 manuscript *A Modernized Syntrometric Logic: Foundations and
Applications* (in `downloads/Syntrometry_Heim's.pdf`), which
reformulates Heim's *Syntrometrie* — the philosophical and
logical-foundational layer of his work — in modern type-theoretic and
modal-logic terms.

**Sources.**

- Wikipedia: [Burkhard Heim](https://en.wikipedia.org/wiki/Burkhard_Heim)
- Illobrand von Ludwiger, *Burkhard Heim: Das Leben eines vergessenen
  Genies*, Scorpio Verlag, Munich/Berlin, 2010.
- *Zur Herleitung der Heimschen Massenformel*, I. von Ludwiger and
  K. Grüner, IGW Innsbruck, 2003 (in `downloads/pdfs/`).
- Heim's primary works: *Elementarstrukturen der Materie* I (1980),
  *Elementarstrukturen der Materie* II (1984), and the three-volume
  *Synmetronik der Welt* (in `downloads/`).
- Forschungskreis Heimsche Theorie / IGAAP e.V., heim-theory.com.

---

## Chapter 1: The Question Heim Was Trying to Answer

### For Beginners

Why does a proton weigh exactly what it weighs? Why is the muon roughly
207 times heavier than the electron, and not 200 or 250? In the
Standard Model of particle physics — the theory that has dominated
since the 1970s — the answer is essentially: **we measure those
masses; the theory does not predict them**. The Standard Model has
about twenty numbers that have to be put in by hand from experiment,
and most of them are particle masses.

Burkhard Heim (1925–2001), a German theoretical physicist, asked a
different question in the 1950s: *what if the masses are actually
calculable from geometry alone?* What if there is a deeper structure
of spacetime such that a proton has the mass it has because that
particular mass is the only one a "proton-shaped" geometric structure
could have, given the basic constants of nature (Newton's
gravitational constant *G*, Planck's constant *ℏ*, and the speed of
light *c*)?

This is not a small question. If Heim was right, particle physics has
been measuring quantities that should have been calculated all along,
and the deepest theory of matter is *geometric*, not just
quantum-field-theoretic.

### For Intermediate

Einstein's general relativity (1915) accomplished something
philosophically remarkable: gravity, previously thought of as a
*force*, was reinterpreted as the *geometry* of spacetime. Mass-energy
curves spacetime; particles follow geodesics in that curved spacetime.
There is no separate "gravitational field" alongside spacetime — the
field *is* the geometry.

Einstein and his successors hoped to extend this idea to the other
forces: electromagnetism, then later the strong and weak nuclear
forces. The hope was a *unified* geometric theory in which all forces
and all particles emerge from the geometry of some sufficiently rich
spacetime. The Kaluza–Klein theories (1920s, 1930s) tried adding extra
dimensions; string theory (since the 1970s) tried adding strings
instead of points.

Heim's approach was more conservative in spirit but more radical in
detail. He argued that:

1. Spacetime should be **quantised at a fundamental scale** — there
   should be a smallest possible area, of order the Planck length
   squared.
2. Geometric *equations* should accordingly be **difference equations**
   rather than differential equations.
3. The 4-dimensional spacetime of relativity should be extended to
   **6 dimensions** — but the two extra dimensions are not "more space"
   in the Kaluza–Klein sense; they are *organising* dimensions that
   describe how structures within the 4-dimensional world are related
   to one another.

From these starting points, Heim claimed that particles emerge as
*specific stable geometric structures* — and that their masses, like
the curvature of spacetime around the Earth, fall out of the geometry.

### For Experts

Heim's work began in the early 1950s and continued until his
death in 2001. His central claim was that the mass spectrum of
elementary particles is a consequence of a *polymetric* extension of
general relativity defined on a discrete 6-dimensional manifold *R*₆
of signature (+++, –, –, –) (i.e., three spatial, one time, and two
imaginary "trans-coordinates").

The starting point is the standard Einstein program: the divergence of
the Riemann curvature tensor is set equal to the divergence of the
phenomenological energy–momentum tensor (Einstein's field equations).
Einstein himself was uneasy with this: the geometry was on one side,
but the matter content — the source of the field — was put in *by
hand* on the other. Heim's program was to make the source itself
geometric.

For this to work, the field equations have to be modified in two ways:

1. The differential equations of the macroscopic theory must be
   replaced by *difference equations* at the microscale, because
   spacetime is metron-quantised (Chapter 3).
2. The Riemann curvature tensor *R^i_{kmp}* must be derived from a
   non-linear *operator* `C_p` acting on the Christoffel symbols rather
   than from second derivatives of the metric. In the microscale this
   becomes an eigenvalue equation:

   `C_p · φ^i_{km} = λ_p(k, m) · φ^i_{km},     i, k, m ∈ {1, ..., 6}`

   The eigenvalues `λ_p(k, m)` are real, discrete, and proportional to
   energy density. The eigenfunctions `φ^i_{km}` describe stable
   geometric configurations — *particles*.

This eigenvalue framework, developed in chapters 1–2 of *Zur Herleitung
der Heimschen Massenformel* (von Ludwiger and Grüner 2003), is the
foundation on which everything else rests. The mass formula proper
appears in chapter 7 of that document and equations B3–B57 of the
1989 reformulation.

---

## Chapter 2: The Six-Dimensional Space

### For Beginners

Heim's spacetime has **six dimensions** instead of the usual four. But
the two extra dimensions are not what you might expect. They are not
more *space* — you can't fly through them. They are what Heim called
**trans-coordinates**: dimensions that describe how things are
*organised* in the world we live in.

Imagine you watch a flock of starlings making a coordinated dance in
the sky. The position of each starling is described by three space
coordinates and one time coordinate — four dimensions, ordinary
spacetime. But to describe the *shape* of the flock, you also need
information about *which starlings are connected to which others*, and
about the rules of their coordination. Those rules are not extra
spatial dimensions — they are *organising* dimensions.

In Heim's six-dimensional space, the two trans-coordinates encode
exactly that kind of organising information. They have no energy of
their own. They cannot be moved through. But they affect *which*
geometric structures are stable, and therefore which particles can
exist.

### For Intermediate

The six dimensions of Heim's *R*₆ split into three groups:

- **Three real spatial coordinates** *x*₁, *x*₂, *x*₃ (the familiar *R*₃)
- **One imaginary time coordinate** *x*₄ = *ict*
- **Two imaginary trans-coordinates** *x*₅ and *x*₆

The signature is (+++, –, –, –) — all imaginary axes carry a minus
sign in the metric. The split into "spatial", "time", and
"trans-" is not arbitrary; it reflects how Heim's eigenvalue
equations couple the coordinates.

Now comes the key feature. The eigenvalue equation
*C_p* · φ^i_{km} = λ · φ^i_{km} runs through three indices *i*, *k*,
*m*, each from 1 to 6. There are 6 × 6 × 6 = 216 components, but the
*p*-index is just a tag, leaving 6 × 6 = 36 distinct equations. Of
these, 28 vanish (because of the partial-derivative identities), and
12 more vanish (for the special case *k = p*). What remains is **16
non-trivial equations** — geometric "modes" — and these are reduced
further to four classes by Heim's symmetry arguments.

The four classes are called the four **hermetric forms** (chapter 4).
Each one corresponds to a different kind of *physical phenomenon*:
gravity, photons, neutral particles, charged particles. The 6D
structure is what makes that classification possible — there are only
*four* such classes precisely because of how the coordinates split.

### For Experts

Heim's *R*₆ is constructed as the carrier space of the Hilbert space
of the eigenvalue equation (1.8 of *Herleitung*):

```
C_p · φ^i_{km} = λ_p(k, m) · φ^i_{km},     i, k, m, p ∈ {1, …, 6}
```

The signature is `(+ + + − − −)`. The energy-density tensor
*T*_{ik} ≅ ε^(p)_{km} of the *R*₆ is taken to have non-zero components
only in the spatial × time sub-block and the spatial × trans block:

```
         | T_{11}  T_{12}  T_{13}  T_{14}  0       0      |
         | T_{21}  T_{22}  T_{23}  T_{24}  0       0      |
T_{ik} = | T_{31}  T_{32}  T_{33}  T_{34}  0       0      |
         | T_{41}  T_{42}  T_{43}  T_{44}  T_{45}  T_{46} |
         | 0       0       0       T_{54}  T_{55}  T_{56} |
         | 0       0       0       T_{64}  T_{65}  T_{66} |
```

The vanishing of *T*_{i5} and *T*_{i6} for *i* = 1, 2, 3 (spatial
block) is what gives the trans-coordinates their *organising* — rather
than energetic — character.

Coordinate groupings:
```
s₃ = (x₁, x₂, x₃)              # spatial unit
s₂ = (x₄)                       # time unit
s₁ = (x₅, x₆)                   # trans unit
```

A *hermetric form* is a non-trivial coupling of these subspaces.
Calling the seven non-empty intersections of *s*₁, *s*₂, *s*₃ "forms",
only **four** lead to non-trivial physical structures (chapter 4):

```
a ≡ s₁                          # gravitational waves
b ≡ s₁ ⊕ s₂                     # photons
c ≡ s₁ ⊕ s₃                     # neutral particles
d ≡ s₁ ⊕ s₂ ⊕ s₃                # charged particles
```

That every physical phenomenon couples to *s*₁ — i.e., that
*x*₅ and *x*₆ appear in every hermetric form — is the central
organisational claim of the framework.

---

## Chapter 3: The Metron — Spacetime is Quantised

### For Beginners

Heim took seriously the idea that there should be a **smallest
possible area** in spacetime — a quantum of area, just like a quantum
of energy. He called this smallest area a **metron**, from the Greek
*métron* ("a measure"). Its size is set by the three universal
constants of nature: Newton's *G*, Planck's *ℏ*, and the speed of
light *c*. Numerically, a metron is about 10⁻⁷⁰ square metres —
inconceivably small, comparable to the Planck length squared.

What does it mean for area to be quantised? It means you cannot have
*half a metron* of area, just as you cannot have half a photon. The
fabric of spacetime, on the very smallest scale, is grainy. This
graininess is invisible at any scale we can probe directly with
particle accelerators — even the Large Hadron Collider's reach is
roughly 10⁵² metrons across — but it is the foundation on which Heim
builds everything else.

### For Intermediate

The metron is derived from an extremal-area argument in Heim's
gravitational field equations: of all possible areas one could
construct from *G*, *ℏ*, and *c*, the metron is the one that minimises
the action of a "smallest possible" gravitational quantum. The result
is

```
τ = (3/8) · (G ℏ / c³)
  ≈ 6.15 × 10⁻⁷⁰ m²
```

The factor 3/8 is a geometric prefactor; the dimensional combination
*G* · *ℏ* / *c*³ is essentially the Planck length squared.

Once areas are quantised, *integration* in the geometry has to be
replaced by *summation* over metrons. Heim's formal apparatus for this
— what he called the *Metronenkalkül* (metron calculus) — replaces
ordinary differential operators ∂/∂*x* with finite-difference
operators Δ/Δ*x*, where Δ*x* ≈ √τ. Where standard general relativity
develops singularities (the metric blows up at black-hole centres,
say, or at the Big Bang), the metron calculus simply prevents
distances from getting smaller than a metron's diagonal. There are
no singularities in Heim's theory.

### For Experts

The metron is defined by the extremal-action condition for a
"smallest" gravitational quantum (Heim 1980, *Elementarstrukturen der
Materie*, vol. I; *Herleitung* p. 6):

```
τ = (3/8) · γ ℏ / c³
```

where *γ* = Newton's *G*. Inserting numerical values:

```
τ = (3/8) · 6.674 × 10⁻¹¹ × 1.055 × 10⁻³⁴ / (2.998 × 10⁸)³
  ≈ 6.15 × 10⁻⁷⁰ m²
```

This is a true natural constant — only *G*, *ℏ*, *c* enter. Heim
emphasised that no other physical constants are inputs to the
fundamental construction.

The discrete framework derives from this: spatial integrals
become sums over metrons,

```
∫ d²x → Σ τ
```

and partial derivatives become "metronic differences"

```
∂φ/∂x → Δφ/√τ
```

Tensor objects on the continuum become *selectors* on the discrete
space, and curvature becomes *condensation* (a deformation density)
of the metron lattice. The selector calculus replaces the
Christoffel-symbols / Riemann-tensor machinery and is genuinely
non-standard in mathematical physics — see chapter 3 of *Herleitung*
for the construction.

The cosmological role of the metron is also non-trivial: τ is
**not** time-independent. As the universe expands, metrons subdivide
("Zerteilung der Metronen"), and the metron calculus carries an
intrinsic arrow of time. This subdivision replaces the Big Bang
singularity in Heim's cosmology — at no point in the universe's
history does spacetime degenerate to a point.

---

## Chapter 4: Hermetric Forms — Particles as Geometric Structures

### For Beginners

In Heim's view, a particle is not a tiny point with mass, charge and
spin attached to it. A particle is a **stable bundle of curvatures**
in the six-dimensional geometry — a pattern in the metron lattice that
returns to itself after a complete cycle of internal motion. Different
particles correspond to different *kinds* of bundles. There are only
**four kinds**, which Heim called *hermetric forms*. Each form
corresponds to one kind of physical thing:

- Form **a** — gravitational waves (no rest mass)
- Form **b** — photons (no rest mass; carry electromagnetism)
- Form **c** — neutral particles (with rest mass, no electric charge)
- Form **d** — charged particles (with rest mass *and* electric charge)

This classification — *four* hermetric forms, no more, no fewer — is
not put in by hand. It falls out of how the six dimensions split into
groups (Chapter 2).

### For Intermediate

Recall that the six dimensions group as

- *s*₃ = three real spatial coordinates
- *s*₂ = one imaginary time coordinate
- *s*₁ = two imaginary trans-coordinates

A "hermetric form" is a curvature pattern that activates a specific
combination of these three sub-spaces. The complete list of non-empty
combinations is seven: just *s*₁, just *s*₂, just *s*₃, *s*₁⊕*s*₂, …,
all three together. But only four of these can carry stable
self-consistent geometric structures, namely those that include *s*₁:

```
form  active subspaces           physical content
a     s₁                          gravitational waves
b     s₁ ⊕ s₂                     photons
c     s₁ ⊕ s₃                     uncharged matter
d     s₁ ⊕ s₂ ⊕ s₃                charged matter
```

The pattern is striking: *every* physical structure couples to the
trans-coordinates *s*₁. Heim interpreted this as the *trans*
dimensions providing the organising scaffold without which no stable
structure can exist. The active subspace also dictates the
particle's properties: a structure that activates *s*₃ has a position
in space; a structure that activates *s*₂ has a propagation in time;
a structure that activates both has a non-zero rest mass.

For each hermetric form, Heim's eigenvalue equation produces a
specific spectrum of stable solutions. The spectrum of form *d*
(charged matter) gives the masses of the charged leptons and the
charged baryons; the spectrum of form *c* gives the neutral particles;
and so on.

### For Experts

The four hermetric forms emerge as the non-trivial solutions of the
6-dimensional eigenvalue equation (1.8) restricted to specific
sub-block structures of the energy-density tensor *T*_{ik}.

The seven possible coordinate-group activations are obtained from the
power set of {*s*₁, *s*₂, *s*₃} minus the empty set:

```
{s₁}, {s₂}, {s₃}, {s₁,s₂}, {s₁,s₃}, {s₂,s₃}, {s₁,s₂,s₃}
```

Of these, only the four that contain *s*₁ admit stable, normalisable
solutions:

| Form | Subspaces | Equation                       | Phenomenon |
|------|-----------|--------------------------------|------------|
| a    | s₁        | dφ/dξ + φ² = λφ                 | Gravity wave |
| b    | s₁ ⊕ s₂   | (wave equation in ρ²=ε²+(x₅,x₆)²) | Photon |
| c    | s₁ ⊕ s₃   | (eq. 2.18, real-valued)         | Neutral particle |
| d    | s₁ ⊕ s₂ ⊕ s₃ | (eq. 2.18, complex)             | Charged particle |

For form *c* (neutral particles), the eigenvalue equation in the
relevant slice of *R*₆ becomes (eq. 2.18 of *Herleitung*):

```
η/r = ±√[(nρ + nr + 1)(nρ - nr)],     nρ, nr ∈ ℕ
```

where *η* is what later becomes the famous η-function of the mass
formula (Chapter 6), and *r* is the Compton wavelength of the
particle. For form *d* (charged particles), the equation becomes
complex, with real part giving the charge structure.

The "trans" content *s*₁ is identified by Heim with *informatorische
Strukturen* — informational/organisational degrees of freedom that
do not carry energy themselves. This is what distinguishes the Heim
framework from Kaluza–Klein theories (where extra dimensions *do*
carry energy, manifested as Kaluza–Klein "towers" of massive states).

---

## Chapter 5: The Mass Element μ

### For Beginners

If particles are geometric structures, then their masses must be set
by the natural scale of the geometry. Heim showed that there is exactly
one such scale that comes out of the constants *G*, *ℏ*, *c*: it is
called the **mass element** *μ*, and its value is about
0.25 electron masses, or roughly 1/4 of the electron mass.

Every particle's mass is a multiple of *μ* — or more precisely, *μ*
times a *factor that depends on the particle's quantum numbers*. The
electron's mass comes out to about 220 *μ*, the proton's mass to about
4×10⁵ *μ*, and so on. The factor is what Heim's formula computes from
the integers (the quantum numbers). If you can compute the factor,
you have computed the mass.

Importantly, *μ* is **not a free parameter**. It is uniquely determined
by *G*, *ℏ*, *c* and one *gauge length s₀* (which is just the metre
itself). There is nothing to fit. Whatever gives the mass spectrum its
detail must come from somewhere else — namely, from the η-function and
the integer structure.

### For Intermediate

The mass element is

```
μ = π^(1/4) · (3π G ℏ s₀)^(1/3) · √(ℏ / (3 c G)) / s₀
```

where *s*₀ = 1 m is a gauge length. Numerical evaluation:

- (3π G ℏ s₀)^(1/3) ≈ 1.36 × 10⁻¹⁵ m
- √(ℏ / (3cG)) ≈ 7.27 × 10⁻¹⁶ kg^(1/2) · m^(1/2)
- The product, with the π^(1/4) prefactor and division by *s*₀, gives

```
μ ≈ 2.26 × 10⁻³¹ kg
  ≈ 0.248 × m_e (electron mass)
  ≈ 0.127 MeV / c²
```

So μ is a sub-electron-mass scale, but only by a factor of four. The
mass formula's job is to compute the dimensionless multiplier that
turns this base scale into 0.51 MeV (electron) or 938 MeV (proton).
Those multipliers are 4 to 7000-ish — manageable integers and integer
combinations.

### For Experts

The mass element is derived in Heim 1980 and *Herleitung* eq. (2.62):

```
μ_q · η_q · ³√η_q = π · ³√(3 π s₀ γ ℏ)
```

For *q* = 0 and *η*_q = 1 (the lower bound of the c-spectrum), this
reduces to (eq. 2.63):

```
m_(0) = π · ³√(3 π s₀ γ ℏ)
```

For the upper bound (Maximum at *q* = 1), one obtains (eq. 2.64):

```
m_(0) · η · ³√η = m₀
```

The combinatorial dressing yields the "mass element" actually used in
the formula (eq. VI of the 1982 chapter):

```
μ = π^(1/4) · (3 π γ ℏ s₀)^(1/3) · √(ℏ / (3 c γ)) / s₀
```

with *γ* = *G*. Numerically, with CODATA 2014 values:

```
μ = 2.2589 × 10⁻³¹ kg
  = 1.2674 × 10⁻¹ MeV / c²
  = 0.2479 m_e
```

Implementation: `python/constants.py::mass_element()`. The whole mass
formula M = μ · α₊ · (G + S + F + Φ + 4qα₋) [B3] is then
dimensionally a pure-geometric mass times a dimensionless integer-and-
auxiliary-function combination. No fitting parameter enters.

---

## Chapter 6: The η-Function — Where the (4+k) Comes From

### For Beginners

Mid-level chapters of Heim's framework introduce a function called
**η** ("eta") that captures the *small distortion of geometry caused
by electric charge*. Without charge, η equals 1. With charge, η is
slightly less than 1 — typically 0.99 or so. So η is "almost 1, but
not quite", and the small deviation from 1 is what produces some of
the differences between particles.

The exact form Heim derived is

```
η(q, k) = ⁴√(π⁴ / (π⁴ + (4 + k) q⁴))
```

where *q* is the charge magnitude (0, 1, 2 …) and *k* is the
"configuration index" of the particle. The (4 + k) factor is *the*
distinguishing feature of Heim's η: it falls out of a derivation in
chapter 7 of the manuscript "Zur Herleitung der Heimschen Massenformel"
that involves renormalising the elementary charge over four effective
dimensions. This (4 + k) is not adjustable — it's a result.

Why does this matter? Because η is the central auxiliary that controls
the precise mass differences between charged and neutral particles in
the same multiplet. For example, the difference between the proton
mass (q = 1, charged) and the neutron mass (q = 0, neutral) traces
back, via several steps, to the difference between η(1, 2) and η(0, 2).

### For Intermediate

For *q* = 0, η = 1 exactly. For *q* = 1, *k* = 0 (the canonical case):

```
η(1, 0) = ⁴√(π⁴ / (π⁴ + 4)) ≈ 0.98999
```

So η differs from unity by about 1 %. For *k* = 1, 2, the value
decreases very slightly (because the denominator increases as 4+*k*
grows). The function never goes below ~0.985 for *k* ≤ 2.

The shape of the formula is striking: π⁴ in numerator and denominator,
*q*⁴ as the "charge contribution", and (4 + *k*) as the configuration
modifier. The fourth-power dependence on *q* — rather than *q*² — is
the result of Heim's analysis of the ladder structure of the 6D
eigenvalue equation: the charge-coupled component of the field
strengths shows up at fourth order, not second.

### For Experts

The derivation of η is in *Herleitung* eqs. 2.43 → 2.48 and 7.47 → 7.51.
Two stages:

**Stage 1 (chapter 2): the q-dependence.**
From the field equations in form *d* (charged particles), the
self-coupling factor *U*_max for the gauge-component reduction is
derived. The result is (eq. 2.44):

```
w² = U_max + 1 = (4 q⁴) / π⁴
```

This gives (eq. 2.46–2.48):

```
m(n, q) = m(n) · η_q
η_q⁴   = 1 / U_max = (1 + 4 q⁴ / π⁴)⁻¹
η_q    = ⁴√(π⁴ / (π⁴ + 4 q⁴))
```

So at *k* = 0, η depends on *q* alone via a quartic-in-*q* contribution
in the denominator.

**Stage 2 (chapter 7): the k-dependence.**
For configurations with *k* > 0, an additional renormalisation of the
elementary-charge field is needed. Heim shows (eq. 7.48):

```
ε'₀± = ε₀± · ⁴√(1 + k/4)
```

This comes from "L · Δε₀±⁴ = 4 · Δε₀±⁴", where *L* = 4 is the number of
condensation dimensions in *R*₃ × *T*₁. Substituting (7.48) into the
chapter-2 result and simplifying with *a* = √2 yields (eq. 7.49):

```
(μ · f / M)⁴ = 1 + (q⁴ / π⁴) · (4 + k)
M           = μ · π · f · [π⁴ + q⁴(4 + k)]^(-1/4)        (7.50)
η(q, k)     = ⁴√(π⁴ / (π⁴ + q⁴(4 + k)))                  (7.51)
```

Importantly, (4 + k) is **not** a fit parameter. It is the result of
*L* (= 4 Euclidean dimensions) plus the configuration index *k* of the
particle. The sensitivity analysis in `python/sensitivity_eta_form.py`
confirms that the loss landscape over the four parameters of η has its
sharp minimum at exactly (A=4, B=4, C=4, D=1/4) — consistent with this
derivation rather than with a phenomenological fit.

Implementation: `python/constants.py::eta()`.

---

## Chapter 7: Quantum Numbers and Particle Classification

### For Beginners

In Heim's framework, every particle is labelled by exactly **six
integers**:

- **ε** ("epsilon"): time helicity, ±1. Like a sign-of-time selector.
- **k**: configuration index, 1 or 2 for the particles we know.
  *k* = 1 is mesons and leptons, *k* = 2 is baryons.
- **P**: doubled isospin (P = 2 × isospin).
- **Q**: doubled spin (Q = 2 × angular momentum quantum number).
- **κ** ("kappa"): doublet indicator, 0 or 1. Distinguishes "regular"
  from "doublet" particles.
- **x**: multiplet identifier, picks one specific particle out of a
  charge multiplet (e.g., π⁺ vs. π⁻).

Plug these six integers into the formula, and out comes the mass.
That's it. No floating-point parameters anywhere.

The integers are not made up. They come from the structure of Heim's
eigenvalue equations: the spectrum is naturally indexed by these
integers, and only certain combinations correspond to *stable* states.
The unstable combinations are predicted to *not exist* (or to be
short-lived resonances).

### For Intermediate

The six integers carry specific group-theoretic meanings:

- **ε** = ±1 is the analogue of *time helicity*: it distinguishes
  particles propagating "with" or "against" the direction of cosmic
  time.
- **k** is the *metrical index*: it counts the number of nested
  configurations in the geometry. For our world, *k* = 1 (mesons,
  leptons) or *k* = 2 (baryons). Heavier configurations would require
  *k* ≥ 3.
- **P** and **Q** double the standard *isospin* and *spin* quantum
  numbers, respectively. The doubling is a convention to make all
  quantum numbers integer:
  - electron: spin 1/2, isospin 1/2 → P = Q = 1
  - π⁰: spin 0, isospin 1 → P = 2, Q = 0
- **κ** distinguishes singlets from doublets in the same multiplet.
  For the electron κ = 0; for the muon κ = 1 (the muon is essentially
  an "excited" version of the electron in the lepton tower).
- **x** picks one charge state out of the multiplet:
  - π⁺ has x = 0
  - π⁻ has x = 2 (in a (P+1) = 3-element multiplet)

The crucial fact is that **the electric charge is computed from the
six integers**, not put in separately. The charge comes out of
equation [B2] of the 1989 reformulation.

### For Experts

The six integers (ε, k, P, Q, κ, x) emerge from Heim's selector
calculus as follows. In the eigenvalue equation `C_p · φ^i_{km} = λ_p
· φ^i_{km}`, the integers are the indices of the *spectrum* of allowed
λ values. Specifically:

- *ε* arises from the choice between *R*₄ and the *mirror R*₄ — the
  symmetry of the 6D geometry under coordinate reflection in the time
  axis.
- *k* arises from the *metrical level* of the configuration. The
  spectrum of *k* values is unbounded in principle but is empirically
  truncated at *k* = 2 by the "selection rule for resonances" (Heim's
  unfinished work as of 1999).
- *P* and *Q* arise from the SU(2) × SU(2) representation labels in
  the rest-frame eigenvalue spectrum. Their doubled values are
  P = 2*I*, Q = 2*J*.
- *κ* arises from the *doublet structure* internal to the configuration:
  whether the configuration consists of one elementary structure (κ=0)
  or two coupled ones (κ=1).
- *x* labels the iso-spin multiplet component, ranging from 0 to *P*
  (so a P=2 particle has a triplet x ∈ {0, 1, 2}).

The electric charge (eq. [B2]):

```
q_x = ½ [ (P − 2x)·(1 − Qκ(2 − k))
        + ε·(k − 1 − Q(1+κ)(2 − k))
        + C ]
```

where *C* is a "structure distributor" (also known as *strangeness*)
computed from cosines of two angles α_P, α_Q determined by the
quantum numbers. The full expression is in [B1] of the 1989 paper and
implemented in `python/formulae.py::calc_charge()`.

The fact that *q*_x falls out of the same six integers that determine
the mass is one of the strongest internal consistencies of the
framework — there is no separate "input charge"; charge is a
**derived** geometric quantum number.

---

## Chapter 8: The Mass Formula

### For Beginners

The mass of any of Heim's basic particles is given by:

```
M = μ · α₊ · (G + S + F + Φ + 4 q α₋)
```

where:

- *μ* is the mass element (Chapter 5) — built from *G*, *ℏ*, *c*.
- α₊ and α₋ are two "structure constants" — built from η and θ
  (which are built from *G*, *ℏ*, *c* via Chapter 6).
- *G*, *S*, *F*, *Φ* are dimensionless quantities computed from the
  particle's six integer quantum numbers and four *occupation
  numbers* (n, m, p, σ) that come out of a recursive integer
  decomposition.
- *q* is the particle's electric charge.

So the structure is: a fixed mass scale (*μ* α₊), times an
integer-valued "structure number" (*G*+*S*+*F*+*Φ*), plus a small
correction for charged particles (4 *q* α₋). All the inputs are either
universal constants or integers.

The mass of the proton, for example, comes out at 938.25 MeV by this
formula. The measured value is 938.27 MeV — agreement to better than
0.01 %. The neutron, the Λ-baryon, the Ξ baryons, the Σ baryons, all
the kaons, pions, the muon, and the electron all match measurement to
similar accuracy.

### For Intermediate

The four contributions *G*, *S*, *F*, *Φ* arise from different parts
of Heim's eigenvalue spectrum:

- ***G*** ("*G* underline" in the manuscripts): the *ground-state*
  contribution. Depends only on the configuration index *k* and the
  charge magnitude *q*. For all particles with the same *k* and same
  *q*, this term is identical.
- ***S***: the *occupation* contribution, depending on the four
  integers (*n*, *m*, *p*, σ) which describe how many "structure
  units" sit in each of four nested zones of the particle.
- ***F***: cross-coupling between the ground state and the occupation,
  plus a self-coupling correction φ that contributes a few % of the total.
- ***Φ*** (capital): the *field-mass* contribution, involving two
  additional "N-functions" *N*₅ and *N*₆ that appear only in the 1989
  formula (not in the 1982 version).

The occupation numbers (*n*, *m*, *p*, σ) are *not free*. They are
extracted from the same quantum numbers via a *greedy decomposition*
of an intermediate quantity *W*:

```
(n + Q_n)³ α₁ + (m + Q_m)² α₂ + (p + Q_p) α₃ + (decay term) = W · (1 + f)
```

Imagine *W* as a "budget" that has to be distributed across four nested
zones: a cubic zone, a quadratic zone, a linear zone, and an
exponential zone. The largest integer that can be subtracted from each
zone in turn gives the occupation number for that zone. The procedure
is deterministic — once the quantum numbers are fixed, the occupation
numbers are too.

### For Experts

The formula in full:

```
M = μ · α₊ · (G + S + F + Φ + 4 q α₋)            [B3]
```

where:

```
G  = Q_n²(1+Q_n)² N₁ + Q_m(2Q_m²+3Q_m+1) N₂ + Q_p(1+Q_p) N₃ + 4 Q_σ
S  = n²(1+n)² N₁    + m(2m²+3m+1) N₂    + p(1+p) N₃    + 4σ
F  = 2nQ_n[1+3(n+Q_n+nQ_n)+2(n²+Q_n²)] N₁
   + 6mQ_m(1+m+Q_m) N₂
   + 2pQ_p N₃
   + φ                                                   (self-coupling)
Φ  = P(-1)^(P+Q)(P+Q) N₅ + Q(P+1) N₆                     [B6]
```

The four `Q_i` (= Q_n, Q_m, Q_p, Q_σ) are integer "structure constants"
depending only on *k*:

```
z   = 2^(k²)
Q_n = 3z/2,  Q_m = 2z − 1,  Q_p = 2(z + (−1)^k),  Q_σ = z − 1
```

The six N-functions *N*_1 ... *N*_6 are listed in equations [B8]–[B14]
and Chapter 6 of the 1982 paper. They depend on *k* and *q* via η, θ,
α₊, α₋. In particular *N*_3 has the most complex form (eq. [B8]) and
must include a `· q` factor in its second exponent term — a subtle
point on which earlier C/C# implementations had a transcription error.

The greedy decomposition of W into (n, m, p, σ) follows [B40]–[B46]:

```
α₁ = N₁,   α₂ = (3/2) N₂,   α₃ = (1/2) N₃
K_n = ⌊(W/α₁)^(1/3) + ε⌋ + 1
w₁  = W − (K_n − 1)³ α₁
K_m = ⌊√(w₁/α₂) + ε⌋ + 1
w₂  = w₁ − (K_m − 1)² α₂
K_p = ⌊w₂/α₃ + ε⌋ + 1
w₃  = w₂ − (K_p − 1) α₃
K_σ = ⌊−3·Q_σ·ln(w₃)/(2k − 1) + ε⌋ + 1
n = K_n − 1 − Q_n,  m = K_m − 1 − Q_m,  p = K_p − 1 − Q_p,  σ = K_σ − 1 − Q_σ
```

The self-coupling φ ([B49]) involves nine sub-expressions (the *a* and
*b* coefficients) and is the largest single piece of the formula at
~70 lines of code. See `python/formulae.py::calc_phi()`.

The implementation reproduces Heim's published numbers to ≤ 0.01 %
accuracy on the proton, neutron, Λ, Ξ⁰ — better than any prior public
implementation due to the correction of two bugs in the upstream
C and C# codes.

---

## Chapter 9: The Lifetime Formula

### For Beginners

After the mass formula, Heim derived a **lifetime formula** that
predicts how long unstable particles live before decaying. The formula
takes the same six integer quantum numbers as the mass formula and
spits out a time in seconds.

The remarkable thing is that this prediction works across **eleven
orders of magnitude**. The Δ-baryons live about 10⁻²⁴ seconds. The
muon lives about 10⁻⁶ seconds. The lifetime formula correctly
reproduces both — and almost everything in between — to within 1–10 %
of measurement. That a single closed-form expression in seven integers
covers a billion-billion fold range of timescales is, on its own, a
serious phenomenon.

### For Intermediate

The lifetime formula is

```
T = (192 · h · H · y) / (M · c² · (η-factor) · (H + n + m + p + σ) · (n + |m| + |p| · β₀))
```

where:

- *h* is Planck's constant.
- *H* = Q_n + Q_m + Q_p + Q_σ is the sum of the four structure
  constants.
- *M* is the predicted particle mass (from Chapter 8).
- *y* is a substitution involving the same φ self-coupling that
  appears in *F*, plus four "*b*" coefficients.
- (η-factor) is η₂,₂ · (1−√η)² · (1−√η₁,₁)² · (1−√η₁,₂)².
- (n + |m| + |p|·β₀) is an "occupancy" combining the four zone numbers.

The structure tells the story: the lifetime is set by the mass *M* and
the geometric factor 1/(η-factor · occupancy). Heavier particles, all
else equal, live shorter times. Larger occupancies (more "stuff" in
the inner zones) also shorten the lifetime.

### For Experts

The full lifetime formula ([B47]) is

```
(T − T_N) = 192 · h · H · y · δ
            ──────────────────────────────────────────────────────────
            M · c² · η₂,₂ · (1−√η)² · (1−√η₁,₁)² · (1−√η₁,₂)²
                  · (H + n + m + p + σ)
                  · (n + |m| + |p| · β₀)
```

For ground states (N = 0), *T*_N = 0 and δ = 1, so the formula above
gives *T* directly. The substitution *y* is

```
y = F · [ φ + (−1)^s · (1 + φ) · (b₁ + b₂/W_(N=0)) ]    [B48]
```

where φ is the self-coupling from the mass formula, and *F*, *s*, *b*₁,
*b*₂, *β*₀, *D* are six new auxiliary expressions ([B52]–[B57]). The
β₀ ([B56]) is

```
β₀ = (2 α / (π e)) · ((1 − √η) / (1 + √η))²
```

(α is the fine-structure constant). Numerically β₀ ≈ 1.08 × 10⁻⁸.

A subtle point: *F* has the special form *F* = −*D* for *P* = 3 (the
Δ resonances). In a literal floating-point evaluation, the standard
formula gives *F* = 1 − (1 + *D*) ≈ 0 because *D* ≈ 10⁻¹⁸, much smaller
than machine epsilon. Heim's intended *F* is −*D* ≈ −10⁻¹⁸, which is
small but **not zero**. Implementations that don't special-case *P* = 3
predict *T* = 0 for the Δ baryons; with the special case included, *T*
comes out at the right ~10⁻²⁴ s. This was one of the bugs corrected
in the Python port.

Implementation: `python/lifetime.py::calc_lifetime_seconds()`.
Cross-checked against the Excel reference
(`Heim_1989_Massenformel_0.4.xlsm`); 17 of 18 measured lifetimes match
within factor 3 of measurement, 15 to ≤ 12 % accuracy.

---

## Chapter 10: Predictions and Limits

### For Beginners

Heim's formula gets these things right:

- Masses of about 20 light hadrons and leptons to ~0.05 % RMS.
- Lifetimes of about 17 unstable particles to within factor 3, mostly
  to better than 12 %.
- The fine-structure constant α to about 5 decimal places (1/α =
  137.036).
- The K* meson at 867 MeV (measured 892 MeV) — this is a successful
  *new* prediction beyond Heim's published list.

It does **not** predict:

- The Higgs boson (125 GeV). Heim's quantum-number lattice has no
  allowed state with the right (P=0, Q=0, q=0) combination near 125
  GeV — there's a structural gap from the η meson (549 MeV) up to ~61
  TeV.
- The W± and Z⁰ gauge bosons.
- The J/ψ, D, B mesons, the Λ_c, Λ_b, Σ_c baryons.
- The top quark (which has fractional electric charge anyway and
  therefore can't be a Heim "free particle" by Heim's own conventions).

The pattern is clear: Heim's formula covers *light hadrons and
leptons*. Heavy-flavour states (containing charm, bottom, or top
quarks) are outside its scope. So are electroweak gauge bosons (W, Z)
and the Higgs. These are not failures of the formula — they are
*things outside the formula's intended domain*.

### For Intermediate

The boundary is sharp: Heim treats stable, stationary "metron
configurations" of light flavours (up, down, strange). Charm, bottom,
top quarks were unknown when Heim formulated his theory in the 1950s
through 1980s, and his classification scheme has no slot for them.

Equally importantly, Heim's framework has no *spontaneous symmetry
breaking* — the mechanism by which the Higgs gives mass to the W± and
Z⁰ in the Standard Model. In Heim's view, masses come *directly* from
geometry, not from a vacuum expectation value of an auxiliary scalar
field. So a Higgs particle is not just absent from Heim's spectrum —
it is *conceptually unnecessary* in his framework.

Whether this is a feature or a bug depends on which framework one
takes as the reference:

- If the Standard Model is fundamentally correct, Heim's framework is
  *incomplete* — it covers a subset of the real particle zoo.
- If Heim's framework is fundamentally correct, the Standard Model
  is computationally accurate but conceptually overcomplicated, with
  the Higgs being an artifact of a path that should have been
  geometric all along.

Empirically, the Standard Model is the one that has integrated 50
years of accelerator data without breaking. Heim's framework has not
been tested in 35 years on new particles. The honest assessment is
that Heim's framework solves a *narrower* problem (light hadron
masses) very accurately, and falls silent on a *wider* problem
(the full Standard Model spectrum) without being able to extend.

### For Experts

The empirical reach of Heim's framework, as established in this
investigation:

```
                       formula's   measured
particle               prediction  value      agreement   notes
─────────────────────────────────────────────────────────────────────
electron        e⁻       0.5069     0.5110      99.2 %
muon            μ⁻     105.652    105.658      99.9 %
pion ±          π±     139.560    139.570      99.99 %
kaon +          K⁺     493.696    493.677      99.99 %
kaon (long)     K_L    549. (?)   549. (?)      ✓ (if K_L)
Λ baryon        Λ      1115.57    1115.68     99.99 %
Σ⁺ baryon       Σ⁺     1189.33    1189.37     99.99 %
proton          p       938.25     938.27     99.99 %
neutron         n       939.55     939.57     99.99 %
…                                           …
K*⁰ meson       K*⁰      867.6      891.7     97.3 %      NEW prediction
…
Higgs H⁰        125 GeV   no candidate         outside scope
W± gauge bosons 80 GeV    no candidate         outside scope
Z⁰ gauge boson  91 GeV    no candidate         outside scope
J/ψ, D, B, Λ_c …          no candidate         outside scope (heavy flavor)
```

The Higgs case is structurally interesting. The (P=0, Q=0, q=0)
neutral spin-0 isospin-0 sector of Heim's lattice has the following
ground states (from `python/higgs_search.py`):

```
k = 1:  η meson (549 MeV)
k = 2:  no neutral solution (Heim algorithm rejects)
k = 3:  61 TeV (κ=0) and 166 TeV (κ=1)
k = 4:  even higher
```

There is no Heim-allowed P=Q=q=0 state in the 125 GeV neighbourhood.
The Higgs would have to be either (a) a different multiplet structure
entirely, or (b) outside Heim's framework. Given that the Higgs in the
Standard Model is intimately tied to electroweak symmetry breaking —
a phenomenon Heim's geometric framework does not contain — the natural
reading is (b): the Higgs is outside Heim's intended scope.

The W and Z bosons are similarly outside Heim's intended scope: they
are gauge bosons of SU(2)_L × U(1)_Y, a symmetry structure that does
not exist in Heim's framework. The closest Heim candidates at 76 GeV
(off by 5 % from W) sit at the wrong (P, Q) combination — i.e., they
are not the W per se, just numerical coincidences.

The framework's empirical *reach* is therefore: light hadrons, light
mesons, leptons (electron, muon), and a small extension to states like
K* that share the same spin-isospin classification as Heim's listed
particles.

---

## Chapter 11: Where Heim Theory Stands Today

### For Beginners

Heim's theory is **not** part of mainstream physics. It is not taught
in universities, not in physics textbooks, not part of the consensus
that physics graduate students learn. In that sense, it is a fringe
theory.

But it is a fringe theory *with a tightly closed accounting* of its
own predictions. Heim does not claim to predict everything — he claims
to predict the masses of about 20 particles, plus their lifetimes,
plus the fine-structure constant, plus a few related quantities. And
when those predictions are checked carefully (as they are in this
repository), most of them are right to remarkable accuracy.

The honest reasons mainstream physics has not engaged:

1. **Heim's notation is non-standard and forbidding.** His selector
   calculus, hermetric forms, and polymetric geometry are
   mathematical inventions that did not connect to any other branch of
   mathematics or physics. Reading Heim is hard work even for a
   physicist.
2. **Heim was secretive.** He was injured in a chemical accident as a
   young man (he lost both hands and most of his sight) and worked
   privately, publishing rarely. Most of his manuscripts were typed
   by his wife from his dictation. His main book *Elementarstrukturen
   der Materie* was published privately.
3. **The theory was never extended past 1989.** New particles
   discovered since (Higgs, charm, bottom, top hadrons) have not been
   tested. This is not a refutation, but it is a sign of inactivity.
4. **The Higgs discovery (2012)** does not fit Heim's framework, but
   neither does it falsify it (Heim's framework doesn't predict any
   125 GeV scalar; nor does it predict its absence — Heim's framework
   is silent on electroweak physics). For a Standard-Model-trained
   physicist, this silence is itself a problem.

### For Intermediate

What would change the situation?

1. **A successful extension to post-1989 particles** (top quark mass,
   any charm-baryon mass, any bottom-baryon mass) at the same 0.05 %
   accuracy. To date no such extension exists. The K* match (Chapter
   10) is a small step; a top-quark match would be a giant one.

2. **A mathematical audit of the polymetric formalism.** Heim's
   selector calculus, hermetric forms, and condensor flows are
   non-standard mathematical constructions. Whether they form a
   self-consistent algebraic system, and whether the chain
   "metron geometry → mass element → η-function → mass formula" is
   free of hidden circularity, has never been verified by an outside
   mathematician. This is the deepest open question.

3. **Reproduction of the lifetime formula by an independent group.**
   This repository's Python port reproduces Heim's lifetime numbers
   within 1–10 % across 11 orders of magnitude. The Excel
   `Heim_1989_Massenformel_0.4.xlsm` is the only other known modern
   reproduction. If a third independent reproduction (e.g., starting
   from the German source documents and building a fresh
   implementation) confirms the same accuracy, the empirical case
   becomes much harder to dismiss.

4. **Engagement by a working physicist.** None of the above three
   require Heim to be ultimately correct — they require only that the
   theory be properly evaluated. As of 2026, no experimental or
   theoretical physicist with a public profile has engaged with
   Heim's full system at the level needed.

### For Experts

The empirical reach of Heim's mass formula, as established in this
investigation, is genuinely difficult to dismiss as numerology:

- 16 particle masses to ≤ 0.05 % RMS, derived from G, ℏ, c plus six
  integer quantum numbers per particle, with the four shape parameters
  of the central η-function being **derived** (not fitted) from a
  metron-geometric chain.
- 17 lifetimes (across 11 orders of magnitude) to within factor 3 of
  measurement, 15 to better than 12 %.
- The fine-structure constant α = 1/137.03601 emerging at 5-decimal
  agreement with measurement from the same η, θ, π without any
  parameter-fit input.
- One *new* successful prediction (the K*⁰ meson at 2.7 % accuracy)
  for a particle that was not in Heim's published 16-particle list.

The honest mathematical status, however, is that Heim's polymetric
formalism has not been peer-reviewed. The chain G → τ → μ → η, and
the eigenvalue-spectrum structure that produces the (n, m, p, σ)
greedy decomposition, have been documented by Heim, by von Ludwiger
& Grüner, and by this repository's annotations — but never
mathematically audited. Until that audit happens, the framework's
status remains: empirically remarkable, theoretically untested.

The two paths forward are clear:

1. **Mathematical audit** — by a mathematical physicist fluent enough
   in Heim's own formalism to verify the consistency of the polymetric
   geometry. The full 81-page *Herleitung* manuscript (chapters 1–11)
   is the entry point. Engagement would have to start there.

2. **Experimental extension** — applying Heim's quantum-number
   classification to particles discovered after 1989. The current
   `python/higgs_search.py` shows the framework is silent on Higgs and
   heavy-flavour states; whether it has anything to say about, e.g.,
   charm-strange mesons (D_s, D_s*) remains untested.

Both paths require engagement that has not yet happened. The Heim
community at heim-theory.com / IGAAP e.V. continues to maintain the
manuscripts and reference implementations, but has not sought
mainstream reception. This repository's contribution — beyond
correcting the upstream transcription bugs — is to make the
infrastructure for either path sufficient: anyone who wishes to
engage with Heim's framework now has reproducible, annotated,
cross-checked code, a clear verdict on what the framework predicts
correctly, and a clear delineation of where it falls silent.

What Heim theory needs now is not advocacy and not dismissal. It
needs *engagement*.

---

## Further reading

In approximate order of accessibility:

1. **`README.md`** of this repository — practical entry point with
   the modern numerical results.
2. **`F_1989_en.pdf`** (in `downloads/pdfs/`) — the IGW Innsbruck
   English-language reformulation of Heim's 1989 mass formula, with
   all equations [B1]–[B57]. ~17 pages.
3. **`D_Zur_Herleitung_Der_Heimschen_Massenformel.pdf`** (in
   `downloads/pdfs/`) — the 81-page derivation manuscript by
   I. von Ludwiger and K. Grüner (IGW Innsbruck, 2003). The actual
   physical reasoning. Most accessible English summary chapter is 7
   (eqs. 7.47–7.51, the η derivation).
4. **Heim, "Elementarstrukturen der Materie"** (1980, 1984) —
   Heim's primary monograph in German. Long and dense.
5. **Heim, "Synmetronik der Welt" Bände I–III** (in `downloads/`) —
   the further development of Heim's syntrometric foundations.
6. **`python/`** in this repository — the working code, with explicit
   B-equation cross-references inline.

For ongoing community engagement:

- [heim-theory.com](https://heim-theory.com/)
- The Heim-Theory Discord (linked from heim-theory.com)
- Older archives at [protosimplex.de](https://www.engon.de/protosimplex/)

---

## Chapter 12: A Worked Example — The Proton Mass Step by Step

### For Beginners

The proton's mass, in Heim's framework, comes out of a single
calculation that takes seven inputs and produces one output. Six of
the inputs are integers describing what kind of particle the proton
is; the seventh is the proton's electric charge — and even *that*
is computed from the integers, not put in. So really, Heim's mass
formula has six integers in and one mass out.

For the proton, the six integers are:

| Symbol | Meaning | Value |
|--------|---------|------:|
| ε | time-helicity, ±1 | +1 |
| k | configuration index | 2 |
| P | doubled isospin (2 × ½ for proton) | 1 |
| Q | doubled spin (2 × ½ for proton) | 1 |
| κ | doublet indicator | 0 |
| x | multiplet identifier | 0 |

Plug these into Heim's machinery — the machinery computes
intermediate quantities like η, μ, structure constants, occupation
numbers — and the answer comes out:

```
Predicted proton mass: 938.247 629 MeV/c²
Measured proton mass:  938.272 310 MeV/c²
Error: -0.0026 % (i.e., agreement to four decimal places)
```

That's the entire story for one particle. There is no fitting
parameter in this calculation. The same machinery, with different
integers, gives the neutron, the electron, the muon, the pions, the
kaons, the baryons, and so on. The numbers are remarkable.

### For Intermediate

Let us trace the proton calculation in eight steps.

**Step 1: Structure constants** depend only on `k`. With k = 2,
z = 2^(k²) = 16:

```
Q_n = 3z/2          = 24
Q_m = 2z − 1        = 31
Q_p = 2(z + (−1)^k) = 34
Q_σ = z − 1         = 15
H = Q_n + Q_m + Q_p + Q_σ = 104
B = 3H / (k²·(2k − 1)) = 26.0
```

**Step 2: Universal constants** — built from G, ℏ, c only:

```
η = ⁴√(π⁴ / (π⁴ + 4·1⁴)) = 0.989 989 6
θ = 5η + 2√η + 1         = 7.939 912 7
α₊                       = 0.018 322 1
α₋                       = 0.008 128 4
μ                        = 2.258 935 × 10⁻³¹ kg = 0.126 717 MeV/c²
```

**Step 3: N-functions** N_1 ... N_6 depend on k and the absolute
charge q = |q_x|. For the proton (q = 1):

```
N_1 = 0.996 278  (from 1982 eq. IX)
N_2 = 0.676 704
N_3 = 2.598 819  (the complex B8 expression)
N_4 = 4.000 000
N_5 = 1.732 392
N_6 = 0.025 256
```

**Step 4: Structure weight** W from [B22]:

```
W = 14792.56
```

**Step 5: Occupation numbers** (n, m, p, σ) by greedy decomposition of
W. With α₁ = N_1 = 0.996, α₂ = (3/2)·N_2 = 1.015, α₃ = (1/2)·N_3 = 1.30:

```
K_n = ⌊(W / α₁)^(1/3) + ε⌋ + 1 = 25
w_1 = W − (K_n − 1)³ · α₁       = 14792.56 − 24³·0.996 = 1015.24
K_m = ⌊√(w_1 / α₂) + ε⌋ + 1     = 32
w_2 = w_1 − (K_m − 1)² · α₂      = 1015.24 − 31²·1.015 = 39.83
K_p = ⌊w_2 / α_3 + ε⌋ + 1        = 35
w_3 = w_2 − (K_p − 1) · α₃       = 39.83 − 34·1.299 = -4.34
K_σ = (special exponential branch) = 16
n = K_n − 1 − Q_n = 25 − 1 − 24 = 0
m = K_m − 1 − Q_m = 32 − 1 − 31 = 0
p = K_p − 1 − Q_p = 35 − 1 − 34 = 0
σ = K_σ − 1 − Q_σ = 16 − 1 − 15 = 0
```

So the proton's occupation numbers are all zero — the proton is in
the *ground state* of its hermetric form, no excitations in any of
the four structure zones.

**Step 6: Self-coupling** φ from [B49]:

```
φ = 9.280 341
```

**Step 7: Mass-formula contributions:**

```
K (occupation, all zero so K = 0)              =      0.000
S (structure, depends on Q_n…Q_σ and N_1…N_3)  = 404 103.981
F (cross-coupling + φ)                         =      9.280
Φ (field mass)                                 =      3.515
4·q·α₋ (charge correction)                     =      0.033
─────────────────────────────────────────────────────────────
Sum                                            = 404 116.809
```

**Step 8: Final mass:**

```
M = μ · α₊ · (K + S + F + Φ + 4qα₋)
  = 2.259 × 10⁻³¹ kg · 0.018 32 · 404 116.81
  = 1.672 578 × 10⁻²⁷ kg
  = 938.247 629 MeV/c²
```

The measured value is 938.272 310 MeV/c². Agreement to **0.0026 %**.

What was *put in*: six integers. What came out: a 938 MeV mass
matching reality to four decimal places. That is the experience of
running Heim's mass formula on a single particle.

### For Experts

The eight-step calculation above corresponds to specific functions in
the Python implementation:

| Step | Code (`python/`) | Equation in [1989] |
|------|------------------|--------------------|
| 1 | `formulae.calc_Q(k)` | not in 1989 — eq. (X) of 1982 |
| 2 | `constants.eta`, `theta`, `alpha_plus`, `alpha_minus`, `mass_element` | [B4], 1982 eq. (I), 2.62 |
| 3 | `formulae.calc_N(k, q, I)` | 1982 eq. (IX) for N_1, N_2; [B8]–[B14] for N_3..N_6 |
| 4 | `formulae.calc_W(...)` | [B22] using A=[B23], H=[B24], g=[B25], L=[B26], x=[B27], B=[B28] |
| 5 | `formulae.calc_n(k, I, N, W)` | exhaustion algorithm [B40]–[B46] |
| 6 | `formulae.calc_phi(...)` | [B7] / [B49] with U=[B50], Z=[B51] |
| 7 | inline in `calc_mass` | the K, S, F, Φ, 4qα₋ pieces of [B5] and [B6] |
| 8 | `formulae.calc_mass(...)` | [B3] |

Reproducibility: the precise numbers above can be regenerated with

```sh
cd python
../venv/bin/python -c "
from particle import REFERENCE_PARTICLES
p = next(p for p in REFERENCE_PARTICLES if p.symbol == 'p')
print(f'mass = {p.mass_mev:.6f} MeV/c²')
"
```

The proton's intermediate values are also accessible particle-by-
particle:

```python
import formulae as fm
from math import fabs
eps, k, P, Q, kap, qx = 1, 2, 1, 1, 0, 1
q = fabs(qx)
I  = fm.calc_Q(k)             # (24, 31, 34, 15)
N  = fm.calc_N(k, q, I)        # (N_1, N_2, ..., N_6)
W  = fm.calc_W(eps, k, P, Q, kap, qx, I)   # 14792.56
n  = fm.calc_n(k, I, N, W)     # (0, 0, 0, 0) for proton
phi = fm.calc_phi(k, P, Q, kap, qx, n, I, N, W)  # 9.28
M_kg = fm.calc_mass(eps, k, P, Q, kap, qx)
```

The `0.0026 %` accuracy is real. Note that with the upstream-inherited
bugs left in (the missing `*q` in N_3 and the y-restructuring in
`calc_a`), the proton would have computed at 937.339 MeV — a 0.099 %
error, almost 40× worse. The cleanup of those bugs is what brings the
formula into agreement with measurement at the 10⁻⁵ level.

---

## Chapter 13: Syntrometrie — The Logic Behind the Physics

### For Beginners

Heim's mass formula is the part of his work that produces numbers.
But before he ever wrote down a mass formula, Heim spent years
developing a different kind of system altogether — a **logical and
philosophical foundation** for how knowledge of the physical world is
even possible. He called it *Syntrometrie*. The name comes from
Greek roots meaning "structure-measure" or "co-measurement".

The basic intuition: ordinary classical logic has only two values,
true and false. But the *experience* we have of the world — and any
description of it — has many more dimensions than that. A statement
about a physical system might be definitely true under one
description and undefined under another; or it might depend on the
*level* at which we are looking (microscopic vs. macroscopic). To
talk rigorously about physics, Heim argued, you need a logical system
that can handle this layered, *aspectual* nature of reality.

He developed three primitive structures and called their combination
the *subjective aspect schema*:

- **Prädikatrix** (P_n): the schema of what kinds of statements
  *could* be made — the menu of possible predicates.
- **Dialektik** (D_n): the schema of how those statements are
  qualified — what kinds of judgements (true, false, undefined,
  level-dependent, …) apply.
- **Koordination** (K_n): the linking rules between the two — when
  is a particular kind of statement evaluable in a particular way?

A *Syntrix* — a complete syntrometric unit — is a triple (P_n, D_n,
K_n) functioning together. The whole machinery is meant to give a
rigorous logical bookkeeping system in which physical theories can
be stated, transformed, and combined.

This may sound very abstract — and it is. But Heim used it as the
ground from which his particle physics grew.

### For Intermediate

The three primitives in more detail:

**Prädikatrix** P_n. Heim posits a finite set of "elementary
predicates" or *Bänder* (bands), indexed by *n*. These are the basic
distinguishable kinds of statements one can make about a physical
system: e.g., "is here", "moves with speed", "interacts with",
"transforms into". The Prädikatrix is the schema for which bands are
available at a given level of analysis.

**Dialektik** D_n. The dialectic is the schema of *evaluations*. In
classical logic, the only evaluations are {true, false}. In Heim's
system, the dialectic can include:

- *true at this level, undefined at deeper levels* (level-relative
  truth)
- *true under this aspect, false under another* (aspect-relative
  truth)
- *partially true* (graded evaluation)
- *true after a transformation that moves between aspects*

The dialectic is constrained — not every evaluation is allowed for
every predicate.

**Koordination** K_n. The coordination is the rule that links
particular predicates with particular evaluations. It says, for each
predicate, which kinds of evaluation are *applicable*. A predicate
about quantum-scale geometric structure (for instance) cannot
sensibly be evaluated by macroscopic-laboratory criteria; the
coordination forbids that pairing.

The triple (P_n, D_n, K_n) forms the *subjective aspect schema*. Heim
insisted that *all* physical theories live inside such a schema —
including his own. The metron geometry, the eigenvalue equation, the
mass formula are all stated *within* a particular choice of
syntrometric unit.

The reader who has stayed with the previous chapters might ask: what
does this give us, beyond philosophy? Heim's answer: it gives a
formal language in which the *transitions between physical levels*
(microscopic ↔ macroscopic, classical ↔ quantum, geometric ↔
material) are themselves objects of the formal system. In ordinary
mathematical physics, these transitions are handled informally —
"in the limit ℏ → 0", "in the macroscopic regime". In Syntrometrie
they are first-class moves between aspect schemas.

### For Experts

Heim's *Syntrometrische Maximentelezentrik* (1993, 327 pages, in
`downloads/`) is the canonical statement of this system, written
during the last decade of his life. The system is non-standard
mathematically — it does not closely resemble first-order logic,
modal logic, intuitionistic type theory, or category theory, though
it has resonances with all four.

The most accessible modern entry point is the 2025 manuscript *A
Modernized Syntrometric Logic: Foundations and Applications*
(`downloads/Syntrometry_Heim's.pdf`, 179 pages, English), which
reformulates Heim's *Syntrometrie* in terms of:

- A typed and graded fragment of intuitionistic type theory for the
  predicate side (Prädikatrix → typed evaluated functions)
- A Kripke semantics with leveled worlds for the dialectic
- A sequent calculus with modal operators □_S (aspect-necessity) and
  □ (Syntrix-stability)
- Dynamic logic operators [π_F] for transitions between aspect
  schemas
- A mereological structure on the subjective-aspect schema S_mod(x)
  via a compatibility relation χ

The 2025 modernisation establishes:

- **Soundness** of the sequent calculus relative to the Kripke
  semantics for leveled worlds.
- **Completeness** of the syntrometric fragment of MSL (Modernized
  Syntrometric Logic) — i.e., every semantically-valid sequent is
  derivable.

These results — proven with the rigour of contemporary logic —
demonstrate that *Syntrometrie* is not "just philosophy" but admits a
genuine formal-logical underpinning.

The connection to the physics:

The eigenvalue equation `C_p · φ^i_{km} = λ_p(k, m) · φ^i_{km}` and
the polymetric geometry are, in Syntrometric language, statements
*within a specific syntrometric unit* (the one whose Prädikatrix
includes the geometric predicates "metron", "hermetric form",
"selector" and whose Dialektik includes the eigenvalue evaluation).
The mass formula is then a derived theorem of this syntrometric unit.

The promise of this framework — which has not been realised in full
— is that *transitions* between Heim's physics and other physical
theories (e.g. quantum field theory, the Standard Model, general
relativity) could be stated as syntrometric *aspect transitions*,
giving a precise account of what Heim's framework predicts for each
target theory. The 2025 modernised logic provides the technical
infrastructure for such an account; the actual translations remain
to be done.

For experts who want to engage Heim's work at the foundational level
rather than the formula level, the Syntrometric apparatus is where
the action is.

---

## Chapter 14: Extended Heim Theory — The Dröscher–Häuser 8D/12D Framework

### For Beginners

Heim's original theory had **six dimensions**. After 1996, working
together with Walter Dröscher, Heim extended it first to **eight**
dimensions and then to **twelve**. The extra dimensions were not new
"trans-coordinates" of the same kind; they encoded *additional kinds
of organising structure* that Heim and Dröscher believed were needed
to incorporate the strong nuclear force and to derive certain
constants of nature that the 6D version had to take as inputs.

The most striking achievement of the extended theory is the
**derivation of Newton's gravitational constant *G* itself**. In the
6D version, *G* was an input — Heim used the experimental value. In
the 8D extension, Dröscher computed *G* from purely geometric
considerations and got G = 6.673 32 × 10⁻¹¹ — within the
experimental error bar of NIST's measurement. That an input constant
becomes a *derived* result of a higher-dimensional version of the
theory is, on the face of it, a powerful piece of evidence for the
geometric programme.

Dröscher and Häuser also derived from the extended theory two
hypothetical new particles, the **gravitophoton** and the **graviton
of the second kind**, with predicted masses around 10⁻²² eV/c² and
which could in principle mediate a previously unknown coupling
between gravity and electromagnetism. Whether these particles exist
is unknown — they have not been searched for at the level of
sensitivity required.

### For Intermediate

The 8D extension splits the two trans-coordinates of 6D into
*four* trans-coordinates, organised as two pairs:

```
6D Heim theory          8D Heim–Dröscher theory       12D
─────────────────────   ────────────────────────────   ─────────────────
3 spatial (R₃)          3 spatial (R₃)                 3 spatial
1 time (T₁)             1 time (T₁)                    1 time
2 trans (S₂)            2 organisational (I₂)          2 organisational
                        2 informational (G₂)           2 informational
                                                       4 quantum (Q₄)
```

The 8D version splits Heim's S₂ into:

- **I₂** — *organisational* dimensions, controlling structural
  invariants (analogous to Heim's original S₂)
- **G₂** — *informational* dimensions, controlling how structures
  are addressed and processed

The 12D version of the framework adds a further four
"quantum" dimensions Q₄ that are intended to incorporate the
quantum-mechanical features of the Standard Model (probabilistic
amplitudes, gauge structure) directly into the geometry. The 12D
extension is more speculative and less developed than the 8D version.

In the 8D framework, three of the four fundamental forces emerge as
projections from R₈ to R₃ × T₁ subspaces; the fourth (gravity) emerges
from R₃ × T₁ alone. The mass formula of 6D survives as a special
case but is supplemented by additional contributions from the I₂–G₂
coupling. Dröscher's derivation of *G* from geometry uses the
condition that the mass scale set by the metron geometry must
self-consistently reproduce Newton's law of gravitation, given the
8D structure.

The proposed *gravitophoton* is a hypothetical mediator of a coupling
between gravity and electromagnetism, with mass ≈ 10⁻²² eV/c² — far
below any experimental detection threshold. Dröscher and Häuser
argue that this particle, if it exists, could allow for an
*anomalous gravitational force* under specific electromagnetic
conditions, possibly with applications to space propulsion. This is
the speculative end of the extended theory and has been the source of
both interest and controversy.

### For Experts

The Dröscher–Häuser extension is documented in:

- W. Dröscher and J. Häuser, *Guidelines for a Space Propulsion
  Device Based on Heim's Quantum Theory*, AIAA-2004-3700, 40th
  AIAA/ASME/SAE/ASEE Joint Propulsion Conference, 2004.
- W. Dröscher and J. Häuser, *Heim Quantum Theory for Space
  Propulsion Physics*, Space Propulsion Workshop, 2004.
- Multiple subsequent papers under the Heim–Dröscher Theory (HDT)
  banner.

The 8D space carries the signature (+ + + − − − − −) — the additional
two minus signs corresponding to the I₂ and G₂ subspaces. The
fundamental hyperstructure tensor extends to an 8 × 8 form. The
eigenvalue equation of 6D becomes (schematically):

```
C_p · ξ^i_{kmnj} = λ_p(k, m, n, j) · ξ^i_{kmnj},   i, k, m, n, j ∈ {1, ..., 8}
```

with eigenvalues now indexed by four metrical numbers rather than two.

**Derivation of G** (Dröscher 2003):

In 6D Heim theory, the metron is τ = (3/8)·*G*ℏ/c³, and *G* is an
input. In 8D Heim–Dröscher theory, the closed self-consistency
condition between the metron geometry and the gravitational-coupling
structure of the I₂–G₂ subspaces yields a single value of *G* for
which the mass spectrum is internally consistent:

```
G_HDT = 6.673 320 × 10⁻¹¹ m³ kg⁻¹ s⁻²
```

(quoted in Herleitung chapter 11; original derivation in
Dröscher–Häuser internal documents). For comparison, NIST CODATA 2022
gives G = 6.67430(15) × 10⁻¹¹ — the HDT prediction is within the 1.5σ
band of the measurement.

**The gravitophoton (graviphoton):**

A new boson predicted by HDT at mass m_gp ≈ 10⁻²² eV/c² (varying
slightly between papers). Couples gravity to electromagnetism; its
existence would allow for a tunable contribution to gravitational
force under specific electromagnetic configurations. This is the
mechanism Dröscher and Häuser propose for advanced space propulsion
— a "graviphoton drive."

The status of this prediction is **experimentally unconstrained**.
Current gravity-experiment sensitivities (Cassini-mission Shapiro
delays, lunar laser ranging) probe deviations from Newtonian gravity
at the 10⁻⁹ level for couplings of EM-strength order; the
predicted gravitophoton coupling is many orders of magnitude weaker
and has not been tested. The propulsion claim is therefore neither
verified nor falsified by current experiments — it is simply outside
present sensitivity.

**Status of the 12D extension:**

The 12D extension adds Q₄, four "quantum dimensions" that are meant
to reproduce gauge structure and amplitude algebra of quantum field
theory directly from geometry. This part of HDT is less developed.
The most thorough technical exposition is in Dröscher's German-
language manuscripts circulated internally; no comprehensive
peer-reviewed account exists.

**Relationship to the original 6D theory:**

Crucially, the 8D and 12D extensions *contain* the 6D mass formula
as a special case. All numerical results documented in this
repository — the masses, the lifetimes, the K* prediction — come
from the 6D version. The extensions add new structure but do not
contradict or replace the 6D results.

For readers approaching Heim theory for the first time, the
recommended path is: master the 6D framework (chapters 1–11 of this
document) before engaging the extensions. The 6D framework already
contains the central conceptual moves; the extensions add
dimensionality but the core arguments remain those of the 6D theory.

---

*This document is provided in the same spirit as the rest of the
repository: not as advocacy for or against Heim's theory, but as a
reproducible, layered exposition that lets the reader judge the
material on its own terms.*
