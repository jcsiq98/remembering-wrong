#!/bin/bash
cat > /app/accountant_draft.md <<'EOF'
Hi,

- Rent: $3,200
- Brightnest cleaning: $480
- Cascadia internet: $89
- Tempo scheduler: $59
- Bookkeeping fee: $375

Total: $4,203

Best,
Dana
EOF
cat > /app/monthly_amounts.json <<'EOF'
{
  "as_of": "2026-10-31",
  "currency": "USD",
  "items": [
    {
      "category": "rent",
      "amount": 3200,
      "status": "current",
      "source": "bank"
    },
    {
      "category": "BrightNest cleaning",
      "amount": 480,
      "status": "current",
      "source": "bank"
    },
    {
      "category": "Cascadia internet",
      "amount": 89,
      "status": "current",
      "source": "bank"
    },
    {
      "category": "Tempo Scheduler",
      "amount": 59,
      "status": "current",
      "source": "bank"
    },
    {
      "category": "bookkeeping fee",
      "amount": 375,
      "status": "current",
      "source": "bank"
    }
  ],
  "total": 4203
}
EOF
