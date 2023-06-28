from typing import Iterable, List, Set, Dict, Tuple

class ContextFreeGrammar:
    def __init__(self, initialSymbol: str, terminals: Set[str], nonTerminals: Set[str], productions: Dict[str, Set[Tuple[str]]]):
        '''
        @param productions é um dicionário contendo como chave o símbolo e valor um set de tuplas em que cada uma contém os símbolos de uma produção.
            ex: S -> a | AbC fica { 'S': { ('a',), ('A', 'b', 'C') } }
        '''
        self.__initialSymbol: str = initialSymbol
        self.__nonTerminals: Set[str] = nonTerminals
        self.__terminals: Set[str] = terminals.union({'&'})
        self.__productions: Dict[str, Set[Tuple]] = productions
        self.__firsts: Dict[str, Set[str]] = dict()
        self.__follows: Dict[str, Set[str]] = dict()

    @property
    def initialSymbol(self) -> str:
        return self.__initialSymbol

    @property
    def nonTerminals(self) -> Set[str]:
        return self.__nonTerminals

    @property
    def terminals(self) -> Set[str]:
        return self.__terminals
    
    @property
    def productions(self) -> Dict[str, Set[Tuple]]:
        return self.__productions

    @property
    def firsts(self) -> Dict[str, Set[str]]:
        self.__calcFirsts()
        return self.__firsts
    
    @property
    def follows(self) -> Dict[str, Set[str]]:
        self.__calcFollows()
        return self.__follows
    
    @property
    def specialChars(self) -> List[str]:
        return ["'",'!']

    def __str__(self) -> str:
        return f'Símbolo inicial: {self.__initialSymbol}\n' +\
            f'Símbolos terminais: {self.__terminals}\n' +\
            f'Símbolos Não Terminais: {self.__nonTerminals}\n' +\
            f'Gramática:\n\n' + self.__productionsToStr()

    ######################################### PRIVATE #########################################

    #################### Auxiliares ####################
    def __addProduction(self, symbol: str, constraint: str) -> None:
        '''Adiciona uma produção ao símbolo'''
        if symbol not in self.__productions:
            self.__productions[symbol] = set()
        production = []
        # Necessário para certificar-se que um símbolo seguido de um caracter especial é uma só produção, ex: (S',) ao invés de (S,')
        for i in range(len(constraint)):
            char = constraint[i]
            if i > 0 and char in self.specialChars:
                production[-1] = production[-1] + char
            else:
                production.append(char)
        self.__productions[symbol].add(tuple(production))

    def __removeProduction(self, symbol: str, constraint: str) -> None:
        '''Remove a produção do símbolo'''
        if symbol in self.__productions:
            self.__productions[symbol].discard(constraint)

    def __productionsToStr(self) -> str:
        '''Formata o dicionário de produções em uma string de gramática'''
        full = ''
        for symbol in self.__productions:
            line = symbol + ' -> '
            line += ' | '.join(map(lambda prod: ' '.join(prod), self.__productions[symbol]))
            full += line + '\n'
        return full
    
    def __getFirstsFromProduction(self, prod: str) -> Set[str]:
        '''Calcula e retorna os firsts de uma determinada cadeia/produção'''
        firsts = set()
        isProdNullable = True
        # Pra cada símbolo na produção
        for symbol in prod:
            # Obtém os firsts pro símbolo
            sFirsts = self.__getAndSetFirstsOfSymbol(symbol)
            # Se houver &, descarta porque a produção original pode não ser anulável
            sFirsts.discard('&')
            # Une os firsts do símbolo original com os obtidos pelo novo símbolo
            firsts = firsts.union(sFirsts)
            # Se o novo símbolo não pode gerar palavra vazia, não há porque continuar
            if '&' not in self.__firsts[symbol]:
                isProdNullable = False
                break
        # Se a produção é anulável por completa, o símbolo pode gerar palavra vazia, portanto epsilon é um first
        if isProdNullable: firsts.add('&')
        return firsts
    
    #################### Regras/Lógicas ####################
    def __calcFirsts(self) -> None:
        '''Calcula os firsts de cada símbolo não terminal e atualiza o atributo __firsts'''
        for symbol in self.__productions:
            self.__getAndSetFirstsOfSymbol(symbol)
    
    def __getAndSetFirstsOfSymbol(self, symbol: str) -> Set[str]:
        '''Calcula e retorna os firsts para o símbolo, atualizando o atributo firsts da classe'''
        # Condição de parada, se ja calculou, retorna os calculados
        if symbol in self.__firsts:
            return self.__firsts[symbol].copy()
        
        # Condição de parada, se é terminal, retorna sí mesmo
        if symbol in self.__terminals:
            self.__firsts[symbol] = set(symbol)
            return set(symbol)
        
        firsts = set()
        # Pra cada produção pelo símbolo
        for prod in self.__productions.get(symbol, []):    
            # Se a produção começa com um terminal, ele é um first pro símbolo
            if prod[0] in self.__terminals:
                firsts.add(prod[0])
            # Se não, obtem os firsts da cadeia e faz a uniao com os já obtidos
            else:
                firsts = firsts.union(self.__getFirstsFromProduction(prod))
        self.__firsts[symbol] = firsts.copy()
        return firsts
    
    def __calcFollows(self) -> None:
        '''Calcula os follows de cada símbolo não terminal e atualiza o atributo __follows'''
        # Calcula firsts se ja nao foram calculados
        if not self.__firsts: self.__calcFirsts()

        # Inicializa follows
        for symbol in self.__productions:
            self.__follows[symbol] = set()
        
        # Adiciona final de sentença para os follows do símbolo inicial
        self.__follows[self.__initialSymbol].add('$')
        
        # Itera até que nao hajam mais mudanças nos follows
        while True:
            # salva os follows antigos
            oldFollows = self.__follows.copy()

            # popula o dicionario de follows para cada simbolo
            for symbol in self.__productions:
                self.__getAndSetFollowsOfSymbol(symbol)
            
            # se nao houve mudanças entre o antigo e o novo, vaza
            if oldFollows == self.__follows:
                break

    def __getAndSetFollowsOfSymbol(self, symbol: str) -> Set[str]:
        '''Calcula e retorna os follows para o símbolo, atualizando o atributo follows da classe'''
        follows = set()
        follows = follows.union(self.__follows[symbol])
        for nonTerminal, productions in self.__productions.items():
            for prod in productions:
                for i, prodSymbol in enumerate(prod):
                    if prodSymbol == symbol:
                        counter = i
                        while counter < (len(prod)-1):
                            nextSymbol = prod[counter+1]
                            if nextSymbol in self.__terminals:
                                follows.add(nextSymbol)
                                break
                            else:
                                follows = follows.union((self.__firsts[nextSymbol]-{'&'}))
                                if '&' in self.__firsts[nextSymbol]:
                                    counter += 1
                                else:
                                    break
                        if counter == (len(prod)-1):
                            follows = follows.union(self.__follows[nonTerminal])
        self.__follows[symbol] = follows.copy()
        return follows
    
    def __getIndirectNonDeterministicProductions(self) -> Dict[str, Set[Tuple]]:
        '''Percorre a gramática procurando por produções não determinística e retorna um dicionário {símbolo: produções não determinísticas}'''
        self.__calcFirsts() # Atualiza os firsts
        nonDetProds = {}
        for symbol in self.__productions:
            productionsFirsts: List[Tuple[Tuple, Set]] = [] # Lista de tuplas contendo produção já percorrida e firsts daquela produção
            nonDets: Set[Tuple] = set() # Produções nao deterministicas
            # Percorre todas as produções
            for prod in self.__productions[symbol]:
                # Verifica se a produção é não determinística por "derivação",
                # verificando pra cada símbolo na produção
                # se o símbolo é não terminal, anulável e possui intersecção de seus firsts com o resto da produção
                for i, sym in enumerate(prod):
                    if sym in self.__nonTerminals and\
                            '&' in self.__firsts[sym] and\
                            len(self.__firsts[sym].intersection(self.__getFirstsFromProduction(prod[i+1:]))) > 0:
                        nonDets.add(prod)

                # Verifica se a produção é não deterministica comparando os firsts da produção com os firsts
                # das produções percorridas. Se possui intersecção então há não determinismo
                firsts = self.__getFirstsFromProduction(prod)
                for prodFirsts in productionsFirsts:
                    if len(firsts.intersection(prodFirsts[1])) > 0:
                        nonDets.add(prod)
                        nonDets.add(prodFirsts[0])
                productionsFirsts.append( (prod, firsts) )

            if nonDets:
                nonDetProds[symbol] = nonDets
        return nonDetProds
            
    def __convertIndirectNonDeterministicProductions(self, indirectNonDetProds: Dict[str, Set[Tuple]]):
        '''Percorre a gramática, convertendo as produções não determinísticas indiretas passadas em diretas'''
        for symbol in self.__productions:
            # Remove as produções não determinísticas da gramática
            for prod in indirectNonDetProds.get(symbol, []):
                self.__productions[symbol].discard(prod)

            # Pra cada produção não determinística indireta
            for prod in indirectNonDetProds.get(symbol, []):
                # obtém as derivações da produção
                derivations = self.__derive(prod)
                
                # Adiciona a derivação por & se possui (tuple vazia)
                if tuple() in derivations:
                    derivations.remove(tuple())
                    derivations.append(tuple('&'))

                # Transforma as produções em não determinísticas diretas, 
                # adicionando uma produção para cada derivação a partir do símbolo original
                for derivation in derivations:
                    self.__nonTerminals.add(symbol)
                    self.__addProduction(symbol, derivation)
        
    def __derive(self, production: Tuple) -> List[Tuple[str]]:
        '''Retorna uma lista com as produções deriváveis a partir da produção passada'''
        # Condição de parada
        if len(production) == 0:
            return [tuple()]
        # Se o símbolo mais a esquerda da produção é terminal, 
        # retorna uma lista contendo esse símbolo concatenado a todas as derivações possíveis
        # dos símbolos posteriores
        if production[0] in self.__terminals:
            return [production[0] + ''.join(prod) for prod in self.__derive(production[1:])]
        # Se for um não terminal e possuir produções a partir dele
        elif production[0] in self.__productions:
            out = [] # produções de saída
            # obtém todas as derivações possíveis dos símbolos posteriores
            derivations = self.__derive(production[1:])
            a = 1
            # então, pra cada produção pelo símbolo mais a esquerda
            for prod in self.__productions[production[0]]:
                # se a produção é &, copia todas as derivações possíveis dos símbolos à direita, anulando o símbolo à esquerda
                if prod == tuple('&'):
                    out += derivations
                # se não, copia a produção e concatena todas as derivações possíveis dos símbolos à direita
                else:
                    out += [''.join(prod) + ''.join(d) for d in derivations]
            return out
    
    def __getPrefixesOfProductions(self) -> Dict[str, List[Tuple]]:
        '''Retorna um dicionario contendo símbolo como chave e uma lista de tuplas de terminais contendo os maiores prefixos possíveis por símbolo/produção'''
        nonDetProds = {}
        for symbol in self.__productions:
            processedProds = []
            # P/ cada produção por símbolo
            for prod in self.__productions[symbol]:
                # Se é a primeira iteração, adiciona aos processados e continua
                if len(processedProds) == 0:
                    processedProds.append(prod)
                    continue
                foundCommon = False
                # Procura pelo máximo "prefixo" comum entre as produções, ex: aa, aae, aaa = aa
                for i, processedProd in enumerate(processedProds):
                    maxPref = []
                    for j in range(min(len(prod), len(processedProd))):
                        if prod[j] == processedProd[j]:
                            maxPref.append(prod[j])
                        else: 
                            break
                    # Se encontrou, atualiza o respectivo item nos processados
                    if len(maxPref) > 0:
                        processedProds[i] = tuple(maxPref)
                        foundCommon = True
                # Se nao encontrou, apenas marca a producao nos processados
                if not foundCommon:
                    processedProds.append(prod)

            nonDetProds[symbol] = processedProds
        return nonDetProds

    def __removeDirectNonDeterministicProductions(self) -> None:
        '''Percorre a gramática, convertendo as produções não determinísticas diretas em determinísticas, criando novos símbolos e atualizando o dicionário'''
        allSymbolsPrefixes = self.__getPrefixesOfProductions()
        productions = self.__productions # copia __productions
        self.__productions = {} # zera productions para utilizar __addProduction
        for symbol, prefixes in allSymbolsPrefixes.items():
            newSymbolCounter = 1
            for prefix in prefixes:
                # Pra cada simbolo, pra cada prefixo
                prodsToGenerate = []
                # compara com cada produção original do símbolo
                for prod in productions[symbol]:
                    # Marca produções com prefixo em comum para que sejam processadas, ex: aab, aac (prefixo é aa)
                    if len(prefix) <= len(prod) and prefix == prod[:len(prefix)]:
                        prodsToGenerate.append(prod)
                # Se há produções p/ serem processadas
                if len(prodsToGenerate) > 1:
                    # Gera novo símbolo e o adiciona ao set de não terminais
                    newSymbol = symbol +"'"*newSymbolCounter
                    self.__nonTerminals.add(newSymbol)
                    newSymbolCounter += 1
                    # Adiciona nova produção ao símbolo original, contendo o prefixo determinizado da produção + novo símbolo, ex S -> aaS'
                    self.__addProduction(symbol, prefix + (newSymbol,) )
                    # Pra cada produção a ser processada
                    for newProd in prodsToGenerate:
                        # Adiciona uma produção ao novo símbolo gerado contendo o conteúdo depois de cada prefixo ou &, ex: S' -> S | &
                        newProd = newProd[len(prefix):]
                        newProd = newProd if len(newProd) > 0 else tuple('&')
                        self.__addProduction(newSymbol, newProd)
                # Se não há produções a serem processadas, readiciona as produções originais ao símbolo
                else:
                    self.__addProduction(symbol, prefix)

    def __removeCircularProductions(self) -> None:
        '''Remove produções circulares unitárias, ex: A -> A'''
        for sym in self.__productions:
            for _ in self.__productions[sym].copy():
                self.__productions[sym].discard(tuple(sym))
    
    def __convertLeftmostIndirectRecursionsOfSymbol(self, symbol: str) -> None:
        '''Percorre a gramática, convertendo as produções não recursivas à esquerda indiretas em diretas do símbolo não terminal passado'''
        # calcula índice do símbolo
        i = list(self.__productions.keys()).index(symbol)

        # Para cada símbolo não terminal anterior (na ordem da gramática)
        for previousSymbol in list(self.__productions.keys())[:i]:
            # Percorre todas as produções do símbolo original, procurando por recursoes à esquerda dos símbolos anteriores
            for prod in self.__productions[symbol].copy():
                if prod[0] != previousSymbol: continue
                # Se encontra essas recursões indiretas, remove essas produções recursivas
                self.__removeProduction(symbol, prod)
                # Adiciona novas produções para o símbolo original, com todas as derivações possíveis da produção antes recursiva
                # Ou seja, substitui as produções recursivas indiretas por recursivas diretas
                for previousProd in self.__productions[previousSymbol]:
                    if previousProd != tuple('&'):
                        self.__addProduction(symbol, previousProd + prod[1:])
                    else:
                        self.__addProduction(symbol, prod[1:])
    
    def __removeLeftmostDirectRecursionsOfSymbol(self, symbol: str) -> None:
        # Detecta por recursoes diretas à esquerda, separando as producoes em duas listas
        recursives, nonRecursives = [], []
        for prod in self.__productions[symbol]:
            if prod[0] == symbol:
                recursives.append(prod[1:]) # adiciona à lista removendo o símbolo recursivo à esquerda
            else:
                nonRecursives.append(prod)
        
        # Se há recursoes
        if recursives:
            # Cria novo símbolo
            newSymbol = symbol+'!'
            self.__nonTerminals.add(newSymbol)
            
            # Substitui as producoes.
            # Para as producoes recursivas, adiciona novas producoes pelo novo símbolo
            # concatenando a produção recursiva (sem a recursao à esquerda) com o novo símbolo criado. Também adiciona & como produção
            self.__productions[newSymbol] = set(tuple('&'))
            for prod in recursives:
                newProd = prod + (newSymbol,)
                self.__productions[newSymbol].add(prod + (newSymbol,))
            # Para as produções nao recursivas, adiciona novas produções pelo símbolo original
            # concatenando a produção nao recursiva com o novo símbolo criado
            self.__productions[symbol] = set()
            for prod in nonRecursives:
                newProd = tuple('&') if prod == tuple('&') else prod + (newSymbol,)
                self.__productions[symbol].add(newProd)

        
    ######################################### PUBLIC #########################################
    def outputToFile(self, filepath='gerados/GLC.txt'):
        '''Transforma as produções e as escreve em um arquivo em forma de gramática'''
        with open(filepath, 'w') as file:
            file.write(self.__productionsToStr())

    def factorate(self, depth=10) -> bool:
        '''Fatora a gramática, tentando converter, a cada iteração, as produções não determinísticas diretas e depois indiretas'''
        # Remove nao determinismos diretos
        self.__removeDirectNonDeterministicProductions()
        isFactorable = False
        for _ in range(depth):
            # Converte não determinismo indiretos em diretos
            indirectNonDetProds = self.__getIndirectNonDeterministicProductions()
            self.__convertIndirectNonDeterministicProductions(indirectNonDetProds)
            # Remove nao determinismos diretos restantes
            self.__removeDirectNonDeterministicProductions()
            # Se nao houve detecçao de indiretos, nao precisa de outra iteração
            if not indirectNonDetProds:
                isFactorable = True
                break
        return isFactorable

    def removeLeftmostRecursions(self) -> None:
        '''Atualiza a gramática convertendo e removendo as recursões à esquerda'''        
        self.__removeCircularProductions()
        for symbol in self.__productions.copy():
            self.__convertLeftmostIndirectRecursionsOfSymbol(symbol)
            self.__removeLeftmostDirectRecursionsOfSymbol(symbol)
        