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

Especificações:

Este trabalho foi desenvolvido em Python3, utilizando as bibliotecas padrões,
e utiliza arquivos de texto como entrada de dados de Grámaticas e Automatos.
A seguir, segue exemplos dos conteudos dos arquivos de entrada:

Automatos:
      _ | a|b
    ->q0|q1|q2
      q1|q1|q2
     *q2|q0|q2

    Se o estado é composto, ex: {q0,q1}, deve estar em ordem crescente e escrito sem as chaves, ex.: q0,q1.
    A presença de espaços entre os separadores | é ignorada.
    -> indica o estado inicial e * indica um estado de aceitação

Gramatica:
    aasdasdasd

Para rodar o programa, execute o arquivo main.py no console atravéz do comando:
    python3 main.py
Uma vez com o programa rodando, digite a operação desejada, e em seguida
indique o nome (com caminho relativo) do arquivo que se deseja rodar a operação

Operações:
    determinizar 
        Determiniza um automato.
    minimizar
        Minimiza um automato. Se não for deterministico, determiniza ele
    uniao
        Faz a união de dois automatos
    intercecao
        Faz a intercecao de dois automatos
    leituraAF
        Pede uma palavra, e verifica se a palavra indica é reconhecida pelo automato
    regex
        Pede uma expreção regular, e cria um automato a partir dela
    sair
        Sai do programa