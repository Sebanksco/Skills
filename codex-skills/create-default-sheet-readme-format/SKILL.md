---
name: create-default-sheet-readme-format
description: Format a Google Sheets README, READMe, Read Me, or instructions tab as a centered gray reading panel with white side padding, black text, wrapped content, fitted rows, and a black outer border. Use when Codex needs to create, clean up, or standardize a spreadsheet documentation tab without changing workbook data.
---

# Create Default Sheet Read ME Format

Use this skill to format a Google Sheets documentation tab as a centered, readable panel.

## Workflow

1. Confirm the exact spreadsheet and README-like tab name.
2. Read spreadsheet metadata and the current README range before editing.
3. Preserve the README text. If the text is in column A, move it to column B.
4. Format only the README tab unless the user explicitly asks for more.
5. Verify the result with a targeted readback of values and cell formatting.

## Default Layout

- Column A is white left padding.
- Column B is the gray content panel.
- Column C is white right padding.
- Text lives only in column B.
- Side columns stay empty and white.
- Hide gridlines when possible.
- Do not use alternating row colors.
- Do not color entire rows across the sheet.

## Panel Style

Apply this style to the content column:

- Light gray background.
- Black text.
- Wrapped text.
- Top vertical alignment.
- Left horizontal alignment.
- Padding around text:
  - top: 6
  - bottom: 6
  - left: 12
  - right: 12
- Black outer border around the gray content panel.
- No inner horizontal borders unless the user explicitly requests them.

## Sizing

Use a document-like layout:

- Left padding column: about 100-140 px.
- Content column: about 600-700 px.
- Right padding column: about 100-140 px.
- Auto-resize rows to fit wrapped text after formatting.

## Safety

- Do not change formulas, dropdowns, task tables, workbook data, or other tabs.
- Do not add unrelated headings, notes, metrics, or extra rows.
- Keep side columns white even if previous formatting used gray, striping, or borders.
- If the README already uses columns A-C for a different intentional layout, ask before moving content.

## Finished Rule

The finished README should look like a centered document panel: white sides, gray middle, black text, black outer border, wrapped text, and row heights fitted to the content.
