# Medium Pipeline Prototype

This is the first real vertical slice of the medium pipeline. It implements only:

1. `source_capture`
2. `decomposition`
3. `normalize_and_convert`
4. `curation_review`
5. `map_to_upstream_namespace`
6. `viable_export_transformation`
7. `final_medium_export`
8. `row_lineage`
9. `validation`

The current scaffold still uses a simple `aggregate_compounds` helper internally, but that helper is not being treated as hardened MVP scope yet.

Deferred from the literature-backed MVP/add-on roadmap:

- `qc_override_policy`
- namespace migration / adaptation logic
- release automation beyond simple draft/candidate checks
- adapt logic
- heavy governance / richer provenance packaging
- full release-state automation

## Input tables

The prototype reads these explicit flat files:

- `source_recipe.tsv`
- `ingredient_component_composition.tsv`
- `curation_decisions.tsv`
- `component_mapping.tsv`
- `viable_compound_rules.tsv`
- `salt_split_rules.tsv`
- `polymer_proxy_rules.tsv`
- `chemical_form_rules.tsv`

## Canonical outputs

- `final_medium_export.tsv`
- `gapseq_medium.csv`
- `row_lineage.tsv`

`final_medium_export.tsv` is the canonical internal export.

The MVP-specific intermediate that now sits between mapping and final export is:

- `viable_compounds.tsv`

## Worked example

The reduced earlier-workbook example lives in:

- `media_pipeline/examples/earlier_workbook_slice/source_recipe.tsv`
- `media_pipeline/examples/earlier_workbook_slice/ingredient_component_composition.tsv`
- `media_pipeline/examples/earlier_workbook_slice/curation_decisions.tsv`
- `media_pipeline/examples/earlier_workbook_slice/component_mapping.tsv`
- `media_pipeline/examples/earlier_workbook_slice/viable_compound_rules.tsv`
- `media_pipeline/examples/earlier_workbook_slice/salt_split_rules.tsv`
- `media_pipeline/examples/earlier_workbook_slice/polymer_proxy_rules.tsv`
- `media_pipeline/examples/earlier_workbook_slice/chemical_form_rules.tsv`

It demonstrates:

- one `direct_export`
- one `salt_split_member`
- one `polymer_proxy`
- one `chemical_form_change`

A second stress-test fixture lives in:

- `media_pipeline/examples/cim_inspired_slice/`

It exercises the same MVP stages with a small CIM-inspired slice and includes:

- one `direct_export`
- one stoichiometric `salt_split_member`
- one `polymer_proxy`
- one `chemical_form_change`
- explicit background-species insertion

## Run end to end

Initialize a prototype scaffold:

```bash
python3 scripts/media_pipeline_cli.py media init --medium-family lbproto --version lbproto_draft_01
```

Build the prototype slice from the worked example:

```bash
python3 scripts/media_pipeline_cli.py media draft-create \
  --medium-family lbproto \
  --version lbproto_draft_01 \
  --source-recipe media_pipeline/examples/earlier_workbook_slice/source_recipe.tsv \
  --decomposition-table media_pipeline/examples/earlier_workbook_slice/ingredient_component_composition.tsv \
  --curation-table media_pipeline/examples/earlier_workbook_slice/curation_decisions.tsv \
  --mapping-table media_pipeline/examples/earlier_workbook_slice/component_mapping.tsv \
  --viable-rules-table media_pipeline/examples/earlier_workbook_slice/viable_compound_rules.tsv \
  --salt-split-rules-table media_pipeline/examples/earlier_workbook_slice/salt_split_rules.tsv \
  --polymer-proxy-rules-table media_pipeline/examples/earlier_workbook_slice/polymer_proxy_rules.tsv \
  --chemical-form-rules-table media_pipeline/examples/earlier_workbook_slice/chemical_form_rules.tsv \
  --namespace-snapshot gapseq_seed_like
```

Inspect outputs:

```bash
sed -n '1,40p' media_pipeline/intermediate/lbproto/lbproto_draft_01/viable_compounds.tsv
sed -n '1,40p' media_pipeline/exports/media/lbproto/lbproto_draft_01/final_medium_export.tsv
sed -n '1,40p' media_pipeline/exports/media/lbproto/lbproto_draft_01/gapseq_medium.csv
sed -n '1,40p' media_pipeline/exports/media/lbproto/lbproto_draft_01/reports/row_lineage.tsv
```

Optional sanity checks:

```bash
python3 scripts/media_pipeline_cli.py media review-mapping --medium-family lbproto --version lbproto_draft_01
python3 scripts/media_pipeline_cli.py media export-medium --medium-family lbproto --version lbproto_draft_01
python3 scripts/media_pipeline_cli.py media release-check --family lbproto --medium-version lbproto_draft_01
```

## What the prototype proves

- workbook-style formula families can be run outside LibreOffice
- decomposition stays explicit in tables
- curation stays explicit in tables
- upstream mapping stays explicit in tables
- viable export transformation stays explicit in tables
- final export, lineage, and basic validation can be reproduced deterministically

## What it does not prove yet

- QC floors/bump-ups
- release lifecycle and adapt pairing
- generalized aggregation hardening
- governance or override-policy frameworks
