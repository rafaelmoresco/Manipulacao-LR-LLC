from reader import Reader
from FiniteAutomata import FiniteAutomata

reader = Reader()
automata: FiniteAutomata = reader.readAF('input.txt')

# print("\nantes de determinizar\n", automata)
automata.determinize()
# print("\ndepois de determinizar\n", automata)
automata.minimize()
print("\ndepois de minimizar\n", automata)
