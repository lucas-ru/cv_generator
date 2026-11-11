"""Import a LinkedIn profile PDF into the CV generator's profile schema."""

import argparse
import json
import os
import re
import unicodedata
from typing import Dict, List, Optional, Tuple

from pypdf import PdfReader
from pypdf.errors import PdfReadError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DEFAULT_OUTPUT = os.path.join(ROOT, ".cv-work", "linkedin_profile.json")
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png"}

REQUIRED_SECTIONS = (
    "Coordonnées",
    "Principales compétences",
    "Résumé",
    "Expérience",
    "Formation",
)
DATE_RANGE_RE = re.compile(
    r"(?P<start>(?:[^\W_]+\s+)?(?:19|20)\d{2})\s*[-–—]\s*"
    r"(?P<end>(?:(?:[^\W_]+\s+)?(?:19|20)\d{2}|"
    r"present|présent|current|actuel|aujourd'hui))",
    re.IGNORECASE,
)
SINGLE_DATE_RE = re.compile(r"(?:[^\W_]+\s+)?(?:19|20)\d{2}", re.IGNORECASE)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
PAGE_FOOTER_RE = re.compile(r"^page\s+\d+\s+of\s+\d+$", re.IGNORECASE)
SKILL_CONTINUATIONS = (" grande", " grand", " de", " du", " des", " et")


class LinkedInExportFormatError(ValueError):
    """Raised when a PDF is not a supported LinkedIn profile export."""


class ProfileSourceError(ValueError):
    """Raised when no unambiguous local profile source can be selected."""


def _fold(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _clean_lines(text: str) -> List[str]:
    lines: List[str] = []
    for raw_line in text.replace("\u00a0", " ").splitlines():
        line = " ".join(raw_line.split())
        if not line or PAGE_FOOTER_RE.match(line):
            continue
        if lines and lines[-1].endswith("-") and line[0].islower():
            lines[-1] += line
        else:
            lines.append(line)
    return lines


def _section_indexes(lines: List[str]) -> Dict[str, int]:
    indexes: Dict[str, int] = {}
    folded_lines = [_fold(line) for line in lines]
    for section in REQUIRED_SECTIONS:
        folded_section = _fold(section)
        try:
            indexes[section] = folded_lines.index(folded_section)
        except ValueError as error:
            raise LinkedInExportFormatError(
                f"Section LinkedIn manquante : {section}."
            ) from error

    if not (
        indexes["Coordonnées"]
        < indexes["Principales compétences"]
        < indexes["Résumé"]
        < indexes["Expérience"]
        < indexes["Formation"]
    ):
        raise LinkedInExportFormatError(
            "L'ordre des sections ne correspond pas à l'export LinkedIn attendu."
        )
    return indexes


def _date_range(line: str) -> Optional[Tuple[str, str]]:
    match = DATE_RANGE_RE.search(line)
    if not match:
        return None
    return match.group("start").strip(), match.group("end").strip()


def _profile_header(
    lines: List[str], skills_index: int, summary_index: int
) -> Tuple[int, str]:
    candidates = [
        index
        for index in range(skills_index + 1, summary_index)
        if lines[index].count(",") >= 2
    ]
    if not candidates:
        raise LinkedInExportFormatError(
            "Impossible d'identifier le bloc nom, intitulé et localisation."
        )

    location_index = candidates[-1]
    if location_index - 2 <= skills_index:
        raise LinkedInExportFormatError(
            "Le bloc d'identité du profil est incomplet."
        )
    return location_index - 2, lines[location_index]


def _skills(lines: List[str], start: int, end: int) -> List[Dict[str, object]]:
    values: List[str] = []
    for line in lines[start:end]:
        if values and (
            values[-1].endswith("-")
            or _fold(values[-1]).endswith(SKILL_CONTINUATIONS)
        ):
            if values[-1].endswith("-"):
                values[-1] += line
            else:
                values[-1] += f" {line}"
        else:
            values.append(line)
    return [{"name": value, "endorsements": 0} for value in values]


def _experiences(
    lines: List[str], start: int, end: int
) -> List[Dict[str, object]]:
    date_indexes = [
        index for index in range(start + 1, end) if _date_range(lines[index])
    ]
    experiences: List[Dict[str, object]] = []

    for position, date_index in enumerate(date_indexes):
        dates = _date_range(lines[date_index])
        if not dates or date_index - 2 < start:
            continue

        next_company_index = (
            date_indexes[position + 1] - 2
            if position + 1 < len(date_indexes)
            else end
        )
        location_index = date_index + 1
        description_end = max(date_index + 2, next_company_index)
        description = " ".join(lines[date_index + 2 : description_end]).strip()
        start_date, end_date = dates

        experiences.append(
            {
                "title": lines[date_index - 1],
                "company": lines[date_index - 2],
                "location": (
                    lines[location_index]
                    if location_index < next_company_index
                    else ""
                ),
                "start_date": start_date,
                "end_date": end_date,
                "is_current": _fold(end_date)
                in {"present", "présent", "current", "actuel", "aujourd'hui"},
                "description": description,
            }
        )
    return experiences


def _education(lines: List[str], start: int) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for index in range(start + 1, len(lines)):
        line = lines[index]
        date_range = _date_range(line)
        if date_range:
            date_match = DATE_RANGE_RE.search(line)
            start_date, end_date = date_range
        else:
            date_match = SINGLE_DATE_RE.search(line)
            if not date_match:
                continue
            start_date, end_date = date_match.group(0).strip(), ""

        if date_match is None or index <= start:
            continue
        degree_field = line[: date_match.start()].rstrip(" ·(").strip()
        if not degree_field:
            continue

        parts = [part.strip() for part in degree_field.split(",", 1)]
        degree = parts[0]
        field = parts[1] if len(parts) == 2 else ""
        if _fold(field) in {"admis", "passed"}:
            degree = degree_field
            field = ""

        entries.append(
            {
                "school": lines[index - 1],
                "degree": degree,
                "field": field,
                "start_date": start_date,
                "end_date": end_date,
                "description": "",
            }
        )
    return entries


def parse_linkedin_text(text: str, source_file: str) -> Dict[str, object]:
    """Map text from the supported French LinkedIn export to the CV schema."""
    lines = _clean_lines(text)
    indexes = _section_indexes(lines)
    skills_index = indexes["Principales compétences"]
    summary_index = indexes["Résumé"]
    name_index, location = _profile_header(lines, skills_index, summary_index)

    if name_index - 1 <= skills_index or not lines[name_index].strip():
        raise LinkedInExportFormatError("Le nom du profil est absent.")

    contacts = lines[indexes["Coordonnées"] + 1 : skills_index]
    email = next(
        (
            match.group(0)
            for line in contacts
            if (match := EMAIL_RE.search(line))
        ),
        "",
    )

    experience_start = indexes["Expérience"]
    education_start = indexes["Formation"]
    experiences = _experiences(lines, experience_start, education_start)
    education = _education(lines, education_start)
    if not experiences or not education:
        raise LinkedInExportFormatError(
            "Le PDF ne contient pas d'expériences ou de formations exploitables."
        )

    summary = " ".join(lines[summary_index + 1 : experience_start]).strip()
    notes = [
        "Le PDF LinkedIn ne fournit pas de photo de profil ; seule une image "
        "PNG/JPG locale de data/ peut être utilisée.",
        "Les compétences reprises sont celles de la section "
        "« Principales compétences » du PDF.",
    ]
    if not email:
        notes.append("Aucune adresse e-mail n'a été trouvée dans le PDF.")
    if not summary:
        notes.append("Aucun résumé n'a été trouvé dans le PDF.")
    notes.append(
        "Les champs absents du PDF, notamment le téléphone et les hobbies, "
        "restent vides."
    )

    return {
        "source_status": "partial",
        "source_type": "linkedin_pdf",
        "source_file": os.path.basename(source_file),
        "source_notes": notes,
        "personal_info": {
            "name": lines[name_index],
            "headline": lines[name_index + 1],
            "email": email,
            "phone": "",
            "location": location,
            "summary": summary,
            "photo": "",
        },
        "experiences": experiences,
        "education": education,
        "skills": _skills(lines, skills_index + 1, name_index),
        "hobbies": [],
    }


def parse_linkedin_pdf(pdf_path: str) -> Dict[str, object]:
    """Extract the supported French LinkedIn profile PDF into the CV schema."""
    try:
        reader = PdfReader(pdf_path)
        if reader.is_encrypted:
            raise LinkedInExportFormatError("Le PDF est chiffré.")
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except (OSError, PdfReadError, ValueError) as error:
        if isinstance(error, LinkedInExportFormatError):
            raise
        raise LinkedInExportFormatError(
            f"Le PDF ne peut pas être lu : {error}"
        ) from error
    return parse_linkedin_text(text, pdf_path)


def _find_pdf(data_dir: str) -> Optional[str]:
    pdf_paths = sorted(
        os.path.join(data_dir, filename)
        for filename in os.listdir(data_dir)
        if filename.lower().endswith(".pdf")
        and os.path.isfile(os.path.join(data_dir, filename))
    )
    if not pdf_paths:
        return None

    preferred = [
        path
        for path in pdf_paths
        if os.path.basename(path).casefold() == "profile.pdf"
    ]
    if len(preferred) == 1:
        return preferred[0]
    if len(pdf_paths) == 1:
        return pdf_paths[0]
    raise ProfileSourceError(
        "Plusieurs PDF sont présents dans data/ sans Profile.pdf unique ; "
        "gardez l'export LinkedIn attendu ou indiquez lequel utiliser."
    )


def find_local_photo_candidates(data_dir: str) -> List[str]:
    """Return supported local photo filenames without reading their contents."""
    return sorted(
        filename
        for filename in os.listdir(data_dir)
        if os.path.splitext(filename)[1].lower() in PHOTO_EXTENSIONS
        and os.path.isfile(os.path.join(data_dir, filename))
    )


def _add_photo_candidates(
    profile: Dict[str, object], data_dir: str
) -> Dict[str, object]:
    candidates = find_local_photo_candidates(data_dir)
    profile["photo_candidates"] = candidates
    notes = profile.get("source_notes")
    if isinstance(notes, list):
        if len(candidates) == 1:
            notes.append(f"Photo locale disponible dans data/ : {candidates[0]}.")
        elif candidates:
            notes.append(
                "Plusieurs photos locales sont disponibles dans data/ ; "
                "demander laquelle utiliser."
            )
        else:
            notes.append("Aucune photo PNG/JPG locale n'est présente dans data/.")
    return profile


def _load_json_fallback(
    data_dir: str, reason: str
) -> Dict[str, object]:
    json_paths = sorted(
        os.path.join(data_dir, filename)
        for filename in os.listdir(data_dir)
        if filename.lower().endswith(".json")
        and os.path.isfile(os.path.join(data_dir, filename))
    )
    preferred = [
        path
        for path in json_paths
        if os.path.basename(path).casefold() == "data.json"
    ]
    if preferred:
        json_path = preferred[0]
    elif len(json_paths) == 1:
        json_path = json_paths[0]
    elif not json_paths:
        raise ProfileSourceError(
            f"{reason} Aucun fichier JSON de profil n'est présent dans data/."
        )
    else:
        raise ProfileSourceError(
            f"{reason} Plusieurs profils JSON sont présents dans data/ ; "
            "indiquez lequel utiliser."
        )

    with open(json_path, encoding="utf-8") as json_file:
        profile = json.load(json_file)
    if not isinstance(profile, dict) or not isinstance(
        profile.get("personal_info"), dict
    ):
        raise ProfileSourceError(
            f"Le fichier {os.path.basename(json_path)} ne contient pas "
            "un profil avec 'personal_info'."
        )

    for category in ("experiences", "education", "skills", "hobbies"):
        if not isinstance(profile.get(category, []), list):
            raise ProfileSourceError(
                f"La catégorie '{category}' du profil JSON doit être une liste."
            )
        profile.setdefault(category, [])

    profile["personal_info"] = dict(profile["personal_info"])
    profile["personal_info"]["photo"] = ""
    profile.pop("generated_date", None)
    profile.update(
        {
            "source_status": "success",
            "source_type": "local_json",
            "source_file": os.path.basename(json_path),
            "source_notes": [reason],
        }
    )
    return profile


def load_profile_source(data_dir: str = DATA) -> Dict[str, object]:
    """Prefer a valid LinkedIn PDF; otherwise load a local JSON profile."""
    pdf_path = _find_pdf(data_dir)
    if pdf_path is None:
        profile = _load_json_fallback(
            data_dir, "Aucun PDF LinkedIn présent dans data/ ; profil JSON utilisé."
        )
    else:
        try:
            profile = parse_linkedin_pdf(pdf_path)
        except LinkedInExportFormatError as error:
            profile = _load_json_fallback(
                data_dir,
                f"{os.path.basename(pdf_path)} ne respecte pas le format "
                f"LinkedIn attendu ({error}) ; profil JSON utilisé.",
            )
    return _add_photo_candidates(profile, data_dir)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importe le PDF LinkedIn local, avec repli sur un profil JSON."
    )
    parser.add_argument(
        "--data-dir",
        default=DATA,
        help="Dossier contenant le PDF LinkedIn ou les profils JSON",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Fichier JSON de profil à générer",
    )
    args = parser.parse_args()

    try:
        profile = load_profile_source(args.data_dir)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as output_file:
            json.dump(profile, output_file, ensure_ascii=False, indent=2)
            output_file.write("\n")
    except (OSError, json.JSONDecodeError, ProfileSourceError) as error:
        parser.error(str(error))

    print(
        f"Profil importé depuis {profile['source_file']} "
        f"({profile['source_type']}) : {os.path.abspath(args.output)}"
    )


if __name__ == "__main__":
    main()
