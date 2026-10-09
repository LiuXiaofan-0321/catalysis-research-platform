"""Readable, aggregated KG facts for a model-written query (replaces V1's hash-path quotes).

The engine links the query to OSDAs, frameworks and synthesis conditions, then states what the
KG synthesis experiments report about them, with counts of experiments and papers. Facts are
built only from experiments whose paper is not excluded (evaluation papers are removed first).
A "flat" rendering of the same matched experiments (one sentence per experiment, no
aggregation) is available as the same-facts control.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict

from .kg_features import PORE_CLASSES
from .kg_synthesis import HETEROATOMS, name_variants, normalize_name
from .retrieval.bundle import count_tokens

CONDITION_PATTERNS = {
    'fluoride medium': re.compile(r'fluorid|\bHF\b|NH4F|\bF-|\bF⁻|\bF/', re.I),
    'germanium in the gel': re.compile(r'germani|\bGe\b|GeO2', re.I),
    'boron in the gel': re.compile(r'\bboron|\bborosilicate|\bB\b|H3BO3', re.I),
    'titanium in the gel': re.compile(r'titan|\bTi\b', re.I),
    'tin in the gel': re.compile(r'\btin\b|\bSn\b|stann', re.I),
    'gallium in the gel': re.compile(r'gallium|\bGa\b', re.I),
    'zinc in the gel': re.compile(r'\bzinc\b|\bZn\b', re.I),
    'phosphorus (AlPO/SAPO) gel': re.compile(r'phosph|\bAlPO|\bSAPO|\bP\b', re.I),
    'high temperature (>=170 C)': re.compile(r'high[- ]temperature|elevated temperature|temperature', re.I),
}
_HETERO_FOR_CONDITION = {'germanium in the gel': 'Ge', 'boron in the gel': 'B', 'titanium in the gel': 'Ti',
                         'tin in the gel': 'Sn', 'gallium in the gel': 'Ga', 'zinc in the gel': 'Zn',
                         'phosphorus (AlPO/SAPO) gel': 'P'}
assert set(_HETERO_FOR_CONDITION.values()) <= set(HETEROATOMS)


def _pct(c, total):
    return f'{100 * c / total:.0f}%'


class KgFactEngine:
    def __init__(self, *, records, links, reagent_names, osda_display, excluded_dois=frozenset(),
                 framework_names=None, link_override=None):
        """records: KG synthesis records; links: entity id -> (osda key, how); reagent_names: entity id -> names;
        osda_display: osda key -> readable name; framework_names: material name -> framework code (from KG entities);
        link_override: (experiment id, entity id) -> (osda key, how), used by the shuffled control."""
        excluded = frozenset(d for d in excluded_dois if d)
        self.records = [r for r in records if not (r.get('doi') and r['doi'] in excluded)]
        self.osda_display = osda_display
        self.by_osda, self.by_framework, self.by_condition = defaultdict(list), defaultdict(list), defaultdict(list)
        self.osda_terms = defaultdict(set)
        for r in self.records:
            keys = set()
            for m in r['reagents']:
                link = (link_override or {}).get((r['experiment'], m)) if link_override else links.get(m)
                if link:
                    keys.add(link[0])
            r = {**r, 'osdas': sorted(keys)}
            for k in keys:
                self.by_osda[k].append(r)
            for p in r['products']:
                self.by_framework[p].append(r)
            if r['fluoride']:
                self.by_condition['fluoride medium'].append(r)
            for cond, het in _HETERO_FOR_CONDITION.items():
                if het in r['heteroatoms']:
                    self.by_condition[cond].append(r)
            if r.get('temperature_c') is not None and r['temperature_c'] >= 170:
                self.by_condition['high temperature (>=170 C)'].append(r)
        # Names that identify an OSDA in a query: ZeoSyn-side display name plus linked KG reagent names.
        for m, (k, _) in links.items():
            for n in reagent_names.get(m, []):
                for term in _query_terms(n):
                    self.osda_terms[k].add(term)
        for k, name in osda_display.items():
            for term in _query_terms(name):
                self.osda_terms[k].add(term)
        self.framework_names = {normalize_name(n): c for n, c in (framework_names or {}).items() if len(normalize_name(n)) >= 4}
        self.codes = set(self.by_framework)

    # ------------------------------------------------------------ query linking
    def link_query(self, query):
        norm = normalize_name(query)
        tokens = set(re.findall(r'[\w*+-]+', query))
        osdas = {k for k, terms in self.osda_terms.items()
                 if any((len(t) >= 6 and t in norm) or (t.isupper() and t in tokens) for t in terms)}
        frameworks = {c for c in self.codes if c in tokens or c.lstrip('*-') in tokens}
        frameworks |= {c for n, c in self.framework_names.items() if n in norm and c in self.codes}
        conditions = {c for c, rx in CONDITION_PATTERNS.items() if rx.search(query) and c in self.by_condition}
        if 'high temperature (>=170 C)' in conditions and not re.search(r'high|elevated', query, re.I):
            conditions.discard('high temperature (>=170 C)')
        return sorted(osdas), sorted(frameworks), sorted(conditions)

    # ------------------------------------------------------------ aggregated facts
    def _product_summary(self, recs, k=5):
        prods = Counter(p for r in recs for p in r['products'])
        total = sum(prods.values())
        top = ', '.join(f'{p} {_pct(c, total)}' for p, c in sorted(prods.items(), key=lambda kv: (-kv[1], kv[0]))[:k])
        pores = ', '.join(f'{name}-pore {_pct(sum(c for p, c in prods.items() if p in members), total)}'
                          for name, members in PORE_CLASSES)
        return top, pores

    def osda_fact(self, key):
        recs = self.by_osda.get(key, [])
        if not recs:
            return None
        papers = len({r['paper_id'] for r in recs})
        top, pores = self._product_summary(recs)
        fl = sum(r['fluoride'] for r in recs)
        temps = sorted(r['temperature_c'] for r in recs if r.get('temperature_c') is not None)
        t = f'; median crystallization temperature {temps[len(temps) // 2]:.0f} C' if temps else ''
        return (f'OSDA "{self.osda_display.get(key, key)}" --used in--> {len(recs)} KG synthesis '
                f'experiments from {papers} papers --produced--> {top} [{pores}]; fluoride medium in {_pct(fl, len(recs))}{t}.')

    def framework_fact(self, code):
        recs = self.by_framework.get(code, [])
        if not recs:
            return None
        papers = len({r['paper_id'] for r in recs})
        osdas = Counter(k for r in recs for k in r.get('osdas', []))
        top = ', '.join(f'"{self.osda_display.get(k, k)}" ({c})' for k, c in osdas.most_common(5)) or 'none linked'
        fl = sum(r['fluoride'] for r in recs)
        het = Counter(h for r in recs for h in r['heteroatoms'])
        het_s = ', '.join(f'{h} {_pct(c, len(recs))}' for h, c in het.most_common(4)) or 'none'
        temps = sorted(r['temperature_c'] for r in recs if r.get('temperature_c') is not None)
        t = f'; median temperature {temps[len(temps) // 2]:.0f} C' if temps else ''
        return (f'Framework {code} <--produced by-- {len(recs)} KG synthesis experiments from {papers} papers; '
                f'most frequent linked OSDAs: {top}; fluoride medium in {_pct(fl, len(recs))}; '
                f'heteroatoms: {het_s}{t}.')

    def condition_fact(self, cond):
        recs = self.by_condition.get(cond, [])
        if not recs:
            return None
        papers = len({r['paper_id'] for r in recs})
        top, pores = self._product_summary(recs)
        return f'Condition "{cond}" --in--> {len(recs)} KG synthesis experiments from {papers} papers --produced--> {top} [{pores}].'

    def flat_lines(self, recs, limit):
        out = []
        for r in sorted(recs, key=lambda r: (r.get('year') or 0, r['experiment']))[:limit]:
            osdas = ', '.join(self.osda_display.get(k, k) for k in r.get('osdas', [])) or 'no linked OSDA'
            cond = []
            if r['fluoride']:
                cond.append('fluoride')
            if r['heteroatoms']:
                cond.append('+'.join(r['heteroatoms']))
            if r.get('temperature_c') is not None:
                cond.append(f'{r["temperature_c"]:.0f} C')
            out.append(f'Paper {r.get("doi") or r["paper_id"]} ({r.get("year") or "n.d."}): synthesis with {osdas}'
                       f'{" (" + ", ".join(cond) + ")" if cond else ""} gave {", ".join(r["products"])}.')
        return out

    # ------------------------------------------------------------ evidence bundle
    def evidence(self, queries, *, token_budget, flat=False):
        """Numbered fact lines for up to len(queries) queries, within a lexical-token budget."""
        items, seen, used = [], set(), 0
        per_query = []
        for q in queries:
            osdas, fws, conds = self.link_query(q)
            per_query.append({'query': q, 'osdas': osdas, 'frameworks': fws, 'conditions': conds})
            if flat:
                recs = {}
                for k in osdas:
                    recs.update({r['experiment']: r for r in self.by_osda[k]})
                for c in fws:
                    recs.update({r['experiment']: r for r in self.by_framework[c]})
                for c in conds:
                    recs.update({r['experiment']: r for r in self.by_condition[c]})
                facts = [('exp', line) for line in self.flat_lines(list(recs.values()), 40)]
            else:
                facts = [('osda:' + k, self.osda_fact(k)) for k in osdas]
                facts += [('framework:' + c, self.framework_fact(c)) for c in fws]
                facts += [('condition:' + c, self.condition_fact(c)) for c in conds]
            for key, text in facts:
                if not text or (key, text) in seen:
                    continue
                n = count_tokens(text)
                if used + n > token_budget:
                    continue
                seen.add((key, text))
                items.append({'id': len(items) + 1, 'key': key, 'text': text, 'tokens': n})
                used += n
        context = '\n'.join(f'[{i["id"]}] {i["text"]}' for i in items)
        return {'items': items, 'context': context, 'tokens': used, 'linking': per_query, 'flat': flat}


def _query_terms(name):
    """Normalized long names and upper-case abbreviations that identify an OSDA (aliases as in name_variants)."""
    out = set()
    for v in name_variants(name):
        norm = normalize_name(v)
        if len(norm) >= 6:
            out.add(norm)
        tok = re.sub(r'[⁺+]|OH$', '', v.strip())
        if re.fullmatch(r'[A-Z][A-Za-z0-9]{1,9}', tok) and sum(ch.isupper() for ch in tok) >= 2:
            out.add(tok)
    return out
