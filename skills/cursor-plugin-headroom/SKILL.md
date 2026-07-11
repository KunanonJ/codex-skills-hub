---
name: cursor-plugin-headroom
description: >-
  Headroom startup hooks for Claude Code and GitHub Copilot CLI. Ensures the
  local Headroom runtime (token compression proxy) is available at session start
  and before shell/PowerShell tool use. Runs headroom init hook ensure with a
  15-second timeout.
metadata:
  version: "0.1.0"
---
# Headroom Plugin Hooks

Lightweight startup hooks that ensure the Headroom runtime is available for
Claude Code and GitHub Copilot CLI sessions.

## Hooks

| Hook | Matcher | Command | Timeout |
|------|---------|---------|---------|
| SessionStart | startup, resume | `headroom init hook ensure` | 15s |
| PreToolUse | Bash, PowerShell | `headroom init hook ensure` | 15s |

## Behavior

The `headroom init hook ensure` command checks for a matching durable
`headroom init` deployment and starts it if needed. This ensures the Headroom
compression proxy is running before any API calls are made.

## Requirements

- `headroom-ai` package installed (`uv tool install "headroom-ai[all]"` or `pip install "headroom-ai[all]"`)
- Headroom proxy initialized (`headroom init`)
