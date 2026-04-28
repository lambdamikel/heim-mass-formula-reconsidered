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

#ifndef __PARTICLE_H__
#define __PARTICLE_H__
typedef
struct particle particle;

#ifndef __REAL_H__
#define __REAL_H__
typedef
double          real;
#endif


#define T_INVALID  (0)            /* the identifier of invalid particle */
#define T_BOSSON   (1)            /* the identifier of bosson particles */
#define T_LEPTON   (2)            /* the identifier of lepton particles */
#define T_MESSON   (3)            /* the identifier of messon particles */
#define T_BARYON   (4)            /* the identifier of baryon particles */


struct particle
{
    char          *name;          /* the scientific name of a  particle */
    char          *symb;          /* the scientific symbol of  particle */
    int            type;          /* the type identifier of a  particle */
    real           chrg;          /* the electric charge quantum number */
    real           mass;          /* the theoretical  mass of  particle */
    real           mexp;          /* the experimental mass of  particle */
    particle      *next;          /* the next object in the linked list */

    int            eps;
    int            k;
    int            P;
    int            Q;
    int            kap;
};

extern particle   *particle_list; /* the list of an elementary paticles */


/*
 * Function name : make_particle
 * Description   : function allocates the particle object and its internal
 *                 variables and places it on the end of the particle list
 * Arguments     : char*     - the name of the particle  common in science
 *                 char*     - the symbol of the particle  used in physics
 *                 int       - the time-helicity (R4 & mirror R4 selector)
 *                 int       - the configuration number ( metrical index )
 *                 int       - the double iso-spin of particle (P = 2 * s)
 *                 int       - the double spin of the particle (Q = 2 * J)
 *                 int       - the doublet number (dist. between doublets)
 *                 int       - the particles iso-spin multiplet identifier
 *                 real      - the particle mass as measured in experiment
 * Returns       : particle* - the pointer to an allocated particle object
 */
extern particle*
make_particle(char*, char*, int, int, int, int, int, int, real);

/*
 * Function name : free_particle
 * Description   : function removes a particle from the global list of the
 *                 particles and deallocates the object and it's variables
 * Arguments     : particle* - the pointer to an allocated particle object
 * Returns       : void      - nothing is returned
 */
extern void
free_particle(particle*);

/*
 * Function name : stat_particles
 * Description   : function generates a list of all the objects present in
 *                 the module and writes it into the requested file stream
 * Arguments     : file*     - the pointer to filestream control structure
 * Returns       : void      - nothing is returned
 */
extern void
stat_particles(FILE*);


#endif
