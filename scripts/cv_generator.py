"""Génération de CV HTML à partir d'un profil JSON."""

import argparse
import base64
import json
import os
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")
OUTPUTS = os.path.join(ROOT, "outputs")
DATA = os.path.join(ROOT, "data")
PHOTO_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
}


def find_single_photo(data_dir: str = DATA) -> Optional[str]:
    """Return the only supported image in the data directory, if there is one."""
    photo_paths = sorted(
        os.path.join(data_dir, filename)
        for filename in os.listdir(data_dir)
        if os.path.splitext(filename)[1].lower() in PHOTO_MIME_TYPES
        and os.path.isfile(os.path.join(data_dir, filename))
    )
    if len(photo_paths) > 1:
        raise ValueError(
            "Plusieurs photos PNG/JPG sont présentes dans data/. "
            "Choisissez-en une avec --photo."
        )
    return photo_paths[0] if photo_paths else None


def image_to_data_uri(photo_path: str) -> str:
    """Embed a PNG or JPEG as a data URI so the generated HTML is portable."""
    extension = os.path.splitext(photo_path)[1].lower()
    mime_type = PHOTO_MIME_TYPES.get(extension)
    if not mime_type:
        raise ValueError("La photo doit être au format PNG, JPG ou JPEG.")

    with open(photo_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded_image}"


class CVGenerator:
    """Génère un CV HTML à partir de données structurées."""

    def __init__(self, template_dir: str = TEMPLATES) -> None:
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(("html", "xml")),
        )

    def generate_cv(
        self,
        choix: str,
        data: Dict[str, Any],
        output_path: str = "cv.html",
        template_path: Optional[str] = None,
    ) -> str:
        """Rend le profil dans un template intégré ou un template HTML personnalisé."""
        if template_path:
            template_dir = os.path.dirname(os.path.abspath(template_path))
            template_name = os.path.basename(template_path)
            environment = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=select_autoescape(("html", "xml")),
            )
            template = environment.get_template(template_name)
        else:
            template = self.env.get_template(f"cv_template_{choix}.html")

        template_data = dict(data)
        template_data.pop("generated_date", None)
        html_content = template.render(**template_data)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

        return output_path


def main() -> None:
    """Charge le profil JSON préparé par les agents et génère le CV HTML."""
    parser = argparse.ArgumentParser(
        description="Génère un CV HTML depuis un profil JSON."
    )
    parser.add_argument(
        "--data",
        required=True,
        help="Fichier JSON du profil adapté par les agents",
    )
    parser.add_argument(
        "--template",
        choices=("1", "2", "3", "4"),
        default="1",
        help="Template intégré à utiliser",
    )
    parser.add_argument(
        "--template-file",
        help="Template HTML personnalisé créé par l'agent UX",
    )
    parser.add_argument(
        "--photo",
        help="Photo PNG/JPG à intégrer (par défaut, l'unique photo trouvée dans data/)",
    )
    parser.add_argument(
        "--output",
        default=os.path.join(OUTPUTS, "cv.html"),
        help="Chemin du fichier HTML à générer",
    )
    args = parser.parse_args()

    with open(args.data, encoding="utf-8") as json_file:
        data = json.load(json_file)
    if not isinstance(data, dict) or not isinstance(data.get("personal_info"), dict):
        parser.error("Le JSON doit contenir un objet 'personal_info'.")

    try:
        photo_path = args.photo or find_single_photo()
        if photo_path:
            data["personal_info"]["photo"] = image_to_data_uri(photo_path)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    generator = CVGenerator()
    output_file = generator.generate_cv(
        args.template,
        data,
        args.output,
        template_path=args.template_file,
    )
    print(f"CV HTML généré : {os.path.abspath(output_file)}")


if __name__ == "__main__":
    main()
