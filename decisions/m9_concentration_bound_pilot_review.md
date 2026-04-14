# M9 Concentration Bound Pilot Review

Current pilot status:

- The pilot row in [concentration_derived_bound_pilot.tsv](/home/andy/Documents/bioreactor/media_pipeline/sources/literature_test_media/literature_test_media_draft_01/concentration_derived_bound_pilot.tsv) is:
  - `D-glucose`
  - `cpd00027`
  - `EX_cpd00027_e0`
  - `11.102 mmol L^-1 inventory`
- It is derived from source recipe row `src_ltm_m9b_004` (`40% glucose`, `5 mL/L`) and dissociation/mapping row `m9d_001`.

Why this is not a measured uptake flux:

- The value is calculated from final medium concentration, not from depletion, biomass normalization, or a time interval.
- The row explicitly records `biomass_normalization = not applied` and leaves `time_window` empty.
- The note states that it is not a measured uptake rate and not a biomass-normalized flux cap.

Policy fit:

- The row follows the new `concentration_derived_availability_bound` policy in the current schema and documentation.
- `formula_type`, `provenance_label`, `bound_unit`, `curator_decision`, and the explanatory note all match the intended optional / legacy-compatible policy shape.

Manual review before generalizing:

- Confirm whether `11.102` is the preferred rounding convention or whether future rows should keep more decimal places.
- Confirm that `mmol L^-1 inventory` is the preferred unit label for all concentration-derived availability rows.
- Confirm that `set_upper_bound` is the best curator decision label for this policy.
- Consider whether provenance should later be split into dedicated source-row and mapping-row fields instead of a combined citation string.
- Confirm whether `0.5,1,2` should remain the default sensitivity multipliers for this policy class.

Recommended next expansion:

- Add `Ammonium` and `Phosphate` next as additional defined M9 pilots, not the full M9 medium yet.
- Keep those rows as `concentration_derived_availability_bound` only, not as biomass-normalized uptake rates.
