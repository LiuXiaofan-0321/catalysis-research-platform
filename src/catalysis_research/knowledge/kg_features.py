"""Literature-prior features for ZeoSyn recipes, aggregated from KG synthesis experiments.

For every recipe the features summarise what the Small KG reports for the same OSDA:
how often it was used, which frameworks it produced and under which conditions.
Leakage rules (all applied before aggregation):

* evaluation papers (held-out test, or dev-validation during development) are removed from the KG;
* each recipe ignores KG experiments from its own paper (training rows included, otherwise the
  feature is spuriously accurate during training);
* optional temporal variant: only KG papers published strictly before the recipe's paper.

The feature list is fixed in advance and does not depend on ZeoSyn labels.
"""
from __future__ import annotations

import math
import random
from collections import Counter, defaultdict

import numpy as np

# IZA pore-size classes as listed in the ZeoSyn repository (utils.py, MIT license).
SMALL_PORE = frozenset('''CHA LTA AEI LEV ANA SOD AEN GIS NON AST ERI DDR RTH MTN MRT RHO ITE AFX ITW DOH AWO RUT
MER ABW PHI LOS EDI SAV SAS MTF KFI ZON ATN AFN PAU NSI SGT JSW AFV AVL SWY UFI ETL APC RTE JBW APD CDO MWF MSO SVV
AVE IHW UOZ OWE DFT PWN AWW SFW ATT LTJ ESV THO LTN EEI POR ACO IRN CAS EAB BCT ATV SAT'''.split())
MEDIUM_PORE = frozenset('''MFI MWW TON AEL FER MTT MEL STF *MRE ITH EUO STW SZR AFO STT IMF CSV TUN CGS MFS NES STI
NAT PON LAU HEU *UOE UOS PWW ITR -SVR -LIT SFF IFW JST PTY SBN SFG RSN VSV PWO EWS RRO JRY MVY CGF ETV AHT'''.split())
LARGE_PORE = frozenset('''*BEA AFI MTW FAU MOR BEC EMT IWR ATO MAZ *STO LTL ISV IFR IWW VET ATS OFF MEI GME CON BPH
SFO MSE CAN UOV IWV SFE ITG *-ITN EZT AFY AFS AFR ASV SFS SAF SSY SBE EON IWS YFI SAO BOG USI DFO *SFV BSV CZP RWY
UWY MOZ GON SOS SSF PUN SOV SOR POS LTF SOF JSR'''.split())
XLARGE_PORE = frozenset('UTL IRR *-SVY *CTH ITT -ITV CFI -CLO VFI -IRY IFO -IFT SFH SFN -IFU ETR DON'.split())
PORE_CLASSES = (('small', SMALL_PORE), ('medium', MEDIUM_PORE), ('large', LARGE_PORE), ('xlarge', XLARGE_PORE))

# The most frequent products of KG synthesis experiments (fixed from the KG alone, not from ZeoSyn labels).
TRACKED_FRAMEWORKS = ('MFI', 'FAU', 'CHA', '*BEA', 'LTA', 'MOR', 'MWW', 'AFI', 'LTL', 'AEI', 'FER', 'SOD')

FEATURES = {
    'kg_osda_known': 'OSDA1 appears in at least one KG synthesis experiment from another paper (1/0)',
    'kg_osda_n_experiments': 'number of KG synthesis experiments using this OSDA',
    'kg_osda_n_papers': 'number of distinct papers reporting syntheses with this OSDA',
    'kg_osda_top_framework': 'framework most often obtained with this OSDA, as an index into kg_framework_vocabulary (-1 if none)',
    'kg_osda_top_share': 'fraction of this OSDA\'s reported products that are its most frequent framework',
    'kg_osda_entropy': 'Shannon entropy (bits) of the frameworks reported with this OSDA; high = promiscuous OSDA',
    'kg_osda_n_frameworks': 'number of distinct frameworks reported with this OSDA',
    **{f'kg_osda_share_{name}_pore': f'fraction of this OSDA\'s reported products that are {name}-pore frameworks'
       for name, _ in PORE_CLASSES},
    **{f'kg_osda_share_{fw.replace("*", "")}': f'fraction of this OSDA\'s reported products that are {fw}'
       for fw in TRACKED_FRAMEWORKS},
    'kg_osda_fluoride_share': 'fraction of this OSDA\'s KG syntheses that use a fluoride medium',
    'kg_osda_median_temperature_c': 'median crystallization temperature (C) reported with this OSDA (-1 if none)',
    'kg_osda_median_product_si_al': 'median product Si/Al reported with this OSDA (-1 if none)',
}
FEATURE_NAMES = tuple(FEATURES)


def osda_experiments(records, links):
    """osda key -> list of experiment summaries (one entry per linked experiment)."""
    by_osda = defaultdict(list)
    for r in records:
        keys = {links[m][0] for m in r['reagents'] if m in links}
        for k in keys:
            by_osda[k].append({'doi': r.get('doi'), 'paper_id': r['paper_id'], 'year': r.get('year'),
                               'products': r['products'], 'fluoride': r['fluoride'],
                               'temperature_c': r.get('temperature_c'), 'product_si_al': r.get('product_si_al')})
    return dict(by_osda)


def shuffled_links(records, links, *, seed):
    """Permute OSDA identities across KG experiments, keeping each OSDA's number of experiments.

    Every (experiment, OSDA) incidence keeps its experiment but receives a random OSDA drawn without
    replacement from the same multiset, so feature distributions stay realistic while the
    OSDA-to-outcome association is destroyed.
    """
    incid = [(r['experiment'], m) for r in records for m in r['reagents'] if m in links]
    keys = [links[m][0] for _, m in incid]
    random.Random(seed).shuffle(keys)
    out = {}
    for (exp, m), k in zip(incid, keys):
        out[(exp, m)] = (k, 'shuffled')
    return out


def osda_experiments_shuffled(records, links, *, seed):
    mapping = shuffled_links(records, links, seed=seed)
    by_osda = defaultdict(list)
    for r in records:
        keys = {mapping[(r['experiment'], m)][0] for m in r['reagents'] if (r['experiment'], m) in mapping}
        for k in keys:
            by_osda[k].append({'doi': r.get('doi'), 'paper_id': r['paper_id'], 'year': r.get('year'),
                               'products': r['products'], 'fluoride': r['fluoride'],
                               'temperature_c': r.get('temperature_c'), 'product_si_al': r.get('product_si_al')})
    return dict(by_osda)


def framework_vocabulary(records):
    return sorted({p for r in records for p in r['products']})


def _aggregate(exps, vocab_index):
    out = dict.fromkeys(FEATURE_NAMES, 0.0)
    out['kg_osda_top_framework'] = -1.0
    # -1 marks "no KG evidence" so every column stays finite for formulas and trees.
    out['kg_osda_median_temperature_c'] = -1.0
    out['kg_osda_median_product_si_al'] = -1.0
    if not exps:
        return out
    products = Counter(p for e in exps for p in e['products'])
    total = sum(products.values())
    top, top_n = sorted(products.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    out.update({
        'kg_osda_known': 1.0, 'kg_osda_n_experiments': float(len(exps)),
        'kg_osda_n_papers': float(len({e['paper_id'] for e in exps})),
        'kg_osda_top_framework': float(vocab_index.get(top, -1)), 'kg_osda_top_share': top_n / total,
        'kg_osda_entropy': -sum(c / total * math.log2(c / total) for c in products.values()),
        'kg_osda_n_frameworks': float(len(products)),
        'kg_osda_fluoride_share': sum(e['fluoride'] for e in exps) / len(exps),
    })
    for name, members in PORE_CLASSES:
        out[f'kg_osda_share_{name}_pore'] = sum(c for p, c in products.items() if p in members) / total
    for fw in TRACKED_FRAMEWORKS:
        out[f'kg_osda_share_{fw.replace("*", "")}'] = products.get(fw, 0) / total
    temps = sorted(e['temperature_c'] for e in exps if e['temperature_c'] is not None)
    sial = sorted(e['product_si_al'] for e in exps if e['product_si_al'] is not None)
    if temps:
        out['kg_osda_median_temperature_c'] = float(np.median(temps))
    if sial:
        out['kg_osda_median_product_si_al'] = float(np.median(sial))
    return out


def recipe_features(*, osda_keys, dois, years, by_osda, vocab, excluded_dois=frozenset(), temporal=False):
    """Feature matrix (rows x FEATURE_NAMES) for ZeoSyn recipes.

    osda_keys: canonical OSDA key per recipe (None for OSDA-free recipes); dois: normalized DOI per recipe;
    years: publication year per recipe (NaN if unknown). excluded_dois: evaluation papers removed from the KG.
    Own-paper exclusion is always applied. With ``temporal`` only KG papers with year < recipe year count;
    recipes without a year then get no KG evidence (features of an unknown OSDA).
    """
    excluded = frozenset(d for d in excluded_dois if d)
    vocab_index = {fw: i for i, fw in enumerate(vocab)}
    pool = {k: [e for e in v if not (e['doi'] and e['doi'] in excluded)] for k, v in by_osda.items()}
    cache, rows = {}, []
    for key, doi, year in zip(osda_keys, dois, years):
        year_key = (int(year) if (year is not None and year == year) else None) if temporal else None
        ck = (key, doi or None, year_key, temporal)
        if ck not in cache:
            exps = pool.get(key, []) if key else []
            exps = [e for e in exps if not (doi and e['doi'] == doi)]
            if temporal:
                exps = [e for e in exps if year_key is not None and e['year'] is not None and e['year'] < year_key]
            cache[ck] = _aggregate(exps, vocab_index)
        rows.append([cache[ck][f] for f in FEATURE_NAMES])
    return np.asarray(rows, dtype=float)


def coverage(features, rows):
    known = features[rows, FEATURE_NAMES.index('kg_osda_known')]
    return float(known.mean()) if len(rows) else 0.0


def direct_answer_audit(features, labels, rows, vocab):
    """How often the KG's top framework for the OSDA equals the recipe's label, and how often the label
    is among the frameworks the KG reports for that OSDA (requires the share columns)."""
    top = features[rows, FEATURE_NAMES.index('kg_osda_top_framework')].astype(int)
    known = features[rows, FEATURE_NAMES.index('kg_osda_known')] > 0
    y = np.asarray(labels)[rows]
    top_label = np.array([vocab[i] if i >= 0 else None for i in top], dtype=object)
    return {
        'rows': int(len(rows)), 'covered_rows': int(known.sum()),
        'top_framework_equals_label': int(((top_label == y) & known).sum()),
        'top_framework_equals_label_rate_among_covered': float(((top_label == y) & known).sum() / max(1, known.sum())),
    }
