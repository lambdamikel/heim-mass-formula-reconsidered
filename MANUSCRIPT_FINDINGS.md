# Manuscript reading findings — J0032 and J0033

Date: May 2026

Comprehensive review of Burkhard Heim's manuscripts J0032 ("Ausgewählte
Ergebnisse einer einheitlichen Quantenfeldtheorie der Materie und
Gravitation", 1973, 50 pp.) and J0033 ("Ausgewählte Ergebnisse b",
1975-76, 61 pp., Mazzone's Script B).

## 1. Heim's own z=0 disclaimer (J0032 p.27a, J0033 p.36-37)

> "Das Ergebnis dieser Arbeit wurde in Tabelle IV für k = 1 und in den
> Tabellen V bis V_b für k = 2 unter der approximativen Voraussetzung
> z(N) = 0 (Approximationsfehler unter 0,1 MeV) zusammengestellt."

Both manuscripts state explicitly that Heim's Tabellen IV (k=1, 23
mesonic resonances) and V_{a,b,c} (k=2, 76 baryonic resonances) were
assembled under the assumption z(N) = 0 for all N, with stated
approximation error under 0.1 MeV.

Three named exceptions where the eqs. (14)-(14b₁) themselves show
uncertainty:

  - ω(783)  [k=1]
  - η'(958) [k=1]
  - N(1688) [k=2]

## 2. The underline notation (J0032 p.27a, J0033 p.37)

> "Die N-Angaben der dritten Spalte unterscheiden zwischen N und N̄,
> wobei die Unterstreichung bedeutet, daß es sich um einen Term
> handelt, welcher der Beziehung (14d) nicht genügt."

In Tabellen IV-V_c, underlined N-values mark resonances that DON'T
satisfy the monotonicity condition (14d).  Per J0032 p.15a:

> "Dieses Auswahlprinzip gilt jedoch nur für stufenweise Anregungen.
> ... Das zu jedem Grundzustand gehörende Spektrum N kann demnach als
> Überlagerung von zwei Spektren aufgefaßt werden, nämlich dem
> Spektrum N möglicher stufenweiser Anregungen die (14d) genügen
> und dem Spektrum N̄ von Termen, die nicht stufenweise, sondern nur
> durch einen einzigen energetischen Vorgang entstehen können."

So Heim distinguishes two kinds of resonances:

  - **Non-underlined N**: stepwise (z=0) excitations.  Should satisfy
    eqs. (14a, 14b) under z=0 approximation.
  - **Underlined N̄**: single-process resonances ("nicht stufenweise,
    sondern nur durch einen einzigen energetischen Vorgang
    entstehen").  Different formula not provided in J0032.

### Mesonic (Tabelle IV) underline status:

  Non-underlined N (13 entries):  ε, ω(783), Φ(1019), E(1420),
    ω(1675), K*(1420), L(1770), ρ(770), δ(970), A1(1100), A2(1310),
    ρ'(1600), g(1680).
  Underlined N̄ (10 entries):    η'(958), S*(993), f(1270), D(1285),
    f'(1514), K*(892), K_A(1240), B(1235), F1(1540), A3(1640).

### Baryonic (Tabellen V, V_a, V_b) underline status:

Detailed per-entry transcription pending — see images at p.40b-d.

## 3. z(N) is explicitly unknown — both manuscripts

J0032 p.26:

> "Zwar ist von z nur bekannt, daß es sich um positive ganze Zahlen
> handelt..."

J0033 p.36:

> "Tatsächlich ist z nicht gegeben, so daß auch Q(N) der N>0 vorerst
> noch unbekannt ist."

There is no closed-form expression for z(N) in either manuscript.
Both treat it as an explicitly open question.

## 4. Heim's "Bemerkung zu (5d)" (J0032 p.40)

> "Es ist durchaus möglich, daß in der Funktion φ noch ein
> unbekanntes additives Glied (abhängig von k, P, Q und κ) fehlt,
> über dessen Existenz und Bau erst eine Beschreibung der noch
> unbekannten Zerfallszeiten Aufschluß geben kann. Ein solches
> additives Glied könnte sich in den Massen jedoch nur in der
> Größenordnung einiger 10⁻² Elektronenmegavolt bemerkbar machen."

Heim flags an additional unknown term in φ of order 10⁻² MeV — likely
explaining our 0.05 MeV residuals in matched configurations.

## 5. Anhang B canonical values (J0032 p.41-43)

Heim's own numerical values for verification:

  η = 0.98998964
  η₁,₁ = 0.98756399
  η₁,₂ = 0.98516776
  η₂,₂ = 0.84242385
  θ = 7.93991266
  θ₁,₁ = 7.92534503
  θ₁,₂ = 7.91095114
  θ₂,₂ = 7.04779227
  α_+ = 0.01832211
  α_- = 0.00812835

  k=1:  Q = (3, 3, 2, 1),  B = 27,  H = 9,  A = 2787.59025432
  k=2:  Q = (24, 31, 34, 15), B = 26, H = 104, A = 14727.57867072

  N_3(2, 0) = 2.71828183 (= e, Euler's number)
  N_5(2, 2) = 76.73214581
  N_6(2, 0) = −0.10493009

  W_{N=0} per particle (page 43):
    e⁻:    38.70294226
    π±:    3514.46294316
    K⁺:    8857.95769020
    η:     9905.00599107
    π⁰:    3419.16217346
    p:     14792.56308050
    Λ:     16827.97671482
    o⁻:    18448.51703290
    n:     14828.61089116
    Σ⁰:    18179.59733741
    Ξ⁰:    18990.08927597
    o⁰:    18508.94119539
    ...

These let us independently verify our calc_W and calc_N implementations.

## 6. The minimal data of Heim's framework (J0033 p.38)

> "Es erscheint vom philosophischen Gesichtspunkt bemerkenswert, daß
> die einheitlichen zahlentheoretischen Funktionen, welche die Massen,
> die Existenzzeiten sowie die Eigenschaften des Spins, Isospins
> sowie der elektrischen Ladung und der sogenannten 'Seltsamkeit'
> aller Elementarkorpuskeln einheitlich beschreiben, im Grunde
> genommen auf nur zwei Parameter k und N zurückgehen, von denen k
> nur die Werte k = 1 oder k = 2 annehmen kann, während N ≥ 0 die
> einfache Folge positiver ganzer Zahlen ist."

The whole framework — mass, lifetime, spin, isospin, charge,
strangeness — reduces to TWO integers: k ∈ {1, 2} and N ∈ ℕ.

## 7. J0033's distinctive content

J0033 differs from J0032 in:

  - Uses RevModPhys.48 (1976) constants (vs J0032's RevModPhys.45 1973):
    ℏ = 1.0545887e-34, μ = 2.25902134e-31 kg (vs J0032's 2.25902741).
  - Section on lifetimes (J0033 eqs. 21-21h) provides explicit
    closed-form for y in the φ-formula (J0032 only gave 13e₁ as
    long expression).  This is the lifetime-predicting formula.

J0033 carries no new z(N) information beyond J0032.

## 8. p.16a correction — K_B interpretation (16 May 2026 reading)

J0032 p.16a "Korrektur zu Seite 16":

> "...wobei N nach (14d) erlaubt sein muß" *entfällt*.  Statt dessen:
> "Ergibt sich K_B = 0, dann besteht keine Möglichkeit einer externen
> Anregung. Desgleichen ist im Fall K_B < 0 diese Möglichkeit nicht
> gegeben; denn in diesem Fall würde der Term vor seinem Zerfall
> zunächst durch eine Emission das tiefste Niveau K_B < 0 anstreben.
> Nur im Fall K_B > 0 der Beziehung 14e liegt die Möglichkeit einer
> externen Anregung vor."

Conceptual clarification (no formula change):

  - K_B > 0:  external excitation possible (true resonance)
  - K_B = 0:  no external excitation possible
  - K_B < 0:  no external excitation possible — the term would
              instead emit down to the lowest K_B < 0 level before
              decay

In Tabellen IV / V this matters for: Λ(1815) K_B=-10, Λ(1860) -5,
Λ(2100) 0, N(1535)⁰ -2, N(1688)⁰ -23, N(2000) -3 & -37, N(2190) -14,
Δ(1690) 0, Δ(1910) -27, S*(993) -1, Σ(1620)⁰ -23, Σ(2620) -27,
Σ(2455)⁰ -45, Σ(3000)⁻ -85, and others.  These are not the "Anregerkurve"-type
external excitations Heim's (14a, 14b) describe — they are
internal structural endpoints.  Our Z=0 classification (commits
a766afe, 1262c7f) treats all sub-sectors uniformly; per Heim's
p.16a correction these K_B ≤ 0 states are conceptually different
from the K_B > 0 excitations.

Does not affect any mass / K_B / W_{N=0} numerical reproduction —
purely an interpretation note.


## 9. Δ-family ground-state mass discrepancy (Open Q 1b refinement)

The 16 May 2026 session traced the long-standing 1.5–1.9 MeV
mass discrepancy for the four Δ ground-state particles
(o⁺⁺, o⁺, o⁰, o⁻) to a structural endpoint:

  - calc_a is correct (Term-für-Term match with J0032 (13c), (13d)).
  - calc_W is correct (matches 20/21 Heim Anhang B W values).
  - calc_n greedy is correct (gives Heim's published (n,m,p,σ)
    for o⁺ and o⁻ exactly; for o⁺⁺ and o⁰ Heim's published
    (n,m,p,σ) is self-inconsistent with Heim's own W₀ values).
  - calc_phi structural formula matches Heim's [B7]/[B49] verbatim
    (verified by user-transcribed manuscript text).
  - Heim's Anhang B per-particle a_1, a_2 columns for the
    o-family contain typos (o⁺⁺ a_1=23 belongs to o⁻ row by W
    consistency, and vice versa).

The remaining 0.85–1.58 MeV per-particle discrepancy comes from
a P=3 specific term we do not compute.  Heim's own "Bemerkung zu
(5d)" (J0032 p.40) explicitly admits:

> "Es ist durchaus möglich, daß in der Funktion φ noch ein
> unbekanntes additives Glied (abhängig von k, P, Q und κ)
> fehlt..."

Heim's stated upper bound (10⁻² MeV) is two orders of magnitude
below what we observe at Δ (≈ 1 MeV).  No documented Δ-specific
correction was found in the manuscript (J0032 §19-23 multiplet
classifications, p.15a / p.16a "Ergänzung" notes, or F-document
[B6]/[B7] sections).  Conclusion: the Δ-family sits at the
empirically-detectable edge of Heim's framework's published
accuracy.


## 10. Lifetime formula (21f) b₂ — `c/ω` identified as gravity-speed ratio

May 2026 reading of J0033 (21f) (b₂ sub-expression of the lifetime
formula) revealed two occurrences of a constant transcribed as `c/ω`
in lines 7 and 10:

    Line 7:  − (B − c/ω)² · (P−1)(P−2)(P−3) · (−1)^(k−1)
    Line 10:                      … + (B/2·(H+2) + c/ω) · …

Our `python/lifetime.py` had `c/ω = 3/4` hard-coded.  Tracking down
the symbols led to Herleitung Kap. 1 (von Ludwiger & Grüner, IGW
Innsbruck 2003):

  - S. 10 Fn. vi:
      > "B. Heim hatte in seiner ersten Publikation (1980) einen
      > Wert von 4/3 c für die Ausbreitungsgeschwindigkeit
      > gravitativer Feldstörungen errechnet, was auf die Verwendung
      > eines falschen Operator-Ausdrucks zurückzuführen war. Im
      > Folgenden wird mit c als der Ausbreitungsgeschwindigkeit
      > von Gravitationsfeldstörungen gerechnet."

  - S. 3310:
      > "Wenn sich ε̇ und η̇ zeitlich nicht ändern, ist ω = c."

Identification:

  - `c` = speed of light.
  - `ω` = propagation speed of gravitational field disturbances.
  - Heim's original 1980 value:  ω = (4/3)·c   ⟹  c/ω = 3/4.
  - IGW-corrected value:         ω =  c        ⟹  c/ω = 1.

### Empirical test

Replacing `c/ω = 3/4 → 1.0` in both lines 7 and 10 of `calc_b2`:

  Score:   17/18 → 16/18 within factor 3 of PDG.
  Effect:  Ω⁻ slips from log-err +0.21 to +0.96 (out of factor 3);
           η improves marginally (−0.33 → −0.25);
           all other 16 particles within ±0.01 of original.

### Interpretation

The b₂ formula is internally consistent in Heim's original
ω = (4/3)·c convention.  The Herleitung (S. 80) explicitly notes:

  > "Wegen des erheblichen Aufwands, den die Überprüfung der
  > Formeln für die Lebensdauern bereitet, wurde dieser Teil von
  > uns noch nicht neu programmiert. Es werden die von Heim
  > gerechneten Werte vorgestellt."

So the IGW group never reprogrammed the lifetime side.  The
ω-correction in their mass-formula chapters was therefore never
propagated through equations (21)–(21h).  Our `c/ω = 3/4` choice
matches Heim's published b₂ kernel; it does NOT match what the
IGW correction would suggest theoretically.

This is documented in `python/lifetime.py:calc_b2` and provides
a concrete example of the gap between Heim's original framework
and IGW's later re-derivation that the lifetime sector still
inherits.

## 11. Implications for our reproduction

- The 12-Λ z=0 sector with b_fit = b_pred = +0.0070 (commit a74c31b) is
  the canonical verification of Heim's z=0 approximation for non-
  underlined Λ resonances.
- The 25/181 z=0 verification rate (commit df86c7c) likely
  understates the framework's match quality because we did NOT
  separate underlined from non-underlined entries.  Heim explicitly
  states only non-underlined should follow (14a, 14b).
- A targeted re-verification restricted to non-underlined entries
  is the natural follow-up.
