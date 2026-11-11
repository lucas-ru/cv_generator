import base64
import importlib.util
import json
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(__file__))
TEMPLATES = os.path.join(ROOT, "templates")

spec = importlib.util.spec_from_file_location(
    "cv_generator", os.path.join(ROOT, "scripts", "cv_generator.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
Generator = mod.CVGenerator


def sample_profile():
    return {
        "personal_info": {
            "name": "Test User",
            "headline": "Engineer",
            "location": "Nowhere",
        },
        "experiences": [],
        "education": [],
        "skills": [],
        "hobbies": [],
    }


def test_all_builtin_templates_render_profile(tmp_path):
    generator = Generator(template_dir=TEMPLATES)

    for choice in ("1", "2", "3", "4"):
        output_path = tmp_path / f"cv_{choice}.html"
        generator.generate_cv(choice, sample_profile(), str(output_path))

        html = output_path.read_text(encoding="utf-8")
        assert "<html" in html.lower()
        assert "Test User" in html
        assert "<img" not in html.lower()


def test_cli_generates_cv_from_json(tmp_path):
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(
        json.dumps(sample_profile(), ensure_ascii=False),
        encoding="utf-8",
    )
    output_path = tmp_path / "nested" / "cv.html"

    result = subprocess.run(
        [
            sys.executable,
            os.path.join(ROOT, "scripts", "cv_generator.py"),
            "--data",
            str(profile_path),
            "--template",
            "1",
            "--output",
            str(output_path),
        ],
        capture_output=True,
        check=True,
        text=True,
    )

    assert output_path.is_file()
    assert "CV HTML généré" in result.stdout
    assert "Test User" in output_path.read_text(encoding="utf-8")


def test_custom_template_escapes_content_and_omits_generation_date(tmp_path):
    generator = Generator(template_dir=TEMPLATES)
    profile = sample_profile()
    profile["personal_info"]["headline"] = "<script>alert(1)</script>"
    profile["generated_date"] = "11/11/2026"
    template_path = tmp_path / "custom.html"
    template_path.write_text(
        "<!doctype html><html><body>{{ personal_info.headline }} "
        "{{ generated_date }}</body></html>",
        encoding="utf-8",
    )
    output_path = tmp_path / "nested" / "cv.html"

    generator.generate_cv(
        "1",
        profile,
        str(output_path),
        template_path=str(template_path),
    )

    html = output_path.read_text(encoding="utf-8")
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<script>" not in html
    assert "11/11/2026" not in html


def test_cli_embeds_selected_photo_in_html(tmp_path):
    profile_path = tmp_path / "profile.json"
    profile_path.write_text(
        json.dumps(sample_profile(), ensure_ascii=False),
        encoding="utf-8",
    )
    photo_path = tmp_path / "portrait.jpg"
    photo_bytes = b"test jpeg bytes"
    photo_path.write_bytes(photo_bytes)
    output_path = tmp_path / "cv.html"

    subprocess.run(
        [
            sys.executable,
            os.path.join(ROOT, "scripts", "cv_generator.py"),
            "--data",
            str(profile_path),
            "--photo",
            str(photo_path),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        check=True,
        text=True,
    )

    html = output_path.read_text(encoding="utf-8")
    expected_uri = (
        "data:image/jpeg;base64,"
        + base64.b64encode(photo_bytes).decode("ascii")
    )
    assert expected_uri in html


def test_photo_discovery_requires_explicit_choice_if_ambiguous(tmp_path):
    (tmp_path / "portrait.png").write_bytes(b"png")
    (tmp_path / "portrait.jpg").write_bytes(b"jpg")
    (tmp_path / "ignore.webp").write_bytes(b"webp")

    with pytest.raises(ValueError, match="(?i)plusieurs photos"):
        mod.find_single_photo(str(tmp_path))


def test_photo_discovery_ignores_unsupported_formats(tmp_path):
    photo_path = tmp_path / "portrait.PNG"
    photo_path.write_bytes(b"png")
    (tmp_path / "ignore.webp").write_bytes(b"webp")

    assert mod.find_single_photo(str(tmp_path)) == str(photo_path)


def test_photo_is_rendered_in_output(tmp_path):
    generator = Generator(template_dir=TEMPLATES)
    profile = sample_profile()
    image_path = tmp_path / "avatar.png"
    image_path.write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00"
        b"\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x02\x00\x01E\x1d\x1b\x1b"
        b"\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    profile["personal_info"]["photo"] = image_path.name
    output_path = tmp_path / "cv.html"

    generator.generate_cv("1", profile, str(output_path))

    html = output_path.read_text(encoding="utf-8")
    assert "<img" in html.lower()
    assert image_path.name in html


def test_corporate_template_has_safe_print_spacing_and_header(tmp_path):
    template_path = os.path.join(TEMPLATES, "cv_template_3.html")
    with open(template_path, encoding="utf-8") as template_file:
        template_source = template_file.read()

    page_css = re.search(r"\.page\s*\{([^}]+)\}", template_source).group(1)
    assert re.search(r"\bmin-height\s*:\s*297mm", page_css)
    assert not re.search(r"(?m)^\s*height\s*:", page_css)
    assert not re.search(r"(?m)^\s*overflow\s*:\s*hidden", page_css)

    section_css = re.search(r"\.section\s*\{([^}]+)\}", template_source).group(1)
    section_gap = re.search(r"margin-bottom\s*:\s*(\d+(?:\.\d+)?)mm", section_css)
    assert float(section_gap.group(1)) <= 5

    profile = sample_profile()
    profile["personal_info"]["photo"] = "data:image/png;base64,dGVzdA=="
    output_path = tmp_path / "cv.html"
    Generator(template_dir=TEMPLATES).generate_cv(
        "3", profile, str(output_path)
    )
    html = output_path.read_text(encoding="utf-8")
    header = html[html.index("<header"):html.index("</header>")]
    assert "header-identity" in html
    assert "header-content--with-photo" in html
    assert '<address class="contact-bar">' in header
    assert header.index("header-identity") < header.index("photo-container")
    assert header.index("photo-container") < header.index('class="contact-bar"')


def test_template_one_keeps_all_profile_categories_and_safe_page_flow(tmp_path):
    template_path = os.path.join(TEMPLATES, "cv_template_1.html")
    with open(template_path, encoding="utf-8") as template_file:
        template_source = template_file.read()

    page_css = re.search(r"\.page-wrapper\s*\{([^}]+)\}", template_source).group(1)
    assert re.search(r"\bmin-height\s*:\s*297mm", page_css)
    assert not re.search(r"(?m)^\s*height\s*:", page_css)
    assert not re.search(r"(?m)^\s*overflow\s*:\s*hidden", page_css)
    assert "fonts.googleapis.com" not in template_source
    print_css = re.search(
        r"@media print\s*\{([\s\S]*?)\n        \}", template_source
    ).group(1)
    assert re.search(r"\.page-wrapper\s*\{[^}]*min-height\s*:\s*0", print_css)
    assert "padding: 0 0 8mm" not in print_css
    assert re.search(
        r"\.name\s*\{[^}]*-webkit-text-fill-color:\s*white",
        print_css,
    )
    assert not re.search(
        r"\.header\s*\{[^}]*background:\s*white",
        print_css,
    )

    profile = sample_profile()
    profile["experiences"] = [
        {
            "title": "Developer",
            "company": "Example",
            "location": "France",
            "start_date": "2022",
            "end_date": "2023",
            "is_current": False,
            "description": "",
        }
    ]
    profile["education"] = [
        {
            "school": "Example School",
            "degree": "Degree",
            "field": "IT",
            "start_date": "2020",
            "end_date": "2022",
            "description": "",
        }
    ]
    profile["skills"] = [{"name": "Python", "endorsements": 0}]
    profile["hobbies"] = ["Lecture", "Sport"]
    output_path = tmp_path / "cv.html"

    Generator(template_dir=TEMPLATES).generate_cv("1", profile, str(output_path))

    html = output_path.read_text(encoding="utf-8")
    for category in ("Expérience", "Formation", "Compétences", "Hobbies"):
        assert category in html
    assert "Lecture" in html
    assert "Sport" in html
