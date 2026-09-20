"""Create a clean, dependency-free statement-of-work DOCX."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape


@dataclass(frozen=True)
class SOW:
    title: str
    client: str
    provider: str
    date: str
    summary: str
    deliverables: list[str]
    milestones: list[tuple[str, str]]
    assumptions: list[str]
    fee: str


def validate_sow(sow: SOW) -> None:
    required = {
        "title": sow.title,
        "client": sow.client,
        "provider": sow.provider,
        "date": sow.date,
        "summary": sow.summary,
        "fee": sow.fee,
    }
    missing = [name for name, value in required.items() if not str(value).strip()]
    if missing:
        raise ValueError("missing required field(s): " + ", ".join(missing))
    if not sow.deliverables:
        raise ValueError("at least one deliverable is required")
    if any(not item.strip() for item in sow.deliverables):
        raise ValueError("deliverables cannot be blank")
    if any(not name.strip() or not date.strip() for name, date in sow.milestones):
        raise ValueError("milestones cannot be blank")


def _run(text: str, *, bold: bool = False, size: int = 22) -> str:
    props = f'<w:rPr><w:sz w:val="{size}"/>'
    if bold:
        props += "<w:b/>"
    props += "</w:rPr>"
    return f"<w:r>{props}<w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r>"


def _paragraph(text: str = "", *, bold: bool = False, size: int = 22, style: str = "") -> str:
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{_run(text, bold=bold, size=size)}</w:p>"


def _heading(text: str, level: int = 1) -> str:
    return _paragraph(text, bold=True, size=32 if level == 1 else 26, style=f"Heading{level}")


def _bullet(text: str) -> str:
    return (
        '<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/>'
        f"</w:numPr></w:pPr>{_run(text)}</w:p>"
    )


def _table(rows: list[tuple[str, str]]) -> str:
    xml = '<w:tbl><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/><w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr>'
    for left, right in rows:
        xml += "<w:tr>"
        for cell in (left, right):
            xml += f"<w:tc><w:p>{_run(cell)}</w:p></w:tc>"
        xml += "</w:tr>"
    return xml + "</w:tbl>"


def _document(sow: SOW) -> str:
    body = [_heading(sow.title), _paragraph(f"Prepared for {sow.client} by {sow.provider}"), _paragraph(sow.date)]
    body += [_heading("1. Overview", 2), _paragraph(sow.summary)]
    body += [_heading("2. Deliverables", 2), *[_bullet(item) for item in sow.deliverables]]
    body += [_heading("3. Milestones", 2), _table(sow.milestones)]
    body += [_heading("4. Assumptions", 2), *[_bullet(item) for item in sow.assumptions]]
    body += [_heading("5. Commercials", 2), _paragraph(sow.fee)]
    body += [_heading("6. Acceptance", 2), _paragraph("The client will review the deliverables promptly and provide written feedback. Work is complete when the listed deliverables are supplied and material feedback has been addressed.")]
    body += [_paragraph("", size=22), _paragraph("Client approval: ____________________    Date: __________", size=22)]
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{''.join(body)}<w:sectPr><w:pgSz w:w=\"12240\" w:h=\"15840\"/><w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\"/></w:sectPr></w:body></w:document>"
    )


_CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'''
_RELATIONSHIPS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''
_DOCUMENT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'''
_STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style></w:styles>'''
_NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''


def generate_docx(sow: SOW, output: Path) -> Path:
    validate_sow(sow)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", _CONTENT_TYPES)
        archive.writestr("_rels/.rels", _RELATIONSHIPS)
        archive.writestr("word/_rels/document.xml.rels", _DOCUMENT_RELS)
        archive.writestr("word/document.xml", _document(sow))
        archive.writestr("word/styles.xml", _STYLES)
        archive.writestr("word/numbering.xml", _NUMBERING)
    return output
