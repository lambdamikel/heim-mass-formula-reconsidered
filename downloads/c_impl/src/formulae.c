/*
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
 * Description   : function calculates the  electric charge quantum number
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

    alp_P = pi * Q * (kap         + bincoeff(P, 2));
    alp_Q = pi * Q * (Q * (k - 1) + bincoeff(P, 2));

    eps_P = eps * cos(alp_P);
    eps_Q = eps * cos(alp_Q);

    C     = 2.0 * (eps_P * P  + eps_Q * Q) * (k + kap - 1) /
        (k * (1 + kap));

    return ((P - 2.0 * x) * (1.0 - Q * kap * (2.0 - k)) +
        eps * (k - 1.0 - Q * (1.0 + kap) * (2.0 - k)) + C) / 2.0;
}

/*
 * Function name : calc_Q
 * Description   : function calculates the "Q" parameters of mass formulae
 * Arguments     : int       - the configuration number ( metrical index )
 *                 int*      - the pointer to the array of the Q variables
 * Returns       : int*      - the pointer to the array of the Q variables
 */
static int*
calc_Q(int k, int *I)
{
    register int   z = (int)pow(2.0, pow(k, 2.0));

    I[1] = 3 * z / 2;
    I[2] = 2 * z - 1;
    I[3] = 2 * (z + (int)pow(-1.0, k));
    I[4] = z - 1;

    return I;
}

/*
 * Function name : calc_N
 * Description   : function calculates the "N" parameters of mass formulae
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

    eta    = query_eta(1, 0);
    eta_11 = query_eta(1, 1);
    eta_1k = query_eta(1, k);
    eta_q1 = query_eta(q, 1);
    eta_qk = query_eta(q, k);
    tet    = query_tet(eta);
    tet_q1 = query_tet(eta_q1);
    alp_p  = query_alp_p(eta, tet);
    alp_n  = query_alp_n(eta, tet);

    z      = pow(2.0, pow(k, 2.0));
    u      = 2.0 * pi * exp(1.0);

    H      = I[1] + I[2] + I[3] + I[4];
    I_1    = H + 0.5 * z * k * pow(-1.0, k);
    I_2    = H - 2.0 * k - 1.0;

    D      = (8.0 / eta) * (1.0 - alp_n / alp_p) * (1.0 - 3.0 * eta / 4.0);

    N[1] = 0.5 * (1.0 + sqrt(eta_qk));

    N[2] = 2.0 / (3.0 * eta_qk);

    N[3] = exp((k - 1.0) * ( 1.0 - pi * ((1.0 - eta_qk) / (1.0 + sqrt(eta_q1))) *
        (1.0 - u * (eta_q1 / tet_q1) * (1.0 - alp_n / alp_p) *
        pow(1.0 - sqrt(eta), 2.0)) ) - ( 4.0 / (3.0 * u) *
        pow(1.0 - sqrt(eta), 2.0) * ((1.5 * pow(u, 2.0) / tet) *
        (1.0 + sqrt(eta_q1)) / (1.0 - eta) - 1.0) )) * (2.0  / k);

    N[4] = 4.0 * (1.0 + q * (k - 1.0)) / k;

    N[5] = D + k * (k - 1.0) * 8.0 * z * I_1 *
        pow(D * (1.0 - sqrt(eta_qk)) / (1.0 + sqrt(eta_qk)), 2.0);

    N[6] = ( 64.0 * k * eta * I[4] ) / ( u * tet ) * ( 1.0 - alp_n / alp_p ) *
        pow((1.0 - sqrt(eta)) / (1.0 + sqrt(eta)), 2.0) * ( sqrt(k) *
        (k * k - 1.0) * I_1 / sqrt(eta_1k) * ( q - (1.0 - q) * I_2 /
        (I[1] * sqrt(eta_1k)) ) + pow(-1.0, k + 1.0) );

    return N;
}

/*
 * Function name : calc_a
 * Description   : function calculates the "a" parameters of mass formulae
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
    H   = I[1] + I[2] + I[3] + I[4];
    B   = 3.0 * H / (k * k * (2.0 * k - 1.0));

    P2  = bincoeff(P, 2);
    P3  = bincoeff(P, 3);
    Q3  = bincoeff(Q, 3);

    a[1] = 1.0 + B + k * (Q * Q + 1.0) * Q3 -
        kap * ((B - 1.0) * (2.0 - k) - 3.0 * (P - Q) * (H - 2.0 * (1.0 + q)) + 1.0) -
        (1 - kap) * ((2.0 - k) * ( 3.0 * (2.0 - q) * P2 - Q * (3.0 * (P + Q) + q)) +
        (k - 1.0) * (k * (P + 1.0) * P2 + (1.0 + (B / k) * (k + P - Q)) * (1.0 - P2) *
        (1.0 - Q3) - q * (1.0 - q) * Q3) );

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

    a[3] = (4.0 * B * Y / (Y + 1)) - (1.0 / (B + 4.0));

    return a;
}

/*
 * Function name : calc_W
 * Description   : function calculates the "W" parameter for mass formulae
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

    H   = I[1] + I[2] + I[3] + I[4];
    g   = pow(I[1], 3.0) + pow(I[2], 2.0) + I[3] * exp(k - 1.0) / k +
        exp((1.0 - 2.0 * k) / 3.0) - (k - 1.0) * H;

    A   = 8.0 * g * H / (2.0 - k + 8 * H * (k - 1.0));
    B   = 3.0 * H / (k * k * (2.0 * k - 1.0));

    a   = calc_a(eps, k, P, Q, kap, q_x, I, avalue - 1);

    X  = (2.0 - k) * (1 - Q - P2) + (a[1] +
        pow(k, 3.0) * (a[2] + a[3] / (4.0 * B)) / (4.0 * H)) / (4.0 * B);

    return A * exp(X) * pow(1.0 - eta, Q * (1.0 - kap) * (2.0 - k)) +
        sqrt(2.0) * (P - Q) * (1.0 - P2) * (1.0 - Q3) * pow(1.0 - sqrt(eta), 2.0);
}

/*
 * Function name : calc_n
 * Description   : function calculates the quadruples  (n, m, p and sigma)
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

    alp[1] = N[1];
    alp[2] = N[2] * 1.5;
    alp[3] = N[3] * 0.5;

    w[1] = W;
    K[1] = (int)(pow(w[1] / alp[1], 1.0 / 3.0) + 0.01);

    w[2] = w[1] - alp[1] * pow(K[1], 3.0);
    K[2] = (int)(sqrt(w[2] / alp[2]) + 0.01);

    w[3] = w[2] - alp[2] * pow(K[2], 2.0);
    K[3] = (int)((w[3] / alp[3]) + 0.01);

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

    n[1] = K[1] - I[1];
    n[2] = K[2] - I[2];
    n[3] = K[3] - I[3];
    n[4] = K[4] - I[4];

    return n;
}

/*
 * Function name : calc_phi
 * Description   : function calculates the value of self coupling function
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

    U = (P * P + 1.5 * (P - Q) + P * (1.0 - q) +
        (1.0 - Q) * 4.0 * kap * B / (3.0 - 2.0 * q) +
        (k - 1.0) * (P + 2.0 * Q - (4.0 * pi / pow(2.0, 1.0/4.0)) *
        (P - Q) * (1.0 - q))) * pow(2.0, k + P + Q + kap) / (eta_qk * eta_qk);

    return (n[3] * n[3] * N[4]) / (1.0 + n[3] * n[3]) * (n[4] + I[4]) /
        sqrt(1.0 + n[4] * n[4]) * ( pow(2.0, 1.0/4.0) - 4.0 * B * U / W) -
        (P + 1) * bincoeff(Q, 3) / alpha + P * pow(P - 2.0, 2.0) *
        (I[2] - I[1]) * sqrt(eta_12) * ( 1.0 + kap * (1.0 - q) /
        (2.0 * alpha * tet) ) * pow(pi / exp(1.0), 2.0);
}

/*
 * Function name : calc_mass
 * Description   : function calculates the mass of the elementary particle
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

    I   = calc_Q(k, ivalue - 1);
    N   = calc_N(k, q, I, nvalue - 1);
    W   = calc_W(eps, k, P, Q, kap, q_x, I);
    n   = calc_n(k, I, N, W, quadrs - 1);

    K   = pow(n[1] * (n[1] + 1.0), 2.0) * N[1] +
        n[2] * (2.0 * n[2] * n[2] + 3.0 * n[2] + 1.0) * N[2] +
        n[3] * (n[3] + 1.0) * N[3] + 4.0 * n[4];

    S   = pow(I[1] * (I[1] + 1.0), 2.0) * N[1] +
        I[2] * (2.0 * I[2] * I[2] + 3.0 * I[2] + 1.0) * N[2] +
        I[3] * (I[3] + 1.0) * N[3] + 4.0 * I[4];

    F   = 2.0 * n[1] * I[1] * ( 1.0 + 3.0 * (n[1] + I[1] + n[1] * I[1]) +
        2.0 * (n[1] * n[1] + I[1] * I[1])) * N[1] +
        6.0 * n[2] * I[2] * (1.0 + n[2] + I[2]) * N[2] +
        2.0 * n[3] * I[3] * N[3] + calc_phi(k, P, Q, kap, q, n, I, N, W);

    PHI = P * pow(-1.0, P + Q) * (P + Q) * N[5] + Q * (P + 1) * N[6];

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
