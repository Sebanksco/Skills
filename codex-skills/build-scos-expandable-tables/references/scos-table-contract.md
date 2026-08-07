# SCOS expandable table contract

## Canonical sources

Inspect current code rather than copying stale snippets:

- `web-portal/public/buyout.html`: `#expandAllBuyouts`, `#collapseAllBuyouts`, `.buyout-package-column-headings`, `#buyoutPackageRows`
- `web-portal/public/buyout.js`: `expandedSovUIDs`, `renderBuyoutRows`, `setExpandedBuyoutRows`, `expandAllBuyoutRows`, `collapseAllBuyoutRows`, `toggleBuyoutPackageRow`
- `web-portal/public/buyout.css`: `.buyout-package-rows`, `.buyout-sov-row`, `.buyout-sov-summary`, `.buyout-sov-packages`, `.buyout-package-row`, `.buyout-package-summary`, `.buyout-package-chevron`
- `web-portal/public/styles.css`: `.status-badge`, `.procurement-stage-bar`, `.procurement-stage` and the `complete`, `current`, `blocked`, `not-started` states

## DOM hierarchy

```text
section
  heading + count/status
  tools
    search/filter when needed
    page actions
    Expand All
    Collapse All
  column headings
  parent rows
    parent disclosure button
      chevron
      summary fields
    parent detail [hidden when collapsed]
      parent action strip: Edit and controlled actions
      child rows
        child summary/banner
        child status chips or procurement stage bar
        child Edit action
```

Use semantic `button` disclosure controls. Connect each button to a stable detail ID through `aria-controls`; keep `aria-expanded` synchronized with `hidden` and the expanded CSS class.

## State contract

Use one `Set` of expanded parent IDs. Use a second `Set` only when children themselves also expand. Rendering may replace DOM, but it must not erase expansion state unless the authoritative record disappeared or the user invoked Collapse All.

Individual toggle:

1. Ignore clicks originating from Edit or another nested action.
2. Resolve the closest parent row by its data attribute.
3. Add or remove its stable ID from the expanded set.
4. Synchronize only disclosure classes, `aria-expanded`, and `hidden` when a full render is unnecessary.

Expand All adds IDs for visible/filter-matching parents. Collapse All clears parent and child expansion sets.

## Child status banner

Choose the smallest established status treatment that communicates the workflow:

- Use `status-badge` for one controlled state such as Active, Needs review, Reference only, or Inactive.
- For an actual procurement child record, prefer `procurement-stage-bar` and render the complete seven-stage workflow in this canonical order:
  1. Requested
  2. Approved
  3. RFQ / ITB
  4. Quote Received
  5. Quote Approved
  6. PO Issued
  7. Delivered / Closed
- Assign every procurement stage one of the established state classes: `complete`, `current`, `blocked`, or `not-started`. Keep future stages visible as `not-started`.
- Put compact source, vendor, or linked-record chips above the stage bar only when those records exist.
- Put the current state and next action below the stage bar when available.

The seven-stage banner is the standard for real procurement records, not an exceptional treatment. Do not fabricate a current stage from sparse data: if authoritative procurement-stage data is unavailable, show a controlled status badge or an explicit unavailable state until the data is resolved.

## Editing contract

Parent and child Edit buttons may open the same dialog, but the dialog must show relationship context and preserve stable identity and row version. Child values may inherit from the parent; show inherited values distinctly and send blank overrides as blank/null rather than copying the parent into the child record.

The API must re-read canonical parent/child relationships, permissions, status, and row version inside the transaction. Keep writes idempotent and audited.

## Responsive and accessibility checks

- Preserve a horizontal-scroll container when the summary needs several fixed columns.
- At narrow widths, keep disclosure and Item visible; allow secondary columns to scroll or hide consistently with the sibling workspace.
- Test keyboard activation, focus visibility, `aria-expanded`, and hidden details.
- Provide loading, empty-parent, and parent-with-no-children messages.
