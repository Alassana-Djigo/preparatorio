# ADR 0005: Modelo de utilizador personalizado

Estado: aceite
Data: 2026-11-19

## Contexto

O Django traz um modelo de utilizador pronto (`auth.User`), mas a documentação recomenda definir um modelo próprio no início de qualquer projeto novo, mesmo que o padrão chegue. Trocar de modelo depois de existirem tabelas e dados é difícil e arriscado, porque outras tabelas ficam ligadas ao modelo antigo. Hoje a base de dados de desenvolvimento só tem as tabelas internas do Django e nenhum dado real, por isso este é o momento mais barato para decidir.

## Decisão

Criamos o modelo `User` no módulo `accounts`, estendendo `AbstractUser` (o modelo completo do Django, pronto a ser ampliado), e definimos `AUTH_USER_MODEL = "accounts.User"` antes de existirem migrações do módulo. Os dados específicos do estudante (curso pretendido, preferências) ficam para o desenho do módulo `accounts`, e não são decididos aqui.

Todo o código passa a obter o modelo com `get_user_model()` ou `settings.AUTH_USER_MODEL`, e nunca importa o `User` diretamente.

## Alternativas consideradas

- Manter o `auth.User` padrão: sem trabalho agora, mas qualquer campo novo ou mudança de login exigiria uma migração de alto risco mais tarde.
- Herdar de `AbstractBaseUser` (controlo total, por exemplo login só por email): mais flexível, mas obriga a escrever o gestor de utilizadores e a tratar permissões à mão, com mais superfície para erros de segurança. Pode ser reavaliado se o login por email ou telefone o justificar.
- Manter o `auth.User` e ligar um modelo de perfil à parte: funciona, mas deixa o problema de fundo por resolver.

## Consequências

- Campos novos no utilizador passam a ser uma migração normal.
- A base de dados de desenvolvimento tem de ser recriada uma vez, porque já tem as tabelas do utilizador antigo. Não perdemos dados reais, porque não existem. Essa recriação será explicada e autorizada no passo de implementação.
- O primeiro teste que escrevemos já usa `get_user_model()`, por isso continua válido.
