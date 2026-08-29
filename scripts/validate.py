#!/usr/bin/env python3
"""Mirror of the app's BundleValidator rules. Exit 1 on any violation."""
import json, sys, subprocess
data = json.load(open("compendium.json"))
errs = []
if data.get("schemaVersion") != 1: errs.append("schemaVersion must be 1")
cats = data.get("categories", []); items = data.get("items", [])
if not cats: errs.append("no categories")
cids = [c["id"] for c in cats]
if len(cids) != len(set(cids)): errs.append("duplicate category id")
iids = [i["id"] for i in items]
dups = {x for x in iids if iids.count(x) > 1}
if dups: errs.append(f"duplicate item ids: {sorted(dups)}")
for i in items:
    if not i.get("name", "").strip(): errs.append(f"empty name: {i.get('id')}")
    if i.get("category") not in cids: errs.append(f"unknown category on {i.get('id')}")
# bundleVersion must be exactly previous + 1 when compared to the base branch
try:
    base = subprocess.run(["git", "show", "origin/main:compendium.json"], capture_output=True, text=True, check=True).stdout
    prev = json.loads(base)["bundleVersion"]
    if data["bundleVersion"] != prev + 1 and data != json.loads(base):
        errs.append(f"bundleVersion must be {prev + 1} (was {data['bundleVersion']})")
    old_ids = {i["id"] for i in json.loads(base)["items"]}
    for i in items:
        if i["id"] in old_ids:
            old = next(o for o in json.loads(base)["items"] if o["id"] == i["id"])
            if old["category"] != i["category"]: errs.append(f"{i['id']} changed category — ids are stable keys")
except subprocess.CalledProcessError:
    pass  # first commit / no base
for e in errs: print("::error::" + e)
print("ok" if not errs else f"{len(errs)} problem(s)")
sys.exit(1 if errs else 0)
