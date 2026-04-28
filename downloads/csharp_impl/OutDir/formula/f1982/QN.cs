using System;
namespace formula.f1982
{
	
	// Version b0.07
	
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
		* N3 - EQUATION (9.9) (p67)
		*   http://www.heim-theory.com/downloads_pw/D_Zur_Herleitung_Der_Heimschen_Massenformel.pdf
		*/
		public override double N3(double k, double q)
		{
			
			// E_ doc don't forget times 2.0
			return 2.0 * alpha3(k, q);
		}
	}
}