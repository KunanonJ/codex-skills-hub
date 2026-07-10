---
name: cursor-plugin-convex-rule-async-handling
description: >-
  Always await promises in Convex functions to prevent unexpected behavior
metadata:
  version: "0.1.0"
---

# Async Handling in Convex

Always await all promises in Convex functions. Not awaiting promises (e.g., `await ctx.scheduler.runAfter`, `await ctx.db.patch`, `await ctx.db.insert`) may cause unexpected behavior.

## Examples

**Bad:**
```typescript
export const updateUser = mutation({
  handler: async (ctx, args) => {
    ctx.db.patch(args.userId, { name: args.name }); // Missing await
  }
});
```

**Good:**
```typescript
export const updateUser = mutation({
  handler: async (ctx, args) => {
    await ctx.db.patch(args.userId, { name: args.name });
  }
});
```

Enable the `no-floating-promises` ESLint rule to catch these errors.
