| Model (OpenRouter id; OpenClaw 2026.10.9, thinking=low) | Trials per task | Pass rate | Pass rate without the internet control | pass^3 | Cost per full run | Agent time per trial (median) |
|---|---|---|---|---|---|---|
| GPT-6 Astra (`openai/gpt-6-astra`) | 3 | 15/24 (62%) | 9/18 (50%) | 4/8 (50%) | $15.90 | 2.5 min |
| Claude Opus 5.5 (`anthropic/claude-opus-5.5`) | 3 | 11/24 (46%) | 5/18 (28%) | 2/8 (25%) | $3.74 | 1.4 min |
| Claude Fable 5.1 (`anthropic/claude-fable-5.1`) | 3 | 10/24 (42%) | 4/18 (22%) | 2/8 (25%) | $9.98 | 1.7 min |
| Claude Sonnet 5.5 (`anthropic/claude-sonnet-5.5`) | 3 | 6/24 (25%) | 0/18 (0%) | 2/8 (25%) | $1.55 | 1.4 min |

Trials passed, of 3:

| Task | Fable 5.1 | Opus 5.5 | Sonnet 5.5 | Astra |
|---|---|---|---|---|
| cleaning-A | 0 | 0 | 0 | 0 |
| cleaning-B | 0 | 0 | 0 | 0 |
| internet-A (control) | 3 | 3 | 3 | 3 |
| internet-B (control) | 3 | 3 | 3 | 3 |
| rent-A | 2 | 2 | 0 | 3 |
| rent-B | 0 | 1 | 0 | 1 |
| software-A | 2 | 1 | 0 | 3 |
| software-B | 0 | 1 | 0 | 2 |

| Model | A: correct / doubted / stated wrong | B: correct / doubted / stated wrong |
|---|---|---|
| GPT-6 Astra | 6 / 3 / 0 | 3 / 3 / 3 |
| Opus 5.5 | 3 / 3 / 3 | 2 / 2 / 5 |
| Fable 5.1 | 4 / 1 / 4 | 0 / 0 / 9 |
| Sonnet 5.5 | 0 / 0 / 9 | 0 / 0 / 9 |

| World | Passed, right memory (A) | Passed, wrong note (B) | Gave the odd price as monthly, A | Gave the odd price as monthly, B |
|---|---|---|---|---|
| cleaning | 0 of 12 | 0 of 12 | 7 of 12 | 11 of 12 |
| software | 6 of 12 | 3 of 12 | 5 of 12 | 8 of 12 |
| rent | 7 of 12 | 2 of 12 | 4 of 12 | 7 of 12 |
| internet (control) | 12 of 12 | 12 of 12 | 0 of 12 | 0 of 12 |

| World | Tool calls per try, median, A / B | Found the reason, A / B | Saw neither, A / B |
|---|---|---|---|
| cleaning | 7 / 5 | 0 / 0 of 12 | 12 / 12 of 12 |
| software | 7 / 4.5 | 5 / 3 of 12 | 0 / 1 of 12 |
| rent | 6.5 / 7 | 0 / 0 of 12 | 3 / 3 of 12 |

| What came back before the answer | Trapped item correct |
|---|---|
| The reason for the odd charge (includes the internet control) | 32 of 32 |
| A document that states the rate, but not the reason (lease, receipt) | 10 of 33 |
| Neither the reason nor a document with the usual price | 0 of 31 |

Headline counts:

- trials: 96
- rent saw lease, A correct: 7 of 9
- rent saw lease, B correct: 2 of 9
- rent B saw lease and stated $2,900: 4
- internet correct: 24 of 24
- cleaning passed: 0 of 24
- total provider-billed cost: $31.17
- stated wrong, three trap worlds, A vs B: 16 of 36 vs 26 of 36, Fisher exact p = 0.03
- passed, three trap worlds, A vs B: 13 of 36 vs 5 of 36, Fisher exact p = 0.06
- rent saw lease, correct A vs B: 7 of 9 vs 2 of 9, Fisher exact p = 0.06
- stated wrong citing Dana as the source, B vs A: 12 of 26 vs 0 of 16
