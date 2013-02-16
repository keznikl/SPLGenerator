"""
Module for generating a single SPL-specific benchmark formula in the DIMACS format.

Usage:
main.py min_vars min_clauses [random seed]

All information is printed on the sys.stderr output. 
The formula itself is printed on the standard output.

The script proceeds as follows:
    - random SPL-formula skeleton is generated using the generators module 
      (with the required number of variables and clauses)
    - the formula is converted to CNF using De-Morgan laws 
      (we prefer equivalent formulas rather than equisatisfiable ones; 
      however, Tseitin's algorighm implementation is available)
    - The CNF formula is converted in the DIMACS format
    
@author: Keznikl
"""

from random import seed, randint, choice, random
from formula import Conjunction, Visitor
from generators import several_perf_posibilites_unknown_cause, several_perf_posibilites_use_fastest
from dimacs import DimacsFormatVisitor
import sys
import datetime 



###############################################################################
# Settings
###############################################################################

# variants of function names on which performance of the main function might depend
parameters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]

# variants of main funciton names
methods = ["m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

#minimum number of clauses to be generated
min_clauses = 1

#minimum number of variables generated
min_vars = 1

#probability of using generators.several_perf_posibilites_unknown_cause instead of generators.several_perf_posibilites_use_fastest
prob_of_unknown_cause_subformula = 0.3

#maximum number of variants on which the main function might depend
max_perf_param_variants= 5


#parse the cmd line args
if len(sys.argv) >= 3:    
    min_vars = int(sys.argv[1])
    min_clauses = int(sys.argv[2])
    print >> sys.stderr, "min_vars: " + str(min_vars)
    print >> sys.stderr, "min_clauses: " + str(min_clauses)
    
if len(sys.argv) >= 4:
    print >> sys.stderr, "setting seed to " + sys.argv[3]
    seed(int(sys.argv[3]))
else:
    seed()
    


###############################################################################
# Helper code
###############################################################################

def random_sublist(list = [], min_length = 1, max_length = None):
    """Select a random sublist of the given list within the given bounds."""
    
    if not list:
        return []

    if max_length is None:
        max_length = len(list)
    length = randint(min(min_length, len(list)), min(max_length, len(list)))
    selected = []
    while len(selected) < min(length, len(list)):
        rnd = choice(list)
        if rnd not in selected:
            selected.append(rnd)
            list = [i for i in list if i!=rnd]
    return selected

class RenameVisitor(Visitor):
    """Formula visitor that renames all variables in the formula with the given unique rpefix.
    
    Fields:
    unique_prefix -- the prefix that is added to all variable names in the formula
    vars          -- the list of renamed variables in the formula (should contain all variables at the end)
    
    """
    def __init__(self, unique_prefix):
        self.unique_prefix  = unique_prefix
        self.vars = []
        
    def acceptVariable(self, f):
        f.name = self.unique_prefix + f.name
        if not f.name in self.vars:
            self.vars.append(f.name)
    
    def numVars(self):
        return len(self.vars)



###############################################################################
# Generator Script
###############################################################################


#current number of generated clauses
cur_clauses = 0
#current number of generated variables
cur_vars = 0

print >> sys.stderr, """
=====================================
GENERATING FORMULAS:
=====================================
"""
total = []
iteration = 1;

start = datetime.datetime.now()
totalTime = datetime.timedelta(0)

while cur_clauses < min_clauses or cur_vars < min_vars:
    m = choice(methods)    
    params = random_sublist(parameters, 2)

    use_unknown_cause = random() < prob_of_unknown_cause_subformula
        
    if use_unknown_cause:        
        current = Conjunction([several_perf_posibilites_unknown_cause(m, params, False)])
    else:        
        current = Conjunction(several_perf_posibilites_use_fastest(m, params, False))

    print >> sys.stderr, "\n".join([f.__str__() for f in current.subf])

    cnf = current #toCNF(current)

    # several iterations correspond to perf. parameter variants n = {10, 100, ...}
    param_variants = randint(1, max_perf_param_variants)
    print >> sys.stderr, "generating %d variants of perf. params" % param_variants 
    for variant in xrange(param_variants):
        clone = cnf.clone()

        prefix = "%d_%d" % (iteration, variant)
        visitor = RenameVisitor(prefix)    
        clone.visit(visitor)
        

        total.append(clone)
        cur_clauses += len(clone.subf)
        cur_vars += visitor.numVars()

    iteration+=1

end = datetime.datetime.now()

print >> sys.stderr, """DONE
=====================================
"""
print >> sys.stderr, "Completed in ", end - start
totalTime += end - start

print >> sys.stderr, """
=====================================
CONVERTING TO CNF
=====================================
"""
# Use De-Morgan laws for converting to CNF. 
# Tseitin's algorithm as we want an equivalent formula, not just equisatisfiable.
# Producing equisatisfiable formulas might introduce different shortest impliciant of the resulting formulas.

start = datetime.datetime.now()

whole = Conjunction(total)
clauses = Conjunction(total).toCNF().subf

end = datetime.datetime.now()
print >> sys.stderr, """DONE
=====================================
"""
print >> sys.stderr, "Completed in ", end - start
totalTime += end - start


print >> sys.stderr, """
=====================================
DIMACS:
=====================================
"""
start = datetime.datetime.now()

formatter = DimacsFormatVisitor()
formatter.processClauses(clauses)

print formatter.getDimacsString()

end = datetime.datetime.now()
print >> sys.stderr, """
=====================================
DONE.
vars:    %d
clauses: %d
=====================================
""" % (formatter.numVars(), formatter.numClauses())
end = datetime.datetime.now()
print >> sys.stderr, "Completed in ", end - start  

totalTime += end - start
print >> sys.stderr, "Total: ", totalTime

