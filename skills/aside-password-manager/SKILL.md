---
name: aside-password-manager
description: >-
  Use Aside Password Manager when it helps with login, signup, password generation, credential storage, payment card / identity autofill on checkout forms, or querying the user's saved credentials.
metadata:
  version: "0.1.0"
---
# Password Manager

Aside Password Manager is a native credential manager the agent can use without seeing generated passwords.
Use `passwordManager` in the REPL to autofill logins, payment cards, and identities, create signup password refs, search saved credential sites, and store credentials.

Before using Aside Password Manager as the website login source, check `memory/USER.md` for connected external password manager preferences.
If the user configured one or more external providers, try a connected provider first and use Aside Password Manager to unlock that provider or as the fallback.
If no connected external provider preference is present, use Aside Password Manager as the default login/autofill source.

## Use Cases

### 1. Check websites the user is using

When searching for task-relevant information, saved credential sites are useful hints about services the user already uses.
It never exposes the secret values so it's safe to use for searching.

```js
const keywords = ['search 1', 'search 2', 'search 3'];
const vaults = await passwordManager.listVaults();
// vaults: [{ vaultId, name }, ...]
const results = await Promise.all(keywords.map(k => passwordManager.listItems({ text: k })));
// results: [[{ title, urls, category, username, oauth, primaryHost, vaultId, itemId }, ...], ...]
```

Use these results to find relevant sites the user already uses.

### 2. Autofill a selected item

When you are on a login page, search login candidates with `listItems(...)`, then use `autofillItem(page, itemId)` only after selecting a clearly matching item.
`listItems(...)` may return multiple candidates. Choose by site, title, username/OAuth account, URLs, and task context. Ask only when the right account is genuinely ambiguous - last resort!
If Aside has no usable login, continue normal page inspection. Users may have other password managers (e.g. 1Password), and focusing a field may reveal their autofill UI.

```js
const candidates = await passwordManager.listItems({ text: 'example.com', category: 'login' });
console.log(candidates);

// If one candidate clearly matches the user's task, use it and continue browsing.
await passwordManager.autofillItem(page, '<selected-item-id>');
```

### 3. Autofill a payment card or identity on checkout forms

`autofillItem` also fills `credit-card` and `identity` items. On a payment/checkout form, search card items and autofill the matching one instead of asking the user to type card details. It fills card number, holder name, expiry, and CVV across the form (including hosted card-number iframes) without exposing the values to you.

```js
const cards = await passwordManager.listItems({ category: 'credit-card' });
console.log(cards);

// Make sure the card form is visible (e.g. the "credit card" payment method is selected), then:
await passwordManager.autofillItem(page, '<selected-card-item-id>');
// Verify from a fresh snapshot that the visible card fields are filled. Never print card values.
```

Billing name/address fields are not card data; fill them from a matching `identity` item or the user's known profile.

### 4. Sign up

If signup is needed to complete the task, save the new credential in Aside vault unless the user explicitly says not to.
For email or username, prefer a common ID / email that the user uses from the user's existing items.
For password: never create or inspect the password yourself. Use `generatePassword(...)`, which returns only a `GeneratedPasswordRef`. Pass only constraints the site explicitly requires.

```js
const passwordRef = await passwordManager.generatePassword({
  length: 12,
  include: ['lowercase', 'uppercase', 'digit', 'symbol'],
  symbols: '!@#$%^&*',
});
```

Pass the reference into the page field. Use a field ref from the latest snapshot.

```js
await passwordManager.fillPassword(page, 'e32', passwordRef);
// proceed to sign up...
```

After signup completes, YOU SHOULD save the credential, unless it would be lost.
Before creating a new item, call `listVaults()`. Choose a vault from a matching existing item, a clearly relevant vault name, or other task context. If there is no better signal, use the first vault.

```js
const vaults = await passwordManager.listVaults();
await passwordManager.createItem({
  vaultId: vaults[0].vaultId,
  category: 'login',
  title: '<human-readable title>',
  urls: ['<page URL>'],
  notes: '<context>',
  fields: [
    { label: 'username', value: username, designation: 'username' },
    { label: 'password', value: passwordRef, designation: 'password', isSecret: true },
  ],
});
```

For reset-password or change-password flows, do not create a duplicate item when the existing item is clear from search results or task context. After the password change succeeds, update the existing item:

```js
await passwordManager.updateItem(itemId, {
  fields: [
    { label: 'password', value: passwordRef, designation: 'password', isSecret: true },
  ],
});
```

### 5. Save credentials

If a website shows a one-time secret, API key, token, SSH key, recovery code, or similar credential that the user may need later, save it in Aside password manager.
Before saving, call `listVaults()` and choose the most context-appropriate vault. If none is obvious, use the first vault.

```js
const secret = await page.locator('<refId>').textContent();
const vaults = await passwordManager.listVaults();
await passwordManager.createItem({
  vaultId: vaults[0].vaultId,
  category: 'api-credential',
  title: '<human-readable title>',
  notes: '<context>',
  urls: ['<page URL>'],
  fields: [
    { label: 'secret', value: secret, isSecret: true },
  ],
});
```

Use `isSecret: true` for values that should be stored as secret/guarded fields. Use a specific category when it is obvious, such as `api-credential` or `ssh-key`. Use `secure-note` when the credential does not fit a structured category.

## API Contract

```ts
declare global {
  passwordManager: PasswordManagerApi;
}

interface PasswordManagerApi {
  /** List available vaults so the agent can choose a save target. */
  listVaults(): Promise<{ vaultId: string; name: string; }[]>;

  /** List vault items for task-relevant sites or credentials. */
  listItems(query?: { text?: string; category?: VaultItemCategory; url?: string; vaultId?: string }): Promise<VaultItemSummary[]>;

  /** Autofill a clearly selected item (login, credit-card, or identity) into the current page without exposing secrets to the agent. */
  autofillItem(page: Page, itemId: string): Promise<void>;

  /** Unlock a connected external password manager using the saved unlock item from Password settings. */
  unlockExternalPasswordManager(page: Page, provider: ExternalPasswordManagerProvider): Promise<void>;

  /** Create an opaque generated-password reference that can be filled or saved but never inspected. */
  generatePassword(options?: PasswordGenerationOptions): Promise<GeneratedPasswordRef>;

  /** Fill a page field with a generated password reference. The password value remains hidden from the agent. */
  fillPassword(page: Page, fieldRef: string, password: GeneratedPasswordRef): Promise<void>;

  /** Create a new vault item. `GeneratedPasswordRef` values are resolved inside password manager. */
  createItem(input: CreateVaultItemInput): Promise<{ itemId: string }>;

  /** Update an existing vault item. Ask the user first if the item or update intent is ambiguous. */
  updateItem(itemId: string, updates: Partial<Pick<CreateVaultItemInput, 'title' | 'urls' | 'fields' | 'notes'>>): Promise<void>;
}

type GeneratedPasswordRef = typeof Symbol('<opaque-handle-of-generated-password>');

type VaultItemCategory = 'login' | 'credit-card' | 'secure-note' | 'identity' | 'password' | 'document' | 'software-license' | 'bank-account' | 'database' | 'driver-license' | 'outdoor-license' | 'membership' | 'passport' | 'rewards-program' | 'social-security' | 'wireless-router' | 'server' | 'email-account' | 'api-credential' | 'medical-record' | 'ssh-key';

type ExternalPasswordManagerProvider = '1password' | 'bitwarden' | 'dashlane' | 'lastpass';

type PasswordGenerationOptions = {
  /** Target length for the site's password rules. Defaults to 20; change only when the site requires a different length. */
  length?: number;
  /** Character classes required by the site. Defaults to all four classes. */
  include?: Array<'lowercase' | 'uppercase' | 'digit' | 'symbol'>;
  /** Symbol set allowed by the site. Defaults to password-manager's standard safe symbols. */
  symbols?: string;
};

type CreateVaultItemInput = {
  vaultId: string;
  category: VaultItemCategory;
  title: string;
  urls?: string[];
  loginType?: 'password' | 'oauth' | 'passkey';
  oauth?: { provider: string; account?: string };
  fields: Array<{
    label: string;
    value: string | GeneratedPasswordRef;
    designation?: 'username' | 'password';
    isSecret?: boolean;
  }>;
  /** leave a concise, user-rememberable context about why you've created */
  notes?: string;
};

type VaultItemSummary = {
  vaultId: string;
  itemId: string;
  title: string;
  urls: string[];
  category: VaultItemCategory;
  /** Username, when the item is login-like and has one. */
  username?: string;
  /** Login mechanism, when the item is login-like and known. */
  loginType?: 'password' | 'oauth' | 'passkey';
  /** @example {"provider": "google", "account": "jun@aside.com"} */
  oauth?: { provider: string; account: string };
  /** Main saved host for quick comparison with task-relevant sites. */
  primaryHost?: string;
};
```
