---
name: cursor-plugin-warp
description: >-
  Warp terminal integration for Claude Code — native notifications via OSC 777
  escape sequences. Hooks into SessionStart, Stop, Notification, PermissionRequest,
  UserPromptSubmit, and PostToolUse lifecycle events. Sends structured JSON payloads
  to Warp for session status, idle prompts, permission requests, and task completion.
metadata:
  version: "0.1.0"
---
# Warp Terminal Integration

Native Warp terminal notifications for Claude Code sessions. Uses OSC 777 escape
sequences to send structured JSON payloads to Warp's cli-agent notification system.

## Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| SessionStart | startup, resume | Emit plugin version, detect Warp |
| Stop | session end | Notify task completion with last query/response |
| Notification | idle_prompt | Alert when Claude is idle and waiting for input |
| PermissionRequest | tool approval | Notify when Claude needs permission to run a tool |
| UserPromptSubmit | prompt sent | Transition session status back to running |
| PostToolUse | tool complete | Transition session from blocked back to running |

## Protocol

Payloads follow the cli-agent notification schema with version negotiation:

```json
{
  "v": 1,
  "agent": "claude",
  "event": "stop|session_start|idle_prompt|permission_request|prompt_submit|tool_complete",
  "session_id": "...",
  "cwd": "...",
  "project": "..."
}
```

The `should-use-structured.sh` guard checks `WARP_CLI_AGENT_PROTOCOL_VERSION` and
`WARP_CLIENT_VERSION` to avoid sending structured notifications to Warp builds that
advertise protocol support but cannot render them.

## Scripts

- `build-payload.sh` — Shared payload builder with protocol version negotiation
- `should-use-structured.sh` — Feature detection for structured notification support
- `warp-notify.sh` — OSC 777 escape sequence emitter to `/dev/tty`
- `on-session-start.sh` — SessionStart hook handler
- `on-stop.sh` — Stop hook with transcript parsing for last query/response
- `on-notification.sh` — Idle prompt notification
- `on-permission-request.sh` — Tool permission request with human-readable summary
- `on-prompt-submit.sh` — Prompt submission status update
- `on-post-tool-use.sh` — Post-tool-use status update

## Requirements

- Warp terminal with cli-agent protocol support
- `jq` for JSON payload construction
