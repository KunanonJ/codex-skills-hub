---
name: cursor-create-skill
description: >-
  Create Cursor Agent Skills. Guides through authoring a new skill including
  SKILL.md structure, directory layout, description best practices, common
  patterns (template, examples, workflow, conditional, feedback loop), and
  utility scripts. Use when authoring a new skill or asking about SKILL.md
  structure.
metadata:
  version: "0.1.0"
---
# Creating Skills in Cursor

This skill guides you through creating effective Agent Skills for Cursor. Skills are markdown files that teach the agent how to perform specific tasks.

## Before You Begin: Gather Requirements

1. **Purpose and scope**: What specific task or workflow should this skill help with?
2. **Target location**: Personal skill (~/.cursor/skills/) or project skill (.cursor/skills/)?
3. **Trigger scenarios**: When should the agent automatically apply this skill?
4. **Key domain knowledge**: What specialized information does the agent need?
5. **Output format preferences**: Are there specific templates or formats required?
6. **Existing patterns**: Are there existing examples or conventions to follow?

## Skill File Structure

### Directory Layout

```
skill-name/
├── SKILL.md              # Required - main instructions
├── reference.md          # Optional - detailed documentation
├── examples.md           # Optional - usage examples
└── scripts/              # Optional - utility scripts
    ├── validate.py
    └── helper.sh
```

### Storage Locations

| Type | Path | Scope |
|------|------|-------|
| Personal | ~/.cursor/skills/skill-name/ | Available across all your projects |
| Project | .cursor/skills/skill-name/ | Shared with anyone using the repository |

**IMPORTANT**: Never create skills in `~/.cursor/skills-cursor/`. This directory is reserved for Cursor's internal built-in skills.

### SKILL.md Structure

```markdown
---
name: your-skill-name
description: Brief description of what this skill does and when to use it
disable-model-invocation: true
---

# Your Skill Name

## Instructions
Clear, step-by-step guidance for the agent.

## Examples
Concrete examples of using this skill.
```

Default `disable-model-invocation: true` so the skill only loads when named explicitly.

### Required Metadata Fields

| Field | Requirements | Purpose |
|-------|--------------|---------|
| `name` | Max 64 chars, lowercase letters/numbers/hyphens only | Unique identifier |
| `description` | Max 1024 chars, non-empty | Helps agent decide when to apply |

## Writing Effective Descriptions

1. **Write in third person**: "Processes Excel files and generates reports"
2. **Be specific and include trigger terms**: Include both WHAT and WHEN
3. **Include trigger scenarios**: "Use when working with PDF files or when the user mentions PDFs"

## Core Authoring Principles

### 1. Concise is Key

The context window is shared. Every token competes for space. Only add context the agent doesn't already have.

### 2. Keep SKILL.md Under 500 Lines

Use progressive disclosure for detailed content.

### 3. Progressive Disclosure

Put essential information in SKILL.md; detailed reference material in separate files.

### 4. Set Appropriate Degrees of Freedom

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches | Code review guidelines |
| **Medium** (pseudocode/templates) | Preferred pattern with variation | Report generation |
| **Low** (specific scripts) | Fragile operations, consistency critical | Database migrations |

## Common Patterns

### Template Pattern
Provide output format templates for consistent results.

### Examples Pattern
Show concrete input/output examples when output quality depends on seeing them.

### Workflow Pattern
Break complex operations into clear steps with checklists.

### Conditional Workflow Pattern
Guide through decision points with branching paths.

### Feedback Loop Pattern
For quality-critical tasks, implement validation loops.

## Skill Creation Workflow

### Phase 1: Discovery
Gather purpose, location, trigger scenarios, requirements, existing patterns.

### Phase 2: Design
Draft name, description, outline sections, identify supporting files.

### Phase 3: Implementation
Create directory structure, write SKILL.md, create supporting files.

### Phase 4: Verification
Verify under 500 lines, description is specific, consistent terminology, references one level deep.

## Summary Checklist

- [ ] Description is specific and includes key terms (WHAT and WHEN)
- [ ] Written in third person
- [ ] SKILL.md body is under 500 lines
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep
- [ ] No time-sensitive information
