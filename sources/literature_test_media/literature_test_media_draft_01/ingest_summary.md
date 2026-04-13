# Literature Test Media Draft 01

This source-stage draft captures recipe rows extracted directly from the local PDFs in `validation/media/literature_test_media/`.

Included files:

- [source_recipe.tsv](/home/andy/Documents/bioreactor/media_pipeline/sources/literature_test_media/literature_test_media_draft_01/source_recipe.tsv)
- [source_composition.tsv](/home/andy/Documents/bioreactor/media_pipeline/sources/literature_test_media/literature_test_media_draft_01/source_composition.tsv)

Scope and boundaries:

- `source_recipe.tsv` contains directly stated recipe or formulation rows, including explicit stock additions where the PDF presents them that way.
- `source_composition.tsv` is present only for M9 because the PDF explicitly provides sub-composition for the `10X M9 SALTS` stock beyond the final medium rows.
- No composition rows were invented for peptones, extracts, digests, infusions, blood, bile salts, agar, or starch.
- Range and variant issues that do not fit the flat source schema cleanly are called out in the human-facing package under [extraction_notes.md](/home/andy/Documents/bioreactor/media_pipeline/results/media_recipes/extraction_notes.md).
