# Project Goblin — Claude Context

## What this is

A containerized AI agent that monitors a self-hosted Jellyfin media server, diagnoses issues using Claude, and takes corrective action only after user approval via Telegram. Built as a PM portfolio project — public repo, incremental commits, structured roadmap.

The user runs Jellyfin on an Asus GV62VR 7RF laptop, managed via Portainer.

## Tech stack

- **Language:** Python
- **Container access:** Docker socket (direct, not Portainer API)
- **Messaging:** `python-telegram-bot`
- **AI brain:** Anthropic API (Claude)
- **Deployment:** Docker container via Portainer
- **Repo:** github.com/karamvirdhanoa/project-goblin

## Repo structure

```
src/
├── config.py              # env var loading and validation
├── agent/main.py          # async poll loop — orchestrates everything
├── monitors/
│   ├── docker_monitor.py  # Docker socket → ContainerSnapshot
│   └── system_monitor.py  # psutil → SystemSnapshot
├── notifiers/
│   └── telegram_notifier.py  # send(), verify_connection()
└── brain/                 # Claude API integration (v0.3)
docs/
├── architecture.md
└── contributing.md
```

## Roadmap

| Version | Description | Status |
|---|---|---|
| v0.1 | Repo scaffolding, README, architecture docs | ✅ Done |
| v0.2 | Docker monitoring, psutil metrics, Telegram skeleton, poll loop | ✅ Done — tested and running on Linux Mint server |
| v0.3 | Claude integration for diagnosis | 🔜 Next |
| v0.4 | Approval flow + restart actions | ⏳ Planned |
| v0.5 | Jellyfin-specific health checks | ⏳ Planned |
| v1.0 | Polished, documented, public release | ⏳ Planned |

## Architecture summary

Poll timer (60s) → Monitor → Evaluator (anomaly?) → Brain (Claude) → Notifier (Telegram) → user approves → Action Executor → Notifier confirms.

**Supervised, never autonomous.** Every action requires explicit user approval via Telegram inline keyboard.

## Key design decisions

- Docker socket directly, not Portainer API — fewer moving parts
- Telegram over WhatsApp — free, clean bot API, supports inline keyboards
- LLM diagnosis, not rule-based alerts — produces actionable plain-English output
- Modular monitors — `docker_monitor`, `system_monitor`, `jellyfin_monitor` drop into `src/monitors/`

## Deferred (v2+)

Setup wizard, Plex/NAS monitors, WhatsApp, web dashboard UI, autonomous mode.

## Conventions

**Commits:** `type(scope): short description`
Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`

**Branches:** `main` (tagged releases) ← PR ← `dev` (active work) ← `feat/short-description`

**Every task ends with a suggested git commit command.**

**Work directly in the project folder** (`/Users/karamvirdhanoa/Projects/project-goblin`), not in a git worktree.
