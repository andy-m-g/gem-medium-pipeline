# M9 Concentration Bound Scope

The current M9 concentration-derived availability-bound pilot includes:

- `D-glucose`
- `Ammonium`
- `Phosphate`

This is intentionally a limited pilot. `Phosphate` is the upper semantic edge of
the current policy because it is already a pooled model-facing source term
assembled from `Na2HPO4` and `KH2PO4`, and it requires an explicit caveat that
it is not full aqueous phosphate speciation, not a measured uptake rate, and
not a biomass-normalized flux cap.

The remaining dissociated M9 compounds were reviewed:

- `Sodium`
- `Potassium`
- `Cl-`
- `Magnesium`
- `Sulfate`
- `Calcium`

Current classification:

- `Magnesium` and `Sulfate`: borderline only with strong caveat
- `Sodium`, `Potassium`, `Cl-`, and `Calcium`: keep `inventory_only` for now

Resulting guidance:

- do not generalize `concentration_derived_availability_bound` to all
  dissociated ions
- stop the current M9 concentration-derived pilot here unless there is a
  specific reason to test `Magnesium` or `Sulfate` separately
- for the remaining M9 ion/source-term rows, `inventory_only` remains the
  default policy
