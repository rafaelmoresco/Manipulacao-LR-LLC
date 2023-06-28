from typing import Tuple, Set, Dict
from FiniteAutomata import FiniteAutomata

class FiniteAutomataUtils():
    def __init__(self) -> None:
        pass

    ######################################### PRIVATE #########################################

    def __dfaSetOp(self, d1: FiniteAutomata, d2: FiniteAutomata, union) -> FiniteAutomata:
        newDStates = self.__carteseanStates(d1.states, d2.states)
        newDAlphabet: set = d1.alphabet.union(d2.alphabet)
        newDInitialState = 'A1'+d1.initialState+';'+'A2'+d2.initialState
        newDAcceptanceStates = set()
        for state in newDStates:
            splitedState = state.split(';')
            if union:
                if splitedState[0].strip('A1') in d1.acceptanceStates or splitedState[1].strip('A2') in d2.acceptanceStates:
                    newDAcceptanceStates.add(state)
            else:
                if splitedState[0].strip('A1') in d1.acceptanceStates and splitedState[1].strip('A2') in d2.acceptanceStates:
                    newDAcceptanceStates.add(state)
        newDTransitions = self.__carteseanTransitions(d1.transitionsDict,d2.transitionsDict,newDStates)
        new = FiniteAutomata(newDStates, newDAlphabet, newDTransitions, newDInitialState, newDAcceptanceStates)
        return new

    
    def __carteseanStates(self, d1S: Set[str], d2S: Set[str]) -> Set[str]:
        dNewS: set = set()
        for s1 in d1S:
            for s2 in d2S:
                dNewS.add(('A1'+s1+';'+'A2'+s2))
        return dNewS

    def __carteseanTransitions(self, d1T: Dict[str, Set[Tuple[str, str, str]]], d2T: Dict[str, Set[Tuple[str, str, str]]], newDStates: Set[str]) -> Set[Tuple[str, str, str]]:
        new = set()
        for state in newDStates:
            splitedState = state.split(';')
            for tran1 in d1T[splitedState[0].strip('A1')]:
                for tran2 in d2T[splitedState[1].strip('A2')]:
                    if tran1[2] == tran2[2]:
                        new.add((state,'A1'+tran1[1]+';'+'A2'+tran2[1],tran1[2]))
        return new

    ######################################### PUBLIC #########################################

    def dfaIntersection(self, d1: FiniteAutomata, d2: FiniteAutomata) -> FiniteAutomata:
        return self.__dfaSetOp(d1, d2, False)
    
    def dfaUnion(self, d1: FiniteAutomata, d2: FiniteAutomata) -> FiniteAutomata:
        return self.__dfaSetOp(d1, d2, True)