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


/*
 * Function name : query_eta
 * Description   : function returns the eta constant used in Heims formula
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
 * Description   : function returns the tet constant used in Heims formula
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
 * Description   : function returns the alp+ constant used in Heim formula
 * Arguments     : real      - the eta constant used in the Heim's formula
 *                 real      - the tet constant used in the Heim's formula
 * Returns       : real      - the alp+ constant used in the Heims formula
 */
real
query_alp_p(real eta, real tet)
{
    return pow(eta, -11.0/6.0) * (1.0 - tet * sqrt(2.0 * eta) *
        pow((2.0 * (1.0 - sqrt(eta))) / (eta * (1.0 + sqrt(eta))), 2.0)) - 1.0;
}

/*
 * Function name : query_alp_n
 * Description   : function returns the alp- constant used in Heim formula
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
 * Description   : function calculates the fine structure constant, alpha,
 *                 the calculation is done according to the Heim's formula
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

    A_1    = sqrt(eta_11) * (1 - sqrt(eta_11)) / (1 + sqrt(eta_11));
    A_2    = sqrt(eta_12) * (1 - sqrt(eta_12)) / (1 + sqrt(eta_12));

    cst    = 9.0 * tet * (1 - A_1 * A_2) / pow(2.0 * pi, 5.0);

    return sqrt(0.5 * (1.0 - sqrt(1.0 - 4.0 * pow(cst, 2.0))));
}

/*
 * Function name : query_miu
 * Description   : function returns the miu constant used in Heims formula
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
