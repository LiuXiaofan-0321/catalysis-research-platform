#!/usr/bin/env python3
"""ZeoSyn V2: build the KG knowledge layer, prepare splits, generate, evaluate and summarize.

  build-kg        KG snapshot -> data/kg_zeolite_v1/ (synthesis records, OSDA links, caches, manifest)
  probe           Gate 1: share of training recipes whose OSDA has KG synthesis evidence from other papers
  rag-allowlist   RAG index -> data/kg_zeolite_v1/rag_synthesis_allowlist.txt.gz (synthesis-related chunks)
  prepare         --split dev|test -> RUN/prepared/ (matrices, kg feature tables, exclusions, tasks)
  generate        LLM trajectories (threads; resumable; RAG loaded once per process)
  evaluate        RandomForest (and optional HGB) scores; --split test needs the frozen protocol
  summarize       statistics, contrasts, mechanism and sensitivity analyses
  audit-retrieval relevance of RAG/KG evidence for the planned queries (GLM judge)
  direct-answer-audit  how often the KG's top framework equals the label (dev only before freezing)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'literature_pipeline' / 'src')]

from catalysis_research.benchmarks import zeosyn as z  # noqa: E402

KG_ARTIFACTS = ROOT / 'data' / 'kg_zeolite_v1'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha(path):
    return z.file_sha256(path)


def save(path, value):
    z.save_json(path, value)


# ---------------------------------------------------------------- build-kg

def cmd_build_kg(args):
    import pandas as pd
    from catalysis_research.knowledge import kg_synthesis as ks
    out = Path(args.out)
    kg_dir = Path(args.kg_dir)
    kg_manifest = read(kg_dir / 'manifest.json')
    from catalysis_research.knowledge.kg_features import PORE_CLASSES
    # The IZA framework list from the ZeoSyn repository's pore classification (independent of recipe labels).
    canon = ks.framework_canonicalizer(sorted(set().union(*(m for _, m in PORE_CLASSES))))
    t = time.time()
    records, reagents, papers, framework_names = ks.stream_synthesis_records(kg_dir, canonical_code=canon)
    print(f'{len(records)} synthesis records, {len(reagents)} reagent entities ({time.time() - t:.0f}s)', flush=True)
    aliases, smiles_keys = ks.zeosyn_osda_aliases(ROOT / 'data/zeosyn/ZEOSYN.xlsx')
    resolvers = [('opsin', ks.OpsinResolver(out / 'opsin_name_cache.json', jar=args.opsin_jar, java=args.java))]
    resolvers.append(('pubchem', ks.PubChemResolver(out / 'pubchem_name_cache.json', offline=args.pubchem != 'online')))
    links, how = ks.link_reagents(reagents, aliases, resolvers=resolvers)
    # Readable OSDA names: the ZeoSyn common name of each structure.
    df = pd.read_excel(ROOT / 'data/zeosyn/ZEOSYN.xlsx', usecols=['osda1', 'osda1 smiles']).dropna()
    display = {}
    for name, smi in df.itertuples(index=False):
        k = smiles_keys.get(smi)
        if k and k not in display:
            display[k] = str(name)
    ks.write_jsonl_gz(out / 'synthesis_records.jsonl.gz', records)
    save(out / 'osda_links.json', {g: list(v) for g, v in sorted(links.items())})
    save(out / 'reagent_names.json', {g: n for g, n in sorted(reagents.items())})
    save(out / 'framework_names.json', dict(sorted(framework_names.items())))
    save(out / 'osda_display.json', dict(sorted(display.items())))
    from catalysis_research.knowledge.kg_features import framework_vocabulary
    save(out / 'framework_vocabulary.json', framework_vocabulary(records))
    linked_exps = sum(any(m in links for m in r['reagents']) for r in records)
    files = ['synthesis_records.jsonl.gz', 'osda_links.json', 'reagent_names.json', 'framework_names.json',
             'osda_display.json', 'framework_vocabulary.json', 'opsin_name_cache.json', 'pubchem_name_cache.json']
    manifest = {
        'schema': ks.SCHEMA,
        'source_kg': {'snapshot_id': kg_manifest.get('snapshot_id'),
                      'snapshot_content_hash': kg_manifest.get('snapshot_content_hash'),
                      'node_count': kg_manifest.get('graph', {}).get('node_count'),
                      'edge_count': kg_manifest.get('graph', {}).get('edge_count')},
        'zeosyn_sha256': z.EXPECTED_SHA256,
        'counts': {'synthesis_records': len(records), 'papers': len({r['paper_id'] for r in records}),
                   'reagent_entities': len(reagents), 'linked_reagent_entities': len(links),
                   'records_with_linked_osda': linked_exps,
                   'distinct_linked_osdas': len({v[0] for v in links.values()}), 'link_methods': dict(how)},
        'tools': {'opsin': '2.8.0', 'pubchem_mode': args.pubchem, 'rdkit': _rdkit_version()},
        'files': {f: sha(out / f) for f in files if (out / f).exists()},
        'rules': {'synthesis_experiment': 'experiment type matches synthesis/hydrothermal/crystallization/... or '
                                          'objective starts with synthesis/preparation; >=1 sample entity with a framework code',
                  'osda_link': 'alias (ZeoSyn names, IUPAC, synonyms; curated abbreviations) or identical structure '
                               '(largest organic fragment, uncharged, stereo removed) via OPSIN or cached PubChem'},
    }
    save(out / 'manifest.json', manifest)
    print(json.dumps(manifest['counts'], indent=1))


def _rdkit_version():
    try:
        import rdkit
        return rdkit.__version__
    except ImportError:
        return None


def load_kg_artifacts(path=KG_ARTIFACTS):
    from catalysis_research.knowledge import kg_synthesis as ks
    path = Path(path)
    manifest = read(path / 'manifest.json')
    for f, h in manifest['files'].items():
        if sha(path / f) != h:
            raise SystemExit(f'{path / f} does not match its manifest hash')
    return {
        'manifest': manifest,
        'records': ks.read_jsonl_gz(path / 'synthesis_records.jsonl.gz'),
        'links': {g: tuple(v) for g, v in read(path / 'osda_links.json').items()},
        'reagent_names': read(path / 'reagent_names.json'),
        'framework_names': read(path / 'framework_names.json'),
        'osda_display': read(path / 'osda_display.json'),
        'vocab': read(path / 'framework_vocabulary.json'),
    }


def zeosyn_osda_keys(frame):
    """Canonical OSDA key of every recipe's OSDA1 (None when absent or unparsable)."""
    from catalysis_research.knowledge.kg_synthesis import canonical_osda
    table = z.load_rdkit_table(ROOT / 'data/zeosyn')  # noqa: F841  (ensures the frozen data is present)
    cache = {}
    keys = []
    for smi in frame['osda1 smiles']:
        if not isinstance(smi, str) or not smi.strip():
            keys.append(None)
            continue
        if smi not in cache:
            cache[smi] = canonical_osda(smi)
        keys.append(cache[smi])
    return keys


# ---------------------------------------------------------------- probe (gate 1)

def cmd_probe(args):
    import numpy as np
    from catalysis_research.knowledge import kg_features as kf
    kg = load_kg_artifacts(args.kg_artifacts)
    data = z.load(ROOT / 'data/zeosyn')
    frame = data.frame
    cfg = read(args.config)
    train, test, test_dois = z.doi_group_split(frame, test_fraction=cfg['split']['test_fraction'], seed=cfg['split']['seed'])
    keys = zeosyn_osda_keys(frame)
    dois = frame['doi'].map(z.normalize_doi).tolist()
    years = frame['year'].tolist()
    by_osda = kf.osda_experiments(kg['records'], kg['links'])
    feats = kf.recipe_features(osda_keys=keys, dois=dois, years=years, by_osda=by_osda, vocab=kg['vocab'],
                               excluded_dois=set(test_dois))
    has_osda = np.array([k is not None for k in keys])
    linked_osda = np.array([k in by_osda for k in keys])
    cov_train = kf.coverage(feats, train)
    report = {
        'gate': {'rule': 'share of TRAINING recipes whose OSDA1 has KG synthesis evidence from another paper '
                         '(test papers removed from the KG) >= 0.40', 'threshold': 0.40,
                 'training_coverage': cov_train, 'passed': bool(cov_train >= 0.40)},
        'training_rows': int(len(train)),
        'training_rows_with_osda': int(has_osda[train].sum()),
        'coverage_among_training_rows_with_osda': kf.coverage(feats, train[has_osda[train]]),
        'training_rows_whose_osda_is_linked_at_all': float(linked_osda[train].mean()),
        'distinct_training_osdas': len({keys[i] for i in train if keys[i]}),
        'distinct_training_osdas_with_kg_evidence': len({keys[i] for i in train if keys[i] and feats[i, 0] > 0}),
        'kg_manifest_counts': kg['manifest']['counts'],
        'note': 'Uses no labels. Test-row coverage is not reported before the protocol is frozen.',
    }
    save(args.output, report)
    print(json.dumps(report, indent=1))


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('build-kg')
    s.add_argument('--kg-dir', required=True)
    s.add_argument('--out', default=str(KG_ARTIFACTS))
    s.add_argument('--opsin-jar')
    s.add_argument('--java')
    s.add_argument('--pubchem', choices=('online', 'cache'), default='cache')
    s = sub.add_parser('probe')
    s.add_argument('--kg-artifacts', default=str(KG_ARTIFACTS))
    s.add_argument('--config', default=str(ROOT / 'configs/experiments/zeosyn-v2.json'))
    s.add_argument('--output', default=str(KG_ARTIFACTS / 'gate1_coverage_probe.json'))
    args = ap.parse_args(argv)
    globals()['cmd_' + args.cmd.replace('-', '_')](args)


if __name__ == '__main__':
    main()
