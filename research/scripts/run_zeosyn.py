#!/usr/bin/env python3
"""ZeoSyn label-free direct-addition experiment: one entry point for every stage.

Stages (run directory layout):
  prepare    -> prepared/{config.json, matrices.npz, data-manifest.json, tasks.json}
  knowledge  -> prepared/{retrieval-config.json, knowledge.json}   (needs RAG index, Small KG, overlay)
  baseline   -> d0.json                                           (D0 RandomForest, all fit seeds)
  probe      -> api-probe.json                                    (one tiny GLM call)
  generate   -> generation/<mode>-replicate-<r>.json              (GLM; no labels)
  evaluate   -> evaluation/<mode>-replicate-<r>.json              (RandomForest; no GLM)
  summarize  -> summary.json
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research' / 'src'))

from catalysis_research.datasets import zeosyn as z  # noqa: E402
from catalysis_research.experiments import zeosyn_direct as zd  # noqa: E402


def sha(path):
    return z.file_sha256(path)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def prepared(run):
    return Path(run) / 'prepared'


def load_run(run):
    p = prepared(run)
    config = zd.load_config(p / 'config.json')
    manifest = read(p / 'data-manifest.json')
    if sha(p / 'matrices.npz') != manifest['matrix_sha256']:
        raise SystemExit('matrices.npz hash mismatch')
    return config, manifest, z.load_matrices(p / 'matrices.npz')


def task_for(run, args):
    if args.task_index is not None:
        t = read(prepared(run) / 'tasks.json')['tasks'][args.task_index]
        if t['index'] != args.task_index:
            raise SystemExit('tasks.json index mismatch')
        return t['mode'], t['replicate']
    if not args.mode or not args.replicate:
        raise SystemExit('Give --task-index or --mode and --replicate')
    return args.mode, args.replicate


def cmd_reproduce(args):
    r = z.reproduce_native(args.data_root, n_jobs=args.n_jobs)
    z.save_json(args.output, r)
    print(json.dumps(r['reproduced']))
    if abs(r['reproduced']['accuracy'] - r['published']['accuracy']) > 0.01:
        raise SystemExit('Native reproduction differs from the published accuracy by more than 0.01')


def cmd_prepare(args):
    run = Path(args.run_dir)
    p = prepared(run)
    if (p / 'data-manifest.json').exists() and not args.force:
        raise SystemExit(f'{p} already prepared; use a new run directory')
    config = zd.load_config(args.config)
    p.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.config, p / 'config.json')
    meta = z.prepare_matrices(args.data_root, p / 'matrices.npz', test_fraction=config['split']['test_fraction'],
                              split_seed=config['split']['seed'])
    meta['config_sha256'] = sha(p / 'config.json')
    z.save_json(p / 'data-manifest.json', meta)
    z.save_json(p / 'tasks.json', {'tasks': zd.tasks(config)})
    print(json.dumps({k: v for k, v in meta.items() if k not in ('test_dois', 'd0_columns', 'raw_inputs')}))


def cmd_knowledge(args):
    from catalysis_research.experiments import zeosyn_knowledge as zk
    from catalysis_research.retrieval import KnowledgeModeRetriever, RetrievalBudget
    run = Path(args.run_dir)
    config, manifest, _ = load_run(run)
    base = read(args.base_retrieval_config)
    matched = zk.match_index_papers(args.rag_index, manifest['test_dois'])
    excluded = set(base['rag']['excluded_paper_ids']) | set(matched)
    counts = zk.exclusion_counts(args.rag_index, excluded)
    rc = zk.retrieval_config(base, matched_ids=matched, counts=counts, test_dois=manifest['test_dois'],
                             matrix_sha256=manifest['matrix_sha256'])
    rc_path = prepared(run) / 'retrieval-config.json'
    z.save_json(rc_path, rc)
    print(json.dumps({'held_out_dois': len(manifest['test_dois']), 'held_out_in_index': len(matched), **counts}))
    retriever = KnowledgeModeRetriever.from_directories(
        config_path=rc_path, rag_index_directory=Path(args.rag_index),
        kg_snapshot_directory=Path(args.snapshot), normalization_overlay_directory=Path(args.overlay))
    r = config['retrieval']
    budget = RetrievalBudget(candidate_limit=r['candidate_limit'], item_limit=r['item_limit'],
                             context_token_budget=r['context_token_budget'],
                             max_items_per_paper=r['max_items_per_paper'], tokenizer_id=r['tokenizer_id'])
    bundles = zk.freeze_bundles(retriever, queries=config['queries'], budget=budget,
                                held_out_dois=manifest['test_dois'])
    knowledge = {'profile': zd.PROFILE, 'queries': config['queries'], 'bundles': bundles,
                 'retrieval_config_sha256': sha(rc_path), 'sources': retriever.source_identities,
                 'matrix_sha256': manifest['matrix_sha256']}
    z.save_json(prepared(run) / 'knowledge.json', knowledge)
    for mode, bs in bundles.items():
        print(mode, [b['selected_count'] for b in bs], [b['selected_token_count'] for b in bs])
    for mode, bs in bundles.items():
        if any(b['selected_count'] == 0 for b in bs):
            raise SystemExit(f'{mode} retrieved no evidence for at least one query')


def load_knowledge(run, config, mode):
    path = prepared(run) / 'knowledge.json'
    if not path.exists():
        if mode == 'agent':
            return {'bundles': {}}, None
        raise SystemExit('prepared/knowledge.json is required for ' + mode)
    k = read(path)
    for mode in ('rag_agent', 'small_kg_rag_agent'):
        if len(k['bundles'].get(mode, [])) != config['rounds']:
            raise SystemExit(f'knowledge.json lacks {mode} bundles for every round')
    return k, sha(path)


def cmd_baseline(args):
    run = Path(args.run_dir)
    config, manifest, m = load_run(run)
    ev = config['evaluation']
    t = time.time()
    rows = zd.evaluate_matrix(m, m['d0'], seeds=ev['fit_seeds'], n_jobs=args.n_jobs, n_estimators=ev['n_estimators'])
    out = {'profile': zd.PROFILE, 'matrix_sha256': manifest['matrix_sha256'], 'per_seed': rows,
           'mean': {k: sum(r[k] for r in rows) / len(rows) for k in zd.METRICS}, 'seconds': time.time() - t}
    z.save_json(run / 'd0.json', out)
    print(json.dumps(out['mean']))


def client_for(config):
    from catalysis_research.models.glm import GlmClient
    return GlmClient(timeout_seconds=config['api_timeout_seconds'])


def cmd_probe(args):
    run = Path(args.run_dir)
    config = zd.load_config(prepared(run) / 'config.json')
    t = time.time()
    r = client_for(config).chat_json(model=config['model'], system='Return JSON only.',
                                     user='Return a JSON object with ok set to true.', max_tokens=2048,
                                     thinking=config['thinking'], reasoning_effort=config['reasoning_effort'])
    out = {'model': r.model, 'ok': r.structured.get('ok'), 'usage': r.usage, 'seconds': time.time() - t,
           'base_url_is_proxy': bool(os.environ.get('ZHIPU_PROXY_BASE_URL'))}
    z.save_json(run / 'api-probe.json', out)
    print(json.dumps(out))
    if out['ok'] is not True:
        raise SystemExit('GLM probe did not return ok=true')


def cmd_generate(args):
    run = Path(args.run_dir)
    config, manifest, m = load_run(run)
    mode, rep = task_for(run, args)
    out = run / 'generation' / f'{mode}-replicate-{rep}.json'
    if out.exists():
        print(f'{out} exists; not regenerating')
        return
    knowledge, khash = load_knowledge(run, config, mode)
    t = time.time()
    g = zd.run_trajectory(config=config, mode=mode, replicate=rep, matrices=m, knowledge=knowledge,
                          client=client_for(config))
    g.update({'config_sha256': sha(prepared(run) / 'config.json'), 'matrix_sha256': manifest['matrix_sha256'],
              'knowledge_sha256': khash, 'seconds': time.time() - t, 'model': config['model'],
              'reasoning_effort': config['reasoning_effort']})
    z.save_json(out, g)
    print(json.dumps({'mode': mode, 'replicate': rep, 'appended': g['appended'],
                      'formulas': [f['formula'] for f in g['final_formulas']]}, ensure_ascii=False))


def cmd_evaluate(args):
    run = Path(args.run_dir)
    config, manifest, m = load_run(run)
    mode, rep = task_for(run, args)
    name = f'{mode}-replicate-{rep}'
    if (run / 'evaluation' / f'{name}.json').exists():
        print(f'evaluation/{name}.json exists; not re-evaluating')
        return
    g = read(run / 'generation' / f'{name}.json')
    d0 = read(run / 'd0.json')
    if g['matrix_sha256'] != manifest['matrix_sha256'] or d0['matrix_sha256'] != manifest['matrix_sha256']:
        raise SystemExit('Generation, D0 and matrices must share one prepared split')
    ev = config['evaluation']
    t = time.time()
    if g['appended'] == 0:
        final = d0['per_seed']
        reused = True
    else:
        x = zd.final_matrix(m, g)
        final = zd.evaluate_matrix(m, x, seeds=ev['fit_seeds'], n_jobs=args.n_jobs, n_estimators=ev['n_estimators'])
        reused = False
    out = {'profile': zd.PROFILE, 'mode': mode, 'replicate': rep, 'appended': g['appended'],
           'final_formulas': g['final_formulas'], 'reused_d0_for_zero_append': reused,
           'per_seed': final, 'delta': zd.paired_delta(final, d0['per_seed']),
           'generation_sha256': sha(run / 'generation' / f'{name}.json'), 'seconds': time.time() - t}
    z.save_json(run / 'evaluation' / f'{name}.json', out)
    print(json.dumps({'mode': mode, 'replicate': rep, **out['delta']['mean']}))


def cmd_summarize(args):
    run = Path(args.run_dir)
    config = zd.load_config(prepared(run) / 'config.json')
    gens = [read(p) for p in sorted((run / 'generation').glob('*.json'))]
    evs = [read(p) for p in sorted((run / 'evaluation').glob('*.json'))]
    s = zd.summarize(config, gens, evs)
    s['d0'] = read(run / 'd0.json')['mean']
    s['missing'] = sorted({f"{t['mode']}-replicate-{t['replicate']}" for t in read(prepared(run) / 'tasks.json')['tasks']}
                          - {f"{e['mode']}-replicate-{e['replicate']}" for e in evs})
    z.save_json(run / 'summary.json', s)
    print(json.dumps(s, indent=1))


def cmd_status(args):
    run = Path(args.run_dir)
    tasks = read(prepared(run) / 'tasks.json')['tasks'] if (prepared(run) / 'tasks.json').exists() else []
    names = [f"{t['mode']}-replicate-{t['replicate']}" for t in tasks]
    gen = {p.stem for p in (run / 'generation').glob('*.json')}
    ev = {p.stem for p in (run / 'evaluation').glob('*.json')}
    out = {'prepared': (prepared(run) / 'data-manifest.json').exists(),
           'knowledge': (prepared(run) / 'knowledge.json').exists(), 'd0': (run / 'd0.json').exists(),
           'probe': (run / 'api-probe.json').exists(), 'generated': len(gen), 'evaluated': len(ev),
           'tasks': len(tasks), 'summary': (run / 'summary.json').exists(),
           'missing_generation_task_indexes': [i for i, n in enumerate(names) if n not in gen],
           'missing_evaluation_task_indexes': [i for i, n in enumerate(names) if n not in ev]}
    print(json.dumps(out))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('reproduce'); s.add_argument('--data-root', required=True); s.add_argument('--output', required=True)
    s.add_argument('--n-jobs', type=int, default=1)
    s = sub.add_parser('prepare'); s.add_argument('--data-root', required=True); s.add_argument('--run-dir', required=True)
    s.add_argument('--config', required=True); s.add_argument('--force', action='store_true')
    s = sub.add_parser('knowledge'); s.add_argument('--run-dir', required=True)
    s.add_argument('--base-retrieval-config', required=True); s.add_argument('--rag-index', required=True)
    s.add_argument('--snapshot', required=True); s.add_argument('--overlay', required=True)
    s = sub.add_parser('baseline'); s.add_argument('--run-dir', required=True); s.add_argument('--n-jobs', type=int, default=1)
    s = sub.add_parser('probe'); s.add_argument('--run-dir', required=True)
    for name in ('generate', 'evaluate'):
        s = sub.add_parser(name); s.add_argument('--run-dir', required=True)
        s.add_argument('--task-index', type=int); s.add_argument('--mode', choices=zd.MODES); s.add_argument('--replicate', type=int)
        if name == 'evaluate':
            s.add_argument('--n-jobs', type=int, default=1)
    s = sub.add_parser('summarize'); s.add_argument('--run-dir', required=True)
    s = sub.add_parser('status'); s.add_argument('--run-dir', required=True)
    args = ap.parse_args(argv)
    globals()['cmd_' + args.cmd.replace('-', '_')](args)


if __name__ == '__main__':
    main()
