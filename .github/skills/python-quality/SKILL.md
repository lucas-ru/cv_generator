---
name: python-quality
description: Apply Python maintainability, PEP 8, type-safety, and error-handling practices when changing the CV generator or its CLI.
---

# Python quality for CV Generator

Use this skill before changing either Python script in this repository: `scripts/cv_generator.py` or `scripts/linkedin_pdf_importer.py`.

## Workflow

1. Read the affected function, its callers, the relevant template, and related tests before editing.
2. Follow the repository's existing patterns and Python 3.9+ compatibility. Use four-space indentation, descriptive `snake_case` names, small cohesive functions, and explicit types where they clarify contracts.
3. Keep the change focused. Prefer the standard library and existing Jinja2 helpers; do not add dependencies or abstractions for a one-off need.
4. Validate external inputs at their boundary. Raise or report actionable errors; do not swallow exceptions or silently substitute invalid data.
5. Use context managers for files, UTF-8 for JSON/HTML, and Jinja autoescaping for HTML data. Never mark user-supplied values safe just to bypass escaping.
6. Preserve existing CLI behavior unless the task explicitly changes it. Avoid premature optimization; optimize only a demonstrated bottleneck without reducing readability.
7. Run the tests relevant to the changed behavior and the project suite when Python behavior changes.

## Scenario: add a custom HTML template option

When asked to let the generator render a designer-created template:

1. Inspect `CVGenerator.generate_cv`, CLI argument parsing in `main`, and tests that render built-in templates.
2. Add the smallest typed parameter/CLI option that accepts a template path while retaining the existing built-in template selector.
3. Load the template with the existing Jinja2 environment conventions and HTML autoescaping. Keep paths and output handling explicit; create the output directory only as needed.
4. Add or update a pytest case using a temporary template and a nested temporary output path. Verify rendered output and that profile text is escaped.
5. Run `python -m pytest -q .\tests` from the project root and report the result.

## Scenario: import a LinkedIn profile PDF

When modifying `scripts/linkedin_pdf_importer.py`:

1. Validate the selected local PDF's export headings and order before extracting fields. Never access LinkedIn online or use a profile URL.
2. Keep extraction deterministic and source-bound: map only visible PDF facts; do not infer missing hobbies, contacts, skills, or experience. If the PDF is absent or invalid, use the documented local JSON fallback and report which file was selected.
3. Keep profile photos separate from PDF parsing. Enumerate only PNG/JPG/JPEG candidates in `data/`; never extract embedded images or preserve stale photo paths from fallback JSON.
4. Make ambiguous PDF/JSON/photo choices explicit rather than silently selecting a different profile or image.
5. Keep the importer CLI focused, use UTF-8 for JSON, surface unreadable input errors, and avoid logging profile content or personal information.

## Completion checklist

- The change matches PEP 8 and nearby code style.
- New inputs have clear validation and failures remain visible.
- No facts or user data are hard-coded into production code.
- Existing template and CLI behavior is preserved unless intentionally changed.
- Tests cover the behavior changed, not implementation details.
