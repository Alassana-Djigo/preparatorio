# Preparatório

Plataforma web de aprendizagem e preparação para exames de acesso ao ensino superior em Angola.

> Estado: desenvolvimento inicial. Ainda não existe uma versão utilizável.

## Como pôr o projeto a correr num PC novo

> Este guia é atualizado sempre que o processo de instalação muda.
>
> Testado em Debian 13 e Ubuntu. Noutros sistemas, os comandos do passo 5 (`sudo -u postgres`) mudam; os comandos SQL são os mesmos.

### O que precisas de ter instalado

- Git, com o nome e o email configurados: `git config --global user.name 'O teu Nome'` e `git config --global user.email 'o-teu@email.com'`
- Python 3.13 ou 3.14 com suporte a ambientes virtuais (no Debian/Ubuntu: `sudo apt install python3-venv`)
- PostgreSQL 15 ou superior, com o servidor a correr (testado com a versão 17)

### Passos

1. Clonar o repositório (é público, por isso o endereço HTTPS não precisa de conta nem de chaves):

   ```bash
   git clone https://github.com/Alassana-Djigo/preparatorio.git
   cd preparatorio
   ```

2. Criar e ativar o ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instalar as dependências:

   ```bash
   pip install -r requirements/dev.txt
   ```

4. Criar o `.env` com uma chave secreta e uma senha da base de dados novas:

   ```bash
   cp .env.example .env
   DB_PASS=$(python -c 'import secrets; print(secrets.token_urlsafe(24))')
   sed -i "s/^DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')/" .env
   sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=$DB_PASS/" .env
   ```

   O `.env` nunca vai para o Git. Cada computador tem o seu.

5. Criar o utilizador e a base de dados no PostgreSQL (usa a mesma senha do passo anterior, por isso corre no mesmo terminal):

   ```bash
   sudo -u postgres psql -c "CREATE USER preparatorio WITH PASSWORD '$DB_PASS' CREATEDB;"
   sudo -u postgres psql -c "CREATE DATABASE preparatorio OWNER preparatorio;"
   unset DB_PASS
   ```

6. Criar as tabelas e verificar que tudo está bem:

   ```bash
   python manage.py migrate
   python manage.py check
   ```

   O `check` deve responder `System check identified no issues (0 silenced).`

## Enviar código a partir de um PC novo

Para abrir pull requests (ver [CONTRIBUTING.md](CONTRIBUTING.md)) precisas do GitHub CLI e de entrar na tua conta:

```bash
sudo apt install gh
gh auth login
```

No `gh auth login`, escolhe `GitHub.com` e `SSH`, e aceita a chave SSH que o `gh` propuser. Como o clone foi por HTTPS, muda depois o endereço do remoto para SSH e testa a ligação:

```bash
git remote set-url origin git@github.com:Alassana-Djigo/preparatorio.git
ssh -T git@github.com
```

Na primeira ligação, responde `yes` à pergunta sobre o servidor. Deves ver `Hi Alassana-Djigo! You've successfully authenticated`. Noutros sistemas, o `gh` instala-se como explica https://cli.github.com.

## Qualidade do código

Antes de cada commit:

```bash
ruff check .
ruff format --check .
pytest
```

## Documentação

- [Visão do produto](docs/visao.md)
- [Arquitetura e módulos](docs/arquitetura.md)
- [Sistema de design](docs/design-system.md)
- [Fluxos e wireframes](docs/fluxos-e-wireframes.md)
- [Domínio académico](docs/dominio-academico.md)
- Decisões de arquitetura: pasta [docs/adr](docs/adr)
- [Como contribuir](CONTRIBUTING.md)
