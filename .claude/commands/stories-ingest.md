---
description: Parse a story backlog xlsx into per-story folders under stories/ in the current working directory, then interactively capture dependencies for each story.
argument-hint: <path-to-xlsx>
---

You are ingesting a Green DC story backlog spreadsheet into the local `stories/` directory.

## Input
$ARGUMENTS

## Step 1 — Resolve the xlsx path

- If `$ARGUMENTS` contains a path (quoted or not), use it verbatim after stripping surrounding quotes. The user may pass the path as an `@`-attachment — accept either form.
- If absent, ask the user for the path. Common default to suggest: `C:\Users\kenneth.h.hernane\Downloads\rm_story.xlsx`.
- Verify the file exists before running anything. If not, stop and surface the bad path.

## Step 2 — Run the parser

From the current working directory, run:

```
python .claude/scripts/parse_stories.py --xlsx "<resolved-path>" --out-dir stories
```

Add `--force` ONLY if the user explicitly said to re-ingest or overwrite.

The script prints a JSON summary on stdout — capture it. It contains: `created`, `updated`, `skipped_existing`, `total_in_xlsx`, `total_in_backlog`, `needs_deps`.

## Step 3 — Show what was ingested

Print a compact markdown table of the stories present in the xlsx (story number, short description, state, points). Mention counts: created vs. updated vs. skipped.

If the script's `skipped_existing` list is non-empty, remind the user those story.md files were preserved as-is (re-run with `--force` to overwrite).

## Step 4 — Capture dependencies interactively

For every story in the parser's `needs_deps` list (i.e. `deps == []` in backlog.json):

- Use **AskUserQuestion** if there are 1–4 such stories: one question per story, with options like "None", "Has prerequisites" (and let user type the story numbers).
- If there are more than 4, batch them in a single chat prompt that lists each story with its short description and asks the user to reply with lines like `STRY0010049: none` or `STRY0010230: STRY0010049, STRY0010053`.

For each declared dependency:
- Validate it is a real story number that exists in `stories/backlog.json` (someone might typo). If not, surface it and re-ask.
- Reject self-dependencies and obvious cycles (A→B and B→A); explain and re-ask.

Once all deps are collected:
- Edit `stories/backlog.json` in place: set `stories.<STRY####>.deps` to the user's array (empty list if "none").
- Re-write each affected `stories/<STRY####>/story.md` — replace the `- Dependencies: ...` line with the new list.
- Re-run the parser ONCE more **without** `--force` so `INDEX.md` is regenerated from the updated backlog. (The script preserves existing deps + status when merging, so this is safe.)

## Step 5 — Wrap-up

Print:
- Absolute path to `stories/` and `stories/INDEX.md`
- Counts: total stories, stories with declared deps, stories without
- Next-step hints, verbatim:
  - Single story: `/stories-run STRY####`
  - Up to 3 in batch: `/stories-batch STRY#### STRY#### STRY####`

## Rules
- Never overwrite an existing `story.md` without `--force`.
- Never invent dependencies — only what the user typed.
- If the parser fails (missing column, malformed story number), surface stderr to the user and stop.
- Do NOT call any ServiceNow MCP tool in this command — ingest is purely local.
