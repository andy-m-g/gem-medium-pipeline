# Medium Layers

This skill governs the conceptual layer separation used when constructing
medium artifacts in this repository.

## Core Rule

Do not silently collapse these layers:

- source inventory
- model-facing representation
- bound assignment
- adaptation

## Definitions

- source inventory: what the source recipe, stock, or composition says is in the
  laboratory medium
- model-facing representation: the explicit chemical form exposed to the model
  after dissociation, salt-member expansion, viable export transformation, or
  related translation
- bound assignment: the explicit policy that records how represented compounds
  are treated for exchange-bound purposes
- adaptation: model supplementation or exchange/reaction changes that alter what
  the model can use, not what the medium contains

## Practical Rules

- source inventory is not automatically uptake flux
- recipe or stock concentration is environmental inventory evidence, not a
  biomass-normalized uptake rate
- dissociation or viable export transformation is not the same as assigning
  lower bounds
- adaptation changes model capability, not medium composition
- unresolved components must remain explicit unless defensible proxy logic
  exists and is recorded explicitly
- bound assignment must stay visible as a separate policy layer even when using
  `inventory_only` or `concentration_derived_availability_bound`

## Common Failure Modes

- treating recipe concentration as a measured uptake rate
- hiding dissociation or salt-splitting logic inside bound assignment
- silently converting unresolved rich ingredients into explicit chemistry
- conflating medium fixes with exchange/reaction adaptation
- using adaptation-style changes to paper over missing medium representation

## Good Repo Changes

- add a source-stage artifact that captures inventory more explicitly
- add a companion dissociation or viable-representation layer with lineage
- add an explicit bound-assignment policy artifact without changing source-stage
  meaning
- add an adaptation manifest or pattern record separately from medium
  composition artifacts

## Prevent

- silent inventory-to-flux conversion
- hidden representation logic inside bound assignment
- hidden adaptation inside medium artifacts
- silent resolution of unresolved components
- terminology drift that erases the current layer contract
