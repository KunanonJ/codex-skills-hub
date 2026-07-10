---
name: aside-site-amazon
description: >-
  Amazon shopping, orders, and account-state guidance.
metadata:
  version: "0.1.0"
---
# Amazon

## Canonical URLs

- Home: `https://www.amazon.com/`
- Search: `https://www.amazon.com/s?k=${query}`
- Orders: `https://www.amazon.com/gp/css/order-history?ref_=nav_orders_first`
- Cart: `https://www.amazon.com/gp/cart/view.html?ref_=nav_cart`
- Account: `https://www.amazon.com/gp/css/homepage.html`

## Efficient Snapshot Strategy

Amazon's snapshot results are large. You should use below selectors to minimize the amount of content captured.
If it's updated, please update this SKILL.md to reflect the new selector.

- On search result page: use `snapshot(page, { selector: '[data-component-type="s-search-results"]' })`
- On cart page: `snapshot(page, { selector: '#activeCartViewForm' })`.
  - Checkout button is outside the form and it can be found via `<input name="proceedToRetailCheckout">` 

## Working style

- Avoid the home page unless the user explicitly wants it. It is noisy and ad-heavy.
- Before anything involving orders, returns, payments, or addresses, verify the active account and address in the header.
- Prefer `Your Orders` for shipment, invoice, return, and rebuy tasks.
- Prefer `Cart` for quantity and checkout-adjacent tasks.
- Re-snapshot after navigation and after inline card expansion because Amazon frequently re-renders order cards.

## Useful shortcuts

- Search: `Option+/`
- Cart: `Shift+Option+C`
- Home: `Shift+Option+H`
- Orders: `Shift+Option+O`
- Shortcuts help: `Shift+Option+Z`
