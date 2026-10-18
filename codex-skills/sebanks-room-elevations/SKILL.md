---
name: sebanks-room-elevations
description: Create and revise SEBANKS room interior elevations in Revit from CAD, furniture, and electrical plans, using the agreed sheet layout, device dimensions, casework details, and source reconciliation rules.
---

# SEBANKS Room Elevations

Use this skill for room elevation production and revisions. SEBANKS is spelled S-E-B-A-N-K-S. These are Clinton Baird's agreed drawing conventions; later explicit project instructions override them.

For Abilene, read [references/abilene-decisions.md](references/abilene-decisions.md). For Revit MCP work, read [references/revit-workflow.md](references/revit-workflow.md). Project decisions are not universal cabinet dimensions or electrical design requirements.

## Establish the source basis

- Inspect the actual CAD/PDF/model and current view before editing. Do not reconstruct geometry, circuit assignments, cabinet sizes, or mounting heights from chat recollection alone.
- Identify the current floor plan, furniture electrical plan, original power plan, relevant elevations, and approved shop details. Record sheet/detail identifiers and revisions used.
- Match rooms by location and function as well as number. Maintain a room-number crosswalk where furniture and architectural/CAD labels differ; never transfer requirements solely because two sheets share a room number.
- Current approved geometry governs walls, doors, and corners. Preserve original circuit intent when the floor plan changes, while relocating boxes to the current layout. Do not reuse obsolete box offsets or invent new circuit assignments.
- Apply explicit user corrections to the affected feature, recording their scope. Do not globally rescale a drawing to correct one opening.
- Unresolved information stays visibly marked for coordination. A schematic fixture outline or unresolved circuit mapping must not be presented as a completed construction detail.

## Sheet and linework standards

- Keep all directions for one room on one sheet. Use compact, balanced spacing; keep notes and plan keys clear of adjacent elevations. Check actual paper size, margins, and PDF settings before claiming single-page print readiness.
- Header: `Room [number] Elevations`, top left, bold Arial, blue, **9/32 inch paper text height**. This is the final approved style, replacing the earlier smaller black heading. Additional room name may follow when useful.
- Use clean thin black CAD-style linework. Show cabinet doors, drawers, handles, countertops, and backsplashes where supported by the sources. Avoid sketch rendering and decorative framing.
- Draw vertical boundaries only at actual wall ends/corners. An open or cropped view edge has no vertical closing line. Show the floor and confirmed ceiling; do not confuse cabinet top with ceiling.
- Hide crop-region outlines and viewport title extension lines that create extraneous boxes or lines through the drawings. Preserve real wall geometry and dimension witness lines.
- Show doors on the viewed wall where present. Show visible side profiles of casework on perpendicular walls; do not turn a perpendicular door into a frontal door on the viewed wall.
- Give each elevation a small room-plan key with the room number, relevant walls/doors/cabinets, and a direction arrow. Identify directions as plan north/east/south/west. Keys are NTS, but must not introduce nonexistent gaps, corners, or fixture positions.

## Devices and dimensions

- Draw receptacles as readable faceplates similar to the accepted architectural example. Show data faceplates separately wherever required by the source. Preserve duplex/quad distinction using the legend or other explicit evidence.
- Draw original power-plan receptacles and data in black; draw furniture-plan electrical and data in blue. Use compact source/type tags (`P-R`, `P-Q`, `P-D`, `F-R`, `F-D`) and a legend that distinguishes duplex, quad and data-port symbols. Retain verified circuit identifiers without burying the elevation in callout text.
- Use horizontal dimensions from an identified wall edge/corner to device center, and vertical AFF dimensions to the defined mounting reference. Replace redundant long outlet labels with these dimensions.
- Default receptacle and data centerlines to **16 inches AFF** unless a specific source/user instruction overrides. Above-desk/counter positions identified at the approved raised height use **44 inches AFF**, not the superseded 40 inches. TV and equipment outlets use their specific documented heights; do not apply 44 inches indiscriminately.
- If a box must relocate behind equipment, show existing and proposed positions with an arrow and the proposed AFF. Coordinate enclosure cutouts and access with the approved equipment detail.
- Do not dimension a schematic position as though surveyed or verified. Mark an unresolved offset for verification rather than deriving false precision from an NTS image.

## Cabinets, corners, and blocking

- Show upper cabinet bottom AFF, cabinet height, and top AFF. Use the applicable room's source detail rather than copying another room's heights.
- Indicate required blocking/backing for wall-mounted upper cabinets with leaders to the supported cabinet groups. Locate backing at manufacturer mounting rails/fastener zones; final backing dimensions and attachment follow approved cabinet/framing details.
- Check whether the run meets wall corners. Do not create intentional end gaps from a schematic plan key. Identify field-fit scribe/filler coordination separately from an actual open space.
- Show adjacent casework in other directions as visible profiles. Do not imply unverified cabinet depths or equipment clearances are established dimensions.

## Complete rooms one by one

Maintain a room checklist in the project workspace: architectural/CAD number, furniture number, sources, required directions, sheet/view identifiers, unresolved coordination items, and verification status. Avoid storing volatile element IDs in this reusable skill.

For each room, reconcile the plans, draft all required directions, place them on one sheet, and inspect the rendered sheet before moving on. Check wall endings, doors, casework, device source/type/offset/AFF, blocking, mini-plan accuracy, header style, and note collisions. Carry unresolved source questions forward explicitly; do not label a partially drawn or unverified room complete.

Use actual tool results to distinguish drafted, visually checked, saved, and PDF-exported work. A view image proves appearance, not an RVT save or a correctly sized PDF. If tools cannot save/export, state the remaining application step accurately.
