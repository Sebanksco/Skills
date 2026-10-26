---
name: email-cleanup
description: Clean promotional email and routine automated notices under a privately configured retention policy, with initial, daily, and weekly passes.
---

# Email Cleanup

Read the private policy at ~/.codex/email-cleanup.json, or its explicitly supplied location, for verified mailbox, authorized categories, age/read rules, exclusions, deletion modes and checkpoints. Never publish that file, sender lists, message contents, IDs or audit logs. Missing policy means inventory only until scope is resolved.

## Select messages

Verify authenticated mailbox identity. Exclude Sent Items, Drafts and hidden/system/recoverable folders unless separately authorized. Never empty Deleted Items merely because matching messages exist there.

Promotions mean actual bulk marketing, offers and unsolicited sales pitches. A vendor sender, keyword or unsubscribe link alone is insufficient: transactional messages can share these. Preserve correspondence, invoices, receipts, price changes, contracts, project documents, clinical mail, requested quotes and account/security matters unless separately included. Honor flags, pins and keep rules.

Routine notices require verified sender and observed subject/body patterns. Distinguish automated SCOS notices from human correspondence mentioning SCOS and tracking copies of project emails. Preserve threats, active outages, billing issues, failed jobs needing intervention and other actionable alerts when policy requires. Quarantine cleanup concerns notification emails only; never release or delete quarantined messages or change filtering policy.

Use exact elapsed age from received time and the configured named time zone for scheduling. Unopened means provider unread state, not tracking history. Prefer APIs that do not mark messages read. Recheck unread state immediately before weekly deletion and retain messages read since inventory. Initial read-or-unread backlog authority does not apply to weekly runs.

## Execute and verify

Inventory and classify first. Follow pagination to exhaustion and record coverage/cursors. Offsets shift during deletion: finish each inventory before mutating, or restart bounded queries and deduplicate stable identities. Search limits are not complete coverage. Keep a private manifest of original IDs/folders, time/read state, classification/reason and intended action. Retain ambiguous messages for review.

Use supported connectors first. Do not invent bulk APIs or extract browser credentials. Move-to-Deleted-Items and permanent deletion are different operations; moving to Deleted Items twice does not prove permanent deletion. Follow current tool confirmation rules. Browser deletion beyond normal recovery requires action-time confirmation, which a skill or scheduled prompt cannot waive. Prepare the exact reviewed selection if confirmation is needed; continue independent soft deletions. Respect retention holds and report unavailable purge capability.

Operate on individual messages, not conversations containing unrelated mail. Refresh IDs after moves and verify destination or deletion result. Check state before retrying uncertain writes. Log verified successful, failed, ambiguous and pending-permanent counts separately; advance checkpoints only on verified outcomes. Do not unsubscribe, block senders, create mail rules or send messages without separate authority.

## Schedule and report

A skill is not a scheduler. When requested, use the Codex automation tool and reuse matching existing jobs. Separate daily routine notices from weekly unread promotions, following private policy. Do not silently make recurring soft deletions permanent.

Continue initial cleanup until covered or a concrete dependency remains; retain checkpoints across turns. Report actual coverage and exact remaining scope, never call a partial scan complete. Scheduled runs should notify only for meaningful completion, failures or required action and remain quiet on unchanged/no-match runs. Keep runtime evidence outside Git.
