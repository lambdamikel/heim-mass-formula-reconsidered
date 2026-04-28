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
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include "constant.h"
#include "particle.h"
#include "formulae.h"

particle          *particle_list = NULL;    /* the list of the paticles */


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
particle*
make_particle(char *name, char *symb, int eps, int k, int P, int Q, int kap,
    int x, real mexp)
{
    register size_t     memory,   length;
    register particle  *retval, **runner;

    length = strlen(name);
    memory = sizeof(particle) + length + strlen(symb) + 2;

    if ((retval = (particle *) malloc(memory)) == NULL)
    {
        return NULL;
    }

    retval->name = strcpy((char *) retval +  sizeof(particle), name);
    retval->symb = strcpy((char *)(retval->name + length + 1), symb);

    runner = &particle_list;

    while (*runner != NULL)
    {
        runner = &(*runner)->next;
    }

   *runner = retval;

    retval->eps  = eps;
    retval->k    = k;
    retval->P    = P;
    retval->Q    = Q;
    retval->kap  = kap;

    retval->chrg = calc_charge(eps, k, P, Q, kap, x);
    retval->mexp = mexp;
    retval->mass = calc_mass(eps, k, P, Q, kap, retval->chrg);

    retval->mass = retval->mass * KG2MEV;

    return retval;
}

/*
 * Function name : free_particle
 * Description   : function removes a particle from the global list of the
 *                 particles and deallocates the object and it's variables
 * Arguments     : particle* - the pointer to an allocated particle object
 * Returns       : void      - nothing is returned
 */
void
free_particle(particle *argval)
{
    if (particle_list != NULL)
    {
        register particle  **runner;

        runner = &particle_list;

        while ((*runner != NULL) && (*runner != argval))
        {
            runner = &(*runner)->next;
        }

       *runner = (*runner)->next;
    }

    free((void *)argval);
}

/*
 * Function name : stat_particles
 * Description   : function generates a list of all the objects present in
 *                 the module and writes it into the requested file stream
 * Arguments     : file*     - the pointer to filestream control structure
 * Returns       : void      - nothing is returned
 */
void
stat_particles(FILE *stream)
{
    register real       rerror;
    register particle  *runner;


    fputs("\n\n"
        " === particles ===============================================================\n"
        " =============================================================================\n"
        " name               | symbol   | q_x | m_the   [Mev] | m_exp   [Mev] | error %\n"
        " -----------------------------------------------------------------------------\n",
        stream);

    runner = particle_list;

    while (runner != NULL)
    {
        if (runner->mexp)
        {
            rerror = 100.0 * (runner->mass / runner->mexp - 1.0);
            fprintf(stream, " %-18s | %-8s | %3.1g | %13.8f | %13.8f | %6.3f%%\n",
                runner->name, runner->symb, runner->chrg, runner->mass, runner->mexp, rerror);
        }
        else
        {
            fprintf(stream, " %-18s | %-8s | %3.1g | %13.8f | %13s | %6s\n",
                runner->name, runner->symb, runner->chrg, runner->mass, "", "");
        }

        runner = runner->next;
    }

    fputs(
        " =============================================================================\n",
        stream);
}
