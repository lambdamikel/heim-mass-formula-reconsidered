// Version b0.07
using System;
using AbstractParticle = formula.AbstractParticle;
namespace formula.f1989
{
	
	public class MainFunctions
	{
		
		// Quantum Number Equations Calculator
		//UPGRADE_NOTE: The initialization of  'qnC' was moved to static method 'formula.f1989.MainFunctions'. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1005"'
		public static formula.QN qnC;
		
		/*
		* The parameters are those found in Tabel I (p2, Selected Results) for particles:
		*         k - column 1
		*         q - absolute value of column 8 (epsilon_q)
		*         n - column 2
		*         m - column 3
		*         p - column 4
		*     sigma - column 5
		*         P - column 6
		*         Q - column 7
		*     kappa - column 10
		* epsilon_q - column 8
		*/
		
		/*
		* G - EQUATION (G underline) XI (p5, 1982 formula)
		*/
		public static double G(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			
			return ((System.Math.Pow(qnC.Q1(k), 2) * System.Math.Pow(1 + qnC.Q1(k), 2) * qnC.N1(k, q)) + (qnC.Q2(k) * ((2 * System.Math.Pow(qnC.Q2(k), 2)) + (3 * qnC.Q2(k)) + 1) * qnC.N2(k, q)) + (qnC.Q3(k) * (1 + qnC.Q3(k)) * qnC.N3(k, q)) + (4 * qnC.Q4(k)));
		}
		
		/*
		* S - EQUATION (K) XI (p5, 1982 formula)
		*/
		public static double S(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int n = particle.n;
			int m = particle.m;
			int p = particle.p;
			int sigma = particle.sigma;
			
			return ((System.Math.Pow(n, 2) * System.Math.Pow(1 + n, 2) * qnC.N1(k, q)) + (m * ((2 * System.Math.Pow(m, 2)) + (3 * m) + 1) * qnC.N2(k, q)) + (p * (1 + p) * qnC.N3(k, q)) + (4 * sigma));
		}
		
		/*
		* F1989 - EQUATION B5 (p11, 1989 formula)
		*/
		public static double F(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int n = particle.n;
			int m = particle.m;
			int p = particle.p;
			int sigma = particle.sigma;
			
			/*
			* NOTE: Based on observation in the Heim Groups Code the missing 
			*       N1 in the first term compared to the 1982 formula was indeed 
			*       a mistake in the 1989 paper.
			*/
			
			return (((2 * n * qnC.Q1(k)) * (1 + (3 * (n + qnC.Q1(k) + (n * qnC.Q1(k)))) + (2 * (System.Math.Pow(n, 2) + System.Math.Pow(qnC.Q1(k), 2)))) * qnC.N1(k, q)) + (6 * m * qnC.Q2(k) * (1 + m + qnC.Q2(k)) * qnC.N2(k, q)) + (2 * p * qnC.Q3(k) * qnC.N3(k, q)) - (SelfCouplingFunction.Instance.phi(particle)));
		}
		
		/*
		* phi - EQUATION B6 (p12, 1989 formula)
		*/
		public static double phi(AbstractParticle particle)
		{
			
			int P = particle.P;
			int Q = particle.Q;
			int k = particle.k;
			int q = particle.q;
			
			return (P * System.Math.Pow(- 1, P + Q) * ((P + Q) * qnC.N5(k, q))) + (Q * (P + 1) * qnC.N6(k, q));
		}
		static MainFunctions()
		{
			qnC = QN.Instance;
		}
	}
}