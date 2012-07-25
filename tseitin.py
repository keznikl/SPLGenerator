'''
Created on 25.7.2012

@author: Keznikl
'''
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
    return Conjunction(toCNFClauses(formula))

def toCNFClauses(formula):
    f = VariableFactory()
    t = formula.derivationTree()
    literals = []
    root = tseitin(t, f, literals)
    res = [root]
    
    # conjoin all conjunctions
    for l in literals:
        if isinstance(l, Conjunction):
            res.extend(l.subf)
        else:
            res.append(l)
    
    return res
    
def tseitin(tree, varFactory, literals):
    # for a variable return only its reference, do not introduce any new literals
    if isinstance(tree, Variable):        
        return tree.clone()
    
    # for other subformulas:
    #    - assign a new variable to @tree
    #    - encode the local constraints,
    #    - add the encoded local constraints in literals
    #    - return the name of the new variable
    v = varFactory.getVariable()
    newVarsForSubf = [tseitin(e, varFactory, literals) for e in tree.getChildren()]
    newLit = tree.encodeLocal(v, newVarsForSubf)
    literals.append(newLit)
    return v
    
