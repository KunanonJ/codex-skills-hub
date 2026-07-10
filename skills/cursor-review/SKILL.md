---
name: cursor-review
description: >-
  Review code changes with Bugbot or Security Review subagent. Use when the
  user asks to review code, check for bugs, or run a security review on their
  current changes or a PR.
metadata:
  version: "0.1.0"
---
# Review

Ask the user which review to run with the AskQuestion tool. If the AskQuestion tool is not available, ask the user directly. Provide exactly one single-select question with two options:

- `bugbot`: Bugbot (`/review-bugbot`)
- `security`: Security Review (`/review-security`)

After the user chooses, run the matching review once:

- Bugbot: follow the `/review-bugbot` instructions.
- Security Review: follow the `/review-security` instructions.
