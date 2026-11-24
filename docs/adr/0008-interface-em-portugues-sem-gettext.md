# ADR 0008: Textos da interface em português, sem gettext por agora

Estado: aceite
Data: 2026-11-23

## Contexto

O produto é para estudantes angolanos, por isso a interface é em português, enquanto os nomes no código são em inglês. O Django traduz sozinho as suas próprias mensagens a partir de `LANGUAGE_CODE = "pt"`, mas os rótulos e as mensagens do nosso código (campos, modelos, erros) são escritos por nós. O Django oferece o gettext (textos marcados para tradução) para suportar vários idiomas.

## Decisão

Os rótulos (`verbose_name`) e as mensagens do projeto escrevem-se diretamente em português, sem gettext. O código continua em inglês.

## Alternativas consideradas

- gettext desde já (`gettext_lazy` e ficheiros de tradução): prepara vários idiomas, mas acrescenta trabalho e ficheiros para uma necessidade que ainda não existe.
- Interface em inglês: contraria o público a que o produto se destina.

## Consequências

- É mais simples de escrever e de ler agora.
- Se um dia fizer falta outro idioma (por exemplo, uma demonstração a parceiros internacionais), será preciso marcar os textos para tradução. É uma alteração mecânica, e os testes dos rótulos mostram o que muda.
- Alterar rótulos gera migrações só de estado, que não mexem nos dados (ver a migração 0004 do `academics`).
