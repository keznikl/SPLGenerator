__author__ = 'Keznikl'



class Formula:
    def toCNF(self):
        pass
    def equals(self, f):
        pass

class Conjunction(Formula):
    def __init__(self, subformulas=[]):
        self.subf = subformulas
    def __str__(self):
        return "(%s)" % " & ".join([f.__str__() for f in self.subf])
    def toCNF(self):
        clauses = []
        for f in [f1.toCNF() for f1 in self.subf]:
            if isinstance(f, Conjunction):
                clauses.extend(f.subf)
            else:
                clauses.append(f)
        return Conjunction(sorted(clauses, key=lambda x: x.__str__()))

    def equals(self, f):
        if not isinstance(f, Conjunction):
            return False
        zipped = zip(self.subf, f.subf)
        return all(c1.equals(c2) for (c1, c2) in zipped)


class Disjunction(Formula):
    def __init__(self, subformulas=[]):
        self.subf = subformulas
    def __str__(self):
        return "(%s)" % " | ".join([f.__str__() for f in self.subf])
    def toCNF(self):
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

            return Conjunction(sorted(filtered, key=lambda x: x.__str__()))
        else:
            return Disjunction(sorted(terms, key=lambda x: x.__str__()))

    def equals(self, f):
        if not isinstance(f, Disjunction):
            return False
        zipped = zip(self.subf, f.subf)
        return all(c1.equals(c2) for (c1, c2) in zipped)


class Negation(Formula):
    def __init__(self, subformula=None):
        self.subf = subformula
    def __str__(self):
        return "!%s" % self.subf.__str__()
    def toCNF(self):
        if isinstance(self.subf, Variable):
            return self
        if isinstance(self.subf, Negation):
            return self.subf.subf
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


class Variable(Formula):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def toCNF(self):
        return self
    def equals(self, c):
        if not isinstance(c, Variable):
            return False
        return self.name == c.name

class Implication(Formula):
    def __init__(self, premise, conclusion):
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

class Equivalence(Formula):
    def __init__(self, left, right):
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

