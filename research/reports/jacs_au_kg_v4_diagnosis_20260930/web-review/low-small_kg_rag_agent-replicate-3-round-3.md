# low/small_kg_rag_agent/replicate-3/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/small_kg_rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h3",
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks (large AV) the same molecule retains more configurational freedom.",
    "rationale": "Entropy loss plausibly increases with the empirical contrast between adsorbate van der Waals volume and framework probe-accessible specific volume: in frameworks with small fixed-probe accessibility a large molecule is more spatially constrained, while open frameworks allow more configurational freedom, consistent with reported use of occupiable volume as an entropy-loss descriptor (E07). Limitations: AV is fixed-probe and mass-specific, not molecule-specific free volume, so no literal Vol/AV free-volume claim is made.",
    "falsification_criteria": "If entropy loss correlates with Vol alone equally well as with this ratio across frameworks spanning the AV range (including AV = 0 frameworks, where the fixed-probe accessibility may still permit molecular adsorption), the AV-contrast mechanism adds no explanatory power and should be rejected in favor of a pure molecular-size mechanism.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E03",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe AV ranks framework openness but is mass-specific and not molecule-specific; AV = 0 for the fixed geometric probe does not imply zero molecular adsorption space, so the ratio remains a smooth empirical proxy at AV = 0. Transferring the Vol/AV contrast to molecules smaller or larger than the probe is an empirical assumption.",
      "physical_interpretation": "Native Vol (van der Waals volume of the adsorbate) against native AV (probe-accessible specific volume of the framework, cm^3/g); the units do not form a physical free-volume equality, only a dimensionless empirical contrast after reference normalization. The additive 0.1 is a fixed smoothing constant without universal physical meaning. The precheck (Spearman +0.68, consistent) supports the declared decreasing-in-AV / increasing-in-Vol descriptor-to-loss direction but does not validate causality.",
      "boundary_behavior": "At AV = 0 the expression is finite, log(1 + 10 * Vol/Vol_ref); as AV grows, (Vol/Vol_ref)/(0.1 + AV/AV_ref) decreases monotonically toward 0, so the descriptor tends to log(1 + 0) = 0, NOT toward log(1 + Vol/Vol_ref). Vol training domain is strictly positive, so no division by zero occurs; the additive 0.1 only guards the legitimate AV zeros (28 training frameworks).",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  {
    "slot_id": "h3",
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + lsd_p / lsd_p_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's fixed-probe accessible specific volume: in frameworks with small probe accessibility, a large molecule has fewer accessible configurations (higher entropy loss), whereas in open frameworks the same molecule retains more configurational freedom.",
    "rationale": "Entropy loss increases with the ratio of molecular volume to the included free-path diameter: large molecules in frameworks with small included diameters along the diffusion path have fewer accessible configurations, while open frameworks preserve more configurational freedom (consistent with reported smaller-pore frameworks showing larger entropy-loss fractions). This replaces the redundant Vol/AV contrast with a non-redundant free-path descriptor; it remains an empirical proxy association, not demonstrated causality.",
    "falsification_criteria": "If the partial derivative of the target with respect to lsd_p (rotor class fixed) is positive, or the training Spearman turns non-positive, the free-path confinement mechanism is contradicted. Competing mechanism: the association may be driven by a hidden framework-density variable; test against density-residualized entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04",
      "E08"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Vol is the molecular van der Waals volume; lsd_p is the largest included sphere along the free-sphere path (Dif), NOT the passing bottleneck Df and NOT necessarily the global cavity Di. The previous resubmission of the Vol-vs-AV contrast was rejected as redundant with the already-retained round-1 input, so accessibility is now proxied by the free-path included diameter instead. The 0.1 constant is an empirical smoother, not a physical threshold.",
      "physical_interpretation": "Vol/Vol_ref and lsd_p/lsd_p_ref are dimensionless q-normalizations against fixed positive training medians; the ratio is row-varying and X/q_X equals the constant X_ref, which must never be used as an input. q-ratio = 1 is not native equality.",
      "boundary_behavior": "lsd_p training domain is strictly positive (min 3.3452), so the denominator 0.1 + lsd_p/lsd_p_ref is strictly positive on every row and the descriptor is finite everywhere; at small lsd_p the descriptor grows boundedly as log(1 + (Vol/Vol_ref)/0.1); at large lsd_p it decays toward log(2).",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "decreasing"
    }
  }
]
```

## h1

候选标识：`low/small_kg_rag_agent/replicate-3/round-3/h1`

最终状态：scored；边际收益：-4.765653 pp；保留：False。

复核改动字段：

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "surface_area_confined_pore_coupling",
    "formula": "log(1 + (LabuteASA / LabuteASA_ref) * (AV_ref / (0.1 + AV)))",
    "hypothesis": "Entropy loss increases with adsorbate molecular surface area, but only in proportion to how confined the framework is: in frameworks with small probe-accessible specific volume, a large-surface-area adsorbate has more adsorbent-contact degrees of freedom suppressed (fewer accessible translations/orientations), raising entropy loss, whereas in open frameworks the same molecule retains configurational freedom.",
    "rationale": "LabuteASA proxies the number of interaction-contact sites on the molecule; AV proxies framework openness. The product couples molecular contact extent to confinement. The 0.1 offset is an empirical smoothing constant to keep the expression finite at AV = 0 (28 training rows); it carries no universal physical meaning. Limitations: LabuteASA is an implicit-H approximate surface, and AV is a fixed-probe mass-specific accessibility, not molecule-specific free volume.",
    "falsification_criteria": "If the positive partial derivative of entropy loss with respect to LabuteASA at fixed rotor class fails to hold, or if the Spearman association of the descriptor with entropy loss is negative in the native regime, the confinement-coupling mechanism is falsified; a competing mechanism is that surface area correlates with enthalpic binding strength that dominates over entropic confinement.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA stands in for contact-degree suppression; AV stands in for framework openness; both are proxies with representation and probe-dependence limitations, and no causal claim is made.",
      "physical_interpretation": "Native quantities only: molecular surface area and probe-accessible specific volume; the normalized ratios are dimensionless row-varying inputs, and no q-unity equality threshold is asserted.",
      "boundary_behavior": "At AV = 0 the offset keeps the argument finite and positive, reflecting that zero fixed-probe accessibility does not imply zero physical adsorption space; LabuteASA has no training zeros, so no other boundary arises.",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "rejected",
    "reason": "Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "surface_area_confined_pore_coupling",
    "formula": "log(1 + (LabuteASA / LabuteASA_ref) * (AV_ref / (0.1 + AV)))",
    "hypothesis": "Entropy loss increases with adsorbate molecular surface area, but only in proportion to how confined the framework is: in frameworks with small probe-accessible specific volume, a large-surface-area adsorbate has more adsorbent-contact degrees of freedom suppressed (fewer accessible translations/orientations), raising entropy loss, whereas in open frameworks the same molecule retains configurational freedom.",
    "rationale": "LabuteASA proxies the number of interaction-contact sites on the molecule; AV proxies framework openness. The product couples molecular contact extent to confinement. The 0.1 offset is an empirical smoothing constant to keep the expression finite at AV = 0 (28 training rows); it carries no universal physical meaning. Limitations: LabuteASA is an implicit-H approximate surface, and AV is a fixed-probe mass-specific accessibility, not molecule-specific free volume.",
    "falsification_criteria": "If the positive partial derivative of entropy loss with respect to LabuteASA at fixed rotor class fails to hold, or if the Spearman association of the descriptor with entropy loss is negative in the native regime, the confinement-coupling mechanism is falsified; a competing mechanism is that surface area correlates with enthalpic binding strength that dominates over entropic confinement.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA stands in for contact-degree suppression; AV stands in for framework openness; both are proxies with representation and probe-dependence limitations, and no causal claim is made.",
      "physical_interpretation": "Native quantities only: molecular surface area and probe-accessible specific volume; the normalized ratios are dimensionless row-varying inputs, and no q-unity equality threshold is asserted.",
      "boundary_behavior": "At AV = 0 the offset keeps the argument finite and positive, reflecting that zero fixed-probe accessibility does not imply zero physical adsorption space; LabuteASA has no training zeros, so no other boundary arises.",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "rejected",
    "reason": "Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references"
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "surface_area_confined_pore_coupling",
    "formula": "log(1 + (LabuteASA / LabuteASA_ref) / (0.1 + AV / AV_ref))",
    "hypothesis": "Entropy loss increases with adsorbate molecular surface area, but only in proportion to how confined the framework is: in frameworks with small probe-accessible specific volume, a large-surface-area adsorbate has more adsorbent-contact degrees of freedom suppressed (fewer accessible translations/orientations), raising entropy loss, whereas in open frameworks the same molecule retains configurational freedom.",
    "rationale": "LabuteASA proxies the number of interaction-contact sites on the molecule; AV proxies framework openness. The product couples molecular contact extent to confinement. The 0.1 offset is an empirical smoothing constant to keep the expression finite at AV = 0 (28 training rows); it carries no universal physical meaning. Limitations: LabuteASA is an implicit-H approximate surface, and AV is a fixed-probe mass-specific accessibility, not molecule-specific free volume.",
    "falsification_criteria": "If the positive partial derivative of entropy loss with respect to LabuteASA at fixed rotor class fails to hold, or if the Spearman association of the descriptor with entropy loss is negative in the native regime, the confinement-coupling mechanism is falsified; a competing mechanism is that surface area correlates with enthalpic binding strength that dominates over entropic confinement.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA stands in for contact-degree suppression; AV stands in for framework openness; both are proxies with representation and probe-dependence limitations, and no causal claim is made.",
      "physical_interpretation": "Native quantities only: molecular surface area and probe-accessible specific volume; the normalized ratios are dimensionless row-varying inputs, and no q-unity equality threshold is asserted.",
      "boundary_behavior": "At AV = 0 (28 training rows) the ratio AV/AV_ref is 0, so the dimensionless offset 0.1 keeps the denominator finite and positive; zero fixed-probe accessibility does not imply zero physical adsorption space. LabuteASA has no training zeros, so no other boundary arises. All quantities are converted to dimensionless form via training references before the addition, so the log argument is unit-compatible and finite for every training row; the 0.1 offset is an empirical smoothing constant with no universal physical meaning.",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
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
        "AV",
        "LabuteASA"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": 0.6831283622787957,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/small_kg_rag_agent/replicate-3/round-3/h2`

最终状态：scored；边际收益：-7.517762 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotational_inertia_entropy_penalty",
    "formula": "rotor_case(log(1 + (PMI1 / PMI1_ref)), log(1 + (PMI2 / PMI2_ref)), log(1 + (PMI2 / PMI2_ref)))",
    "hypothesis": "Entropy loss increases with the rotational inertia proxy of the adsorbate within each rotor class: heavier (larger moment of inertia) molecules lose more rotational configurational freedom upon adsorption in rigid pure-silica frameworks, since confinement suppresses rotational states progressively more for larger inertia at fixed rotor class.",
    "rationale": "PMI1 is used for the single-site branch (54 rows, near-zero PMI2/PMI3 for monoatomic-like species where PMI1 is the only finite moment), and PMI2 for linear and nonlinear branches. The rotor_case branches smooth over representation limits: PMI values are heavy-atom implicit-H proxies, and legitimate zeros in PMI2/PMI3 for single-site species are handled by routing to the single-site branch. Log arguments are dimensionless and finite for all finite native values. Limitations: heavy-atom proxies are not true all-atom inertias, and the branch choice is an empirical convention.",
    "falsification_criteria": "If the partial derivative of predicted entropy loss with respect to PMI2 (rotor class fixed) is not positive, or if within-class association of inertia with entropy loss is negative in the native PMI2 regime [0, 2299.28] for nonlinear rows, the rotational-inertia penalty mechanism is falsified; a competing mechanism is that inertia merely re-expresses molecular weight/volume already captured by retained descriptors.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments stand in for rotational state suppression; single-site species are routed via PMI1; proxy zeros are physical, not missing data.",
      "physical_interpretation": "Native moments of inertia of the implicit-H heavy-atom representation; normalized ratios are dimensionless row-varying inputs; no physical unity threshold is implied.",
      "boundary_behavior": "Single-site rows (PMI2 = PMI3 = 0 legitimately) use the PMI1 branch, which is strictly positive in training, so every row yields a finite value with no imputation.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
        "PMI1",
        "PMI2"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI2": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.40693871290526923,
      "target_association": "consistent",
      "perturbation": 3.956905037,
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
    "name": "rotational_inertia_entropy_penalty",
    "formula": "rotor_case(log(1 + (PMI1 / PMI1_ref)), log(1 + (PMI2 / PMI2_ref)), log(1 + (PMI2 / PMI2_ref)))",
    "hypothesis": "Entropy loss increases with the rotational inertia proxy of the adsorbate within each rotor class: heavier (larger moment of inertia) molecules lose more rotational configurational freedom upon adsorption in rigid pure-silica frameworks, since confinement suppresses rotational states progressively more for larger inertia at fixed rotor class.",
    "rationale": "PMI1 is used for the single-site branch (54 rows, near-zero PMI2/PMI3 for monoatomic-like species where PMI1 is the only finite moment), and PMI2 for linear and nonlinear branches. The rotor_case branches smooth over representation limits: PMI values are heavy-atom implicit-H proxies, and legitimate zeros in PMI2/PMI3 for single-site species are handled by routing to the single-site branch. Log arguments are dimensionless and finite for all finite native values. Limitations: heavy-atom proxies are not true all-atom inertias, and the branch choice is an empirical convention.",
    "falsification_criteria": "If the partial derivative of predicted entropy loss with respect to PMI2 (rotor class fixed) is not positive, or if within-class association of inertia with entropy loss is negative in the native PMI2 regime [0, 2299.28] for nonlinear rows, the rotational-inertia penalty mechanism is falsified; a competing mechanism is that inertia merely re-expresses molecular weight/volume already captured by retained descriptors.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments stand in for rotational state suppression; single-site species are routed via PMI1; proxy zeros are physical, not missing data.",
      "physical_interpretation": "Native moments of inertia of the implicit-H heavy-atom representation; normalized ratios are dimensionless row-varying inputs; no physical unity threshold is implied.",
      "boundary_behavior": "Single-site rows (PMI2 = PMI3 = 0 legitimately) use the PMI1 branch, which is strictly positive in training, so every row yields a finite value with no imputation.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
        "PMI1",
        "PMI2"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI2": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.40693871290526923,
      "target_association": "consistent",
      "perturbation": 3.956905037,
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
    "name": "rotational_inertia_entropy_penalty",
    "formula": "rotor_case(log(1 + (PMI1 / PMI1_ref)), log(1 + (PMI2 / PMI2_ref)), log(1 + (PMI2 / PMI2_ref)))",
    "hypothesis": "Entropy loss increases with the rotational inertia proxy of the adsorbate within each rotor class: heavier (larger moment of inertia) molecules lose more rotational configurational freedom upon adsorption in rigid pure-silica frameworks, since confinement suppresses rotational states progressively more for larger inertia at fixed rotor class.",
    "rationale": "PMI1 is used for the single-site branch (54 rows, near-zero PMI2/PMI3 for monoatomic-like species where PMI1 is the only finite moment), and PMI2 for linear and nonlinear branches. The rotor_case branches smooth over representation limits: PMI values are heavy-atom implicit-H proxies, and legitimate zeros in PMI2/PMI3 for single-site species are handled by routing to the single-site branch. Log arguments are dimensionless and finite for all finite native values. Limitations: heavy-atom proxies are not true all-atom inertias, and the branch choice is an empirical convention.",
    "falsification_criteria": "If the partial derivative of predicted entropy loss with respect to PMI2 (rotor class fixed) is not positive, or if within-class association of inertia with entropy loss is negative in the native PMI2 regime [0, 2299.28] for nonlinear rows, the rotational-inertia penalty mechanism is falsified; a competing mechanism is that inertia merely re-expresses molecular weight/volume already captured by retained descriptors.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments stand in for rotational state suppression; single-site species are routed via PMI1; proxy zeros are physical, not missing data.",
      "physical_interpretation": "Native moments of inertia of the implicit-H heavy-atom representation; normalized ratios are dimensionless row-varying inputs; no physical unity threshold is implied.",
      "boundary_behavior": "Single-site rows (PMI2 = PMI3 = 0 legitimately) use the PMI1 branch, which is strictly positive in training, so every row yields a finite value with no imputation.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
        "PMI1",
        "PMI2"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI2": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.40693871290526923,
      "target_association": "consistent",
      "perturbation": 3.956905037,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/small_kg_rag_agent/replicate-3/round-3/h3`

最终状态：scored；边际收益：-5.848919 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, novelty_status, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, variable_mappings.ASA, variable_mappings.AV

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks the same molecule retains more configurational freedom.",
    "rationale": "This is the round-1 retained descriptor, re-proposed for the h3 slot. Vol proxies molecule size; AV proxies framework openness. The 0.1 offset is an empirical smoothing constant keeping the expression finite at AV = 0 (28 training rows) and carries no universal physical meaning. Limitations: AV is a fixed-probe mass-specific accessibility, not molecule-specific free volume, and Vol is a vdw volume that does not capture shape anisotropy.",
    "falsification_criteria": "If the partial derivative of predicted entropy loss with respect to Vol at fixed rotor class is not positive in the native AV regime, or if within-regime Spearman association with entropy loss turns negative, the accessible-volume-contrast mechanism is falsified; a competing mechanism is that lsd_p (included diameter along path) rather than AV governs the contrast, as tested by the alternative retained descriptor.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol stands in for translational configurational restriction; AV stands in for framework accessible space; both are geometric proxies and no causal claim is asserted.",
      "physical_interpretation": "Native vdw volume and probe-accessible specific volume; normalized ratios are dimensionless row-varying inputs; no physical equality threshold at q = 1 is implied.",
      "boundary_behavior": "At AV = 0 the offset yields a large but finite value, consistent with zero fixed-probe accessibility not implying zero physical adsorption space; Vol has no training zeros, so no other boundary arises.",
      "vary_input": "Vol",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
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
        "AV",
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "reason": "Redundant with a current input"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + ASA / ASA_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks the same molecule retains more configurational freedom.",
    "rationale": "The prior Vol/AV contrast was rejected in precheck as redundant with a current input (AV overlaps the retained round-2 descriptor). Replacing the framework term with ASA, the probe-accessible specific area, keeps the same size-vs-openness contrast while using a distinct mass-specific accessibility quantity: entropy loss increases when a large-vdw-volume molecule occupies frameworks with small probe-accessible specific area. ASA is still a fixed-probe, mass-specific accessibility, not molecule-specific free volume, and the 0.1 offset remains an empirical smoothing constant for the 28 zero-accessibility rows, carrying no universal physical meaning.",
    "falsification_criteria": "If the partial derivative of predicted entropy loss with respect to Vol at fixed rotor class is not positive in the native ASA regime [0, 2874.75], or if the within-regime Spearman association of the descriptor with entropy loss is negative, the area-based contrast mechanism is falsified; a competing mechanism is that the retained lsd_p-based contrast, or enthalpic size effects, already account for the association.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol proxies translational configurational restriction; ASA proxies framework accessible surface/openness; both are geometric proxies, and no causal claim is asserted. Normalized ratios are dimensionless row-varying inputs and q-unity implies no physical equality threshold.",
      "physical_interpretation": "Native vdw volume (angstrom^3) and probe-accessible specific area (m^2/g); no source-specific percentage or coefficient is imported as a universal constant.",
      "boundary_behavior": "At ASA = 0 (28 training rows) the offset keeps the argument finite and positive, reflecting that zero fixed-probe accessibility does not imply zero physical adsorption space; Vol has no training zeros, so no other boundary arises.",
      "vary_input": "Vol",
      "descriptor_direction": "increasing",
      "regime_input": "ASA",
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
        "ASA",
        "Vol"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.49329589835528664,
      "target_association": "consistent",
      "perturbation": 0.7023999999999999,
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
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + ASA / ASA_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks the same molecule retains more configurational freedom.",
    "rationale": "The prior Vol/AV contrast was rejected in precheck as redundant with a current input (AV overlaps the retained round-2 descriptor). Replacing the framework term with ASA, the probe-accessible specific area, keeps the same size-vs-openness contrast while using a distinct mass-specific accessibility quantity: entropy loss increases when a large-vdw-volume molecule occupies frameworks with small probe-accessible specific area. ASA is still a fixed-probe, mass-specific accessibility, not molecule-specific free volume, and the 0.1 offset remains an empirical smoothing constant for the 28 zero-accessibility rows, carrying no universal physical meaning.",
    "falsification_criteria": "If the partial derivative of predicted entropy loss with respect to Vol at fixed rotor class is not positive in the native ASA regime [0, 2874.75], or if the within-regime Spearman association of the descriptor with entropy loss is negative, the area-based contrast mechanism is falsified; a competing mechanism is that the retained lsd_p-based contrast, or enthalpic size effects, already account for the association.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol proxies translational configurational restriction; ASA proxies framework accessible surface/openness; both are geometric proxies, and no causal claim is asserted. Normalized ratios are dimensionless row-varying inputs and q-unity implies no physical equality threshold.",
      "physical_interpretation": "Native vdw volume (angstrom^3) and probe-accessible specific area (m^2/g); no source-specific percentage or coefficient is imported as a universal constant.",
      "boundary_behavior": "At ASA = 0 (28 training rows) the offset keeps the argument finite and positive, reflecting that zero fixed-probe accessibility does not imply zero physical adsorption space; Vol has no training zeros, so no other boundary arises.",
      "vary_input": "Vol",
      "descriptor_direction": "increasing",
      "regime_input": "ASA",
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
        "ASA",
        "Vol"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.49329589835528664,
      "target_association": "consistent",
      "perturbation": 0.7023999999999999,
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
    "full_index_rows_in_task_scope": 6004,
    "pending_source_review": [
      {
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6fab6b0978c4d29070fba0dc",
        "paper_id": "doi:10.1021/acs.chemrev.3c00801",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9805f0a944c903cd7580bbcb",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f0a5a652a4377235ec566770",
        "paper_id": "doi:10.1007/s00894-008-0417-6",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:16e2b39b6d98fe8886d05f3e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2cab4c5858c1d76e029f2dbd",
        "paper_id": "pmc:pmc10979502",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:43dedbc998f9c278eea622b0",
        "paper_id": "pmc:pmc9739862",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:522d58342ca7e271d4501291",
        "paper_id": "doi:10.26434/chemrxiv.11695482.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:560d540c09c85dfa3faa0e8c",
        "paper_id": "doi:10.1021/acs.jpcb.1c02929",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cc904c61f240366bfe7825e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c5d1446664ef3ac88a98d251",
        "paper_id": "doi:10.1039/d5tb00256g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d6ea1a200a0f892c276c47fa",
        "paper_id": "doi:10.1021/acs.jctc.4c00236",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e3ee147f884c3f765d75e734",
        "paper_id": "pmc:pmc10050162",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e516c57edc2303f716b18822",
        "paper_id": "doi:10.1021/jp0488362",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:0073e59a7f2489677568aec4",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:06a26a29dca2516a90c93ace",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement Entropy loss increases with adsorbate molecular surface area, but only in proportion to how confined the framework is: in frameworks with small probe-accessible specific volume, a large-surface-area adsorbate has more adsorbent-contact degrees of freedom suppressed (fewer accessible translations/orientations), raising entropy loss, whereas in open frameworks the same molecule retains configurational freedom. log(1 + (LabuteASA / LabuteASA_ref) * (AV_ref / (0.1 + AV))) Entropy loss increases with the rotational inertia proxy of the adsorbate within each rotor class: heavier (larger moment of inertia) molecules lose more rotational configurational freedom upon adsorption in rigid pure-silica frameworks, since confinement suppresses rotational states progressively more for larger inertia at fixed rotor class. rotor_case(log(1 + (PMI1 / PMI1_ref)), log(1 + (PMI2 / PMI2_ref)), log(1 + (PMI2 / PMI2_ref))) Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks the same molecule retains more configurational freedom. log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:65209fe749e6f7590f4dd3bc",
      "chunk:e98dff054a73e56b28f6bdf3"
    ],
    "items": 10,
    "lexical_tokens": 4774,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [
    {
      "record_id": "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "paper_id": "pmc:pmc6161062",
      "document_id": "document:7ba8c366c10dc56ab9a75bda",
      "quote": "Linear alkanes lose approximately 38% of their gas-phase entropy upon adsorption in MFI, a medium pore zeolite, while experiencing a smaller loss of 20% in the larger pore FAU framework.",
      "locator": {
        "kind": "pdf_page",
        "page": 1
      },
      "applicability": {
        "source_conditions": "Reported zeolite adsorption comparison; linear alkanes, MFI and FAU. Temperature, loading and framework chemistry are not fully resolved in this excerpt.",
        "transfer_assumptions": [
          "Transfer to pure-silica rigid frameworks at infinite dilution remains a hypothesis.",
          "Source-specific percentages and fitted coefficients must not become universal constants.",
          "Cavity diameter and lsd_f/lsd_p are different geometric quantities; proxy mapping must be justified."
        ],
        "proxy_inputs": [
          "AV",
          "lsd_f",
          "lsd_p",
          "Vol"
        ],
        "proxy_caveat": "D0 inputs are proxies, not measurements of lost freedom. AV is per framework mass, not molecular free volume. Normalized ratios do not preserve physical threshold 1.",
        "status": "conditional_use"
      },
      "id": "E04"
    },
    {
      "record_id": "chunk:e9ae89d415e72e1faf77faf0",
      "paper_id": "doi:10.1021/acs.jpcc.0c02671",
      "document_id": "document:679638c993b24ed3004656c6",
      "quote": "combinations , it remains overwhelming to apply them to the millions of hypothetical frameworks . Novel topology-based , data-driven approaches have been shown to be adequate in predicting specific features such as adsorption capacity $ ^ { 6 } $ and selectivity . $ ^ { 26 } $ However , there are currently no similar models for entropy . The use of empirical correlations offers an expedient route in predicting sensible thermodynamic quantities without resorting to experiments or simulations. De Moor et al. $ ^{12} $ used ab initio simulations to show that adsorption enthalpies and entropies for n-alkanes within acidic zeolites are linearly correlated with their carbon number. Campbell and Sellers compiled a collection of experimental alkane entropies on two-dimensional (2D) catalytic surfaces. $ ^{27,28} $ The key finding of their work was that the ratio of the adsorbed-phase entropy to the gas-phase entropy was approximately two-thirds. They proposed a general and elegant explanation, suggesting that the adsorption of a molecule from an unhindered gas phase onto a two-dimensional surface would eliminate a dimension of translational freedom, i.e., the adsorbate behaves as a 2D gas. This correlation was found to hold across many molecules, spanning 50R of entropy space with a standard deviation of only 2R (where R is the universal gas constant). Campbell and Sellers' correlation was observed for other two-dimensional surfaces: Otyepková et al. calculated the adsorption entropy of a chemically diverse set of molecules adsorbed onto organic \"van der Waals\" materials using inverse gas chromatography and ab initio simulations. $ ^{29,30} $ Their results showed an entropic loss of approximately 40% relative to the gas-phase entropy. Likewise, Budi et al. calculated the adsorption entropy of a set of chemically diverse molecules adsorbed on mineral surfaces using density functional theory. $ ^{31} $ Although predicting a larger entropic loss relative to Campbell and Sellers' correlation, their data showed a strong linear dependence between the adsorbed-phase entropy and the gas-phase entropy. Dauenhauer and Abdelrhaman $ ^{13} $ expanded this idea to three-dimensional frameworks by compiling experimentally determined adsorption entropies for alkanes adsorbed in nine aluminosilicate zeolites. They showed that the entropic loss upon adsorption can be linearly correlated with the molecule's gas-phase translational and rotational entropies and that the occupiable volume of a zeolite is a useful descriptor in predicting such losses.",
      "locator": {
        "section": "introduction",
        "page": 1
      },
      "applicability": {
        "record_id": "chunk:8ee2f667b946a68346bce30b",
        "paper_id": "doi:10.1021/acs.jpcc.0c02671",
        "decision": "conditional_use",
        "reason": "Relevant adsorption-entropy mechanism or approximation caveat, with original qualifications retained",
        "source_conditions": "See preserved original passage; source method and target-regime transfer are not presumed identical",
        "transfer_assumptions": [
          "No outcome-fitted coefficient, quoted percentage, or source-specific geometry becomes a universal constant.",
          "Any available D0 quantity used as a proxy requires an explicit mapping and limitation."
        ],
        "status": "conditional_use"
      },
      "id": "E07"
    }
  ],
  "mechanism_cards": [
    {
      "mechanism_id": "mfi_fau_rotation",
      "evidence_id": "E01",
      "applicability": {
        "source_conditions": "Reported zeolite adsorption comparison; linear alkanes, MFI and FAU. Temperature, loading and framework chemistry are not fully resolved in this excerpt.",
        "transfer_assumptions": [
          "Transfer to pure-silica rigid frameworks at infinite dilution remains a hypothesis.",
          "Source-specific percentages and fitted coefficients must not become universal constants.",
          "Cavity diameter and lsd_f/lsd_p are different geometric quantities; proxy mapping must be justified."
        ],
        "proxy_inputs": [
          "lsd_f",
          "lsd_p",
          "PMI1",
          "PMI2",
          "PMI3"
        ],
        "proxy_caveat": "D0 inputs are proxies, not measurements of lost freedom. AV is per framework mass, not molecular free volume. Normalized ratios do not preserve physical threshold 1.",
        "status": "conditional_use"
      },
      "relation": "GREATER_REPORTED_LOSS",
      "subject": "framework confinement in MFI relative to FAU",
      "object": "loss of adsorbate rotational degrees of freedom"
    },
    {
      "mechanism_id": "cavity_rotation",
      "evidence_id": "E02",
      "applicability": {
        "source_conditions": "Reported zeolite adsorption comparison; FER/FAU cavity comparison. Temperature, loading and framework chemistry are not fully resolved in this excerpt.",
        "transfer_assumptions": [
          "Transfer to pure-silica rigid frameworks at infinite dilution remains a hypothesis.",
          "Source-specific percentages and fitted coefficients must not become universal constants.",
          "Cavity diameter and lsd_f/lsd_p are different geometric quantities; proxy mapping must be justified."
        ],
        "proxy_inputs": [
          "lsd_f",
          "lsd_p",
          "GeDi"
        ],
        "proxy_caveat": "D0 inputs are proxies, not measurements of lost freedom. AV is per framework mass, not molecular free volume. Normalized ratios do not preserve physical threshold 1.",
        "status": "conditional_use"
      },
      "relation": "GREATER_REPORTED_LOSS",
      "subject": "smaller cavity diameter in the reported FER/FAU comparison",
      "object": "loss of adsorbate rotational entropy"
    },
    {
      "mechanism_id": "translation_rotation",
      "evidence_id": "E03",
      "applicability": {
        "source_conditions": "Reported zeolite adsorption comparison; translation and rotation of adsorbates. Temperature, loading and framework chemistry are not fully resolved in this excerpt.",
        "transfer_assumptions": [
          "Transfer to pure-silica rigid frameworks at infinite dilution remains a hypothesis.",
          "Source-specific percentages and fitted coefficients must not become universal constants.",
          "Cavity diameter and lsd_f/lsd_p are different geometric quantities; proxy mapping must be justified."
        ],
        "proxy_inputs": [
          "AV",
          "Vol",
          "PMI1",
          "PMI2",
          "PMI3"
        ],
        "proxy_caveat": "D0 inputs are proxies, not measurements of lost freedom. AV is per framework mass, not molecular free volume. Normalized ratios do not preserve physical threshold 1.",
        "status": "conditional_use"
      },
      "relation": "REPORTED_CONTRIBUTIONS",
      "subject": "adsorbate translational and rotational motions",
      "object": "adsorption entropy losses"
    },
    {
      "mechanism_id": "mfi_fau_entropy",
      "evidence_id": "E04",
      "applicability": {
        "source_conditions": "Reported zeolite adsorption comparison; linear alkanes, MFI and FAU. Temperature, loading and framework chemistry are not fully resolved in this excerpt.",
        "transfer_assumptions": [
          "Transfer to pure-silica rigid frameworks at infinite dilution remains a hypothesis.",
          "Source-specific percentages and fitted coefficients must not become universal constants.",
          "Cavity diameter and lsd_f/lsd_p are different geometric quantities; proxy mapping must be justified."
        ],
        "proxy_inputs": [
          "AV",
          "lsd_f",
          "lsd_p",
          "Vol"
        ],
        "proxy_caveat": "D0 inputs are proxies, not measurements of lost freedom. AV is per framework mass, not molecular free volume. Normalized ratios do not preserve physical threshold 1.",
        "status": "conditional_use"
      },
      "relation": "GREATER_REPORTED_LOSS",
      "subject": "MFI relative to larger-pore FAU for linear alkanes",
      "object": "fraction of gas-phase entropy lost on adsorption"
    },
    {
      "mechanism_id": "rrho_mobility",
      "evidence_id": "E05",
      "applicability": {
        "source_conditions": "Review of hydrocarbon adsorption calculations at zeolite active sites; not a direct pure-silica universal law",
        "transfer_assumptions": [
          "Source claim is conditional and does not demonstrate the relation in this benchmark.",
          "PMI and pore diameters are imperfect proxies for rotational freedom; preserve the distinction between cages and free-path diameters."
        ],
        "proxy_inputs": [
          "PMI1",
          "PMI2",
          "PMI3",
          "lsd_f",
          "lsd_p"
        ],
        "proxy_caveat": "This source motivates an explicitly testable hypothesis; it supplies no fitted formula coefficients.",
        "status": "conditional_use"
      },
      "relation": "REPORTED_APPROXIMATION_LIMITATION",
      "subject": "immobile RRHO treatment of guest molecules",
      "object": "adsorption entropy error when retained mobility is neglected"
    },
    {
      "mechanism_id": "cage_rotational_equilibrium",
      "evidence_id": "E06",
      "applicability": {
        "source_conditions": "Linear and singly branched molecules predominantly in MCM-22 supercages; source also discusses diffusion at 450–850 K. Transfer to all frameworks and 298 K unproven",
        "transfer_assumptions": [
          "Source claim is conditional and does not demonstrate the relation in this benchmark.",
          "PMI and pore diameters are imperfect proxies for rotational freedom; preserve the distinction between cages and free-path diameters."
        ],
        "proxy_inputs": [
          "PMI1",
          "PMI2",
          "PMI3",
          "GeDi",
          "lsd_f",
          "lsd_p"
        ],
        "proxy_caveat": "This source motivates an explicitly testable hypothesis; it supplies no fitted formula coefficients.",
        "status": "conditional_use"
      },
      "relation": "SOURCE_PROPOSES_POSSIBLE_EFFECT",
      "subject": "differences in molecular rotational freedom inside MCM-22 supercages",
      "object": "adsorption equilibrium"
    }
  ]
}
```
