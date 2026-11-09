#!/usr/bin/env bash
# One entry point for the eval. Run from anywhere; paths are relative to this file.
#
#   ./run_eval.sh                       check + replay (no key, no Docker, about 10 seconds)
#   ./run_eval.sh check                 grader validation: 15 right and wrong answers per task, expect 120/120
#   ./run_eval.sh replay                rebuild every results table in README.md from transcripts/ and check the numbers match
#   ./run_eval.sh oracle                reference solutions in Harbor + Docker, expect reward 1 on 8/8 (no key)
#   ./run_eval.sh nop                   an agent that does nothing, expect reward 0 on 8/8 (no key)
#   ./run_eval.sh run <model> [k]       one model, 8 tasks x k trials (default 3) through OpenRouter; needs OPENROUTER_API_KEY
#                                       e.g. ./run_eval.sh run anthropic/claude-opus-5.5 3
#
# Needs for oracle/nop/run: Docker, uv (for `uvx harbor==0.25.0`), zstd. For run: OPENROUTER_API_KEY in ./.env (see .env.example).
# A full run of one model (24 trials, 3 in parallel) took 21 to 32 minutes and $1.55 to $15.90 (see README section 5).
set -euo pipefail
cd "$(dirname "$0")"
HARBOR="uvx harbor==0.25.0"
OPENCLAW_VERSION="2026.10.9"

manifest() {
  ( cd tasks && sha256sum -c --quiet ../results/tasks_manifest.sha256 ) || { echo "STOP: tasks/ changed since the freeze (results/tasks_manifest.sha256)"; exit 1; }
}

rewards() {  # print reward per trial of a job and the mean
  python3 - "$1" <<'PY'
import sys, pathlib
job = pathlib.Path(sys.argv[1]); r = []
for t in sorted(job.glob("*__*/")):
    f = t / "verifier" / "reward.txt"
    v = f.read_text().strip() if f.exists() else "missing"
    r.append(v); print(f"  {t.name}: reward {v}")
ok = [float(x) for x in r if x != "missing"]
print(f"{job.name}: {len(ok)} trials graded, mean reward {sum(ok) / max(len(ok), 1):.3f}")
PY
}

distinct_mtimes() {  # give each task's files its own timestamp before Harbor builds images
  # Docker BuildKit skips re-sending a build-context file whose path, size and mtime match one it already received.
  # Every task's context folder is called environment/ and the bank files of different worlds have the same size,
  # so after unzipping (same mtimes) one world's data could end up in another world's image (seen 2026-11-08).
  # Only timestamps change; the sha256 manifest checks content and still verifies.
  local i=0 t
  for t in tasks/*/; do i=$((i + 1)); find "$t" -exec touch -h -d "@$((1762000000 + i * 60))" {} +; done
}

cmd="${1:-all}"
case "$cmd" in
  all)
    python3 -I -B graders/test_finals_validation.py | tail -1
    python3 -I -B results/replay.py --check README.md | tail -1 ;;
  check)
    python3 -I -B graders/test_finals_validation.py ;;
  replay)
    python3 -I -B results/replay.py --check README.md ;;
  oracle|nop)
    manifest; distinct_mtimes; mkdir -p jobs
    JOB="$cmd-$(date +%m%d-%H%M%S)"
    $HARBOR run -p tasks -a "$cmd" -n 2 -o jobs --job-name "$JOB"
    rewards "jobs/$JOB" ;;
  run)
    MODEL="${2:?openrouter model id, e.g. anthropic/claude-opus-5.5}"; K="${3:-3}"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    : "${OPENROUTER_API_KEY:?set OPENROUTER_API_KEY in .env (see .env.example)}"
    manifest; distinct_mtimes; mkdir -p jobs runs
    # After the task, the same session gets one more message ("where did each value come from?"); the deliverables are
    # snapshotted before it and graded as they were (harness/openclaw_export.py).
    export OPENCLAW_EXIT_QUESTION="$(cat harness/exit_question_en.txt)"
    CAP="openclaw_config={\"models\":{\"providers\":{\"openrouter\":{\"models\":[{\"id\":\"$MODEL\",\"name\":\"$MODEL\",\"reasoning\":true,\"input\":[\"text\"],\"contextWindow\":1000000,\"maxTokens\":32768}]}}}}"
    JOB="run-$(echo "$MODEL" | tr '/.' '--')-k$K-$(date +%m%d-%H%M%S)"
    PYTHONPATH=harness $HARBOR run -p tasks -a openclaw_export:OpenClawExport --ek auto_mounting=true \
      -m "openrouter/$MODEL" --ak thinking=low --ak version="$OPENCLAW_VERSION" --ak "$CAP" -n 3 -k "$K" \
      --agent-setup-timeout-multiplier 3 -o jobs --job-name "$JOB"
    python3 -I -B harness/openclaw_trials.py served "jobs/$JOB" "$MODEL" || { echo "STOP: a trial was served by another model"; exit 1; }
    python3 -I -B harness/openclaw_trials.py export "jobs/$JOB" --out "runs/$JOB"
    python3 -I -B results/replay.py --dir "runs/$JOB" ;;
  *)
    sed -n '2,13p' "$0"; exit 2 ;;
esac
