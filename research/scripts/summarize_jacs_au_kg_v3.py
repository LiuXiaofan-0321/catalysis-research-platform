"""Summarize the main V3 pilot and the separate same-facts text control."""
import argparse
import json
from pathlib import Path

from analyze_jacs_au_kg_v2 import analyze


def summarize(root):
    main = analyze(root, 3)
    control = analyze(root/'ablation-flat', 3)
    if main['profile'] != 'jacs-au-kg-v3' or control['profile'] != 'jacs-au-kg-v3':
        raise ValueError('V3 records required')
    if main['graph_view'] != 'paths' or control['graph_view'] != 'text':
        raise ValueError('Wrong ablation rendering')
    control['groups'] = {'small_kg_rag_agent': control['groups']['small_kg_rag_agent']}
    control['expected_modes'] = ['small_kg_rag_agent']
    control['complete'] = control['groups']['small_kg_rag_agent']['completed'] == 3 and not control['unfinished_or_failed']
    paired = []
    for replicate in range(1, 4):
        filename = f'small_kg_rag_agent-replicate-{replicate}.json'
        a = root/'discovery'/filename
        b = root/'ablation-flat/discovery'/filename
        if not a.exists() or not b.exists(): continue
        graph = json.loads(a.read_text(encoding='utf-8'))
        flat = json.loads(b.read_text(encoding='utf-8'))
        # Query order can change after feedback. Compare complete scientific
        # facts, removing only per-prompt evidence IDs; report rather than hide
        # any actual content differences in a future expanded evidence pool.
        def facts(rd):
            return sorted(json.dumps({k:v for k,v in x.items() if k != 'id'}, ensure_ascii=False, sort_keys=True)
                          for x in rd['items'])
        paired.append({'replicate': replicate, 'rounds': [
            {'round': x['round'], 'same_facts': facts(x) == facts(y)}
            for x,y in zip(graph['evidence_by_round'], flat['evidence_by_round'])]})
    result = {'profile': 'jacs-au-kg-v3', 'complete': main['complete'] and control['complete'],
              'main': main, 'flat_control': control, 'paired_fact_checks': paired,
              'interpretation': 'Development pilot; unchanged native D0. Differences in predictive gain do not by themselves validate a mechanism.'}
    (root/'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps({'complete': result['complete'], 'main_complete': main['complete'],
                      'flat_complete': control['complete']}, ensure_ascii=False))
    if not result['complete']: raise RuntimeError('Incomplete V3 pilot; see summary.json')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    summarize(parser.parse_args().root)
