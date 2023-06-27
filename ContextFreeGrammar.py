from typing import List, Set, Dict, Tuple

class ContextFreeGrammar:
    def __init__(self, initialSymbol: str, terminals: Set[str], nonTerminals: Set[str], productions: Dict[str, Set[Tuple[str]]]):
        '''
        @param productions é um dicionário contendo como chave o símbolo e valor um set de tuplas contendo os símbolos de uma produção.
            ex: S -> a | AbC fica { 'S': { ('a',), ('A', 'b', 'C') } }
        '''
        self.__initialSymbol: str = initialSymbol
        self.__terminals: Set[str] = terminals.union({'&'})
        self.__nonTerminals: Set[str] = nonTerminals
        self.__productions: Dict[str, Set[Tuple]] = productions

    def __str__(self) -> str:
        return f'Símbolo inicial: {self.__initialSymbol}\n' +\
            f'Terminais: {self.__terminals}\n' +\
            f'Não terminais: {self.__nonTerminals}\n' +\
            f'    Gramática:\n' + self.__productionsToStr()

    ######################################### PRIVATE #########################################

    #################### Auxiliares ####################
    def __addProduction(self, symbol: str, constraint: str) -> None:
        '''Adiciona uma produção ao símbolo'''
        if symbol not in self.__productions:
            self.__productions[symbol] = set()
        self.__productions[symbol].add(tuple(constraint))

    def __removeProduction(self, symbol: str, constraint: str) -> None:
        '''Remove a produção do símbolo'''
        if symbol in self.__productions:
            self.__productions[symbol].discard(constraint)

    def __productionsToStr(self) -> str:
        '''Formata o dicionário de produções em uma string de gramática'''
        full = ''
        for symbol in self.__productions:
            line = symbol + ' -> '
            line += ' | '.join(map(lambda prod: ''.join(prod), self.__productions[symbol]))
            full += line + '\n'
        return full

    #################### Regras/Lógicas ####################

    ######################################### PUBLIC #########################################

    def writeToFile(self, filepath='gerados/GLC.txt'):
        '''Transforma as produções e as escreve em um arquivo em forma de gramática'''
        with open(filepath, 'w') as file:
            file.write(self.__productionsToStr())