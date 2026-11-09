import json
import sys
from pathlib import Path

sys.path.insert(0, "/tests")
from grade2 import grade_task

SPEC = json.loads(Path("/tests/expected_values.json").read_text())


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def test_answer_file_and_draft():
    res = grade_task(_read("/app/" + SPEC["json"]), _read("/app/" + SPEC["draft"]), SPEC)
    Path("/logs/verifier").mkdir(parents=True, exist_ok=True)
    Path("/logs/verifier/fields.json").write_text(json.dumps(res, indent=1))
    assert res["pass"], res["reason"]
