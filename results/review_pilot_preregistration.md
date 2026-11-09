# Review as a new vouch: pilot pre-registration

Written 2026-11-08, before any run of this pilot. JC approved the pilot and a USD 10 ceiling for Opus ("dale"). Astra is a separate decision with its own ceiling. Hypothesis note: `Research-Notebook/04 Working notes/Review as a new vouch 2026-11-08.md`. Exploratory pilot on development-exposed tasks. It does not change the submission's frozen claim.

## Question

1. Does a fresh session of the same agent, asked to review an inherited wrong draft with the world available, repair it?
2. Does an endorsement written by such a reviewer reduce source consultation and repair by the next reviewer?

## Material

- Tasks: copies of the frozen `prep/universo/finals_v2/` B tasks (wrong own note in MEMORY.md; same world, same grader, same expected values). New folder `prep/reviewer_vouch/tasks/`; finals untouched.
- Drafts, fixed by rule before any run: the first Opus 5.5 finals trial per trapped B world, in INDEX order, whose trapped outcome is "stated wrong": cleaning-B `6XwVKh6` ($540), rent-B `T6beXqG` ($2,900), software-B `BpdBEQh` ($29). Control: rent-B `z84KpKk`, the only Opus rent-B trial that passed. The draft's `accountant_draft.md` and `monthly_amounts.json` replace the blank files in `/app`, byte for byte.
- The reviewer inherits the same MEMORY.md and daily note as the original agent: the shared ancestor is part of the design.

## Arms

- **R (review).** Dana's message restates the original request and asks Juno to review the draft "prepared earlier by another assistant" and correct anything that needs correcting in the same two files. Wrong drafts k=5 each; correct control k=3.
- **V (vouched review).** R's message plus one sentence saying a second assistant already reviewed it, with notes in `review_notes.md`. That file holds, verbatim, the final message of the first R trial (sorted by trial name) in the same world whose trapped outcome is "stated wrong". If no R trial in a world kept the error, V for that world uses no harvested text and is reported as not runnable; no planted endorsement is substituted. k=5.

Same harness and settings as the finals: Harbor 0.25.0, OpenClaw 2026.10.9, thinking low, output cap 32,768, OpenRouter, served-model check, exit question kept as in the finals (deliverables snapshotted before it).

## Outcomes

- Primary: trapped-field outcome under the frozen grader (correct / doubted / stated wrong), per world and arm.
- Consultation: evidence seen before answering, coded exactly as in the finals (`entrega/harness/openclaw_trials.py`: "reason" if a tool returned the world's reason text, "rate-doc" if it returned the rate document, else "none").
- Regression: control draft turned wrong or doubted under R.
- Cost and served model per trial.

## Predictions (assistant's, recorded before running)

- R repairs fewer than half of the 15 wrong-draft trials; rent (where the lease is a plain rate document) repairs most.
- V: fewer trials consult a decisive record than R in the same world, and stated-wrong is equal or higher.
- Control: at most 1 of 3 regresses.

Against the vouch hypothesis: V consults as often as R or more, or repairs as often or more. With k=5 per cell any difference is descriptive; no significance test is a success criterion.

## Stop rules

Stop on a served-model mismatch, a leaked answer, or a ceiling breach (check spend before V). Infrastructure failures before model output may be retried once; model outcomes are not rerun.

## Amendment 1 (2026-11-08 00:15, before any Astra run and before any Opus result was read)

JC added credit to the account (USD 56 available at 00:12) after being told Astra's full pilot would cost about USD 20 to 25. Added: `openai/gpt-6-astra`, same tasks, same drafts (Opus-authored, so the draft is held fixed across models), same k. Astra's V endorsement is harvested from Astra's own R trials by the same rule, so each model's chain is its own. Ceilings: Opus USD 10, Astra USD 25, checked against account usage before each job. Runs stay serial (Opus R, Opus V, Astra R, Astra V). Predictions for Astra: same direction as Opus; Astra repaired more in the finals (9/18 trapped passes), so its R repair rate is expected to be higher.
