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
                            if nfa[i+1][j+1] == '-':
                                nfa[i+1][j+1] = nfa[k+1][j+1]
                            else:
                                nfa[i+1][j+1] = nfa[i+1][j+1] + ',' + nfa[k+1][j+1]
        # Troca um estado por seu epsilon fecho
        for i in range(len(nfa)-1):
            for j in range(len(nfa[0])):
                strip = nfa[i+1][j].strip('->')
                strip = strip.strip('*')
                if strip in translationDic.keys():
                    nfa[i+1][j] = nfa[i+1][j].replace(strip,strip+','+translationDic[strip])
        print(nfa)
        # Executa o algoritmo sem epsilon transicoes
        return self.notEpsilonTran(nfa)

    def notEpsilonTran(self, nfa):
        queue = []
        totalStates = []
        dfa = nfa
        for i in range(len(nfa)-1):
            queue.append(nfa[i+1])
            strip = dfa[i+1][0].strip('->')
            strip = strip.strip('*')
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
        f = True
        final = False
        for i in range(len(dfa[0])-1):
            newLine.append('')
        states = state.split(',')
        for i in range(len(dfa)-1):
            strip = dfa[i+1][0].strip('->')
            strip = strip.strip('*')
            if strip in states:
                for j in range(len(dfa[0])-1):
                    if dfa[i+1][j+1] not in newLine[j+1] and dfa[i+1][j+1] != '-':
                        if f:
                            newLine[j+1] = newLine[j+1]+dfa[i+1][j+1]
                        else:
                            newLine[j+1] = newLine[j+1]+','+dfa[i+1][j+1]
                f = False
                    
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
print(teste.epsilonTran(aaaa))
'''
