# Arquitetura: mapa dos módulos

Primeira proposta, a rever com ADRs quando houver razão para mudar. Os nomes no código são em inglês; a interface e a documentação são em português.

## Módulos e responsabilidades

| Módulo | Responsabilidade |
|---|---|
| `core` | Sistema de design, componentes e utilitários comuns |
| `accounts` | Registo, login, perfil e preferências do estudante |
| `academics` | Universidades, faculdades, cursos, concursos, catálogo de disciplinas e exigências por ano |
| `content` | Temas, aulas, exemplos, origem e verificação do conteúdo |
| `exercises` | Questões, resoluções e correção de respostas |
| `progress` | Diagnóstico, domínio por tema, revisões e plano de estudo |
| `exams` | Provas anteriores, simulados com cronómetro e resultados |
| `tutor` | Professor com IA e validação matemática |
| `voice` | Reconhecimento de fala, síntese de voz e aula por turnos |

A administração de conteúdo usa o Django Admin, personalizado em cada módulo.

## Regra de dependência

Cada módulo só pode depender dos que estão listados aqui. As dependências vão num só sentido, sem ciclos.

- `core`: não depende de nenhum módulo (todos o podem usar)
- `accounts`: nenhum
- `academics`: nenhum
- `content`: `academics`
- `exercises`: `content`
- `progress`: `accounts`, `exercises`
- `exams`: `accounts`, `academics`, `exercises`
- `tutor`: `content`, `exercises`, `progress`
- `voice`: `tutor`
