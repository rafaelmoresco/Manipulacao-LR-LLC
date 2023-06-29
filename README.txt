UNIVERSIDADE FEDERAL DE SANTA CATARINA - DEPARTAMENTO DE INFORMÁTICA E ESTATÍSTICA
FLORIANÓPOLIS, 28 DE JUNHO DE 2023
INTEGRANTES
    BERNARDO GOMES DUARTE
    EDUARDO BORGES SIQUEIRA
    RAFAEL MORESCO VIEIRA
    SAMUEL MOREIRA RANZOLIN

Manipulação de Linguagens Regulares e Linguagens Livres de Contexto

Este trabalho foi desenvolvido para a disciplina Linguagens Formais e Compiladores
(INE5421), e tem como objetivo demonstrar o domínio sobre Linguagens Regulares e
Linguages Livres de Contexto.

ESPECIFICAÇÕES:

Este trabalho foi desenvolvido em Python3, utilizando as bibliotecas padrões,
e utiliza arquivos de texto como entrada de dados de Grámaticas e Automatos.
A seguir, segue exemplos dos conteudos dos arquivos de entrada:

Automatos:

    X|  a   | b      | &
->*q0| q0,q1| q2     | q3
  *q1| q1   | q3     | q3
  *q2| -    | q2,q4  | -
   q3| q1,q3| q2,q3  | q4
   q4| q4   | q2     | q3

    Se o estado é composto, ex: {q0,q1}, deve estar em ordem crescente e escrito sem as chaves, ex.: q0,q1.
    A presença de espaços entre os separadores | é ignorada.
    -> indica o estado inicial e * indica um estado de aceitação

Gramatica:

P -> KVC
K -> cK | &
V -> vV | F
F -> fP;F | &
C -> bVCe | k;C | &

    A primeira linha indica qual símbolo é o símbolo inicial da gramatica
    A presença de espaços entre os separadores | é ignorada.
    
Para rodar o programa, execute o arquivo main.py no console atravéz do comando:
    python3 main.py
Uma vez com o programa rodando, digite a operação desejada, e em seguida
indique o nome (com caminho relativo) do arquivo que se deseja rodar a operação

Operações:
    disponivel
        Lista todas as opreações disponíveis
    determinizarAF
        Determiniza um automato.
    minimizarAF
        Minimiza um automato. Se não for deterministico, determiniza ele
    uniaoAF
        Faz a união de dois automatos
    intercecaoAF
        Faz a intercecao de dois automatos
    leituraAF
        Pede uma palavra, e verifica se a palavra indica é reconhecida pelo automato
    regex
        Pede uma expreção regular, e cria um automato a partir dela
    sair
        Sai do programa

Estrutura:

O código foi desenvolvido com orientação a objetos. O arquivo main é responsável por
unir todas as classes e fazer a interface com o usuário. O arquivo FiniteAutomata
possuí a classe FiniteAutomata, que é respónsavel por todas as opreações intrinsicas de
um automato finito. As opreações de união e interseção de Automatos ficam na classe de apoio
FiniteAutomataUtils, encontrada no arquivo de mesmo nome. O arquivo RegEx possui duas classes,
a RegexTree e a RegexNode. A classe RegexTree recebe o total de uma expreção regular, e a
transforma em uma árvore, onde cada nodo é uma classe RegexNode. A RegexTree cria um automato
com a expreção regular de entrada. O arquivo ContextFreeGrammar possui uma classe com o mesmo nome,
e é respónsavel por todas as opreações sobre uma gramática livre de contexto, além de ser
responsável pela criação de uma tabela de parser e um automata de pilha para reconhecer
uma palavra de entrada. O arquivo RegularGrammar possui a classe GR, que possui algoritmos
para converter uma gramatica regular em um automato finito e vice versa. O arquivo reader
possui a classe Reader, que transforma um arquivo .txt de entrada em um automato, uma gramatica
regular ou uma gramatica livre de contexto.