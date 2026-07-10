---
name: cursor-automate
description: >-
  Create Cursor Automations interactively. Use when the user explicitly wants
  to make, build, set up, or create a new Cursor Automation — for example
  "create a Cursor automation", "open the Automations editor with this draft",
  or "set up a scheduled Cursor agent".
metadata:
  version: "0.1.0"
---
# Create Automation (Interactive)

Use this skill when the user explicitly wants to make, build, set up, or create a new **Cursor Automation** — for example "create a Cursor automation", "open the Automations editor with this draft", or "set up a scheduled Cursor agent".

**Disambiguation.** "Automation" in a user workspace can mean many things (`.github/workflows`, CI pipelines, scheduled jobs, scripts, dbt, browser automation, shell scripts, workflow engines). Do **not** assume generic phrases like "automate this", "help me automate my deploys", or "make an automation" mean **Cursor Automation**. Route to the named surface when the user mentions one, use normal repo/product exploration when the context points elsewhere, or ask a short clarifying question when the target surface is ambiguous.

## Execution spine (every run)

1. **Finish-path check.** Verify the in-app Automations editor handoff is available. If not, immediately say "Please use this skill in the Agents Window." and stop.
2. **Capture intent + proactive integration discovery.** If the prompt is missing 2+ of {what kicks it off, what should happen, what outcome}, send one short message asking for a 1-2 sentence description. Proactively run discovery for any integration the user named or implied.
3. **Completeness gates.** Work through trigger, tool, prompt, naming, and PCD checks. Do not jump to a summary while required fields are still unknown.
4. **One consolidated question.** Ask inline for whatever integration discovery couldn't resolve.
5. **Draft table → approval → finish handoff.** Show a compact Markdown table recapping name / description, trigger, tools, instructions, resolved settings, and "to finish in editor". User approves, then open the Automations editor.

## House rules

- **Plain language only.** Never show MCP / tool / proto names, enum values, or raw CLI output in user-visible chat.
- **No YAML in finalization.** The draft table = compact Markdown only.
- **No automatic fallbacks.** Never submit, open a URL, paste a browser prefill link, or switch buckets.
- **Creation-only.** This skill prepares new automations only. Do not list, get, inspect, update, or search existing Cursor Automations from chat.

## Trigger categories

| Trigger | Description |
|---------|-------------|
| On a schedule | Cron-based recurring runs |
| On a GitHub / GitLab event | PR opened, pushed, merged, commented, label change, branch push, CI completed |
| On a Slack event | New message, reaction added, channel created |
| On a Linear event | Issue created, status changed, end of cycle |
| On a PagerDuty incident | Incident triggered, acknowledged, resolved, any |
| On a Sentry issue | Issue created, resolved, assigned, archived, unresolved, any |
| On an incoming HTTP webhook | Webhook trigger |

## Available tools

| Label | Purpose |
|-------|---------|
| Comment on PRs | Post comments on pull requests |
| Post to Slack | Send messages to Slack channels |
| Read Slack | Read messages from Slack channels |
| Request reviewers | Assign PR reviewers |
| Manage check runs | Create/update CI check runs |
| Use MCP server | Call tools from connected MCP servers |

## Authoring funnel

Work in Automations UI order: trigger → tools → prompt → name/description → draft table.

1. **Trigger**: Pick from the trigger categories above, resolve picker-backed values via integration discovery.
2. **Tools**: Select which tools the automation needs.
3. **Prompt + name**: Ask "What should the agent do when [trigger]?" Suggest a name + 1-2 sentence description.
4. **Draft table**: Recap as a compact Markdown table. Get approval.
5. **Finish**: Open the Automations editor with the reviewed draft.

## Draft table format

| Draft field | What will open in the editor |
|-------------|------------------------------|
| Name / description | Short plain-language value |
| Trigger | What starts the automation |
| Tools | Enabled capabilities |
| Instructions | The prompt behavior, summarized |
| Resolved settings | Repo / branch, Slack channel, service / project, schedule |
| To finish in editor | Settings deferred to the Automations UI; write "None" if nothing is deferred |
