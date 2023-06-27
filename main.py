from reader import Reader
from FiniteAutomata import FiniteAutomata
from FiniteAutomataUtils import FiniteAutomataUtils

reader = Reader()
faUtils = FiniteAutomataUtils()
# automata: FiniteAutomata = reader.readAF('no&.txt')
glc = reader.readGLC('testes/glc_recursiva.txt')
glc.writeToFile()