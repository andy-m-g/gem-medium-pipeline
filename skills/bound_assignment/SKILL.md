# Bound Assignment

This skill governs the meaning of `bound_assignment.tsv` rows and the policy
classes used to connect explicit medium evidence to exchange-bound decisions.

## Core Rule

Inventory, availability bounds, and physiological uptake-rate caps are not
interchangeable.

## Policy Classes

- `inventory_only`: keep environmental availability explicit without assigning a
  numeric cap
- `concentration_derived_availability_bound`: record a numeric availability
  value derived from source concentration for a defined or fully resolved
  compound; this is not a biomass-normalized uptake rate
- `biomass_time_cap`: use a `mmol gDW^-1 h^-1` cap only when biomass and time
  support are explicit
- `depletion_informed_cap`: use a rate cap derived from depletion evidence over
  a defined interval
- `measured_rate_override`: use an explicit measured uptake-rate override with
  supporting normalization and time context
- `kinetic_cap`: use a kinetic-constraint cap when the row is justified by
  kinetic literature or equivalent evidence
- `heuristic_fallback`: use an explicit fallback cap only when stronger
  evidence is absent and the heuristic status remains visible
- `unresolved`: keep unresolved ingredients or remainders explicit with no
  direct exchange bound

## Practical Guardrails

- do not label concentration-derived values as measured uptake
- do not use `mmol gDW^-1 h^-1` without biomass normalization and time support
- do not assign numeric bounds to unresolved rich-medium remainder
- do not silently upgrade heuristic rows into stronger evidence classes
- do not treat `inventory_only` rows as hidden physiological caps
- do not assign numeric counterion bounds without explicit justification for why
  that source term should be bounded

## When To Use Which Class

- use `inventory_only` as the conservative default for source-supported medium
  presence
- use `concentration_derived_availability_bound` only for defined or fully
  resolved compounds when explicit curator approval exists
- use `biomass_time_cap`, `depletion_informed_cap`, or
  `measured_rate_override` only when the evidence actually supports
  physiological rate semantics
- use `kinetic_cap` when the cap is coming from kinetic evidence rather than
  direct depletion or direct uptake measurement
- use `heuristic_fallback` only as an acknowledged fallback with high
  uncertainty kept visible
- use `unresolved` when an ingredient remains chemically unresolved or should
  stay explicit without an exchange mapping

## Common Failure Modes

- treating `maxFlux`-like values as automatically physiological
- mixing source inventory semantics with uptake-rate semantics in one row
- assigning numeric bounds to counterions just because a dissociated source term
  exists
- treating concentration-derived pilot rows as if they were measured uptake
  overrides
- converting unresolved rich-medium rows into numeric exchange bounds without
  defensible proxy logic

## Good Repo Examples

- M9 inventory-only: the dissociated M9 rows in
  `sources/literature_test_media/literature_test_media_draft_01/bound_assignment_dissociated.tsv`
  stay `inventory_only` / `open_unbounded_inventory`
- M9 concentration-derived pilot: the scoped pilot in
  `sources/literature_test_media/literature_test_media_draft_01/concentration_derived_bound_pilot.tsv`
  uses `concentration_derived_availability_bound` for `D-glucose`,
  `Ammonium`, and `Phosphate` with explicit caveats
- unresolved rich-medium rows: unresolved ingredients remain visible as
  `unresolved` rows rather than being silently expanded into direct chemistry

## Prevent

- inventory-to-rate conflation
- silent policy upgrades
- hidden heuristic caps
- numeric bounds for unresolved remainder
- bound-assignment rows being used to hide representation or adaptation changes
