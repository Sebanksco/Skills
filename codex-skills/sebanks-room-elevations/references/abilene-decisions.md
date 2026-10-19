# Abilene project decisions

Confirmed by Clinton Baird during the elevation coordination chat, 2026-10-17. Verify drawing evidence when using these decisions. They do not replace the current approved construction documents.

## Source hierarchy and identification

- The CAD drawing imported into Revit is the source of truth for room dimensions and layout, per Clinton's later explicit instruction. Furniture electrical governs furniture/device requirements, not replacement room geometry. The black original power plan E-2.2 retains circuit intent; old box positions may change.
- ATT 7 Furniture Electrical Plan, F0-03, printed 7/30/2026, is furniture support information. It does not establish all required building power/data devices.
- ATT 2 Furniture Details and Images contains room casework and furniture details. The original architectural kitchen elevation is A-3.5 detail 02.
- The signed floor plan dated 2026.06.03 is a comparison reference only where it differs from the imported CAD. A file upload/name dated 10.14.26 does not by itself make the original 2024 drawing content a new revision.
- Retain the owner's elevation labels while recording the verified imported-CAD labels: Copy/Supply = **elevation 105 / CAD 110**; Auxiliary Office 2 = **elevation 105A / CAD 105**; Break Room = **elevation 110 / CAD 115**; Group 1 Storage = **elevation 110S / duplicated CAD 110**. Earlier conversational CAD numbering was inaccurate; the actual DWG labels govern this crosswalk. Match by location and function.
- Ceiling is **9 feet AFF**, per Clinton. Flag conflicts with older schedules.
- Lobby-to-main-hall opening is **5 feet**, per Clinton, superseding the earlier 6 feet 1/4 inch reading. Do not rescale the whole plan.
- The long main hallway is **6 feet 1-1/4 inches wide** to allow for drywall and a finished **6 foot center tile zone**. This is distinct from the 5 foot short connector. Do not substitute one width for the other.
- Scope excludes **all hallway elevations, Mechanical/Electrical, and the mop-sink/Janitor room**. Create elevations for every wall of the remaining rooms, including vestibule, restrooms, and storage rooms.

## Lobby / Waiting 101

- Water fountain is on the **east wall of the main lobby, beside the bathroom**. It is **not on the south wall**. Apply this to the elevation and every mini-plan.
- Fountain model, mounting AFF, and rough-in location remain subject to its approved submittal; no height was established by the user's location correction.
- North windows and other openings need supported elevation dimensions. Do not treat a plan symbol as evidence of head/sill height.
- Legacy CD/Final source `24019-111124-L.pdf` (11.11.24), A-2.3/02 window types, A-3.1/01 exterior front and A-3.2/04 section: the current CAD plan-north lobby facade has a **Type D storefront, 12 feet wide x 6 feet high, sill 3 feet / head 9 feet AFF**, with an upper **Type C clerestory, 12 feet wide x 4 feet high, sill 14 feet 10 inches / head 18 feet 10 inches AFF**. Preserve the current CAD horizontal location. Legacy geographic west/front corresponds to current CAD plan north; reverse the exterior viewpoint for the interior.
- These are multi-lite storefront assemblies (three fixed-lite bays; Type D three rows, Type C one row), distinct from the owner's typical single-pane 5-by-5 windows. Do not put a center divider inside an individual lite. Show the legacy assembly divisions as source evidence for coordination rather than applying them globally to typical windows.
- **Unresolved ceiling conflict:** the legacy lobby schedule/sections show a tall lobby (20 foot roof plate, ceiling to underside of joists), while the owner previously specified 9 feet. Keep the owner's datum and flag the upper glazing/tall wall as legacy reference for review; do not silently approve a ceiling change. A roof plate datum is not a verified horizontal finished-ceiling height.

## Copy/Supply 105

- Primary IT enclosure: 26RU CUBE-iT, **48 H x 24 W x 30 D inches**; centered on plan-north wall, **bottom 30 inches AFF**, **top 78 inches AFF**.
- Original power plan shows a quad at the north cabinet location. Show the original **16 inches AFF** position and relocation arrow to **36 inches AFF behind the cabinet**.
- Other enclosure receptacles must align with manufacturer rear access/cutouts; original enclosure design guide calls for separate UPS/PDU power. Do not treat the quad as a substitute for those connections.
- Secondary lessor internet cabinet: 12RU / **24 inch height**. It has **no assigned position in this room**. Red note on the north elevation: `LESSOR INTERNET CABINET HAS NO ASSIGNED POSITION IN THIS ROOM. PLEASE ADVISE.` Do not draw an invented installed position.
- North elevation shows the visible side profiles of the east and west furniture-plan cabinets.
- West/east upper cabinets: **bottom 54 inches AFF**, **24 inch cabinet height**, **top 78 inches AFF**. Show blocking and top AFF.
- Above-counter receptacle is **44 inches AFF**. West horizontal dimension was taken as **3 feet 2 inches from the plan-north corner** in the furniture electrical plan.
- Include the south-end door on plan-west, and actual south wall corner on plan-east. Verify jamb offsets and casework depth against shop details.
- West cabinet run lengths conflict between source views; preserve the coordination issue instead of silently selecting a final shop dimension.

## Break Room 110 / furniture 115

- East kitchen casework comes from original A-3.5 detail 02, visible in the original black plan, even though missing from the furniture-only sheet.
- Base run modules: **1 ft 6 in, 2 ft dishwasher, 3 ft accessible sink, 2 ft 6 in, 3 ft 6 in refrigerator opening, 2 ft**; total **14 ft 6 in**.
- Counter **34 inches AFF**. Main uppers: bottom **66 inches AFF**, height **30 inches**. Over-refrigerator upper: bottom **72 inches AFF**, height **24 inches**. End upper: bottom **54 inches AFF**, height **42 inches**. All upper tops **96 inches AFF**. Do not copy Room 105's 78 inch top.
- Show vertical wall-corner lines from floor to 9 foot ceiling at both run ends. Original detail depicts the run reaching both corners; no intentional gaps. Correct the mini-plan to agree. Any small field-fit scribe/filler is a shop-drawing coordination item.
- Blocking leaders must cover all upper cabinet groups. Appliance power and data/device mapping remain to be reconciled with the current room layout.

## Other specific heights

- Office MD1 wall overheads: owner-selected **bottom 54 inches AFF**, source height **17 inches**, **top 71 inches AFF**. Verify source width: typically 60 inches, VOPS 78 inches, reception 60 inches north and 102 inches south. Exact horizontal positions and mounting rails require approved shops.
- Typical windows: owner specified **60 inches overall height**, with **2 inches frame/jamb deducted at the top and bottom**, leaving **56 inches clear glass height**. This top/bottom interpretation is recorded for review; do not infer sill/head AFF from it. Retain actual CAD widths and flag non-typical assemblies. Windows are **single pane with no center vertical mullion**. Do not apply this to door leaves or invent a door/frame arrangement.
- Storage 104 south-wall original duplex: **16 inches horizontally from the east corner**, **16 inches AFF to center**, per owner. This clears the CAD door opening and supersedes the earlier omitted/conflicting location.

- Furniture electrical TV outlets in Group 2 and Children's Room use the specific **54 inches AFF** callout where shown; confirm the associated device and room crosswalk.
- Above-counter Copy/Supply outlet and identified raised desk/counter outlets use **44 inches AFF**, superseding an earlier 40 inch interpretation.

## Source access

Locate the above documents in the Abilene project SharePoint folders (`00 All Files`, construction documents, procurement, and approved submittals) or the authorized local project source folder. The enclosure guide in procurement is named `Telecommunications Enclosure (TE) Desgin Guide.pdf` (source spelling). Do not embed credentials, private chat photos, or source PDFs in a public skill repository.

## Later owner revisions - October 18, 2026

These decisions supersede earlier conflicting entries above.

### Lobby ceiling, vestibule and glazing

- Main lobby ceiling, including the north side, is 18 feet AFF. Other rooms retain their room-specific ceiling datums.
- South reception and east walls have a 12-inch projecting fur-down. Its underside is 9 feet AFF; its 18-inch height places its top at 10 feet 6 inches AFF. Show the front band and visible adjoining-wall profiles.
- Vestibule enclosure projects into the lobby with its top at 9 feet AFF, below the main 18-foot lobby ceiling.
- Current CAD south vestibule face has two sliding tracks at y=625/623 and y=623/621, x=839.625 through 936.625: 97 inches overall. Show the double slider on the lobby-facing front. Actual head and frame profiles require verification.
- Preserve legacy north clerestory head at 18 feet 10 inches AFF pending review. Flag its 10-inch conflict with the owner ceiling rather than silently changing glazing.

### Lobby fountain and TV electrical

- Owner confirms the Elkay high/low fountain and bottle filler are on CAD plan EAST beside the restrooms. The earlier west description is resolved.
- Show a representative Elkay ezH2O outline. Final model, handedness, mounting AFF and rough-in follow the approved submittal.
- Highlight the two-gang receptacle box relocation BEHIND the fountain in both sets. Cross out its source position and show an arrow. Final AFF must coordinate with rear access.
- Mark the adjacent fountain data drop REMOVE.
- Flag missing elevated TV power and data in the lobby. Wall, horizontal position and AFF remain to coordinate; do not invent a TV location.

### Independent base and furnished sets

- Maintain A-series base elevations with fixed cabinets, equipment, bathroom fixtures and electrical/data; exclude loose furniture.
- Maintain independent F-series views and sheets adding loose furniture from the current yellow overlay, top-level CET furniture CAD blocks and ATT 2 details. Exclude the nested original architect representative furniture.
- Use gray generic furniture outlines. Unverified product profiles, dimensions and finishes remain approximate. Keep one room per page and publish separate PDFs.
- Hide unrelated OST_Viewers reference markers in each duplicated view. These can print as large dashed boxes even with crop visibility off. Preserve actual boundary and casework geometry.
- Refresh standalone room review PDFs from the latest combined base PDF after revisions so mobile links retain current dimensions.

### Lavatory mirrors, soap and receptacles

- Mirrors OVER LAVATORIES are 24 inches wide by 36 inches high. Do not apply this size to unrelated glazing.
- Automatic soap dispenser envelope: 11 inches high by 5 inches wide by 5 inches deep.
- Provide 7 inches clear from mirror edge to adjacent receptacle faceplate edge: 1-inch clearance, 5-inch dispenser, 1-inch clearance.
- Use 8.5 inches from mirror edge to receptacle OC with a 3-inch plate allowance. Verify the actual selected faceplate before rough-in.
- In Rooms 102 and 103, center mirrors on the imported CAD lavatory centerlines. Dimension BOTH required mirror OC and receptacle OC from the PLAN NORTH finished wall corner, with centerline marks.
- Room 102: mirror OC 33.125 inches (2 feet 9-1/8 inches); receptacle OC 53.625 inches (4 feet 5-5/8 inches), from north corner.
- Room 103: mirror OC 33.125 inches (2 feet 9-1/8 inches); receptacle OC 12.625 inches (1 foot 0-5/8 inch), from north corner.
- Proposed receptacles retain 44 inches AFF. Mirror and soap mounting AFF remain to verify; owner supplied sizes, not revised mounting heights.
- Staff restrooms 112 and 113 show soap beside lav mirrors. Their existing outlets are elsewhere; do not invent a new adjacent outlet. Apply the 7-inch rule if one is provided.

### Source review corrections

- Group 1 / Room 111: ATT 2 page 17 specifies two wall-mounted MD1 storage units, 78 inches wide by 17 inches high, on the east and south sides. Include them in both sets with visible adjoining profiles and blocking leaders.
- The Group 1 source calls these units overhead while illustrating low wall-hung credenzas. Do not automatically apply the office 54-inch mounting height. Mark bottom/top AFF to verify; illustrated vertical location and 12-inch depth are schematic.
- Kitchen / Break Room 110 (furniture 115): furnished set includes DT1 Jive TCRA-4284 table, 42 by 84 by 36 inches high, and CH1 GAKG-1935 cart, 36 inches high by 19 deep by 35 wide, from ATT 2 page 16.
- Place kitchen table/cart from current CAD blocks C88/C63. CAD cart footprint of about 43.05 by 21.75 inches differs from listed body dimensions; verify handle/caster envelope or model. Keep loose table/cart out of the base set.
