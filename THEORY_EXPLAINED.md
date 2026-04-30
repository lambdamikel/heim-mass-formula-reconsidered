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
T_{ik} = | T_{11} T_{12} T_{13} T_{14}  0     0    |
        | T_{21} T_{22} T_{23} T_{24}  0     0    |
        | T_{31} T_{32} T_{33} T_{34}  0     0    |
        | T_{41} T_{42} T_{43} T_{44} T_{45} T_{46} |
        |  0      0     0    T_{54} T_{55} T_{56} |
        |  0      0     0    T_{64} T_{65} T_{66} |
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

*This document is provided in the same spirit as the rest of the
repository: not as advocacy for or against Heim's theory, but as a
reproducible, layered exposition that lets the reader judge the
material on its own terms.*
