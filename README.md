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

## Where the launch-week facts came from (2026-11-18)
Numbers and requirements only, rewritten in our own words; no names, titles or text copied.
- Trophies (55: 1 platinum, 2 gold, 6 silver, 46 bronze) and the 100% requirement counts: the
  PowerPyx trophy roadmap and completion checklist pages, and Press Start's checklist article.
- Codes: only sequences that the PowerPyx cheats page and the GameRiv cheats page both list
  (17 of 61). All are marked `reported`. A code becomes `verified` only when someone on this
  project enters it on a console, with that date. Sequences the sources do not agree on are left out.
- Five trophies have no confirmed requirement yet and say so.


## Where the tips came from (2026-11-24)
Facts only, rewritten in our own words; no names, titles or text copied.
- Checklist hints (14 lines) and the two trophy notes were taken from search summaries of
  published 100% checklists, trophy roadmaps, robbery, fence, stunt and collectible guides
  (PowerPyx, Push Square, games.gg, Alcast, GamerFuzion, KeenGamer, game-checklists and others).
- They were NOT cross-checked line by line against each page and NOT verified by play. A line
  that starts with "Reported:" is one we already know rests on a single guide.
- A hint is corrected or removed when someone on this project sees otherwise in the game.

## Robbery spots and secrets (2026-11-24)
Facts only, in our own words; no place, bank, character, show or game names.
- Robbery spots (8 lines): two bank guides (games.gg and one fan site) were opened and agree on the
  eight large vaults, their areas, payout ranges and the small-bank counts ("Reported:" marks
  what only one of them says); a third (GamerFuzion)
  agrees on the counts and the how-to. No guide lists the loan-store locations, so none are here.
- Secrets (8 lines): three pages were opened (Red Bull and two fan sites). Seven lines
  appear on all three; "After the lights" on two. Where they disagree the hint says so. Finds
  that are only a reference to a film, show or earlier game are left out.
- Not verified by play.
