from __future__ import annotations

import gzip
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

from ..kg.freeze_stage1 import verify_snapshot
from .schema import EvidenceContractError


TERM_RE = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*|[\u4e00-\u9fff]+")


def _terms(value: Any) -> set[str]:
    return {term.casefold() for term in TERM_RE.findall(str(value or ""))}


def _gzip_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as source:
        for line in source:
            if line.strip():
                yield json.loads(line)


class FrozenKgRetriever:
    """Deterministic lexical seed plus bounded graph traversal for smoke tests."""

    def __init__(self, snapshot_directory: Path):
        self.snapshot_directory = snapshot_directory.resolve()
        report = verify_snapshot(self.snapshot_directory)
        if not report["valid"]:
            raise EvidenceContractError(
                "Invalid KG snapshot: " + "; ".join(report["failures"])
            )
        self.manifest = json.loads(
            (self.snapshot_directory / "manifest.json").read_text(encoding="utf-8")
        )
        self.nodes = {
            row["id"]: row
            for row in _gzip_jsonl(
                self.snapshot_directory / self.manifest["artifacts"]["nodes"]["path"]
            )
        }
        self.edges = list(
            _gzip_jsonl(
                self.snapshot_directory / self.manifest["artifacts"]["edges"]["path"]
            )
        )
        self.adjacency: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        for edge in self.edges:
            self.adjacency[edge["from_node_id"]].append(edge)
            self.adjacency[edge["to_node_id"]].append(edge)

    @staticmethod
    def _node_text(node: dict[str, Any]) -> str:
        return " ".join(
            (
                str(node.get("label") or ""),
                str(node.get("canonical_name") or ""),
                json.dumps(node.get("data") or {}, ensure_ascii=False, sort_keys=True),
            )
        )

    def retrieve(
        self,
        *,
        query: str,
        candidate_limit: int = 30,
        max_hops: int = 2,
    ) -> list[dict[str, Any]]:
        if not 0 <= max_hops <= 2:
            raise EvidenceContractError("max_hops must be between 0 and 2")
        query_terms = _terms(query)
        seeds: list[tuple[float, str]] = []
        for node_id, node in self.nodes.items():
            overlap = query_terms & _terms(self._node_text(node))
            if overlap:
                score = sum(1.0 + len(term) ** 0.5 for term in overlap)
                seeds.append((score, node_id))
        seeds.sort(key=lambda item: (-item[0], item[1]))
        candidates: dict[tuple[str, str, int, str], dict[str, Any]] = {}
        for seed_score, seed_id in seeds[:candidate_limit]:
            queue = deque([(seed_id, [], [], 0)])
            visited = {seed_id}
            while queue:
                node_id, path_nodes, path_edges, depth = queue.popleft()
                node = self.nodes[node_id]
                evidence_groups = [
                    (node.get("evidence") or [], "node", node_id, None)
                ]
                if path_edges:
                    edge = next(item for item in self.adjacency[node_id] if item["id"] == path_edges[-1])
                    evidence_groups.append((edge.get("evidence") or [], "edge", edge["id"], edge))
                for evidence, record_type, record_id, edge in evidence_groups:
                    for index, item in enumerate(evidence):
                        quote = str(item.get("quote") or "").strip()
                        document_id = item.get("document_id")
                        page = item.get("pdf_page_index")
                        paper_id = (edge or {}).get("source_paper_id") or node.get("source_paper_id")
                        if not paper_id and edge:
                            paper_id = edge.get("source_paper_id")
                        if not paper_id:
                            paper_id = next(
                                (
                                    adjacent.get("source_paper_id")
                                    for adjacent in self.adjacency[node_id]
                                    if adjacent.get("source_paper_id")
                                ),
                                None,
                            )
                        if not all((quote, document_id, page is not None, paper_id)):
                            continue
                        candidate = {
                            "record_id": f"kg:{record_type}:{record_id}:{index}",
                            "paper_id": paper_id,
                            "document_id": document_id,
                            "document_type": item.get("document_type") or "unknown",
                            "page": page,
                            "quote": quote,
                            "source_record": {"type": record_type, "id": record_id},
                            "kg_node_ids": [*path_nodes, node_id],
                            "kg_edge_ids": path_edges,
                            "kg_path_ids": [*path_nodes, node_id],
                            "score": seed_score / (1 + depth),
                            "evidence_validation": item.get("evidence_validation") or "unknown",
                            "review_status": (edge or node).get("review_status") or "unknown",
                        }
                        key = (str(paper_id), str(document_id), int(page), quote)
                        current = candidates.get(key)
                        if current is None:
                            candidates[key] = candidate
                        else:
                            current["kg_node_ids"] = sorted(
                                set(current["kg_node_ids"])
                                | set(candidate["kg_node_ids"])
                            )
                            current["kg_edge_ids"] = sorted(
                                set(current["kg_edge_ids"])
                                | set(candidate["kg_edge_ids"])
                            )
                            if len(candidate["kg_path_ids"]) > len(current["kg_path_ids"]):
                                current["kg_path_ids"] = candidate["kg_path_ids"]
                            current["score"] = max(current["score"], candidate["score"])
                if depth >= max_hops:
                    continue
                for edge in sorted(self.adjacency[node_id], key=lambda item: item["id"]):
                    neighbor = edge["to_node_id"] if edge["from_node_id"] == node_id else edge["from_node_id"]
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, [*path_nodes, node_id], [*path_edges, edge["id"]], depth + 1))
        ranked = sorted(
            candidates.values(),
            key=lambda row: (-row["score"], row["record_id"]),
        )
        return ranked[:candidate_limit]
