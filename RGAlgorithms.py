from pprint import pprint


class GR():
    def __init__(self, af):
        self.af = af
    
    def AFparaGR(self):
        # N = K (conjunto de variaveis nao terminais da gramatica = conjunto finito de estados)
        n = self.getConjuntoEstados()
        print(n)
        # T = Σ (conjunto de variáveis terminais = conjunto finito de símbolos de entrada)
        t = self.getConjuntoSimbolos()
        print(t)
        # S = q0 (símbolo inicial = estado inicial q0)
        s = self.getEstadoInicial()
        print(s)
        # Estados finais
        f = self.getEstadosFinais()
        print(f)
        # Definir P
        # Agora começa o problema

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
    
    def getConjuntoSimbolos(self):
        conjuntoSimbolosFinal = []
        for simbolo in self.af[0]:
            if(simbolo != 'X' and simbolo != '&'):
                conjuntoSimbolosFinal.append(simbolo)
        return conjuntoSimbolosFinal 

    def getEstadoInicial(self):
        conjuntoEstados = []
        for linha in self.af:
            conjuntoEstados.append(linha[0])
        conjuntoEstados.pop(0)
        for estado in conjuntoEstados:
            if (estado[0] == '-' and estado[1] == '>'):
                return estado.replace("-", "").replace(">", "").replace("*", "")
            
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
            

aaaa = [['X', 'a', 'b', 'c', '&'], 
        ['->*q0', 'q0', '-', '-', 'q1'], 
        ['*q1', '-', 'q1', '-', 'q2'], 
        ['*q2', '-', '-', 'q2', '-']]
teste = GR(aaaa)
teste.AFparaGR()