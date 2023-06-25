from typing import List, Tuple, Set, Dict, AnyStr
from FiniteAutomata import FiniteAutomata
from copy import deepcopy
### AUXILIARY METHODS
#Regex validation
def isValidRegex(regex: str) -> bool:
    return validBrackets(regex) and validOperations(regex)  

def validBrackets(regex: str) -> bool:
    opened_brackets = 0
    for c in regex:
        if c == '(':
            opened_brackets += 1
        if c == ')':
            opened_brackets -= 1
        if opened_brackets < 0:
            print('ERROR missing bracket')
            return False
    if opened_brackets == 0:
        return True
    print('ERROR unclosed brackets')
    return False    

def validOperations(regex: str) -> bool:
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

        #Check if it is leaf
        if len(regex) == 1 and self.__isLetter(regex):
            #Leaf
            self.__item = regex
            #Lambda checking
            if self.__item == '&':
                self.__nullable = True
            else:
                self.__nullable = False
            return
        
        #It is an internal node
        #Finding the leftmost operators in all three
        kleene = -1
        or_operator = -1
        concatenation = -1
        i = 0

        #Getting the rest of terms    
        while i < len(regex):
            if regex[i] == '(':
                #Composed block
                bracketing_level = 1
                #Skipping the entire term
                i+=1
                while bracketing_level != 0 and i < len(regex):
                    if regex[i] == '(':
                        bracketing_level += 1
                    if regex[i] == ')':
                        bracketing_level -= 1
                    i+=1
            else:
                #Going to the next char
                i+=1
            
            #Found a concatenation in previous iteration
            #And also it was the last element check if breaking
            if i == len(regex):
                break

            #Testing if concatenation
            if self.__isConcat(regex[i]):
                if concatenation == -1:
                    concatenation = i
                continue
            #Testing for kleene
            if regex[i] == '*':
                if kleene == -1:
                    kleene = i
                continue
            #Testing for or operator
            if regex[i] == '|':
                if or_operator == -1:
                    or_operator = i
        
        #Setting the current operation by priority
        if or_operator != -1:
            #Found an or operation
            self.__item = '|'
            self.__children.append(RegexNode(self.__trimBrackets(regex[:or_operator]),self.__alphabet))
            self.__children.append(RegexNode(self.__trimBrackets(regex[(or_operator+1):]),self.__alphabet))
        elif concatenation != -1:
            #Found a concatenation
            self.__item = '.'
            self.__children.append(RegexNode(self.__trimBrackets(regex[:concatenation]),self.__alphabet))
            self.__children.append(RegexNode(self.__trimBrackets(regex[concatenation:]),self.__alphabet))
        elif kleene != -1:
            #Found a kleene
            self.__item = '*'
            self.__children.append(RegexNode(self.__trimBrackets(regex[:kleene]),self.__alphabet))

    def __trimBrackets(self, regex: str) -> str:
        while regex[0] == '(' and regex[-1] == ')' and isValidRegex(regex[1:-1]):
            regex = regex[1:-1]
        return regex
    
    def __isConcat(self, c: str) -> bool:
        return c == '(' or self.__isLetter(c)
    
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
            if self.__children[0].__nullable:
                self.__firstpos = sorted(list(set(self.__children[0].firstpos + self.__children[1].firstpos)))
            else:
                self.__firstpos = deepcopy(self.__children[0].firstpos)
            #Lastpos
            if self.__children[1].__nullable:
                self.__lastpos = sorted(list(set(self.__children[0].lastpos + self.__children[1].lastpos)))
            else:
                self.__lastpos = deepcopy(self.__children[1].lastpos)
            #Nullable
            self.__nullable = self.__children[0].__nullable and self.__children[1].__nullable
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