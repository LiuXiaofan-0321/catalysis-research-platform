from __future__ import annotations

import gzip
import hashlib
import io
import json
import math
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any, Iterable


SNAPSHOT_SCHEMA_VERSION = "kg_snapshot.v1"
FREEZER_VERSION = "stage1_kg_freezer.v1"
DEFAULT_ONTOLOGY_VERSION = "catalysis_evidence_graph.v1"

NODE_TYPES = (
    "paper",
    "entity",
    "keyword",
    "experiment",
    "observation",
    "claim",
)

RELATION_TYPES = (
    "PAPER_MENTIONS_ENTITY",
    "PAPER_HAS_KEYWORD",
    "PAPER_REPORTS_EXPERIMENT",
    "EXPERIMENT_USES_SAMPLE",
    "EXPERIMENT_USES_MATERIAL",
    "EXPERIMENT_USES_METHOD",
    "EXPERIMENT_PRODUCES_OBSERVATION",
    "PAPER_REPORTS_OBSERVATION",
    "OBSERVATION_OF_SAMPLE",
    "OBSERVATION_MEASURES_PROPERTY",
    "OBSERVATION_MEASURED_BY",
    "PAPER_ASSERTS_CLAIM",
)


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_hash(value: Any) -> str:
    serialized = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return sha256_bytes(serialized.encode("utf-8"))


def canonical_hash(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def compact_text(value: Any, maximum: int = 1200) -> str:
    normalized = re.sub(r"\s+", " ", str(value or "")).strip()
    return normalized[:maximum]


def normalize_key(value: Any) -> str:
    normalized = compact_text(value).lower()
    return re.sub(r"[\s\-_/\\()[\]{}:;,.，。；：]+", "", normalized)


def clamp01(value: Any, fallback: float = 0.75) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return fallback
    if not math.isfinite(number):
        return fallback
    return max(0.0, min(1.0, number))


def evidence_for(record: dict[str, Any] | None) -> list[dict[str, Any]]:
    evidence = (record or {}).get("evidence")
    if not isinstance(evidence, list):
        return []
    return [item for item in evidence if isinstance(item, dict)]


def confidence_for(record: dict[str, Any] | None) -> float:
    validations = [
        item.get("evidence_validation")
        for item in evidence_for(record)
    ]
    if "unverified" in validations:
        fallback = 0.42
    elif "locally_recovered" in validations:
        fallback = 0.72
    elif "exact" in validations:
        fallback = 0.96
    else:
        fallback = 0.7
    if (record or {}).get("needs_visual_review"):
        fallback = min(fallback, 0.58)
    return clamp01((record or {}).get("confidence"), fallback)


def review_status_for(record: dict[str, Any] | None) -> str:
    value = record or {}
    if value.get("review_status") == "needs_review":
        return "needs_review"
    if value.get("needs_visual_review"):
        return "needs_review"
    return "extracted"


def document_key_for(
    paper: dict[str, Any],
    source: dict[str, Any] | None,
) -> str:
    paper_id = compact_text(paper.get("id"), 400)
    if paper_id:
        return paper_id
    doi = compact_text(paper.get("doi"), 400)
    if doi:
        return f"doi:{doi.lower().removeprefix('doi:')}"
    source = source or {}
    source_sha = compact_text(
        paper.get("source_pdf_sha256") or source.get("source_pdf_sha256"),
        128,
    )
    if source_sha:
        return f"sha256:{source_sha}"
    return "paper:" + stable_hash(
        [paper.get("title"), paper.get("year"), paper.get("source_path")]
    )[:32]


def global_node_key(
    kind: str,
    category: Any,
    canonical: Any,
    fallback: Any,
) -> str:
    normalized = normalize_key(canonical) or normalize_key(fallback)
    return (
        f"{kind}:{compact_text(category, 80) or 'other'}:"
        f"{stable_hash(normalized)[:24]}"
    )


def paper_node_key(node_type: str, document_key: str, local_id: Any) -> str:
    return (
        f"{node_type}:"
        f"{stable_hash([document_key, compact_text(local_id, 160)])[:28]}"
    )


def node_id_for(node_key: str) -> str:
    return f"kg-node-{stable_hash(node_key)[:32]}"


def document_id_for(document_key: str) -> str:
    return f"kg-document-{stable_hash(document_key)[:32]}"


def edge_id_for(edge_key: str) -> str:
    return f"kg-edge-{stable_hash(edge_key)[:32]}"


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as output:
        for row in rows:
            output.write(canonical_json(row))
            output.write("\n")


def _write_jsonl_gzip(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("wb") as raw_output:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            compresslevel=9,
            fileobj=raw_output,
            mtime=0,
        ) as compressed:
            with io.TextIOWrapper(
                compressed,
                encoding="utf-8",
                newline="\n",
            ) as output:
                for row in rows:
                    output.write(canonical_json(row))
                    output.write("\n")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]


def _read_jsonl_gzip(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]


def _git_state(repository_root: Path) -> dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    status = run("status", "--porcelain")
    return {
        "commit": run("rev-parse", "HEAD"),
        "tree": run("rev-parse", "HEAD^{tree}"),
        "branch": run("branch", "--show-current"),
        "dirty": bool(status),
    }


def source_topic_for(source_path: Any) -> str:
    parts = PurePosixPath(str(source_path or "").replace("\\", "/")).parts
    for index, part in enumerate(parts[:-1]):
        if part.lower() == "reaction" and index + 1 < len(parts):
            return parts[index + 1]
    return "unknown"


def paper_distributions(
    papers: Iterable[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    paper_rows = list(papers)
    year_distribution = Counter(
        str(paper.get("year") or "unknown")
        for paper in paper_rows
    )
    paper_type_distribution = Counter(
        str(paper.get("paper_type") or "unknown")
        for paper in paper_rows
    )
    source_topic_distribution = Counter(
        source_topic_for(paper.get("source_path"))
        for paper in paper_rows
    )
    reaction_category_distribution = Counter(
        str(category)
        for paper in paper_rows
        for category in (paper.get("reaction_categories") or ["unknown"])
    )
    return {
        "year": dict(sorted(year_distribution.items())),
        "paper_type": dict(sorted(paper_type_distribution.items())),
        "source_topic": dict(sorted(source_topic_distribution.items())),
        "reaction_category": dict(
            sorted(reaction_category_distribution.items())
        ),
    }


def _snapshot_hash_identity(
    *,
    snapshot_id: str,
    knowledge_level: str,
    source_archive_sha256: str,
    artifact_files: dict[str, Any],
    ontology_version: str,
    corpus: dict[str, Any] | None = None,
    selection: dict[str, Any] | None = None,
    coverage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    identity: dict[str, Any] = {
        "snapshot_id": snapshot_id,
        "knowledge_level": knowledge_level,
        "source_archive_sha256": source_archive_sha256,
        "artifact_files": artifact_files,
        "ontology_version": ontology_version,
    }
    if corpus is not None:
        identity["corpus"] = corpus
    if selection is not None:
        identity["selection"] = selection
    if coverage is not None:
        identity["coverage"] = coverage
    return identity


def _increment(counter: Counter[str], value: Any) -> None:
    counter[compact_text(value, 300) or "unknown"] += 1


def _upsert_node(
    nodes: dict[str, dict[str, Any]],
    *,
    node_key: str,
    node_type: str,
    label: str,
    canonical_name: str = "",
    zh_name: str = "",
    local_id: str | None = None,
    data: dict[str, Any] | None = None,
    evidence: list[dict[str, Any]] | None = None,
    confidence: float = 0.75,
    review_status: str = "extracted",
    source_document_id: str | None = None,
) -> str:
    node_id = node_id_for(node_key)
    current = nodes.get(node_key)
    if current is None:
        nodes[node_key] = {
            "id": node_id,
            "node_key": node_key,
            "node_type": node_type,
            "label": label,
            "canonical_name": canonical_name,
            "zh_name": zh_name,
            "local_id": local_id,
            "data": data or {},
            "evidence": evidence or [],
            "confidence": clamp01(confidence),
            "review_status": review_status,
            "source_document_id": source_document_id,
        }
        return node_id

    current.update(
        {
            "label": label,
            "canonical_name": canonical_name,
            "zh_name": zh_name,
            "data": data or {},
            "evidence": evidence or [],
            "confidence": max(
                float(current.get("confidence", 0.0)),
                clamp01(confidence),
            ),
            "review_status": (
                "needs_review"
                if review_status == "needs_review"
                else current.get("review_status", "extracted")
            ),
        }
    )
    return node_id


def _insert_edge(
    edges: dict[str, dict[str, Any]],
    *,
    edge_type: str,
    from_node_id: str,
    to_node_id: str,
    source_document_id: str,
    source_record_type: str,
    source_record_id: str | None = None,
    evidence: list[dict[str, Any]] | None = None,
    confidence: float = 0.75,
    review_status: str = "extracted",
) -> None:
    if not from_node_id or not to_node_id or from_node_id == to_node_id:
        return
    edge_key = stable_hash(
        [
            edge_type,
            from_node_id,
            to_node_id,
            source_document_id,
            source_record_type,
            source_record_id or "",
        ]
    )[:36]
    edges[edge_key] = {
        "id": edge_id_for(edge_key),
        "edge_key": edge_key,
        "edge_type": edge_type,
        "from_node_id": from_node_id,
        "to_node_id": to_node_id,
        "source_document_id": source_document_id,
        "source_record_type": source_record_type,
        "source_record_id": source_record_id,
        "evidence": evidence or [],
        "confidence": clamp01(confidence),
        "review_status": review_status,
        "status": "active",
    }


def _build_graph(
    artifacts: list[tuple[str, bytes, dict[str, Any]]],
    allowed_systems: set[str],
) -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    papers: list[dict[str, Any]] = []
    nodes: dict[str, dict[str, Any]] = {}
    edges: dict[str, dict[str, Any]] = {}
    seen_document_keys: set[str] = set()
    seen_paper_ids: set[str] = set()

    extraction_versions: Counter[str] = Counter()
    prompt_versions: Counter[str] = Counter()
    extraction_models: Counter[str] = Counter()
    requested_models: Counter[str] = Counter()
    evidence_validations: Counter[str] = Counter()
    extraction_timestamps: list[str] = []

    for entry_name, raw_json, artifact in artifacts:
        extraction = artifact.get("extraction") or {}
        paper = extraction.get("paper") or {}
        source = artifact.get("source") or {}
        catalysis_system = compact_text(
            paper.get("catalysis_system"),
            80,
        ).lower()
        if catalysis_system not in allowed_systems:
            continue

        document_key = document_key_for(paper, source)
        if document_key in seen_document_keys:
            raise ValueError(f"Duplicate document key: {document_key}")
        seen_document_keys.add(document_key)

        paper_id = compact_text(paper.get("id"), 400) or document_key
        if paper_id in seen_paper_ids:
            raise ValueError(f"Duplicate paper ID: {paper_id}")
        seen_paper_ids.add(paper_id)

        metadata = extraction.get("extraction_metadata") or {}
        schema_version = compact_text(extraction.get("schema_version"), 160)
        prompt_version = compact_text(metadata.get("prompt_version"), 240)
        extraction_model = compact_text(metadata.get("model"), 240)
        requested_model = compact_text(source.get("model_requested"), 240)
        extracted_at = compact_text(metadata.get("extracted_at"), 100)

        _increment(extraction_versions, schema_version)
        _increment(prompt_versions, prompt_version)
        _increment(extraction_models, extraction_model)
        _increment(requested_models, requested_model)
        if extracted_at:
            extraction_timestamps.append(extracted_at)

        for group_name in ("entities", "experiments", "observations", "claims"):
            for record in extraction.get(group_name) or []:
                for evidence in evidence_for(record):
                    _increment(
                        evidence_validations,
                        evidence.get("evidence_validation"),
                    )

        source_pdf_sha256 = compact_text(
            paper.get("source_pdf_sha256")
            or source.get("source_pdf_sha256"),
            128,
        )
        papers.append(
            {
                "paper_id": paper_id,
                "document_key": document_key,
                "title": compact_text(paper.get("title"), 600),
                "doi": compact_text(paper.get("doi"), 240) or None,
                "year": paper.get("year"),
                "journal": compact_text(paper.get("journal"), 300) or None,
                "paper_type": compact_text(paper.get("paper_type"), 80) or None,
                "catalysis_system": catalysis_system,
                "reaction_categories": paper.get("reaction_categories") or [],
                "source_path": compact_text(
                    paper.get("source_path") or source.get("path"),
                    900,
                ),
                "raw_pdf_sha256": source_pdf_sha256,
                "structured_json_entry": entry_name,
                "structured_json_sha256": sha256_bytes(raw_json),
                "extracted_text_sha256": compact_text(
                    metadata.get("extracted_text_sha256")
                    or source.get("extracted_text_sha256"),
                    128,
                ),
                "extraction_schema_version": schema_version,
                "extraction_prompt_version": prompt_version,
                "extraction_model": extraction_model,
                "extracted_at": extracted_at,
            }
        )

        document_id = document_id_for(document_key)
        paper_node_id = _upsert_node(
            nodes,
            node_key=f"paper:{stable_hash(document_key)[:28]}",
            node_type="paper",
            label=compact_text(paper.get("title"), 600) or document_key,
            canonical_name=compact_text(paper.get("title"), 600),
            local_id=document_key,
            data=paper,
            confidence=1.0,
            source_document_id=document_id,
        )

        entity_ids: dict[str, str] = {}
        for entity in extraction.get("entities") or []:
            canonical = compact_text(
                entity.get("canonical_name")
                or entity.get("raw_term")
                or entity.get("zh_name"),
                300,
            )
            zh_name = compact_text(
                entity.get("zh_name") or entity.get("normalized_term"),
                300,
            )
            if not canonical and not zh_name:
                continue
            node_id = _upsert_node(
                nodes,
                node_key=global_node_key(
                    "entity",
                    entity.get("type"),
                    canonical,
                    zh_name,
                ),
                node_type="entity",
                label=zh_name or canonical,
                canonical_name=canonical,
                zh_name=zh_name,
                local_id=compact_text(entity.get("id"), 160) or None,
                data=entity,
                evidence=evidence_for(entity),
                confidence=confidence_for(entity),
                review_status=review_status_for(entity),
            )
            if entity.get("id"):
                entity_ids[str(entity["id"])] = node_id
            _insert_edge(
                edges,
                edge_type="PAPER_MENTIONS_ENTITY",
                from_node_id=paper_node_id,
                to_node_id=node_id,
                source_document_id=document_id,
                source_record_type="entity",
                source_record_id=compact_text(entity.get("id"), 160) or None,
                evidence=evidence_for(entity),
                confidence=confidence_for(entity),
                review_status=review_status_for(entity),
            )

        for keyword in (extraction.get("keywords") or {}).get("extracted") or []:
            normalized = compact_text(
                keyword.get("normalized_term") or keyword.get("raw_term"),
                300,
            )
            raw = compact_text(keyword.get("raw_term"), 300)
            if not normalized and not raw:
                continue
            node_id = _upsert_node(
                nodes,
                node_key=global_node_key(
                    "keyword",
                    keyword.get("category"),
                    normalized,
                    raw,
                ),
                node_type="keyword",
                label=normalized or raw,
                canonical_name=raw,
                zh_name=normalized,
                local_id=compact_text(keyword.get("id"), 160) or None,
                data=keyword,
                evidence=evidence_for(keyword),
                confidence=confidence_for(keyword),
                review_status=review_status_for(keyword),
            )
            _insert_edge(
                edges,
                edge_type="PAPER_HAS_KEYWORD",
                from_node_id=paper_node_id,
                to_node_id=node_id,
                source_document_id=document_id,
                source_record_type="keyword",
                source_record_id=compact_text(keyword.get("id"), 160) or None,
                evidence=evidence_for(keyword),
                confidence=confidence_for(keyword),
                review_status=review_status_for(keyword),
            )

        experiment_ids: dict[str, str] = {}
        for experiment in extraction.get("experiments") or []:
            if not experiment.get("id"):
                continue
            experiment_local_id = str(experiment["id"])
            node_id = _upsert_node(
                nodes,
                node_key=paper_node_key(
                    "experiment",
                    document_key,
                    experiment_local_id,
                ),
                node_type="experiment",
                label=(
                    compact_text(experiment.get("objective"), 360)
                    or (
                        f"{compact_text(experiment.get('experiment_type'), 80) or '实验'} "
                        f"{experiment_local_id}"
                    )
                ),
                canonical_name=compact_text(
                    experiment.get("experiment_type"),
                    120,
                ),
                local_id=compact_text(experiment_local_id, 160),
                data=experiment,
                evidence=evidence_for(experiment),
                confidence=confidence_for(experiment),
                review_status=review_status_for(experiment),
                source_document_id=document_id,
            )
            experiment_ids[experiment_local_id] = node_id
            _insert_edge(
                edges,
                edge_type="PAPER_REPORTS_EXPERIMENT",
                from_node_id=paper_node_id,
                to_node_id=node_id,
                source_document_id=document_id,
                source_record_type="experiment",
                source_record_id=experiment_local_id,
                evidence=evidence_for(experiment),
                confidence=confidence_for(experiment),
                review_status=review_status_for(experiment),
            )
            for field_name, edge_type in (
                ("sample_entity_ids", "EXPERIMENT_USES_SAMPLE"),
                ("material_entity_ids", "EXPERIMENT_USES_MATERIAL"),
                ("method_entity_ids", "EXPERIMENT_USES_METHOD"),
            ):
                for local_id in experiment.get(field_name) or []:
                    target = entity_ids.get(str(local_id))
                    if target:
                        _insert_edge(
                            edges,
                            edge_type=edge_type,
                            from_node_id=node_id,
                            to_node_id=target,
                            source_document_id=document_id,
                            source_record_type="experiment",
                            source_record_id=experiment_local_id,
                            evidence=evidence_for(experiment),
                            confidence=confidence_for(experiment),
                            review_status=review_status_for(experiment),
                        )

        for observation in extraction.get("observations") or []:
            if not observation.get("id"):
                continue
            observation_local_id = str(observation["id"])
            node_id = _upsert_node(
                nodes,
                node_key=paper_node_key(
                    "observation",
                    document_key,
                    observation_local_id,
                ),
                node_type="observation",
                label=(
                    compact_text(observation.get("metric_name"), 240)
                    or observation_local_id
                ),
                canonical_name=compact_text(
                    observation.get("metric_name"),
                    240,
                ),
                local_id=compact_text(observation_local_id, 160),
                data=observation,
                evidence=evidence_for(observation),
                confidence=confidence_for(observation),
                review_status=review_status_for(observation),
                source_document_id=document_id,
            )
            experiment_node_id = experiment_ids.get(
                str(observation.get("experiment_id") or "")
            )
            _insert_edge(
                edges,
                edge_type=(
                    "EXPERIMENT_PRODUCES_OBSERVATION"
                    if experiment_node_id
                    else "PAPER_REPORTS_OBSERVATION"
                ),
                from_node_id=experiment_node_id or paper_node_id,
                to_node_id=node_id,
                source_document_id=document_id,
                source_record_type="observation",
                source_record_id=observation_local_id,
                evidence=evidence_for(observation),
                confidence=confidence_for(observation),
                review_status=review_status_for(observation),
            )
            for field_name, edge_type in (
                ("sample_entity_id", "OBSERVATION_OF_SAMPLE"),
                ("property_entity_id", "OBSERVATION_MEASURES_PROPERTY"),
                ("method_entity_id", "OBSERVATION_MEASURED_BY"),
            ):
                target = entity_ids.get(
                    str(observation.get(field_name) or "")
                )
                if target:
                    _insert_edge(
                        edges,
                        edge_type=edge_type,
                        from_node_id=node_id,
                        to_node_id=target,
                        source_document_id=document_id,
                        source_record_type="observation",
                        source_record_id=observation_local_id,
                        evidence=evidence_for(observation),
                        confidence=confidence_for(observation),
                        review_status=review_status_for(observation),
                    )

        for claim in extraction.get("claims") or []:
            if not claim.get("id"):
                continue
            claim_local_id = str(claim["id"])
            node_id = _upsert_node(
                nodes,
                node_key=paper_node_key(
                    "claim",
                    document_key,
                    claim_local_id,
                ),
                node_type="claim",
                label=(
                    compact_text(claim.get("statement"), 600)
                    or claim_local_id
                ),
                canonical_name=compact_text(claim.get("claim_type"), 120),
                local_id=compact_text(claim_local_id, 160),
                data=claim,
                evidence=evidence_for(claim),
                confidence=confidence_for(claim),
                review_status=review_status_for(claim),
                source_document_id=document_id,
            )
            _insert_edge(
                edges,
                edge_type="PAPER_ASSERTS_CLAIM",
                from_node_id=paper_node_id,
                to_node_id=node_id,
                source_document_id=document_id,
                source_record_type="claim",
                source_record_id=claim_local_id,
                evidence=evidence_for(claim),
                confidence=confidence_for(claim),
                review_status=review_status_for(claim),
            )

    metadata = {
        "extraction_schema_versions": dict(sorted(extraction_versions.items())),
        "prompt_versions": dict(sorted(prompt_versions.items())),
        "extraction_models": dict(sorted(extraction_models.items())),
        "requested_models": dict(sorted(requested_models.items())),
        "evidence_validation_distribution": dict(
            sorted(evidence_validations.items())
        ),
        "extraction_timestamp_min": (
            min(extraction_timestamps) if extraction_timestamps else None
        ),
        "extraction_timestamp_max": (
            max(extraction_timestamps) if extraction_timestamps else None
        ),
    }
    return papers, nodes, edges, metadata


def freeze_stage1_archive(
    *,
    archive_path: Path,
    output_directory: Path,
    snapshot_id: str,
    knowledge_level: str,
    domain: str,
    expected_papers: int,
    allowed_systems: set[str],
    repository_root: Path,
    ontology_version: str = DEFAULT_ONTOLOGY_VERSION,
    frozen_at: str | None = None,
    selected_entries: set[str] | None = None,
    git_state: dict[str, Any] | None = None,
    corpus: dict[str, Any] | None = None,
    selection: dict[str, Any] | None = None,
    coverage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    archive_path = archive_path.resolve()
    output_directory = output_directory.resolve()
    repository_root = repository_root.resolve()
    if output_directory.exists():
        raise FileExistsError(
            f"Snapshot directory already exists and will not be overwritten: "
            f"{output_directory}"
        )

    resolved_git_state = git_state or _git_state(repository_root)
    freeze_timestamp = frozen_at or datetime.now(timezone.utc).isoformat()
    archive_sha256 = sha256_file(archive_path)

    with zipfile.ZipFile(archive_path) as archive:
        all_entries = sorted(
            (
                entry
                for entry in archive.infolist()
                if entry.filename.startswith("json/")
                and entry.filename.lower().endswith(".json")
            ),
            key=lambda entry: entry.filename,
        )
        if selected_entries is None:
            entries = all_entries
        else:
            available_names = {entry.filename for entry in all_entries}
            missing_entries = sorted(selected_entries - available_names)
            if missing_entries:
                raise ValueError(
                    "Selected archive entries are missing: "
                    + ", ".join(missing_entries)
                )
            entries = [
                entry
                for entry in all_entries
                if entry.filename in selected_entries
            ]
        artifacts: list[tuple[str, bytes, dict[str, Any]]] = []
        for entry in entries:
            raw_json = archive.read(entry)
            artifacts.append(
                (
                    entry.filename,
                    raw_json,
                    json.loads(raw_json.decode("utf-8")),
                )
            )
        dataset_manifest = json.loads(
            archive.read("dataset-manifest.json").decode("utf-8")
        )

    papers, nodes, edges, extraction_metadata = _build_graph(
        artifacts,
        allowed_systems,
    )
    if len(papers) != expected_papers:
        raise ValueError(
            f"Expected {expected_papers} papers, found {len(papers)}"
        )
    if any(not paper["raw_pdf_sha256"] for paper in papers):
        raise ValueError("Every paper must have a raw PDF SHA256")
    if len({paper["structured_json_sha256"] for paper in papers}) != len(papers):
        raise ValueError("Structured JSON hashes must be unique per paper")

    node_type_distribution = Counter(
        node["node_type"] for node in nodes.values()
    )
    relation_distribution = Counter(
        edge["edge_type"] for edge in edges.values()
    )
    review_status_distribution = Counter(
        node["review_status"] for node in nodes.values()
    )

    ontology = {
        "ontology_version": ontology_version,
        "description": (
            "Frozen projection of Stage 1 catalysis artifacts using the "
            "current production graph semantics."
        ),
        "node_types": list(NODE_TYPES),
        "relation_types": list(RELATION_TYPES),
        "global_node_types": ["entity", "keyword"],
        "paper_scoped_node_types": [
            "paper",
            "experiment",
            "observation",
            "claim",
        ],
        "provenance_fields": [
            "source_document_id",
            "source_record_type",
            "source_record_id",
            "evidence",
            "confidence",
            "review_status",
        ],
    }

    output_directory.parent.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(
        tempfile.mkdtemp(
            prefix=f".{output_directory.name}-",
            dir=output_directory.parent,
        )
    )
    try:
        paper_ids_path = temporary_root / "paper_ids.txt"
        papers_path = temporary_root / "papers.jsonl"
        nodes_path = temporary_root / "nodes.jsonl.gz"
        edges_path = temporary_root / "edges.jsonl.gz"
        ontology_path = temporary_root / "ontology.json"

        paper_ids_path.write_text(
            "".join(f"{paper['paper_id']}\n" for paper in papers),
            encoding="utf-8",
            newline="\n",
        )
        _write_jsonl(papers_path, papers)
        _write_jsonl_gzip(
            nodes_path,
            sorted(nodes.values(), key=lambda item: item["id"]),
        )
        _write_jsonl_gzip(
            edges_path,
            sorted(edges.values(), key=lambda item: item["id"]),
        )
        _write_json(ontology_path, ontology)

        artifact_files = {
            "paper_ids": {
                "path": "paper_ids.txt",
                "sha256": sha256_file(paper_ids_path),
                "count": len(papers),
            },
            "papers": {
                "path": "papers.jsonl",
                "sha256": sha256_file(papers_path),
                "count": len(papers),
            },
            "nodes": {
                "path": "nodes.jsonl.gz",
                "sha256": sha256_file(nodes_path),
                "count": len(nodes),
            },
            "edges": {
                "path": "edges.jsonl.gz",
                "sha256": sha256_file(edges_path),
                "count": len(edges),
            },
            "ontology": {
                "path": "ontology.json",
                "sha256": sha256_file(ontology_path),
            },
        }
        snapshot_content_hash = canonical_hash(
            _snapshot_hash_identity(
                snapshot_id=snapshot_id,
                knowledge_level=knowledge_level,
                source_archive_sha256=archive_sha256,
                artifact_files=artifact_files,
                ontology_version=ontology_version,
                corpus=corpus,
                selection=selection,
                coverage=coverage,
            )
        )
        try:
            source_path = str(archive_path.relative_to(repository_root))
        except ValueError:
            source_path = str(archive_path)

        manifest = {
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "snapshot_id": snapshot_id,
            "knowledge_level": knowledge_level,
            "domain": domain,
            "status": "frozen",
            "frozen_at": freeze_timestamp,
            "snapshot_content_hash": snapshot_content_hash,
            "source_archive": {
                "path": source_path.replace("\\", "/"),
                "sha256": archive_sha256,
                "bytes": archive_path.stat().st_size,
                "dataset_manifest": dataset_manifest,
                "dataset_generated_at": dataset_manifest.get("generatedAt"),
            },
            "paper_count": len(papers),
            "raw_pdf_hash_count": len(
                {paper["raw_pdf_sha256"] for paper in papers}
            ),
            "structured_json_hash_count": len(
                {paper["structured_json_sha256"] for paper in papers}
            ),
            "graph": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "node_type_distribution": dict(
                    sorted(node_type_distribution.items())
                ),
                "relation_distribution": dict(
                    sorted(relation_distribution.items())
                ),
                "node_review_status_distribution": dict(
                    sorted(review_status_distribution.items())
                ),
            },
            "paper_distributions": paper_distributions(papers),
            "extraction": extraction_metadata,
            "ontology": {
                "version": ontology_version,
                "manifest": "ontology.json",
            },
            "artifacts": artifact_files,
            "generation": {
                "freezer_version": FREEZER_VERSION,
                "code": resolved_git_state,
                "allowed_systems": sorted(allowed_systems),
                "paper_ordering": "lexicographic ZIP entry path",
                "overwrite_policy": "forbidden",
                "selected_entry_count": len(entries),
            },
        }
        if corpus is not None:
            manifest["corpus"] = corpus
        if selection is not None:
            manifest["selection"] = selection
        if coverage is not None:
            manifest["coverage"] = coverage
        _write_json(temporary_root / "manifest.json", manifest)
        temporary_root.replace(output_directory)
        return manifest
    except BaseException:
        shutil.rmtree(temporary_root, ignore_errors=True)
        raise


def verify_snapshot(snapshot_directory: Path) -> dict[str, Any]:
    snapshot_directory = snapshot_directory.resolve()
    manifest = json.loads(
        (snapshot_directory / "manifest.json").read_text(encoding="utf-8")
    )
    failures: list[str] = []
    for name, artifact in manifest.get("artifacts", {}).items():
        path = snapshot_directory / artifact["path"]
        if not path.is_file():
            failures.append(f"Missing artifact: {name}")
            continue
        actual_hash = sha256_file(path)
        if actual_hash != artifact["sha256"]:
            failures.append(
                f"Hash mismatch for {name}: {actual_hash} != "
                f"{artifact['sha256']}"
            )

    expected_content_hash = canonical_hash(
        _snapshot_hash_identity(
            snapshot_id=manifest["snapshot_id"],
            knowledge_level=manifest["knowledge_level"],
            source_archive_sha256=manifest["source_archive"]["sha256"],
            artifact_files=manifest["artifacts"],
            ontology_version=manifest["ontology"]["version"],
            corpus=manifest.get("corpus"),
            selection=manifest.get("selection"),
            coverage=manifest.get("coverage"),
        )
    )
    if expected_content_hash != manifest.get("snapshot_content_hash"):
        failures.append("Snapshot content hash mismatch")

    papers_path = snapshot_directory / manifest["artifacts"]["papers"]["path"]
    paper_ids_path = (
        snapshot_directory / manifest["artifacts"]["paper_ids"]["path"]
    )
    nodes_path = snapshot_directory / manifest["artifacts"]["nodes"]["path"]
    edges_path = snapshot_directory / manifest["artifacts"]["edges"]["path"]

    papers = _read_jsonl(papers_path)
    paper_ids = [
        line.strip()
        for line in paper_ids_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    nodes = _read_jsonl_gzip(nodes_path)
    edges = _read_jsonl_gzip(edges_path)

    if len(papers) != manifest["paper_count"]:
        failures.append("Paper count does not match manifest")
    if len(paper_ids) != manifest["paper_count"]:
        failures.append("Paper ID count does not match manifest")
    if paper_ids != [paper["paper_id"] for paper in papers]:
        failures.append("Paper ID list does not match papers.jsonl ordering")
    if len(set(paper_ids)) != len(paper_ids):
        failures.append("Duplicate paper IDs detected")
    if len({paper["raw_pdf_sha256"] for paper in papers}) != manifest[
        "raw_pdf_hash_count"
    ]:
        failures.append("Raw PDF hash count does not match manifest")
    if len({paper["structured_json_sha256"] for paper in papers}) != manifest[
        "structured_json_hash_count"
    ]:
        failures.append("Structured JSON hash count does not match manifest")

    node_ids = [node["id"] for node in nodes]
    edge_ids = [edge["id"] for edge in edges]
    if len(nodes) != manifest["graph"]["node_count"]:
        failures.append("Node count does not match manifest")
    if len(edges) != manifest["graph"]["edge_count"]:
        failures.append("Edge count does not match manifest")
    if len(set(node_ids)) != len(node_ids):
        failures.append("Duplicate node IDs detected")
    if len(set(edge_ids)) != len(edge_ids):
        failures.append("Duplicate edge IDs detected")

    node_id_set = set(node_ids)
    dangling_edges = [
        edge["id"]
        for edge in edges
        if edge["from_node_id"] not in node_id_set
        or edge["to_node_id"] not in node_id_set
    ]
    if dangling_edges:
        failures.append(f"Dangling edges detected: {len(dangling_edges)}")

    node_type_distribution = dict(
        sorted(Counter(node["node_type"] for node in nodes).items())
    )
    relation_distribution = dict(
        sorted(Counter(edge["edge_type"] for edge in edges).items())
    )
    if node_type_distribution != manifest["graph"]["node_type_distribution"]:
        failures.append("Node type distribution does not match manifest")
    if relation_distribution != manifest["graph"]["relation_distribution"]:
        failures.append("Relation distribution does not match manifest")
    if manifest.get("paper_distributions") is not None and (
        paper_distributions(papers) != manifest["paper_distributions"]
    ):
        failures.append("Paper distributions do not match manifest")

    repository_root = next(
        (
            parent
            for parent in (snapshot_directory, *snapshot_directory.parents)
            if (parent / ".git").exists()
        ),
        snapshot_directory.parents[2],
    )
    source_archive_path = repository_root / manifest["source_archive"]["path"]
    source_archive_valid: bool | None = None
    if source_archive_path.is_file():
        source_archive_valid = (
            sha256_file(source_archive_path)
            == manifest["source_archive"]["sha256"]
        )
        if not source_archive_valid:
            failures.append("Source archive hash mismatch")

    return {
        "snapshot_id": manifest.get("snapshot_id"),
        "valid": not failures,
        "failures": failures,
        "snapshot_content_hash": manifest.get("snapshot_content_hash"),
        "paper_count": manifest.get("paper_count"),
        "node_count": manifest.get("graph", {}).get("node_count"),
        "edge_count": manifest.get("graph", {}).get("edge_count"),
        "relation_distribution": relation_distribution,
        "dangling_edge_count": len(dangling_edges),
        "source_archive_valid": source_archive_valid,
    }
