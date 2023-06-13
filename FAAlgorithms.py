from pprint import pprint
from typing import List, Tuple, Set, Dict, ClassVar
from FiniteAutomata import FiniteAutomata

class NFA():

    def __init__(self) -> None:
        pass

    def NFAtoDFA(self, nfa):
        # Verifica se exitem Epsilon transicoes no automato
        if '&' in nfa[0]:
            dfa = self.epsilonTran(nfa)
        else:
            dfa = self.notEpsilonTran(nfa)

        return dfa

    def minDFA(self, dfa: list):
        transitions = []
        states = []
        finalStates = []
        # Anota os estadoss
        states, finalStates, transitions, initial = self.getProperties(dfa)
        # Remove estados inalcansáveis
        states, transitions = self.reachable(transitions, initial)
        # Atualiza lista de estados finais
        for state in finalStates:
            if state not in states:
                finalStates.remove(state)
        finalStatesCopy = finalStates[:]
        # Remove estados mortos
        states, transitions = self.alive(transitions, finalStatesCopy)
        # Remove inalcansáveis se criados no processo anterior
        states, transitions = self.reachable(transitions, initial)
        # Atualiza lista de estados finais
        for state in finalStates:
            if state not in states:
                finalStates.remove(state)
        # Atualiza o Automato
        dfa = self.dfaUpdate(dfa, states)
        # Pega as transições do automato, agora incluindo as para o estado morto
        transitionsEmpty = []
        for i in range(len(dfa)-1):
            temp = dfa[i+1][0]
            temp = temp.strip('->')
            temp = temp.strip('*')
            for j in range(len(dfa[0])-1):
                # Percorre pelos itens encontraods
                transitionsEmpty.append((temp, dfa[i+1][j+1], dfa[0][j+1]))
        # Remove estados equivalentes
        self.equivalence(states, finalStates, transitionsEmpty, dfa)
        return self.renameStates(dfa)
        
    def getProperties(self, dfa, empty=False):
        finalStates = []
        transitions = []
        states = []
        for i in range(len(dfa)-1):
            temp = dfa[i+1][0]
            # Define o estado inicial
            if temp[0] == '-' and temp[1] == '>':
                temp = temp.strip('->')
                if temp[0] == '*':
                    temp = temp.strip('*')
                    finalStates.append(temp)
                initial = temp
                states.append(temp)
            # Define os estados finais
            elif '*' == temp[0]:
                temp = temp.strip('*')
                finalStates.append(temp)
                states.append(temp)
            else:
                states.append(temp)
            # Anota as transições
            for j in range(len(dfa[0])-1):
                # Percorre pelos itens encontraods
                if empty or dfa[i+1][j+1] != '-':
                    transitions.append((temp, dfa[i+1][j+1], dfa[0][j+1]))
        return states, finalStates, transitions, initial

    def dfaUnion(self, d1: FiniteAutomata, d2: FiniteAutomata) -> FiniteAutomata:
        newDStates = self.carteseanStates(d1.states, d2.states)
        newDAlphabet = d1.alphabet.union(d2.alphabet)
        newDInitialState = 'A1'+d1.initialState+';'+'A2'+d2.initialState
        newDAcceptanceStates = set()
        for state in newDStates:
            splitedState = state.split(';')
            if splitedState[0].strip('A1') in d1.acceptanceStates or splitedState[1].strip('A2') in d2.acceptanceStates:
                newDAcceptanceStates.add(state)
        newDTransitions = self.carteseanTransitions(d1.transitions,d2.transitions,newDStates)
        new = FiniteAutomata(newDStates, newDAlphabet, newDTransitions, newDInitialState, newDAcceptanceStates)
        return new


        


    def dfaIntersection(self, d1: FiniteAutomata, d2: FiniteAutomata) -> FiniteAutomata:
        newDStates = self.cartesean(d1.states, d2.states)
        newDAlphabet = d1.alphabet.union(d2.alphabet)
        newDInitialState = 'A1'+d1.initialState+';'+'A2'+d2.initialState
        newDAcceptanceStates = set()
        for state in newDStates:
            splitedState = state.split(';')
            if splitedState[0].strip('A1') in d1.acceptanceStates and splitedState[1].strip('A2') in d2.acceptanceStates:
                newDAcceptanceStates.add(state)
        newDTransitions = self.carteseanTransitions(d1.transitions,d2.transitions,newDStates)
        new = FiniteAutomata(newDStates, newDAlphabet, newDTransitions, newDInitialState, newDAcceptanceStates)
        return new
    
    def carteseanStates(self, d1S: Set[str], d2S: Set[str]) -> Set[str]:
        dNewS: set = set()
        for s1 in d1S:
            for s2 in d2S:
                dNewS.add(('A1'+s1+';'+'A2'+s2))
        return dNewS

    def carteseanTransitions(self, d1T, d2T, newDStates):
        new = set()
        for tran1 in d1T:
            for tran2 in d2T:
                for state in newDStates:
                    splitedState = state.split(';')
                    if tran1[0] in splitedState[0].strip('A1') and tran2[0] in splitedState[1].strip('A2') and tran1[2] == tran1[2]:
                        new.add((state,'A1'+tran1[1]+';'+'A2'+tran2[1]),tran1[2])
        return new

    def equivalence(self, states, finalStates, transitions, dfa):
        helpList = []
        equivalenceClass = []
        destinationList = []
        equivalenceClass.append(finalStates)
        for state in states:
            if state not in finalStates:
                helpList.append(state)
        if helpList != []:
            equivalenceClass.append(helpList)
        deadList = []
        deadList.append('-')
        equivalenceClass.append(deadList)
        equivalent = True
        while equivalent:
            equivalent = False
            # Percorre os simbolos do Automato
            for symbol in dfa[0][1:]:
                removeList = []
                oldEquivalenceClass = equivalenceClass[:]
                # Cria uma lista para salvar os destinos
                destinationList = []
                for eClass in oldEquivalenceClass:
                    destinationList.append(-1)
                # Percorre as classes de equivalencia
                for eClass in oldEquivalenceClass:
                    if eClass[0] == '-':
                        continue
                    # Percorre as transições para encontrar o destino do primeiro item da classe
                    for tran in transitions:
                        if tran[0] == eClass[0] and tran[2] == symbol:
                            for destination in oldEquivalenceClass:
                                if tran[1] in destination:
                                    # Define o destino na lista de apoio
                                    destinationList[oldEquivalenceClass.index(eClass)] = oldEquivalenceClass.index(destination)
                                    break
                            break
                    # Variaveis para salvar as novas classes
                    newClasses = []
                    newDestinations = []
                    # Olha os outros itens da classe
                    for item in eClass[1:]:
                        for tran in transitions:
                            if tran[2] == symbol and tran[0] == item:
                                for destination in oldEquivalenceClass:
                                    # Se o destino for diferente da primeira na classe, desvia
                                    if tran[1] in destination and destinationList[oldEquivalenceClass.index(eClass)] != oldEquivalenceClass.index(destination): 
                                        equivalent = True
                                        removeList.append(item)
                                        # Se ainda não foi criado uma classe na lista de classes novas, uma é criada
                                        if len(newClasses) == 0:
                                            newClass = []
                                            newDestination = []
                                            newClass.append(item)
                                            newDestination.append(oldEquivalenceClass.index(destination))
                                            newClasses.append(newClass)
                                            newDestinations.append(newDestination)
                                            break
                                        else:
                                            exists = False
                                            # Percorre as os destinos novos e procura se encontra uma nova classe para o mesmo destino
                                            for new in newDestinations:
                                                if oldEquivalenceClass.index(destination) == new:
                                                    newClasses[newDestinations.index(new)].append(item)
                                                    exists = True
                                                    break
                                            # Se não econtrar, cria uma nova
                                            if not exists:
                                                newClass = []
                                                newDestination = []
                                                newClass.append(item)
                                                newDestination.append(oldEquivalenceClass.index(destination))
                                                newClasses.append(newClass)
                                                newDestinations.append(newDestination)
                                            break
                                else:
                                    break
                    # Remove os itens que não pertencem mais a uma classe
                    for eClass in equivalenceClass:
                        for item in eClass:
                            if item in removeList:
                                eClass.remove(item)
                                removeList.remove(item) 
                    # Adiciona os itens em suas novas classes
                    for item in newClasses:
                        equivalenceClass.append(item)
        # Transforma as classes de equivalencia em string
        helperList = []
        for eClass in equivalenceClass:
            equivalenceClass[equivalenceClass.index(eClass)] = ','.join(eClass)
            helperList.append(True)
        # Troca estados pelos estados equivalentes e remove estados repetidos
        for state in dfa[1:]:
            notRemoved = True
            sState = state[0].strip('->')
            sState = sState.strip('*')
            for eClass in equivalenceClass:
                if eClass == '-':
                    continue
                if sState in eClass:
                    if helperList[equivalenceClass.index(eClass)]:
                        dfa[dfa.index(state)][0] = dfa[dfa.index(state)][0].replace(sState, eClass)
                        helperList[equivalenceClass.index(eClass)] = False
                    else:
                        dfa.remove(state)
                        notRemoved = False
                    break
            if notRemoved:
                for j in range(len(dfa[0])-1):
                    if dfa[dfa.index(state)][j+1] == '-':
                        continue
                    for eClass in equivalenceClass:
                        if eClass == '-':
                            continue
                        strip = dfa[dfa.index(state)][j+1].strip('->')
                        strip = strip.strip('*')
                        if strip in eClass:
                            dfa[dfa.index(state)][j+1] = dfa[dfa.index(state)][j+1].replace(strip, eClass)
        return dfa                 
    
    def dfaUpdate(self, dfa, states):
        for item in dfa[1:]:
            strip = item[0].strip('->')
            strip = strip.strip('*')
            if strip not in states:
                dfa.remove(item)
            else:
                for tran in item[1:]:
                    if tran != '-' and tran not in states:
                        tran = '-'
        return dfa

    def reachable(self, transitions, initial):
        reachableStates = []
        reachableTransitions = []
        reachableStates.append(initial)
        reachable = True
        while reachable:
            reachable = False
            for item in transitions:
                if item[0] in reachableStates:
                    if item[1] not in reachableStates:    
                        reachableStates.append(item[1])
                    reachableTransitions.append(item)
                    transitions.remove(item)
                    reachable = True
        return reachableStates, reachableTransitions
        
    def alive(self, transitions, finalStates):
        aliveStates = finalStates
        aliveTransitions = []
        alive = True
        while alive:
            alive = False
            for item in transitions:
                if item[1] in aliveStates:
                    if item[0] not in aliveStates:
                        aliveStates.append(item[0])
                    aliveTransitions.append(item)
                    transitions.remove(item)
                    alive = True
        return aliveStates, aliveTransitions        

    def epsilonTran(self, nfa):
        epsilon = []
        finalStates = []
        # Descobre em qual coluna temos a & transicao
        for i in range(len(nfa[0])):
            if nfa[0][i] == '&':
                epsilonPosition = i
        # Anota as transicoes listadas
        for i in range(len(nfa)-1):
            # Encontra o que está no &
            transitions = nfa[i+1][epsilonPosition].split(',')
            # Percorre pelos itens encontraods
            for item in transitions:
                # Se o item existir, cria um par (a,b) onde a->b
                if item != '-':
                    strip = nfa[i+1][0].strip('->')
                    strip = strip.strip('*')
                    epsilon.append((strip,item))
        # Faz epsilon fecho
        oldEpsilon = []
        while oldEpsilon != epsilon:
            oldEpsilon = epsilon
            epsilon = []
            for item in oldEpsilon:
                epsilon.append(item)
            for ab in oldEpsilon:
                for bc in oldEpsilon:
                    if ab[1] == bc[0]:
                        if ((ab[0],bc[1]) not in oldEpsilon):
                            epsilon.append((ab[0],bc[1]))
        # Remove as epsilon transicoes do automato
        for i in range(len(nfa)):
            nfa[i].pop(epsilonPosition)
        # Monta um dicionario para modificar o automato
        translationDic = {}
        for item in epsilon:
            if item[0] not in translationDic.keys():
                translationDic[item[0]] = item[1]
            else:
                if item[1] not in translationDic[item[0]]:
                    translationDic[item[0]] = translationDic[item[0]] + ',' + item[1]
        # Funcao para fazer a uniao dos estados
        for i in range(len(nfa)-1):
            strip = nfa[i+1][0].strip('->')
            strip = strip.strip('*')
            if strip in translationDic.keys():
                unionStates = translationDic[strip].split(',')
                unionStates.insert(1,strip)
                for j in range(len(nfa[0])-1):
                    for k in range(len(nfa)-1):
                        strip = nfa[k+1][0].strip('->')
                        strip = strip.strip('*')
                        if strip in unionStates and i != k and nfa[k+1][j+1] != '-':
                            add = nfa[k+1][j+1].split(',')
                            add.sort()
                            if nfa[i+1][j+1] == '-':
                                nfa[i+1][j+1] = ','.join(add)
                            else:
                                for addition in add:
                                    if addition not in nfa[i+1][j+1]:
                                        nfa[i+1][j+1] = nfa[i+1][j+1] + ',' + addition
                    sort = nfa[i+1][j+1].split(',')
                    sort.sort()
                    nfa[i+1][j+1] = ','.join(sort)
        # Troca um estado por seu epsilon fecho
        for i in range(len(nfa)-1):
            for j in range(len(nfa[0])):
                final = False
                initial = False
                if '->' in nfa[i+1][j]:
                    initial = True
                if '*' in nfa[i+1][j]:
                    final = True
                    finalObject = nfa[i+1][j].strip('->')
                    finalStates.append(finalObject.strip('*'))
                strip = nfa[i+1][j].strip('->')
                strip = strip.strip('*')
                strip = strip.split(',')
                for replace in strip:
                    if replace in translationDic.keys():
                        add = translationDic[replace].split(',')
                        #strip = strip.split(',')
                        for addition in add:
                            if addition not in strip:
                                strip.append(addition)
                        strip.sort()
                        nfa[i+1][j] = ','.join(strip)
                        if final:
                            nfa[i+1][j] = '*'+nfa[i+1][j]
                        if initial:
                            nfa[i+1][j] = '->'+nfa[i+1][j]
        res = []
        [res.append(x) for x in nfa if x not in res]
        # Executa o algoritmo sem epsilon transicoes
        return self.notEpsilonTran(res,final=finalStates)

    def notEpsilonTran(self, nfa, final=[]):
        queue = []
        totalStates = []
        dfa = nfa
        for i in range(len(nfa)-1):
            queue.append(nfa[i+1])
            strip = dfa[i+1][0].strip('->')
            strip = strip.strip('*')
            if strip not in totalStates:
                totalStates.append(strip)
        while queue:
            state = queue.pop(0)
            for i in range(len(state)-1):
                if ',' in state[i+1]:
                    if state[i+1] not in totalStates:
                        totalStates.append(state[i+1].strip('*'))
                        newSate = self.addState(dfa, state[i+1])
                        queue.append(newSate)
                        dfa.append(newSate)
                    
        for i in range(len(dfa)-1):
            if '*' not in dfa[i+1][0]:
                for finalState in final:
                    if finalState in dfa[i+1][0]:
                        if '->' in dfa[i+1][0]:
                            strip = dfa[i+1][0].strip('->')
                            dfa[i+1][0] = '->*'+strip
                            break
                        else:
                            dfa[i+1][0] = '*'+dfa[i+1][0]
                            break
        dfa = self.renameStates(dfa)
        return dfa
                        
    def addState(self, dfa, state):
        newLine = []
        newLine.append(state)
        final = False
        for i in range(len(dfa[0])-1):
            newLine.append('-')
        states = state.split(',')
        states.sort()
        for i in range(len(dfa)-1):
            strip = dfa[i+1][0].strip('->')
            strip = strip.strip('*')
            strip = strip.split(',')
            check =  all(item in states for item in strip)
            if check:
                for j in range(len(dfa[0])-1):
                    add = dfa[i+1][j+1].split(',')
                    add.sort()
                    for adding in add:
                        if adding not in newLine[j+1] and adding != '-':
                            if newLine[j+1] == '-':
                                newLine[j+1] = adding
                            else:
                                newLine[j+1] = newLine[j+1]+','+adding
                                sort = newLine[j+1].split(',')
                                sort.sort()
                                newLine[j+1] = ','.join(sort) 
                if '*' in dfa[i+1][0]:
                    final = True
                else:
                    final = False
        if final:
            newLine[0] = '*' + newLine[0]
        return newLine
        
    def renameStates(self, dfa):
        newStates = {}
        for i in range(len(dfa)-1):
            strip = dfa[i+1][0].strip('->')
            strip = strip.strip('*')
            newStates[strip] = 'S'+str(i)
            dfa[i+1][0] = dfa[i+1][0].replace(strip, newStates[strip])
        for i in range((len(dfa)-1)):
            for j in range(len(dfa[0])-1):
                if dfa[i+1][j+1] != '-':
                    dfa[i+1][j+1] = dfa[i+1][j+1].replace(dfa[i+1][j+1], newStates[dfa[i+1][j+1]])
        return dfa
'''
teste = NFA()
aaaa = [['X', 'a', 'b', 'c', '&'], ['->*q0', 'q0', '-', '-', 'q1'], ['*q1', '-', 'q1', '-', 'q2'], ['*q2', '-', '-', 'q2', '-']]
questao7 = [['X', 'a', 'b', '&'], ['->q0', 'q0,q1', 'q2', 'q3'], ['*q1', 'q1', 'q3', 'q3'], ['*q2', '-', 'q2,q4', '-'], ['q3', 'q1,q3', 'q2,q3', 'q4'], ['q4', 'q4', 'q2', 'q3']]
preset3 = [['X','a','b','&'],['->1','-','2','3'],['*2','1','2','-'],['3','2,3','3','-']]
pprint(teste.minDFA(teste.epsilonTran(questao7)))
'''