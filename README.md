# Media Pipeline

This repository contains an MVP GEM medium reconstruction / adaptation pipeline.
Its focus is translating laboratory media into explicit model-facing medium
artifacts while keeping three layers separate:

- source inventory
- model-facing chemical representation
- bound assignment

## Current Scope

This repo is still MVP / prototype status. The current implemented vertical
slice covers source capture, decomposition, normalization and conversion,
curation review, upstream namespace mapping, viable export transformation, final
medium export, lineage, and basic validation. The current emphasis is
conservative, provenance-aware medium construction rather than aggressive
automation.

## Core Ideas

- source inventory is not automatically uptake flux
- dissociation or other model-facing representation steps are distinct from
  bound assignment
- `inventory_only`, `concentration_derived_availability_bound`, and stronger
  cap types are distinct policy classes
- unresolved rich-medium components remain explicit unless supported by
  defensible proxy logic

## Where To Start

- [README_prototype.md](README_prototype.md)
- [MVP_STATUS.md](MVP_STATUS.md)
- [decisions/medium_layer_contract.md](decisions/medium_layer_contract.md)
- [decisions/bound_assignment.md](decisions/bound_assignment.md)

## Current Example Areas

- literature-test-media extraction and source-stage flattening
- M9 broth / M9 agar pilot work for conservative direct and dissociated cases
- yeast-extract partial-proxy pilot

## Repo Structure

- `schemas/`: TSV schemas and validation-facing constraints
- `templates/`: starter TSV templates for curator-facing artifacts
- `sources/`: extracted or curated source-medium artifacts
- `decisions/`: short policy notes, review notes, and explicit curator decisions
- `examples/`: worked slices and reference fixtures
- `upstream_snapshots/`: frozen local upstream namespace snapshots used for validation

For the full prototype walkthrough, CLI usage, and current fixture details, use
[README_prototype.md](README_prototype.md).
