from typing import List
from FiniteAutomata import FiniteAutomata
from copy import deepcopy
#################### Auxiliares ####################
# Validação de Regex
def isValidRegex(regex: str) -> bool:
    return validBrackets(regex) and validOperations(regex)  
# Validação de ()s
def validBrackets(regex: str) -> bool:
    openedBrackets = 0
    # Percorre o Regex somando para ( e subtraindo para )
    for c in regex:
        if c == '(':
            openedBrackets += 1
        if c == ')':
            openedBrackets -= 1
        if openedBrackets < 0:
            print('Falta (')
            return False
    if openedBrackets == 0:
        return True
    print('Falta )')
    return False    
# Validação de Operações
def validOperations(regex: str) -> bool:
    # Percorre todos os caracteres do regex, contando a posição de cada
    for i, c in enumerate(regex):
        if c == '*':
            if i == 0:
                print('* sem termo em', i)
                return False
            if regex[i - 1] in '(|':
                print('* sem termo em', i)
                return False
        if c == '|':
            if i == 0 or i == len(regex) - 1:
                print('| com falta de termo em', i)
                return False
            if regex[i - 1] in '(|':
                print('| com falta de termo em', i)
                return False
            if regex[i + 1] in ')|':
                print('E| com falta de termo em', i)
                return False
    return True

class RegexNode:

    def __init__(self, regex: str, alphabet: set) -> None:
        self.__alphabet = alphabet
        self.__nullable = None
        self.__firstpos: List[int] = []
        self.__lastpos: List[int] = []
        self.__item = None
        self.__position = None
        self.__children: List['RegexNode'] = []

        # Verifica se é uma folha
        if len(regex) == 1 and self.__isLetter(regex):
            # Folha
            self.__item = regex
            # Se for &, folha é nullable
            if self.__item == '&':
                self.__nullable = True
            else:
                self.__nullable = False
            return
        
        # Se não é uma folha, continua gerando a árvore
        # Encontra a operação mais a esquerda
        kleene = -1
        orOperator = -1
        concatenation = -1
        i = 0

        # Pega o resto dos termos    
        while i < len(regex):
            if regex[i] == '(':
                # Bloco composto
                bracketingLevel = 1
                # Pula todo o termo
                i+=1
                while bracketingLevel != 0 and i < len(regex):
                    if regex[i] == '(':
                        bracketingLevel += 1
                    if regex[i] == ')':
                        bracketingLevel -= 1
                    i+=1
            else:
                # Vai para o próximo char
                i+=1
            
            # Se for o ultimo elemento, saí do loop
            if i == len(regex):
                break

            # Verifica se é uma concatenação
            if self.__isConcat(regex[i]):
                if concatenation == -1:
                    concatenation = i
                continue
            # Verifica se é um fecho de kleene
            if regex[i] == '*':
                if kleene == -1:
                    kleene = i
                continue
            # Verifica se é uma operação ou
            if regex[i] == '|':
                if orOperator == -1:
                    orOperator = i
        
        # Define a operação
        if orOperator != -1:
            # Encontrou um ou
            self.__item = '|'
            self.__children.append(RegexNode(self.__trimBrackets(regex[:orOperator]),self.__alphabet))
            self.__children.append(RegexNode(self.__trimBrackets(regex[(orOperator+1):]),self.__alphabet))
        elif concatenation != -1:
            # Encontrou uma concatenação
            self.__item = '.'
            self.__children.append(RegexNode(self.__trimBrackets(regex[:concatenation]),self.__alphabet))
            self.__children.append(RegexNode(self.__trimBrackets(regex[concatenation:]),self.__alphabet))
        elif kleene != -1:
            # Encontrou um fecho
            self.__item = '*'
            self.__children.append(RegexNode(self.__trimBrackets(regex[:kleene]),self.__alphabet))
    
    ######################################### PRIVATE #########################################

    #################### Auxiliares ####################
    # Remove os ()s das extremidades
    def __trimBrackets(self, regex: str) -> str:
        while regex[0] == '(' and regex[-1] == ')' and isValidRegex(regex[1:-1]):
            regex = regex[1:-1]
        return regex
    # Verifica se é concatenação
    def __isConcat(self, c: str) -> bool:
        return c == '(' or self.__isLetter(c)
    # Verifica se é uma letra individual
    def __isLetter(self, c: str) -> bool:
        return c in self.__alphabet
    
    @property
    def nullable(self) -> bool:
        return self.__nullable
    @property
    def firstpos(self) -> List[int]:
        return self.__firstpos
    @property
    def lastpos(self) -> List[int]:
        return self.__lastpos
    
    ######################################### PUBLIC #########################################

    def calcFunctions(self, pos: int, followpos: List[str]) -> int:
        # Se for uma folha
        if self.__isLetter(self.__item):
            self.__firstpos = [pos]
            self.__lastpos = [pos]
            self.__position = pos
            # Adiciona a posição atual no followpos
            followpos.append([self.__item,[]])
            return pos+1
        # Se é um nodo interno
        for child in self.__children:
            pos = child.calcFunctions(pos, followpos)
            # Calcula as funções dos filhos

        # É um concat
        if self.__item == '.':
            #Firstpos
            if self.__children[0].nullable:
                self.__firstpos = sorted(list(set(self.__children[0].firstpos + self.__children[1].firstpos)))
            else:
                self.__firstpos = deepcopy(self.__children[0].firstpos)
            #Lastpos
            if self.__children[1].nullable:
                self.__lastpos = sorted(list(set(self.__children[0].lastpos + self.__children[1].lastpos)))
            else:
                self.__lastpos = deepcopy(self.__children[1].lastpos)
            #Nullable
            self.__nullable = self.__children[0].nullable and self.__children[1].nullable
            #Followpos
            for i in self.__children[0].lastpos:
                for j in self.__children[1].firstpos:
                    if j not in followpos[i][1]:
                        followpos[i][1] = sorted(followpos[i][1] + [j])

        # É um ou
        elif self.__item == '|':
            #Firstpos
            self.__firstpos = sorted(list(set(self.__children[0].firstpos + self.__children[1].firstpos)))
            #Lastpos
            self.__lastpos = sorted(list(set(self.__children[0].lastpos + self.__children[1].lastpos)))
            #Nullable
            self.__nullable = self.__children[0].__nullable or self.__children[1].__nullable

        # É um fecho de kleene
        elif self.__item == '*':
            #Firstpos
            self.__firstpos = deepcopy(self.__children[0].firstpos)
            #Lastpos
            self.__lastpos = deepcopy(self.__children[0].lastpos)
            #Nullable
            self.__nullable = True
            #Followpos
            for i in self.__children[0].lastpos:
                for j in self.__children[0].firstpos:
                    if j not in followpos[i][1]:
                        followpos[i][1] = sorted(followpos[i][1] + [j])

        return pos

class RegexTree:

    def __init__(self, regex: str) -> None:
        self.__regex = self.__preProcess(regex)
        self.__alphabet = set(self.__regex) - set('()|*')
        self.__root = RegexNode(self.__regex, self.__alphabet)
        self.__followpos: List[str] = []
        self.__functions()

    ######################################### PRIVATE #########################################

    # Valida se o regex é valido e prepara ele para ser processado
    def __preProcess(self, regex) -> str:
        # Valida
        if not isValidRegex(regex):
            print('Regex inválido')
            exit()
        regex = self.__cleanKleene(regex)
        regex = regex.replace(' ','')
        # Coloca tudo entre ()s e adiciona fim de sentença
        regex = '(' + regex + ')' + '#'
        # Remove ()s desnecessários
        while '()' in regex:
            regex = regex.replace('()','')
        return regex

    def __cleanKleene(self, regex: str) -> str:
        for i in range(0, len(regex) - 1):
            while i < len(regex) - 1 and regex[i + 1] == regex[i] and regex[i] == '*':
                regex = regex[:i] + regex[i + 1:]
        return regex
    
    # Calcula as funções firstpos, lastpos e followpos
    def __functions(self) -> None:
        self.__root.calcFunctions(0, self.__followpos)
    
    ######################################### PUBLIC #########################################

    # Converte para um Automato Finito Deterministico
    def toDfa(self) -> 'FiniteAutomata':

        def containsHashtag(q: List[int]) -> bool:
            for i in q:
                if self.__followpos[i][0] == '#':
                    return True
            return False

        markedStates = [] # Estados marcados
        statesList = [] # Lista de psoições na forma de followpos ( array de posições ) 
        rAlphabet = self.__alphabet - {'#', '&'} # Alfabeto
        transitions = set() # Conjunto de transições ( conjunto de tuplas )
        acceptanceStates = set() #Estados de aceitação na forma de indices
        q0 = self.__root.firstpos # Estado inicial

        # Adiciona q0 na lista de estados, e se ele for de aceitação, adiciona para conjunto aceitação
        statesList.append(q0)
        if containsHashtag(q0):
            # Como se trabalha com indices, é transformado em string
            acceptanceStates.add('q'+str(statesList.index(q0)))
        
        # Enquanto existir estados não marcados
        while len(statesList) - len(markedStates) > 0:
            # Escolhemos um estatado não marcado para gerar transições
            q = [i for i in statesList if i not in markedStates][0]
            # Marcando e estado escolhido
            markedStates.append(q)
            # Para cada letra do alfabeto
            for a in rAlphabet:
                # Encontra-se o destino U ( δ(q,a) = U )
                U = []
                # Para cada posição em q
                for i in q:
                    # Se possui o a
                    if self.__followpos[i][0] == a:
                        # Adicionamos a U
                        U = U + self.__followpos[i][1]
                # Removendo repitidos e ordenando U
                U = sorted(list(set(U)))
                # Verifica se U é vazio
                if len(U) == 0:
                    # Se vazio, ignora
                    continue
                # Se ainda não está na lista de estados
                if U not in statesList:
                    statesList.append(U)
                    # Se final, adiciona em lista de finais
                    if containsHashtag(U):
                        acceptanceStates.add('q'+str(statesList.index(U)))
                # δ = (estado q, destino U, simbolo a)
                transitions.add(('q'+str(statesList.index(q)),'q'+str(statesList.index(U)),a))
        states = set()
        # Transforma os estados em indice em strings qi
        for state in statesList:
            states.add('q'+str(statesList.index(state)))
        new = FiniteAutomata(states,rAlphabet,transitions,'q'+str(statesList.index(q0)),acceptanceStates)
        new.outputToFile('RegexToDFA')
        return new