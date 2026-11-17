# Sidequest compendium data

Community-maintained checklist data for the Sidequest iOS companion app (an offline companion for an open-world game). The app fetches `compendium.json` from this repo on launch and falls back to a bundled copy offline.

## Contributing
Edit `compendium.json` in a pull request. Rules — CI enforces the first three, reviewers enforce the rest:
1. `schemaVersion` stays `1`. Bump `bundleVersion` by exactly 1 per merged PR (the app rejects lower or equal versions).
2. Every `id` is unique and never changes once merged (the app keys user checkmarks on it). Removed items should be deleted, not renamed.
3. Every item's `category` exists in `categories`; every `name` is non-empty.
4. **No trademarks, no copied content.** Item names and hints are your own generic descriptions (name, category, location hint). No game title, publisher, city/character names, in-game brand names, mission text, dialogue or artwork. Reviewers will decline PRs that break this.
5. Keep hints short and spoiler-light.

## Schema (v1)
```json
{ "schemaVersion": 1, "bundleVersion": 1, "updatedAt": "YYYY-MM-DD",
  "categories": [ { "id": "vehicles", "name": "Vehicles", "order": 1 } ],
  "items": [ { "id": "veh-001", "category": "vehicles", "name": "…", "hint": "…", "tags": ["…"] } ],
  "checkpoints": [ { "id": "cp-01", "label": "…", "progress": 25 } ] }
```
Unknown fields are ignored by the app. Not affiliated with any game publisher.

## launch.json (app 1.1 and later)
Codes, trophies and story checkpoints. Older app versions never read this file. Bump `bundleVersion` on every change; the app ignores a file that is not newer than the one it holds.
```json
{ "schemaVersion": 1, "bundleVersion": 2, "updatedAt": "YYYY-MM-DD",
  "codes": [ { "id": "c-001", "name": "…", "effect": "Player", "sequence": ["north", "r1", "left"], "phone": "…",
               "status": "verified | reported | unconfirmed", "checkedAt": "YYYY-MM-DD", "note": "…" } ],
  "trophies": [ { "id": "t-001", "name": "…", "detail": "…", "grade": "bronze | silver | gold | platinum", "progress": 25 } ],
  "checkpoints": [ { "id": "cp-01", "label": "…", "progress": 25 } ] }
```
- Buttons are named by position so one sequence serves both pads: `north east south west`, `up down left right`, `l1 r1 l2 r2`.
- **`verified` means someone entered it on a console on the `checkedAt` date.** Seen online is `reported`. Never add a code from an earlier game.
- Trophy names and requirements are written in your own words; `progress` is where on the 0-100 story scale it stops being a spoiler.
