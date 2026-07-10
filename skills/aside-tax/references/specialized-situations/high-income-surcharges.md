# High-Income Surcharges: NIIT + Additional Medicare Tax

Two surcharges apply to high-income taxpayers. Both feed into **Schedule 2** and add to total tax on Form 1040 line 23.

## Additional Medicare Tax (Form 8959)

### What It Is

A 0.9% surtax on Medicare wages, RRTA compensation, and self-employment income above threshold amounts.

### Thresholds (not indexed for inflation)

| Filing Status | Threshold |
|---|---|
| MFJ | $250,000 |
| MFS | $125,000 |
| Single / HOH / QSS | $200,000 |

### Who Must File Form 8959

- Any single W-2 with Box 5 (Medicare wages) > $200,000, **or**
- Combined Medicare wages + SE income exceed the threshold for filing status

### Computation Notes

- Medicare wages and SE income are **combined** against the threshold. A self-employment loss is ignored (not negative).
- Employers must withhold 0.9% on wages exceeding $200,000 regardless of filing status. The withholding threshold ($200K) differs from the MFJ tax threshold ($250K) — MFJ filers may owe additional tax even if neither spouse exceeded $200K individually.
- The withholding from W-2 Box 6 that is attributable to Additional Medicare Tax is reconciled on Form 8959 and any excess is credited on Form 1040.

### Form Flow

Form 8959 → Schedule 2 line 11 → Form 1040 line 23

---

## Net Investment Income Tax — NIIT (Form 8960)

### What It Is

A 3.8% surtax on the lesser of: net investment income, or MAGI exceeding the threshold.

### Thresholds (not indexed for inflation)

| Filing Status | Threshold |
|---|---|
| MFJ / QSS | $250,000 |
| MFS | $125,000 |
| Single / HOH | $200,000 |

### What Counts as Net Investment Income

- Interest, dividends, capital gains, rental/royalty income, passive business income
- **Not** included: wages, SE income, Social Security, tax-exempt interest, distributions from qualified retirement plans
- Digital asset gains are subject to NIIT

### Computation

The tax is 3.8% of the **lesser of**:
- Net investment income (Form 8960 Part I minus Part II deductions), or
- MAGI minus the threshold

If MAGI is at or below the threshold, NIIT is zero regardless of investment income.

### Form Flow

Form 8960 → Schedule 2 line 12 → Form 1040 line 23

---

## When Both Apply

High-income taxpayers with both earned and investment income often owe both surcharges. They are computed independently — Additional Medicare Tax on earned income, NIIT on investment income.

## Key Instructions

- `irs-instructions/f8959/general-instructions.md` — Additional Medicare Tax rules, threshold chart, examples
- `irs-instructions/f8959/line-instructions.md` — Form 8959 line-by-line
- `irs-instructions/f8960/overview.md` — NIIT overview
- `irs-instructions/f8960/general-instructions.md` — who must file, definitions
- `irs-instructions/f8960/investment-income.md` — what counts as net investment income
- `irs-instructions/f8960/expenses-and-tax.md` — deductions and tax computation
