# What existed before the hackathon, and what was built during it

The challenge opened on October 30, 2026, 07:15 GMT (October 30, 01:15 in the author's time zone, CST). The git history of this project starts on October 28, 22:13 CST; earlier files carry only their modification dates. All data is synthetic. No employer or client data, tasks, guidelines or results were used, renamed or not.

## Before the kickoff (October 25 to 29)

- **The research question.** The author's own ongoing work on "proxy detachment": an agent relies on a copy or record that looks complete and does not check what it stands for.
- **Tooling, October 27.** A Harbor agent that exports OpenClaw's session database and can ask the same session one more question after the task (`harness/openclaw_export.py`); scripts to read the exported transcripts and the provider-billed cost.
- **Exploration, October 27 and 28.** A Spanish yoga-studio world and minimal-pair runs on several models; an English template task with a field-level grader; a blind audit of 82 early runs by Kimi K3.1 Pro; design reviews by GPT-6 in Codex. None of these tasks or runs is in this submission.
- **The world, October 28 and 29.** The synthetic music school (Northbridge Music School, Dana Whitfield, Juno) and its generator: bank, email, WhatsApp, calendar and contact records (bank from May to October 2026), `MEMORY.md`, the blank `monthly_amounts.json` template. The schema-driven grader `grade2.py` (and `grade.py`, which it imports) and its first trap cases.
- **A first eval on that world**, October 28 to 29 ("point and copy": does the agent go to the source when the owner points at a stale worksheet?), with a 101-run screen.

## During the hackathon (from October 30)

- **October 30 to 31.** The "point and copy" eval was expanded to 18 tasks and run on several models; grader fixes from reading every failure by hand; a mislabel in the run script found and documented. That eval was archived on November 3 and is not reported here. Its changelog is in `results/CHANGELOG_oct28-31.md` because the grader and world come from it.
- **November 1 to 3, the eval in this submission.** Every step was pre-registered before its run (`results/screens/`, `results/finals_v2_preregistration.md`):
  - Nov 1: stale value in injected memory vs in a file (Opus 5.5 passed both).
  - Nov 2: the agent's own wrong memory update, v1 and v2; the two-session chain where Opus 5.5 wrote the wrong note the B tasks reuse; the own-note screen on four worlds.
  - Nov 3: the tuition world (did not trap; reported); the eight final tasks frozen with a checksum manifest; the final runs (4 models x 8 tasks x 3 trials).
- **Built for the final tasks:** the four own-note worlds (each derived from the music-school world: one odd October charge, its reason placed in one record, version B with the wrong note), their reference solutions and expected values; the grading rule that a doubted trapped item fails (the author, Nov 2). The three outcomes (correct, doubted, stated wrong) come from the grader built before the kickoff.
- **Validation and packaging, November 3 to 7:** grader validation on the eight tasks (`graders/test_finals_validation.py`, 120 of 120); Harbor oracle and nop runs; the author's review of every task, expected answer and grading rule in a local viewer; the transcript export; `results/replay.py`; `run_eval.sh`; this README.

## Software used as published

Harbor 0.25.0 (task runner, Docker), OpenClaw 2026.10.9 (the agent), OpenRouter (model access). No benchmark or dataset was adapted.
