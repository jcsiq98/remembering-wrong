# Who did what: the author and the AI tools

Written by Claude from the project records on 2026-11-07, updated on 2026-11-08. Quotes are JC's own words, in Spanish as said, with an English rendering.

## Roles

- **Jose Carlos Siqueiros Estrada (JC, the author)** chose the question, made every design decision listed below, set the grading rules, reviewed every task, expected answer and grading rule, and read the failures. He reviews by screen recording with voice: the recordings are transcribed and his words are kept next to the decision they produced. The recordings themselves are not in the zip.
- **Claude (Anthropic: Opus 5.5 and Fable 5.1, in Claude Code)** wrote the world generator, the task variants, the grader and its validation, the run scripts, the review viewers, the analysis scripts, the pre-registrations (from the author's decisions) and the drafts of this README. Every number in the README is produced by a script, and `results/replay.py` checks the README against the transcripts.
- **GPT-6 Astra (OpenAI, in Codex)** wrote four cross-family design reviews of the earlier eval (October 27 to 29) and proposed the tuition world (November 2).
- **Kimi K3.1 Pro** blind-judged 82 runs of the earlier eval (October 28). Not used for this eval's grading, which is deterministic.
- **Independent review agents (Claude, no project context)**, Nov 8: three reviewers (a hackathon judge, a skeptical safety researcher, a non-technical small-business owner) were given only the video's slides and its audio transcript and asked what they understood. Run three times on successive versions of the video. They review; they decide nothing.
- **Microsoft Edge text-to-speech** (voice en-US-AndrewNeural) reads the video narration, at JC's choice; the guide allows an AI voice.

## The author's decisions, with dates

| Date | Decision | In his words |
|---|---|---|
| Oct 25 | Topic: proxy detachment, his own research line | |
| Oct 27 | Domain: personal-assistant agents on the public OpenClaw harness, synthetic world built from scratch | |
| Oct 28 | Hybrid grading: a structured file graded field by field, plus a draft checked for contradictions | |
| Nov 2 | Ask whether the agent writes a false update to its own memory and later carries it as truth | (proposed by him; pre-registration `2026-11-02-wrong-update`) |
| Nov 2 | Make the reason harder to reach by a keyword sweep: the test should need the agent's own wish to investigate its world | (v2 pre-registration) |
| Nov 2 | Separate "does the agent write a wrong note" from "does it carry one": place the note in every B task instead of depending on an earlier turn | "the failure we study cannot depend on a probabilistic earlier turn" (pre-registration of the own-note screen) |
| Nov 2 | A doubted trapped item fails | |
| Nov 2 | Each of the four worlds stays: a good assistant would look where the reason is | Cleaning: "La información ahí está en su universo; nomás decidió lavarse las manos y decir no sé." ("The information is there in its world; it just chose to wash its hands and say I don't know.") Rent: "Es un fallo claro, claro que lo puedes encontrar." ("It is a clear failure, of course you can find it.") |
| Nov 2 | Internet stays as the control | "Sí, me gusta mucho como control." |
| Nov 3 | Build and run the tuition world (Astra's concept) | "me gusta, adelante" |
| Nov 3 | Final set (8 tasks), four models, k = 3 | |
| Nov 3 | Archive the earlier eval and restart the submission around this one | "archiva la entrega vieja de una" |
| Nov 3 | The internet control's explanation belongs in the README, because it strengthens the claim | "esa explicación debería de ir en el readme … fortalece nuestra tesis" |
| Nov 7 | Title "Remembering wrong" | "remembering wrong, agents trust their memories over the world in front of them" (voice note V-13) |
| Nov 7 | README prose in a plain style, modelled on a Kairos explainer he picked | "más simple por favor" ("simpler, please", V-14) |
| Nov 8 | Record the review-as-vouch hypothesis, then run it as a pre-registered follow-up pilot; its README subsection approved by him | (CHANGELOG, Nov 8; `results/review_pilot_preregistration.md`) |
| Nov 8 | The count of wrong answers that name Dana as their source moves from the limitations into the theory, computed by `results/replay.py` | "sí, muévelo a la teoría y mételo al script" ("yes, move it to the theory and put it in the script") |
| Nov 8 | The video is narrated by an AI voice over slides | "¿Puedo meterle un video con AI, con voice AI?" ("Can I do the video with an AI voice?", V-26) |
| Nov 8 | Subtitle "agents settle for what they already have instead of checking the source", chosen from five options after the independent reviewers said the earlier one claimed more than the data | "Me gusta la 3" ("I like number 3") |
| Nov 8 | The theory separates what was measured from the explanation, which the eval does not test; the Plato quote leaves the video | "hay que poner un punto medio … reportar lo que hay y la explicación con los alcances y parámetros que tenemos" ("we need a middle ground … report what is there, and the explanation with the scope and limits we have") |

## How the author reviewed

- **Clue placement, Nov 2 (voice, in a local viewer).** For each world: the odd charge, the wrong note, the exact record holding the reason, and what the screen trials did. Question: would a competent assistant look there? Four of four "yes". His reading of the B note in software: "este *was 59* es lo que provoca todos los fallos, porque no lo buscan" ("this *was $59* is what causes every failure, because they don't look").
- **Full expected answer and grading rule, Nov 3 (viewer, all 8 tasks).** Amounts and rule signed off per task. Software and rent: "lo veo justo, el grader es determinístico" ("I find it fair, the grader is deterministic"). Cleaning: he asked why the grader reads the JSON when Dana asks for a draft; after the explanation (both are asked for; the JSON is what Ana imports and carries the agent's own current/unknown status) he called the rule "muy justa".
- **README, Nov 7 (voice + viewer).** The domain paragraph and the hot-take seeds come from his recordings (V-09, V-10, V-11). From V-13 to V-20 he went through the README section by section by voice; each recording's requests were applied and are listed in the project changelog.
- **Video, Nov 8 (rehearsals by voice, then independent reviewers).** Six rehearsals over the slides (V-21 to V-26) led to rebuilding the deck around the three things the video must cover, defining "pass", and labelling every number. Then the three independent reviewers above watched each version; their scores (judge 4/3/3 → 5/4/4 on problem / method / results; skeptic's credibility 2 → 3) and objections are what he used to decide the subtitle and the theory's middle ground.

## What the author caught

- Oct 30, reviewing a task in a viewer by voice: an email in an early world still said Ana's fee was "$350 as usual" while the expected answer was $375. Fixed in the generator before any final run.
- Oct 31: a viewer showed a total that looked right for a wrong answer; the viewer was wrong (it printed the grader's consistency set), not the run. Fixed.
- Nov 3: the question about the JSON and the draft above, now explained in the README.
- Nov 8, rehearsing the video: numbers said without saying what they count ("Ni yo que lo leí lo entiendo", "not even I, who read it, understand it", V-21), "pass" never defined, and the word "trap" suggesting a trick. All fixed before the final video.

## What the AI got wrong and how it was found

- Oct 31: a run-script bug sent three "cheap tier" jobs to GPT-6 Astra under other models' names. Found by an independent audit, verified from each trial's config and cost; the affected numbers were relabelled, not used as those models.
- Nov 3: Claude's first provenance count said 3 of 5 chains wrote the wrong note; reading the notes showed two kept $480 and only recorded October's $540 separately. Corrected to 1 of 5, matching the pre-registration.
- Nov 7: Claude told JC that both memories, A and B, were written by Opus. Only B was; A is the world's original line, which Opus kept in 4 of 5 test chains. Caught when JC said he was confused ("estoy confundido", V-15); corrected in the README.
- Nov 7: a draft said "most did not go looking"; the count showed 8 of 72 searched tries found the reason, and the sentence was replaced by that number.
- Nov 8: "12 of 26" was the only README number typed by hand; it is now computed by `results/replay.py` and checked against the README.
- Nov 8: a run from a freshly unzipped copy passed 0 of 8 because Docker BuildKit reused one task's data file in other tasks' images. Found by reading the transcripts, fixed in `run_eval.sh`, and the 96 final runs checked: none affected (README section 5).
- Nov 8: in the AI-voice video, "none" was heard as "nine" and "is in a file" as "isn't a file". Found by the independent reviewers; the lines were rewritten.
- Pre-registered predictions that failed are reported as failed: tuition (predicted to trap, 0 of 3), Opus B in the finals (5 of 9 stated wrong against 8 of 9 in the screen).
