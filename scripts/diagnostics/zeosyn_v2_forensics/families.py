import re
T_ATOMS = r'(Si|Al|P|Ge|B|Ga|Ti|Zn|Be|Sn|Zr|V|W|Cu|Mg)'
def norm(f):
    return re.sub(r'\s+', '', f or '')
def strip_wrap(f):
    # drop leading unary functions and parentheses so the leading operand is visible
    changed = True
    while changed:
        changed = False
        m = re.match(r'^(log|log10|log2|sqrt|abs|exp)\((.*)\)$', f)
        if m: f = m.group(2); changed = True
        if f.startswith('(') and f.endswith(')'):
            depth = 0; ok = True
            for i, ch in enumerate(f):
                depth += ch == '('; depth -= ch == ')'
                if depth == 0 and i < len(f) - 1: ok = False; break
            if ok: f = f[1:-1]; changed = True
    return f
def split_top(f):
    """numerator / denominator at the top-level division, if any"""
    depth = 0
    for i, ch in enumerate(f):
        depth += ch == '('; depth -= ch == ')'
        if ch == '/' and depth == 0: return f[:i], f[i + 1:]
    return f, ''
def family(formula):
    f = strip_wrap(norm(formula))
    if not f: return 'NONE'
    if 'cryst_time' in f or 'cryst_temp' in f: return 'KINETIC_time_temp'
    num, den = split_top(f)
    num_s = strip_wrap(num); den_s = strip_wrap(den)
    def has(x, pat): return re.search(pat, x) is not None
    lead = re.match(r'^[A-Za-z0-9_]+', num_s)
    lead = lead.group(0) if lead else ''
    # alkalinity: OH (or OH+F, OH-F, OH+Na..) over T atoms or water or OSDA
    if lead == 'OH' or re.match(r'^OH[+\-*]', num_s):
        if 'sda1' in den_s: return 'ALKALINITY_OH_per_OSDA'
        return 'ALKALINITY_OH_per_T'
    # dilution: H2O over T atoms, or T atoms over H2O
    if lead == 'H2O' and den_s: return 'DILUTION_H2O_per_T'
    if has(den_s, r'^H2O') and has(num_s, T_ATOMS) and not has(num_s, r'\b(OH|F|Na|K|sda1)\b'): return 'DILUTION_H2O_per_T'
    # fluoride
    if lead == 'F' or re.match(r'^F[+\-*]', num_s):
        if 'OH' in f: return 'FLUORIDE_vs_OH'
        if 'sda1' in den_s or 'osda_charge' in den_s: return 'FLUORIDE_per_OSDA'
        return 'FLUORIDE_per_T'
    # heteroatoms
    if re.match(r'^(Ge|B|Ti|Ga|Zn|Sn|Zr|V|W|Cu|Be)\b', num_s) and not re.match(r'^B\b', num_s) or re.match(r'^Ge\b', num_s): return 'HETEROATOM_fraction'
    if re.match(r'^\(?(Ge|Ti|B|Zn|Sn|Ga)\+(Ti|B|Zn|Sn|Ga|Ge)', num_s): return 'HETEROATOM_fraction'
    # AlPO balance
    if lead == 'P' or re.match(r'^(Al-P|P-Al|abs\(Al-P)', num_s) or (lead == 'Al' and re.match(r'^(Al\+P|P\b)', den_s)): return 'ALPO_P_Al_balance'
    # organic charge per T / vs inorganic
    if has(num_s, r'osda_charge\*sda1|sda1\*osda_charge|sda1\*maximum\(osda_charge|sda1\*abs\(osda_charge|abs\(osda_charge\)\*sda1|maximum\(osda_charge,0\)\*sda1'):
        if has(den_s, r'\b(Na|K|Li|Cs|Rb)\b'): return 'CHARGE_organic_vs_inorganic'
        return 'OSDA_charge_per_T'
    # inorganic cations
    if re.match(r'^(Na|K|Li|Cs|Rb|Ca|Sr|Ba|Mg|2\*\()', num_s):
        if has(den_s, r'sda1|osda_charge'): return 'CHARGE_organic_vs_inorganic'
        if has(den_s, T_ATOMS): return 'INORGANIC_cation_per_Al_or_T'
        return 'INORGANIC_cation_mix'
    # OSDA loading
    if lead == 'sda1':
        if has(den_s, r'\b(Na|K|Li|Cs|Rb)\b'): return 'CHARGE_organic_vs_inorganic'
        if has(den_s, r'\b(Al|P)\b') and not has(den_s, r'\bSi\b') and 'osda_charge' in num_s: return 'OSDA_charge_per_T'
        return 'OSDA_loading_per_T'
    if lead.startswith('osda_'): return 'OSDA_molecular_property_combo'
    # Si / Al / P composition (incl. Si fraction of T, non-Si fraction)
    if lead in ('Si', 'Al') or re.match(r'^(Si|Al)\+', num_s): return 'SI_AL_P_composition'
    if has(f, r'\bSi\b') and has(f, r'\b(Al|P)\b'): return 'SI_AL_P_composition'
    return 'OTHER'
