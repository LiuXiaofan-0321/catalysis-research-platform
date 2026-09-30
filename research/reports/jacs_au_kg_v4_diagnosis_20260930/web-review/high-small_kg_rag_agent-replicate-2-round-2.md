# high/small_kg_rag_agent/replicate-2/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/small_kg_rag_agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h3",
    "name": "cage_window_path_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "Frameworks whose included free-path diameter (Dif) greatly exceeds their passing bottleneck (Df) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom, and the pre-declared association is that increasing contrast correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas).",
    "rationale": "Connectivity-family hypothesis retained with an honest status update. The contrast Dif/Df distinguishes cage-window topologies from open channels: lsd_p is the included diameter along the free path and lsd_f the passing bottleneck; neither equals the global cavity diameter Di. The training-only precheck finds essentially no marginal association with entropy loss/R (spearman about -0.02), so the pre-declared increasing direction is neither confirmed nor contradicted, and the competing rattling-freedom explanation (large contrast yields local freedom and lower loss) remains live. Sources report cavity-size-dependent entropy losses (E02, E04) and propose cage rotational effects on equilibrium (E06), but these are conditional reports that supply no fitted coefficients for this benchmark.",
    "falsification_criteria": "If, once lsd_f (or lsd_p alone) is controlled for, the contrast log(q_lsd_p/q_lsd_f) shows no association with entropy loss/R within the training quantile range — as the current marginal spearman of about -0.02 already suggests — or shows the sign opposite to the pre-declared increasing direction, the cage-window contrast mechanism is falsified in favor of a pure bottleneck/kinetic or cavity-size explanation.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E06"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Zeo++ Df (lsd_f, passing bottleneck) and Dif (lsd_p, largest included sphere along the free-sphere path) are rigid fixed-probe geometric outputs on the published numerical scale; neither is the global cavity diameter Di, and neither measures adsorbed-phase configurational entropy. Framework flexibility, defects and molecule-specific probe sizes are ignored.",
      "physical_interpretation": "q_lsd_p and q_lsd_f are row-varying ratios to fixed positive training-reference medians (6.38663 and 5.16326); a q-ratio of 1 is not a native equality threshold. The log-ratio is only a dimensionless cage-window contrast coordinate. The training-only precheck returns spearman about -0.02 with entropy loss/R, so the pre-declared increasing association is currently unconfirmed on training data; the descriptor is retained as a pre-registered falsification test, not a validated predictor.",
      "boundary_behavior": "lsd_f (min 0.85684) and lsd_p (min 3.3452) have zero_n = 0 over all 2361 training rows, so q_lsd_p/q_lsd_f is strictly positive and the log-ratio is finite on every row; no epsilon shifting or imputation is invoked. Behavior outside the positive domain is undefined and not claimed.",
      "vary_input": "lsd_p",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  }
]
```

## h1

候选标识：`high/small_kg_rag_agent/replicate-2/round-2/h1`

最终状态：scored；边际收益：-1.093400 pp；保留：False。

复核改动字段：evidence_ids

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "accessible_volume_to_molecule_volume_ratio",
    "formula": "q_AV / q_Vol",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the ratio of the framework's probe-accessible specific volume (AV) to the adsorbate's van der Waals volume (Vol) proxies the translational free space available per unit of molecular size. The pre-declared association is that increasing AV/Vol (more accessible volume relative to molecular volume) correlates with decreasing entropy loss/R, because a larger relative free volume permits more translational microstates in the adsorbed phase relative to the gas.",
    "rationale": "AV is a fixed-probe, mass-specific accessibility and is not molecule-specific free volume; Vol is an all-atom vdW volume. Their dimensionless ratio is used only as an empirical confinement proxy, not as a physical equality threshold. The target is entropy loss/R, so the declared direction is on entropy loss, not on s_ads/s_gas directly. All 14 published D0 inputs already enter the nonlinear ANN, so this descriptor can only re-express existing inputs; its value lies in testing whether the volume-ratio axis carries entropy-loss association not captured by the raw inputs.",
    "falsification_criteria": "If training Spearman association between q_AV/q_Vol and entropy loss/R is inconsistent with the declared decreasing direction, or if the marginal MAE improvement over the retained baseline set is non-positive, the free-volume-ratio mechanism is falsified for this dataset. A competing mechanism that would also falsify it: entropy loss dominated by rotational or bottleneck effects such that volume ratio carries no residual association after h3 and h2 are accounted for.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Assumes the fixed geometric probe used to compute AV rank-orders molecular translational freedom across frameworks for the adsorbates in the training domain. AV=0 (28 training rows) means zero accessibility for the fixed probe and does not imply zero physical molecular adsorption space; the ratio is used as a monotone empirical proxy only. Vol is an all-atom quantity while most shape inputs here are heavy-atom proxies; the mixing is acknowledged as a representation limitation.",
      "physical_interpretation": "Native meanings: AV is probe-accessible cm^3/g of framework, Vol is the adsorbate vdW volume in angstrom^3. q_AV and q_Vol are row-varying ratios to fixed positive training-reference medians (AV_ref = 0.0759781, Vol_ref = 67.24). No q-value of 1 is interpreted as a physical threshold.",
      "boundary_behavior": "At AV=0 the descriptor is exactly 0 (finite): q_AV=0 divided by the always-positive q_Vol. This is a legitimate physical zero of the fixed-probe proxy, not an imputation; it encodes maximal confinement under the proxy. For large AV and small Vol the descriptor grows smoothly and monotonically; no log or division by a legitimate zero occurs anywhere in the training domain.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        1.0
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
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.6742603187530807,
      "target_association": "consistent",
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
    "slot_id": "h1",
    "name": "accessible_volume_to_molecule_volume_ratio",
    "formula": "q_AV / q_Vol",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the ratio of the framework's probe-accessible specific volume (AV) to the adsorbate's van der Waals volume (Vol) proxies the translational free space available per unit of molecular size. The pre-declared association is that increasing AV/Vol (more accessible volume relative to molecular volume) correlates with decreasing entropy loss/R, because a larger relative free volume permits more translational microstates in the adsorbed phase relative to the gas.",
    "rationale": "AV is a fixed-probe, mass-specific accessibility and is not molecule-specific free volume; Vol is an all-atom vdW volume. Their dimensionless ratio is used only as an empirical confinement proxy, not as a physical equality threshold. The target is entropy loss/R, so the declared direction is on entropy loss, not on s_ads/s_gas directly. All 14 published D0 inputs already enter the nonlinear ANN, so this descriptor can only re-express existing inputs; its value lies in testing whether the volume-ratio axis carries entropy-loss association not captured by the raw inputs.",
    "falsification_criteria": "If training Spearman association between q_AV/q_Vol and entropy loss/R is inconsistent with the declared decreasing direction, or if the marginal MAE improvement over the retained baseline set is non-positive, the free-volume-ratio mechanism is falsified for this dataset. A competing mechanism that would also falsify it: entropy loss dominated by rotational or bottleneck effects such that volume ratio carries no residual association after h3 and h2 are accounted for.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E07"
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
      "mechanism_family": "translation",
      "proxy_assumptions": "Assumes the fixed geometric probe used to compute AV rank-orders molecular translational freedom across frameworks for the adsorbates in the training domain. AV=0 (28 training rows) means zero accessibility for the fixed probe and does not imply zero physical molecular adsorption space; the ratio is used as a monotone empirical proxy only. Vol is an all-atom quantity while most shape inputs here are heavy-atom proxies; the mixing is acknowledged as a representation limitation.",
      "physical_interpretation": "Native meanings: AV is probe-accessible cm^3/g of framework, Vol is the adsorbate vdW volume in angstrom^3. q_AV and q_Vol are row-varying ratios to fixed positive training-reference medians (AV_ref = 0.0759781, Vol_ref = 67.24). No q-value of 1 is interpreted as a physical threshold.",
      "boundary_behavior": "At AV=0 the descriptor is exactly 0 (finite): q_AV=0 divided by the always-positive q_Vol. This is a legitimate physical zero of the fixed-probe proxy, not an imputation; it encodes maximal confinement under the proxy. For large AV and small Vol the descriptor grows smoothly and monotonically; no log or division by a legitimate zero occurs anywhere in the training domain.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        1.0
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
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.6742603187530807,
      "target_association": "consistent",
      "perturbation": 0.001538232,
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
    "name": "accessible_volume_to_molecule_volume_ratio",
    "formula": "q_AV / q_Vol",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the ratio of the framework's probe-accessible specific volume (AV) to the adsorbate's van der Waals volume (Vol) proxies the translational free space available per unit of molecular size. The pre-declared association is that increasing AV/Vol (more accessible volume relative to molecular volume) correlates with decreasing entropy loss/R, because a larger relative free volume permits more translational microstates in the adsorbed phase relative to the gas.",
    "rationale": "AV is a fixed-probe, mass-specific accessibility and is not molecule-specific free volume; Vol is an all-atom vdW volume. Their dimensionless ratio is used only as an empirical confinement proxy, not as a physical equality threshold. The target is entropy loss/R, so the declared direction is on entropy loss, not on s_ads/s_gas directly. All 14 published D0 inputs already enter the nonlinear ANN, so this descriptor can only re-express existing inputs; its value lies in testing whether the volume-ratio axis carries entropy-loss association not captured by the raw inputs.",
    "falsification_criteria": "If training Spearman association between q_AV/q_Vol and entropy loss/R is inconsistent with the declared decreasing direction, or if the marginal MAE improvement over the retained baseline set is non-positive, the free-volume-ratio mechanism is falsified for this dataset. A competing mechanism that would also falsify it: entropy loss dominated by rotational or bottleneck effects such that volume ratio carries no residual association after h3 and h2 are accounted for.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E07"
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
      "mechanism_family": "translation",
      "proxy_assumptions": "Assumes the fixed geometric probe used to compute AV rank-orders molecular translational freedom across frameworks for the adsorbates in the training domain. AV=0 (28 training rows) means zero accessibility for the fixed probe and does not imply zero physical molecular adsorption space; the ratio is used as a monotone empirical proxy only. Vol is an all-atom quantity while most shape inputs here are heavy-atom proxies; the mixing is acknowledged as a representation limitation.",
      "physical_interpretation": "Native meanings: AV is probe-accessible cm^3/g of framework, Vol is the adsorbate vdW volume in angstrom^3. q_AV and q_Vol are row-varying ratios to fixed positive training-reference medians (AV_ref = 0.0759781, Vol_ref = 67.24). No q-value of 1 is interpreted as a physical threshold.",
      "boundary_behavior": "At AV=0 the descriptor is exactly 0 (finite): q_AV=0 divided by the always-positive q_Vol. This is a legitimate physical zero of the fixed-probe proxy, not an imputation; it encodes maximal confinement under the proxy. For large AV and small Vol the descriptor grows smoothly and monotonically; no log or division by a legitimate zero occurs anywhere in the training domain.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        1.0
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
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.6742603187530807,
      "target_association": "consistent",
      "perturbation": 0.001538232,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/small_kg_rag_agent/replicate-2/round-2/h2`

最终状态：scored；边际收益：-4.735425 pp；保留：False。

复核改动字段：evidence_ids

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_class_heavy_atom_inertia_hindrance",
    "formula": "rotor_case(1.0, log(1.0 + q_PMI2), log(1.0 + q_PMI3))",
    "hypothesis": "Rotational entropy loss on adsorption at infinite dilution scales with the heavy-atom principal moment of inertia about the largest axis, with the relevant proxy depending on rotor class: single-site adsorbates (e.g., methane) have no heavy-atom rotational hindrance proxy and contribute a constant; linear adsorbates are proxied by PMI2; nonlinear adsorbates by PMI3. The pre-declared association is that increasing the class-matched inertia proxy correlates with increasing entropy loss/R, because larger moments of inertia correspond to more restricted rotational libration in the confined framework relative to free gas rotation.",
    "rationale": "PMI proxies come from the original implicit-H/heavy-atom representation; they are not true all-atom moments of inertia and hydrogen rotation is not captured. Legitimate zeros occur for single-site species (54 training rows); the rotor_case construction ensures those rows take the constant branch rather than entering a log of zero, and no median imputation is used. log(1+q) is an empirical monotone smoothing chosen to keep the dimensionless log argument strictly positive at q=0; it carries no universal physical meaning and is disclosed as a numerical form, not a law. The prior h2 (q_PMI3 * q_Vol) showed a consistent positive association (Spearman 0.404) but was not retained; this variant removes the Vol coupling to test the pure inertia axis and makes the rotor-class dependence explicit.",
    "falsification_criteria": "If the class-matched inertia proxy shows training association inconsistent with the declared increasing entropy-loss direction within any rotor class, or if rotor_class-fixed partial-derivative diagnostics show mechanism_validated = false with non-positive marginal MAE improvement, the rotational-hindrance mechanism as proxied by heavy-atom PMI is falsified. A competing mechanism that would also falsify it: entropy loss governed primarily by translational/configurational confinement (h1, h3) with inertia adding no residual signal.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Explicit rotor_case branches: single_site -> 1.0 (constant, no heavy-atom inertia proxy exists for single-site species; this does not assert true all-atom inertia is zero); linear -> log(1 + q_PMI2); nonlinear -> log(1 + q_PMI3). Branch selection uses the native PMI proxy categories with normalized tolerance 1e-10. Assumes heavy-atom PMI rank-orders rotational confinement within each class; transfer across chemical classes is not claimed. q_PMI values are row-varying ratios to fixed positive training-reference medians (PMI2_ref = 93.79729089, PMI3_ref = 125.4948325).",
      "physical_interpretation": "Native meanings: PMI2 and PMI3 are the second and third principal moments of inertia of the heavy-atom (implicit-H) molecular representation in angstrom^2*amu. The descriptor is dimensionless; log arguments 1+q are dimensionless by construction. No unity threshold of q is interpreted physically.",
      "boundary_behavior": "Single-site rows (PMI2 = PMI3 = 0, 54 training rows) take the constant branch 1.0, avoiding 0/0 and log(0); the constant encodes the absence of a heavy-atom rotational hindrance proxy rather than zero rotational entropy loss. Linear rows use PMI2 (min 0 in training, but the +1 smoothing keeps log finite at q=0). Nonlinear rows use PMI3, finite for all values in [0, 2414.63]. All branches output dimensionless-compatible values.",
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
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI2": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.3675774051544217,
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
    "name": "rotor_class_heavy_atom_inertia_hindrance",
    "formula": "rotor_case(1.0, log(1.0 + q_PMI2), log(1.0 + q_PMI3))",
    "hypothesis": "Rotational entropy loss on adsorption at infinite dilution scales with the heavy-atom principal moment of inertia about the largest axis, with the relevant proxy depending on rotor class: single-site adsorbates (e.g., methane) have no heavy-atom rotational hindrance proxy and contribute a constant; linear adsorbates are proxied by PMI2; nonlinear adsorbates by PMI3. The pre-declared association is that increasing the class-matched inertia proxy correlates with increasing entropy loss/R, because larger moments of inertia correspond to more restricted rotational libration in the confined framework relative to free gas rotation.",
    "rationale": "PMI proxies come from the original implicit-H/heavy-atom representation; they are not true all-atom moments of inertia and hydrogen rotation is not captured. Legitimate zeros occur for single-site species (54 training rows); the rotor_case construction ensures those rows take the constant branch rather than entering a log of zero, and no median imputation is used. log(1+q) is an empirical monotone smoothing chosen to keep the dimensionless log argument strictly positive at q=0; it carries no universal physical meaning and is disclosed as a numerical form, not a law. The prior h2 (q_PMI3 * q_Vol) showed a consistent positive association (Spearman 0.404) but was not retained; this variant removes the Vol coupling to test the pure inertia axis and makes the rotor-class dependence explicit.",
    "falsification_criteria": "If the class-matched inertia proxy shows training association inconsistent with the declared increasing entropy-loss direction within any rotor class, or if rotor_class-fixed partial-derivative diagnostics show mechanism_validated = false with non-positive marginal MAE improvement, the rotational-hindrance mechanism as proxied by heavy-atom PMI is falsified. A competing mechanism that would also falsify it: entropy loss governed primarily by translational/configurational confinement (h1, h3) with inertia adding no residual signal.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E06"
    ],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Explicit rotor_case branches: single_site -> 1.0 (constant, no heavy-atom inertia proxy exists for single-site species; this does not assert true all-atom inertia is zero); linear -> log(1 + q_PMI2); nonlinear -> log(1 + q_PMI3). Branch selection uses the native PMI proxy categories with normalized tolerance 1e-10. Assumes heavy-atom PMI rank-orders rotational confinement within each class; transfer across chemical classes is not claimed. q_PMI values are row-varying ratios to fixed positive training-reference medians (PMI2_ref = 93.79729089, PMI3_ref = 125.4948325).",
      "physical_interpretation": "Native meanings: PMI2 and PMI3 are the second and third principal moments of inertia of the heavy-atom (implicit-H) molecular representation in angstrom^2*amu. The descriptor is dimensionless; log arguments 1+q are dimensionless by construction. No unity threshold of q is interpreted physically.",
      "boundary_behavior": "Single-site rows (PMI2 = PMI3 = 0, 54 training rows) take the constant branch 1.0, avoiding 0/0 and log(0); the constant encodes the absence of a heavy-atom rotational hindrance proxy rather than zero rotational entropy loss. Linear rows use PMI2 (min 0 in training, but the +1 smoothing keeps log finite at q=0). Nonlinear rows use PMI3, finite for all values in [0, 2414.63]. All branches output dimensionless-compatible values.",
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
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI2": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.3675774051544217,
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
    "name": "rotor_class_heavy_atom_inertia_hindrance",
    "formula": "rotor_case(1.0, log(1.0 + q_PMI2), log(1.0 + q_PMI3))",
    "hypothesis": "Rotational entropy loss on adsorption at infinite dilution scales with the heavy-atom principal moment of inertia about the largest axis, with the relevant proxy depending on rotor class: single-site adsorbates (e.g., methane) have no heavy-atom rotational hindrance proxy and contribute a constant; linear adsorbates are proxied by PMI2; nonlinear adsorbates by PMI3. The pre-declared association is that increasing the class-matched inertia proxy correlates with increasing entropy loss/R, because larger moments of inertia correspond to more restricted rotational libration in the confined framework relative to free gas rotation.",
    "rationale": "PMI proxies come from the original implicit-H/heavy-atom representation; they are not true all-atom moments of inertia and hydrogen rotation is not captured. Legitimate zeros occur for single-site species (54 training rows); the rotor_case construction ensures those rows take the constant branch rather than entering a log of zero, and no median imputation is used. log(1+q) is an empirical monotone smoothing chosen to keep the dimensionless log argument strictly positive at q=0; it carries no universal physical meaning and is disclosed as a numerical form, not a law. The prior h2 (q_PMI3 * q_Vol) showed a consistent positive association (Spearman 0.404) but was not retained; this variant removes the Vol coupling to test the pure inertia axis and makes the rotor-class dependence explicit.",
    "falsification_criteria": "If the class-matched inertia proxy shows training association inconsistent with the declared increasing entropy-loss direction within any rotor class, or if rotor_class-fixed partial-derivative diagnostics show mechanism_validated = false with non-positive marginal MAE improvement, the rotational-hindrance mechanism as proxied by heavy-atom PMI is falsified. A competing mechanism that would also falsify it: entropy loss governed primarily by translational/configurational confinement (h1, h3) with inertia adding no residual signal.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E06"
    ],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Explicit rotor_case branches: single_site -> 1.0 (constant, no heavy-atom inertia proxy exists for single-site species; this does not assert true all-atom inertia is zero); linear -> log(1 + q_PMI2); nonlinear -> log(1 + q_PMI3). Branch selection uses the native PMI proxy categories with normalized tolerance 1e-10. Assumes heavy-atom PMI rank-orders rotational confinement within each class; transfer across chemical classes is not claimed. q_PMI values are row-varying ratios to fixed positive training-reference medians (PMI2_ref = 93.79729089, PMI3_ref = 125.4948325).",
      "physical_interpretation": "Native meanings: PMI2 and PMI3 are the second and third principal moments of inertia of the heavy-atom (implicit-H) molecular representation in angstrom^2*amu. The descriptor is dimensionless; log arguments 1+q are dimensionless by construction. No unity threshold of q is interpreted physically.",
      "boundary_behavior": "Single-site rows (PMI2 = PMI3 = 0, 54 training rows) take the constant branch 1.0, avoiding 0/0 and log(0); the constant encodes the absence of a heavy-atom rotational hindrance proxy rather than zero rotational entropy loss. Linear rows use PMI2 (min 0 in training, but the +1 smoothing keeps log finite at q=0). Nonlinear rows use PMI3, finite for all values in [0, 2414.63]. All branches output dimensionless-compatible values.",
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
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI2": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.3675774051544217,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/small_kg_rag_agent/replicate-2/round-2/h3`

最终状态：scored；边际收益：-0.043238 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.GeDi, variable_mappings.lsd_f

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "cage_window_path_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "Frameworks whose included free-path diameter (lsd_p, Zeo++ Dif) greatly exceeds their passing bottleneck (lsd_f, Zeo++ Df) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom. The pre-declared association is that increasing log(q_lsd_p / q_lsd_f) correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas). Round-1 diagnostics were inconclusive (training Spearman -0.0195) yet the descriptor was retained with the largest marginal MAE improvement (0.0189); the hypothesis remains open pending mechanism-level validation.",
    "rationale": "Df is strictly the passing bottleneck free sphere and Dif is the included sphere along the free-sphere path; neither is the global cavity diameter Di, and Di is not an input to D0. The contrast ratio is a connectivity/topology proxy for cage-vs-channel architecture, not a direct measure of configurational entropy. Both lsd quantities are strictly positive in the training domain (Df in [0.85684, 7.68726], Dif in [3.3452, 15.5604]), so the log argument is always positive and finite. Since all published D0 inputs already enter the nonlinear ANN, this descriptor re-expresses the pair (Dif, Df) as a pure contrast, isolating topology from absolute pore size.",
    "falsification_criteria": "If class-conditional or residual association of log(q_lsd_p/q_lsd_f) with entropy loss/R remains inconclusive or opposite to the declared increasing direction after conditioning on absolute pore size (e.g., alongside h1), the cage-window contrast mechanism is falsified for this dataset. A competing mechanism that would also falsify it: entropy loss set by absolute bottleneck size (Df alone) rather than the Dif/Df contrast, in which case the ratio adds no information beyond the ANN's existing inputs.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Assumes Zeo++ Df/Dif geometry on the published numerical scale rank-orders cage-like vs channel-like connectivity for these frameworks. Assumes kinetic escape topology relates to equilibrium configurational restriction only indirectly; AV fixed-probe accessibility and kinetic escape do not by themselves determine equilibrium entropy, so this is a proxy claim only. q_lsd_p and q_lsd_f are row-varying ratios to fixed positive training-reference medians (lsd_p_ref = 6.38663, lsd_f_ref = 5.16326).",
      "physical_interpretation": "Native meanings: lsd_f is the largest sphere that can pass through a periodic free path (bottleneck); lsd_p is the largest included sphere along that path. The descriptor is the dimensionless log-contrast; q = 1 carries no physical unity threshold. The descriptor is invariant to equal scaling of both diameters and responds only to their contrast.",
      "boundary_behavior": "Both inputs are strictly positive across the entire training domain, so q_lsd_p/q_lsd_f > 0 and the log is finite for all 2361 rows. The ratio is bounded by the native domain (roughly Dif/Df in a physically realizable range where Dif >= path-relevant included spheres); no zero, near-zero, or negative argument arises, and no epsilon is needed.",
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
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "lsd_f": "bottleneck_free_sphere_Df",
        "lsd_p": "included_along_free_path_Dif"
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
    "name": "cage_window_path_contrast",
    "formula": "q_GeDi / q_lsd_p",
    "hypothesis": "Frameworks whose included free-path diameter (lsd_p, Zeo++ Dif) greatly exceeds their passing bottleneck (lsd_f, Zeo++ Df) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom. The pre-declared association is that increasing log(q_lsd_p / q_lsd_f) correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas). Round-1 diagnostics were inconclusive (training Spearman -0.0195) yet the descriptor was retained with the largest marginal MAE improvement (0.0189); the hypothesis remains open pending mechanism-level validation.",
    "rationale": "The previous cage-window contrast log(q_lsd_p/q_lsd_f) was rejected as redundant, so the slot is replaced by a molecule-to-cavity contrast that is a new combination rather than a re-expression of the retained descriptor. Under the stored connectivity family and the fixed increasing entropy-loss direction, the claim is conditional: frameworks whose included free-path diameter (lsd_p, Dif) is small relative to the adsorbate's heavy-atom span (GeDi) confine the molecule more tightly in cage-scale space, which the cited sources associate with larger entropy losses (E02: smaller cavity diameter, greater reported rotational entropy loss in FER vs FAU; E06: rotational freedom inside MCM-22 supercages proposed to affect adsorption equilibrium). This is a proxy association only: Dif is not Di, GeDi is a heavy-atom length, and neither kinetic escape nor fixed-probe geometry determines equilibrium entropy by itself. Because all published D0 inputs already enter the nonlinear ANN, the descriptor can only re-express existing inputs; its value is testing whether the molecule-to-cavity axis carries residual entropy-loss association not captured by h1 (volume axis) and h2 (rotor-class inertia axis).",
    "falsification_criteria": "If the training association of q_GeDi/q_lsd_p with entropy loss/R is opposite to the declared increasing direction, or if the marginal MAE improvement over the retained baseline set (including h1 and h2) is non-positive, the molecule-to-cavity contrast mechanism is falsified for this dataset. Competing mechanisms that would also falsify it: entropy loss governed primarily by accessible-volume (h1) or rotor-class inertia (h2) axes with no residual GeDi/lsd_p signal; entropy loss set by absolute pore size rather than the molecule-to-cavity contrast; or a representation artifact in which the heavy-atom GeDi zeros of single-site rows drive the association.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E06"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "GeDi (largest distance between two molecular atoms, implicit-H/heavy-atom representation) is used as a molecular length-scale proxy; hydrogen extent is not captured, so the true molecular span can be larger. lsd_p is Zeo++ Dif, the largest included sphere ALONG the free-sphere path; it is NOT the global cavity diameter Di and is used only as a conditional cavity-scale proxy per the diameter-roles constraint (the source mechanism in E02 refers to average cavity diameter, a different quantity). The ratio is a dimensionless molecule-to-cavity confinement contrast used as an empirical proxy only; q-ratio = 1 carries no physical unity-threshold meaning. Transfer from the reported MFI/FAU/FER and MCM-22 comparisons to pure-silica rigid frameworks at infinite dilution remains a hypothesis; no source percentage or coefficient becomes a constant.",
      "physical_interpretation": "Native meanings: GeDi is the largest interatomic distance within the adsorbate (angstrom, heavy-atom representation); lsd_p is the largest included sphere along the periodic free-sphere path (angstrom, Zeo++ Dif). q_GeDi and q_lsd_p are row-varying ratios to fixed positive training-reference medians (GeDi_ref = 3.302656784, lsd_p_ref = 6.38663). The descriptor is dimensionless; it contrasts molecular span with cavity-scale included space, so a larger value indicates a molecule filling more of the cage-scale space available to it.",
      "boundary_behavior": "GeDi has legitimate zeros for the 54 single-site rows (a single heavy atom in the implicit-H representation yields zero maximum pair distance); there the descriptor is exactly 0 because q_lsd_p > 0 everywhere (native lsd_p in [3.3452, 15.5604]). This is a disclosed representation zero of the heavy-atom pair-distance proxy, not an imputation and not a claim that the true molecular diameter of a single-site adsorbate is zero. For all non-single-site rows GeDi > 0 and the ratio is smooth and strictly positive. The denominator is never zero, so there is no division by a legitimate zero, no log of a non-positive argument, and no epsilon anywhere in the training domain.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
      "regime_input": "GeDi",
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
        "GeDi",
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.6546880504725221,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
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
    "name": "cage_window_path_contrast",
    "formula": "q_GeDi / q_lsd_p",
    "hypothesis": "Frameworks whose included free-path diameter (lsd_p, Zeo++ Dif) greatly exceeds their passing bottleneck (lsd_f, Zeo++ Df) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom. The pre-declared association is that increasing log(q_lsd_p / q_lsd_f) correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas). Round-1 diagnostics were inconclusive (training Spearman -0.0195) yet the descriptor was retained with the largest marginal MAE improvement (0.0189); the hypothesis remains open pending mechanism-level validation.",
    "rationale": "The previous cage-window contrast log(q_lsd_p/q_lsd_f) was rejected as redundant, so the slot is replaced by a molecule-to-cavity contrast that is a new combination rather than a re-expression of the retained descriptor. Under the stored connectivity family and the fixed increasing entropy-loss direction, the claim is conditional: frameworks whose included free-path diameter (lsd_p, Dif) is small relative to the adsorbate's heavy-atom span (GeDi) confine the molecule more tightly in cage-scale space, which the cited sources associate with larger entropy losses (E02: smaller cavity diameter, greater reported rotational entropy loss in FER vs FAU; E06: rotational freedom inside MCM-22 supercages proposed to affect adsorption equilibrium). This is a proxy association only: Dif is not Di, GeDi is a heavy-atom length, and neither kinetic escape nor fixed-probe geometry determines equilibrium entropy by itself. Because all published D0 inputs already enter the nonlinear ANN, the descriptor can only re-express existing inputs; its value is testing whether the molecule-to-cavity axis carries residual entropy-loss association not captured by h1 (volume axis) and h2 (rotor-class inertia axis).",
    "falsification_criteria": "If the training association of q_GeDi/q_lsd_p with entropy loss/R is opposite to the declared increasing direction, or if the marginal MAE improvement over the retained baseline set (including h1 and h2) is non-positive, the molecule-to-cavity contrast mechanism is falsified for this dataset. Competing mechanisms that would also falsify it: entropy loss governed primarily by accessible-volume (h1) or rotor-class inertia (h2) axes with no residual GeDi/lsd_p signal; entropy loss set by absolute pore size rather than the molecule-to-cavity contrast; or a representation artifact in which the heavy-atom GeDi zeros of single-site rows drive the association.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E06"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "GeDi (largest distance between two molecular atoms, implicit-H/heavy-atom representation) is used as a molecular length-scale proxy; hydrogen extent is not captured, so the true molecular span can be larger. lsd_p is Zeo++ Dif, the largest included sphere ALONG the free-sphere path; it is NOT the global cavity diameter Di and is used only as a conditional cavity-scale proxy per the diameter-roles constraint (the source mechanism in E02 refers to average cavity diameter, a different quantity). The ratio is a dimensionless molecule-to-cavity confinement contrast used as an empirical proxy only; q-ratio = 1 carries no physical unity-threshold meaning. Transfer from the reported MFI/FAU/FER and MCM-22 comparisons to pure-silica rigid frameworks at infinite dilution remains a hypothesis; no source percentage or coefficient becomes a constant.",
      "physical_interpretation": "Native meanings: GeDi is the largest interatomic distance within the adsorbate (angstrom, heavy-atom representation); lsd_p is the largest included sphere along the periodic free-sphere path (angstrom, Zeo++ Dif). q_GeDi and q_lsd_p are row-varying ratios to fixed positive training-reference medians (GeDi_ref = 3.302656784, lsd_p_ref = 6.38663). The descriptor is dimensionless; it contrasts molecular span with cavity-scale included space, so a larger value indicates a molecule filling more of the cage-scale space available to it.",
      "boundary_behavior": "GeDi has legitimate zeros for the 54 single-site rows (a single heavy atom in the implicit-H representation yields zero maximum pair distance); there the descriptor is exactly 0 because q_lsd_p > 0 everywhere (native lsd_p in [3.3452, 15.5604]). This is a disclosed representation zero of the heavy-atom pair-distance proxy, not an imputation and not a claim that the true molecular diameter of a single-site adsorbate is zero. For all non-single-site rows GeDi > 0 and the ratio is smooth and strictly positive. The denominator is never zero, so there is no division by a legitimate zero, no log of a non-positive argument, and no epsilon anywhere in the training domain.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
      "regime_input": "GeDi",
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
        "GeDi",
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.6546880504725221,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
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
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
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
        "record_id": "chunk:3bfcfc2025ac5aeef52fad62",
        "paper_id": "doi:10.1039/d5cs00613a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a0cd449d6b57331770df6c51",
        "paper_id": "doi:10.1021/acs.langmuir.2c00923",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:147fa339122edc3ff44ba658",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:560d540c09c85dfa3faa0e8c",
        "paper_id": "doi:10.1021/acs.jpcb.1c02929",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:8dc09a802942ff3d455ea3a8",
        "paper_id": "doi:10.26434/chemrxiv.9725948.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:93de9e75ac405f37027570ab",
        "paper_id": "doi:10.1038/nmat1090",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b86d2d3284fbbe6696210c35",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c879f65535252d897ab77d4e",
        "paper_id": "doi:10.1039/c3cc40731d",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, the ratio of the framework's probe-accessible specific volume (AV) to the adsorbate's van der Waals volume (Vol) proxies the translational free space available per unit of molecular size. The pre-declared association is that increasing AV/Vol (more accessible volume relative to molecular volume) correlates with decreasing entropy loss/R, because a larger relative free volume permits more translational microstates in the adsorbed phase relative to the gas. q_AV / q_Vol Rotational entropy loss on adsorption at infinite dilution scales with the heavy-atom principal moment of inertia about the largest axis, with the relevant proxy depending on rotor class: single-site adsorbates (e.g., methane) have no heavy-atom rotational hindrance proxy and contribute a constant; linear adsorbates are proxied by PMI2; nonlinear adsorbates by PMI3. The pre-declared association is that increasing the class-matched inertia proxy correlates with increasing entropy loss/R, because larger moments of inertia correspond to more restricted rotational libration in the confined framework relative to free gas rotation. rotor_case(1.0, log(1.0 + q_PMI2), log(1.0 + q_PMI3)) Frameworks whose included free-path diameter (lsd_p, Zeo++ Dif) greatly exceeds their passing bottleneck (lsd_f, Zeo++ Df) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom. The pre-declared association is that increasing log(q_lsd_p / q_lsd_f) correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas). Round-1 diagnostics were inconclusive (training Spearman -0.0195) yet the descriptor was retained with the largest marginal MAE improvement (0.0189); the hypothesis remains open pending mechanism-level validation. log(q_lsd_p / q_lsd_f)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:e98dff054a73e56b28f6bdf3",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:d52b47528dc9757d7e603c4f"
    ],
    "items": 10,
    "lexical_tokens": 4791,
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
