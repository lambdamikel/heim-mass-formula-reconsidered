// Version b0.07
using System;
using AbstractParticle = formula.AbstractParticle;
using AbstractFormula = formula.AbstractFormula;
namespace formula.dummyHG
{
	
	
	/*
	* This is a dummy class with the intended purpos of 
	* returning known results from the Selected Results
	* paper. It can be used to verify alternative real
	* formulas.
	*/
	public class SelfCouplingFunction : formula.SelfCouplingFunction
	{
		public static formula.SelfCouplingFunction Instance
		{
			// ensure singleton and of extended QN type
			
			get
			{
				
				if (instance == null)
				{
					instance = new SelfCouplingFunction();
				}
				
				return instance;
			}
			
		}
		
		private static SelfCouplingFunction instance;
		
		private SelfCouplingFunction()
		{
		}
		
		public virtual double phi(AbstractParticle particle)
		{
			
			switch (particle.index)
			{
				case AbstractFormula.E_MINUS:  return 0;
				case AbstractFormula.E_ZERO:  return 0;
				case AbstractFormula.MU:  return 2.57120915;
				case AbstractFormula.PI_CHARGE:  return - 2.32863274;
				case AbstractFormula.PI_ZERO:  return - 5.12094079;
				case AbstractFormula.ETA:  return 5.06612007;
				case AbstractFormula.K_CHARGE:  return - 40.78574065;
				case AbstractFormula.K_ZERO:  return - 12.73395842;
				case AbstractFormula.P:  return 9.28034058;
				case AbstractFormula.N:  return 11.16885467;
				case AbstractFormula.LAMBDA:  return 0;
				case AbstractFormula.SIGMA_PLUS:  return - 6.00947753;
				case AbstractFormula.SIGMA_MINUS:  return - 2.01125294;
				case AbstractFormula.SIGMA_ZERO:  return 11.78154008;
				case AbstractFormula.XI_CHARGE:  return 23.44132266;
				case AbstractFormula.XI_ZERO:  return 90.44612205;
				case AbstractFormula.OMEGA_CHARGE:  return - 137.03604095;
				case AbstractFormula.DELTA_PLUSPLUS:  return - 1364.07751672;
				case AbstractFormula.DELTA_PLUS:  return - 623.74523006;
				case AbstractFormula.DELTA_MINUS:  return - 985.00227539;
				case AbstractFormula.DELTA_ZERO:  return - 548.14408156;
				}
			throw new System.ArithmeticException("Result unknown for phi(" + particle + ")");
		}
		
		public virtual double W(AbstractParticle particle)
		{
			
			switch (particle.index)
			{
				case AbstractFormula.E_MINUS:  return 38.70294226;
				case AbstractFormula.E_ZERO:  return 38.51308957;
				case AbstractFormula.MU:  return 2830.2632345;
				case AbstractFormula.PI_CHARGE:  return 3514.46294316;
				case AbstractFormula.PI_ZERO:  return 3419.16217346;
				case AbstractFormula.ETA:  return 9905.00599107;
				case AbstractFormula.K_CHARGE:  return 8857.95769020;
				case AbstractFormula.K_ZERO:  return 9332.35821820;
				case AbstractFormula.P:  return 14792.56308050;
				case AbstractFormula.N:  return 14828.61089116;
				case AbstractFormula.LAMBDA:  return 16827.97671482;
				case AbstractFormula.SIGMA_PLUS:  return 18124.03136129;
				case AbstractFormula.SIGMA_MINUS:  return 18183.30294347;
				case AbstractFormula.SIGMA_ZERO:  return 18179.59733741;
				case AbstractFormula.XI_CHARGE:  return 18998.73451193;
				case AbstractFormula.XI_ZERO:  return 18990.08927597;
				case AbstractFormula.OMEGA_CHARGE:  return 23157.61451004;
				case AbstractFormula.DELTA_PLUSPLUS:  return 18115.38391620;
				case AbstractFormula.DELTA_PLUS:  return 18467.56082305;
				case AbstractFormula.DELTA_MINUS:  return 18508.94119539;
				case AbstractFormula.DELTA_ZERO:  return 18448.51703290;
				}
			throw new System.ArithmeticException("Result unknown for W(" + particle + ")");
		}
		
		public virtual double A(double k)
		{
			
			if (k == 1)
			{
				
				return 2787.59025432;
			}
			else if (k == 2)
			{
				
				return 14727.57867072;
			}
			
			throw new System.ArithmeticException("Result unknown for A(" + k + ")");
		}
		
		public virtual double H(double k)
		{
			
			if (k == 1)
			{
				
				return 9;
			}
			else if (k == 2)
			{
				
				return 104;
			}
			
			throw new System.ArithmeticException("Result unknown for H(" + k + ")");
		}
		
		public virtual double B(double k)
		{
			
			if (k == 1)
			{
				
				return 27;
			}
			else if (k == 2)
			{
				
				return 26;
			}
			
			throw new System.ArithmeticException("Result unknown for B(" + k + ")");
		}
		
		public virtual double a1(AbstractParticle particle)
		{
			
			switch (particle.index)
			{
				case AbstractFormula.E_MINUS:  return 35;
				case AbstractFormula.E_ZERO:  return 34;
				case AbstractFormula.MU:  return 1;
				case AbstractFormula.PI_CHARGE:  return 25;
				case AbstractFormula.PI_ZERO:  return 22;
				case AbstractFormula.ETA:  return 28;
				case AbstractFormula.K_CHARGE:  return 16;
				case AbstractFormula.K_ZERO:  return 22;
				case AbstractFormula.P:  return 0;
				case AbstractFormula.N:  return 0;
				case AbstractFormula.LAMBDA:  return 13;
				case AbstractFormula.SIGMA_PLUS:  return 21;
				case AbstractFormula.SIGMA_MINUS:  return 21;
				case AbstractFormula.SIGMA_ZERO:  return 21;
				case AbstractFormula.XI_CHARGE:  return 26;
				case AbstractFormula.XI_ZERO:  return 26;
				case AbstractFormula.OMEGA_CHARGE:  return 47;
				case AbstractFormula.DELTA_PLUSPLUS:  return 23;
				case AbstractFormula.DELTA_PLUS:  return 23;
				case AbstractFormula.DELTA_MINUS:  return 23;
				case AbstractFormula.DELTA_ZERO:  return 21;
				}
			
			//UPGRADE_TODO: The equivalent in .NET for method 'java.lang.Object.toString' may return a different value. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1043"'
			throw new System.ArithmeticException("Result unknown for a1(" + particle + ")");
		}
		
		public virtual double a2(AbstractParticle particle)
		{
			
			switch (particle.index)
			{
				case AbstractFormula.E_MINUS:  return 11;
				case AbstractFormula.E_ZERO:  return 28;
				case AbstractFormula.MU:  return 23;
				case AbstractFormula.PI_CHARGE:  return 0;
				case AbstractFormula.PI_ZERO:  return 2;
				case AbstractFormula.ETA:  return 33;
				case AbstractFormula.K_CHARGE:  return 31;
				case AbstractFormula.K_ZERO:  return 17;
				case AbstractFormula.P:  return 23;
				case AbstractFormula.N:  return 36;
				case AbstractFormula.LAMBDA:  return 45;
				case AbstractFormula.SIGMA_PLUS:  return 30;
				case AbstractFormula.SIGMA_MINUS:  return 47;
				case AbstractFormula.SIGMA_ZERO:  return 46;
				case AbstractFormula.XI_CHARGE:  return 25;
				case AbstractFormula.XI_ZERO:  return 22;
				case AbstractFormula.OMEGA_CHARGE:  return 3;
				case AbstractFormula.DELTA_PLUSPLUS:  return 27;
				case AbstractFormula.DELTA_PLUS:  return 22;
				case AbstractFormula.DELTA_MINUS:  return 39;
				case AbstractFormula.DELTA_ZERO:  return 27;
				}
			throw new System.ArithmeticException("Result unknown for a2(" + particle + ")");
		}
		
		public virtual double a3(AbstractParticle particle)
		{
			
			switch (particle.index)
			{
				case AbstractFormula.E_MINUS:  return 89.96774158;
				case AbstractFormula.E_ZERO:  return 77.11059862;
				case AbstractFormula.MU:  return 7.26891022;
				case AbstractFormula.PI_CHARGE:  return 95.62488526;
				case AbstractFormula.PI_ZERO:  return - 0.03225806;
				case AbstractFormula.ETA:  return 48.65020426;
				case AbstractFormula.K_CHARGE:  return 7.26891022;
				case AbstractFormula.K_ZERO:  return 98.29474138;
				case AbstractFormula.P:  return 84.22944059;
				case AbstractFormula.N:  return 101.15000035;
				case AbstractFormula.LAMBDA:  return - 0.033333333;
				case AbstractFormula.SIGMA_PLUS:  return 26.15371691;
				case AbstractFormula.SIGMA_MINUS:  return 94.49556347;
				case AbstractFormula.SIGMA_ZERO:  return 83.86257747;
				case AbstractFormula.XI_CHARGE:  return 15.61504747;
				case AbstractFormula.XI_ZERO:  return 71.62409771;
				case AbstractFormula.OMEGA_CHARGE:  return 69.73881899;
				case AbstractFormula.DELTA_PLUSPLUS:  return 82.92386515;
				case AbstractFormula.DELTA_PLUS:  return 22.64335811;
				case AbstractFormula.DELTA_MINUS:  return 93.76289283;
				case AbstractFormula.DELTA_ZERO:  return 69.73881899;
				}
			throw new System.ArithmeticException("Result unknown for a3(" + particle + ")");
		}
	}
}