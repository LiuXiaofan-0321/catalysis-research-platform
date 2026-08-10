from __future__ import annotations

from pathlib import Path
from typing import TypedDict


LAYOUT_SCHEMA_VERSION = "research_layout.v1"

REQUIRED_DIRECTORIES = (
    "configs",
    "models",
    "kg_snapshots",
    "prompts",
    "experiments",
    "benchmarks",
    "descriptors",
    "datasets",
    "runs",
    "evaluation",
    "statistics",
    "manifests",
    "scripts",
    "reports",
)

REQUIRED_DOCUMENTS = (
    "CURRENT_ARCHITECTURE.md",
    "NMI_GAP_ANALYSIS.md",
    "RESEARCH_IMPLEMENTATION_PLAN.md",
    "EXPERIMENT_PROTOCOL.md",
)


class DirectoryStatus(TypedDict):
    path: str
    exists: bool
    is_directory: bool


class DocumentStatus(TypedDict):
    path: str
    exists: bool
    is_file: bool


class LayoutStatus(TypedDict):
    schema_version: str
    research_root: str
    repository_root: str
    valid: bool
    directories: dict[str, DirectoryStatus]
    documents: dict[str, DocumentStatus]


def default_research_root() -> Path:
    return Path(__file__).resolve().parents[2]


def inspect_layout(root: Path | None = None) -> LayoutStatus:
    research_root = (root or default_research_root()).resolve()
    repository_root = research_root.parent
    directories: dict[str, DirectoryStatus] = {}
    documents: dict[str, DocumentStatus] = {}

    for name in REQUIRED_DIRECTORIES:
        path = research_root / name
        directories[name] = {
            "path": str(path),
            "exists": path.exists(),
            "is_directory": path.is_dir(),
        }

    for name in REQUIRED_DOCUMENTS:
        path = repository_root / name
        documents[name] = {
            "path": str(path),
            "exists": path.exists(),
            "is_file": path.is_file(),
        }

    return {
        "schema_version": LAYOUT_SCHEMA_VERSION,
        "research_root": str(research_root),
        "repository_root": str(repository_root),
        "valid": (
            all(item["is_directory"] for item in directories.values())
            and all(item["is_file"] for item in documents.values())
        ),
        "directories": directories,
        "documents": documents,
    }
