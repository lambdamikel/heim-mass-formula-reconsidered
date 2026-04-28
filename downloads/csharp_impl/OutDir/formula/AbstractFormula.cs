using System;
namespace formula
{
	
	// Version b0.07
	
	/*
	* Abstract formula class.
	*
	* NOTE: extend this class to test an alternative formula then the 
	*       rigid 1982 or 1989 formulas
	*/
	public abstract class AbstractFormula
	{
		public abstract QN QuantumNumberCalculator{get;}
		public abstract SelfCouplingFunction SelfCouplingFunction{get;}
		
		private static readonly double KILO_PER_UNIT = 1.66053886 * System.Math.Pow(10, - 27);
		private const double MEV_PER_UNIT = 931.494043;
		
		public const int NUM_PARTICLES = 21;
		
		public const int E_MINUS = 0;
		public const int E_ZERO = 1;
		public const int MU = 2;
		public const int PI_CHARGE = 3;
		public const int PI_ZERO = 4;
		public const int ETA = 5;
		public const int K_CHARGE = 6;
		public const int K_ZERO = 7;
		public const int P = 8;
		public const int N = 9;
		public const int LAMBDA = 10;
		public const int SIGMA_PLUS = 11;
		public const int SIGMA_MINUS = 12;
		public const int SIGMA_ZERO = 13;
		public const int XI_CHARGE = 14;
		public const int XI_ZERO = 15;
		public const int OMEGA_CHARGE = 16;
		public const int DELTA_PLUSPLUS = 17;
		public const int DELTA_PLUS = 18;
		public const int DELTA_MINUS = 19;
		public const int DELTA_ZERO = 20;
		
		protected internal AbstractParticle e_minus;
		protected internal AbstractParticle e_zero;
		protected internal AbstractParticle mu;
		protected internal AbstractParticle pi_charge;
		protected internal AbstractParticle pi_zero;
		protected internal AbstractParticle eta;
		protected internal AbstractParticle k_charge;
		protected internal AbstractParticle k_zero;
		protected internal AbstractParticle p;
		protected internal AbstractParticle n;
		protected internal AbstractParticle lambda;
		protected internal AbstractParticle sigma_plus;
		protected internal AbstractParticle sigma_minus;
		protected internal AbstractParticle sigma_zero;
		protected internal AbstractParticle xi_charge;
		protected internal AbstractParticle xi_zero;
		protected internal AbstractParticle omega_charge;
		protected internal AbstractParticle delta_plusplus;
		protected internal AbstractParticle delta_plus;
		protected internal AbstractParticle delta_minus;
		protected internal AbstractParticle delta_zero;
		
		public virtual AbstractParticle getParticle(int particle_index)
		{
			
			switch (particle_index)
			{
				case E_MINUS:  return e_minus;
				case E_ZERO:  return e_zero;
				case MU:  return mu;
				case PI_CHARGE:  return pi_charge;
				case PI_ZERO:  return pi_zero;
				case ETA:  return eta;
				case K_CHARGE:  return k_charge;
				case K_ZERO:  return k_zero;
				case P:  return p;
				case N:  return n;
				case LAMBDA:  return lambda;
				case SIGMA_PLUS:  return sigma_plus;
				case SIGMA_MINUS:  return sigma_minus;
				case SIGMA_ZERO:  return sigma_zero;
				case XI_CHARGE:  return xi_charge;
				case XI_ZERO:  return xi_zero;
				case OMEGA_CHARGE:  return omega_charge;
				case DELTA_PLUSPLUS:  return delta_plusplus;
				case DELTA_PLUS:  return delta_plus;
				case DELTA_MINUS:  return delta_minus;
				case DELTA_ZERO:  return delta_zero;
				
				default:  return null;
			}
		}
		
		public virtual int getParticleIndex(AbstractParticle particle)
		{
			for (int i = 0; i < NUM_PARTICLES; i++)
			{
				try
				{
					if (particle.Equals(getParticle(i)))
						return i;
				}
				catch (System.NullReferenceException e)
				{
					/* if it's null it's definitly 
					not the one we're looking for */
				}
			}
			
			throw new System.Exception("Unknown Particle");
		}
		
		
		public virtual double massEquation(AbstractParticle particle)
		{
			// Conversion to MeV
			return (M(particle) / KILO_PER_UNIT) * MEV_PER_UNIT;
		}
		
		public abstract double M(AbstractParticle particle);
	}
}