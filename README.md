# Preparatório

Plataforma web de aprendizagem e preparação para exames de acesso ao ensino superior em Angola.

> Estado: desenvolvimento inicial. Ainda não existe uma versão utilizável.

## Como pôr o projeto a correr num PC novo

> Este guia é atualizado sempre que o processo de instalação muda.

### O que precisas de ter instalado

- Git
- Python 3.13 com suporte a ambientes virtuais (no Debian/Ubuntu: `sudo apt install python3-venv`)

### Passos

1. Clonar o repositório (precisa de acesso ao GitHub por SSH):

   ```bash
   git clone git@github.com:Alassana-Djigo/preparatorio.git
   cd preparatorio
   ```

2. Criar e ativar o ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instalar as dependências:

   ```bash
   pip install -r requirements/base.txt
   ```

4. Criar o ficheiro `.env` com uma chave secreta nova:

   ```bash
   cp .env.example .env
   sed -i "s/^DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')/" .env
   ```

   O `.env` nunca vai para o Git. Cada computador tem o seu.

5. Verificar que tudo está bem:

   ```bash
   python manage.py check
   ```

   Deve responder `System check identified no issues (0 silenced).`

## Documentação

- [Visão do produto](docs/visao.md)
- [Arquitetura e módulos](docs/arquitetura.md)
- Decisões de arquitetura: pasta [docs/adr](docs/adr)
