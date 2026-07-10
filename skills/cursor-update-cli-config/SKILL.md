---
name: cursor-update-cli-config
description: >-
  View and modify Cursor CLI configuration settings in
  ~/.cursor/cli-config.json. Use when the user wants to change CLI settings,
  configure permissions, switch approval mode, enable vim mode, toggle display
  options, configure sandbox, or manage any CLI preferences.
metadata:
  version: "0.1.0"
---
# Cursor CLI Configuration

View and modify Cursor CLI settings stored in `~/.cursor/cli-config.json`.

## Config File Location

The config file is `~/.cursor/cli-config.json`.

Projects can layer overrides via `.cursor/cli.json` files. The CLI walks from the git root to the current working directory and merges each `.cursor/cli.json` it finds (deeper files take precedence). Project overrides only affect the current session.

## How to Modify

Read `~/.cursor/cli-config.json`, apply changes, and write it back. Changes take effect after restarting the CLI.

## Available Settings

### `permissions` (required)
Tool permission rules. Each entry is a string pattern.
- `allow`: string[] — patterns for allowed tool calls (e.g. `"Shell(**)"`, `"Mcp(server-name, tool-name)"`)
- `deny`: string[] — patterns for denied tool calls

### `editor`
- `vimMode`: boolean — enable vim keybindings
- `defaultBehavior`: `"ide"` | `"agent"` — default behavior mode

### `display` (optional)
- `showLineNumbers`: boolean (default: false) — show line numbers in code output
- `showThinkingBlocks`: boolean (default: false) — show model thinking/reasoning blocks
- `showStatusIndicators`: boolean (default: false) — show status indicators

### `channel` (optional)
Release channel: `"prod"` | `"lab"` | `"static"`

### `maxMode` (optional)
boolean (default: false) — enable max mode for higher-quality model responses

### `approvalMode` (optional)
Controls tool approval behavior:
- `"allowlist"` (default) — require approval for tools not in the allow list
- Run Everything — auto-approve all tool calls (same as `--force` / `--yolo`)

### `sandbox` (optional)
Sandbox execution environment settings:
- `mode`: `"disabled"` | `"enabled"` (default: `"disabled"`)
- `networkAccess`: `"user_config_only"` | `"user_config_with_defaults"` | `"allow_all"`
- `networkAllowlist`: string[] — domains the sandbox is allowed to reach

### `network` (optional)
- `useHttp1ForAgent`: boolean (default: false) — use HTTP/1.1 instead of HTTP/2

### `bedrock` (optional)
AWS Bedrock integration settings:
- `enabled`: boolean (default: false)
- `mode`: `"access-key"` | `"team-role"`
- `region`: string — AWS region
- `testModel`: string — model to use for testing

### `attribution` (optional)
Controls how agent work is attributed in git:
- `attributeCommitsToAgent`: boolean (default: true)
- `attributePRsToAgent`: boolean (default: true)

### `webFetchDomainAllowlist` (optional)
string[] — domains the web fetch tool is allowed to access

## Fields You Should NOT Modify

These are internal/cached state:
- `version` — config schema version
- `model` / `selectedModel` / `modelParameters` — managed by the model picker
- `privacyCache` — cached privacy mode state
- `authInfo` — cached authentication info
