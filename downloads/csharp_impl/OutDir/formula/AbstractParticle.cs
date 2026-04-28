using System;
namespace formula
{
	
	// Version b0.07
	
	/*
	* Objects of this class represent particles. Particles are uniquely 
	* given by the parameters k, P, Q, kappa and x. From these values the 
	* structure distributor C, the electrical charge quantum number qx and 
	* the electrical charge amount q is calculated.
	*
	* NOTE: The value x for particles can be choosen amoung those values x
	* which fulfill 0 <= x <= P for any combination of the 4 other input 
	* values.
	*
	* NOTE: This is an abstract class which must be extended by the three
	*       abstract methods. This is because there are different 
	*       interpretations of C, qx and q in different formulas 
	*
	* NOTE Problems :
	*
	*    1) Should Time-helicity be true (+1) or false (-1)? see p2 1989 
	*       note.
	*/
	public abstract class AbstractParticle : System.Collections.IComparer
	{
		protected internal abstract int ChargeAmount{get;}
		
		// Time helicity - p3 1982 (seems it's supposed to be true ie. '+1'?)
		public const bool TIME_HELICITY = true;
		public int k;
		
		// Double Isospin
		public int P;
		
		// Double Space-spin
		public int Q;
		
		// Doblet Number
		public int kappa;
		
		// Component of the Isospin-multiplet
		public int x;
		
		// Structure Distributor
		public int C;
		
		// Quantum Number (Electrical Charge)
		public int qx;
		
		// Electrical Charge Amount
		public int q;
		
		// n, m, p and sigma
		public int n;
		public int m;
		public int p;
		public int sigma;
		
		// The ParticleIndex, type of the particle
		public int index;
		
		// A name for the particle
		public System.String name;
		
		public AbstractParticle(System.String name, int index, int k, int P, int Q, int kappa, int x)
		{
			// Make sure input parameters are ligit
			if (checkParameterConstraints(k, P, Q, kappa, x))
			{
				throw new System.Exception("Paramter Constraints Violated");
			}
			
			this.index = index;
			this.name = name;
			
			this.k = k;
			this.P = P;
			this.Q = Q;
			this.kappa = kappa;
			this.x = x;
			
			this.C = getStructureDistributor(TIME_HELICITY);
			this.qx = getQuantumNumber(TIME_HELICITY);
			this.q = ChargeAmount;
			
			try
			{
				this.n = get_n();
				this.m = get_m();
				this.p = get_p();
				this.sigma = get_sigma();
			}
			catch (System.Exception e)
			{
				System.Console.Out.WriteLine("one or more of n, m, p, sigma has not been initialized: ");
				throw e;
			}
		}
		
		protected internal abstract int getStructureDistributor(bool timeHelicity);
		protected internal abstract int getQuantumNumber(bool timeHelicity);
		
		protected internal abstract int get_n();
		protected internal abstract int get_m();
		protected internal abstract int get_p();
		protected internal abstract int get_sigma();
		
		// Since noone can seem to figure out W atm. this simply returns
		// values given in Selected Results
		protected internal virtual double W()
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
		
		/*
		* Lets make sure that constructor parameters are ligit
		* NOTE: Since the global vars are final they cannot be
		* changed once they pass this check
		*/
		private bool checkParameterConstraints(int k, int P, int Q, int kappa, int x)
		{
			bool volation = false;
			
			if (k < 1 || 2 < k)
				volation = true;
			
			if (P < 0 || 3 < P)
				volation = true;
			
			if (Q < 0 || 3 < Q)
				volation = true;
			
			if (kappa < 0 || 1 < kappa)
				volation = true;
			
			if (x < 0 || P < x)
				volation = true;
			
			return volation;
		}
		
		public override System.String ToString()
		{	
			System.String type = "";
			if (k == 1 && Q == 1)
			{		
				type = "Lepton";
			}
			else if (k == 1 && Q == 0)
			{	
				type = "Messon";
			}
			else
			{	
				type = "Baryon";
			}
			
			return type + " " + name;
		}
		
		public virtual int Compare(System.Object o1, System.Object o2)
		{
			AbstractParticle p1 = (AbstractParticle) o1;
			AbstractParticle p2 = (AbstractParticle) o2;
			
			if (p1.k > p2.k)
			{		
				return 1;
			}
			else if (p1.k < p2.k)
			{	
				return - 1;
			}
			else if (p1.Q > p2.Q)
			{	
				return 1;
			}
			else if (p1.Q < p2.Q)
			{	
				return - 1;
			}
			else
			{	
				return 0;
			}
		}
		
		public  virtual bool Equals(System.Object o)
		{
			AbstractParticle p = (AbstractParticle) o;
			
			if (p.k == this.k && p.P == this.P && p.Q == this.Q && p.kappa == this.kappa && p.x == this.x)
				return true;
			
			return false;
		}
	}
}