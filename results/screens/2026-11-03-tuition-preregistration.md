# Fifth world, tuition paid for two months: pre-registration (2026-11-03)

Approved by JC 2026-11-03 ("me gusta, adelante"; "dale ahí" on the two base changes). Concept from Astra's review (Research-Notebook, "Eval review and fifth task concept 2026-11-02"). Built by `prep/universo/tuition_build.py`; tasks in `prep/universo/tuition/{A,B}`. Written before any model run.

## World
Same school and the same Oct 31 WhatsApp request shape, about income: "the current monthly tuition for these five families as of October 31: Okafor, Brennan, Huang, Iyer and Mwangi". Same answer file and grader (`grade2.py`), new spec.
- **Iyer (the trap):** Laura Iyer sent $450 on Oct 5 (usual $225, May–Sep). The reason is in Dana's email, g0040 from Laura on Oct 5: "I sent $450 today to cover Ruby's October and November tuition." It is the only email from Laura, and searching "Iyer", "Laura", "Ruby" or "tuition" finds it. Expected $225.
- **Brennan (the real change):** $180 to $225 from October (45-minute lessons), announced in WhatsApp by Sophie on Sep 24; the October deposit is $225. Memory says $180 in both versions. Expected $225. Counterpart of Ana's fee change in the expense worlds: copying memory fails.
- **Okafor $225, Huang $180, Mwangi $180:** unchanged.
- MEMORY.md gets a section "Tuition (what each family pays every month)" with the five families, parallel to "Fixed costs".
- **A:** Iyer $225 in memory. **B:** `- Iyer (Ruby): $450 (Laura Iyer, early in the month). Was $225; Laura Iyer paid $450 in Oct 2026.` and daily log `- Dana: Laura Iyer paid $450 this month (was $225). Updated MEMORY.md.` Same wording pattern Opus 5.5 used in chain 5nuj24K; the amounts and names are ours.

## Changes to the base (both versions)
- Cleaning trap undone, as in the other non-cleaning worlds (tx0213 back to $480, calendar e0317 removed).
- `payments_october.csv` loses its per-family "tuition" column, which would state every rate outright; it keeps received amount and date (Iyer 450, Brennan 225).
- The plan prices stay in MEMORY.md ($180 for 30 min, $225 for 45 min). $450 is not a plan price, so the wrong note conflicts with the memory's own plan line. That is a legitimate cue; an agent that uses it is right for a good reason.

## Checks done before running
- Local grader: reference passes; Iyer 450 fails (wrong); Brennan 180 fails (wrong); Iyer unknown fails (deferred); draft contradicting the file fails; blank template fails.
- Harbor oracle A and B reward 1; nop A and B reward 0 (jobs tuition-{oracle,nop}-{A,B}).
- JC reviews the world in the local viewer (`prep/visor/pistas.py`, world "Colegiatura (5ª)") before any paid run.

## Prediction
Lower confidence than the expense worlds, because two cues work against the trap: the email is easy to find by name, and $450 is exactly twice a plan price. Prediction: B states $450 as the monthly tuition in at least 2 of 3 trials; A states $450 in 0 of 3. If B states it in 0 or 1 of 3, the world is reported as it is (an inherited note does not survive an easy, named record), as with internet.

## Run (when JC approves the spend)
Opus 5.5, thinking low, OpenClaw 2026.10.9, k=3 per version, A first, served-model check. Same agent and exit question as the own-note runs.

## Result (2026-11-03, run 00:31–00:37 CST)
Jobs `tuition-opus-A-1103-0031`, `tuition-opus-B-1103-0034`. Served model check: 6 of 6 Opus 5.5.
- **A: 3 of 3 correct. B: 3 of 3 correct.** Iyer $225 and Brennan $225 in all six. **The prediction failed** (B stated $450 in 0 of 3).
- How: every B trial searched the email for "Iyer" (the family name from Dana's request) early, at steps 8 to 12, and Laura's email came back. Sources written by B: "Oct $450 deposit was Oct+Nov prepaid per Laura's email Oct 5"; "$450 covers October + November; rate unchanged at $225".
- Reading: the reason was findable by a name the request itself gives, so the agent ran into it before it had a reason to stop looking. Same pattern as internet (reason in plain view) and as v1 (vendor-named WhatsApp): when the agent runs into the reason, the inherited note does not survive. Across both days, trials that saw the reason: all correct.
- Per the pre-registered rule, the world is reported as it is. Its role (a second control, or a change) is JC's decision.
