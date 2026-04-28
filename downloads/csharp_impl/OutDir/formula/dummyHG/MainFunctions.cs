// Version b0.07
using System;
using AbstractParticle = formula.AbstractParticle;
using Constants = formula.Constants;
using MathL = formula.MathL;
namespace formula.dummyHG
{
	
	/*
	* This class is the main entry point for the mass equation given as M, EQUATION
	* B3 (p11, 1989 formula). The parameter mu in the front of the mass equation is 
	* given in kg thus the mass equation result is in kg (since no other values with 
	* type occur in the formula). The mass is converted to MeV before being returned.
	*/
	public class MainFunctions
	{
		
		// Quantum Number Equations Calculator
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
		* F1982 - EQUATION (H) XI (p5, 1982 formula)
		*/
		public static double F(AbstractParticle particle)
		{
			
			int k = particle.k;
			int q = particle.q;
			int n = particle.n;
			int m = particle.m;
			int p = particle.p;
			
			return (((2 * n * qnC.Q1(k)) * (1 + (3 * (n + qnC.Q1(k) + (n * qnC.Q1(k)))) + (2 * (System.Math.Pow(n, 2) + System.Math.Pow(qnC.Q1(k), 2)))) * qnC.N1(k, q)) + (6 * m * qnC.Q2(k) * (1 + m + qnC.Q2(k)) * qnC.N2(k, q)) + (2 * p * qnC.Q3(k) * qnC.N3(k, q)));
		}
		

		/*
		* phi - EQUATION XI (p5, 1982 formula)
		*/
		public static double phi(AbstractParticle particle)
		{
			
			int P = particle.P;
			int Q = particle.Q;
			int k = particle.k;
			int q = particle.q;
			int kappa = particle.kappa;
			
			return ((3 * (P / (System.Math.PI * System.Math.Sqrt(qnC.eta(k, q)))) * (1 - (Constants.alphaMinus / Constants.alphaPlus)) * (P + Q) * System.Math.Pow(- 1, P + Q) * (1 - (Constants.alpha / 3) + ((System.Math.PI / 2) * (k - 1) * System.Math.Pow(3, 1 - (q / 2)))) * (1 + (2 * k * (kappa / (3 * System.Math.Pow(Constants.eta, 2))) * Constants.geometricalConstant * (1 + (System.Math.Pow(Constants.geometricalConstant, 2) * (P - Q) * (System.Math.Pow(System.Math.PI, 2) - q))))) * System.Math.Pow(1 + (4 * Constants.geometricalConstant * (MathL.comb((int) P, 2) / k) * System.Math.Pow(Constants.geometricalConstant / 6, q)), - 1) * ((2 * System.Math.Sqrt(qnC.eta(1, 1)) * System.Math.Sqrt(qnC.eta(k, q))) + (q * System.Math.Pow(Constants.eta, 2) * (k - 1))) * (1 + (4 * System.Math.PI * (Constants.alpha / Constants.eta) * System.Math.Sqrt(Constants.eta))) * (1 + (Q * (1 - kappa) * (2 - k) * (qnC.N1(k, q) / qnC.Q1(k))))) + (4 * (1 - (Constants.alphaMinus / Constants.alphaPlus)) * Constants.alpha * ((P + Q) / System.Math.Pow(Constants.geometricalConstant, 2))) + (4 * q * (Constants.alphaMinus / Constants.alphaPlus)));
		}
		static MainFunctions()
		{
			qnC = QN.Instance;
		}
	}
}