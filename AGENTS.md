# AGENTS.md

## Project Focus
This repository contains an MVP medium-construction pipeline for GEM workflows.

## Core Principles
- Preserve the distinction between upstream gapseq alignment and local curator decisions.
- Keep manual decisions in TSV tables, not hidden in code.
- Treat `final_medium_export.tsv` as the canonical internal output.
- Treat `gapseq_medium.csv` as a downstream compatibility export.
- Keep provenance explicit through `row_lineage.tsv` and rule tables.
- Do not redesign the architecture unless explicitly asked.

## Current MVP Scope

### In Scope
- `source_capture`
- `decomposition`
- `normalize_and_convert`
- `curation_review`
- `map_to_upstream_namespace`
- `viable_export_transformation`
- `final_medium_export`
- `row_lineage`
- basic validation

### Deferred Unless Explicitly Requested
- formal `qc_override_policy`
- namespace migration
- `adapt` workflow
- heavy release governance
- richer provenance bundles

## Working Style
- Prefer small, reviewable changes.
- Update README and example files when behavior changes.
- Keep scientific judgment in tables and notes, not in hidden code paths.
- Avoid committing bulky generated artifacts unless they are intentional reference fixtures.

## Internal Skills
- Repo behavior is also guided by the internal `skills/` documents.
- Current skill areas cover medium layers, bound assignment, rich ingredients, and upstream snapshot validation.

## Repo Hygiene
- `undermind/` is intentionally ignored and should not be reintroduced into version control.
- Do not commit caches, logs, bulk validation outputs, or temporary artifacts unless explicitly asked.
