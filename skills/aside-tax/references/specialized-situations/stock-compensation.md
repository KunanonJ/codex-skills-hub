# Stock Compensation

## Types and Tax Treatment

### Incentive Stock Options (ISO)

- **Exercise**: No regular income tax at exercise, but the **bargain element** (FMV minus exercise price) is an AMT adjustment (Form 6251 line 2i). Check AMT exposure — see `references/specialized-situations/amt-screening.md`.
- **Sale of ISO shares**: Report on Form 8949. Holding period determines treatment:
  - **Qualifying disposition** (held > 2 years from grant AND > 1 year from exercise): long-term capital gain. Basis = exercise price.
  - **Disqualifying disposition**: ordinary income = FMV at exercise minus exercise price (reported on W-2). Capital gain/loss on any remaining difference.
- **Key document**: Form 3921 reports the exercise — date of grant, exercise date, exercise price, FMV at exercise, and shares transferred.

### Non-Qualified Stock Options (NSO)

- **Exercise**: Ordinary income = FMV at exercise minus exercise price. Included in W-2 Box 1 (wages) and often in Box 12 Code V. No AMT adjustment.
- **Sale of shares**: Report on Form 8949. Basis = FMV at exercise (the amount already taxed as ordinary income). Holding period starts at exercise date.
- **No special form**: NSO exercises don't generate a Form 3921.

### Restricted Stock Units (RSU)

- **Vesting**: Ordinary income = FMV at vesting. Included in W-2 Box 1. Employer typically withholds shares for taxes.
- **Sale of shares**: Report on Form 8949. Basis = FMV at vesting. Holding period starts at vesting date.
- **1099-B reporting**: Brokers sometimes report $0 cost basis on 1099-B for RSU sales. The actual basis is the FMV at vesting (from W-2 records). Use Box B or E on Form 8949 and enter the corrected basis in column (e) with adjustment code B in column (f).

### Employee Stock Purchase Plan (ESPP)

- **Key document**: Form 3922 reports the purchase.
- **Qualifying disposition** (held > 2 years from offering AND > 1 year from purchase): ordinary income = lesser of (discount at offering or gain at sale). Remainder is capital gain.
- **Disqualifying disposition**: ordinary income = FMV at purchase minus price paid (reported on W-2). Remainder is capital gain/loss.

## Form Flow

- W-2 ordinary income → Form 1040 line 1a
- Capital gain/loss → Form 8949 → Schedule D → Form 1040 line 7
- ISO AMT adjustment → Form 6251 line 2i → Schedule 2 line 2

## Key Instructions

- `irs-instructions/f8949/` — reporting sales on Form 8949
- `irs-instructions/f6251/instructions.md` — AMT (for ISO exercises)
- `irs-instructions/f1040sd/` — Schedule D capital gains
