# Saved power and data plan standard

Established from the owner's approved Abilene drafting workflow, 27 October 2026. Apply as the starting SEBANKS plan profile; explicit project/user changes take precedence. These are Revit drafting settings, not manufacturer device dimensions.

## Line weights and text

| Item | Saved setting |
| --- | --- |
| Receptacle, quad, data, and wall-sconce symbol strokes | Revit line-weight index **4** |
| Architectural wall/base-plan strokes | Index **2** where used in the established CAD reconstruction |
| Fine fixture/detail strokes | Index **1** where used in that reconstruction |
| Ordinary notes and drafted dimension text | **Arial, 3/64 inch paper height** = 1.5/32 inch = 0.046875 inch = 3.375 points |
| Power-plan bottom-right title | **POWER PLAN**, black, bold Arial, **3/16 inch paper height** |

The saved ordinary text height in Revit internal feet is **0.00390625**; title height is **0.015625**. Duplicate the text type before changing size, bold, or color for a special note. Do not resize the shared ordinary-note type to make a heading. Text is paper-sized; symbols are geometry, not a font.

## Compact outlet geometry

Approved starting geometry at **1:64 (3/16 inch = 1 foot)**, in model feet:

- Circle radius **0.28 ft**, diameter **0.56 ft**. If rebuilding with straight detail segments, use 32 segments for the circle.
- Parallel strokes at local x = **-0.11 and +0.11 ft**.
- Local positive y points **toward the wall**. Each parallel stroke runs from local y = **-0.23** to **+0.5883324828705 ft**. Place the circle center 0.5883324828705 ft from the wall so both legs meet the correct face.
- Duplex: circle plus the two parallel strokes. Quad: same geometry plus **one** perpendicular cross stroke from local x = -0.364 to +0.364 ft at local y = 0. Preserve the quad distinction when changing color or thickness.
- Data: separate outline triangle approximately **0.8 ft wide by 0.7 ft deep**. Preserve source/user orientation; do not rotate all triangles indiscriminately. Keep the symbol clear of the wall and assigned to the correct room side.
- Keep the established size and appearance when revising an existing plan. At another view scale, confirm the intended printed symbol size before applying these model dimensions unchanged. At 1:64, the circle diameter prints approximately **0.105 inch**.
- Group all strokes for each glyph. Use the same line-weight index on circle, legs, and quad cross; do not leave a replacement glyph thinner than neighboring symbols.

## Sources, colors, and placement

- Original architectural power-plan devices: **black RGB (0,0,0)**.
- Furniture-plan power/data: **blue RGB (0,65,220)**, positioned, oriented, and dimensioned from the furniture source against current architectural geometry.
- Owner-directed relocation destinations: **red RGB (220,0,0)**. Preserve their nearby original-device reference when requested. The owner can explicitly direct other symbols to red; for example, all three Janitorial GFCIs were explicitly made red. Do not infer color solely from whether a symbol is new.
- Bottom of receptacle/data box: **16 inches AFF U.N.O.** in the current power-plan legend. This overrides the earlier centerline default for this plan. Project-specific raised mounting heights remain specific instructions, not a global 16-inch override.
- Use dimensions from the specified opening/corner to device center. Avoid redundant wording such as "TO RECEP CL" when the dimension's reference is clear.
- Receptacle legs meet the assigned wall face, not the far side or wall center. Maintain room-side association when walls shift.
- Include **SEE ELEVATIONS** in each restroom when the coordinated elevations govern accessory/device mounting.

## Wall sconces

Use a distinct wall-mounted lighting symbol, not a duplex or data triangle. The approved schematic plan glyph is a semicircle projecting into the served space, with a flat mounting edge on the wall and two short diagonal strokes from the mounting center toward the arc. Starting radius **0.32 ft**, line-weight index **4**. Group its strokes.

For the owner's four marked hall locations, labels read **SCONCE / 80" AFF**. The 80-inch height is that project instruction, not a universal sconce or accessibility height. Follow marked locations; do not invent precise dimension strings from hand-drawn markup circles.
