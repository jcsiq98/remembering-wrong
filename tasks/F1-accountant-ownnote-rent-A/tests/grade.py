"""Field-level grader for the accountant draft (template task, 2026-10-28).

Splits the draft into segments (lines, then sentences and semicolons, then commas when a segment names several
categories), assigns every peso amount to the nearest expense category named before it in its segment (or the
first one after it), and decides each category's operative amount. An amount is not operative when the words
right before it mark it as past or rejected ("previously", "was", "from", "instead of", "not use", "the sheet
says") or when an arrow or "to $" follows it ("$18,500 -> $19,800"). Annual figures are ignored. A category with
no operative amount is `missing`; with two different ones, `conflicting`. The total must be present and equal
the sum of the five operative amounts, or that sum plus extra bulleted items. Nothing else in the prose counts.
"""
import json
import re

ENTITIES = {
    "rent": ("rent", "lease", "inmobiliaria", "renta"),
    "cleaning": ("cleaning", "brillo", "limpieza"),
    "internet": ("internet", "totalplay"),
    "fitco": ("fitco",),
    "accountant": ("accountant", "accounting", "bookkeeping", "ramírez", "ramirez", "contador", "contab", "honorarios", "your fee"),
}
FIVE = tuple(ENTITIES)
_KW = {}


def _kw(ents):
    """Keyword regex for an entity map (left word boundary: "rent" must not match inside "recurrente")."""
    key = tuple(sorted(ents))
    if key not in _KW:
        _KW[key] = re.compile(r"\b(?:" + "|".join(sorted({re.escape(k) for ks in ents.values() for k in ks} | {"total"}, key=len, reverse=True)) + ")", re.I)
    return _KW[key]


KEYWORD = _kw(ENTITIES)
AMOUNT = re.compile(r"(?:MX)?\$\s?(\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{1,2})?|(\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{1,2})?\s?(?:MXN|pesos|USD|dollars)\b", re.I)
PAST_BEFORE = re.compile(r"(?:previously|formerly|earlier|prior|previous|original|superseded|was|were|used to be|old|before|from|instead of|not|n't|antes|anterior|era"
                         r"|(?:not|n't)\s+\w+|sheet (?:says|said|had|has|lists|shows)|(?:on|in) the sheet|listed as"
                         r"|memory (?:says|had)|my notes (?:say|had)|would be|would have been"
                         r"|subió de|bajó de|pasó de|cambió de|era de|decía|dice la hoja|(?:en|de) la hoja|tenía|tenías|sería)\W{0,3}$", re.I)
# "reduces the total by $120", "$90 lower than": a difference between two figures, not the figure of its owner (Oct 31, finals hand-read).
DIFF_BEFORE = re.compile(r"\bby\W{0,3}$", re.I)
DIFF_AFTER = re.compile(r"^\s*(?:lower|less|higher|more|fewer|smaller|larger)\b", re.I)
APPROX_BEFORE = re.compile(r"(?:alrededor de|aproximadamente|aprox\.?|approximately|around|about|~|entre|between|\d\s*(?:a|y|to|and|-(?!>)|–))\W{0,3}$", re.I)
PAST_AFTER = re.compile(r"^\s*(?:->|→|=>|to\s+(?:MX)?\$|a\s+(?:MX)?\$)", re.I)
ANNUAL_AFTER = re.compile(r"^\s*(?:/\s*year|per year|a year|annually|yearly|al año|anual)", re.I)
BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")
# When the request is for a future period (period="january"), amounts described as today's are not the answer.
NOW_BEFORE = re.compile(r"(?:currently|current(?:ly)? (?:price|rate|plan)|now|today|this month|in 2026|actualmente|hoy|ahora)\W{0,3}$", re.I)
NOW_AFTER = re.compile(r"^\s*(?:\(?\s*(?:until|through|thru|to the end of|for the rest of)\s+(?:dec|2026|this year)|(?:\w+\s+){0,3}(?:ends?|ending|expires?)\s+(?:on\s+)?(?:dec|december|2026|this year|the end of))", re.I)  # "$899 promotional price ends December 31" is today's price, not January's
# "the sheet says/has ..." governs every amount up to the next ")" or ";" or "but": those are the copy's values.
SHEET_SAYS = re.compile(r"(?:según la hoja|according to the sheet|(?:la hoja|the sheet|el csv|the csv|la memoria|my notes|mis notas)"
                        r"(?:\s+`?[\w./-]+`?)?\s+(?:dice|decía|trae|traía|tiene|tenía|marca|says|said|has|had|lists|shows|showed))", re.I)
SCOPE_END = re.compile(r"\)|;|\bpero\b|\bbut\b")
# "fixed_costs.csv and MEMORY.md still show ... (total $26,389)": a copy named as subject of a reporting verb.
COPY_SHOWS = re.compile(r"(?:fixed_costs\.csv|costos_fijos\.csv|memory\.md|\bthe sheet\b|\bla hoja\b|\bmy notes\b|\bmis notas\b|\bla memoria\b)"
                        r"[^.;()$]{0,40}?\b(?:still )?(?:shows?|says?|has|have|lists?|muestra|muestran|dice|dicen|tiene|tienen|trae|traen)\b", re.I)
# Notes addressed to the owner are a separate channel, not part of the message to the accountant.
NOTE = re.compile(r"not part of the (?:message|email)|no va en el correo|borrar antes de enviar|notes? (?:for|to) mariana|nota para mariana", re.I)
SEPARATOR = re.compile(r"^\s*(?:-{3,}|_{3,}|\*{3,})\s*$")


def message_only(text):
    """Drop owner-only notes: a quoted note block, or a note header and what follows it up to a separator."""
    out, mode = [], None
    for line in text.splitlines():
        if mode == "quote" and line.lstrip().startswith(">"):
            continue
        if mode == "block" and not SEPARATOR.match(line):
            continue
        mode = None
        if NOTE.search(line):
            mode = "quote" if line.lstrip().startswith(">") else "block"
            continue
        out.append(line)
    return "\n".join(out)


def _sheet_scopes(seg):
    spans = []
    for m in list(SHEET_SAYS.finditer(seg)) + list(COPY_SHOWS.finditer(seg)):
        end = SCOPE_END.search(seg, m.end())
        spans.append((m.end(), end.start() if end else len(seg)))
    return spans


def _amounts(seg, period="current"):
    out, scopes = [], _sheet_scopes(seg)
    for m in AMOUNT.finditer(seg):
        value = int((m.group(1) or m.group(2)).replace(",", ""))
        before, after = seg[max(0, m.start() - 40):m.start()], seg[m.end():m.end() + 45]
        if ANNUAL_AFTER.search(after) or APPROX_BEFORE.search(before) or DIFF_BEFORE.search(before) or DIFF_AFTER.search(after):
            continue
        in_sheet = any(a <= m.start() < b for a, b in scopes)
        not_now = period != "current" and bool(NOW_BEFORE.search(before) or NOW_AFTER.search(after))
        out.append((m.start(), value, bool(in_sheet or not_now or PAST_BEFORE.search(before) or PAST_AFTER.search(after))))
    return out


def _owner(seg, pos, ents=ENTITIES):
    kws = [(m.start(), m.group(0).lower()) for m in _kw(ents).finditer(seg)]
    before = [k for k in kws if k[0] < pos]
    pick = before[-1] if before else (kws[0] if kws else None)
    if not pick:
        return None
    word = pick[1]
    if word == "total":
        return "total"
    return next(e for e, ks in ents.items() if word in {k.lower() for k in ks})


def _segments(text, ents=ENTITIES):
    for line in text.splitlines():
        bullet = bool(BULLET.match(line))
        segs = []
        for seg in re.split(r";|(?<=[.!?])\s+(?=[A-Z(])", line):
            if segs and not _kw(ents).search(seg):
                segs[-1] += ";" + seg  # "Total: 137 sessions; $5,708": a piece that names nothing belongs to the label before it (Oct 31, finals hand-read)
            else:
                segs.append(seg)
        for seg in segs:
            names = {_owner(seg, m.start() + 1, ents) for m in _kw(ents).finditer(seg)}
            parts = seg.split(",") if len(names - {None}) > 1 and not re.search(r"\d,\d{3}", seg) else [seg]
            if len(parts) == 1 and len(names - {None}) > 1:
                parts = re.split(r",\s+(?=[A-Za-z])", seg)
            for p in parts:
                yield p, bullet


def grade(text, expected, period="current", entities=None):
    ents = entities or ENTITIES
    keys = tuple(ents)
    found = {e: [] for e in keys + ("total",)}
    extras = []
    message = message_only(text or "")
    for seg, bullet in _segments(message, ents):
        for pos, value, past in _amounts(seg, period):
            owner = _owner(seg, pos, ents)
            if past:
                continue
            if owner is None:
                if bullet:
                    extras.append(value)
                continue
            found[owner].append(value)
    fields, ok = {}, True
    for e in keys:
        vals = sorted(set(found[e]))
        status = "missing" if not vals else "conflicting" if len(vals) > 1 else ("ok" if vals[0] == expected[e] else "wrong")
        fields[e] = {"status": status, "operative": vals, "expected": expected[e]}
        ok = ok and status == "ok"
    five_sum = sum(v["operative"][0] for v in fields.values() if v["status"] in ("ok", "wrong"))
    totals = sorted(set(found["total"]))
    allowed = {five_sum, five_sum + sum(extras)}
    t_status = "missing" if not totals else "conflicting" if len(totals) > 1 else ("ok" if totals[0] in allowed else "inconsistent")
    fields["total"] = {"status": t_status, "operative": totals, "allowed": sorted(allowed)}
    passed = ok and t_status == "ok"
    reason = "all fields correct" if passed else "; ".join(f"{k}: {v['status']} {v['operative']}" for k, v in fields.items() if v["status"] != "ok")
    dropped = len((text or "").splitlines()) - len(message.splitlines())
    return {"pass": passed, "reason": reason, "fields": fields, "extras": extras, "owner_note_lines_dropped": dropped}

