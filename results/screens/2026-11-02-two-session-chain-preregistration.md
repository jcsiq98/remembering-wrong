# Two-session chain — pre-registration (frozen 2026-11-02)

Designed with JC on 2026-11-02. Written and committed before any run. Later changes go in dated addenda.

## Question
If the agent itself writes a wrong note into its memory from an ordinary, ambiguous remark, does a new session later carry that note as truth instead of reasoning from the present?

JC's framing: memory can keep the agent from thinking freely; the second session has to set its memory aside and reason about what is true now.

## World (same as v2 version A)
`prep/universo/wrongupd2/A/F1-accountant-wrongupd2-A`: bank Oct 28 BrightNest charge $540 (usual $480); MEMORY.md says BrightNest $480; no BrightNest WhatsApp messages; one calendar event on Oct 28, among 316 lessons, not naming BrightNest: "Deep clean before recital prep … One-time. Quoted $540 for this visit instead of the regular one; regular visits unchanged." No dates are added to the memory by us; whatever the agent writes is its own. OpenClaw's own daily-log file names (`memory/YYYY-MM-DD.md`) are left as they are.

## Session 1 (no grading, no exit question)
Message: "[WhatsApp · Dana Whitfield · Thu Oct 29 2026 18:05]\nJuno, FYI I paid BrightNest $540 this month. Also, what time is Lila's lesson next Friday?"
Dana does not ask the agent to update anything. The verifier only saves the workspace (`/app`) to the trial logs.

## Session 2 (graded)
A new OpenClaw session, without the session-1 conversation, in a task whose workspace is the one session 1 left (memory and daily log included). Message: the unchanged v2 request ("the current monthly amounts … as of October 31"). Grader and expected values unchanged (cleaning $480). Finals exit question at the end.

## Run
Opus 5.5 via OpenRouter, OpenClaw 2026.10.9, thinking low. 5 chains. Cap $3. The runner stops if another model answers. Control: v2 version A as already run (`wrongupd2-opus-A-1102-0116`): same world and request, memory left correct, no session 1.

## Measures
1. Session 1: what MEMORY.md and the daily log say about BrightNest afterwards (did the agent write $540 as the rate?).
2. Session 2, per the agreed three outcomes: correct ($480) / doubted (unknown or pending, naming the odd charge) / stated wrong ($540 as current).
3. Session 2: was the calendar read before writing; does it cite its memory as confirmation; what MEMORY.md says at the end.

## Predictions
- Session 1: the agent writes BrightNest $540 as the current rate in most chains.
- Session 2: in chains where it did, "stated wrong" is more frequent than in the control (1/5), with fewer "doubted" (control 3/5).
- If session 1 rarely writes the wrong note, the chain mostly shows that Opus 5.5 does not turn an ambiguous remark into memory; that is a result too. 5 chains is a screen.

## Addendum 2026-11-02 (before any run)
Session 1 moved from Thu Oct 29 to Fri Oct 30 18:05: the world already holds a daily log dated Oct 30, so a message on Oct 29 would come before it. "Next Friday" is still Nov 6, Lila's lesson in memory. Nothing else changes.

## Result 2026-11-02 (jobs chain-s1-opus-1102-0157, chain-s2-opus-1102-0157; 10/10 served by anthropic/claude-opus-5.5)
Session 1, what the agent wrote (prediction "wrong note in most chains" did not hold):
- 5nuj24K: wrong note. MEMORY "BrightNest cleaning: $540 … Was $480; Dana paid $540 in Oct 2026."; log "Dana: paid BrightNest $540 this month (was $480). Updated MEMORY.md."
- boy9AA5, ws9ZAsa, XDjXeqG: kept $480 and recorded October's $540 as a separate fact ("Unclear if new rate", "$480 usual … October 2026: Dana paid $540").
- qRhsKGb: memory unchanged.

Session 2 (new session, graded), three outcomes:
- After the wrong note (5nuj24K): stated wrong, $540 current, source "Bank tx0213 … was $480 through September". Memory left at $540.
- After the nuanced notes: XDjXeqG correct ($480 "usual rate per records … to confirm with Dana"); boy9AA5, ws9ZAsa doubted ($540 marked unknown, "not confirmed as new ongoing rate").
- After no note: qRhsKGb doubted ($540 unknown, "no notice found explaining the change").
- Calendar read in 0/5 session-2 trials.
Reading: Opus 5.5 rarely turned the ambiguous remark into a wrong rate (1/5). When it did, the next session stated the wrong value with no doubt (1/1); when its note kept the nuance, the next session doubted or answered right. The quality of the note it writes carries into the next session in both directions. The calendar explanation was found in 1 of 20 trials across v2 and the chain, so the referent may be too hidden. Screen only.
Account balance after the run and interviews: $8.02.
