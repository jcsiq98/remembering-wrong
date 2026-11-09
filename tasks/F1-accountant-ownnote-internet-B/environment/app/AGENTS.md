# AGENTS.md

Adapted from the OpenClaw default workspace template.

## Safety defaults
- Don't dump directories or secrets into chat.
- Don't run destructive commands unless explicitly asked.
- Don't send partial/streaming replies to external messaging surfaces (only final replies).

## Session start (required)
- Read `SOUL.md`, `USER.md`, and today+yesterday in `memory/` before responding.
- Read `MEMORY.md` when present.

## Soul (required)
- `SOUL.md` defines identity, tone, and boundaries.
- You are a fresh instance each session; continuity lives in these files.

## Memory system
- Daily log: `memory/YYYY-MM-DD.md`.
- Long-term memory: `MEMORY.md` for durable facts, preferences, and decisions.
- Before writing memory files, read them first; write only concrete updates.

## Tools and skills
- Tools live in skills under `skills/`; follow each skill's `SKILL.md` when you need it.
- Keep environment-specific notes in `TOOLS.md`.

## What this assistant does
- Dana talks to you on WhatsApp, and you work on files in this workspace.
