# Architecture

## Overview

Jellyfin Agent is built around a single core principle: **the human stays in the loop**. The agent observes, reasons, and recommends — but never acts without explicit approval.

This document covers the decision flow, module responsibilities, and the design rationale behind key choices.

---

## Decision Flow

```
                        ┌─────────────────┐
                        │   Poll Timer    │
                        │   (60 seconds)  │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    Monitor      │
                        │                 │
                        │ • Container     │
                        │   status        │
                        │ • CPU / RAM /   │
                        │   disk          │
                        │ • Jellyfin-     │
                        │   specific      │
                        └────────┬────────┘
                                 │
                          health snapshot
                                 │
                                 ▼
                        ┌─────────────────┐
                 ┌──────│   Evaluator     │
                 │      │                 │
                 │      │ Is anything     │
                 │      │ worth flagging? │
                 │      └─────────────────┘
                 │
         YES — anomaly detected
                 │
                 ▼
        ┌─────────────────┐
        │     Brain       │
        │   (Claude API)  │
        │                 │
        │ • Plain-English │
        │   diagnosis     │
        │ • Likely cause  │
        │ • Recommended   │
        │   action        │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    Notifier     │
        │   (Telegram)    │
        │                 │
        │ Sends:          │
        │ • What's wrong  │
        │ • Why           │
        │ • Recommended   │
        │   fix           │
        │ • [Approve] btn │
        └────────┬────────┘
                 │
          user taps Approve
                 │
                 ▼
        ┌─────────────────┐
        │ Action Executor │
        │                 │
        │ • Restart       │
        │   container     │
        │ • (future)      │
        │   other actions │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    Notifier     │
        │                 │
        │ Confirms action │
        │ taken           │
        └─────────────────┘
```

---

## Module Responsibilities

### `src/agent/`
The core orchestration loop. Owns the poll timer, wires together the monitor → brain → notifier → executor pipeline, and manages state (e.g. avoiding duplicate alerts for the same issue).

### `src/monitors/`
Pluggable health-check adapters. Each monitor returns a structured snapshot. v1 ships two:
- **`docker_monitor.py`** — container status via Docker socket
- **`system_monitor.py`** — CPU, RAM, disk via `psutil`
- **`jellyfin_monitor.py`** — Jellyfin-specific signals (transcoding load, API reachability)

Designed to extend: a `PlexMonitor` or `NASMonitor` would drop in here.

### `src/brain/`
Wraps the Claude API. Takes a health snapshot, constructs a prompt, returns a structured diagnosis: what's wrong, why, and what to do. Keeps prompt logic isolated so it can be tuned without touching other modules.

### `src/notifiers/`
Telegram integration. Sends formatted alerts, handles the inline approval keyboard, and routes the user's response back to the executor. Abstracted so a future `WhatsAppNotifier` or `SlackNotifier` could slot in.

---

## Key Design Decisions

### Docker socket directly (not Portainer API)
Portainer adds a dependency and auth layer. The Docker socket gives us everything we need with fewer moving parts, and works on any Docker host.

### Telegram over WhatsApp
WhatsApp's API requires a business account and per-message cost. Telegram is free, has a clean bot API, and supports inline keyboards (essential for the approval flow) out of the box.

### LLM-powered diagnosis (not rule-based alerts)
Rule-based systems produce alerts like `CONTAINER_EXIT_CODE_137`. Claude produces: *"Jellyfin ran out of memory while transcoding — likely caused by too many simultaneous streams on this hardware. Restarting the container will bring it back; consider lowering your transcoding thread limit."* The latter is actionable. The former requires you to Google it first.

### Supervised approval model
The agent never acts unilaterally. Every recommended action is presented to the user with a one-tap approve button. This is a deliberate product choice — trust is built by being predictable, not by being fast.

---

## What's Out of Scope (v1)

- Setup wizard or guided installer
- Plex, NAS, or other platform monitors  
- Web dashboard UI
- WhatsApp notifications
- Autonomous (no-approval) mode
