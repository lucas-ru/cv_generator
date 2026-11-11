---
name: cv-playwright-e2e
description: Validate a finalized CV in Chromium against its UX template, including print rendering and PDF pagination.
---

# Playwright end-to-end review for CVs

Apply this skill after every final HTML generation or correction. The test must use the finalized CV, the exact UX template used to generate it, and the matching profile JSON.

## Setup

Install the declared Python dependencies and Chromium once per environment:

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Scenario: final CV review

1. Confirm that `outputs/cv-cible.html`, `.cv-work/cv_template.html`, and `.cv-work/cv_profile.json` exist and belong to the same generation. A skipped test is not a successful review.
2. Run the E2E test from the project root:

   ```powershell
   $env:CV_E2E_HTML = ".\outputs\cv-cible.html"
   $env:CV_E2E_TEMPLATE = ".\.cv-work\cv_template.html"
   $env:CV_E2E_PROFILE = ".\.cv-work\cv_profile.json"
   $env:CV_E2E_EVIDENCE_DIR = ".\.cv-work\playwright-review"
   python -m pytest -q -s .\tests\e2e\test_final_cv_playwright.py
   ```

3. Compare the rendered HTML screenshot and the print-media screenshot to the reference screenshots rendered from the UX template with the same profile.
4. Review the generated PDF preview. Check A4 portrait dimensions, page count, text on every page, visible profile sections, the photo when selected, and the template's branded header and colors. When experience markers are present, verify their measured gap from the title is at least 7 CSS pixels. Print backgrounds are enabled for the PDF test.
5. Treat a visual mismatch, blank page, missing content, broken image, horizontal overflow, failed test, or skipped test as a blocking defect. Correct the source template or generation process, never just the generated output, then rerun the test.
6. Pass the report and evidence paths to `CV Workflow Improver` for an accept/reject decision before the orchestrator presents the CV for user feedback.

The test writes screenshots, the HTML reference, the PDF previews, and a technical report under `.cv-work/playwright-review/`. These files may contain profile information; keep them local and never add them to Git or send them to external services.
