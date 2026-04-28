// Version b0.07
using System;
using AbstractFormula = formula.AbstractFormula;
using AbstractParticle = formula.AbstractParticle;
namespace formula.dummyHG
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
				
				return QN.Instance;
			}
			
		}
		override public formula.SelfCouplingFunction SelfCouplingFunction
		{
			get
			{
				
				return formula.dummyHG.SelfCouplingFunction.Instance;
			}
			
		}
		
		public Formula()
		{
			
			try
			{
				e_minus = new Particle("e(minus)", E_MINUS, 1, 1, 1, 0, 1);
				e_zero = new Particle("e(zero)", E_ZERO, 1, 1, 1, 0, 0);
				
				mu = new Particle("mu", MU, 1, 1, 1, 1, 0); // x: 0-1?
				
				pi_charge = new Particle("pi(charge)", PI_CHARGE, 1, 2, 0, 0, 0); // x: 0-2?
				pi_zero = new Particle("pi(zero)", PI_ZERO, 1, 2, 0, 0, 1); // x: 0-2?
				
				eta = new Particle("eta", ETA, 1, 0, 0, 0, 0);
				
				k_charge = new Particle("k(charge)", K_CHARGE, 1, 1, 0, 1, 0); // x: 0-1?
				k_zero = new Particle("k(zero)", K_ZERO, 1, 1, 0, 1, 1); // x: 0-1?
				
				p = new Particle("proton", P, 2, 1, 1, 0, 0); // x: 0-1?
				n = new Particle("neutron", N, 2, 1, 1, 0, 1); // x: 0-1?
				
				lambda = new Particle("lambda", LAMBDA, 2, 0, 1, 0, 0);
				
				sigma_plus = new Particle("sigma(plus)", SIGMA_PLUS, 2, 2, 1, 0, 0); // x: 0-2?
				sigma_minus = new Particle("sigma(minus)", SIGMA_MINUS, 2, 2, 1, 0, 2); // x: 0-2?
				sigma_zero = new Particle("sigma(zero)", SIGMA_ZERO, 2, 2, 1, 0, 1); // x: 0-2?
				
				xi_charge = new Particle("xi(charge)", XI_CHARGE, 2, 1, 1, 1, 1); // x: 0-1?
				xi_zero = new Particle("xi(zero)", XI_ZERO, 2, 1, 1, 1, 0); // x: 0-1?
				
				omega_charge = new Particle("omega(charge)", OMEGA_CHARGE, 2, 0, 3, 0, 0);
				
				delta_plusplus = new Particle("delta(plusplus)", DELTA_PLUSPLUS, 2, 3, 3, 0, 0); // x: 0-3?
				delta_plus = new Particle("delta(plus)", DELTA_PLUS, 2, 3, 3, 0, 1); // x: 0-3?
				delta_minus = new Particle("delta(minus)", DELTA_MINUS, 2, 3, 3, 0, 3); // x: 0-3?
				delta_zero = new Particle("delta(zero)", DELTA_ZERO, 2, 3, 3, 0, 2); // x: 0-3?
			}
			catch (System.Exception e)
			{
				System.Console.Out.WriteLine("Particle Construction error: " + e);
			}
		}
		
		public override double M(AbstractParticle particle)
		{
			
			switch (particle.index)
			{
				case AbstractFormula.E_MINUS:  return 0.51100343;
				case AbstractFormula.E_ZERO:  return 0.51617049;
				case AbstractFormula.MU:  return 105.65948493;
				case AbstractFormula.PI_CHARGE:  return 139.56837088;
				case AbstractFormula.PI_ZERO:  return 134.96004114;
				case AbstractFormula.ETA:  return 548.80002432;
				case AbstractFormula.K_CHARGE:  return 493.71425074;
				case AbstractFormula.K_ZERO:  return 497.72299959;
				case AbstractFormula.P:  return 938.27959246;
				case AbstractFormula.N:  return 939.57336128;
				case AbstractFormula.LAMBDA:  return 1115.59979064;
				case AbstractFormula.SIGMA_PLUS:  return 1189.37409717;
				case AbstractFormula.SIGMA_MINUS:  return 1197.30443002;
				case AbstractFormula.SIGMA_ZERO:  return 1192.47794854;
				case AbstractFormula.XI_CHARGE:  return 1321.29326013;
				case AbstractFormula.XI_ZERO:  return 1314.90206200;
				case AbstractFormula.OMEGA_CHARGE:  return 1672.17518902;
				case AbstractFormula.DELTA_PLUSPLUS:  return 1232.91663788;
				case AbstractFormula.DELTA_PLUS:  return 1234.60981181;
				case AbstractFormula.DELTA_MINUS:  return 1237.06132359;
				case AbstractFormula.DELTA_ZERO:  return 1229.99529979;
				}
			throw new System.ArithmeticException("Result unknown for M(" + particle + ")");
		}
	}
}