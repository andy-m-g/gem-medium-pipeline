# Medium Layer Contract

This note defines the working boundary between source-medium evidence,
model-facing chemical representation, and exchange-bound assignment in the MVP
pipeline.

## Purpose

- keep medium inventory distinct from model uptake constraints
- preserve short, explicit contracts for later diet adaptation and
  model-facing medium construction
- keep provenance and uncertainty visible instead of hiding decisions in code

## Layer contract

### 1. Source inventory layer

- `source_recipe.tsv` and `source_composition.tsv` record what the laboratory
  medium contains as stated by the source.
- This layer supports explicit ingredient and stock-member inventory capture.
- This layer does not by itself assign exchange reactions or uptake caps.
- Recipe concentration, stock concentration, and final broth concentration are
  environmental inventory evidence, not biomass-normalized uptake flux.

### 2. Model-facing chemical representation layer

- A companion representation layer may be needed when source ingredients are not
  in the chemical form required for model exchange handling.
- Dissociation, salt-member expansion, or other viable representation steps are
  model-facing translation steps derived from source inventory.
- This layer is distinct from flux assignment: it decides how inventory is
  represented to the model, not how much uptake is allowed.

### 3. Bound-assignment layer

- `bound_assignment.tsv` records how a represented ingredient or compound is
  being treated for exchange-bound purposes.
- The table must support both:
  - inventory-only rows that keep availability explicit without imposing a cap
  - future capped rows when stronger uptake evidence exists
- The default conservative rule is that recipe inventory is not uptake flux.

### 4. Future capped-bound layer

- Actual uptake caps are appropriate only when the evidence supports moving from
  environmental presence to a flux constraint.
- Useful evidence classes include:
  - direct recipe inventory
  - partial rich-medium proxy inventory
  - depletion-informed bounds
  - measured uptake overrides
  - heuristic caps
- These classes should stay explicit so later users can distinguish source
  evidence from stronger or weaker flux-setting assumptions.

### 5. Validation and adaptation interaction

- Medium representation and bound assignment affect later model adaptation, but
  they should remain analytically distinct from it.
- Validation should check whether the represented medium is explicit,
  traceable, and internally consistent.
- Adaptation can then use that explicit medium as evidence without collapsing
  representation decisions, uptake-cap decisions, and model-gap decisions into a
  single step.

## Current operational rule for M9

- source inventory remains intact in `source_recipe.tsv` and
  `source_composition.tsv`
- `m9_dissociation_mapping.tsv` is a companion model-facing representation layer
- `bound_assignment_dissociated.tsv` remains `inventory_only` /
  `open_unbounded_inventory`
- no uptake caps are assigned yet

For `literature_test_media_draft_01`, this means the dissociated M9 layer is a
conservative model-facing inventory view only. It does not replace the source
inventory and it does not yet justify biomass-normalized exchange limits.
