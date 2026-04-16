# Rich Ingredients

This skill governs how the repo handles rich or unresolved medium ingredients
that are not directly GEM-ready at source stage.

## What Counts

Typical cases include:

- yeast extract
- tryptone and other peptones or digest peptones
- meat extract
- brain or heart infusion
- blood
- agar and other structural solidifiers
- other named bulk ingredients that do not expose metabolite-level composition

## Core Rule

Unresolved ingredients remain unresolved unless explicit composition or
defensible partial proxy support exists.

## Allowed Handling Modes

- leave unresolved: keep the ingredient explicit as source inventory or as an
  unresolved bound-assignment row with no silent chemistry expansion
- partial explicit proxy plus unresolved remainder: represent only the narrow
  supported fraction and retain the unresolved remainder as a first-class
  artifact
- direct explicit chemistry: use only when the source or separately curated
  evidence truly supports explicit composition for that ingredient

## Prohibited

- hidden full decomposition of peptones, extracts, infusions, blood, or agar
- treating proxy chemistry as if it were full composition
- dropping the unresolved remainder silently after adding a proxy fraction
- assigning numeric bounds to unresolved remainder
- using bound assignment to hide missing composition evidence

## Repo Examples

- yeast-extract partial proxy pilot: a small explicit amino-acid fraction is
  represented in `decisions/yeast_extract_partial_proxy.tsv`, while the
  unresolved remainder stays explicit and inventory-only in
  `decisions/yeast_extract_partial_proxy_bound_assignment.tsv`
- M9 agar unresolved handling: `agar` remains an explicit unresolved row rather
  than being silently decomposed into nutrient chemistry
- literature-test-media extraction: `results/media_recipes/bulk_unresolved_ingredients.tsv`
  keeps peptones, extracts, infusions, blood, agar-like materials, and other
  bulk ingredients visible as unresolved source-stage classes

## Decision Criteria

A proxy is defensible when:

- the represented fraction is explicitly supported by curated source material or
  preserved local evidence
- the scope is narrow and stated as partial rather than full composition
- the represented compounds are concrete enough to map or carry forward
  explicitly
- the unresolved remainder is retained and documented

A proxy is not yet defensible when:

- the ingredient is named only as a bulk material with no metabolite-level
  support
- the proposed chemistry depends on assumption stacking or generic folklore
- the remainder would disappear from the record
- the representation would imply stronger bound or adaptation claims than the
  evidence supports

## Common Failure Modes

- expanding rich ingredients automatically because they are common media terms
- equating vendor-style ingredient names with explicit chemistry
- letting a partial proxy masquerade as complete decomposition
- converting unresolved remainder into exchange-level rows
- mixing structural solidifier handling with nutrient availability claims
