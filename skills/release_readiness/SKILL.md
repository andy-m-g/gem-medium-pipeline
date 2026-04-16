# Release Readiness

This skill governs when a medium artifact or medium-related repo change is ready
to trust, share, or promote.

## Core Rule

An artifact is not release-ready just because it exists or passes structural
validation. Semantic clarity, provenance, explicit caveats, and correct layer
meaning must also be reviewable.

## Minimum Checks

- layer semantics are clear: source inventory, model-facing representation, and
  bound assignment are not collapsed
- provenance is explicit and reviewable
- unresolved components or remainders have not been silently lost
- upstream support is not overstated
- bound-assignment semantics are explicit and match the stated policy class
- pilots are labeled clearly as pilots and not presented as general rules
- caveats are present where the artifact needs them
- generated artifacts are not confused with canonical artifacts

## Typical Artifact Classes

- source inventory artifacts: ready when source meaning, units, and unresolved
  ingredients are explicit
- model-facing representation artifacts: ready when dissociation, salt-member
  expansion, viable export transformation, or proxy logic remain visible
- inventory-only bound artifacts: ready when they preserve availability without
  pretending to be uptake-rate caps
- concentration-derived availability-bound pilots: ready only when numeric
  semantics, unit meaning, and non-rate caveats are explicit
- partial rich-medium proxy artifacts: ready only when the represented fraction
  is narrow and the unresolved remainder remains first-class
- release-like exports: ready when canonical outputs, compatibility exports, and
  lineage are not being conflated

## Stop And Review When

- numeric bounds exist but their semantics are unclear
- an unresolved remainder disappears after adding explicit chemistry
- local placeholders are presented as if they were upstream-backed
- a pilot is starting to look like a general policy
- counterions, pooled source terms, or buffer terms are being overinterpreted

## Good Release-Ready Behavior

- explicit scope notes
- explicit caveat text where needed
- clear separation between canonical outputs and generated reports
- explicit policy labels such as `inventory_only` or
  `concentration_derived_availability_bound`
- bounded pilot scope with a visible stopping point

## Prevent

- trusting structural validation alone
- silent inventory-to-flux upgrades
- silent loss of unresolved ingredients or remainders
- overstated upstream backing
- treating a scoped pilot as a repo-wide rule
