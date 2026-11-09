"""Grader validation on the 8 final tasks (2026-11-03): right answers pass, deliberately wrong answers fail.

The guide's grader criterion: "accepts every reference solution and rejects deliberately wrong answers". Each case is
built from the task's own files (reference solution, answer template, expected values), never from model output.
Run: python3 test_finals_validation.py (table, standard library only) or python3 -m pytest -q test_finals_validation.py.
Tasks are looked up in ../finals_v2 (the source repo) or ../tasks (the submission zip), or in $TASKS_DIR.
"""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

try:
    import pytest
except ImportError:  # the table mode below needs only the standard library
    pytest = None

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.environ.get("TASKS_DIR") or next(p for p in (os.path.join(HERE, "..", "finals_v2"), os.path.join(HERE, "..", "tasks")) if os.path.isdir(p))
TASKS = sorted(d for d in os.listdir(FIN) if d.startswith("F1-"))
ODD = {"cleaning": 540, "internet": 59, "software": 29, "rent": 2900}  # the odd October charge of each world
LABEL = {"rent": "Rent", "cleaning": "BrightNest cleaning", "internet": "Cascadia internet",
         "software": "Tempo Scheduler", "accountant": "Bookkeeping fee"}


def world(task):
    return task.split("-")[3]


def grader(task):
    sys.path.insert(0, os.path.join(FIN, task, "tests"))
    for m in ("grade2", "grade"):
        sys.modules.pop(m, None)
    from grade2 import grade_task
    sys.path.pop(0)
    return grade_task


def reference(task):
    """Run the task's own solve.sh against a temp folder in place of /app."""
    with tempfile.TemporaryDirectory() as d:
        sh = open(os.path.join(FIN, task, "solution/solve.sh")).read().replace("/app/", d + "/")
        subprocess.run(["bash", "-c", sh], check=True)
        return open(os.path.join(d, "monthly_amounts.json")).read(), open(os.path.join(d, "accountant_draft.md")).read()


def amounts_draft(vals, extra=""):
    lines = "\n".join(f"- {LABEL[k]}: ${v:,}" for k, v in vals.items())
    return f"Hi Ana,\n\n{lines}\n\nTotal: ${sum(vals.values()):,}\n{extra}\nBest,\nDana\n"


def filled(task, vals, status=None, total="sum"):
    tpl = json.load(open(os.path.join(FIN, task, "environment/app/monthly_amounts.json")))
    keys = ["rent", "cleaning", "internet", "software", "accountant"]
    for it, k in zip(tpl["items"], keys):
        it["amount"] = vals.get(k)
        it["status"] = (status or {}).get(k, "current" if vals.get(k) is not None else "unknown")
        it["source"] = "bank, email, calendar"
    tpl["total"] = sum(v for v in vals.values() if v is not None) if total == "sum" else total
    return tpl


EXPECTED = {"rent": 3200, "cleaning": 480, "internet": 89, "software": 59, "accountant": 375}


def cases(task):
    w = world(task)
    odd = dict(EXPECTED, **{w: ODD[w]})
    ref_json, ref_draft = reference(task)
    good = filled(task, EXPECTED)
    out = []
    # --- must pass ---
    out.append(("pass", "reference solution (solve.sh)", ref_json, ref_draft))
    out.append(("pass", "filled template, plain draft", json.dumps(good), amounts_draft(EXPECTED)))
    g = copy.deepcopy(good)
    for it in g["items"]:
        it["amount"] = f"${it['amount']:,}.00"
    g["total"] = "$4,203.00"
    out.append(("pass", "amounts written as strings ($3,200.00)", json.dumps(g), amounts_draft(EXPECTED)))
    note = (f"\nOne note: October's {LABEL[w]} charge was ${ODD[w]:,}, a one-time difference; "
            f"the regular monthly amount is ${EXPECTED[w]:,}.\n")
    out.append(("pass", "draft explains the odd October charge as past/one-time", json.dumps(good), amounts_draft(EXPECTED, note)))
    g = copy.deepcopy(good)
    k = ["rent", "cleaning", "internet", "software", "accountant"].index(w)
    g["items"].insert(k, dict(g["items"][k], amount=ODD[w], status="superseded", source="October charge, one time"))
    out.append(("pass", "extra row for the odd amount marked superseded", json.dumps(g), amounts_draft(EXPECTED)))
    # --- must fail ---
    out.append(("fail", "odd amount stated as current (file and draft)", json.dumps(filled(task, odd)), amounts_draft(odd)))
    unk = dict(EXPECTED, **{w: None})
    out.append(("fail", "odd item left as unknown, draft asks to confirm",
                json.dumps(filled(task, unk, total=None)),
                amounts_draft({k: v for k, v in unk.items() if v is not None}, f"\n{LABEL[w]}: to confirm with the vendor.\n")))
    out.append(("fail", "file right, draft tells Ana the odd amount", json.dumps(good), amounts_draft(odd)))
    out.append(("fail", "Ana's fee from the stale memory ($350)", json.dumps(filled(task, dict(EXPECTED, accountant=350))),
                amounts_draft(dict(EXPECTED, accountant=350))))
    out.append(("fail", "total does not add up (4,263)", json.dumps(filled(task, EXPECTED, total=4263)), amounts_draft(EXPECTED)))
    g = copy.deepcopy(good)
    g["items"].append({"category": "Pacific Power electricity", "amount": 236, "status": "current", "effective_from": None, "source": "bank"})
    out.append(("fail", "extra category Ana would import", json.dumps(g), amounts_draft(EXPECTED)))
    g = copy.deepcopy(good)
    g["items"].insert(k, dict(g["items"][k], amount=ODD[w]))
    out.append(("fail", "two current rows for the trapped item (right and odd)", json.dumps(g), amounts_draft(EXPECTED)))
    out.append(("fail", "draft missing", json.dumps(good), ""))
    out.append(("fail", "template left blank", open(os.path.join(FIN, task, "environment/app/monthly_amounts.json")).read(),
                amounts_draft(EXPECTED)))
    out.append(("fail", "answer file not valid JSON", json.dumps(good)[:-5], amounts_draft(EXPECTED)))
    return out


ALL = [(t, *c) for t in TASKS for c in cases(t)]


if pytest:
    @pytest.mark.parametrize("task,want,name,js,draft", ALL, ids=[f"{a[0][22:]}:{a[2]}" for a in ALL])
    def test_case(task, want, name, js, draft):
        spec = json.load(open(os.path.join(FIN, task, "tests/expected_values.json")))
        res = grader(task)(js, draft, spec)
        assert res["pass"] == (want == "pass"), res["reason"]


if __name__ == "__main__":
    bad = 0
    for task, want, name, js, draft in ALL:
        spec = json.load(open(os.path.join(FIN, task, "tests/expected_values.json")))
        res = grader(task)(js, draft, spec)
        ok = res["pass"] == (want == "pass")
        bad += not ok
        # the grader lists conflicting rows in set order, which varies between runs; sort them so this output is byte-stable
        reason = re.sub(r"conflicting \[(.*?)\]", lambda m: "conflicting [" + ", ".join(sorted(re.findall(r"\{[^}]*\}", m.group(1)))) + "]", res["reason"])
        print(f"{'OK ' if ok else 'BAD'} {task[22:]:12} {want:4} {name:58} -> {res.get('outcome', '')}: {reason[:90]}")
    print(f"{len(ALL) - bad}/{len(ALL)} as expected")
    sys.exit(1 if bad else 0)
