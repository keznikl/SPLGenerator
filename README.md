Generator of benchmark SPL formulas
===================================

##Usage:
	
	python main.py [min_vars min_clauses] [random seed]> [your favorite SAT solver]

Generates a propositional skeletons of a single SPL-specific benchmark formula in the DIMACS format.

All information is printed on the `sys.stderr` output. 
The formula itself is printed on the standard output.

##Details:	
Contains tools for manipulating propositional formulas (including transformation to CNF via De-Morgan laws and Tseitin's algorithm)


