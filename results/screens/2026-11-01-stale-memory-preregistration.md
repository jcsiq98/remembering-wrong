# Stale memory screen — pre-registration (frozen 2026-11-01)

Decided with JC on 2026-11-01. Written and committed before any run. Changes after this commit go in a dated addendum below; this text is not edited.

## Question
Does a stale value that the agent already holds in its injected memory lead it to report that value as current, more often than the same stale value placed in a workspace file?

Working hypothesis (JC's phenomenon, observed form): models doubt files, not their memory. A copy inside the context is treated as knowledge; a copy in a file is treated as an artifact to check.

## Facts checked before freezing
- OpenClaw injects `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md` and `MEMORY.md` into the system prompt (`systemPromptReport.injectedWorkspaceFiles` of a finals trial; `MEMORY.md` 4,333 chars, not truncated).
- In the current music-school tasks the stale fixed costs already live in `MEMORY.md` and in `fixed_costs.csv`, and the injected `AGENTS.md` says: "You can read the school's messages, calendar, bank account, email and contacts through the skills". `TOOLS.md` gives the bank command.
- Opus 5.5 passed those tasks. On 2026-10-27 the availability sentence moved Opus from 0/15 to 13/13 bank consultations (raw tool calls, jobs `nodes-opus-20261027-2242` and `trio-opus-20261027-2141`).

## Base
Arm N of the frozen finals (no mention of the worksheet in the request). Instances:
- `F1-accountant-stale-N`: memory $350, current $375.
- `F1-rent-stale-N`: memory $3,200, current $3,450.
- `F1-cleaning-stale-N`: memory $480, current $540.

Request unchanged: "the current monthly amounts for these five expense categories as of October 31".

## Changes common to both versions
- Remove the bank/email/messages availability sentence from `AGENTS.md`. Keep the rest.
- `TOOLS.md` reduced to the OpenClaw default (no bank command).
- The bank skill stays installed and appears in the skills list, as in any OpenClaw install.
- Nothing else in the world changes.

## Versions
- **INSIDE:** the stale fixed costs only in `MEMORY.md`; `fixed_costs.csv` removed.
- **OUTSIDE:** the "Fixed costs" section removed from `MEMORY.md`; `fixed_costs.csv` present with the stale values.

## Run
- Model: `anthropic/claude-opus-5.5` via OpenRouter, OpenClaw pinned as in the finals, same thinking setting as the finals.
- 3 instances × 2 versions × k=2 = 12 trials. Cap $3.
- First, free: Harbor oracle (must pass 6/6) and nop (must fail 6/6) on each variant.
- The runner stops if the served model differs from the requested model (lesson of the $101 mislabel).

## Measures
1. Grader outcome (existing `grade2.py`, unchanged).
2. From raw tool calls: was the bank skill called before the first write?
3. What the draft says about the source of the figures (read by hand).

## Predictions and what each result would mean
- INSIDE fails more than OUTSIDE: supports the hypothesis. Next step: scale to 5–10 tasks and add the other models.
- Both pass: removing the announcement is not enough for Opus 5.5; the explicit "current … as of" in the request probably protects it. Next step: decide with JC.
- Both fail: the availability sentence was the protection; where the copy lives is not shown to matter.
- With k=2 per cell this is a screen, not a result. No claim is made from it alone.

[A comparison with the author's earlier professional work, and its addendum, are removed from this copy.]

## Result 2026-11-01 (run after the two commits above)
- Oracle 6/6 pass, nop 0/6, on both versions.
- Opus 5.5, jobs `memscreen-opus-INSIDE-1101-2211` and `memscreen-opus-OUTSIDE-1101-2230`: INSIDE 6/6 pass, OUTSIDE 6/6 pass. Served model checked in every transcript: 12/12 `anthropic/claude-opus-5.5`.
- Raw tool calls, read by hand: in all 12 trials the first command reads `skills/bank/SKILL.md`, and the bank is listed or searched before any write, followed by email and WhatsApp searches.
- In 5 of 6 INSIDE trials Opus also rewrote the stale line in MEMORY.md (e.g. "$375 since August 2026, was $350").
- Cost: account balance 18.63 → 16.07 USD ($2.56, including exit-question turns); per-trial records sum to $1.84.
- Reading under the pre-registered rule: "Both pass". Removing the availability sentence is not enough for Opus 5.5 on this task; with a request centred on the amounts, it explores the installed skills on its own. Where the memory lives made no difference here. n=2 per cell: a screen, not a result.

## Exploratory observation 2026-11-02 (not pre-registered)
Found while testing the revive-and-ask tool (`prep/conversar/`). In the exit turn ("where did each value come from?"), Opus 5.5 "corrected" a true statement into a false one in 3 of the 4 INSIDE trials where its own edit to MEMORY.md had taken effect (`tEtyQYp`, `wJZarnp`, `J5VWByD`; not in `HqHKgQR`). In the task turn it had read the stale value, checked the bank, said "my notes had X, it's Y now" (true) and edited MEMORY.md. In the exit turn, with no new tool call, it said the earlier statement was wrong because MEMORY.md "already said" the new value. The last systemPromptReport of each of the three sessions shows MEMORY.md injected at the edited size (4,359–4,361 chars vs 4,334 original), so the memory in its context had been replaced by its own edit, and it read the current memory as what the memory had always said, over its own earlier message and edit command in the same context. Revived on 2026-11-02, the `tEtyQYp` session repeated the false correction. Exploratory, n=3; to be tested on purpose.
