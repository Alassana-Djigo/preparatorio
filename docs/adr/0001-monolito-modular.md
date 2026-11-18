# ADR 0001: Monólito modular em Django

Estado: aceite
Data: 2026-11-18

## Contexto

O projeto é desenvolvido por uma só pessoa, com orçamento próximo de zero e um computador de desenvolvimento com recursos limitados. Ao mesmo tempo, precisa de crescer em áreas distintas: estrutura académica, conteúdos, exercícios, tutor com IA, voz e simulados.

## Decisão

Uma única aplicação Django, organizada em módulos (apps) com responsabilidades separadas. Um só repositório, um só processo e uma só base de dados PostgreSQL.

## Alternativas consideradas

- Microserviços (vários programas independentes que comunicam entre si). Rejeitado: aumenta o custo de alojamento e a complexidade de operação, sem benefício real nesta escala.
- Uma aplicação Django sem separação em módulos. Rejeitado: fica difícil de manter e de testar à medida que cresce.

## Consequências

- Simples de desenvolver, testar e alojar, e portanto barato.
- Fronteiras claras entre módulos permitem separar uma parte no futuro, se for mesmo necessário.
- Exige disciplina: um módulo não deve depender dos detalhes internos de outro.
