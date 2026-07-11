# ai-skills-hub

542 cross-platform SKILL.md workflows for AI coding agents.

A unified skills repository that aggregates skills from Cursor (built-in + 30
plugins), Aside, Claude Code agents, and hand-curated coding workflows. Every
skill is portable across Cursor, Claude Code, Codex, Gemini CLI, Windsurf, and
other AI developer platforms.

## Skill Sources

| Source | Count | Description |
| --- | --- | --- |
| Cursor built-in | 20 | SDK, canvas, hooks, statusline, review, shell, onboard |
| Cursor plugins | 316 | 30 plugins — Cloudflare, Figma, Firebase, PostHog, Sentry, Stripe, Resend, Convex, MongoDB, and more |
| Aside built-in | 45 | Browser automation, document processing (DOCX/XLSX/PDF/PPTX), Google suite, Slack, Notion, tax forms |
| Claude agents | 60 | Code review, TDD, security, architecture, build resolvers, performance, accessibility |
| Curated skills | 101 | Code review, debugging, testing, frontend, backend, DevOps, security, documentation, MCP |

## Install

### Cursor

```bash
npx skills add KunanonJ/ai-skills-hub -g -a cursor -s '*' --copy -y
```

### Claude Code

```bash
npx skills add KunanonJ/ai-skills-hub -g -a claude-code -s '*' --copy -y
```

### Codex

```bash
npx skills add KunanonJ/ai-skills-hub -g -a codex -s '*' --copy -y
```

### Manual Copy

```bash
git clone --depth 1 https://github.com/KunanonJ/ai-skills-hub.git /tmp/ai-skills-hub
rsync -a /tmp/ai-skills-hub/skills/ ~/.claude/skills/
```

Use the target skill directory for your agent, such as `~/.claude/skills/`,
`~/.codex/skills/`, or `~/.cursor/skills/`.

### Selective Install

Install a specific category:

```bash
# Cursor plugins only
rsync -a /tmp/ai-skills-hub/skills/cursor-plugin-*/ ~/.claude/skills/

# Claude agents only
rsync -a /tmp/ai-skills-hub/skills/agent-*/ ~/.claude/skills/

# Aside skills only
rsync -a /tmp/ai-skills-hub/skills/aside-*/ ~/.claude/skills/
```

## What Is Included

### Cursor Built-in Skills

Canvas, SDK (TypeScript + Python), shell integration, statusline configuration,
hook creation, rule and skill authoring, code review (standard + Bugbot +
security), subagent creation, PR splitting, CLI config management.

### Cursor Plugin Skills (30 plugins)

| Plugin | Skills | Highlights |
| --- | --- | --- |
| Cloudflare | 19 | Workers, Durable Objects, Agents SDK, Wrangler, email service |
| PostHog | 73 | Analytics, experiments, feature flags, session replay |
| Sentry | 31 | Error tracking, alerts, PR review, SDK guides |
| pstack | 36 | Full-stack development toolkit |
| Figma | 11 | Design context, code connect, motion, slides |
| Firebase | 11 | Auth, Firestore, hosting, AI logic |
| Convex | 7 | Real-time backend, schema, functions |
| MongoDB | 8 | Queries, aggregation, schema design |
| Superpowers | 14 | Agent orchestration, workflow automation |
| Tavily | 6 | Search, crawl, extract, research |
| Resend | 5 | Email sending, React Email, CLI |
| Stripe | 4 | Payments, billing, Connect |
| Cursor Team Kit | 18 | Team collaboration, shared workflows |
| Others | 73 | Canva, Context7, Shadcn, Railway, Postman, Ponytail, and more |

### Aside Skills

Browser automation (Chrome, visual browse, CAPTCHA solving), document processing
(DOCX, XLSX, PDF, PPTX with scripts), Google suite (Docs, Gmail, Sheets, Search,
Accounts), password managers (1Password, Bitwarden, LastPass, Dashlane, Apple
Passwords), Slack, Notion, YouTube, X/Twitter, image search, and 16 site-specific
skills (GitHub, Jira, Linear, Confluence, Airtable, and more).

### Claude Code Agents

60 specialized agents covering code review, TDD, security review, architecture,
build error resolution (TypeScript, Go, Rust, Python, Java, Kotlin, Swift, C++,
Dart/Flutter, Django, PyTorch), performance optimization, accessibility, database
review, documentation, and multi-language code reviewers.

### Curated Coding Skills

| Area | Examples |
| --- | --- |
| Review and debugging | `code-review`, `bug-hunter`, `systematic-debugging` |
| Testing | `test-driven-development`, `playwright`, `property-based-testing` |
| Code quality | `clean-code`, `refactoring-patterns`, `codebase-cleanup-tech-debt` |
| Documentation | `documentation`, `architecture-patterns`, `api-design-principles` |
| Frontend | `typescript-expert`, `react-patterns`, `nextjs-best-practices` |
| Backend | `backend-api-design`, `python-best-practices`, `fastapi-pro` |
| Infrastructure | `postgresql`, `docker-patterns`, `kubernetes-patterns` |
| Delivery | `github-actions-advanced`, `ci-cd-patterns`, `deployment-patterns` |
| Security | `security-review`, `secrets-management`, `dependency-check` |
| MCP and agents | `mcp-server-patterns`, `git-worktree`, `openai-docs` |

Browse the complete set in [`skills/`](./skills/) or
[`skills-manifest.txt`](./skills-manifest.txt).

## Skill Format

Every skill follows the same structure:

```
skills/<name>/
  SKILL.md          # Main skill document with YAML frontmatter
  hooks.json        # Optional: lifecycle hooks
  scripts/          # Optional: supporting scripts
  sdk/              # Optional: type definitions or SDK files
```

Frontmatter format:

```yaml
---
name: skill-name
description: >-
  One-line description of what the skill does and when to use it.
metadata:
  version: "0.1.0"
---
```

## Validation

Check that all skills have valid frontmatter:

```bash
python -m app.skill_quality normalize-metadata --check
```

## Archive

The previous full corpus (4,874 skills) and the original 100-skill lean set are
preserved:

- Full corpus: branch `archive/full-corpus-fa85915`, tag `full-corpus-fa85915`
- Release history: v4.0.0 through v4.4.0

```bash
git fetch origin archive/full-corpus-fa85915
git checkout archive/full-corpus-fa85915
```

## Contributing

PRs welcome. Each skill needs a `SKILL.md` with valid `name` and `description`
frontmatter. Use `metadata.version: "0.1.0"` for new skills.
