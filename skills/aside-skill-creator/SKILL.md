---
name: aside-skill-creator
description: >-
  Create or update Aside skills. Use when the user wants to turn reusable instructions, site instructions, workflows, domain knowledge, scripts, references, or templates into an Aside skill under the current agent's skills directory.
metadata:
  version: "0.1.0"
---

# Skill Creator

Use this skill to create or update Aside skills for the current agent.

## Where to create skills

Create user-owned skills under:

```text
<agent-dir>/skills/<skill-name>/SKILL.md
```

Use bash tool and write_file tool to create the skill file.

## Frontmatter

Aside reads `SKILL.md` frontmatter for discovery and activation. Use only fields that Aside understands:

```yaml
---
name: my-skill
description: Clear trigger description for when Aside should use this skill.
---
```

## Body

Write the body as durable operating instructions for a future Aside agent.

Keep the body concise and procedural:

1. State the workflow or decision rule.
2. Point to bundled `scripts/`, `references/`, or `assets/` only when they materially help.
3. Include concrete examples when they prevent ambiguity.
4. Remove setup notes, changelogs, implementation history, and placeholder text.

Put trigger information in `description`, not in a "When to use" body section. The body is only useful after the skill has already been selected or loaded.

## Creation Workflow

1. Clarify the reusable behavior with concrete examples.
2. Pick a short lowercase hyphen-case skill name.
3. Create or update `<agent-dir>/skills/user/<skill-name>/SKILL.md`.
4. Add only necessary resources beside that `SKILL.md`.
5. Validate the final frontmatter against Aside's supported fields.
6. Keep changes scoped to the requested skill.

## Quality Bar

- Prefer one focused skill over a broad catch-all.
- Keep instructions portable across sessions.
- Do not include icons or icon assets.
- Do not create extra README, changelog, install guide, or quick-reference files.
