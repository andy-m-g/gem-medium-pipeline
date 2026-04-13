# Extraction Notes

## PDFs processed

- `/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/BHI/53286dat.pdf`
- `/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/blood_agar/TS-4011564.pdf`
- `/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/FTM/IFU112640.pdf`
- `/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/LB/MR_LB.pdf`
- `/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/M9/MEDIA-M1.pdf`
- `/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/macconkey_agar/IFU453801.pdf`
- `/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/RCM/27546dat.pdf`
- `/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/TSB/22092dat.pdf`

## Parse failures

- No complete parse failures.
- `TS-4011564.pdf` and `IFU453801.pdf` are copy-restricted PDFs, but `pdftotext -layout` still yielded usable local text in this environment.

## Ambiguities

- Blood agar supplementation is stated as `5-7%` blood rather than a single scalar amount. The human-facing extraction preserves the percentage wording; the pipeline-native `source_recipe.tsv` represents the same addition as `50-70 mL/L` in a visible note-bearing way so the current schema can still carry it.
- M9 agar says to add ingredients `as for broth`; the extracted rows repeat the broth additions explicitly in the human-facing package, but the quote snippets keep the indirection visible.
- M9 broth notes `Do Not add CaCl2 for Pseudomonas`. This was preserved in notes but not treated as a separate variant because the PDF presents it as a conditional note rather than a full alternate recipe block.
- The supplier sheets often distinguish dehydrated preparation mass (`Suspend X g in 1 L`) from the ingredient formulation table. The extraction package prioritizes the formulation tables for ingredient rows and keeps the preparation mass only in notes or snippets when useful.

## OCR usage

- No OCR was used.
- All text was extracted from the local PDFs with `pdftotext -layout`.

## Missing page numbers

- No missing page numbers for the extracted recipe claims.
- All formulation claims used here came from page 1 of the relevant PDF.

## Multiple variants in one PDF

- `TS-4011564.pdf`: captured both `Blood Agar Base N° 2` and the supplemented blood-added variant.
- `MR_LB.pdf`: captured the broth recipe and the agar addition note as a separate agar variant.
- `MEDIA-M1.pdf`: captured three explicit formulations: `10X M9 salts stock`, `M9 broth`, and `M9 agar`.

## Normalization decisions

- `ingredient_name_raw` preserves source wording, capitalization, and parenthetical qualifiers where present.
- `ingredient_name_normalized` was kept conservative and mostly lowercased with light normalization (`D(+)-Glucose` to `D-glucose`, `NaCl` to `sodium chloride`, `dH2O` to `deionized water`).
- Stock labels such as `1 M MgSO4` and `40% glucose` were preserved as stock-form additions rather than silently converted to final molar or mass concentrations.
- Agar and starch were treated as unresolved polymeric materials for GEM purposes even when chemically named, because this package is meant for metabolite-level training support and these rows still require explicit downstream representation decisions.
- `Bile Salts` were treated conservatively as unresolved mixed material because the PDF does not specify a defined salt composition.

## Path and layout decisions

- Human-facing outputs were written under `/home/andy/Documents/bioreactor/media_pipeline/results/media_recipes/`.
- Pipeline-native outputs were written under `/home/andy/Documents/bioreactor/media_pipeline/sources/literature_test_media/literature_test_media_draft_01/`.
- The human-facing package is broader: it preserves summary rows, variant distinctions, bulk flags, and quote snippets intended for review and training.
- The pipeline-native draft is narrower: it maps the same source-grounded recipe facts into the repo’s existing `source_recipe.tsv` and `source_composition.tsv` conventions without inventing metabolite composition for complex ingredients.

## Pipeline-native outputs

- Yes. Pipeline-native outputs were also created.
- Relationship:
  - `results/media_recipes/` is the review-oriented extraction package.
  - `sources/literature_test_media/literature_test_media_draft_01/` is the source-stage package aligned to existing pipeline conventions.
