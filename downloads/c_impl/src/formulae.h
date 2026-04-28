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

#ifndef __FORMULAE_H__
#define __FORMULAE_H__


#ifndef __REAL_H__
#define __REAL_H__
typedef double real;
#endif


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
extern real
calc_charge(int, int, int, int, int, int);

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
extern real
calc_mass(int, int, int, int, int, real);

/*
 * Function name : stat_formulaes
 * Description   : function generates a statistics on all the formulaes in
 *                 the module and writes it into the requested file stream
 * Arguments     : file*     - the pointer to filestream control structure
 *                 particle* - the pointer to the heading of particle list
 * Returns       : void      - nothing is returned
 */
extern void
stat_formulaes(FILE*, particle*);


#endif
