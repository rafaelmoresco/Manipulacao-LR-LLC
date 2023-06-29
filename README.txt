UNIVERSIDADE FEDERAL DE SANTA CATARINA - DEPARTAMENTO DE INFORMÁTICA E ESTATÍSTICA
FLORIANÓPOLIS, 28 DE JUNHO DE 2023
INTEGRANTES
    BERNARDO GOMES DUARTE (19100520)
    EDUARDO BORGES SIQUEIRA (19100523)
    RAFAEL MORESCO VIEIRA (19200435)
    SAMUEL MOREIRA RANSOLIN (19102348)

Manipulação de Linguagens Regulares e Linguagens Livres de Contexto

Este trabalho foi desenvolvido para a disciplina Linguagens Formais e Compiladores
(INE5421), e tem como objetivo demonstrar o domínio sobre Linguagens Regulares e
Linguages Livres de Contexto.

DETALHES SOBRE A APLICAÇÃO:

Este trabalho foi desenvolvido em Python3 (versão >=3.8), utilizando as bibliotecas padrões.
Para rodar o programa, execute o arquivo main.py no console através do comando:
    python3 main.py
Digite então a operação desejada ou `disponivel` para listar todas as operações disponíveis.
O programa requisitará o nome (com caminho relativo ao main.py) do arquivo de entrada respectivo 
à operação escolhida. A especificação desses arquivos se encontra mais adiante neste arquivo.
Realizada a operação, o programa gera um arquivo contendo o automato/gr/glc resultante.

DETALHES SOBRE A MODELAGEM:

O código foi desenvolvido sobre o paradigma de orientação a objetos. O arquivo/módulo main
é responsável por instanciar todas as classes e servir de interface com o usuário.
Além do main, a aplicação possui outros módulos, cada um é responsável por implementar seus
respectivos algoritmos em relação à sua classe. Seguem mais detalhes:
    reader.py - Não necessariamente relacionado ao trabalho em sí, mas implementa uma classe
        responsável por fazer a leitura dos arquivos de texto;
    FiniteAutomata.py - Implementa uma classe que faz a manipulação de um autômato finito.
        Utiliza um set para guardar os estados; um set para guardar o alfabeto; um set
        para guardar os estados de aceitação; um atributo de string que guarda o estado inicial;
        e um set de tuplas em que cada tupla representa uma transição, com a tupla tendo a seguinte
        assinatura (estadoDe, estadoPara, símboloDeTransição). Além disso, possui um dicionário
        em que cada chave é um estado, e o valor é um set contendo as tuplas de transição daquele
        estado.
    FiniteAutomataUtils.py - Implementa uma classe auxiliar responsável por realizar as operações
        de interseção e união entre diferentes instâncias da classe FiniteAutomata.
    RegularGrammar.py - Implementa uma classe responsável por fazer conversões entre gramáticas
        regulares e autômatos finitos, e vice-versa. Dentro da classe, autômatos são recebidos 
        em forma de FiniteAutomata e então transformados em matrizes, sendo a matriz uma 
        representação da tabela de transições do autômato. As gramáticas também são manipuladas 
        em forma de matriz, sendo cada linha dessa matriz composta pelo não terminal e suas
        produções.
    RegEx.py - Implementa duas classes, 
        RegexNode: possui as propriedades de um nodo de uma árvore regex. Contém uma lista de
            índices para os firstpos; uma lista de índices para os lastpos; um atributo que
            indica se é nullable ou não; e um set que guarda o alfabeto;
        RegexTree: A partir de uma expressão regular de entrada, gera uma árvore 
            composta por RegexNodes. Possui uma lista de índices followpos e calcula as funções
            followpos através de seus nodos-filhos. Gera um FiniteAutomata a partir dos followpos.
    ContextFreeGrammar.py - Implementa uma classe responsável por manipular uma gramática livre de
            contexto. Possui um atributo de string que indica o símbolo inicial; um set para guardar 
            os símbolos não terminais; um set para guardar os símbolos terminais; um dicionário para
            guardar os firsts, em que cada chave é um não terminal e o valor é um set contendo os
            respectivos follows para o não terminal; da mesma forma um dicionário para os follows.
            Além disso, possui um dicionário que guarda as produções, em que cada chave é um não 
            terminal e o valor é um set de tuplas, sendo cada tupla uma produção do não terminal.
            Também possui um dicionário/hashmap que guarda a tabela do Preditivo LL(1), sendo a 
            chave desse dicionário/hashmap a tupla (Não Terminal, Terminal) e o valor sua produção.

ESPECIFICAÇÕES DOS ARQUIVOS DE ENTRADA:

Automato Finito:

    X|  a   | b      | &
->*q0| q0,q1| q2     | q3
  *q1| q1   | q3     | q3
  *q2| -    | q2,q4  | -
   q3| q1,q3| q2,q3  | q4
   q4| q4   | q2     | q3

    -> indica o estado inicial
    * indica que o estado é de aceitação
    Se o estado é composto, ex: {q0,q1}, deve estar em ordem crescente e escrito sem as chaves e 
        sem espaço entre os estados, ex.: q0,q1
    A presença de espaços entre os separadores | é ignorada pelo leitor de arquivo.

Gramatica Regular:

S -> aA | bB | b
A -> aS
B -> bB | b

    O primeiro símbolo não terminal lido é entendido como símbolo inicial da gramática.
    As produções devem possuir terminal seguido de não terminal, sem espaço entre os símbolos.
    A presença de espaços entre os separadores | é ignorada.
    
Gramática Livre de Contexto:

E -> E + T | E − T | T
T -> T ∗ F | F | T / F
F -> F ∗ ∗ P | P
P -> ( E ) | id | cte

    O primeiro símbolo não terminal lido é entendido como símbolo inicial da gramática.
    As operações de eliminação de recursão à esquerda seguirão a ordem em que a gramática foi
        escrita. No exemplo assima, a recursão de E será eliminada antes da de T.
    Cada símbolo na produção deve ser separado por espaço. 
    Os símbolos minúsculos são lidos como terminais, e os maiúsculos como não terminais.
    São aceitos símbolos terminais "compostos" como `id` e `cte` do exemplo.
    Os caracteres ' e ! são reservados, portanto não são aceitas gramáticas com símbolos sucedidos
        por estes.

OPERAÇÕES DISPONÍVEIS:
    Gerais:
        disponivel
            Lista todas as operações disponíveis;
        sair
            Termina o programa;
    
    Autômato Finito:
        determinizarAF
            Determiniza um Autômato Finito caso seja indeterminístico 
            (contendo transições por épsilon-fecho ou não), caso contrário retorna ele mesmo;
        minimizarAF
            Minimiza um Autômato Finito, removendo estados mortos, inalcançáveis e 
            equivalentes/redundantes;
        uniaoAF
            Realiza a união entre dois Autômatos Finitos, retornando um novo Autômato Finito;
        intersecaoAF
            Realiza a interseção entre dois Autômatos Finitos, retornando um novo Autômato Finito;
        leituraSentencaAF
            Verifica se um Autômato Finito reconhece uma sentença;

    Conversões:
        GRparaAF
            Converte uma Gramática Regular para um Autômato Finito;
        AFparaGR
            Conterte um Autômato Finito para uma Gramática Regular;
        REGEXparaAFD
            Converte uma Expressão Regular para um Autômato Finito, usando o algorítmo baseado em 
            árvore sintática;

    Gramática Livre de Contexto
        fatorarGLC
            Fatora uma Gramática Livre de Contexto, tentando converter as produções não determinísticas 
            diretas e indiretas;
        removerRecursaoEsqGLC
            Tenta remover as recursões à esquerda de uma Gramática Livre de Contexto;
        leituraSentencaGLC
            Verifica se uma sentença pode ser gerada a partir de uma Gramática Livre de Contexto
            simulando um Autômato de Pilha a partir da tabela LL(1) da Gramática (se for LL(1));
