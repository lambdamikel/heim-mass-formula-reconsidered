// Version b0.07
using System;
using AbstractFormula = formula.AbstractFormula;
using AbstractParticle = formula.AbstractParticle;
namespace formula.experimental
{
	
	/*
	* Dummy Implementation, presents Selected Results
	*/
	public class Formula:AbstractFormula
	{
		override public formula.QN QuantumNumberCalculator
		{
			get
			{
				
				throw new System.Exception("There are no experimental results regarding the quantum number equations");
			}
			
		}
		override public formula.SelfCouplingFunction SelfCouplingFunction
		{
			get
			{
				
				throw new System.Exception("There are no experimental results regarding the selfcoupling function");
			}
			
		}
		
		public Formula()
		{
		}
		
		public override double M(AbstractParticle particle)
		{
			
			switch (particle.index)
			{
				case AbstractFormula.E_MINUS:  return 0.51099891844;	
				//case AbstractFormula.E_ZERO: return 0.51617049; This has not been experimentaly verified
				case AbstractFormula.MU:  return 105.658389;
				case AbstractFormula.PI_CHARGE:  return 139.57018;
				case AbstractFormula.PI_ZERO:  return 134.9766;
				case AbstractFormula.ETA:  return 547.30;
				case AbstractFormula.K_CHARGE:  return 493.677;
				case AbstractFormula.K_ZERO:  return 497.672;
				case AbstractFormula.P:  return 938.27231;
				case AbstractFormula.N:  return 939.56563;
				case AbstractFormula.LAMBDA:  return 1115.683;
				case AbstractFormula.SIGMA_PLUS:  return 1189.37;
				case AbstractFormula.SIGMA_MINUS:  return 1197.449;
				case AbstractFormula.SIGMA_ZERO:  return 1192.642;
				case AbstractFormula.XI_CHARGE:  return 1321.32;
				case AbstractFormula.XI_ZERO:  return 1314.9;
				case AbstractFormula.OMEGA_CHARGE:  return 1672.45;
				case AbstractFormula.DELTA_PLUSPLUS:  return 1232;
				case AbstractFormula.DELTA_PLUS:  return 1232;
				case AbstractFormula.DELTA_MINUS:  return 1232;
				case AbstractFormula.DELTA_ZERO:  return 1232;
				}
			throw new System.Exception("Result unknown for M(" + particle + ")");
		}
	}
}