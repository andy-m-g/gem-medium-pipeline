# Bound Assignment Artifact

This note records the purpose and use of the `bound_assignment.tsv` artifact introduced for the prototype media pipeline.

Purpose:

- preserve explicit curator-facing records for how model-facing exchange bounds were assigned
- keep the distinction visible between laboratory medium inventory and model uptake constraints
- connect source-side medium evidence to exchange-bound decisions without hiding the judgment in code

Core rule:

- medium inventory is not uptake flux
- recipe concentration or source composition can justify that a compound is available in the environment
- a biomass-normalized uptake bound in `mmol gDW^-1 h^-1` requires stronger evidence, additional assumptions, or both

How this artifact fits the pipeline:

- upstream source tables such as `source_recipe.tsv` and `source_composition.tsv` capture what the laboratory medium contains
- decomposition, mapping, and viable-export stages determine what explicit model-facing compounds can be represented
- `bound_assignment.tsv` is the row-level bridge between that explicit chemical layer and the bound values eventually used for exchange constraints
- rows can represent either:
  - a direct exchange-level assignment
  - an explicitly unresolved ingredient that is being kept visible with no direct exchange bound

Practical use:

- use one row per exchange reaction when the mapped metabolite and bound are unambiguous
- use an unresolved row when a rich-medium ingredient remains chemically unresolved and should not be silently converted into a direct exchange constraint
- keep provenance explicit through `formula_type`, `evidence_type`, `provenance_label`, `uncertainty_level`, `curator_decision`, and `citation_source`
- treat the template under [bound_assignment.tsv](/home/andy/Documents/bioreactor/media_pipeline/templates/tsv/bound_assignment.tsv) as the canonical starter table
- validate the header and controlled vocabularies against [tsv.bound_assignment.yaml](/home/andy/Documents/bioreactor/media_pipeline/schemas/tsv.bound_assignment.yaml)

Optional concentration-derived availability policy:

- `concentration_derived_availability_bound` records a numeric bound-like value derived directly from medium concentration for a defined or fully resolved compound.
- This policy is supported as an optional mode and as a legacy-compatible representation for historical CIM/BHI-style spreadsheet exports.
- It differs from `inventory_only` because it assigns a numeric model-facing availability value rather than leaving the exchange open.
- It differs from `biomass_time_cap` because it is not a `mmol gDW^-1 h^-1` uptake-rate estimate and does not use biomass or time normalization.
- It differs from `heuristic_fallback` because the primary numeric value comes from source concentration or an explicit concentration conversion rather than from a fallback cap chosen mainly by heuristic judgment.
- This policy requires explicit curator approval, should normally use `bound_unit = mmol L^-1 inventory`, and must not be interpreted as a measured uptake rate.
- It is not the default policy for source inventory, and it should not be used for unresolved rich-medium remainders.
- Supporting rationale and terminology notes are recorded in `/home/andy/Documents/bioreactor/media_pipeline/undermind/flux_calculation/Availability_bounds_from_medium_composition_report.pdf`.

Undermind evidence bundle:

- the evidence and planning bundle used for this artifact lives locally under:
  `/home/andy/Documents/bioreactor/media_pipeline/undermind/bulk_ingredient_adaptation`
- specifically:
  - `0_Rich_medium_proxy_decisions_for_GEM.pdf`
  - `1_Evidence_ranked_flux_assignment_for_GEM_media.pdf`
  - `2_Operational_bound_assignment_checklist.pdf`
  - `3_Bound_assignment_schema_specification.pdf`
  - `4_Bound_assignment_TSV_template.pdf`
  - `5_Bound_assignment_validator_rule_matrix.pdf`
- a separate local note on concentration-derived availability encoding also lives under:
  `/home/andy/Documents/bioreactor/media_pipeline/undermind/flux_calculation/Availability_bounds_from_medium_composition_report.pdf`

Boundary:

- this artifact does not change existing medium drafts, exports, or validation outputs
- it adds an explicit place to record how a curator moved from medium evidence to exchange-bound decisions
- it is not a new policy engine and it does not imply automatic conversion from source concentration to uptake rate
