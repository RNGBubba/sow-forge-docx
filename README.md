# SOW Forge

SOW Forge is an original, dependency-free Python utility that turns a small JSON brief into a professional Microsoft Word statement of work (`.docx`). It is intended for independent consultants and small studios that want a repeatable starting document without uploading client information to a web service.

## Usage

```bash
python sowgen_cli.py example.json output/statement-of-work.docx
```

The input fields are `title`, `client`, `provider`, `date`, `summary`, `deliverables`, `milestones` (pairs of name/date), `assumptions`, and `fee`. The generator validates required content, writes the Office Open XML package directly, and includes headings, bullet lists, a milestone table, commercials, and an acceptance section.

## Verification

```bash
python -m pytest -q
python sowgen_cli.py example.json /tmp/example-sow.docx
python -c "import zipfile; assert zipfile.is_zipfile('/tmp/example-sow.docx')"
```

No external package or network access is required.

## License

MIT. See `LICENSE`.
