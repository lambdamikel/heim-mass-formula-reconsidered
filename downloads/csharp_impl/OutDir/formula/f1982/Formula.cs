// Version b0.07
using System;
using AbstractFormula = formula.AbstractFormula;
using AbstractParticle = formula.AbstractParticle;
using Constants = formula.Constants;
namespace formula.f1982
{
	
	/*
	* Implementation of 1982 formula.
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
				
				throw new System.Exception("There is no SelfCouplingFunction in formula 1982.");
			}
			
		}
		
		public Formula()
		{
			
			try
			{
				// NOTE: parameters 'new Particle(particleIndex, k, P, Q, kappa, x)'
				
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
		
		/*
		* The Mass Equation, M - EQUATION XII (p5, 1982 formula)
		*/
		public override double M(AbstractParticle particle)
		{
			// Result of mass equation (in kg)
			return (Constants.massElement * Constants.alphaPlus * (MainFunctions.G(particle) + MainFunctions.S(particle) + MainFunctions.F(particle) + MainFunctions.phi(particle)));
		}
	}
}