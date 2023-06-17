from typing import List, Tuple, Set, Dict

class FiniteAutomata:
    
    def __init__(self, states: Set[str], alphabet: Set[str], transitions: Set[Tuple[str, str, str]], initialState: str, acceptanceStates: Set[str]) -> None:
        '''
        @param transitions Lista de tuplas em que cada tupla contem, nessa ordem: estado de, estado para, transita por
        '''
        self.__states = states
        self.__alphabet = alphabet
        self.__transitions = transitions
        self.__transitionsDict = self.__transitionsToDict()
        self.__initialState = initialState
        self.__acceptanceStates = acceptanceStates

    def __str__(self):
        return f'Estados: {self.__states}\n' +\
            f'Alfabeto: {self.__alphabet}\n' +\
            f'Transicoes: {self.__transitionsDict}\n' +\
            f'Estado Inicial: {self.__initialState}\n' +\
            f'Estados de Aceitacao: {self.__acceptanceStates}'
    
    @property
    def states(self) -> Set[str]:
        return self.__states
    
    @property
    def initialState(self) -> str:
        return self.__initialState
    
    @property
    def acceptanceStates(self) -> Set[str]:
        return self.__acceptanceStates
    
    @property
    def transitions(self) -> Set[Tuple[str, str, str]]:
        return self.__transitions
    
    @property
    def alphabet(self) -> Set[str]:
        return self.__alphabet

    @property
    def isDeterministic(self) -> bool:
        if '&' in self.__alphabet: return False
        # if len(self.__transitions) < (len(self.__states) * len(self.__alphabet)): return False
        for (_, to, _) in self.__transitions:
            if self.__isCompositeState(to) and to not in self.__states: return False
        return True
    
    @transitions.setter
    def transitions(self, value: Set[Tuple[str, str, str]]):
        self.__transitions = value
        self.__transitionsDict = self.__transitionsToDict()

    def __transitionsToDict(self) -> Dict[str, Set[Tuple[str, str, str]]]:
        transitions = {}
        for (initial, to, transition) in self.__transitions:
            if not transitions.get(initial):
                transitions[initial] = {(initial, to, transition)}
            else:
                transitions[initial].add((initial, to, transition))
        return transitions
    
    ######################################### PRIVATE #########################################

    #################### Auxiliares ####################

    def __splitClassesOfEquivalence(self, equivalenceClasses, splittable, symbol) -> List:
        '''Calcula e retorna novas classes de equivalência de splittable'''
        equivalenceClassesDict = {','.join(key): [] for key in equivalenceClasses}
        equivalenceClassesDict['-'] = []

        for x in splittable:
            nextState = self.__nextState(x, symbol) ## calcula para onde o estado vai
            for key, value in equivalenceClassesDict.items():
                if nextState in key.split(','):
                    value.append(x)
                    break

        return [value for _, value in equivalenceClassesDict.items() if value != []]

    def __nextState(self, initialState: str, symbol: str) -> str:
        '''[Apenas AFD] Retorna o estado alcançado por initialState através do símbolo symbol. Se não houver, retorna "-"'''
        for (initial, to, transitionsBy) in self.__transitions:
            if initialState == initial and transitionsBy == symbol:
                return to
        return '-'
    
    def __isCompositeState(self, state: str) -> bool:
        '''Verifica se o estado passado é um "estado composto", ex. "q1,q2"'''
        return len(state.split(',')) > 1

    def __stateTransitsBySymbol(self, state: str, symbol: str) -> bool:
        for (_, _, s) in self.__transitionsDict[state]:
            if s == symbol: return True
        return False
    
    def __obtainNewTransitions(self, state: str) -> Set[Tuple[str, str, str]]:
        '''Obtem as transicoes a partir do estado passado, ex "q1,q2"'''
        sortedStates = sorted(state.split(','))
        
        newTransitions = set()
        for symbol in self.__alphabet:
            if symbol == '&': continue
            newTransition = set()
            for state in sortedStates:
                for (_, tran, sym) in self.__transitionsDict[state]:
                    if symbol == sym:
                        [newTransition.add(t) for t in tran.split(',')]
                
            newTransition = ','.join(sorted(list(newTransition)))
            if newTransition:
                newTransitions.add((','.join(sortedStates), newTransition, symbol))
        
        return newTransitions
    
    def __extractStateTransitionsBySymbol(self, state: str, symbol: str) -> Set[str]:
        for (_, to, sym) in self.__transitionsDict[state]:
            if symbol == sym: return set(to.split(','))
        return {}

    def __obtainEpsilonClosureOfState(self, state: str) -> Set[str]:
        '''Computa e retorna o epsilon-fecho do estado'''
        epsilonStates: Set[str] = {state}
        unprocessedStates = [state]
        while unprocessedStates:
            state = unprocessedStates.pop()
            for epsilonTransitionState in self.__extractStateTransitionsBySymbol(state, '&'):
                if epsilonTransitionState not in epsilonStates:
                    unprocessedStates.append(epsilonTransitionState)
                    epsilonStates.add(epsilonTransitionState)
        
        return epsilonStates

    def __obtainReachableStatesByStatesAndSymbol(self, states: Set[str], symbol: str) -> Set[str]:
        '''Retorna os estados alcançados pelos estados passados através do symbol'''
        transitionExtractedStates = set()
        for state in states:
            [transitionExtractedStates.add(extracted) for extracted in self.__extractStateTransitionsBySymbol(state, symbol)]
        
        finalStates = transitionExtractedStates.copy()
        
        for extractedState in transitionExtractedStates:
            for epsilonClosuredState in self.__obtainEpsilonClosureOfState(extractedState):
                finalStates.add(epsilonClosuredState)

        return finalStates
    
    def __updateAcceptanceStates(self) -> None:
        '''Compara os estados do automato com os estados de aceitação, marcando novos estados de aceitação se houverem'''
        newAcceptanceStates = set()
        for state in self.__states:
            for s in state.split(','):
                if s in self.__acceptanceStates:
                    newAcceptanceStates.add(state)
                    break
        [self.__acceptanceStates.add(newAccState) for newAccState in newAcceptanceStates]

    #################### Regras/Lógicas ####################

    def __removeUnreachableStates(self) -> None:
        '''Calcula e remove estados inalcançáveis, atualizando o automato por completo'''
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
        self.transitions = reachableTransitions
        # Remove dos estados de aceitação os estados inalcançaveis
        self.__acceptanceStates = set([state for state in self.__acceptanceStates if state in reachableStates])

    def __removeDeadStates(self) -> None:
        '''Calcula e remove estados mortos, atualizando o automato por completo'''
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
        self.transitions = aliveTransitions
                    
    def __removeEquivalents(self):
        '''Calcula as classes de equivalência e remove estados redundantes, atualizando o automato por completo'''
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
         
        self.transitions = set(newTransitions)

        for eClass in equivalenceClasses:    
            # Atualiza o estado inicial   
            if self.__initialState in eClass:
                self.__initialState = ','.join(eClass)
            
            # Atualiza os estados de aceitacao 
            for acceptanceState in oldAcceptanceStates:
                if acceptanceState in eClass:
                    self.__acceptanceStates.add(','.join(eClass))

        self.__states = set([','.join(group) for group in equivalenceClasses])
    
    def __convertEpsilonTransitions(self) -> None:
        '''Elimina as transicoes por épsilon, substituindo as transicoes dos estados a partir dos cálculos de epsilon-fecho correspondentes'''
        epsilonClosureOfStateCache: Dict[str, Set[str]] = {}
        for symbol in self.__alphabet:
            for state, stateTransitions in self.__transitionsDict.items():
                # Pega dos fechos computados para o estado ou computa e adiciona se nao houver
                epsilonClosuredStates = epsilonClosureOfStateCache.get(state) or self.__obtainEpsilonClosureOfState(state)
                if not epsilonClosureOfStateCache.get(state):
                    epsilonClosureOfStateCache[state] = epsilonClosuredStates
                
                # Obtem o resto dos estados alcançáveis por epsilon
                epsilonClosuredStatesForSymbol = self.__obtainReachableStatesByStatesAndSymbol(list(epsilonClosuredStates), symbol)

                # Substitui a respectiva transicao pelo epsilon-fecho calculado
                for transition in stateTransitions:
                    if transition[2] == symbol: self.__transitions.remove(transition)
                if epsilonClosuredStatesForSymbol:
                    self.__transitions.add((state, ','.join(sorted(list((epsilonClosuredStatesForSymbol)))), symbol))
                self.transitions = self.__transitions # trigger @property.set pq python
        
        # Remove as transicoes por epsilon
        for transition in list(self.__transitions):
            if transition[2] == '&': self.__transitions.remove(transition)
        self.transitions = self.__transitions # trigger @property.set pq python

    def __convertIndeterministicTransitions(self) -> None:
        '''Elimina as transicoes indeterministicas, gerando novos estados com transicoes correspondentes'''
        determinizedStates = set()
        determinizedTransitions = set()
        unprocessedStates = self.__states.copy()
        # Percorre todos os estados originais do automato e estados novos gerados a partir do processo de determinização
        while unprocessedStates:
            # Pega um estado e o marca como determinizado
            state = unprocessedStates.pop()
            determinizedStates.add(state)
            # Se é um estado original, copia suas transições para transições determinizadas
            # Se é um estado novo, gera novas transicoes as adiciona às transições determinizadas
            for (initial, to, symbol) in (self.__transitionsDict.get(state) or self.__obtainNewTransitions(state)):
                determinizedTransitions.add((initial, to, symbol))
                # Ao se deparar com um estado não determinizado, adiciona à lista para futura iteração
                if to not in determinizedStates:
                    unprocessedStates.add(to)
        
        # Atualiza o automato
        self.__states = determinizedStates
        self.transitions = determinizedTransitions # transitions ao inves de __transitions pra invocar @property.set (porque python)
        self.__updateAcceptanceStates()

    

    ######################################### PUBLIC #########################################

    def minimize(self) -> 'FiniteAutomata':
        '''Minimiza a instância de FiniteAutomata, removendo estados mortos, inalcançáveis e equivalentes/redundantes'''
        # Itera até remover todos estados mortos e inalcançaveis 
        while True:
            previousStates = self.__states
            self.__removeDeadStates()
            self.__removeUnreachableStates()
            if previousStates == self.__states:
                break
        
        # Calcula as classes de equivalência e substitui/remove as redundantes
        self.__removeEquivalents()
        return self

    def determinize(self) -> 'FiniteAutomata':
        '''Determiniza a instância de FiniteAutomata se for indeterminística (contendo transições por épsilon-fecho ou não), caso contrário retorna ela mesma'''
        # Se é um DFA, nao faz nada
        if self.isDeterministic: 
            return self
        # Se possui transicoes por epsilon, converte em nao-deterministico sem transicoes por epsilon
        if '&' in self.__alphabet:
            self.__convertEpsilonTransitions()
        # Converte em um automato determinístico
        self.__convertIndeterministicTransitions()
        return self
    
    def read(self, word: str) -> bool:
        word = list(word)
        currentState = self.__initialState
        helperBool = True
        for letter in word:
            if letter in self.__alphabet:
                for transition in self.__transitionsDict[currentState]:
                    if letter in transition[2]:
                        currentState = transition[1]
                        helperBool = True
                        break
                    else:
                        helperBool = False
                if not helperBool:
                    return False
            else:
                return False
        if currentState in self.__acceptanceStates:
            return True