# BET: SOW Forge DOCX generator

## Offer

An original, local-only Python tool for consultants and small studios: turn a structured JSON brief into a polished Microsoft Word statement of work. It avoids uploads and has no runtime dependencies.

## Suggested price

Free/open source for adoption; offer a $29-$79 customization or branded-template service as the first paid upsell.

## 30-day path

Publish the public repository, demonstrate the generated sample document, and share it with independent consultants and small agencies through permitted, non-spam channels. Convert requests for custom branding, clauses, or field mappings into fixed-price services.

## Human click

A buyer must choose to download, run, or request customization. No payment rail was used or claimed.

## Artifact

- `output/statement-of-work.docx` — generated sample DOCX.
- `sowgen.py` and `sowgen_cli.py` — implementation.
- `test_sowgen.py` — tests.
- `receipts/t_b9c27d09.json` — DoneMeans receipt bound to the generated artifact and test command.

## Verification

- `python -m pytest -q` -> 2 passed.
- CLI generation completed: `python sowgen_cli.py example.json output/statement-of-work.docx`.
- ZIP/DOCX validity check passed with Python `zipfile`.
- DoneMeans receipt verification passed:
  `uv run --project /home/vboxuser/projects/donemeans donemeans --root /home/vboxuser/projects/overnight-revenue/bets/docx-sow-template receipt verify receipts/t_b9c27d09.json`

## GitHub

https://github.com/RNGBubba/sow-forge-docx

Published as a new public repository. No private repositories, secrets, paid services, or external messages were used.
