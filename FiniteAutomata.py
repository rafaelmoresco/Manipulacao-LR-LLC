from typing import List, Tuple, Set, Dict

class FiniteAutomata:
    
    def __init__(self, states: Set[str], alphabet: Set[str], transitions: Set[Tuple[str, str, str]], initialState: str, acceptanceStates: Set[str]) -> None:
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
            
            if sorted(equivalenceClasses) == sorted(oldEquivalenceClasses):
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

    def __transitionsToDict(self) -> Dict[str, List[Set[Tuple[str, str, str]]]]:
        transitions = {}
        for (initial, to, transition) in self.__transitions:
            if not transitions.get(initial):
                transitions[initial] = [(initial, to, transition)]
            else:
                transitions[initial].append((initial, to, transition))
        return transitions

    def __obtainNewTransitions(self, newState: str) -> Set[Tuple[str, str, str]]:
        sortedNewStates = sorted(newState.split(','))
        transitionsDict = self.__transitionsToDict()
        
        newTransitions = set()
        for symbol in self.__alphabet:
            if symbol == '&': continue
            newTransition = set()
            for state in sortedNewStates:
                for (_, tran, sym) in transitionsDict[state]:
                    if symbol == sym:
                        [newTransition.add(t) for t in tran.split(',')]
                
            newTransition = ','.join(sorted(list(newTransition)))
            if newTransition:
                newTransitions.add((','.join(sortedNewStates), newTransition, symbol))
        
        return newTransitions

    def __epsilonRemoval(self) -> None:
        # Dicionario cuja chave é o estado e o valor é o epsilon fecho desse estado
        # Inicializa adicionando o proprio estado ao epsilon fecho
        epsilonClosure: Dict[str, set] = {state: {state} for state in self.__states}
        
        # Adiciona as transicoes restantes de epsilon-fecho para cada estado
        while True:
            oldClosure = epsilonClosure.copy()
            # Percorre as transiões e procura & transições
            for (initial, to, transition) in self.__transitions:
                if transition == '&':
                    # Percorre os itens em &* e procura a chave
                    epsilonClosure[initial] = epsilonClosure[initial].union(epsilonClosure[to])
            if oldClosure == epsilonClosure:
                break
        
        self.__initialState = ','.join(sorted(list(epsilonClosure[self.__initialState])))
        
        newStates = set()
        processedStates = set()
        newTransitions = set()
        # Itera pela primeira vez, substituindo estados por epsilon-fecho e gerando novas transicoes
        for state in epsilonClosure:
            for (newInitial, newTo, symbol) in self.__obtainNewTransitions(','.join(epsilonClosure[state])):
                newTransitions.add((newInitial, newTo, symbol))
                processedStates.add(newInitial)
                if newTo not in processedStates:
                    newStates.add(newTo)

        # Enquanto houverem novos estados, gera novas transicoes
        while newStates:
            for (newInitial, newTo, symbol) in self.__obtainNewTransitions(newStates.pop()):
                newTransitions.add((newInitial, newTo, symbol))
                processedStates.add(newInitial)
                if newTo not in processedStates:
                    newStates.add(newTo)

        # Substitui transicoes originais pelas novas geradas a partir de epsilon fecho
        self.__transitions = newTransitions

        # remove epsilon do alfabeto
        self.__alphabet.remove('&')

        # substitui o resto do automato (estados, estados de aceitacao)
        self.__states = set()
        oldAcceptanceStates = self.__acceptanceStates
        self.__acceptanceStates = set()
        for (initial, to, symbol) in self.__transitions:
            self.__states.add(initial)
            for state in initial.split(','):
                if state in oldAcceptanceStates:
                    self.__acceptanceStates.add(initial)
                    break

    def __indeterminismRemoval(self) -> None:
        pass

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

    def determinize(self) -> 'FiniteAutomata':
        if '&' in self.__alphabet:
            self.__epsilonRemoval()
        self.__indeterminismRemoval()