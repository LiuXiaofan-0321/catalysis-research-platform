from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

from catalysis_literature.hashing import canonical_json, content_hash, stable_id


SUPPORTED_SUFFIXES = {".md", ".pdf"}
EXCLUDED_DIRECTORY_SUFFIXES = ("_spectra", "_null")
IGNORED_ASSET_DIRECTORIES = {
    "__pycache__",
    "assets",
    "figures",
    "images",
    "imgs",
}
PMC_PATTERN = re.compile(r"PMC\d+", re.IGNORECASE)


def _excluded_directory(name: str) -> bool:
    return name.casefold().endswith(EXCLUDED_DIRECTORY_SUFFIXES)


def _paper_identity(name: str) -> tuple[str, str | None] | None:
    lowered = name.casefold()
    if lowered.startswith("10.") and "_" in name:
        doi = name.replace("_", "/", 1).casefold()
        return f"doi:{doi}", doi
    if PMC_PATTERN.fullmatch(name):
        return f"pmc:{lowered}", None
    return None


def _article_root(path: Path, corpus_root: Path) -> tuple[Path, str, str | None] | None:
    for parent in (path.parent, *path.parents):
        if parent == corpus_root:
            break
        identity = _paper_identity(parent.name)
        if identity is not None:
            ancestors = []
            for ancestor in parent.parents:
                if ancestor == corpus_root:
                    break
                ancestors.append(ancestor.name.casefold())
            # ACS SI folders often repeat the DOI with a `_supporting` suffix.
            # They are documents of the enclosing article, not article roots.
            if "si-output" in ancestors:
                continue
            return parent, identity[0], identity[1]
    return None


def _document_type(path: Path, article_root: Path) -> str:
    relative = path.relative_to(article_root)
    values = [part.casefold() for part in relative.parts]
    joined = "/".join(values)
    if any(
        marker in joined
        for marker in (
            "si-output",
            "supporting",
            "supplementary",
            "supp_info",
            "supp-info",
        )
    ):
        return "si"
    stem = path.stem.casefold()
    if re.search(r"(?:^|[._-])si(?:$|[._-])", stem):
        return "si"
    return "main"


def _candidate_score(path: Path, document_type: str) -> tuple[int, int, str]:
    relative = str(path).casefold()
    score = 100 if path.suffix.casefold() == ".md" else 0
    if document_type == "main" and "main-output" in relative:
        score += 20
    if document_type == "si" and "si-output" in relative:
        score += 20
    return score, -len(path.parts), relative


def _si_key(path: Path, article_root: Path) -> str:
    relative = path.relative_to(article_root)
    parts = list(relative.parts)
    lowered = [part.casefold() for part in parts]
    if "si-output" in lowered:
        index = lowered.index("si-output")
        if index + 1 < len(parts) - 1:
            return parts[index + 1].casefold()
    stem = path.stem.casefold()
    for suffix in ("_supporting", "-supporting", "_supplementary", "-supplementary"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem


def discover_records(corpus_root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = corpus_root.resolve()
    candidates: dict[tuple[str, str], list[tuple[Path, str, str | None]]] = defaultdict(list)
    excluded = Counter()
    ignored_assets = Counter()
    scanned_files = 0
    for directory, directory_names, file_names in os.walk(root):
        kept: list[str] = []
        for name in directory_names:
            if _excluded_directory(name):
                excluded[name] += 1
            elif name.casefold() in IGNORED_ASSET_DIRECTORIES:
                ignored_assets[name] += 1
            else:
                kept.append(name)
        directory_names[:] = kept
        directory_path = Path(directory)
        for name in file_names:
            path = directory_path / name
            if path.suffix.casefold() not in SUPPORTED_SUFFIXES:
                continue
            scanned_files += 1
            article = _article_root(path, root)
            if article is None:
                continue
            article_directory, paper_id, doi = article
            candidates[(paper_id, str(article_directory))].append(
                (path.resolve(), _document_type(path, article_directory), doi)
            )

    bundles_by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for (paper_id, article_directory_text), files in candidates.items():
        article_directory = Path(article_directory_text)
        main_candidates = [path for path, kind, _ in files if kind == "main"]
        main = (
            max(main_candidates, key=lambda path: _candidate_score(path, "main"))
            if main_candidates
            else None
        )
        si_candidates: dict[str, list[Path]] = defaultdict(list)
        for path, kind, _ in files:
            if kind == "si":
                si_candidates[_si_key(path, article_directory)].append(path)
        si_paths = [
            max(paths, key=lambda path: _candidate_score(path, "si"))
            for _, paths in sorted(si_candidates.items())
        ]
        relative = article_directory.relative_to(root)
        collection = relative.parts[0]
        doi = next((value for _, _, value in files if value), None)
        bundles_by_paper[paper_id].append(
            {
                "paper_id": paper_id,
                "doi": doi,
                "article_directory": article_directory,
                "collection": collection,
                "main": main,
                "si": sorted(si_paths, key=lambda path: str(path).casefold()),
            }
        )

    selected_bundles: list[dict[str, Any]] = []
    duplicate_paper_count = 0
    for paper_id, bundles in sorted(bundles_by_paper.items()):
        duplicate_paper_count += max(0, len(bundles) - 1)

        def bundle_score(bundle: dict[str, Any]) -> tuple[int, int, int, str]:
            main = bundle["main"]
            return (
                int(main is not None and main.suffix.casefold() == ".md"),
                int(main is not None),
                sum(path.suffix.casefold() == ".md" for path in bundle["si"]),
                str(bundle["article_directory"]).casefold(),
            )

        selected_bundles.append(max(bundles, key=bundle_score))

    records: list[dict[str, Any]] = []
    missing_main = 0
    orphan_si_documents = 0
    included_papers = 0
    for bundle in selected_bundles:
        main = bundle["main"]
        if main is None:
            missing_main += 1
            orphan_si_documents += len(bundle["si"])
            continue
        included_papers += 1
        selection_index = included_papers
        common = {
            "paper_id": bundle["paper_id"],
            "doi": bundle["doi"],
            "source_collection": bundle["collection"],
            "source_article_directory": str(bundle["article_directory"]),
            "selection_index": selection_index,
        }
        records.append(
            {
                "path": str(main),
                "document_id": stable_id("document", bundle["paper_id"], "main"),
                "document_type": "main",
                **common,
            }
        )
        for si_index, path in enumerate(bundle["si"], start=1):
            records.append(
                {
                    "path": str(path),
                    "document_id": stable_id(
                        "document",
                        bundle["paper_id"],
                        "si",
                        str(path.relative_to(bundle["article_directory"])).casefold(),
                    ),
                    "document_type": "si",
                    "si_index": si_index,
                    **common,
                }
            )
    summary = {
        "schema_version": "full_corpus_selection.v1",
        "corpus_root": str(root),
        "excluded_directory_suffixes": list(EXCLUDED_DIRECTORY_SUFFIXES),
        "excluded_directories": dict(sorted(excluded.items())),
        "ignored_asset_directories": dict(sorted(ignored_assets.items())),
        "scanned_candidate_files": scanned_files,
        "discovered_paper_identity_count": len(selected_bundles),
        "paper_count": included_papers,
        "document_count": len(records),
        "main_document_count": sum(row["document_type"] == "main" for row in records),
        "si_document_count": sum(row["document_type"] == "si" for row in records),
        "missing_main_paper_count": missing_main,
        "excluded_orphan_si_document_count": orphan_si_documents,
        "duplicate_paper_bundle_count": duplicate_paper_count,
        "selection_hash": content_hash(records),
    }
    return records, summary


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(f"{canonical_json(record)}\n" for record in records),
        encoding="utf-8",
        newline="\n",
    )


def write_outputs(
    *,
    records: list[dict[str, Any]],
    summary: dict[str, Any],
    output_directory: Path,
    batch_size: int,
    config_template: Path | None,
    config_output_directory: Path | None,
    workspace: Path | None,
) -> dict[str, Any]:
    output = output_directory.resolve()
    master = output / "master.jsonl"
    _write_jsonl(master, records)
    records_by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        records_by_paper[record["paper_id"]].append(record)
    paper_ids = sorted(records_by_paper)
    shards: list[dict[str, Any]] = []
    for start in range(0, len(paper_ids), batch_size):
        shard_number = len(shards) + 1
        shard_id = f"shard-{shard_number:04d}"
        selected_ids = paper_ids[start : start + batch_size]
        shard_records = [
            record for paper_id in selected_ids for record in records_by_paper[paper_id]
        ]
        path = output / "shards" / f"{shard_id}.jsonl"
        _write_jsonl(path, shard_records)
        shards.append(
            {
                "shard_id": shard_id,
                "path": str(path),
                "paper_count": len(selected_ids),
                "document_count": len(shard_records),
                "content_hash": content_hash(shard_records),
            }
        )
    summary = {**summary, "batch_size": batch_size, "batch_count": len(shards), "shards": shards}
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    if config_template is not None:
        if config_output_directory is None or workspace is None:
            raise ValueError("Config output directory and workspace are required")
        template = yaml.safe_load(config_template.read_text(encoding="utf-8"))
        config_output_directory.mkdir(parents=True, exist_ok=True)
        for shard in shards:
            payload = dict(template)
            payload["source"] = shard["path"]
            payload["workspace"] = str(workspace.resolve())
            (config_output_directory / f"{shard['shard_id']}.yaml").write_text(
                yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
                newline="\n",
            )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-root", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=200)
    parser.add_argument("--config-template", type=Path)
    parser.add_argument("--config-output-directory", type=Path)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if args.batch_size < 1:
        raise ValueError("--batch-size must be at least 1")
    output = args.output_directory.resolve()
    if output.exists():
        if not args.overwrite:
            raise FileExistsError(output)
        shutil.rmtree(output)
    config_output = (
        args.config_output_directory.resolve()
        if args.config_output_directory is not None
        else None
    )
    if config_output is not None and config_output.exists():
        if not args.overwrite:
            raise FileExistsError(config_output)
        shutil.rmtree(config_output)
    records, summary = discover_records(args.corpus_root)
    summary = write_outputs(
        records=records,
        summary=summary,
        output_directory=output,
        batch_size=args.batch_size,
        config_template=args.config_template,
        config_output_directory=config_output,
        workspace=args.workspace,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
