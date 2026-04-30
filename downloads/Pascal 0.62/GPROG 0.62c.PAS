PROGRAM GPROG {$N+};
{*
Transscription of program GPROG dated 17/03/1982 by H.D.Schulz, DESY
Formulas given by Burkhard Heim 17/09/1978
Transscription 17/06/2001 by A. Mueller for MS-Fortran
Transscription 12/03/2006 by Olaf Posdzech for Turbo-Pascal, Free Pascal
   v0.62c: Overflows when computing very large N > 180! See readme.txt for details.

program reads as input from file 'gprogin.dat'
        Name of particle
        baryon number +1   = K
        2*isospin          = PG
        2*spin             = QG
        dublett factor     = KAPPA

 The original program consistently used REAL*16 in an IBM environment.
 	3.1415926535Q0   replaced by 3.14159265358979D0
	x**0.25Q0       replaced by Dsqrt(Dsqrt(x))
 function IBINOM(in,ik) rewritten
 Fortran function IDINT overloaded for possible roundup, c.f. module ROUND
 Default compiler settings should result in a 52 bit  FP precision

Pascal (OP2006):  When calculating terms like b(:extended)= b + a*a*a Pascal uses
for the intermediate product a*a*a the same type as for a. Using a:int the
product runs out of range then.
              Integer        Longint
max value       32768     2147483647
->max value K1     32           1290
->max value K2    181          46340

 Schriftlicher Hinweis von H. D. Schulz :
   Es liegt noch ein Programmfehler fuer die Strangeness S vor, der sich
   nur bei dem baryonischen Theta-Doublett bemerkbar macht , dieses ist
   im printout mit xi bezeichnet .
*}

const
  print=2;  {set amount of outputs: 1=masses only, 2=basic, 3=intermediate results}
  dest =2;  {output: 1=screen, 2=file'gprogout.lis'}
  ant  =1;  {1=process particles only, 2=process also antiparticles}
  nmax:longint =10;  {maximum resonance to be processed, 0=ground level only,
                     1= till maximum lme, others=up to this level}
  loop=40000; {end of search loop for maximum excitation level}
              {originally  hardcoded : nend = 112 , loop = 50000}
  ja = 1;    {first multiplett to be calculated}
  je = 15;   {je<=15 last multiplet to be calculated}

type
   z1=1..6;
   mat1=array[z1, z1] of extended;

var
  f,fi:text;    {input and output files}
  t1:string[24];{section '... ' in grpogin.dat}
  t2:char;
  a:mat1;      {Matrix A[rs] (GXXIV)}

  {constants}
  alfa,alfm,alfp,amu,beta,c,ebn,eq,eta,fakMeV,gam,hq,
  pi,rg,s0,theta,xi: extended;                {when using real gam*hq=0 (out of range)}
  {quantum numbers}
  eps,k,P,Q,kappa,x,cs,qx,kq,n,xe,epsp,epsq:integer;

  {particle properties}
  q1,q2,q3,q4,n1,n2,n3,n4,k1,k2,k3,k4,l1,l2,l3,l4:longint; {amounts of protosimplexes in zones}
  {when calculating terms like b(:extended)= b + a*a*a pascal uses the same type as a
  for the intermidiate product a*a*a. Using a:int the product runs out of range then.}
  alf1,alf2,alf3,an1,an2,an3,
  gkq,wgxk,wgx,an,aq,agx,bgx,
  w1,w2,w3,w4,fn,kgh,fig,am: extended;
  lme,nend:longint;                  {maximum excitation level}
  i,j,epsi,ni:integer;               {counter in loops}
  y:char;                            {keystroke if needed}
  msg:string;

{Functions missing in Pascal ===============================================}
{Power = b**p }
{This dunction does not work with b<0! Replaced such terms in the following 
with the combination cos(pi*p)*po(-b,p)  (OP2006)}
{In many Heim terms full integer accuracy is needed. Better use b*b*b then po(b,3)}
FUNCTION po(b,p:extended):extended;     {when using real ga*hq=out of range}
   BEGIN if b=0 then po:=0 else po:=exp(p*ln(b)) END;

{binomial coefficients}
Function binom(n,k:integer):integer;
var bi,d2,den:longint;
begin
 bi:=1;
 d2:=1;
 den:=1;
 if n<k then binom:=0                  {not existent}
  else
  if (k=n) or (k=0) then binom:=1      {borders}
   else
   BEGIN {now k<n}
    for i:=1 to n do bi:=bi*i;         {fakul(n)  }
    for i:=1 to k do d2:=d2*i;         {fakul(k)  }
    for i:=1 to (n-k) do den:=den*i;   {fakul(n-k)}
    binom:=bi div (den*d2)             {binom:= fakul(n)/(fakul(k)*fakul(n-k))}
   END;
END;


{Functions needed for calculation =============================================== }

{formel (7a), (V)}
FUNCTION etaqk(kq,k:extended):extended;
   BEGIN
    etaqk:=pi / po( kq*kq*kq*kq *(4+k) + pi*pi*pi*pi,1/4)
   END;

(*{Original FORTRAN procedure used to truncate numbers}
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
C	IDint = IDNint(X)   ! das ergibt Fehler wegen w4 < 0 in Gstruc.for
	Z = X
C	if(int(Z) .ne. IDint) write(6,1) '### IDint of : X,Y = ',X,Y
1	 format( 1x,a,D24.15,1pe15.7)
C     Protokolliert , wenn abs(Rest) > 0.5 verworfen wird :
C      if( abs(float(IDint))+0.5 .LT. abs(X) )
C	+  write(6,1) '### truncated: X, float(IDint) = ', X,float(IDint)
	return
	end	 function Idint
	End Module ROUND
*)

{Procedures used by main program==================================================}

{Defining values of constants used}
PROCEDURE GVALUES;
BEGIN
{if more values are given the last one is active}
{(Sch) = Schulz 1982 (original code)}

  pi := 3.14159265358979E0;
  pi := 3.1415926535E0;   {(Sch)}
  pi := 4*arctan(1);
  ebn := exp(1);

  hq := 1.0545887E-34;	 {(Sch)}
  hq := 1.054571596E-34; {CODATA'98}

  gam := 6.672308E-11 ;{theory W.Droescher(2000)}
  gam := 6.6733082E-11;{Zitat Heim, Aug. 2003}

  gam := 6.6733198E-11;{theory W.Droescher(2002)}
  gam := 6.67390E-11  ;{Messung 2003}
  gam := 6.67259E-11  ;{CODATA mean}
  gam := 6.663E-11    ;{lower limit CODATA}
  gam := 6.673E-11    ;{CODATA'98 (+-10)}
  gam := 6.683E-11    ;{upper limit CODATA}
  gam := 6.67407E-11  ;{Künding 2003}
  gam := 6.67422E-11  ;{value June 2001 (+-90)}
  gam := 6.67512E-11  ;{upper limit (2001)}
  gam := 6.67332E-11  ;{lower limit (2001)}
  gam := 6.6732E-11   ;{Sch}
  gam := 6.6733198E-11;{theory W.Droescher(2002)}



  Rg := 376.73037659  ;{Sch}
  Rg := 376.730313461 ;{CODATA 1998}

  c := 2.99792458E8   ;{Sch}

  s0 := 1             ;{length unit = 1 [m]}

  {(2-6)}
  fakMeV := 0.05609545E31   ;{Sch}
  fakMeV := 0.056095892E31 ;{CODATA'98 [kg] -> [MeV/c**2] }


(* here are the values B. Heim used in the 1980s:
   m0=1.256637E-6;       {my0 Induction constant}
   e0=8.854188E-12;      {e0 Influenz constant}
   gam=6.672206E-11;     {gamma}
   hq=1.054573E-34;      {Planck}
*)
END;


PROCEDURE GINIT;
{computation of basic constants from gamma, hq, pi and ebn}
 VAR
  temp1,zw2,zw3:extended;
 BEGIN
  {Computations}
  xi := 0.5 *(1 + sqrt(5)) ;

  {(2B,2-1)}
  eta := pi/ sqrt(sqrt(4 + pi*pi*pi*pi) );

  {(2A,2-2)}
  theta := 5*eta + 2*sqrt(eta)+1;

  {(2,2-5) f(const)}
  eq := 3/(4*pi*pi)*sqrt(2*theta*hq/Rg);

{computation of alpha and beta (the 1982 DESY code used a hard coded alpha as input)}
{(22)}

  alfa := 1/137.03602725E0 ;{Sch}
  alfa := 1/137.03599976E0 ;{CODATA 1998}

{(2-6)}
  beta := 1/1.00001411E0;

(*
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
  Writeln[f,'Now using alpha Heim(1982)');
  Writeln[f,'alpha(1982) = ', alpha,'      beta(1982)= ',beta);

  {Heim 1989}
  sqeta := sqrt(eta)
  sqeta := (1 - sqeta)/(1 + sqeta)
  sqeta := sqeta*sqeta
  alk2=1 - (1+etaqk(2,2))/( eta*etaqk(1,1)*etaqk(1,2) ) *sqeta2

  dd(2)=9*theta /(2*pi)^5 *alk2   {1989 GL. V}

  beta=sqrt(1/2*(1 + sqrt(1 - 4*dd*dd)) )
  alfa=sqrt(1/2*(1 - sqrt(1 - 4*dd*dd)) )
  Writeln[f,'Now using alpha Heim(1989)');
  Writeln[f,'alpha(1989) = ', alpha,'      beta(1989)= ',beta);
*)


{(3-1) minimum mass unit}
  amu:=sqrt(sqrt(pi)) * po(3*pi*s0*gam*hq,1/3) * sqrt(c*hq/(3*gam)) / (c*s0) ;

{(3-3) geometrical constants}
  temp1:= 1 - 2/3*xi*eta*eta * (1 - sqrt(eta));
  alfp := temp1/(eta*eta* po(eta,1/3)) - 1  ;
  alfm := temp1/( eta * po(eta,1/3)) - 1    ;

{print constants}
  writeln(f,'Data input:');
  writeln(f,'----------------------');
  writeln(f,' Pi                             =',pi  );
  writeln(f,' base of natural logarithm: ebn =',ebn );
  writeln(f,' plancks constant/2Pi:      hq  =',hq  ,' [Ws*s]');
  writeln(f,' speed of light : c             =',c   ,' [m/s]' );
  writeln(f,' gravitational constant: gam    =',gam ,' [m**3/(kg*s*s)');
  writeln(f,' Vacuum wave resistance:   Rg   =',rg  ,' [Ohm]');
  writeln(f,' Fine structure constant: alfa  =',alfa );
  writeln(f,' "strong" constant: beta        =',beta );
  writeln(f,'                     1/ alfa    =',1/alfa );
  writeln(f,'                     1/beta     =',1/beta );
  writeln(f,' Conversion kg - MeV : fakMeV   =',fakMeV,' [MeV/kg]');
  writeln(f,' Length unit:s0                 =',s0  ,' [m]');
  writeln(f,'Derived constants:');
  writeln(f,'-----------------');
  writeln(f,' Geometrical shortening: eta    =',eta);
  writeln(f,' Geometrical shortening: theta  =',theta);
  writeln(f,' Elementary charge: eq          =',eq  ,' [As]');
  writeln(f,' Mass element amu               =',amu ,' [kg]');
  writeln(f,' Geometrical shortening: alfp   =',alfp);
  writeln(f,' Geometrical shortening: alfm   =',alfm);
  writeln(f,' Geometrical shortening: xi     =',xi  );
  writeln(f,' ');

{(4-8) Matrix}
{values A25, A31, A33, A36 depend strongly from beta because using the term 1-beta**2 (OP2006)}

{Parameters for computation of w1 (Structure potenz of mesons)}
a[1,1]:=po(pi*ebn*xi*xi,2)*(1-4*pi*alfa*alfa)/(2*eta*eta);
a[1,2]:=2*pi*ebn*xi*xi * (theta/8 - pi*ebn*eta*alfa*alfa/3) / 3;
a[1,3]:=3*(4+eta*alfa)*(1-eta*eta/5*po( ((1-sqrt(eta)) / (1+sqrt(eta)) ),2) );
a[1,4]:=(1 + 3*eta/(4*xi)*(2*eta*alfa - ebn*ebn*xi*po( (1-sqrt(eta))/(1+sqrt(eta)),2) ))/alfa;
a[1,5]:=ebn*ebn*(1 - 2*ebn*alfa*alfa/eta)/3;
a[1,6]:=pi*pi*ebn*ebn * (1 + alfa/(5*eta)*(1 + 6*alfa/pi));

a[2,1]:=2*po((ebn*alfa/(2*eta)),2) *(1 - alfa/(2*xi*xi));
a[2,2]:=xi*(1-xi*po((alfa*xi/(eta*eta)),2) ) /12;
a[2,3]:=(eta*eta + 6*xi*alfa*alfa)/ebn;

{Parameters for computation of w3 (Structure potenz baryons)}
a[2,4]:=2*xi*xi/(3*eta) ;
a[2,5]:=xi*pi*pi*ebn*ebn *(1 - beta*beta);
a[2,6]:=2*(1 - pi/2*po((ebn*xi*alfa),2)*sqrt(eta))/(ebn*xi*xi);

{(5-1)}
zw2:=pi*ebn*alfa;
zw3:=1-beta*beta;
a[3,1]:=zw2*zw2*(1 - pi*pi*ebn*ebn*zw3);
a[3,2]:=xi*xi*(1 + po((2*ebn*alfa/eta),2))/6;
a[3,3]:=zw2*zw2*xi*xi*(1 - 2*pi*ebn*xi*ebn*xi*zw3);
a[3,4]:=eta*sqrt(2*pi*eta);
a[3,5]:=3*alfa/(ebn*xi*xi);
a[3,6]:=1/(1 - pi*ebn*xi*xi*ebn*ebn*zw3);

{Parameters for computation of avx (resonance basis)}
a[4,1]:=(xi*(2+xi*xi*alfa*alfa) - 2*beta)/(2*beta - alfa);
a[4,2]:=pi*xi*xi*eta*(beta-3*alfa)/2;
a[4,3]:=xi/2;
a[4,4]:=2*eta*eta/(xi*xi);
a[4,5]:=(3*beta - alfa)/(6*xi);
a[4,6]:=pi*ebn/(xi*eta) - ebn*eta*eta*alfa/2;

a[5,1]:=po((2*alfa + 1),2);
a[5,2]:=6*alfa/(eta*eta);
a[5,3]:=po(xi/eta,3);

{Parameters for computation of bvx (resonance rise)}
a[5,4]:=alfa*(beta - alfa)*sqrt(1.5);
a[5,5]:=xi*xi*xi;
a[5,6]:=po(xi/eta,4);

a[6,1]:=pi*xi*(2*beta - alfa)/(12*beta);
a[6,2]:=pi*pi*(beta - 2*alfa)/12;
a[6,3]:=sqrt(eta)/9;
a[6,4]:=pi/(3*eta);
a[6,5]:=pi/(3*xi);
a[6,6]:=xi*eta;

{print of matrix}
  if print>1 then
   BEGIN
       writeln(f,'Parameter matrix:');
       for i:=1 to 6 do for j:=1 to 6 do
       BEGIN
        write(f,a[i,j]);
        if 0=j mod 6 then BEGIN writeln(f,' '); writeln(f,' ') END
         else write(' ':3)
       END;
   END;
 END;


PROCEDURE GBASE; {This routine computes numbers for the ground level N = 0}
 VAR
  s:integer;
  zw1,wg1,wg2:extended;
 BEGIN
  writeln(f,'=========================================================');
  writeln(f,'Terms:');
  writeln(f,'  Cs = Strangness quantum number');
  writeln(f,'  kq = |qx| (amount of charges)');
  writeln(f,'  eps= Particle (1) / Antiparticle (-1)');
  writeln(f,'  qx = Charge quantum number');
  writeln(f,'  N  = Resonance');
  writeln(f,'  am = Mass of particle');
  writeln(f,'  Remaining values are natural integer constants.');
  writeln(f,'');

{values dependent on k only}
{(3-6) # f(k) }
  s  := k*k + 1;
  q1 := round( 3 * po(2,s-2) );
  q2 := round( po(2,s) - 1 );
  q3 := round( po(2,s) + 2*cos(pi*k) );  {po(-1,k) is not possible in function po}
  q4 := round( po(2,s-1) - 1 );


{values dependent additionaly on kq (charge quantum number)}
{(3-5) f(kq,k)	}
  alf1 := (1 + sqrt(etaqk(kq,k)))/2;
  an1  := alf1;
  alf2 := 1/etaqk(kq,k);
  an2  := 2*alf2 / 3   ;

  zw1  := etaqk(kq,k);
  alf3 := exp(k-1)/k - kq*(alfa/3*(1+sqrt(zw1)) * po(xi/(zw1*zw1),2*k+1)* zw1*zw1*zw1
         + etaqk(1,1)/(ebn*zw1)*po(2*xi*zw1,k) * po( (1-sqrt(zw1)) / (1+sqrt(zw1)),2) );
  an3  := 2*alf3;

{print intermediate results}
  if print > 1 then
  BEGIN
   writeln(f,'Ground level ---------------------------------------');
   writeln(f,'  Q1   Q2   Q3   Q4');
   writeln(f,q1:4,' ',q2:4 ,' ', q3:4,' ',q4:4);
  END;

  if print>2 then
   BEGIN
    writeln(f,'Test print GBASE:');
    writeln(f,' s = ',s);
    writeln(f,' etaqk= ',zw1);
    writeln(f,' alf1 = ', alf1,'    N1 = ',an1);
    writeln(f,' alf2 = ', alf2,'    N2 = ',an2);
    writeln(f,' alf3 = ', alf3,'    N3 = ',an3);
   END;

{(4-2), (XV) Basic rise}
  gkq:=q1*q1*q1*alf1 + q2*q2*alf2 + q3*alf3 + exp((1-2*k)/3);

{(4-3)}
  if k=1 then
  BEGIN {Meson:   wvx = w1 + 1 }
   zw1 :=etaqk(kq,k);
   wg1 :=(1-Q)*(a[1,1]-P*(a[1,2]+kappa*kq/zw1*a[1,3])-binom(P,2)*(a[1,4]-kq/zw1*a[1,5]))+kappa*Q*zw1*a[1,6];
   {deleted **(2-k)=**1 because k=1 here (OP2006)}
   wgxk:= wg1 + 1
  END
   else BEGIN  {Baryon:  wvx = 1 + w2}
     zw1:=etaqk(kq,k);
     wg2:=((kq-1)*a[2,1]+(1-P)*a[2,2]+binom(P,2)*(a[2,3]-qx*zw1/(1+a[2,4]*(1+qx))*a[2,5]) + kappa*(a[2,6]+kq*zw1*zw1*a[3,1]) +
     binom(Q,3)*zw1*a[3,2] + binom(P,3)*(kq*kq*kq*a[3,3]/(3-kq)*(qx-cos(pi*kq))+ ebn*(P-Q)*po(eta,(kq-1)*kq/4)/(8-
     a[6,6]*kq*(kq-1))*(1-kq/zw1*(2-kq)*po(a[3,4],1-qx)*a[3,5])*zw1/(eta*eta)-a[3,6]));  {deleted **(k-1)=**1 because k=2 here}
     wgxk:= 1 + wg2
     END;

{(4-2) }
  wgx:= gkq*wgxk;
{(4-5)} {-alfa**y substituted with cos(pi*y)*alfa**y}
  an:=P*a[4,2]*(1-kappa*a[4,3]*(1+a[4,4]* cos(pi*(2-k))*po(alfa,2-k)* po(a[4,5],k-1))
    * (1 - kappa*Q*a[4,6]*(2-k)) - a[5,1]*(k-1)*(1-kappa));

{(4-6)}
  aq:=1-kq*a[5,2]*(1-2*kappa*po(a[5,3],k))* (1+qx/6*(3-qx)*(k-1)*(1-kappa)) ;

{(4-4)}
  agx:= a[4,1]/k*(1 + an*aq);

{(4-7)}
  bgx:=(a[5,4]*po(a[5,5],k-1)*(1+P*a[5,6]*(1-kappa*a[6,1]*po(a[6,2],1-k))*(1+kq*a[6,3]*(1+kappa*a[6,4])))*
       (1-1/k*po(a[6,5]*(kq+k-1),2-k)*binom(P,2)*(1-binom(P,3))))/(po(k,P)*(1+P+Q+kappa*po(eta,2-kq))) ;

  if print>2 then
   BEGIN
    writeln(f,' gkq  = ',gkq);
    writeln(f,' w1   = ',wg1, '    w2 = ',wg2);
    writeln(f,' wgxk = ',wgxk,'  wgx  = ',wgx);
    writeln(f,' an   = ',an  ,'   aq  = ',aq);
    writeln(f,' agx  = ',agx, '   bgx = ',bgx);
    writeln(f,' ');
   END
  END;


PROCEDURE GSTRUC;
{ calculates the structure parameters n1, n2, n3, n4 by use of the quantum numbers and N }
 BEGIN
  msg:='';              {empty}
{compute fn= f(N)}
{(5-2) f(kq,k,P,kappa,eps,lq)}
  fn := (1-Q*(2-k)*(1-kappa))*(agx*n/(n+2)+bgx*sqrt(n*(n-2)));

{determination of structure parameters}
{Despite Heim suggested rounding up when K>x.99 I removed this because it
produced errors in the case of neutron and N>3 (OP2006)}
{(6-1)}
  w1 := wgx*(1+fn);
  k1 := trunc(po(w1/alf1,1/3)+ 0.0000000001);   {round up when k > .99..}
  n1 := k1 - q1;

  w2 := w1 - k1*k1*k1*alf1;
     if k1*k1*k1<0 then writeln(f,'K1**3 out of range in GSTRUK! Use type real(extended) here!');
     if print=3 then writeln(f,'k1^3=',k1*k1*k1,'   faktor=',k1*k1*k1*alf1);
  k2 := trunc(sqrt(w2/alf2) + 0.0000000001);    {round up when k > .99...}
  n2 := k2 - q2;

  w3 := w2 - k2*k2*alf2;
  k3 := trunc(w3/alf3 + 0.0000000001);           {round up when k > .99..}
  n3 := k3 - q3;

  w4 := w3 - k3*alf3;
{Now 3 cases are possible. The code for this has had an error in the 1982 DESY version
so that coumputation of K4 failed in the case w4 > 1 (OP2006)}

  if w4<=0 then k4 := trunc(alf3*k3 + 0.0000000001)                         {case a, XXXI}
   else k4 := trunc(-ln(w4)/(2*k-1)*(3*q4) + 0.0000000001);    {FORTRAN log(x) = ln (x)}
    if w4>1 then
     BEGIN
      k3 := k3 - 1;
      n3 := k3 - q3;
      k4 := k4 + trunc(alf3*k3 + 0.0000000001); {round up when k > .99..}
      msg:='Resonance not allowed!';
      if print>1 then writeln(f,'Corrected values of K3, n3, K4, n4. ', msg)
     END;
  n4:= k4 - q4;

{test print}
   if print>2 then
   BEGIN
    writeln(f,'Test print GSTRUC:');
    writeln(f,' fn =',fn);
    writeln(f,' W1 =',w1);
    writeln(f,' W2 =',w2);
    writeln(f,' W3 =',w3);
    writeln(f,' W4 =',w4);
    writeln(f,' ')
   END;

  if print>1 then
   BEGIN
    writeln(f,'  K1   K2   K3   K4   n1   n2   n3   n4');
    writeln(f,k1:4, ' ',k2:4,' ',k3:4,' ',k4:4,' ',n1:4,' ',n2:4,' ',n3:4,' ',n4:4);
    writeln(f,' ')
   END;
  END;



PROCEDURE GMASS; {computation of masses from quantum numbers and N}
 VAR zw1:extended;
 BEGIN

{The DESY term kgh represents terms K + G + h from the 1982 script (XI)}
{Ni are substituted here with alphai (IX), Ki = ni + Qi}
{The composed term kgh has less elements and therefore computation is more accurate}
{(3-9) f(k)}
  kgh := 4*(alf1*k1*k1*(1+k1)*(1+k1)*0.25 + alf2*k2*(2*k2*k2 + 3*k2 + 1)/6 + alf3*k3*(1+k3)*0.5 + k4);

{(3-7) f(k,kq,P,Q,kappa)}
  zw1 := etaqk(kq,k);
  fig := 3*P/(pi*sqrt(zw1))*(1-alfm/alfp)*(P+Q)*cos(pi*(P+Q) )*(1-alfa/3+pi/2*(k-1)*po(3,1-kq/2))*
  (1 + 2*k*kappa/(3*eta*eta)*xi*(1+xi*xi*(P-Q)*(pi*pi - kq))) / (1 + 4*xi/k*binom(P,2)*po(xi/6,kq))*
  (2*sqrt(etaqk(1,1)*zw1) + kq*eta*eta*(k-1))*(1+(4*pi*alfa)/(eta*sqrt(eta)))*(1+Q*(1-kappa)*(2-k)*n1/q1)+
  4*(1-alfm/alfp)*alfa/(xi*xi)*(P+Q)+4*kq*alfm/alfp ;

(*
fik:=(fig-4*kq*alfm/alfp)*0.25;  {? OP2006}
*)

  if print>2 then
   BEGIN
    writeln(f,'Test print GMASS:');
    writeln(f,' kgh                      fig');
    writeln(f,kgh ,'  ',fig);
    writeln(f,'');
   END;

{(3-9)  f}
  am := amu*fakMeV*alfp*(kgh + fig);
 END;


PROCEDURE GLIMIT; {search for resonance limits}
 var
  a1,a2,a3,qa,ra,da,sa,ta,temp1,ft:extended;
  ls,ltmp:longint;             {integer in Pascal is limited to 32.000}
  temp2:integer;               {0 when electrons/1 else}
 BEGIN
  lme:=0;
  if ((Q*(2-k)*(1-kappa)) = 1) then exit; {skip search when calculating e- (Electrons)}

  {(XXXIII) substituted with M0 and G=k+1}
  l1 := trunc( po( (po(2*(P+1),2-k)* (k+1) )  / (4*alf1)* (kgh+fig),1/3) - q1 + 0.0000000001); {round up when >.99.. OP2006}

  {now bringing (XXXIV) into normalized form x**3 + a1x**2 + a2*x +a3 = 0 with x=(L2 + Q2)}
  a1 := 1.5;
  a2 := 0.5;
  a3 := -3*alf1/alf2*po(l1+q1,3);

  {Cardan solution of the reduced equation with substitutions q and r}
  qa := (3*a2 - a1*a1)/9;
  ra := (9*a1*a2 - 27*a3 - 2*a1*a1*a1)/54;

  {diskriminant}
  da := Sqrt(qa*qa*qa + ra*ra);

  {solution}
  sa := po(ra+da,1/3);
  ta := po(ra-da,1/3);
  l2 := trunc(sa + ta - a1/3 - q2 + 0.0000000001);    {round up when >.99..}

  {(XXXIV-2), (XXXIV-3)}
  l3 := trunc( sqrt(2*alf2/alf3*(l2+q2)*(l2+q2) + 0.25)- 0.5 - q3 + 0.0000000001);  {round up here when >.99? OP2006}
  l4 := trunc( alf3*(l3+q3) - q4 + 0.0000000001);     {round up when >.99..}

  {(XXXV)}
  {determine maximum n=lme in lme= 1 .. loop }
  {determine f(L)=temp1}
  temp1 := (alf1*po(l1+q1,3) + alf2*(l2+q2)*(l2+q2) + alf3*(l3+q3)
           + exp( ((1-2*k)*(l4+q4)) / (3*q4))) /wgx - 1;
  temp2 := 1 - Q*(2-k)*(1-kappa);       {case selector, =0 if electron selected, =1 else,
                                         left part of f(N) (XXV) }

  for ls:= 3 to loop do
   BEGIN
    {if print>2 then writeln(ls); } {test}
    ltmp := ls  - 1;
    if ltmp=1 then   {skip over n=1 otherwise Fn becomes imaginary}
     else
     BEGIN
      if ls=loop-1 then writeln(f,'loop = ',loop, ' *** No excitation within these iterations! Setting Le = loop.');
      ft := temp2*( agx*ltmp/(ltmp+2) + bgx*sqrt(ltmp*(ltmp-2)) ); {XXV}
      if ft<=temp1 then                 {go on searching}
      else BEGIN lme:= ltmp-1; ls:=loop END  {exit when ft(ltemp) < temp1(L1,L2,L3,L4), Le=preceding value }
     END;
   END;       {end of search loop for le}

   if print>2 then
   BEGIN
    writeln(f,'Test print GLIMIT:');
    writeln(f, 'a1 = ',a1,'   a2 = ', a2,'   a3 = ', a3);
    writeln(f, 'qa = ',qa,'   ra = ', ra,'   da = ', da);
    writeln(f, 'sa = ',sa,'   ta = ', ta);
    writeln(f, 'temp1 = ',temp1,'   temp2 = ', temp2,'  ft = ',ft);
    writeln(f, ' ');
   END;

   {print maximum parameters}
   writeln(f,'Resonance limit for element x=',x ,':');
   writeln(f,'  L1   L2   L3   L4   Le');
   writeln(f,l1:4 ,' ', l2:4, ' ', l3:4, ' ', l4:4,'',lme:5);
   writeln(f,'----------------------------------------------------');


END;


{==== Main program ================================================ }
BEGIN
 {define output destination}
 if dest=1 then BEGIN assign(f,'Output'); rewrite(f) END
  else BEGIN assign(f,'gprogout.lis'); rewrite(f);
  writeln('Output is directed to the file "grogout.lis"!')  END;

 writeln(f,' ****************************************************');
 writeln(f,' * Mass formula of elementary particles by B.Heim   *');
 writeln(f,' * Program : H.D. Schulz, 26/07/82  DESY            *');
 writeln(f,' * Pascal version 0.62 by Olaf Posdzech, 2006       *');
 writeln(f,' ****************************************************');
 writeln(f,' ');


 GVALUES;  {setting values of natural constants used}

{setting controls}
assign(fi,'gprogin.dat');
reset(fi);
for i:=1 to 5 do readln(fi,t1,t2);  {skip first lines here}

(*
{read additional inputs from file if needed}
 readln(fi,t1,print);
 readln(fi,t1,nend);
 readln(fi,t1,loop);
 readln(fi,t1,ant);
 readln(fi,t1);
 readln(fi,t1,ja,je);
*)

 writeln(f,' Used loop limits : ');
 writeln(f,' ================== ');
 writeln(f,'  nend, maximum excitation level = ', nend);
 writeln(f,'  loop, resonance search         = ', loop);
 writeln(f,'  ant,  particle/antiparticle    = ', ant );
 writeln(f,' ');

 GINIT;  {computation of basic constants from gamma, hq, pi and ebn}

 writeln(f,'Data sets named: ', ja , ' to ', je);

 if ja>1 then for i:=1 to 5*(ja-1) do readln(fi);
for j:=ja to je do {compute data sets no.  ja .. je}
 BEGIN

{read set of quantum numbers of multiplet}
readln(fi,t1);
writeln(f,'========================================================');
writeln(f,'Starting computation of multiplet #',j,':');
writeln(f,t1);
readln(fi,t1,k); writeln(f,'k = Baryon number + 1 = ',k);
readln(fi,t1,P); writeln(f,'P = 2* Isospin        = ',P);
readln(fi,t1,Q);     writeln(f,'Q = 2* Spin           = ',Q);
readln(fi,t1,kappa); writeln(f,'kappa = Doublett      = ',kappa);

for epsi := 1 to ant do  {define eps=particle/antiparticle, 2nd loop is for the antiparticle}
BEGIN
 eps := 1 - (epsi-1)*2 ; {+1/-1}

 {computation of strangeness}
 epsp := round( eps* cos( pi * Q * (kappa+binom(P,2)) ));
 epsq := round( eps* cos( pi * Q * (Q*(k-1)+binom(P,2)) ));
 cs   := round( 2/(k*(1+kappa)) * (P*epsp + Q*epsq)*(k-1+kappa));

 {define isomultiplett component}
 xe := P + 1; {number of elements in multiplett}

 for x := 1 to xe do
 BEGIN
  writeln(f,'');
  writeln(f,'=========================================================');
  writeln(f,'Now calculating element of multiplet ',j,', x = ',x);

  {F(k,pg,qg,kappa,eps) }
  qx:= round( ((P+2-2*x)*(1-kappa*Q*(2-k))+cs+eps*(k-1-(1+kappa)*Q*(2-k)))/2 );

  {compute charge kq }
  kq := abs(qx);

  {test print }
  if print>2 then
     BEGIN
      writeln(f,'Test print MAIN:');
      writeln(f,'=========================================================');
      writeln(f,'eps epsp  epsq    cs   kq    x   qx');
      writeln(f,eps,'     ',epsp:2,'    ',epsq:2,'    ',cs:2,'    ',kq,'    ',x,'   ',qx:2);
     END;

 GBASE;      {compute numbers for the ground level N = 0}

 {The original DESY code has had a loop here calculating masses for n=0 to maximum n
 while skipping n=1. This has been cut off here for more clearity. }

{calculating mass for N = 0}
 {  writeln(f,'N = ',n);  }
   n:=0;
   GSTRUC;
   GMASS;
   {print output}
   writeln(f,'  Cs   kq  eps   qx    N    am [MeV]');
   writeln(f,cs:4,'    ', kq, '    ', eps, '   ', qx:2, ' ', n:4,'   ', am,' ',msg);
   writeln(f,'----------------------------------------------------');

{search  for maximum excitation level n=le}
   GLIMIT;    {This has been put into a procedure here OP2006}

{skip over N = 1 otherwise Fn becomes imaginary, nend=1 used here as nend:=lme}
if nmax=1 then nend:=lme else if nmax>lme then nend:=lme else nend:=nmax;

if print=3 then writeln('x=',x,'  nend=',nend);

{calculate masses for N = 2 to nend}
 for  n:= 2 to nend do
   BEGIN
    {writeln(f,'N = ',n);  }
    GSTRUC;
    GMASS;
    {print output}
    if print>1 then
    writeln(f,'  Cs   kq  eps   qx    N    am [MeV]');
    writeln(f,cs:4,'    ', kq, '    ', eps, '   ', qx:2, ' ', n:4,'   ', am,' ',msg);
    if print > 1 then writeln(f,'----------------------------------------------------');
   END;

   END; {loop element x of multiplett}
  END; {loop particle/antiparticle}
  END; {loop multiplett j}
  writeln(f,'***************************************************');
  close(f);      {output file}
  close(fi);     {input file}
END.
