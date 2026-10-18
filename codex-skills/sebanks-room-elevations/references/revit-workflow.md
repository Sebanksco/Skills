# Revit MCP implementation notes

These describe the Revit 2026 bridge used for the original workflow. Discover current tool schemas/capabilities before acting; do not assume the same identifiers or functionality in another model/session.

## Preserve the distinction between drafting and modeling

The initial Abilene elevations were drafted with detail lines and text notes in section views away from the CAD imports. They are not automatically generated from modeled walls, and their drafted dimension strings are not associative Revit Dimensions. Inspect the current document before choosing the appropriate technique; use actual model-derived elevations when geometry is available and appropriate.

## Coordinate and text handling

- A section looking along model negative Y had view-right in model negative X. Confirm view orientation before drawing or moving content; do not transpose east/west based on screen assumptions.
- `create_section_view` width/height represented half extents in this bridge.
- Text note wrap width was in **paper feet**, while detail geometry was in model feet. For a desired model-space wrap width W at scale S, pass W/S paper feet.
- Text type `Text Size` was written in raw internal feet using `units: internal`. Approved heading height 9/32 paper inch equals **0.0234375 internal feet**. Numeric bridge unit conversion for this parameter previously failed when using `feet`.
- Duplicate a text type before changing size/color if other notes share it. Copying a TextNoteType via `copy_element` worked; a FamilySymbol-only duplication tool did not.
- In this bridge's packed integer color parameter: blue RGB(0,0,255) = **16711680**; red RGB(255,0,0) = **255**. Confirm by rendering, not only by write success.

## Remove extraneous boxes and lines

- Crop visibility is separate from crop activation. Set `Crop Region Visible` off even when `Crop View` is off; otherwise crop boxes can still appear on screen.
- Long crossing horizontal lines can be viewport title extensions. Duplicate the viewport type, disable `Show Extension Line` and, where redundant, `Show Title`; assign only the intended viewports. Do not globally change unrelated sheets' viewport types.
- Do not erase actual wall/cabinet geometry to fix a viewport or crop display issue.

## Verify changes and preserve work

- Group related operations in a supported batch transaction when possible. Check every operation's result and render the affected elevation and sheet afterward.
- Verify that moving viewports actually changed the sheet even when an element-location comparison is unsupported by the API.
- The original bridge did not expose RVT save or PDF export. Recheck current capabilities. Never claim a save, final PDF, paper size, or print margins solely from a successful image export.
- A later bridge exposes `export_view_pdf`; verify returned files, page count, dimensions, colors, text and rendered pages before claiming PDF completion. A composed fit-to-page review set must be labeled accordingly; its view scale is not a verified printed scale.
- Moving individual joined detail lines can stretch adjoining lines or open a blocking `Can't keep elements joined` failure dialog. Cancel the rejected transaction, inspect the actual state, and rebuild the affected drafted panel when necessary. Do not keep retrying the same move or assume a timed-out batch rolled back.
- Revit modal dialogs can block bridge commands. Resolve visible dialogs before repeated retries; avoid unsupported arbitrary-script workarounds.
