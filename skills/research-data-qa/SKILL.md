---
name: research-data-qa
description: Independently audit research datasets for structural integrity, evidence and provenance, coverage, contradictions, and readiness. Use when a dataset needs a reproducible quality review before analysis, sharing, or downstream use.
---

# Research Data QA

Perform independent, read-only quality assurance on the actual supplied data. Treat researcher labels, checksums, summaries, and claimed tool runs as assertions until reproduced. Keep structural validation, source verification, coverage assessment, rights review, and downstream acceptance as distinct gates. Do not silently repair source data or approve a production use.

## Freeze and inspect

Record the supplied artifact, version, researcher/source, date, requested scope, and SHA-256 when source bytes are available. Preserve originals. Inspect the saved rows and every relevant table; a narrative without record-level data is a lead, not an auditable dataset. Record which tools, sources, and execution capabilities are available. Do not incur paid service costs without explicit approval.

## Validate structure reproducibly

When a schema is supplied, use it as the contract and run `scripts/validate_dataset.py --input <csv-directory> --schema <schema.json>`. The schema file describes tables, required columns, optional ID columns, and foreign-key relationships; see [references/schema-format.md](references/schema-format.md). Capture the actual JSON report. If the tool cannot run, perform only checks that can be reproduced and mark unavailable checks `NOT_RUN`.

Review required tables and columns, blank or duplicate IDs, broken references, malformed rows, inconsistent types and status vocabularies, unsupported claims of verification, broken evidence links, count mismatches, duplicate candidates, and contradictory values. A script proves only the mechanical checks it implements; it does not prove the truth or freshness of external sources.

## Verify claims and scope

For consequential facts, inspect appropriate primary sources and record claim-specific URLs or record identifiers, publisher, relevant excerpt or field, access date, source date, and reviewer conclusion. Keep identity, status, location, authorization, and other distinct claims separate where the domain requires it. Challenge stale or conflicting evidence. Do not invent sources, bypass access controls, or turn missing evidence into a negative finding.

Track requested scope and searched coverage explicitly. Distinguish searched, searched with no supported result, incomplete, and blocked. A requested category that was not searched is incomplete, not a zero count. Recompute totals from actual saved rows and distinguish observed totals from reported totals.

## Report findings and gates

Produce an acceptance summary, severity-ranked finding ledger, coverage/evidence manifest, and non-destructive handoff. Each material finding should identify the dataset and record, field, observed value, recommended disposition, check, supporting evidence, date, confidence, and follow-up owner/action when known. Preserve the source value; use `UNKNOWN` for unsupported values.

Report structural integrity, source support, coverage, rights/privacy, independent review, and downstream eligibility separately using `PASS`, `FAIL`, `HOLD`, or `NOT_RUN`. Keep the overall recommendation on `HOLD` when a critical condition failed, is disputed, or was not evaluated. Do not claim a dataset is ready for publication, ingestion, or another consequential use based only on automated checks.

## Optional structured checks

- For a configurable CSV structural audit, use the validator and format reference above.
- For domain-specific facts or rules not represented in that schema, document the limitation and conduct a separate evidence-based review; do not quietly expand the generic validator's meaning.
- Return proposed corrections in a separate ledger or copy. Never overwrite the researcher's source rows.
