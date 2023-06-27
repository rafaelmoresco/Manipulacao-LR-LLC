class GR():
    def __init__(self):
        pass
    
    def AFparaGR(self, af):
        #Seta o automato finito
        af = af
        # N = K (conjunto de variaveis nao terminais da gramatica = conjunto finito de estados)
        n = self.getConjuntoEstados(af)
        # T = Σ (conjunto de variáveis terminais = conjunto finito de símbolos de entrada)
        t = self.getConjuntoSimbolos(af)
        # S = q0 (símbolo inicial = estado inicial q0)
        s = self.getEstadoInicial(af)
        # Estados finais
        f = self.getEstadosFinais(af)
        # Definir P
        gr = af[1:]
        grFinal = []
        aux = []
        # Cria lista transformando os estados da AF em não terminais da gramatica 
        for elemento in gr:
            aux.append(elemento[0])
            grFinal.append(aux)
            aux = []
        # Analisa o automato linha por linha afim de retirar os elementos para a formação da gramatica regular
        for index, linha in enumerate(gr):
            for i in range(1, len(t)+1):
                # Verifica se a transição existe
                if(linha[i] != '-'):
                    prod = af[0][i] + linha[i]
                    grFinal[index].append(prod)
                    if (linha[i] in f):
                        grFinal[index].append(af[0][i])
        #print(grFinal)
        self.printGR(grFinal)
    
    def GRparaAF(self, gr):
        # Caminho contrário puta merda mas fazer o que
        # conjunto de estados finitos = cojunto de variaveis nao terminais + o estado de aceitação
        k = self.getConjuntoVariaveisNaoTerminais(gr)
        #print(k)
        # conjunto finito de símbolos de entrada = conjunto de variáveis terminais
        e = self.getConjuntoVariaveisTerminais(gr)
        #print(e)
        # estado inicial = simbolo inicial
        q0 = self.getSimboloInicial(gr)
        #print(q0)
        # montarAF (PQP)
        af = []
        primeiraLinha = []
        # Coloca o X no cabeçalho
        primeiraLinha.append('X')
        # Complementa o cabeçalho com os simbolos da gramatica
        for simbolo in e:
            primeiraLinha.append(simbolo)
        # Adiciona o cabeçalho como primeira linha da AF final
        af.append(primeiraLinha)
        aux = []
        # Cria matriz base com estados x transições, para que sejam populadas posteriormente
        for estado in k:
            aux.append(estado)
            af.append(aux)
            aux = []
        # Para facilitar a manipulação, cria listas vazias nas posições da matriz para que só sejam anexados os estados depois
        for i in range(len(primeiraLinha)-1):
            for linha in af[1:]:
                linha.append([])
        # Gerada a matriz no formato final, preenche as listas dos estados com o que vem da gramatica
        # Analisa linha por linha da gramatica, pegando as produções da mesma
        for index, linha in enumerate(gr):
            for element in linha[1:]:
                # Se a produção não é somente um terminal
                if("|" in element):
                    # Separa o terminal do não terminal (o formato usado é a|A, por exemplo)
                    # Depois de separado, o ele procura a coluna que possui aquele terminal e coloca o não terminal na linha que está
                    # sendo trabalhada, porém na coluna referente ao terminal identificado
                    auxiliar = element.split("|")
                    indice = af[0].index(auxiliar[0])
                    af[index+1][indice].append(auxiliar[1])
                # Se a produção for somente um terminal
                else:
                    # Se for terminal, precisamos garantir também a transação também para o estado de aceitação
                    indice = af[0].index(element)
                    af[index+1][indice].append("Aceitacao")
                    # Caso o terminal analizado leve para um estado não terminal, precisamos colocar esse estado como estado de aceitação
                    for elementos in linha[1:]:
                        if(element + '|' in elementos):
                            uxiliar = elementos.split("|")
                            for indices ,linhas in enumerate(af):
                                # Depois de identificado, colocamos então a marcação nos estados de aceitação identificados
                                if (linha[0] == uxiliar[1] and '*' not in af[indice+1][0]):
                                    af[indice+1][0] = '*'+af[indice+1][0]
        #print(af)
        self.printAF(af)

    # Método de print do AF
    def printAF(self, afFinal):
        for linhas in afFinal:
            print(linhas)

    # Retorna símbolo inicial da gramática
    def getSimboloInicial(self, gr):
        return gr[0][0]
    
    # Retorna conjunto de variáveis terminais da gramática
    def getConjuntoVariaveisTerminais(self, gr):
        conjuntoTerminais = []
        for linha in gr:
            for i in range(1, len(linha)):
                if('|' in linha[i]):
                    aux = linha[i].split('|')
                    if(aux[0] not in conjuntoTerminais):
                        conjuntoTerminais.append(aux[0])
                else:
                    if(linha[i] not in conjuntoTerminais):
                        conjuntoTerminais.append(linha[i])
        return conjuntoTerminais

    # Retorna conjunto de variáveis não terminais da gramática
    def getConjuntoVariaveisNaoTerminais(self, gr):
        conjuntoNaoTerminais = []
        for linha in gr:
            conjuntoNaoTerminais.append(linha[0])
        conjuntoNaoTerminais.append('*Aceitacao')
        return conjuntoNaoTerminais

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

    # Retorna estados da AF
    def getConjuntoEstados(self, af):
        conjuntoEstados = []
        conjuntoEstadosTotais = []
        for linha in af:
            conjuntoEstados.append(linha[0])
        conjuntoEstados.pop(0)
        for estado in conjuntoEstados:
            estadoNovo = estado.replace("-", "").replace(">", "").replace("*", "")
            conjuntoEstadosTotais.append(estadoNovo)
        return conjuntoEstadosTotais
    
    # Retorna os simbolos da primeira linha da AF
    def getConjuntoSimbolos(self, af):
        conjuntoSimbolosFinal = []
        for simbolo in af[0]:
            if(simbolo != 'X' and simbolo != '&'):
                conjuntoSimbolosFinal.append(simbolo)
        return conjuntoSimbolosFinal 

    # Retorna estado inicial da AF
    def getEstadoInicial(self, af):
        conjuntoEstados = []
        for linha in af:
            conjuntoEstados.append(linha[0])
        conjuntoEstados.pop(0)
        for estado in conjuntoEstados:
            if (estado[0] == '-' and estado[1] == '>'):
                return estado.replace("-", "").replace(">", "").replace("*", "")
            
    # Retorna estados de aceitação da AF
    def getEstadosFinais(self, af):
        conjuntoEstados = []
        conjuntoEstadosFinais = []
        for linha in af:
            conjuntoEstados.append(linha[0])
        conjuntoEstados.pop(0)
        for estado in conjuntoEstados:
            if (estado[0] == '*'):
                estadoFinal = estado.replace("-", "").replace(">", "").replace("*", "")
                conjuntoEstadosFinais.append(estadoFinal)
        return conjuntoEstadosFinais

######################################## EXEMPLOS ########################################

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
 ['->S0', 'S4', 'S5'],
 ['*S1', 'S1', 'S5'],
 ['*S2', '-', 'S5'],
 ['S3', 'S1', 'S5'],
 ['*S4', 'S4', 'S5'],
 ['*S5', 'S1', 'S5']]

ex_gr = [['->S', 'a|A', 'b|B', 'b'],
         ['A', 'a|S'],
         ['B', 'b|B', 'b']]

teste = GR()
#teste.AFparaGR(questao7)
teste.GRparaAF(ex_gr)