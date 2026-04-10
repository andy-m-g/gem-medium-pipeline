# Earlier Workbook Prototype Example

This example is a reduced, explicit flat-file reconstruction of the earlier workbook logic. It is intentionally small:

- `Yeast Extract`
- `NaCl`
- `Lactic acid`
- a few representative decomposition rows
- explicit background-species insertions (`O2`, `H2O`, `H+`)
- direct mapping into a gapseq/SEED-like namespace
- explicit viable-export rules after mapping

It is not a full reproduction of the workbook. It is a vertical slice that exercises:

1. `source_capture`
2. `decomposition`
3. `normalize_and_convert`
4. `curation_review`
5. `map_to_upstream_namespace`
6. `viable_export_transformation`
7. `final_medium_export`
8. `row_lineage`
9. `validation`

The viable transformation example includes:

- `direct_export` for `Alanine`
- `salt_split_member` for `Sodium chloride -> Sodium + Cl-`
- `polymer_proxy` for `Cellulose -> D-Cellobiose`
- `chemical_form_change` for `Lactic acid -> L-Lactate`

Use the repo-level prototype README for exact commands.
