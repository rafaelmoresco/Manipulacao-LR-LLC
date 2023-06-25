from typing import List, Tuple, Set, Dict, AnyStr
from FiniteAutomata import FiniteAutomata
from copy import deepcopy
#################### Auxiliares ####################
# Validação de Regex
def isValidRegex(regex: str) -> bool:
    return validBrackets(regex) and validOperations(regex)  
# Validação de ()s
def validBrackets(regex: str) -> bool:
    openedBrackets = 0
    for c in regex:
        if c == '(':
            openedBrackets += 1
        if c == ')':
            openedBrackets -= 1
        if openedBrackets < 0:
            print('ERROR missing bracket')
            return False
    if openedBrackets == 0:
        return True
    print('ERROR unclosed brackets')
    return False    
# Validação de Operações
def validOperations(regex: str) -> bool:
    # Percorre todos os caracteres do regex, contando a posição de cada
    for i, c in enumerate(regex):
        if c == '*':
            if i == 0:
                print('ERROR * with no argument at', i)
                return False
            if regex[i - 1] in '(|':
                print('ERROR * with no argument at', i)
                return False
        if c == '|':
            if i == 0 or i == len(regex) - 1:
                print('ERROR | with missing argument at', i)
                return False
            if regex[i - 1] in '(|':
                print('ERROR | with missing argument at', i)
                return False
            if regex[i + 1] in ')|':
                print('ERROR | with missing argument at', i)
                return False
    return True

class RegexNode:

    def __init__(self, regex: str, alphabet: set):
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

    def calcFunctions(self, pos: int, followpos: List[str]):
        if self.__isLetter(self.__item):
            #Is a leaf
            self.__firstpos = [pos]
            self.__lastpos = [pos]
            self.__position = pos
            #Add the position in the followpos list
            followpos.append([self.__item,[]])
            return pos+1
        #Is an internal node
        for child in self.__children:
            pos = child.calcFunctions(pos, followpos)
        #Calculate current functions

        if self.__item == '.':
            #Is concatenation
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

        elif self.__item == '|':
            #Is or operator
            #Firstpos
            self.__firstpos = sorted(list(set(self.__children[0].firstpos + self.__children[1].firstpos)))
            #Lastpos
            self.__lastpos = sorted(list(set(self.__children[0].lastpos + self.__children[1].lastpos)))
            #Nullable
            self.__nullable = self.__children[0].__nullable or self.__children[1].__nullable

        elif self.__item == '*':
            #Is kleene
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

    def __preProcess(self, regex) -> str:
        if not isValidRegex(regex):
            exit()
        regex = self.__cleanKleene(regex)
        regex = regex.replace(' ','')
        regex = '(' + regex + ')' + '#'
        while '()' in regex:
            regex = regex.replace('()','')
        return regex

    def __cleanKleene(self, regex: str) -> str:
        for i in range(0, len(regex) - 1):
            while i < len(regex) - 1 and regex[i + 1] == regex[i] and regex[i] == '*':
                regex = regex[:i] + regex[i + 1:]
        return regex
    
    def __functions(self) -> None:
        self.__root.calcFunctions(0, self.__followpos)
    
    ######################################### PUBLIC #########################################

    def toDfa(self) -> 'FiniteAutomata':

        def containsHashtag(q) -> bool:
            for i in q:
                if self.__followpos[i][0] == '#':
                    return True
            return False

        markedStates = [] #Marked states
        statesList = [] #States list in the followpos form ( array of positions ) 
        rAlphabet = self.__alphabet - {'#', '&'} #Automata alphabet
        transitions = set() #Delta function, an array of dictionaries d[q] = {x1:q1, x2:q2 ..} where d(q,x1) = q1, d(q,x2) = q2..
        acceptanceStates = set() #FInal states list in the form of indexes (int)
        q0 = self.__root.firstpos

        statesList.append(q0)
        if containsHashtag(q0):
            acceptanceStates.add('q'+str(statesList.index(q0)))
        
        while len(statesList) - len(markedStates) > 0:
            #There exists one unmarked
            #We take one of those
            q = [i for i in statesList if i not in markedStates][0]
            #Generating the delta dictionary for the new state
            #We mark it
            markedStates.append(q)
            #For each letter in the automata's alphabet
            for a in rAlphabet:
                # Compute destination state ( d(q,a) = U )
                U = []
                #Compute U
                #foreach position in state
                for i in q:
                    #if i has label a
                    if self.__followpos[i][0] == a:
                        #We add the position to U's composition
                        U = U + self.__followpos[i][1]
                U = sorted(list(set(U)))
                #Checking if this is a valid state
                if len(U) == 0:
                    #No positions, skipping, it won't produce any new states ( also won't be final )
                    continue
                if U not in statesList:
                    statesList.append(U)
                    if containsHashtag(U):
                        acceptanceStates.add('q'+str(statesList.index(U)))
                #d(q,a) = U
                transitions.add(('q'+str(statesList.index(q)),'q'+str(statesList.index(U)),a))
        states = set()
        for state in statesList:
            states.add('q'+str(statesList.index(state)))
        return FiniteAutomata(states,rAlphabet,transitions,'q'+str(statesList.index(q0)),acceptanceStates)