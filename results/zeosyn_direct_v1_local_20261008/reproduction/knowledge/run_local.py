"""Local CPU launcher. Calls the unchanged release-matched repository code."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import getpass
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'knowledge'
ENTRY = ROOT / 'scripts/run_zeosyn.py'
SOURCE_CONFIG = ROOT / 'configs/experiments/zeosyn-direct-v1.json'
RELEASE = ROOT / '.local-knowledge/knowledge-zeolite-v1-20261008'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(stage, run, *args, log=None):
    command = [sys.executable, '-u', str(ENTRY), stage, '--run-dir', str(run), *map(str, args)]
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        # Append to logs so interrupted work retains its original diagnostics.
        with log.open('a', encoding='utf-8') as handle:
            subprocess.run(command, cwd=ROOT, check=True, stdout=handle, stderr=subprocess.STDOUT)
    else:
        subprocess.run(command, cwd=ROOT, check=True)


def prepare(args, run):
    manifest = run / 'prepared/data-manifest.json'
    if not manifest.exists():
        call('prepare', run, '--data-root', ROOT / 'data/zeosyn', '--config', SOURCE_CONFIG)
    if digest(run / 'prepared/config.json') != digest(SOURCE_CONFIG):
        raise RuntimeError('Prepared config differs from release config; use a separate run directory.')
    if not (run / 'prepared/knowledge.json').exists():
        call('knowledge', run, '--base-retrieval-config', ROOT / 'configs/retrieval/small-kg-hybrid-v1.json',
             '--rag-index', ASSETS / 'rag/full-rag-v1-index', '--snapshot', ASSETS / 'kg/Small-KG-zeolite-v1',
             '--overlay', ASSETS / 'normalization/scientific-normalization-Small-KG-zeolite-v1.1')
    if not (run / 'd0.json').exists():
        call('baseline', run, '--n-jobs', args.rf_jobs)
    call('status', run)


def experiment(args, run):
    prepare(args, run)
    tasks = read(run / 'prepared/tasks.json')['tasks']
    if not os.environ.get('ZHIPU_API_KEY'):
        if not sys.stdin.isatty():
            raise RuntimeError('Set ZHIPU_API_KEY in your terminal before starting generation.')
        os.environ['ZHIPU_API_KEY'] = getpass.getpass('ZHIPU_API_KEY (hidden, kept in memory): ')
    if not os.environ.get('ZHIPU_API_KEY'):
        raise RuntimeError('ZHIPU_API_KEY is empty.')
    if not (run / 'api-probe.json').exists():
        call('probe', run)

    def generate(task):
        name = f"{task['mode']}-replicate-{task['replicate']}"
        call('generate', run, '--task-index', task['index'], log=run / 'local-logs' / f'{name}.log')
        print(f'Generation complete: {name}', flush=True)

    pending = [t for t in tasks if not (run / 'generation' / f"{t['mode']}-replicate-{t['replicate']}.json").exists()]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(generate, t) for t in pending]
        try:
            for future in as_completed(futures):
                future.result()
        except BaseException:
            for future in futures:
                future.cancel()
            raise
    # Freeze all generations before evaluating; no scores feed back to the model.
    for task in tasks:
        name = f"{task['mode']}-replicate-{task['replicate']}"
        if not (run / 'evaluation' / f'{name}.json').exists():
            call('evaluate', run, '--task-index', task['index'], '--n-jobs', args.rf_jobs)
    call('summarize', run)
    call('status', run)


def query(args, run):
    from catalysis_research.knowledge.retrieval import KnowledgeModeRetriever, RetrievalBudget
    config_path = run / 'prepared/retrieval-config.json'
    if not config_path.exists():
        raise RuntimeError('Run prepare first to freeze the held-out-paper exclusions.')
    started = time.perf_counter()
    retriever = KnowledgeModeRetriever.from_directories(
        config_path=config_path, rag_index_directory=ASSETS / 'rag/full-rag-v1-index',
        kg_snapshot_directory=ASSETS / 'kg/Small-KG-zeolite-v1',
        normalization_overlay_directory=ASSETS / 'normalization/scientific-normalization-Small-KG-zeolite-v1.1')
    budget = RetrievalBudget(**read(config_path)['budget'])
    print(f'Loaded once in {time.perf_counter() - started:.2f}s. Offline; no GLM calls.', flush=True)
    output_root = RELEASE / 'queries'
    output_root.mkdir(exist_ok=True)
    modes = ['rag_agent', 'small_kg_rag_agent'] if args.mode == 'both' else [args.mode]
    text = args.query
    while True:
        if not text:
            if not args.interactive:
                break
            try:
                text = input('Query (empty to exit): ').strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not text:
                break
        for mode in modes:
            started = time.perf_counter()
            bundle = retriever.retrieve(query=text, experiment_mode=mode, budget=budget)
            seconds = time.perf_counter() - started
            output = output_root / f'{time.time_ns()}-{mode}.json'
            output.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(json.dumps({'mode': mode, 'selected_count': bundle['selected_count'],
                              'selected_token_count': bundle['selected_token_count'],
                              'query_seconds': round(seconds, 3), 'output': str(output)}, ensure_ascii=False), flush=True)
        if not args.interactive:
            break
        text = None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'run', 'status', 'query'])
    parser.add_argument('--run-dir', type=Path, default=ROOT / 'runs/zeosyn-local-v1-20261008')
    parser.add_argument('--rf-jobs', type=int, choices=range(1, 17), default=8)
    parser.add_argument('--workers', type=int, choices=range(1, 6), default=5)
    parser.add_argument('--mode', choices=['rag_agent', 'small_kg_rag_agent', 'both'], default='both')
    parser.add_argument('--query')
    parser.add_argument('--interactive', action='store_true')
    args = parser.parse_args()
    if args.stage == 'query' and not args.query and not args.interactive:
        parser.error('query requires --query or --interactive')
    expected = read(RELEASE / 'manifest.json')['source_code_commit']
    actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if actual != expected:
        raise RuntimeError(f'Release expects code {expected}; current code is {actual}.')
    os.environ.update(HF_HUB_CACHE=str(ASSETS / 'cache/huggingface'), HF_HUB_OFFLINE='1',
                      TRANSFORMERS_OFFLINE='1', OMP_NUM_THREADS=str(args.rf_jobs), MKL_NUM_THREADS=str(args.rf_jobs))
    run = args.run_dir.resolve()
    if args.stage == 'prepare':
        prepare(args, run)
    elif args.stage == 'run':
        experiment(args, run)
    elif args.stage == 'query':
        query(args, run)
    else:
        call('status', run)


if __name__ == '__main__':
    main()
