# Investments

Directory structure and lookup table for Schedule B (interest/dividends), Schedule D (capital gains/losses), and Form 8949 (capital asset sales).

## Directory Structure

```
irs-instructions/
├── f1040sb/
│   └── instructions.md                  # Interest/dividends over $1,500, foreign accounts
├── f1040sd/
│   ├── overview.md                      # Heading, Future Dev, What's New
│   ├── general-instructions.md          # When to use, other forms, capital assets, basis
│   ├── special-situations.md            # Capital gain distributions, home sale, partnerships
│   ├── exclusions-and-deferrals.md      # QSB stock, QOF, installment sales
│   ├── sales-and-trades.md              # Wash sales, traders, short sales, options
│   └── specific-instructions.md         # Line-by-line, carryover worksheet, 28% rate
└── f8949/
    ├── overview.md                      # Heading, Future Dev, What's New
    ├── general-instructions.md          # Purpose, who files, basis, holding periods
    ├── column-instructions.md           # Columns a-g instructions, code table, examples
    ├── reporting-requirements.md        # Parts I & II reporting requirements, box types
    ├── worksheets.md                    # Basis adjustments, market discount, CPDI worksheets
    └── qof-reporting.md                 # QOF deferral, section 1231 gains, deferred gain
```

## Lookup Table

| When working on... | Load these files |
|---|---|
| Interest/dividends detail (Schedule B) | `irs-instructions/f1040sb/instructions.md` |
| Capital gains overview (Schedule D) | `irs-instructions/f1040sd/overview.md` |
| Capital gains general instructions | `irs-instructions/f1040sd/general-instructions.md` |
| Capital gains special situations | `irs-instructions/f1040sd/special-situations.md` |
| Exclusions and deferrals (QSB, QOF) | `irs-instructions/f1040sd/exclusions-and-deferrals.md` |
| Wash sales, traders, short sales | `irs-instructions/f1040sd/sales-and-trades.md` |
| Capital gains line-by-line instructions | `irs-instructions/f1040sd/specific-instructions.md` |
| Capital asset sales overview (Form 8949) | `irs-instructions/f8949/overview.md` |
| Form 8949 general instructions | `irs-instructions/f8949/general-instructions.md` |
| Form 8949 column instructions (columns a-g) | `irs-instructions/f8949/column-instructions.md` |
| Form 8949 reporting requirements (Parts I & II) | `irs-instructions/f8949/reporting-requirements.md` |
| Form 8949 worksheets (basis, market discount) | `irs-instructions/f8949/worksheets.md` |
| QOF reporting (Form 8949) | `irs-instructions/f8949/qof-reporting.md` |

All file paths are relative to the skill root.
