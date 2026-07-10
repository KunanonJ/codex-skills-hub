---
name: cursor-plugin-teamkit-rule-no-inline-imports
description: >-
  Keep imports at top of file and avoid inline imports
metadata:
  version: "0.1.0"
---

# No inline imports

Always place imports at the top of the module. Avoid inline imports in function bodies, type annotations, or interface fields unless there is a strict circular-dependency reason and it is documented.
