#!/usr/bin/env python3
"""Rules for map.json (app 1.4 and later). Stricter than the app's MapBundleValidator, which
drops a bad entry quietly: here any bad entry fails the push. Exit 1 on any violation."""
import json, subprocess, sys

FREE_LIMIT = 10
KINDS = {"vault", "secret", "collectible", "activity", "other"}
STATUS = {"verified", "unverified"}


def check(data, line_ids, previous=None):
    """Return a list of problems. `line_ids` = checklist item ids a pin may link to.
    `previous` = the last published map.json, or None."""
    errs = []
    if data.get("schemaVersion") != 1: errs.append("schemaVersion must be 1")
    if not isinstance(data.get("bundleVersion"), int): errs.append("bundleVersion must be an integer")
    pins, lines = data.get("pins", []), data.get("storyLines", [])
    seen, free = set(), 0
    for p in pins:
        pid = p.get("id")
        if not pid or pid in seen: errs.append(f"missing or duplicate pin id: {pid}")
        seen.add(pid)
        for axis in ("x", "y"):
            v = p.get(axis)
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= 1:
                errs.append(f"pin {pid}: {axis} must be a number from 0 to 1")
        if not str(p.get("label", "")).strip(): errs.append(f"pin {pid}: empty label")
        if p.get("kind") not in KINDS: errs.append(f"pin {pid}: kind must be one of {sorted(KINDS)}")
        if p.get("status") not in STATUS: errs.append(f"pin {pid}: status must be one of {sorted(STATUS)}")
        prog = p.get("progress")
        if prog is not None and not (type(prog) is int and 0 <= prog <= 100): errs.append(f"pin {pid}: progress 0-100")
        if "free" in p and type(p["free"]) is not bool: errs.append(f"pin {pid}: free must be true or false")
        if p.get("free") is True:
            free += 1
            # A free pin is shown to everyone, so it can never be one that hides behind progress.
            if prog is not None: errs.append(f"pin {pid}: a free pin cannot carry a progress value")
        if p.get("line") is not None and p["line"] not in line_ids:
            errs.append(f"pin {pid}: line '{p['line']}' is not an item in compendium.json")
    if free > FREE_LIMIT: errs.append(f"{free} free pins; at most {FREE_LIMIT}")
    if len(pins) >= FREE_LIMIT and free != FREE_LIMIT:
        errs.append(f"{len(pins)} pins but {free} marked free; mark exactly {FREE_LIMIT}")
    seen = set()
    for s in lines:
        sid = s.get("id")
        if not sid or sid in seen: errs.append(f"missing or duplicate story line id: {sid}")
        seen.add(sid)
        if not str(s.get("label", "")).strip(): errs.append(f"story line {sid}: empty label")
        prog = s.get("progress")
        if not (type(prog) is int and 0 <= prog <= 100): errs.append(f"story line {sid}: progress 0-100 is required")
    if previous:
        if isinstance(previous.get("bundleVersion"), int) and isinstance(data.get("bundleVersion"), int) \
                and data != previous and data["bundleVersion"] <= previous["bundleVersion"]:
            errs.append("content changed: bundleVersion must go up")
        old = {p.get("id"): p.get("line") for p in previous.get("pins", [])}
        for p in pins:
            # A player's tick is stored against the pin's line. Moving a published pin to another
            # line (or off one) would lose that tick, so the link is fixed once published.
            if p.get("id") in old and old[p["id"]] != p.get("line"):
                errs.append(f"pin {p['id']}: line changed from '{old[p['id']]}' to '{p.get('line')}'; publish a new pin id instead")
    return errs


def published():
    """The last map.json this branch differs from: HEAD's if the file was edited, else the one before."""
    here = open("map.json").read()
    for rev in ("HEAD", "HEAD~1"):
        r = subprocess.run(["git", "show", f"{rev}:map.json"], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout != here:
            try: return json.loads(r.stdout)
            except ValueError: return None
    return None


def selftest():
    ok = {"schemaVersion": 1, "bundleVersion": 2, "pins": [
        {"id": "a", "x": 0.5, "y": 0.5, "kind": "vault", "label": "A", "status": "unverified", "free": True, "line": "l1"}],
        "storyLines": [{"id": "s", "label": "Chapter 1, job 1", "progress": 0}]}
    assert check(ok, {"l1"}) == [], check(ok, {"l1"})
    def broken(**change):
        d = json.loads(json.dumps(ok)); d["pins"][0].update(change); return check(d, {"l1", "l2"}, ok if "line" in change else None)
    assert broken(x=1.5) and broken(y="0.5") and broken(label=" ") and broken(kind="bank") and broken(status="sure")
    assert broken(progress=5), "a free pin with progress must fail"
    assert broken(line="nope") and broken(free="yes")
    assert any("line changed" in e for e in broken(line="l2"))
    many = {"schemaVersion": 1, "bundleVersion": 1, "pins": [
        {"id": f"p{i}", "x": 0.1, "y": 0.1, "kind": "secret", "label": "P", "status": "unverified", "free": i < 11} for i in range(12)]}
    assert any("at most" in e for e in check(many, set()))
    for p in many["pins"]: p["free"] = False
    assert any("exactly" in e for e in check(many, set()))
    assert check({"schemaVersion": 1, "bundleVersion": 1, "storyLines": [{"id": "s", "label": "L"}]}, set())
    assert check({"schemaVersion": 1, "bundleVersion": 1}, set()) == []
    print("validate_map selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    data = json.load(open("map.json"))
    line_ids = {i.get("id") for i in json.load(open("compendium.json")).get("items", [])}
    errs = check(data, line_ids, published())
    for e in errs: print("::error::" + e)
    print("map.json ok" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)
