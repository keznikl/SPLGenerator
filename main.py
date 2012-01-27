__author__ = 'Keznikl'

from random import *
from generators import *
from dimacs import DimacsFormatVisitor



###############################################################################
# Settings
###############################################################################
parameters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
methods = ["m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
min_clauses = 1000
min_vars = 1000
num_toplevel_disj = 3
max_perf_param_variants= 2

###############################################################################
# Generator Script
###############################################################################

seed()

def random_sublist(list = [], min_length = 1, max_length = None):
    if not list:
        return []

    if max_length is None:
        max_length = len(list)
    length = randint(min_length, min(max_length, len(list)))
    selected = []
    while len(selected) < min(length, len(list)):
        rnd = choice(list)
        if rnd not in selected:
            selected.append(rnd)
            list = [i for i in list if i!=rnd]
    return selected

class RenameVisitor(Visitor):
    def __init__(self, unique_prefix):
        self.unique_prefix  = unique_prefix
        self.vars = []
    def acceptVariable(self, f):
        f.name = self.unique_prefix + f.name
        if not f.name in self.vars:
            self.vars.append(f.name)
    def numVars(self):
        return len(self.vars)



cur_clauses = 0
cur_vars = 0

print """
=====================================
TOP-LEVEL NON-PRIMITIVE CONJUNCTIONS:
=====================================
"""
total = []
iteration = 1;
while cur_clauses < min_clauses or cur_vars < min_vars:

    m = choice(methods)
    params = random_sublist(parameters, 2)
    current = Conjunction(several_perf_posibilites_use_fastest(m, params))

    print "\n".join([f.__str__() for f in current.subf])

    cnf = current.toCNF()

    # several iterations correspond to perf. parameter variants n = {10, 100, ...}
    param_variants = randint(1, max_perf_param_variants)
    for variant in xrange(param_variants):
        clone = cnf.clone()

        prefix = "%d_%d" % (iteration, variant)
        visitor = RenameVisitor(prefix)
        clone.visit(visitor)

        total.append(clone)
        cur_clauses += len(clone.subf)
        cur_vars += visitor.numVars()

    iteration+=1

print """
=====================================
TOP-LEVEL NON-PRIMITIVE CONJUNCTIONS:
=====================================
"""
l = random_sublist(methods, num_toplevel_disj, num_toplevel_disj)
for m in l:
    params = random_sublist(parameters, 2)
    f = several_perf_posibilites_unknown_cause(m, params)
    print f.__str__()
    total.append(f)

print """
=====================================
CONVERTING TO CNF..."""
top = Conjunction(total).toCNF()

formatter = DimacsFormatVisitor()

formatter.processClauses(top.subf)

print """DONE
=====================================

"""

print """
=====================================
DIMACS:
=====================================
"""
print formatter.getDimacsString()

print """
=====================================
DONE.
vars:    %d
clauses: %d
=====================================
""" % (formatter.numVars(), formatter.numClauses())
