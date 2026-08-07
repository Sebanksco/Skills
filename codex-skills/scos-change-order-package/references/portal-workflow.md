# SCOS portal and client-review workflow

Revalidate this workflow against the live portal and current repository before every write. A Codex skill supplies operating instructions; it does not grant authentication, roles, project access, SharePoint permission, or a server-side integration.

## Authorization boundaries

Treat each state-changing action as separately authorized:

| Action | Default |
| --- | --- |
| Open SCOS, select a project, and inspect Change Orders | Allowed when requested |
| Populate an unsaved Create New form | Allowed when requested |
| Upload a file to SharePoint or change sharing | Require clear user authorization and exact destination |
| Save Draft | Require explicit authorization |
| Submit for internal review | Require explicit authorization |
| Record an internal decision | Require the authorized human decision |
| Issue to client reviewers and send email | Require explicit authorization and exact recipients |
| Approve, reject, request revision, or post an OCO | Require the authorized human action |

Do not interpret “prepare,” “populate,” or “for review” as authorization to save, send, approve, or post.

## Portal preparation

1. Use the browser-control skill and inspect the current page before every interaction.
2. Confirm the authenticated identity and role. Never request, expose, or reuse passwords, cookies, tokens, or session storage.
3. Select the exact project on Home and record its displayed ProjectID and name.
4. Open **Change Orders** and verify the same project remains active.
5. Confirm the workspace loads its project-scoped Buyouts, commitments, contacts, and existing change orders. Stop when the project is not enabled or required lineage is absent.
6. Open **Create New** and map only validated manifest values into current controls.
7. Resolve Buyout, commitment, and reviewer selections from the choices returned for that project. Never enter invented identifiers.
8. Keep **Schedule impact** editable. If it is `0` days, ask the user to confirm that zero is intentional before saving.
9. Capture a form-state summary and leave the form unsaved for human review unless **Save Draft** is explicitly authorized.

## TXM project constraint

The portal project selector includes Cimmaron and additional projects, including `TXM | Manor Microhospital`. Never treat the initially active project as TXM; select and verify TXM explicitly.

The last verified production response reported that TXM was not enabled for the controlled SQL Change Order workflow and exposed no Buyout package, commitment, or owner reviewer choices. If that response remains, report: `I could not create PCO 11 in production because TXM is blocked by the site's project configuration.` Do not attempt to save PCO 11 until the live project workspace returns the required lineage.

For TXM, the user supplied these intended Owner Representative email addresses:

- `henry.johnson@pannenbier.com`
- `pat.freese@freesejohnson.com`

Treat the email addresses and requested Owner Representative role as user-confirmed inputs. Verify display name, organization, Entra identity mapping, and exact live role value before saving either contact; do not infer missing values from an email address. Contact configuration is a state-changing portal action and requires authorization in the active task. Configuring the contacts does not authorize issuing a PCO or sending an email. Do not release any email to either recipient until the user separately authorizes issuance and the exact PCO revision and package have passed review.

## Supporting documents

Use SharePoint as the evidence store when the live SCOS form accepts attachment metadata rather than binary file upload.

1. Resolve the exact project site, library, and change-order folder before uploading.
2. Preserve original architect documents, drawings, subcontractor estimates, correspondence, and generated package PDF.
3. Use stable SharePoint item or sharing URLs; reject expiring download URLs.
4. Record filename, category, content type, SHA-256 when local bytes are available, notes, and the exact revision supported.
5. Re-fetch an uploaded file and verify its identity and accessibility before attaching its metadata in SCOS.
6. Do not broaden SharePoint sharing merely to make a link work. Client access must follow the approved project permission model.

Attach evidence using the current categories. Keep the final ownership package PDF on the exact issued revision and distinguish it clearly from raw source and pricing documents.

## Save and list verification

Before **Save Draft**, verify the form summary, cost reconciliation, reviewer selection, package link, project, Buyout, commitment, and unresolved warnings. After an authorized save:

1. re-read the returned record;
2. locate it in the project Change Orders list;
3. verify its PCO number, revision, draft status, title, owner amount, downstream cost, GC markup, editable schedule impact, zero-day confirmation when applicable, Buyout and commitment lineage, references, and attachments;
4. report any mismatch and stop before submission or issuance.

## Controlled client review

Use the existing lifecycle in order: save draft, submit for internal review, record internal approval, then issue the exact revision to selected client reviewers.

Before issuance, verify:

- every recipient is an active Owner or Owner Representative contact with client review enabled;
- the exact revision is internally approved;
- the package PDF is attached to that revision through a stable SharePoint URL;
- the amount, revision fingerprint, validity, and schedule impact match the reviewed package;
- the email action is explicitly authorized.

The verified July 2026 implementation emails an authenticated `/client/pco-review` link. The assigned client signs in with the mapped Microsoft Entra identity and can review the issued revision, references, eligible attachments, and then approve, reject, or request revision. The link does not approve the PCO by itself.

The current email template does not contain a separate direct package-PDF URL. If a direct PDF link is required, treat that as a portal code change: add the exact-revision package URL to the controlled notification payload while retaining the authenticated review link. Do not claim this behavior exists until verified in deployed code and a representative notification.

## Failure conditions

Stop the affected operation when:

- the active project is ambiguous or changes unexpectedly;
- the controlled SQL Change Order workspace is not enabled;
- Buyout or commitment lineage is missing;
- an attachment URL is unstable, inaccessible, or mapped to another revision;
- the client reviewer is missing, inactive, or not client-review enabled;
- financial totals differ by more than $0.01 or conflicting totals remain unresolved;
- the package is not readable or does not match the form;
- the portal response cannot be re-read and verified.
