from reader import Reader
from FiniteAutomata import FiniteAutomata
from FiniteAutomataUtils import FiniteAutomataUtils

reader = Reader()
algoritm = FiniteAutomataUtils()
automata: FiniteAutomata = reader.readAF('no&.txt')

print("\nantes de determinizar\n", automata)
automata.determinize()
automata.minimize()
print("\ndepois de minimizar\n", automata)
# print(automata.read('aa'))