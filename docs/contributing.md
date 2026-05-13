# Contributing

Thanks for your interest in Project Goblin. This is a portfolio project built in public — contributions, issues, and feedback are all welcome.

---

## Getting Started

```bash
git clone https://github.com/karamvirdhanoa/project-goblin.git
cd project-goblin
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # fill in your credentials
```

---

## Commit Convention

This project uses conventional commits:

```
type(scope): short description

Examples:
feat(monitor): add Docker socket polling
fix(notifier): handle Telegram timeout gracefully
docs(readme): add architecture overview
chore(config): update docker-compose scaffold
test(brain): add unit tests for prompt builder
```

Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`

---

## Branch Strategy

- `main` — stable, tagged releases only
- `dev` — active development
- Feature branches: `feat/short-description`

Open PRs against `dev`.

---

## Reporting Issues

Use GitHub Issues. Include:
- What you expected to happen
- What actually happened
- Your OS, Docker version, and Python version
- Relevant logs (sanitise any tokens first)

---

## Roadmap

See the roadmap section in the [README](../README.md) for what's planned. If you want to work on something, open an issue first so we can discuss approach before you invest time.
