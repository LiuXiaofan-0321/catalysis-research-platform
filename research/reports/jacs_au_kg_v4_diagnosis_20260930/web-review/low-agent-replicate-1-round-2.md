# low/agent/replicate-1/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h2",
    "name": "accessible_volume_crowding_entropy",
    "formula": "-log(AV / AV_ref + 1) * (Vol / Vol_ref)",
    "hypothesis": "Adsorption entropy loss increases with the logarithm of the inverse of probe-accessible specific framework volume (AV) multiplied by adsorbate van der Waals volume: molecules large relative to the accessible free volume lose more configurational (positional) entropy upon adsorption, independent of bottleneck shape.",
    "rationale": "Configurational entropy of a confined particle scales with accessible phase-space volume; the descriptor is the negative log of (dimensionless AV contrast + 1), which increases as probe-accessible volume decreases, multiplied by adsorbate van der Waals volume as an explicit crowding proxy. AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume. Limitation: the +1 shift is an empirical smoothing device for AV = 0 rows, not a physical length scale, and the log form is a free-volume-like ansatz, not a derived law.",
    "falsification_criteria": "If entropy loss is uncorrelated (or anti-correlated) with the AV-contrast term on frameworks with AV > 0 at matched adsorbate size, the positional-crowding mechanism is falsified. Also falsified if the compressed-log dependence (saturating in AV) fits worse than a linear AV contrast on held-out data. Competing mechanism: adsorbate–surface contact-area effects dominating over free-volume crowding.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Fixed-probe AV approximates the accessible free-volume scale for all adsorbates; Vol/Vol_ref proxies relative crowding; zero-AV frameworks map to zero descriptor magnitude, an empirical smoothing of an inaccessible-probe boundary, not a physical claim of zero crowding.",
      "physical_interpretation": "AV is probe-accessible specific volume (cm^3/g), Vol is van der Waals volume; AV_ref is the fixed positive training-reference median, so AV/AV_ref is dimensionless and row-varying; no physical meaning is assigned to AV = AV_ref.",
      "boundary_behavior": "AV/AV_ref + 1 >= 1 for all AV >= 0, so the log is defined and finite on every training row, including the 28 zero-AV rows where log(1) = 0 (descriptor vanishes at zero accessibility rather than diverging). Vol is strictly positive. No imputation and no arbitrary epsilon: the +1 is a dimensionless additive constant guaranteeing finiteness on the full observed support.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        0.9
      ],
      "entropy_direction": "increasing"
    }
  }
]
```

## h1

候选标识：`low/agent/replicate-1/round-2/h1`

最终状态：scored；边际收益：+2.957330 pp；保留：True。

复核改动字段：falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_included_sphere_coupling",
    "formula": "(Vol / Vol_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "Adsorption entropy loss increases with the ratio of adsorbate van der Waals volume to the included-sphere diameter along the free-sphere path (lsd_p): molecules that are large relative to the largest sphere that fits along the diffusion path are confined into fewer accessible positional configurations at the adsorption site, increasing entropy loss at infinite dilution.",
    "rationale": "lsd_p (Dif) characterizes the local free space along the path, a softer confinement measure than the bottleneck Df which failed in round 1. Using Vol rather than MW couples geometric confinement to molecular size without rotor-class confounding. Limitation: lsd_p is a fixed-probe geometric proxy, not a molecule-specific free volume; the linear inverse scaling is an empirical smoothing choice.",
    "falsification_criteria": "If training Spearman between the descriptor and entropy loss within the lsd_p regime is near zero or positive (contradicting the declared negative association of entropy with increasing descriptor), or if partial-derivative perturbation diagnostics show the association is driven only by Vol, the hypothesis is falsified in favor of a pure size effect independent of path confinement.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_p is a Zeo++ included-sphere proxy on the free-sphere path, not the global cavity Di and not a molecule-specific measure; Vol is an implicit-H van der Waals volume; transferability across framework topologies is assumed only through these two scalars.",
      "physical_interpretation": "Increasing Vol (larger molecule) or decreasing lsd_p (tighter included sphere along path) both reduce accessible configurational volume; q-normalized products carry no universal physical meaning at q=1.",
      "boundary_behavior": "Both Vol and lsd_p are strictly positive over the training domain (Vol min 20.424, lsd_p min 3.3452), so the expression is finite for every training row; no zero-division occurs and no imputation is needed.",
      "vary_input": "lsd_p",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "Vol",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 2361,
      "nonzero_fraction": 0.0
    },
    "reason": "Formula contradicts its predeclared proxy direction"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_included_sphere_coupling",
    "formula": "(Vol / Vol_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "Adsorption entropy loss increases with the ratio of adsorbate van der Waals volume to the included-sphere diameter along the free-sphere path (lsd_p): molecules that are large relative to the largest sphere that fits along the diffusion path are confined into fewer accessible positional configurations at the adsorption site, increasing entropy loss at infinite dilution.",
    "rationale": "The expression (Vol/Vol_ref)*(lsd_p_ref/lsd_p) is decreasing in lsd_p, so the predeclared descriptor_direction 'increasing' contradicted the formula for all rows. The declared association (entropy loss increases as the included-sphere diameter along the path shrinks relative to molecular size) is unchanged; only the proxy derivative direction is corrected to 'decreasing' in lsd_p. Entropy direction remains increasing in the descriptor. lsd_p remains a fixed-probe geometric proxy (Dif, included sphere along the free path, not global cavity Di); linear inverse scaling is empirical smoothing.",
    "falsification_criteria": "If training Spearman between the descriptor and entropy loss is near zero or negative, or if perturbation diagnostics show the association is driven only by Vol, the path-confinement coupling is falsified in favor of a pure size effect.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_p is a Zeo++ included-sphere proxy on the free-sphere path (Dif), not the global cavity Di and not a molecule-specific measure; Vol is an implicit-H van der Waals volume; transferability across framework topologies is assumed only through these two scalars.",
      "physical_interpretation": "Increasing Vol (larger molecule) or decreasing lsd_p (tighter included sphere along path) both reduce accessible configurational volume, so the descriptor decreases in lsd_p while the declared entropy-loss association increases in the descriptor; q-normalized products carry no universal physical meaning at q=1.",
      "boundary_behavior": "Vol (min 20.424) and lsd_p (min 3.3452) are strictly positive over training, so the expression is finite for every row with no division by legitimate zero.",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "Vol",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        3.3452,
        15.5604
      ],
      "training_spearman": 0.6790106516914549,
      "target_association": "consistent",
      "perturbation": 0.0452717,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_included_sphere_coupling",
    "formula": "(Vol / Vol_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "Adsorption entropy loss increases with the ratio of adsorbate van der Waals volume to the included-sphere diameter along the free-sphere path (lsd_p): molecules that are large relative to the largest sphere that fits along the diffusion path are confined into fewer accessible positional configurations at the adsorption site, increasing entropy loss at infinite dilution.",
    "rationale": "The expression (Vol/Vol_ref)*(lsd_p_ref/lsd_p) is decreasing in lsd_p, so the predeclared descriptor_direction 'increasing' contradicted the formula for all rows. The declared association (entropy loss increases as the included-sphere diameter along the path shrinks relative to molecular size) is unchanged; only the proxy derivative direction is corrected to 'decreasing' in lsd_p. Entropy direction remains increasing in the descriptor. lsd_p remains a fixed-probe geometric proxy (Dif, included sphere along the free path, not global cavity Di); linear inverse scaling is empirical smoothing.",
    "falsification_criteria": "If training Spearman between the descriptor and entropy loss is near zero or negative, or if perturbation diagnostics show the association is driven only by Vol, the path-confinement coupling is falsified in favor of a pure size effect.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_p is a Zeo++ included-sphere proxy on the free-sphere path (Dif), not the global cavity Di and not a molecule-specific measure; Vol is an implicit-H van der Waals volume; transferability across framework topologies is assumed only through these two scalars.",
      "physical_interpretation": "Increasing Vol (larger molecule) or decreasing lsd_p (tighter included sphere along path) both reduce accessible configurational volume, so the descriptor decreases in lsd_p while the declared entropy-loss association increases in the descriptor; q-normalized products carry no universal physical meaning at q=1.",
      "boundary_behavior": "Vol (min 20.424) and lsd_p (min 3.3452) are strictly positive over training, so the expression is finite for every row with no division by legitimate zero.",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "Vol",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        3.3452,
        15.5604
      ],
      "training_spearman": 0.6790106516914549,
      "target_association": "consistent",
      "perturbation": 0.0452717,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/agent/replicate-1/round-2/h2`

最终状态：scored；边际收益：+0.721583 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_area_entropic_cost",
    "formula": "log(LabuteASA / LabuteASA_ref + 1) * (density / density_ref) ** 2",
    "hypothesis": "Adsorption entropy loss increases with the adsorbate's molecular surface area (LabuteASA) raised against framework density: heavier (denser) frameworks pack adsorption sites more tightly, so a molecule with larger contact surface experiences stronger confinement of its translational and orientational freedom upon adsorption, losing more entropy at infinite dilution.",
    "rationale": "Round 1 showed the AV-based crowding descriptor was contradicted (-0.055 Spearman); surface-area contact rather than volume crowding is the alternative connectivity/surface mechanism. LabuteASA is strictly positive in training (min 7.45), and density is strictly positive (min 0.76), so the log argument is always >1. Limitation: density is on an unresolved native scale, and the square exponent is a fixed empirical smoothing constant with no universal meaning.",
    "falsification_criteria": "If the training association between this descriptor and entropy loss is contradicted (Spearman sign opposite to declared) within the density regime, or if replacing density by a constant does not degrade marginal improvement (i.e., density adds no information beyond molecular surface area), the surface-density coupling hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "LabuteASA approximates the molecule-surface contact area available for framework interaction; framework density on the published numerical scale is treated as a monotone proxy for packing tightness; both are geometric surrogates, not energetic descriptors.",
      "physical_interpretation": "The descriptor is a dimensionless product of a log-scaled surface-area ratio and a squared density ratio; no q-unity threshold is asserted and the fixed exponent 2 is an empirical choice.",
      "boundary_behavior": "LabuteASA has zero_n=0 and density has zero_n=0 over training, so the log argument exceeds 1 and the expression is finite for all rows; no legitimate zero is divided by.",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "density",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "LabuteASA",
        "density"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": 0.5870493565805309,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_area_entropic_cost",
    "formula": "log(LabuteASA / LabuteASA_ref + 1) * (density / density_ref) ** 2",
    "hypothesis": "Adsorption entropy loss increases with the adsorbate's molecular surface area (LabuteASA) raised against framework density: heavier (denser) frameworks pack adsorption sites more tightly, so a molecule with larger contact surface experiences stronger confinement of its translational and orientational freedom upon adsorption, losing more entropy at infinite dilution.",
    "rationale": "Round 1 showed the AV-based crowding descriptor was contradicted (-0.055 Spearman); surface-area contact rather than volume crowding is the alternative connectivity/surface mechanism. LabuteASA is strictly positive in training (min 7.45), and density is strictly positive (min 0.76), so the log argument is always >1. Limitation: density is on an unresolved native scale, and the square exponent is a fixed empirical smoothing constant with no universal meaning.",
    "falsification_criteria": "If the training association between this descriptor and entropy loss is contradicted (Spearman sign opposite to declared) within the density regime, or if replacing density by a constant does not degrade marginal improvement (i.e., density adds no information beyond molecular surface area), the surface-density coupling hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "LabuteASA approximates the molecule-surface contact area available for framework interaction; framework density on the published numerical scale is treated as a monotone proxy for packing tightness; both are geometric surrogates, not energetic descriptors.",
      "physical_interpretation": "The descriptor is a dimensionless product of a log-scaled surface-area ratio and a squared density ratio; no q-unity threshold is asserted and the fixed exponent 2 is an empirical choice.",
      "boundary_behavior": "LabuteASA has zero_n=0 and density has zero_n=0 over training, so the log argument exceeds 1 and the expression is finite for all rows; no legitimate zero is divided by.",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "density",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "LabuteASA",
        "density"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": 0.5870493565805309,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_area_entropic_cost",
    "formula": "log(LabuteASA / LabuteASA_ref + 1) * (density / density_ref) ** 2",
    "hypothesis": "Adsorption entropy loss increases with the adsorbate's molecular surface area (LabuteASA) raised against framework density: heavier (denser) frameworks pack adsorption sites more tightly, so a molecule with larger contact surface experiences stronger confinement of its translational and orientational freedom upon adsorption, losing more entropy at infinite dilution.",
    "rationale": "Round 1 showed the AV-based crowding descriptor was contradicted (-0.055 Spearman); surface-area contact rather than volume crowding is the alternative connectivity/surface mechanism. LabuteASA is strictly positive in training (min 7.45), and density is strictly positive (min 0.76), so the log argument is always >1. Limitation: density is on an unresolved native scale, and the square exponent is a fixed empirical smoothing constant with no universal meaning.",
    "falsification_criteria": "If the training association between this descriptor and entropy loss is contradicted (Spearman sign opposite to declared) within the density regime, or if replacing density by a constant does not degrade marginal improvement (i.e., density adds no information beyond molecular surface area), the surface-density coupling hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "LabuteASA approximates the molecule-surface contact area available for framework interaction; framework density on the published numerical scale is treated as a monotone proxy for packing tightness; both are geometric surrogates, not energetic descriptors.",
      "physical_interpretation": "The descriptor is a dimensionless product of a log-scaled surface-area ratio and a squared density ratio; no q-unity threshold is asserted and the fixed exponent 2 is an empirical choice.",
      "boundary_behavior": "LabuteASA has zero_n=0 and density has zero_n=0 over training, so the log argument exceeds 1 and the expression is finite for all rows; no legitimate zero is divided by.",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "density",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "LabuteASA",
        "density"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": 0.5870493565805309,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/agent/replicate-1/round-2/h3`

最终状态：scored；边际收益：-0.190958 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "rotor_class_asphericity_branch",
    "formula": "rotor_case(SPAN / SPAN_ref, (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref) ** -0.5, (PMI3 / PMI3_ref) ** 0.5 * (GeDi / GeDi_ref))",
    "hypothesis": "Adsorption entropy loss depends on rotor class: (a) for single-site adsorbates entropy loss increases with heavy-atom enclosing radius (SPAN) as a proxy for site footprint; (b) for linear rotors entropy loss decreases with the asphericity contrast PMI2*PMI3^(-1/2), since near-prolate molecules retain more rotational freedom about their long axis in a cavity; (c) for nonlinear rotors entropy loss increases with the geometric-mean extent PMI3^(1/2)*GeDi, since larger, more extended three-dimensional bodies lose more orientational entropy upon confinement.",
    "rationale": "Round 1's single pooled planarity descriptor was consistent but weak (Spearman 0.25); branching by rotor class removes class confounding between heavy-atom geometry and entropy loss, which the pooled descriptor could not resolve. Limitations: PMI/SPAN/GeDi are heavy-atom (implicit-H) proxies; single-site molecules legitimately have near-zero PMI values, so the single-site branch uses SPAN only; branch exponents are fixed empirical constants, not universal laws.",
    "falsification_criteria": "If within any rotor-class regime the training Spearman between the branch expression and entropy loss shows the opposite sign to the declared direction (positive in branch a, negative in branch b, positive in branch c), or if the branched descriptor's marginal improvement over the current retained set is negative and exceeds the round-1 pooled descriptor's deficit (-0.0171), the rotor-class dependence hypothesis is falsified for that class.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI1/2/3, SPAN and GeDi are heavy-atom representation proxies; near-zero PMI values for single-site molecules are legitimate and must not be treated as physical all-atom inertia zero; rotor classification follows the native proxy categories with 1e-10 normalized tolerance.",
      "physical_interpretation": "Each branch is a dimensionless product/quotient of q-normalized heavy-atom descriptors; branch selection is discrete and no physical threshold is claimed at q=1; negative exponents express empirical asphericity contrast.",
      "boundary_behavior": "Single-site branch uses SPAN (legitimate zeros exist for 54 rows); since the single-site branch never uses PMI, zero PMI rows evaluate only via SPAN which is finite (0 for single-site rows yields descriptor 0, finite). Linear and nonlinear branches require PMI2, PMI3 > 0; the training rotor counts (214 linear, 2093 nonlinear) are consistent with positive PMI2/PMI3 for those classes, and SPAN/GeDi are positive for all linear and nonlinear rows, so every training row yields a finite value in its selected branch.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "GeDi",
        "PMI2",
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 214,
      "nonzero_fraction": 0.8864887759423973
    },
    "reason": "Formula contradicts its predeclared proxy direction"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "rotor_class_asphericity_branch",
    "formula": "rotor_case(SPAN / SPAN_ref, (PMI2 / PMI2_ref) ** -0.5 * (PMI3 / PMI3_ref) ** 0.5, (PMI3 / PMI3_ref) ** 0.5 * (GeDi / GeDi_ref))",
    "hypothesis": "Adsorption entropy loss depends on rotor class: (a) for single-site adsorbates entropy loss increases with heavy-atom enclosing radius (SPAN) as a proxy for site footprint; (b) for linear rotors entropy loss decreases with the asphericity contrast PMI2*PMI3^(-1/2), since near-prolate molecules retain more rotational freedom about their long axis in a cavity; (c) for nonlinear rotors entropy loss increases with the geometric-mean extent PMI3^(1/2)*GeDi, since larger, more extended three-dimensional bodies lose more orientational entropy upon confinement.",
    "rationale": "The precheck varied PMI3 and found the linear branch (PMI2*PMI3^-0.5) decreasing in PMI3 for 214 rows, contradicting the declared descriptor_direction 'increasing'. The linear branch is replaced by its reciprocal-asphericity form PMI2^-0.5 * PMI3^0.5, which is monotonically decreasing in the asphericity contrast and increasing in PMI3, matching the hypothesis statement that near-prolate (high-asphericity-contrast) linear rotors retain rotational freedom and lose less entropy. Since entropy_direction is stored as increasing, this makes the linear-branch descriptor consistently increasing in PMI3 like the nonlinear branch. All PMI/SPAN/GeDi values remain heavy-atom (implicit-H) proxies; branch exponents are fixed empirical constants, not universal laws.",
    "falsification_criteria": "If within any rotor-class regime the training Spearman between the branch expression and entropy loss shows the opposite sign to the declared direction (increasing in PMI3 for both linear and nonlinear branches), or if the branched descriptor's marginal improvement is negative and exceeds the round-1 pooled descriptor's deficit (-0.0171), the rotor-class dependence is falsified for that class.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2, PMI3, SPAN and GeDi are heavy-atom representation proxies with legitimate near-zero values for single-site molecules; rotor classification follows the native proxy categories with 1e-10 normalized tolerance; no all-atom inertia claim is made.",
      "physical_interpretation": "Each branch is a dimensionless product of q-normalized heavy-atom descriptors; the linear branch expresses empirical inverse asphericity contrast; no threshold is claimed at q=1.",
      "boundary_behavior": "Single-site rows (54) use only SPAN; zero SPAN yields descriptor 0, finite. Linear and nonlinear rows have strictly positive PMI2/PMI3 within the 1e-10 normalized tolerance, and SPAN/GeDi are positive there, so every selected branch is finite for all training rows; negative exponent -0.5 applies only to strictly positive PMI2 in the linear branch.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "GeDi",
        "PMI2",
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2414.631462
      ],
      "training_spearman": 0.37780564308963,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "rotor_class_asphericity_branch",
    "formula": "rotor_case(SPAN / SPAN_ref, (PMI2 / PMI2_ref) ** -0.5 * (PMI3 / PMI3_ref) ** 0.5, (PMI3 / PMI3_ref) ** 0.5 * (GeDi / GeDi_ref))",
    "hypothesis": "Adsorption entropy loss depends on rotor class: (a) for single-site adsorbates entropy loss increases with heavy-atom enclosing radius (SPAN) as a proxy for site footprint; (b) for linear rotors entropy loss decreases with the asphericity contrast PMI2*PMI3^(-1/2), since near-prolate molecules retain more rotational freedom about their long axis in a cavity; (c) for nonlinear rotors entropy loss increases with the geometric-mean extent PMI3^(1/2)*GeDi, since larger, more extended three-dimensional bodies lose more orientational entropy upon confinement.",
    "rationale": "The precheck varied PMI3 and found the linear branch (PMI2*PMI3^-0.5) decreasing in PMI3 for 214 rows, contradicting the declared descriptor_direction 'increasing'. The linear branch is replaced by its reciprocal-asphericity form PMI2^-0.5 * PMI3^0.5, which is monotonically decreasing in the asphericity contrast and increasing in PMI3, matching the hypothesis statement that near-prolate (high-asphericity-contrast) linear rotors retain rotational freedom and lose less entropy. Since entropy_direction is stored as increasing, this makes the linear-branch descriptor consistently increasing in PMI3 like the nonlinear branch. All PMI/SPAN/GeDi values remain heavy-atom (implicit-H) proxies; branch exponents are fixed empirical constants, not universal laws.",
    "falsification_criteria": "If within any rotor-class regime the training Spearman between the branch expression and entropy loss shows the opposite sign to the declared direction (increasing in PMI3 for both linear and nonlinear branches), or if the branched descriptor's marginal improvement is negative and exceeds the round-1 pooled descriptor's deficit (-0.0171), the rotor-class dependence is falsified for that class.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2, PMI3, SPAN and GeDi are heavy-atom representation proxies with legitimate near-zero values for single-site molecules; rotor classification follows the native proxy categories with 1e-10 normalized tolerance; no all-atom inertia claim is made.",
      "physical_interpretation": "Each branch is a dimensionless product of q-normalized heavy-atom descriptors; the linear branch expresses empirical inverse asphericity contrast; no threshold is claimed at q=1.",
      "boundary_behavior": "Single-site rows (54) use only SPAN; zero SPAN yields descriptor 0, finite. Linear and nonlinear rows have strictly positive PMI2/PMI3 within the 1e-10 normalized tolerance, and SPAN/GeDi are positive there, so every selected branch is finite for all training rows; negative exponent -0.5 applies only to strictly positive PMI2 in the linear branch.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "GeDi",
        "PMI2",
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2414.631462
      ],
      "training_spearman": 0.37780564308963,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## 本轮检索及引用原文

```json
{
  "retrieval": {
    "mode": "no_retrieval",
    "items": 0,
    "lexical_tokens": 0
  },
  "cited_items": [],
  "mechanism_cards": []
}
```
