/*
 * ============================================================================
 *  formulae.c — Annotated Reference Implementation of Heim's 1989 Mass Formula
 * ============================================================================
 *
 *  Original code: Eli Gildish, 2006 (see LICENSE notice at end of file).
 *  Annotations:   added 2026 — cross-references to "Heim's Mass Formula
 *                 (1989), IGW Innsbruck 2002/2003" (file F_1989_en.pdf),
 *                 hereafter cited as [1989].
 *
 *  Code is functionally unchanged from the upstream version. Only comments
 *  have been added or extended. Any tag of the form [B##] refers to the
 *  numbered equations in [1989], pages 11–17.
 *
 *  --------------------------------------------------------------------------
 *  Variable name mapping  (code  →  [1989]  →  meaning)
 *  --------------------------------------------------------------------------
 *      eps      ε              time-helicity sign, ±1
 *      k        k              metrical/configuration index, k ∈ {1, 2, …}
 *      P        P              double iso-spin (P = 2 s)
 *      Q        Q              double angular momentum (Q = 2 J)
 *      kap      κ              doublet indicator, ∈ {0, 1}
 *      x        x              iso-spin multiplet identifier
 *      q_x      ε·q            signed elementary charge, q = |q_x|
 *      I[1..4]  Q_n,Q_m,Q_p,Q_σ four "structure constants" (eq. X of 1982)
 *      n[1..4]  n,m,p,σ        the four occupation numbers of the structure
 *                              zones — extracted from W via [B42..B46]
 *      N[1..6]  N_1..N_6       the "N-functions" (eq. IX of 1982 + [B8..B14])
 *      a[1..3]  a_1, a_2, a_3  combinatorial parameters [B29..B31]
 *      W        W_(N=0)        zone-occupation weight  [B22]
 *      eta      η              η(q,k) auxiliary function (1982 eq. I)
 *      tet      θ              θ(η) = 5η + 2√η + 1
 *      alp_p,n  α_+, α_-       structure constants [B4]
 *      miu      μ              "mass element" (≈ proton mass scale)
 *
 *  --------------------------------------------------------------------------
 *  Function map
 *  --------------------------------------------------------------------------
 *      calc_charge    →  [B2]              (with α_Q from [B1])
 *      calc_Q         →  Q_n,Q_m,Q_p,Q_σ   (eq. X of 1982; not in [1989])
 *      calc_N         →  N_1,N_2 from 1982 eq. IX; N_3 = [B8]; N_4 = [B9];
 *                        N_5 = [B10] with A from [B11], N(k) from [B12];
 *                        N_6 = [B13] with N'(k) from [B14]
 *      calc_a         →  a_1 [B30], a_2 [B29], a_3 [B31] (Y is the "y'·2B"
 *                        bracket inside [B31])
 *      calc_W         →  W_(N=0) = [B22], with A [B23], H [B24], g [B25],
 *                        L [B26], x [B27], B [B28]
 *      calc_n         →  exhaustion algorithm of [B40..B46]
 *                        (extracts n,m,p,σ from W_(N=0))
 *      calc_phi       →  self-coupling φ from [B7] (referred as [B49])
 *                        and U from [B50], Z from [B51]
 *      calc_mass      →  main mass formula M = [B3]
 *
 *  --------------------------------------------------------------------------
 *  EMPIRICALLY FITTED CONSTANTS  (Heim 1989, concluding remarks p. 19)
 *  --------------------------------------------------------------------------
 *  "the free eligible parameters for the expression φ with eq.(B50) were
 *   fitted by empirical facts [i.e. ⁴√2, (π/e)², and 4π·⁴√(1/2)]"
 *
 *  Locations in this file:
 *      [FITTED #1]  pow(2.0, 1.0/4.0)               = ⁴√2
 *                   in calc_phi (return statement, factor before "- 4*B*U/W")
 *                   maps to [B7] / [B50] inner factor
 *
 *      [FITTED #2]  pow(pi / exp(1.0), 2.0)         = (π/e)²
 *                   in calc_phi (final term involving sqrt(eta_12))
 *                   maps to second additive piece of [B7]
 *
 *      [FITTED #3]  4.0 * pi / pow(2.0, 1.0/4.0)    = 4π·⁴√(1/2)
 *                   in calc_phi inside U (calc_phi line "U = …")
 *                   maps to coefficient (4π/⁴√2) in [B50]
 *
 *  --------------------------------------------------------------------------
 *  Master equation  [B3]
 *  --------------------------------------------------------------------------
 *      M = μ · α_+ · [(G + S + F + Φ) + 4 q α_-]
 *
 *  Note on naming: the upstream code names two different things "phi":
 *      Φ  (capital, named PHI in calc_mass)  is [B6]
 *           = P·(-1)^(P+Q)·(P+Q)·N_5  +  Q·(P+1)·N_6
 *      φ  (lowercase, calc_phi)  is [B7] / [B49]
 *           the "self-coupling function" embedded in F  via [B5]:
 *           F = 2nQ_n[…]·N_1 + 6mQ_m[…]·N_2 + 2pQ_p·N_3  +  φ·δ(N)
 *
 *  In this file: PHI (in calc_mass) is the [B6] term, while calc_phi is the
 *  [B7] self-coupling that is added inside the F-sum (last piece, where
 *  calc_mass calls "+ calc_phi(...)" inside the F formula).
 *  ============================================================================
 */

#include <math.h>
#include <stdio.h>
#include "constant.h"
#include "particle.h"
#include "formulae.h"


/*
 * Function name : factorial
 * Description   : function calculates the factorial n! (or product of all
 *                 natural numbers less than and equal to n) of a number n
 * Arguments     : int       - the natural numb. to find the factorial for
 * Returns       : int       - the factorial of natural number in argument
 */
static int
factorial(int arg)
{
    return (arg <= 1) ? 1 : arg * factorial(arg - 1);
}

/*
 * Function name : bincoeff
 * Description   : function calculates binomial coefficient of the natural
 *                 number n and the integer k, which is n! / k! / (n - k)!
 *                 Used throughout the formula as ( P  2 ), ( P  3 ), ( Q  3 )
 *                 in the [1989] notation.
 * Arguments     : int       - the "numenator" of the binomial coeffecient
 *                 int       - the denumenator of the binomial coeffecient
 * Returns       : int       - the binomial coeffecient of the two numbers
 */
static int
bincoeff(int num, int den)
{
    return ((den < 0) || (den > num)) ? 0 : factorial(num) /
        (factorial(den) * factorial(num - den));
}

/*
 * Function name : calc_charge
 * Description   : function calculates the  electric charge quantum number.
 *                 Implements [B2]:
 *                   q_x = ½ · [ (P − 2x) · (1 − Q·κ·(2−k))
 *                              + ε · (k − 1 − Q·(1+κ)·(2−k))
 *                              + C ]
 *                 with C derived from α_Q [B1] applied to both P and Q
 *                 (alp_P, alp_Q below).
 *                 (Note: the displayed [B2] has "(P-2x+2)" — this code uses
 *                  "(P-2x)" because the upstream multiplet identifier x
 *                  ranges differently. Check against the 1982 eq.(II) for
 *                  exact convention.)
 * Arguments     : int       - the time-helicity (R4 & mirror R4 selector)
 *                 int       - the configuration number ( metrical index )
 *                 int       - the double iso-spin of particle (P = 2 * s)
 *                 int       - the double spin of the particle (Q = 2 * J)
 *                 int       - the doublet number (dist. between doublets)
 *                 int       - the particles iso-spin multiplet identifier
 * Returns       : real      - the particle electric charge quantum number
 */
real
calc_charge(int eps, int k, int P, int Q, int kap, int x)
{
    register real  alp_P, alp_Q, eps_P, eps_Q, C;

    /* α_P, α_Q angles — variant of [B1]: α_Q = π Q [Q + (P/2)] */
    alp_P = pi * Q * (kap         + bincoeff(P, 2));
    alp_Q = pi * Q * (Q * (k - 1) + bincoeff(P, 2));

    eps_P = eps * cos(alp_P);
    eps_Q = eps * cos(alp_Q);

    /* C is the structure-distributor (called "strangeness" in [1989], divided
     * by k per the [1989] introductory note) */
    C     = 2.0 * (eps_P * P  + eps_Q * Q) * (k + kap - 1) /
        (k * (1 + kap));

    /* Implements [B2] with the offset convention noted above */
    return ((P - 2.0 * x) * (1.0 - Q * kap * (2.0 - k)) +
        eps * (k - 1.0 - Q * (1.0 + kap) * (2.0 - k)) + C) / 2.0;
}

/*
 * Function name : calc_Q
 * Description   : function calculates the "Q" parameters of mass formulae,
 *                 i.e. Q_n, Q_m, Q_p, Q_σ in [1989] notation.
 *                 These are the four "structure constants" that depend
 *                 ONLY on k (not on the particle's quantum numbers).
 *                 They originate from eq.(X) of the 1982 paper; [1989]
 *                 reuses them without redefinition.
 *
 *                 Definitions encoded here (z = 2^(k²)):
 *                   Q_n = 3z/2
 *                   Q_m = 2z − 1
 *                   Q_p = 2(z + (−1)^k)
 *                   Q_σ = z − 1
 *
 *                 Note the explicit 2^(k²) — the structure constants grow
 *                 hyper-exponentially with k. For k=1: z=2, k=2: z=16,
 *                 k=3: z=512, etc.
 *
 * Arguments     : int       - the configuration number ( metrical index )
 *                 int*      - the pointer to the array of the Q variables
 * Returns       : int*      - the pointer to the array of the Q variables
 */
static int*
calc_Q(int k, int *I)
{
    register int   z = (int)pow(2.0, pow(k, 2.0));

    I[1] = 3 * z / 2;                        /* Q_n */
    I[2] = 2 * z - 1;                        /* Q_m */
    I[3] = 2 * (z + (int)pow(-1.0, k));      /* Q_p */
    I[4] = z - 1;                            /* Q_σ */

    return I;
}

/*
 * Function name : calc_N
 * Description   : function calculates the "N" parameters of mass formulae.
 *                 These are six functions of (k, q):
 *                   N_1, N_2  — from 1982 eq.(IX), unchanged in 1989
 *                   N_3       — [B8]  (greatly elaborated in 1989 vs 1982)
 *                   N_4       — [B9]  = (4/k)·[1 + q·(k−1)]
 *                   N_5       — [B10] using A [B11] and N(k) [B12]
 *                   N_6       — [B13] using N'(k) [B14]
 *                 N_5 and N_6 are NEW in 1989 (do not exist in 1982).
 * Arguments     : int       - the configuration number ( metrical index )
 *                 real      - the amount of electric charge quantum value
 *                 int*      - the pointer to the array of the Q variables
 *                 real*     - the pointer to the array of the N variables
 * Returns       : real*     - the pointer to the array of the N variables
 */
static real*
calc_N(int k, real q, int *I, real *N)
{
    register real  eta, eta_11, eta_1k, eta_q1, eta_qk, tet, tet_q1;
    register real  alp_p, alp_n, z, u, I_1, I_2, H, D;

    /* η evaluated at various (q,k) combinations — 1982 eq.(I) */
    eta    = query_eta(1, 0);
    eta_11 = query_eta(1, 1);
    eta_1k = query_eta(1, k);
    eta_q1 = query_eta(q, 1);
    eta_qk = query_eta(q, k);
    tet    = query_tet(eta);
    tet_q1 = query_tet(eta_q1);
    alp_p  = query_alp_p(eta, tet);          /* α_+ from [B4] */
    alp_n  = query_alp_n(eta, tet);          /* α_- from [B4] */

    z      = pow(2.0, pow(k, 2.0));          /* same z as in calc_Q */
    u      = 2.0 * pi * exp(1.0);            /* "u" as used in [B8]: u = 2πe */

    H      = I[1] + I[2] + I[3] + I[4];                /* H ≡ Q_n+Q_m+Q_p+Q_σ  [B24] */
    I_1    = H + 0.5 * z * k * pow(-1.0, k);           /* matches N(k) of [B12] modulo k(-1)^k·2^(k-1) */
    I_2    = H - 2.0 * k - 1.0;                        /* matches N'(k) of [B14] */

    D      = (8.0 / eta) * (1.0 - alp_n / alp_p) * (1.0 - 3.0 * eta / 4.0);
                                                       /* D = A from [B11] */

    /* N_1 — from 1982 eq.(IX). Form: ½(1 + √η_qk) */
    N[1] = 0.5 * (1.0 + sqrt(eta_qk));

    /* N_2 — from 1982 eq.(IX). Form: 2/(3·η_qk) */
    N[2] = 2.0 / (3.0 * eta_qk);

    /* N_3 — [B8]. The 1989 elaboration. The 2/k prefactor comes from solving
     * "ln(N_3 · k/2) = …" for N_3 (i.e. N_3 = (2/k)·exp[…]).
     * The expression inside exp() exactly mirrors [B8]. */
    N[3] = exp((k - 1.0) * ( 1.0 - pi * ((1.0 - eta_qk) / (1.0 + sqrt(eta_q1))) *
        (1.0 - u * (eta_q1 / tet_q1) * (1.0 - alp_n / alp_p) *
        pow(1.0 - sqrt(eta), 2.0)) ) - ( 4.0 / (3.0 * u) *
        pow(1.0 - sqrt(eta), 2.0) * ((1.5 * pow(u, 2.0) / tet) *
        (1.0 + sqrt(eta_q1)) / (1.0 - eta) - 1.0) )) * (2.0  / k);

    /* N_4 — [B9]. Form: (4/k)·[1 + q(k-1)]. */
    N[4] = 4.0 * (1.0 + q * (k - 1.0)) / k;

    /* N_5 — [B10] with D = A [B11] and the (1 - √η_qk)/(1 + √η_qk) ratio. */
    N[5] = D + k * (k - 1.0) * 8.0 * z * I_1 *
        pow(D * (1.0 - sqrt(eta_qk)) / (1.0 + sqrt(eta_qk)), 2.0);

    /* N_6 — [B13] with I_2 = N'(k) [B14] and I_1 the N(k)-analog [B12]. */
    N[6] = ( 64.0 * k * eta * I[4] ) / ( u * tet ) * ( 1.0 - alp_n / alp_p ) *
        pow((1.0 - sqrt(eta)) / (1.0 + sqrt(eta)), 2.0) * ( sqrt(k) *
        (k * k - 1.0) * I_1 / sqrt(eta_1k) * ( q - (1.0 - q) * I_2 /
        (I[1] * sqrt(eta_1k)) ) + pow(-1.0, k + 1.0) );

    /* eta_11 read above is part of the [1989] notation but is unused in
     * this routine; preserved for clarity. */
    (void)eta_11;

    return N;
}

/*
 * Function name : calc_a
 * Description   : function calculates the "a" parameters of mass formulae.
 *                 a_1, a_2, a_3 are combinatorial coefficients used inside
 *                 the W weight [B22] via x [B27].
 *                   a_1 = [B30]  (note: in [1989] B30 comes after B29!)
 *                   a_2 = [B29]
 *                   a_3 = [B31]
 *                 The "Y" in this code corresponds to the "y'·2B" bracket
 *                 inside [B31]: a_3 = 4B·(y'/(y'+1)) − 1/(B+4).
 * Arguments     : int       - the time-helicity (R4 & mirror R4 selector)
 *                 int       - the configuration number ( metrical index )
 *                 int       - the double iso-spin of particle (P = 2 * s)
 *                 int       - the double spin of the particle (Q = 2 * J)
 *                 int       - the doublet number (dist. between doublets)
 *                 real      - the particle electric charge quantum number
 *                 int*      - the pointer to the array of the Q variables
 *                 real*     - the pointer to the array of the a variables
 * Returns       : real*     - the pointer to the array of the a variables
 */
static real*
calc_a(int eps, int k, int P, int Q, int kap, real q_x, int *I, real *a)
{
    register int   H, P2, P3, Q3;
    register real  eta, q, B, Y;

    q   = fabs(q_x);

    eta = query_eta(1, 0);
    H   = I[1] + I[2] + I[3] + I[4];                   /* H [B24] */
    B   = 3.0 * H / (k * k * (2.0 * k - 1.0));         /* B [B28] */

    P2  = bincoeff(P, 2);
    P3  = bincoeff(P, 3);
    Q3  = bincoeff(Q, 3);

    /* a_1 — [B30]. */
    a[1] = 1.0 + B + k * (Q * Q + 1.0) * Q3 -
        kap * ((B - 1.0) * (2.0 - k) - 3.0 * (P - Q) * (H - 2.0 * (1.0 + q)) + 1.0) -
        (1 - kap) * ((2.0 - k) * ( 3.0 * (2.0 - q) * P2 - Q * (3.0 * (P + Q) + q)) +
        (k - 1.0) * (k * (P + 1.0) * P2 + (1.0 + (B / k) * (k + P - Q)) * (1.0 - P2) *
        (1.0 - Q3) - q * (1.0 - q) * Q3) );

    /* a_2 — [B29]. */
    a[2] = B * (1.0 - Q3 * (1.0 - P3)) + (6.0 / k) -
        kap * (0.5 * Q * (B - 7.0 * k) - (3.0 * q - 1.0) * (k - 1.0) +
        0.5 * (P - Q) * (4.0 + (B + 1.0) * (1.0 - q))) -
        (1 - kap) * ((2.0 - k) * (P * (0.5 * B + q + 2.0) -
        Q * (0.5 * B + 1.0 - 4.0 * (1.0 + 4.0 * q))) +
        (k - 1.0) * (1.0 - Q3) * ( 0.25 * (B - 2.0) * (1.0 + 1.5 * (P - Q)) -
        0.5 * B * (1 - q) - P2 * ((2.0 - eps * q_x) * (0.5 * (B + q - eps * q_x) +
        3.0 * eps * q_x) - 0.25 * (B + 2.0) * (1.0 - q))) -
        P3 * (2.0 * (1.0 + eps * q_x) + 0.5 * (2.0 - q) * (3.0 * (1.0 - q) +
        eps * q_x - q) - 0.25 * q * (1.0 - q) * (B - 4.0) - 0.25 * (B - 2.0) +
        0.5 * B * (1.0 - q)) );

    /* Y — the "y'·2B" expression inside [B31]. */
    Y    = kap * ( (sqrt(eta) / k) * ( 4.0 * (2.0 - sqrt(eta)) -
        pi * exp(1.0) * sqrt(eta) * (1.0 - eta)) * (k + exp(1.0) * sqrt(eta) * (k - 1.0)) +
        5.0 * (1.0 - q) * (4.0 * B + P + Q) / (2.0 * k + pow(-1.0, k)) ) +
        (1 - kap) * ((P - 1.0) * (P - 2.0) * (2.0 / (k * k) * (H + 2.0) + 0.5 * (2.0 - k) / pi) +
        P2 * (1.0 - Q3) * (0.5 * q * B * (B + 2.0 * (P - Q)) +
        (k - 1) * (P * (P + 2.0) * B + pow(P + 1.0, 2.0) - q * (1.0 + eps * q_x) *
        (k * (P * P + 1.0) * (B + 2.0) + 0.25 * (P * P + P + 1.0)) -
        q * (1.0 - eps * q_x) * (B + P * P + 1.0)) + ((P - Q) * (H + 2.0) +
        P * (5.0 * B * (1.0 + q) * Q + k * (k - 1.0) *
        ( k * pow(P + Q, 2.0) * (H + 3.0 * k + 1.0) * (1.0 - q) -
        0.5 * (B + 6.0 * k)))) * (1.0 - P2) * (1.0 - Q3) + P3 * (2.0 - q) * Q *
        (eps * q_x * (B + 2.0 * Q + 1.0) + (0.5 * q / k) * (1.0 - eps * q_x) *
        (2.0 * k + 1.0) + (1.0 - q) * (Q * Q + 2.0 * B + 1.0)) ) );

    Y    = 0.5 * Y / B;

    /* a_3 — [B31]. y' = Y in the upstream variable naming. */
    a[3] = (4.0 * B * Y / (Y + 1)) - (1.0 / (B + 4.0));

    return a;
}

/*
 * Function name : calc_W
 * Description   : function calculates the "W" parameter for mass formulae.
 *                 Implements W_(N=0) = [B22]:
 *                   W = A · e^x · (1 − η)^L
 *                       + (P − Q) · (1 − (P 2)) · (1 − (Q 3)) · (1 − √η)² · √2
 *                 with A [B23], L [B26] = (1−κ)·Q·(2−k), x [B27], B [B28].
 * Arguments     : int       - the time-helicity (R4 & mirror R4 selector)
 *                 int       - the configuration number ( metrical index )
 *                 int       - the double iso-spin of particle (P = 2 * s)
 *                 int       - the double spin of the particle (Q = 2 * J)
 *                 int       - the doublet number (dist. between doublets)
 *                 real      - the particle electric charge quantum number
 *                 int*      - the pointer to the array of the Q variables
 * Returns       : real      - the value of the parameter Wvx = W(N=0) = W
 */
static real
calc_W(int eps, int k, int P, int Q, int kap, real q_x, int *I)
{
    real           avalue[6], *a;
    register int   P2, Q3;
    register real  eta, H, g, A, B, X;

    eta = query_eta(1,0);
    P2  = bincoeff(P, 2);
    Q3  = bincoeff(Q, 3);

    H   = I[1] + I[2] + I[3] + I[4];                          /* H [B24] */

    /* g [B25] — uses I[1]^3 (Q_n^3). The IGW Innsbruck reformulation prints
     * "Q_n^2" in [B25], but Heim's own research-group C# implementation
     * (downloads/csharp_impl/.../HeimGroup/SelfCouplingFunction.cs) uses
     * Q_n^3, in agreement with this code. The PDF has a typesetting error;
     * Q_n^3 is correct. */
    g   = pow(I[1], 3.0) + pow(I[2], 2.0) + I[3] * exp(k - 1.0) / k +
        exp((1.0 - 2.0 * k) / 3.0) - (k - 1.0) * H;

    A   = 8.0 * g * H / (2.0 - k + 8 * H * (k - 1.0));        /* A [B23] */
    B   = 3.0 * H / (k * k * (2.0 * k - 1.0));                /* B [B28] */

    a   = calc_a(eps, k, P, Q, kap, q_x, I, avalue - 1);

    /* x [B27]:  [1 − Q − (P 2)] · (2 − k)  +  (1/4B) · [a_1 + (k³/4H) · (a_2 + a_3/4B)] */
    X  = (2.0 - k) * (1 - Q - P2) + (a[1] +
        pow(k, 3.0) * (a[2] + a[3] / (4.0 * B)) / (4.0 * H)) / (4.0 * B);

    /* W [B22]. The exponent on (1 − η) is L = Q·(1 − κ)·(2 − k) [B26]. */
    return A * exp(X) * pow(1.0 - eta, Q * (1.0 - kap) * (2.0 - k)) +
        sqrt(2.0) * (P - Q) * (1.0 - P2) * (1.0 - Q3) * pow(1.0 - sqrt(eta), 2.0);
}

/*
 * Function name : calc_n
 * Description   : function calculates the quadruples (n, m, p and σ) by
 *                 the "exhaustion process" of [B40..B46]:
 *
 *                   (n+Q_n)³·α_1 + (m+Q_m)²·α_2 + (p+Q_p)·α_3
 *                                + exp[−(2k−1)/(3Q_σ)·(σ+Q_σ)]
 *                       = W_(N=0) · (1 + f(N))                           [B40]
 *
 *                 with α_1 = N_1, α_2 = (3/2)·N_2, α_3 = (1/2)·N_3.
 *
 *                 The greedy decomposition recovers, in order:
 *                   K_n = ⌊(w/α_1)^(1/3)⌋,    w_1 = w − (K_n − 1)³·α_1   [B42]
 *                   K_m = ⌊√(w_1/α_2)⌋,       w_2 = w_1 − (K_m − 1)²·α_2 [B43]
 *                   K_p = ⌊w_2/α_3⌋,          w_3 = w_2 − (K_p − 1)·α_3  [B44]
 *                   then w_3 − exp(−βK) ≤ 0 fixes K_σ                    [B45]
 *                 and finally:
 *                   n = K_n − 1 − Q_n,  m = K_m − 1 − Q_m,
 *                   p = K_p − 1 − Q_p,  σ = K_σ − 1 − Q_σ                [B46]
 *
 *                 The code uses one-step-shifted K (no "-1" in cube/square),
 *                 which is algebraically equivalent.
 *
 * Arguments     : int       - the configuration number ( metrical index )
 *                 int*      - the pointer to the array of the Q variables
 *                 real*     - the pointer to the array of the N variables
 *                 int*      - the pointer to the vector of the quadruples
 *                 real      - the value of the parameter W[N=0](1 + f(N))
 * Returns       : int*      - the pointer to the vector of the quadruples
 */
static int*
calc_n(int k, int *I, real *N, real W, int *n)
{
    int            kvalue[4], *K   = kvalue - 1;
    real           wvalue[4], *w   = wvalue - 1;
    real           alphas[3], *alp = alphas - 1;;

    /* α_1, α_2, α_3 from [B40] (note the 3/2 and 1/2 factors). */
    alp[1] = N[1];
    alp[2] = N[2] * 1.5;
    alp[3] = N[3] * 0.5;

    /* Step 1: cubic coefficient — [B42] */
    w[1] = W;
    K[1] = (int)(pow(w[1] / alp[1], 1.0 / 3.0) + 0.01);

    /* Step 2: quadratic coefficient — [B43] */
    w[2] = w[1] - alp[1] * pow(K[1], 3.0);
    K[2] = (int)(sqrt(w[2] / alp[2]) + 0.01);

    /* Step 3: linear coefficient — [B44] */
    w[3] = w[2] - alp[2] * pow(K[2], 2.0);
    K[3] = (int)((w[3] / alp[3]) + 0.01);

    /* Step 4: exponential remainder — [B45] with β = (2k−1)/(3·Q_σ) */
    w[4] = w[3] - alp[3] * K[3];

    if (w[4] <= 0.0)
    {
        K[4]  = (int)((alp[3] * K[3]) + 0.01);
    }
    else if (w[4] > 1.0)
    {
        K[4] = (int)((-3.0 * I[4] * log(w[4]) / (2.0 * k - 1.0)) + 0.01);

        K[3]--;
        K[4] += (int)(alp[3] * K[3]);
    }
    else
    {
        K[4] = (int)((-3.0 * I[4] * log(w[4]) / (2.0 * k - 1.0)) + 0.01);
    }

    /* [B46]: n_i = K_i − Q_i  (the "−1" is absorbed into the K-shift above) */
    n[1] = K[1] - I[1];
    n[2] = K[2] - I[2];
    n[3] = K[3] - I[3];
    n[4] = K[4] - I[4];

    return n;
}

/*
 * Function name : calc_phi
 * Description   : function calculates the value of self coupling function.
 *                 Implements φ from [B7] / [B49]:
 *
 *   φ = [N_4·p²/(1+p²)] · [(σ+Q_σ)/√(1+σ²)] · [⁴√2 − 4·B·U·W^(−1)]
 *       + P·(P−2)²·(1 + κ·(1−q)/(2αθ))·(π/e)²·√η_12·(Q_m − Q_n)
 *       − (P+1)·(Q 3)/α
 *
 *                 with U from [B50]:
 *
 *   U = 2^Z · [P² + (3/2)(P−Q) + P(1−q) + 4κB(1−Q)/(3−2q)
 *              + (k−1){P + 2Q − (4π/⁴√2)·(P−Q)·(1−q)}] · η_qk^(−2)
 *
 *                 and Z = k + P + Q + κ from [B51].
 *
 *                 ⚠  This function contains all three EMPIRICALLY FITTED
 *                    constants per Heim (1989) p.19:
 *                       ⁴√2          → pow(2, 1/4)        [FITTED #1]
 *                       (π/e)²       → pow(pi/e, 2)       [FITTED #2]
 *                       4π/⁴√2       → 4π · pow(2, -1/4)  [FITTED #3]
 *
 * Arguments     : int       - the configuration number ( metrical index )
 *                 int       - the double iso-spin of particle (P = 2 * s)
 *                 int       - the double spin of the particle (Q = 2 * J)
 *                 int       - the doublet number (dist. between doublets)
 *                 real      - the particle electric charge quantum number
 *                 int*      - the vector of metrical structure elements n
 *                 int*      - the pointer to the array of the Q variables
 *                 real*     - the pointer to the array of the N variables
 *                 real      - the value of the parameter Wvx = W(N=0) = W
 * Returns       : real      - the result of self coupling func evaluation
 */
static real
calc_phi(int k, int P, int Q, int kap, real q_x, int *n, int *I, real *N, real W)
{
    register real  q, alpha, eta_12, eta_qk, tet, H, B, U;

    q      = fabs(q_x);
    alpha  = query_alpha();
    eta_12 = query_eta(1,2);
    eta_qk = query_eta(q,k);
    tet    = query_tet(query_eta(1,0));

    H      = I[1] + I[2] + I[3] + I[4];
    B      = 3.0 * H / ( k * k * (2.0 * k - 1.0));

    /* U — [B50]. Note 2^Z = 2^(k+P+Q+κ) per [B51]. */
    U = (P * P + 1.5 * (P - Q) + P * (1.0 - q) +
        (1.0 - Q) * 4.0 * kap * B / (3.0 - 2.0 * q) +
        (k - 1.0) * (P + 2.0 * Q - (4.0 * pi / pow(2.0, 1.0/4.0)) *
                                /* ^^^^^^^^^^^^^^^^^^^^^^^^^^ [FITTED #3]  4π/⁴√2 */
        (P - Q) * (1.0 - q))) * pow(2.0, k + P + Q + kap) / (eta_qk * eta_qk);

    /* φ proper — [B7]. Three additive pieces:
     *   1)  envelope · [⁴√2 − 4BU/W]      ← contains [FITTED #1]
     *   2)  P·(P−2)²·(1 + …)·(π/e)²·…    ← contains [FITTED #2]
     *   3)  −(P+1)·(Q 3)/α
     */
    return (n[3] * n[3] * N[4]) / (1.0 + n[3] * n[3]) * (n[4] + I[4]) /
        sqrt(1.0 + n[4] * n[4]) * ( pow(2.0, 1.0/4.0) - 4.0 * B * U / W) -
                                /* ^^^^^^^^^^^^^^^^^ [FITTED #1]  ⁴√2 */
        (P + 1) * bincoeff(Q, 3) / alpha + P * pow(P - 2.0, 2.0) *
        (I[2] - I[1]) * sqrt(eta_12) * ( 1.0 + kap * (1.0 - q) /
        (2.0 * alpha * tet) ) * pow(pi / exp(1.0), 2.0);
                              /* ^^^^^^^^^^^^^^^^^^^^^^^^ [FITTED #2]  (π/e)² */
}

/*
 * Function name : calc_mass
 * Description   : function calculates the mass of the elementary particle.
 *                 Implements [B3]:
 *                   M = μ · α_+ · [(G + S + F + Φ) + 4 q α_-]
 *
 *                 where:
 *                   G  = "G underline" [B5] — depends only on k, q
 *                   S  = analogous Σ over occupations (n,m,p,σ)
 *                   F  = cross terms in (n·Q_n) etc. + φ (self-coupling) [B5]
 *                   Φ  = P·(-1)^(P+Q)·(P+Q)·N_5 + Q·(P+1)·N_6              [B6]
 *
 *                 The four occupation numbers (n,m,p,σ) come from calc_n()
 *                 via the exhaustion algorithm [B40..B46]. The 4qα_- term
 *                 is the new 1989 correction, absent in the 1982 formula.
 *
 * Arguments     : int       - the time-helicity (R4 & mirror R4 selector)
 *                 int       - the configuration number ( metrical index )
 *                 int       - the double iso-spin of particle (P = 2 * s)
 *                 int       - the double spin of the particle (Q = 2 * J)
 *                 int       - the doublet number (dist. between doublets)
 *                 real      - the particle electric charge quantum number
 * Returns       : real      - the mass of a particle as predicted by Heim
 */
real
calc_mass(int eps, int k, int P, int Q, int kap, real q_x)
{
    int            ivalue[4], *I, quadrs[4], *n;
    real           nvalue[6], *N;
    register real  q, eta, tet, W, K, S, F, PHI;

    q   = fabs(q_x);
    eta = query_eta(1,0);
    tet = query_tet(eta);

    I   = calc_Q(k, ivalue - 1);                              /* Q_n,Q_m,Q_p,Q_σ */
    N   = calc_N(k, q, I, nvalue - 1);                        /* N_1..N_6 */
    W   = calc_W(eps, k, P, Q, kap, q_x, I);                  /* W_(N=0) [B22] */
    n   = calc_n(k, I, N, W, quadrs - 1);                     /* (n,m,p,σ) [B40-B46] */

    /* K = "occupation contribution" — same shape as the G underline term
     * in [B5] but with n,m,p,σ instead of Q_n,Q_m,Q_p,Q_σ. */
    K   = pow(n[1] * (n[1] + 1.0), 2.0) * N[1] +
        n[2] * (2.0 * n[2] * n[2] + 3.0 * n[2] + 1.0) * N[2] +
        n[3] * (n[3] + 1.0) * N[3] + 4.0 * n[4];

    /* S = "structure-constant contribution" — the G underline term in [B5];
     * same shape as K but with I_i (= Q_n etc.) instead of n_i. */
    S   = pow(I[1] * (I[1] + 1.0), 2.0) * N[1] +
        I[2] * (2.0 * I[2] * I[2] + 3.0 * I[2] + 1.0) * N[2] +
        I[3] * (I[3] + 1.0) * N[3] + 4.0 * I[4];

    /* F — [B5]. Cross terms n_i·Q_i, plus the self-coupling φ. */
    F   = 2.0 * n[1] * I[1] * ( 1.0 + 3.0 * (n[1] + I[1] + n[1] * I[1]) +
        2.0 * (n[1] * n[1] + I[1] * I[1])) * N[1] +
        6.0 * n[2] * I[2] * (1.0 + n[2] + I[2]) * N[2] +
        2.0 * n[3] * I[3] * N[3] + calc_phi(k, P, Q, kap, q, n, I, N, W);

    /* Φ — [B6].  (Distinct from φ! Capital Phi uses N_5 and N_6.) */
    PHI = P * pow(-1.0, P + Q) * (P + Q) * N[5] + Q * (P + 1) * N[6];

    /* M — [B3]. The "+ 4qα_-" is the 1989 addition over 1982. */
    return query_miu() * query_alp_p(eta, tet) *
        (K + S + F + PHI + 4.0 * q * query_alp_n(eta, tet));
}

/*
 * Function name : stat_formulaes
 * Description   : function generates a statistics on all the formulaes in
 *                 the module and writes it into the requested file stream
 * Arguments     : file*     - the pointer to filestream control structure
 *                 particle* - the pointer to the heading of particle list
 * Returns       : void      - nothing is returned
 */
void
stat_formulaes(FILE *stream, particle *oblist)
{
    int                 ivalue[4], *I, quadrs[4], *n = quadrs - 1;
    real                nvalue[6], *N, avalue[3], *a = avalue - 1;
    register int        k;
    register real       q,  W, phi;
    register particle  *runner;

    fputs("\n\n"
        " === N params ================================================================\n"
        " =============================================================================\n"
        " k : q |    N_1    |    N_2    |    N_3    |    N_4    |    N_5    |    N_6   \n"
        " -----------------------------------------------------------------------------\n",
        stream);

    for (k = 1; k <= 2; k++)
    {
        I = calc_Q(k, ivalue - 1);

        for (q = 0; q <= 2; q = q + 1)
        {
            N = calc_N(k, q, I, nvalue - 1);

            fprintf(stream, " %1d : %1g | %9.6f | %9.6f | %9.6f | %9.6f | %9.6f | %9.6f\n",
                k, q, N[1], N[2], N[3], N[4], N[5], N[6]);
        }
    }

    fputs(
        " =============================================================================\n",
        stream);


    fputs("\n\n"
        " === functions ===============================================================\n"
        " =============================================================================\n"
        " particle |  n  |  m  |  p  | sig | a_1 | a_2 |   a_3   |     W     |   phi   \n"
        " -----------------------------------------------------------------------------\n",
        stream);

    runner = oblist;

    while (runner != NULL)
    {
        q = fabs(runner->chrg);

        I = calc_Q(runner->k, I);
        N = calc_N(runner->k, q, I, N);
        a = calc_a(runner->eps, runner->k, runner->P, runner->Q, runner->kap, runner->chrg, I, a);
        W = calc_W(runner->eps, runner->k, runner->P, runner->Q, runner->kap, runner->chrg, I);
        n = calc_n(runner->k, I, N, W, quadrs - 1);

        phi = calc_phi(runner->k, runner->P, runner->Q, runner->kap, runner->chrg, n, I, N, W);

        fprintf(stream, " %-8s | %3d | %3d | %3d | %3d | %3.3g | %3.3g | %7.3f | %9.3f | %8.3f\n",
            runner->symb, n[1], n[2], n[3], n[4], a[1], a[2], a[3], W, phi);

        runner = runner->next;
    }

    fputs(
        " =============================================================================\n",
        stream);
}

/*
 * ============================================================================
 *  Original upstream license (preserved verbatim):
 * ============================================================================
 * Copyright (c) 2006 Eli Gildish (netloc@gmail.com). All rights reserved.
 *
 * Redistribution  and  use in source  and  binary forms,  with or without
 * modification,  are permitted provided that the following conditions and
 * exceptions are met:
 *
 * - Redistribution of source code must retain the above copyright notice,
 *   this list of conditions and the following disclaimer.
 * - Redistributions  in  binary  form  must reproduce the above copyright
 *   notice,  this list of conditions  and the following disclaimer in the
 *   documentation  and/or other materials provided with the distribution.
 * - The name of the author may not be used to endorse or promote products
 *   derived from this software without specific prior written permission.
 * - Any commercial distribution  or use whatsoever is not allowed without
 *   a written permission from the author.
 *
 * THIS SOFTWARE IS PROVIDED AS IS, AND ANY EXPRESS OR IMPLIED WARRANTIES,
 * INCLUDING, BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY
 * AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL
 * THE AUTHOR BE LIABLE FOR ANY  DIRECT,  INDIRECT,  INCIDENTAL,  SPECIAL,
 * EXEMPLARY,  OR  CONSEQUENTIAL DAMAGES  (INCLUDING,  BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE  GOODS OR SERVICES;   LOSS OF USE,  DATA,  OR
 * PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED  AND  ON  ANY THEORY
 * OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE  OR  OTHERWISE)  ARISING IN  ANY  WAY OUT OF THE USE OF THIS
 * SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * ============================================================================
 */
