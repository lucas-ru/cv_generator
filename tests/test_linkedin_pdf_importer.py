import json
import os
import sys

import pytest
from pypdf import PdfWriter

from scripts import linkedin_pdf_importer
from scripts.linkedin_pdf_importer import (
    LinkedInExportFormatError,
    ProfileSourceError,
    load_profile_source,
    parse_linkedin_pdf,
    parse_linkedin_text,
)

ROOT = os.path.dirname(os.path.dirname(__file__))
LINKEDIN_PDF_TEXT = """\
Coordonnées
profile@example.com
www.linkedin.com/in/example
(LinkedIn)
Principales compétences
Intelligence artificielle (IA)
Conception de Harnais
Modèles de Langage de Grande
Taille (LLM)
lucas plume
Ingénieur DevOps chez Example Company
Annecy, Auvergne-Rhône-Alpes, France
Résumé
Profil professionnel de démonstration.
Expérience
Example Company
Ingénieur DevOps
octobre 2023 - Present (3 ans)
Annecy, Auvergne-Rhône-Alpes, France
Gestion de la production et automatisation.
Second Company
Développeur
septembre 2021 - août 2023 (2 ans)
Annecy, Auvergne-Rhône-Alpes, France
Third Company
Développeur web
avril 2020 - septembre 2021 (1 an 6 mois)
Chavanod, Auvergne-Rhône-Alpes, France
Refonte graphique et correction de bugs.
Fourth Company
Équipier
octobre 2019 - avril 2020 (7 mois)
Epagny Metz-Tessy, Auvergne-Rhône-Alpes, France
Fifth Company
Cuisinier
octobre 2018 - octobre 2019 (1 an 1 mois)
Sillingy, Auvergne-Rhône-Alpes, France
Formation
MyDigitalSchool
Master, Management de projet · (septembre 2021 - août 2023)
Université Savoie Mont Blanc
Licence professionnelle, Développement informatique multi-
supports · (2020 - 2021)
Université Savoie Mont Blanc
DUT, Informatique · (2018 - 2020)
Lycée Louis Lachenal
Baccalauréat scientifique, Admis · (juin 2018)
"""


def sample_profile(name="JSON Profile"):
    return {
        "personal_info": {
            "name": name,
            "headline": "Developer",
            "photo": "C:\\old\\profile.jpg",
        },
        "experiences": [],
        "education": [],
        "skills": [],
        "hobbies": ["Lecture"],
        "generated_date": "11/11/2026",
    }


def create_blank_pdf(path):
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    with open(path, "wb") as pdf_file:
        writer.write(pdf_file)


def test_linkedin_pdf_template_is_mapped_without_online_or_photo_data():
    profile = parse_linkedin_text(LINKEDIN_PDF_TEXT, "Profile.pdf")

    assert profile["source_type"] == "linkedin_pdf"
    assert profile["source_status"] == "partial"
    assert profile["personal_info"]["email"] == "profile@example.com"
    assert profile["personal_info"]["photo"] == ""
    assert len(profile["experiences"]) == 5
    assert len(profile["education"]) == 4
    assert len(profile["skills"]) == 3
    assert profile["hobbies"] == []
    assert any(
        skill["name"] == "Modèles de Langage de Grande Taille (LLM)"
        for skill in profile["skills"]
    )
    assert profile["education"][-1]["degree"] == "Baccalauréat scientifique, Admis"

    serialized = json.dumps(profile, ensure_ascii=False).casefold()
    assert "linkedin.com" not in serialized
    assert "source_url" not in profile


def test_cli_writes_profile_json_from_linkedin_pdf(tmp_path, monkeypatch, capsys):
    class FakePage:
        def extract_text(self):
            return LINKEDIN_PDF_TEXT

    class FakeReader:
        is_encrypted = False
        pages = [FakePage()]

        def __init__(self, _pdf_path):
            pass

    output_path = tmp_path / "imported_profile.json"
    script_path = os.path.join(ROOT, "scripts", "linkedin_pdf_importer.py")
    (tmp_path / "Profile.pdf").write_bytes(b"test PDF")
    (tmp_path / "portrait.jpg").write_bytes(b"jpg")
    monkeypatch.setattr(linkedin_pdf_importer, "PdfReader", FakeReader)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            script_path,
            "--data-dir",
            str(tmp_path),
            "--output",
            str(output_path),
        ],
    )

    linkedin_pdf_importer.main()

    imported = json.loads(output_path.read_text(encoding="utf-8"))
    assert imported["source_type"] == "linkedin_pdf"
    assert imported["source_file"] == "Profile.pdf"
    assert imported["photo_candidates"] == ["portrait.jpg"]
    assert "linkedin_pdf" in capsys.readouterr().out


def test_pdf_outside_linkedin_template_falls_back_to_data_json(tmp_path):
    create_blank_pdf(tmp_path / "Profile.pdf")
    (tmp_path / "data.json").write_text(
        json.dumps(sample_profile(), ensure_ascii=False), encoding="utf-8"
    )

    profile = load_profile_source(str(tmp_path))

    assert profile["source_type"] == "local_json"
    assert profile["source_file"] == "data.json"
    assert profile["personal_info"]["name"] == "JSON Profile"
    assert profile["personal_info"]["photo"] == ""
    assert profile["hobbies"] == ["Lecture"]
    assert "ne respecte pas le format LinkedIn attendu" in profile["source_notes"][0]


def test_missing_pdf_uses_data_json_and_clears_stale_photo(tmp_path):
    (tmp_path / "data.json").write_text(
        json.dumps(sample_profile(), ensure_ascii=False), encoding="utf-8"
    )
    (tmp_path / "alternative.json").write_text(
        json.dumps(sample_profile("Alternative")), encoding="utf-8"
    )
    (tmp_path / "portrait.JPG").write_bytes(b"jpg")
    (tmp_path / "ignore.webp").write_bytes(b"webp")

    profile = load_profile_source(str(tmp_path))

    assert profile["source_file"] == "data.json"
    assert profile["personal_info"]["photo"] == ""
    assert profile["source_type"] == "local_json"
    assert profile["photo_candidates"] == ["portrait.JPG"]


def test_multiple_local_photos_are_reported_without_selecting_one(tmp_path):
    (tmp_path / "portrait.jpg").write_bytes(b"jpg")
    (tmp_path / "avatar.png").write_bytes(b"png")
    (tmp_path / "ignore.webp").write_bytes(b"webp")
    (tmp_path / "data.json").write_text(
        json.dumps(sample_profile()), encoding="utf-8"
    )

    profile = load_profile_source(str(tmp_path))

    assert profile["photo_candidates"] == ["avatar.png", "portrait.jpg"]
    assert "Plusieurs photos locales" in profile["source_notes"][-1]


def test_ambiguous_json_fallback_requires_a_choice(tmp_path):
    (tmp_path / "first.json").write_text(
        json.dumps(sample_profile("First")), encoding="utf-8"
    )
    (tmp_path / "second.json").write_text(
        json.dumps(sample_profile("Second")), encoding="utf-8"
    )

    with pytest.raises(ProfileSourceError, match="Plusieurs profils JSON"):
        load_profile_source(str(tmp_path))


def test_non_linkedin_pdf_is_rejected_when_parsed_directly(tmp_path):
    pdf_path = tmp_path / "other.pdf"
    create_blank_pdf(pdf_path)

    with pytest.raises(LinkedInExportFormatError, match="Section LinkedIn manquante"):
        parse_linkedin_pdf(str(pdf_path))
