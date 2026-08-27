from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


EXTRACTION_SCHEMA_VERSION = "catalysis_paper_extraction.v2"
RUN_SCHEMA_VERSION = "literature_run.v1"
INDEX_SCHEMA_VERSION = "rag_index.v1"
PARSED_DOCUMENT_SCHEMA_VERSION = "parsed_document.v1"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceRecord(StrictModel):
    pdf_page_index: int = Field(ge=1)
    section: str | None = None
    source: Literal["text", "table", "figure", "caption", "supporting_information"] = "text"
    source_id: str | None = None
    quote: str = Field(min_length=1)
    evidence_validation: Literal["exact", "locally_recovered", "unverified"] | None = None


class KeywordRecord(StrictModel):
    id: str
    raw_term: str
    normalized_term: str
    category: str = "other"
    importance: Literal["core", "supporting"] = "supporting"
    definition_in_context: str | None = None
    source_scope: str | None = None
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    needs_visual_review: bool = False
    review_status: Literal["extracted", "needs_review"] | None = None


class EntityRecord(StrictModel):
    id: str
    type: str = "other"
    canonical_name: str
    zh_name: str | None = None
    aliases: list[str] = Field(default_factory=list)
    identifiers: dict[str, Any] = Field(default_factory=dict)
    attributes: dict[str, Any] = Field(default_factory=dict)
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    needs_visual_review: bool = False
    review_status: Literal["extracted", "needs_review"] | None = None


class ExperimentRecord(StrictModel):
    id: str
    experiment_type: str = "other"
    objective: str | None = None
    sample_entity_ids: list[str] = Field(default_factory=list)
    material_entity_ids: list[str] = Field(default_factory=list)
    method_entity_ids: list[str] = Field(default_factory=list)
    conditions: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    needs_visual_review: bool = False
    review_status: Literal["extracted", "needs_review"] | None = None


class ObservationRecord(StrictModel):
    id: str
    experiment_id: str | None = None
    sample_entity_id: str | None = None
    property_entity_id: str | None = None
    method_entity_id: str | None = None
    metric_name: str
    numeric_value: float | None = None
    text_value: str | None = None
    unit: str | None = None
    raw_value: str | None = None
    uncertainty: float | str | None = None
    comparison_operator: str = "not_applicable"
    conditions: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    needs_visual_review: bool = False
    review_status: Literal["extracted", "needs_review"] | None = None

    @model_validator(mode="after")
    def require_value(self) -> "ObservationRecord":
        if self.numeric_value is None and not self.text_value and not self.raw_value:
            raise ValueError("observation requires numeric_value, text_value, or raw_value")
        return self


class ClaimRecord(StrictModel):
    id: str
    claim_type: str = "reported_result"
    statement: str
    evidence_basis: str = "unclear"
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    needs_visual_review: bool = False
    review_status: Literal["extracted", "needs_review"] | None = None


class PageRecord(StrictModel):
    page_index: int = Field(ge=1)
    text: str
    blocks: list[dict[str, Any]] = Field(default_factory=list)


class ChunkRecord(StrictModel):
    chunk_id: str
    paper_id: str
    kind: str = "section"
    section: str | None = None
    page_start: int = Field(ge=1)
    page_end: int = Field(ge=1)
    text: str
    token_count: int = Field(ge=1)
    source_text_sha256: str


class ParsedDocument(StrictModel):
    schema_version: str = PARSED_DOCUMENT_SCHEMA_VERSION
    paper_id: str
    source_path: str
    source_pdf_sha256: str
    parser_name: str
    parser_version: str
    parser_config_hash: str
    page_count: int = Field(ge=1)
    extracted_characters: int = Field(ge=0)
    extracted_text_sha256: str
    quality: dict[str, Any]
    pages: list[PageRecord]
    chunks: list[ChunkRecord]


class PaperArtifactV2(StrictModel):
    schema_version: str = EXTRACTION_SCHEMA_VERSION
    paper: dict[str, Any]
    abstract: dict[str, Any]
    summary: dict[str, Any]
    keywords: dict[str, Any]
    entities: list[EntityRecord]
    experiments: list[ExperimentRecord]
    observations: list[ObservationRecord]
    claims: list[ClaimRecord]
    visual_review_items: list[dict[str, Any]] = Field(default_factory=list)
    quality: dict[str, Any]
    extraction_metadata: dict[str, Any]

    @model_validator(mode="after")
    def validate_references_and_pages(self) -> "PaperArtifactV2":
        page_count = int(self.paper.get("page_count") or 0)
        entity_ids = {item.id for item in self.entities}
        experiment_ids = {item.id for item in self.experiments}
        containers: list[Any] = []
        containers.extend(self.entities)
        containers.extend(self.experiments)
        containers.extend(self.observations)
        containers.extend(self.claims)
        for keyword in self.keywords.get("extracted") or []:
            containers.append(KeywordRecord.model_validate(keyword))
        for finding in self.summary.get("main_findings") or []:
            if isinstance(finding, dict):
                containers.append(finding)
        for item in containers:
            evidence = item.get("evidence", []) if isinstance(item, dict) else item.evidence
            for entry in evidence:
                record = (
                    EvidenceRecord.model_validate(entry)
                    if isinstance(entry, dict)
                    else entry
                )
                if page_count and record.pdf_page_index > page_count:
                    raise ValueError("evidence page exceeds PDF page count")
        for experiment in self.experiments:
            references = (
                experiment.sample_entity_ids
                + experiment.material_entity_ids
                + experiment.method_entity_ids
            )
            if set(references) - entity_ids:
                raise ValueError(f"{experiment.id} references an unknown entity")
        for observation in self.observations:
            if observation.experiment_id and observation.experiment_id not in experiment_ids:
                raise ValueError(f"{observation.id} references an unknown experiment")
            for identifier in (
                observation.sample_entity_id,
                observation.property_entity_id,
                observation.method_entity_id,
            ):
                if identifier and identifier not in entity_ids:
                    raise ValueError(f"{observation.id} references an unknown entity")
        return self
