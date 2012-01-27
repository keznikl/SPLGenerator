__author__ = 'Keznikl'

from random import *
from generators import *
from dimacs import DimacsFormatVisitor

seed()

#print Implication(
#    Conjunction([Variable("PMA1"), Variable("PMA2")]),
#    Conjunction([Variable("PMB1"), Variable("PMB2")])).toCNF().__str__()

parameters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
methods = ["m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
max_iterations = 15

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


formulas = []
for i in xrange(randint(1, max_iterations)):
    for m in random_sublist(methods):
        params = random_sublist(parameters, 2)
        formulas.append(Conjunction(several_perf_posibilites_use_fastest(m, params, False)))

print "\n".join([f.__str__() for f in formulas])
print """
=====================================
DIMACS:
=====================================
"""
formatter = DimacsFormatVisitor()
for f in formulas:
    formatter.processClauses(f.toCNF().subf)
    formatter.reset()
print formatter.getDimacsString()

#print "\n".join([f.__str__() for f in several_perf_posibilites_use_fastest("m", ["a", "b", "c"], False)])