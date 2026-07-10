---
name: cursor-canvas
description: >-
  A Cursor Canvas is a live React app (.canvas.tsx) that the user can open
  beside the chat. Use a canvas when the agent produces a standalone analytical
  artifact — quantitative analyses, billing investigations, security audits,
  architecture reviews, data-heavy content, timelines, charts, tables,
  interactive explorations, or any response that benefits from visual layout.
  Must read this skill when creating, editing, or debugging any .canvas.tsx file.
metadata:
  version: "0.1.0"
---
# Cursor Canvas

A canvas is a single `.canvas.tsx` file the IDE compiles so the user can open it beside the chat.

## Workflow

### 1. Decide whether to use a canvas

The trigger is **user intent**, not response shape. Ask: would the user benefit from viewing this output as its **own standalone artifact**, separate from the chat?

**Use a canvas when the agent produces new standalone analytical output:**
- Quantitative analyses and metrics breakdowns
- Billing or account investigations with structured findings
- Security audits or architecture reviews with categorized findings
- Cross-system data analyses and overlap reports
- Structured data from MCP tools where the data IS the deliverable
- Financial analyses, usage trend reports
- Tables with more than a handful of rows

**Do NOT use a canvas when:**
- The user asks for work in a **specific tool** (e.g., "create a Datadog dashboard")
- The user has a **specific deliverable** (e.g., "draft a support response", "fix this code")
- The user is **working within an existing artifact**
- Short factual answers, one-off file edits, or quick clarifying questions
- MCP tools are queried as an **intermediate step** for a different deliverable

### 2. Write the canvas

**Location.** Canvases live at `/Users/<user>/.cursor/projects/<workspace>/canvases/<name>.canvas.tsx`. The IDE only detects canvases in that exact directory — subfolders and other locations are not picked up.

**File rules:**
- Exactly one `.canvas.tsx` file per canvas. Never create helper files or supporting modules.
- Import **only** from `cursor/canvas`. No relative imports, no npm packages, no Node built-ins.
- Default-export the top-level component.
- Embed all data inline. **No `fetch()`, no network calls.**

**Never render empty states.** If a section has no data, omit it entirely.

**Label every plot.** Charts and tables must be self-describing:
- A title naming the specific metric
- Axis labels with units on both axes
- A legend when more than one series is shown
- The source and time range in a small caption

## Design guidance

Be creative. The SDK gives you expressive building blocks. But avoid slop: no gradients, no emojis, no box-shadows, no rainbow coloring. Cursor canvases are flat, minimal, and purposeful.

### Visual hierarchy

Primary content gets more space, larger headings, and accent color. Supporting content stays compact.

**Color.** All colors from `useHostTheme()` tokens. No hardcoded hex. Use accent color deliberately.

### Slop patterns — forbidden

- **Gradients** — no `linear-gradient`, `radial-gradient`
- **Emojis** — no emoji as icons, status indicators, or bullets
- **Box shadows** — no `box-shadow`. Flat surfaces only.
- **Wall of identical cards** — mix open sections with cards
- **Rainbow coloring** — most elements are neutral; color is used sparingly
- **Giant text** — font sizes above H1 (24px)
- **Decorative borders** — borders are structural, not decorative

### Pre-delivery self-check

Before returning canvas code, verify:
1. Does the layout have visual hierarchy? One thing should stand out.
2. Is there variety in the composition?
3. Slop check: scan for the forbidden patterns above.

## Introducing the canvas

Always include a markdown link to the `.canvas.tsx` file using its full absolute path. When you create a canvas, add a short note telling the user they can open it beside the chat.

## Troubleshooting

If a canvas appears blank or missing, the most common cause is that it was not written under the correct `canvases/` path. Every canvas edit returns a `Canvas TypeScript check` line reporting current type errors — treat that as authoritative diagnostics.
