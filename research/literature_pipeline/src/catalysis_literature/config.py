from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .hashing import content_hash


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ParserConfig(StrictModel):
    engine: Literal["auto", "pymupdf", "pypdf", "markdown"] = "auto"
    docling_fallback: bool = True
    min_document_characters: int = 200
    max_empty_page_ratio: float = 0.6
    max_replacement_ratio: float = 0.02
    fail_on_low_quality: bool = False


class ChunkingConfig(StrictModel):
    target_tokens: int = 500
    overlap_tokens: int = 60
    min_tokens: int = 80
    exclude_references: bool = True

    @model_validator(mode="after")
    def validate_sizes(self) -> "ChunkingConfig":
        if self.target_tokens < 100:
            raise ValueError("target_tokens must be at least 100")
        if not 0 <= self.overlap_tokens < self.target_tokens:
            raise ValueError("overlap_tokens must be smaller than target_tokens")
        return self


class ExtractionConfig(StrictModel):
    enabled: bool = True
    provider: Literal["deepseek", "zhipu", "mock"] = "deepseek"
    model: str = "deepseek-v4-flash"
    base_url: str = "https://api.deepseek.com"
    temperature: float = 0.0
    seed: int = 20260827
    max_tokens_core: int = 8000
    max_tokens_data: int = 8000
    max_context_tokens_core: int = 7000
    max_context_tokens_data: int = 7000
    workers: int = 4
    requests_per_minute: int = 60
    prompt_version: str = "catalysis-paper-extraction-v2.1"


class IndexConfig(StrictModel):
    enabled: bool = True
    backend: Literal["auto", "lancedb", "portable"] = "auto"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embedding_revision: str = "default"
    embedding_batch_size: int = 64
    vector_dimensions: int = 384
    allow_hash_embedding_fallback: bool = False
    top_k_dense: int = 40
    top_k_lexical: int = 40
    top_k_final: int = 12
    max_records_per_paper: int = 2
    context_token_budget: int = 6000


class ExecutionConfig(StrictModel):
    large_run_threshold: int = 100
    result_progress_interval: int = 25

    @model_validator(mode="after")
    def validate_execution(self) -> "ExecutionConfig":
        if self.large_run_threshold < 1:
            raise ValueError("large_run_threshold must be at least 1")
        if self.result_progress_interval < 1:
            raise ValueError("result_progress_interval must be at least 1")
        return self


class PipelineConfig(StrictModel):
    schema_version: str = "literature_pipeline_config.v1"
    source: Path
    workspace: Path = Path("research/literature_pipeline/workspace")
    collection_hint: str | None = None
    parser: ParserConfig = Field(default_factory=ParserConfig)
    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)
    extraction: ExtractionConfig = Field(default_factory=ExtractionConfig)
    index: IndexConfig = Field(default_factory=IndexConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)

    def resolved(self, base: Path) -> "PipelineConfig":
        payload = self.model_dump()
        for field in ("source", "workspace"):
            path = Path(payload[field])
            payload[field] = path if path.is_absolute() else (base / path).resolve()
        return PipelineConfig.model_validate(payload)

    @property
    def config_hash(self) -> str:
        payload = self.model_dump(mode="json")
        return content_hash(payload)


def load_config(path: Path) -> PipelineConfig:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Pipeline config must be a YAML object")
    return PipelineConfig.model_validate(payload).resolved(path.resolve().parent)
