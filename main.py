from reader import Reader
from FiniteAutomata import FiniteAutomata
from FAAlgorithms import FAAlgorithm

reader = Reader()
algoritm = FAAlgorithm()
automata: FiniteAutomata = reader.readAF('no&.txt')

print("\nantes de determinizar\n", automata)
automata.determinize()
automata.minimize()
print("\ndepois de minimizar\n", automata)
# print(automata.read('aa'))