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
    def transitionsDict(self) -> Dict[str, Set[Tuple[str, str, str]]]:
        return self.__transitionsDict

    @property
    def alphabet(self) -> Set[str]:
        return self.__alphabet

    @property
    def isDeterministic(self) -> bool:
        if '&' in self.__alphabet: return False
        # if len(self.__transitions) < (len(self.__states) * len(self.__alphabet)): return False
        for (_, to, _) in self.__transitions:
            if self.__isCompoundState(to) and to not in self.__states: return False
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
    
    def __isCompoundState(self, state: str) -> bool:
        '''Verifica se o estado passado é um estado "composto", ex. "q1,q2"'''
        return len(state.split(',')) > 1

    def __mapEquivalenceClassesIndexes(self, classes: List[List[str]]) -> Dict[str, int]:
        '''Mapeia as classes de equivalência passadas e gera um dicionario/map contendo a classe e seu índice'''
        classesDict: Dict[str, int] = {}
        for i, statesGroup in enumerate(classes):
            for state in statesGroup:
                if state in self.__states:
                    classesDict[state] = i
        
        classesDict['-'] = len(classes)
        return classesDict
    
    def __generateEquivalenceClasses(self, eqClasses: List[List[str]]) -> List[List[str]]:
        '''Computa novas classes de equivalência a partir da classe de equivalência passada'''
        # Gera um map que contém estado como chave e índice da classe de equivalencia como valor
        classesIndexMap: Dict[str, int] = self.__mapEquivalenceClassesIndexes(eqClasses)
        
        # Separam-se as classes de equivalência pelos seus tamanhos isolando as classes que contém somente um estado.
        # Assim, somente classes de equivalência não únicas/com mais de um estado devem ser processadas
        uniqueClasses: List[List[str]] = []
        compoundClasses: List[List[str]] = []
        for stateGroup in eqClasses:
            if len(stateGroup) > 1:
                compoundClasses.append(stateGroup)
            elif len(stateGroup) == 1:
                uniqueClasses.append(stateGroup)

        # O seguinte dicionário armazena os índices de classes de equivalência como chave, e seus estados como valor
        # Assim, conforme novos índices vão sendo gerados, os valores contidos no dicionário serão as classes de eq. resultantes
        classesCombinationsPerSymbolDict: Dict[str, List[str]] = {}
        # O processamento ocorre da seguinte forma:
        for compoundStateGroup in compoundClasses:
            for state in compoundStateGroup:
                # Para cada estado, gera-se uma combinação através do índice (classesIndexMap) da classe de equivalência resultate
                # da transição por cada símbolo. Assim, se um estado transita para a classe de índice 0 por um símbolo, e para a classe
                # de índice 1 por outro, a combinação resultate é '01'.
                eqClassCombination = ''
                for symbol in self.__alphabet:
                    eqClassCombination += str(classesIndexMap[self.__nextState(state, symbol)])
                # A combinação então gerada é utilizada como chave para o dicionário, e o estado é adicionado ao valor.
                # Ou seja, cada elemento do dicionário representa uma classe de equivalência.
                if not classesCombinationsPerSymbolDict.get(eqClassCombination):
                    classesCombinationsPerSymbolDict[eqClassCombination] = [state]
                else:
                    classesCombinationsPerSymbolDict[eqClassCombination].append(state)
        
        newClasses: List[List[str]] = list(classesCombinationsPerSymbolDict.values())
        if len(uniqueClasses) > 0:
            newClasses.extend(uniqueClasses)
        return newClasses

    def __areEquivalenceClassesEqual(self, classesA: List[List[str]], classesB: List[List[str]]) -> bool:
        '''Verifica se as duas classes de equivalência passadas são iguais (implementação tosca de .equals())'''
        if len(classesA) != len(classesB): return False

        classesSet = set()
        for statesGroup in classesA:
            classesSet.add(''.join(statesGroup))
        
        equivalents = True
        for statesGroup in classesB:
            if not ''.join(statesGroup) in classesSet:
                equivalents = False
                break
        
        return equivalents

    def __nextState(self, state: str, symbol: str) -> str:
        '''[AFD] Retorna o estado alcançado a partir da transição de initialState através de symbol'''
        for (_, to, sym) in self.__transitionsDict[state]:
            if sym == symbol: return to
        return '-'
    
    def __extractStateTransitionsBySymbol(self, state: str, symbol: str) -> Set[str]:
        '''[AFND] Retorna todos os estados alcançados a partir de uma transição de state através de symbol'''
        for (_, to, sym) in self.__transitionsDict[state]:
            if symbol == sym: return set(to.split(','))
        return {}
    
    def __stateTransitsBySymbol(self, state: str, symbol: str) -> bool:
        '''Verifica se o estado tem transições não vazias pelo símbolo passado'''
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

    def __renameCompoundStates(self) -> None:
        '''Renomeia todos os estados "compostos" para estados "simples", ex.: "q1,q2" -> "nQ1"'''
        # Define o prefixo e "índice" da label para os estados a serem renomeador
        newStatePrefix = 'nQ'
        newStateCount = 0
        for state in self.__states:
            if newStatePrefix in state:
                splitted = state.split(',')
                # Definitivamente deve ter um jeito melhor de fazer isso, mas nao consigo mais usar o cerebro
                if len(splitted) > 1:
                    count = newStateCount
                    for s in splitted:
                        count = int(s[2:]) if int(s[2:]) > count else count
                else:
                    count = int(state[2:])
                newStateCount = count+1 if newStateCount <= count else newStateCount
                
        for state in self.__states.copy():
            if not self.__isCompoundState(state): continue
            # Gera novo nome
            newStateName = newStatePrefix + str(newStateCount)
            newStateCount += 1

            # Substitui nome nas transicoes
            for transition in self.__transitions:
                (initial, to, symbol) = transition
                isNewTransition = False
                if initial == state:
                    isNewTransition = True
                    initial = newStateName
                if to == state:
                    isNewTransition = True
                    to = newStateName
                if isNewTransition:
                    self.__transitions.remove(transition)
                    self.__transitions.add((initial, to, symbol))
                    self.transitions = self.__transitions

            # Substitui nome no estado inicial
            self.__initialState = newStateName if state == self.__initialState else self.__initialState

            # Substitui nome no estado final
            for finalState in self.__acceptanceStates:
                if state == finalState:
                    self.__acceptanceStates.remove(finalState)
                    self.__acceptanceStates.add(newStateName)

            # Substitui nome na lista de estados
            self.__states.remove(state)
            self.__states.add(newStateName)

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

    def __removeEquivalents(self) -> None:
        '''Calcula as classes de equivalência e remove estados redundantes, atualizando o automato por completo'''
        finalStates = list(self.__acceptanceStates.copy())
        nonFinalStates = [state for state in self.__states if state not in finalStates]

        # Separa classes de equivalência, a princípio entre estados finais e não finais
        currentEquivalentClasses: List[List[str]] = [nonFinalStates, finalStates]
        # Divide as classes de equivalência enquanto continuam sendo divididas
        while True:
            previousEquivalentClasses = currentEquivalentClasses
            currentEquivalentClasses = self.__generateEquivalenceClasses(currentEquivalentClasses)
            if self.__areEquivalenceClassesEqual(currentEquivalentClasses, previousEquivalentClasses):
                break
        
        # Redefine estado inicial
        for stateGroup in currentEquivalentClasses:
            if self.__initialState in stateGroup:
                self.__initialState = ','.join(stateGroup)
                break
        
        # Redefine as transicoes
        classesIndexDict = self.__mapEquivalenceClassesIndexes(currentEquivalentClasses)
        newTransitions: Set[tuple] = set()
        for stateGroup in currentEquivalentClasses:
            firstState = stateGroup[0]
            newState = ','.join(stateGroup)
            for symbol in self.__alphabet:
                nextState = self.__nextState(firstState, symbol)
                if nextState != '-':
                    newTransitions.add((
                        newState,
                        ','.join(currentEquivalentClasses[classesIndexDict[nextState]]),
                        symbol
                    ))
        self.transitions = newTransitions
        
        # Redefine os estados
        self.__states = {','.join(stateGroup) for stateGroup in currentEquivalentClasses}

        # Redefine estados de aceitaçao
        self.__acceptanceStates = {newState for newState in self.__states if any(finalState in newState for finalState in finalStates)}

        # self.__renameCompoundStates()
        
    
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

        # Remove epsilon do alfabeto
        self.__alphabet.remove('&')

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
        self.__renameCompoundStates()

    def __readWord(self, word: str) -> bool:
        word = list(word)
        currentState = self.__initialState
        helperBool = True
        # Percorre todas as letras da palavra
        for letter in word:
            # Primeiro verifica se o símbolo está no alfabeto
            if letter in self.__alphabet:
                # Olha todas as transições do estado atual, procurando uma com o símbolo atual
                for transition in self.__transitionsDict[currentState]:
                    if letter in transition[2]:
                        currentState = transition[1]
                        helperBool = True
                        break
                    else:
                        helperBool = False
                # Quando não encontra uma transição pelo símbolo no estado atual, retorna falso
                if not helperBool:
                    return False
            else:
                return False
        # Ao terminar a palavra, verifica se o estado atual é um estado de aceitação
        if currentState in self.__acceptanceStates:
            return True
        else:
            return False
    ######################################### PUBLIC #########################################

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

    def minimize(self) -> 'FiniteAutomata':
        '''Minimiza a instância de FiniteAutomata, removendo estados mortos, inalcançáveis e equivalentes/redundantes'''
        if not self.isDeterministic:
            print("Tentando minimizar automato não determinístico. Efetuando processo de determinização.")
            self.determinize()
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

    def read(self, word: str) -> bool:
        # Se é um DFA, faz uma leitura direta da palavra
        if self.isDeterministic:
            return self.__readWord(word)
        # Se é um NFA, determiniza antes de ler a palavra
        else:
            self.determinize()
            return self.__readWord(word)
