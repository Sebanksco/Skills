---
name: sebanks-revit-drafting
description: "Create and revise SEBANKS Revit power and data plan drafting using the saved outlet symbols, line weights, text sizes, source colors, and verified save workflow."
---

# SEBANKS Revit Drafting

Use for editable Revit plan annotations and electrical/data coordination drawings. This is a drafting standard, not electrical engineering approval or permission to change circuits. Later explicit user instructions govern. For interior elevation sheets, also use the existing `sebanks-room-elevations` skill when available.

## Establish the drawing

- Inspect the active document, path, view, view scale, current geometry, and existing symbols before editing. The architectural CAD controls walls, openings, and dimensions; match rooms by position/function as well as number across source revisions.
- Treat north, south, east, and west as **plan directions** unless the user explicitly says otherwise.
- Distinguish native modeled elements from drafted detail groups. A 2D symbol is not a hosted MEP device. Never claim model-derived elevations, associative dimensions, circuits, or a verified installation from detail linework alone.
- Read [references/power-data-standard.md](references/power-data-standard.md) for the approved line, text, symbol, and color settings. Preserve user-adjusted locations and source/type distinctions.

## Revise and verify

- Use the connected Revit tools when available. Recheck tool schemas and group members; do not reuse remembered element IDs from another session or document.
- Group each glyph for single-click movement and rotation. Its legs terminate at the intended room/hall wall face. Keep data triangles distinct from power symbols and orient them deliberately.
- If only thickness/color changes, preserve symbol position, rotation, and duplex/quad type. When a joined detail edit fails, inspect the state and rebuild only the affected glyph; do not repeatedly move joined lines through a failure dialog.
- Inspect a rendered view and the affected area after changes. Keep notes, dimension strings, and symbol geometry clear of fixtures and adjoining rooms. Selection axes and temporary dimensions disappear on deselection; they are not necessarily persistent drawing vectors.
- Preserve the source of requested additions and relocations. Do not invent circuit assignments or infer that a protection rule requires an extra number of receptacles. Check applicable primary code sources if asked for code guidance.

## Save and export

- Save the RVT and verify the document reports no unsaved modifications before claiming it is saved or uploading it. Synchronize the authorized SharePoint copy only after the local save is confirmed.
- A modal dialog or active command can block the connector. Inspect the UI before retrying. For an authorization failure after restart, check for competing Revit instances; preserve and save their work before consolidating sessions. Do not disable authentication.
- Export only the requested views/sheets. Verify PDF existence, page count, paper size, visible colors, line weights, and clipping; a view image alone does not verify a PDF or print scale. Revit line-weight indices map through the project's line-weight table and do not establish a universal millimeter thickness.
- Keep project-specific files, room mappings, element IDs, and pending coordination in the project workspace. Publish reusable instructions without private project paths, credentials, or client records.
