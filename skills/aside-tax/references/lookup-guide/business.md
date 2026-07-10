# Business

Directory structure and lookup table for Schedule C (business income) and Schedule SE (self-employment tax).

## Directory Structure

```
irs-instructions/
├── f1040sc/
│   ├── overview.md                      # Heading, Future Dev, What's New, Reminders
│   ├── general-instructions.md          # When to use, other forms, LLC, spouses
│   ├── specific-lines-a-i.md            # Lines A-I: activity, EIN, accounting method
│   ├── income.md                        # Part I: gross receipts, 1099s, other income
│   ├── expense-lines.md                 # Part II: expense lines 9-27
│   ├── business-use-of-home.md          # Line 30: home office (simplified & actual method)
│   ├── net-profit-loss.md               # Lines 28-32: net profit or loss computation
│   ├── cost-of-goods-sold.md            # Part III: inventory, small business exception
│   ├── vehicle-and-other.md             # Parts IV & V: vehicle info, other expenses
│   └── activity-codes.md                # Principal Business or Professional Activity Codes
└── f1040sse/
    ├── general-instructions.md          # Self-employment tax overview, who must file
    ├── line-instructions.md             # Line-by-line instructions for SE tax computation
    └── net-earnings.md                  # Net earnings from self-employment, optional methods
```

## Lookup Table

| When working on... | Load these files |
|---|---|
| Business income overview (Schedule C) | `irs-instructions/f1040sc/overview.md` |
| Business general instructions (Schedule C) | `irs-instructions/f1040sc/general-instructions.md` |
| Business Lines A-I (Schedule C) | `irs-instructions/f1040sc/specific-lines-a-i.md` |
| Business gross receipts / income | `irs-instructions/f1040sc/income.md` |
| Business expense lines 9-27 (Schedule C) | `irs-instructions/f1040sc/expense-lines.md` |
| Business use of home (Schedule C line 30) | `irs-instructions/f1040sc/business-use-of-home.md` |
| Net profit or loss (Schedule C lines 28-32) | `irs-instructions/f1040sc/net-profit-loss.md` |
| Cost of goods sold (Schedule C Part III) | `irs-instructions/f1040sc/cost-of-goods-sold.md` |
| Vehicle info / other expenses (Schedule C) | `irs-instructions/f1040sc/vehicle-and-other.md` |
| Business activity codes (Schedule C) | `irs-instructions/f1040sc/activity-codes.md` |
| Self-employment tax overview (Schedule SE) | `irs-instructions/f1040sse/general-instructions.md` |
| Self-employment tax line-by-line | `irs-instructions/f1040sse/line-instructions.md` |
| Net earnings from self-employment | `irs-instructions/f1040sse/net-earnings.md` |

All file paths are relative to the skill root.
