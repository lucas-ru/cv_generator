---
name: cv-template-fallback
description: Select and adapt an existing CV template when company brand research is missing or inconclusive.
---

# Fallback design using project templates

Apply this skill whenever `.cv-work/company_brand.json` has no reliable visual evidence, no usable sources, or explicitly reports missing/inconclusive research.

## Workflow

1. Read the job title, sector, seniority, offer language, and target audience from `.cv-work/offer_brief.json`.
2. Inspect the four templates in `templates/`. Start from the closest usable existing design; do not invent a new visual identity or choose arbitrary corporate colors.
3. Use these starting points:
   - `cv_template_1.html`: balanced, contemporary general-purpose layout.
   - `cv_template_2.html`: Swiss, minimal, high-contrast style for engineering, technology, or product roles.
   - `cv_template_3.html`: polished corporate style for enterprise, consulting, operations, or finance roles.
   - `cv_template_4.html`: editorial, asymmetric style for creative, communications, or leadership roles.
4. When no reliable company design is found, first discard any template that cannot satisfy the content, accessibility, photo, or print-layout requirements without a major redesign. From the remaining templates, choose the lowest preference weight in the table below. A lower number means the user prefers that template more. Use role fit only as a tie-breaker; do not override the user's ranking merely because a different template seems more conventional for the sector.
5. Preserve the selected template's visual system. Make only restrained adjustments needed for readability, content completeness, and the offer's language. If necessary, fix clipping or responsive defects while preserving the chosen design.
6. If no role or brand evidence distinguishes equally ranked choices, use the lower-weight template.
7. Clearly report in `.cv-work/company_brand.json` or the handoff summary that this is a template-based fallback, not researched company branding, and record the selected template and its weight.

## Template preference weights

These are user preference scores, not brand evidence. The larger the weight, the less preferred the design:

| Template | Weight |
| --- | ---: |
| `cv_template_1.html` | 1 |
| `cv_template_2.html` | 8 |
| `cv_template_3.html` | 3 |
| `cv_template_4.html` | 7 |

With these defaults, template 1 is selected when it meets the requirements. If the user changes their preferences, update only this table and the README's matching table; keep the ascending-weight selection rule.

## Scenario: no company website or brand assets found

For an unavailable employer site and a Tech Lead Dev offer:

1. Do not invent a logo, brand palette, or company visual identity.
2. Among templates that can present the complete profile in a readable, print-safe layout, choose the one with the lowest weight. With the defaults above, use template 1.
3. Carry the chosen template's existing typography, spacing, and palette into `.cv-work/cv_template.html`; do not present its palette as the employer's brand.
4. Preserve every non-empty profile category, including skills and hobbies. Keep an optional profile photo conditional so the layout has no empty photo slot when none is provided.
