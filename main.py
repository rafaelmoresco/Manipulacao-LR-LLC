from reader import Reader
from FiniteAutomata import FiniteAutomata
from FiniteAutomataUtils import FiniteAutomataUtils
from RegularGrammar import GR
from RegEx import RegexTree

reader = Reader()
algoritm = FiniteAutomataUtils()
regularGrammar = GR()

AVAILABLE_OPERATIONS = ["disponivel", "determinizarAF", "minimizarAF", "uniaoAF", "intersecaoAF", "regex", "leituraAF", "GRparaAF", "AFparaGR", "sair"]

print("Digite a operação ['disponivel' para listar as opções]:",end='\n> ')
while True:
    x = input()
    if x == "disponivel":
        print(', '.join(AVAILABLE_OPERATIONS))
    elif x == "determinizarAF":
        print("Digite o arquivo de origem: ",end='\n> ')
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.determinize().outputToFile('gerados/determinizarAF.txt')
    elif x == "minimizarAF":
        print("Digite o arquivo de origem: ",end='\n> ')
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.minimize().outputToFile('gerados/minimizarAF.txt')
    elif x == "uniaoAF":
        print("Digite o primeiro aquivo de origem: ",end='\n> ')
        y = input()
        print("Digite o segundo aquivo de origem: ",end='\n> ')
        z = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata2: FiniteAutomata = reader.readAF(z)
        automata = algoritm.dfaUnion(inputAutomata, inputAutomata2)
        automata.outputToFile('gerados/uniaoAF.txt')
    elif x == "intersecaoAF":
        print("Digite o primeiro aquivo de origem: ",end='\n> ')
        y = input()
        print("Digite o segundo aquivo de origem: ",end='\n> ')
        z = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata2: FiniteAutomata = reader.readAF(z)
        automata = algoritm.dfaIntersection(inputAutomata, inputAutomata2)
        automata.outputToFile('gerados/interseccaoAF.txt')
    elif x == "regex":
         print("Digite o Regex: ", end='\n> ')
         y = input()
         regex = RegexTree(y)
         automata = regex.toDfa()
         automata.outputToFile('gerados/regex.txt')
    elif x == "leituraAF":
        print("Digite o arquivo de origem: ",end='\n> ')
        y = input()
        print("Digite a palavra para ser lida: ",end='\n> ')
        z = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        if inputAutomata.read(z):
            print("Palavra reconhecida!")
        else:
            print("Palavra não reconhecida!")
    elif x == "GRparaAF":
        print("Digite o arquivo de origem: ",end='\n> ')
        y = input()
        gr = reader.readGr(y)
        automata = regularGrammar.GRparaAF(gr)
        automata.outputToFile("gerados/GRparaAF.txt")
    elif x == "AFparaGR":
        print("Digite o arquivo de origem: ",end='\n> ')
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        regularGrammar.AFparaGR(inputAutomata)
    elif x == "sair":
        exit()
    else:
        print("Operação inválida!")