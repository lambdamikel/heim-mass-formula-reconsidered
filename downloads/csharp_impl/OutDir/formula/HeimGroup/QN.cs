// Version b0.07
using System;
using Constants = formula.Constants;
namespace formula.HeimGroup
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
		* N3 - Based on Heim Theory Group code
		*/
		public override double N3(double k, double q)
		{
			
			double u = 2.0 * System.Math.PI * System.Math.E;
			
			double zw5 = ((k - 1.0) * (1.0 - (System.Math.PI * ((1 - eta(k, q)) / (1 + System.Math.Sqrt(eta(1, q)))))) * (1 - ((u * ((eta(1, q)) / (theta(1, q)))) * (1 - (Constants.alphaMinus / Constants.alphaPlus)) * System.Math.Pow(1 - System.Math.Sqrt(Constants.eta), 2))));
			
			double zw4 = (System.Math.Pow(1 - System.Math.Sqrt(Constants.eta), 2) * ((((3.0 / 4.0) * System.Math.Pow(u, 2) * 2.0 * (1 + System.Math.Sqrt(eta(1, q)))) / ((1 - Constants.eta) * Constants.theta)) - 1) * ((4.0 / 3.0) / u));
			
			return (System.Math.Pow(System.Math.E, zw5 - zw4) * (2.0 / k));
		}
	}
}