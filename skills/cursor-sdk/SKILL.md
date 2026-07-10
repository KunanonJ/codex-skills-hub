---
name: cursor-sdk
description: >-
  Guide users building apps, scripts, CI pipelines, or automations on top of the
  Cursor SDK — TypeScript (@cursor/sdk) or Python (cursor-sdk / cursor_sdk).
  Covers Agent.create, Agent.prompt, Agent.resume, streaming, local vs cloud
  runtime, MCP servers, error handling, and production best practices. Use when
  the user mentions integrating or writing code against the Cursor SDK.
metadata:
  version: "0.1.0"
---
# Cursor SDK

The Cursor SDK runs Cursor agents programmatically. Two language variants share the same concepts:

- **TypeScript** (`@cursor/sdk`, npm) - docs at cursor.com/docs/sdk/typescript
- **Python** (`cursor-sdk`, pip) - docs at cursor.com/docs/sdk/python

Both are in public beta and follow the same `Agent` → `Run` model across local (runs on the caller's machine against `cwd`) and cloud (runs on a Cursor-hosted VM against a cloned repo) runtimes.

## Pick the language

1. **The user named it.** Go with what they named.
2. **The codebase signals it.** `pyproject.toml` / `.py` files → Python. `package.json` / `.ts` files → TypeScript.
3. **No signal either way.** Ask: *"TypeScript or Python?"*

## The Three Invocation Patterns

### 1. `Agent.prompt(...)` - one-shot

Fire-and-forget scripts, GitHub Actions steps, "send prompt, get result, exit" flows. No streaming, no follow-ups, no cleanup to remember.

**TypeScript:**
```typescript
import { Agent } from "@cursor/sdk";
const result = await Agent.prompt("Refactor src/utils.ts for readability", {
  apiKey: process.env.CURSOR_API_KEY!,
  model: { id: "composer-2.5" },
  local: { cwd: process.cwd() },
});
console.log(result.status, result.result);
```

**Python:**
```python
from cursor_sdk import Agent, AgentOptions, LocalAgentOptions
result = Agent.prompt(
    "Refactor src/utils.py for readability",
    AgentOptions(api_key=os.environ["CURSOR_API_KEY"], model="composer-2.5",
                 local=LocalAgentOptions(cwd=os.getcwd())),
)
print(result.status, result.result)
```

### 2. `Agent.create(...)` + `agent.send(...)` - durable with follow-ups

Streaming, multi-turn conversation, lifecycle operations (cancel, status listener).

**TypeScript:**
```typescript
import { Agent } from "@cursor/sdk";
await using agent = await Agent.create({
  apiKey: process.env.CURSOR_API_KEY!, model: { id: "composer-2.5" },
  local: { cwd: process.cwd() },
});
const run = await agent.send("Find the bug in src/auth.ts");
for await (const event of run.stream()) {
  if (event.type === "assistant")
    for (const block of event.message.content)
      if (block.type === "text") process.stdout.write(block.text);
}
await run.wait();
const run2 = await agent.send("Now write a regression test for it");
await run2.wait();
```

**Python:**
```python
from cursor_sdk import Agent, LocalAgentOptions
with Agent.create(model="composer-2.5", api_key=os.environ["CURSOR_API_KEY"],
                  local=LocalAgentOptions(cwd=os.getcwd())) as agent:
    run = agent.send("Find the bug in src/auth.py")
    for message in run.messages():
        if message.type == "assistant":
            for block in message.message.content:
                if block.type == "text": print(block.text, end="")
    run.wait()
    run2 = agent.send("Now write a regression test for it")
    run2.wait()
```

### 3. `Agent.resume(...)` - pick up an existing agent later

Cross-process boundaries: cron continuations, webhooks, interactive CLIs. Runtime is auto-detected from the ID prefix — `bc-` is cloud, anything else is local.

**TypeScript:**
```typescript
await using agent = await Agent.resume(previousAgentId, { apiKey });
const run = await agent.send("Also update the changelog");
await run.wait();
```

**Python:**
```python
with Agent.resume(previous_agent_id, AgentOptions(api_key=os.environ["CURSOR_API_KEY"])) as agent:
    run = agent.send("Also update the changelog")
    run.wait()
```

**Inline MCP servers are not persisted across resume** — pass them again.

## Top Five Traps

1. **Wrong runtime by accident**: Always set `local` or `cloud` explicitly — the SDK defaults to local silently.
2. **Two kinds of failure**: Thrown `CursorAgentError` = run never executed (auth, config). `result.status == "error"` = run executed and failed. Different fixes.
3. **Forgetting to dispose**: Use `await using` (TS) or `with ... as agent:` (Python). Skipping disposal leaks child processes and memory.
4. **Streaming is optional but `wait()` is required**: `wait()` returns the terminal result. Always call it.
5. **Not every operation is supported on every runtime**: Guard with `run.supports("cancel")` before calling.

## Local vs Cloud

- **Local** — runs on the caller's machine against `cwd`. Good for dev loops and CI with a repo checkout.
- **Cloud** — runs on a Cursor-hosted VM against a freshly cloned repo. Good for long jobs and fire-and-forget automation.

## Auth

```bash
export CURSOR_API_KEY="cursor_..."
```

Both SDKs read `CURSOR_API_KEY` when no key is passed explicitly.

## Model Selection

`composer-2.5` is the current default. `model="auto"` lets the server pick. `Cursor.models.list()` returns valid IDs.

## MCP Servers

Both SDKs support HTTP (with `headers` or OAuth `auth`) or stdio (`command` / `args` / `env`). Pass servers inline on `Agent.create` or `agent.send`.

- **Inline servers fully replace creation-time servers on a per-send override — not merged.**
- **Resume requires re-passing servers** — they are not persisted.

## Production Best Practices

1. **Always dispose.** `await using` (TS) or `with ... as agent:` (Python).
2. **Distinguish startup vs run failures.** Exit 1 for `CursorAgentError`, exit 2 for `result.status == "error"`.
3. **Log `run.id` and `agent.agentId` immediately after `send()`.**
4. **Respect `error.isRetryable`.** Blind retries can cause duplicate cloud runs.
5. **Always pass `apiKey` explicitly** in shared-infrastructure code.
6. **Prefer `Agent.prompt(...)` for true one-shots** — it disposes for you.
