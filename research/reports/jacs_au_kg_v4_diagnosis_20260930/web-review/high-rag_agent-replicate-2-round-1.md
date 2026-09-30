# high/rag_agent/replicate-2/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/rag_agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`high/rag_agent/replicate-2/round-1/h1`

最终状态：scored；边际收益：+1.262050 pp；保留：True。

复核改动字段：evidence_ids, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_volume_confinement",
    "formula": "log((q_Vol**(0.3333333333)) / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because tighter passage relative to molecular size reduces the accessible translational configuration space.",
    "rationale": "Translational confinement at infinite dilution is governed by the free volume actually reachable by a molecule of a given size; Zeo++ Df (lsd_f) is the largest free sphere that can pass through the periodic path, so a molecule whose cubic volume scale approaches the bottleneck experiences strong translational restriction. The descriptor is a dimensionless re-expression of two native inputs (Vol, lsd_f) already present in the nonlinear ANN baseline; it adds interpretability, not new information. Limitation: Df is a geometric bottleneck proxy, not a global cavity diameter, and vdW volume is not the kinetic diameter seen by the framework.",
    "falsification_criteria": "If entropy loss computed from published D0 values shows no monotone positive association with (Vol)^(1/3)/Df across the training domain, or if frameworks with equal Df but different pore connectivity (e.g., 1D channels vs 3D cages) show systematically different entropy loss at the same descriptor value, the confinement-ratio mechanism is falsified in favor of a connectivity or multi-site mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "(Vol)^(1/3) is a length-scale proxy for the molecule and lsd_f (Df) is a bottleneck proxy only; neither is the true kinetic dimension nor the global cavity diameter Di. Both proxies are transferable only within this rigid pure-silica, infinite-dilution regime.",
      "physical_interpretation": "Vol is the native vdW volume; lsd_f is the native passing free sphere. q_Vol and q_lsd_f are dimensionless ratios to fixed positive training-reference medians; no q-unity or X/q_X quantity is used and no threshold at ratio 1 is claimed as physics.",
      "boundary_behavior": "Vol (min 20.424) and lsd_f (min 0.85684) are strictly positive over the full training domain, so the descriptor is finite for every row with no imputation; near the domain minima the descriptor stays finite and the monotone claim is only declared over the observed range, with fixed q reference constants carrying no universal physical meaning.",
      "vary_input": "Vol",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
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
        "lsd_f"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.85684,
        7.68726
      ],
      "training_spearman": 0.6285950097652175,
      "target_association": "consistent",
      "perturbation": 0.7023999999999999,
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
    "name": "bottleneck_volume_confinement",
    "formula": "log((q_Vol**(0.3333333333)) / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because tighter passage relative to molecular size reduces the accessible translational configuration space.",
    "rationale": "Translational confinement at infinite dilution is governed by the free volume actually reachable by a molecule of a given size; lsd_f (Zeo++ Df) is the largest free sphere that can pass through the periodic path, so a molecule whose cubic volume scale approaches the bottleneck experiences strong translational restriction. Literature reports that entropic loss correlates with gas-phase translational/rotational entropies and with framework occupiable volume (E07) and that tighter frameworks show larger entropy-loss fractions for linear alkanes (E04), consistent in direction with this descriptor. The descriptor is a dimensionless re-expression of two native inputs already present in the nonlinear ANN baseline; it adds interpretability, not new information. Limitations: Df is a geometric bottleneck proxy, not a global cavity diameter, and vdW volume is not the kinetic diameter seen by the framework; training association (Spearman ~0.63) is consistent but does not validate causality.",
    "falsification_criteria": "If entropy loss computed from published D0 values shows no monotone positive association with (Vol)^(1/3)/Df across the training domain, or if frameworks with equal Df but different pore connectivity (e.g., 1D channels vs 3D cages) show systematically different entropy loss at the same descriptor value, the confinement-ratio mechanism is falsified in favor of a connectivity or multi-site mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "(Vol)^(1/3) is a length-scale proxy for the molecule and lsd_f (Df) is the passing-bottleneck proxy only; neither is the true kinetic dimension nor the global cavity diameter Di, and Di is not available in D0. Cited comparisons (E02, E04) use average cavity/pore size, a different geometric quantity from Df; the transfer to a Df-based descriptor is a hypothesis. Source temperature, loading and framework chemistry are not fully resolved, and no source percentage or coefficient becomes a universal constant. Both proxies are transferable only within this rigid pure-silica, infinite-dilution regime.",
      "physical_interpretation": "Vol is the native vdW volume; lsd_f is the native passing free sphere (bottleneck), not the included-along-path Dif (lsd_p) and not a cavity diameter. q_Vol and q_lsd_f are dimensionless row-varying ratios to fixed positive training-reference medians; no q-unity threshold and no X/q_X construction is used.",
      "boundary_behavior": "Vol (min 20.424) and lsd_f (min 0.85684) are strictly positive over the full training domain, so log((q_Vol**(1/3))/q_lsd_f) is finite for every row with no imputation or epsilon; the monotone claim is declared only over the observed training range, and the fixed reference constants Vol_ref^(1/3)/lsd_f_ref carry no universal physical meaning (they rescale the physical ratio Vol**(1/3)/Df by a constant).",
      "vary_input": "Vol",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
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
        "lsd_f"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.85684,
        7.68726
      ],
      "training_spearman": 0.6285950097652175,
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
    "slot_id": "h1",
    "name": "bottleneck_volume_confinement",
    "formula": "log((q_Vol**(0.3333333333)) / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because tighter passage relative to molecular size reduces the accessible translational configuration space.",
    "rationale": "Translational confinement at infinite dilution is governed by the free volume actually reachable by a molecule of a given size; lsd_f (Zeo++ Df) is the largest free sphere that can pass through the periodic path, so a molecule whose cubic volume scale approaches the bottleneck experiences strong translational restriction. Literature reports that entropic loss correlates with gas-phase translational/rotational entropies and with framework occupiable volume (E07) and that tighter frameworks show larger entropy-loss fractions for linear alkanes (E04), consistent in direction with this descriptor. The descriptor is a dimensionless re-expression of two native inputs already present in the nonlinear ANN baseline; it adds interpretability, not new information. Limitations: Df is a geometric bottleneck proxy, not a global cavity diameter, and vdW volume is not the kinetic diameter seen by the framework; training association (Spearman ~0.63) is consistent but does not validate causality.",
    "falsification_criteria": "If entropy loss computed from published D0 values shows no monotone positive association with (Vol)^(1/3)/Df across the training domain, or if frameworks with equal Df but different pore connectivity (e.g., 1D channels vs 3D cages) show systematically different entropy loss at the same descriptor value, the confinement-ratio mechanism is falsified in favor of a connectivity or multi-site mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "(Vol)^(1/3) is a length-scale proxy for the molecule and lsd_f (Df) is the passing-bottleneck proxy only; neither is the true kinetic dimension nor the global cavity diameter Di, and Di is not available in D0. Cited comparisons (E02, E04) use average cavity/pore size, a different geometric quantity from Df; the transfer to a Df-based descriptor is a hypothesis. Source temperature, loading and framework chemistry are not fully resolved, and no source percentage or coefficient becomes a universal constant. Both proxies are transferable only within this rigid pure-silica, infinite-dilution regime.",
      "physical_interpretation": "Vol is the native vdW volume; lsd_f is the native passing free sphere (bottleneck), not the included-along-path Dif (lsd_p) and not a cavity diameter. q_Vol and q_lsd_f are dimensionless row-varying ratios to fixed positive training-reference medians; no q-unity threshold and no X/q_X construction is used.",
      "boundary_behavior": "Vol (min 20.424) and lsd_f (min 0.85684) are strictly positive over the full training domain, so log((q_Vol**(1/3))/q_lsd_f) is finite for every row with no imputation or epsilon; the monotone claim is declared only over the observed training range, and the fixed reference constants Vol_ref^(1/3)/lsd_f_ref carry no universal physical meaning (they rescale the physical ratio Vol**(1/3)/Df by a constant).",
      "vary_input": "Vol",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
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
        "lsd_f"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.85684,
        7.68726
      ],
      "training_spearman": 0.6285950097652175,
      "target_association": "consistent",
      "perturbation": 0.7023999999999999,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/rag_agent/replicate-2/round-1/h2`

最终状态：scored；边际收益：-2.644391 pp；保留：False。

复核改动字段：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "inertia_rotational_hindrance",
    "formula": "rotor_case(0.0, log(q_PMI3), log(q_PMI3))",
    "hypothesis": "At infinite dilution, rotational entropy loss (-delta_s_rot/R) increases monotonically with the adsorbate's largest heavy-atom principal moment of inertia (PMI3) for linear and nonlinear molecules, whereas single-site (spherical-top) molecules experience near-zero rotational entropy loss upon adsorption.",
    "rationale": "Gas-phase rotational entropy grows with the principal moments of inertia; when a molecule is immobilized in a cage or channel, the largest moment's free rotation is the most hindered, so the entropy penalty should scale with PMI3. The rotor_case branches are empirical smoothing of the heavy-atom proxy categories (single_site n=54, linear n=214, nonlinear n=2093), not a physical law; the zero single_site branch is a declared branch limit, motivated by the spherical-top approximation for molecules such as methane. PMI values are heavy-atom (implicit-H) proxies; true all-atom inertia is not zero and is not claimed to be. The descriptor re-expresses a native ANN input and contributes no new predictive information.",
    "falsification_criteria": "If entropy loss for linear molecules does not increase with PMI3 after volume is held fixed, or if single-site molecules show entropy losses comparable to low-PMI3 nonlinear molecules beyond translational contributions, the rotational-hindrance hypothesis is falsified. A competing mechanism is that entropy loss is set by contact-area frustration (shape) rather than inertia; distinguishing test: partial out Vol/LabuteASA and retest the PMI3 residual association.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI3 in the original implicit-H/heavy-atom representation proxies rotational hindrance; rotor_case membership (normalized tolerance 1e-10) is taken as exact within training. The proxy fails for molecules where hydrogen rotation or light-atom inertia dominates and across representation changes.",
      "physical_interpretation": "PMI3 is the native largest heavy-atom principal moment; q_PMI3 = PMI3 / PMI3_ref is a dimensionless row-varying input against the fixed positive training median, and log(q_PMI3) is dimensionless. No q-unity threshold is interpreted physically.",
      "boundary_behavior": "rotor_case branches: single_site -> 0.0 (dimensionless, finite by construction for the 54 single-site rows including methane-like cases); linear -> log(q_PMI3) with PMI3 > 0 for all 214 linear rows (PMI1 = 0 for linear molecules is never used); nonlinear -> log(q_PMI3) with PMI3 > 0 for all 2093 nonlinear rows (PMI2/PMI3 = 0 occurs only in the single_site branch). Every row yields a finite value without imputation.",
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
        "PMI3"
      ],
      "quantity_roles": {
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2414.631462
      ],
      "training_spearman": 0.3836040448784733,
      "target_association": "consistent",
      "perturbation": 4.425680816,
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
    "name": "inertia_rotational_hindrance",
    "formula": "rotor_case(0.0, log(q_PMI3), log(q_PMI3))",
    "hypothesis": "At infinite dilution, rotational entropy loss (-delta_s_rot/R) increases monotonically with the adsorbate's largest heavy-atom principal moment of inertia (PMI3) for linear and nonlinear molecules, whereas single-site (spherical-top) molecules experience near-zero rotational entropy loss upon adsorption.",
    "rationale": "Gas-phase rotational entropy grows with the principal moments of inertia; when a molecule is immobilized in a cage or channel, the largest moment's free rotation is the most hindered, so the entropy penalty should scale with PMI3. Literature reports larger rotational entropy losses in smaller-pore frameworks (E01, E02) and identifies translational plus rotational motions as the relevant contributions (E03), with the caveat that immobile-adsorbate RRHO treatments overestimate losses when retained mobility is neglected (E05). The rotor_case branches are empirical smoothing of the heavy-atom proxy categories (single_site n=54, linear n=214, nonlinear n=2093), not a physical law; the zero single_site branch is a declared branch limit, motivated by the spherical-top approximation for molecules such as methane. PMI values are heavy-atom (implicit-H) proxies; true all-atom inertia is not zero and is not claimed to be. The descriptor re-expresses a native ANN input and contributes no new predictive information; the training association (Spearman ~0.38) does not validate causality.",
    "falsification_criteria": "If entropy loss for linear molecules does not increase with PMI3 after volume is held fixed, or if single-site molecules show entropy losses comparable to low-PMI3 nonlinear molecules beyond translational contributions, the rotational-hindrance hypothesis is falsified. A competing mechanism is that entropy loss is set by contact-area frustration (shape) rather than inertia; distinguishing test: partial out Vol/LabuteASA and retest the PMI3 residual association.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E01",
      "E02",
      "E03",
      "E05"
    ],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI3 in the original implicit-H/heavy-atom representation proxies rotational hindrance; it is not true all-atom inertia, and zero heavy-atom PMI entries are legitimate representation zeros, not physical zero inertia. Rotor_case membership (normalized tolerance 1e-10) is taken as exact within training. The proxy fails where hydrogen rotation or light-atom inertia dominates and across representation changes. Cited rotational-loss comparisons (E01, E02, E06) use framework cavity size or gyration-sphere arguments under conditions (temperature, loading, framework chemistry) not fully resolved here; no source percentage or coefficient is transferred as a constant. RRHO-based rotational treatments have reported limitations (E05) that motivate treating this as an association, not a validated partition-function model.",
      "physical_interpretation": "PMI3 is the native largest heavy-atom principal moment; q_PMI3 = PMI3 / PMI3_ref is a dimensionless row-varying input against the fixed positive training median, and log(q_PMI3) is dimensionless. No q-unity threshold and no X/q_X construction is used.",
      "boundary_behavior": "rotor_case branches: single_site -> 0.0 (finite by construction for the 54 single-site rows including methane; a declared empirical branch limit, not a physical claim that spherical tops lose no rotational entropy); linear -> log(q_PMI3) with PMI3 > 0 for all 214 linear rows (PMI1 = 0 for linear molecules is never used); nonlinear -> log(q_PMI3) with PMI3 > 0 for all 2093 nonlinear rows (PMI2/PMI3 = 0 occurs only in the single_site branch). Every training row yields a finite value without imputation; PMI3 = 0 never enters a logarithm.",
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
        "PMI3"
      ],
      "quantity_roles": {
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2414.631462
      ],
      "training_spearman": 0.3836040448784733,
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
    "slot_id": "h2",
    "name": "inertia_rotational_hindrance",
    "formula": "rotor_case(0.0, log(q_PMI3), log(q_PMI3))",
    "hypothesis": "At infinite dilution, rotational entropy loss (-delta_s_rot/R) increases monotonically with the adsorbate's largest heavy-atom principal moment of inertia (PMI3) for linear and nonlinear molecules, whereas single-site (spherical-top) molecules experience near-zero rotational entropy loss upon adsorption.",
    "rationale": "Gas-phase rotational entropy grows with the principal moments of inertia; when a molecule is immobilized in a cage or channel, the largest moment's free rotation is the most hindered, so the entropy penalty should scale with PMI3. Literature reports larger rotational entropy losses in smaller-pore frameworks (E01, E02) and identifies translational plus rotational motions as the relevant contributions (E03), with the caveat that immobile-adsorbate RRHO treatments overestimate losses when retained mobility is neglected (E05). The rotor_case branches are empirical smoothing of the heavy-atom proxy categories (single_site n=54, linear n=214, nonlinear n=2093), not a physical law; the zero single_site branch is a declared branch limit, motivated by the spherical-top approximation for molecules such as methane. PMI values are heavy-atom (implicit-H) proxies; true all-atom inertia is not zero and is not claimed to be. The descriptor re-expresses a native ANN input and contributes no new predictive information; the training association (Spearman ~0.38) does not validate causality.",
    "falsification_criteria": "If entropy loss for linear molecules does not increase with PMI3 after volume is held fixed, or if single-site molecules show entropy losses comparable to low-PMI3 nonlinear molecules beyond translational contributions, the rotational-hindrance hypothesis is falsified. A competing mechanism is that entropy loss is set by contact-area frustration (shape) rather than inertia; distinguishing test: partial out Vol/LabuteASA and retest the PMI3 residual association.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E01",
      "E02",
      "E03",
      "E05"
    ],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI3 in the original implicit-H/heavy-atom representation proxies rotational hindrance; it is not true all-atom inertia, and zero heavy-atom PMI entries are legitimate representation zeros, not physical zero inertia. Rotor_case membership (normalized tolerance 1e-10) is taken as exact within training. The proxy fails where hydrogen rotation or light-atom inertia dominates and across representation changes. Cited rotational-loss comparisons (E01, E02, E06) use framework cavity size or gyration-sphere arguments under conditions (temperature, loading, framework chemistry) not fully resolved here; no source percentage or coefficient is transferred as a constant. RRHO-based rotational treatments have reported limitations (E05) that motivate treating this as an association, not a validated partition-function model.",
      "physical_interpretation": "PMI3 is the native largest heavy-atom principal moment; q_PMI3 = PMI3 / PMI3_ref is a dimensionless row-varying input against the fixed positive training median, and log(q_PMI3) is dimensionless. No q-unity threshold and no X/q_X construction is used.",
      "boundary_behavior": "rotor_case branches: single_site -> 0.0 (finite by construction for the 54 single-site rows including methane; a declared empirical branch limit, not a physical claim that spherical tops lose no rotational entropy); linear -> log(q_PMI3) with PMI3 > 0 for all 214 linear rows (PMI1 = 0 for linear molecules is never used); nonlinear -> log(q_PMI3) with PMI3 > 0 for all 2093 nonlinear rows (PMI2/PMI3 = 0 occurs only in the single_site branch). Every training row yields a finite value without imputation; PMI3 = 0 never enters a logarithm.",
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
        "PMI3"
      ],
      "quantity_roles": {
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2414.631462
      ],
      "training_spearman": 0.3836040448784733,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/rag_agent/replicate-2/round-1/h3`

最终状态：scored；边际收益：-3.279102 pp；保留：False。

复核改动字段：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "asphericity_orientation_penalty",
    "formula": "log(q_LabuteASA / (q_Vol**(0.6666666667)))",
    "hypothesis": "At infinite dilution, adsorption entropy loss increases with adsorbate asphericity, proxied by the dimensionless ratio of Labute accessible surface area to van der Waals volume raised to the 2/3 power, because elongated or branched molecules lose more orientational and coupled rotational-translational entropy when their orientation freedom is restricted by framework walls.",
    "rationale": "A sphere minimizes surface area for a given volume, so surface-to-volume^(2/3) is a classical shape/roughness index: values above the spherical baseline indicate elongation, branching, or surface corrugation, all of which increase the number of wall-contact geometries that must be frozen out upon adsorption. This is a shape-family mechanism distinct from the translation (h1) and rotation (h2) slots, covering the required two-family minimum jointly. The descriptor is a smooth, all-positive re-expression of two native inputs already in the ANN; it is an empirical_proxy association claim, not a causal or validated-novelty claim. Limitation: LabuteASA is an approximate implicit-H surface, so the index mixes size-independent shape with H-count effects.",
    "falsification_criteria": "If, after controlling for Vol (pure size effect), entropy loss shows no positive residual association with the asphericity index, or if near-spherical molecules with large cages show losses comparable to highly aspherical ones, the orientation-freezing mechanism is falsified. A competing mechanism is that the index merely tracks MW/LabuteASA size; test by stratifying at fixed LabuteASA and retesting.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA (angstrom^2) and vdW Vol (angstrom^3) are computed on the same original implicit-H representation, so the ratio is representation-consistent within this dataset; transfer to all-atom or other surface definitions is not assumed. The 2/3 exponent is the geometric isoperimetric scaling, used as a fixed numeric normalization, not a fitted constant with physical meaning.",
      "physical_interpretation": "Both quantities are native adsorbate geometry quantities; q_LabuteASA and q_Vol are dimensionless ratios to fixed positive training-reference medians, making the log argument dimensionless. No physical q-unity threshold and no X/q_X construction is used.",
      "boundary_behavior": "LabuteASA (min 7.4506) and Vol (min 20.424) are strictly positive over the whole training domain, so the descriptor is finite for every row with no imputation or epsilon; the monotone association is declared only within the observed quantile range, and fixed q reference constants carry no universal physical meaning.",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        "Vol"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        20.424,
        161.144
      ],
      "training_spearman": 0.381525237901583,
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
    "slot_id": "h3",
    "name": "asphericity_orientation_penalty",
    "formula": "log(q_LabuteASA / (q_Vol**(0.6666666667)))",
    "hypothesis": "At infinite dilution, adsorption entropy loss increases with adsorbate asphericity, proxied by the dimensionless ratio of Labute accessible surface area to van der Waals volume raised to the 2/3 power, because elongated or branched molecules lose more orientational and coupled rotational-translational entropy when their orientation freedom is restricted by framework walls.",
    "rationale": "At infinite dilution, adsorption entropy loss is hypothesized to increase with adsorbate asphericity, proxied by the dimensionless ratio of Labute accessible surface area to van der Waals volume raised to the 2/3 power, because elongated or branched molecules lose more orientational and coupled rotational-translational entropy when their orientation freedom is restricted by framework walls. Source discussion of gyration radius versus available cage space (E10) and differential rotational freedom of linear versus branched isomers in supercage subsections (E06) motivates the direction of this association under restricted conditions. This is a shape-family mechanism distinct from the translation (h1) and rotation (h2) slots, covering the required two-family minimum jointly. The descriptor is a smooth, all-positive re-expression of two native inputs already in the ANN; it is an empirical_proxy association claim, not a causal or validated-novelty claim. Limitations: LabuteASA is an approximate implicit-H surface, so the index mixes size-independent shape with H-count effects.",
    "falsification_criteria": "If, after controlling for Vol (pure size effect), entropy loss shows no positive residual association with the asphericity index, or if near-spherical molecules with large cages show losses comparable to highly aspherical ones, the orientation-freezing mechanism is falsified. A competing mechanism is that the index merely tracks MW/LabuteASA size; test by stratifying at fixed LabuteASA and retesting.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E06",
      "E10"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA (angstrom^2) and vdW Vol (angstrom^3) are computed on the same original implicit-H representation, so the ratio is representation-consistent within this dataset; transfer to all-atom or other surface definitions is not assumed. The 2/3 exponent is the geometric isoperimetric scaling, used as a fixed numeric normalization, not a fitted constant with physical meaning. Cited support (E06, E10) concerns rotational freedom of linear vs branched molecules relative to cage subsections under MCM-22-specific conditions (450-850 K diffusion discussions); transfer to this benchmark's frameworks and temperatures is a hypothesis, and the gyration-sphere/cage-radius comparison in the sources is a different geometric construction from this shape index.",
      "physical_interpretation": "Both quantities are native adsorbate geometry quantities; q_LabuteASA and q_Vol are dimensionless row-varying ratios to fixed positive training-reference medians, making the log argument dimensionless. No physical q-unity threshold and no X/q_X construction is used.",
      "boundary_behavior": "LabuteASA (min 7.4506) and Vol (min 20.424) are strictly positive over the whole training domain, so log(q_LabuteASA / q_Vol**(2/3)) is finite for every row with no imputation or epsilon; the monotone association is declared only within the observed quantile range, and the fixed reference constants Vol_ref**(2/3)/LabuteASA_ref carry no universal physical meaning (they rescale the physical index ASA/Vol**(2/3) by a constant).",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        "Vol"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        20.424,
        161.144
      ],
      "training_spearman": 0.381525237901583,
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
    "slot_id": "h3",
    "name": "asphericity_orientation_penalty",
    "formula": "log(q_LabuteASA / (q_Vol**(0.6666666667)))",
    "hypothesis": "At infinite dilution, adsorption entropy loss increases with adsorbate asphericity, proxied by the dimensionless ratio of Labute accessible surface area to van der Waals volume raised to the 2/3 power, because elongated or branched molecules lose more orientational and coupled rotational-translational entropy when their orientation freedom is restricted by framework walls.",
    "rationale": "At infinite dilution, adsorption entropy loss is hypothesized to increase with adsorbate asphericity, proxied by the dimensionless ratio of Labute accessible surface area to van der Waals volume raised to the 2/3 power, because elongated or branched molecules lose more orientational and coupled rotational-translational entropy when their orientation freedom is restricted by framework walls. Source discussion of gyration radius versus available cage space (E10) and differential rotational freedom of linear versus branched isomers in supercage subsections (E06) motivates the direction of this association under restricted conditions. This is a shape-family mechanism distinct from the translation (h1) and rotation (h2) slots, covering the required two-family minimum jointly. The descriptor is a smooth, all-positive re-expression of two native inputs already in the ANN; it is an empirical_proxy association claim, not a causal or validated-novelty claim. Limitations: LabuteASA is an approximate implicit-H surface, so the index mixes size-independent shape with H-count effects.",
    "falsification_criteria": "If, after controlling for Vol (pure size effect), entropy loss shows no positive residual association with the asphericity index, or if near-spherical molecules with large cages show losses comparable to highly aspherical ones, the orientation-freezing mechanism is falsified. A competing mechanism is that the index merely tracks MW/LabuteASA size; test by stratifying at fixed LabuteASA and retesting.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E06",
      "E10"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA (angstrom^2) and vdW Vol (angstrom^3) are computed on the same original implicit-H representation, so the ratio is representation-consistent within this dataset; transfer to all-atom or other surface definitions is not assumed. The 2/3 exponent is the geometric isoperimetric scaling, used as a fixed numeric normalization, not a fitted constant with physical meaning. Cited support (E06, E10) concerns rotational freedom of linear vs branched molecules relative to cage subsections under MCM-22-specific conditions (450-850 K diffusion discussions); transfer to this benchmark's frameworks and temperatures is a hypothesis, and the gyration-sphere/cage-radius comparison in the sources is a different geometric construction from this shape index.",
      "physical_interpretation": "Both quantities are native adsorbate geometry quantities; q_LabuteASA and q_Vol are dimensionless row-varying ratios to fixed positive training-reference medians, making the log argument dimensionless. No physical q-unity threshold and no X/q_X construction is used.",
      "boundary_behavior": "LabuteASA (min 7.4506) and Vol (min 20.424) are strictly positive over the whole training domain, so log(q_LabuteASA / q_Vol**(2/3)) is finite for every row with no imputation or epsilon; the monotone association is declared only within the observed quantile range, and the fixed reference constants Vol_ref**(2/3)/LabuteASA_ref carry no universal physical meaning (they rescale the physical index ASA/Vol**(2/3) by a constant).",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        "Vol"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        20.424,
        161.144
      ],
      "training_spearman": 0.381525237901583,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
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
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a716c0f2d08195e0bc57308d",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d3a799358d58da57167e96f1",
        "paper_id": "doi:10.1021/acs.langmuir.3c03931",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
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
        "record_id": "chunk:43dedbc998f9c278eea622b0",
        "paper_id": "pmc:pmc9739862",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d8eef552eba72a99f7974a84",
        "paper_id": "doi:10.1039/b819334g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08aecb87be6d1cda8c6566fa",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:166106b9d0f41731d2d72c4f",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3f5768387a8e2dd4104cc2f6",
        "paper_id": "doi:10.1039/c3cc40731d",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:4ee093d81da6b5c01358e0ca",
        "paper_id": "doi:10.1021/acs.jctc.5c01100",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cc904c61f240366bfe7825e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd6fadcf0e5f2fd99bb3f46e",
        "paper_id": "doi:10.1021/acsami.5c17486",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d270ec3d6183be4a3de52cd8",
        "paper_id": "doi:10.1039/c3cp55039g",
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
    "query": "adsorption entropy confinement For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because tighter passage relative to molecular size reduces the accessible translational configuration space. log((q_Vol**(0.3333333333)) / q_lsd_f) At infinite dilution, rotational entropy loss (-delta_s_rot/R) increases monotonically with the adsorbate's largest heavy-atom principal moment of inertia (PMI3) for linear and nonlinear molecules, whereas single-site (spherical-top) molecules experience near-zero rotational entropy loss upon adsorption. rotor_case(0.0, log(q_PMI3), log(q_PMI3)) At infinite dilution, adsorption entropy loss increases with adsorbate asphericity, proxied by the dimensionless ratio of Labute accessible surface area to van der Waals volume raised to the 2/3 power, because elongated or branched molecules lose more orientational and coupled rotational-translational entropy when their orientation freedom is restricted by framework walls. log(q_LabuteASA / (q_Vol**(0.6666666667)))",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:11077178fd4d765fcf20a5a1"
    ],
    "items": 10,
    "lexical_tokens": 4503,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [
    {
      "record_id": "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "paper_id": "pmc:pmc6161062",
      "document_id": "document:7ba8c366c10dc56ab9a75bda",
      "quote": "alkanes adsorbed in MFI experience a 3-fold larger loss in rotational degrees of freedom than in the larger pore FAU",
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
          "lsd_f",
          "lsd_p",
          "PMI1",
          "PMI2",
          "PMI3"
        ],
        "proxy_caveat": "D0 inputs are proxies, not measurements of lost freedom. AV is per framework mass, not molecular free volume. Normalized ratios do not preserve physical threshold 1.",
        "status": "conditional_use"
      },
      "id": "E01"
    },
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
      "record_id": "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "paper_id": "pmc:pmc6161062",
      "document_id": "document:7ba8c366c10dc56ab9a75bda",
      "quote": "Adsorption can therefore be best described by considering entropic losses due to both translational and rotational motions",
      "locator": {
        "kind": "pdf_page",
        "page": 1
      },
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
      "id": "E03"
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
      "record_id": "chunk:878e3cf9557831b0616715f9",
      "paper_id": "doi:10.1002/cphc.201701084",
      "document_id": "document:2599bae9c40111b40c45ccef",
      "quote": "and rotational movements of the guest molecule relative to the zeolite host as vibrations under the rigid rotor-harmonic oscillator ( RRHO ) approximation has been shown to overestimate the entropy losses associated with the adsorption of the guest molecules from the gas phase into the zeolite pores . $ ^ { [ 59 , 84 , 85 ] } $ In their study of hydrocarbon adsorption in zeolites, De Moor et al. demonstrated that the entropy cannot be calculated correctly by treating the guest molecules as immobile adsorbates in the RRHO approximation, and that the remaining mobility of the adsorbed species at the active sites needs to be taken into account. $ ^{[85]} $ The authors suggested an alternative, mobile adsorbate calculation, which uses a so-called mobile block analysis of the Hessian (MBH) $ ^{[86,87]} $ to identify those low-frequency modes corresponding to overall global translations and rotations of the guest molecule relative to the framework. Once identified, the contributions of the modes to the partition function are replaced by the correct ones for translational or rotational motions.",
      "locator": {
        "kind": "markdown_section",
        "section": "3.3. thermochemical calculations"
      },
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
      "id": "E05"
    },
    {
      "record_id": "chunk:51aa804bfe1967d7ebb1d76f",
      "paper_id": "doi:10.1021/jp060657s",
      "document_id": "document:efa163ae1d6a7d3f748b3c99",
      "quote": "break-word ; ' > 1.07 $ ^ { a } $ Length of the molecule . $ ^ { b } $ Radius in the central section of the supercage . $ ^ { c } $ Radius in the upper and lower pockets of the supercage . interconnect these cages. Molecular dynamics simulations showed that diffusion of 2-MeC6 in MCM-22 (between 450 and 850 K) in the sinusoidal 10-MR channels does not occur to a significant extent. $ ^{67} $ That study also stated that interstage diffusion (in the short bridges that connect the neighboring supercages) does not happen (for n-C7 and 2-MeC6) until elevated temperatures so that molecules spend most of their time inside the cage. In an NMR study of xenon adsorption in zeolite MCM-22, it was found that, particularly at low coverage, xenon atoms predominantly prefer to locate inside the supercages. $ ^{68} $ During the discussions of infrared spectrometric (IR) results, $ ^{69} $ it was declared that the supercages constitute about 70% of the micropore volume, indicating that the majority of the adsorption phenomenon is happening there. This argument was strengthened by the modeling calculations. $ ^{70} $ The authors determined the adsorption isotherm of n-C6 and 3-MeC5 at various temperatures on ITQ-1, the pure silica analogue of MCM-22, and suggested that three out of four adsorbate molecules are located in the large cages and one molecule in the sinusoidal channel system, which is in agreement with the supremacy of adsorption inside the supercages. In summary, on the basis of supporting information from literature, adsorption of linear and singly branched molecules will be considered, occurring principally inside the supercages of MCM-22. As the adsorbed molecules, whether they are linear or branched, are confined in a closed space, i.e., the supercage, their losses in translational and vibrational degrees of freedom will be comparable. Differences in rotational freedom in the supercages of MCM-22 may have a substantial impact on the adsorption equilibrium. Rotational entropy of the different species was qualitatively analyzed by comparing the radius of gyration of each molecule to the available space in the",
      "locator": {
        "kind": "markdown_section",
        "section": "discussion"
      },
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
      "id": "E06"
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
    },
    {
      "record_id": "chunk:11077178fd4d765fcf20a5a1",
      "paper_id": "doi:10.1021/jp060657s",
      "document_id": "document:efa163ae1d6a7d3f748b3c99",
      "quote": ". Rotational entropy of the different species was qualitatively analyzed by comparing the radius of gyration of each molecule to the available space in the Figure 9. Drawing of 2-methylbutane in the lower pocket of the MCM-22 supercage. Yellow sphere represents the Gyration sphere circumscribing the rotational movement of the molecule around its center of gravity. The van der Waals contact surface of zeolite and adsorbed molecule are represented by a transparent surface. Figure 10. 2-methylpentane molecule in the central part of the MCM-22 supercage. supercage. Molecular diameters and lengths were calculated assuming that these properties can be best represented by van der Waals volumes of the molecule. From these dimensions, the radius of gyration $ R_g $ was calculated, assuming rotation around the center of mass. This radius was then compared to the radius of the largest sphere that fits into the van der Waals contour of the cage ( $ R_c $), differentiating between two adsorption spots inside the supercage. These are the upper and lower pockets and the large central section of the supercage (see Figure 1). In Table 4, the $ R_g $ values of each adsorbate is compared to $ R_c $ of the pockets ( $ R_{c,p} $) and the central section ( $ R_{c,c} $) separately. This comparison provides an estimate of the ability of a molecule to rotate in different sections of a supercage of MCM-22. A ratio higher than unity denotes that this particular molecule is larger than the pockets or the central section, consequently designating if it can rotate freely therein or not. For pentane and 2-MeC4, the gyration sphere of the branched isomer neatly fits in the pockets of the supercage, whereas rotation of n-C5 in there is already severely restricted (Figure 9). Both components retain their rotational freedom in the larger central section. A linear hexane molecule is able to rotate neither",
      "locator": {
        "section": "discussion",
        "page": 1
      },
      "applicability": {
        "record_id": "chunk:51aa804bfe1967d7ebb1d76f",
        "paper_id": "doi:10.1021/jp060657s",
        "decision": "conditional_use",
        "reason": "Relevant adsorption-entropy mechanism or approximation caveat, with original qualifications retained",
        "source_conditions": "See preserved original passage; source method and target-regime transfer are not presumed identical",
        "transfer_assumptions": [
          "No outcome-fitted coefficient, quoted percentage, or source-specific geometry becomes a universal constant.",
          "Any available D0 quantity used as a proxy requires an explicit mapping and limitation."
        ],
        "status": "conditional_use"
      },
      "id": "E10"
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
