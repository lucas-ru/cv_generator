---
name: cv-print-layout
description: Design and review balanced A4 CV layouts with safe page margins, consistent section rhythm, and a structured photo/contact header.
---

# A4 CV layout and print review

Apply this skill when creating or revising a CV template, especially after user feedback about spacing, page edges, or header hierarchy.

## Layout rules

1. Treat the full A4 page as a constrained content area, not as empty canvas to fill. Keep vertical spacing consistent between summary, experience, education, and sidebar sections.
2. Do not use fixed page height together with `overflow: hidden`; this can clip the last education date or content. Prefer natural document flow and an A4 `min-height` on screen, then remove page-sized minimum heights from `html`, `body`, and the wrapper in print styles. Let genuinely long content continue onto another page rather than clipping or compressing it into the border.
3. Keep the final visible line (including the last education date) comfortably inside the print-safe area through section spacing. Do not add bottom padding outside a page-sized wrapper; it can create an otherwise blank extra page. Inspect the actual print preview or exported PDF.
4. Avoid automatic space distribution such as `margin-top: auto`, `justify-content: space-between`, or stretched grid rows between experience and education. Use deliberate, repeatable section margins instead.
5. Structure the header explicitly:
   - one identity block for the candidate name and one short, grammatically coherent headline;
   - an optional photo aligned in its own column, never inserted between the identity and contact details;
   - a separate contact row below the identity/photo, wrapping cleanly without tiny text or clipping.
6. Make the photo conditional. When absent, collapse its column and leave no empty frame or reserved block. Give a present image a useful alt text, preserve its aspect ratio, and size it modestly.
7. Prefer a small spacing scale and readable typography. Reduce excessive gaps before shrinking body text. Keep the layout legible in grayscale and in browser print output.

## Scenario: education is pushed to the page edge

When a CV has a large gap before education and the final DUT/degree date touches the bottom:

1. Inspect page wrappers for fixed `height`, `overflow: hidden`, and forced grid/flex distribution.
2. Reduce the gap between sections and education-item padding using the same spacing rhythm as the experience list.
3. Create a safe bottom inset through the content spacing, not by adding padding after an A4-sized wrapper. Do not solve the problem by pushing the last date farther down or shrinking it.
4. Re-render the real profile with the chosen photo and inspect the complete A4 page at print size.
5. Verify the header's name/title and contacts form separate, readable groups; verify the photo is either neatly aligned or completely absent.
6. If all content cannot fit legibly on one page, allow a clean second page and explain why rather than clipping content.

## Visual acceptance checklist

- The top-to-bottom hierarchy is clear at normal zoom.
- Experience and education sections have comparable, intentional spacing.
- The final date and all other content sit within a visible bottom margin.
- The header is balanced with and without a photo; contact details do not overlap or bunch together.
- The browser print preview contains every item and does not add accidental blank pages.
- Use a solid high-contrast text fill for names and headings rather than transparent gradient text. Preserve the template's brand backgrounds in print, set print-color adjustment, and enable background graphics during PDF export.
- Compare both screen and print-media output with the selected UX template; do not replace a branded header or section background with white only in print styles.
