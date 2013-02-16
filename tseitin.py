"""
Module containing implementaiton of Tseitin's algorihm for conversion in CNF.

@author: Keznikl
"""

from formula import *
  
class VariableFactory:
    def __init__(self, unique_prefix=''):
        self.counter = 0
        self.unique_prefix = unique_prefix
    def getVariable(self):
        v = Variable(self.unique_prefix + str(self.counter))
        self.counter += 1        
        return v
    
def toCNF(formula):
    """Convert the formula into an equisatisfiable CNF formula using Tseitin's algorithm."""
    return Conjunction(toCNFClauses(formula))

def toCNFClauses(formula):
    """Convert the formula into an equisatisfiable list of clauses using Tseitin's algorithm."""
    f = VariableFactory()
    t = formula.derivationTree()
    clauses = []
    root = tseitin(t, f, clauses)
    res = [root]
    
    # conjoin all conjunctions
    for c in clauses:
        if isinstance(c, Conjunction):
            res.extend(c.subf)
        else:
            res.append(c)
    
    return res
    
def tseitin(tree, varFactory, clauses):
    """Convert the given derivation tree of the formula into an equisatisfiable list of clauses usinf Tseitin's algorithm.
    
    tree       -- the derivation tree of the formula to be converted
    varFactory -- a factory for creating new variable names
    clauses    -- the clauses of the Tseitin's encoding
    
    returns    -- the new variable representing the root of the derivation tree
    
    """ 
    # for a variable return only its reference, do not introduce any new clauses
    if isinstance(tree, Variable):        
        return tree.clone()
    
    # for other subformulas:
    #    - assign a new variable to @tree
    #    - encode the local constraints,
    #    - add the encoded local constraints in clauses
    #    - return the name of the new variable
    v = varFactory.getVariable()
    newVarsForSubf = [tseitin(e, varFactory, clauses) for e in tree.getChildren()]
    newLit = tree.encodeTseitin(v, newVarsForSubf)
    clauses.append(newLit)
    return v
    
