---
name: coding-guardrails
description: Enforce source inspection and evidence-based coding claims. Use when Codex edits, reviews, debugs, or explains code, especially when referencing line numbers, files, functions, spreadsheet schemas, Apps Script, or repository behavior.
---

# Coding Guardrails

Follow these rules for code work:

- Read the relevant source file section before making claims about line numbers, functions, headers, mappings, trigger behavior, or control flow.
- Do not assume code lines, file contents, function bodies, or current behavior from memory, prior conversation, pasted excerpts, summaries, or old diffs when the local file can be read.
- Before saying "currently", "now", "line X", "this function does", or "the code writes", verify against the latest local file contents.
- If exact line references matter, run a targeted search or line-numbered read immediately before answering.
- If unable to read the source, say that explicitly and label any statement as an inference.
- For all code, use properties, environment variables, or an appropriate secret store for credentials, API keys, tokens, spreadsheet IDs, deployment IDs, and other secrets unless the user specifically instructs otherwise.
- Search and map spreadsheet or tabular data by normalized header name, not by fixed indexes such as `row[x]`, unless the user specifically requests fixed-position handling or the source has no headers.
- Do not make assumptions about headers, columns, row positions, or schemas; inspect the current source before editing or explaining behavior.
- When implementing changes, first suggest the intended code behavior or approach, then create or edit the code after the direction is clear.
