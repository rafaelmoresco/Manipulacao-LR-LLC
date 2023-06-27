from typing import List, Tuple, Set
from FiniteAutomata import FiniteAutomata
from ContextFreeGrammar import ContextFreeGrammar

class Reader():
    def __readFile(self, fileName):
        f = open(fileName,"r")
        content = f.readlines()
        f.close()
        return content

    def readAF(self, fileName: str) -> FiniteAutomata:
        '''Lê um arquivo contendo uma tabela de transicoes de um AF e retorna uma instância de FiniteAutomata correspondente'''
        content = self.__readFile(fileName)

        alphabet: List[str] = content[0].replace(' ', '').strip('\n').split('|')[1:]
        states: Set[str] = set()
        initialState: str = None
        acceptanceStates: Set[str] = set()
        transitions: Set[Tuple[str, str, str]] = set()
        
        for i in range(1, len(content)):
            line = content[i].replace(' ', '').strip('\n')
            splitedLine = line.split('|')
            state = splitedLine[0]
            cleanState = state.replace('->', '').strip('*')
            states.add(cleanState)

            if '->' in state:
                initialState = cleanState
            if '*' in state:
                acceptanceStates.add(cleanState)

            for j in range(len(splitedLine)-1):
                if '-' not in splitedLine[j+1]:
                    transitions.add((cleanState, splitedLine[j+1].strip('*'), alphabet[j]))

        return FiniteAutomata(states, set(alphabet), transitions, initialState, acceptanceStates)

    def readGr():
        pass

    def readGLC(self, filepath: str) -> ContextFreeGrammar:
        '''Lê um arquivo contendo as definições de uma GLC e retorna uma instância de ContextFreeGrammar correspondente'''
        with open(filepath, 'r') as file:
            lines = file.read().split('\n')

        productions = dict()
        terminals = set()
        nonTerminals = set()
        for i, line in enumerate(lines):
            if len(line) <= 0:
                break
            
            line = line.split('->')
            symbol = line[0].strip()
            nonTerminals.add(symbol)
            if i == 0:
                initialSymbol = symbol
            
            for char in line[1]:
                if char == " " or char == "|": continue
                if char.isupper():
                    nonTerminals.add(char)
                else:
                    terminals.add(char)
            
            productions[symbol] = set()
            constraints = list(map(lambda prod: prod.strip(), line[1].split('|')))
            for constraint in constraints:
                productions[symbol].add(tuple(constraint))
        
        return ContextFreeGrammar(initialSymbol, terminals, nonTerminals, productions)