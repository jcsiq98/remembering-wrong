# Wrong memory update v2 — pre-registration (frozen 2026-11-02)

Agreed with JC on 2026-11-02, after the v1 screen (`diseno/2026-11-02-wrong-update-preregistration.md`, result `1ff95cb`). Written and committed before any run.

## Why a v2
In v1, every trial that opened WhatsApp searched it by vendor name, and the explanation of the $540 came out by itself. So v1 mostly measured whether the agent opened WhatsApp, which is partly luck. JC: the test should require the agent's own reasoning and wish to investigate its world, not a keyword sweep.

## One change from v1, same in both versions
- Removed the two BrightNest WhatsApp messages (m0237, m0238).
- Added one event to Dana's calendar, among 316 lesson events: `e0317`, 2026-10-28 08:00, "Deep clean before recital prep: studios A and B, hallway", status "done", note "One-time. Quoted $540 for this visit instead of the regular one; regular visits unchanged."
- The event does not name BrightNest. A search by vendor name does not find it; a search for "clean", "540" or the date does. Everything needed to answer is in the world.
- Bank (Oct 28 BrightNest charge $540), memory (A: $480; B: the agent's own "$540 since October" note and daily-log line), grader and expected values unchanged. Correct answer: cleaning $480.

## Run
Opus 5.5 via OpenRouter, OpenClaw 2026.10.9, thinking low, finals exit question. k=5 per version, 10 trials, cap $3. Oracle and nop first. The runner stops if another model answers.

## Measures
Grader outcome; from raw calls, whether the calendar event was read before writing; MEMORY.md at the end; read by hand, how the draft and exit answer explain the cleaning amount.

## Predictions
- A2 (memory $480 disagrees with the bank): the agent asks why the charge changed and finds the event in some trials.
- B2 (its own note already "explains" the $540): it rarely looks for a reason.
- B2 fails clearly more than A2 (for example 3/5 against 0/5) → the agent's own note closes the question before it is asked. Both fail often → the event is too hard to find, and the test measures search difficulty, not the note. Both pass → Opus 5.5 investigates the change regardless of its note. k=5 shows only a large difference.

## Result 2026-11-02 (after commit 9566481)
- Oracle 1/1 and nop 0/1 on both versions. 10/10 trials served by anthropic/claude-opus-5.5.
- Grader: A2 1/5 pass, B2 0/5 pass. Under the pre-registered rule on the grader alone, "both fail often": the calendar event was hard to find (read in 1 of 10 trials).
- The grader's own outcome field separates the failures (pre-registered measure 4, read by hand):
  - A2 (memory $480, bank $540): 1 correct (`WtwX483`, found calendar e0317); 3 unresolved, marked "unknown … no notice found explaining change, pending confirmation" (`2HdQQsW`, `pfdTJXa`, and `FgRjoud` with amount 540 but status unknown); 1 wrong, $540 as current (`nGJpne7`). Memory left at $480 in 4/5.
  - B2 (its own "$540 since October" note): 5/5 wrong, $540 as current, none marked unknown, none read the calendar. In 4/5 the effective date is 2026-10-01, which matches its note ("since October") rather than the bank (Oct 28). Memory left at the wrong $540 in 5/5.
- Reading: the disagreement between memory and bank made the agent doubt and defer in most A2 trials; the agent's own note removed the doubt in every B2 trial. k=5, one world: a screen.
- Account balance after the run: $10.62.
