#!/usr/bin/env python3
"""Refresh the local frozen gapseq-like compound snapshot from seed_metabolites_edited.tsv."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_SOURCE_NOTE = (
    "Derived from gapseq dat/seed_metabolites_edited.tsv as an explicit local "
    "snapshot refresh. Normal pipeline validation remains local and snapshot-based."
)
DEFAULT_UPSTREAM_PATH_NOTE = "dat/seed_metabolites_edited.tsv"
DEFAULT_SOURCE_URL = (
    "https://raw.githubusercontent.com/jotech/gapseq/main/dat/seed_metabolites_edited.tsv"
)


@dataclass
class LoadedSource:
    content: bytes
    mode: str
    reference: str
    local_path: str | None
    url: str | None


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    default_source_file = repo_root.parent / "data" / "seed_metabolites_edited.tsv"
    default_snapshot_dir = repo_root / "upstream_snapshots" / "gapseq_seed_like"
    default_gapseq_repo = repo_root.parent / "pkgs" / "gapseq_pipeline"

    parser = argparse.ArgumentParser(
        description=(
            "Refresh the frozen local gapseq-like compound snapshot from "
            "seed_metabolites_edited.tsv."
        )
    )
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--source-file",
        type=Path,
        default=default_source_file,
        help=(
            "Local path to seed_metabolites_edited.tsv. "
            f"Default: {default_source_file}"
        ),
    )
    source_group.add_argument(
        "--source-url",
        help=(
            "Explicit URL to fetch seed_metabolites_edited.tsv from. "
            "This is never used by normal pipeline validation."
        ),
    )
    parser.add_argument(
        "--snapshot-dir",
        type=Path,
        default=default_snapshot_dir,
        help=f"Snapshot directory to refresh. Default: {default_snapshot_dir}",
    )
    parser.add_argument(
        "--namespace",
        default="gapseq_seed_like",
        help="Namespace label written into the snapshot manifest.",
    )
    parser.add_argument(
        "--source-reference",
        default=DEFAULT_UPSTREAM_PATH_NOTE,
        help=(
            "Stable source reference recorded in compounds.tsv evidence_source and "
            "manifest provenance. Default: dat/seed_metabolites_edited.tsv"
        ),
    )
    parser.add_argument(
        "--source-note",
        default=DEFAULT_SOURCE_NOTE,
        help="Additional provenance note for the snapshot manifest.",
    )
    parser.add_argument(
        "--gapseq-repo",
        type=Path,
        default=default_gapseq_repo,
        help=(
            "Optional local gapseq checkout used only for manifest provenance "
            f"discovery. Default: {default_gapseq_repo}"
        ),
    )
    parser.add_argument(
        "--default-source-url",
        default=DEFAULT_SOURCE_URL,
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def run_git(repo: Path, *args: str) -> str | None:
    if not repo.exists():
        return None
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return completed.stdout.strip() or None


def load_source(args: argparse.Namespace) -> LoadedSource:
    if args.source_url:
        with urllib.request.urlopen(args.source_url) as response:
            content = response.read()
        return LoadedSource(
            content=content,
            mode="url",
            reference=args.source_reference,
            local_path=None,
            url=args.source_url,
        )

    source_file = args.source_file.resolve()
    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")
    return LoadedSource(
        content=source_file.read_bytes(),
        mode="file",
        reference=args.source_reference,
        local_path=str(source_file),
        url=None,
    )


def parse_compounds(content: bytes) -> list[dict[str, str]]:
    text = content.decode("utf-8-sig")
    rows = list(csv.DictReader(text.splitlines(), delimiter="\t"))
    if not rows:
        raise ValueError("Source TSV is empty.")
    if "id" not in rows[0] or "name" not in rows[0]:
        raise ValueError("Source TSV must include 'id' and 'name' columns.")

    compounds_by_id: dict[str, str] = {}
    for row in rows:
        compound_id = (row.get("id") or "").strip()
        compound_name = (row.get("name") or "").strip()
        if not compound_id:
            continue
        if not compound_name:
            compound_name = compound_id
        previous = compounds_by_id.get(compound_id)
        if previous is not None and previous != compound_name:
            raise ValueError(
                f"Conflicting names for compound id {compound_id}: "
                f"{previous!r} vs {compound_name!r}"
            )
        compounds_by_id[compound_id] = compound_name

    return [
        {"compound_id": compound_id, "compound_name": compounds_by_id[compound_id]}
        for compound_id in sorted(compounds_by_id)
    ]


def write_compounds_tsv(
    output_path: Path, compounds: list[dict[str, str]], source_reference: str
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(
            ["compound_id", "compound_name", "evidence_source", "evidence_note"]
        )
        for compound in compounds:
            writer.writerow(
                [
                    compound["compound_id"],
                    compound["compound_name"],
                    source_reference,
                    "present in gapseq seed_metabolites_edited snapshot import",
                ]
            )


def build_manifest(
    args: argparse.Namespace,
    loaded_source: LoadedSource,
    compounds: list[dict[str, str]],
) -> dict[str, object]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    import_date = now.split("T", 1)[0]
    gapseq_repo = args.gapseq_repo.resolve()

    manifest: dict[str, object] = {
        "snapshot_id": f"{args.namespace}_seed_metabolites_edited_{import_date}",
        "namespace": args.namespace,
        "description": (
            "Frozen local compound reference derived from gapseq "
            "seed_metabolites_edited.tsv for snapshot-based validation."
        ),
        "upstream_sources": [args.source_reference],
        "source_provenance": {
            "import_mode": loaded_source.mode,
            "source_reference": loaded_source.reference,
            "source_file": loaded_source.local_path,
            "source_url": loaded_source.url,
            "imported_at_utc": now,
            "source_sha256": sha256_bytes(loaded_source.content),
            "source_size_bytes": len(loaded_source.content),
            "source_row_count": len(compounds),
            "gapseq_branch": run_git(gapseq_repo, "rev-parse", "--abbrev-ref", "HEAD"),
            "gapseq_commit": run_git(gapseq_repo, "rev-parse", "HEAD"),
            "gapseq_remote_origin": run_git(gapseq_repo, "remote", "get-url", "origin"),
            "gapseq_repo_path": str(gapseq_repo) if gapseq_repo.exists() else None,
            "gapseq_upstream_path": DEFAULT_UPSTREAM_PATH_NOTE,
            "source_note": args.source_note,
        },
        "derived_outputs": {
            "compounds_tsv": "compounds.tsv",
            "compound_count": len(compounds),
            "columns": [
                "compound_id",
                "compound_name",
                "evidence_source",
                "evidence_note",
            ],
        },
    }
    return manifest


def write_manifest(output_path: Path, manifest: dict[str, object]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    loaded_source = load_source(args)
    compounds = parse_compounds(loaded_source.content)

    snapshot_dir = args.snapshot_dir.resolve()
    compounds_path = snapshot_dir / "compounds.tsv"
    manifest_path = snapshot_dir / "snapshot_manifest.json"

    write_compounds_tsv(compounds_path, compounds, args.source_reference)
    manifest = build_manifest(args, loaded_source, compounds)
    write_manifest(manifest_path, manifest)

    print(
        f"Refreshed {args.namespace} snapshot with {len(compounds)} compounds from "
        f"{loaded_source.reference}",
        file=sys.stdout,
    )
    print(f"Wrote {compounds_path}", file=sys.stdout)
    print(f"Wrote {manifest_path}", file=sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
