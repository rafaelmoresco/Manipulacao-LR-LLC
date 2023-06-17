from reader import Reader
from FiniteAutomata import FiniteAutomata
from FAAlgorithms import FAAlgorithm

reader = Reader()
algoritm = FAAlgorithm()
automata: FiniteAutomata = reader.readAF('no&.txt')

print("\nantes de determinizar\n", automata)
automata.determinize()
print("\ndepois de determinizar\n", automata)
print(automata.read('aa'))
automata.minimize()
print("\ndepois de minimizar\n", automata)

# a: FiniteAutomata = reader.readAF('a.txt')
# b: FiniteAutomata = reader.readAF('b.txt')
# 
# print("\nA\n", a)
# print("\nB\n", b)
# c: FiniteAutomata = algoritm.dfaIntersection(a,b)
# print("\nC\n", c)