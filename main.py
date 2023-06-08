from reader import Reader
from FiniteAutomata import FiniteAutomata

reader = Reader()
automata: FiniteAutomata = reader.readAF('input.txt')

print("\nantes de minimizar\n", automata)
automata.minimize()
print("\ndepois de minimizar\n", automata)

