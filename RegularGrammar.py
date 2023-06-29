from reader import Reader
from FiniteAutomata import FiniteAutomata

class GR():
    def __init__(self):
        pass
    
    def AFparaGR(self, af: FiniteAutomata, outputFilename):
        afMatriz = []
        # Coloca elemento X no cabeçalho da matriz e adiciona estados em ordem
        afMatriz.append(['X'])
        for elements in sorted(af.states):
            afMatriz.append([elements])

        # Garante que o estado inicial é o primeiro a aparecer na lista
        afMatriz.insert(1, afMatriz.pop(afMatriz.index([af.initialState])))

        # Opera sobre e coloca o epsilon para o final
        sortedAlphabet = sorted(af.alphabet)
        if(sortedAlphabet[0] == '&'):
            sortedAlphabet.pop(0)
            sortedAlphabet.append('&')

        # Coloca elementos do alfabeto na primeira linha da matriz
        for elements in sortedAlphabet:
            afMatriz[0].append(elements)

        # Preenche com listas vazias onde serão colocadas as transições
        for i in range(len(afMatriz[0])-1):
            for linha in afMatriz[1:]:
                linha.append([])

        # Monta as transições 
        for tuplas in sorted(af.transitions):
            for indice ,linha in enumerate(afMatriz[1:]):
                for index, element in enumerate(linha[1:]):
                    if(tuplas[0] == linha[0] and tuplas[2] == afMatriz[0][index+1]):
                        afMatriz[indice+1][index+1] = tuplas[1]

        # Adiciona o caracter - onde não tem transições
        for linhas in afMatriz:
            for i in range(len(linhas)):
                if (linhas[i] == []):
                    linhas[i] = '-'

        # Marca estado inicial
        for estados in afMatriz[1:]:
            if(estados[0] == af.initialState):
                estados[0] = '->' + estados[0]

        # Marca estados de aceitação
        for estados in afMatriz[1:]:
            if(estados[0] in af.acceptanceStates):
                estados[0] = '*' + estados[0]

        #Seta o automato finito
        af = afMatriz
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
        self.outputGRToFile(grFinal, outputFilename)
    
    def GRparaAF(self, gr):
        # Caminho contrário puta merda mas fazer o que
        # conjunto de estados finitos = cojunto de variaveis nao terminais + o estado de aceitação
        k = self.getConjuntoVariaveisNaoTerminais(gr)
        # conjunto finito de símbolos de entrada = conjunto de variáveis terminais
        e = self.getConjuntoVariaveisTerminais(gr)
        # estado inicial = simbolo inicial
        q0 = self.getSimboloInicial(gr)
        # montarAF 
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
                if("," in element):
                    # Separa o terminal do não terminal (o formato usado é a,A)
                    # Depois de separado, o ele procura a coluna que possui aquele terminal e coloca o não terminal na linha que está
                    # sendo trabalhada, porém na coluna referente ao terminal identificado
                    auxiliar = element.split(",")
                    indice = af[0].index(auxiliar[0])
                    af[index+1][indice].append(auxiliar[1])
                # Se a produção for somente um terminal
                else:
                    # Se for terminal, precisamos garantir também a transação para o estado de aceitação (criando não determinismo)
                    indice = af[0].index(element)
                    af[index+1][indice].append("X")
        return self.convertToAF(af)

    # Método de conversao para AF
    def convertToAF(self, afFinal):
        afFinal[1][0] = '->' + afFinal[1][0]
        for linhas in afFinal:
            linhas[0] = linhas[0].replace("-", "").replace(">", "").replace("*", "")
            for elements in linhas:
                if elements == []:
                    elements.append("-")

        # Método que monta as tuplas de transições para criação do automato
        setTuplas = []
        for linha in afFinal[1:]:
            for index, element in enumerate(linha[1:]):
                if (len(element) == 1):
                    if(element == ['-']):
                        break
                    else:
                        a = (linha[0],element[0],afFinal[0][index+1])
                        setTuplas.append(a)
                else:
                    for estados in element:
                        a = (linha[0],estados[0],afFinal[0][index+1])
                        setTuplas.append(a)
        return FiniteAutomata(set(self.getConjuntoEstados(afFinal)), set(self.getConjuntoSimbolos(afFinal)), set(setTuplas), afFinal[1][0], {'X'})
 
    # Retorna símbolo inicial da gramática
    def getSimboloInicial(self, gr):
        return gr[0][0]
    
    # Retorna conjunto de variáveis terminais da gramática
    def getConjuntoVariaveisTerminais(self, gr):
        conjuntoTerminais = []
        for linha in gr:
            for i in range(1, len(linha)):
                if(',' in linha[i]):
                    aux = linha[i].split(',')
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
        conjuntoNaoTerminais.append('*X')
        return conjuntoNaoTerminais

    # Printa a GR formatada
    def outputGRToFile(self, grFinal, filename):
        arquivo = open(filename, "a")
        for linha in grFinal:
            for i in range(0, len(linha)):
                if(i == 0):
                    valor = linha[i].replace("*", "").replace("->", "")
                    arquivo.write(valor + " ->")
                elif(i == 1):
                    arquivo.write(" " + linha[i])
                else: 
                    arquivo.write(" | " + linha[i])
            arquivo.write('\n')
        arquivo.close()
        print(f'Arquivo "{filename}" gerado/atualizado!')

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
