---
name: cursor-plugin-teamkit-rule-typescript-exhaustive-switch
description: >-
  Use exhaustive switch handling for TypeScript unions and enums
metadata:
  version: "0.1.0"
---

typescript-exhaustive-switch: In switch statements over discriminated unions or enums, use a `never` check in the default case so newly added variants cause compile-time failures until handled.
