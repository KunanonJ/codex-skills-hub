# Itemized Deductions

Directory structure and lookup table for Schedule A (itemized deductions).

## Directory Structure

```
irs-instructions/
└── f1040sa/
    ├── overview.md                      # Heading, Future Dev, What's New, General Instructions
    ├── medical-dental.md                # Medical/dental expenses, 7.5% threshold
    ├── taxes-you-paid.md                # SALT limit, income/sales tax election, worksheets
    ├── interest-you-paid.md             # Home mortgage interest, points, investment interest
    ├── gifts-to-charity.md              # Qualified orgs, $250+ gifts, AGI limits
    ├── other-deductions.md              # Casualty/theft losses, other deductions, total
    └── sales-tax-tables.md              # 2025 optional state sales tax tables
```

## Lookup Table

| When working on... | Load these files |
|---|---|
| Itemized deductions overview (Schedule A) | `irs-instructions/f1040sa/overview.md` |
| Medical/dental deductions | `irs-instructions/f1040sa/medical-dental.md` |
| SALT / property tax deductions | `irs-instructions/f1040sa/taxes-you-paid.md` |
| Mortgage / investment interest deductions | `irs-instructions/f1040sa/interest-you-paid.md` |
| Charitable contribution deductions | `irs-instructions/f1040sa/gifts-to-charity.md` |
| Other itemized deductions / totals | `irs-instructions/f1040sa/other-deductions.md` |
| State sales tax tables (Schedule A) | `irs-instructions/f1040sa/sales-tax-tables.md` |

All file paths are relative to the skill root.
