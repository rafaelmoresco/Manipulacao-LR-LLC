from pprint import pprint

class NFA():

    def __init__(self) -> None:
        self.temp = []

    def NFAtoDFA(self, nfa):
        # Verifica se exitem Epsilon transicoes no automato
        if '&' in nfa[0]:
            dfa = self.epsilonTran(nfa)
        else:
            dfa = self.notEpsilonTran(nfa)

        return dfa

    def epsilonTran(self, nfa):
        epsilon = []
        # Descobre em qual coluna temos a & transicao
        for i in range(len(nfa[0])):
            if nfa[0][i] == '&':
                epsilonPosition = i
        # Anota as transicoes listadas
        for i in range(len(nfa)-1):
            strip = nfa[i+1][epsilonPosition].strip('*')
            transitions = strip.split(',')
            for item in transitions:
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
                strip = nfa[i+1][j].strip('->')
                strip = strip.strip('*')
                if strip in translationDic.keys():
                    add = translationDic[strip].split(',')
                    strip = strip.split(',')
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
        return self.notEpsilonTran(res)

    def notEpsilonTran(self, nfa):
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
        
'''
teste = NFA()
aaaa = [['X', 'a', 'b', 'c', '&'], ['->*q0', 'q0', '-', '-', 'q1'], ['*q1', '-', 'q1', '-', 'q2'], ['*q2', '-', '-', 'q2', '-']]
questao7 = [['X', 'a', 'b', '&'], ['->q0', 'q0,q1', 'q2', 'q3'], ['*q1', 'q1', 'q3', 'q3'], ['*q2', '-', 'q2,q4', '-'], ['q3', 'q1,q3', 'q2,q3', 'q4'], ['q4', 'q4', 'q2', 'q3']]
preset3 = [['X','a','b','&'],['1','-','2','3'],['2','1','2','-'],['3','2,3','3','-']]
pprint(teste.epsilonTran(questao7))
'''
