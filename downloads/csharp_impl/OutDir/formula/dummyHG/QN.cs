using System;
namespace formula.dummyHG
{
	
	// Version b0.07
	
	/*
	* This is a dummy class with the intended purpos of 
	* returning known results from the Selected Results
	* paper. It can be used to verify alternative real
	* formulas.
	*/
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
		
		public override double eta(double k, double q)
		{
			
			
			switch ((int) k)
			{
				
				
				case 0: 
					//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
					if ((int) q == 1)
						return 0.98998964;
					break;
				
				case 1: 
					if ((int) q == 1)
						return 0.98756399;
					break;
				
				case 2: 
					if ((int) q == 1)
						return 0.98516776;
					else
					{
						if ((int) q == 2)
							return 0.84242385;
					}
					break;
				}
			
			throw new System.ArithmeticException("Result unknown for eta(" + k + ", " + q + ")");
		}
		
		public override double theta(double k, double q)
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			switch ((int) k)
			{
				
				
				case 0: 
					if ((int) q == 1)
						return 7.93991266;
					break;
				
				case 1: 
					if ((int) q == 1)
						return 7.92534503;
					break;
				
				case 2: 
					if ((int) q == 1)
						return 7.91095114;
					else
					{
						if ((int) q == 2)
							return 7.04779227;
					}
					break;
				}
			
			throw new System.ArithmeticException("Result unknown for theta(" + k + ", " + q + ")");
		}
		
		
		public override double alpha1(double k, double q)
		{
			
			throw new System.ArithmeticException("Result unknown for alpha1(" + k + ", " + q + ")");
		}
		
		public override double N1(double k, double q)
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			switch ((int) k)
			{
				
				
				case 1: 
					if ((int) q == 0)
						return 1;
					else
					{
						if ((int) q == 1)
							return 0.99688127;
					}
					break;
				
				case 2: 
					if ((int) q == 0)
						return 1;
					else
					{
						if ((int) q == 1)
							return 0.99627809;
						else
						{
							if ((int) q == 2)
								return 0.95891826;
						}
					}
					break;
				}
			
			throw new System.ArithmeticException("Result unknown for N1(" + k + ", " + q + ")");
		}
		
		
		public override double alpha2(double k, double q)
		{
			
			throw new System.ArithmeticException("Result unknown for alpha2(" + k + ", " + q + ")");
		}
		
		public override double N2(double k, double q)
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			switch ((int) k)
			{
				case 1: 
					if ((int) q == 0)
						return 0.66666667;
					else
					{
						if ((int) q == 1)
							return 0.67506174;
					}
					break;
				
				case 2: 
					if ((int) q == 0)
						return 0.66666667;
					else
					{
						if ((int) q == 1)
							return 0.67670370;
						else
						{
							if ((int) q == 2)
								return 0.79136728;
						}
					}
					break;
				}
			
			throw new System.ArithmeticException("Result unknown for N2(" + k + ", " + q + ")");
		}
		
		
		public override double alpha3(double k, double q)
		{
			
			throw new System.ArithmeticException("Result unknown for alpha3(" + k + ", " + q + ")");
		}
		
		public override double N3(double k, double q)
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			switch ((int) k)
			{
				
				
				case 1: 
					if ((int) q == 0)
						return 2;
					else
					{
						if ((int) q == 1)
							return 1.95731764;
					}
					break;
				
				case 2: 
					if ((int) q == 0)
						return 2.71828183;
					else
					{
						if ((int) q == 1)
							return 2.59881924;
						else
						{
							if ((int) q == 2)
								return 2.12190443;
						}
					}
					break;
				}
			
			throw new System.ArithmeticException("Result unknown for N3(" + k + ", " + q + ")");
		}
		
		public override double N4(double k, double q)
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			switch ((int) k)
			{
				
				
				case 1: 
					if ((int) q == 0)
						return 4;
					else
					{
						if ((int) q == 1)
							return 4;
					}
					break;
				
				case 2: 
					if ((int) q == 0)
						return 2;
					else
					{
						if ((int) q == 1)
							return 4;
						else
						{
							if ((int) q == 2)
								return 6;
						}
					}
					break;
				}
			
			throw new System.ArithmeticException("Result unknown for N4(" + k + ", " + q + ")");
		}
		
		public override double N5(double k, double q)
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			switch ((int) k)
			{
				
				
				case 1: 
					if ((int) q == 0)
						return 1.15773470;
					else
					{
						if ((int) q == 1)
							return 1.15773470;
					}
					break;
				
				case 2: 
					if ((int) q == 0)
						return 1.15773470;
					else
					{
						if ((int) q == 1)
							return 1.73247496;
						else
						{
							if ((int) q == 2)
								return 76.73214581;
						}
					}
					break;
				}
			
			throw new System.ArithmeticException("Result unknown for N5(" + k + ", " + q + ")");
		}
		
		public override double N6(double k, double q)
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			switch ((int) k)
			{
				
				
				case 1: 
					if ((int) q == 0)
						return 0.00000164;
					else
					{
						if ((int) q == 1)
							return 0.00000164;
					}
					break;
				
				case 2: 
					if ((int) q == 0)
						return - 0.10493009;
					else
					{
						if ((int) q == 1)
							return 0.02518725;
						else
						{
							if ((int) q == 2)
								return 0.15580107;
						}
					}
					break;
				}
			
			throw new System.ArithmeticException("Result unknown for N6(" + k + ", " + q + ")");
		}
		
		public override double Q1(double k)
		{
			
			if (k == 1)
			{
				
				return 3;
			}
			else if (k == 2)
			{
				
				return 24;
			}
			
			throw new System.ArithmeticException("Result unknown for Q1(" + k + ")");
		}
		
		
		public override double Q2(double k)
		{
			
			if (k == 1)
			{
				
				return 3;
			}
			else if (k == 2)
			{
				
				return 31;
			}
			
			throw new System.ArithmeticException("Result unknown for Q2(" + k + ")");
		}
		
		public override double Q3(double k)
		{
			
			if (k == 1)
			{
				
				return 2;
			}
			else if (k == 2)
			{
				
				return 34;
			}
			
			throw new System.ArithmeticException("Result unknown for Q3(" + k + ")");
		}
		
		public override double Q4(double k)
		{
			
			if (k == 1)
			{
				
				return 1;
			}
			else if (k == 2)
			{
				
				return 15;
			}
			
			throw new System.ArithmeticException("Result unknown for Q4(" + k + ")");
		}
	}
}