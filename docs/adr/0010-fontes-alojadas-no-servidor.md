# ADR 0010: Fontes alojadas no servidor e ficheiros de design no módulo core

Estado: aceite
Data: 2026-11-25

## Contexto

O sistema de design escolheu o Plus Jakarta Sans (interface) e o Instrument Serif (títulos) e deixou em aberto onde alojar as fontes e se as licenças o permitem. Os estudantes usam equipamentos modestos e ligações lentas, e a plataforma não deve enviar dados dos estudantes a serviços de terceiros sem necessidade. As duas fontes têm a licença SIL Open Font License 1.1 (confirmada nos metadados dos pacotes), que permite usá-las e distribuí-las, desde que a licença as acompanhe.

## Decisão

1. As fontes são servidas pelo nosso próprio servidor, em ficheiros woff2 do subconjunto latino (que cobre o português), na pasta `core/static/core/fonts/`, com a licença de cada uma ao lado.
2. O Plus Jakarta Sans vai em versão variável (pesos 200 a 800, 27 KB) e o Instrument Serif só em regular (21 KB). Sem itálicos por agora.
3. O CSS usa `font-display: swap` (o texto aparece logo na fonte de reserva do sistema e troca quando a fonte chega) e as pilhas de reserva do sistema de design.
4. Os ficheiros de design partilhados (fontes, variáveis CSS e modelo base das páginas) vivem no módulo `core`.
5. A origem e a versão ficam registadas em `core/static/core/fonts/ORIGEM.md`. Os ficheiros vêm dos pacotes Fontsource 5.3.0.

## Alternativas consideradas

- Pedir as fontes ao Google Fonts: é uma dependência externa que pode falhar ou ser lenta, e envia o endereço de cada visitante a terceiros.
- Só fontes do sistema: não custa nada, mas perde-se a identidade visual.
- Incluir os itálicos e outros alfabetos: mais peso sem necessidade.

## Consequências

- Cerca de 48 KB a mais no repositório e nas páginas, e nenhuma dependência externa.
- A licença tem de acompanhar sempre os ficheiros, e um teste verifica que está lá.
- Os testes verificam que as fontes existem, que são woff2 válidos e que o CSS só aponta para ficheiros que existem.
- Para usar texto noutro alfabeto, ou itálicos, é preciso acrescentar os ficheiros correspondentes.
