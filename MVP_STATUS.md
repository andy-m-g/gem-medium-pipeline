# Medium Pipeline MVP Status

This document is a checkpoint summary of what the current medium-pipeline MVP
does today.

## Current MVP Scope

The MVP currently includes these implemented stages:

1. `source_capture`
2. `decomposition`
3. `normalize_and_convert`
4. `curation_review`
5. `map_to_upstream_namespace`
6. `viable_export_transformation`
7. `final_medium_export`
8. `row_lineage`
9. `validation`

Small implementation extensions now add:

10. `recipe_source_ingestion`
11. `model_diagnostic_harvest`
12. `curator_revision_proposal_generation`

The current flat-file inputs are:

- `source_recipe.tsv`
- `ingredient_component_composition.tsv`
- `curation_decisions.tsv`
- `component_mapping.tsv`
- `viable_compound_rules.tsv`
- `salt_split_rules.tsv`
- `polymer_proxy_rules.tsv`
- `chemical_form_rules.tsv`

The current canonical outputs are:

- `final_medium_export.tsv`
- `gapseq_medium.csv`
- `reports/row_lineage.tsv`

New explicit report outputs can include:

- `sources/<family>/<version>/source_document_cells.tsv`
- `validation/media/<family>/<version>/model_diagnostic_signals.tsv`
- `validation/media/<family>/<version>/diagnostic_medium_comparison.tsv`
- `exports/media/<family>/<version>/reports/diagnostic_version_history.tsv`
- `exports/media/<family>/<version>/reports/curator_revision_proposals.tsv`

Reusable curator pattern capture now also exists in:

- `media_pipeline/decisions/adaptation_patterns.tsv`

## Current Validation

The MVP currently performs:

- schema validation for the input TSVs and manifest
- upstream-reference validation against the extracted namespace snapshot
- stage-consistency validation across mapping, viable transformation, final export, and policy-driven background-species lineage
- release checks that fail when unresolved mappings, missing upstream references, missing reports, or stage-consistency violations remain

Upstream-reference validation distinguishes:

- `valid_upstream`
- `missing_upstream`
- `local_only_expected`

## Reference Fixtures

Two reference fixtures currently pass `release-check`:

- `lbproto`
  demonstrates an earlier workbook-style slice with direct export, salt split,
  polymer proxy, chemical-form change, and explicit background species
- `cimproto`
  demonstrates a CIM-inspired slice with the same MVP stages plus more explicit
  local-vs-upstream placeholder handling and stoichiometric salt splitting

Together, the two fixtures show that the MVP can represent:

- direct upstream-backed exports
- retained local placeholders that resolve later
- viable export transformations that replace intermediate forms
- policy-driven background-species insertion with lineage preserved

## Explicitly Deferred

The following remain out of MVP scope:

- `qc_override_policy`
- adapt logic / namespace migration logic
- new workflow stages beyond the current vertical slice
- richer governance or override-policy frameworks
- heavy release automation beyond the current draft/candidate checks
- generalized hardening of the internal aggregation helper

The pattern catalog is intentionally not automatic adapt logic. It preserves
repeatable reasoning for later workflow training while keeping scientific
judgment explicit.

## Likely Next Expansion Points

The next practical expansions are likely to be:

- stronger fixture coverage for additional medium patterns and edge cases
- broader upstream snapshot coverage so fewer biologically real compounds remain local placeholders
- richer validation around model exchange coverage and draft readiness
- a clearer promotion path from prototype release checks to fuller release lifecycle automation
