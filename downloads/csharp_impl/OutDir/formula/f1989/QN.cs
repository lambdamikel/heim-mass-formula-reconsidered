// Version b0.07
using System;
using Constants = formula.Constants;
namespace formula.f1989
{
	
	public class QN:formula.QN
	{
		public static formula.QN Instance
		{
			// ensure singleton and of extended QN type
			
			get
			{
				
				if (instance == null)
				{
					instance = new QN();
				}
				
				return instance;
			}
			
		}
		
		private static QN instance;
		
		private QN()
		{
		}
		
		/*
		* N3 - EQUATION B8 (p12, 1989 formula)
		* From http://www.heim-theory.com/downloads/F_Heims_Mass_Formula_1989.pdf
		*/
		public override double N3(double k, double q)
		{
			
			double u = 2.0 * System.Math.PI * System.Math.E;
			
			return (System.Math.Pow(System.Math.E, (k - 1) * (1 - (System.Math.PI * ((1 - eta(k, q)) / (1 + System.Math.Sqrt(eta(1, q)))) * (1 - (u * ((eta(1, q)) / (theta(1, q))) * (1 - (Constants.alphaMinus / Constants.alphaPlus)) * System.Math.Pow((1 - System.Math.Sqrt(Constants.eta)), 2))))) - ((2 / (3 * System.Math.PI * System.Math.E)) * System.Math.Pow((1 - System.Math.Sqrt(Constants.eta)), 2) * ((6.0 * System.Math.Pow(System.Math.PI, 2) * (System.Math.Pow(System.Math.E, 2) / Constants.theta) * ((1 + System.Math.Sqrt(eta(1, q))) / (1 - Constants.eta))) - 1))) / (k / 2.0));
		}
	}
}