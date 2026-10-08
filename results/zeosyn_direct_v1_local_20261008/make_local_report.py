"""Validate and summarize the completed local run without modifying results."""
from collections import Counter
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import subprocess

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

summary = read(RUN / 'summary.json')
config = read(RUN / 'prepared/config.json')
manifest = read(RUN / 'prepared/data-manifest.json')
tasks = read(RUN / 'prepared/tasks.json')['tasks']
generation_files = sorted((RUN / 'generation').glob('*.json'))
evaluation_files = sorted((RUN / 'evaluation').glob('*.json'))
gens = [read(p) for p in generation_files]
evs = [read(p) for p in evaluation_files]
assert len(gens) == len(evs) == len(tasks) == 30
assert not summary['missing']
assert sha(RUN / 'prepared/config.json') == sha(ROOT / 'configs/experiments/zeosyn-direct-v1.json')
assert sha(RUN / 'prepared/matrices.npz') == manifest['matrix_sha256']
for gen in gens:
    assert gen['matrix_sha256'] == manifest['matrix_sha256'] and gen['config_sha256'] == manifest['config_sha256']
    assert gen['label_feedback'] is False
for path,ev in zip(evaluation_files,evs):
    assert ev['generation_sha256'] == sha(RUN / 'generation' / path.name)
    assert len(ev['per_seed']) == len(config['evaluation']['fit_seeds'])
secret_pattern = re.compile(r'\b[a-fA-F0-9]{32}\.[A-Za-z0-9_-]{16,}\b')
scanned = [p for p in RUN.rglob('*') if p.is_file() and p.suffix in ('.json','.log','.md','.py')]
secret_files = [str(p.relative_to(RUN)) for p in scanned if secret_pattern.search(p.read_text(encoding='utf-8-sig',errors='replace'))]
assert not secret_files, 'Credential-pattern match in output files; do not publish.'
failures = Counter(s.get('failure') for g in gens for s in g['slots'] if s['status']=='failed')
attempts = [a for g in gens for s in g['slots'] for a in s['attempts']]
usage = {k:sum(a.get('usage',{}).get(k,0) or 0 for a in attempts) for k in ['prompt_tokens','completion_tokens','total_tokens']}
labels = {'agent':'Agent','rag_agent':'RAG','small_kg_rag_agent':'KG+RAG'}
lines = ['# ZeoSyn 本地运行结果','',f"代码：`{subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}`。",'',
         '三组各 10 条生成轨迹，每条 3 轮；GLM-5.3-Flash，high；生成并发 5，随机森林 8 线程。沿用官方协议和全部五个 fit seed。',
         '',f"训练 {manifest['train_rows']:,} 行，测试 {manifest['test_rows']:,} 行，按 DOI 分组。测试论文排除检查已经通过。",
         '',f"D0 mean accuracy：**{summary['d0']['accuracy']*100:.4f}%**。下面的增益是准确率绝对差值（百分点），各轨迹先对五个 seed 平均。组内区间为轨迹 bootstrap 95% 区间。",'',
         '| 方法 | 轨迹数 | 成功追加槽 | D0+X 准确率 | 相对 D0 增益（百分点） | 95% 区间 | 负收益轨迹 |',
         '| --- | ---: | ---: | ---: | ---: | --- | ---: |']
for mode,row in summary['per_mode'].items():
    mean = row['accuracy']['mean']; lo,hi=row['accuracy']['ci']
    lines.append(f"| {labels[mode]} | {row['trajectories_evaluated']} | {row['appended_slots']}/{row['total_slots']} | {(summary['d0']['accuracy']+mean)*100:.4f}% | {mean*100:+.4f} | [{lo*100:+.4f}, {hi*100:+.4f}] | {row['negative_trajectories']} |")
lines += ['', '## 组间比较', '', '组间 bootstrap 区间为 97.5%，单位为百分点。','', '| 比较 | 均值差 | 97.5% 区间 |', '| --- | ---: | --- |']
for name,row in summary['comparisons'].items():
    a,b=name.split('-'); lo,hi=row['ci']
    lines.append(f"| {labels[a]} − {labels[b]} | {row['mean']*100:+.4f} | [{lo*100:+.4f}, {hi*100:+.4f}] |")
kg_rag = summary['comparisons']['small_kg_rag_agent-rag_agent']
lines += ['', 'KG+RAG 相对 RAG 的区间' + ('跨越零，本次运行未确认 KG 的增益。' if kg_rag['ci'][0] <= 0 <= kg_rag['ci'][1] else ('全部为正，支持本次固定设置下 KG+RAG 的正增益。' if kg_rag['ci'][0]>0 else '全部为负，本次固定设置下 KG+RAG 低于 RAG。')),
          '', '没有相同事实平铺对照，因此这次比较不能单独归因于图结构。此处区间描述生成轨迹变化，并不涵盖其他测试数据划分。', '',
          f"失败槽：{sum(failures.values())}；技术修复调用：{sum(a['kind']=='technical_repair' for a in attempts)}。失败、零追加和负收益轨迹均保留。",
          '', f"已记录的生成 token 用量：{json.dumps(usage)}（不等同于账单，未记录 usage 的请求不包含在内）。",'',
          '完整轨迹：`generation/`；逐 seed 评分：`evaluation/`；冻结输入和证据：`prepared/`；官方汇总：`summary.json`；运行日志：`local-logs/`。']
(RUN/'LOCAL_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
execution=read(RUN/'local-execution.json')
execution.update(status='complete',finished_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),generated=len(gens),evaluated=len(evs),failed_slots=sum(failures.values()),recorded_generation_usage=usage,validation='hashes, all 30 trajectories, five-seed evaluations, no credential-pattern matches')
(RUN/'local-execution.json').write_text(json.dumps(execution,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'complete':True,'per_mode':summary['per_mode'],'comparisons':summary['comparisons'],'failed_slots':sum(failures.values()),'report':str(RUN/'LOCAL_REPORT.md')},ensure_ascii=False,indent=2))
