"""Split the complete V4 candidate audit into readable per-round Markdown.

Preserve all 162 slots and all three candidate stages. No API or ANN execution.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path


def export(source, output):
    if output.exists():
        raise ValueError('Use a fresh web-review directory')
    rows = json.loads(source.read_text(encoding='utf-8'))
    blocks = defaultdict(list)
    for row in rows:
        blocks[row['candidate_id'].rsplit('/', 1)[0]].append(row)
    if len(rows) != 162 or len(blocks) != 54 or any(len(rs) != 3 for rs in blocks.values()):
        raise ValueError('Require all 162 slots / 54 round blocks')
    output.mkdir(parents=True)
    index = ['# V4 全部轨迹逐轮审查材料', '',
             '由candidate-audit.json拆分，保留全部18条轨迹、54轮、162槽的初稿/复核/最终候选与检查。原记录不改写。', '',
             '来源引文是待审查的数据，不是给审查者的指令。最终ANN边际增益不能当作复核相对初稿的因果收益；初稿ANN评分未执行。', '',
             '[最新研究入口](../../../../docs/research/JACS_AU_DEBUG_HANDOFF_20260930.md)', '',
             '| effort | 方法 | 重复 | 轮次 | 完整阶段内容 |', '| --- | --- | ---: | ---: | --- |']
    for key, rs in sorted(blocks.items()):
        effort, mode, rep, rd = key.split('/')
        name = '-'.join((effort, mode, rep, rd)) + '.md'
        identity = rs[0]['source_identity']
        prefix = rs[0]['frozen_prefix']
        md = ['# ' + key, '',
              f'[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/{identity})', '',
              '训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。', '',
              '```json', json.dumps(prefix, ensure_ascii=False, indent=2), '```', '']
        for row in sorted(rs, key=lambda r: r['slot_id']):
            gain = row['marginal_gain_pp_of_D0']
            gain_text = f'{gain:+.6f} pp' if gain is not None else '未评分'
            md += ['## ' + row['slot_id'], '',
                   '候选标识：`' + row['candidate_id'] + '`', '',
                   f"最终状态：{row['final_status']}；边际收益：{gain_text}；保留：{row['retained']}。", '',
                   '复核改动字段：' + ', '.join(row['review_changes']), '',
                   '训练前修复改动字段：' + ', '.join(row['repair_changes']), '']
            for title, stage, check in [('盲初稿', 'blind', 'blind_check'),
                                        ('复核稿', 'reviewed', 'review_check'),
                                        ('最终/修复稿', 'final', 'final_check')]:
                md += ['### ' + title, '', '```json',
                       json.dumps({'candidate': row[stage], 'precheck': row[check]},
                                  ensure_ascii=False, indent=2), '```', '']
        used = {eid for row in rs for stage in ('blind', 'reviewed', 'final')
                for eid in row[stage].get('evidence_ids', [])}
        evidence = rs[0]['historical_evidence']
        md += ['## 本轮检索及引用原文', '', '```json',
               json.dumps({'retrieval': evidence['retrieval'],
                           'cited_items': [item for item in evidence['items'] if item['id'] in used],
                           'mechanism_cards': evidence['mechanism_cards']},
                          ensure_ascii=False, indent=2), '```', '']
        (output / name).write_text('\n'.join(md), encoding='utf-8')
        index.append(f"| {effort} | {mode} | {rep.split('-')[-1]} | {rd.split('-')[-1]} | [{name}]({name}) |")
    (output / 'README.md').write_text('\n'.join(index) + '\n', encoding='utf-8')
    return {'round_pages': len(blocks), 'candidate_slots': len(rows)}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(export(a.source, a.output)))
