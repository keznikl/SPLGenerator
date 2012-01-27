__author__ = 'Keznikl'


from generators import *

#print Implication(
#    Conjunction([Variable("PMA1"), Variable("PMA2")]),
#    Conjunction([Variable("PMB1"), Variable("PMB2")])).toCNF().__str__()


print "\n".join([f.__str__() for f in several_perf_posibilites_use_fastest("m", ["a", "b", "c"], False)])