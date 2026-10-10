import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import sys, json, glob, csv, collections, statistics
F = _REPO + '/docs/experiments/zeosyn_v2_forensics'
sys.path.insert(0, F)
from families import family
RUN = _REPO + '/results/zeosyn_v2_dev_1'
evals = {}
for fn in glob.glob(RUN + '/evaluation/*-replicate-*.json'):
    e = json.load(open(fn)); evals[(e['mode'], e['replicate'])] = e
rows = []
for fn in sorted(glob.glob(RUN + '/generation/*.json')):
    g = json.load(open(fn)); e = evals[(g['mode'], g['replicate'])]
    for s in g['slots']:
        c = s.get('candidate') or {}; plan = s.get('plan') or {}; ev = s.get('evidence') or {}
        ok = [a for a in s['attempts'] if a['kind'] in ('proposal', 'technical_repair') and 'precheck' in a]
        used = ok[-1]['precheck']['used_inputs'] if ok else []
        repaired = any(a['kind'] == 'technical_repair' for a in s['attempts'])
        errs = [a.get('error') for a in s['attempts'] if a.get('error')]
        status = 'failed' if s['status'] != 'appended' else ('repaired' if repaired else 'accepted')
        linking = ev.get('linking') or []
        usage = {k: sum((a.get('usage') or {}).get(k, 0) or 0 for a in s['attempts']) for k in ('prompt_tokens', 'completion_tokens')}
        reasoning = sum((((a.get('usage') or {}).get('completion_tokens_details') or {}).get('reasoning_tokens', 0) or 0) for a in s['attempts'])
        items = ev.get('items', [])
        rows.append(dict(
            group=g['mode'], traj=g['replicate'], round=s['round'], factor=plan.get('factor'),
            queries=' || '.join(plan.get('queries', [])), n_queries=len(plan.get('queries', [])),
            name=c.get('name'), formula=c.get('formula'), family=family(c.get('formula')),
            used_inputs=' '.join(used), uses_kg_feature=' '.join(c.get('uses_kg_inputs', [])) or '-',
            evidence_items=len(items), evidence_tokens=ev.get('tokens'),
            evidence_keys=' | '.join(i['key'] for i in items),
            linked_osdas=sum(len(l['osdas']) for l in linking), linked_frameworks=sum(len(l['frameworks']) for l in linking),
            linked_conditions=sum(len(l['conditions']) for l in linking),
            evidence_ids=' '.join(map(str, c.get('evidence_ids', []))) or '-',
            cited_keys=' | '.join(c.get('cited_evidence_keys', [])) or '-',
            knowledge_source=c.get('knowledge_source'), novelty=c.get('novelty'),
            status=status, repair_error='; '.join(errs), prompt_tokens=usage['prompt_tokens'],
            completion_tokens=usage['completion_tokens'], reasoning_tokens=reasoning,
            traj_delta_acc_pp=round(100 * e['delta']['mean']['accuracy'], 3),
            traj_delta_bacc_pp=round(100 * e['delta']['mean']['balanced_accuracy'], 3),
            traj_delta_f1_pp=round(100 * e['delta']['mean']['macro_f1'], 3),
            traj_delta_acc_kgcovered_pp=round(100 * e['strata']['kg_covered']['accuracy_delta'], 3),
            traj_delta_acc_notcovered_pp=round(100 * e['strata']['kg_not_covered']['accuracy_delta'], 3),
        ))
with open(F + '/slots_v2.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('wrote', len(rows), 'rows to slots_v2.csv')
print('\n=== CONDENSED SLOT TABLE (group traj round | status | family | formula | cites | kg_feat | traj d-acc pp) ===')
for r in rows:
    print(f"{r['group']:11s} r{r['traj']:<2d} R{r['round']} | {r['status']:8s} | {r['family']:30s} | {r['formula'][:70]:70s} | ev={r['evidence_items']} cite={r['evidence_ids']:4s} | kg={r['uses_kg_feature']} | {r['traj_delta_acc_pp']:+.2f}")
print('\n=== FAMILY COUNTS BY GROUP ===')
fam = collections.defaultdict(collections.Counter)
for r in rows: fam[r['group']][r['family']] += 1
allf = sorted({f for g in fam for f in fam[g]})
print(f"{'family':32s}" + ''.join(f'{g:>13s}' for g in fam) + '   total')
for f in allf:
    print(f"{f:32s}" + ''.join(f'{fam[g][f]:13d}' for g in fam) + f"{sum(fam[g][f] for g in fam):8d}")
print('distinct families overall:', len(allf))
print('\n=== FAMILY BY ROUND (all groups) ===')
fr = collections.defaultdict(collections.Counter)
for r in rows: fr[r['round']][r['family']] += 1
for rd in sorted(fr): print(rd, dict(fr[rd].most_common()))
print('\n=== OVERLAP BETWEEN GROUPS ===')
groups = list(fam)
for i in range(len(groups)):
    for j in range(i + 1, len(groups)):
        a, b = set(fam[groups[i]]), set(fam[groups[j]])
        fa = {r['formula'].replace(' ', '') for r in rows if r['group'] == groups[i]}
        fb = {r['formula'].replace(' ', '') for r in rows if r['group'] == groups[j]}
        print(f"{groups[i]:11s} vs {groups[j]:11s}: families Jaccard={len(a & b) / len(a | b):.2f} ({len(a & b)}/{len(a | b)}); exact-formula overlap {len(fa & fb)} of {len(fa | fb)} distinct")
print('\n=== PER-TRAJECTORY DELTAS (pp) ===')
for g in groups:
    print(g)
    for r in range(1, 11):
        e = evals[(g, r)]; st = e['strata']
        fams = [x['family'] for x in rows if x['group'] == g and x['traj'] == r]
        print(f"  r{r:<2d} acc {100*e['delta']['mean']['accuracy']:+.3f}  bacc {100*e['delta']['mean']['balanced_accuracy']:+.3f}  f1 {100*e['delta']['mean']['macro_f1']:+.3f} | covered {100*st['kg_covered']['accuracy_delta']:+.2f} notcov {100*st['kg_not_covered']['accuracy_delta']:+.2f} noOSDA {100*st['no_osda']['accuracy_delta']:+.2f} common {100*st['osda_common_in_training']['accuracy_delta']:+.2f} rare {100*st['osda_rare_in_training']['accuracy_delta']:+.2f} | seeds " + ' '.join(f"{100*p['accuracy']:+.2f}" for p in e['delta']['per_seed']) + ' | ' + ', '.join(f[:14] for f in fams))
    d = [100 * evals[(g, r)]['delta']['mean']['accuracy'] for r in range(1, 11)]
    print(f"  mean {statistics.mean(d):+.3f} sd {statistics.stdev(d):.3f} min {min(d):+.3f} max {max(d):+.3f}")
print('\n=== EVIDENCE USE / SOURCE / NOVELTY BY GROUP ===')
for g in groups:
    rs = [r for r in rows if r['group'] == g]
    print(g, 'slots', len(rs), 'repaired', sum(r['status'] == 'repaired' for r in rs),
          'with evidence items', sum(r['evidence_items'] > 0 for r in rs), 'mean items', round(statistics.mean(r['evidence_items'] for r in rs), 2),
          'citing', sum(r['evidence_ids'] != '-' for r in rs), 'uses kg feature', sum(r['uses_kg_feature'] != '-' for r in rs),
          'knowledge_source', dict(collections.Counter(r['knowledge_source'] for r in rs)),
          'novelty', dict(collections.Counter(r['novelty'] for r in rs)),
          'queries/slot', round(statistics.mean(r['n_queries'] for r in rs), 2),
          'tokens/slot prompt', round(statistics.mean(r['prompt_tokens'] for r in rs)), 'completion', round(statistics.mean(r['completion_tokens'] for r in rs)), 'reasoning', round(statistics.mean(r['reasoning_tokens'] for r in rs)))
print('\n=== KG LINKING: what the model queries resolved to (kg + kg_shuffled) ===')
for g in ('kg', 'kg_shuffled'):
    rs = [r for r in rows if r['group'] == g]
    print(g, 'slots with 0 evidence items:', sum(r['evidence_items'] == 0 for r in rs), '| linked osdas total', sum(r['linked_osdas'] for r in rs), 'frameworks', sum(r['linked_frameworks'] for r in rs), 'conditions', sum(r['linked_conditions'] for r in rs))
    kc = collections.Counter(k.split(':')[0] for r in rs for k in r['evidence_keys'].split(' | ') if k)
    cc = collections.Counter(k.split(':')[0] for r in rs for k in r['cited_keys'].split(' | ') if k and k != '-')
    print('   evidence item types', dict(kc), '| cited item types', dict(cc))
    print('   most common evidence keys', collections.Counter(k for r in rs for k in r['evidence_keys'].split(' | ') if k).most_common(12))
print('\n=== INPUT COLUMN USAGE (all 120 formulas) ===')
cu = collections.Counter(u for r in rows for u in r['used_inputs'].split())
print(cu.most_common(40))
print('\n=== ALL DISTINCT QUERIES BY GROUP ===')
for g in groups:
    qs = [q for r in rows if r['group'] == g for q in r['queries'].split(' || ') if q]
    print(g, len(qs), 'queries,', len(set(qs)), 'distinct')
