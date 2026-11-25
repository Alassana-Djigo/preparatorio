# ADR 0009: Visibilidade dos dados para o estudante

Estado: aceite
Data: 2026-11-24

## Contexto

O ADR 0006 exige que nenhum dado por verificar seja apresentado como oficial. Os dados têm uma origem (oficial ou demonstração) e um estado de verificação. Falta decidir o que o estudante vê, onde a regra vive e como tratar dados que dependem uns dos outros: uma exigência depende de um concurso, de um curso, de uma faculdade e de uma instituição.

## Decisão

1. O estudante vê sempre os dados oficiais verificados. Os oficiais por verificar nunca aparecem (só no administrador). Os de demonstração só aparecem se a opção `SHOW_DEMO_DATA` estiver ligada e levam sempre a etiqueta "Dados de demonstração" (`provenance_label`).
2. A opção `SHOW_DEMO_DATA` vem desligada por defeito (variável de ambiente `DJANGO_SHOW_DEMO_DATA`) e ligada no desenvolvimento.
3. A regra vive no método `.public()` das consultas de cada modelo com proveniência. A consulta normal (`objects`) continua a devolver tudo.
4. Um dado só é público se toda a cadeia de que depende também o for.
5. O catálogo de disciplinas não tem proveniência e é sempre visível.

## Alternativas consideradas

- Mostrar só o oficial verificado, sempre: impede demonstrações enquanto não houver dados reais.
- Mostrar tudo com etiquetas: um estudante podia agir com um dado por verificar.
- Fazer a consulta normal filtrar: o Django usa-a nas ligações entre tabelas e nas validações, e linhas escondidas dão erros confusos.
- Avaliar só o próprio registo: um curso verificado podia aparecer pendurado numa faculdade escondida.

## Consequências

- Em produção, enquanto não houver dados verificados, o estudante não vê nada. É de propósito: é melhor não mostrar do que mostrar errado.
- Quem escrever uma página para estudantes tem de usar `.public()`. Os testes das páginas vão verificar isso.
- As consultas juntam as tabelas da cadeia e ficam mais elaboradas, mas todas as combinações estão testadas.
