"""Command-line entry point for the SOW DOCX generator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sowgen import SOW, generate_docx


def _load(path: Path) -> SOW:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return SOW(
        title=raw["title"],
        client=raw["client"],
        provider=raw["provider"],
        date=raw["date"],
        summary=raw["summary"],
        deliverables=list(raw["deliverables"]),
        milestones=[(str(row[0]), str(row[1])) for row in raw["milestones"]],
        assumptions=list(raw.get("assumptions", [])),
        fee=raw["fee"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a polished DOCX statement of work from JSON.")
    parser.add_argument("input", type=Path, help="SOW JSON input")
    parser.add_argument("output", type=Path, help="DOCX output")
    args = parser.parse_args()
    generate_docx(_load(args.input), args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
