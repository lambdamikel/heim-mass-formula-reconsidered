/*
 *
 * Transcription of program GPROG dated 17/03/1982 by H.D.Schulz, DESY
 * Formulas given by Burkhard Heim 17/09/1978
 * Transcription 17/06/2001 by A. Mueller for MS-Fortran
 * Transcription 12/03/2006 by Olaf Posdzech for Turbo-Pascal, Free Pascal
 *  v0.61: Overflows when computing very large N > 180! See readme.txt for details.
 * Port to "C" by leovinus 16/03/2006.
 *
 * program reads as input from file 'gprogin.dat'
 *       Name of particle
 *       baryon number +1   = K
 *       2*isospin          = PG
 *       2*spin             = QG
 *       dublett factor     = KAPPA
 *
 * The original program consistently used REAL*16 in an IBM environment.
 *  3.1415926535Q0   replaced by 3.14159265358979D0
 *  x**0.25Q0       replaced by Dsqrt(Dsqrt(x))
 * function IBINOM(in,ik) rewritten
 * Fortran function IDINT overloaded for possible roundup, c.f. module ROUND
 * Default compiler settings should result in a 52 bit  FP precision
 *
 * Pascal (OP2006):  When calculating terms like b(:extended)= b + a*a*a Pascal uses
 * for the intermediate product a*a*a the same type as for a. Using a:int the
 * product runs out of range then.
 *               Integer        Longint
 * max value       32768     2147483647
 * ->max value K1     32           1290
 * ->max value K2    181          46340
 *
 * C port remarks
 * - use "gprog | sed 's/e+/E+/g' | sed 's/e-/E-/g'| sed 's/E+/E+00/g' | sed 's/E-/E-00/g' > out"
 *   to generate output which is compatible with the PASCAL output.
 * - check whether we use ROUND in correct places.
 * v0.66 25/04/2006
 * - added "tau" in table, improved neutrino computations, added cmd-line
 *   parameters. You can now do "gprog -gamma=6.673e-11" and similar stuff.
 *   Use "gprog -help" for more info.
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <limits.h>
#include <string.h>

static const int  ant  =1;    /* 1=process particles only, 2=process also antiparticles */
static  int  print=1;         /* set amount of outputs: 1=masses only, 2=basic, 3=intermediate results */
static  long nmax =10;        /* maximum resonance to be processed, 0=ground level only,
                                 1= till maximum lme, others=up to this level */
static  int  loop=40000;      /* end of search loop for maximum excitation level */
                              /* originally  hardcoded : nend = 112 , loop = 50000 */
static const int  ja = 1;     /* first multiplett to be calculated */
static const int  je = 200;   /* je<=15 last multiplet to be calculated. 200 is for much more input. */

/* Mhh, shouldn't be necessary*/
double round(double);
double trunc(double);
double myround(double x);

#if 1
# define ROUND   myround
# define ROUND2  myround
#else
  /* This is the PASCAL configuration */
# define ROUND  trunc
# define ROUND2 round
#endif

static FILE *fi; /* input file */

static char t1[100]; /* line buff for reading '... ' in gprogin.dat, only [24] needed */
static char particlename[100];

static double a[7][7];     /* Matrix A[rs] (GXXiV) of 6x6, keep pascalidx 1..6, ignore 0 */

  /* constants */

static double alfa,alfm,alfp,amu,beta,c,ebn,eq,eta,fakMeV,gam,hq,
              pi,rg,s0,theta,xi;                /* when using real gam*hq=0 (out of range) */

  /* quantum numbers*/

static int eps,k,P,Q,kappa,x,cs,qx,kq,n,xe,epsp,epsq;

  /* particle properties */

static long q1,q2,q3,q4,n1,n2,n3,n4,k1,k2,k3,k4,l1,l2,l3,l4;  /* amounts of protosimplexes in zones */

  /* when calculating terms like b(:double)= b + a*a*a pascal uses the same type as a
     for the intermediate product a*a*a. Using a:int the product runs out of range then. */

static double alf1,alf2,alf3,an1,an2,an3,
              gkq,wgxk,wgx,an,aq,agx,bgx,
              w1,w2,w3,w4,fn,kgh,fig,am,am_field;

static long lme,nend;                 /* maximum excitation level*/
static int i,j,epsi,ni;               /* counter in loops */
static char y;                        /* keystroke if needed */

/* WARNING - ni and y are unused in program !  */

/* Prototypes */
void GInit  (void);
void GValues(void);
void GBase  (void);
void GStruc (void);
void GLimit (void);
void GMass  (void);

/* Increase as necessary */
#define STRSIZE          64
#define MAX_NR_PARTICLES 1000

typedef struct
{
    char name[STRSIZE];
    char desc[STRSIZE];
    double computed_mass;
    double ref_mass;
    double std;
} Particle;

/*
 * Descriptor is "k P Q kappa#x qx cs#neutrino" with an optional "neutrino" part.
 * Basically, a neutrino is particle with no mass, just mass based on ist "field".
 *
 * Reference masses from 
 *  http://pdg.lbl.gov/2005/mcdata/mass_width_2004.csv
 * Other refs for neutrino masses/estimates
 *  http://www.citebase.org/cgi-bin/citations?id=oai:arXiv.org:hep-ph/0505028
 *  http://arxiv.org/ftp/physics/papers/0602/0602118.pdf
 *
 *    name      descriptor  comp.mass, ref mass, ref uncertainty 
 */
static Particle particle[MAX_NR_PARTICLES] = {

    { "eta",    "1000#100",  0.0, 547.75, 0.12},
    { "e-" ,    "1110#2-10", 0.0, 0.51099892, 4e-8 },
    { "mu",     "1111#1-10", 0.0, 105.658369, 0.00009 },
    { "tau",    "1111#1-10@2", 0.0, 1776.99, 0.29 },
    { "K+-",    "1101#111",  0.0, 493.677, 0.016},
    { "K0",     "1101#201",  0.0, 497.648, 0.022},
    { "pi0",    "1200#200",  0.0, 134.9766, 0.0006},
    { "pi+-",   "1200#110" , 0.0, 139.57018, 0.00035},
    { "lambda", "2010#10-1", 0.0, 1115.683, 0.006},
    { "omega",  "2030#1-1-3",0.0, 1672.45, 0.29},
    { "p",      "2110#110",  0.0, 938.27203,  8e-5 },
    { "n",      "2110#200",  0.0, 939.56536,  8e-5 },
    { "xi0",    "2111#10-2", 0.0, 1314.82, 0.20},
    { "xi-",    "2111#2-1-2",0.0, 1321.31, 0.13},
    { "sig+",   "2210#11-1", 0.0, 1189.37, 0.06},
    { "sig0",   "2210#20-1", 0.0, 1192.642, 0.024},
    { "sig-",   "2210#3-1-1",0.0, 1197.449 , 0.030},
    { "delta++","2330#120",  0.0, 1232, 2.0},
    { "delta+", "2330#210",  0.0, 1232, 2.0},
    { "delta0", "2330#300",  0.0, 1232, 2.0},
    { "delta-", "2330#4-10", 0.0, 1232, 2.0},
#if 0    
    { "neutrino1" , "1010#100#1", 0.0, -1.0 , 0.0 }, /* All uncharged */
    { "neutrino2" , "1110#100#1", 0.0, -1.0 , 0.0 }, /* No ref. mass  */
    { "neutrino3" , "1200#200#1", 0.0, -1.0 , 0.0 },
    { "neutrino4" , "2110#200#1", 0.0, -1.0 , 0.0 },
    { "neutrino5" , "2111#10-2#1", 0.0, -1.0 , 0.0 },
#else
    /* Here, we tried a more standard neutrino definition. */
    { "e-neutrino" ,   "1110#100#1",    0.0, -1.0 , 0.0 },  
    { "mu-neutrino" ,  "1111#1-10#1",   0.0, -1.0 , 0.0 },
    { "tau-neutrino" , "1111#1-10#1@2", 0.0, -1.0 , 0.0 },
#endif
};

static int nrParticles = 0; /* Init */

/* ---------------------------------------------------------------
 * Parse cmd line arguments and override variables if available.
 * Examples:
 * -gamma=6.674e-11
 * -rg=....
 * -print=..
 * -nmax=..
 * -maxloop=..
 * (No whitespace between parameter name and "=" and value!)
 */

typedef enum { Gamma, Rg, Print, Nmax, Maxloop, Help } OptionType ;

typedef struct {
 char      *name;
 OptionType type;
} Option;

static Option options[] = {
  { "-gamma=" ,  Gamma},
  { "-rg=",      Rg },
  { "-print=",   Print},
  { "-nmax=",    Nmax },
  { "-maxloop=", Maxloop },
  { "-help",     Help }
};

void parseArgs(int argc, char *argv[])
{
  int i,j;
  int found = 0;

  if (argc <= 1) return ; /* no args */

  for (i=1; i < argc; i++)
  {
    found = 0; /* Init */

    for (j=0; j < sizeof(options)/sizeof(Option); j++)
    {
        if (!strncmp(argv[i],options[j].name, strlen(options[j].name) ))
        {
          char *myarg = argv[i]+strlen(options[j].name);
          
          assert(strlen(argv[i]) >= strlen(options[j].name));
          
          if ( (strlen(argv[i]) > strlen(options[j].name)) || (options[j].type == Help))
          {  
             found = 1; /* We have a match for this cmdline param */

             if (options[j].type != Help)
                 printf("Cmd-line parameter %s overriding default value with %s\n", 
                         options[j].name, myarg);
             
             switch (options[j].type)
             {
               case Gamma  : gam   = atof(myarg); break;
               case Rg     : rg    = atof(myarg); break; 
               case Print  : print = atoi(myarg); if ((print < 1) || (print > 3)) print = 1; break;
               case Nmax   : nmax  = atoi(myarg); if (nmax < 1) nmax =10; break;
               case Maxloop: loop  = atoi(myarg); if (loop < 1) loop = 40000; break;
               case Help   :
                 fprintf(stderr,"Usage: %s -help -gamma=<value> -rg=<value> -print=1/2/3 -nmax=<value> -maxloop=<value>\n",argv[0]);
                 fprintf(stderr,"  -help     - prints this\n");
                 fprintf(stderr,"  -print=   - verbosity level. 1 is default, 2 is more, 3 is all.\n");
                 fprintf(stderr,"  -gamma=   - override default gravitational constant G. \n");
                 fprintf(stderr,"              Default 6.6733198e-11. Example -gamma=6.673e-11\n");
                 fprintf(stderr,"  -rg=      - override default vacumm wave resistance.\n");
                 fprintf(stderr,"              Default 376.730313461. Example -rg=376.73\n");
                 fprintf(stderr,"  -nmax=    - override maximum resonance  level of particle. 1 is all.\n");
                 fprintf(stderr,"              Default 10.\n");
                 fprintf(stderr,"  -maxloop= - override maximum excitation level of particle.\n");
                 fprintf(stderr,"              Default 40000.\n");

                 exit(1);
                 break;
             }
          }
          else
            fprintf(stderr,"Warning!! Empty cmdline option %s \n",argv[i]);
            
          break;
        } /* end if */
    } /* end j */

    if (found == 0) /* Was there a match for this cmdline param? */
      fprintf(stderr,"Unknown option %s !!\n",argv[i]);

  } /* end i */
}
/* ------------------------------------------------------------------- */

void initParticleList(void)
{
    int i = 0;
    while (particle[i++].ref_mass != 0.0);

    assert(i < MAX_NR_PARTICLES);

    nrParticles = i-1;
    printf("\nInitially, %d reference particles in list\n",nrParticles);
}

/* 
 * In order to uniquely identify particles in the final table, we 
 * use a string descriptor. This is composed by a mandatory part
 * "k P Q kappa#x qx cs" without whitespace. For example "1111#1-10".
 * In addition, we have two optional parts: an optional extension "#1"
 * if it is a neutrino like particle, and "@x" (with x a number > 1)
 * which indicates that it is not a groundstate, but an excitation.
 */
void makeParticleDescription(char *desc,int k_,int P_,int Q_,int kappa_,
                             int x_,int qx_,int cs_,int neutrino_, int excitation_)
{
  char neutrino_desc  [10];
  char excitation_desc[10];
  
  assert(desc);
  assert((neutrino_ == 0) || (neutrino_ == 1));
  assert(excitation_ >= 1);
  
  if (excitation_ == 1)
    strcpy(excitation_desc,"");                  /* Ground state - empty descriptor part */
  else
    sprintf(excitation_desc,"@%d", excitation_); /* A particle state different from "1" */

  if (neutrino_ == 0)
    strcpy(neutrino_desc,"");                /* Normal particle, not a neutrino */
  else
    sprintf(neutrino_desc,"#%d", neutrino_); /* Just field mass == neutrino */
 
  /* Assemble descriptor */
  sprintf(desc,"%d%d%d%d#%d%d%d%s%s",k_,P_,Q_,kappa_, x_, qx_, cs_, neutrino_desc, excitation_desc); 
}

void printParticle(Particle *p)
{
    double diff;

    assert(p);
    assert(p->ref_mass != 0.0);

    if (p->ref_mass != -1.0)
    {
        /* Reference mass available, so compute deviation. */
        diff = 100.0*(p->ref_mass - p->computed_mass)/ p->ref_mass;
        if (diff < 0.0) diff *= -1.0;
    }
    else
        diff = -1.0;

    printf("%12s = %12s = ref= %12.10g comp= %14.10g = diff[%%]=%10.3g%%\n",
            p->name, p->desc, p->ref_mass, p->computed_mass, diff );
}

int addParticle(int k_,int P_,int Q_,int kappa_,int x_,int qx_,int cs_, double mass, int neutrino_, int excitation_)
{
    char desc[STRSIZE];
    int  i, idx = -1;

    makeParticleDescription(desc,k_,P_,Q_,kappa_,x_,qx_,cs_,neutrino_, excitation_);
    assert(strlen(desc) > 0);

    for (i=0; i < nrParticles; i++)
    {
        /* DBG printParticle(&particle[i]); */

        if (strcmp(desc, particle[i].desc)==0)
        {
            /* Ok, found particle in list */
            /* assert(particle[i].computed_mass == 0.0); don't add twice :) */
            
            if (particle[i].computed_mass != 0.0) /* don't add twice :) */
            {
                fprintf(stderr,"WARNING: Your are adding particle '%s' for a 2nd time! Ignored!\n", particle[i].desc);
                return idx; /* exit routine */
            }
            
            particle[i].computed_mass = mass;
            idx = i;
        }
    }

    if ((idx == -1) && (print > 1) && (nrParticles < (MAX_NR_PARTICLES)))
    {
        /* Particle not yet in list. Maybe there was no given name or description. */
        /* So, add it - NOTE: to keep list small, we only add the additional possibilities for "print>1" */
        /* Note, we do not add more aprticles than MAX_NR_PARTICLES. */
        
        strcpy(particle[nrParticles].name,"-");
        strcpy(particle[nrParticles].desc,desc);
        particle[nrParticles].ref_mass = -1.0;
        particle[nrParticles].computed_mass = mass;

        nrParticles++;
        assert(nrParticles < MAX_NR_PARTICLES);
    }

    return idx;
}

void evaluate(void)
{
    int i,n = 0;
    double diff = 0.0;

    assert(nrParticles > 0);

    printf("   Particle  | description   |  reference mass |   computed mass     | diff[%%]\n");
    printf("     name    | kPQkap#x,qx,cs|                 |                     |    \n");
    printf("------------------------------------------------------------------------------------------\n");
    for(i=0; i< nrParticles; i++)
    {
        Particle *p = &particle[i];

        printParticle(p);

        if (p->ref_mass > 0.0) /* If ref_mass is given */
        {
            double d = 100.0*(p->computed_mass - p->ref_mass)/p->ref_mass;
            if (d < 0.0) d *= -1.0;

            diff += d;
            n    += 1;
        }
    }
    printf("-----------------------------------------------------------------------------------------\n");
    printf("NrParticles with reference mass= %d, avg. diff[%%]= %12.8g %%\n", n, diff/ (n*1.0) );
    printf("-----------------------------------------------------------------------------------------\n");
}

/*
 * This function does not work with b<0! Replaced such terms in the following
 * with the combination cos(pi*p)*po(-b,p)  (OP2006)
 * In many Heim terms full integer accuracy is needed. Better use b*b*b then po(b,3)
 *
FUNCTION po(b,p:extended):extended;     {when using real ga*hq=out of range}
   BEGIN if b=0 then po:=0 else po:=exp(p*ln(b)) END;

 * Just use pow() with double input.
 */

/* binomial coefficients */
int binom(int n,int k)
{
  int bi,d2,den;
  int binom=0;

  bi=1;
  d2=1;
  den=1;

  assert(n< 10); /* some 'random' restrictions to prevent overflow */
  assert(k <10);

  if (n < k)
    { binom = 0;}                /* not existent */
  else
  {
    if ((k == n) || (k==0))
      { binom = 1; }      /* borders */
    else
    {
      /* now k < n */
      for (i=1; i<=n; i++)      { bi=bi*i; }     /* fakul(n) */
      for (i=1; i<=k; i++)      { d2=d2*i; }     /* fakul(k) */
      for (i=1; i<=(n-k); i++)  { den=den*i; }   /* fakul(n-k) */

      binom = bi / (den*d2);   /* binom:= fakul(n)/(fakul(k)*fakul(n-k)) */
    }
  }

  return binom;
}

/* Functions needed for calculation =============================================== */

/* formel (7a), (V) */
/* Note: In recent Java code, kq=q and k=k. They could be int's*/
double etaqk(double kq, double k)
{
  double etaqk_ = 0.0;

  etaqk_ = pi / pow( kq*kq*kq*kq *(4.0 + k) + pi*pi*pi*pi, 0.25);

  return etaqk_;
}


/* TST function for C port - not in PASCAL. I suspect the FORTRAN round()
 * serves a similar goal.
 */
double myround(double x)
{
  double result,org;
  double eps = 0.0000001;
  int a,b;

  /* WARNING - the code is VERY sensitive to small variations!
   *
   * Comparing the use of myround() vs. trunc, switched via the ROUND macro in the heading.
   * Use trunc() to get baseline
   * myround() Use 0.000, 0.001, 0.01, 0.0000001 to see differences.
   *
   */
  org =x;

  if (x < 0.0)
   x = x - eps;
  else
   x = x + eps;

  a = ((int)trunc(x));
  b = ((int)trunc(org));
  if (a != b)
  {
    /* diff due to adding an eps */
    fprintf(stderr,"WARN:x~%d org~%d x=%.15e org=%.15e\n", a, b, x, org);
  }

  result = trunc(x);

  return(result);
}

/*
{Original FORTRAN procedure used to truncate numbers}
PROCEDURE round
     contains
    Integer*4 Function IDint( X )
shall overload Fortran IDint, to provide round up when abs(x) very closely below
an integer number, otherwise truncate.
    Real*8 X, BigOne
    Real*4 Y , Z
    data bigone/ 1.000 000 000 000 1 D0 /
used to override double precision truncation errors before truncating to integer
    Y = BigOne * X
    IDint = Int(Y)
C   IDint = IDNint(X)   ! das ergibt Fehler wegen w4 < 0 in Gstruc.for
    Z = X
C   if(int(Z) .ne. IDint) write(6,1) '### IDint of : X,Y = ',X,Y
1    format( 1x,a,D24.15,1pe15.7)
C     Protokolliert , wenn abs(Rest) > 0.5 verworfen wird :
C      if( abs(float(IDint))+0.5 .LT. abs(X) )
C   +  write(6,1) '### truncated: X, float(IDint) = ', X,float(IDint)
    return
    end  function Idint
    End Module ROUND
*/

/* Procedures used by main program================================================== */

/* Defining values of constants used */
void GValues(void)
{

  /* if more values are given the last one is active */
  /* (Sch) = Schulz 1982 (original code) */

#if 0
  /* old PASCAL code - deactivated */
  pi = 3.14159265358979E0;
  pi = 3.1415926535E0;   /*(Sch)*/
  pi = 4.0*arctan(1.0);
  ebn = exp(1.0);

  hq := 1.0545887E-34;   {(Sch)}
  hq := 1.054571596E-34; {CODATA98}

  gam := 6.672308E-11 ;{theory W.Droescher(2000)}
  gam := 6.6733082E-11;{Zitat Heim, Aug. 2003}

  gam := 6.6733198E-11;{theory W.Droescher(2002)}
  gam := 6.67390E-11  ;{Messung 2003}
  gam := 6.67259E-11  ;{CODATA mean}
  gam := 6.663E-11    ;{lower limit CODATA}
  gam := 6.673E-11    ;{CODATA98 (+-10)}
  gam := 6.683E-11    ;{upper limit CODATA}
  gam := 6.67407E-11  ;{Künding 2003}
  gam := 6.67422E-11  ;{value June 2001 (+-90)}
  gam := 6.67512E-11  ;{upper limit (2001)}
  gam := 6.67332E-11  ;{lower limit (2001)}
  gam := 6.6732E-11   ;{Sch}
  gam := 6.6733198E-11;{theory W.Droescher(2002)}

/* predicion based on avg mean deviation gamma= 6.67279915 + 0.0000015  e-11*/

  Rg := 376.73037659  ;{Sch}
  Rg := 376.730313461 ;{CODATA 1998}

  {(2-6)}
  fakMeV := 0.05609545E31   ;{Sch}
  fakMeV := 0.056095892E31 ;{CODATA98 [kg] -> [MeV/c**2] }

  /* here are the values B. Heim used in the 1980s:
     m0=1.256637E-6;       {my0 Induction constant}
     e0=8.854188E-12;      {e0 Influenz constant}
     gam=6.672206E-11;     {gamma}
     hq=1.054573E-34;      {Planck}
  */
#endif

#if 1
                    /* C math - use double's */
  pi = M_PI;        /* from        math.h = 3.14159265358979323846 */
  ebn = M_E;        /* from        math.h = 2.7182818284590452354 */
#else
               /* C math - future use - long double */
  pi  = M_PIl; /* long double math.h = 3.1415926535897932384626433832795029L */
  ebn = M_El;  /* long double math.h = 2.7182818284590452353602874713526625L */
#endif

  hq  = 1.054571596e-34;   /* CODATA'98                    */
  gam = 6.6733198e-11;     /* GAMMA  */   /* theory W.Droescher(2002)     */

  rg  = 376.730313461;     /* CODATA 1998                  */
  c   = 299792458.0;       /* Sch                          */
  s0  = 1;                 /* length unit = 1 [m]          */
  fakMeV = 0.056095892e31; /* CODATA'98 [kg] -> [MeV/c**2] */

} /* end GValues() */

void GInit(void)
{
  /* computation of basic constants from gamma, hq, pi and ebn */

  double temp1,zw2,zw3;
  double tmp2 = 0.0;

  /* Computations */
  xi = 0.5 *(1.0 + sqrt(5.0));

  /* (2B,2-1) */
  eta = pi / sqrt(sqrt(4.0 + pi*pi*pi*pi) );

  /* (2A,2-2) */
  theta = 5.0*eta + 2.0*sqrt(eta)+1.0;

  /* (2,2-5) f(const) */
  eq = 3.0 / (4.0*pi*pi)*sqrt(2.0*theta*hq/rg);

  /* computation of alpha and beta (the 1982 DESY code used a hard coded alpha as input) */
  /* (22) */
  /* alfa := 1/137.03602725E0 ;{Sch} */

  alfa = 1.0/137.03599976 ; /* CODATA 1998 */

  /* (2-6) */
  beta = 1.0/1.00001411;

/* --------------------------
  {TESTING for different formulas for Alpha  ( 9.Feb.2006 )}
  {Heim 1982}
  a1 := sqrt(etaqk(1,1))
  a1 := a1*( 1-a1)/(1+a1)
  a2 := sqrt(etaqk(1,2))
  a2 := a2*( 1-a2)/(1+a2)
  alk1 = 1 - a1*a2

  dd(1)=9*theta /(2*pi)^5 *alk1  {1982 Gl.(22a)}

  beta=sqrt(1/2*(1 + sqrt(1 - 4*dd*dd)) )
  alfa=sqrt(1/2*(1 - sqrt(1 - 4*dd*dd)) )
  Writeln[f,'Now using alpha Heim(1982)");
  Writeln[f,'alpha(1982) = ', alpha,'      beta(1982)= ',beta);

  {Heim 1989}
  sqeta := sqrt(eta)
  sqeta := (1 - sqeta)/(1 + sqeta)
  sqeta := sqeta*sqeta
  alk2=1 - (1+etaqk(2,2))/( eta*etaqk(1,1)*etaqk(1,2) ) *sqeta2

  dd(2)=9*theta /(2*pi)^5 *alk2   {1989 GL. V}

  beta=sqrt(1/2*(1 + sqrt(1 - 4*dd*dd)) )
  alfa=sqrt(1/2*(1 - sqrt(1 - 4*dd*dd)) )
  Writeln[f,'Now using alpha Heim(1989)");
  Writeln[f,'alpha(1989) = ', alpha,'      beta(1989)= ',beta);
 *--------------------------------
 */


  /* (3-1) minimum mass unit */
  amu = sqrt(sqrt(pi)) * pow(3.0*pi*s0*gam*hq,(1.0/3.0)) * sqrt(c*hq/(3.0*gam)) / (c*s0) ;

  /* (3-3) geometrical constants */
  temp1 = 1.0 - 2.0/3.0*xi*eta*eta * (1.0 - sqrt(eta));
  alfp  = temp1 / (eta*eta* pow(eta,(1.0/3.0))) - 1.0 ;
  alfm  = temp1 / (eta    * pow(eta,(1.0/3.0))) - 1.0 ;

  /* print constants */
  printf("Data input:\n");
  printf("----------------------\n");
  printf(" Pi                             =%.14e\n", pi  );
  printf(" base of natural logarithm: ebn =%.14e\n", ebn );
  printf(" plancks constant/2Pi:      hq  =%.14e%s\n", hq  ," [Ws*s]");
  printf(" speed of light : c             =%.14e%s\n", c   ," [m/s]" );
  printf(" gravitational constant: gam    =%.14e%s\n", gam ," [m**3/(kg*s*s)");
  printf(" Vacuum wave resistance:   Rg   =%.14e%s\n", rg  ," [Ohm]");
  printf(" Fine structure constant: alfa  =%.14e\n", alfa );
  printf(" \"strong\" constant: beta        =%.14e\n", beta );
  printf("                     1/ alfa    =%.14e\n", 1.0/alfa  );
  printf("                     1/beta     =%.14e\n", 1.0/beta );
  printf(" Conversion kg - MeV : fakMeV   =%.14e%s\n", fakMeV," [MeV/kg]");
  printf(" Length unit:s0                 =%.14e%s\n", s0    ," [m]");
  printf("Derived constants:\n");
  printf("-----------------\n");
  printf(" Geometrical shortening: eta    =%.14e\n",eta);
  printf(" Geometrical shortening: theta  =%.14e\n",theta);
  printf(" Elementary charge: eq          =%.14e%s\n",eq  ," [As]");
  printf(" Mass element amu               =%.14e%s\n",amu ," [kg]");
  printf(" Geometrical shortening: alfp   =%.14e\n",alfp);
  printf(" Geometrical shortening: alfm   =%.14e\n",alfm);
  printf(" Geometrical shortening: xi     =%.14e\n",xi  );
  printf(" \n");

  /* (4-8) Matrix */
  /*values A25, A31, A33, A36 depend strongly from beta
    because using the term 1-beta**2 (OP2006) */

  /* Parameters for computation of w1 (Structure potenz of mesons) */
  tmp2 = ((1.0-sqrt(eta)) / (1.0+sqrt(eta)) );

  a[1][1] = pow(pi*ebn*xi*xi,2.0)* (1.0 - 4.0*pi*alfa*alfa)/(2.0*eta*eta);
  a[1][2] = 2.0*pi*ebn*xi*xi * (theta/8.0 - pi*ebn*eta*alfa*alfa/3.0) / 3.0;
  a[1][3] = 3.0*(4+eta*alfa)*(1.0-eta*eta/5.0*pow( tmp2 , 2.0) );
  a[1][4] = (1.0 + 3.0*eta/(4.0*xi)*(2.0*eta*alfa - ebn*ebn*xi*pow( tmp2 , 2.0) ))/alfa;
  a[1][5] = ebn*ebn*(1.0 - 2.0*ebn*alfa*alfa/eta)/3.0;
  a[1][6] = pi*pi*ebn*ebn * (1.0 + alfa/(5.0*eta)*(1.0 + 6.0*alfa/pi));

  a[2][1] = 2.0*pow((ebn*alfa/(2.0*eta)),2.0) *(1.0 - alfa/(2.0*xi*xi));
  a[2][2] = xi*(1.0-xi*pow((alfa*xi/(eta*eta)),2.0) ) /12.0;
  a[2][3] = (eta*eta + 6.0*xi*alfa*alfa)/ebn;

  /* Parameters for computation of w3 (Structure potenz baryons) */
  a[2][4] = 2.0*xi*xi/(3.0*eta) ;
  a[2][5] = xi*pi*pi*ebn*ebn *(1.0 - beta*beta);
  a[2][6] = 2.0*(1.0 - pi/2.0*pow((ebn*xi*alfa),2.0)*sqrt(eta))/(ebn*xi*xi);

  /* (5-1) */
  zw2 = pi*ebn*alfa;
  zw3 = 1.0 - beta*beta;

  a[3][1] = zw2*zw2*(1.0 - pi*pi*ebn*ebn*zw3);
  a[3][2] = xi*xi*(1.0 + pow((2.0*ebn*alfa/eta),2.0))/6.0;
  a[3][3] = zw2*zw2*xi*xi*(1.0 - 2.0*pi*ebn*xi*ebn*xi*zw3);
  a[3][4] = eta*sqrt(2.0*pi*eta);
  a[3][5] = 3.0*alfa/(ebn*xi*xi);
  a[3][6] = 1.0/(1.0 - pi*ebn*xi*xi*ebn*ebn*zw3);

  /* Parameters for computation of avx (resonance basis) */
  a[4][1] = (xi*(2.0 + xi*xi*alfa*alfa) - 2.0 *beta)/(2.0*beta - alfa);
  a[4][2] = pi*xi*xi*eta*(beta - 3.0*alfa)/2.0;
  a[4][3] = xi/2.0;
  a[4][4] = 2.0*eta*eta/(xi*xi);
  a[4][5] = (3.0*beta - alfa)/(6.0*xi);
  a[4][6] = pi*ebn/(xi*eta) - ebn*eta*eta*alfa/2.0;

  a[5][1] = pow((2.0*alfa + 1),2.0);
  a[5][2] = 6.0*alfa/(eta*eta);
  a[5][3] = pow(xi/eta,3.0);

  /* Parameters for computation of bvx (resonance rise) */
  a[5][4] = alfa*(beta - alfa)*sqrt(1.5);
  a[5][5] = xi*xi*xi;
  a[5][6] = pow(xi/eta,4.0);

  a[6][1] = pi*xi*(2.0*beta - alfa)/(12.0 * beta);
  a[6][2] = pi*pi*(beta - 2.0*alfa)/12.0;
  a[6][3] = sqrt(eta)/9.0;
  a[6][4] = pi/(3.0*eta);
  a[6][5] = pi/(3.0*xi);
  a[6][6] = xi*eta;

  /* print of matrix */
  if (print > 2)
  {
       printf("Parameter matrix:\n");

       for (i=1; i<=6;i++)
       {
         for (j=1; j<=6;j++)
         {
           printf("%.14e  ", a[i][j]);
         }
         printf("\n");
       }
   }
} /* end of GInit() */

/* This routine computes numbers for the ground level N = 0 */
void GBase(void)
{
  double s;
  double zw1,wg1,wg2;

  zw1 = wg1 = wg2 = -1.0; /* INIT for safety */

  printf("=========================================================\n");
  printf("Terms:\n");
  printf("  Cs = Strangeness quantum number\n");
  printf("  kq = |qx| (amount of charges)\n");
  printf("  eps= Particle (1) / Antiparticle (-1)\n");
  printf("  qx = Charge quantum number\n");
  printf("  N  = Resonance\n");
  printf("  am = Mass of particle\n");
  printf("  Remaining values are natural integer constants.\n");
  printf("\n");

  /* values dependent on k only */
  /* (3-6) # f(k) */
  s  = k*k + 1.0;
  q1 = ROUND2( 3.0 * pow(2.0,s - 2.0) );
  q2 = ROUND2( pow(2.0,s) - 1.0 );
  /* q3 = ROUND2( pow(2.0,s) + 2.0*cos(pi*k) ); */ /* pow(-1,k) is not possible in function po */
  q3 = ROUND2( pow(2.0,s) + 2.0*pow(-1.0,k));
  q4 = ROUND2( pow(2.0,s - 1.0) - 1.0 );


  /* values dependent additionaly on kq (charge quantum number) */
  /* (3-5) f(kq,k)  */
  /* Note - k is int */

  alf1 = (1.0 + sqrt(etaqk(kq,k)))/2.0;
  an1  = alf1;            /* N1(q,k) */

  alf2 = 1.0/etaqk(kq,k);
  an2  = 2.0*alf2 / 3.0 ; /* N2(q,k) */

  zw1  = etaqk(kq,k);
  alf3 = exp(k-1.0)/(1.0*k) - kq*(alfa/3.0*(1.0+sqrt(zw1)) * pow(xi/(zw1*zw1),2.0*k+1.0)* zw1*zw1*zw1
         + etaqk(1.0,1.0)/(ebn*zw1)*pow(2.0*xi*zw1,k*1.0) * pow( (1.0-sqrt(zw1)) / (1.0+sqrt(zw1)),2.0) );
  an3  = 2.0*alf3;        /* N3(q,k) - is the same as N3_1982 in Java code by L.
                             N3(2,2) =2.007.. != table -> the value in selected results in wrong?*/

 /* print intermediate results */
  if (print > 1)
  {
    printf("Ground level ---------------------------------------\n");
    printf("   Q1    Q2    Q3    Q4\n");
    printf("%5ld%6ld%6ld%6ld\n", q1,q2,q3,q4);
  }

  if (print > 2)
  {
    printf("Test print GBASE:\n");
    printf(" s    = %.14e\n",s);
    printf(" etaqk= %.14e\n", zw1);
    printf(" alf1 = %.14e    N1 = %.14e\n",alf1,an1);
    printf(" alf2 = %.14e    N2 = %.14e\n",alf2,an2);
    printf(" alf3 = %.14e    N3 = %.14e\n",alf3,an3);
  }

  /* (4-2), (XV) Basic rise */
  gkq =q1*q1*q1*alf1 + q2*q2*alf2 + q3*alf3 + exp((1.0-2.0*k)/3.0);

  /* (4-3) */
  if (k == 1)
  {
    /* Meson:   wvx = w1 + 1  */
    zw1 = etaqk(kq,k);
    wg1 = (1.0-Q)*(a[1][1]-P*(a[1][2]+kappa*kq/zw1*a[1][3])-
                   binom(P,2)*(a[1][4]-kq/zw1*a[1][5]))+kappa*Q*zw1*a[1][6];

    /* deleted **(2-k)=**1 because k=1 (OP2006) */
    wgxk = wg1 + 1.0;
  }
  else
  {
    /* Baryon:  wvx = 1 + w2 */
    zw1 = etaqk(kq,k);
    wg2 = ( (kq-1.0)*a[2][1]+(1.0-P)*a[2][2] +
             binom(P,2)* (a[2][3]-qx*zw1/(1.0+a[2][4]*(1.0+qx))*a[2][5]) +
             kappa*(a[2][6] + kq*zw1*zw1*a[3][1]) +
             binom(Q,3)*zw1*a[3][2] +
             binom(P,3)*(kq*kq*kq*a[3][3]/(3.0-kq)*(qx-cos(pi*kq))+
                         ebn*(P-Q)*pow(eta,(kq-1.0)*kq/4.0)/ (8-a[6][6]*kq*(kq-1.0)) *
                         (1.0-kq/zw1*(2.0-kq)*pow(a[3][4],1.0-qx) *a[3][5])*zw1/(eta*eta)-a[3][6]));
               /* deleted **(k-1)=**1 because k=2 here */
    wgxk= 1.0 + wg2;
  }

  /* (4-2) */
  wgx = gkq*wgxk;

  /* (4-5)} {-alfa**y substituted with cos(pi*y)*alfa**y */
  an = P*a[4][2]*(1.0 - kappa*a[4][3]*(1.0+a[4][4]* cos(pi*(2.0-k))*
                        pow(alfa,2.0-k)* pow(a[4][5],k-1.0)) *
                        (1 - kappa*Q*a[4][6]*(2.0-k))
                      - a[5][1]*(k-1.0)*(1.0-kappa));

  /* (4-6) */
  aq = 1.0 - kq*a[5][2]* (1.0 - 2.0*kappa*pow(a[5][3],k*1.0)) *
           (1.0 + qx/6.0*(3.0-qx)*(k-1.0)*(1.0-kappa));

  /* (4-4) */
  agx = a[4][1]/k *(1.0 + an*aq);

  /* (4-7) */
  bgx = (a[5][4] * pow(a[5][5],k-1.0)*
            (1.0+P*a[5][6]*(1.0-kappa*a[6][1]*pow(a[6][2],1.0-k))*
             (1.0+kq*a[6][3]*(1.0+kappa*a[6][4]))
            )* (1.0-1.0/k*pow(a[6][5]*(kq+k-1.0),2.0-k)*binom(P,2)*(1.0-binom(P,3)))) /
        (pow(k*1.0,P*1.0) * (1.0+P+Q+kappa*pow(eta,2.0-kq))) ; /* denominator for WHOLE expression */

  if (print > 2)
  {
    printf(" gkq  = %.14e\n",gkq);
    printf(" w1   = %.14e    w2   = %.14e\n", wg1,  wg2);
    printf(" wgxk = %.14e    wgx  = %.14e\n", wgxk, wgx);
    printf(" an   = %.14e    aq   = %.14e\n", an,   aq);
    printf(" agx  = %.14e    bgx  = %.14e\n", agx, bgx);
    printf(" \n");
  }
} /* End GBase() */

/* calculates the structure parameters n1, n2, n3, n4 by use of the quantum numbers and N */
void GStruc(void)
{
  /* compute fn= f(N)              */
  /* (5-2) f(kq,k,P,kappa,eps,lq)} */
  fn = (1.0 - Q*(2.0-k)*(1.0-kappa)) * (agx*n/(n+2.0)+bgx*sqrt(n*(n-2.0)));

  /*
   * determination of structure parameters
   * Despite Heim suggested rounding up when K>x.99 I removed this because it
   * produced errors in the case of neutron and N>3 (OP2006)
   * (6-1)
   */

  /* n1,k1 == int ;  alf1, w1 == double */

  /* ORG k1 = trunc(pow(w1/alf1,1.0/3.0)+ 0.0); */  /* round up when k > .99? */
  w1 = wgx * (1.0 + fn);
  k1 = ROUND( pow(w1/alf1, 1.0/3.0) );   /* round up when k > .99? */
  n1 = k1 - q1; 

  if (k1*k1*k1 < 0)
    printf("K1**3 out of range in GStruc! Use type double here!\n");

  if (print >= 3)
    printf("k1^3=%ld   faktor=%.14e\n", k1*k1*k1,  k1*k1*k1*alf1);

  assert(k1*k1*k1 >= 0);

  /* ORG- k2 = trunc(sqrt(w2/alf2) + 0.0);  */  /* round up when k > .99? */
  w2 = w1 - k1*k1*k1*alf1;
  k2 = ROUND(sqrt(w2/alf2));    /* round up when k > .99? */
  n2 = k2 - q2; 

  /* ORG- k3 = trunc(w3/alf3 + 0.0);   */ /* round up when k > .9)*/
  w3 = w2 - k2*k2*alf2;
  k3 = ROUND(w3/alf3 );           /* round up when k > .9) */
  n3 = k3 - q3;

  /* Now 3 cases are possible. The code for this has had an error in the 1982 DESY version
   * so that coumputation of K4 failed in the case w4 > 1 (OP2006)
   */
  w4 = w3 - k3*alf3;

  if (w4 <= 0.0)
    { k4 = ROUND(alf3*k3);   } /* case a, XXXI  -- was trunc() */
  else
  {
    k4 = ROUND( -log(w4)/(2.0*k - 1.0)*(3.0*q4) );  /* C, FORTRAN log(x) = PASCAL ln (x) -- org trunc()*/
    if (w4 > 1.0)
    {
       k3 = k3 - 1;
       n3 = k3 - q3;
       k4 = (k4 + ROUND(alf3*k3)); /* round up when k > .99? -- org == trunc() */
        
       if (print > 1)
           printf("Case c: Corrected value of K3, n3, K4, n4. This resonance is not allowed!\n");
    }
  }

  n4 = k4 - q4;

  /* For neutrinos' it is roughly ... n1= -q1; n2= -q2; n3= -q3; n4=-q4; */
  /* See below */

  /* test print */
  if (print > 2)
  {
    printf("Test print GSTRUC:\n");
    printf(" fn =%.14e\n",fn);
    printf(" W1 =%.14e\n",w1);
    printf(" W2 =%.14e\n",w2);
    printf(" W3 =%.14e\n",w3);
    printf(" W4 =%.14e\n",w4);
    printf(" \n");
  }

  if (print > 1)
  {
    printf("----------------------------------------------------\n");
    printf("   K1    K2    K3    K4    n1    n2    n3    n4\n");
    printf("%5ld%6ld%6ld%6ld%6ld%6ld%6ld%6ld\n",
           k1,k2,k3,k4, n1,n2,n3,n4);
    printf(" \n");
   }

} /* end fo GStruc() */



/* computation of masses from quantum numbers and N */
void GMass(void)
{
  double fik = 0.0, zw1 = 0.0;

  /* The mass equation is (XII,1982),       M = amu*  alfp* (K + G + H + fig)
   * The modified version of (B3,1989) is , M = amu* (alfp *(K + G + F + Phi) + 4*q*alfm)
   * Note: We put the () for the 1989 version such that it is identical result to 1982. Different from paper.
   *
   * The DESY term "kgh" represents terms K + G + h from the 1982 script (XI)
   * Ni are substituted here with alphai (IX), Ki = ni + Qi
   * The composed term kgh has less elements and therefore computation is more accurate
   */

  /* (3-9) f(k) */
  kgh = 4.0*( alf1*k1*k1*(1.0+k1)*(1.0+k1)*0.25 +
              alf2*k2*(2.0*k2*k2 + 3.0*k2 + 1.0) / 6.0 +
              alf3*k3*(1.0+k3)*0.5 + k4);

  /* (3-7) f(k,kq,P,Q,kappa) */
  zw1 = etaqk(kq,k);

  fig = 3.0*P/(pi*sqrt(zw1))*(1.0-alfm/alfp)*(P+Q)*cos(pi*(P+Q) )*(1.0-alfa/3.0+pi/2.0*(k-1.0)*pow(3.0,1.0-kq/2.0))*
  (1.0 + 2.0*k*kappa/(3.0*eta*eta)*xi*(1.0+xi*xi*(P-Q)*(pi*pi - kq))) / (1.0 + 4.0*xi/k*1.0*binom(P,2)*pow(xi/6.0,kq))*
  (2.0*sqrt(etaqk(1,1)*zw1) + kq*eta*eta*(k-1.0))*(1.0+(4.0*pi*alfa)/(eta*sqrt(eta)))*(1.0+Q*(1.0-kappa)*(2.0-k)*n1/q1)+
  4.0*(1.0-alfm/alfp)*alfa/(xi*xi)*(P+Q)+4.0*kq*alfm/alfp ;

  /* Field mass for a particle with empty protosimplex - just mass of "field". */
  /* This corresponds for some particle descriptions with neutrino mass.     */
  /* PS: "fik" means "fi klein" in German which means "the small phi", see 1989 document. I suppose "fig"
          means therefore "the large phi" */ 
          
  fik = (fig - 4.0 * kq * alfm/alfp); 

  if ( print > 2)
  {
    printf("Test print GMASS:\n");
    printf("%20s  %20s %20s\n",        "kgh","fig","fik");
    printf("%20.14e  %20.14e  %20.14e\n", kgh ,fig, fik);
    printf("\n");
  }

  /* (3-9)  Mass = f */
  am       = amu * fakMeV * alfp * (kgh + fig);
  am_field = amu * fakMeV * alfp * fik;
  
} /* end of GMass() */

/* search for resonance limits */
void GLimit(void)
{
  double a1,a2,a3,qa,ra,da,sa,ta,temp1,ft;
  long   ls,ltmp;    /* integer in Pascal is limited to 32.000 */
  int    temp2;      /* 0 when electrons/1 else */

  lme=0;

  if ((Q*(2-k)*(1-kappa)) == 1)
   return;  /* EARLY out - skip search when calculating e- (Electrons) */

  /* (XXXIII) substituted with M0 and G=k+1 - PASCAL used trunc() */
  l1 = ROUND( pow( (pow(2.0*(P+1.0),2.0-k)* (k+1.0) ) / (4.0*alf1)* (kgh+fig), 1.0/3.0) - q1); /* round up here when >.99? OP2006 */

  /* now bringing (XXXIV) into normalized form x**3 + a1x**2 + a2*x +a3 = 0 with x=(L2 + Q2) */
  a1 = 1.5;
  a2 = 0.5;
  a3 = -3.0 * alf1/alf2*pow(l1+q1*1.0, 3.0);

  /* Cardan solution of the reduced equation with substitutions q and r */
  qa = (3.0*a2 - a1*a1)/9.0;
  ra = (9.0*a1*a2 - 27.0*a3 - 2.0*a1*a1*a1)/54.0;

  /* discriminant */
  da = sqrt(qa*qa*qa + ra*ra);

  /* solution */
  sa = pow(ra+da*1.0, 1.0/3.0);
  ta = pow(ra-da*1.0, 1.0/3.0);
  l2 = ROUND(sa + ta - a1/3.0 - q2);  /* round up here when >.99? OP2006 - ORG trunc()*/

  /* (XXXIV-2), (XXXIV-3) */
  l3 = ROUND( sqrt(2.0*alf2/alf3*(l2+q2)*(l2+q2) + 0.25)- 0.5 - q3 );  /* round up here when >.99? OP2006 */
  l4 = ROUND( alf3*(l3+q3) - q4 );                                     /* round up here when >.99? OP2006 */

  /* (XXXV)
   * determine maximum n=lme in lme= 1 .. loop
   * determine f(L)=temp1
   */
  temp1 = (alf1*pow(l1+q1*1.0, 3.0) + alf2*(l2+q2)*(l2+q2) + alf3*(l3+q3)
           + exp( ((1.0-2.0*k)*(l4+q4)) / (3.0*q4))) /wgx - 1.0;

  temp2 = 1.0 - Q*(2.0-k)*(1.0-kappa);   /* case selector, =0 if electron selected, =1 else,
                                            left part of f(N) (XXV)  */

  /* ls from 3..40000 or something like that */
  ft = 0.0; /* INIT for safety */
  for (ls= 3; ls <= loop; ls++)
  {
    /* if print>2 then writeln(ls); test */
    ltmp = ls  - 1;

    if (ltmp == 1)
    { /* skip over n=1 otherwise Fn becomes imaginary */ }
    else
    {
      /* ltmp > 1 */
      if (ls == (loop-1))
         printf("loop = %d *** No excitation within these iterations! Setting Le = loop.\n", loop);

      ft = temp2 *( agx*ltmp/(1.0*ltmp+2.0) + bgx*sqrt(ltmp*(ltmp-2.0)) ); /* XXV */

      if (ft <= temp1)
        { /* go on searching */ }
      else
        { lme = ltmp-1; ls=loop; }  /* exit when ft(ltemp) < temp1(L1,L2,L3,L4), Le=preceding value */
    }
   } /* end of search loop for le */

   /* print maximum parameters */
   printf("Resonance limit for element x=%d:\n",x);
   printf("   L1    L2    L3    L4    Le\n");
   printf("%5ld%6ld%6ld%6ld%6ld\n",l1,l2,l3,l4,lme);
   printf("----------------------------------------------------\n");

   if (print > 2)
   {
     printf("Test print GLIMIT:\n");
     printf("a1   = %18.10e a2   = %18.10e a3 = %18.10e\n", a1,a2,a3);
     printf("qa   = %18.10e ra   = %18.10e da = %18.10e\n", qa,ra,da);
     printf("sa   = %18.10e ta   = %18.10e\n", sa, ta);
     printf("temp1= %18.10e temp2= %d  ft = %18.10e\n",temp1, temp2,ft);
     printf("\n");
   }

} /* end of GLimit() */

/* ==== Main program ================================================ */

int main(int argc, char *argv[])
{

 /* define output destination - just use stdout for 'f' */

 printf(" *****************************************************************\n");
 printf(" * Mass formula of elementary particles by B.Heim                *\n");
 printf(" * Program : H.D. Schulz, 26/07/82  DESY                         *\n");
 printf(" * C version 0.66, based on PASCAL from Olaf Posdzech, March2006 *\n");
 printf(" *****************************************************************\n");
 printf(" \n");

 GValues();            /* setting values of natural constants used */
 parseArgs(argc,argv); /* Can specify nmax, print, max loop, gamma/g, and rg on cmd line - override if existing. */
 initParticleList();

 /* setting controls */

 fi = fopen("gprogin.dat","rt");
 assert(fi != NULL);

#if 1
 for( i=1; i<= 5; i++)
   fgets(t1,100,fi); /* skip first 5 lines here */

#else
/*
{read additional inputs from file if needed}
 readln(fi,t1,print);
 readln(fi,t1,nend);
 readln(fi,t1,loop);
 readln(fi,t1,ant);
 readln(fi,t1);
 readln(fi,t1,ja,je);
*/
#endif

 printf(" Used loop limits : \n");
 printf(" ================== \n");
 printf("  nend, maximum excitation level = %ld\n", nend);
 printf("  loop, resonance search         = %d\n", loop);
 printf("  ant,  particle/antiparticle    = %d\n", ant );
 printf(" \n");

 GInit();   /* computation of basic constants from gamma, hq, pi and ebn */

 printf("Data sets named: %d%s%d\n", ja , " to ", je);

 if (ja > 1)
 {
   int i;

   for(i=1; i <= (5*(ja-1)); i++)
     fgets(t1,100,fi); /* read line from input file */
 }

 /* Main loop */
 assert(je >= ja);
 for (j=ja; j <= je; j++) /* compute data sets no.  ja .. je */
 {

   /* read set of quantum numbers of multiplet */

   fgets(t1,100,fi);
    if (feof(fi)) break; /* Don't read/continue beyond EOF */

   /* Make sure we read the correct line, starting with "'---" */
   assert((t1[1]=='-') && (t1[2]=='-') && (t1[3]=='-'));

   strcpy(particlename,t1);

   printf("========================================================\n");
   printf("Starting computation of multiplet #%d%s\n",j,":");
   printf("%s",t1);

#define OFFSET 23

   fgets(t1,100,fi); assert(strlen(t1) > OFFSET); k =atoi(t1+OFFSET);
   fgets(t1,100,fi); assert(strlen(t1) > OFFSET); P =atoi(t1+OFFSET);
   fgets(t1,100,fi); assert(strlen(t1) > OFFSET); Q =atoi(t1+OFFSET);
   fgets(t1,100,fi); assert(strlen(t1) > OFFSET); kappa =atoi(t1+OFFSET);

   printf("k = Baryon number + 1 = %d\n",k);
   printf("P = 2* Isospin        = %d\n",P);
   printf("Q = 2* Spin           = %d\n",Q);
   printf("kappa = Doublett      = %d\n",kappa);

   for (epsi= 1; epsi <= ant; epsi++) /* define eps=particle/antiparticle, 2nd loop is for the antiparticle */
   {
     eps = 1 - (epsi-1)*2 ; /* +1/-1 */

     /* computation of strangeness */
     epsp = ROUND2( eps* cos( pi * Q * (kappa + binom(P,2)) ));
     epsq = ROUND2( eps* cos( pi * Q * (Q * (k-1) + binom(P,2)) ));
     cs   = ROUND2( 2.0/(k*(1.0+kappa))  * (P * epsp + Q*epsq) * (k-1.0+kappa));

     /* define isomultiplett component */
     xe = P + 1; /* number of elements in multiplett */

     for (x = 1; x <= xe; x++)
     {
       printf("\n");
       printf("=========================================================\n");
       printf("Now calculating element of multiplet %d%s%d\n",j,", x = ",x);

       /* F(k,pg,qg,kappa,eps) */
       qx= ROUND2( ((P+2.0-2.0*x)*(1.0-kappa*Q*(2.0-k))+cs+eps*(k-1.0-(1+kappa)*Q*(2-k)))/2.0 );

       /* compute charge kq */
       kq = abs(qx);

       /* test print */
       if (print > 2)
       {
         printf("Test print MAIN:\n");
         printf("=========================================================\n");
         printf("  eps  epsp  epsq    cs    kq     x    qx\n");
         printf("%5d%6d%6d%6d%6d%6d%6d\n", eps,epsp,epsq,cs,kq,x,qx);
       }

       GBase();      /* compute numbers for the ground level N = 0 */

       /* The original DESY code has had a loop here calculating masses for n=0 to maximum n
        * while skipping n=1. This has been cut off here for more clearity. */

       /* calculating mass for N = 0 */
       /*  printf("N = ',n);  */
       n=0;

       GStruc();
       GMass();

       addParticle(k,P,Q,kappa,x,qx,cs, am, 0, 1);       /* Add computed particle - ground-state */

       /* Add "particle" based on mass of field == neutrino. 
        * The constraints according to Heim for "possible" neutrino's
        * are "derived from lepton" (k==1) and (P+Q) is even. See PhysOrg
        * discussion and books. 
        */
       if ((k == 1) && (((P+Q)%2) == 0) ) 
         addParticle(k,P,Q,kappa,x,qx,cs, am_field, 1, 1); /* Add particle based on mass of field == neutrino */

       /* print output */
       printf("   Cs    kq   eps    qx     N    am [MeV]  particleName\n");
       printf("#%4d%6d%6d%6d%6d    %.14e x=%d  %s\n", cs,kq,eps,qx,n,am,x,particlename); 
       printf("----------------------------------------------------\n");

       /* search  for maximum excitation level n=le */
       GLimit();    /* This has been put into a procedure here OP2006 */

       /* skip over N = 1 otherwise Fn becomes imaginary, nend=1 used here as nend:=lme */

       if (nmax == 1)
       { nend = lme; }
       else
       {
         if (nmax > lme)
           { nend = lme; }
         else
           { nend = nmax; }
       }

       if (print == 3)
         printf("x=%d  nend=%ld\n", x, nend);

       /* calculate masses for N = 2 to nend */
       for (n = 2; n <= nend; n++)
       {
         /* printf("N = %d\n",n);   */
         GStruc();
         GMass();

         addParticle(k,P,Q,kappa,x,qx,cs, am, 0, n);       /* Add computed particle - excitated state */
         
         /* Add particle based on mass of field == neutrino. 
          * The constraints according to Heim for "possible" neutrino's
          * are "derived from lepton" (k==1) and (P+Q) is even. See PhysOrg
          * discussion and Heim books. 
          * However, this excludes the neutrino1 from being stored, although
          * that was explicit in gprogin.dat. 
          */
         if ((k == 1) && (((P+Q)%2) == 0) ) 
           addParticle(k,P,Q,kappa,x,qx,cs, am_field, 1, n); 

         /* print output */
         if (print >= 1)
         {
           /*printf("  Cs    kq   eps    qx     N    am [MeV]\n"); */
           printf("%5d%6d%6d%6d%6d    %.14e\n", cs,kq,eps,qx,n,am );
         }
       } /* end n*/

     } /* loop element x of multiplett */
   } /* loop particle/antiparticle */
  } /* loop multiplett j */

  printf("***************************************************\n");

  /* Post evaluation:
   * Compare all computed masses with given masses and
   * print differences.
   */
  evaluate();

  /* Finish up */
  fclose(fi);     /* input file */

  return 0;

} /* end main */
