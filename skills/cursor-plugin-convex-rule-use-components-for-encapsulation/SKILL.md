---
name: cursor-plugin-convex-rule-use-components-for-encapsulation
description: >-
  Use Convex components to encapsulate features instead of mixing everything in one codebase. Components are self-contained, reusable, and maintainable.
metadata:
  version: "0.1.0"
---

# Use Components for Encapsulation

When building features in Convex, prefer **components** over monolithic code. Components are self-contained mini-backends that encapsulate functionality.

## What Are Components?

Components are:
- 🔒 **Sandboxed** - Can't access your main app's tables unless explicitly passed
- 📦 **Self-contained** - Include their own schema, functions, and data
- 🔄 **Reusable** - Can be used across multiple projects
- 🧩 **Composable** - Multiple components work as siblings
- 📚 **npm-installable** - Install from npm or use locally

**Think of them as:** Microservices within your Convex backend, but without the deployment complexity.

## When to Use Components

### ✅ Use Components For:

**Feature Encapsulation:**
- Authentication/authorization
- File storage
- Rate limiting
- Analytics/tracking
- Notifications
- Search functionality
- Workflow orchestration
- AI agents

**Reusable Patterns:**
- Multi-tenant isolation
- Audit logging
- Caching layers
- Background job queues
- Event sourcing

**Third-Party Integrations:**
- Stripe payments
- SendGrid emails
- Cloudflare R2 storage
- External API wrappers

### ❌ Don't Use Components For:

- Core domain models that are tightly coupled
- One-off functionality specific to your app
- Simple utility functions (use convex-helpers instead)

## Component vs Monolithic Code

### ❌ Without Components (Monolithic)

```typescript
// Everything mixed in convex/files.ts
export const uploadFile = mutation({
  handler: async (ctx, args) => {
    // File upload logic
    // Rate limiting logic
    // Audit logging logic
    // Storage logic
    // All in one file!
  },
});

// Hard to:
// - Reuse in other projects
// - Test in isolation
// - Update without breaking other features
// - Share with team
```

### ✅ With Components (Encapsulated)

```typescript
// convex.config.ts
import { defineApp } from "convex/server";
import storage from "@convex-dev/storage";
import ratelimit from "@convex-dev/ratelimiter";
import audit from "./audit/convex.config";

export default defineApp({
  components: {
    storage,      // Sibling component #1
    ratelimit,    // Sibling component #2
    audit,        // Sibling component #3
  },
});

// convex/files.ts - clean and focused
import { components } from "./_generated/api";

export const uploadFile = mutation({
  handler: async (ctx, args) => {
    // Check rate limit (component)
    await components.ratelimit.check(ctx, { key: ctx.user._id });

    // Store file (component)
    const fileId = await components.storage.store(ctx, args.file);

    // Log action (component)
    await components.audit.log(ctx, { action: "upload", fileId });

    return fileId;
  },
});

// Each component:
// - Maintained separately
// - Reusable across projects
// - Testable in isolation
// - Can be updated independently
```

## Sibling Components Pattern

Multiple components at the same level (siblings) that work together:

```typescript
// convex.config.ts
export default defineApp({
  components: {
    // These are sibling components
    auth: authComponent,
    storage: storageComponent,
    payments: paymentsComponent,
    emails: emailComponent,
    analytics: analyticsComponent,
  },
});

// Usage - siblings don't see each other's internals
export const createSubscription = mutation({
  handler: async (ctx, args) => {
    // 1. Verify user (auth component)
    const user = await components.auth.getCurrentUser(ctx);

    // 2. Create payment (payments component)
    const subscription = await components.payments.createSubscription(ctx, {
      userId: user._id,
      plan: args.plan,
    });

    // 3. Track event (analytics component)
    await components.analytics.track(ctx, {
      event: "subscription_created",
      userId: user._id,
    });

    // 4. Send confirmation (emails component)
    await components.emails.send(ctx, {
      to: user.email,
      template: "subscription_confirmation",
    });

    return subscription;
  },
});
```

**Benefits:**
- Each component handles one concern
- Components can't interfere with each other
- Easy to replace one component without affecting others
- Clear boundaries between features

## Installing Components

### From npm (Official Components)

```bash
npm install @convex-dev/ratelimiter
npm install @convex-dev/storage
npm install @convex-dev/agent
```

```typescript
// convex.config.ts
import { defineApp } from "convex/server";
import ratelimiter from "@convex-dev/ratelimiter/convex.config";
import storage from "@convex-dev/storage/convex.config";

export default defineApp({
  components: {
    ratelimiter,
    storage,
  },
});
```

### Local Components (Your Own)

```bash
# Create a component directory
mkdir -p convex/components/audit
```

```typescript
// convex/components/audit/convex.config.ts
import { defineComponent } from "convex/server";

export default defineComponent("audit");

// convex/components/audit/schema.ts
export default defineSchema({
  auditLogs: defineTable({
    userId: v.id("users"),
    action: v.string(),
    timestamp: v.number(),
    metadata: v.any(),
  }).index("by_user", ["userId"]),
});

// convex/components/audit/logs.ts
export const log = mutation({
  args: {
    userId: v.id("users"),
    action: v.string(),
    metadata: v.any(),
  },
  handler: async (ctx, args) => {
    await ctx.db.insert("auditLogs", {
      ...args,
      timestamp: Date.now(),
    });
  },
});
```

```typescript
// convex.config.ts - use your local component
import { defineApp } from "convex/server";
import audit from "./components/audit/convex.config";

export default defineApp({
  components: {
    audit, // Local component as sibling
  },
});
```

## Official Components to Use

Browse the [Component Directory](https://www.convex.dev/components) for:

**Authentication:**
- `@convex-dev/better-auth` - Better Auth integration

**Storage:**
- `@convex-dev/r2` - Cloudflare R2 file storage

**Payments:**
- `@convex-dev/polar` - Polar billing/subscriptions

**AI:**
- `@convex-dev/agent` - AI agent workflows

**Backend Utilities:**
- `@convex-dev/ratelimiter` - Rate limiting
- `@convex-dev/aggregate` - Aggregations
- `@convex-dev/action-cache` - Action caching
- `@convex-dev/sharded-counter` - Distributed counters
- `@convex-dev/migrations` - Data migrations

## Creating Your Own Components

**When to create a component:**

1. **Feature is self-contained**
   - Has its own data model
   - Doesn't need direct access to main app tables
   - Can work independently

2. **You'll reuse it**
   - Across multiple projects
   - In different contexts
   - Share with team/community

3. **Clear boundaries**
   - Well-defined API surface
   - Minimal coupling to main app
   - Can be versioned independently

**Structure:**
```
convex/
├── components/
│   ├── notifications/
│   │   ├── convex.config.ts
│   │   ├── schema.ts
│   │   ├── send.ts
│   │   └── read.ts
│   ├── analytics/
│   │   ├── convex.config.ts
│   │   ├── schema.ts
│   │   └── track.ts
│   └── search/
│       ├── convex.config.ts
│       ├── schema.ts
│       └── index.ts
├── convex.config.ts  # App configuration
└── ...               # Main app code
```

## Component Communication

### ✅ Good: Parent → Component

```typescript
// Main app calls component
import { components } from "./_generated/api";

export const createUser = mutation({
  handler: async (ctx, args) => {
    const userId = await ctx.db.insert("users", args);

    // Parent app can call component
    await components.analytics.track(ctx, {
      event: "user_created",
      userId,
    });
  },
});
```

### ✅ Good: Component → Parent (via passed data)

```typescript
// Component receives parent data as arguments
import { components } from "./_generated/api";

// Pass user ID to component
await components.notifications.send(ctx, {
  userId: user._id, // From parent's user table
  message: "Welcome!",
});
```

### ❌ Bad: Component directly accessing parent tables

```typescript
// Inside component - DON'T DO THIS
export const notify = mutation({
  handler: async (ctx, args) => {
    // ❌ Can't access parent's users table
    const user = await ctx.db.get(args.userId); // Error!
  },
});
```

### ❌ Bad: Sibling → Sibling directly

```typescript
// ❌ Components can't call each other directly
// Must go through parent app
```

## Migration Strategy

### From Monolithic to Components

**Step 1:** Identify feature boundaries
```
Current: Everything in convex/
Target: Features as components
```

**Step 2:** Extract one feature as component
```bash
mkdir -p convex/components/analytics
# Move analytics code to component
```

**Step 3:** Update main app to use component
```typescript
import analytics from "./components/analytics/convex.config";

export default defineApp({
  components: { analytics },
});
```

**Step 4:** Repeat for other features

**Benefits:**
- Incremental migration (no big bang rewrite)
- Test each component independently
- Can mix monolithic + components during transition

## Best Practices

1. **One concern per component**
   - auth component handles ONLY auth
   - storage component handles ONLY storage
   - Don't create "utils" component with everything

2. **Clear API surface**
   - Export only what's needed
   - Keep internals private
   - Document component's public functions

3. **Minimize coupling**
   - Pass data as arguments, don't access parent tables
   - Make components work independently
   - Avoid tight coupling between siblings

4. **Version your components**
   - Use semantic versioning
   - Document breaking changes
   - Allow multiple versions if needed

5. **Test components in isolation**
   - Each component can be tested separately
   - Mock external dependencies
   - Integration tests at app level

## Examples from the Wild

**Multi-tenant SaaS:**
```typescript
components: {
  auth: authComponent,           // User authentication
  organizations: orgComponent,   // Multi-tenant isolation
  billing: billingComponent,     // Stripe integration
  analytics: analyticsComponent, // Event tracking
  emails: emailComponent,        // SendGrid wrapper
}
```

**E-commerce:**
```typescript
components: {
  cart: cartComponent,           // Shopping cart
  inventory: inventoryComponent, // Stock management
  orders: ordersComponent,       // Order processing
  payments: paymentsComponent,   // Payment processing
  shipping: shippingComponent,   // Shipping integration
}
```

**AI Application:**
```typescript
components: {
  agent: agentComponent,         // AI agent workflows
  embeddings: embeddingsComponent, // Vector storage
  documents: documentsComponent, // Document processing
  chat: chatComponent,           // Chat interface
}
```

## Quick Decision Tree

```
Need to add a feature?
├─ Is it self-contained? ─→ YES ─→ Use component
│                         └─ NO ─→ Add to main app
│
├─ Will you reuse it? ─→ YES ─→ Use component
│                     └─ NO ─→ Consider main app
│
├─ Third-party integration? ─→ YES ─→ Use component
│                           └─ NO ─→ Continue checking
│
└─ Complex feature with own data model? ─→ YES ─→ Use component
                                        └─ NO ─→ Main app is fine
```

## Learn More

- [Convex Components Documentation](https://docs.convex.dev/components)
- [Component Directory](https://www.convex.dev/components)
- [Using Components](https://docs.convex.dev/components/using)
- [Authoring Components](https://docs.convex.dev/components/authoring)
- [Stack: Backend Components](https://stack.convex.dev/backend-components)

## Checklist

- [ ] Identify features that could be components
- [ ] Check [Component Directory](https://www.convex.dev/components) for existing solutions
- [ ] Install components via npm or create locally
- [ ] Configure in `convex.config.ts`
- [ ] Use sibling components for feature encapsulation
- [ ] Keep components focused (one concern each)
- [ ] Test components in isolation
- [ ] Document component APIs
