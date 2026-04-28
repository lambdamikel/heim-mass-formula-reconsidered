// Version b0.07
using System;
using AbstractParticle = formula.AbstractParticle;
using AbstractFormula = formula.AbstractFormula;
namespace formula.dummyHG
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
				
				switch (index)
				{
					case AbstractFormula.E_MINUS:  return 1;
					case AbstractFormula.E_ZERO:  return 0;
					case AbstractFormula.MU:  return 1;
					case AbstractFormula.PI_CHARGE:  return 1;
					case AbstractFormula.PI_ZERO:  return 0;
					case AbstractFormula.ETA:  return 0;
					case AbstractFormula.K_CHARGE:  return 1;
					case AbstractFormula.K_ZERO:  return 0;
					case AbstractFormula.P:  return 1;
					case AbstractFormula.N:  return 0;
					case AbstractFormula.LAMBDA:  return 0;
					case AbstractFormula.SIGMA_PLUS:  return 1;
					case AbstractFormula.SIGMA_MINUS:  return 1;
					case AbstractFormula.SIGMA_ZERO:  return 0;
					case AbstractFormula.XI_CHARGE:  return 1;
					case AbstractFormula.XI_ZERO:  return 0;
					case AbstractFormula.OMEGA_CHARGE:  return 1;
					case AbstractFormula.DELTA_PLUSPLUS:  return 2;
					case AbstractFormula.DELTA_PLUS:  return 1;
					case AbstractFormula.DELTA_MINUS:  return 1;
					case AbstractFormula.DELTA_ZERO:  return 0;
					}
				throw new System.ArithmeticException("Result unknown for q(" + this + ")");
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
			
			switch (index)
			{
				case AbstractFormula.E_MINUS:  return 0;
				case AbstractFormula.E_ZERO:  return 0;
				case AbstractFormula.MU:  return 0;
				case AbstractFormula.PI_CHARGE:  return 0;
				case AbstractFormula.PI_ZERO:  return 0;
				case AbstractFormula.ETA:  return 0;
				case AbstractFormula.K_CHARGE:  return 1;
				case AbstractFormula.K_ZERO:  return 1;
				case AbstractFormula.P:  return 0;
				case AbstractFormula.N:  return 0;
				case AbstractFormula.LAMBDA:  return - 1;
				case AbstractFormula.SIGMA_PLUS:  return - 1;
				case AbstractFormula.SIGMA_MINUS:  return - 1;
				case AbstractFormula.SIGMA_ZERO:  return - 1;
				case AbstractFormula.XI_CHARGE:  return - 2;
				case AbstractFormula.XI_ZERO:  return - 2;
				case AbstractFormula.OMEGA_CHARGE:  return - 3;
				case AbstractFormula.DELTA_PLUSPLUS:  return 0;
				case AbstractFormula.DELTA_PLUS:  return 0;
				case AbstractFormula.DELTA_MINUS:  return 0;
				case AbstractFormula.DELTA_ZERO:  return 0;
				}
			throw new System.ArithmeticException("Result unknown for C(" + this + ")");
		}
		
		/*
		* qx - One of EQUATIONS II (p3, 1982 formula)
		*/
		protected internal override int getQuantumNumber(bool timeHelicity)
		{
			
			switch (index)
			{
				case AbstractFormula.E_MINUS:  return - 1;
				case AbstractFormula.E_ZERO:  return 0;
				case AbstractFormula.MU:  return - 1;
				case AbstractFormula.PI_CHARGE:  return 1;
				case AbstractFormula.PI_ZERO:  return 0;
				case AbstractFormula.ETA:  return 0;
				case AbstractFormula.K_CHARGE:  return 1;
				case AbstractFormula.K_ZERO:  return 0;
				case AbstractFormula.P:  return 1;
				case AbstractFormula.N:  return 0;
				case AbstractFormula.LAMBDA:  return 0;
				case AbstractFormula.SIGMA_PLUS:  return 1;
				case AbstractFormula.SIGMA_MINUS:  return - 1;
				case AbstractFormula.SIGMA_ZERO:  return 0;
				case AbstractFormula.XI_CHARGE:  return - 1;
				case AbstractFormula.XI_ZERO:  return 0;
				case AbstractFormula.OMEGA_CHARGE:  return - 1;
				case AbstractFormula.DELTA_PLUSPLUS:  return 2;
				case AbstractFormula.DELTA_PLUS:  return 1;
				case AbstractFormula.DELTA_MINUS:  return - 1;
				case AbstractFormula.DELTA_ZERO:  return 0;
				}
			throw new System.ArithmeticException("Result unknown for qx(" + this + ")");
		}
		
		protected internal override int get_n()
		{
			
			switch (index)
			{
				case AbstractFormula.E_MINUS:  return 0;
				case AbstractFormula.E_ZERO:  return 0;
				case AbstractFormula.MU:  return 11;
				case AbstractFormula.PI_CHARGE:  return 12;
				case AbstractFormula.PI_ZERO:  return 12;
				case AbstractFormula.ETA:  return 18;
				case AbstractFormula.K_CHARGE:  return 17;
				case AbstractFormula.K_ZERO:  return 18;
				case AbstractFormula.P:  return 0;
				case AbstractFormula.N:  return 0;
				case AbstractFormula.LAMBDA:  return 1;
				case AbstractFormula.SIGMA_PLUS:  return 2;
				case AbstractFormula.SIGMA_MINUS:  return 2;
				case AbstractFormula.SIGMA_ZERO:  return 2;
				case AbstractFormula.XI_CHARGE:  return 2;
				case AbstractFormula.XI_ZERO:  return 2;
				case AbstractFormula.OMEGA_CHARGE:  return 4;
				case AbstractFormula.DELTA_PLUSPLUS:  return 2;
				case AbstractFormula.DELTA_PLUS:  return 2;
				case AbstractFormula.DELTA_MINUS:  return 2;
				case AbstractFormula.DELTA_ZERO:  return 2;
				}
			throw new System.ArithmeticException("Result unknown for n(" + this + ")");
		}
		
		protected internal override int get_m()
		{
			
			switch (index)
			{
				case AbstractFormula.E_MINUS:  return 0;
				case AbstractFormula.E_ZERO:  return 0;
				case AbstractFormula.MU:  return 6;
				case AbstractFormula.PI_CHARGE:  return 9;
				case AbstractFormula.PI_ZERO:  return 3;
				case AbstractFormula.ETA:  return 22;
				case AbstractFormula.K_CHARGE:  return 26;
				case AbstractFormula.K_ZERO:  return 5;
				case AbstractFormula.P:  return 0;
				case AbstractFormula.N:  return 0;
				case AbstractFormula.LAMBDA:  return 3;
				case AbstractFormula.SIGMA_PLUS:  return - 7;
				case AbstractFormula.SIGMA_MINUS:  return - 6;
				case AbstractFormula.SIGMA_ZERO:  return - 7;
				case AbstractFormula.XI_CHARGE:  return 7;
				case AbstractFormula.XI_ZERO:  return 6;
				case AbstractFormula.OMEGA_CHARGE:  return 4;
				case AbstractFormula.DELTA_PLUSPLUS:  return 1;
				case AbstractFormula.DELTA_PLUS:  return - 1;
				case AbstractFormula.DELTA_MINUS:  return - 1;
				case AbstractFormula.DELTA_ZERO:  return - 1;
				}
			throw new System.ArithmeticException("Result unknown for m(" + this + ")");
		}
		
		protected internal override int get_p()
		{
			
			switch (index)
			{
				case AbstractFormula.E_MINUS:  return 0;
				case AbstractFormula.E_ZERO:  return 0;
				case AbstractFormula.MU:  return 11;
				case AbstractFormula.PI_CHARGE:  return 2;
				case AbstractFormula.PI_ZERO:  return 6;
				case AbstractFormula.ETA:  return 17;
				case AbstractFormula.K_CHARGE:  return 30;
				case AbstractFormula.K_ZERO:  return 5;
				case AbstractFormula.P:  return 0;
				case AbstractFormula.N:  return - 2;
				case AbstractFormula.LAMBDA:  return 0;
				case AbstractFormula.SIGMA_PLUS:  return - 12;
				case AbstractFormula.SIGMA_MINUS:  return - 5;
				case AbstractFormula.SIGMA_ZERO:  return - 14;
				case AbstractFormula.XI_CHARGE:  return - 17;
				case AbstractFormula.XI_ZERO:  return - 1;
				case AbstractFormula.OMEGA_CHARGE:  return - 1;
				case AbstractFormula.DELTA_PLUSPLUS:  return 9;
				case AbstractFormula.DELTA_PLUS:  return - 1;
				case AbstractFormula.DELTA_MINUS:  return - 16;
				case AbstractFormula.DELTA_ZERO:  return - 10;
				}
			throw new System.ArithmeticException("Result unknown for p(" + this + ")");
		}
		
		protected internal override int get_sigma()
		{
			
			switch (index)
			{
				case AbstractFormula.E_MINUS:  return 0;
				case AbstractFormula.E_ZERO:  return 1;
				case AbstractFormula.MU:  return 6;
				case AbstractFormula.PI_CHARGE:  return 3;
				case AbstractFormula.PI_ZERO:  return 4;
				case AbstractFormula.ETA:  return 14;
				case AbstractFormula.K_CHARGE:  return 28;
				case AbstractFormula.K_ZERO:  return 2;
				case AbstractFormula.P:  return 0;
				case AbstractFormula.N:  return 17;
				case AbstractFormula.LAMBDA:  return - 11;
				case AbstractFormula.SIGMA_PLUS:  return 10;
				case AbstractFormula.SIGMA_MINUS:  return - 8;
				case AbstractFormula.SIGMA_ZERO:  return - 2;
				case AbstractFormula.XI_CHARGE:  return 2;
				case AbstractFormula.XI_ZERO:  return 6;
				case AbstractFormula.OMEGA_CHARGE:  return - 15;
				case AbstractFormula.DELTA_PLUSPLUS:  return 4;
				case AbstractFormula.DELTA_PLUS:  return - 6;
				case AbstractFormula.DELTA_MINUS:  return - 15;
				case AbstractFormula.DELTA_ZERO:  return 2;
				}
			throw new System.ArithmeticException("Result unknown for sigma(" + this + ")");
		}
		static Particle()
		{
			qnC = QN.Instance;
		}
	}
}