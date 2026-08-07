---
name: build-scos-expandable-tables
description: Build or revise SCOS web-portal tables that contain parent rollups and child records. Use when a page must match the /buyout Owner SOV directory, including individually expandable parent rows, Expand All and Collapse All controls, nested child rows, parent and child edit actions, status chips or procurement-stage banners, loading and empty states, responsive behavior, and accessible disclosure controls.
---

# Build SCOS Expandable Tables

Use the current `/buyout` Owner SOV directory as the visual and interaction authority. Inspect its HTML, JavaScript, CSS, and current tests before editing another page. Read [references/scos-table-contract.md](references/scos-table-contract.md) for the canonical contract and selectors.

## Workflow

1. Inspect the target page, shared `styles.css`, and the live `/buyout` implementations named in the reference.
2. Identify the authoritative parent ID, child ID, editable state, status, permissions, and server-owned data. Never infer these from display text.
3. Preserve expanded parent IDs in a `Set`. Do not use array position or visible label as identity.
4. Render each parent as one disclosure row with a chevron, summary columns, `aria-expanded`, and `aria-controls`.
5. Render children inside the parent's hidden detail container. Use compact child summary rows. For actual procurement children, prefer the established seven-stage procurement banner whenever authoritative stage data is available. For configuration or reference children, use a controlled status chip instead.
6. Add both `Expand All` and `Collapse All`. Apply them only to currently rendered/filter-matching parents. Disable them when no parents are visible.
7. Keep the parent header clickable except for nested action buttons. Prevent Edit and other child actions from toggling the parent.
8. Reuse in-page dialogs for parent and child edits. Enforce permissions, validation, concurrency, idempotency, and audit on the server.
9. Update the asset cache version. Test one-parent, several-parent, no-child, empty, filtered, view-only, stale-write, desktop, and narrow layouts.

## Required behavior

- Start collapsed unless the existing page has a persisted expansion policy.
- Allow every parent to expand or collapse independently.
- Keep child rows unavailable to keyboard and pointer interaction while their parent detail is hidden.
- Put parent Edit in the expanded parent action strip when the `/buyout` pattern does so.
- Put child Edit and status indicators in the child banner/detail area, not in a competing page-level toolbar.
- Render status from controlled states. Use existing `status-badge`, `procurement-stage-bar`, and `procurement-stage` classes and their established colors.
- For procurement records, render all seven stages in canonical order: Requested, Approved, RFQ / ITB, Quote Received, Quote Approved, PO Issued, and Delivered / Closed.
- Do not remove or collapse unstarted procurement stages; render them as `not-started` so the complete workflow remains visible.
- Escape every user or database value before inserting HTML.
- Use friendly labels; never expose database UIDs.

## Avoid

- Flat tables that merely indent children without disclosure behavior.
- One global expanded boolean.
- Comma-separated identifiers, editable hidden IDs, inline styles, or a new status color system.
- Expanding or collapsing every record in the database when a filter shows only a subset.
- Browser-only authorization or status-transition rules.

## Verification

Run syntax checks and focused tests. Add assertions for individual disclosure, Expand All, Collapse All, `aria-expanded`, hidden child containers, parent Edit, child Edit, and status rendering. Report deployment and migration separately.
