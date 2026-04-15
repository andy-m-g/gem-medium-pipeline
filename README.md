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

## Quick Start

From the repository root:

```bash
cd /home/andy/Documents/bioreactor/media_pipeline
python3 scripts/media_pipeline_cli.py media init --medium-family lbproto --version lbproto_draft_01
```

Build the worked example:

```bash
python3 scripts/media_pipeline_cli.py media draft-create \
  --medium-family lbproto \
  --version lbproto_draft_01 \
  --source-recipe examples/earlier_workbook_slice/source_recipe.tsv \
  --decomposition-table examples/earlier_workbook_slice/ingredient_component_composition.tsv \
  --curation-table examples/earlier_workbook_slice/curation_decisions.tsv \
  --mapping-table examples/earlier_workbook_slice/component_mapping.tsv \
  --viable-rules-table examples/earlier_workbook_slice/viable_compound_rules.tsv \
  --salt-split-rules-table examples/earlier_workbook_slice/salt_split_rules.tsv \
  --polymer-proxy-rules-table examples/earlier_workbook_slice/polymer_proxy_rules.tsv \
  --chemical-form-rules-table examples/earlier_workbook_slice/chemical_form_rules.tsv \
  --namespace-snapshot gapseq_seed_like
```

Review outputs:

```bash
python3 scripts/media_pipeline_cli.py media release-check --family lbproto --medium-version lbproto_draft_01
sed -n '1,40p' exports/media/lbproto/lbproto_draft_01/final_medium_export.tsv
sed -n '1,40p' exports/media/lbproto/lbproto_draft_01/reports/row_lineage.tsv
```

## Usage Tutorial

Typical workflow:

1. Capture the medium source into explicit TSVs such as `source_recipe.tsv` and,
   when needed, `source_composition.tsv`.
2. Add explicit decomposition and curation tables that keep proxy logic,
   salt-splitting, polymer handling, and chemical-form changes visible.
3. Map compounds into the frozen upstream namespace snapshot under
   `upstream_snapshots/`.
4. Generate model-facing artifacts and final exports with preserved lineage.
5. Review bound-assignment policy separately from source inventory and
   model-facing representation.

Two good first fixtures are:

- `examples/earlier_workbook_slice/` for a small workbook-style slice
- `examples/cim_inspired_slice/` for a slightly richer CIM-like slice

For the full stage-by-stage walkthrough and additional commands, use
[README_prototype.md](README_prototype.md).

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

## Common Tasks

- Build a reference fixture: use the `media draft-create` command shown above
- Review draft consistency: run `media release-check`
- Refresh the local upstream snapshot intentionally: use
  `python3 scripts/refresh_gapseq_seed_snapshot.py`
- Inspect current implementation status: read [MVP_STATUS.md](MVP_STATUS.md)

## Notes

- `final_medium_export.tsv` is the canonical internal export
- `gapseq_medium.csv` is a downstream compatibility export
- `undermind/` is intentionally local support material, not ordinary pipeline
  input

For the full prototype walkthrough, CLI usage, and current fixture details, use
[README_prototype.md](README_prototype.md).
