# Adjustments & Taxes

Directory structure and lookup table for Schedules 1, 1-A, 2, and 3 — additional income, adjustments to income, additional taxes, and additional credits/payments.

## Directory Structure

```
irs-instructions/
├── f1040s1/
│   ├── additional-income-overview.md    # Part I overview: Lines 1-8z introduction
│   ├── other-income-lines.md            # Part I: Lines 2a-8z details
│   ├── income-refund-worksheet.md       # State/local refund worksheet
│   ├── adjustments-to-income.md         # Part II: Lines 11-26 overview
│   ├── ira-deduction.md                 # IRA deduction worksheet and rules
│   └── student-loan-and-other.md        # Student loan interest, other adjustments
├── f1040s1a/
│   ├── overview.md                      # General instructions, MAGI computation
│   ├── tips-definitions.md              # Part II: qualified tips definitions
│   ├── tips-calculation.md              # Part II: tips deduction calculation, up to $25K
│   ├── overtime-deduction.md            # Part III: qualified overtime, up to $12.5K
│   ├── vehicle-loan-interest.md         # Part IV: car loan interest, up to $10K
│   └── senior-deduction.md              # Part V: enhanced senior deduction, up to $6K
├── f1040s2/
│   ├── overview.md                      # General instructions
│   ├── tax-and-amt.md                   # Part I: Lines 1a-1z additions to tax, Line 2 AMT
│   └── other-taxes.md                   # Part II: Lines 4-21 (SE, household, Medicare, NIIT, etc.)
└── f1040s3/
    ├── nonrefundable-credits.md         # Lines 1-8: foreign tax, education, energy, etc.
    └── refundable-credits.md            # Lines 9-15: PTC, excess SS, fuel, other
```

## Lookup Table

| When working on... | Load these files |
|---|---|
| Tips/overtime/car loan/senior deductions | `irs-instructions/f1040s1a/*.md` |
| Additional income overview (Schedule 1 Part I) | `irs-instructions/f1040s1/additional-income-overview.md` |
| Additional income lines (Schedule 1 Part I) | `irs-instructions/f1040s1/other-income-lines.md` |
| State/local refund worksheet (Schedule 1) | `irs-instructions/f1040s1/income-refund-worksheet.md` |
| Adjustments to income (Schedule 1 Part II) | `irs-instructions/f1040s1/adjustments-to-income.md` |
| IRA deduction worksheet (Schedule 1) | `irs-instructions/f1040s1/ira-deduction.md` |
| Student loan interest / other adjustments | `irs-instructions/f1040s1/student-loan-and-other.md` |
| Schedule 2 overview / general instructions | `irs-instructions/f1040s2/overview.md` |
| AMT, additions to tax (Schedule 2 Part I) | `irs-instructions/f1040s2/tax-and-amt.md` |
| Self-employment tax, NIIT, other taxes (Schedule 2 Part II) | `irs-instructions/f1040s2/other-taxes.md` |
| Foreign tax credit, education credits | `irs-instructions/f1040s3/nonrefundable-credits.md` |
| Premium tax credit | `irs-instructions/f1040s3/refundable-credits.md` |

All file paths are relative to the skill root.
