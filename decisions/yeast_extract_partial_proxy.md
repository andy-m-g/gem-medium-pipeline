# Yeast Extract Partial-Proxy Pilot

This note defines a first curator-facing pilot for representing `yeast extract`
as a small explicit chemistry fraction plus an explicit unresolved remainder.

Purpose:

- test a conservative artifact shape for partial rich-medium proxy inventory
- keep the represented fraction reviewable instead of silently expanding yeast
  extract into a full composition
- preserve the unresolved remainder as a first-class artifact

Working rule for this pilot:

- `yeast_extract_partial_proxy.tsv` captures only a small explicit fraction of
  yeast extract chemistry that is supported by preserved local evidence and the
  refreshed local upstream snapshot
- `yeast_extract_partial_proxy_bound_assignment.tsv` translates only those
  explicit proxy rows into the existing `bound_assignment` contract
- the unresolved remainder stays explicit and is not translated into exchange-
  level chemistry

Boundaries:

- this is a yeast-extract-only pilot, not a general rich-medium policy
- this layer remains inventory-only
- recipe inventory is not uptake flux
- no biomass-normalized uptake caps are assigned here
- no row should be interpreted as a full decomposition of yeast extract

Evidence posture:

- the source-stage literature extraction continues to treat yeast extract as an
  unresolved composite ingredient
- the explicit proxy rows here are a narrow add-on derived from preserved local
  yeast-related curation evidence under
  `/home/andy/Documents/bioreactor/data/dev/diet/LB_Steps_autolysed_yeast_nofatty acids.ods`
- compounds were included only when they are both explicitly listed in that
  preserved local workbook and present in the refreshed local
  `gapseq_seed_like` snapshot

Intentional non-goals:

- no hidden or automatic extension to tryptone, peptone, BHI, blood, or other
  rich ingredients
- no automatic uptake caps
- no automatic carry-over from partial proxy inventory into adaptation logic
