// Version b0.07

//import formula.*;
using System;
using AbstractFormula = formula.AbstractFormula;
using AbstractParticle = formula.AbstractParticle;
using Constants = formula.Constants;
using QN = formula.QN;
using SelfCouplingFunction = formula.SelfCouplingFunction;

/*
* This class is used to check results of equations to known results.
* If values differ by more then 6 figures they are reported as
* incorrect and the result value, tabel value and difference is
* displayed. If the case is correct 'GOOD' is displayed together
* with the result value.
*/
public class HeimUnit
{
	
	// This is the limit used to determine correct results
	
	private static readonly double limit;
	
	private static int output_fmt = 0;
	
	[STAThread]
	public static int  Main(System.String[] args)
	{
		
		// interpret the command line option(s), if any
		for (int i = 0; i < args.Length; i++)
		{
			if (args[i].Equals("-csv"))
			{
				output_fmt = 1;
			}
		}
		
		// Setup formulas
		AbstractFormula formula1989 = new formula.f1989.Formula();
		AbstractFormula formula1982 = new formula.f1982.Formula();
		AbstractFormula formulaHG = new formula.HeimGroup.Formula();
		
		// Dummy formula (returns results given in 
		// the paper Selected Results)
		AbstractFormula dummyHG = new formula.dummyHG.Formula();
		
		// Experimental results
		AbstractFormula experimental = new formula.experimental.Formula();
		

		//Create Output
		particle_Tests(formulaHG, dummyHG, experimental);
		
		Console.WriteLine("Press ENTER to close... ");
		String name = Console.ReadLine();
		return 1;
	}
	
	public static void  alpha_Tests()
	{
		
		unitCase(Constants.alphaPlus, 0.01832211, "Alpha Plus");
		unitCase(Constants.alphaMinus, 0.00812835, "Alpha Minus");
		
		unitCase(Constants.altAlphaPlus, 0.01832211, "Alpha Plus Old");
		unitCase(Constants.altAlphaMinus, 0.00812835, "Alpha Minus Old");
	}
	
	public static void  etaAndTheta_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			QN qnC1 = formula.QuantumNumberCalculator;
			QN qnC2 = dummy.QuantumNumberCalculator;
			
			unitCase(Constants.eta, 0.98998964, "Constant eta");
			
			unitCase(qnC1.eta(0, 1), qnC2.eta(0, 1), "eta(0,1) = eta");
			unitCase(qnC1.eta(1, 1), qnC2.eta(1, 1), "eta(1,1)");
			unitCase(qnC1.eta(2, 1), qnC2.eta(2, 1), "eta(2,1)");
			unitCase(qnC1.eta(2, 2), qnC2.eta(2, 2), "eta(2,2)");
			
			unitCase(Constants.theta, 7.93991266, "Constant theta");
			
			unitCase(qnC1.theta(0, 1), qnC2.theta(0, 1), "theta(0,1) = theta");
			unitCase(qnC1.theta(1, 1), qnC2.theta(1, 1), "theta(1,1)");
			unitCase(qnC1.theta(2, 1), qnC2.theta(2, 1), "theta(2,1)");
			unitCase(qnC1.theta(2, 2), qnC2.theta(2, 2), "theta(2,2)");
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  quantumNumber_equationQ_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			QN qnC1 = formula.QuantumNumberCalculator;
			QN qnC2 = dummy.QuantumNumberCalculator;
			
			unitCase(qnC1.Q1(1), qnC2.Q1(1), "Q1(1)");
			unitCase(qnC1.Q2(1), qnC2.Q2(1), "Q2(1)");
			unitCase(qnC1.Q3(1), qnC2.Q3(1), "Q3(1)");
			unitCase(qnC1.Q4(1), qnC2.Q4(1), "Q4(1)");
			
			unitCase(qnC1.Q1(2), qnC2.Q1(2), "Q1(2)");
			unitCase(qnC1.Q2(2), qnC2.Q2(2), "Q2(2)");
			unitCase(qnC1.Q3(2), qnC2.Q3(2), "Q3(2)");
			unitCase(qnC1.Q4(2), qnC2.Q4(2), "Q4(2)");
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  quantumNumber_equationN_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			QN qnC1 = formula.QuantumNumberCalculator;
			QN qnC2 = dummy.QuantumNumberCalculator;
			
			unitCase(qnC1.N1(1, 1), qnC2.N1(1, 1), "N1(1,1)");
			unitCase(qnC1.N1(1, 0), qnC2.N1(1, 0), "N1(1,0)");
			unitCase(qnC1.N1(2, 1), qnC2.N1(2, 1), "N1(2,1)");
			unitCase(qnC1.N1(2, 0), qnC2.N1(2, 0), "N1(2,0)");
			unitCase(qnC1.N1(2, 2), qnC2.N1(2, 2), "N1(2,2)");
			
			unitCase(qnC1.N2(1, 1), qnC2.N2(1, 1), "N2(1,1)");
			unitCase(qnC1.N2(1, 0), qnC2.N2(1, 0), "N2(1,0)");
			unitCase(qnC1.N2(2, 1), qnC2.N2(2, 1), "N2(2,1)");
			unitCase(qnC1.N2(2, 0), qnC2.N2(2, 0), "N2(2,0)");
			unitCase(qnC1.N2(2, 2), qnC2.N2(2, 2), "N2(2,2)");
			
			unitCase(qnC1.N3(1, 1), qnC2.N3(1, 1), "N3(1,1)");
			unitCase(qnC1.N3(1, 0), qnC2.N3(1, 0), "N3(1,0)");
			unitCase(qnC1.N3(2, 1), qnC2.N3(2, 1), "N3(2,1)");
			unitCase(qnC1.N3(2, 0), qnC2.N3(2, 0), "N3(2,0)");
			unitCase(qnC1.N3(2, 2), qnC2.N3(2, 2), "N3(2,2)");
			
			unitCase(qnC1.N4(1, 1), qnC2.N4(1, 1), "N4(1,1)");
			unitCase(qnC1.N4(1, 0), qnC2.N4(1, 0), "N4(1,0)");
			unitCase(qnC1.N4(2, 1), qnC2.N4(2, 1), "N4(2,1)");
			unitCase(qnC1.N4(2, 0), qnC2.N4(2, 0), "N4(2,0)");
			unitCase(qnC1.N4(2, 2), qnC2.N4(2, 2), "N4(2,2)");
			
			unitCase(qnC1.N5(1, 1), qnC2.N5(1, 1), "N5(1,1)");
			unitCase(qnC1.N5(1, 0), qnC2.N5(1, 0), "N5(1,0)");
			unitCase(qnC1.N5(2, 1), qnC2.N5(2, 1), "N5(2,1)");
			unitCase(qnC1.N5(2, 0), qnC2.N5(2, 0), "N5(2,0)");
			unitCase(qnC1.N5(2, 2), qnC2.N5(2, 2), "N5(2,2)");
			
			unitCase(qnC1.N6(1, 1), qnC2.N6(1, 1), "N6(1,1)");
			unitCase(qnC1.N6(1, 0), qnC2.N6(1, 0), "N6(1,0)");
			unitCase(qnC1.N6(2, 1), qnC2.N6(2, 1), "N6(2,1)");
			unitCase(qnC1.N6(2, 0), qnC2.N6(2, 0), "N6(2,0)");
			unitCase(qnC1.N6(2, 2), qnC2.N6(2, 2), "N6(2,2)");
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  selfCouplingsFunction_BandH_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			
			SelfCouplingFunction scf1 = formula.SelfCouplingFunction;
			SelfCouplingFunction scf2 = dummy.SelfCouplingFunction;
			
			unitCase(scf1.B(1), scf2.B(1), "B(1)");
			unitCase(scf1.B(2), scf2.B(2), "B(2)");
			
			unitCase(scf1.H(1), scf2.H(1), "H(1)");
			unitCase(scf1.H(2), scf2.H(2), "H(2)");
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  selfCouplingsFunction_A_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			
			SelfCouplingFunction scf1 = formula.SelfCouplingFunction;
			SelfCouplingFunction scf2 = dummy.SelfCouplingFunction;
			
			unitCase(scf1.A(1), scf2.A(1), "A(1)");
			unitCase(scf1.A(2), scf2.A(1), "A(2)");
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  selfCouplingsFunction_a1_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			
			SelfCouplingFunction scf1 = formula.SelfCouplingFunction;
			SelfCouplingFunction scf2 = dummy.SelfCouplingFunction;
			
			for (int i = 0; i < AbstractFormula.NUM_PARTICLES; i++)
			{
				
				//UPGRADE_TODO: The equivalent in .NET for method 'java.lang.Object.toString' may return a different value. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1043"'
				unitCase(scf1.a1(formula.getParticle(i)), scf2.a1(dummy.getParticle(i)), "a1 " + formula.getParticle(i));
			}
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  selfCouplingsFunction_a2_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			
			SelfCouplingFunction scf1 = formula.SelfCouplingFunction;
			SelfCouplingFunction scf2 = dummy.SelfCouplingFunction;
			
			for (int i = 0; i < AbstractFormula.NUM_PARTICLES; i++)
			{
				
				//UPGRADE_TODO: The equivalent in .NET for method 'java.lang.Object.toString' may return a different value. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1043"'
				unitCase(scf1.a2(formula.getParticle(i)), scf2.a2(dummy.getParticle(i)), "a2 " + formula.getParticle(i));
			}
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  selfCouplingsFunction_a3_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			
			SelfCouplingFunction scf1 = formula.SelfCouplingFunction;
			SelfCouplingFunction scf2 = dummy.SelfCouplingFunction;
			
			for (int i = 0; i < AbstractFormula.NUM_PARTICLES; i++)
			{
				
				//UPGRADE_TODO: The equivalent in .NET for method 'java.lang.Object.toString' may return a different value. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1043"'
				unitCase(scf1.a3(formula.getParticle(i)), scf2.a3(dummy.getParticle(i)), "a3 " + formula.getParticle(i));
			}
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  selfCouplingsFunction_W_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			
			SelfCouplingFunction scf1 = formula.SelfCouplingFunction;
			SelfCouplingFunction scf2 = dummy.SelfCouplingFunction;
			
			for (int i = 0; i < AbstractFormula.NUM_PARTICLES; i++)
			{
				
				//UPGRADE_TODO: The equivalent in .NET for method 'java.lang.Object.toString' may return a different value. 'ms-help://MS.VSCC.2003/commoner/redir/redirect.htm?keyword="jlca1043"'
				unitCase(scf1.W(formula.getParticle(i)), scf2.W(dummy.getParticle(i)), "W " + formula.getParticle(i));
			}
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  selfCouplingsFunction_phi_Tests(AbstractFormula formula, AbstractFormula dummy)
	{
		
		try
		{
			
			SelfCouplingFunction scf1 = formula.SelfCouplingFunction;
			SelfCouplingFunction scf2 = dummy.SelfCouplingFunction;
			
			for (int i = 0; i < AbstractFormula.NUM_PARTICLES; i++)
			{	
				unitCase(scf1.phi(formula.getParticle(i)), scf2.phi(dummy.getParticle(i)), "phi " + formula.getParticle(i));
			}
		}
		catch (System.Exception e)
		{
			SupportClass.WriteStackTrace(e, Console.Error);
		}
	}
	
	public static void  massEquation_Tests(AbstractFormula formula, AbstractFormula dummy, AbstractFormula experimental)
	{
		
		double result;
		double table;
		double exp;
		System.String equation;
		
		for (int i = 0; i < AbstractFormula.NUM_PARTICLES; i++)
		{
			
			try
			{
				result = formula.massEquation(formula.getParticle(i));
				table = dummy.M(dummy.getParticle(i));
				equation = "Mass " + formula.getParticle(i);
				
				try
				{
					exp = experimental.M(dummy.getParticle(i));
					unitCase(result, table, exp, equation);
				}
				catch (System.Exception e)
				{
					unitCase(result, table, equation);
				}
			}
			catch (System.Exception e)
			{
				SupportClass.WriteStackTrace(e, Console.Error);
			}
		}
	}
	
	
	public static void  particle_Tests(AbstractFormula formula, AbstractFormula dummy, AbstractFormula experimental)
	{
		
		double result;
		double table;
		double exp;
		System.String equation;
		
		for (int i = 0; i < AbstractFormula.NUM_PARTICLES; i++)
		{
			
	
			unitCase(formula.getParticle(i).C, dummy.getParticle(i).C, "C " + formula.getParticle(i));
			unitCase(formula.getParticle(i).qx, dummy.getParticle(i).qx, "qx " + formula.getParticle(i));
			unitCase(formula.getParticle(i).q, dummy.getParticle(i).q, "q " + formula.getParticle(i));
			unitCase(formula.getParticle(i).n, dummy.getParticle(i).n, "n " + formula.getParticle(i));
			unitCase(formula.getParticle(i).m, dummy.getParticle(i).m, "m " + formula.getParticle(i));
			unitCase(formula.getParticle(i).p, dummy.getParticle(i).p, "p " + formula.getParticle(i));
			unitCase(formula.getParticle(i).sigma, dummy.getParticle(i).sigma, "sigma " + formula.getParticle(i));
			
			try
			{
				result = formula.massEquation(formula.getParticle(i));
				table = dummy.M(dummy.getParticle(i));
				equation = "Mass " + formula.getParticle(i);
				
				try
				{
					exp = experimental.M(dummy.getParticle(i));
					unitCase(result, table, exp, equation);
				}
				catch (System.Exception e)
				{
					unitCase(result, table, equation);
				}
			}
			catch (System.Exception e)
			{
				SupportClass.WriteStackTrace(e, Console.Error);
			}
		}
	}
	
	/*
	* If values differ by more then 6 figures they are reported as
	* incorrect and the result value, tabel value and difference is
	* displayed. If the case is correct 'GOOD' is displayed together
	* with the result value.
	*/
	public static void  unitCase(double result, double table, System.String equation)
	{
		
		double difference = System.Math.Abs(result - table);
		
		if (output_fmt == 1)
		{
			unitCaseCSV(result, table, "", difference, equation);
			return ;
		}
		
		if (difference < limit)
		{
			System.Console.Out.WriteLine();
			System.Console.Out.WriteLine("=====> " + equation + " GOOD");
			System.Console.Out.WriteLine("result: " + result);
			System.Console.Out.WriteLine();
		}
		else
		{
			System.Console.Out.WriteLine();
			System.Console.WriteLine("=====> " + equation + " INCORRECT!!!");
			System.Console.Out.WriteLine("result: " + result);
			System.Console.Out.WriteLine(" table: " + table);
			System.Console.Out.WriteLine("  diff: " + difference);
			System.Console.Out.WriteLine();
		}
	}
	
	public static void  unitCase(double result, double table, double experimental, System.String equation)
	{
		
		double difference = System.Math.Abs(result - table);
		double diffHeimGroup = System.Math.Abs(table - experimental);
		
		if (output_fmt == 1)
		{
			unitCaseCSV(result, table, "" + experimental, difference, equation);
			return ;
		}
		
		if (difference < limit)
		{
			System.Console.Out.WriteLine();
			System.Console.Out.WriteLine("=====> " + equation + " GOOD (TABLE)");
			System.Console.Out.WriteLine("result: " + result);
			System.Console.Out.WriteLine();
		}
		else
		{
			System.Console.Out.WriteLine();
			System.Console.Out.WriteLine("=====> " + equation + " INCORRECT (TABLE)!!!");
			System.Console.Out.WriteLine("  result: " + result);
			System.Console.Out.WriteLine("   table: " + table);
			System.Console.Out.WriteLine("    diff: " + difference);
			System.Console.Out.WriteLine("(HG)diff: " + diffHeimGroup);
			System.Console.Out.WriteLine();
		}
	}
	
	public static void  unitCaseCSV(double result, double table, System.String experimental, double difference, System.String equation)
	{
		System.Console.Out.Write("\"" + equation + "\",");
		System.Console.Out.Write((difference < limit)?"Good,":"INCORRECT!!!,");
		System.Console.Out.WriteLine(result + "," + table + "," + experimental);
	}
	static HeimUnit()
	{
		limit = System.Math.Pow(10, - 6);
	}
}