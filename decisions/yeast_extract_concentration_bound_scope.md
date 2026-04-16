# Yeast Extract Concentration Bound Scope

The current yeast-extract pilot is a partial explicit proxy inventory layer with
an explicitly retained unresolved remainder. Its purpose is to keep a small,
reviewable chemistry fraction visible without silently treating yeast extract as
fully resolved.

Current conclusion:

- do not create a numeric `concentration_derived_availability_bound` pilot for
  the existing yeast-extract proxy rows now

Why not:

- the current explicit rows already depend on an interpretive partial-proxy step
- adding numeric concentration-derived bounds would add a second assumption
  layer on top of that proxy logic
- this would risk blurring partial proxy inventory with fuller chemical
  resolution than the pilot actually supports

Safe future boundary:

- `Alanine` and `Glycine` are the safest possible later micro-pilot candidates
- even those should only be tested if a specific future use case justifies the
  extra assumption layer

Resulting guidance:

- keep the current yeast-extract proxy rows `inventory_only`
- keep the unresolved remainder explicit and without numeric bounds
- do not generalize `concentration_derived_availability_bound` into partial
  rich-medium proxy rows by default
