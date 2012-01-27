__author__ = 'Keznikl'

class Visitor:
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
    def __init__(self, is_cnf = False):
        self.is_cnf = is_cnf
    def toCNF(self):
        pass
    def visit(self, visitor):
        pass
    def equals(self, f):
        pass
    def clone(self):
        pass

class Conjunction(Formula):
    def __init__(self, subformulas, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.subf = subformulas
    def __str__(self):
        return "(%s)" % " & ".join([f.__str__() for f in self.subf])
    def toCNF(self):
        if self.is_cnf:
            return self
        clauses = []
        if all(isinstance(c, Conjunction) for c in self.subf):
            clauses = reduce(lambda l, c: l + c.toCNF().subf, self.subf, [])
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
        return Conjunction([f.clone() for f in self.subf], is_cnf=self.is_cnf)

class Disjunction(Formula):
    def __init__(self, subformulas=[], is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.subf = subformulas
    def __str__(self):
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
            clauses.extend([Disjunction([cl] + terms + rest).toCNF() for cl in c.subf])

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
        return Disjunction([f.clone() for f in self.subf], is_cnf=self.is_cnf)

class Negation(Formula):
    def __init__(self, subformula=None, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.subf = subformula
    def __str__(self):
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

    def equals(self, f):
        if not isinstance(f, Negation):
            return False
        return self.subf.equals(f.subf)

    def visit(self, visitor):
        visitor.acceptNegation(self)
        self.subf.visit(visitor)

    def clone(self):
        return Negation(self.subf.clone(), is_cnf=self.is_cnf)

class Variable(Formula):
    def __init__(self, name, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.name = name
    def __str__(self):
        return self.name
    def toCNF(self):
        if self.is_cnf:
            return self
        return Variable(self.name, is_cnf=True)
    def equals(self, c):
        if not isinstance(c, Variable):
            return False
        return self.name == c.name
    def visit(self, visitor):
        visitor.acceptVariable(self)
    def clone(self):
        return Variable(self.name, is_cnf=self.is_cnf)

class Implication(Formula):
    def __init__(self, premise, conclusion, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.premise = premise
        self.conclusion = conclusion

    def __str__(self):
        return "(%s => %s)" % (self.premise.__str__(), self.conclusion.__str__())

    def toCNF(self):
        return Disjunction([Negation(self.premise), self.conclusion]).toCNF()

    def equals(self, f):
        if not isinstance(f, Implication):
            return False
        return self.premise.equals(f.premise) and self.conclusion.equals(f.conclusion)

    def visit(self, visitor):
        visitor.acceptImplication(self)
        self.premise.visit(visitor)
        self.conclusion.visit(visitor)

    def clone(self):
        return Implication(self.premise.clone(), self.conclusion.clone())


class Equivalence(Formula):
    def __init__(self, left, right, is_cnf=False):
        Formula.__init__(self, is_cnf)
        self.left = left
        self.right = right

    def __str__(self):
        return "(%s <=> %s)" % (self.left.__str__(), self.right.__str__())

    def toCNF(self):
        return Conjunction([Implication(self.left, self.right), Implication(self.right, self.left)]).toCNF()

    def equals(self, f):
        if not isinstance(f, Equivalence):
            return False
        return self.left.equals(f.left) and self.right.equals(f.right)

    def visit(self, visitor):
        visitor.acceptEquivalence(self)
        self.left.visit(visitor)
        self.right.visit(visitor)

    def clone(self):
        return Equivalence(self.left.clone(), self.right.clone())


