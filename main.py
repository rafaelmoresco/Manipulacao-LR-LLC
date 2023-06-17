from reader import Reader
from FiniteAutomata import FiniteAutomata
from FAAlgorithms import NFA

reader = Reader()
algoritm = NFA()
automata: FiniteAutomata = reader.readAF('input.txt')

# print("\nantes de determinizar\n", automata)
# automata.determinize()
# print("\ndepois de determinizar\n", automata)
# print(automata.read('101'))
# automata.minimize()
# print("\ndepois de minimizar\n", automata)

a: FiniteAutomata = reader.readAF('a.txt')
b: FiniteAutomata = reader.readAF('b.txt')

print("\nA\n", a)
print("\nB\n", b)
c: FiniteAutomata = algoritm.dfaUnion(a,b)
print("\nC\n", c)