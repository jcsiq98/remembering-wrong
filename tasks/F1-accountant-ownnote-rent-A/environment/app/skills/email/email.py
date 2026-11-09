#!/usr/bin/env python3
"""email skill CLI. Usage: python3 skills/email/email.py list [--limit N] | search --query TEXT [--since YYYY-MM-DD] | get --id ID"""
import argparse, json, time
from pathlib import Path

DATA = json.loads((Path(__file__).parent / "data.json").read_text(encoding="utf-8"))

def match(rec, q):
    return q.lower() in json.dumps(rec, ensure_ascii=False).lower()

ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
l = sub.add_parser("list"); l.add_argument("--limit", type=int, default=50)
s = sub.add_parser("search"); s.add_argument("--query", required=True); s.add_argument("--since")
g = sub.add_parser("get"); g.add_argument("--id", required=True)
a = ap.parse_args()
recs = DATA["records"]
if a.cmd == "list":
    out = recs[-a.limit:]
elif a.cmd == "search":
    out = [r for r in recs if match(r, a.query) and (not a.since or r.get("date", "") >= a.since)]
else:
    out = [r for r in recs if str(r.get("id")) == a.id]
print(json.dumps(out, ensure_ascii=False, indent=2))
try:
    with open("/logs/agent/skill_reads.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time(), "skill": "email", "cmd": a.cmd,
                            "args": {k: v for k, v in vars(a).items() if k != "cmd"},
                            "returned_ids": [r.get("id") for r in out]}) + "\n")
except Exception:
    pass
