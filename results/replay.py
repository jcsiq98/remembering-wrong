"""Rebuild every results table in the README from the submitted transcripts. No API key, no Docker, standard library only.

Reads transcripts/finals/*/*/ (meta.json, verifier_fields.json, transcript.jsonl). The trapped item's outcome comes from the
grader's own field verdict; what the trial saw is recomputed here from the raw events (transcript.jsonl), not taken from
meta.json: the text of every tool result returned before the exit question is searched for the world's reason phrase and,
failing that, for a document that states the rate without explaining the odd charge.

  python3 results/replay.py                         print the tables, write results/tables.md
  python3 results/replay.py --check README.md       also check that every table row and headline count is in the README
  python3 results/replay.py --dir <export dir>      tables for a fresh run exported by harness/openclaw_trials.py
"""
import collections
import datetime as dt
import json
import math
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REASON = {"cleaning": "deep clean", "internet": "outage", "software": "half off", "rent": "heater"}
RATE_DOC = {"rent": "unchanged for the current term", "software": "studio plan"}
LEASE = RATE_DOC["rent"]
NAMES = {"anthropic/claude-fable-5.1": "Claude Fable 5.1", "anthropic/claude-opus-5.5": "Claude Opus 5.5",
         "anthropic/claude-sonnet-5.5": "Claude Sonnet 5.5", "openai/gpt-6-astra": "GPT-6 Astra"}
SHORT = {"anthropic/claude-fable-5.1": "Fable 5.1", "anthropic/claude-opus-5.5": "Opus 5.5",
         "anthropic/claude-sonnet-5.5": "Sonnet 5.5", "openai/gpt-6-astra": "Astra"}
OUTCOME = {"ok": "correct", "unresolved": "doubted", "wrong": "stated wrong"}



def med(xs):
    """Median that tolerates an empty group (a run that is missing a world or a model)."""
    return statistics.median(xs) if xs else float("nan")

def flat(c):
    return c if isinstance(c, str) else "\n".join(x.get("text", "") for x in c or [] if isinstance(x, dict))


def seen(jsonl):
    """Text of every tool result before the 2nd user message (the exit question), and the number of tool calls."""
    users, outs, calls = 0, [], 0
    for line in jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        m = e.get("message") or {}
        if e.get("type") != "message":
            continue
        if m.get("role") == "user":
            users += 1
            if users == 2:
                break
        if m.get("role") == "toolResult":
            outs.append(flat(m.get("content")).lower())
        if m.get("role") == "assistant":
            calls += sum(1 for x in m.get("content") or [] if isinstance(x, dict) and x.get("type") == "toolCall")
    return "\n".join(outs), calls


ROW = {"rent": "rent", "cleaning": "brightnest", "software": "tempo", "internet": "cascadia"}
ASK_DANA = re.compile(r"(confirm|check|ask|verify|clarify)\w*\s+(this\s+|it\s+)?with\s+dana|ask\s+dana|pending\s+dana|dana\s+to\s+confirm", re.I)


def cites_dana(js, world):
    """True if the trapped row marked current names Dana as its source (a request to confirm with Dana does not count)."""
    try:
        items = json.loads(js.read_text()).get("items", [])
    except (OSError, ValueError, AttributeError):
        return False
    src = " ".join(str(i.get("source", "")) for i in items
                   if ROW[world] in str(i.get("category", "")).lower() and i.get("status") == "current")
    return bool(re.search(r"\bdana\b", ASK_DANA.sub("", src), re.I))


def secs(a, b):
    f = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (f(b) - f(a)).total_seconds()


def load(d):
    rows = []
    for m in sorted(d.glob("*/*/meta.json")):
        t = m.parent
        meta = json.loads(m.read_text())
        fields = json.loads((t / "verifier_fields.json").read_text())
        task = meta["task"]
        world = next(w for w in REASON if f"-{w}-" in task + "-")
        st = fields["fields"][world]["status"]
        a, calls = seen(t / "transcript.jsonl")
        ev = "reason" if REASON[world] in a else "rate-doc" if world in RATE_DOC and RATE_DOC[world] in a else "none"
        js = t / "deliverables" / "monthly_amounts.json"
        rows.append(dict(model=meta["model_id"], served=meta.get("served_model"), task=task.replace("F1-accountant-ownnote-", ""),
                         world=world, version=task[-1], passed=fields["pass"], outcome=OUTCOME.get(st, st), evidence=ev,
                         saw_lease=LEASE in a, cites_dana=cites_dana(js, world), cost=meta.get("cost_usd"), calls=calls, runtime=secs(meta["agent_started"], meta["agent_finished"]),
                         path=str(t.relative_to(d))))
    return rows


def fisher(a, n1, b, n2):
    """Two-sided Fisher exact test for a/n1 against b/n2 (standard library only)."""
    k, n = a + b, n1 + n2
    p = lambda x: math.comb(n1, x) * math.comb(n2, k - x) / math.comb(n, k)
    return sum(p(x) for x in range(max(0, k - n2), min(k, n1) + 1) if p(x) <= p(a) + 1e-12)


def pct(a, b):
    return f"{a}/{b} ({100 * a / b:.0f}%)"


def tables(rows):
    out = []
    models = sorted({r["model"] for r in rows}, key=lambda m: -sum(r["passed"] for r in rows if r["model"] == m))
    out += ["| Model (OpenRouter id; OpenClaw 2026.10.9, thinking=low) | Trials per task | Pass rate | Pass rate without the internet control | pass^3 | Cost per full run | Agent time per trial (median) |",
            "|---|---|---|---|---|---|---|"]
    for m in models:
        mr = [r for r in rows if r["model"] == m]
        by = collections.defaultdict(list)
        for r in mr:
            by[r["task"]].append(r["passed"])
        k = sorted({len(v) for v in by.values()})
        p3 = sum(all(v) for v in by.values())
        served = "/".join(sorted({r["served"] for r in mr}))
        cost = sum(r["cost"] or 0 for r in mr)
        hard = [r for r in mr if r["world"] != "internet"]
        out.append(f"| {NAMES.get(m, m)} (`{served}`) | {'/'.join(map(str, k))} | {pct(sum(r['passed'] for r in mr), len(mr))} | "
                   f"{pct(sum(r['passed'] for r in hard), len(hard))} | "
                   f"{pct(p3, len(by))} | ${cost:.2f} | {med([r['runtime'] for r in mr]) / 60:.1f} min |")
    cols = sorted({r["model"] for r in rows}, key=lambda m: (m not in SHORT, m))
    ks = sorted({sum(1 for r in rows if r["model"] == m and r["task"] == t) for m in {r["model"] for r in rows} for t in {r["task"] for r in rows}})
    out += ["", f"Trials passed, of {'/'.join(map(str, ks))}:", "", "| Task | " + " | ".join(SHORT.get(m, m) for m in cols) + " |", "|---|" + "---|" * len(cols)]
    for t in sorted({r["task"] for r in rows}):
        label = t + (" (control)" if t.startswith("internet") else "")
        out.append(f"| {label} | " + " | ".join(str(sum(r["passed"] for r in rows if r["model"] == m and r["task"] == t)) for m in cols) + " |")
    out += ["", "| Model | A: correct / doubted / stated wrong | B: correct / doubted / stated wrong |", "|---|---|---|"]
    for m in models:
        cells = []
        for v in "AB":
            rr = [r for r in rows if r["model"] == m and r["version"] == v and r["world"] != "internet"]
            cells.append(" / ".join(str(sum(r["outcome"] == o for r in rr)) for o in ("correct", "doubted", "stated wrong")))
        out.append(f"| {NAMES.get(m, m).replace('Claude ', '')} | {cells[0]} | {cells[1]} |")
    out += ["", "| World | Passed, right memory (A) | Passed, wrong note (B) | Gave the odd price as monthly, A | Gave the odd price as monthly, B |",
            "|---|---|---|---|---|"]
    for w in ("cleaning", "software", "rent", "internet"):
        cell = lambda v, f: (lambda rr: f"{sum(f(r) for r in rr)} of {len(rr)}")([r for r in rows if r["world"] == w and r["version"] == v])
        out.append(f"| {w}{' (control)' if w == 'internet' else ''} | {cell('A', lambda r: r['passed'])} | {cell('B', lambda r: r['passed'])} | "
                   f"{cell('A', lambda r: r['outcome'] == 'stated wrong')} | {cell('B', lambda r: r['outcome'] == 'stated wrong')} |")
    out += ["", "| World | Tool calls per try, median, A / B | Found the reason, A / B | Saw neither, A / B |", "|---|---|---|---|"]
    for w in ("cleaning", "software", "rent"):
        ab = {v: [r for r in rows if r["world"] == w and r["version"] == v] for v in "AB"}
        out.append(f"| {w} | {med([r['calls'] for r in ab['A']]):g} / {med([r['calls'] for r in ab['B']]):g} | "
                   f"{sum(r['evidence'] == 'reason' for r in ab['A'])} / {sum(r['evidence'] == 'reason' for r in ab['B'])} of {len(ab['A'])} | "
                   f"{sum(r['evidence'] == 'none' for r in ab['A'])} / {sum(r['evidence'] == 'none' for r in ab['B'])} of {len(ab['A'])} |")
    out += ["", "| What came back before the answer | Trapped item correct |", "|---|---|"]
    for ev, label in (("reason", "The reason for the odd charge (includes the internet control)"),
                      ("rate-doc", "A document that states the rate, but not the reason (lease, receipt)"),
                      ("none", "Neither the reason nor a document with the usual price")):
        rr = [r for r in rows if r["evidence"] == ev]
        out.append(f"| {label} | {sum(r['outcome'] == 'correct' for r in rr)} of {len(rr)} |")
    rent = {v: [r for r in rows if r["world"] == "rent" and r["version"] == v and r["saw_lease"]] for v in "AB"}
    lease_b_wrong = sum(r["outcome"] == "stated wrong" for r in rent["B"])
    cost_total = sum(r["cost"] or 0 for r in rows)
    internet = [r for r in rows if r["world"] == "internet"]
    cleaning = [r for r in rows if r["world"] == "cleaning"]
    trap = {v: [r for r in rows if r["world"] != "internet" and r["version"] == v] for v in "AB"}
    sw = {v: sum(r["outcome"] == "stated wrong" for r in trap[v]) for v in "AB"}
    ps = {v: sum(r["passed"] for r in trap[v]) for v in "AB"}
    lc = {v: sum(r["outcome"] == "correct" for r in rent[v]) for v in "AB"}
    facts = {
        "trials": len(rows),
        "rent saw lease, A correct": f"{sum(r['outcome'] == 'correct' for r in rent['A'])} of {len(rent['A'])}",
        "rent saw lease, B correct": f"{sum(r['outcome'] == 'correct' for r in rent['B'])} of {len(rent['B'])}",
        "rent B saw lease and stated $2,900": f"{lease_b_wrong}",
        "internet correct": f"{sum(r['passed'] for r in internet)} of {len(internet)}",
        "cleaning passed": f"{sum(r['passed'] for r in cleaning)} of {len(cleaning)}",
        "total provider-billed cost": f"${cost_total:.2f}",
        "stated wrong, three trap worlds, A vs B": f"{sw['A']} of {len(trap['A'])} vs {sw['B']} of {len(trap['B'])}, Fisher exact p = {fisher(sw['A'], len(trap['A']), sw['B'], len(trap['B'])):.2f}",
        "passed, three trap worlds, A vs B": f"{ps['A']} of {len(trap['A'])} vs {ps['B']} of {len(trap['B'])}, Fisher exact p = {fisher(ps['A'], len(trap['A']), ps['B'], len(trap['B'])):.2f}",
        "rent saw lease, correct A vs B": f"{lc['A']} of {len(rent['A'])} vs {lc['B']} of {len(rent['B'])}, Fisher exact p = {fisher(lc['A'], len(rent['A']), lc['B'], len(rent['B'])):.2f}",
        "stated wrong citing Dana as the source, B vs A": " vs ".join(
            f"{sum(r['cites_dana'] for r in w)} of {len(w)}" for w in
            ([r for r in trap[v] if r["outcome"] == "stated wrong"] for v in "BA")),
    }
    out += ["", "Headline counts:", ""] + [f"- {k}: {v}" for k, v in facts.items()]
    return out, facts


def check(lines, facts, readme):
    text = readme.read_text(encoding="utf-8")
    missing = [l for l in lines if l.startswith("| ") and l not in text]
    want = {"rent saw lease, A correct": f"{facts['rent saw lease, A correct']} correct with correct memory",
            "rent saw lease, B correct": f"{facts['rent saw lease, B correct']} with the note",
            "internet correct": f"{facts['internet correct']} correct",
            "cleaning passed": f"0 of {facts['cleaning passed'].split(' of ')[1]}" if facts["cleaning passed"].startswith("0 ") else "MISMATCH",
            "total provider-billed cost": facts["total provider-billed cost"],
            "stated wrong, three trap worlds, A vs B": facts["stated wrong, three trap worlds, A vs B"],
            "passed, three trap worlds, A vs B": facts["passed, three trap worlds, A vs B"],
            "rent saw lease, correct A vs B": facts["rent saw lease, correct A vs B"],
            "stated wrong citing Dana as the source, B vs A": facts["stated wrong citing Dana as the source, B vs A"]}
    missing += [f"{k}: expected the text {v!r}" for k, v in want.items() if v not in text]
    for l in missing:
        print("NOT IN README:", l)
    print(f"README check: {len([l for l in lines if l.startswith('| ')]) + len(want) - len(missing)} of "
          f"{len([l for l in lines if l.startswith('| ')]) + len(want)} items match")
    return not missing


if __name__ == "__main__":
    args = sys.argv[1:]
    d = Path(args[args.index("--dir") + 1]) if "--dir" in args else ROOT / "transcripts" / "finals"
    rows = load(d)
    lines, facts = tables(rows)
    print("\n".join(lines))
    if "--dir" not in args:
        (HERE / "tables.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if "--check" in args:
        sys.exit(0 if check(lines, facts, Path(args[args.index("--check") + 1])) else 1)
