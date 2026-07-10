---
name: aside-google-accounts
description: >-
  IMPORTANT- Read this skill before interacting any Google apps!
metadata:
  version: "0.1.0"
---
# Google Accounts

Use the `googleAccounts` global in the REPL tool to discover signed-in Google accounts. Uses cookie-only HTTP — no tab needed.

## Usage

```js
await googleAccounts.print();
```

## Methods

### `googleAccounts.print(): Promise<void>`

Print all signed-in Google accounts to the console. Token-efficient.

### `googleAccounts.list(): Promise<GoogleAccountInfo[]>`

Returns all signed-in Google accounts. Use this when you need programmatic access.

```ts
interface GoogleAccountInfo {
  accountId: number;      // matches Gmail /u/{uid}/
  name: string;
  email: string;
  profileImageUrl: string;
}
```
