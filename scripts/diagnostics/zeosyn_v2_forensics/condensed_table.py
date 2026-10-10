import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import csv, json, os
F=_REPO + '/docs/experiments/zeosyn_v2_forensics'
rows=list(csv.DictReader(open(F+'/slots_v2.csv')))
S={}
p=F+'/single_descriptor_scores.json'
if os.path.exists(p): S=json.load(open(p)).get('single',{})
ab={'ALKALINITY_OH_per_T':'ALK','DILUTION_H2O_per_T':'DIL','SI_AL_P_composition':'SiAlP','FLUORIDE_per_T':'F/T','FLUORIDE_vs_OH':'F-OH','INORGANIC_cation_per_Al_or_T':'INORG','OSDA_loading_per_T':'SDA/T','OSDA_charge_per_T':'SDAq/T','CHARGE_organic_vs_inorganic':'ORG/INORG','HETEROATOM_fraction':'HET','ALPO_P_Al_balance':'P-Al','OSDA_molecular_property_combo':'SDAmol'}
def cut(s,n): s=s or ''; return s if len(s)<=n else s[:n-1]+'…'
out=['| grp | r | R | fam | factor chosen | queries written | name = formula | inputs | kg_* | ev→cite | status | single Δacc | traj Δacc / Δbacc / ΔF1 |','|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for x in rows:
    qs=[q for q in x['queries'].split(' || ') if q]
    q=' ‖ '.join(cut(s,46) for s in qs) if qs else '—'
    inputs=x['used_inputs'].split()
    inp=' '.join(inputs) if len(inputs)<=6 else f"{' '.join(inputs[:4])} +{len(inputs)-4}"
    st={'accepted':'ok','repaired':'REPAIRED','failed':'FAILED'}[x['status']]
    cite=x['evidence_ids'].replace(' ',',') if x['evidence_ids']!='-' else '—'
    sd=S.get(x['formula']); sds=f"{100*sd['delta']['mean']['accuracy']:+.2f}" if sd else 'n/a'
    out.append(f"| {x['group']} | {x['traj']} | {x['round']} | {ab[x['family']]} | {cut(x['factor'],42)} | {q} | {x['name']} = `{cut(x['formula'],56)}` | {inp} | {x['uses_kg_feature'] if x['uses_kg_feature']!='-' else 'none'} | {x['evidence_items']}→{cite} | {st} | {sds} | {float(x['traj_delta_acc_pp']):+.2f} / {float(x['traj_delta_bacc_pp']):+.2f} / {float(x['traj_delta_f1_pp']):+.2f} |")
open(F+'/slots_v2_condensed.md','w').write('\n'.join(out)+'\n')
print(len(out)-2,'rows; chars', sum(len(l) for l in out), '| singles available for', sum(1 for x in rows if x['formula'] in S), 'slots')
