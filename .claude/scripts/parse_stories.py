"""Parse a story backlog xlsx into per-story folders under stories/.

Usage:
    python parse_stories.py --xlsx <path> --out-dir <stories_dir> [--force]

Effects:
    - Creates <out-dir>/<STRY####>/story.md for each row in the xlsx.
    - Maintains <out-dir>/backlog.json (machine-readable) — preserves any
      existing `deps` and `status` values across re-ingest.
    - Refreshes <out-dir>/INDEX.md (human-readable backlog table).

Stdout:
    A JSON summary describing created / updated / skipped story numbers.

Expected xlsx columns (matched by header, case-insensitive):
    Original task | Short description | Epic | Points | State | Status
    | Assigned to | Sprint | Acceptance criteria
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any

warnings.filterwarnings("ignore", module="openpyxl")
import openpyxl  # noqa: E402


STORY_NUMBER_RE = re.compile(r"^STRY\d{7}$")

REQUIRED_HEADERS = {
    "original task": "story_number",
    "short description": "short_description",
    "epic": "epic",
    "points": "points",
    "state": "state",
    "status": "status",
    "assigned to": "assigned_to",
    "sprint": "sprint",
    "acceptance criteria": "acceptance_criteria",
}


def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:max_len].rstrip("-")


def strip_html(raw: str) -> str:
    if not raw:
        return ""
    text = html.unescape(raw)
    text = re.sub(r"<\s*br\s*/?\s*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</\s*p\s*>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<\s*p[^>]*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def map_headers(header_row: tuple[Any, ...]) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for idx, cell in enumerate(header_row):
        if cell is None:
            continue
        key = str(cell).strip().lower()
        if key in REQUIRED_HEADERS:
            mapping[REQUIRED_HEADERS[key]] = idx
    missing = set(REQUIRED_HEADERS.values()) - set(mapping)
    if missing:
        raise SystemExit(
            f"Missing required columns in xlsx: {sorted(missing)}. "
            f"Found headers: {[str(c).strip() if c else '' for c in header_row]}"
        )
    return mapping


def read_rows(xlsx_path: Path) -> list[dict[str, Any]]:
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise SystemExit("Empty workbook")
    header_map = map_headers(rows[0])
    out: list[dict[str, Any]] = []
    for row_idx, row in enumerate(rows[1:], start=2):
        record = {field: row[col_idx] for field, col_idx in header_map.items()}
        story_number = (record.get("story_number") or "").strip()
        if not story_number:
            continue
        if not STORY_NUMBER_RE.match(story_number):
            print(
                f"  ! skipping row {row_idx}: malformed story number '{story_number}'",
                file=sys.stderr,
            )
            continue
        record["story_number"] = story_number
        record["short_description"] = (record.get("short_description") or "").strip()
        record["epic"] = (record.get("epic") or "").strip()
        record["state"] = (record.get("state") or "").strip()
        record["status"] = (record.get("status") or "").strip()
        record["assigned_to"] = (record.get("assigned_to") or "").strip()
        record["sprint"] = (record.get("sprint") or "").strip()
        record["acceptance_criteria"] = strip_html(record.get("acceptance_criteria") or "")
        try:
            record["points"] = float(record.get("points")) if record.get("points") is not None else None
        except (TypeError, ValueError):
            record["points"] = None
        out.append(record)
    return out


def write_story_md(folder: Path, record: dict[str, Any], deps: list[str], status: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {record['story_number']} — {record['short_description']}",
        "",
        f"- Epic: {record['epic'] or '(none)'}",
        f"- Points: {record['points'] if record['points'] is not None else '(none)'}",
        f"- State: {record['state'] or '(none)'}",
        f"- Sprint: {record['sprint'] or '(none)'}",
        f"- Assigned to: {record['assigned_to'] or '(none)'}",
        f"- Dependencies: {', '.join(deps) if deps else '(none)'}",
        f"- Status: {status}",
        "",
        "## Acceptance criteria",
        "",
        record["acceptance_criteria"] or "(none provided)",
        "",
    ]
    (folder / "story.md").write_text("\n".join(lines), encoding="utf-8")


def write_index_md(out_dir: Path, backlog: dict[str, Any]) -> None:
    lines = [
        "# Stories backlog",
        "",
        f"Source: `{backlog.get('source', '')}`  ",
        f"Last ingested: {backlog.get('ingested_at', '')}",
        "",
        "| Story | Short description | Epic | Points | State | Deps | Status |",
        "|-------|-------------------|------|--------|-------|------|--------|",
    ]
    for number, entry in sorted(backlog["stories"].items()):
        deps = ", ".join(entry["deps"]) if entry["deps"] else "—"
        points = entry["points"] if entry["points"] is not None else "—"
        lines.append(
            f"| [{number}]({number}/story.md) "
            f"| {entry['short_description']} "
            f"| {entry['epic']} "
            f"| {points} "
            f"| {entry['state']} "
            f"| {deps} "
            f"| {entry['status']} |"
        )
    lines.append("")
    lines.append("Runner commands:")
    lines.append("")
    lines.append("- Single story: `/stories-run <STRY####>`")
    lines.append("- Batch up to 3: `/stories-batch <STRY####> [STRY####] [STRY####]`")
    lines.append("")
    (out_dir / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def load_existing_backlog(out_dir: Path) -> dict[str, Any]:
    path = out_dir / "backlog.json"
    if not path.exists():
        return {"version": 1, "source": "", "ingested_at": "", "stories": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"backlog.json is corrupt: {exc}")
    data.setdefault("stories", {})
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xlsx", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing story.md files")
    args = parser.parse_args()

    if not args.xlsx.exists():
        raise SystemExit(f"xlsx not found: {args.xlsx}")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    rows = read_rows(args.xlsx)
    backlog = load_existing_backlog(args.out_dir)
    backlog["source"] = str(args.xlsx.name)
    backlog["ingested_at"] = datetime.now().isoformat(timespec="seconds")

    created: list[str] = []
    updated: list[str] = []
    skipped: list[str] = []

    for record in rows:
        number = record["story_number"]
        existing = backlog["stories"].get(number)
        deps = existing["deps"] if existing else []
        status = existing["status"] if existing else "ingested"

        entry = {
            "short_description": record["short_description"],
            "epic": record["epic"],
            "points": record["points"],
            "state": record["state"],
            "sprint": record["sprint"],
            "assigned_to": record["assigned_to"],
            "slug": slugify(record["short_description"]),
            "deps": deps,
            "status": status,
        }
        backlog["stories"][number] = entry

        story_folder = args.out_dir / number
        story_md = story_folder / "story.md"
        if story_md.exists() and not args.force:
            skipped.append(number)
        else:
            write_story_md(story_folder, record, deps, status)
            if existing is None:
                created.append(number)
            else:
                updated.append(number)

    backlog_path = args.out_dir / "backlog.json"
    backlog_path.write_text(
        json.dumps(backlog, indent=2, sort_keys=True), encoding="utf-8"
    )
    write_index_md(args.out_dir, backlog)

    summary = {
        "out_dir": str(args.out_dir.resolve()),
        "source": str(args.xlsx.resolve()),
        "created": created,
        "updated": updated,
        "skipped_existing": skipped,
        "total_in_xlsx": len(rows),
        "total_in_backlog": len(backlog["stories"]),
        "needs_deps": sorted(
            n for n, e in backlog["stories"].items() if not e["deps"]
        ),
    }
    json.dump(summary, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
