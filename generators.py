"""
Module containing factory methods for generating SPL-specific propositional formulas in CNF.

@author: Keznikl
"""

from formula import *

def several_perf_posibilites_unknown_cause(method = "", possibilities = [], cnf = False):
    """Return propositional skeleton of a SPL formula expressing that performance of the 
    given method depends on one of the listed possibilities.
    
    Keyword arguments:
    method        -- the method dependency of which is expressed
    possibilities -- list of possibilities one of which the method depends on
    cnf           -- indicates, whether the resulting formula should be in CNF
    
    """
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
    """Return list of formulas represenring the propositional skeleton of a SPL formula 
    expressing that performance of the given method depends on one the fastest of 
    the listed possibilities.
    
    Keyword arguments:
    method        -- the method dependency of which is expressed
    possibilities -- list of possibilities one of which the method depends on
    cnf           -- indicates, whether the resulting list of formulas should be in CNF
    
    """
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
            # (Sa => (Pma1&Pma2))
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

