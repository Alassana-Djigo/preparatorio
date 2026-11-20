# ADR 0006: Modelo do domínio académico

Estado: aceite
Data: 2026-11-20

## Contexto

O módulo `academics` descreve instituições, cursos e o que cada concurso de acesso exige. Os requisitos mudam de ano para ano, o brief do produto exige que não se inventem dados oficiais, e muitos módulos dependem deste (`content`, `exams`, `progress`). Mudar a estrutura depois de existirem dados reais é caro.

## Decisão

1. As exigências pertencem ao par curso + concurso de acesso (`CourseRequirement`), e não ao curso. Cada concurso é uma instituição num ano letivo.
2. As disciplinas vivem num catálogo único e partilhado (`Subject`). As diferenças de programa entre instituições tratam-se no módulo `content`.
3. Todo o dado que descreve a realidade tem proveniência: origem (oficial ou demonstração), fonte, estado de verificação e data. Só o que é oficial e verificado aparece ao estudante como oficial, e a demonstração aparece identificada como tal.

O modelo completo, as regras e as questões em aberto estão em `docs/dominio-academico.md`.

## Alternativas consideradas

- Lista de disciplinas dentro do curso: mais simples, mas perde o histórico de cada ano.
- Exigências num campo JSON: flexível, mas deixa de ser possível perguntar à base de dados que cursos exigem uma disciplina.
- Disciplinas separadas por instituição: duplica conteúdo e dificulta partilhar aulas e exercícios.
- Fonte como texto livre, sem estado de verificação: mais rápido, mas não impede que dados por verificar sejam apresentados como oficiais.

## Consequências

- Mais tabelas, mas perguntas simples ("que cursos exigem Física em 2026/2027?") e histórico completo.
- O administrador tem de permitir registar fontes e marcar verificações.
- As regras de coerência (por exemplo, o curso pertencer à instituição do concurso) são testadas e não dependem só do administrador.
- Os dados reais têm de ser recolhidos de documentos oficiais pelo dono do projeto. Até lá, usamos apenas dados de demonstração, identificados como tal.
