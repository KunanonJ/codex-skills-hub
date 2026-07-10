---
name: cursor-plugin-convex-rule-authentication-checks
description: >-
  Implement authentication checks in all public functions
metadata:
  version: "0.1.0"
---

# Authentication & Authorization

Every public function that accesses user data MUST verify authentication using `ctx.auth.getUserIdentity()`.

## Pattern

```typescript
export const getMyTasks = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) {
      throw new Error("Not authenticated");
    }

    const user = await getUserByIdentity(ctx, identity);
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", q => q.eq("userId", user._id))
      .collect();
  },
});
```

## Access Control Best Practices

1. **Use unguessable IDs**: Always use Convex IDs or UUIDs for access checks, never spoofable data like email addresses
2. **Check ownership**: Verify the authenticated user owns or has permission to access the resource
3. **Never trust client**: Client can send any ID—always verify server-side

## Example: Secure Update

```typescript
export const updateTask = mutation({
  args: { taskId: v.id("tasks"), text: v.string() },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const task = await ctx.db.get(args.taskId);
    if (!task) throw new Error("Task not found");

    const user = await getUserByIdentity(ctx, identity);
    if (task.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    await ctx.db.patch(args.taskId, { text: args.text });
  },
});
```
