from typing import List, Tuple, Set, Dict
from FiniteAutomata import FiniteAutomata
from copy import deepcopy
### AUXILIARY METHODS
#Regex validation
def is_valid_regex(regex):
    return valid_brackets(regex) and valid_operations(regex)  
def valid_brackets(regex):
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
def valid_operations(regex):
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

    def __init__(self, regex, alphabet):
        self.__alphabet = alphabet
        self.nullable = None
        self.firstpos = []
        self.lastpos = []
        self.item = None
        self.position = None
        self.children = []

        #Check if it is leaf
        if len(regex) == 1 and self.is_letter(regex):
            #Leaf
            self.item = regex
            #Lambda checking
            if self.item == '&':
                self.nullable = True
            else:
                self.nullable = False
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
            if self.is_concat(regex[i]):
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
            self.item = '|'
            self.children.append(RegexNode(self.trim_brackets(regex[:or_operator]),self.__alphabet))
            self.children.append(RegexNode(self.trim_brackets(regex[(or_operator+1):]),self.__alphabet))
        elif concatenation != -1:
            #Found a concatenation
            self.item = '.'
            self.children.append(RegexNode(self.trim_brackets(regex[:concatenation]),self.__alphabet))
            self.children.append(RegexNode(self.trim_brackets(regex[concatenation:]),self.__alphabet))
        elif kleene != -1:
            #Found a kleene
            self.item = '*'
            self.children.append(RegexNode(self.trim_brackets(regex[:kleene]),self.__alphabet))

    def trim_brackets(self, regex):
        while regex[0] == '(' and regex[-1] == ')' and is_valid_regex(regex[1:-1]):
            regex = regex[1:-1]
        return regex
    
    def is_concat(self, c):
        return c == '(' or self.is_letter(c)
    
    def is_letter(self, c):
        return c in self.__alphabet
    
    def calc_functions(self, pos, followpos):
        if self.is_letter(self.item):
            #Is a leaf
            self.firstpos = [pos]
            self.lastpos = [pos]
            self.position = pos
            #Add the position in the followpos list
            followpos.append([self.item,[]])
            return pos+1
        #Is an internal node
        for child in self.children:
            pos = child.calc_functions(pos, followpos)
        #Calculate current functions

        if self.item == '.':
            #Is concatenation
            #Firstpos
            if self.children[0].nullable:
                self.firstpos = sorted(list(set(self.children[0].firstpos + self.children[1].firstpos)))
            else:
                self.firstpos = deepcopy(self.children[0].firstpos)
            #Lastpos
            if self.children[1].nullable:
                self.lastpos = sorted(list(set(self.children[0].lastpos + self.children[1].lastpos)))
            else:
                self.lastpos = deepcopy(self.children[1].lastpos)
            #Nullable
            self.nullable = self.children[0].nullable and self.children[1].nullable
            #Followpos
            for i in self.children[0].lastpos:
                for j in self.children[1].firstpos:
                    if j not in followpos[i][1]:
                        followpos[i][1] = sorted(followpos[i][1] + [j])

        elif self.item == '|':
            #Is or operator
            #Firstpos
            self.firstpos = sorted(list(set(self.children[0].firstpos + self.children[1].firstpos)))
            #Lastpos
            self.lastpos = sorted(list(set(self.children[0].lastpos + self.children[1].lastpos)))
            #Nullable
            self.nullable = self.children[0].nullable or self.children[1].nullable

        elif self.item == '*':
            #Is kleene
            #Firstpos
            self.firstpos = deepcopy(self.children[0].firstpos)
            #Lastpos
            self.lastpos = deepcopy(self.children[0].lastpos)
            #Nullable
            self.nullable = True
            #Followpos
            for i in self.children[0].lastpos:
                for j in self.children[0].firstpos:
                    if j not in followpos[i][1]:
                        followpos[i][1] = sorted(followpos[i][1] + [j])

        return pos

    def write_level(self, level):
        print(str(level) + ' ' + self.item, self.firstpos, self.lastpos, self.nullable, '' if self.position == None else self.position)
        for child in self.children:
            child.write_level(level+1)

class RegexTree:

    def __init__(self, regex: str) -> None:
        self.__regex = self.__preProcess(regex)
        self.__alphabet = set(self.__regex) - set('()|*')
        self.__root = RegexNode(self.__regex, self.__alphabet)
        self.__followpos = []
        self.__functions()
    
    def __preProcess(self, regex) -> str:
        if not is_valid_regex(regex):
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
    

    def __functions(self):
        positions = self.__root.calc_functions(0, self.__followpos)   
    
    def toDfa(self) -> 'FiniteAutomata':

        def contains_hashtag(q):
            for i in q:
                if self.__followpos[i][0] == '#':
                    return True
            return False

        markedStates = [] #Marked states
        statesList = [] #States list in the followpos form ( array of positions ) 
        rAlphabet = self.__alphabet - {'#', '&'} #Automata alphabet
        transitions = set() #Delta function, an array of dictionaries d[q] = {x1:q1, x2:q2 ..} where d(q,x1) = q1, d(q,x2) = q2..
        finalStates = [] #FInal states list in the form of indexes (int)
        q0 = self.__root.firstpos

        statesList.append(q0)
        if contains_hashtag(q0):
            finalStates.append(statesList.index(q0))
        
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
                    if contains_hashtag(U):
                        finalStates.append(str(statesList.index(U)))
                #d(q,a) = U
                transitions.add((str(statesList.index(q)),str(statesList.index(U)),a))
        states = set()
        for state in statesList:
            states.add(str(statesList.index(state)))
        return FiniteAutomata(states,set(rAlphabet),transitions,str(statesList.index(q0)),set(finalStates))

#Main
regex = '(aa|b)*ab(bb|a)*'
'''
#Construct
tree = RegexTree(regex)
dfa = tree.toDfa()

#Test
message = 'baaab'
print('This is the regex : ' + regex)
print('This is the automata : \n')
print(dfa)
print(dfa.read(message))
'''

