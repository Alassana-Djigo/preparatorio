# ADR 0004: Python 3.13 e Django 6.1

Estado: aceite, complementado pelo [ADR 0007](0007-python-3-13-e-3-14.md)
Data: 2026-11-18

## Contexto

O projeto começa agora, sem código existente. O computador de desenvolvimento tem Python 3.13.5. Segundo a documentação oficial, o Django 6.1 suporta Python 3.12, 3.13 e 3.14. O suporte principal do 6.1 deve acabar em abril de 2027 e o suporte alargado (só segurança) em dezembro de 2027.

## Decisão

Usamos Python 3.13 e Django 6.1, fixando a série 6.1 nas dependências: recebemos correções 6.1.x, mas não saltamos de versão sem decisão nossa.

## Alternativas consideradas

- Django 5.2 LTS (versão de suporte longo): mais tempo sem mudar de versão, mas sem as novidades recentes.
- Esperar por uma versão LTS mais recente: atrasa o início sem benefício real.

## Consequências

- Começamos na versão atual, sem dívida de atualização.
- Teremos de planear uma subida de versão antes do fim do suporte, e o ADR será revisto nessa altura.
- Todas as dependências devem ser compatíveis com Python 3.13.
