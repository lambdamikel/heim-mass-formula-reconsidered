using System;
namespace formula
{
	// Version b0.07
	
	/*
	* This class deals with equations related to determining the value of the Quantum 
	* Number EQUATIONS IX-X (p5, 1982 formula) and B8-B14 (p12, 1989 formula). Note that
	* equation N3 is the one given in the 1989 formula. 
	*/
	public abstract class QN
	{
		public QN()
		{
			InitBlock();
		}
		private void  InitBlock()
		{
			fineStructureConstant = Constants.alpha;
			thetaConstant = Constants.geometricalConstant;
		}
		
		/*
		* eta - one of EQUATIONS V (p3, 1982 formula)
		*
		* NOTE: eta(1,0) = eta according to the 1989 formula. The constant version 
		* of the function eta, eta(1,0) is given in the Constants class.
		*/
		public virtual double eta(double k, double q)
		{			
			return System.Math.PI / System.Math.Pow(System.Math.Pow(System.Math.PI, 4.0) + ((4.0 + k) * System.Math.Pow(q, 4.0)), (1.0) / (4.0));
		}
		
		/*
		* theta - one of EQUATIONS V (p3, 1982 formula)
		*
		* NOTE: theta(1,0) = theta according to the 1989 formula. The constant version 
		* of the function theta, theta(1,0) is given in the Constants class.
		*/
		public virtual double theta(double k, double q)
		{	
			return (5 * eta(k, q)) + (2 * System.Math.Sqrt(eta(k, q))) + 1;
		}
		
		public virtual double alpha1(double k, double q)
		{	
			return 0.5 * (1 + System.Math.Sqrt(eta(k, q)));
		}
		
		/*
		* N1 - one of EQUATIONS IX (p5, 1982 formula)
		*/
		public virtual double N1(double k, double q)
		{	
			return alpha1(k, q);
		}
		
		public virtual double alpha2(double k, double q)
		{	
			return (1 / eta(k, q));
		}
		
		/*
		* N2 - one of EQUATIONS IX (p5, 1982 formula)
		*/
		public virtual double N2(double k, double q)
		{	
			return (2.0 / 3.0) * alpha2(k, q);
		}
		
		private double fineStructureConstant;
		private double thetaConstant;
		
		
		// Document D, p67, (9.9)
		// D_ doc (seems good :) - we are only off for q=2 and N3(2,2)
		private double H(double k, double q)
		{
			return ((fineStructureConstant / 3.0) * (1.0 + System.Math.Sqrt(eta(k, q))) * System.Math.Pow((thetaConstant / (eta(k, q) * eta(k, q))), (2.0 * k + 1.0)) * System.Math.Pow(eta(k, q), 3.0));
		}
		
		// Document D, p67, (9.9)
		// D_ doc  better? has to be right
		private double G(double k, double q)
		{	
			return ((eta(1, 1) / (System.Math.E * eta(k, q))) * System.Math.Pow((2.0 * thetaConstant * eta(k, q)), k) * System.Math.Pow(((1.0 - System.Math.Sqrt(eta(k, q))) / (1.0 + System.Math.Sqrt(eta(k, q)))), 2.0));
		}
		
		public virtual double alpha3(double k, double q)
		{	
			return ((System.Math.Pow(System.Math.E, (k - 1)) / k) - q * (H(k, q) + G(k, q)));
		}
		
		public abstract double N3(double k, double q);
		
		/*
		* N4 - EQUATION B9 (p12, 1989 formula)
		*/
		public virtual double N4(double k, double q)
		{	
			return (4.0 / k) * (1.0 + (q * (k - 1.0)));
		}
		
		/*
		* A - EQUATION B11 (p12, 1989 formula)
		*/
		private double A()
		{	
			return ((8.0 / Constants.eta) * (1.0 - (Constants.alphaMinus / Constants.alphaPlus)) * (1.0 - ((3.0 * Constants.eta) / 4.0)));
		}
		
		/*
		* N - EQUATION B12 (p12, 1989 formula)
		*/
		private double N(double k)
		{	
			return (Q1(k) + Q2(k) + Q3(k) + Q4(k) + (k * (System.Math.Pow(- 1, k)) * System.Math.Pow(2, System.Math.Pow(k, 2) - 1)));
		}
		
		/*
		* N' - EQUATION B14 (p12, 1989 formula)
		*/
		private double diffN(double k)
		{	
			return (Q1(k) + Q2(k) + Q3(k) + Q4(k) - (2 * k) - 1);
		}
		
		/*
		* N5 - EQUATION B10 (p12, 1989 formula)
		*/
		public virtual double N5(double k, double q)
		{	
			return (A() * (1.0 + (k * (k - 1.0) * System.Math.Pow(2.0, System.Math.Pow(k, 2.0) + 3.0) * N(k) * A() * System.Math.Pow((1 - System.Math.Sqrt(eta(k, q))) / (1 + System.Math.Sqrt(eta(k, q))), 2))));
		}
		
		/*
		* N6 - EQUATION B13 (p12, 1989 formula)
		*/
		public virtual double N6(double k, double q)
		{	
			return (((2 * k) / (System.Math.PI * System.Math.E * Constants.theta)) * ((System.Math.Sqrt(k) * (System.Math.Pow(k, 2) - 1) * (N(k) / System.Math.Sqrt(eta(k, 1))) * (q - ((1 - q) * (diffN(k) / (Q1(k) * System.Math.Sqrt(eta(k, 1))))))) + System.Math.Pow(- 1, k + 1)) * Constants.eta * (1 - (Constants.alphaMinus / Constants.alphaPlus)) * System.Math.Pow(4 * ((1 - System.Math.Sqrt(Constants.eta)) / (1 + System.Math.Sqrt(Constants.eta))), 2) * Q4(k));
		}
		
		
		/*
		* Small Function needed for the below equations
		*/
		private double s(double k)
		{	
			return System.Math.Pow(k, 2) + 1;
		}
		
		/*
		* Q1 - one of EQUATIONS X (p5, 1982 formula)
		* 
		* NOTE: in the 1989 formula this is refered to as Qn
		*/
		public virtual double Q1(double k)
		{	
			return 3 * System.Math.Pow(2, s(k) - 2);
		}
		
		/*
		* Q2 - one of EQUATIONS X (p5, 1982 formula)
		* 
		* NOTE: in the 1989 formula this is refered to as Qm
		*/
		public virtual double Q2(double k)
		{	
			return System.Math.Pow(2, s(k)) - 1;
		}
		
		/*
		* Q3 - one of EQUATIONS X (p5, 1982 formula)
		* 
		* NOTE: in the 1989 formula this is refered to as Qp
		*/
		public virtual double Q3(double k)
		{	
			return System.Math.Pow(2, s(k)) + (2 * System.Math.Pow(- 1, k));
		}
		
		/*
		* Q4 - one of EQUATIONS X (p5, 1982 formula)
		* 
		* NOTE: in the 1989 formula this is refered to as Qsigma
		*/
		public virtual double Q4(double k)
		{
			return System.Math.Pow(2, s(k) - 1) - 1;
		}
	}
}