"""Offline audit of saved prompts; no API calls, model fits, or score edits."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from catalysis_research.experiments.jacs_au_knowledge import select_evidence
from catalysis_research.retrieval.bundle import count_tokens

BENCHMARK_ID = 'pmc:pmc11672123'


def serialized(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def tokens(value):
    return count_tokens(serialized(value))


def key(item):
    # Prompt items omit document_id; paper + exact quote is the comparable unit.
    return item['paper_id'], item['quote']


def text_fields(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from text_fields(item)
    elif isinstance(value, list):
        for item in value:
            yield from text_fields(item)


def pack_graph(items):
    """Intern complete objects, retaining variants even if their source IDs match.

    Assert exact round-trip reconstruction, including qualifiers and provenance.
    This measures storage/prompt repetition, not new prediction performance.
    """
    packed = {'items': deepcopy(items), 'nodes': {}, 'edges': {}, 'supports': {}}
    indexes = {kind: {} for kind in ('nodes', 'edges', 'supports')}

    def intern(kind, value):
        encoded = serialized(value)
        if encoded not in indexes[kind]:
            ref = kind[0] + str(len(indexes[kind]) + 1)
            indexes[kind][encoded] = ref
            packed[kind][ref] = deepcopy(value)
        return indexes[kind][encoded]

    for item in packed['items']:
        for path in item.get('graph_paths', []):
            path['nodes'] = [intern('nodes', node) for node in path['nodes']]
            refs = []
            for edge in path['edges']:
                edge['support'] = [intern('supports', support) for support in edge['support']]
                refs.append(intern('edges', edge))
            path['edges'] = refs
    restored = deepcopy(packed['items'])
    for item in restored:
        for path in item.get('graph_paths', []):
            path['nodes'] = [deepcopy(packed['nodes'][ref]) for ref in path['nodes']]
            path['edges'] = [deepcopy(packed['edges'][ref]) for ref in path['edges']]
            for edge in path['edges']:
                edge['support'] = [deepcopy(packed['supports'][ref]) for ref in edge['support']]
    assert restored == items, 'Deduplication changed a source fact or qualification'
    return packed


def describe(values):
    return {'mean': statistics.mean(values), 'min': min(values), 'max': max(values)} if values else None


def audit(root):
    bank = json.loads((root / 'evidence/bank.json').read_text(encoding='utf-8'))
    records = [json.loads(p.read_text(encoding='utf-8')) for p in sorted((root / 'discovery').glob('*.json'))]
    result = {
        'audit_type': 'offline_saved_prompt_diagnosis',
        'benchmark_identity': {
            'doi': '10.1021/jacsau.4c00429', 'pmcid': 'PMC11672123', 'pmid': '39735916',
            'verification_url': 'https://pubmed.ncbi.nlm.nih.gov/39735916/',
            'present_in_exclusion_list': BENCHMARK_ID in bank['source_audit']['excluded_paper_ids'],
        },
        'benchmark_rows_in_bank': {
            ch: [{'record_id': r['record_id'], 'document_id': r['document_id'], 'locator': r['locator']}
                 for r in bank[ch] if r['paper_id'] == BENCHMARK_ID] for ch in ('rag', 'kg')
        },
        'groups': {}, 'kg_round_replays': [],
        'limitations': [
            'Replay and compression do not measure a change in predictive performance.',
            'Known benchmark-alias detection is not a complete audit of all external papers or LLM pretraining.',
            'Citations record attribution, not causal dependence or verification of a hypothesis.',
            'Compression retains contaminated facts for measurement only; these must be excluded from future runs.',
        ],
    }
    relations = Counter()
    for mode in sorted({r['mode'] for r in records}):
        runs = [r for r in records if r['mode'] == mode]
        prompt_counts = []; contaminated_candidates = []; retained_contaminated = []
        overlaps = []
        for run in runs:
            contaminated_ids = set()
            previous = None
            for rd in run['evidence_by_round']:
                items = rd['items']
                leaked = [e for e in items if e['paper_id'] == BENCHMARK_ID]
                contaminated_ids.update(e['id'] for e in leaked)
                prompt_counts.append(len(leaked))
                current = {key(e) for e in items}
                if previous is not None and current | previous:
                    overlaps.append(len(current & previous) / len(current | previous))
                previous = current
                if mode != 'small_kg_rag_agent':
                    continue
                bank['active_round'] = rd['round']
                replay, _ = select_evidence(bank, 'rag_agent', rd['retrieval']['query'])
                replay_keys = {key(e) for e in replay}
                actual_keys = {key(e) for e in items}
                all_text = list(text_fields(items))
                anchor_in_nested_text = sum(any(e['quote'] in text for text in all_text) for e in replay)
                packed = pack_graph(items)
                # Counterfactual preserves all anchor RAG + all actual KG facts.
                merged = deepcopy(replay) + [deepcopy(e) for e in items if 'kg' in e['channels']]
                # IDs label evidence; assign distinct IDs for this offline union only.
                for i, item in enumerate(merged):
                    item['id'] = f'U{i+1:02d}'
                union_packed = pack_graph(merged)
                edges = [e for item in items for p in item.get('graph_paths', []) for e in p['edges']]
                supports = [s['quote'] for e in edges for s in e['support']]
                relations.update(e['relation'] for e in edges)
                result['kg_round_replays'].append({
                    'replicate': run['replicate'], 'round': rd['round'],
                    'actual_items': len(items), 'actual_rag_items': sum('rag' in e['channels'] for e in items),
                    'rag_anchor_items': len(replay), 'rag_anchor_quotes_preserved_any_channel': len(replay_keys & actual_keys),
                    'rag_anchor_verbatim_quotes_present_including_nested_fields': anchor_in_nested_text,
                    'original_tokens': tokens(items), 'lossless_deduplicated_tokens': tokens(packed),
                    'rag_anchor_plus_same_kg_deduplicated_tokens': tokens(union_packed),
                    'round_trip_exact': True,
                    'edge_occurrences': len(edges), 'support_quote_occurrences': len(supports),
                    'unique_support_quotes': len(set(supports)),
                    'benchmark_evidence_ids': [e['id'] for e in leaked],
                })
            for rd in run['rounds']:
                for c in rd['candidates']:
                    if set(c.get('evidence_ids', [])) & contaminated_ids:
                        entry = {'replicate': run['replicate'], 'round': rd['round'],
                                 'name': c['name'], 'formula': c['formula'],
                                 'benchmark_citations': sorted(set(c['evidence_ids']) & contaminated_ids)}
                        contaminated_candidates.append(entry)
                        if c['retained']:
                            retained_contaminated.append(entry)
        result['groups'][mode] = {
            'runs': len(runs), 'prompt_rounds': len(prompt_counts),
            'rounds_containing_benchmark': sum(n > 0 for n in prompt_counts),
            'benchmark_items_per_round': describe(prompt_counts),
            'candidates_citing_benchmark': contaminated_candidates,
            'retained_citing_benchmark': retained_contaminated,
            'adjacent_round_evidence_jaccard': describe(overlaps),
        }
    replays = result['kg_round_replays']
    result['replay_summary'] = {k: describe([r[k] for r in replays]) for k in (
        'actual_rag_items', 'rag_anchor_quotes_preserved_any_channel', 'original_tokens',
        'rag_anchor_verbatim_quotes_present_including_nested_fields',
        'lossless_deduplicated_tokens', 'rag_anchor_plus_same_kg_deduplicated_tokens',
        'support_quote_occurrences', 'unique_support_quotes')}
    result['relation_occurrences'] = dict(relations)
    result['paper_relation_fraction'] = sum(v for k, v in relations.items() if k.startswith('PAPER_')) / sum(relations.values())
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    result = audit(args.root)
    target = args.root / 'diagnosis.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    print(json.dumps({
        'output': str(target), 'replay_summary': result['replay_summary'],
        'paper_relation_fraction': result['paper_relation_fraction'],
        'benchmark_excluded': result['benchmark_identity']['present_in_exclusion_list'],
        'groups': {m: {**{k: g[k] for k in ('rounds_containing_benchmark', 'benchmark_items_per_round', 'adjacent_round_evidence_jaccard')},
                       'candidates_citing_benchmark': len(g['candidates_citing_benchmark']),
                       'retained_citing_benchmark': len(g['retained_citing_benchmark'])} for m, g in result['groups'].items()},
    }, ensure_ascii=False, indent=2))
