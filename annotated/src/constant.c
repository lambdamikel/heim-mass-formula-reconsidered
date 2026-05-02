/*
 * ============================================================================
 *  constant.c — Auxiliary functions η, θ, α_±, α (fine-structure), μ
 * ============================================================================
 *
 *  Annotations:  cross-references to "Heim's Mass Formula (1989), IGW
 *                Innsbruck 2002/2003" (file F_1989_en.pdf), cited as [1989].
 *
 *  These functions provide the dimensionless "structure constants" that
 *  feed the mass formula in formulae.c. None of these depends on a
 *  particle's quantum numbers — they are universal scaffold values.
 *
 *  --------------------------------------------------------------------------
 *  Function map
 *  --------------------------------------------------------------------------
 *      query_eta(q,k)   →  η(q,k) — 1982 eq.(I).  Form:
 *                                η(q,k) = ⁴√(π⁴ / (π⁴ + (4+k)·q⁴))
 *                          Note:  η ≡ η(1,0) (q=1, k=0) is the "default" η
 *                          used pervasively. η(q,k) → 1 for q→0 or large π⁴.
 *
 *      query_tet(η)     →  θ(η) — auxiliary, defined by 1982 eq.(I):
 *                                θ = 5η + 2√η + 1
 *
 *      query_alp_p(η,θ) →  α_+ = (η^(1/6)/η²)·(1 − θ·[2(1−√η)/(η(1+√η))]²·√(2η)) − 1
 *                          [B4]
 *
 *      query_alp_n(η,θ) →  α_- = (α_+ + 1)·η − 1                              [B4]
 *
 *      query_alpha()    →  Sommerfeld fine-structure constant α, derived from
 *                          [B58]–[B61]:
 *                              α·√(1 − α²) = (9θ/(2π)⁵)·(1 − C')
 *                          with K_α = 1 − C' from [B59]:
 *                              K_α = 1 − (1+η_22)/(η·η_11·η_12)
 *                                       · ((1−√η)/(1+√η))²
 *                          and α_+ = ½D'²(1 − √(1 − 4/D'²)) where
 *                          D' = (2π)⁵/(9θK_α).
 *                          The expected value is 1/α ≈ 137.0360, in
 *                          agreement with experiment to ~5 decimals.
 *
 *      query_miu()      →  μ — the "mass element", a pure-geometric mass
 *                          scale:
 *                              μ = π^(1/4) · (3πGℏs₀)^(1/3) · √(ℏ/(3cG)) / s₀
 *                          with s₀ = 1 m (gauge factor). μ ≈ 2.26·10⁻³¹ kg.
 *                          Built only from G, ℏ, c — the three genuine
 *                          natural constants of Heim's framework.
 *
 *  --------------------------------------------------------------------------
 *  CODATA values used (frozen in 2006)
 *  --------------------------------------------------------------------------
 *      G   = 6.6742e-11      (modern: 6.67430e-11; small drift, irrelevant)
 *      h   = 6.6260693e-34   (modern exact: 6.62607015e-34)
 *      c   = 299 792 458     (defined exact)
 *      e   = 1.60217653e-19  (modern exact: 1.602176634e-19)
 *
 *  These are *not* free parameters — they are inputs from physics. The only
 *  constants the Heim mass formula admits are G, ℏ, c (and π, e mathema-
 *  tically). Per [1989] §3, α is *derived*, not input.
 *  ============================================================================
 */

#include <math.h>
#include <stdio.h>
#include "constant.h"


/*
 * Function name : query_eta
 * Description   : function returns the eta constant used in Heims formula.
 *                 Implements 1982 eq.(I):
 *                     η(q,k) = (π⁴ / (π⁴ + (4+k)·q⁴))^(1/4)
 *
 *                 Properties:
 *                   • η(0, k) = 1                       (zero-charge limit)
 *                   • η(q, k) decreases with k and q    (more "bending")
 *                   • η(1, 0) ≈ 0.98999 ← the canonical "η"
 *                   • η(1, 1) ≈ 0.98770
 *                   • η(1, 2) ≈ 0.98519
 *
 *                 The (4 + k) coefficient and the *quartic* q-dependence
 *                 are derived in chapter 7 of "Zur Herleitung der Heimschen
 *                 Massenformel" (eqs. 7.47 → 7.51), from a metron-quantised
 *                 geometry plus the renormalisation ε'₀± = ε₀±·⁴√(1+k/4) of
 *                 the elementary charge field. The (4+k) factor falls out
 *                 of L·Δε₀±⁴ = 4·Δε₀±⁴, with L = 4 the dimensions
 *                 participating in charge condensation.
 *
 * Arguments     : real      - the amount of electric charge quantum value
 *                 int       - the configuration number ( metrical index )
 * Returns       : real      - the eta constant used in the Heim's formula
 */
real
query_eta(real q, int k)
{
    return pow(pow(pi, 4.0) / (pow(pi, 4.0) + (4.0 + k) * pow(q, 4.0)), 0.25);
}

/*
 * Function name : query_tet
 * Description   : function returns the tet constant used in Heims formula.
 *                 Implements 1982 eq.(I):  θ = 5η + 2√η + 1
 *                 This is a polynomial in √η:  θ = (√η)·(5√η + 2) + 1.
 *                 For η ≈ 1: θ ≈ 8 (used as θ ≈ 7.94 throughout).
 *
 * Arguments     : real      - the eta constant used in the Heim's formula
 * Returns       : real      - the tet constant used in the Heim's formula
 */
real
query_tet(real eta)
{
    return 5.0 * eta + 2.0 * sqrt(eta) + 1.0;
}

/*
 * Function name : query_alp_p
 * Description   : function returns the alp+ constant used in Heim formula.
 *                 Implements α_+ from [B4]:
 *                     α_+ = (⁶√η / η²) · ( 1 − θ · √(2η) · [2(1−√η)/(η·(1+√η))]² ) − 1
 *
 *                 For η ≈ 0.99: α_+ ≈ 0.0183. This is one of the two
 *                 universal "structure constants" that multiplies the entire
 *                 mass formula.
 *
 *                 NOTE: The relation between α_+ here and α_+ in the
 *                       fine-structure derivation [B58–B62] is non-trivial.
 *                       The same symbol "α_+" denotes two related but
 *                       distinct quantities; care needed when reading [1989].
 *
 * Arguments     : real      - the eta constant used in the Heim's formula
 *                 real      - the tet constant used in the Heim's formula
 * Returns       : real      - the alp+ constant used in the Heims formula
 */
real
query_alp_p(real eta, real tet)
{
    return pow(eta, -11.0/6.0) * (1.0 - tet * sqrt(2.0 * eta) *
        pow((2.0 * (1.0 - sqrt(eta))) / (eta * (1.0 + sqrt(eta))), 2.0)) - 1.0;
    /*  NB: pow(eta, -11/6) = ⁶√η / η²  (since -11/6 = 1/6 - 2). */
}

/*
 * Function name : query_alp_n
 * Description   : function returns the alp- constant used in Heim formula.
 *                 Implements α_- from [B4]:
 *                     α_- = (α_+ + 1) · η − 1
 *
 *                 For η ≈ 0.99 and α_+ ≈ 0.0183: α_- ≈ 0.00813.
 *
 *                 α_- enters the mass formula [B3] as the "charge-correction"
 *                 coefficient: + 4·q·α_-. This term is the principal addition
 *                 of the 1989 formula relative to 1982.
 *
 * Arguments     : real      - the eta constant used in the Heim's formula
 *                 real      - the tet constant used in the Heim's formula
 * Returns       : real      - the alp- constant used in the Heims formula
 */
real
query_alp_n(real eta, real tet)
{
    return eta * (query_alp_p(eta, tet) + 1.0) - 1.0;
}

/*
 * Function name : query_alpha
 * Description   : function calculates the Sommerfeld fine-structure constant
 *                 α according to Heim's derivation [B58]–[B62]:
 *
 *                     α · √(1 − α²) = (9θ / (2π)⁵) · (1 − C')                 [B58]
 *                     1 − C' = K_α
 *                            = 1 − (1 + η_22)/(η · η_11 · η_12)
 *                                  · [(1 − √η)/(1 + √η)]²                    [B59]
 *
 *                 Solving for α (taking the smaller positive root) yields a
 *                 value around 0.007297, i.e. 1/α ≈ 137.0360 — matching the
 *                 measured value to ~5 decimals.
 *
 *                 IMPORTANT: This is a derived value, not a fitted one.
 *                 No empirical input goes in besides π, e (Euler), and the
 *                 universal η, θ derivations from G, ℏ, c via the Heim
 *                 framework. This is the strongest single point in
 *                 favour of the theory.
 *
 *                 Returned: α directly (≈ 0.00729735…).
 *
 * Arguments     : void      - no arguments
 * Returns       : real      - the fine structure constant (~1.0 / 137.03)
 */
real
query_alpha()
{
    register real       eta, eta_11, eta_12, tet, A_1, A_2, cst;

    eta    = query_eta(1,0);
    eta_11 = query_eta(1,1);
    eta_12 = query_eta(1,2);
    tet    = query_tet(eta);

    /* A_1 = √η_11 · (1 − √η_11)/(1 + √η_11)
     * A_2 = √η_12 · (1 − √η_12)/(1 + √η_12)
     * The product A_1·A_2 plays the role of the (1 − √η)/(1 + √η) ratio in
     * [B59], extended to η_11 and η_12. */
    A_1    = sqrt(eta_11) * (1 - sqrt(eta_11)) / (1 + sqrt(eta_11));
    A_2    = sqrt(eta_12) * (1 - sqrt(eta_12)) / (1 + sqrt(eta_12));

    /* cst ≡ α·√(1 − α²) from [B58], where (1 − A_1·A_2) plays the role of
     * (1 − C') = K_α from [B59]. */
    cst    = 9.0 * tet * (1 - A_1 * A_2) / pow(2.0 * pi, 5.0);

    /* Solve  α·√(1 − α²) = cst  for α (smaller positive root):
     *   α² = ½(1 ± √(1 − 4·cst²))   →   α = √(α²) (lower branch).
     */
    return sqrt(0.5 * (1.0 - sqrt(1.0 - 4.0 * pow(cst, 2.0))));
}

/*
 * Function name : query_miu
 * Description   : function returns the miu constant used in Heim's formula.
 *                 The "mass element" μ — a pure-geometric mass scale built
 *                 from only G, ℏ, c (and a gauge length s₀ = 1 m):
 *
 *                     μ = π^(1/4) · (3π·G·ℏ·s₀)^(1/3) · √(ℏ/(3cG)) / s₀
 *
 *                 Numerical value: μ ≈ 2.259·10⁻³¹ kg ≈ 0.248 m_e.
 *                 The metron area τ = (3/8)·G·ℏ/c³ ≈ 6.15·10⁻⁷⁰ m² is the
 *                 ultimate origin of this scale; μ is essentially derived
 *                 from τ via dimensional consistency.
 *
 *                 The proton mass arises in the formula as roughly
 *                       m_p ≈ μ · α_+ · (Q-sum at k=2) ≈ 938 MeV
 *                 — i.e. the "α_+" prefactor and the very large structure
 *                 constants Q_n…Q_σ at k=2 (z = 2¹⁶ = 65 536) jointly
 *                 produce the baryon-scale numbers.
 *
 * Arguments     : void      - no arguments
 * Returns       : real      - the miu constant used in the Heim's formula
 */
real
query_miu()
{
    return pow(pi, 1.0/4.0) * pow(3.0 * pi * G * h_bar * s_0, 1.0/3.0) *
        sqrt(h_bar / (3.0 * c * G)) / s_0;
}

/*
 * Function name : stat_constants
 * Description   : function creates a list of all the constants present in
 *                 the module and writes it into the requested file stream
 * Arguments     : file*     - the pointer to filestream control structure
 * Returns       : void      - nothing is returned
 */
void
stat_constants(FILE *stream)
{
    register real       eta, tet;

    eta = query_eta(1,0);
    tet = query_tet(eta);

    fprintf(stream, "\n\n"
        " === constants ===============================================================\n"
        " =============================================================================\n"
        " name                               | symbol  |     units    | value          \n"
        " -----------------------------------------------------------------------------\n"
        " pi                                 | pi      |     -----    | %15.10g\n"
        " eta                                | eta     |     -----    | %15.10g\n"
        " theta                              | tet     |     -----    | %15.10g\n"
        " alpha_+                            | alp+    |     -----    | %15.10g\n"
        " alpha_-                            | alp-    |     -----    | %15.10g\n"
        " speed of light                     | c       |    m / s     | %15.10g\n"
        " gravitational constant             | G       | N * m^2 / kg | %15.10g\n"
        " elementary charge                  | e       |       C      | %15.10g\n"
        " planck's constant                  | h       |     J * s    | %15.10g\n"
        " dirac's constant                   | h-bar   |     J * s    | %15.10g\n"
        " constant of induction              | miu_0   |     N / A    | %15.10g\n"
        " constant of influence              | eps_0   |     F / m    | %15.10g\n"
        " fine structure constant            | alpha   |     -----    | %15.10g\n"
        " gauge factor                       | s_0     |       m      | %15.10g\n"
        " mass element                       | miu     |       kg     | %15.10g\n"
        " =============================================================================\n",
        pi, eta, tet, query_alp_p(eta, tet), query_alp_n(eta, tet), c, G,
        e, h, h_bar, miu_0, eps_0, query_alpha(), s_0, query_miu());
}

/*
 * ============================================================================
 *  Original upstream license (preserved verbatim):
 * ============================================================================
 * Copyright (c) 2006 Eli Gildish (netloc@gmail.com). All rights reserved.
 *
 * Redistribution  and  use in source  and  binary forms,  with or without
 * modification,  are permitted provided that the following conditions and
 * exceptions are met:  [...]  (full text in formulae.c)
 * ============================================================================
 */
