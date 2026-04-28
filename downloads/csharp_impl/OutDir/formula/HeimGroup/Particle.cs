// Version b0.07
using System;
using AbstractParticle = formula.AbstractParticle;
using AbstractFormula = formula.AbstractFormula;
using MathL = formula.MathL;
namespace formula.HeimGroup
{
	
	/*
	* Practical implementation of particle representation based on 
	* 1982 formula.
	*/
	public class Particle:AbstractParticle
	{
		override protected internal int ChargeAmount
		{
			/*
			* q - one of EQUATIONS II (p3, 1982 formula)
			*/
			get
			{	
				return MathL.trunc(System.Math.Abs(qx));
			}
			
		}
		
		// Quantum Number Equations Calculator
		public static formula.QN qnC;
		private int[] K;
		
		public Particle(System.String name, int index, int k, int P, int Q, int kappa, int x):base(name, index, k, P, Q, kappa, x)
		{
		}
		
		/*
		* C - one of EQUATIONS I (p2, 1982 formula)
		*/
		protected internal override int getStructureDistributor(bool timeHelicity)
		{
			double alpha_P = System.Math.PI * Q * (kappa + MathL.comb(P, 2));	
			double alpha_Q = System.Math.PI * Q * (Q + MathL.comb(P, 2));
			double epsilon_P;
			double epsilon_Q;
			if (timeHelicity)
			{
				epsilon_P = System.Math.Cos(alpha_P);
				epsilon_Q = System.Math.Cos(alpha_Q);
			}
			else
			{	
				epsilon_P = - System.Math.Cos(alpha_P);
				epsilon_Q = - System.Math.Cos(alpha_Q);
			}
			
			return MathL.trunc((2 * ((P * epsilon_P) + (Q * epsilon_Q)) * (k - 1 + kappa)) / ((1 + kappa) * k));
		}
		
		/*
		* qx - One of EQUATIONS II (p3, 1982 formula)
		*/
		protected internal override int getQuantumNumber(bool timeHelicity)
		{
			if (timeHelicity)
			{	
				return MathL.trunc((1.0 / 2.0) * (((P - (2 * x)) * (1 - (kappa * Q * (2 - k)))) + (k - 1 - ((1 + kappa) * Q * (2 - k))) + C));
			}
			else
			{	
				return MathL.trunc((1.0 / 2.0) * (((P - (2 * x)) * (1 - (kappa * Q * (2 - k)))) - (k - 1 - ((1 + kappa) * Q * (2 - k))) + C));
			}
		}
		
		protected internal override int get_n()
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			return getEquationK(1) - (int) qnC.Q1(k);
		}
		
		protected internal override int get_m()
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			return getEquationK(2) - (int) qnC.Q2(k);
		}
		
		protected internal override int get_p()
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			return getEquationK(3) - (int) qnC.Q3(k);
		}
		
		protected internal override int get_sigma()
		{
			
			//UPGRADE_WARNING: Narrowing conversions may produce unexpected results in C#. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1042"'
			return getEquationK(4) - (int) qnC.Q4(k);
		}
		
		private int getEquationK(int i)
		{
			
			if (K == null)
			{
				K = calculateEquationsK();
			}
			
			switch (i)
			{
				
				
				case 1:  return K[0];
				
				case 2:  return K[1];
				
				case 3:  return K[2];
				
				case 4:  return K[3];
				}
			
			throw new System.Exception("Invalid equation K (must be 1-4)");
		}
		
		private int[] calculateEquationsK()
		{
			
			double[] W = new double[4];
			int[] K = new int[4];
			
			W[0] = Wrap();
			K[0] = MathL.trunc(MathL.root(W[0] / getAlpha(1), 3));
			for (int i = 1; i < 4; i++)
			{
				
				W[i] = W[i - 1] - (getAlpha(i) * System.Math.Pow(K[i - 1], 4 - i));
				
				if (i == 1)
					K[1] = MathL.trunc(System.Math.Sqrt(W[1]) * (1 / getAlpha(2)));
				else if (i == 2)
				{
					//System.out.println("" + this + " K2 " + (W[2]/getAlpha(3)));
					K[2] = MathL.trunc(W[2] / getAlpha(3));
					//System.out.println("" + this + " K2 " + MathL.trunc(W[2]/getAlpha(3)));
				}
				else if (i == 3)
				{
					//System.out.println("" + this + " K3 " + (-3*qnC.Q4(k)*Math.log(W[3]))/((2*k)-1));
					K[3] = MathL.trunc(((- 3) * qnC.Q4(k) * System.Math.Log(W[3])) / ((2 * k) - 1));
				}
			}
			
			return K;
		}
		
		private double getAlpha(int i)
		{
			
			switch (i)
			{
				
				
				case 1:  return qnC.alpha1(k, q);
				
				case 2:  return qnC.alpha2(k, q);
				
				case 3:  return qnC.alpha3(k, q);
				}
			
			throw new System.Exception("Invalid equation alpha (must be 1-3)");
		}

		protected internal virtual double Wrap()
		{
			if (index == AbstractFormula.E_MINUS)
				return 38.7;
			else if (index == AbstractFormula.E_ZERO)
				return 38.51;
			else if (index == AbstractFormula.MU)
				return 2830.26;
			else if (index == AbstractFormula.PI_CHARGE)
				return 3514.46;
			else if (index == AbstractFormula.PI_ZERO)
				return 3419.16;
			else if (index == AbstractFormula.ETA)
				return 9905.01;
			else if (index == AbstractFormula.K_CHARGE)
				return 8857.96;
			else if (index == AbstractFormula.K_ZERO)
				return 9332.36;
			else if (index == AbstractFormula.P)
				return 14792.56;
			else if (index == AbstractFormula.N)
				return 14828.61;
			else if (index == AbstractFormula.LAMBDA)
				return 16827.98;
			else if (index == AbstractFormula.SIGMA_PLUS)
				return 18124.03;
			else if (index == AbstractFormula.SIGMA_MINUS)
				return 18183.3;
			else if (index == AbstractFormula.SIGMA_ZERO)
				return 18179.6;
			else if (index == AbstractFormula.XI_CHARGE)
				return 18998.73;
			else if (index == AbstractFormula.XI_ZERO)
				return 18990.09;
			else if (index == AbstractFormula.OMEGA_CHARGE)
				return 23157.61;
			else if (index == AbstractFormula.DELTA_PLUSPLUS)
				return 18115.38;
			else if (index == AbstractFormula.DELTA_PLUS)
				return 18467.56;
			else if (index == AbstractFormula.DELTA_MINUS)
				return 18448.52;
			else if (index == AbstractFormula.DELTA_ZERO)
				return 18508.94;
			
			throw new System.Exception("Unknown Particle");
		}

		static Particle()
		{
			qnC = QN.Instance;
		}
	}
}