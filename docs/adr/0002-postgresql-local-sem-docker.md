# ADR 0002: PostgreSQL instalado no sistema, sem Docker no desenvolvimento

Estado: aceite
Data: 2026-11-18

## Contexto

O computador de desenvolvimento tem pouco espaço livre em disco (cerca de 3 GB) e memória limitada. O PostgreSQL 17 já está instalado e ativo no sistema. O produto exige PostgreSQL como base de dados principal.

## Decisão

No desenvolvimento local usamos o PostgreSQL 17 do sistema. O Docker não é requisito para trabalhar no projeto. A configuração da base de dados vem de variáveis de ambiente, nunca do código.

## Alternativas consideradas

- Docker Compose: reprodutível, mas as imagens ocupam disco e memória que não temos de sobra.
- SQLite no desenvolvimento: muito leve, mas comporta-se de forma diferente do PostgreSQL e pode esconder erros que só apareceriam em produção.

## Consequências

- Ambiente leve e fiel ao de produção.
- Quem quiser colaborar precisa de instalar o PostgreSQL manualmente, e isso ficará explicado no README.
- Docker pode ser adicionado mais tarde como opção, sem alterar o código da aplicação.
