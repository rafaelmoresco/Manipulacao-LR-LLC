from pprint import pprint
from typing import List, Tuple, Set, Dict, ClassVar
from FiniteAutomata import FiniteAutomata

class NFA():

    def __init__(self) -> None:
        pass

    def dfaUnion(self, d1: FiniteAutomata, d2: FiniteAutomata) -> FiniteAutomata:
        newDStates = self.carteseanStates(d1.states, d2.states)
        newDAlphabet: set = d1.alphabet.union(d2.alphabet)
        newDInitialState = 'A1'+d1.initialState+';'+'A2'+d2.initialState
        newDAcceptanceStates = set()
        for state in newDStates:
            splitedState = state.split(';')
            if splitedState[0].strip('A1') in d1.acceptanceStates or splitedState[1].strip('A2') in d2.acceptanceStates:
                newDAcceptanceStates.add(state)
        newDTransitions = self.carteseanTransitions(d1.transitionsDict,d2.transitionsDict,newDStates)
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
        newDTransitions = self.carteseanTransitions(d1.transitionsDict,d2.transitionsDict,newDStates)
        new = FiniteAutomata(newDStates, newDAlphabet, newDTransitions, newDInitialState, newDAcceptanceStates)
        return new
    
    def carteseanStates(self, d1S: Set[str], d2S: Set[str]) -> Set[str]:
        dNewS: set = set()
        for s1 in d1S:
            for s2 in d2S:
                dNewS.add(('A1'+s1+';'+'A2'+s2))
        return dNewS

    def carteseanTransitions(self, d1T: Dict[str, Set[Tuple[str, str, str]]], d2T: Dict[str, Set[Tuple[str, str, str]]], newDStates: Set[str]) -> Set[Tuple[str, str, str]]:
        new = set()
        print(d1T)
        for state in newDStates:
            splitedState = state.split(';')
            print(splitedState)
            for tran1 in d1T[splitedState[0].strip('A1')]:
                for tran2 in d2T[splitedState[1].strip('A2')]:
                    if tran1[2] == tran2[2]:
                        new.add((state,'A1'+tran1[1]+';'+'A2'+tran2[1],tran1[2]))
        return new

'''
teste = NFA()
aaaa = [['X', 'a', 'b', 'c', '&'], ['->*q0', 'q0', '-', '-', 'q1'], ['*q1', '-', 'q1', '-', 'q2'], ['*q2', '-', '-', 'q2', '-']]
questao7 = [['X', 'a', 'b', '&'], ['->q0', 'q0,q1', 'q2', 'q3'], ['*q1', 'q1', 'q3', 'q3'], ['*q2', '-', 'q2,q4', '-'], ['q3', 'q1,q3', 'q2,q3', 'q4'], ['q4', 'q4', 'q2', 'q3']]
preset3 = [['X','a','b','&'],['->1','-','2','3'],['*2','1','2','-'],['3','2,3','3','-']]
pprint(teste.minDFA(teste.epsilonTran(questao7)))
'''