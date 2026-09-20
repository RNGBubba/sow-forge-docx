import zipfile
from pathlib import Path

import pytest

from sowgen import SOW, generate_docx, validate_sow


def sample_sow() -> SOW:
    return SOW(
        title="Website accessibility audit",
        client="Northstar Studio",
        provider="RNGBubba Consulting",
        date="2026-09-20",
        summary="Review the public website and provide a prioritized remediation brief.",
        deliverables=["Audit brief in PDF", "Prioritized issue register"],
        milestones=[("Kickoff", "2026-09-22"), ("Delivery", "2026-10-02")],
        assumptions=["Client supplies a staging URL and one point of contact."],
        fee="USD 1,200 fixed fee",
    )


def test_generate_docx_contains_required_word_parts_and_text(tmp_path: Path):
    output = tmp_path / "statement-of-work.docx"
    generate_docx(sample_sow(), output)

    assert zipfile.is_zipfile(output)
    with zipfile.ZipFile(output) as docx:
        names = set(docx.namelist())
        assert "[Content_Types].xml" in names
        assert "word/document.xml" in names
        document_xml = docx.read("word/document.xml").decode("utf-8")
        assert "Website accessibility audit" in document_xml
        assert "Prioritized issue register" in document_xml
        assert "USD 1,200 fixed fee" in document_xml


def test_validate_sow_rejects_missing_deliverables():
    sow = sample_sow()
    invalid = SOW(**{**sow.__dict__, "deliverables": []})

    with pytest.raises(ValueError, match="deliverable"):
        validate_sow(invalid)
