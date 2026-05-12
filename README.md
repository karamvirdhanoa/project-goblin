# 👺 Project Goblin

An AI-powered monitoring agent for self-hosted Jellyfin media servers. It watches your containers, diagnoses issues in plain English using Claude, and asks for your approval before taking any action — all via Telegram.

> **Status:** v0.1 — scaffolding & documentation  
> **Target:** Self-hosters running Jellyfin via Docker/Portainer

---

## The Problem

Running Jellyfin on old hardware means things break silently. Containers crash, disks fill up, memory spikes — and you find out only when someone complains that nothing's streaming. There's no intelligent layer that tells you *what* went wrong and *what to do about it*.

## The Solution

Project Goblin runs alongside your stack. Every 60 seconds it checks your containers and system health, sends the picture to Claude for analysis, and messages you on Telegram with a plain-English diagnosis and a recommended action. You approve — it acts.

**Supervised, not autonomous.** It never does anything without your say-so.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Project Goblin                    │
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌───────────────┐  │
│  │ Monitor  │───▶│  Brain   │───▶│   Notifier    │  │
│  │          │    │ (Claude) │    │  (Telegram)   │  │
│  │ - Docker │    │          │    │               │  │
│  │ - System │    │ Diagnose │    │ Alert + await │  │
│  │ - Jelly  │    │ + advise │    │ approval      │  │
│  └──────────┘    └──────────┘    └───────┬───────┘  │
│       ▲                                  │          │
│       │          ┌───────────┐           │          │
│       └──────────│  Action   │◀──────────┘          │
│                  │ Executor  │  (on approval)        │
│                  └───────────┘                      │
└─────────────────────────────────────────────────────┘
          │                          │
    Docker socket               Telegram API
    /var/run/docker.sock
```

See [`docs/architecture.md`](docs/architecture.md) for the full decision flow.

---

## Quickstart

> **Prerequisites:** Docker, a running Jellyfin container, a Telegram bot token, an Anthropic API key.

```bash
# 1. Clone the repo
git clone https://github.com/karamvirdhanoa/project-goblin.git
cd project-goblin

# 2. Configure
cp .env.example .env
# Edit .env with your tokens and container name

# 3. Run
docker compose up -d
```

That's it. Watch your Telegram for the first health report.

---

## Configuration

All configuration is via environment variables. Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `TELEGRAM_BOT_TOKEN` | Token from @BotFather |
| `TELEGRAM_CHAT_ID` | Your personal chat ID |
| `JELLYFIN_CONTAINER_NAME` | Name of your Jellyfin container |
| `POLL_INTERVAL_SECONDS` | How often to check (default: 60) |
| `LOG_LEVEL` | `INFO` or `DEBUG` |

---

## Roadmap

| Version | Description | Status |
|---|---|---|
| v0.1 | Repo scaffolding, README, architecture | ✅ Done |
| v0.2 | Docker health monitoring + Telegram skeleton | 🔜 Next |
| v0.3 | Claude integration for diagnosis | ⏳ Planned |
| v0.4 | Approval flow + restart actions | ⏳ Planned |
| v0.5 | Jellyfin-specific health checks | ⏳ Planned |
| v1.0 | Polished, documented, public release | ⏳ Planned |

---

## Project Structure

```
project-goblin/
├── src/
│   ├── agent/          # Core polling loop and orchestration
│   ├── monitors/       # Docker + system + Jellyfin health checks
│   ├── notifiers/      # Telegram messaging
│   └── brain/          # Claude API integration
├── docs/
│   ├── architecture.md # Decision flow and design rationale
│   └── contributing.md # How to contribute
├── tests/
├── config/
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

---

## Contributing

See [`docs/contributing.md`](docs/contributing.md).

---

## License

MIT
