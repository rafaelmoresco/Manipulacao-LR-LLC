class NFA():

    def __init__(self) -> None:
        self.temp = []

    def NFAtoDFA(self, nfa):
        if '&' in nfa[0]:
            dfa = self.epsilonTran(nfa)
        else:
            dfa = self.notEpsilonTran(nfa)

        return dfa

    def epsilonTran(self, nfa):
        epsilon = []
        
        for i in range(len(nfa[0])):
            if nfa[0][i] == '&':
                epsilonPosition = i

        for i in range(len(nfa)-1):
            epsilon.append([nfa[i+1][0]])

        for _ in range(3):
            for i in range(len(nfa)-1):
                if nfa[i+1][epsilonPosition] != '-':
                    test = []
                    test = nfa[i+1][epsilonPosition].split(',')
                    for item in test:
                        if item not in epsilon[i]:
                            print(epsilon[i])
                            epsilon[i].append(item)
        print(epsilon)
        nfa[0].pop(epsilonPosition)
        for i in range(len(nfa)-1):
            nfa[i+1].pop(epsilonPosition)
            for j in range(len(nfa[0])):
                for e in range(len(epsilon)):
                    strip = epsilon[e][0].strip('->')
                    strip = strip.strip('*')
                    if strip in nfa[i+1][j]:
                        print(epsilon[e])
                        nfa[i+1][j] = ','.join(epsilon[e])
        print(nfa)
        return self.notEpsilonTran(nfa)

    def notEpsilonTran(self, nfa):
        queue = []
        totalStates = []
        dfa = nfa
        for i in range(len(nfa)-1):
            queue.append(nfa[i+1])
            totalStates.append(nfa[i+1][0])
        while queue:
            state = queue.pop(0)
            for i in range(len(state)-1):
                if ',' in state[i+1]:
                    if state[i+1] not in totalStates:
                        totalStates.append(state[i+1])
                        newSate = self.addState(dfa, state[i+1])
                        queue.append(newSate)
                        dfa.append(newSate)
        return dfa
                        

    def addState(self, dfa, state):
        newLine = []
        newLine.append(state)
        f = True
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
aaaa = [['X', 'a', 'b', '&'], ['->q0', 'q1', 'q2', 'q1'], ['q1', 'q2,q0', 'q1', '-'], ['*q2', 'q1', 'q2', '-']]
print(teste.epsilonTran(aaaa))
'''
