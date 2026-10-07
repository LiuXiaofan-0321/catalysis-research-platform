from __future__ import annotations

import gzip
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

from ..kg_freeze import verify_snapshot
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
        excluded_paper_ids: Iterable[str] = (),
        include_graph_semantics: bool = False,
    ) -> list[dict[str, Any]]:
        if not 0 <= max_hops <= 2:
            raise EvidenceContractError("max_hops must be between 0 and 2")
        query_terms = _terms(query)
        excluded = frozenset(str(value) for value in excluded_paper_ids)
        seeds: list[tuple[float, str]] = []
        for node_id, node in self.nodes.items():
            if str(node.get("source_paper_id") or "") in excluded:
                continue
            overlap = query_terms & _terms(self._node_text(node))
            if overlap:
                score = sum(1.0 + len(term) ** 0.5 for term in overlap)
                seeds.append((score, node_id))
        seeds.sort(key=lambda item: (-item[0], item[1]))
        candidates: dict[tuple[str, str, int, str], dict[str, Any]] = {}
        edge_by_id = {edge['id']: edge for edge in self.edges} if include_graph_semantics else {}
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
                        # Shared nodes may aggregate evidence from several papers.
                        # Prefer the cited document's identity over an adjacent edge.
                        paper_id = getattr(self, 'document_paper_ids', {}).get(str(document_id))
                        paper_id = paper_id or (edge or {}).get("source_paper_id") or node.get("source_paper_id")
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
                        if str(paper_id or "") in excluded:
                            continue
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
                        if include_graph_semantics:
                            # Keep each connected traversal separate. Aggregated node/
                            # edge ID sets are provenance, not a reconstructed path.
                            path = {
                                "nodes": [
                                    {"id": value, "type": self.nodes[value].get("node_type", "unknown"),
                                     "label": self.nodes[value].get("label") or self.nodes[value].get("canonical_name") or value,
                                     "data": self.nodes[value].get("data") or {},
                                     "review_status": self.nodes[value].get("review_status", "unknown")}
                                    for value in [*path_nodes, node_id]
                                ],
                                "edges": [
                                    {"id": value,
                                     "source": edge_by_id[value]["from_node_id"],
                                     "target": edge_by_id[value]["to_node_id"],
                                     "relation": edge_by_id[value].get("edge_type") or "unspecified_relation",
                                     "source_paper_id": edge_by_id[value].get("source_paper_id"),
                                     "review_status": edge_by_id[value].get("review_status", "unknown"),
                                     "evidence": edge_by_id[value].get("evidence") or []}
                                    for value in path_edges
                                ],
                                "interpretation": "Extracted graph relations; traversal does not establish causality.",
                            }
                            candidate["kg_paths"] = [path]
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
                            if include_graph_semantics:
                                paths = current.setdefault("kg_paths", [])
                                if path not in paths:
                                    paths.append(path)
                                # Prefer informative connected paths, with deterministic
                                # tie breaking, and bound serialized graph size.
                                paths.sort(key=lambda p: (-len(p['edges']), tuple(n['id'] for n in p['nodes'])))
                                del paths[3:]
                if depth >= max_hops:
                    continue
                for edge in sorted(self.adjacency[node_id], key=lambda item: item["id"]):
                    if str(edge.get("source_paper_id") or "") in excluded:
                        continue
                    neighbor = edge["to_node_id"] if edge["from_node_id"] == node_id else edge["from_node_id"]
                    if str(self.nodes[neighbor].get("source_paper_id") or "") in excluded:
                        continue
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, [*path_nodes, node_id], [*path_edges, edge["id"]], depth + 1))
        ranked = sorted(
            candidates.values(),
            key=lambda row: (-row["score"], row["record_id"]),
        )
        return ranked[:candidate_limit]
