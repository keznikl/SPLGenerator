__author__ = 'Keznikl'

from random import *
from generators import *
from dimacs import DimacsFormatVisitor



###############################################################################
# Settings
###############################################################################
parameters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
methods = ["m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
min_clauses = 5000
min_vars = 5000


###############################################################################
# Generator Script
###############################################################################

seed()

def random_sublist(list = [], min_length = 1):
    if not list:
        return []

    length = randint(min_length, len(list))
    selected = []
    while len(selected) < min(length, len(list)):
        rnd = choice(list)
        if rnd not in selected:
            selected.append(rnd)
            list = [i for i in list if i!=rnd]
    return selected


cur_clauses = 0
cur_vars = 0
formatter = DimacsFormatVisitor()


while cur_clauses < min_clauses or cur_vars < min_vars:
    current = []
    for m in random_sublist(methods):
        params = random_sublist(parameters, 2)
        current.append(Conjunction(several_perf_posibilites_use_fastest(m, params, False)))

    print "\n".join([f.__str__() for f in current])
    for f in current:
        formatter.processClauses(f.toCNF().subf)
    cur_clauses = formatter.numClauses()
    cur_vars = formatter.numVars()
    formatter.reset()

print """
=====================================
DIMACS:
=====================================
"""
print formatter.getDimacsString()

