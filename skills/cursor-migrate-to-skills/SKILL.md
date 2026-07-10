---
name: cursor-migrate-to-skills
description: >-
  Convert 'Applied intelligently' Cursor rules (.cursor/rules/*.mdc) and slash
  commands (.cursor/commands/*.md) to Agent Skills format (.cursor/skills/). Use
  when you want to migrate rules or commands to skills, convert .mdc rules to
  SKILL.md format, or consolidate commands into the skills directory.
metadata:
  version: "0.1.0"
---
# Migrate Rules and Slash Commands to Skills

Convert Cursor rules ("Applied intelligently") and slash commands to Agent Skills format.

**CRITICAL: Preserve the exact body content. Do not modify, reformat, or "improve" it - copy verbatim.**

## Locations

| Level | Source | Destination |
|-------|--------|-------------|
| Project | `{workspaceFolder}/**/.cursor/rules/*.mdc`, `{workspaceFolder}/.cursor/commands/*.md` | `.cursor/skills/` |
| User | `~/.cursor/commands/*.md` | `~/.cursor/skills/` |

Notes:
- Cursor rules inside the project can live in nested directories. Be thorough in your search.
- Ignore anything in ~/.cursor/worktrees
- Ignore anything in ~/.cursor/skills-cursor (reserved for Cursor's internal built-in skills)

## Finding Files to Migrate

**Rules**: Migrate if rule has a `description` but NO `globs` and NO `alwaysApply: true`.

**Commands**: Migrate all - they're plain markdown without frontmatter.

## Conversion Format

### Rules: .mdc → SKILL.md

```markdown
# Before: .cursor/rules/my-rule.mdc
---
description: What this rule does
globs:
alwaysApply: false
---
# Title
Body content...
```

```markdown
# After: .cursor/skills/my-rule/SKILL.md
---
name: my-rule
description: What this rule does
---
# Title
Body content...
```

Changes: Add `name` field, remove `globs`/`alwaysApply`, keep body exactly.

### Commands: .md → SKILL.md

```markdown
# Before: .cursor/commands/commit.md
# Commit current work
Instructions here...
```

```markdown
# After: .cursor/skills/commit/SKILL.md
---
name: commit
description: Commit current work with standardized message format
disable-model-invocation: true
---
# Commit current work
Instructions here...
```

Changes: Add frontmatter with `name` (from filename), `description` (infer from content), and `disable-model-invocation: true`, keep body exactly.

## Notes

- `name` must be lowercase with hyphens only
- `description` is critical for skill discovery
- Optionally delete originals after verifying migration works

## Workflow

1. Create the skills directories if they don't exist
2. Find files to migrate in both project and user directories
3. For rules, check if it's an "applied intelligently" rule (has `description`, no `globs`, no `alwaysApply: true`). Commands are always migrated.
4. Make a list of files to migrate. If empty, done.
5. For each file, read it, then write the new skill file preserving the body content EXACTLY.
6. Delete the original file.
7. Summarize the results. Let the user know they can ask to undo the migration.

**CRITICAL: Copy the body content character-for-character. Do not reformat, fix typos, or "improve" anything.**
