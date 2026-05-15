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

## 8. Implications for our reproduction

- The 12-Λ z=0 sector with b_fit = b_pred = +0.0070 (commit a74c31b) is
  the canonical verification of Heim's z=0 approximation for non-
  underlined Λ resonances.
- The 25/181 z=0 verification rate (commit df86c7c) likely
  understates the framework's match quality because we did NOT
  separate underlined from non-underlined entries.  Heim explicitly
  states only non-underlined should follow (14a, 14b).
- A targeted re-verification restricted to non-underlined entries
  is the natural follow-up.
