# Kontrabator 2026 — Modern Apparatus Design

*An engineering specification for a modern test of Heim's 1957
contrabaric-effect claim, using commercially available components
at the level of a small university physics laboratory.*

> ⚠ **Status note.** This design is a *specification*, not a built
> apparatus. It exists to answer the question "what would it
> actually take to test the Kontrabarie effect with modern equipment?"
> rather than "do we already know the effect exists?" — for which
> the honest answer is **no** (see THEORY_EXPLAINED.md Chapter 15
> for the historical record). The companion script
> `python/kontrabarie_design.py` does the parametric thrust
> prediction; this document is the engineering side.

---

## 1. Design objectives

The apparatus must satisfy three criteria, in order of importance:

1. **Reach Heim's predicted detection floor.** Heim's 1957 prototype
   failed because the components had too much loss and the
   seismometer detection threshold was too high. The modern apparatus
   must improve over Heim 1957 by **at least 6 orders of magnitude
   in detection sensitivity** (µN-class force resolution vs. Heim's
   ~mm-scale seismometer floor).

2. **Pass a falsification test.** Heim's parametric thrust law is
   `F = m₀ · C · shape(x)` with `x = ∛λ'` and
   `λ' = 2π·r·L·ε / (m₀·V')`. Doubling the input power L must
   produce a *predictable* change in F (specifically: shifting x
   away from the first maximum of `shape(x)`). A constant offset
   that does not move with power is an artifact.

3. **Be buildable in 12–18 months by 1 graduate student + 1 RF
   engineer + 1 mechanical engineer**, with a budget of order
   USD 2–5 million for hardware. Outside the scope of this design:
   ground-up custom-fabrication of the cycle former — that part will
   need iteration based on early measurements.

---

## 2. System architecture

```
   ┌──────────────────────────────────────────────────────┐
   │ RF source                                            │
   │ 30 GHz / 100 kW CW gyrotron (CPI VGT-8030)           │
   │ with 60 kV HV supply and 1 T NbTi solenoid           │
   └───────────────────────────┬──────────────────────────┘
                               │  HE₁₁ corrugated waveguide, 15 m, < 0.1 dB/m
                               ▼
   ┌──────────────────────────────────────────────────────┐
   │ Vacuum window + isolator                             │
   │ CVD-diamond window, ferrite isolator > 30 dB         │
   └───────────────────────────┬──────────────────────────┘
                               │  UHV transition, 10⁻⁷ Torr
                               ▼
   ┌──────────────────────────────────────────────────────┐
   │ SCRF niobium cavity @ 2 K                            │
   │ 9-cell scaled-ILC, Q₀ > 10⁹                          │
   │ cooled by Cryomech He cryostat (separate loop)       │
   └───────────────────────────┬──────────────────────────┘
                               │  evanescent coupling into cycle former
                               ▼
   ┌──────────────────────────────────────────────────────┐
   │ Cycle former (toroidal)                              │
   │ major radius 50 cm, minor 5 cm                       │
   │ gyrotropic-metamaterial inner liner                  │
   │ (YIG / SRR / chiral — see open questions)            │
   └───────────────────────────┬──────────────────────────┘
                               │  ponderomotive force coupling — if effect exists
                               ▼
   ┌──────────────────────────────────────────────────────┐
   │ Torsion-pendulum thrust stand                        │
   │ NASA-Eagleworks pattern, 1 µN resolution             │
   │ laser interferometer readout, 1 nm displacement      │
   └──────────────────────────────────────────────────────┘

   All of the above sits inside a vacuum chamber
   (2.5 m × 1.5 m × 1.5 m, 10⁻⁷ Torr base, Pfeiffer pumping).
```

Five distinct subsystems:

1. **RF source**: 30 GHz, 100 kW CW gyrotron.
2. **Transmission line**: HE₁₁ corrugated waveguide.
3. **SCRF cavity**: Niobium superconducting cavity at 2 K.
4. **Cycle former**: Toroidal ring with gyrotropic metamaterial liner.
5. **Diagnostic chain**: Vacuum chamber + torsion pendulum + control electronics.

---

## 3. Bill of materials (subsystem breakdown)

### 3.1 RF source

| Item | Specification | Vendor / model | ~Cost (USD) |
|---|---|---|---|
| Gyrotron | 30 GHz, 100 kW CW, TE₀₃ output | CPI VGT-8030 or GYCOM equivalent | 800 k |
| HV power supply | 60 kV, 8 A regulated, < 0.1 % ripple | TDK-Lambda 480 kW supply | 250 k |
| Superconducting magnet | 1.07 T axial at gyrotron cavity | Cryogenic Ltd 1.5 T NbTi solenoid | 150 k |
| Beam dump / mode converter | TE₀₃ → HE₁₁ converter | Custom (Calabazas Creek) | 80 k |
| RF safety enclosure | Faraday cage, interlocks | Frankonia or equivalent | 40 k |
| **Subtotal** | | | **~1.32 M** |

### 3.2 Transmission line

| Item | Specification | Vendor / model | ~Cost (USD) |
|---|---|---|---|
| HE₁₁ corrugated waveguide | 50 mm bore, 15 m total length, low loss < 0.1 dB/m | Calabazas Creek custom | 200 k |
| Miter bends | 90° HE₁₁ conserving, 6 units | same vendor | 60 k |
| Vacuum window (ceramic) | CVD diamond or BeO, 100 kW rated, 30 GHz | Brewer Science / II-VI | 35 k |
| Directional coupler / monitor | 60 dB, calibrated power tap | Millitech | 18 k |
| Switching ferrite isolator | Tx/Rx isolation, > 30 dB | Quinstar QFX-30 | 25 k |
| **Subtotal** | | | **~340 k** |

### 3.3 SCRF cavity

| Item | Specification | Vendor / model | ~Cost (USD) |
|---|---|---|---|
| Niobium cavity (9-cell ILC-style, scaled) | 30 GHz fundamental, Q₀ > 10⁹ at 2 K | Research Instruments GmbH | 450 k |
| Helium cryostat | 4 K bath + 2 K λ-plate, 500 W cooling at 2 K | Cryomech AL-330 / Linde turnkey | 350 k |
| LN₂ pre-cooler | 100 L/day | standard | 60 k |
| RF feedthrough | 30 GHz, 100 kW CW, into 2 K | custom CERN-style | 80 k |
| Tuning mechanism | piezo + stepper, dual-stage | custom | 35 k |
| **Subtotal** | | | **~975 k** |

### 3.4 Cycle former (the experimental heart)

| Item | Specification | Vendor / model | ~Cost (USD) |
|---|---|---|---|
| Toroidal mount | 50 cm major radius, 5 cm minor radius, sapphire substrate | machined to order | 80 k |
| Gyrotropic metamaterial liner | YIG-loaded photonic crystal or chiral SRR array, 30 GHz designed | research-grade, partner with NIST or Sandia metamaterials group | 200 k |
| Tuning probes | 4× insertion probes for mode-control | standard | 20 k |
| **Subtotal** | | | **~300 k** |

This subsystem is where Heim's prescription is least specific — modern
photonic-crystal design tools can enumerate candidate gyrotropic
structures, but verifying that any given one implements Heim's
`rot rot · F = 0` condition operationally is non-trivial and is the
likely failure mode of a first build. Plan for *two or three
iterations* of the metamaterial liner.

### 3.5 Diagnostic chain

| Item | Specification | Vendor / model | ~Cost (USD) |
|---|---|---|---|
| Vacuum chamber | 2.5 m × 1.5 m × 1.5 m, stainless 304 | custom (Nor-Cal Products) | 90 k |
| Turbomolecular pumping station | base pressure 10⁻⁷ Torr | Pfeiffer HiCube 80 + ion getter | 60 k |
| Torsion pendulum thrust stand | 1 µN resolution at 100 kW input power, NASA-Eagleworks pattern | custom (Tajmar group / TU Dresden has built equivalents) | 180 k |
| Laser interferometer readout | 1 nm displacement resolution | SIOS SP-S 120 | 70 k |
| Optical-table isolation | 4 × Newport S-2000 stage, on dedicated concrete pad | Newport | 45 k |
| EM shielding (Mu-metal + RF) | inside vacuum chamber | custom | 20 k |
| **Subtotal** | | | **~465 k** |

### 3.6 Control, DAQ, calibration

| Item | Specification | Vendor / model | ~Cost (USD) |
|---|---|---|---|
| RF master oscillator | 30 GHz ± 1 Hz stability | Pasternack PE15UN1003 / OEwaves | 35 k |
| Digital phase-lock control | 4-channel FPGA + DACs | Liquid Instruments Moku:Pro | 15 k |
| Force-stand DAQ | 24-bit, 100 kS/s, low-drift | NI cDAQ + 9239 | 8 k |
| Thermal monitoring | 16-channel resistance thermometry, mK-class | Lake Shore 372 | 28 k |
| Calibration weights / known-force generator | electrostatic pull-plate, 0.1-1000 µN traceable | NIST-traceable calibration | 25 k |
| **Subtotal** | | | **~111 k** |

---

## 4. Cost summary

| Subsystem | Subtotal |
|---|---:|
| RF source (gyrotron + magnet + HV) | 1.32 M |
| Transmission line | 340 k |
| SCRF cavity + cryogenics | 975 k |
| Cycle former (experimental) | 300 k |
| Diagnostic chain + vacuum | 465 k |
| Control + DAQ | 111 k |
| Spares + iteration budget (15 %) | 510 k |
| **Hardware total** | **≈ 4.0 M USD** |
| Personnel (12–18 months, 3 FTE) | 1.0 M |
| **Project total** | **≈ 5.0 M USD** |

For comparison: a small physics graduate-thesis experiment is
typically USD 100 k - 1 M; a mid-sized lab apparatus (e.g. an
ion trap, a tabletop cold-atom experiment) is USD 1 M - 5 M; a
single ATLAS detector module is > USD 10 M. This proposal sits at
the *bottom of the mid-range* of experimental physics — small for
HEP, large for a typical solid-state lab.

---

## 5. Operating parameters at the design point

Plugging the apparatus parameters into Heim's prediction from
`python/kontrabarie_design.py`:

```
Heim's reduced parameter:   λ' = 2π · r · L · ε / (m₀ · V')

  r   = 0.50 m         (major radius of cycle former)
  L   = 100 000 W      (input power, 100 kW)
  ε   = 0.5            (assumed transformation efficiency)
  m₀  = 50 kg          (apparatus mass — cycle former subsystem only)
  V'  = 0.003 m³       (active volume inside cycle former)

  λ'  ≈ 1.05 × 10⁶  (dimensionless after Heim's implicit time-scale
                    normalisation, which the IvL 2017 paper does
                    not pin down — see kontrabarie_design.py for
                    the operator-tuning interpretation we adopt)
```

The apparatus is geometrically tuned (by adjusting r and V' through
the cycle-former design and tuning probes) so that x sits at the
first positive maximum of Heim's bracket function, where
`shape(x_peak) ≈ 2.99`.

Predicted thrust at the design point, parametric in Heim's unknown
overall coupling scale C (units: m/s²):

| C [m/s²]  | F [N]    | F / L [N / kW] | Interpretation              |
|----------:|---------:|---------------:|-----------------------------|
| 7.4 × 10⁻⁶ |  3.3 × 10⁻⁴ |          0.0033 | photon-rocket floor       |
| 1 × 10⁻⁴   |  0.015      |          0.15   | 100× above photon floor   |
| 1 × 10⁻³   |  0.15       |          1.5    | "Heim 1957 floor"         |
| 1 × 10⁻²   |  1.5        |         15      | 0.1 % of g                |
| 1          | 150         |       1500      | full antigravity          |

The apparatus's force-measurement floor of **~1 µN** detects effects
at **C > 7 × 10⁻⁹ m/s²**, i.e. five orders of magnitude below the
"Heim 1957 floor" and three orders of magnitude below even the
photon-rocket-equivalent C. So the apparatus is sensitive enough to
either confirm or rule out the contrabaric effect at any
physically interesting magnitude.

---

## 6. Measurement protocol (the falsification test)

The core experimental run is **not** "see if the thrust stand
deflects when the gyrotron is on." That measurement alone is
hopelessly susceptible to thermal, EM-leakage, and electrostatic
artifacts. The falsification protocol uses three runs in sequence:

### Run A — Reference (cycle former tuned to peak)

- RF on, 100 kW for 60 s.
- Apparatus tuned so x ≈ x_peak.
- Record force-stand deflection F_A.

### Run B — Detuned cavity (control for systematic offsets)

- RF on, 100 kW for 60 s.
- SCRF cavity detuned by Δf = ±10 MHz (Q drops by ≥ 10²).
- Cycle-former mode no longer resonates.
- Heim's effect should vanish; thermal / EM-leakage / electrostatic
  effects should remain.
- Record force-stand deflection F_B.

**Differential signal:** ΔF₁ = F_A − F_B.

If ΔF₁ ≈ 0, the "Heim signal" from Run A is an artifact.

### Run C — Power scan (falsification of Heim's scaling law)

- Repeat Run A at L ∈ {25, 50, 100, 200, 400} kW (over a factor of
  16 in input power).
- Heim's law predicts F ∝ shape(x(L)) with x ∝ L^(1/3); at five
  power points the resulting F-vs-L curve must follow this
  functional form.
- A real Heim effect *must* follow this scaling. Thermal artifacts
  scale linearly with L; EM-leakage artifacts scale roughly with √L;
  electrostatic scales with L²; vibration scales with √L.
- Fit ΔF(L) to all four hypotheses (Heim, thermal, EM-leakage,
  electrostatic) and report likelihood ratios.

**Falsification criterion**: a measured F-vs-L curve consistent at
> 3σ with one of the artifact hypotheses (linear, √L, L²) and
inconsistent at > 3σ with Heim's `shape(∛(L^something))` law is a
clean falsification.

### Run D — Polarity reversal

- Heim's geometric framework permits a *direction* for the
  ponderomotive force, set by the orientation of the gyrotropic
  cycle former.
- Rotate the cycle former by 180°. The force direction should
  reverse. If it doesn't, the signal is not orientation-dependent
  → not Heim's effect.

### Total observation budget

- 4 runs × 5 power points × 60 s × 5 repeats = 5000 s of beam time.
- Total integrated power: ~5 × 10⁸ J = 140 kWh.
- Cost of running the apparatus: dominated by helium boil-off and
  RF tube depreciation; ~USD 20-50k per data-collection campaign.

---

## 7. What can go wrong (engineering risks)

In order of likelihood:

1. **Cycle former doesn't implement Heim's `rot rot · F = 0`
   condition.** The single biggest open question — modern
   metamaterial design has dozens of candidate gyrotropic structures
   but no consensus on which one implements Heim's specific operator
   algebra. Mitigation: budget 2-3 metamaterial iterations and an
   in-situ characterisation step (probes that measure E-field
   topology inside the cycle former) before any thrust measurement.

2. **Thermal drift.** 100 kW dissipated in a 50 kg apparatus over
   60 s is ~120 J → ΔT ~ 1 °C if all goes into the structure.
   Even at 10⁻⁶ K/K thermal expansion, a 10 cm beam path moves by
   100 nm → laser-interferometer reads false signal. Mitigation:
   active thermal stabilisation of the thrust-stand pivots to
   ≤ 1 mK; differential measurement Run A − Run B.

3. **EM leakage radiation pressure.** Even 0.01 % of 100 kW leaking
   from the apparatus = 10 W of stray radiation = 33 nN of
   radiation pressure if it hits the thrust stand at normal
   incidence. Mitigation: Mu-metal + RF-absorbing chamber liner
   around thrust stand; characterisation runs with absorbers
   blocking line-of-sight from cavity to pendulum.

4. **Mechanical vibration**. Gyrotrons, vacuum pumps, helium
   compressors all run at known frequencies (50/60 Hz, kHz pump
   blades). Mitigation: 4-stage Newport vibration isolation;
   bandpass filter the DAQ to exclude known carrier frequencies.

5. **Charge buildup**. SCRF cavity at high gradient develops
   surface charges; these couple to the thrust stand
   electrostatically. Mitigation: grounded RF-shield around stand;
   measurement in static-charged vs static-discharged conditions
   to bound the effect.

6. **The effect simply doesn't exist.** A clean null result across
   all four runs at the design sensitivity would be the *most likely
   outcome* given current physics consensus, and would be an
   important measurement in its own right — it would constrain
   C < 10⁻⁹ m/s² at 95 % confidence, putting Heim's contrabaric
   effect below the photon-rocket equivalent and effectively
   ruling it out as an exploitable propulsion mechanism.

---

## 8. Site requirements

- 100 m² lab floor space, 4 m ceiling clearance.
- 3-phase 480 V, 600 A service for gyrotron HV supply.
- Cooling water: 100 L/min at 15 °C for gyrotron and cavity heat loads.
- Helium: 200 L liquid per week initial fill, ~30 L/week steady state.
- Concrete pad isolated from building structure for thrust-stand mount.
- Class-100,000 cleanroom airflow around the SCRF cavity assembly area.

A standard university accelerator-physics group typically has all of
the above already; a generic physics or engineering department
would need a ~6-month site-prep phase.

---

## 9. Open engineering questions

Items where Heim's prescription is incomplete and the design must be
empirically resolved during commissioning:

1. **Which gyrotropic metamaterial implements Heim's cycle-former
   operator?** Open. Three candidate structures to test:
   (a) YIG-loaded photonic crystal with externally biased magnetic
   field;
   (b) Bianisotropic split-ring-resonator (SRR) array on sapphire;
   (c) Helical chiral-metamaterial inner liner.
2. **What efficiency ε is realistically achievable?** Heim's
   formula uses ε as a free parameter (his 1957 prototype had
   ε ≪ 1 %). Modern SCRF cavities reach round-trip efficiencies
   > 99.9 %; whether this translates to Heim's specific
   "transformation efficiency" depends on the cycle-former
   coupling.
3. **What is the correct value of m₀ in Heim's formula?** Is it
   the apparatus total mass, the cycle-former mass, or the
   active-volume mass? The IvL 2017 paper does not pin this
   down. Sensitivity studies during commissioning should
   determine the empirical answer.
4. **Polarity of the predicted force.** Heim's framework prescribes
   the *direction* of the ponderomotive force from the orientation
   of the rot-rot operator on E × H, but the sign convention is
   not explicit in the available 1959 text. Run D (polarity
   reversal) is the cleanest experimental probe.

---

## 10. Comparison with prior attempts

| Year | Group | Apparatus | Outcome |
|---|---|---|---|
| 1957 | Heim (Northeim) | Hand-soldered 17 cm hollow rings, ~10 kW magnetron | Negative (component loss too high) |
| 1985 | MBB / DASA | Proposed SQUID gravito-magnetic test | Funded experiment never completed |
| 1991–97 | Li & Torr (Univ. of Alabama in Huntsville) | Theoretical: gravitomagnetic field from rotating SC + B-field via Cooper-pair phase coherence | Published theory; not cleanly confirmed experimentally |
| 1992–96 | Podkletnov (Tampere) | Rotating superconductor + EM field | Initial positive, refuted by replications |
| 2002–08 | Tajmar et al. (ARC Seibersdorf) | Rotating SC + gyroscopes | Initial 10⁻⁸ effect, attributed to systematics |
| 2003 | Millis & Davis (AIAA) | "Frontiers of Propulsion Science" review | Concluded Heim's design is "promising" but untested |
| 2026 | **(this design)** | Modern SCRF cavity + metamaterial cycle former + µN thrust stand | **Proposed — not built.** |

The 2026 design improves over Heim 1957 by:

- ~10⁴× higher RF power (100 kW vs ~10 kW pulsed)
- ~10⁵× higher cavity Q (10⁹ vs ~10⁴ for hand-soldered rings)
- ~10⁶× better force resolution (1 µN vs ~10 mm seismometer floor at
  the relevant mass scale)
- Quantitative falsification protocol (Heim had no such protocol)

---

## 11. License + status

This design specification is offered openly under the same
non-commercial terms as the rest of the repository. It is *not* a
sales pitch for the apparatus, and the author has no financial
interest in its construction. The intent is to make clear what an
honest test of Heim's claim would require, so that the physics
community can either fund the test or explicitly decline to.

The companion Python script `python/kontrabarie_design.py` produces
the thrust-prediction numbers cited above and is the place to vary
apparatus parameters (radius, power, mass, volume, efficiency) and
see how the prediction changes.

Engineering corrections, vendor updates, and refinements are
welcome via repository issues.

---

*If the apparatus is built and the effect is observed at the
predicted scaling: extraordinary news for physics. If the apparatus
is built and a clean null is obtained: an important constraint on
the framework, and the end of a 70-year open question.*

*Either outcome is more useful than the present situation, in which
the effect is neither confirmed nor refuted because the experiment
has simply not been performed.*
