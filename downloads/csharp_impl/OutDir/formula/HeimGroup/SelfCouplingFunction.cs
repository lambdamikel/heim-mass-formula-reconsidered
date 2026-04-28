// Version b0.07
using System;
using MathL = formula.MathL;
using Constants = formula.Constants;
using AbstractParticle = formula.AbstractParticle;
namespace formula.HeimGroup
{
	
	/*
	* NOTE: In this revised revision everything has been checked against the 
	*       Heim Groups fortran code
	*
	* This class deals with all equations related to determining the value of the so 
	* called 'self-couplings function' phi given as EQUATION B7 (p12, 1989 formula).
	* It is needed to evaluate EQUATION B5 (p11, 1989 formula).
	* 
	* The main sub-equations of the self-couplings function are EQUATIONS B22-B28 
	* (p13, 1989 formula) as well as U given just below phi EQUATION B7. Also a1,
	* a2, and a3 EQUATIONS B29-B31 (p14, 1989 formula) are needed to evaluate x
	* EQUATION B27 (p13, 1989 formula).
	*
	* NOTE: Minor probems:
	*
	*    1) a1, a2 and a3 return incorrect values for a few particals Tabel VIII
	*       (p10, Selected Results).
	*/
	public class SelfCouplingFunction : formula.SelfCouplingFunction
	{
		public static formula.SelfCouplingFunction Instance
		{
			// ensure singleton and of extended QN type
			
			get
			{
				
				if (instance == null)
				{
					instance = new SelfCouplingFunction();
				}
				
				return instance;
			}
			
		}
		
		// Quantum Number Equations Calculator
		//UPGRADE_NOTE: The initialization of  'qnC' was moved to static method 'formula.HeimGroup.SelfCouplingFunction'. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1005"'
		public static formula.QN qnC;
		
		private static SelfCouplingFunction instance;
		
		private SelfCouplingFunction()
		{
		}
		
		/*
		* Self Couplings Function phi - EQUATION B7 (p12, 1989 formula)
		*/
		public virtual double phi(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int p = particle.p;
			int sigma = particle.sigma;
			int P = particle.P;
			int Q = particle.Q;
			int kappa = particle.kappa;
			int qx = particle.qx;
			
			// NOTE: phi is solely incorrect at this point because W is incorrect!
			
			return ((((qnC.N4(k, q) * System.Math.Pow(p, 2)) / (1 + System.Math.Pow(p, 2))) * ((sigma + qnC.Q4(k)) / System.Math.Sqrt(1 + System.Math.Pow(sigma, 2))) * (MathL.root(2, 4.0) - (4 * B(k) * U(particle) * System.Math.Pow(W(particle), - 1)))) + (P * System.Math.Pow(P - 2, 2) * (1.0 + (kappa * ((1 - q) / (2.0 * Constants.alpha * Constants.theta)))) * System.Math.Pow(System.Math.PI / System.Math.E, 2) * System.Math.Sqrt(qnC.eta(2, 1)) * (qnC.Q1(k) - qnC.Q2(k))) - ((P + 1) * (MathL.comb((int) Q, 3) / Constants.alpha)));
		}
		
		/*
		* U - Given just below EQUATION B7 (p12, 1989 formula) or as EQUATION B50 (p17, 1989 formula)
		*/
		private double U(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int p = particle.p;
			int sigma = particle.sigma;
			int P = particle.P;
			int Q = particle.Q;
			int kappa = particle.kappa;
			int qx = particle.qx;
			
			return (System.Math.Pow(2, k + P + Q + kappa) * (System.Math.Pow(P, 2) + ((3.0 / 2.0) * (P - Q)) + (P * (1 - q)) + (4 * kappa * B(k) * ((1 - Q) / (3 - (2 * q)))) + ((k - 1) * (P + (2 * Q) - (4.0 * System.Math.PI * (P - Q) * ((1 - q) / MathL.root(2, 4.0)))))) * System.Math.Pow(qnC.eta(k, q), - 2));
		}
		
		/*
		* W - EQUATION B22 (p13, 1989 formula)
		*/
		public virtual double W(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int p = particle.p;
			int sigma = particle.sigma;
			int P = particle.P;
			int Q = particle.Q;
			int kappa = particle.kappa;
			int qx = particle.qx;
			
			// NOTE: the values for function W on tables VIII do not correlate...
			// W is the reason that phi is impricise!
			
			return ((A(k) * System.Math.Pow(System.Math.E, x(particle)) * System.Math.Pow(1 - Constants.eta, L(k, Q, kappa))) + ((P - Q) * (1 - (MathL.comb((int) P, 2) * (1 - MathL.comb((int) Q, 3)))) * System.Math.Pow(1 - System.Math.Sqrt(Constants.eta), 2) * System.Math.Sqrt(2.0)));
		}
		
		/*
		* A - EQUATION B23 (p13, 1989 formula)
		*/
		public virtual double A(double k)
		{
			
			// NOTE: the values for function A on tables VI do not correlate...
			
			// Is this a problem with function g?
			
			// Interresting that A(1) has the exact same decimal figures 
			// as in the table but incorrect overall value
			
			return 8 * g(k) * H(k) * System.Math.Pow(2 - k + (8 * H(k) * (k - 1)), - 1);
		}
		
		/*
		* H - EQUATION B24 (p13, 1989 formula)
		*
		* Relies on the Quantum Number equations, these are in the QN class.
		*/
		public virtual double H(double k)
		{
			
			return qnC.Q1(k) + qnC.Q2(k) + qnC.Q3(k) + qnC.Q4(k);
		}
		
		/*
		* g - EQUATION B25 (p13, 1989 formula)
		*
		* Relies on the Quantum Number equations, these are in the QN class.
		*/
		private double g(double k)
		{
			
			return (System.Math.Pow(qnC.Q1(k), 3) + System.Math.Pow(qnC.Q2(k), 2) + ((qnC.Q3(k) / k) * System.Math.Pow(System.Math.E, k - 1)) + System.Math.Pow(System.Math.E, ((- ((2 * k) - 1)) / 3.0)) - (H(k) * (k - 1)));
		}
		
		/*
		* L - EQUATION B26 (p13, 1989 formula)
		*/
		private double L(double k, double Q, double kappa)
		{
			
			return (1 - kappa) * Q * (2 - k);
		}
		
		/*
		* x - EQUATION B27 (p13, 1989 formula)
		*/
		private double x(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int p = particle.p;
			int sigma = particle.sigma;
			int P = particle.P;
			int Q = particle.Q;
			int kappa = particle.kappa;
			int qx = particle.qx;
			
			return (((1 - Q - MathL.comb((int) P, 2)) * (2 - k)) + ((1.0 / (4.0 * B(k))) * (a1(particle) + ((System.Math.Pow(k, 3) / (4 * H(k))) * (a2(particle) + (a3(particle) / (4 * B(k))))))));
		}
		
		/*
		* B - EQUATION B28 (p13, 1989 formula)
		*/
		public virtual double B(double k)
		{
			
			return 3 * H(k) * System.Math.Pow(System.Math.Pow(k, 2) * ((2 * k) - 1), - 1);
		}
		
		// a1, a2 and a3
		
		/*
		* a1
		*/
		public virtual double a1(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int p = particle.p;
			int sigma = particle.sigma;
			int P = particle.P;
			int Q = particle.Q;
			int kappa = particle.kappa;
			int qx = particle.qx;
			
			double ia1 = (1 + B(k) + (k * (System.Math.Pow(Q, 2) + 1) * MathL.comb((int) Q, 3)) - (kappa * (((B(k) - 1) * (2 - k)) - (3 * (H(k) - (2 * (1 + q))) * (P - Q)) + 1)));
			
			double ia2 = ((3 * (2 - q) * MathL.comb((int) P, 2)) - (Q * ((3 * (P + Q)) + q))) * (2 - k);
			
			double ia3 = (1 + ((B(k) / k) * (k + P - Q))) * (1 - MathL.comb((int) P, 2)) * (1 - MathL.comb((int) Q, 3));
			
			double a1 = (ia1 - ((1 - kappa) * (ia2 + (((k * (P + 1) * MathL.comb((int) P, 2)) + ia3 - (q * (1 - q) * MathL.comb((int) Q, 3))) * (k - 1)))));
			
			return a1;
		}
		
		/*
		* a2
		*/
		public virtual double old_a2(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int p = particle.p;
			int sigma = particle.sigma;
			int P = particle.P;
			int Q = particle.Q;
			int kappa = particle.kappa;
			int qx = particle.qx;
			
			double ieq = qx;
			
			double zw = (((B(k) * (1 - (MathL.comb((int) Q, 3) * (1 - MathL.comb((int) P, 3))))) + (6.0 / k)) - (kappa * (((1.0 / 2.0) * (Q * (B(k) - (7 * k)))) - (((3 * q) - 1) * (k - 1)) + ((1.0 / 2.0) * (P - Q) * (4 + (B(k) + 1)) * (1 - q)))));
			
			double teil1 = zw;
			
			double z4 = P * (((1.0 / 2.0) * B(k)) + 2.0 + q) * (2 - k);
			
			double z5 = (- Q) * (((1.0 / 2.0) * B(k)) + (1 - (4 * (1 + (4 * q))))) * (2 - k);
			
			double teil2 = z4 + z5;
			
			double z6 = (1.0 / 4.0) * (B(k) - 2) * (1.0 + (1.5 * (P - Q)));
			
			double z7 = (- (1.0 / 2.0)) * (B(k) * (1 - q));
			
			double z8 = (((1.0 / 2.0) * (B(k) + q - ieq)) + (3 * ieq)) * (2 - ieq);
			
			double z9 = (- (1.0 / 4.0)) * ((B(k) + 2) * (1 - q));
			
			double teil3 = (z6 + z7 - (MathL.comb((int) P, 2) * (z8 + z9))) * ((1 - MathL.comb((int) Q, 3)) * (k - 1));
			
			double teil4 = ((- MathL.comb((int) P, 3)) * (((2 * (1 + ieq)) + ((1.0 / 2.0) * ((2 - q) * ((3 * (1 - q)) + ieq))) - q) - ((1.0 / 4.0) * q * ((1 - q) * (B(k) - 4.0))) - ((1.0 / 4.0) * (B(k) - 2)) + ((1.0 / 2.0) * (B(k) * (1 - q)))));
			
			double a2 = teil1 - (1 - kappa) * (teil2 + teil3 + teil4);
			
			return a2;
		}
		
		/*
		* a2
		*/
		public virtual double a2(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int p = particle.p;
			int sigma = particle.sigma;
			int P = particle.P;
			int Q = particle.Q;
			int kappa = particle.kappa;
			int qx = particle.qx;
			
			double ieq = qx;
			
			double z1 = (B(k) * (1.0 - (MathL.comb((int) Q, 3) * (1 - MathL.comb((int) P, 3))))) + (6.0 / k);
			
			double z2 = (P - Q) * (4 + ((B(k) + 1) * (1 - q))) / 2.0;
			
			double z3 = ((B(k) - (7 * k)) * (Q / 2.0)) - (((3 * q) - 1) * (k - 1));
			
			double z4 = P * ((B(k) / 2.0) + 2 + q) * (2 - k);
			
			double z5 = (- Q) * ((B(k) / 2.0) + 1 - (4 * (1 + (4 * q)))) * (2 - k);
			
			double z6 = (B(k) - 2) * (1 + (3 * ((P - Q) / 2.0))) / 4.0;
			
			double z7 = (- (1 - q)) * (B(k) / 2.0);
			
			double z8 = (((B(k) + q - ieq) / 2.0) + (3 * ieq)) * (2 - ieq);
			
			double z9 = (- (B(k) + 2)) * ((1 - q) / 4.0);
			
			double z10 = (2 - q) * ((3 * (1 - q)) + ieq) / 2.0;
			
			double z11 = (- q) * (1 - q) * (B(k) - 4) / 4.0;
			
			double z12 = (- (B(k) - 2)) / 4.0;
			
			double z13 = B(k) * (1 - q) / 2.0;
			
			double teil1 = z1 - (kappa * (z3 + z2));
			
			double teil2 = z4 + z5;
			
			double teil3 = (z6 + z7 - (MathL.comb((int) P, 2) * (z8 + z9))) * (1 - MathL.comb((int) q, 3)) * (k - 1);
			
			double teil4 = (- MathL.comb((int) P, 3)) * (((2 * (1 + ieq)) + z10 - q) + z11 + z12 + z13);
			
			double a2 = teil1 - (1 - kappa) * (teil2 + teil3 + teil4);
			
			return a2;
		}
		
		/*
		* a3
		*/
		public virtual double a3(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int p = particle.p;
			int sigma = particle.sigma;
			int P = particle.P;
			int Q = particle.Q;
			int kappa = particle.kappa;
			int qx = particle.qx;
			
			double ieq = qx;
			
			double wet = System.Math.Sqrt(Constants.eta);
			
			double zw = (((wet / k) * ((4 * (2.0 - wet)) - (System.Math.PI * System.Math.E * (1 - Constants.eta) * wet)) * (k + (System.Math.E * wet * (k - 1)))) + (5 * (1.0 - q) * ((4 * B(k)) + P + Q) / ((2 * k) + System.Math.Pow(- 1, k))));
			
			double z2 = (P - 1) * (P - 2) * ((2.0 * (H(k) + 2) / System.Math.Pow(k, 2)) + ((2 - k) * (1.0 / 2.0) / System.Math.PI));
			
			double z3 = q * B(k) * (1.0 / 2.0) * (B(k) + (2 * (P - Q)));
			
			double z1 = ((P * (P + 2) * B(k)) + ((P + 1) * (P + 1)) - (q * (1 + ieq) * ((k * (System.Math.Pow(P, 2) + 1) * (B(k) + 2)) + ((System.Math.Pow(P, 2) + P + 1) / 4.0))) - (q * (1 - ieq) * (B(k)) + System.Math.Pow(P, 2) + 1)) * (k - 1);
			
			double z4 = ((((P - Q) * (H(k) + 2)) + (P * ((5 * B(k) * (1 + q) * Q) + (k * (k - 1) * ((k * System.Math.Pow(P + Q, 2) * (H(k) + (3 * k) + 1) * (1 - q)) - ((B(k) + (6 * k)) / 2.0)))))) * (1.0 - MathL.comb((int) Q, 3)) * (1.0 - MathL.comb((int) P, 2)));
			
			double z5 = (((ieq * (B(k) + (2 * Q) + 1)) + (q * (1.0 / 2.0) * (1 - ieq) * ((2 * k) + 1) / k) + ((1 - q) * (System.Math.Pow(Q, 2) + 1 + (2 * B(k))))) * Q * (2 - q) * MathL.comb((int) P, 3));
			
			double zw1 = z2 + (MathL.comb((int) P, 2) * (1 - MathL.comb((int) Q, 3)) * (z3 + z1)) + z4 + z5;
			
			double y = kappa * zw + (1 - kappa) * zw1;
			
			y = y * (1.0 / 2.0) / B(k);
			
			double a3 = ((4 * B(k)) * y / (1.0 + y)) - (1.0 / (4 + B(k)));
			
			return a3;
		}
		static SelfCouplingFunction()
		{
			qnC = QN.Instance;
		}
	}
}