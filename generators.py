__author__ = 'Keznikl'

from formula import *

def several_perf_posibilites_unknown_cause(method = "", possibilities = [], cnf = False):
    if not possibilities:
        return
    ret = Disjunction([
        Conjunction([
            Variable("P" + method + p + "1"),
            Variable("P" + method + p + "2")
        ])
        for p in possibilities
    ])
    if cnf:
        return ret.toCNF()
    else:
        return ret

def several_perf_posibilites_use_fastest(method = "", possibilities = [], cnf = False):
    if not possibilities:
        return
    ret =  [
               Conjunction(
                   # Pa<b & Pa<c <=> Sa
                   [Equivalence(
                       Conjunction([
                       Variable("P" + p + "<" + r)
                       for r in possibilities if r != p
                       ]),
                       Variable("S" + p)
                   )
                    for p in possibilities]
               )] + [
        Conjunction(
            # (Pa<b <=> !Pb<a)
            [Equivalence(
                Variable("P" + a + "<" + b),
                Negation(Variable("P" + b + "<" + a))
            )
             for a in possibilities for b in possibilities if a != b]
        )]  + [
        Conjunction(
            # (Pa<b <=> !Pb<a)
            [Implication(
                Variable("S" + p),
                Conjunction([
                    Variable("P" + method + p + "1"),
                    Variable("P" + method + p + "2")
                ])
            )
             for p in possibilities]
        )]
    if cnf:
        return [f.toCNF() for f in ret]
    else:
        return ret

