"""V4: feature-domain aware proposals, source retrieval and executable grounding.

No labels enter domain summaries, graph construction or evidence retrieval.
Historical protocols remain reproducible. All scientific checks are shared.
"""
from __future__ import annotations

import ast
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re

import numpy as np
from scipy.stats import spearmanr

from .jacs_au import FEATURES
from .jacs_au_knowledge import INPUT_SCHEMA, audit_dimensions, relevance, scope_tags
from .jacs_au_kg_v3 import audit_bank as audit_v3, complete_quote, token_count
from .jacs_au_sources import assert_clean, contamination_reason, exclusion_closure

PROFILE = 'jacs-au-kg-v4'
EXECUTION_REVISION = 'explicit-normalization-20260930c'
ROTOR_TOL = 1e-10
ROLES = {
    **{k: 'adsorbate_geometry_proxy' for k in FEATURES[:9]},
    **{k: 'heavy_atom_inertia_proxy' for k in ['PMI1', 'PMI2', 'PMI3']},
    'PBF': 'heavy_atom_planarity', 'SPAN': 'heavy_atom_enclosing_radius',
    'GeDi': 'heavy_atom_pair_distance', 'Vol': 'molecular_vdw_volume',
    'density': 'native_framework_density_proxy',
    'ASA': 'probe_accessible_specific_area', 'AV': 'probe_accessible_specific_volume',
    'lsd_f': 'bottleneck_free_sphere_Df', 'lsd_p': 'included_along_free_path_Dif',
}
INPUTS = deepcopy(INPUT_SCHEMA)
for _k, _v in ROLES.items():
    INPUTS[_k]['quantity_role'] = _v
INPUTS['lsd_f']['meaning'] = 'Zeo++ Df: largest sphere able to pass through a periodic free path; bottleneck proxy, NOT global cavity diameter Di.'
INPUTS['lsd_p']['meaning'] = 'Zeo++ Dif: largest included sphere ALONG the free-sphere path; NOT bottleneck Df and NOT necessarily global cavity Di.'
for _k in ['PMI1', 'PMI2', 'PMI3', 'SPAN', 'GeDi', 'PBF']:
    INPUTS[_k]['representation'] = 'Original implicit-H/heavy-atom representation; legitimate zero values. Not full all-atom molecular geometry.'
INPUTS['AV']['zero_meaning'] = 'Zero accessibility for the fixed geometric probe does not imply zero physical molecular adsorption space.'


def load_config(path):
    c = json.loads(Path(path).read_text(encoding='utf-8'))
    if c.get('profile') != PROFILE or c.get('reasoning_effort') not in ('low', 'high'):
        raise ValueError('Explicit V4 low/high config required')
    if c.get('execution_revision')!=EXECUTION_REVISION:raise ValueError('Current partial-update execution contract required')
    if c['rounds'] != 3 or c['proposals_per_round'] != 3:
        raise ValueError('V4 pilot requires 3 x 3')
    for group in ('retrieval', 'generation'):
        if any(type(v) is not int or v <= 0 for v in c[group].values()):
            raise ValueError('Budgets must be positive integers')
    if c['generation']['max_tokens_on_truncation'] < c['generation']['max_tokens']:
        raise ValueError('Invalid recovery cap')
    if c['model'] != 'glm-5.3-flash' or c['thinking'] != 'enabled':
        raise ValueError('Frozen model required for the effort comparison')
    return c


def build_bank(v3):
    audit_v3(v3)
    b = deepcopy(v3)
    b.update(profile=PROFILE, source_profile=v3['profile'], review_revision='20260930-v4',
             retrieval_policy='Per-round full-index search; reviewed identities only, complete paragraphs, no benchmark findings')
    b.pop('budget_config', None)
    return b


def audit_bank(bank):
    if bank.get('profile') != PROFILE or bank.get('review_revision') != '20260930-v4':
        raise ValueError('V4 bank required')
    original = deepcopy(bank)
    original.update(profile='jacs-au-kg-v3', review_revision='20260929-scope2')
    audit_v3(original)


def rotor_classes(env):
    # Classification concerns the native proxy, not the true all-atom molecule.
    small = np.abs(env['q_PMI3']) <= ROTOR_TOL
    linear = np.abs(env['q_PMI1']) <= ROTOR_TOL
    return np.where(small, 0, np.where(linear, 1, 2))


def training_domains(env, train):
    result = {}
    for k in FEATURES:
        a = np.asarray(env[k])[train]
        result[k] = dict(min=float(a.min()), max=float(a.max()), zero_n=int(np.sum(a == 0)),
                         near_zero_n=int(np.sum(np.abs(env['q_'+k][train]) <= ROTOR_TOL)),
                         quantiles={str(q): float(np.quantile(a, q)) for q in [0, .1, .25, .5, .75, .9, 1]},
                         ref=float(env[k+'_ref'][train[0]]))
    classes = rotor_classes(env)[train]
    return {'training_n': len(train), 'inputs': result,
            'rotor_proxy_counts': {name: int(np.sum(classes == i)) for i, name in enumerate(['single_site', 'linear', 'nonlinear'])},
            'notes': ['Positive reference medians DO NOT remove input zeros.',
                      'Use full-domain finite proxies or explicit rotor_case branches; no median imputation of physical zeros.',
                      'Independent q-normalization does not turn one into a physical equality threshold.',
                      'All statistics and reference values use training features only.']}


def evaluate_formula(formula, env):
    if not isinstance(formula, str) or len(formula) > 1500:
        raise ValueError('Invalid formula length')
    tree = ast.parse(formula, mode='eval')
    if len(list(ast.walk(tree))) > 160: raise ValueError('Formula too complex')
    funcs = {'log': np.log, 'log10': np.log10, 'sqrt': np.sqrt, 'abs': np.abs,
             'exp': np.exp, 'minimum': np.minimum, 'maximum': np.maximum}
    def visit(n, depth=0):
        if depth > 20: raise ValueError('Formula too deep')
        if isinstance(n, ast.Expression): return visit(n.body, depth+1)
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            if not np.isfinite(n.value) or abs(n.value) > 1e6: raise ValueError('Constant out of bounds')
            return float(n.value)
        if isinstance(n, ast.Name) and n.id in env and not n.id.startswith('_'): return env[n.id]
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            a=visit(n.operand, depth+1); return -a if isinstance(n.op, ast.USub) else a
        if isinstance(n, ast.BinOp):
            a,b=visit(n.left, depth+1),visit(n.right, depth+1)
            if isinstance(n.op, ast.Add): return a+b
            if isinstance(n.op, ast.Sub): return a-b
            if isinstance(n.op, ast.Mult): return a*b
            if isinstance(n.op, ast.Div): return np.divide(a,b)
            if isinstance(n.op, ast.Pow):
                if not np.isscalar(b) or abs(b)>8: raise ValueError('Exponent must be a constant in [-8,8]')
                return np.power(a,b)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and not n.keywords:
            name=n.func.id
            if name=='rotor_case' and len(n.args)==3:
                a,b,c=[visit(x,depth+1) for x in n.args]
                cl=env.get('_rotor_class')
                if cl is None: cl=rotor_classes(env)
                return np.where(cl==0,a,np.where(cl==1,b,c))
            expected=2 if name in ('minimum','maximum') else 1
            if name in funcs and len(n.args)==expected:
                return funcs[name](*(visit(x,depth+1) for x in n.args))
        raise ValueError('Unsupported formula syntax/input')
    with np.errstate(all='ignore'): values=np.asarray(visit(tree),dtype=float)
    if values.shape != (len(env['MW']),): raise ValueError('Formula must return one value per system')
    return values


def formula_symbols(formula):
    return {n.id for n in ast.walk(ast.parse(formula, mode='eval')) if isinstance(n,ast.Name)}


def audit_formula(formula):
    tree=ast.parse(formula,mode='eval')
    calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='rotor_case']
    if not calls: return audit_dimensions(formula)
    if len(calls)!=1 or len(calls[0].args)!=3: raise ValueError('Exactly one three-branch rotor_case is supported')
    call=calls[0]; dims=[]
    for branch in call.args:
        class Replace(ast.NodeTransformer):
            def visit_Call(self,n):
                if isinstance(n.func,ast.Name) and n.func.id=='rotor_case': return deepcopy(branch)
                return self.generic_visit(n)
        expr=ast.unparse(Replace().visit(deepcopy(tree)))
        d=audit_dimensions(expr)['output_dimensions']
        # A pure zero branch can carry the common branch's units.
        if not (isinstance(branch,ast.Constant) and branch.value==0 and tree.body is call): dims.append(d)
    if dims and any(d!=dims[0] for d in dims): raise ValueError('Rotor branches must have compatible dimensions')
    return {'status':'passed','output_dimensions':dims[0] if dims else {},'explicit_rotor_branches':True}


def validate_candidates(value):
    cs=deepcopy(value.get('descriptor_candidates',[]))
    if len(cs)!=3 or {c.get('slot_id') for c in cs}!={'h1','h2','h3'}:
        raise ValueError('Exactly three unique hypothesis slots h1/h2/h3 required')
    cs=sorted(cs,key=lambda c:c['slot_id'])
    for c in cs:
        for key in ('name','formula','hypothesis','rationale','falsification_criteria','novelty_status'):
            if not isinstance(c.get(key),str) or not c[key].strip(): raise ValueError('Missing '+key)
        if c['novelty_status'] not in ('known_relation','new_combination','uncertain'): raise ValueError('Invalid novelty status')
        t=c.get('scientific_test',{})
        for k in ('proxy_assumptions','physical_interpretation','boundary_behavior'):
            if not isinstance(t.get(k),str) or not t[k].strip(): raise ValueError('Missing scientific '+k)
        if t.get('mechanism_family') not in ('translation','rotation','shape','connectivity','coupling'): raise ValueError('Invalid mechanism family')
        if t.get('vary_input') not in FEATURES or t.get('regime_input') not in FEATURES: raise ValueError('Unknown native test variable')
        q=t.get('regime_train_quantiles')
        if not isinstance(q,list) or len(q)!=2 or any(type(x) not in (int,float) or not np.isfinite(x) for x in q) or not 0<=q[0]<q[1]<=1 or q[1]-q[0]<.25:
            raise ValueError('Regime must cover at least 25 percent of training quantiles')
        if t.get('descriptor_direction') not in ('increasing','decreasing') or t.get('entropy_direction') not in ('increasing','decreasing'):
            raise ValueError('Invalid expected direction')
        if not isinstance(c.get('variable_mappings'),dict): raise ValueError('Explicit variable mappings required')
        raw=c.get('physical_claims',[])
        allowed={'empirical_proxy','nonlinear_rotor_expression','probe_volume_proxy','geometric_path_contrast'}
        if not isinstance(raw,list) or not all(isinstance(s,str) for s in raw):raise ValueError('physical_claims must be a list of type labels')
        canonical=[];notes=[]
        for text in raw:
            prefix=text.split(':',1)[0].strip()
            if prefix in allowed:
                if prefix not in canonical:canonical.append(prefix)
                if text!=prefix:notes.append(text)
            elif text.lower().startswith('rotor_case ') and 'rotor_case' in c['formula']:
                # This describes the implementation branches, not a new claim type.
                notes.append(text)
            else:raise ValueError('Unsupported physical_claims label; use exactly '+', '.join(sorted(allowed))+'; put explanations in rationale')
        c['physical_claims']=canonical
        if notes:
            c.setdefault('physical_claims_original',deepcopy(raw))
            c['physical_claim_annotations']=list(dict.fromkeys(c.get('physical_claim_annotations',[])+notes))
    if len({c['scientific_test']['mechanism_family'] for c in cs})<2: raise ValueError('At least two mechanism families required')
    return cs


def grounding_check(c):
    symbols=formula_symbols(c['formula'])
    used={k for k in FEATURES if k in symbols or 'q_'+k in symbols}
    mappings=c['variable_mappings']
    for k in used:
        if mappings.get(k)!=ROLES[k]: raise ValueError('Wrong physical variable mapping: '+k+' requires '+ROLES[k])
    t=c['scientific_test']
    if t['vary_input'] not in used: raise ValueError('Vary-input must actually occur in the formula')
    claims=c.get('physical_claims',[])
    permitted={'empirical_proxy','nonlinear_rotor_expression','probe_volume_proxy','geometric_path_contrast'}
    if not isinstance(claims,list) or not set(claims)<=permitted: raise ValueError('Unknown physical claim')
    if 'nonlinear_rotor_expression' in claims and 'rotor_case' not in symbols:
        raise ValueError('Nonlinear rotor expressions require explicit single-site/linear/nonlinear branches')
    text=' '.join(str(c.get(k,'')) for k in ('hypothesis','rationale'))+' '+t['physical_interpretation']
    for var,wrong in [('lsd_f',r'(?:global\s+)?(?:cage interior|cavity diameter|largest included sphere)'),('lsd_p',r'(?:bottleneck|window) diameter')]:
        if re.search(var+r'\s+(?:is|represents|proxies)\s+(?:the\s+)?'+wrong,text,re.I):
            raise ValueError('Diameter interpretation conflicts with native Df/Dif definitions')
    return {'status':'passed','used_variables':sorted(used),'quantity_roles':{k:mappings[k] for k in sorted(used)},
            'interpretation':'Executable definition checks; not a proof of all natural-language claims or causality.'}


def precheck(c, env, train, entropy, reference):
    report={'status':'rejected'}
    try:
        report['dimensions']=audit_formula(c['formula'])
        report['grounding']=grounding_check(c)
        local={k:np.asarray(v)[train].copy() for k,v in env.items()}
        local['_rotor_class']=rotor_classes(local)
        before=evaluate_formula(c['formula'],local)
        bad=~np.isfinite(before)
        if bad.any():
            symbols=formula_symbols(c['formula'])
            report['domain_failure']={'invalid_n':int(bad.sum()),'invalid_fraction':float(bad.mean()),
                'zero_variables_on_invalid_rows':{k:int(np.sum(local[k][bad]==0)) for k in FEATURES if k in symbols or 'q_'+k in symbols},
                'nonfinite_rule':'Every training row must have a finite feature; physical zeros are not imputed.'}
            raise ValueError('Formula undefined on observed training support; use a justified finite proxy or explicit rotor branches')
        if np.std(before)<1e-12: raise ValueError('Constant training descriptor')
        for col in reference[train].T:
            if np.std(col)>1e-12 and abs(float(np.corrcoef(before,col)[0,1]))>=.999:
                raise ValueError('Redundant with a current input')
        t=c['scientific_test'];axis=local[t['regime_input']]
        lo,hi=np.quantile(axis,t['regime_train_quantiles']);mask=(axis>=lo)&(axis<=hi)
        if mask.sum()<64: raise ValueError('Insufficient cases in declared regime')
        vals=local[t['vary_input']];step=max(float(np.quantile(vals,.9)-np.quantile(vals,.1))*.01,1e-8)
        plus={k:v.copy() for k,v in local.items()}
        plus[t['vary_input']]=vals+step
        plus['q_'+t['vary_input']]=plus[t['vary_input']]/plus[t['vary_input']+'_ref']
        after=evaluate_formula(c['formula'],plus)
        if not np.isfinite(after[mask]).all(): raise ValueError('Perturbed proxy undefined in declared regime')
        delta=after[mask]-before[mask];sign=1 if t['descriptor_direction']=='increasing' else -1
        tol=1e-10*max(1.,float(np.std(before[mask])))
        if np.any(sign*delta < -tol) or np.mean(sign*delta > tol)<.5:
            report['direction_failure']={'opposite_n':int(np.sum(sign*delta < -tol)),'nonzero_fraction':float(np.mean(sign*delta > tol))}
            raise ValueError('Formula contradicts its predeclared proxy direction')
        rho=float(spearmanr(before[mask],np.asarray(entropy)[train][mask]).statistic)
        expected=1 if t['entropy_direction']=='increasing' else -1
        assoc='inconclusive' if not np.isfinite(rho) or abs(rho)<.05 else ('consistent' if expected*rho>0 else 'contradicted')
        report.update(status='passed',scientific_check={'regime_n':int(mask.sum()),'native_regime_bounds':[float(lo),float(hi)],
            'training_spearman':rho if np.isfinite(rho) else None,'target_association':assoc,'perturbation':step,
            'mechanism_validated':False,'rotor_class_fixed_during_partial_derivative':True})
    except (ValueError,SyntaxError,OverflowError,FloatingPointError,TypeError) as e:
        report['reason']=str(e)
    return report


def checked_values(formula,env):
    values=evaluate_formula(formula,env)
    if not np.isfinite(values).all():
        # No post-score/test repair or imputation. Preserve this technical failure.
        raise ValueError('Feature not finite during frozen transformation; do not reselect using heldout diagnostics')
    return values


def compact_history(rounds):
    return [{'round':r['round'],'after_mae_R':r['after_mae_R'],
             'candidates':[{**{k:c[k] for k in ('slot_id','name','formula','status','retained','marginal_improvement','reason') if k in c},
                            'training_diagnostics':{k:v for k,v in c.get('precheck',{}).items() if k in ('domain_failure','direction_failure','scientific_check')}}
                            for c in r['candidates']]} for r in rounds]


def scientific_graph(bank):
    """Shared quantities connect qualified observations to executable input rules."""
    nodes={k:{'id':k,'type':'measured_proxy','role':ROLES[k],'definition':INPUTS[k]} for k in FEATURES}
    edges=[]
    for row in bank['kg']:
        mid=row['mechanism_id'];nodes[mid]={'id':mid,'type':'conditional_mechanism','source_conditions':row['applicability']['source_conditions']}
        for k in row['applicability']['proxy_inputs']:
            edges.append({'from':mid,'to':k,'type':'MAY_USE_PROXY_UNDER_ASSUMPTIONS',
                          'assumptions':row['applicability']['transfer_assumptions'],'caveat':row['applicability']['proxy_caveat'],
                          'source_record_id':row['record_id']})
    # Definitions and computational rules are explicitly distinguished from observations.
    rules=[{'id':'rotor_domains','inputs':['PMI1','PMI2','PMI3'],'rule':'Separate native single-site, linear and nonlinear proxies; nonlinear rotor logs need rotor_case.', 'origin':'native representation plus training support'},
           {'id':'diameter_roles','inputs':['lsd_f','lsd_p'],'rule':'Df is passing bottleneck; Dif is included along path; neither is global Di.', 'origin':'native descriptor definition'},
           {'id':'probe_volume','inputs':['AV','Vol'],'rule':'AV is mass-specific fixed-probe accessibility; AV=0 does not make adsorption impossible; no literal AV/Vol free-volume claim.', 'origin':'native descriptor units and measurement'},
           {'id':'normalization','inputs':FEATURES,'rule':'q_X = X/X_ref; X_ref is a fixed positive training reference. X/q_X equals the constant X_ref where X>0 and is undefined at X=0. Do not use q_X as X_ref. q-ratio=1 is not native equality.', 'origin':'normalization algebra'}]
    for rule in rules:
        nodes[rule['id']]={'id':rule['id'],'type':'definition_constraint','rule':rule['rule'],'origin':rule['origin']}
        for k in rule['inputs']: edges.append({'from':k,'to':rule['id'],'type':'REQUIRES_DEFINITION_CHECK'})
    return {'nodes':nodes,'edges':edges,'rules':rules,'causality':'No causal edges inferred from co-occurrence or MAE.'}


def graph_paths_for(candidates,graph):
    used=set().union(*(ground_symbols(c.get('formula','')) for c in candidates))
    relevant=[e for e in graph['edges'] if e['to'] in used or (e['from'] in used and e['type']=='REQUIRES_DEFINITION_CHECK')]
    ids={e[k] for e in relevant for k in ('from','to')}
    # Source conditions/assumptions already occur once in the evidence registry.
    # The graph supplies links, not a second serialized copy of those paragraphs.
    nodes={}
    for k in sorted(ids):
        n=graph['nodes'][k]
        if k in FEATURES: n={'id':k,'type':'measured_proxy','definition_ref':'inputs.'+k}
        elif n['type']=='conditional_mechanism': n={'id':k,'type':n['type'],'conditions_ref':'evidence.mechanism_cards.'+k+'.applicability_ref'}
        nodes[k]=n
    edges=[{k:v for k,v in e.items() if k not in ('assumptions','caveat')} for e in relevant]
    return {'nodes':nodes,'edges':edges,
            'executed_checks':['quantity-role mapping','global training feature domain','rotor branches','proxy partial derivative'],
            'note':'Paths connect a qualified source mechanism to a shared proxy and its definition constraints.'}


def pack_evidence(evidence):
    """Intern identical applicability objects; complete quotes occur once."""
    result=deepcopy(evidence);conditions={};lookup={}
    for row in result['items']+result['mechanism_cards']:
        value=row.pop('applicability',{})
        # Per-record identifiers do not alter scientific source conditions.
        value={k:v for k,v in value.items() if k not in ('record_id','paper_id','decision','reason')}
        key=json.dumps(value,ensure_ascii=False,sort_keys=True)
        if key not in lookup:
            ref='C'+str(len(lookup)+1);lookup[key]=ref;conditions[ref]=value
        row['applicability_ref']=lookup[key]
    result['source_conditions']=conditions
    return result


def ground_symbols(formula):
    try: symbols=formula_symbols(formula)
    except SyntaxError: return set()
    return {k for k in FEATURES if k in symbols or 'q_'+k in symbols}


class FullIndexEvidence:
    """Search complete indexed paragraphs inside the reviewed identity boundary.

    Unknown papers are logged as pending review, never promoted to mechanism law.
    No embeddings/API or repeated hash scans are needed for the lexical search.
    """
    def __init__(self,index,bank):
        self.index=Path(index);self.bank=bank;self.rows=[]
        papers=[json.loads(x) for x in (self.index/'papers.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
        documents=[json.loads(x) for x in (self.index/'documents.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
        excluded,docs=exclusion_closure(papers,documents)
        self.excluded=set(excluded)|set(bank['source_audit']['excluded_paper_ids'])
        self.excluded_docs=set(docs)|set(bank['source_audit']['excluded_document_ids'])
        self.reviewed={r['paper_id']:r['applicability'] for r in bank['rag']}
        for name in ['chunks.jsonl','evidence_records.jsonl']:
            with (self.index/name).open(encoding='utf-8') as f:
                for line in f:
                    if not line.strip(): continue
                    row=json.loads(line);paper=str(row.get('paper_id',''))
                    if paper in self.excluded or row.get('document_id') in self.excluded_docs or contamination_reason(row): continue
                    quote=complete_quote(row.get('text') or row.get('quote') or '')
                    if not relevance(quote)[0]: continue
                    self.rows.append({'record_id':row['record_id'],'paper_id':paper,'document_id':row.get('document_id'),
                        'quote':quote,'locator':{'section':row.get('section'),'page':row.get('page_start')},
                        'applicability':deepcopy(self.reviewed.get(paper,{})),
                        '_terms':set(re.findall(r'[a-z]{3,}',quote.lower()))})

    def search(self,query):
        terms=set(re.findall(r'[a-z]{3,}',query.lower()))
        ranked=sorted(self.rows,key=lambda r:(-len(terms&r['_terms']),r['record_id']))
        accepted=[{k:v for k,v in r.items() if k!='_terms'} for r in ranked if r['paper_id'] in self.reviewed]
        pending=[{'record_id':r['record_id'],'paper_id':r['paper_id'],'reason':'source identity/application not reviewed'}
                 for r in ranked[:30] if r['paper_id'] not in self.reviewed]
        return accepted,{'full_index_rows_in_task_scope':len(self.rows),'pending_source_review':pending,
                         'identity_boundary':'Reviewed source papers; new passages retain full conditions and conditional transfer status.'}


def select_evidence(bank, candidates, history, config, live=None):
    query='adsorption entropy confinement '+' '.join(c.get('hypothesis','')+' '+c.get('formula','') for c in candidates)
    if history: query+=' '+' '.join(c.get('reason','') for c in history[-1]['candidates'])
    terms=set(re.findall(r'[a-z]{3,}',query.lower()))
    rows=deepcopy(bank['rag']);trace={'mode':'frozen_bank_fallback'}
    if live:
        fresh,trace=live.search(query[:2400]);rows+=fresh;trace['mode']='live_full_index_reviewed_identity_search'
    rows.sort(key=lambda r:(-len(terms&set(re.findall(r'[a-z]{3,}',r['quote'].lower()))),r['record_id']))
    # Required mechanism source paragraphs are anchors available to BOTH text/KG.
    anchors=[]
    for row in bank['kg']:
        anchors.append({'record_id':row['record_id'],'paper_id':row['paper_id'],'document_id':row['document_id'],
                        'quote':row['quote'],'locator':row['locator'],'applicability':row['applicability']})
    chosen=[];seen=set();counts=Counter();rb=config['retrieval']
    for row in anchors+rows:
        key=(row['paper_id'],row['document_id'],row['quote'])
        if key in seen: continue
        if row not in anchors and counts[row['paper_id']]>=rb['max_items_per_paper']: continue
        item={k:deepcopy(row.get(k)) for k in ('record_id','paper_id','document_id','quote','locator','applicability')}
        item['id']='E'+str(len(chosen)+1).zfill(2)
        if token_count(chosen+[item])>rb['context_lexical_tokens']: continue
        assert_clean(item,bank['source_audit']['excluded_paper_ids'],bank['source_audit']['excluded_document_ids'])
        chosen.append(item);seen.add(key);counts[row['paper_id']]+=1
        if len(chosen)>=rb['max_items']: break
    if not chosen: raise ValueError('No clean reviewed evidence selected')
    # Quote text is stored once. Cards refer to that evidence instead of repeating it.
    cards=[]
    for row in bank['kg']:
        eid=next((x['id'] for x in chosen if x['paper_id']==row['paper_id'] and row['quote']==x['quote']),None)
        if eid:
            cards.append({'mechanism_id':row['mechanism_id'],'evidence_id':eid,'applicability':row['applicability'],
                          'relation':row['graph_paths'][0]['edges'][0]['relation'],
                          'subject':row['graph_paths'][0]['nodes'][0]['label'],'object':row['graph_paths'][0]['nodes'][1]['label']})
    trace.update(query=query[:2400],selected_records=[x['record_id'] for x in chosen],
                 items=len(chosen),lexical_tokens=token_count(chosen),unique_source_papers=len(counts),
                 mechanism_cards=len(cards),all_source_paragraphs_complete=True,quotes_serialized_once=True)
    return {'items':chosen,'mechanism_cards':cards},trace
