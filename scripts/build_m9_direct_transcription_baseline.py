#!/usr/bin/env python3
"""Build a conservative direct-transcription baseline for M9 broth only."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_RECIPE_PATH = (
    REPO_ROOT
    / "sources/literature_test_media/literature_test_media_draft_01/source_recipe.tsv"
)
SOURCE_COMPOSITION_PATH = (
    REPO_ROOT
    / "sources/literature_test_media/literature_test_media_draft_01/source_composition.tsv"
)
SNAPSHOT_PATH = REPO_ROOT / "upstream_snapshots/gapseq_seed_like/compounds.tsv"
OUTPUT_DIR = REPO_ROOT / "exports/baselines/m9_direct_transcription"
REPORTS_DIR = OUTPUT_DIR / "reports"
OUTPUT_TSV = OUTPUT_DIR / "m9_direct_transcription.tsv"
OUTPUT_CSV = OUTPUT_DIR / "m9_direct_transcription.csv"
OUTPUT_MANIFEST = OUTPUT_DIR / "m9_direct_transcription_manifest.yaml"
OUTPUT_SUMMARY = REPORTS_DIR / "direct_transcription_summary.md"
OUTPUT_VALIDATION = REPORTS_DIR / "direct_transcription_mapping_validation.tsv"


MWS = {
    "D-glucose": 180.156,
    "Na2HPO4": 141.958,
    "KH2PO4": 136.086,
    "NaCl": 58.44,
    "NH4Cl": 53.491,
    "MgSO4": 120.366,
    "CaCl2": 110.984,
}

STOCK_NAME_TO_COMPOUND = {
    "1 M MgSO4": "MgSO4",
    "1 M CaCl2": "CaCl2",
    "40% glucose": "D-glucose",
}


@dataclass
class BaselineRow:
    baseline_row_id: str
    medium_name: str
    source_recipe_term: str
    source_row_id: str
    source_composition_row_id: str
    baseline_class: str
    explicit_compound_name: str
    final_amount: str
    final_amount_unit: str
    final_inventory_mmol_per_l: str
    molecular_weight: str
    source_concentration_note: str
    mapping_status: str
    mapped_compound_id: str
    mapped_compound_name: str
    bound_semantics: str
    evidence_note: str
    decision_note: str


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_name(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def load_snapshot_name_map(path: Path) -> dict[str, tuple[str, str]]:
    rows = read_tsv(path)
    snapshot_name_map: dict[str, tuple[str, str]] = {}
    for row in rows:
        normalized = normalize_name(row["compound_name"])
        snapshot_name_map.setdefault(
            normalized,
            (row["compound_id"], row["compound_name"]),
        )
    return snapshot_name_map


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fmt_decimal(value: float, digits: int = 6) -> str:
    text = f"{value:.{digits}f}".rstrip("0").rstrip(".")
    return text if text else "0"


def parse_float(value: str) -> float:
    return float(value.strip())


def make_mapping(explicit_compound_name: str, snapshot_name_map: dict[str, tuple[str, str]]) -> tuple[str, str, str]:
    exact = snapshot_name_map.get(normalize_name(explicit_compound_name))
    if exact is None:
        return ("local_only_expected", "", "")
    return ("valid_upstream", exact[0], exact[1])


def build_stock_member_rows(
    broth_row: dict[str, str],
    composition_rows: list[dict[str, str]],
    snapshot_name_map: dict[str, tuple[str, str]],
) -> list[BaselineRow]:
    factor_l_per_l = parse_float(broth_row["quantity"]) / 1000.0
    rows: list[BaselineRow] = []
    next_index = 1
    for comp_row in composition_rows:
        component_name = comp_row["component_raw"].strip()
        if component_name == "dH2O":
            continue
        grams_per_l_stock = parse_float(comp_row["amount_raw"])
        final_g_per_l = grams_per_l_stock * factor_l_per_l
        mw = MWS[component_name]
        final_mmol_per_l = final_g_per_l / mw * 1000.0
        mapping_status, mapped_id, mapped_name = make_mapping(component_name, snapshot_name_map)
        rows.append(
            BaselineRow(
                baseline_row_id=f"m9dt::{next_index}",
                medium_name="literature_test_media_draft_01 M9 broth direct transcription",
                source_recipe_term=broth_row["ingredient_name"],
                source_row_id=broth_row["source_row_id"],
                source_composition_row_id=comp_row["source_row_id"],
                baseline_class="explicitly_flattened_from_stock",
                explicit_compound_name=component_name,
                final_amount=fmt_decimal(final_g_per_l),
                final_amount_unit="g/L",
                final_inventory_mmol_per_l=fmt_decimal(final_mmol_per_l),
                molecular_weight=fmt_decimal(mw, 3),
                source_concentration_note=(
                    f"{broth_row['quantity']} {broth_row['unit']} of {broth_row['ingredient_name']} stock; "
                    f"explicit stock member {component_name} is {grams_per_l_stock:g} g/L in source_composition.tsv"
                ),
                mapping_status=mapping_status,
                mapped_compound_id=mapped_id,
                mapped_compound_name=mapped_name,
                bound_semantics="inventory_only",
                evidence_note=(
                    f"Direct transcription keeps the explicit stock member {component_name} as named in source_composition.tsv "
                    "and does not dissociate it into layered source terms."
                ),
                decision_note=(
                    "Explicit stock flattening is allowed because the stock composition is stated directly in the source; "
                    "no salt dissociation is applied."
                ),
            )
        )
        next_index += 1
    return rows


def build_direct_recipe_row(
    source_row: dict[str, str],
    snapshot_name_map: dict[str, tuple[str, str]],
    row_index: int,
) -> BaselineRow:
    ingredient_name = source_row["ingredient_name"].strip()
    explicit_compound_name = STOCK_NAME_TO_COMPOUND[ingredient_name]
    quantity = parse_float(source_row["quantity"])
    unit = source_row["unit"].strip()

    if ingredient_name == "40% glucose":
        final_g_per_l = quantity * 0.4
        final_mmol_per_l = final_g_per_l / MWS[explicit_compound_name] * 1000.0
        final_amount = fmt_decimal(final_g_per_l)
        final_unit = "g/L"
        source_note = "5 mL/L of 40% glucose stock interpreted conservatively as 0.4 g/mL glucose"
    elif ingredient_name == "1 M MgSO4":
        final_mmol_per_l = quantity
        final_g_per_l = final_mmol_per_l / 1000.0 * MWS[explicit_compound_name]
        final_amount = fmt_decimal(final_mmol_per_l)
        final_unit = "mmol/L"
        source_note = "2 mL/L of 1 M MgSO4 gives 2 mmol/L explicit MgSO4 inventory"
    elif ingredient_name == "1 M CaCl2":
        final_mmol_per_l = quantity
        final_g_per_l = final_mmol_per_l / 1000.0 * MWS[explicit_compound_name]
        final_amount = fmt_decimal(final_mmol_per_l)
        final_unit = "mmol/L"
        source_note = "0.1 mL/L of 1 M CaCl2 gives 0.1 mmol/L explicit CaCl2 inventory"
    else:
        raise ValueError(f"Unhandled direct-recipe ingredient: {ingredient_name}")

    mapping_status, mapped_id, mapped_name = make_mapping(explicit_compound_name, snapshot_name_map)
    return BaselineRow(
        baseline_row_id=f"m9dt::{row_index}",
        medium_name="literature_test_media_draft_01 M9 broth direct transcription",
        source_recipe_term=ingredient_name,
        source_row_id=source_row["source_row_id"],
        source_composition_row_id="",
        baseline_class="retained_as_named_source_compound",
        explicit_compound_name=explicit_compound_name,
        final_amount=final_amount,
        final_amount_unit=final_unit,
        final_inventory_mmol_per_l=fmt_decimal(final_mmol_per_l),
        molecular_weight=fmt_decimal(MWS[explicit_compound_name], 3),
        source_concentration_note=source_note,
        mapping_status=mapping_status,
        mapped_compound_id=mapped_id,
        mapped_compound_name=mapped_name,
        bound_semantics="inventory_only",
        evidence_note=(
            f"Direct transcription keeps {explicit_compound_name} as the explicit named source compound "
            "derived from the stated stock addition."
        ),
        decision_note=(
            "Minimal normalization is applied only to compute final per-liter inventory; "
            "no layered dissociation or availability-bound upgrade is applied."
        ),
    )


def write_manifest(inputs: list[Path], outputs: list[Path], counts: dict[str, int]) -> None:
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = [
        "schema_id: m9_direct_transcription_manifest.v1",
        "object_type: direct_transcription_baseline",
        "baseline_id: m9_direct_transcription",
        f"created_at: {created_at}",
        "scope: M9 broth only",
        "notes:",
        "  - Conservative direct-transcription baseline.",
        "  - Explicit stock-member flattening is allowed when source_composition.tsv states the stock members directly.",
        "  - No salt dissociation, proxy enrichment, viable export transformation, or concentration-derived availability bounds are applied.",
        "inputs:",
    ]
    for path in inputs:
        lines.append(f"  - path: {path}")
        lines.append(f"    sha256: {sha256_file(path)}")
    lines.extend(
        [
            "outputs:",
        ]
    )
    for path in outputs:
        lines.append(f"  - {path}")
    lines.extend(
        [
            "counts:",
        ]
    )
    for key, value in counts.items():
        lines.append(f"  {key}: {value}")
    OUTPUT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_summary(rows: list[BaselineRow], excluded_recipe_rows: list[str]) -> None:
    mapped = sum(1 for row in rows if row.mapping_status == "valid_upstream")
    unmapped = len(rows) - mapped
    flattened = sum(1 for row in rows if row.baseline_class == "explicitly_flattened_from_stock")
    retained = len(rows) - flattened
    lines = [
        "# Direct Transcription Summary",
        "",
        "Scope: `M9 broth` only.",
        "",
        f"- baseline rows emitted: `{len(rows)}`",
        f"- retained as named source compounds: `{retained}`",
        f"- explicitly flattened from stock composition: `{flattened}`",
        f"- upstream-backed exact-name mappings: `{mapped}`",
        f"- local-only expected named compounds: `{unmapped}`",
        "",
        "Conservative rules applied:",
        "- explicit stock members from `source_composition.tsv` were flattened only for the `M9 salts` stock",
        "- `1 M MgSO4`, `1 M CaCl2`, and `40% glucose` were normalized only enough to compute final per-liter explicit source inventory",
        "- no salt dissociation into sodium/phosphate/ammonium-style layered source terms was applied",
        "- no concentration-derived availability bounds were assigned",
        "",
        "Excluded procedural rows:",
    ]
    for row_id in excluded_recipe_rows:
        lines.append(f"- `{row_id}`")
    lines.append("")
    lines.append(
        "This baseline is intended as a source-faithful inventory-presence control rather than a model-facing reconstructed medium."
    )
    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    source_recipe_rows = read_tsv(SOURCE_RECIPE_PATH)
    source_composition_rows = read_tsv(SOURCE_COMPOSITION_PATH)
    snapshot_name_map = load_snapshot_name_map(SNAPSHOT_PATH)

    broth_rows = [row for row in source_recipe_rows if row["medium_family"] == "m9_broth"]
    stock_composition_rows = [
        row for row in source_composition_rows if row["source_medium_id"] == "m9_stock_10x"
    ]

    rows: list[BaselineRow] = []
    excluded_recipe_rows: list[str] = []

    stock_row = next(row for row in broth_rows if row["ingredient_name"] == "M9 salts")
    rows.extend(build_stock_member_rows(stock_row, stock_composition_rows, snapshot_name_map))

    next_index = len(rows) + 1
    for broth_row in broth_rows:
        ingredient_name = broth_row["ingredient_name"]
        if ingredient_name == "M9 salts":
            continue
        if ingredient_name == "dH2O":
            excluded_recipe_rows.append(broth_row["source_row_id"])
            continue
        rows.append(build_direct_recipe_row(broth_row, snapshot_name_map, next_index))
        next_index += 1

    row_dicts = [row.__dict__ for row in rows]
    fieldnames = list(BaselineRow.__annotations__.keys())
    write_tsv(OUTPUT_TSV, fieldnames, row_dicts)
    write_csv(OUTPUT_CSV, fieldnames, row_dicts)

    validation_rows = [
        {
            "baseline_row_id": row.baseline_row_id,
            "explicit_compound_name": row.explicit_compound_name,
            "mapping_status": row.mapping_status,
            "mapped_compound_id": row.mapped_compound_id,
            "mapped_compound_name": row.mapped_compound_name,
            "reason": (
                "normalized exact-name match found in frozen snapshot"
                if row.mapping_status == "valid_upstream"
                else "direct transcription retains explicit named source compound even when the snapshot lacks that exact compound name"
            ),
        }
        for row in rows
    ]
    write_tsv(
        OUTPUT_VALIDATION,
        [
            "baseline_row_id",
            "explicit_compound_name",
            "mapping_status",
            "mapped_compound_id",
            "mapped_compound_name",
            "reason",
        ],
        validation_rows,
    )

    write_summary(rows, excluded_recipe_rows + ["row_ltm_m9s_005"])
    write_manifest(
        inputs=[SOURCE_RECIPE_PATH, SOURCE_COMPOSITION_PATH, SNAPSHOT_PATH],
        outputs=[OUTPUT_TSV, OUTPUT_CSV, OUTPUT_VALIDATION, OUTPUT_SUMMARY],
        counts={
            "baseline_rows": len(rows),
            "flattened_stock_rows": sum(
                1 for row in rows if row.baseline_class == "explicitly_flattened_from_stock"
            ),
            "retained_named_source_rows": sum(
                1 for row in rows if row.baseline_class == "retained_as_named_source_compound"
            ),
            "upstream_backed_rows": sum(1 for row in rows if row.mapping_status == "valid_upstream"),
            "local_only_expected_rows": sum(
                1 for row in rows if row.mapping_status == "local_only_expected"
            ),
        },
    )

    print(json.dumps({"baseline_rows_written": len(rows), "output_tsv": str(OUTPUT_TSV)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
