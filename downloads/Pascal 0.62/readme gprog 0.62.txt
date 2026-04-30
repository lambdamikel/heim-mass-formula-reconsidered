GPROG pas -- Unified formula of elementary masses by Burkhard Heim (1982) in Pascal
===================================================================================

Transscription of program GPROG dated 17/03/1982 by H.D.Schulz, DESY, Germany
Formulas given by Burkhard Heim 17/09/1978
Transscription 2006 by Olaf Posdzech for Turbo-Pascal, Free Pascal
C version by leovinus.


Changelog
0.62c 06-03-20 + Corrections in output formatting (less spaces).
               + Moved up test print of GLIMIT. 
               + Added note "Resonance not allowed" to mass values in case c.
               + Fixed a bug resulting from limited number length in connection
                 with periodical numbers. 
                 Example values given for e-:
                 changed K4 = trunc (0.333333333333333 / 1 * 3 ) = 0
                 into    K4 = trunc (0.333333333333333 / 1 * 3 + 0.0000000001) = 1
                 Added an internal truncation offset of 0.0000000001 to all truncations.
                 (Until N=10 only the value of e- changed).
               + Fixed missing brackets in calculating a[2,2] and at the end of wg2.
                 This changed values of Lambda, Sigma, omega, omikrons(!), Delta. 
               + Fixed wrong closing bracket in aq:=... . 
                 This changed resonances of p, n, sigma, omikrons, delta.
               - Overflows when computing very large N > 180!
               - Failed to run the program with free pascal.
0.61  06-03-15 + Changed remaining reals into type extended (20 digits).
               - Inaccurate value of wg2 in the case of multiplet 11 (omicron).
                 Resonance limits match 100% those calculated in 
                 'Heim 1982 mass formula 0.6.xls' except those of omicrons.
               - Overflows when computing very large N > 180!
               - Failed to run the program with free pascal.
0.6   06-03-14   First running version using extended accuray (20 digits)
0.5	         Removed numerical correction (rounding up when Ki>x.99) because this 
                 produced an error in neutron (N=4).
                 This is in accordence with [2]. The notes in [1] and [4] regarding 
                 wrong values in some cases might have been an effect of too less 
                 digits used in a historic programming language.



Notes:
I fixed some errors in gprogin.dat.
Changed the quantum numbers of omicron from (2330) to (2310).
Changed the name of multiplet (2111) from theta to xi.
Both changes according to Illobrand von Ludwiger.
(OP2006)

Hints:
It is possible to minimize the mismatch of computed particle masses
with the their empirical values using the gravitational constant g/gamma.
A value of gam=6.67279915e-11 + 0.0000015 achieved that. This needs  to 
be done with taking more particles into account such as tau.

The quantum number sets named nue1...nue3 found in the original 1982 DESY code are unnecessary when computing particle masses.

Contact: Olaf Posdzech, op@engon.de