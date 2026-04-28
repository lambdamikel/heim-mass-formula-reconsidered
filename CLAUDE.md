# CLAUDE.md

Project context for Claude Code. Keep this file concise; it loads into every
session.

## What this project is

A reproducible investigation of Burkhard Heim's 1989 elementary-particle mass
formula. The repository:

- Hosts Eli Gildish's 2006 C re-implementation as an upstream snapshot.
- Provides an annotated copy that maps every line to its corresponding
  equation in the IGW Innsbruck 2002/2003 reformulation of Heim's 1989
  manuscript (cited as `[1989]` with equation tags `[B##]`).
- Provides a Python port that produces bit-identical numerical output.
- Provides sensitivity-analysis scripts and their plots.

The README is the public-facing story. CLAUDE.md is the operating manual.

## Build / run

```sh
# Annotated C reference (default target builds and runs)
cd annotated && make

# Python port (Python 3.10+; Python 3.12 confirmed)
python3 -m venv venv
./venv/bin/pip install numpy matplotlib
./venv/bin/python python/heimmass.py

# Sensitivity sweeps
./venv/bin/python python/sensitivity.py             # 3 fitted constants ±10%
./venv/bin/python python/sensitivity_wide.py        # same, ±3 decades log
./venv/bin/python python/sensitivity_diagnostic.py  # per-particle effect
./venv/bin/python python/sensitivity_structural.py  # mu, eta, theta, Q_i
./venv/bin/python python/sensitivity_eta_form.py    # eta's 4 shape parameters
```

Plots land in `python/plots/`.

## Verifying changes

The Python port is held to bit-identical numerical equality with the C
reference. Any change to either side should be cross-checked:

```sh
./annotated/heimmass > /tmp/c.out
./venv/bin/python python/heimmass.py > /tmp/py.out
# Compare the 21 mass values; they should agree to all 8 displayed digits.
```

There is no automated test suite yet — adding one (pytest snapshot of the
21 reference masses) is a worthwhile next step.

## Layout — key files

```
README.md                          Public-facing report (English)
REPORT.de.md                       Companion narrative (German)
LICENSE                            Non-commercial; inherits Eli Gildish's terms

downloads/c_impl/                  Upstream C, untouched
downloads/csharp_impl/             Upstream C# variants (1982/1989/HeimGroup)
downloads/pdfs/                    Heim 1982/1989 reformulations + derivation

annotated/src/formulae.c           Mass formula, every line tagged with [B##]
annotated/src/constant.c           eta, theta, alpha+/-, alpha (fine), mu
annotated/Makefile                 `-lm` and `-Wno-array-bounds` already added

python/constants.py                Physical & auxiliary constants
python/formulae.py                 calc_charge, calc_Q, calc_N, calc_a,
                                   calc_W, calc_n, calc_phi, calc_mass
python/particle.py                 Particle dataclass + REFERENCE_PARTICLES
python/heimmass.py                 Main runner
```

## Domain conventions you must know

### Naming traps

The mass formula contains TWO things called "phi":
- **calc_phi** in code, lowercase φ in [B7] / [B49] — the *self-coupling*
  function. Lives inside the F-term.
- **PHI** local variable in `calc_mass`, capital Φ in [B6] —
  P·(−1)^(P+Q)·(P+Q)·N₅ + Q·(P+1)·N₆. Distinct from φ.

Don't confuse them when making edits.

### Indexing

The C source uses 1-based arrays via the pointer-minus-1 trick (`int *I =
ivalue - 1; I[1]..I[4]`). The Python port uses native 0-based indexing.
Mapping:

```
C: I[1..4]  ↔  Python: I[0..3]   (Q_n, Q_m, Q_p, Q_sigma)
C: N[1..6]  ↔  Python: N[0..5]   (N_1 .. N_6)
C: a[1..3]  ↔  Python: a[0..2]   (a_1, a_2, a_3)
C: n[1..4]  ↔  Python: n[0..3]   (n, m, p, sigma)
```

### CODATA values are frozen at 2006

To preserve bit-identical output to the C reference, the Python port uses
the 2006 values of G, h, e, etc. — not modern (post-2019 SI redefinition)
values. Do not "modernise" them without also re-baselining all expected
outputs.

### Empirically fitted constants

Three constants in `calc_phi` are flagged `[FITTED #1..#3]` in both C and
Python sources:

```
FOURTH_ROOT_2     = 2^(1/4)            # ≈ 1.1892
PI_OVER_E_SQR     = (pi/e)^2           # ≈ 1.3360
FOUR_PI_OVER_4RT2 = 4*pi*2^(-1/4)      # ≈ 10.5697
```

Per Heim (1989, p. 19) these were fitted to empirical particle data.
Sensitivity analysis shows they are essentially inert — see README. The
analysis scripts patch them via `setattr(formulae, ...)`.

### Equation references

`[B##]` always refers to the IGW Innsbruck restatement
(`downloads/pdfs/F_1989_en.pdf`). `1982 eq.(I)`, `eq.(IX)`, `eq.(X)` refer
to Heim's 1982 paper (`downloads/pdfs/E_1982.pdf`). The full derivation
chapters 7–9 are *not* publicly available — only the first 10 of 81 pages
are in `D_Herleitung.pdf`.

## Working style for this repository

- **Don't add features the user did not ask for.** This is an analysis
  project, not a refactor. Improvements to the formula's correctness must
  be verified against the literature before being applied.
- **Preserve the upstream code under `downloads/c_impl/` verbatim.** Edits
  should land in `annotated/` (annotation-only) or `python/` (port and
  derivative work). Changes to `downloads/c_impl/` would lose the
  reference baseline.
- **Numerical changes require verification.** Any change that affects
  computation must reproduce the 21 reference masses to ≥8 digits or be
  flagged as deliberate.
- **Cite the source equation.** When adding code that implements something
  from `[1989]`, tag the relevant block with `[B##]` so future readers can
  cross-reference.
- **Don't update git config.** The repo was initialised with a one-shot
  `-c user.email=… -c user.name=…` for the first commit (`miacwess@gmail.com`,
  `lambdamikel`). Continue that pattern if more commits are needed in the
  same session.

## License caveat for code generation

The upstream C code (Eli Gildish, 2006) is non-commercial. Derivative work
in this repository (annotations, Python port, analysis) inherits those
terms. Do not relicense — and warn the user before doing anything that
would imply commercial use, redistribution under different terms, or
sublicensing.

## Known open questions (not blocking work — just context)

1. The functional form of η is *defined*, not derived, in the publicly
   available manuscripts. Whether it follows from the 6D field equations
   is the central open question.
2. The greedy decomposition in `calc_n` produces integer occupation
   numbers that flip discontinuously with small perturbations of W, making
   the loss landscape jagged. This is a feature of the algorithm, not a
   numerical bug.
3. Lifetimes and resonance widths predicted by Heim's full system are not
   implemented in either Gildish's C code or our Python port. Adding them
   would substantially widen the empirical test surface.
4. Equation [B25] in the 1989 PDF shows `Q_n^2`, but Heim's own
   research-group C# implementation (`downloads/csharp_impl/.../HeimGroup/
   SelfCouplingFunction.cs`) uses `Q_n^3`, matching Eli Gildish's C and
   our Python port. The PDF has a typesetting error; `Q_n^3` is correct.
   Resolved 2026-04.
