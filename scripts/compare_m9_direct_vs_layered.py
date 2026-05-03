#!/usr/bin/env python3
"""Compare the M9 direct-transcription baseline against layered reconstruction artifacts."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = (
    REPO_ROOT
    / "exports/baselines/m9_direct_transcription/m9_direct_transcription.tsv"
)
M9_DISSOCIATION_PATH = (
    REPO_ROOT
    / "sources/literature_test_media/literature_test_media_draft_01/m9_dissociation_mapping.tsv"
)
BOUND_DIRECT_PATH = (
    REPO_ROOT
    / "sources/literature_test_media/literature_test_media_draft_01/bound_assignment.tsv"
)
BOUND_LAYERED_PATH = (
    REPO_ROOT
    / "sources/literature_test_media/literature_test_media_draft_01/bound_assignment_dissociated.tsv"
)
BOUND_PILOT_PATH = (
    REPO_ROOT
    / "sources/literature_test_media/literature_test_media_draft_01/concentration_derived_bound_pilot.tsv"
)
OUTPUT_DIR = REPO_ROOT / "exports/comparisons/m9_direct_vs_layered"
OUTPUT_COMPARISON = OUTPUT_DIR / "m9_direct_vs_layered_comparison.tsv"
OUTPUT_SEMANTIC = OUTPUT_DIR / "m9_semantic_differences.tsv"
OUTPUT_BOUND = OUTPUT_DIR / "m9_bound_assignment_comparison.tsv"
OUTPUT_SUMMARY = OUTPUT_DIR / "m9_direct_vs_layered_summary.md"


def normalize_name(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def parse_citation_refs(value: str) -> tuple[set[str], set[str], set[str]]:
    source_rows: set[str] = set()
    composition_rows: set[str] = set()
    mapping_rows: set[str] = set()
    for part in value.split(";"):
        item = part.strip()
        if item.startswith("source_recipe:"):
            source_rows.update(x for x in item.split(":", 1)[1].split("|") if x)
        elif item.startswith("source_composition:"):
            composition_rows.update(x for x in item.split(":", 1)[1].split("|") if x)
        elif item.startswith("m9_dissociation_mapping:"):
            mapping_rows.update(x for x in item.split(":", 1)[1].split("|") if x)
    return source_rows, composition_rows, mapping_rows


def build_bound_indexes(rows: list[dict[str, str]]) -> tuple[dict[tuple[str, str], list[dict[str, str]]], dict[str, list[dict[str, str]]]]:
    key_index: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    mapping_index: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        source_rows, composition_rows, mapping_rows = parse_citation_refs(row["citation_source"])
        if not composition_rows:
            composition_rows = {""}
        for source_row in source_rows:
            for composition_row in composition_rows:
                key_index[(source_row, composition_row)].append(row)
        for mapping_row in mapping_rows:
            mapping_index[mapping_row].append(row)
    return key_index, mapping_index


def layered_representation_change_class(direct_name: str, layered_name: str) -> str:
    return (
        "retained_as_named_source_compound"
        if normalize_name(direct_name) == normalize_name(layered_name)
        else "retained_in_direct_replaced_in_layered"
    )


def pilot_match_class(pilot_rows: list[dict[str, str]]) -> str:
    return "inventory_only_vs_concentration_derived" if pilot_rows else "inventory_only_in_both"


def interpretation_note(direct_name: str, layered_name: str, pilot_rows: list[dict[str, str]]) -> str:
    if normalize_name(direct_name) == normalize_name(layered_name) and pilot_rows:
        return (
            "Layered reconstruction retains the same named compound but adds a concentration-derived availability pilot, "
            "which is a semantic upgrade beyond direct inventory presence."
        )
    if normalize_name(direct_name) == normalize_name(layered_name):
        return "Direct transcription and layered reconstruction both retain the same named compound at inventory-only semantics."
    if pilot_rows:
        return (
            f"Layered reconstruction replaces direct source compound {direct_name} with model-facing source term {layered_name} "
            "and also introduces a concentration-derived availability pilot for part of that reconstructed representation."
        )
    return (
        f"Layered reconstruction replaces direct source compound {direct_name} with model-facing source term {layered_name} "
        "while keeping inventory-only semantics."
    )


def main() -> int:
    if not BASELINE_PATH.exists():
        raise FileNotFoundError(
            f"Baseline file not found: {BASELINE_PATH}. Run build_m9_direct_transcription_baseline.py first."
        )

    baseline_rows = read_tsv(BASELINE_PATH)
    dissociation_rows = [
        row
        for row in read_tsv(M9_DISSOCIATION_PATH)
        if row["medium_name"] == "literature_test_media_draft_01 M9 broth"
    ]
    direct_bound_rows = [
        row
        for row in read_tsv(BOUND_DIRECT_PATH)
        if row["medium_name"] == "literature_test_media_draft_01 M9 broth"
    ]
    layered_bound_rows = [
        row
        for row in read_tsv(BOUND_LAYERED_PATH)
        if row["medium_name"] == "literature_test_media_draft_01 M9 broth dissociated"
    ]
    pilot_rows = read_tsv(BOUND_PILOT_PATH)

    direct_bound_index, _ = build_bound_indexes(direct_bound_rows)
    layered_bound_index, layered_bound_mapping_index = build_bound_indexes(layered_bound_rows)
    pilot_index, pilot_mapping_index = build_bound_indexes(pilot_rows)

    comparison_rows: list[dict[str, str]] = []
    bound_rows: list[dict[str, str]] = []

    comp_id = 1
    bound_id = 1
    for baseline_row in baseline_rows:
        key = (baseline_row["source_row_id"], baseline_row["source_composition_row_id"])
        related_mapping_rows = [
            row
            for row in dissociation_rows
            if row["source_row_id"] == baseline_row["source_row_id"]
            and row["source_composition_row_id"] == baseline_row["source_composition_row_id"]
        ]
        direct_bound_matches = direct_bound_index.get(key, [])

        related_pilot_rows: list[dict[str, str]] = []
        for mapping_row in related_mapping_rows:
            related_pilot_rows.extend(
                pilot_index.get(key, []) + pilot_mapping_index.get(mapping_row["mapping_row_id"], [])
            )
        # Remove duplicates while preserving order.
        seen_pilots: set[tuple[str, str]] = set()
        deduped_pilots: list[dict[str, str]] = []
        for pilot_row in related_pilot_rows:
            dedupe_key = (pilot_row["ingredient"], pilot_row["mapped_metabolite"])
            if dedupe_key in seen_pilots:
                continue
            seen_pilots.add(dedupe_key)
            deduped_pilots.append(pilot_row)
        related_pilot_rows = deduped_pilots

        if not related_mapping_rows:
            comparison_rows.append(
                {
                    "comparison_row_id": f"m9cmp::{comp_id}",
                    "source_recipe_term": baseline_row["source_recipe_term"],
                    "source_row_id": baseline_row["source_row_id"],
                    "source_composition_row_id": baseline_row["source_composition_row_id"],
                    "direct_transcription_class": baseline_row["baseline_class"],
                    "direct_transcription_representation": baseline_row["explicit_compound_name"],
                    "layered_representation": "",
                    "representation_change_class": "present_only_in_direct",
                    "bound_semantics_direct": baseline_row["bound_semantics"],
                    "bound_semantics_layered": "",
                    "bound_change_class": "inventory_only_in_both",
                    "manuscript_relevance_note": "No layered broth representation was found for this direct baseline row.",
                }
            )
            comp_id += 1
            continue

        layered_names = sorted({row["model_facing_compound_name"] for row in related_mapping_rows})
        layered_inventory_semantics = sorted(
            {
                row["formula_type"]
                for mapping_row in related_mapping_rows
                for row in layered_bound_mapping_index.get(mapping_row["mapping_row_id"], [])
            }
        )
        pilot_names = sorted({row["ingredient"] for row in related_pilot_rows})

        bound_rows.append(
            {
                "bound_comparison_id": f"m9bnd::{bound_id}",
                "source_recipe_term": baseline_row["source_recipe_term"],
                "source_row_id": baseline_row["source_row_id"],
                "source_composition_row_id": baseline_row["source_composition_row_id"],
                "direct_transcription_representation": baseline_row["explicit_compound_name"],
                "direct_bound_semantics": baseline_row["bound_semantics"],
                "direct_bound_artifact_match": "|".join(
                    sorted({row["ingredient"] for row in direct_bound_matches})
                ),
                "layered_inventory_representation": "|".join(layered_names),
                "layered_inventory_semantics": "|".join(layered_inventory_semantics) or "inventory_only",
                "layered_concentration_derived_representation": "|".join(pilot_names),
                "layered_concentration_derived_bound_values": "|".join(
                    f"{row['ingredient']}={row['bound_value']} {row['bound_unit']}" for row in related_pilot_rows
                ),
                "bound_change_class": pilot_match_class(related_pilot_rows),
                "notes": (
                    "Layered workflow keeps inventory-only semantics for the reconstructed representation."
                    if not related_pilot_rows
                    else "Layered workflow adds a concentration-derived availability pilot beyond the direct baseline."
                ),
            }
        )
        bound_id += 1

        for mapping_row in related_mapping_rows:
            layered_name = mapping_row["model_facing_compound_name"]
            matching_layered_bounds = layered_bound_mapping_index.get(mapping_row["mapping_row_id"], [])
            relevant_pilot_rows = [
                row
                for row in related_pilot_rows
                if normalize_name(row["ingredient"]) == normalize_name(layered_name)
            ]
            if not relevant_pilot_rows and layered_name == "Phosphate":
                relevant_pilot_rows = [row for row in related_pilot_rows if row["ingredient"] == "Phosphate"]
            comparison_rows.append(
                {
                    "comparison_row_id": f"m9cmp::{comp_id}",
                    "source_recipe_term": baseline_row["source_recipe_term"],
                    "source_row_id": baseline_row["source_row_id"],
                    "source_composition_row_id": baseline_row["source_composition_row_id"],
                    "direct_transcription_class": baseline_row["baseline_class"],
                    "direct_transcription_representation": baseline_row["explicit_compound_name"],
                    "layered_representation": layered_name,
                    "representation_change_class": layered_representation_change_class(
                        baseline_row["explicit_compound_name"], layered_name
                    ),
                    "bound_semantics_direct": baseline_row["bound_semantics"],
                    "bound_semantics_layered": "|".join(
                        sorted({row["formula_type"] for row in matching_layered_bounds})
                    )
                    or "inventory_only",
                    "bound_change_class": pilot_match_class(relevant_pilot_rows),
                    "manuscript_relevance_note": interpretation_note(
                        baseline_row["explicit_compound_name"], layered_name, relevant_pilot_rows
                    ),
                }
            )
            comp_id += 1

        layered_only_pilots = [
            row
            for row in related_pilot_rows
            if normalize_name(row["ingredient"])
            not in {normalize_name(name) for name in layered_names}
        ]
        for pilot_row in layered_only_pilots:
            comparison_rows.append(
                {
                    "comparison_row_id": f"m9cmp::{comp_id}",
                    "source_recipe_term": baseline_row["source_recipe_term"],
                    "source_row_id": baseline_row["source_row_id"],
                    "source_composition_row_id": baseline_row["source_composition_row_id"],
                    "direct_transcription_class": baseline_row["baseline_class"],
                    "direct_transcription_representation": baseline_row["explicit_compound_name"],
                    "layered_representation": pilot_row["ingredient"],
                    "representation_change_class": "present_only_in_layered",
                    "bound_semantics_direct": baseline_row["bound_semantics"],
                    "bound_semantics_layered": pilot_row["formula_type"],
                    "bound_change_class": "inventory_only_vs_concentration_derived",
                    "manuscript_relevance_note": (
                        f"Layered workflow introduces pooled source-term {pilot_row['ingredient']} with a concentration-derived "
                        "availability pilot that has no direct-transcription analogue."
                    ),
                }
            )
            comp_id += 1

    semantic_rows = [
        row
        for row in comparison_rows
        if row["representation_change_class"] != "retained_as_named_source_compound"
        or row["bound_change_class"] != "inventory_only_in_both"
    ]

    comparison_fieldnames = [
        "comparison_row_id",
        "source_recipe_term",
        "source_row_id",
        "source_composition_row_id",
        "direct_transcription_class",
        "direct_transcription_representation",
        "layered_representation",
        "representation_change_class",
        "bound_semantics_direct",
        "bound_semantics_layered",
        "bound_change_class",
        "manuscript_relevance_note",
    ]
    write_tsv(OUTPUT_COMPARISON, comparison_fieldnames, comparison_rows)
    write_tsv(OUTPUT_SEMANTIC, comparison_fieldnames, semantic_rows)
    write_tsv(
        OUTPUT_BOUND,
        [
            "bound_comparison_id",
            "source_recipe_term",
            "source_row_id",
            "source_composition_row_id",
            "direct_transcription_representation",
            "direct_bound_semantics",
            "direct_bound_artifact_match",
            "layered_inventory_representation",
            "layered_inventory_semantics",
            "layered_concentration_derived_representation",
            "layered_concentration_derived_bound_values",
            "bound_change_class",
            "notes",
        ],
        bound_rows,
    )

    retained_replaced = sum(
        1 for row in comparison_rows if row["representation_change_class"] == "retained_in_direct_replaced_in_layered"
    )
    pilot_upgrades = sum(
        1 for row in comparison_rows if row["bound_change_class"] == "inventory_only_vs_concentration_derived"
    )
    lines = [
        "# M9 Direct vs Layered Summary",
        "",
        "Scope: `M9 broth` only.",
        "",
        f"- comparison rows: `{len(comparison_rows)}`",
        f"- semantic-difference rows: `{len(semantic_rows)}`",
        f"- direct compounds replaced by layered source terms: `{retained_replaced}`",
        f"- rows showing concentration-derived availability upgrades: `{pilot_upgrades}`",
        "",
        "Most manuscript-relevant outcomes:",
        "- direct transcription retains explicit named source compounds such as `Na2HPO4`, `KH2PO4`, `NH4Cl`, `MgSO4`, and `CaCl2`",
        "- layered reconstruction replaces several of those named source compounds with model-facing source terms such as `Phosphate`, `Ammonium`, `Sodium`, `Potassium`, `Cl-`, `Magnesium`, and `Calcium`",
        "- the layered M9 pilot further upgrades selected inventory-only rows into `concentration_derived_availability_bound` rows for `D-glucose`, `Ammonium`, and pooled `Phosphate`",
        "",
        f"Generated at: `{datetime.now(timezone.utc).replace(microsecond=0).isoformat()}`",
    ]
    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "comparison_rows_written": len(comparison_rows),
                "semantic_rows_written": len(semantic_rows),
                "bound_rows_written": len(bound_rows),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
