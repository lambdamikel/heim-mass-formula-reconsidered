// Version b0.07
using System;
namespace formula
{
	
	/*
	* This interface deals with all equations related to determining the value of the so 
	* called 'self-couplings function' phi given as EQUATION B7 (p12, 1989 formula).
	* It is needed to evaluate EQUATION B5 (p11, 1989 formula).
	* 
	* The main sub-equations of the self-couplings function are EQUATIONS B22-B28 
	* (p13, 1989 formula) as well as U given just below phi EQUATION B7. Also a1,
	* a2, and a3 EQUATIONS B29-B31 (p14, 1989 formula) are needed to evaluate x
	* EQUATION B27 (p13, 1989 formula).
	*
	* NOTE: This is simply an interface, the implementation can be found in the relevant 
	*       package
	*/
	public interface SelfCouplingFunction
		{
			double phi(AbstractParticle particle);
			double W(AbstractParticle particle);
			double A(double k);
			double H(double k);
			double B(double k);
			double a1(AbstractParticle particle);
			double a2(AbstractParticle particle);
			double a3(AbstractParticle particle);
		}
}