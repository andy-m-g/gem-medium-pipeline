# M9 Defined Concentration Artifact Deferred

Considered:

- creating a small defined-medium concentration-derived artifact for M9

The candidate contents would have been:

- `D-glucose`
- `Ammonium`
- `Phosphate`

Why this is not being implemented now:

- the current `concentration_derived_bound_pilot.tsv` already serves the
  intended review and policy-testing purpose
- `Phosphate` is already the semantic edge case for this policy in M9
- adding another named artifact would add structure faster than it adds clarity
- the repo should avoid making this look like a default export pattern for
  defined media

Resulting guidance:

- keep the current pilot as the explicit numeric exception
- keep `inventory_only` as the default conservative layer
- revisit a named M9-defined concentration-derived artifact only if repeated
  reuse or sharing clearly justifies it
