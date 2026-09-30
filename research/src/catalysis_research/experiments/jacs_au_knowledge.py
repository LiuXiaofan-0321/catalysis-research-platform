"""Task-specific knowledge and formula checks for the JACS Au KG pilot.

All three conditions receive the same variable dictionary and formula checks.
The graph supplies extracted relations with provenance, never invented causal
edges. Search uses a frozen evidence bank and completed scoring feedback only.
"""
from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction
import html
import json
import re

import numpy as np

from .jacs_au import FEATURES, UNITS, DOI
from .jacs_au_sources import contamination_reason
from ..retrieval.bundle import count_tokens


PROFILE = "jacs-au-kg-v2"
RETRIEVAL_DEFAULTS = {
    'candidates_per_source_per_bank_query': 160,
    'candidates_per_round': 120,
    'max_items': 32,
    'max_items_per_paper': 4,
    'context_lexical_tokens': 32000,
    'kg_priority_items': 8,
}
GENERATION_DEFAULTS = {'max_tokens': 16000, 'max_tokens_on_truncation': 32000}


def load_budget_config(path=None):
    """One executable budget contract for evidence building and all three modes."""
    config = json.loads(path.read_text()) if path is not None else {}
    if config and config.get('profile') != PROFILE:
        raise ValueError('Budget configuration profile mismatch')
    retrieval = {key: config.get('retrieval', {}).get(key, default)
                 for key, default in RETRIEVAL_DEFAULTS.items()}
    generation = {key: config.get('generation', {}).get(key, default)
                  for key, default in GENERATION_DEFAULTS.items()}
    for name, value in [*retrieval.items(), *generation.items()]:
        if type(value) is not int or value <= 0:
            raise ValueError(f'Budget {name} must be a positive integer')
    if retrieval['kg_priority_items'] >= retrieval['candidates_per_round']:
        raise ValueError('KG priority must leave room for RAG candidates')
    if generation['max_tokens_on_truncation'] < generation['max_tokens']:
        raise ValueError('Truncation recovery output budget must not be smaller')
    return {'retrieval': retrieval, 'generation': generation}
DESCRIPTIONS = [
    "Molecular weight of the adsorbate.",
    "Labute approximate molecular surface area of the adsorbate.",
    "Mean atom distance from the best-fit molecular plane; measures planarity.",
    "First principal moment of inertia of the adsorbate.",
    "Second principal moment of inertia of the adsorbate.",
    "Third principal moment of inertia of the adsorbate.",
    "Radius enclosing all molecular atoms about the center of mass.",
    "Largest distance between two molecular atoms.",
    "Van der Waals volume of the adsorbate molecule.",
    "Framework density on the published numerical scale; physical unit unresolved.",
    "Framework surface area accessible to a probe, per framework mass.",
    "Framework volume accessible to a probe, per framework mass.",
    "Diameter of the largest free sphere in the framework.",
    "Diameter of the largest sphere along a free-sphere path in the framework.",
]
INPUT_SCHEMA = {name: {"unit": unit, "meaning": meaning,
                       "role": "adsorbate" if i < 9 else "framework"}
                for i, (name, unit, meaning) in enumerate(zip(FEATURES, UNITS, DESCRIPTIONS))}
# Keep native mass conventions and unresolved density distinct. Do not silently
# equate g/mol, amu, framework mass, or a disputed density scale.
DIMENSIONS = {
    "MW": {"molecular_mass_per_mole": Fraction(1)},
    "LabuteASA": {"length": Fraction(2)}, "PBF": {"length": Fraction(1)},
    **{name: {"atomic_mass": Fraction(1), "length": Fraction(2)} for name in ["PMI1", "PMI2", "PMI3"]},
    **{name: {"length": Fraction(1)} for name in ["SPAN", "GeDi", "lsd_f", "lsd_p"]},
    "Vol": {"length": Fraction(3)}, "density": {"native_density": Fraction(1)},
    "ASA": {"length": Fraction(2), "framework_mass": Fraction(-1)},
    "AV": {"length": Fraction(3), "framework_mass": Fraction(-1)},
}
QUERIES = [
    "zeolite adsorption entropy molecular confinement translational rotational freedom",
    "adsorbate molecular shape principal moments inertia rotational entropy pore confinement",
    "zeolite accessible pore volume occupiable volume molecular volume adsorption entropy",
    "zeolite cage channel free sphere pore diameter entropy loss confinement",
    "adsorption entropy molecular surface area pore surface geometric descriptors limitations",
]


def formula_environment(data, train):
    env = {name: data['x'][:, i] for i, name in enumerate(FEATURES)}
    references = {}
    for name, values in list(env.items()):
        positive = np.abs(values[train])
        positive = positive[np.isfinite(positive) & (positive > 1e-12)]
        if not len(positive):
            raise ValueError(f"No nonzero training reference for {name}")
        reference = float(np.median(positive))
        env[name + '_ref'] = np.full(len(values), reference)
        env['q_' + name] = values / reference
        references[name] = reference
    return env, references


def audit_dimensions(formula):
    """Reject mixed units and dimensional logs before spending a model fit."""
    if not isinstance(formula, str) or len(formula) > 1500: raise ValueError('Invalid formula length')
    tree = ast.parse(formula, mode='eval')
    if len(list(ast.walk(tree))) > 160: raise ValueError('Formula too complex')
    symbols = {**DIMENSIONS, **{name + '_ref': dims for name, dims in DIMENSIONS.items()},
               **{'q_' + name: {} for name in FEATURES}}
    def tidy(dims):
        return {key: value for key, value in dims.items() if value}
    def combine(a, b, sign=1):
        return tidy({key: a.get(key, Fraction(0)) + sign * b.get(key, Fraction(0))
                     for key in set(a) | set(b)})
    def compatible(a, b):
        da, za = a; db, zb = b
        if da != db and not (za or zb):
            raise ValueError("Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references")
        return db if za else da
    def visit(node):
        if isinstance(node, ast.Name) and node.id in symbols:
            return symbols[node.id], False
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if not np.isfinite(node.value): raise ValueError("Nonfinite constant")
            return {}, node.value == 0
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            return visit(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, (ast.Add, ast.Sub)): return compatible(a, b), False
            if isinstance(node.op, ast.Mult): return combine(a[0], b[0]), False
            if isinstance(node.op, ast.Div): return combine(a[0], b[0], -1), False
            if isinstance(node.op, ast.Pow):
                def constant(n):
                    if isinstance(n, ast.Constant) and type(n.value) in (int, float):
                        if not np.isfinite(n.value): raise ValueError('Nonfinite exponent')
                        return Fraction(str(n.value))
                    if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
                        return constant(n.operand) * (-1 if isinstance(n.op, ast.USub) else 1)
                    if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                        left, right = constant(n.left), constant(n.right)
                        if isinstance(n.op, ast.Add): return left + right
                        if isinstance(n.op, ast.Sub): return left - right
                        if isinstance(n.op, ast.Mult): return left * right
                        if not right: raise ValueError('Zero denominator in exponent')
                        return left / right
                    raise ValueError('Exponent must be a fixed numeric expression')
                power = constant(node.right)
                if abs(power) > 8: raise ValueError('Exponent must be within [-8,8]')
                return tidy({key: p * power for key, p in a[0].items()}), False
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and not node.keywords:
            name = node.func.id
            expected = 2 if name in {'minimum', 'maximum'} else 1
            if len(node.args) != expected: raise ValueError("Invalid function arguments")
            args = [visit(arg) for arg in node.args]
            if name in {'minimum', 'maximum'}: return compatible(*args), False
            if name == 'abs': return args[0]
            if name == 'sqrt': return {key: p / 2 for key, p in args[0][0].items()}, False
            if name in {'log', 'log10', 'exp'}:
                if args[0][0]: raise ValueError(f"{name} requires a dimensionless argument; divide by a matching reference")
                return {}, False
        raise ValueError("Unsupported formula symbol or syntax")
    dims, _ = visit(tree.body)
    if dims.get('native_density'):
        raise ValueError('Density physical unit is unresolved; use q_density or density/density_ref')
    return {'status': 'passed', 'output_dimensions': {key: str(value) for key, value in sorted(dims.items())},
            'limitation': 'Unit algebra does not verify the mechanism or numerical unit conversion.'}


def clean_excerpt(quote):
    # Retain the original source quote in the bank. Prompt text is normalized,
    # not mislabelled as a new verbatim quotation.
    text = html.unescape(str(quote))
    text = re.sub(r'<\s*/?\s*(?:div|img|span|a|br|p)\b[^>]*>', ' ', text, flags=re.I)
    paragraphs = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', text)]
    relevant = [p for p in paragraphs if re.search(r'entrop|rotat|translat|confin', p, re.I)]
    text = ' '.join(relevant or paragraphs)
    # Choose a contiguous window around the relevant discussion if boilerplate
    # precedes it. The transform is recorded and the original remains available.
    match = re.search(r'entrop|rotat|translat|confin', text, re.I)
    if match and match.start() > 200:
        start = max(0, text.rfind('. ', 0, match.start()) + 2)
        text = text[start:]
    return text.strip()


def relevance(quote):
    text = quote.lower()
    if DOI in text or 'elucidating thermodynamically driven structure' in text:
        return False, 'benchmark_reference', 0
    if len(re.findall(r'[a-z]+', text)) < 8:
        return False, 'table_fragment_or_short_quote', 0
    entropy = bool(re.search(r'entrop|rotat|translat', text))
    system = bool(re.search(r'adsorb|adsorp|confin|zeolit|micropor|nanopor', text))
    if not entropy or not system:
        return False, 'missing_adsorption_entropy_mechanism', 0
    if re.search(r'epoxid|turnover|aqueous', text) and not re.search(r'adsorb|adsorp', text):
        return False, 'reaction_or_solvent_entropy_scope', 0
    score = sum(bool(re.search(pattern, text)) for pattern in [r'entrop', r'confin', r'rotat', r'translat', r'adsorp|adsorb', r'volume|pore|shape|inertia'])
    return True, 'eligible', score


def scope_tags(quote):
    tags = []
    for tag, pattern in [('pure_silica', r'pure.silica|all.silica|silicalite'),
                         ('aluminosilicate_or_protonic', r'aluminosilicat|protonic|acid site'),
                         ('cation_or_water', r'cation|water|h2o|aqueous'),
                         ('infinite_dilution', r'infinite.dilution|zero.loading'),
                         ('298K', r'298\s*.?\s*k')]:
        if re.search(pattern, quote, re.I): tags.append(tag)
    return tags or ['conditions_not_explicit_in_excerpt']


def scientific_data(value):
    """Keep scientific fields intact; omit file bookkeeping and duplicate evidence."""
    if isinstance(value, dict):
        return {key: scientific_data(item) for key, item in value.items()
                if 'sha256' not in str(key).lower() and key not in {
                    'source_path', 'source_documents', 'evidence', 'artifact_path',
                }}
    if isinstance(value, list): return [scientific_data(item) for item in value]
    return value


def compact_paths(paths):
    result = []
    for path in sorted(paths, key=lambda p: -len(p.get('edges', [])))[:2]:
        if not path.get('edges'): continue
        nodes = [{'id': n['id'], 'type': n.get('type'), 'label': n.get('label'),
                  'source_data': scientific_data(n.get('data') or {}),
                  'review_status': n.get('review_status', 'unknown')} for n in path['nodes']]
        edges = []
        for edge in path['edges']:
            edges.append({'id': edge['id'], 'source': edge['source'], 'target': edge['target'],
                          'relation': edge.get('relation', 'unspecified_relation'),
                          'review_status': edge.get('review_status', 'unknown'),
                          'source_paper_id': edge.get('source_paper_id'),
                          'support': [{'quote': str(e.get('quote') or ''),
                                       'document_id': e.get('document_id'),
                                       'page': e.get('pdf_page_index'),
                                       'validation': e.get('evidence_validation', 'unknown')}
                                      for e in edge.get('evidence', [])]})
        result.append({'nodes': nodes, 'edges': edges,
                       'interpretation': 'Extracted directed relations, not a proof of causality or applicability.'})
    return result


def prepare_bank_rows(rows, channel, excluded):
    accepted = []; rejected = []
    seen = set()
    for row in rows:
        original = str(row.get('quote') or row.get('text') or '')
        excerpt = clean_excerpt(original)
        ok, reason, score = relevance(excerpt)
        if str(row.get('paper_id')) in excluded: ok, reason = False, 'excluded_paper'
        if contamination_reason(row): ok, reason = False, 'benchmark_reference'
        if not ok:
            rejected.append({'record_id': row['record_id'], 'reason': reason}); continue
        key = (row['paper_id'], row['document_id'], excerpt)
        if key in seen: continue
        seen.add(key)
        paths = compact_paths(row.get('kg_paths') or []) if channel == 'kg' else []
        if channel == 'kg' and not paths:
            rejected.append({'record_id': row['record_id'], 'reason': 'no_connected_relation_path'}); continue
        locator = row.get('provenance_locator')
        if not locator:
            if str(row.get('source_path', '')).endswith(('.md', '.markdown')):
                locator = {'kind': 'markdown_section', 'section': row.get('section')}
            else: locator = {'kind': 'pdf_page', 'page': row.get('page') or row.get('pdf_page_index')}
        if locator['kind'] == 'pdf_page' and (not isinstance(locator.get('page'), int) or locator['page'] < 1):
            rejected.append({'record_id': row['record_id'], 'reason': 'invalid_provenance'}); continue
        accepted.append({'record_id': row['record_id'], 'paper_id': row['paper_id'],
                         'document_id': row['document_id'], 'quote': excerpt, 'original_quote': original,
                         'quote_transform': 'HTML cleanup and entropy-related paragraph/window selection',
                         'locator': locator, 'channel': channel, 'scope_tags': scope_tags(excerpt),
                         'relevance_score': score, 'source_score': float(row.get('score', 0)),
                         'graph_paths': paths})
    return accepted, rejected


def adaptive_query(round_no, retained, history, requested_queries=()):
    # No data arrays or test metrics are accepted by this function.
    terms = [QUERIES[0]]
    for entry in retained[-2:]:
        symbols = [node.id.removeprefix('q_').removesuffix('_ref')
                   for node in ast.walk(ast.parse(entry['formula'], mode='eval')) if isinstance(node, ast.Name)]
        terms.extend(INPUT_SCHEMA[s]['meaning'] for s in symbols if s in INPUT_SCHEMA)
    terms.extend(str(q)[:180] for q in list(requested_queries)[:3] if isinstance(q, str))
    if history and any(c.get('status') == 'rejected' for c in history[-1]['candidates']):
        terms.append('dimensionless relative pore molecular geometry physical regime limitations')
    terms.append(QUERIES[(round_no - 1) % len(QUERIES)])
    return ' '.join(dict.fromkeys(terms))[:1500]


def select_evidence(bank, mode, query, *, graph_view='paths', token_budget=32000,
                    item_limit=32, candidate_limit=120, paper_limit=4, kg_priority_items=8):
    if mode == 'agent': return [], {'query': query, 'items': 0, 'lexical_tokens': 0, 'graph_paths': 0}
    if graph_view not in {'paths', 'text'}: raise ValueError('Unknown graph view')
    query_terms = set(re.findall(r'[a-z]{3,}', query.lower()))
    def rank(rows):
        return sorted(rows, key=lambda r: (-(r['relevance_score'] + .1 * len(query_terms & set(re.findall(r'[a-z]{3,}', r['quote'].lower())))), r['record_id']))
    rag = rank(bank['rag'])[:candidate_limit]
    kg = rank(bank['kg'])[:candidate_limit] if mode == 'small_kg_rag_agent' else []
    # Same total candidate cap. Reserve useful graph evidence, rather than
    # requiring irrelevant paths merely to satisfy a graph quota.
    if not kg:
        candidates = rag
    else:
        # Interleave after the initial graph entries so a generous budget can
        # carry complementary RAG passages as well as graph paths.
        candidates = list(kg[:kg_priority_items])
        tail_kg = kg[kg_priority_items:]
        for i in range(max(len(rag), len(tail_kg))):
            if i < len(rag): candidates.append(rag[i])
            if i < len(tail_kg): candidates.append(tail_kg[i])
        candidates = candidates[:candidate_limit]
    selected = []; paper_counts = Counter(); seen = set(); skipped_budget = 0
    def serialized_tokens(items):
        return count_tokens(json.dumps(items, ensure_ascii=False))
    for row in candidates:
        key = (row['paper_id'], row['document_id'], row['quote'])
        if key in seen or paper_counts[row['paper_id']] >= paper_limit: continue
        item = {'id': f"R{bank.get('active_round', 1)}E{len(selected)+1:02d}",
                'paper_id': row['paper_id'], 'quote': row['quote'], 'locator': row['locator'],
                'scope_tags': row['scope_tags'], 'channels': [row['channel']],
                'quote_transform': row['quote_transform']}
        if row['graph_paths']:
            if graph_view == 'paths': item['graph_paths'] = row['graph_paths']
            else:
                # The text control keeps the same facts and provenance, removing
                # path organization rather than deleting graph-selected evidence.
                item['graph_facts_as_text'] = [
                    f"{edge['source']} {edge['relation']} {edge['target']}; support={json.dumps(edge['support'], ensure_ascii=False)}"
                    for path in row['graph_paths'] for edge in path['edges']]
                item['graph_nodes_as_text'] = [f"{node['id']}: {node['label']}; {json.dumps(node['source_data'], ensure_ascii=False)}"
                                              for path in row['graph_paths'] for node in path['nodes']]
        tokens = serialized_tokens([*selected, item])
        if tokens > token_budget:
            # Preserve the passage, conditions and supporting quotes together.
            # Skip a whole oversized item instead of cutting away qualifications.
            skipped_budget += 1; continue
        selected.append(item); paper_counts[row['paper_id']] += 1; seen.add(key)
        if len(selected) >= item_limit: break
    used = serialized_tokens(selected) if selected else 0
    return selected, {'query': query, 'items': len(selected), 'lexical_tokens': used,
                      'context_token_budget': token_budget, 'graph_view': graph_view,
                      'graph_paths': sum(len(e.get('graph_paths', [])) for e in selected),
                      'kg_selected_items': sum('kg' in e['channels'] for e in selected),
                      'paper_ids': sorted(paper_counts), 'candidate_cap': candidate_limit,
                      'item_limit': item_limit, 'items_per_paper_limit': paper_limit,
                      'whole_items_skipped_for_budget': skipped_budget,
                      'item_limit_reached': len(selected) >= item_limit,
                      'near_context_limit': used >= .9 * token_budget,
                      'length_matched': False,
                      'length_policy': 'Common cap including serialized graph facts; actual lengths logged, no irrelevant padding.'}
