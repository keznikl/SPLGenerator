__author__ = 'Keznikl'

from formula import *

class DimacsFormatVisitor():
    def __init__(self):
        self.variables = {}
        self.var_counter = 1
        self.clauses = []

    def reset(self, reset_clauses = False):
        self.variables = {}
        if reset_clauses:
            self.var_counter = 1
            self.clauses = []

    def getDimacsString(self):
        num_variables = self.var_counter - 1
        num_clauses = len(self.clauses)
        header = "c code verification example\np cnf %d %d\n" % (num_variables, num_clauses)
        return header + "\n".join(self.clauses)

    def processClauses(self, c):
        self.clauses.extend([self.formatClause(cl) for cl in c])

    def formatClause(self, clause):
        assert isinstance(clause, Disjunction)
        return " ".join([self.formatVar(v) for v in clause.subf] + ["0"])

    def formatVar(self, var):
        assert isinstance(var, Negation) or isinstance(var, Variable)
        if isinstance(var, Negation):
            return "-%s" % self.formatVar(var.subf)
        else:
            vcode = self.variables.get(var.name, None)
            # var.name not in self.variables
            if not vcode:
                vcode = "%d" % self.var_counter
                self.var_counter += 1
                self.variables[var.name] = vcode
            return vcode

    def numClauses(self):
        return len(self.clauses)
    def numVars(self):
        return self.var_counter - 1
