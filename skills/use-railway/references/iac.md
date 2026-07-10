# Infrastructure as Code

Define, import, preview, and apply a Railway project from `.railway/railway.ts`.

Use Railway IaC when the user wants project-level configuration in source control: services, databases, buckets, volumes, variables, replicas, domains, and canvas groups. Do not use it for a single-service deploy setting that is already owned by `railway.json` or `railway.toml`; migrate that service first so there is only one source of truth.

## Files

Railway IaC uses TypeScript:

```text
.railway/railway.ts
.railway/README.md
.agents/skills/railway-config/SKILL.md
```

`railway config init` and `railway config pull` create the support files when missing. The project-local `railway-config` skill helps future agents edit `.railway/railway.ts` safely.

## Initialize or import

```bash
railway config init                         # create a starter .railway/railway.ts
railway config init --force                 # overwrite existing generated files
railway config pull                         # import the linked project
railway config pull --force                 # overwrite existing .railway/railway.ts
railway config pull --json                  # print current graph instead of writing files
railway config pull --agent                 # ask an agent to clean the import afterward
```

If the directory is not linked, the CLI prompts for project/environment in an interactive terminal. In agent workflows, prefer linking first or passing explicit project/environment context when the CLI supports it.

## Plan

Always plan before applying:

```bash
railway config plan
railway config plan --json
railway config plan --verbose
railway config plan --show-values
railway config plan --detailed-exit-code
```

Plan output summarizes changes in Terraform style:

```text
Plan: 1 to add, 0 to change, 0 to destroy
```

Variable values are redacted by default. Use `--show-values` only when the user is intentionally reviewing non-secret config or accepts the secret exposure risk. Use `--detailed-exit-code` for CI drift checks: exit `0` means no changes, exit `2` means changes are pending, and other non-zero exits are errors.

## Apply

```bash
railway config apply
railway config apply --yes
railway config apply --yes --confirm-destructive
railway config apply --json --yes --confirm-destructive
```

`apply` always runs a fresh plan first. If the environment changed after the last plan, Railway rejects the apply and asks for a new plan. In non-interactive or agent sessions, destructive changes require `--confirm-destructive` in addition to `--yes` or `--json`; do not add it unless the user explicitly approved the destructive impact.

## Authoring pattern

Keep `.railway/railway.ts` readable and explicit:

```ts
import { defineRailway, project, service } from "railway/iac";

export default defineRailway(() => {
  const web = service("web", {
    build: "pnpm build",
    start: "pnpm start",
  });

  return project("my-project", {
    resources: [web],
  });
});
```

Use imported helpers when needed: `service`, `postgres`, `redis`, `mysql`, `mongo`, `bucket`, `volume`, `group`, `github`, `image`, and `preserve`.

## Migration from config as code

When a service has `railway.json` or `railway.toml`:

1. Run `railway config pull --force`.
2. Translate only the intended service settings into `.railway/railway.ts`.
3. Remove the old service-level config file or clear its custom config file path.
4. Run `railway config plan`.
5. Apply only when the plan matches the intended migration.

If the plan shows unexpected service deletes, variable deletes, bucket deletes, or unrelated changes, stop and inspect the generated file before applying.

## Troubleshoot IaC

- **Service is already managed by `railway.json` or `railway.toml`**: migrate that service first; Railway blocks dual ownership.
- **Plan shows secrets as hidden**: this is expected. Use `--show-values` only with user approval.
- **Apply says the plan is stale**: run `railway config plan` again, inspect the new diff, then re-apply.
- **Destructive apply blocked**: get explicit user approval and rerun with `--confirm-destructive`.
- **Imported variables use `preserve()`**: Railway could not safely print encrypted secret values; preserve keeps the remote value.
- **Generated code is too literal**: edit `.railway/railway.ts` into a cleaner shape, then verify with `railway config plan`.

## Validated against

- Docs: [infrastructure-as-code.md](https://docs.railway.com/infrastructure-as-code), [infrastructure-as-code/reference.md](https://docs.railway.com/infrastructure-as-code/reference)
- CLI source: [config/mod.rs](https://github.com/railwayapp/cli/blob/v5.23.3/src/commands/config/mod.rs), [config/runner.rs](https://github.com/railwayapp/cli/blob/v5.23.3/src/commands/config/runner.rs)
