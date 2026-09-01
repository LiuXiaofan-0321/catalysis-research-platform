#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPOSITORY_ROOT / "research" / "src"))

from catalysis_research.kg.freeze_stage1 import (  # noqa: E402
    freeze_stage1_archive,
    verify_snapshot,
)


FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
ONTOLOGY_VERSION = "catalysis_evidence_graph.v2"


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    )


def _zip_write(archive: zipfile.ZipFile, name: str, payload: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def _namespace(identifier: Any, document_id: str) -> str:
    return f"{document_id}::{identifier}"


def _annotate_evidence(container: dict[str, Any], document: dict[str, Any]) -> None:
    for evidence in container.get("evidence") or []:
        if not isinstance(evidence, dict):
            continue
        current = evidence.get("document_id")
        if current and str(current) != str(document["document_id"]):
            raise ValueError(
                f"Evidence document mismatch in {document['document_id']}: {current}"
            )
        evidence["document_id"] = document["document_id"]
        evidence["document_type"] = document["document_type"]


def _namespace_extraction(
    extraction: dict[str, Any], document: dict[str, Any]
) -> dict[str, Any]:
    extraction = copy.deepcopy(extraction)
    document_id = str(document["document_id"])
    entity_ids = {
        str(item["id"]): _namespace(item["id"], document_id)
        for item in extraction.get("entities") or []
        if item.get("id")
    }
    experiment_ids = {
        str(item["id"]): _namespace(item["id"], document_id)
        for item in extraction.get("experiments") or []
        if item.get("id")
    }

    for item in extraction.get("entities") or []:
        _annotate_evidence(item, document)
        item["id"] = entity_ids[str(item["id"])]
    for item in (extraction.get("keywords") or {}).get("extracted") or []:
        _annotate_evidence(item, document)
        item["id"] = _namespace(item["id"], document_id)
    for item in extraction.get("experiments") or []:
        _annotate_evidence(item, document)
        item["id"] = experiment_ids[str(item["id"])]
        for field in ("sample_entity_ids", "material_entity_ids", "method_entity_ids"):
            item[field] = [entity_ids[str(value)] for value in item.get(field) or []]
    for item in extraction.get("observations") or []:
        _annotate_evidence(item, document)
        item["id"] = _namespace(item["id"], document_id)
        if item.get("experiment_id"):
            item["experiment_id"] = experiment_ids[str(item["experiment_id"])]
        for field in ("sample_entity_id", "property_entity_id", "method_entity_id"):
            if item.get(field):
                item[field] = entity_ids[str(item[field])]
    for item in extraction.get("claims") or []:
        _annotate_evidence(item, document)
        item["id"] = _namespace(item["id"], document_id)
    for item in (extraction.get("summary") or {}).get("main_findings") or []:
        if isinstance(item, dict):
            _annotate_evidence(item, document)
    return extraction


def _ordered_unique(values: list[Any]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for value in values:
        key = _canonical_json(value)
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def _merge_paper_artifacts(
    paper_id: str,
    documents: list[dict[str, Any]],
    artifacts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    ordered = sorted(
        documents,
        key=lambda item: (item["document_type"] != "main", item["document_id"]),
    )
    if sum(item["document_type"] == "main" for item in ordered) != 1:
        raise ValueError(f"Paper must have exactly one main document: {paper_id}")
    namespaced = [
        (
            document,
            _namespace_extraction(
                artifacts[document["document_id"]]["extraction"], document
            ),
        )
        for document in ordered
    ]
    main_document, main = namespaced[0]
    merged = copy.deepcopy(main)
    merged["paper"]["id"] = paper_id
    merged["paper"]["source_pdf_sha256"] = main_document["source_document_sha256"]
    merged["paper"]["source_path"] = main_document["source_path"]
    merged["paper"]["reaction_categories"] = _ordered_unique(
        [
            category
            for _, extraction in namespaced
            for category in extraction.get("paper", {}).get("reaction_categories") or []
        ]
    )
    merged["paper"]["source_documents"] = [
        {
            "document_id": document["document_id"],
            "document_type": document["document_type"],
            "source_path": document["source_path"],
            "source_document_sha256": document["source_document_sha256"],
            "artifact_sha256": document["artifact_sha256"],
        }
        for document in ordered
    ]
    for field in ("entities", "experiments", "observations", "claims"):
        merged[field] = [
            item
            for _, extraction in namespaced
            for item in extraction.get(field) or []
        ]
    merged.setdefault("keywords", {})["extracted"] = [
        item
        for _, extraction in namespaced
        for item in (extraction.get("keywords") or {}).get("extracted") or []
    ]
    merged.setdefault("summary", {})["main_findings"] = [
        item
        for _, extraction in namespaced
        for item in (extraction.get("summary") or {}).get("main_findings") or []
    ]
    merged["visual_review_items"] = [
        {**item, "document_id": document["document_id"], "document_type": document["document_type"]}
        for document, extraction in namespaced
        for item in extraction.get("visual_review_items") or []
        if isinstance(item, dict)
    ]
    merged["quality"] = {
        "extraction_status": "completed",
        "source_document_count": len(ordered),
        "needs_review_count": sum(
            int((extraction.get("quality") or {}).get("needs_review_count") or 0)
            for _, extraction in namespaced
        ),
        "boundary_normalizations": [
            item
            for _, extraction in namespaced
            for item in (extraction.get("quality") or {}).get("boundary_normalizations") or []
        ],
    }
    metadata = merged.setdefault("extraction_metadata", {})
    metadata["aggregation_version"] = "main_si_by_paper.v1"
    metadata["source_document_ids"] = [item["document_id"] for item in ordered]
    source = copy.deepcopy(artifacts[main_document["document_id"]].get("source") or {})
    source.update(
        {
            "paper_id": paper_id,
            "document_id": paper_id,
            "document_type": "paper",
            "path": main_document["source_path"],
            "source_pdf_sha256": main_document["source_document_sha256"],
            "source_documents": merged["paper"]["source_documents"],
        }
    )
    return {"source": source, "extraction": merged}


def build_aggregated_archive(
    *,
    corpus_directory: Path,
    output_archive: Path,
    expected_documents: int,
    expected_papers: int,
) -> dict[str, Any]:
    if output_archive.exists():
        raise FileExistsError(output_archive)
    documents = _load_jsonl(corpus_directory / "documents.jsonl")
    if len(documents) != expected_documents:
        raise ValueError(f"Expected {expected_documents} documents, found {len(documents)}")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for document in documents:
        grouped[str(document["paper_id"])].append(document)
    if len(grouped) != expected_papers:
        raise ValueError(f"Expected {expected_papers} papers, found {len(grouped)}")

    artifacts: dict[str, dict[str, Any]] = {}
    with zipfile.ZipFile(corpus_directory / "structured-documents.zip") as archive:
        for document in documents:
            raw = archive.read(document["artifact_entry"])
            actual_hash = hashlib.sha256(raw).hexdigest()
            if actual_hash != document["artifact_sha256"]:
                raise ValueError(f"Artifact hash mismatch: {document['document_id']}")
            artifacts[str(document["document_id"])] = json.loads(raw)

    output_archive.parent.mkdir(parents=True, exist_ok=True)
    entry_rows: list[dict[str, Any]] = []
    with zipfile.ZipFile(output_archive, "w") as archive:
        for paper_id in sorted(grouped):
            artifact = _merge_paper_artifacts(paper_id, grouped[paper_id], artifacts)
            raw = (_canonical_json(artifact) + "\n").encode("utf-8")
            entry = f"json/{hashlib.sha256(paper_id.encode()).hexdigest()[:24]}.json"
            _zip_write(archive, entry, raw)
            entry_rows.append(
                {
                    "paper_id": paper_id,
                    "entry": entry,
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "document_count": len(grouped[paper_id]),
                }
            )
        manifest = {
            "schema": "catalysis_research_dataset.v2",
            "corpus_id": "zeolite-structured-corpus-v1",
            "aggregation_version": "main_si_by_paper.v1",
            "counts": {"papers": len(grouped), "documents": len(documents)},
            "entry_content_hash": hashlib.sha256(
                "\n".join(_canonical_json(row) for row in entry_rows).encode("utf-8")
            ).hexdigest(),
        }
        _zip_write(
            archive,
            "dataset-manifest.json",
            (
                json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n"
            ).encode("utf-8"),
        )
    return manifest


def read_aggregated_archive_manifest(
    archive_path: Path, *, expected_documents: int, expected_papers: int
) -> dict[str, Any]:
    with zipfile.ZipFile(archive_path) as archive:
        manifest = json.loads(archive.read("dataset-manifest.json"))
        entries = [
            item
            for item in archive.infolist()
            if item.filename.startswith("json/")
            and item.filename.lower().endswith(".json")
        ]
    counts = manifest.get("counts") or {}
    if int(counts.get("documents") or -1) != expected_documents:
        raise ValueError("Existing Stage 1 archive document count mismatch")
    if int(counts.get("papers") or -1) != expected_papers:
        raise ValueError("Existing Stage 1 archive paper count mismatch")
    if len(entries) != expected_papers:
        raise ValueError("Existing Stage 1 archive entry count mismatch")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build strict Small KG from frozen corpus.")
    parser.add_argument("--corpus-directory", type=Path, required=True)
    parser.add_argument("--stage1-archive", type=Path, required=True)
    parser.add_argument("--snapshot-directory", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--expected-documents", type=int, default=8927)
    parser.add_argument("--expected-papers", type=int, default=6691)
    parser.add_argument("--reuse-stage1-archive", action="store_true")
    parser.add_argument("--code-commit")
    args = parser.parse_args()

    if args.stage1_archive.exists() and args.reuse_stage1_archive:
        archive_manifest = read_aggregated_archive_manifest(
            args.stage1_archive,
            expected_documents=args.expected_documents,
            expected_papers=args.expected_papers,
        )
    else:
        archive_manifest = build_aggregated_archive(
            corpus_directory=args.corpus_directory.resolve(),
            output_archive=args.stage1_archive.resolve(),
            expected_documents=args.expected_documents,
            expected_papers=args.expected_papers,
        )
    snapshot = freeze_stage1_archive(
        archive_path=args.stage1_archive,
        output_directory=args.snapshot_directory,
        snapshot_id="Small-KG-zeolite-v1",
        knowledge_level="Small/Local",
        domain="zeolite_catalysis",
        expected_papers=args.expected_papers,
        allowed_systems={"thermal_catalysis", "photocatalysis", "both", "unclear"},
        repository_root=args.repository_root,
        ontology_version=ONTOLOGY_VERSION,
        corpus=archive_manifest,
        git_state=(
            {
                "commit": args.code_commit,
                "tree": "recorded-in-source-repository",
                "branch": "main",
                "dirty": False,
            }
            if args.code_commit
            else None
        ),
        strict_grounded_edges=True,
        normalize_science_concepts=True,
    )
    verification = verify_snapshot(args.snapshot_directory)
    if not verification["valid"]:
        raise ValueError("Snapshot verification failed: " + "; ".join(verification["failures"]))
    print(
        json.dumps(
            {"archive": archive_manifest, "snapshot": snapshot, "verification": verification},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
