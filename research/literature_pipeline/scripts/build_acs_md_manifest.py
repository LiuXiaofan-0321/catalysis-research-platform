from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )


def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def stable_id(prefix: str, *parts: Any, length: int = 24) -> str:
    return f"{prefix}:{content_hash(parts)[:length]}"


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def canonical_doi(directory_name: str) -> str:
    return directory_name.replace("_", "/", 1).casefold()


def choose_main_pdf(article_directory: Path, article_name: str) -> Path | None:
    # ACS exports use either article/<pdf> or article/article/<pdf>.
    candidates = sorted(
        [
            *article_directory.glob("*.pdf"),
            *article_directory.glob("*/*.pdf"),
        ],
        key=lambda path: str(path).casefold(),
    )
    exact = [path for path in candidates if path.stem.casefold() == article_name.casefold()]
    return (exact or candidates or [None])[0]


def build_records(batch_directory: Path, limit: int) -> tuple[list[dict], dict]:
    articles = sorted(
        (path for path in batch_directory.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    )[:limit]
    if len(articles) != limit:
        raise RuntimeError(
            f"Requested {limit} papers but found only {len(articles)} in {batch_directory}"
        )

    records: list[dict] = []
    paper_rows: list[dict] = []
    for selection_index, article_directory in enumerate(articles, start=1):
        article_name = article_directory.name
        doi = canonical_doi(article_name)
        paper_id = f"doi:{doi}"
        main_candidates = sorted(
            article_directory.glob("*/main-output/*.md"),
            key=lambda path: str(path).casefold(),
        )
        if len(main_candidates) != 1:
            raise RuntimeError(
                f"Expected one main MD for {article_name}, found {len(main_candidates)}"
            )
        main_path = main_candidates[0].resolve()
        si_paths = sorted(
            article_directory.glob("*/si-output/*/*.md"),
            key=lambda path: str(path).casefold(),
        )
        original_pdf = choose_main_pdf(article_directory, article_name)
        common = {
            "paper_id": paper_id,
            "doi": doi,
            "publisher": "ACS",
            "source_collection": "ACS",
            "source_batch": batch_directory.name,
            "source_article_directory": str(article_directory.resolve()),
            "selection_index": selection_index,
            "original_pdf_path": str(original_pdf.resolve()) if original_pdf else None,
        }
        records.append(
            {
                "path": str(main_path),
                "document_id": stable_id("document", paper_id, "main"),
                "document_type": "main",
                **common,
            }
        )
        for si_index, si_path in enumerate(si_paths, start=1):
            records.append(
                {
                    "path": str(si_path.resolve()),
                    "document_id": stable_id(
                        "document",
                        paper_id,
                        "si",
                        str(si_path.relative_to(article_directory)).casefold(),
                    ),
                    "document_type": "si",
                    "si_index": si_index,
                    "si_name": si_path.stem,
                    **common,
                }
            )
        paper_rows.append(
            {
                "paper_id": paper_id,
                "doi": doi,
                "selection_index": selection_index,
                "main_md": str(main_path),
                "si_md_count": len(si_paths),
                "original_pdf_path": common["original_pdf_path"],
            }
        )

    summary = {
        "schema_version": "acs_md_selection.v1",
        "source_batch": str(batch_directory.resolve()),
        "selection_order": "case-insensitive article-directory name",
        "requested_papers": limit,
        "paper_count": len(paper_rows),
        "document_count": len(records),
        "main_document_count": len(paper_rows),
        "si_document_count": sum(row["si_md_count"] for row in paper_rows),
        "papers_with_si": sum(row["si_md_count"] > 0 for row in paper_rows),
        "papers_with_original_pdf": sum(bool(row["original_pdf_path"]) for row in paper_rows),
        "paper_ids": [row["paper_id"] for row in paper_rows],
        "selection_hash": content_hash(records),
        "papers": paper_rows,
    }
    return records, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if args.limit < 1:
        raise ValueError("--limit must be at least 1")
    output = args.output.resolve()
    summary_path = output.with_suffix(".summary.json")
    if not args.overwrite and (output.exists() or summary_path.exists()):
        raise FileExistsError(output)
    records, summary = build_records(args.batch_directory.resolve(), args.limit)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(f"{canonical_json(record)}\n" for record in records),
        encoding="utf-8",
        newline="\n",
    )
    write_json(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
