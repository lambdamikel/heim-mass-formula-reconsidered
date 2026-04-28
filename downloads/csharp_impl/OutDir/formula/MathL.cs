// Version b0.07
using System;
namespace formula
{
	
	// Extended math library with... Factorial, Combination, Root
	public class MathL
	{
		public static System.Decimal factorial(int r)
		{
			System.Decimal n = new System.Decimal(1);
			for (int i = 1; i <= r; i++)
			{
				n = System.Decimal.Multiply(n, new System.Decimal(i));
			}	
			return n;
		}
		
		public static int comb(int n, int r)
		{	
			return System.Decimal.ToInt32((System.Decimal.Divide(factorial(n), System.Decimal.Multiply(factorial(r), factorial(n - r)))));
		}
		
		public static double root(double a, double b)
		{			
			return System.Math.Pow(a, (1.0 / b));
		}
		
		public static double doubleToDecimals(double value_Renamed, int decimals)
		{			
			System.Decimal bigDecimal = new System.Decimal(value_Renamed);
			return System.Decimal.ToDouble(bigDecimal);
		}
		
		/*
		* Type conversion from double to int in the heim mass formula 
		* must occur according to the following.
		*/
		public static int trunc(double a)
		{			
			if (a < 0)
			{
				return (int) System.Math.Ceiling(a);
			}
			else
			{
				return (int) System.Math.Floor(a);
			}
		}
	}
}