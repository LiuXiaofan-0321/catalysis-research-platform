# low/rag_agent/replicate-3/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`low/rag_agent/replicate-3/round-1/h1`

最终状态：scored；边际收益：-3.057526 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confined_translator",
    "formula": "log(1 + q_lsd_f) * (MW / MW_ref) ** 0.5",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss grows with adsorbate molecular weight but is moderated by the framework passing bottleneck (Df): larger bottleneck free spheres permit more adsorbed-state translation, so entropy loss decreases with lsd_f at fixed adsorbate size, hence s_ads/s_gas increases with lsd_f for heavier adsorbates.",
    "rationale": "Heavy molecules lose more gas-phase translational entropy upon confinement; the bottleneck Df controls how much adsorbed-state wandering remains. This is an empirical proxy hypothesis from steric confinement theory; Df is a passing-sphere bottleneck, not the global cavity diameter, so it may under-represent large-cage frameworks.",
    "falsification_criteria": "If D0-derived entropy loss is uncorrelated (or anti-correlated) with lsd_f within fixed-MW bins, or if lsd_p (included sphere along path) explains variance better than lsd_f, the bottleneck-moderation mechanism is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "MW proxies gas-phase translational entropy scale; Df proxies confinement strength; both are coarse geometric surrogates with no quantum or vibrational content.",
      "physical_interpretation": "q_lsd_f is a dimensionless normalized bottleneck proxy; no physical meaning attaches to q_lsd_f = 1.",
      "boundary_behavior": "Formula is finite across the full training domain since lsd_f and MW are strictly positive; the log smooths small-bottleneck frameworks without invoking a physical threshold.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "MW",
      "regime_train_quantiles": [
        0.25,
        0.75
      ],
      "entropy_direction": "decreasing"
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1213,
      "native_regime_bounds": [
        56.06260026,
        102.1044651
      ],
      "training_spearman": -0.26859757103543364,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
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
    "slot_id": "h1",
    "name": "bottleneck_confined_translator",
    "formula": "log(1 + q_lsd_f) * (MW / MW_ref) ** 0.5",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss grows with adsorbate molecular weight but is moderated by the framework passing bottleneck (Df): larger bottleneck free spheres permit more adsorbed-state translation, so entropy loss decreases with lsd_f at fixed adsorbate size, hence s_ads/s_gas increases with lsd_f for heavier adsorbates.",
    "rationale": "Heavy molecules lose more gas-phase translational entropy upon confinement; the bottleneck Df controls how much adsorbed-state wandering remains. This is an empirical proxy hypothesis from steric confinement theory; Df is a passing-sphere bottleneck, not the global cavity diameter, so it may under-represent large-cage frameworks.",
    "falsification_criteria": "If D0-derived entropy loss is uncorrelated (or anti-correlated) with lsd_f within fixed-MW bins, or if lsd_p (included sphere along path) explains variance better than lsd_f, the bottleneck-moderation mechanism is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "MW proxies gas-phase translational entropy scale; Df proxies confinement strength; both are coarse geometric surrogates with no quantum or vibrational content.",
      "physical_interpretation": "q_lsd_f is a dimensionless normalized bottleneck proxy; no physical meaning attaches to q_lsd_f = 1.",
      "boundary_behavior": "Formula is finite across the full training domain since lsd_f and MW are strictly positive; the log smooths small-bottleneck frameworks without invoking a physical threshold.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "MW",
      "regime_train_quantiles": [
        0.25,
        0.75
      ],
      "entropy_direction": "decreasing"
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1213,
      "native_regime_bounds": [
        56.06260026,
        102.1044651
      ],
      "training_spearman": -0.26859757103543364,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
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
    "name": "bottleneck_confined_translator",
    "formula": "log(1 + q_lsd_f) * (MW / MW_ref) ** 0.5",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss grows with adsorbate molecular weight but is moderated by the framework passing bottleneck (Df): larger bottleneck free spheres permit more adsorbed-state translation, so entropy loss decreases with lsd_f at fixed adsorbate size, hence s_ads/s_gas increases with lsd_f for heavier adsorbates.",
    "rationale": "Heavy molecules lose more gas-phase translational entropy upon confinement; the bottleneck Df controls how much adsorbed-state wandering remains. This is an empirical proxy hypothesis from steric confinement theory; Df is a passing-sphere bottleneck, not the global cavity diameter, so it may under-represent large-cage frameworks.",
    "falsification_criteria": "If D0-derived entropy loss is uncorrelated (or anti-correlated) with lsd_f within fixed-MW bins, or if lsd_p (included sphere along path) explains variance better than lsd_f, the bottleneck-moderation mechanism is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "MW proxies gas-phase translational entropy scale; Df proxies confinement strength; both are coarse geometric surrogates with no quantum or vibrational content.",
      "physical_interpretation": "q_lsd_f is a dimensionless normalized bottleneck proxy; no physical meaning attaches to q_lsd_f = 1.",
      "boundary_behavior": "Formula is finite across the full training domain since lsd_f and MW are strictly positive; the log smooths small-bottleneck frameworks without invoking a physical threshold.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "MW",
      "regime_train_quantiles": [
        0.25,
        0.75
      ],
      "entropy_direction": "decreasing"
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1213,
      "native_regime_bounds": [
        56.06260026,
        102.1044651
      ],
      "training_spearman": -0.26859757103543364,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/rag_agent/replicate-3/round-1/h2`

最终状态：scored；边际收益：+1.211246 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, formula, novelty_status, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_volume_entropy_reservoir",
    "formula": "log(1 + AV/AV_ref) / (Vol / Vol_ref) ** 0.5",
    "hypothesis": "Entropy loss at infinite dilution decreases with the probe-accessible specific volume (AV) of the framework and increases with adsorbate van der Waals volume (Vol): frameworks offering more accessible space preserve more adsorbed-phase configurational/vibrational freedom, while bulky molecules lose more entropy upon docking.",
    "rationale": "AV is a fixed-probe, mass-specific accessibility measure, not molecule-specific free volume; this mismatch is a declared proxy limitation. Vol proxies the molecule's steric demand. The mechanism is configurational freedom, not kinetic escape, which alone does not determine equilibrium entropy.",
    "falsification_criteria": "If frameworks with AV = 0 (inaccessible to the geometric probe) do not show systematically larger entropy loss than high-AV frameworks for molecules they do adsorb, the probe-volume proxy mechanism is falsified; a competing shape/cavity-shape mechanism would then be favored.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe AV is assumed monotone with molecule-accessible space for the adsorbates studied; this fails for molecules near or larger than the probe, and AV = 0 rows rely on other channels for adsorption.",
      "physical_interpretation": "AV/AV_ref is a dimensionless row-varying accessibility ratio; the log(1+·) form is an empirical smoothing with no physical unity threshold.",
      "boundary_behavior": "At AV = 0 (28 training rows) log(1+0)=0, giving a finite descriptor of 0: zero fixed-probe accessibility maps to maximal entropy loss in this descriptor, an explicit empirical choice, not a physical law.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
      "regime_train_quantiles": [
        0.1,
        0.9
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
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1909,
      "native_regime_bounds": [
        37.872,
        108.112
      ],
      "training_spearman": -0.6305624166411415,
      "target_association": "contradicted",
      "perturbation": 0.001538232,
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
    "name": "accessible_volume_entropy_reservoir",
    "formula": "((Vol / Vol_ref) ** 0.5) / log(1 + AV / AV_ref)",
    "hypothesis": "Entropy loss at infinite dilution decreases with the probe-accessible specific volume (AV) of the framework and increases with adsorbate van der Waals volume (Vol): frameworks offering more accessible space preserve more adsorbed-phase configurational/vibrational freedom, while bulky molecules lose more entropy upon docking.",
    "rationale": "The training-only precheck contradicted the original increasing descriptor (Spearman -0.63): empirically, higher probe-accessible volume associates with LOWER entropy loss, consistent with E02 (smaller cavities lose more rotational entropy) and E04 (larger-pore FAU shows smaller fractional entropy loss than MFI). The descriptor was inverted so the descriptor-decreasing-in-AV form carries the declared increasing entropy-loss direction. Mechanism remains configurational freedom, not kinetic escape; association is not causation.",
    "falsification_criteria": "If, within fixed-Vol bins, entropy loss no longer decreases with the inverted AV descriptor, or if lsd_f/lsd_p cavity-size descriptors explain more variance than probe accessibility, the accessible-volume-reservoir mechanism is falsified in favor of a cavity-diameter mechanism.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E02",
      "E04",
      "E09"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe AV is assumed monotone with molecule-accessible space for the adsorbates studied; this fails for molecules near or larger than the probe. AV is mass-specific accessibility, not molecule-specific free volume; the mapping to configurational freedom is a declared proxy limitation. No source coefficient becomes a universal constant (C4, C7).",
      "physical_interpretation": "AV/AV_ref is a dimensionless row-varying accessibility ratio; Vol/Vol_ref is a dimensionless row-varying steric-demand ratio. Neither ratio unity carries a physical threshold meaning. The descriptor decreases with AV and increases with Vol, matching the predeclared entropy-loss direction.",
      "boundary_behavior": "At AV = 0 (28 training rows), log(1+0)=0 makes the ratio undefined; to keep every training row finite, use the equivalent finite form (Vol/Vol_ref)**0.5 * (1 + AV_ref / maximum(AV, AV_ref)) which equals 2*(Vol/Vol_ref)**0.5 at AV=0 and approaches (Vol/Vol_ref)**0.5 for large AV. This is an empirical smoothing choice, not a physical law.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "Vol",
      "regime_train_quantiles": [
        0.1,
        0.9
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
    "domain_failure": {
      "invalid_n": 28,
      "invalid_fraction": 0.011859381617958492,
      "zero_variables_on_invalid_rows": {
        "Vol": 0,
        "AV": 28
      },
      "nonfinite_rule": "Every training row must have a finite feature; physical zeros are not imputed."
    },
    "reason": "Formula undefined on observed training support; use a justified finite proxy or explicit rotor branches"
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_volume_entropy_reservoir",
    "formula": "((Vol / Vol_ref) ** 0.5) * (1 + AV_ref / maximum(AV, AV_ref))",
    "hypothesis": "Entropy loss at infinite dilution decreases with the probe-accessible specific volume (AV) of the framework and increases with adsorbate van der Waals volume (Vol): frameworks offering more accessible space preserve more adsorbed-phase configurational/vibrational freedom, while bulky molecules lose more entropy upon docking.",
    "rationale": "The training-only precheck contradicted the original increasing descriptor (Spearman -0.63): empirically, higher probe-accessible volume associates with LOWER entropy loss, consistent with E02 (smaller cavities lose more rotational entropy) and E04 (larger-pore FAU shows smaller fractional entropy loss than MFI). The descriptor was inverted so the descriptor-decreasing-in-AV form carries the declared increasing entropy-loss direction. Mechanism remains configurational freedom, not kinetic escape; association is not causation.",
    "falsification_criteria": "If, within fixed-Vol bins, entropy loss no longer decreases with the inverted AV descriptor, or if lsd_f/lsd_p cavity-size descriptors explain more variance than probe accessibility, the accessible-volume-reservoir mechanism is falsified in favor of a cavity-diameter mechanism.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E02",
      "E04",
      "E09"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe AV is assumed monotone with molecule-accessible space for the adsorbates studied; this fails for molecules near or larger than the probe. AV is mass-specific accessibility, not molecule-specific free volume; the mapping to configurational freedom is a declared proxy limitation. No source coefficient becomes a universal constant (C4, C7).",
      "physical_interpretation": "AV/AV_ref is a dimensionless row-varying accessibility ratio; Vol/Vol_ref is a dimensionless row-varying steric-demand ratio. Neither ratio unity carries a physical threshold meaning. The descriptor decreases with AV and increases with Vol, matching the predeclared entropy-loss direction.",
      "boundary_behavior": "Finite on the full training domain. At AV = 0 (28 training rows, zero accessibility for the fixed geometric probe), maximum(AV, AV_ref) = AV_ref > 0, so the descriptor equals 2*(Vol/Vol_ref)**0.5; for large AV it decreases toward (Vol/Vol_ref)**0.5. The maximum() clamp is an empirical smoothing choice to avoid division by the legitimate physical zero AV = 0 (zero fixed-probe accessibility does not imply zero molecular adsorption space); it is not a physical threshold or imputed value. The descriptor remains decreasing in AV and increasing in Vol, consistent with the stored hypothesis and entropy_direction.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "Vol",
      "regime_train_quantiles": [
        0.1,
        0.9
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
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1909,
      "native_regime_bounds": [
        37.872,
        108.112
      ],
      "training_spearman": 0.5402686474228463,
      "target_association": "consistent",
      "perturbation": 0.001538232,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/rag_agent/replicate-3/round-1/h3`

最终状态：scored；边际收益：-2.659050 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "rotor_case_shape_quenching",
    "formula": "rotor_case(log(1 + q_SPAN), log(1 + (SPAN/SPAN_ref) * (PBF/PBF_ref + 1)), log(1 + (SPAN/SPAN_ref) ** 2 * (PMI3/PMI3_ref) ** 0.25))",
    "hypothesis": "Adsorbed-phase rotational entropy loss depends on rotor class and molecular shape: single-site molecules (e.g., methane) lose little rotational entropy and depend only weakly on size; linear molecules lose rotation mainly through planarity-aligned confinement (PBF scaling); nonlinear molecules lose rotational entropy roughly with the square of enclosing radius times a weak moment-of-inertia factor, reflecting hindered tumbling in cages.",
    "rationale": "Rotor classes are defined by PMI-proxy categories in the training table (54 single-site, 214 linear, 2093 nonlinear rows); the descriptors use heavy-atom shape proxies (SPAN, PBF, PMI3), not true all-atom moments of inertia. The branch structure is an empirical smoothing choice; exponents are fixed and carry no universal meaning.",
    "falsification_criteria": "If within-class correlations of entropy loss with SPAN (or SPAN×PBF, or SPAN²·PMI3^0.25) do not show the predeclared increasing association, or if a single unified shape descriptor outperforms all three branches, the rotor-dependent shape-quenching hypothesis is falsified in favor of a rotor-agnostic size mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "PBF": "heavy_atom_planarity",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom SPAN/PBF/PMI3 proxy rotational hinderance; legitimate zero values in these proxies (e.g., single diatomic-like rows) are handled by the additive +1 inside PBF scaling and the log(1+·) smoothing, not by imputation.",
      "physical_interpretation": "q_SPAN and SPAN/SPAN_ref are the same dimensionless ratio; no branch switch or physical transition occurs at ratio unity.",
      "boundary_behavior": "Single-site branch is finite for all SPAN ≥ 0; linear branch stays finite at PBF = 0 via the +1 term; nonlinear branch stays finite at SPAN = 0 and PMI3 = 0 since base 1 plus nonnegative terms; all three branches yield compatible dimensionless descriptor values.",
      "vary_input": "SPAN",
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
        "PBF",
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
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
      "training_spearman": 0.40377462750345666,
      "target_association": "consistent",
      "perturbation": 0.02159332416,
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
    "slot_id": "h3",
    "name": "rotor_case_shape_quenching",
    "formula": "rotor_case(log(1 + q_SPAN), log(1 + (SPAN/SPAN_ref) * (PBF/PBF_ref + 1)), log(1 + (SPAN/SPAN_ref) ** 2 * (PMI3/PMI3_ref) ** 0.25))",
    "hypothesis": "Adsorbed-phase rotational entropy loss depends on rotor class and molecular shape: single-site molecules (e.g., methane) lose little rotational entropy and depend only weakly on size; linear molecules lose rotation mainly through planarity-aligned confinement (PBF scaling); nonlinear molecules lose rotational entropy roughly with the square of enclosing radius times a weak moment-of-inertia factor, reflecting hindered tumbling in cages.",
    "rationale": "Rotor classes are defined by PMI-proxy categories in the training table (54 single-site, 214 linear, 2093 nonlinear rows); the descriptors use heavy-atom shape proxies (SPAN, PBF, PMI3), not true all-atom moments of inertia. The branch structure is an empirical smoothing choice; exponents are fixed and carry no universal meaning.",
    "falsification_criteria": "If within-class correlations of entropy loss with SPAN (or SPAN×PBF, or SPAN²·PMI3^0.25) do not show the predeclared increasing association, or if a single unified shape descriptor outperforms all three branches, the rotor-dependent shape-quenching hypothesis is falsified in favor of a rotor-agnostic size mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "PBF": "heavy_atom_planarity",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom SPAN/PBF/PMI3 proxy rotational hinderance; legitimate zero values in these proxies (e.g., single diatomic-like rows) are handled by the additive +1 inside PBF scaling and the log(1+·) smoothing, not by imputation.",
      "physical_interpretation": "q_SPAN and SPAN/SPAN_ref are the same dimensionless ratio; no branch switch or physical transition occurs at ratio unity.",
      "boundary_behavior": "Single-site branch is finite for all SPAN ≥ 0; linear branch stays finite at PBF = 0 via the +1 term; nonlinear branch stays finite at SPAN = 0 and PMI3 = 0 since base 1 plus nonnegative terms; all three branches yield compatible dimensionless descriptor values.",
      "vary_input": "SPAN",
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
        "PBF",
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
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
      "training_spearman": 0.40377462750345666,
      "target_association": "consistent",
      "perturbation": 0.02159332416,
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
    "name": "rotor_case_shape_quenching",
    "formula": "rotor_case(log(1 + q_SPAN), log(1 + (SPAN/SPAN_ref) * (PBF/PBF_ref + 1)), log(1 + (SPAN/SPAN_ref) ** 2 * (PMI3/PMI3_ref) ** 0.25))",
    "hypothesis": "Adsorbed-phase rotational entropy loss depends on rotor class and molecular shape: single-site molecules (e.g., methane) lose little rotational entropy and depend only weakly on size; linear molecules lose rotation mainly through planarity-aligned confinement (PBF scaling); nonlinear molecules lose rotational entropy roughly with the square of enclosing radius times a weak moment-of-inertia factor, reflecting hindered tumbling in cages.",
    "rationale": "Rotor classes are defined by PMI-proxy categories in the training table (54 single-site, 214 linear, 2093 nonlinear rows); the descriptors use heavy-atom shape proxies (SPAN, PBF, PMI3), not true all-atom moments of inertia. The branch structure is an empirical smoothing choice; exponents are fixed and carry no universal meaning.",
    "falsification_criteria": "If within-class correlations of entropy loss with SPAN (or SPAN×PBF, or SPAN²·PMI3^0.25) do not show the predeclared increasing association, or if a single unified shape descriptor outperforms all three branches, the rotor-dependent shape-quenching hypothesis is falsified in favor of a rotor-agnostic size mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "PBF": "heavy_atom_planarity",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom SPAN/PBF/PMI3 proxy rotational hinderance; legitimate zero values in these proxies (e.g., single diatomic-like rows) are handled by the additive +1 inside PBF scaling and the log(1+·) smoothing, not by imputation.",
      "physical_interpretation": "q_SPAN and SPAN/SPAN_ref are the same dimensionless ratio; no branch switch or physical transition occurs at ratio unity.",
      "boundary_behavior": "Single-site branch is finite for all SPAN ≥ 0; linear branch stays finite at PBF = 0 via the +1 term; nonlinear branch stays finite at SPAN = 0 and PMI3 = 0 since base 1 plus nonnegative terms; all three branches yield compatible dimensionless descriptor values.",
      "vary_input": "SPAN",
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
        "PBF",
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
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
      "training_spearman": 0.40377462750345666,
      "target_association": "consistent",
      "perturbation": 0.02159332416,
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
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:869af4527dd765744b7ebc76",
        "paper_id": "pmc:pmc8659101",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:560d540c09c85dfa3faa0e8c",
        "paper_id": "doi:10.1021/acs.jpcb.1c02929",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c515aa77b0e6afe8275e4595",
        "paper_id": "doi:10.1039/d5cs00613a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:147fa339122edc3ff44ba658",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:45c6c30e39c58cf298acb495",
        "paper_id": "pmc:pmc8113345",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:4ee093d81da6b5c01358e0ca",
        "paper_id": "doi:10.1021/acs.jctc.5c01100",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss grows with adsorbate molecular weight but is moderated by the framework passing bottleneck (Df): larger bottleneck free spheres permit more adsorbed-state translation, so entropy loss decreases with lsd_f at fixed adsorbate size, hence s_ads/s_gas increases with lsd_f for heavier adsorbates. log(1 + q_lsd_f) * (MW / MW_ref) ** 0.5 Entropy loss at infinite dilution decreases with the probe-accessible specific volume (AV) of the framework and increases with adsorbate van der Waals volume (Vol): frameworks offering more accessible space preserve more adsorbed-phase configurational/vibrational freedom, while bulky molecules lose more entropy upon docking. log(1 + AV/AV_ref) / (Vol / Vol_ref) ** 0.5 Adsorbed-phase rotational entropy loss depends on rotor class and molecular shape: single-site molecules (e.g., methane) lose little rotational entropy and depend only weakly on size; linear molecules lose rotation mainly through planarity-aligned confinement (PBF scaling); nonlinear molecules lose rotational entropy roughly with the square of enclosing radius times a weak moment-of-inertia factor, reflecting hindered tumbling in cages. rotor_case(log(1 + q_SPAN), log(1 + (SPAN/SPAN_ref) * (PBF/PBF_ref + 1)), log(1 + (SPAN/SPAN_ref) ** 2 * (PMI3/PMI3_ref) ** 0.25))",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:8dd99e6f4fc8a3c4e46d940b",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:4e0a09f3bacb310a3d0b505c"
    ],
    "items": 10,
    "lexical_tokens": 4763,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [
    {
      "record_id": "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "paper_id": "pmc:pmc6161062",
      "document_id": "document:7ba8c366c10dc56ab9a75bda",
      "quote": "Also, more rotational entropy was lost in smaller pore zeolites (FER $ \\sim $ 4.3 Å) when compared to larger pore zeolites (FAU $ \\sim $ 13 Å); in this case, the average cavity diameter is a descriptor for zeolite framework and indicates the extent of confinement.",
      "locator": {
        "kind": "pdf_page",
        "page": 1
      },
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
      "id": "E02"
    },
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
      "id": "E09"
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
