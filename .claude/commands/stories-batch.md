---
description: Run up to 3 ingested stories sequentially in dependency order through the full /sn-workflow. All gates preserved per story. Halts the batch on the first failure or cancel.
argument-hint: <STRY####> [STRY####] [STRY####]
---

You are running a batch of 1–3 stories sequentially. Each story goes through the full `/sn-workflow` with all human-in-the-loop gates intact.

## Input
$ARGUMENTS

## Step 1 — Parse and validate

- Extract 1–3 story numbers from `$ARGUMENTS` (whitespace or comma-separated). Each must match `STRY\d{7}`.
- **Hard cap: 3.** If more than 3 are given, refuse and ask the user to narrow it down. Do not silently truncate.
- For each number, confirm `stories/<STRY####>/story.md` exists. Missing → stop and tell the user to ingest first.
- Read `stories/backlog.json`. Confirm every requested story is present.

## Step 2 — Resolve dependencies and pick an order

Build a dependency graph restricted to the requested batch:

1. **In-batch deps** (a requested story depends on another requested story) define the topo order inside the batch.
2. **External deps** (a requested story depends on a story NOT in the batch) must be checked against `backlog.json`:
   - If the external dep's `status == "done"` → OK.
   - Otherwise → flag it.

Topo-sort the in-batch deps. On a cycle, stop and surface the cycle.

Show the user:
- Planned execution order (numbered 1..N)
- Any external deps that are not yet `done` (story number + status)
- Any requested story whose own `status` is already `done` (offer to re-run or skip)

**GATE 0**: ask the user to confirm before starting the batch. If they decline, stop.

## Step 3 — Execute each story in order

Read `.claude/commands/sn-workflow.md` once. You'll execute it for each story.

For each story in topo order (i = 1..N):

1. Print a clear banner: `=== Starting story i of N: STRY#### — <short description> ===`
2. Update `backlog.json`: set this story's `status = "running"`.
3. Read this story's `stories/<STRY####>/story.md`. The header + **Acceptance criteria** section is the story-text argument.
4. Execute every step in `sn-workflow.md` end-to-end with that story text:
   - Step 0 setup (instance confirm + story number + folder probe + update-set probe)
   - Step 1 analysis + GATE
   - Step 2 development + GATE
   - Step 3 testing + GATE
   - Step 4 documentation
   - Step 5 wrap-up + update-set completion ask
5. After `/sn-workflow` returns:
   - **Success** (doc produced, no FAIL the user rejected): set this story's `status = "done"` in `backlog.json`, then continue to story i+1.
   - **User cancelled / phase errored / user accepted a FAIL but flagged as blocking**: set `status = "blocked"`, write a one-line `last_run_note`, **STOP THE BATCH**. Do not start later stories — they may depend on this one. Surface the failure and the remaining unexecuted stories.

## Step 4 — Final summary

Print a single summary table covering all stories in the batch:

| # | Story | Outcome | Workflow folder | Update set | ATF result | Tech-doc |
|---|-------|---------|-----------------|-----------|------------|----------|

Then a one-liner per story explaining the outcome (e.g. "done after 1 dev-cycle", "blocked at test phase: <reason>", "not started: batch halted at story 1").

## Rules
- **Hard cap of 3.** Never run a 4th in the same invocation.
- **Never auto-approve** a `/sn-workflow` gate. The whole point of sequential mode is to keep the gates.
- **Halt on first failure.** Do not start later stories after a stop — silent skipping of dependent stories is worse than a clear halt.
- Touch only the requested stories' entries in `backlog.json`. Do not bulk-modify.
- Do NOT modify `.claude/commands/sn-workflow.md` or any `sn-*` agent.
- If `/sn-workflow` refuses for a structural reason (e.g. analyst flags prod), stop the batch immediately and surface it.
