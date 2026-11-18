# ADR 0003: Frontend com Django Templates e HTMX

Estado: aceite
Data: 2026-11-18

## Contexto

A aplicação deve ser rápida em equipamentos modestos e com internet limitada, e simples de manter por uma só pessoa. A maior parte das páginas (aulas, exercícios, resultados) é conteúdo com interações pontuais, não uma aplicação com estado complexo no navegador.

## Decisão

As páginas são geradas no servidor com Django Templates. O HTMX trata das interações que precisam de atualizar partes da página (por exemplo, corrigir uma resposta). O Alpine.js só entra se houver uma necessidade concreta. As funcionalidades que o HTMX não cobre, como gravar a voz do estudante no microfone, usam JavaScript simples e isolado.

## Alternativas consideradas

- React ou Next.js: muito poderosos, mas obrigam a manter duas aplicações, enviam muito mais JavaScript ao telemóvel do estudante e aumentam a complexidade sem necessidade nesta fase.
- Django Templates sem HTMX: mais simples ainda, mas cada interação recarregaria a página inteira.

## Consequências

- Páginas leves e rápidas, boas para ligações lentas.
- Um só projeto e uma só linguagem principal (Python).
- A parte de voz exigirá JavaScript próprio, e deve ficar bem organizada.
- Se no futuro a interface ficar muito interativa, esta decisão pode ser revista.
