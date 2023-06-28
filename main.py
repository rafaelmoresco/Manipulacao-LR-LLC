from reader import Reader
from FiniteAutomata import FiniteAutomata
from FiniteAutomataUtils import FiniteAutomataUtils
from RegEx import RegexTree

reader = Reader()
algoritm = FiniteAutomataUtils()

while True:
    print("Digite a operação: ",end='')
    x = input()
    if x == "determinizar":
        print("Digite o arquivo de origem: ",end='')
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.determinize()
    elif x == "minimizar":
        print("Digite o arquivo de origem: ",end='')
        y = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.minimize()
    elif x == "uniao":
        print("Digite o primeiro aquivo de origem: ",end='')
        y = input()
        print("Digite o segundo aquivo de origem: ",end='')
        z = input()
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata2: FiniteAutomata = reader.readAF(z)
        new = algoritm.dfaUnion(inputAutomata, inputAutomata2)
    elif x == "intersecao":
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
    elif x == "sair":
        exit()
        break
    else:
        print("Operação Inválida!")