---
name: pytest-workflow
description: Design and run behavior-focused pytest coverage for changes to CV generation, Jinja templates, JSON inputs, and the CLI.
---

# pytest workflow for CV Generator

Use this skill whenever changing Python behavior, HTML templates, CLI behavior, DOCX export, or the data passed between them.

## Test-first workflow

1. Identify the user-visible contract being changed and inspect existing tests in `tests/test_generator.py`.
2. Add a focused test that fails for the missing or incorrect behavior before implementing the fix when practical.
3. Use `tmp_path` for JSON, templates, and generated HTML. Do not write test outputs into the real `data/` or `outputs/` directories.
4. Assert observable outcomes: output path exists, HTML contains expected visible content, untrusted text is escaped, and unsupported behavior fails clearly. Avoid asserting private implementation details.
5. Cover relevant edge cases, such as a nested output directory, an empty optional field, a custom template, or missing/invalid input when that boundary is changed.
6. Run the focused test while iterating, then run the full project suite after the change:

   ```powershell
   python -m pytest -q .\tests
   ```

7. If pytest is unavailable, check the selected interpreter and install only the dependencies already declared in `requirements.txt`. Do not hide test failures or claim success until the command exits successfully.

## Scenario: custom template must safely render a CV

For a change that adds or modifies custom-template rendering:

1. Create a temporary Jinja template such as `<!doctype html><html><body>{{ personal_info.headline }}</body></html>`.
2. Supply a profile headline containing markup, for example `<script>alert(1)</script>`.
3. Generate to a nested path under `tmp_path`.
4. Assert the output exists, contains the escaped text `&lt;script&gt;...`, and does not contain a raw `<script>` tag.
5. Keep the existing built-in-template tests passing to catch regressions in the four supplied designs.

## Scenario: optional photo in `data/`

When adding or changing photo support, cover both selection and rendering:

1. Verify a lone `.png`, `.jpg`, or `.jpeg` is detected and embedded as a data URI.
2. Verify multiple candidate photos require an explicit selection rather than silently choosing one.
3. Verify unsupported formats are ignored or rejected with a clear error.
4. Verify an HTML output with a photo remains self-contained and still renders without a photo.

Use temporary files for these cases; never add fixture photos to the real `data/` directory.

## Scenario: LinkedIn PDF import and JSON fallback

When modifying `scripts/linkedin_pdf_importer.py`:

1. Use a sanitized LinkedIn-export text fixture to test section validation and mapping; do not make tests depend on an ignored personal PDF under `data/`.
2. Verify extracted experiences, education, skills, empty optional fields, and that profile URLs or photo data are not copied into the CV profile.
3. Exercise the CLI output with a mocked PDF reader and a temporary directory.
4. Verify a missing or invalid PDF selects the documented JSON fallback, stale JSON photo paths are cleared, and ambiguous JSON inputs fail clearly.
5. Test photo discovery using temporary PNG/JPG/JPEG names, including ignored unsupported extensions and multiple-photo cases. Tests must not call Google or other external sites; any researched hobby suggestions are separate and require user confirmation.

Also verify that metadata such as `generated_date` is not emitted when the template does not need it, and that visible CV copy does not acquire automatic signatures or target-role annotations.

## Scenario: export a cover letter to DOCX

When changing `scripts/cover_letter_exporter.py` or its CLI:

1. Use temporary Markdown input and a nested output path under `tmp_path`; never write generated DOCX files into the real `outputs/` directory.
2. Reopen the result with `python-docx` and assert that letter paragraphs, intentional line breaks, and formal-letter formatting (sender, recipient/date alignment, bold subject) are preserved.
3. Verify that empty input fails clearly and creates no output, and that the CLI reports successful generation.
4. Run the focused exporter tests while iterating, then run `python -m pytest -q .\tests`.

## Coverage standard

“Complete coverage” means tests exercise each changed behavior and its meaningful boundary cases, not that every line or trivial accessor has a test. Add parametrized cases when several inputs share one contract. Keep tests deterministic, independent, and fast; never call external websites from unit tests.
