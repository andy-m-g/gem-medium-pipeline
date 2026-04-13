# Media Recipe Extraction Package

This package captures source-grounded recipe rows from local supplier or literature-style PDFs under `validation/media/literature_test_media/`. It is intentionally conservative: original wording is preserved, page-level provenance is attached to each extracted claim, and unresolved composite ingredients remain unresolved rather than being decomposed implicitly for GEM use.

## BHI

What it is: Brain Heart Broth (`53286 Brain Heart Broth`).

Typical use: Cultivation of various fastidious, pathogenic microorganisms including yeasts and molds; also examination of water, wastewater, meat, and foods.

Defined / semi-defined / undefined-complex classification: `undefined-complex`

Readable ingredient list:
- Calf brains (infusion from 200g), 12.5 g/L
- Beef heart (infusion from 250g), 5.0 g/L
- Peptone, 10.0 g/L
- Sodium chloride, 5.0 g/L
- D(+)-Glucose, 2.0 g/L
- Disodium hydrogen phosphate, 2.5 g/L

Source PDF and page: [53286dat.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/BHI/53286dat.pdf), page 1

Source/reference as stated: `53286 Brain Heart Broth`

GEM relevance note: Brain and heart infusions plus generic peptone are unresolved bulk ingredients. They should remain unresolved at source capture unless an independent composition source is curated.

## Blood Agar

What it is: `Blood Agar Base N° 2`, with an explicit supplemented variant prepared by adding blood after reconstitution.

Typical use: Isolation and cultivation of fastidious and non-fastidious microorganisms and determination of haemolytic properties.

Defined / semi-defined / undefined-complex classification: `undefined-complex`

Readable ingredient list for base:
- Peptone, 15.0 g/L
- Liver extract, 2.5 g/L
- Yeast extract, 5.0 g/L
- Sodium chloride, 5.0 g/L
- Agar, 13.0 g/L

Readable ingredient list for supplemented variant:
- Blood Agar Base N° 2 as above
- Sterile defibrinated sheep or horse blood, 5-7% v/v addition after cooling

Source PDF and page: [TS-4011564.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/blood_agar/TS-4011564.pdf), page 1

Source/reference as stated: `TS-401156 rev 3 2023/04`

GEM relevance note: The base already contains unresolved extract and peptone materials. The supplemented variant adds defibrinated animal blood, which is also not directly GEM-ready.

## FTM

What it is: Fluid Thioglycollate Medium (`Thioglycollate Medium w/ Indicator and Dextrose`) classical formula.

Typical use: General-purpose liquid medium for qualitative cultivation of aerobes and anaerobes and for sterility testing.

Defined / semi-defined / undefined-complex classification: `undefined-complex`

Readable ingredient list:
- Casein Peptone, 15.0 g/L
- Yeast Extract, 5.0 g/L
- Dextrose, 5.0 g/L
- Sodium Chloride, 2.5 g/L
- L-Cystine, 0.5 g/L
- Sodium Thioglycollate, 0.5 g/L
- Resazurin, 1.0 mg/L
- Agar, 0.75 g/L

Source PDF and page: [IFU112640.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/FTM/IFU112640.pdf), page 1

Source/reference as stated: `IFU 112640, Revised June 20, 2013`

GEM relevance note: Casein peptone and yeast extract remain unresolved. Low agar is also not directly metabolite-level.

## LB

What it is: LB (Luria-Bertani Medium), with a broth recipe and an agar addition note.

Typical use: General rich growth medium; the local PDF is a CCAP preparation recipe adapted from Bertani 1951.

Defined / semi-defined / undefined-complex classification: `undefined-complex`

Readable ingredient list for broth:
- Tryptone, 10.0 g/L
- NaCl, 10.0 g/L
- Yeast extract, 5.0 g/L

Readable ingredient list for agar:
- LB broth as above
- Bacteriological Agar, 15 g/L

Source PDF and page: [MR_LB.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/LB/MR_LB.pdf), page 1

Source/reference as stated: `Bertani, G (1951) Studies on lysogenesis. I. The mode of phage liberation by lysogenic Escherichia coli. J. Bacteriol. 62 (3): 293–300 – adapted for CCAP`

GEM relevance note: Tryptone and yeast extract are unresolved composite ingredients. Agar requires either proxy handling or later exclusion with provenance.

## M9

What it is: M9 minimal medium with an explicit 10X salts stock, broth preparation, and agar preparation.

Typical use: Defined minimal medium for broth or agar culture.

Defined / semi-defined / undefined-complex classification:
- `defined` for the 10X salts stock
- `defined` for the broth recipe
- `semi-defined` for the agar variant because agar is unresolved for GEM encoding

Readable ingredient list for 10X stock:
- Na2HPO4, 60 g per 1 L stock
- KH2PO4, 30 g per 1 L stock
- NaCl, 5 g per 1 L stock
- NH4Cl, 10 g per 1 L stock
- dH2O to 1 litre

Readable ingredient list for broth:
- 900 mL dH2O
- 100 mL 10X M9 salts
- 2 mL 1 M MgSO4
- 0.1 mL 1 M CaCl2
- 5 mL 40% glucose

Readable ingredient list for agar:
- 900 mL dH2O
- 20 g agar
- ingredients as for broth after cooling

Source PDF and page: [MEDIA-M1.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/M9/MEDIA-M1.pdf), page 1

Source/reference as stated: `Molecular Cloning, A Laboratory Manual 1st ed. Maniatis. 1982. p.68.`

GEM relevance note: The broth and stock are fully explicit at source level. The agar variant remains non-direct only because agar itself is a polymeric solidifier.

## MacConkey Agar

What it is: Classical MacConkey Agar formula.

Typical use: Selective and differential isolation of gram-negative bacilli on the basis of lactose fermentation.

Defined / semi-defined / undefined-complex classification: `undefined-complex`

Readable ingredient list:
- Gelatin Peptone, 17.0 g/L
- Meat Peptone, 1.5 g/L
- Lactose, 10.0 g/L
- Neutral Red, 30.0 mg/L
- Sodium Chloride, 5.0 g/L
- Crystal Violet, 1.0 mg/L
- Bile Salts, 1.5 g/L
- Casein Peptone, 1.5 g/L
- Agar, 13.5 g/L

Source PDF and page: [IFU453801.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/macconkey_agar/IFU453801.pdf), page 1

Source/reference as stated: `IFU 453801, Revised September 30, 2010`

GEM relevance note: Multiple digest materials plus bile salts and agar are unresolved for direct metabolite-level export.

## RCM

What it is: Reinforced Clostridial Medium (`27546 Clostridial Nutrient Medium`).

Typical use: Cultivation and enumeration of clostridia and other anaerobes as well as facultative microorganisms.

Defined / semi-defined / undefined-complex classification: `undefined-complex`

Readable ingredient list:
- Meat extract, 10.0 g/L
- Peptone, 5.0 g/L
- D(+)-Glucose, 5.0 g/L
- Yeast extract, 3.0 g/L
- Starch, 1.0 g/L
- Sodium chloride, 5.0 g/L
- Sodium acetate, 3.0 g/L
- L-Cysteine hydrochloride, 0.5 g/L
- Agar, 0.5 g/L

Source PDF and page: [27546dat.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/RCM/27546dat.pdf), page 1

Source/reference as stated: `27546 Clostridial Nutrient Medium (Reinforced Clostridial Medium; RCM)`

GEM relevance note: Meat extract, peptone, yeast extract, starch, and agar all require explicit downstream handling rather than silent decomposition.

## TSB

What it is: Tryptic Soy Broth (`22092 Tryptic Soy Broth`).

Typical use: Rich broth for luxuriant growth of many fastidious organisms; also noted for Campylobacter jejuni motility-test confirmation.

Defined / semi-defined / undefined-complex classification: `undefined-complex`

Readable ingredient list:
- Casein peptone (pancreatic), 17.0 g/L
- Soya peptone (papain digest.), 3.0 g/L
- Sodium chloride, 5.0 g/L
- Dipotassium hydrogen phosphate, 2.5 g/L
- Glucose, 2.5 g/L

Source PDF and page: [22092dat.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/TSB/22092dat.pdf), page 1

Source/reference as stated: `22092 Tryptic Soy Broth (TSB, (Tryptone Soya Broth, CASO Broth, Soybean Casein digest Broth, Casein Soya Broth)`

GEM relevance note: Both peptone rows are unresolved digest materials and should remain unresolved unless an explicit composition source is later added.

## Bulk or unresolved ingredients that need extra determination for GEM translation

These ingredients were intentionally not decomposed in this package:
- Infusions: calf brain infusion, beef heart infusion
- Extracts: liver extract, yeast extract, meat extract
- Peptones and digests: peptone, casein peptone, tryptone, gelatin peptone, meat peptone, soya peptone
- Blood material: sterile defibrinated sheep or horse blood
- Mixed or polymeric materials: bile salts, agar, starch

Each is listed in [bulk_unresolved_ingredients.tsv](/home/andy/Documents/bioreactor/media_pipeline/results/media_recipes/bulk_unresolved_ingredients.tsv) with the reason it is not yet GEM-ready and a conservative example path to resolution.

## References

- `53286 Brain Heart Broth`; local PDF: [53286dat.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/BHI/53286dat.pdf)
- `TS-401156 rev 3 2023/04`; local PDF: [TS-4011564.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/blood_agar/TS-4011564.pdf)
- `IFU 112640, Revised June 20, 2013`; local PDF: [IFU112640.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/FTM/IFU112640.pdf)
- `Bertani, G (1951) Studies on lysogenesis. I. The mode of phage liberation by lysogenic Escherichia coli. J. Bacteriol. 62 (3): 293–300 – adapted for CCAP`; local PDF: [MR_LB.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/LB/MR_LB.pdf)
- `Molecular Cloning, A Laboratory Manual 1st ed. Maniatis. 1982. p.68.`; local PDF: [MEDIA-M1.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/M9/MEDIA-M1.pdf)
- `IFU 453801, Revised September 30, 2010`; local PDF: [IFU453801.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/macconkey_agar/IFU453801.pdf)
- `27546 Clostridial Nutrient Medium (Reinforced Clostridial Medium; RCM)`; local PDF: [27546dat.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/RCM/27546dat.pdf)
- `22092 Tryptic Soy Broth (TSB, (Tryptone Soya Broth, CASO Broth, Soybean Casein digest Broth, Casein Soya Broth)`; local PDF: [22092dat.pdf](/home/andy/Documents/bioreactor/media_pipeline/validation/media/literature_test_media/TSB/22092dat.pdf)
