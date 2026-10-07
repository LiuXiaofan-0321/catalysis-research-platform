#!/usr/bin/env python3
"""Knowledge-base tooling: normalization overlay build/verify, one retrieval, retrieval audit.

  knowledge.py normalization build  --snapshot S --corpus C --output O --config configs/normalization/...
  knowledge.py normalization verify --overlay O --snapshot S --corpus C
  knowledge.py retrieve       --config configs/retrieval/small-kg-hybrid-v1.json --rag-index I --snapshot S --overlay O --mode rag_agent --query "..."
  knowledge.py audit-retrieval --config ... --questions configs/retrieval/zeolite-retrieval-audit-v1.json --rag-index I --snapshot S --overlay O --output out.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'literature_pipeline' / 'src'))

from catalysis_research.knowledge.normalization import build_normalization_overlay, verify_normalization_overlay  # noqa: E402
from catalysis_research.knowledge.retrieval import (  # noqa: E402
    EXPERIMENT_KNOWLEDGE_MODES, KnowledgeModeRetriever, RetrievalBudget, run_knowledge_retrieval_audit,
)


def dump(value, output=None):
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + '\n', encoding='utf-8')
    print(text)


def service(args):
    config = json.loads(args.config.read_text(encoding='utf-8'))
    s = KnowledgeModeRetriever.from_directories(config_path=args.config, rag_index_directory=args.rag_index,
                                                kg_snapshot_directory=args.snapshot,
                                                normalization_overlay_directory=args.overlay)
    return s, RetrievalBudget(**config['budget'])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    norm = sub.add_parser('normalization').add_subparsers(dest='action', required=True)
    b = norm.add_parser('build')
    for k in ('snapshot', 'corpus', 'output', 'config'):
        b.add_argument('--' + k, type=Path, required=True)
    b.add_argument('--code-commit')
    v = norm.add_parser('verify')
    for k in ('overlay', 'snapshot', 'corpus'):
        v.add_argument('--' + k, type=Path, required=True)
    for name in ('retrieve', 'audit-retrieval'):
        p = sub.add_parser(name)
        for k in ('config', 'rag-index', 'snapshot', 'overlay'):
            p.add_argument('--' + k, type=Path, required=True)
        if name == 'retrieve':
            p.add_argument('--mode', choices=EXPERIMENT_KNOWLEDGE_MODES, required=True)
            p.add_argument('--query', required=True)
            p.add_argument('--output', type=Path)
        else:
            p.add_argument('--questions', type=Path, required=True)
            p.add_argument('--output', type=Path, required=True)
    args = ap.parse_args(argv)
    if args.cmd == 'normalization' and args.action == 'build':
        dump(build_normalization_overlay(snapshot_directory=args.snapshot, corpus_directory=args.corpus,
                                         output_directory=args.output, config_path=args.config,
                                         code_commit=args.code_commit))
        return 0
    if args.cmd == 'normalization':
        out = verify_normalization_overlay(overlay_directory=args.overlay, snapshot_directory=args.snapshot,
                                           corpus_directory=args.corpus)
        dump(out)
        return 0 if out['valid'] else 1
    s, budget = service(args)
    if args.cmd == 'retrieve':
        dump(s.retrieve(query=args.query, experiment_mode=args.mode, budget=budget), args.output)
        return 0
    out = run_knowledge_retrieval_audit(service=s, questions_path=args.questions, budget=budget)
    dump(out, args.output)
    return 0 if out['automatic_gate_passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
