from typing import List, Tuple, Set, Callable, List
import aux

class FiniteAutomata:
    
    def __init__(self, states: Set[str], alphabet: Set[str], transitions: List[Tuple[str, str, str]], initialState: str, acceptanceStates: Set[str]) -> None:
        '''
        @param transitions Lista de tuplas em que cada tupla contem, nessa ordem: estado de, estado para, transita por
        '''
        self.__states = states
        self.__alphabet = alphabet
        self.__transitions = transitions
        self.__initialState = initialState
        self.__acceptanceStates = acceptanceStates

    def __str__(self):
        return f'Estados: {self.__states}\n' +\
            f'Alfabeto: {self.__alphabet}\n' +\
            f'Transicoes: {self.__transitions}\n' +\
            f'Estado Inicial: {self.__initialState}\n' +\
            f'Estados de Aceitacao: {self.__acceptanceStates}'
    
    ######################################### PRIVATE #########################################

    def __removeUnreachables(self) -> None:
        reachableStates = set()
        reachableTransitions = set()
        reachableStates.add(self.__initialState)
        transitions = list(self.__transitions)
        reaching_states = True

        # Itera ate achar todos os estados alcançaveis
        while reaching_states:
            reaching_states = False
            for item in transitions:
                if item[0] in reachableStates:
                    reachableStates.add(item[1])
                    reachableTransitions.add(item)
                    transitions.remove(item)
                    reaching_states = True
        self.__states = reachableStates

        # Atualiza os estados com os estados alcançaveis
        self.__transitions = reachableTransitions
        # Remove dos estados de aceitação os estados inalcançaveis
        self.__acceptanceStates = set([state for state in self.__acceptanceStates if state in reachableStates])

    def __removeDeads(self) -> None:
        aliveStates = self.__acceptanceStates.copy()
        transitions = list(self.__transitions)
        aliveTransitions = set()
        alive = True
        while alive:
            alive = False
            for item in transitions:
                if item[1] in aliveStates:
                    aliveStates.add(item[0])
                    aliveTransitions.add(item)
                    transitions.remove(item)
                    alive = True
        self.__states = aliveStates
        self.__transitions = aliveTransitions

    # Apenas para AFD
    def __nextState(self, initialState, symbol) -> str:
        for [initial, to, transitionsBy] in self.__transitions:
            if initialState == initial and transitionsBy == symbol:
                return to
        return '-'
        
    def __splitClassesOfEquivalence(self, equivalenceClasses, splittable, symbol) -> List:
        equivalenceClassesDict = {','.join(key): [] for key in equivalenceClasses}
        equivalenceClassesDict['-'] = []

        for x in splittable:
            nextState = self.__nextState(x, symbol) ## calcula para onde o estado vai
            for key, value in equivalenceClassesDict.items():
                if nextState in key.split(','):
                    value.append(x)
                    break

        return [value for _, value in equivalenceClassesDict.items() if value != []]
            
    
    def __removeEquivalents(self):
        statesNotFinal = []
        equivalenceClasses: List[set] = []
        finalStates = self.__acceptanceStates.copy()
        
        equivalenceClasses.append(finalStates)
        statesNotFinal = [state for state in self.__states if state not in finalStates]
        if statesNotFinal != []:
            equivalenceClasses.append(statesNotFinal)
        # Acha as classes de equivalencia
        while True:
            oldEquivalenceClasses = equivalenceClasses.copy()
            for symbol in self.__alphabet:
                for stateGroup in equivalenceClasses:
                    equivalenceClassesCpy = equivalenceClasses.copy()
                    equivalenceClasses.remove(stateGroup)
                    equivalenceClasses.extend(self.__splitClassesOfEquivalence(equivalenceClassesCpy, stateGroup, symbol))

            if equivalenceClasses == oldEquivalenceClasses:
                break

        # Atualiza o automato com os novos estados
        oldAcceptanceStates = self.__acceptanceStates.copy()
        self.__acceptanceStates = set()
        newTransitions = list(self.__transitions)
        
        # Atualiza as transicoes
        for i, (initial, to, transition) in enumerate(newTransitions):
            newInitial = initial
            newTo = to
            for eClass in equivalenceClasses:
                if initial in eClass:
                    newInitial = ','.join(eClass)
                if to in eClass:
                    newTo = ','.join(eClass)
            newTransitions[i] = (newInitial, newTo, transition)
         
        self.__transitions = set(newTransitions)

        for eClass in equivalenceClasses:    
            # Atualiza o estado inicial   
            if self.__initialState in eClass:
                self.__initialState = ','.join(eClass)
            
            # Atualiza os estados de aceitacao 
            for acceptanceState in oldAcceptanceStates:
                if acceptanceState in eClass:
                    self.__acceptanceStates.add(','.join(eClass))

        self.__states = set([','.join(group) for group in equivalenceClasses])

    ######################################### PUBLIC #########################################

    def isDeterministic(self) -> bool:
        initials: List[tuple] = [(initial, condition) for [initial, final, condition] in self.__transitions]        
        initialsSet: set = set(initials)
        if len(initials) != len(initialsSet):
            return False
        else:
            for (_,condition) in initialsSet:
                if condition == '&': return False
        return True

    def minimize(self) -> 'FiniteAutomata':
        # Itera até remover todos estados mortos e inalcançaveis 
        while True:
            previousStates = self.__states
            self.__removeDeads()
            self.__removeUnreachables()
            if previousStates == self.__states:
                break
        
        # Faz as classes de equivalencia
        self.__removeEquivalents()
        return self