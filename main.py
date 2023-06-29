from reader import Reader
from FiniteAutomata import FiniteAutomata
from FiniteAutomataUtils import FiniteAutomataUtils
from RegularGrammar import GR
from ContextFreeGrammar import ContextFreeGrammar
from RegEx import RegexTree

reader = Reader()
finiteAutomataUtils = FiniteAutomataUtils()

AVAILABLE_OPERATIONS = {
    'Geral': ['disponivel', 'sair'],
    'Autômato Finito': ["determinizarAF", "minimizarAF", "uniaoAF", "intersecaoAF", 'leituraSentencaAF'],
    'Conversões': ['GRparaAF', 'AFparaGR', 'REGEXparaAFD'],
    'Gramática Livre de Contexto': ['fatorarGLC', 'removerRecursaoEsqGLC', 'leituraSentencaGLC']
}

while True:
    print("Digite a operação ['disponivel' para listar as opções]:")
    x = input('> ')

    ######### GERAL #########
    if x == "disponivel":
        for type in AVAILABLE_OPERATIONS:
            print(type + ':')
            for op in AVAILABLE_OPERATIONS[type]:
                print("   " + op)
    elif x == "sair":
        exit()
    
    ######### AUTOMATO FINITO #########
    elif x == "determinizarAF":
        print("Digite o arquivo de origem: ")
        y = input('> ')
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.determinize().outputToFile('gerados/determinizarAF.txt')
    elif x == "minimizarAF":
        print("Digite o arquivo de origem: ")
        y = input('> ')
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata.minimize().outputToFile('gerados/minimizarAF.txt')
    elif x == "uniaoAF":
        print("Digite o primeiro aquivo de origem: ")
        y = input('> ')
        print("Digite o segundo aquivo de origem: ")
        z = input('> ')
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata2: FiniteAutomata = reader.readAF(z)
        automata = finiteAutomataUtils.dfaUnion(inputAutomata, inputAutomata2)
        automata.outputToFile('gerados/uniaoAF.txt')
    elif x == "intersecaoAF":
        print("Digite o primeiro aquivo de origem: ")
        y = input('> ')
        print("Digite o segundo aquivo de origem: ")
        z = input('> ')
        inputAutomata: FiniteAutomata = reader.readAF(y)
        inputAutomata2: FiniteAutomata = reader.readAF(z)
        automata = finiteAutomataUtils.dfaIntersection(inputAutomata, inputAutomata2)
        automata.outputToFile('gerados/interseccaoAF.txt')
    elif x == "leituraSentencaAF":
        print("Digite o arquivo de origem: ")
        y = input('> ')
        print("Digite a palavra para ser lida: ")
        z = input('> ')
        inputAutomata: FiniteAutomata = reader.readAF(y)
        if inputAutomata.read(z):
            print("Palavra reconhecida!")
        else:
            print("Palavra não reconhecida!")
    
    ######### CONVERSOES #########
    elif x == "GRparaAF":
        print("Digite o arquivo de origem: ")
        y = input('> ')
        gr = reader.readGr(y)
        regularGrammar = GR()
        automata = regularGrammar.GRparaAF(gr)
        automata.outputToFile("gerados/GRparaAF.txt")
    elif x == "AFparaGR":
        print("Digite o arquivo de origem: ")
        y = input('> ')
        inputAutomata: FiniteAutomata = reader.readAF(y)
        regularGrammar = GR()
        regularGrammar.AFparaGR(inputAutomata, 'gerados/AFparaGR.txt')
    elif x == "REGEXparaAFD":
         print("Digite o Regex: ",)
         y = input('> ')
         regex = RegexTree(y)
         automata = regex.toDfa()
         automata.outputToFile('gerados/REGEXparaAFD.txt')

    ######### GLC #########
    elif x == 'fatorarGLC':
        print("Digite o arquivo de origem da GLC:")
        y = input('> ')
        glc = reader.readGLC(y)
        glc.leftFactor()
        glc.outputToFile('gerados/fatorarGLC.txt')
    elif x == 'removerRecursaoEsqGLC':
        print("Digite o arquivo de origem da GLC:")
        y = input('> ')
        glc = reader.readGLC(y)
        glc.removeLeftmostRecursions()
        glc.outputToFile('gerados/removerRecursaoEsqGLC.txt')
    elif x == 'leituraSentencaGLC':
        print("Digite o arquivo de origem da GLC:")
        y = input('> ')
        print("Digite a sentença a ser lida [cada nao terminal separado por espaço]:")
        z = input('> ')
        glc = reader.readGLC(y)
        glc.read(z)
        glc.outputToFile('gerados/removerRecursaoEsqGLC.txt')
    else:
        print("Operação inválida!")
