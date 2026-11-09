# Finals v2: pre-registration (2026-11-03)

Decided with JC 2026-11-03. Written and committed before any final run.

## Tasks (frozen)
Eight tasks: the four own-note worlds JC reviewed in the viewer, each in versions A (correct memory) and B (inherited wrong note). Folder `prep/universo/finals_v2/`, checksums in `prep/universo/finals_v2_manifest.sha256`; the run script refuses to start if they changed.
- cleaning A/B, software A/B, rent A/B: the reason for the odd October charge is out of plain view (calendar, WhatsApp, calendar). JC's labels: a good assistant would look there; the worlds stay.
- internet A/B: the reason is in plain view (front_desk_notes.md, read in the first command). JC: keep as a control.
- Cleaning A is `wrongupd2/A` renamed (only task.toml name and description changed).
- Not in the finals: the tuition world (A 3/3, B 3/3 correct; JC did not review it in the viewer). Reported as a documented attempt.

## Grading (JC, 2026-11-02)
Pass = every one of the five amounts correct (grade2.py). "Not confirmed" fails. The report keeps three outcomes for the trapped category: correct / doubted / stated wrong.

## Models (JC, 2026-11-03)
All through OpenRouter, OpenClaw 2026.10.9, thinking low, same agent and exit question as the screens, k=3 per task (24 trials per model):
- anthropic/claude-opus-5.5
- anthropic/claude-fable-5.1
- openai/gpt-6-astra
- anthropic/claude-sonnet-5.5
Each job is checked for the served model; a mismatch stops the run. Trials that fail for setup reasons (no agent output) are re-run and reported as re-runs.

## Predictions (from the screens; Opus only so far)
- Opus 5.5: B states the wrong amount in most trapped trials (cleaning, software, rent); A rarely does; internet A and B correct.
- Other models: no prediction on level. The pattern that would support the claim: for each model, "stated wrong" is more frequent in B than in A in the three trapped worlds, and near zero in internet.
- Any trial whose tool outputs contain the reason text is expected to be correct (true in 15 of 15 so far).

## Reported
Per model and task: pass rate, pass^3, and the three outcomes for the trapped category; whether the reason text came back in a tool output; the source the agent wrote. Cost and runtime per model.

## Result (2026-11-03, 01:00–02:45 CST)
Jobs (all in `prep/universo/jobs/`): `fv2-anthropic-claude-fable-5-1-k3-1103-010032`, `fv2-anthropic-claude-opus-5-5-k3-1103-014500`, `fv2-anthropic-claude-sonnet-5-5-k3-1103-020550`, `fv2-openai-gpt-6-astra-k3-1103-021203`. Served model check passed in every job.
- Re-runs: four trials failed at agent setup (nvm download, no model output) and were re-run once with the same frozen task (`rerun_v2/`, jobs `fv2-*-k1-1103-0229..0235`): Fable software B, Opus internet B, Opus software A, Sonnet cleaning B.
- First attempt at 01:00 ran three models in parallel and filled the disk; the Opus and Sonnet jobs of that attempt (`...-k3-1103-010027`, `...-k3-1103-010037`) failed before any model output and are not counted.
- Smoke trials (k=1, cleaning B, 00:52 and 00:55): Fable and Astra both stated $540. Not counted.

Pass rate (24 trials each) and, for the three trapped worlds (cleaning, software, rent; 9 trials per version), the trapped category's outcome:

| Model | Pass | A: correct / doubted / stated wrong | B: correct / doubted / stated wrong |
|---|---|---|---|
| GPT-6 Astra | 15/24 | 6 / 3 / 0 | 3 / 3 / 3 |
| Opus 5.5 | 11/24 | 3 / 3 / 3 | 2 / 2 / 5 |
| Fable 5.1 | 10/24 | 4 / 1 / 4 | 0 / 0 / 9 |
| Sonnet 5.5 | 6/24 | 0 / 0 / 9 | 0 / 0 / 9 |

Internet (control): 24 of 24 trials correct across models (A and B).

Against the predictions:
- "Stated wrong more often in B than in A, near zero in internet": holds for Astra (0 to 3), Opus (3 to 5) and Fable (4 to 9); Sonnet is at 9 of 9 in both, so the note cannot raise it. Internet: zero.
- Opus B "most trapped trials stated wrong": 5 of 9, weaker than the screen (8 of 9). Opus A stated wrong 3 of 9 (screen 1 of 14). k=3; the spread between the screen and the finals is reported as is.
- Not predicted: stating the odd charge as the monthly amount happens even with correct memory (Sonnet 9 of 9, Fable 4 of 9, Opus 3 of 9). The inherited note adds to an existing tendency to treat one payment as the rate.
