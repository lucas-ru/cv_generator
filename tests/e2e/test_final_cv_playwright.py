"""Playwright checks for the finalized CV and its source template."""

import copy
import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional

import pytest
from pypdf import PdfReader
from playwright.sync_api import Page, Route, sync_playwright

from scripts.cv_generator import CVGenerator


ROOT = Path(__file__).resolve().parents[2]
HTML_PATH = Path(os.environ.get("CV_E2E_HTML", ROOT / "outputs" / "cv-cible.html"))
TEMPLATE_PATH = Path(
    os.environ.get("CV_E2E_TEMPLATE", ROOT / ".cv-work" / "cv_template.html")
)
PROFILE_PATH = Path(
    os.environ.get("CV_E2E_PROFILE", ROOT / ".cv-work" / "cv_profile.json")
)
EVIDENCE_PATH = Path(
    os.environ.get("CV_E2E_EVIDENCE_DIR", ROOT / ".cv-work" / "playwright-review")
).resolve()
A4_WIDTH_PT = 595.28
A4_HEIGHT_PT = 841.89


class _ImageSourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, Optional[str]]]
    ) -> None:
        if tag == "img":
            self.images.append({key: value or "" for key, value in attrs})


def _normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _photo_data_uri(html: str) -> str:
    parser = _ImageSourceParser()
    parser.feed(html)
    image_sources = [
        image.get("src", "")
        for image in parser.images
        if image.get("src", "").startswith("data:image/")
    ]
    for image in parser.images:
        alt = image.get("alt", "").casefold()
        source = image.get("src", "")
        if source.startswith("data:image/") and (
            "photo" in alt or "portrait" in alt
        ):
            return source
    return image_sources[0] if image_sources else ""


def _finalized_paths() -> tuple[Path, Path, Path]:
    return HTML_PATH.resolve(), TEMPLATE_PATH.resolve(), PROFILE_PATH.resolve()


def _block_external_resources(route: Route) -> None:
    if route.request.url.startswith(("http://", "https://")):
        route.abort()
    else:
        route.continue_()


def _capture_page(page: Page, html_path: Path, screenshot_path: Path) -> dict:
    page.goto(html_path.as_uri(), wait_until="load")
    page.add_style_tag(
        content=(
            "*, *::before, *::after { animation: none !important; "
            "transition: none !important; caret-color: transparent !important; }"
        )
    )
    page.evaluate("() => document.fonts.ready.then(() => true)")
    page.wait_for_function(
        "() => Array.from(document.images).every((image) => image.complete)"
    )
    screen_result = page.evaluate(
        """() => {
            const root = document.documentElement;
            const header = document.querySelector('header, .header');
            const headerStyle = header ? getComputedStyle(header) : null;
            const experience = document.querySelector('.experience-item');
            const experienceTitle = experience
                ? experience.querySelector('.item-title, h3')
                : null;
            const markerStyle = experience
                ? getComputedStyle(experience, '::before')
                : null;
            const experienceMarkerGap = experienceTitle && markerStyle
                && markerStyle.content !== 'none'
                ? experienceTitle.getBoundingClientRect().left
                    - experience.getBoundingClientRect().left
                    - parseFloat(markerStyle.left)
                    - parseFloat(markerStyle.width)
                : null;
            return {
                text: document.body.innerText,
                horizontalOverflow: root.scrollWidth > root.clientWidth + 1,
                images: Array.from(document.images).map((image) => ({
                    complete: image.complete,
                    width: image.naturalWidth,
                })),
                header: headerStyle ? {
                    backgroundColor: headerStyle.backgroundColor,
                    backgroundImage: headerStyle.backgroundImage,
                    color: headerStyle.color,
                } : null,
                experienceMarkerGap,
            };
        }"""
    )
    page.screenshot(path=str(screenshot_path), full_page=True, animations="disabled")
    return screen_result


def _capture_print(
    page: Page, html_path: Path, screenshot_path: Path, pdf_path: Path
) -> dict:
    page.goto(html_path.as_uri(), wait_until="load")
    page.add_style_tag(
        content=(
            "*, *::before, *::after { animation: none !important; "
            "transition: none !important; caret-color: transparent !important; }"
        )
    )
    page.evaluate("() => document.fonts.ready.then(() => true)")
    page.wait_for_function(
        "() => Array.from(document.images).every((image) => image.complete)"
    )
    page.emulate_media(media="print")
    page.set_viewport_size({"width": 794, "height": 1123})
    result = page.evaluate(
        """() => {
            const root = document.documentElement;
            const header = document.querySelector('header, .header');
            const headerStyle = header ? getComputedStyle(header) : null;
            const experience = document.querySelector('.experience-item');
            const experienceTitle = experience
                ? experience.querySelector('.item-title, h3')
                : null;
            const markerStyle = experience
                ? getComputedStyle(experience, '::before')
                : null;
            const experienceMarkerGap = experienceTitle && markerStyle
                && markerStyle.content !== 'none'
                ? experienceTitle.getBoundingClientRect().left
                    - experience.getBoundingClientRect().left
                    - parseFloat(markerStyle.left)
                    - parseFloat(markerStyle.width)
                : null;
            return {
                horizontalOverflow: root.scrollWidth > root.clientWidth + 1,
                header: headerStyle ? {
                    backgroundColor: headerStyle.backgroundColor,
                    backgroundImage: headerStyle.backgroundImage,
                    color: headerStyle.color,
                } : null,
                experienceMarkerGap,
            };
        }"""
    )
    page.screenshot(path=str(screenshot_path), full_page=True, animations="disabled")
    page.pdf(
        path=str(pdf_path),
        format="A4",
        print_background=True,
        prefer_css_page_size=True,
    )
    return result


def _pdf_pages(pdf_path: Path) -> tuple[list[str], list[tuple[float, float]]]:
    reader = PdfReader(str(pdf_path))
    texts = [
        _normalized_text(page.extract_text() or "")
        for page in reader.pages
    ]
    sizes = [
        (float(page.mediabox.width), float(page.mediabox.height))
        for page in reader.pages
    ]
    return texts, sizes


def _profile_facts(profile: dict) -> list[str]:
    personal_info = profile.get("personal_info", {})
    facts = [personal_info.get("name", "")]
    for collection, keys in (
        ("experiences", ("title",)),
        ("education", ("school", "degree")),
        ("skills", ("name",)),
        ("hobbies", ()),
    ):
        entries = profile.get(collection, [])
        if not isinstance(entries, list) or not entries:
            continue
        first = entries[0]
        if isinstance(first, str):
            facts.append(first)
        else:
            facts.extend(first.get(key, "") for key in keys)
    return [fact for fact in facts if fact]


def test_final_cv_html_and_pdf_match_template(tmp_path):
    html_path, template_path, profile_path = _finalized_paths()
    missing = [
        str(path)
        for path in (html_path, template_path, profile_path)
        if not path.is_file()
    ]
    if missing:
        pytest.skip(
            "Finalized CV E2E requires generated HTML, UX template, and profile: "
            + ", ".join(missing)
        )

    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile = copy.deepcopy(profile)
    profile.setdefault("personal_info", {})["photo"] = _photo_data_uri(
        html_path.read_text(encoding="utf-8")
    )
    reference_html = EVIDENCE_PATH / "template-reference.html"
    EVIDENCE_PATH.mkdir(parents=True, exist_ok=True)
    CVGenerator(template_dir=str(template_path.parent)).generate_cv(
        "1",
        profile,
        str(reference_html),
        template_path=str(template_path),
    )

    final_screen = EVIDENCE_PATH / "cv-html.png"
    template_screen = EVIDENCE_PATH / "template-html.png"
    final_print = EVIDENCE_PATH / "cv-print.png"
    template_print = EVIDENCE_PATH / "template-print.png"
    final_pdf = EVIDENCE_PATH / "cv-preview.pdf"
    template_pdf = EVIDENCE_PATH / "template-preview.pdf"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1200, "height": 1200})
        context.route("**/*", _block_external_resources)
        page = context.new_page()
        final_screen_result = _capture_page(page, html_path, final_screen)
        template_screen_result = _capture_page(page, reference_html, template_screen)
        assert not final_screen_result["horizontalOverflow"]
        assert all(
            image["complete"] and image["width"] > 0
            for image in final_screen_result["images"]
        )
        assert final_screen_result["header"] == template_screen_result["header"]
        assert final_screen.read_bytes() == template_screen.read_bytes(), (
            "Rendered HTML differs visually from the selected UX template; "
            "compare cv-html.png with template-html.png."
        )

        page.set_viewport_size({"width": 794, "height": 1123})
        final_print_result = _capture_print(
            page, html_path, final_print, final_pdf
        )
        template_print_result = _capture_print(
            page, reference_html, template_print, template_pdf
        )
        assert not final_print_result["horizontalOverflow"]
        marker_gap = final_print_result["experienceMarkerGap"]
        if marker_gap is not None:
            assert marker_gap >= 7, (
                "The experience marker is too close to its title; "
                "leave a visible gap of at least 7 CSS pixels."
            )
        assert final_print_result["header"] == template_print_result["header"]
        assert final_print.read_bytes() == template_print.read_bytes(), (
            "Print rendering differs visually from the selected UX template; "
            "compare cv-print.png with template-print.png."
        )
        context.close()
        browser.close()

    final_texts, final_sizes = _pdf_pages(final_pdf)
    template_texts, _ = _pdf_pages(template_pdf)
    assert final_texts, "The PDF export contains no pages."
    assert all(final_texts), "The PDF export contains a blank page."
    assert final_texts == template_texts, (
        "PDF pagination or extracted content differs from the selected template."
    )
    for width, height in final_sizes:
        assert width == pytest.approx(A4_WIDTH_PT, abs=1.5)
        assert height == pytest.approx(A4_HEIGHT_PT, abs=1.5)

    pdf_text = " ".join(final_texts)
    for fact in _profile_facts(profile):
        assert _normalized_text(fact) in pdf_text

    report = {
        "status": "passed",
        "html_path": str(html_path),
        "template_path": str(template_path),
        "pdf_pages": len(final_texts),
        "blank_pages": 0,
        "template_visual_match": True,
        "experience_marker_gap_px": marker_gap,
        "html_screenshot": str(final_screen),
        "template_screenshot": str(template_screen),
        "print_screenshot": str(final_print),
        "template_print_screenshot": str(template_print),
        "pdf_preview": str(final_pdf),
    }
    (EVIDENCE_PATH / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
