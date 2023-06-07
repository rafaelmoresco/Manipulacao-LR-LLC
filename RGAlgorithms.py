class GR():
    def __init__(self):
        self.af = 0
        self.n = []
        self.t = []
        self.s = 0
        self.f = []
    
    def AFparaGR(self, af):
        #Seta o automato finito
        self.af = af;
        # N = K (conjunto de variaveis nao terminais da gramatica = conjunto finito de estados)
        self.n = self.getConjuntoEstados()
        # T = Σ (conjunto de variáveis terminais = conjunto finito de símbolos de entrada)
        self.t = self.getConjuntoSimbolos()
        # S = q0 (símbolo inicial = estado inicial q0)
        self.s = self.getEstadoInicial()
        # Estados finais
        self.f = self.getEstadosFinais()
        # Definir P
        gr = self.af[1:]
        grFinal = []
        aux = []
        for elemento in gr:
            aux.append(elemento[0])
            grFinal.append(aux)
            aux = []
        for index, linha in enumerate(gr):
            for i in range(1, len(self.t)+1):
                if (linha[i] == '-'):
                    break
                else:
                    prod = self.af[0][i] + linha[i]
                    grFinal[index].append(prod)
                    if (linha[i] in self.f):
                        grFinal[index].append(self.af[0][i])
        self.printGR(grFinal)

    # Printa a GR formatada
    def printGR(self, grFinal):
        for linha in grFinal:
            for i in range(0, len(linha)):
                if(i == 0):
                    valor = linha[i].replace("*", "")
                    print(valor, end="")
                else:
                    print(" ," + linha[i], end="")
            print('\n')

    # Pega estados na primeira coluna apenas da matriz
    def getConjuntoEstados(self):
        conjuntoEstados = []
        conjuntoEstadosTotais = []
        for linha in self.af:
            conjuntoEstados.append(linha[0])
        conjuntoEstados.pop(0)
        for estado in conjuntoEstados:
            estadoNovo = estado.replace("-", "").replace(">", "").replace("*", "")
            conjuntoEstadosTotais.append(estadoNovo)
        return conjuntoEstadosTotais
    
    # Pega os simbolos da primeira linha da matriz
    def getConjuntoSimbolos(self):
        conjuntoSimbolosFinal = []
        for simbolo in self.af[0]:
            if(simbolo != 'X' and simbolo != '&'):
                conjuntoSimbolosFinal.append(simbolo)
        return conjuntoSimbolosFinal 

    # Pega simbolo inicial
    def getEstadoInicial(self):
        conjuntoEstados = []
        for linha in self.af:
            conjuntoEstados.append(linha[0])
        conjuntoEstados.pop(0)
        for estado in conjuntoEstados:
            if (estado[0] == '-' and estado[1] == '>'):
                return estado.replace("-", "").replace(">", "").replace("*", "")
            
    # Pega estados finais
    def getEstadosFinais(self):
        conjuntoEstados = []
        conjuntoEstadosFinais = []
        for linha in self.af:
            conjuntoEstados.append(linha[0])
        conjuntoEstados.pop(0)
        for estado in conjuntoEstados:
            if (estado[0] == '*'):
                estadoFinal = estado.replace("-", "").replace(">", "").replace("*", "")
                conjuntoEstadosFinais.append(estadoFinal)
        return conjuntoEstadosFinais

comEpsilon = [['X', 'a', 'b', 'c', '&'], 
        ['->*q0', 'q0', '-', '-', 'q1'],
        ['*q1', '-', 'q1', '-', 'q2'], 
        ['*q2', '-', '-', 'q2', '-']]

slide = [['X', 'a', 'b'], 
        ['->S', 'A', 'B'], 
        ['*A', 'S', 'C'], 
        ['B', 'C', 'S'],
        ['C','B','A']]

questao7 = [['X', 'a', 'b'],
 ['->q0q3q4', 'q0q1q3q4', 'q2q3q4'],
 ['*q1q3q4', 'q1q3q4', 'q2q3q4'],
 ['*q2', '-', 'q2q3q4'],
 ['q3q4', 'q1q3q4', 'q2q3q4'],
 ['*q0q1q3q4', 'q0q1q3q4', 'q2q3q4'],
 ['*q2q3q4', 'q1q3q4', 'q2q3q4']]

teste = GR()
teste.AFparaGR(slide)