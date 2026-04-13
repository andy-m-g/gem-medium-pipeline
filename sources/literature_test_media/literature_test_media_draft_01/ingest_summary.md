# Literature Test Media Draft 01

This source-stage draft captures recipe rows extracted directly from the local PDFs in `validation/media/literature_test_media/`.

Included files:

- [source_recipe.tsv](/home/andy/Documents/bioreactor/media_pipeline/sources/literature_test_media/literature_test_media_draft_01/source_recipe.tsv)
- [source_composition.tsv](/home/andy/Documents/bioreactor/media_pipeline/sources/literature_test_media/literature_test_media_draft_01/source_composition.tsv)
- [bound_assignment.tsv](/home/andy/Documents/bioreactor/media_pipeline/sources/literature_test_media/literature_test_media_draft_01/bound_assignment.tsv)
- [m9_dissociation_mapping.tsv](/home/andy/Documents/bioreactor/media_pipeline/sources/literature_test_media/literature_test_media_draft_01/m9_dissociation_mapping.tsv)
- [bound_assignment_dissociated.tsv](/home/andy/Documents/bioreactor/media_pipeline/sources/literature_test_media/literature_test_media_draft_01/bound_assignment_dissociated.tsv)

Scope and boundaries:

- `source_recipe.tsv` contains directly stated recipe or formulation rows, including explicit stock additions where the PDF presents them that way.
- `source_composition.tsv` is present only for M9 because the PDF explicitly provides sub-composition for the `10X M9 SALTS` stock beyond the final medium rows.
- `bound_assignment.tsv` currently contains a first concrete inventory-only bound table for `M9 broth` as the cleanest directly translatable case from this package.
- `m9_dissociation_mapping.tsv` adds an explicit M9-only companion representation layer from source inventory to model-facing compound members.
- `bound_assignment_dissociated.tsv` keeps the dissociated M9 members at `inventory_only` / `open_unbounded_inventory`; it does not assign biomass-normalized uptake caps.
- No composition rows were invented for peptones, extracts, digests, infusions, blood, bile salts, agar, or starch.
- Range and variant issues that do not fit the flat source schema cleanly are called out in the human-facing package under [extraction_notes.md](/home/andy/Documents/bioreactor/media_pipeline/results/media_recipes/extraction_notes.md).

M9 companion dissociation notes:

- The original recipe-level M9 inventory remains intact and unchanged.
- The dissociation layer is a companion model-facing representation derived from that source inventory, not a replacement for it.
- Source recipe inventory is not uptake flux, and the dissociated representation is not a flux cap.
- Phosphate is represented conservatively as a source-term `Phosphate` member contributed by both `Na2HPO4` and `KH2PO4`; no detailed aqueous phosphate-buffer speciation is attempted here.
- Members lacking current local upstream snapshot support are intentionally emitted as `local_proxy_or_override` / `local_only_expected` and remain local-only pending a separate upstream-snapshot curation task.
