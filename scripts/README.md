Utility scripts used for explicit maintenance tasks live here.

`refresh_gapseq_seed_snapshot.py` refreshes the frozen local
`upstream_snapshots/gapseq_seed_like/` reference from
gapseq's `dat/seed_metabolites_edited.tsv`. It is an explicit import step and is
not part of ordinary medium processing or validation.
