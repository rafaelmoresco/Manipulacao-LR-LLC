from reader import Reader
from FiniteAutomata import FiniteAutomata
from FiniteAutomataUtils import FiniteAutomataUtils
from RegularGrammar import GR
from ContextFreeGrammar import ContextFreeGrammar
from RegEx import RegexTree

reader = Reader()
algoritm = FiniteAutomataUtils()
regularGrammar = GR()

while True:
    print("Digite a operação: ",end='')
    x = input()
    if x == "determinizarAF":
        print("Digite o arquivo de origem: ",end='')
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.determinize()
    elif x == "minimizarAF":
        print("Digite o arquivo de origem: ",end='')
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.minimize()
    elif x == "uniaoAF":
        print("Digite o primeiro aquivo de origem: ",end='')
        y = input()
        print("Digite o segundo aquivo de origem: ",end='')
        z = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata2: FiniteAutomata = reader.readAF(z)
        new = algoritm.dfaUnion(inputAutomata, inputAutomata2)
    elif x == "intersecaoAF":
        print("Digite o primeiro aquivo de origem: ",end='')
        y = input()
        print("Digite o segundo aquivo de origem: ",end='')
        z = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata2: FiniteAutomata = reader.readAF(z)
        new = algoritm.dfaIntersection(inputAutomata, inputAutomata2)
    elif x == "regex":
         print("Digite o Regex: ", end='')
         y = input()
         regex = RegexTree(y)
         new = regex.toDfa()
    elif x == "leituraAF":
        print("Digite o arquivo de origem: ",end='')
        y = input()
        print("Digite a palavra para ser lida: ",end='')
        z = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        if inputAutomata.read(z):
            print("Palavra reconhecida!")
        else:
            print("Palavra não reconhecida!")
    elif x == "GRparaAF":
        print("Digite o arquivo de origem: ",end='')
        y = input()
        gr = reader.readGr(y)
        new = regularGrammar.GRparaAF(gr)
        new.outputToFile("RGtoFA")
    elif x == "AFparaGR":
        print("Digite o arquivo de origem: ",end='')
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        regularGrammar.AFparaGR(inputAutomata)
    elif x == "sair":
        exit()
    else:
        print("Operação Inválida!")