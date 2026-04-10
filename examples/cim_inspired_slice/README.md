# CIM-Inspired Prototype Slice

This example is a small, explicit flat-file fixture meant to stress-test the
current MVP against a minimal but meaningful subset of CIM-like medium logic.

It includes:

- one `direct_export` case: `D-Glucose`
- one `salt_split_member` case: `Disodium phosphate -> Sodium + Phosphate`
- one `polymer_proxy` case: `Starch -> Maltose`
- one `chemical_form_change` case: `Citric acid -> Citrate`
- explicit background-species insertions: `O2`, `H2O`, `H+`

The scientific choices remain in the TSV rule tables, not in code. This is
still only a prototype slice and not a full CIM implementation.

With the current extracted `gapseq_seed_like` snapshot, this fixture is expected
to show:

- `valid_upstream` for glucose, sodium, phosphate, maltose, O2, H2O, and H+
- `local_only_expected` for explicitly local placeholder rows and local
  provenance rows such as the retained salt/acid intermediates and
  `workbook_slice` references
- no `missing_upstream` rows in the corrected fixture
