"""Synthesis knowledge extracted from the frozen Small KG and linked to ZeoSyn OSDAs.

The Small KG (catalysis_evidence_graph.v2) stores, per paper, experiments with the
materials they use (EXPERIMENT_USES_MATERIAL), the samples they produce or study
(EXPERIMENT_USES_SAMPLE) and free-form conditions. Entity nodes are merged across
papers and carry an extracted ``identifiers.framework_code``.

This module streams the snapshot (it never loads the graph into memory), keeps the
synthesis experiments that name a product framework, and links their organic
reagents to ZeoSyn OSDAs by chemical structure. Nothing here reads ZeoSyn labels.
"""
from __future__ import annotations

import ast
import gzip
import json
import re
import io
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

SCHEMA = 'zeosyn_kg_synthesis.v1'
SYNTHESIS_TYPE = re.compile(
    r'synth|hydrothermal|crystalli|prepar|interzeolite|transformation|dry[ _-]?gel|steam[ _-]?assist|'
    r'solvothermal|ionothermal|seed|recrystal', re.I)
FLUORIDE = re.compile(r'\bHF\b|NH4F|NH₄F|fluorid|\bF-\b|F⁻|hydrofluoric', re.I)
HETEROATOMS = {
    'Ge': re.compile(r'\bGe\b|germani|GeO', re.I), 'B': re.compile(r'\bboric|\bboron|H3BO3|\bB2O3', re.I),
    'Ti': re.compile(r'\bTi\b|titan|TBOT|TEOT', re.I), 'Sn': re.compile(r'\bSn\b|\btin\b|stann', re.I),
    'Ga': re.compile(r'\bGa\b|gallium', re.I), 'Zn': re.compile(r'\bZn\b|zinc', re.I),
    'P': re.compile(r'phosphoric|H3PO4|\bP2O5', re.I),
}
# Words that describe the form of a reagent rather than its identity.
_FORM_WORDS = re.compile(
    r'\b(hydroxide|bromide|chloride|iodide|fluoride|salts?|solution|aqueous|aq|cations?|dications?|ions?|'
    r'template|structure[- ]directing agents?|organic|o?sda[- ]?\w*|wt ?%|\d+ ?wt|\d+ ?%)\b', re.I)


def _rows(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt', encoding='utf-8') as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def letters_key(code):
    return re.sub(r'[^A-Z]', '', str(code or '').upper())


def framework_canonicalizer(iza_codes):
    """Map KG codes (BEA, *BEA, -SVR) onto IZA spelling; anything that is not an IZA framework code
    (e.g. material families such as SAPO or ALPO stored as a code) is dropped."""
    table = {letters_key(c): c for c in iza_codes}

    def canonical(code):
        return table.get(letters_key(code))
    return canonical


def _to_celsius(value, unit):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    u = str(unit or '').strip().lower()
    if u in ('k', 'kelvin'):
        v -= 273.15
    elif u not in ('°c', 'c', '℃', 'degc', 'oc'):
        return None
    return v if 20 <= v <= 400 else None


def _to_hours(value, unit):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    u = str(unit or '').strip().lower()
    scale = {'h': 1, 'hr': 1, 'hrs': 1, 'hour': 1, 'hours': 1, 'd': 24, 'day': 24, 'days': 24,
             'min': 1 / 60, 'mins': 1 / 60, 'minutes': 1 / 60, 'week': 168, 'weeks': 168}.get(u)
    return v * scale if scale and 0 < v * scale <= 24 * 365 else None


def stream_synthesis_records(kg_dir, *, canonical_code):
    """Return (records, reagent_entities, paper_meta, material_name_to_framework) from one pass over
    nodes and one over edges."""
    kg_dir = Path(kg_dir)
    papers = {}
    for p in _rows(kg_dir / 'papers.jsonl'):
        papers[str(p['paper_id'])] = {'doi': (p.get('doi') or '').strip().lower() or None,
                                      'year': p.get('year') if isinstance(p.get('year'), int) else None}
    entities, experiments = {}, {}
    for n in _rows(kg_dir / 'nodes.jsonl.gz'):
        t = n['node_type']
        if t == 'entity':
            d = n.get('data') or {}
            names = [n.get('canonical_name') or d.get('canonical_name') or '']
            names += [a for a in (d.get('aliases') or []) if isinstance(a, str)]
            entities[n['id']] = {
                'type': d.get('type'), 'names': [x for x in dict.fromkeys(names) if x],
                'code': canonical_code((d.get('identifiers') or {}).get('framework_code')),
                'si_al': (d.get('attributes') or {}).get('si_al_ratio'),
            }
        elif t == 'experiment':
            d = n.get('data') or {}
            etype = (d.get('experiment_type') or '').strip()
            temps, hours, text = [], [], [etype, d.get('objective') or '', n.get('label') or '']
            for c in d.get('conditions') or []:
                name = str(c.get('name') or '').lower()
                if name == 'temperature':
                    temps.append(_to_celsius(c.get('value'), c.get('unit')))
                elif name == 'time':
                    hours.append(_to_hours(c.get('value'), c.get('unit')))
                text.append(str(c.get('raw_value') or ''))
            experiments[n['id']] = {'type': etype, 'objective': str(d.get('objective') or ''),
                                    'temps': [x for x in temps if x is not None],
                                    'hours': [x for x in hours if x is not None], 'text': ' '.join(text)}
    materials, samples, exp_paper = defaultdict(list), defaultdict(list), {}
    for e in _rows(kg_dir / 'edges.jsonl.gz'):
        et = e.get('edge_type')
        if et not in ('EXPERIMENT_USES_MATERIAL', 'EXPERIMENT_USES_SAMPLE'):
            continue
        src, dst = e['from_node_id'], e['to_node_id']
        if src not in experiments or dst not in entities:
            continue
        (materials if et == 'EXPERIMENT_USES_MATERIAL' else samples)[src].append(dst)
        if e.get('source_paper_id'):
            exp_paper.setdefault(src, str(e['source_paper_id']))
    records, reagents, framework_names = [], {}, defaultdict(Counter)
    for gid, x in experiments.items():
        paper = exp_paper.get(gid)
        products = sorted({entities[s]['code'] for s in samples.get(gid, []) if entities[s]['code']})
        # A synthesis experiment by its type, or by an objective that starts with making the material.
        is_synthesis = SYNTHESIS_TYPE.search(x['type']) or re.match(r'\s*(synthes|prepar|crystalliz)', x['objective'], re.I)
        if not paper or not products or not is_synthesis:
            continue
        mats = [m for m in dict.fromkeys(materials.get(gid, [])) if entities[m]['type'] == 'synthesis_reagent']
        material_text = ' '.join(n for m in materials.get(gid, []) for n in entities[m]['names'])
        full_text = x['text'] + ' ' + material_text
        for m in mats:
            reagents[m] = entities[m]['names']
        for smp in samples.get(gid, []):
            if entities[smp]['code']:
                for nm in entities[smp]['names']:
                    framework_names[nm][entities[smp]['code']] += 1
        si_al = [float(entities[s]['si_al']) for s in samples.get(gid, [])
                 if isinstance(entities[s]['si_al'], (int, float)) and 0 < entities[s]['si_al'] < 1e5]
        records.append({
            'experiment': gid, 'paper_id': paper, 'doi': papers.get(paper, {}).get('doi'),
            'year': papers.get(paper, {}).get('year'), 'experiment_type': x['type'],
            'reagents': mats, 'products': products,
            'temperature_c': (sorted(x['temps'])[len(x['temps']) // 2] if x['temps'] else None),
            'time_h': (sorted(x['hours'])[len(x['hours']) // 2] if x['hours'] else None),
            'fluoride': bool(FLUORIDE.search(full_text)),
            'heteroatoms': sorted(k for k, rx in HETEROATOMS.items() if rx.search(full_text)),
            'product_si_al': (sorted(si_al)[len(si_al) // 2] if si_al else None),
        })
    records.sort(key=lambda r: r['experiment'])
    # A material name maps to a framework only when the KG is unanimous about it.
    names = {n: next(iter(c)) for n, c in framework_names.items() if len(c) == 1 and 3 <= len(n) <= 40}
    return records, reagents, papers, names


# ---------------------------------------------------------------- OSDA identity

def canonical_osda(smiles):
    """OSDA identity: standard InChIKey of the largest organic fragment, uncharged where possible, without stereo.

    InChI merges resonance forms (imidazolium charge drawn on either nitrogen) and protonation states,
    which canonical SMILES does not; ZeoSyn and OPSIN often draw the same ion differently.
    """
    from rdkit import Chem, RDLogger
    from rdkit.Chem.MolStandardize import rdMolStandardize
    RDLogger.DisableLog('rdApp.*')
    if not isinstance(smiles, str) or not smiles.strip():
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    frags = [f for f in Chem.GetMolFrags(mol, asMols=True) if any(a.GetSymbol() == 'C' for a in f.GetAtoms())]
    if not frags:
        return None
    mol = max(frags, key=lambda f: (f.GetNumHeavyAtoms(), Chem.MolToSmiles(f)))
    mol = rdMolStandardize.Uncharger().uncharge(mol)
    Chem.RemoveStereochemistry(mol)  # ZeoSyn SMILES rarely carry stereo; KG names often do (cis/trans, R/S)
    key = Chem.MolToInchiKey(mol)
    return key or None


def normalize_name(name):
    text = str(name or '').lower()
    text = text.replace('⁺', '+').replace('⁻', '-').replace('ʹ', "'").replace('′', "'")
    text = re.sub(r'\(\s*\+\s*\)|\+|\(\s*2\+\s*\)', ' ', text)
    text = _FORM_WORDS.sub(' ', text)
    return re.sub(r'[^a-z0-9]', '', text)


def name_variants(name):
    """The name, its trailing " (alias)" groups, and the name without them.

    Only a parenthetical separated by whitespace at the END of the name is an alias
    ("tetrapropylammonium hydroxide (TPAOH)"); parentheses inside a chemical name are
    nomenclature ("1,4-bis(N-methylpyrrolidinium)butane") and are never split off.
    Slash-separated mixtures ("TEAOH/Cu-TEPA") give one candidate per part.
    """
    out = []
    for part in [name] + ([x for x in name.split('/') if x.strip()] if '/' in name else []):
        rest, aliases = part.strip(), []
        while True:
            m = re.match(r'^(.*\S)\s+\(([^()]+)\)\s*$', rest)
            if not m:
                break
            rest, aliases = m.group(1), [m.group(2)] + aliases
        out += [part.strip(), rest] + aliases
    cleaned = []
    for v in out:
        v = re.sub(r'\s+', ' ', _FORM_WORDS.sub(' ', v)).strip(' ,;:-')
        if len(v) >= 2 and not re.fullmatch(r'[\d\s.,%-]+', v):
            cleaned.append(v)
    return list(dict.fromkeys(cleaned))


_ID_LIKE = re.compile(r'^(\d[\d-]+\d|nsc ?\d+|zinc\d+|chebi:\d+|inchi=.*|brn \d+|einecs .*|ccris .*|hsdb .*|ai3-.*|'
                      r'.*_(aldrich|sigma|fluka|riedel|sial)|ncgc.*|mls\d+|smr\d+|oprea.*|cbdive.*)$', re.I)


def zeosyn_osda_aliases(zeosyn_xlsx):
    """normalized alias -> canonical OSDA key, from osda{1,2,3}, IUPAC names and synonyms."""
    import pandas as pd
    cols = [f'osda{i}{s}' for i in (1, 2, 3) for s in ('', ' iupac', ' synonyms', ' smiles')]
    df = pd.read_excel(zeosyn_xlsx, usecols=cols)
    aliases, keys = {}, {}
    for i in (1, 2, 3):
        for row in df[[f'osda{i}', f'osda{i} iupac', f'osda{i} synonyms', f'osda{i} smiles']].dropna(
                subset=[f'osda{i} smiles']).drop_duplicates(f'osda{i} smiles').itertuples(index=False):
            name, iupac, syn, smiles = row
            key = keys.setdefault(smiles, canonical_osda(smiles))
            if not key:
                continue
            names = [(name, 4), (iupac, 4)]
            if isinstance(syn, str) and syn.startswith('['):
                try:
                    names += [(x, 6) for x in ast.literal_eval(syn)]
                except (ValueError, SyntaxError):
                    pass
            for n, min_len in names:
                if isinstance(n, str) and n.strip() and not _ID_LIKE.match(n.strip()):
                    norm = normalize_name(n)
                    if len(norm) >= min_len:
                        aliases.setdefault(norm, set()).add(key)
    # Ambiguous aliases (pointing to several structures) are dropped.
    return {a: next(iter(k)) for a, k in aliases.items() if len(k) == 1}, {s: k for s, k in keys.items() if k}


class PubChemThrottled(RuntimeError):
    """PubChem kept refusing requests (HTTP 429/503); rerun later, the cache keeps finished names."""


class PubChemResolver:
    """Name -> SMILES through PubChem PUG REST, cached on disk so the result is frozen and reusable.

    PubChem asks for at most 5 requests/s and throttles with HTTP 429/503; this client sends one
    request per ``min_interval`` seconds, backs off for minutes on throttling, and stops with
    PubChemThrottled after ``max_consecutive_failures`` so a later run can resume from the cache.
    Only definitive answers (a structure, or 404 "no such name") are cached.
    """

    URL = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/property/ConnectivitySMILES/JSON'

    def __init__(self, cache_path, *, min_interval=1.0, timeout=30, backoff=(30, 60, 120),
                 max_consecutive_failures=5, offline=False):
        self.cache_path = Path(cache_path)
        self.cache = json.loads(self.cache_path.read_text()) if self.cache_path.exists() else {}
        self.min_interval, self.timeout, self.backoff = min_interval, timeout, backoff
        self.max_consecutive_failures, self.offline = max_consecutive_failures, offline
        self._last, self._failures, self.calls = 0.0, 0, 0

    def resolve(self, name):
        if name in self.cache:
            return self.cache[name]
        if self.offline:
            return None
        url = self.URL.format(urllib.parse.quote(name, safe=''))
        for wait in (0, *self.backoff):
            time.sleep(max(wait, self.min_interval - (time.time() - self._last)))
            self._last = time.time()
            self.calls += 1
            try:
                with urllib.request.urlopen(url, timeout=self.timeout) as r:
                    props = json.loads(r.read().decode())['PropertyTable']['Properties']
                smiles = props[0].get('ConnectivitySMILES') or props[0].get('CanonicalSMILES')
            except urllib.error.HTTPError as e:
                if e.code in (400, 404):
                    smiles = None
                else:
                    continue
            except (urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError):
                continue
            self._failures = 0
            self.cache[name] = smiles
            return smiles
        self._failures += 1
        if self._failures >= self.max_consecutive_failures:
            self.save()
            raise PubChemThrottled(f'{self._failures} consecutive names failed; resume later')
        return None

    def save(self):
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(dict(sorted(self.cache.items())), indent=0, ensure_ascii=False) + '\n')


_ORGANIC_HINT = re.compile(r'ammon|amin|azan|azoni|pyrid|piperid|pyrrolid|imidazol|quinuclid|adamant|phosphon|'
                           r'choline|morpholin|azepan|imine|spart|bicyclo|\b[A-Z][A-Za-z]{1,8}(OH|Br|Cl|I|F)?[+⁺]?\b')

# Common OSDA abbreviations in the zeolite literature (curated; applied only to a bare abbreviation,
# with OH/Br/Cl/I suffixes and charges stripped). Expanded names are then matched like any other name.
ABBREVIATIONS = {
    'TPA': 'tetrapropylammonium', 'TPRA': 'tetrapropylammonium', 'TEA': 'tetraethylammonium',
    'TMA': 'tetramethylammonium', 'TBA': 'tetrabutylammonium', 'TMADA': 'N,N,N-trimethyl-1-adamantylammonium',
    'TMAD': 'N,N,N-trimethyl-1-adamantylammonium', 'HMI': 'hexamethyleneimine', 'DPA': 'dipropylamine',
    'DEA': 'diethylamine', 'TEPA': 'tetraethylenepentamine', 'TETA': 'triethylenetetramine',
    'DETA': 'diethylenetriamine', 'EDA': 'ethylenediamine', 'CTA': 'cetyltrimethylammonium',
    'CTAB': 'cetyltrimethylammonium', 'CTAC': 'cetyltrimethylammonium', 'BTMA': 'benzyltrimethylammonium',
    'BTEA': 'benzyltriethylammonium', 'DABCO': '1,4-diazabicyclo[2.2.2]octane', 'HM': 'hexamethonium',
    'DMDMP': 'N,N-dimethyl-3,5-dimethylpiperidinium', 'BMIM': '1-butyl-3-methylimidazolium',
    'EMIM': '1-ethyl-3-methylimidazolium', 'TBP': 'tetrabutylphosphonium', 'TEAH': 'tetraethylammonium',
    'TPAH': 'tetrapropylammonium', 'MEA': 'monoethanolamine', 'TREN': 'tris(2-aminoethyl)amine',
}


# Ambiguous without a counter-ion/charge (TEA: triethylamine or tetraethylammonium; DEA: diethylamine or
# diethanolamine; TMA: trimethylamine or tetramethylammonium): expanded only as quaternary salts (TEAOH, TEA+).
AMBIGUOUS_UNLESS_SALT = {'TEA', 'DEA', 'TMA'}


def abbreviation_expansion(name):
    raw = re.sub(r'\s', '', str(name))
    tok = re.sub(r'[⁺+]', '', raw)
    if not re.fullmatch(r'[A-Za-z]{2,8}', tok):
        return None
    if tok.upper() in ABBREVIATIONS and tok.upper() not in AMBIGUOUS_UNLESS_SALT:
        return ABBREVIATIONS[tok.upper()]
    stripped = re.sub(r'(OH|Br|Cl)$', '', tok)
    salt = stripped != tok or raw != tok
    if stripped.upper() in AMBIGUOUS_UNLESS_SALT and not salt:
        return None
    return ABBREVIATIONS.get(stripped.upper()) if len(stripped) >= 2 else None


_ALLOWED_ELEMENTS = {'C', 'H', 'N', 'O', 'P', 'S', 'F', 'Cl', 'Br', 'I', 'Si', 'B'}


def structure_is_single_organic(smiles):
    """A structure link is accepted only for one organic component without metals (counter-ions allowed)."""
    from rdkit import Chem, RDLogger
    RDLogger.DisableLog('rdApp.*')
    mol = Chem.MolFromSmiles(smiles) if smiles else None
    if mol is None or any(a.GetSymbol() not in _ALLOWED_ELEMENTS for a in mol.GetAtoms()):
        return False
    organic = [f for f in Chem.GetMolFrags(mol, asMols=True) if any(a.GetSymbol() == 'C' for a in f.GetAtoms())]
    return len(organic) == 1 and organic[0].GetNumHeavyAtoms() >= 2


def structure_lookup_allowed(name, resolver_label):
    """No structure lookup for polymers or metal complexes; PubChem only for full names, not abbreviations."""
    if re.search(r'poly|polymer|\[.*(Co|Ni|Cu|Rh|Pd|Pt|Au|Fe|Zn|Mn|Cr)\b', name, re.I):
        return False
    if resolver_label == 'pubchem' and (len(name) < 8 or not re.search(r'[a-z]{4}', name)):
        return False
    return True


class OpsinResolver:
    """Offline IUPAC-name -> SMILES with OPSIN (Java), batched, cached on disk with the OPSIN version."""

    def __init__(self, cache_path, *, jar=None, java=None, version='2.8.0'):
        self.cache_path, self.jar, self.java, self.version = Path(cache_path), jar, java, version
        data = json.loads(self.cache_path.read_text()) if self.cache_path.exists() else {}
        if data and data.get('opsin_version') != version:
            raise ValueError(f'OPSIN cache was built with {data.get("opsin_version")}, not {version}')
        self.cache = data.get('names', {})

    def prefetch(self, names):
        todo = sorted({n for n in names if n not in self.cache})
        if not todo:
            return
        if not (self.jar and self.java):
            raise RuntimeError(f'{len(todo)} names are not in the OPSIN cache and no OPSIN jar/java was given')
        import subprocess
        out = subprocess.run([str(self.java), '-Xmx256m', '-jar', str(self.jar), '-osmi'],
                             input='\n'.join(n.replace('\n', ' ') for n in todo) + '\n',
                             capture_output=True, text=True, check=True).stdout.split('\n')
        for n, smi in zip(todo, out):
            self.cache[n] = smi.strip() or None
        self.save()

    def resolve(self, name):
        return self.cache.get(name)

    def save(self):
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps({'opsin_version': self.version,
                                               'names': dict(sorted(self.cache.items()))}, indent=0, ensure_ascii=False) + '\n')


GENERIC = re.compile(r'alkyl|\bosdas\b|\bsdas\b|\bamines\b|\btemplates\b|mixture|quaternary ammonium|'
                     r'organic cations?\b|structure[- ]directing agent\b', re.I)


def candidate_names(names):
    """Names to try for one reagent: variants and abbreviation expansions, without parent-only aliases.

    A candidate whose normalized form is a proper part of a longer candidate of the same entity
    (e.g. "imidazolium" next to "N,N-diisopropyl imidazolium") is dropped as unspecific.
    """
    out = []
    for n in names:
        for v in name_variants(n):
            out.append(v)
            exp = abbreviation_expansion(v)
            if exp:
                out.append(exp)
    out = list(dict.fromkeys(out))
    norms = {c: normalize_name(c) for c in out}
    return [c for c in out if len(norms[c]) < 4 or not any(norms[c] != o and norms[c] in o for o in norms.values())]


def _long_form(name):
    return len(name) >= 8 and re.search(r'[a-z]{4}', name) is not None


def link_reagents(reagents, aliases, *, resolvers=(), log=print):
    """entity id -> (osda key, how) for reagents that are ZeoSyn OSDAs.

    1. Generic class names (tetraalkylammonium, "cyclic amine OSDAs", ...) are never linked.
    2. Structure of record: the first long-form name that a resolver (OPSIN offline, then cached PubChem)
       parses into a single organic, metal-free structure. If it exists, the reagent links only when that
       structure equals a ZeoSyn OSDA (an abbreviation alias cannot override an explicit chemical name).
    3. Otherwise exact alias: ZeoSyn names/IUPAC/synonyms and curated abbreviation expansions.
    """
    keys = set(aliases.values())
    links, how, outcome = {}, Counter(), Counter()
    cands = {}
    for gid, names in sorted(reagents.items()):
        if names and GENERIC.search(names[0]):
            outcome['generic_name'] += 1
            continue
        cands[gid] = candidate_names(names)
    record = {}
    for label, resolver in resolvers:
        todo = [c for gid, cs in cands.items() if gid not in record for c in cs
                if _long_form(c) and structure_lookup_allowed(c, label)]
        if hasattr(resolver, 'prefetch'):
            resolver.prefetch(todo)
        for gid, cs in cands.items():
            if gid in record:
                continue
            for c in cs:
                if not (_long_form(c) and structure_lookup_allowed(c, label)):
                    continue
                smi = resolver.resolve(c)
                if smi and structure_is_single_organic(smi):
                    record[gid] = (canonical_osda(smi), label)
                    break
    for gid, cs in cands.items():
        if gid in record:
            k, label = record[gid]
            if k in keys:
                links[gid] = (k, label)
                how[label] += 1
            else:
                outcome['structure_not_a_zeosyn_osda'] += 1
            continue
        k = next((aliases[normalize_name(c)] for c in cs if normalize_name(c) in aliases), None)
        if k:
            links[gid] = (k, 'alias')
            how['alias'] += 1
        else:
            outcome['unlinked'] += 1
    log(f'  linked {len(links)} {dict(how)}; not linked {dict(outcome)}')
    return links, how


def write_jsonl_gz(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # mtime=0 and a fixed filename keep the archive byte-identical across rebuilds.
    with open(path, 'wb') as raw, gzip.GzipFile(filename='', fileobj=raw, mode='wb', compresslevel=9, mtime=0) as gz, \
            io.TextIOWrapper(gz, encoding='utf-8') as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n')


def read_jsonl_gz(path):
    return list(_rows(path))
