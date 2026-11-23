# Research Data QA — an Agent Skill by The Ask Why Company

Independently assess research datasets with repeatable structural checks, traceable findings, and a fail-closed quality recommendation.

**When it's used:** use when reviewing collected CSV, JSON, spreadsheet, or database-export data for completeness, consistency, provenance, evidence coverage, or readiness for later use.

Read the skill: [skills/research-data-qa/SKILL.md](skills/research-data-qa/SKILL.md)

Works with any AI agent that reads the open [Agent Skills](https://agentskills.io) `SKILL.md` format.

## Install in Claude

**Claude Code:** `/plugin marketplace add theaskwhy/research-data-qa` then `/plugin install research-data-qa@research-data-qa`. Replace the placeholder with the Git host path where you obtained this package.

**Manual:** copy `skills/research-data-qa/` into `~/.claude/skills/` or `.claude/skills/`.

**Claude.ai:** zip the `skills/research-data-qa` folder and upload it under Settings → Capabilities → Skills.

## Use it with any AI agent

This skill uses the open **Agent Skills** standard (`SKILL.md`) and works with Claude Code, OpenAI Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Antigravity, OpenCode, Goose and other compatible agents.

**Quickest:** `npx skills add theaskwhy/research-data-qa`

**Manual:** copy `skills/research-data-qa/` into your tool's skills folder, such as `~/.codex/skills/`, `.agents/skills/`, `~/.cursor/skills/`, `.github/skills/`, or `.claude/skills/`. Tools without skill support can use `SKILL.md` in their instruction file.

## Licence

MIT © The Ask Why Company LLC. A credit is appreciated if you use or adapt this skill.
