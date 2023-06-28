from typing import List, Tuple, Set
from FiniteAutomata import FiniteAutomata

class Reader():
    def __readFile(self, fileName):
        f = open(fileName,"r")
        content = f.readlines()
        f.close()
        return content

    def readAF(self, fileName: str) -> FiniteAutomata:
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

    def readGr(self, fileName: str):
        content = self.__readFile(fileName)
        grFormatada = []

        for i in range(0, len(content)):
            linha = content[i].replace(' ', '').strip('\n').split('->')
            aux = linha[1].split('|')
            for i in range(0, len(aux)):
                linha.append(aux[i])
            linha.pop(1)
            grFormatada.append(linha)

        for i, linha in enumerate(grFormatada):
            for j, element in enumerate(linha):
                if (len(element) > 1):
                    grFormatada[i][j] = element[:1] + ',' + element[1:]
        
        return grFormatada

