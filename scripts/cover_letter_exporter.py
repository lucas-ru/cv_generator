"""Export a plain-text Markdown cover letter to a PDF-convertible DOCX file."""

import argparse
import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Mm, Pt


def export_markdown_to_docx(input_path: Path, output_path: Path) -> None:
    """Convert blank-line-separated letter paragraphs into a formatted DOCX."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    if input_path.resolve() == output_path.resolve():
        raise ValueError("Les fichiers d'entrée et de sortie doivent être différents.")
    if output_path.suffix.lower() != ".docx":
        raise ValueError("Le fichier de sortie doit avoir l'extension .docx.")

    source = input_path.read_text(encoding="utf-8-sig").strip()
    paragraphs = [
        [line.strip() for line in block.splitlines() if line.strip()]
        for block in re.split(r"\n\s*\n", source)
        if block.strip()
    ]
    if not paragraphs:
        raise ValueError("La lettre est vide : aucun fichier DOCX n'a été créé.")
    subject_index = next(
        (
            index
            for index, lines in enumerate(paragraphs)
            if lines[0].casefold().startswith("objet :")
        ),
        None,
    )

    document = Document()
    section = document.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(25)
    section.bottom_margin = Mm(25)
    section.left_margin = Mm(25)
    section.right_margin = Mm(25)

    normal_style = document.styles["Normal"]
    normal_style.font.name = "Arial"
    normal_style.font.size = Pt(11)
    normal_style.paragraph_format.space_after = Pt(8)
    normal_style.paragraph_format.line_spacing = 1.15

    for paragraph_index, lines in enumerate(paragraphs):
        paragraph = document.add_paragraph()
        if subject_index is not None and paragraph_index in (
            1,
            subject_index - 1,
        ):
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for index, line in enumerate(lines):
            if index:
                paragraph.add_run().add_break()
            run = paragraph.add_run(line)
            if subject_index is not None and paragraph_index == 0 and index == 0:
                run.bold = True
                run.font.size = Pt(14)
            elif subject_index is not None and paragraph_index == subject_index:
                run.bold = True

    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(output_path))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convertit une lettre Markdown en document Word DOCX."
    )
    parser.add_argument(
        "--input", required=True, type=Path, help="Fichier source Markdown"
    )
    parser.add_argument(
        "--output", required=True, type=Path, help="Fichier DOCX de sortie"
    )
    args = parser.parse_args()

    try:
        export_markdown_to_docx(args.input, args.output)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Document Word généré : {args.output}")


if __name__ == "__main__":
    main()
