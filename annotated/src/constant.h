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

#ifndef __CONSTANT_H__
#define __CONSTANT_H__

#ifndef __REAL_H__
#define __REAL_H__
typedef double real;
#endif

/*
 * Variable name : KG2MEV
 * Description   : conversions among kilograms and megaelectronvolts (MeV)
 */
#define KG2MEV    ((real)5.609588357e+29)

/*
 * Variable name : pi
 * Description   : the mathematical constant pi is a real number, which is
 *                 defined as the ratio of a circle's circumference to its
 *                 diameter in Euclidean geometry
 */
#define pi         ((real)3.14159265358979323846264338327950288419716939937510)

/*
 * Variable name : c
 * Description   : the speed of light in vacuum has originally denoted the
 *                 distance light travels in an absolute vacuum per a time
 *                 period;  however,  lately its value was rounded and the
 *                 standard meter was redefined to  represent the distance
 *                 traveled by light in a vacuum per 1/299792458 of second
 */
#define c          ((real)299792458.0)

/*
 * Variable name : G
 * Description   : the law of universal gravitation states that attractive
 *                 force between two bodies is proportional to the product
 *                 of their masses and inversely proportional to square of
 *                 the distance between them;   the constant of proportion
 *                 is known as the "universal gravitational constant"
 */
#define G          ((real)6.6742e-11)

/*
 * Variable name : e
 * Description   : the elementary electrical charge, e,  is defined as the
 *                 absolute value of electrical charge carried by a single
 *                 electron or equivalently by a single proton
 */
#define e          ((real)1.60217653e-19)

/*
 * Variable name : h
 * Description   : the Planck's constant, h, relates the energy in quantum
 *                 of electromagnetic radiation (photon) to it's frequency
 */
#define h         ((real)6.6260693e-34)

/*
 * Variable name : h_bar
 * Description   : the reduced form of Planck's constant known as h-bar or
 *                 as Dirac's constant, frequently appears in formulations
 *                 of quantum mechanics;  h-bar equals h divided by 2 * pi
 */
#define h_bar      ((real)(0.5 * h / pi))

/*
 * Variable name : miu_0
 * Description   : the magnetic constant (or constant of induction), miu_0
 *                 represents the permeability,  i.e. the degree of magne-
 *                 tization, of the vacuum
 */
#define miu_0      ((real)4.0e-7 * pi)

/*
 * Variable name : eps_0
 * Description   : the electric constant (or constant of influence), eps_0
 *                 represents the permittivity,  i.e. the ability to store
 *                 electrical charge, of the vacuum
 */
#define eps_0      ((real)(1.0 / miu_0 / (c * c)))

/*
 * Variable name : s_0
 * Description   : the gauge factor, s_0, is defined as the sensitivity of
 *                 the strain gauge,  i.e. the vacuum's relative change in
 *                 resistance to the applied strain
 */
#define s_0        ((real)1.0)

/*
 * Function name : query_eta
 * Description   : function returns the eta constant used in Heims formula
 * Arguments     : real      - the amount of electric charge quantum value
 *                 int       - the configuration number ( metrical index )
 * Returns       : real      - the eta constant used in the Heim's formula
 */
extern real
query_eta(real, int);

/*
 * Function name : query_tet
 * Description   : function returns the tet constant used in Heims formula
 * Arguments     : real      - the eta constant used in the Heim's formula
 * Returns       : real      - the tet constant used in the Heim's formula
 */
extern real
query_tet(real);

/*
 * Function name : query_alp_p
 * Description   : function returns the alp+ constant used in Heim formula
 * Arguments     : real      - the eta constant used in the Heim's formula
 *                 real      - the tet constant used in the Heim's formula
 * Returns       : real      - the alp+ constant used in the Heims formula
 */
extern real
query_alp_p(real, real);

/*
 * Function name : query_alp_n
 * Description   : function returns the alp- constant used in Heim formula
 * Arguments     : real      - the eta constant used in the Heim's formula
 *                 real      - the tet constant used in the Heim's formula
 * Returns       : real      - the alp- constant used in the Heims formula
 */
extern real
query_alp_n(real, real);

/*
 * Function name : query_alpha
 * Description   : function calculates the fine structure constant, alpha,
 *                 the calculation is done according to the Heim's formula
 * Arguments     : void      - no arguments
 * Returns       : real      - the fine structure constant (~1.0 / 137.03)
 */
extern real
query_alpha();

/*
 * Function name : query_miu
 * Description   : function returns the miu constant used in Heims formula
 * Arguments     : void      - no arguments
 * Returns       : real      - the miu constant used in the Heim's formula
 */
extern real
query_miu();

/*
 * Function name : stat_constants
 * Description   : function creates a list of all the constants present in
 *                 the module and writes it into the requested file stream
 * Arguments     : file*     - the pointer to filestream control structure
 * Returns       : void      - nothing is returned
 */
extern void
stat_constants(FILE*);

#endif
