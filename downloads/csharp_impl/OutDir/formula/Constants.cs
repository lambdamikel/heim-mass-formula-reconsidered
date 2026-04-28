// Version b0.07
using System;
namespace formula
{
	
	/*
	* This class contains constants which in some cases are used throughout the 
	* mass equation calculations. The physics constants though are only used to
	* calculate the derived mass element constant, which is one of the 
	* introductory parts of the mass equations. The mass element has type kg.
	*
	* NOTE: I've used the most recent precise values i could find. 
	*/
	public class Constants
	{
		public static double GravitationConstant
		{
			set
			{
				gravitationConstant = value;
				massElement = (MathL.root(System.Math.PI, 4.0) * MathL.root(3.0 * System.Math.PI * gravitationConstant * plancksConstant, 3.0) * System.Math.Sqrt(plancksConstant / (3.0 * lightVelocity * gravitationConstant)));
				massElementHG = (MathL.root(System.Math.PI, 4.0) * MathL.root(3.0 * System.Math.PI * gravitationConstant * plancksConstant, 3.0) * (System.Math.Sqrt((lightVelocity * plancksConstant) / (3 * gravitationConstant)) / lightVelocity));
			}	
		}
		
		

		private static readonly double plancksConstant = (6.6260693 * System.Math.Pow(10.0, - 34.0)) / (2.0 * System.Math.PI);
		private static readonly double lightVelocity = 2.99792458 * System.Math.Pow(10.0, 8.0);
		public static double gravitationConstant;
		private static readonly double inductionConstant = System.Math.PI * 4.0 * System.Math.Pow(10.0, - 7.0);
		private static readonly double influenceConstant = 1.0 / (inductionConstant * lightVelocity * lightVelocity);
		private static readonly double vacuumWaveResistance = (inductionConstant * lightVelocity);
		public static readonly double geometricalConstant = (1.0 + System.Math.Sqrt(5.0)) / 2.0;
		public static double massElement;
		
		
		/*
		* The Mass Constant - HG code
		*
		* Looks like theres a new version of the Mass Constant
		* in the Heim Groups code.
		*/
		public static double massElementHG;
		
		
		/* Inverse fine-structure constant - Note this is "alpha == alpha(+)^(-1)" !
		* alpha - middle of page (p4, 1982 formula)
		*/
		public const double alpha = 1.0 / 137.03599911;
		
		
		/*
		* eta - constant version of eta in EQUATIONS V (p3, 1982 formula) and VII
		*
		* NOTE: The non-constant versions can be found in the EQ class.
		*/
		public static readonly double eta = System.Math.PI / MathL.root((System.Math.Pow(System.Math.PI, 4.0) + 4.0), 4.0);
		
		
		/*
		* theta - constant version of theta in EQUATIONS V (p3, 1982 formula)
		*
		* NOTE: The non-constant versions can be found in the EQ class.
		*/
		public static readonly double theta = (5.0 * eta) + (2.0 * System.Math.Sqrt(eta)) + 1.0;
		
		
		// HD: just before eq. VII.
		private static readonly double t = 1.0 - ((2.0 / 3.0) * geometricalConstant * System.Math.Pow(eta, 2) * (1.0 - System.Math.Sqrt(eta)));
		
		
		/*
		* alpha+ - one of EQUATIONS VIII (p4, 1982 formula)
		*/
		public static readonly double alphaPlus = t * (1.0 / (System.Math.Pow(eta, 2.0) * MathL.root(eta, 3.0))) - 1.0;
		
		
		/*
		* alpha- - one of EQUATIONS VIII (p4, 1982 formula)
		*/
		public static readonly double alphaMinus = t * (1.0 / (eta * MathL.root(eta, 3.0))) - 1.0;
		
		
		/*
		* alpha+ - one of EQUATIONS B4 (p11, 1989 formula)
		*/
		public static readonly double altAlphaPlus = (System.Math.Pow(eta, (1.0 / 6.0)) / System.Math.Pow(eta, 2.0) * (1.0 - theta * System.Math.Pow((2.0 * (1.0 - System.Math.Sqrt(eta))) / (eta * (1.0 + System.Math.Sqrt(eta))), 2.0) * System.Math.Sqrt(2.0 * eta)) - 1.0);
		
		
		/*
		* alpha- - one of EQUATIONS B4 (p11, 1989 formula)
		*/
		public static readonly double altAlphaMinus = ((altAlphaPlus + 1.0) * eta) - 1.0;
		
		
		static Constants()
		{
			gravitationConstant = 6.6742 * System.Math.Pow(10.0, - 11.0);
			massElement = (MathL.root(System.Math.PI, 4.0) * MathL.root(3.0 * System.Math.PI * gravitationConstant * plancksConstant, 3.0) * System.Math.Sqrt(plancksConstant / (3.0 * lightVelocity * gravitationConstant)));
			massElementHG = (MathL.root(System.Math.PI, 4.0) * MathL.root(3.0 * System.Math.PI * gravitationConstant * plancksConstant, 3.0) * (System.Math.Sqrt((lightVelocity * plancksConstant) / (3 * gravitationConstant)) / lightVelocity));
		}
	}
}