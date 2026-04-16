# Upstream Snapshot Validation

This skill governs how the repo uses frozen upstream reference snapshots and
how local-only versus upstream-backed identifiers should be treated during
validation.

## Core Rule

Ordinary validation uses frozen local snapshots, not live upstream queries.

## Why

- reproducibility: the same draft should validate against the same local
  reference set
- provenance: the snapshot manifest records where the imported reference came
  from and when it was refreshed
- reviewability: upstream expansion happens through explicit files that can be
  inspected and compared
- offline stability: normal pipeline behavior must not depend on live network or
  live GitHub availability

## Alignment Classes

- directly upstream-backed: the current frozen snapshot contains the compound id
  and supports claiming upstream-backed status
- inferred from convention: a local representation may follow repo convention or
  companion mapping logic, but it is not upstream-backed unless the current
  snapshot actually contains it
- local proxy or override: explicit local placeholder, proxy, or curator
  override retained for workflow clarity without pretending it was validated
  upstream
- unresolved or local-only expected: rows intentionally kept visible as local
  placeholders or unresolved cases until snapshot coverage or separate curation
  expands

## Refresh Behavior

- upstream expansion happens through explicit snapshot refresh or import, not
  silently during normal runs
- the maintenance utility is `scripts/refresh_gapseq_seed_snapshot.py`
- the frozen `gapseq_seed_like` snapshot lives under
  `upstream_snapshots/gapseq_seed_like/`
- ordinary validation reads local `compounds.tsv` and
  `snapshot_manifest.json`; it does not fetch live upstream data

## Practical Guardrails

- do not claim upstream support if the current frozen snapshot does not support
  it
- do not hide local placeholders or proxy rows as if they were validated
  upstream ids
- do not make runtime validation depend on live GitHub, remote TSV fetches, or
  mutable external state
- do not treat a refresh-capable maintenance script as ordinary validation
  behavior
- do not erase the distinction between upstream-backed cleanup and local-only
  expected rows

## Repo Examples

- M9 dissociation cleanup: several dissociated M9 source terms now map to
  upstream-backed ids in the refreshed local `gapseq_seed_like` snapshot, but
  that support comes from the frozen local snapshot used at validation time
- local snapshot refresh: `scripts/refresh_gapseq_seed_snapshot.py` imports
  `dat/seed_metabolites_edited.tsv` into local `compounds.tsv` plus
  `snapshot_manifest.json` as an explicit maintenance step

## Common Failure Modes

- treating live upstream availability as the validation truth instead of the
  frozen local snapshot
- claiming a local convention-based id is upstream-backed without snapshot
  support
- silently changing validation outcomes by refreshing references during normal
  processing
- hiding local-only expected rows instead of labeling them explicitly
