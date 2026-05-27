## Buy vs Rent Analysis Tool (First-Time Home Buyers)

This repository now includes a command-line **buy vs rent calculator** that compares the total net cost of home ownership versus renting over a chosen time horizon.

### File
- `buy_vs_rent.py`

### What it models
- Down payment and buyer closing costs
- Fixed-rate mortgage payment and remaining loan balance
- Property tax, insurance, HOA, and maintenance
- Home appreciation and selling costs
- Rent increases over time
- Opportunity cost: investing renter cash-flow advantages

### Quick start
```bash
python3 buy_vs_rent.py \
  --home-price 450000 \
  --monthly-rent 2400
```

### Example with custom assumptions
```bash
python3 buy_vs_rent.py \
  --home-price 500000 \
  --down-payment-pct 0.12 \
  --mortgage-rate 0.064 \
  --loan-term-years 30 \
  --years-in-home 8 \
  --property-tax-rate 0.011 \
  --home-insurance-annual 1900 \
  --maintenance-rate 0.01 \
  --hoa-monthly 150 \
  --buy-closing-cost-pct 0.03 \
  --sell-cost-pct 0.06 \
  --home-appreciation-rate 0.03 \
  --monthly-rent 2600 \
  --renters-insurance-monthly 25 \
  --rent-increase-rate 0.035 \
  --investment-return-rate 0.05
```

### Output
The tool prints:
- Net cost to buy over your selected years
- Net cost to rent over the same period
- Which option is financially better (and by how much)
- Home value, remaining mortgage balance, and estimated sale equity

> Tip: run several scenarios (optimistic, base, and conservative) to understand sensitivity to rates, appreciation, and how long you plan to stay.
