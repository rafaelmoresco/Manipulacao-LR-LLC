from reader import Reader
from FiniteAutomata import FiniteAutomata
from FiniteAutomataUtils import FiniteAutomataUtils
from RegEx import RegexTree

reader = Reader()
algoritm = FiniteAutomataUtils()

while True:
    x = input()
    if x == "determinizar":
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.determinize()
    elif x == "minimizar":
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.minimize()
    elif x == "uniao":
        y, z = input().split()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata2: FiniteAutomata = reader.readAF(z)
        new = algoritm.dfaUnion(inputAutomata, inputAutomata2)
    elif x == "intersecao":
        y, z = input().split()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata2: FiniteAutomata = reader.readAF(z)
        new = algoritm.dfaIntersection(inputAutomata, inputAutomata2)
    elif x == "regex":
         y = input()
         regex = RegexTree(y)
         new = regex.toDfa()
    elif x == "leituraAF":
        y, z = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.read(z)
    elif x == "sair":
        break
    else:
        print("Operação Inválida")