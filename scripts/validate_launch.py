#!/usr/bin/env python3
"""Mirror of the app's LaunchBundleValidator rules for launch.json. Exit 1 on any violation."""
import json, sys
data = json.load(open("launch.json"))
errs = []
TOKENS = {"north", "east", "south", "west", "up", "down", "left", "right", "l1", "r1", "l2", "r2"}
STATUS = {"verified", "reported", "unconfirmed"}
GRADES = {"bronze", "silver", "gold", "platinum"}
if data.get("schemaVersion") != 1: errs.append("schemaVersion must be 1")
if not isinstance(data.get("bundleVersion"), int): errs.append("bundleVersion must be an integer")
seen = set()
for c in data.get("codes", []):
    cid = c.get("id")
    if not cid or ("code", cid) in seen: errs.append(f"missing or duplicate code id: {cid}")
    seen.add(("code", cid))
    if not c.get("name", "").strip(): errs.append(f"empty name on code {cid}")
    if c.get("status") not in STATUS: errs.append(f"code {cid}: status must be one of {sorted(STATUS)}")
    if c.get("status") == "verified" and not c.get("checkedAt"): errs.append(f"code {cid}: verified needs checkedAt")
    bad = [t for t in c.get("sequence", []) if t not in TOKENS]
    if bad: errs.append(f"code {cid}: unknown buttons {bad}")
    if not c.get("sequence") and not c.get("phone"): errs.append(f"code {cid}: needs a sequence or a phone number")
for t in data.get("trophies", []):
    tid = t.get("id")
    if not tid or ("trophy", tid) in seen: errs.append(f"missing or duplicate trophy id: {tid}")
    seen.add(("trophy", tid))
    if not t.get("name", "").strip(): errs.append(f"empty name on trophy {tid}")
    if t.get("grade", "bronze") not in GRADES: errs.append(f"trophy {tid}: unknown grade")
    p = t.get("progress")
    if p is not None and not (isinstance(p, int) and 0 <= p <= 100): errs.append(f"trophy {tid}: progress 0-100")
for e in errs: print("::error::" + e)
print("launch.json ok" if not errs else f"{len(errs)} problem(s)")
sys.exit(1 if errs else 0)
