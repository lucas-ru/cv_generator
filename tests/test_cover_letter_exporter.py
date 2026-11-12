import subprocess
import sys
from pathlib import Path

import pytest
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

from scripts.cover_letter_exporter import export_markdown_to_docx

ROOT = Path(__file__).resolve().parents[1]


def test_exporter_creates_readable_docx_in_nested_output_directory(tmp_path):
    source = tmp_path / "lettre.md"
    source.write_text(
        "Madame, Monsieur,\n\n"
        "Je candidate au poste d'ingénieure.\n\n"
        "Mon expérience correspond aux besoins du poste.\n\n"
        "Je serais heureuse d'échanger avec vous.\n\n"
        "Cordialement,\nCamille",
        encoding="utf-8",
    )
    output = tmp_path / "nested" / "lettre.docx"

    export_markdown_to_docx(source, output)

    document = Document(str(output))
    assert [paragraph.text for paragraph in document.paragraphs] == [
        "Madame, Monsieur,",
        "Je candidate au poste d'ingénieure.",
        "Mon expérience correspond aux besoins du poste.",
        "Je serais heureuse d'échanger avec vous.",
        "Cordialement,\nCamille",
    ]
    assert output.is_file()


def test_exporter_rejects_empty_letter(tmp_path):
    source = tmp_path / "lettre.md"
    source.write_text(" \n\n", encoding="utf-8")
    output = tmp_path / "lettre.docx"

    with pytest.raises(ValueError, match="lettre est vide"):
        export_markdown_to_docx(source, output)

    assert not output.exists()


def test_exporter_formats_standard_cover_letter_blocks(tmp_path):
    source = tmp_path / "lettre.md"
    source.write_text(
        "Lucas Plume\n+33 6 29 39 83 65 | lucas@example.com\n\n"
        "Équipe de recrutement\nCA-GIP\nGuyancourt\n\n"
        "Cran-Gevrier, le 12 novembre 2026\n\n"
        "Objet : Candidature au poste de Tech Lead Dev\n\n"
        "Madame, Monsieur,\n\n"
        "Introduction.\n\nDéveloppement.\n\nConclusion.\n\n"
        "Veuillez agréer mes salutations distinguées.\n\nLucas Plume",
        encoding="utf-8",
    )
    output = tmp_path / "lettre.docx"

    export_markdown_to_docx(source, output)

    document = Document(str(output))
    assert document.paragraphs[0].runs[0].bold
    assert document.paragraphs[0].runs[0].font.size == Pt(14)
    assert document.paragraphs[1].alignment == WD_ALIGN_PARAGRAPH.RIGHT
    assert document.paragraphs[2].alignment == WD_ALIGN_PARAGRAPH.RIGHT
    assert all(run.bold for run in document.paragraphs[3].runs)


def test_exporter_cli_creates_docx(tmp_path):
    source = tmp_path / "lettre.md"
    source.write_text(
        "Première partie.\n\nDeuxième partie.\n\nTroisième partie.",
        encoding="utf-8",
    )
    output = tmp_path / "lettre.docx"

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "cover_letter_exporter.py"),
            "--input",
            str(source),
            "--output",
            str(output),
        ],
        capture_output=True,
        check=True,
        text=True,
    )

    assert "Document Word généré" in result.stdout
    assert [paragraph.text for paragraph in Document(str(output)).paragraphs] == [
        "Première partie.",
        "Deuxième partie.",
        "Troisième partie.",
    ]
