#!/usr/bin/env python3
"""ZeoSyn V2: build the KG knowledge layer, prepare splits, generate, evaluate and summarize.

  build-kg        KG snapshot -> data/kg_zeolite_v1/ (synthesis records, OSDA links, caches, manifest)
  probe           Gate 1: share of training recipes whose OSDA has KG synthesis evidence from other papers
  rag-allowlist   RAG index -> data/kg_zeolite_v1/rag_synthesis_allowlist.txt.gz (synthesis-related chunks)
  prepare         --split dev|test -> RUN/prepared/ (matrices, kg feature tables, exclusions, tasks)
  generate        LLM trajectories (threads; resumable; RAG loaded once per process)
  evaluate        RandomForest (and optional HGB) scores; --split test needs the frozen protocol
  summarize       statistics, contrasts, mechanism and sensitivity analyses
  prepare-rag     retrieval config for a prepared split (evaluation papers excluded, allowlist applied)
  audit-retrieval relevance of RAG/KG evidence for the planned queries (GLM judge)
  direct-answer-audit  how often the KG's top framework equals the label (dev only before freezing)
  status          progress of a run
  collect         copy a run into results/<name>/ with an artifact hash list
  freeze          record the pre-registration hash in the config (required before any test evaluation)

The full desktop procedure is in docs/experiments/ZEOSYN_V2_RUNBOOK.md.
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
    df = pd.read_excel(ROOT / 'data/zeosyn/ZEOSYN.xlsx', usecols=[f'osda{i}{s}' for i in (1, 2, 3) for s in ('', ' smiles')])
    display = {}
    for i in (1, 2, 3):
        for name, smi in df[[f'osda{i}', f'osda{i} smiles']].dropna().itertuples(index=False):
            k = smiles_keys.get(smi)
            if k and k not in display:
                display[k] = str(name)
    ks.write_jsonl_gz(out / 'synthesis_records.jsonl.gz', records)
    save(out / 'osda_links.json', {g: list(v) for g, v in sorted(links.items())})
    save(out / 'reagent_names.json', {g: n for g, n in sorted(reagents.items())})
    save(out / 'framework_names.json', dict(sorted(framework_names.items())))
    save(out / 'osda_display.json', dict(sorted(display.items())))
    # Every ZeoSyn OSDA SMILES -> identity key, so later stages need no RDKit.
    all_smiles = set()
    full = pd.read_excel(ROOT / 'data/zeosyn/ZEOSYN.xlsx', usecols=['osda1 smiles', 'osda2 smiles', 'osda3 smiles'])
    for c in full.columns:
        all_smiles |= {x for x in full[c].dropna() if isinstance(x, str) and x.strip()}
    save(out / 'zeosyn_osda_keys.json', {smi: ks.canonical_osda(smi) for smi in sorted(all_smiles)})
    from catalysis_research.knowledge.kg_features import framework_vocabulary
    save(out / 'framework_vocabulary.json', framework_vocabulary(records))
    linked_exps = sum(any(m in links for m in r['reagents']) for r in records)
    files = ['synthesis_records.jsonl.gz', 'osda_links.json', 'reagent_names.json', 'framework_names.json',
             'osda_display.json', 'framework_vocabulary.json', 'zeosyn_osda_keys.json', 'opsin_name_cache.json',
             'pubchem_name_cache.json']
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


def zeosyn_osda_keys(frame, artifacts=KG_ARTIFACTS):
    """Identity key of every recipe's OSDA1 from the frozen table (None when absent or unparsable)."""
    table = read(Path(artifacts) / 'zeosyn_osda_keys.json')
    keys = []
    for smi in frame['osda1 smiles']:
        if not isinstance(smi, str) or not smi.strip():
            keys.append(None)
        elif smi in table:
            keys.append(table[smi])
        else:
            raise SystemExit(f'OSDA SMILES missing from zeosyn_osda_keys.json: {smi}')
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
    keys = zeosyn_osda_keys(frame, args.kg_artifacts)
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


# ---------------------------------------------------------------- rag-allowlist (D1)

ALLOWLIST_NAME = 'rag_synthesis_allowlist.txt.gz'
_SKIP_SECTIONS = ('acknowledg', 'conflict of interest', 'references', 'data availability', 'author', 'keywords',
                  'cartesian coordinates', 'copyright', 'funding', 'abbreviations', 'competing interest')
_SYN_SECTION = ('synthes', 'experimental', 'preparation', 'materials and methods', 'zeolite synthesis')
_SYN_TERMS = ('synthes', 'hydrothermal', 'crystalliz', 'crystallis', 'autoclave', ' gel', 'molar composition',
              'structure-directing', 'structure directing', 'osda', ' sda', 'template', 'teflon', 'calcin',
              ' aging', ' aged', 'seed', 'mineraliz', 'fluoride', 'phase selectiv', 'competing phase', 'interzeolite')


_MARKUP = __import__('re').compile(r'<[^>]*>|imgs/\S+|\$[^$]*\$|\{\s*\}|text-align\s*:\s*\w+|word-wrap\s*:\s*[\w-]+')


def synthesis_score(section, text):
    """Distinct synthesis terms in the chunk (+1 for a synthesis/experimental section); -1 for non-content."""
    sec = (section or '').lower()
    if any(sec.startswith(s) or s in sec for s in _SKIP_SECTIONS) or sec.startswith('umb'):
        return -1
    if sum(ch.isalpha() for ch in _MARKUP.sub(' ', text or '')) < 200:  # mostly table/image markup
        return -1
    body = ' ' + (text or '').lower()
    hits = sum(t in body for t in _SYN_TERMS)
    return hits + (1 if any(s in sec for s in _SYN_SECTION) else 0)


def cmd_rag_allowlist(args):
    """A chunk is kept when it hits >= 2 distinct synthesis terms (a synthesis/experimental section counts as one)."""
    import gzip
    import io
    idx = Path(args.rag_index)
    keep, total, by_section = [], 0, {}
    with open(idx / 'chunks.jsonl', encoding='utf-8') as fh:
        for line in fh:
            r = json.loads(line)
            total += 1
            if synthesis_score(r.get('section'), r.get('text')) >= 2:
                keep.append(r['record_id'])
    keep.sort()
    out = Path(args.out) / ALLOWLIST_NAME
    with open(out, 'wb') as raw, gzip.GzipFile(filename='', fileobj=raw, mode='wb', compresslevel=9, mtime=0) as gz, \
            io.TextIOWrapper(gz, encoding='utf-8') as fh:
        fh.write('\n'.join(keep) + '\n')
    stats = {'index_id': read(idx / 'manifest.json')['index_id'],
             'index_hash': read(idx / 'manifest.json')['logical_content_hash'],
             'chunks': total, 'kept': len(keep), 'kept_fraction': len(keep) / max(1, total),
             'rule': 'keep a chunk with >= 2 distinct synthesis terms; a synthesis/experimental section counts as one; '
                     'acknowledgement/reference/author/coordinate sections and chunks with < 200 letters outside '
                     'markup are never kept',
             'terms': list(_SYN_TERMS), 'sha256': sha(out)}
    save(Path(args.out) / 'rag_synthesis_allowlist.json', stats)
    print(json.dumps(stats, indent=1))


# ---------------------------------------------------------------- prepare

def run_paths(run):
    run = Path(run)
    return run, run / 'prepared'


def cmd_prepare(args):
    import shutil
    import numpy as np
    import pandas as pd
    from catalysis_research.discovery import zeosyn_v2 as v2
    from catalysis_research.knowledge import kg_features as kf
    cfg = v2.load_config(args.config)
    run, p = run_paths(args.run_dir)
    if (p / 'data-manifest.json').exists() and not args.force:
        raise SystemExit(f'{p} already prepared; use a new run directory')
    p.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.config, p / 'config.json')
    sp = cfg['split']
    if args.reuse_matrices:
        ref = read(args.reuse_matrices_manifest)
        if sha(args.reuse_matrices) != ref['matrix_sha256'] or ref['split_seed'] != sp['seed'] \
                or ref['test_fraction'] != sp['test_fraction']:
            raise SystemExit('reused matrices do not match their manifest or the configured split')
        shutil.copyfile(args.reuse_matrices, p / 'matrices.npz')
        meta = {k: ref[k] for k in ('rows', 'train_rows', 'test_rows', 'test_dois', 'split_seed', 'test_fraction',
                                    'source_hashes', 'matrix_sha256')}
        meta['reused_from'] = str(args.reuse_matrices)
    else:
        meta = z.prepare_matrices(ROOT / 'data/zeosyn', p / 'matrices.npz', test_fraction=sp['test_fraction'],
                                  split_seed=sp['seed'])
    m = z.load_matrices(p / 'matrices.npz')
    # The native row order depends only on the OSDA SMILES keys, so the frame is rebuilt from the few
    # columns needed here (much less memory); the order is then checked against the frozen matrices.
    df = pd.read_excel(ROOT / 'data/zeosyn/ZEOSYN.xlsx',
                       usecols=['Unnamed: 0', 'Si', 'doi', 'year', 'osda1 smiles', 'osda2 smiles', 'osda3 smiles'])
    osda = pd.read_csv(ROOT / 'data/zeosyn/osda_descriptors.csv', usecols=['osda smiles'])
    frame = z.native_frame(df, osda)
    del df, osda
    dois = frame['doi'].map(z.normalize_doi).tolist()
    years = pd.to_numeric(frame['year'], errors='coerce').to_numpy(float)
    if [d or '' for d in dois] != list(m['doi']) or not np.array_equal(years, m['year'], equal_nan=True):
        raise SystemExit('recipe order differs from the prepared matrices')
    years = years.tolist()
    keys = zeosyn_osda_keys(frame, args.kg_artifacts)
    outer_train, outer_test = m['train'], m['test']
    test_dois = {d for d in meta['test_dois']}
    if args.split == 'test':
        train, ev, excluded = outer_train, outer_test, set(test_dois)
    else:
        pi, pv, dev_dois = z.doi_group_split(pd.DataFrame({'doi': [dois[i] for i in outer_train]}),
                                             test_fraction=sp['dev_fraction'], seed=sp['dev_seed'])
        train, ev = outer_train[pi], outer_train[pv]
        excluded = set(test_dois) | set(dev_dois)  # development never sees test papers either
    kg = load_kg_artifacts()
    by_osda = kf.osda_experiments(kg['records'], kg['links'])
    by_osda_shuffled = kf.osda_experiments_shuffled(kg['records'], kg['links'], seed=cfg['kg']['shuffle_seed'])
    common = dict(osda_keys=keys, dois=dois, years=years, vocab=kg['vocab'])
    zeosyn_dois = {d for d in dois if d}
    tables = {
        'kg': kf.recipe_features(by_osda=by_osda, excluded_dois=excluded, **common),
        'kg_shuffled': kf.recipe_features(by_osda=by_osda_shuffled, excluded_dois=excluded, **common),
        'temporal': kf.recipe_features(by_osda=by_osda, excluded_dois=excluded, temporal=True, **common),
        'external': kf.recipe_features(by_osda=by_osda, excluded_dois=excluded | zeosyn_dois, **common),
    }
    np.savez_compressed(p / 'kg_tables.npz', **{f'{t}__{f}': tables[t][:, i] for t in tables
                                                for i, f in enumerate(kf.FEATURE_NAMES)})
    np.savez_compressed(p / 'split.npz', train=train, eval=ev)
    save(p / 'osda_keys.json', keys)
    save(p / 'excluded_dois.json', sorted(excluded))
    save(p / 'tasks.json', {'tasks': v2.tasks(cfg)})
    manifest = {
        'split': args.split, 'rows': int(len(keys)), 'train_rows': int(len(train)), 'eval_rows': int(len(ev)),
        'excluded_dois': len(excluded), 'matrix': {k: meta[k] for k in ('matrix_sha256', 'split_seed', 'test_fraction', 'source_hashes')},
        'kg_artifacts_manifest_sha256': sha(KG_ARTIFACTS / 'manifest.json'),
        'kg_coverage': {t: {'train': kf.coverage(tables[t], train), 'eval': kf.coverage(tables[t], ev)} for t in tables},
        'files': {f: sha(p / f) for f in ('config.json', 'matrices.npz', 'kg_tables.npz', 'split.npz', 'osda_keys.json',
                                          'excluded_dois.json', 'tasks.json')},
        'note': 'Coverage uses no labels. Imputation is fitted on the outer training rows (features only).',
    }
    save(p / 'data-manifest.json', manifest)
    print(json.dumps({k: v for k, v in manifest.items() if k != 'files'}, indent=1))


def load_split(run, *, check=True):
    import numpy as np
    from catalysis_research.knowledge import kg_features as kf
    run, p = run_paths(run)
    man = read(p / 'data-manifest.json')
    if check:
        for f, h in man['files'].items():
            if sha(p / f) != h:
                raise SystemExit(f'{p / f} changed after prepare')
        if sha(KG_ARTIFACTS / 'manifest.json') != man['kg_artifacts_manifest_sha256']:
            raise SystemExit('the KG layer (data/kg_zeolite_v1) changed after this split was prepared; run prepare again')
    m = z.load_matrices(p / 'matrices.npz')
    s = np.load(p / 'split.npz')
    with np.load(p / 'kg_tables.npz') as t:
        raw = {k: t[k] for k in t.files}
    tables = {name: {f: raw[f'{name}__{f}'] for f in kf.FEATURE_NAMES} for name in ('kg', 'kg_shuffled', 'temporal', 'external')}
    return {'name': man['split'], 'train': s['train'], 'eval': s['eval'], 'y': m['y'], 'd0': m['d0'],
            'd0_names': list(z.D0), 'env': m['env'], 'doi': m['doi'], 'osda_keys': read(p / 'osda_keys.json'),
            'kg_tables': {'kg': tables['kg'], 'kg_shuffled': tables['kg_shuffled']},
            'kg_variants': {'temporal': tables['temporal'], 'external': tables['external']},
            'excluded_dois': set(read(p / 'excluded_dois.json')), 'manifest': man}


def cmd_prepare_rag(args):
    """Retrieval config for this split: evaluation papers excluded (fail-closed counts) plus the synthesis allowlist."""
    from catalysis_research.discovery import zeosyn_knowledge as zk
    run, p = run_paths(args.run_dir)
    cfg = read(p / 'config.json')
    excluded_dois = read(p / 'excluded_dois.json')
    base = read(ROOT / cfg['rag']['base_config'])
    matched = zk.match_index_papers(args.rag_index, excluded_dois)
    excluded = set(base['rag']['excluded_paper_ids']) | set(matched)
    counts = zk.exclusion_counts(args.rag_index, excluded)
    rc = zk.retrieval_config(base, matched_ids=matched, counts=counts, test_dois=excluded_dois,
                             matrix_sha256=read(p / 'data-manifest.json')['matrix']['matrix_sha256'])
    allow = ROOT / cfg['rag']['allowlist']
    rc['rag']['allowlist'] = str(allow)
    rc['rag']['allowlist_sha256'] = sha(allow)
    rc['budget'] = {k: cfg['rag'][k] for k in ('candidate_limit', 'item_limit', 'context_token_budget',
                                               'max_items_per_paper', 'tokenizer_id')}
    save(p / 'retrieval-config.json', rc)
    print(json.dumps({'excluded_papers_in_index': len(matched), **counts}, indent=1))


# ---------------------------------------------------------------- generate

def kg_engine(split, kg, *, shuffled, seed):
    from catalysis_research.knowledge import kg_features as kf
    from catalysis_research.knowledge.kg_facts import KgFactEngine
    override = kf.shuffled_links(kg['records'], kg['links'], seed=seed) if shuffled else None
    return KgFactEngine(records=kg['records'], links=kg['links'], reagent_names=kg['reagent_names'],
                        osda_display=kg['osda_display'], excluded_dois=split['excluded_dois'],
                        framework_names=kg['framework_names'], link_override=override)


def evidence_providers(modes, split, cfg, *, run=None, rag_index=None, snapshot=None, overlay=None):
    from catalysis_research.discovery import zeosyn_v2 as v2
    out = {}
    if any(m in v2.KG_MODES for m in modes):
        kg = load_kg_artifacts()
        real = kg_engine(split, kg, shuffled=False, seed=None)
        for m in modes:
            if m in ('kg', 'kg_flat'):
                out[m] = v2.KgEvidence(real, token_budget=cfg['evidence_token_budget'], flat=(m == 'kg_flat'))
            elif m == 'kg_shuffled':
                out[m] = v2.KgEvidence(kg_engine(split, kg, shuffled=True, seed=cfg['kg']['shuffle_seed']),
                                       token_budget=cfg['evidence_token_budget'])
    if 'rag' in modes:
        from catalysis_research.knowledge.retrieval import KnowledgeModeRetriever, RetrievalBudget
        if not (rag_index and overlay):
            raise SystemExit('rag needs --rag-index and --overlay')
        _, p = run_paths(run)
        if not (p / 'retrieval-config.json').exists():
            raise SystemExit('run prepare-rag first')
        retriever = KnowledgeModeRetriever.rag_only_from_directories(
            config_path=p / 'retrieval-config.json', rag_index_directory=Path(rag_index),
            normalization_overlay_directory=Path(overlay))
        b = read(p / 'retrieval-config.json')['budget']
        out['rag'] = v2.RagEvidence(retriever, budget=RetrievalBudget(**b), token_budget=cfg['evidence_token_budget'],
                                    lock=threading.Lock())
    if 'agent' in modes:
        out['agent'] = v2.NoEvidence()
    return out


def cmd_generate(args):
    from catalysis_research.discovery import zeosyn_v2 as v2
    from catalysis_research.llm.glm import GlmClient
    run, p = run_paths(args.run_dir)
    cfg = v2.load_config(p / 'config.json')
    split = load_split(run)
    modes = args.modes or cfg['modes']
    reps = parse_range(args.replicates) if args.replicates else range(1, cfg['replicates_per_mode'] + 1)
    todo = [(m, r) for m in modes for r in reps if not (run / 'generation' / f'{m}-replicate-{r}.json').exists()]
    print(f'{len(todo)} trajectories to generate on the {split["name"]} split: {modes}', flush=True)
    if not todo:
        return
    providers = evidence_providers({m for m, _ in todo}, split, cfg, run=run, rag_index=args.rag_index,
                                   snapshot=args.snapshot, overlay=args.overlay)
    client = GlmClient(timeout_seconds=cfg['api_timeout_seconds'])
    (run / 'generation').mkdir(parents=True, exist_ok=True)
    (run / 'logs').mkdir(parents=True, exist_ok=True)
    hashes = {f: sha(p / f) for f in ('config.json', 'data-manifest.json')}

    def one(mode, rep):
        name = f'{mode}-replicate-{rep}'
        logf = open(run / 'logs' / f'{name}.log', 'a', encoding='utf-8')

        def log(msg):
            line = f'{time.strftime("%H:%M:%S")} {msg}'
            logf.write(line + '\n')
            logf.flush()
            print(line, flush=True)
        t = time.time()
        try:
            g = v2.run_trajectory(config=cfg, mode=mode, replicate=rep, split=split, evidence_provider=providers[mode],
                                  client=client, log=log)
        finally:
            logf.close()
        g.update({'prepared_sha256': hashes, 'seconds': time.time() - t, 'model': cfg['model'],
                  'reasoning_effort': cfg['reasoning_effort']})
        save(run / 'generation' / f'{name}.json', g)
        return name, g['appended']

    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(one, m, r): (m, r) for m, r in todo}
        for f in as_completed(futs):
            try:
                name, n = f.result()
                print(f'done {name}: {n} appended', flush=True)
            except Exception as exc:  # noqa: BLE001 - reported, file not written, rerun resumes
                failures.append((futs[f], repr(exc)))
                print(f'FAILED {futs[f]}: {exc!r}', flush=True)
    if failures:
        raise SystemExit(f'{len(failures)} trajectories failed (API/network); rerun the same command to resume')


def parse_range(text):
    out = []
    for part in text.split(','):
        a, _, b = part.partition('-')
        out += list(range(int(a), int(b or a) + 1))
    return out


# ---------------------------------------------------------------- evaluate / summarize

def protocol_frozen(cfg):
    pr = cfg['protocol']
    doc = ROOT / pr['prereg']
    return bool(pr.get('frozen')) and doc.exists() and pr.get('prereg_sha256') == sha(doc)


def cmd_evaluate(args):
    import numpy as np
    from catalysis_research.discovery import zeosyn_v2 as v2
    from catalysis_research.discovery import zeosyn_v2_eval as ev
    run, p = run_paths(args.run_dir)
    cfg = v2.load_config(p / 'config.json')
    split = load_split(run)
    if split['name'] == 'test' and not (args.confirmatory and protocol_frozen(cfg)):
        raise SystemExit('test evaluation requires --confirmatory and a frozen protocol (configs: protocol.frozen, prereg_sha256)')
    e = cfg['evaluation']
    kw = dict(n_estimators=e['n_estimators'], n_jobs=args.n_jobs)
    out_dir = run / 'evaluation'
    out_dir.mkdir(parents=True, exist_ok=True)
    base_path = out_dir / 'd0.json'
    if base_path.exists():
        base = read(base_path)
        base_preds = np.load(out_dir / 'd0-predictions.npy', allow_pickle=True)
    else:
        rows, base_preds = ev.score(split, split['d0'], seeds=e['fit_seeds'], **kw)
        base = {'per_seed': rows, 'mean': {k: float(np.mean([r[k] for r in rows])) for k in ev.METRICS}}
        save(base_path, base)
        np.save(out_dir / 'd0-predictions.npy', base_preds)
    lib_path = out_dir / 'library-only.json'
    if not lib_path.exists():
        # E5 diagnostic: D0 + every kg_* column, no LLM; by stratum it shows where the KG channel carries information.
        lib = {}
        for table in ('kg', 'kg_shuffled'):
            rows, preds = ev.score(split, ev.library_matrix(split, table), seeds=e['fit_seeds'], **kw)
            lib[table] = {'per_seed': rows, 'delta': ev.paired(rows, base['per_seed']),
                          'strata': ev.stratified_deltas(split, preds, base_preds)}
        save(lib_path, lib)
    gens = sorted((run / 'generation').glob('*.json'))
    for gpath in gens:
        name = gpath.stem
        target = out_dir / f'{name}.json'
        if target.exists():
            continue
        g = read(gpath)
        t = time.time()
        if g['appended'] == 0:
            rows, preds = base['per_seed'], base_preds
        else:
            rows, preds = ev.score(split, v2.final_matrix(split, g), seeds=e['fit_seeds'], **kw)
        res = {'mode': g['mode'], 'replicate': g['replicate'], 'split': split['name'], 'appended': g['appended'],
               'final_formulas': g['final_formulas'], 'per_seed': rows, 'delta': ev.paired(rows, base['per_seed']),
               'strata': ev.stratified_deltas(split, preds, base_preds), 'generation_sha256': sha(gpath)}
        if g['mode'] == 'kg' and g['appended']:
            res['sensitivity'] = {}
            for variant in ('temporal', 'external'):
                vs = ev.variant_split(split, variant)
                vrows, _ = ev.score(vs, v2.final_matrix(vs, g), seeds=e['fit_seeds'], **kw)
                res['sensitivity'][variant] = ev.paired(vrows, base['per_seed'])['mean']
        res['seconds'] = time.time() - t
        save(target, res)
        print(f'{name}: {res["delta"]["mean"]}', flush=True)
    if args.hgb:
        cmd_evaluate_hgb(run, split, cfg, args)


def cmd_evaluate_hgb(run, split, cfg, args):
    """Sensitivity: the same frozen descriptor sets scored with HistGradientBoosting (one seed)."""
    from catalysis_research.discovery import zeosyn_v2 as v2
    from catalysis_research.discovery import zeosyn_v2_eval as ev
    h = cfg['evaluation']['sensitivity_predictor']
    target = run / 'evaluation' / 'hgb.json'
    res = read(target) if target.exists() else {}
    kw = dict(seeds=h['seeds'], n_estimators=None, n_jobs=args.n_jobs, predictor='hgb', hgb=h)
    if 'd0' not in res:
        res['d0'] = ev.score(split, split['d0'], **kw)[0]
        save(target, res)
    for gpath in sorted((run / 'generation').glob('*.json')):
        if gpath.stem in res:
            continue
        g = read(gpath)
        rows = res['d0'] if g['appended'] == 0 else ev.score(split, v2.final_matrix(split, g), **kw)[0]
        res[gpath.stem] = {'mode': g['mode'], 'per_seed': rows, 'delta': ev.paired(rows, res['d0'])['mean']}
        save(target, res)
        print(f'hgb {gpath.stem}: {res[gpath.stem]["delta"]}', flush=True)


def cmd_summarize(args):
    import numpy as np
    from catalysis_research.discovery import zeosyn_v2 as v2
    from catalysis_research.discovery import zeosyn_v2_eval as ev
    run, p = run_paths(args.run_dir)
    cfg = v2.load_config(p / 'config.json')
    gens = [read(x) for x in sorted((run / 'generation').glob('*.json'))]
    evs = [read(x) for x in sorted((run / 'evaluation').glob('*-replicate-*.json'))]
    d0 = read(run / 'evaluation' / 'd0.json')['mean']
    lib = {t: {**v['delta']['mean'], 'strata': v.get('strata')} for t, v in read(run / 'evaluation' / 'library-only.json').items()}
    s = ev.summarize(cfg, gens, evs, d0=d0, library=lib)
    s['split'] = read(p / 'data-manifest.json')['split']
    kg_sens = [e['sensitivity'] for e in evs if e['mode'] == 'kg' and e.get('sensitivity')]
    if kg_sens:
        s['sensitivity_kg'] = {v: float(np.mean([x[v][cfg['evaluation']['primary_metric']] for x in kg_sens]))
                               for v in ('temporal', 'external')}
    hgb = run / 'evaluation' / 'hgb.json'
    if hgb.exists():
        h = read(hgb)
        s['sensitivity_hgb'] = {m: float(np.mean([v['delta'][cfg['evaluation']['primary_metric']] for k, v in h.items()
                                                  if k != 'd0' and v['mode'] == m])) for m in {v['mode'] for k, v in h.items() if k != 'd0'}}
    usage = {'prompt_tokens': 0, 'completion_tokens': 0}
    for g in gens:
        for sl in g['slots']:
            for a in sl['attempts']:
                for k in usage:
                    usage[k] += (a.get('usage') or {}).get(k, 0) or 0
    s['usage'] = usage
    s['missing'] = sorted({f"{t['mode']}-replicate-{t['replicate']}" for t in read(p / 'tasks.json')['tasks']}
                          - {f"{e['mode']}-replicate-{e['replicate']}" for e in evs})
    save(run / 'summary.json', s)
    print(json.dumps({k: s[k] for k in ('split', 'd0', 'library_only', 'contrasts', 'hypotheses', 'missing')}, indent=1))


# ---------------------------------------------------------------- audits

AUDIT_SYSTEM = 'You judge retrieval quality for zeolite synthesis research. Return one JSON object only.'


def cmd_audit_retrieval(args):
    """D3: share of returned items a GLM judge rates relevant to the query (same queries for every source)."""
    import random
    from catalysis_research.discovery import zeosyn_v2 as v2
    from catalysis_research.llm.glm import GlmClient
    run, p = run_paths(args.run_dir)
    cfg = v2.load_config(p / 'config.json')
    split = load_split(run)
    queries = read(args.queries)['queries'] if args.queries else []
    if not queries:
        for gpath in sorted((run / 'generation').glob('*.json')):
            for sl in read(gpath)['slots']:
                queries += (sl.get('plan') or {}).get('queries', [])
        queries = sorted(set(queries))
        random.Random(0).shuffle(queries)
        queries = queries[:args.max_queries]
    providers = evidence_providers(args.modes, split, cfg, run=run, rag_index=args.rag_index,
                                   snapshot=args.snapshot, overlay=args.overlay)
    client = GlmClient(timeout_seconds=600)
    out = {'queries': queries, 'modes': {}}
    for mode in args.modes:
        judged, empty = [], 0
        for q in queries:
            evd = providers[mode]([q])
            empty += not evd['items']
            for it in evd['items']:
                text = evd['context'].split(f'[{it["id"]}] ', 1)[-1].split('\n[')[0][:1500]
                r = client.chat_json(model=cfg['model'], system=AUDIT_SYSTEM, max_tokens=2048, thinking='enabled', reasoning_effort='low',
                                     user=f'Query: {q}\n\nRetrieved item:\n{text}\n\nIs this item relevant evidence for '
                                          'the query about zeolite synthesis (it states facts that bear on the query)? '
                                          'Return {"relevant": true or false}.')
                judged.append({'query': q, 'key': it['key'], 'relevant': bool(r.structured.get('relevant'))})
        rate = sum(j['relevant'] for j in judged) / max(1, len(judged))
        out['modes'][mode] = {'items': len(judged), 'relevant_rate': rate, 'target': 0.70, 'passed': rate >= 0.70,
                              'empty_queries': empty, 'judgements': judged}
        print(mode, json.dumps({k: v for k, v in out['modes'][mode].items() if k != 'judgements'}), flush=True)
    save(Path(args.output), out)


def cmd_direct_answer_audit(args):
    from catalysis_research.discovery import zeosyn_v2 as v2
    from catalysis_research.knowledge import kg_features as kf
    run, p = run_paths(args.run_dir)
    cfg = v2.load_config(p / 'config.json')
    split = load_split(run)
    if split['name'] == 'test' and not protocol_frozen(cfg):
        raise SystemExit('the test-side audit uses test labels; run it after the protocol is frozen')
    import numpy as np
    feats = np.column_stack([split['kg_tables']['kg'][f] for f in kf.FEATURE_NAMES])
    res = kf.direct_answer_audit(feats, split['y'], split['eval'], load_kg_artifacts()['vocab'])
    res['split'] = split['name']
    save(run / 'direct-answer-audit.json', res)
    print(json.dumps(res, indent=1))


def cmd_status(args):
    run, p = run_paths(args.run_dir)
    tasks = read(p / 'tasks.json')['tasks'] if (p / 'tasks.json').exists() else []
    names = [f"{t['mode']}-replicate-{t['replicate']}" for t in tasks]
    gen = {x.stem for x in (run / 'generation').glob('*.json')}
    evd = {x.stem for x in (run / 'evaluation').glob('*-replicate-*.json')}
    print(json.dumps({'prepared': (p / 'data-manifest.json').exists(), 'retrieval_config': (p / 'retrieval-config.json').exists(),
                      'tasks': len(tasks), 'generated': len(gen & set(names)), 'evaluated': len(evd & set(names)),
                      'summary': (run / 'summary.json').exists(),
                      'missing_generation': [n for n in names if n not in gen]}, indent=1))


def cmd_collect(args):
    """Copy a run into results/<name>/ (prepared inputs, generations, evaluations, audits, summary, logs)."""
    import shutil
    run, p = run_paths(args.run_dir)
    dest = ROOT / 'results' / args.name
    if dest.exists():
        raise SystemExit(f'{dest} exists; choose another --name')
    if not (run / 'summary.json').exists() and not args.partial:
        raise SystemExit('summary.json missing; use --partial to collect anyway')
    shutil.copytree(p, dest / 'prepared')
    for sub in ('generation', 'evaluation', 'logs'):
        if (run / sub).exists():
            shutil.copytree(run / sub, dest / sub)
    for f in run.glob('*.json'):
        shutil.copy2(f, dest / f.name)
    key = os.environ.get('ZHIPU_API_KEY', '')
    for f in dest.rglob('*'):
        if f.is_file() and f.suffix in ('.json', '.log', '.txt', '.md'):
            text = f.read_text(encoding='utf-8', errors='ignore')
            if (key and key in text) or 'Bearer ' in text:
                shutil.rmtree(dest)
                raise SystemExit(f'credential-like text in {f.name}; nothing collected')
    (dest / '.gitattributes').write_text('* binary\n', encoding='utf-8')  # keep exact bytes so hashes survive cloning
    save(dest / 'ARTIFACTS.json', {str(f.relative_to(dest)): sha(f) for f in sorted(dest.rglob('*'))
                                   if f.is_file() and f.name != 'ARTIFACTS.json'})
    print(f'collected {dest}; commit it with git add results/{args.name}')


def cmd_freeze(args):
    """Record the pre-registration hash in the config and mark the protocol frozen (commit the result)."""
    cfg_path = Path(args.config)
    cfg = read(cfg_path)
    doc = ROOT / cfg['protocol']['prereg']
    if not doc.exists():
        raise SystemExit(f'{doc} is missing')
    if 'TO BE CONFIRMED' in doc.read_text(encoding='utf-8'):
        raise SystemExit('the pre-registration still contains items marked TO BE CONFIRMED')
    cfg['protocol']['prereg_sha256'] = sha(doc)
    cfg['protocol']['frozen'] = True
    cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'frozen: {doc.name} sha256 {cfg["protocol"]["prereg_sha256"]}; commit {cfg_path} and the document now')


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
    s = sub.add_parser('rag-allowlist')
    s.add_argument('--rag-index', required=True)
    s.add_argument('--out', default=str(KG_ARTIFACTS))
    s = sub.add_parser('prepare')
    s.add_argument('--split', choices=('dev', 'test'), required=True)
    s.add_argument('--run-dir', required=True)
    s.add_argument('--config', default=str(ROOT / 'configs/experiments/zeosyn-v2.json'))
    s.add_argument('--reuse-matrices', help='a matrices.npz from an earlier run with the same split (verified by hash)')
    s.add_argument('--reuse-matrices-manifest', help='the data-manifest.json that records that matrices file')
    s.add_argument('--kg-artifacts', default=str(KG_ARTIFACTS))
    s.add_argument('--force', action='store_true')
    s = sub.add_parser('prepare-rag')
    s.add_argument('--run-dir', required=True)
    s.add_argument('--rag-index', required=True)
    for name in ('generate', 'audit-retrieval'):
        s = sub.add_parser(name)
        s.add_argument('--run-dir', required=True)
        s.add_argument('--rag-index')
        s.add_argument('--snapshot')
        s.add_argument('--overlay')
        if name == 'generate':
            s.add_argument('--modes', nargs='+')
            s.add_argument('--replicates', help='e.g. 1-10 or 1,3,5')
            s.add_argument('--workers', type=int, default=5)
        else:
            s.add_argument('--modes', nargs='+', default=['rag', 'kg'])
            s.add_argument('--queries', help='JSON file {"queries": [...]}; default: queries written in this run')
            s.add_argument('--max-queries', type=int, default=30)
            s.add_argument('--output', required=True)
    s = sub.add_parser('evaluate')
    s.add_argument('--run-dir', required=True)
    s.add_argument('--n-jobs', type=int, default=os.cpu_count() or 1)
    s.add_argument('--hgb', action='store_true', help='also run the HGB sensitivity analysis')
    s.add_argument('--confirmatory', action='store_true')
    for name in ('summarize', 'direct-answer-audit', 'status'):
        s = sub.add_parser(name)
        s.add_argument('--run-dir', required=True)
    s = sub.add_parser('collect')
    s.add_argument('--run-dir', required=True)
    s.add_argument('--name', required=True, help='folder name under results/, e.g. zeosyn_v2_dev_1')
    s.add_argument('--partial', action='store_true')
    s = sub.add_parser('freeze')
    s.add_argument('--config', default=str(ROOT / 'configs/experiments/zeosyn-v2.json'))
    args = ap.parse_args(argv)
    globals()['cmd_' + args.cmd.replace('-', '_')](args)
    try:  # not available on Windows
        import resource
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(f'[{args.cmd}] peak memory {peak / (2**30 if sys.platform == "darwin" else 2**20):.2f} GiB', flush=True)
    except ImportError:
        pass


if __name__ == '__main__':
    main()
