# Como contribuir

## Fluxo de trabalho

O ramo `main` está protegido: só recebe código através de pull request com o CI verde. Não há pushes diretos, nem para o dono do repositório.

1. Atualizar o `main`:

   ```bash
   git switch main
   git pull
   ```

2. Criar um ramo (`feature/nome-da-funcionalidade` ou `fix/nome-do-problema`):

   ```bash
   git switch -c feature/nome-da-funcionalidade
   ```

3. Fazer commits pequenos e coerentes, seguindo o Conventional Commits (ver abaixo).

4. Verificar localmente antes de cada commit:

   ```bash
   ruff check .
   ruff format --check .
   pytest
   ```

5. Enviar o ramo e abrir o pull request. O título do pull request segue o mesmo formato dos commits, porque é a mensagem do commit que entra no `main`:

   ```bash
   git push -u origin feature/nome-da-funcionalidade
   gh pr create --base main
   ```

6. Esperar pelo CI e juntar o pull request com `squash`:

   ```bash
   gh pr checks --watch
   gh pr merge --squash
   ```

7. Voltar ao `main` e atualizar: `git switch main && git pull`.

## Mensagens de commit (Conventional Commits)

Formato: `tipo(âmbito): descrição curta, no imperativo, em inglês`

| Tipo | Quando usar |
|---|---|
| `feat` | nova funcionalidade |
| `fix` | correção de um erro |
| `docs` | documentação |
| `test` | testes |
| `refactor` | reorganização sem mudar o comportamento |
| `chore` | manutenção e dependências |
| `ci` | alterações de integração e entrega contínuas |
| `style` | estilo, sem mudança funcional |

Exemplos: `feat(auth): implement student registration`, `fix(tutor): handle invalid mathematical answers`.

## Regras que não mudam

- Segredos nunca entram no Git. O `.env` está no `.gitignore`; os nomes das variáveis estão no `.env.example`.
- Sem `git push --force` nem `git reset --hard` sem discutir os riscos antes.
- Se o processo de instalação mudar, o `README.md` é atualizado no mesmo commit.
