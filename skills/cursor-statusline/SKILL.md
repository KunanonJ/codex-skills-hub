---
name: cursor-statusline
description: >-
  Configure a custom status line in the CLI. Use when the user mentions status
  line, statusline, statusLine, CLI status bar, prompt footer customization, or
  wants to add session context above the prompt.
metadata:
  version: "0.1.0"
---
# CLI Status Line

The CLI supports a user-configurable status line rendered above the prompt. A command is spawned on each conversation update, receives a JSON payload on stdin describing the session, and its stdout is displayed as the status line.

## Configuration

Add a `statusLine` entry to `~/.cursor/cli-config.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.cursor/statusline.sh",
    "padding": 2
  }
}
```

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `type` | yes | — | Must be `"command"` |
| `command` | yes | — | Path to executable or inline command. `~` is expanded. |
| `padding` | no | `0` | Horizontal inset (characters) for the status line container. |
| `updateIntervalMs` | no | `300` | Minimum interval between invocations. Clamped to >= 300ms. |
| `timeoutMs` | no | `2000` | Maximum time the command may run before killed. |

## Stdin payload

The command receives a JSON object on stdin with these fields:

| Field | Description |
|-------|-------------|
| `session_id` | Unique session identifier |
| `session_name` | Custom session name (absent if no name set) |
| `transcript_path` | Path to conversation transcript file |
| `render_width_chars` | Usable terminal columns |
| `cwd` | Current working directory |
| `autorun` | `true` when auto-run is enabled |
| `model.id`, `model.display_name` | Current model identifier and display name |
| `model.param_summary` | Formatted parameter summary (absent when empty) |
| `model.max_mode` | `true` when max mode is enabled (absent otherwise) |
| `version` | CLI version string |
| `context_window.used_percentage` | Percentage of context window used |
| `context_window.remaining_percentage` | Percentage remaining |
| `vim.mode` | `"NORMAL"` or `"INSERT"` when vim mode is enabled |
| `worktree.name` | Worktree name when running inside a worktree |

## Stdout / rendering

- **Multiple lines** are supported: each line renders as a separate row.
- **ANSI color codes** are supported (chalk, tput, `\033[32m`, etc.).
- If the command exits non-zero with empty stdout, the status line is not updated.
- If the command times out, the in-flight process is killed.
- The status line runs locally and does not consume API tokens.

## Examples

### Basic: model + context usage

```bash
#!/usr/bin/env bash
payload=$(cat)
model=$(echo "$payload" | jq -r '.model.display_name')
pct=$(echo "$payload" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
printf "\033[90m%s  ctx %s%%\033[0m" "$model" "$pct"
```

### Context progress bar

```bash
#!/usr/bin/env bash
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

BAR_WIDTH=10
FILLED=$((PCT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
BAR=""
[ "$FILLED" -gt 0 ] && printf -v FILL "%${FILLED}s" && BAR="${FILL// /▓}"
[ "$EMPTY" -gt 0 ] && printf -v PAD "%${EMPTY}s" && BAR="${BAR}${PAD// /░}"

echo "[$MODEL] $BAR $PCT%"
```

### Multi-line with git info

```bash
#!/usr/bin/env bash
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(echo "$input" | jq -r '.workspace.current_dir')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

BRANCH=""
git rev-parse --git-dir > /dev/null 2>&1 && BRANCH=" | $(git branch --show-current 2>/dev/null)"

echo -e "\033[36m[$MODEL]\033[0m ${DIR##*/}$BRANCH"
echo -e "ctx $PCT%"
```

### Inline jq command (no script file)

```json
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'"
  }
}
```

## Testing

Test a script with mock input:

```bash
echo '{"model":{"display_name":"Opus"},"context_window":{"used_percentage":25}}' | ./statusline.sh
```
