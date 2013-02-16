"""
Module for representing SAT formulas and their transformation to CNF.

@author: Keznikl
"""

class Visitor:
    """Interface for the visitor class over Formula sub-classes."""
    def acceptConjunction(self, f):
        pass
    def acceptDisjunction(self, f):
        pass
    def acceptNegation(self, f):
        pass
    def acceptImplication(self, f):
        pass
    def acceptEquivalence(self, f):
        pass
    def acceptVariable(self, f):
        pass

class Formula:
    """Base class for all logical operators in a proposition formula. 
    Instances represent the parse tree of a propositional formula.
    """
    
    def __init__(self, is_cnf = False):
        """A formula can be initialized as already in CNF.
        Checking is_cnf optimizes the runtime of the translation to CNF.        
        """
        self.is_cnf = is_cnf
        
    def toCNF(self):
        """Convert the formula represented by this node to CNF using De-Morgan laws."""
        pass
    
    def visit(self, visitor):
        """Aplly the visitor on the current parse-tree node of the formula and pass it to children.""" 
        pass
    
    def equals(self, f):
        """True iff this formula parse tree equals the parse tree of f."""
        pass
    
    def clone(self):
        """Deep clone the parse tree represented by this node. Maintains the is_cnf attribute."""
        pass
    
    def derivationTree(self):
        """Simplify the parse tree into a derivation tree."""
        pass
    
    def getChildren(self):
        """Return the children of the current node (not recursive)."""
        return []
    
    def encodeTseitin(self, newVar, subf):
        """Encodes the derivation tree represented by this node and it's children using tseitin's encoding.
        
        newVar -- the new variable for the current node
        subf -- the new variables for the children.
        
        """
        pass


class Conjunction(Formula):
    """Represents a conjunction in a parse tree of a propositional formula.
    
    Fields:
    is_cnf -- indicates if the subtree of self is already in CNF
    subf   -- list of sub-formulas in conjunction (childern in the parse tree)
    
    """
    
    def __init__(self, subformulas, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.subf = subformulas    
        
    def __str__(self):
        """Convert to string so that elements of the conjunction are in parentheses and separated by '&'."""
        return "(%s)" % " & ".join([f.__str__() for f in self.subf])
       
    def toCNF(self):        
        if self.is_cnf:
            return self
        clauses = []
        if all(isinstance(c, Conjunction) for c in self.subf):
            [clauses.extend(c.toCNF().subf) for c in self.subf]
        else:
            for f in [f1.toCNF() for f1 in self.subf]:
                if isinstance(f, Conjunction):
                    clauses.extend(f.subf)
                else:
                    clauses.append(f)
        #filter duplicates
        filtered = []
        for c in clauses:
            if not [f for f in filtered if f.equals(c)]:
                filtered.append(c)
        return Conjunction(sorted(filtered, key=lambda x: x.__str__()), is_cnf=True)
    
    def encodeTseitin(self, newVar, subf):
        return Equivalence(newVar, Conjunction(subf)).toCNF()
    
    def getChildren(self):
        """ Return the childern of self in the parse tree."""
        return self.subf
    
    def derivationTree(self):
        if len(self.subf) < 1:
            raise Exception("Too few subformulas in a conjunction")
        elif len(self.subf) == 1:
            return self.subf[0].derivationTree()        
        else:
            return Conjunction([e.derivationTree() for e in self.subf])
        
    def equals(self, f):
        if not isinstance(f, Conjunction):
            return False
        zipped = zip(self.subf, f.subf)
        return all(c1.equals(c2) for (c1, c2) in zipped)

    def visit(self, visitor):
        visitor.acceptConjunction(self)
        for f in self.subf:
            f.visit(visitor)

    def clone(self):
        """ Deep clone the parse subtree represetned by self."""
        return Conjunction([f.clone() for f in self.subf], is_cnf=self.is_cnf)


class Disjunction(Formula):
    """Represents a disjunction in a parse tree of a propositional formula.
    
    Fields:
    is_cnf -- indicates if the subtree of self is already in CNF
    subf   -- list of sub-formulas in disjunction (childern in the parse tree)
    
    """
    
    def __init__(self, subformulas=[], is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.subf = subformulas
        
    def __str__(self):
        """Convert to string so that elements of the disjunction are in parentheses and separated by '|'."""
        return "(%s)" % " | ".join([f.__str__() for f in self.subf])
    
    def toCNF(self):
        if self.is_cnf:
            return self
        terms = []
        conjunctions = []
        for f in [f1.toCNF() for f1 in self.subf]:
            if isinstance(f, Disjunction):
                terms.extend(f.subf)
            elif isinstance(f, Conjunction):
                conjunctions.append(f)
            else:
                terms.append(f)
            # propagate conjuncitons
        clauses = []
        for c in conjunctions:
            rest = [cl for cl in conjunctions if cl != c]
            clauses.extend([Disjunction([cl] + terms + rest) for cl in c.subf])

        if clauses:
            cnfClauses = Conjunction(clauses).toCNF().subf
            #filter duplicates
            filtered = []
            for c in cnfClauses:
                if not [f for f in filtered if f.equals(c)]:
                    filtered.append(c)

            return Conjunction(sorted(filtered, key=lambda x: x.__str__()), is_cnf=True)
        else:
            return Disjunction(sorted(terms, key=lambda x: x.__str__()), is_cnf=True)
    
    def derivationTree(self):
        if len(self.subf) < 2:
            raise Exception("To few subformulas in a conjunction") 
        elif len(self.subf) == 1:
            return self.subf[0].derivationTree()       
        else:
            return Disjunction([e.derivationTree() for e in self.subf])
        
    def getChildren(self):
        """ Return the childern of self in the parse tree."""
        return self.subf
    
    def encodeTseitin(self, newVar, subf):
        return Equivalence(newVar, Disjunction(subf)).toCNF()
    
    def equals(self, f):
        if not isinstance(f, Disjunction):
            return False
        zipped = zip(self.subf, f.subf)
        return all(c1.equals(c2) for (c1, c2) in zipped)

    def visit(self, visitor):
        visitor.acceptDisjunction(self)
        for f in self.subf:
            f.visit(visitor)

    def clone(self):
        """ Deep clone the parse subtree represetned by self."""
        return Disjunction([f.clone() for f in self.subf], is_cnf=self.is_cnf)
    

class Negation(Formula):
    """Represents a negation in a parse tree of a propositional formula.
    
    Fields:
    is_cnf -- indicates if the subtree of self is already in CNF
    subf   -- a sub-formula to be negated (a child in the parse tree)
    
    """
    
    def __init__(self, subformula=None, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.subf = subformula
        
    def __str__(self):
        """Convert to string so that the child is prepended by '!'."""
        return "!%s" % self.subf.__str__()
    
    def toCNF(self):
        if self.is_cnf:
            return self
        if isinstance(self.subf, Variable):
            return Negation(self.subf.toCNF(), is_cnf=True)
        if isinstance(self.subf, Negation):
            return self.subf.subf.toCNF()
        elif isinstance(self.subf, Disjunction):
            return Conjunction([Negation(f) for f in self.subf.subf]).toCNF()
        elif isinstance(self.subf, Conjunction):
            return Disjunction([Negation(f) for f in self.subf.subf]).toCNF()
        else:
            return Negation(self.subf.toCNF()).toCNF()
        
    def derivationTree(self):    
        return Negation(self.subf.derivationTree())
    
    def getChildren(self):
        """ Return the list containing the sole child of self in the parse tree."""
        return [self.subf]
    
    def encodeTseitin(self, newVar, subf):
        assert len(subf) == 1
        return Equivalence(newVar, Negation(subf[0])).toCNF()

    def equals(self, f):
        if not isinstance(f, Negation):
            return False
        return self.subf.equals(f.subf)

    def visit(self, visitor):
        visitor.acceptNegation(self)
        self.subf.visit(visitor)

    def clone(self):
        """ Deep clone the parse subtree represetned by self."""
        return Negation(self.subf.clone(), is_cnf=self.is_cnf)


class Variable(Formula):
    """Represents a variable in a parse tree of a propositional formula.
    
    Fields:
    is_cnf -- indicates if the subtree of self is already in CNF. 
              Although could be always True, both values are used to distinquish 
              between the original parse tree and the converted one.
    name   -- name of the variable
    
    """
    
    def __init__(self, name, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.name = name
        
    def __str__(self):
        """Return the variable name."""
        return self.name
    
    def toCNF(self):
        if self.is_cnf:
            return self
        return Variable(self.name, is_cnf=True)
    
    def derivationTree(self):    
        return self.clone()
    
    def getChildren(self):
        return []
    
    def encodeTseitin(self, newVar, subf):
        assert False, "encodeTseitin shouldn't be called on variable nodes"   
             
    def equals(self, c):
        if not isinstance(c, Variable):
            return False
        return self.name == c.name
    
    def visit(self, visitor):
        visitor.acceptVariable(self)
        
    def clone(self):
        """Clone the variable."""
        return Variable(self.name, is_cnf=self.is_cnf)
  

class Implication(Formula):
    """Represents an implication in a parse tree of a propositional formula.
    
    Fields:
    is_cnf     -- indicates if the subtree of self is already in CNF 
    premise    -- the premise (left part) of the implication
    conclusion -- the conclusion (right part) of the implication
    
    """
    
    def __init__(self, premise, conclusion, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.premise = premise
        self.conclusion = conclusion

    def __str__(self):
        """Convert to string in the form (premise => conclusion)."""
        return "(%s => %s)" % (self.premise.__str__(), self.conclusion.__str__())

    def toCNF(self):
        return Disjunction([Negation(self.premise), self.conclusion]).toCNF()
    
    def derivationTree(self):    
        return Implication(self.premise.derivationTree(), self.conclusion.derivationTree())
    
    def getChildren(self):
        return [self.premise, self.conclusion]
    
    def encodeTseitin(self, newVar, subf):
        assert len(subf) == 2
        return Equivalence(newVar, Implication(subf[0], subf[1])).toCNF()

    def equals(self, f):
        if not isinstance(f, Implication):
            return False
        return self.premise.equals(f.premise) and self.conclusion.equals(f.conclusion)

    def visit(self, visitor):
        visitor.acceptImplication(self)
        self.premise.visit(visitor)
        self.conclusion.visit(visitor)

    def clone(self):
        """ Deep clone the parse subtree represetned by self."""
        return Implication(self.premise.clone(), self.conclusion.clone())


class Equivalence(Formula):
    """Represents an equivalence in a parse tree of a propositional formula.
    
    Fields:
    is_cnf -- indicates if the subtree of self is already in CNF 
    left   -- the left part of the equivalence
    right  -- the right part of the equivalence
    
    """
    
    def __init__(self, left, right, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.left = left
        self.right = right

    def __str__(self):
        """Convert to string in the form (left <=> right)."""
        return "(%s <=> %s)" % (self.left.__str__(), self.right.__str__())

    def toCNF(self):
        return Conjunction([Implication(self.left, self.right), Implication(self.right, self.left)]).toCNF()
    
    def derivationTree(self):    
        return Equivalence(self.left.derivationTree(), self.right.derivationTree())
    
    def getChildren(self):
        return [self.left, self.right]
    
    def encodeTseitin(self, newVar, subf):
        assert len(subf) == 2
        return Equivalence(newVar, Equivalence(subf[0], subf[1])).toCNF()

    def equals(self, f):
        if not isinstance(f, Equivalence):
            return False
        return self.left.equals(f.left) and self.right.equals(f.right)

    def visit(self, visitor):
        visitor.acceptEquivalence(self)
        self.left.visit(visitor)
        self.right.visit(visitor)

    def clone(self):
        """ Deep clone the parse subtree represetned by self."""
        return Equivalence(self.left.clone(), self.right.clone())


