# high/small_kg_rag_agent/replicate-2/round-3

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

候选标识：`high/small_kg_rag_agent/replicate-2/round-3/h1`

最终状态：scored；边际收益：-1.731558 pp；保留：False。

复核改动字段：evidence_ids

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "molecular_length_bottleneck_mismatch",
    "formula": "q_GeDi / q_lsd_f",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, when the adsorbate's largest heavy-atom extent (GeDi) is large relative to the framework's passing free-sphere bottleneck (Df), the molecule experiences stronger translational confinement in the pore network, and the pre-declared association is that increasing GeDi/Df mismatch correlates with increasing entropy loss/R (reduced adsorbed-phase translational freedom relative to the gas).",
    "rationale": "The passing bottleneck Df (lsd_f) bounds the connectivity of the pore network for a hard probe, while GeDi measures the molecular long-axis extent in the heavy-atom representation. A large ratio indicates a molecule whose span is comparable to or larger than the window opening, plausibly restricting translational excursions between cages or channels. This is a geometric confinement proxy only: Df is a hard-sphere bottleneck, not a molecule-specific window, GeDi ignores hydrogen atoms and conformational flexibility, and equilibrium entropy loss is not determined by kinetic escape alone.",
    "falsification_criteria": "If the training Spearman association between q_GeDi/q_lsd_f and entropy loss/R is opposite in sign to the declared increasing direction, or if the descriptor's marginal MAE contribution is non-positive relative to the retained model, the confinement-mismatch mechanism as proxied here is falsified for this dataset; a competing mechanism is that accessible volume (AV) rather than bottleneck geometry controls translational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "GeDi is an implicit-H/heavy-atom proxy for molecular span, not the full all-atom kinetic diameter; lsd_f is the Zeo++ passing bottleneck, not the global cavity diameter Di; the ratio assumes hard-sphere-like steric confinement dominates translational entropy loss at infinite dilution.",
      "physical_interpretation": "The descriptor uses only native quantities through q-normalization against fixed training-reference medians; q-unity carries no physical threshold meaning, only scale.",
      "boundary_behavior": "GeDi has legitimate zeros (54 training rows, e.g. single-site proxies) giving descriptor value 0, which is finite and interpreted as no steric mismatch; lsd_f is strictly positive in the training domain [0.85684, 7.68726], so no division by zero occurs.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
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
        "GeDi",
        "lsd_f"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.608006859917338,
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
    "name": "molecular_length_bottleneck_mismatch",
    "formula": "q_GeDi / q_lsd_f",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, when the adsorbate's largest heavy-atom extent (GeDi) is large relative to the framework's passing free-sphere bottleneck (Df), the molecule experiences stronger translational confinement in the pore network, and the pre-declared association is that increasing GeDi/Df mismatch correlates with increasing entropy loss/R (reduced adsorbed-phase translational freedom relative to the gas).",
    "rationale": "The passing bottleneck Df (lsd_f) bounds the connectivity of the pore network for a hard probe, while GeDi measures the molecular long-axis extent in the heavy-atom representation. A large ratio indicates a molecule whose span is comparable to or larger than the window opening, plausibly restricting translational excursions between cages or channels. This is a geometric confinement proxy only: Df is a hard-sphere bottleneck, not a molecule-specific window, GeDi ignores hydrogen atoms and conformational flexibility, and equilibrium entropy loss is not determined by kinetic escape alone.",
    "falsification_criteria": "If the training Spearman association between q_GeDi/q_lsd_f and entropy loss/R is opposite in sign to the declared increasing direction, or if the descriptor's marginal MAE contribution is non-positive relative to the retained model, the confinement-mismatch mechanism as proxied here is falsified for this dataset; a competing mechanism is that accessible volume (AV) rather than bottleneck geometry controls translational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "GeDi is an implicit-H/heavy-atom proxy for molecular span, not the full all-atom kinetic diameter; lsd_f is the Zeo++ passing bottleneck, not the global cavity diameter Di; the ratio assumes hard-sphere-like steric confinement dominates translational entropy loss at infinite dilution.",
      "physical_interpretation": "The descriptor uses only native quantities through q-normalization against fixed training-reference medians; q-unity carries no physical threshold meaning, only scale.",
      "boundary_behavior": "GeDi has legitimate zeros (54 training rows, e.g. single-site proxies) giving descriptor value 0, which is finite and interpreted as no steric mismatch; lsd_f is strictly positive in the training domain [0.85684, 7.68726], so no division by zero occurs.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
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
        "GeDi",
        "lsd_f"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.608006859917338,
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
    "name": "molecular_length_bottleneck_mismatch",
    "formula": "q_GeDi / q_lsd_f",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, when the adsorbate's largest heavy-atom extent (GeDi) is large relative to the framework's passing free-sphere bottleneck (Df), the molecule experiences stronger translational confinement in the pore network, and the pre-declared association is that increasing GeDi/Df mismatch correlates with increasing entropy loss/R (reduced adsorbed-phase translational freedom relative to the gas).",
    "rationale": "The passing bottleneck Df (lsd_f) bounds the connectivity of the pore network for a hard probe, while GeDi measures the molecular long-axis extent in the heavy-atom representation. A large ratio indicates a molecule whose span is comparable to or larger than the window opening, plausibly restricting translational excursions between cages or channels. This is a geometric confinement proxy only: Df is a hard-sphere bottleneck, not a molecule-specific window, GeDi ignores hydrogen atoms and conformational flexibility, and equilibrium entropy loss is not determined by kinetic escape alone.",
    "falsification_criteria": "If the training Spearman association between q_GeDi/q_lsd_f and entropy loss/R is opposite in sign to the declared increasing direction, or if the descriptor's marginal MAE contribution is non-positive relative to the retained model, the confinement-mismatch mechanism as proxied here is falsified for this dataset; a competing mechanism is that accessible volume (AV) rather than bottleneck geometry controls translational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "GeDi is an implicit-H/heavy-atom proxy for molecular span, not the full all-atom kinetic diameter; lsd_f is the Zeo++ passing bottleneck, not the global cavity diameter Di; the ratio assumes hard-sphere-like steric confinement dominates translational entropy loss at infinite dilution.",
      "physical_interpretation": "The descriptor uses only native quantities through q-normalization against fixed training-reference medians; q-unity carries no physical threshold meaning, only scale.",
      "boundary_behavior": "GeDi has legitimate zeros (54 training rows, e.g. single-site proxies) giving descriptor value 0, which is finite and interpreted as no steric mismatch; lsd_f is strictly positive in the training domain [0.85684, 7.68726], so no division by zero occurs.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
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
        "GeDi",
        "lsd_f"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.608006859917338,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/small_kg_rag_agent/replicate-2/round-3/h2`

最终状态：scored；边际收益：+4.190223 pp；保留：True。

复核改动字段：evidence_ids, scientific_test.boundary_behavior

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "inertial_anisotropy_rotational_hindrance",
    "formula": "log(1.0 + q_PMI3) - log(1.0 + q_PMI1)",
    "hypothesis": "Adsorbates whose heavy-atom principal moment ratio PMI3/PMI1 is large (elongated or anisotropic shapes) have fewer accessible rotational orientations inside rigid pure-silica pore geometries at infinite dilution, because reorientation of a long axis is sterically restricted; the pre-declared association is that increasing inertial anisotropy correlates with increasing entropy loss/R through the rotational contribution.",
    "rationale": "PMI1 and PMI3 are the smallest and largest heavy-atom principal moments; their contrast is a shape-anisotropy proxy in the original implicit-H representation. Anisotropic molecules in confined geometries plausibly lose orientational/rotational freedom relative to the gas. Limitations: these are heavy-atom inertia proxies, not true all-atom moments (single-site molecules legitimately have zero moments, which is not asserted to be physical all-atom inertia); the log(1+q) form is an empirical smoothing choice with no universal physical meaning, adopted to keep the descriptor finite and monotone across the legitimate zero boundary; rotor class is held fixed in the diagnostic partial derivative.",
    "falsification_criteria": "If the training Spearman association of the anisotropy descriptor with entropy loss/R is opposite to the declared increasing direction, or if stratifying by rotor class (single-site vs linear vs nonlinear) removes the association, the rotational-hindrance interpretation is falsified and the descriptor would instead be reinterpreted as a bulk size/shape surrogate coupled to translational or volume effects.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI1": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI contrast proxies rotational shape anisotropy; transfer to all-atom rotational entropy is imperfect, especially for single-site and linear rotors where PMI1 is legitimately zero; the 1+q offset is empirical smoothing, not physics.",
      "physical_interpretation": "Native PMI1 and PMI3 are principal moments in the original implicit-H representation; q-normalization is against the fixed training-reference medians (PMI1_ref = 43.29513794, PMI3_ref = 125.4948325) and carries no universal physical meaning.",
      "boundary_behavior": "At PMI1 = 0 (113 training rows, including single-site and linear proxies), the descriptor reduces to log(1 + q_PMI3), which is finite and non-negative; at PMI3 = 0 the descriptor is log(1 + q_PMI1) shifted, also finite; no legitimate zero is divided by and no imputation is used.",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI1",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.205832341455294,
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
    "name": "inertial_anisotropy_rotational_hindrance",
    "formula": "log(1.0 + q_PMI3) - log(1.0 + q_PMI1)",
    "hypothesis": "Adsorbates whose heavy-atom principal moment ratio PMI3/PMI1 is large (elongated or anisotropic shapes) have fewer accessible rotational orientations inside rigid pure-silica pore geometries at infinite dilution, because reorientation of a long axis is sterically restricted; the pre-declared association is that increasing inertial anisotropy correlates with increasing entropy loss/R through the rotational contribution.",
    "rationale": "PMI1 and PMI3 are the smallest and largest heavy-atom principal moments; their contrast is a shape-anisotropy proxy in the original implicit-H representation. Anisotropic molecules in confined geometries plausibly lose orientational/rotational freedom relative to the gas. Limitations: these are heavy-atom inertia proxies, not true all-atom moments (single-site molecules legitimately have zero moments, which is not asserted to be physical all-atom inertia); the log(1+q) form is an empirical smoothing choice with no universal physical meaning, adopted to keep the descriptor finite and monotone across the legitimate zero boundary; rotor class is held fixed in the diagnostic partial derivative.",
    "falsification_criteria": "If the training Spearman association of the anisotropy descriptor with entropy loss/R is opposite to the declared increasing direction, or if stratifying by rotor class (single-site vs linear vs nonlinear) removes the association, the rotational-hindrance interpretation is falsified and the descriptor would instead be reinterpreted as a bulk size/shape surrogate coupled to translational or volume effects.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E06"
    ],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI1": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI contrast proxies rotational shape anisotropy; transfer to all-atom rotational entropy is imperfect, especially for single-site and linear rotors where PMI1 is legitimately zero; the 1+q offset is empirical smoothing, not physics.",
      "physical_interpretation": "Native PMI1 and PMI3 are principal moments in the original implicit-H representation; q-normalization is against the fixed training-reference medians (PMI1_ref = 43.29513794, PMI3_ref = 125.4948325) and carries no universal physical meaning.",
      "boundary_behavior": "At PMI1 = 0 (113 training rows, including single-site and linear-rotor proxies) the descriptor reduces to log(1 + q_PMI3), which is finite and non-negative. PMI3 = 0 can only occur together with PMI1 = 0 because principal moments are ordered PMI1 <= PMI2 <= PMI3; the 54 such single-site rows therefore give descriptor value exactly 0, not log(1 + q_PMI1). No legitimate zero is divided by and no imputation is used; the 1+q offsets are empirical smoothing that keeps the descriptor finite across the zero boundary.",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI1",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.205832341455294,
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
    "name": "inertial_anisotropy_rotational_hindrance",
    "formula": "log(1.0 + q_PMI3) - log(1.0 + q_PMI1)",
    "hypothesis": "Adsorbates whose heavy-atom principal moment ratio PMI3/PMI1 is large (elongated or anisotropic shapes) have fewer accessible rotational orientations inside rigid pure-silica pore geometries at infinite dilution, because reorientation of a long axis is sterically restricted; the pre-declared association is that increasing inertial anisotropy correlates with increasing entropy loss/R through the rotational contribution.",
    "rationale": "PMI1 and PMI3 are the smallest and largest heavy-atom principal moments; their contrast is a shape-anisotropy proxy in the original implicit-H representation. Anisotropic molecules in confined geometries plausibly lose orientational/rotational freedom relative to the gas. Limitations: these are heavy-atom inertia proxies, not true all-atom moments (single-site molecules legitimately have zero moments, which is not asserted to be physical all-atom inertia); the log(1+q) form is an empirical smoothing choice with no universal physical meaning, adopted to keep the descriptor finite and monotone across the legitimate zero boundary; rotor class is held fixed in the diagnostic partial derivative.",
    "falsification_criteria": "If the training Spearman association of the anisotropy descriptor with entropy loss/R is opposite to the declared increasing direction, or if stratifying by rotor class (single-site vs linear vs nonlinear) removes the association, the rotational-hindrance interpretation is falsified and the descriptor would instead be reinterpreted as a bulk size/shape surrogate coupled to translational or volume effects.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E06"
    ],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI1": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI contrast proxies rotational shape anisotropy; transfer to all-atom rotational entropy is imperfect, especially for single-site and linear rotors where PMI1 is legitimately zero; the 1+q offset is empirical smoothing, not physics.",
      "physical_interpretation": "Native PMI1 and PMI3 are principal moments in the original implicit-H representation; q-normalization is against the fixed training-reference medians (PMI1_ref = 43.29513794, PMI3_ref = 125.4948325) and carries no universal physical meaning.",
      "boundary_behavior": "At PMI1 = 0 (113 training rows, including single-site and linear-rotor proxies) the descriptor reduces to log(1 + q_PMI3), which is finite and non-negative. PMI3 = 0 can only occur together with PMI1 = 0 because principal moments are ordered PMI1 <= PMI2 <= PMI3; the 54 such single-site rows therefore give descriptor value exactly 0, not log(1 + q_PMI1). No legitimate zero is divided by and no imputation is used; the 1+q offsets are empirical smoothing that keeps the descriptor finite across the zero boundary.",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI1",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.205832341455294,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/small_kg_rag_agent/replicate-2/round-3/h3`

最终状态：scored；边际收益：+2.051071 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.Vol, variable_mappings.lsd_f

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "cage_window_path_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "Frameworks whose included free-path diameter (Dif, lsd_p) greatly exceeds their passing bottleneck (Df, lsd_f) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom, and the pre-declared association is that increasing path contrast correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas).",
    "rationale": "The Dif/Df contrast distinguishes cage-window topologies from channel-like topologies using only framework geometry. The association direction is pre-declared as increasing entropy loss with increasing contrast. Limitations acknowledged: both quantities are hard-sphere geometric proxies on the fixed probe scale, the contrast does not encode adsorbate size, and the round-1 diagnostic showed an inconclusive training Spearman (-0.019), so the descriptor is retained for its positive marginal MAE contribution rather than a validated mechanism; correlation and perturbation tests do not establish causality.",
    "falsification_criteria": "If re-scoring confirms a non-positive marginal MAE contribution, or if the sign of the training association becomes significantly opposite to the declared increasing entropy-loss direction at sufficient sample resolution, the cage-window contrast hypothesis as proxied by Dif/Df is falsified; a competing mechanism is that bottleneck size alone (Df) rather than the contrast controls translational entropy loss.",
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
      "proxy_assumptions": "lsd_p is the largest included sphere along the free-sphere path and lsd_f is the passing bottleneck; neither equals the global cavity diameter Di; the contrast is assumed to proxy cage-vs-channel topology effects on configurational entropy without adsorbate-specific steric terms.",
      "physical_interpretation": "Both inputs are strictly positive in the training domain (lsd_f in [0.85684, 7.68726], lsd_p in [3.3452, 15.5604]); the log of the q-ratio is dimensionless and its unity carries no physical threshold meaning.",
      "boundary_behavior": "No legitimate zeros exist for lsd_f or lsd_p in the training domain, so the ratio and logarithm are finite for every training row; the descriptor would diverge only outside the physical domain, which does not occur here and requires no imputation.",
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
    "formula": "q_Vol / (q_lsd_p ** 3)",
    "hypothesis": "Frameworks whose included free-path diameter (Dif, lsd_p) greatly exceeds their passing bottleneck (Df, lsd_f) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom, and the pre-declared association is that increasing path contrast correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas).",
    "rationale": "The prior draft resubmitted log(q_lsd_p / q_lsd_f), which was already retained in round 1 and was correctly rejected as redundant. Since the stored cage-window connectivity hypothesis cannot be edited, this patch keeps the slot within the same connectivity family but replaces the duplicate with a complementary, non-redundant contrast: how much of the along-path included (cage-scale) volume proxy the adsorbate itself occupies. In frameworks where the included free-path diameter greatly exceeds the bottleneck (cage-like topology, retained separately via the Dif/Df contrast), a molecule that fills a larger fraction of the cage-scale volume is pre-declared to retain less local positional and orientational freedom, correlating with increasing entropy loss/R. Sources qualitatively support molecule-size-versus-available-cage-space contrasts (radius of gyration relative to available supercage space) as affecting adsorption entropy, but transfer to this benchmark is a hypothesis; no source coefficient becomes a constant, and association/perturbation diagnostics do not establish causality.",
    "falsification_criteria": "If the training Spearman association between q_Vol / (q_lsd_p ** 3) and entropy loss/R is opposite in sign to the declared increasing direction, or if the descriptor's marginal MAE contribution is non-positive relative to the retained model, or if stratifying by cage-vs-channel character (high vs low retained Dif/Df contrast) removes the association, the molecule-to-cage-scale packing modulation of the connectivity mechanism is falsified for this dataset. A competing mechanism is that accessible volume (AV) or bottleneck size (Df) alone, rather than the molecule-to-included-path packing contrast, controls the entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06",
      "E07",
      "E09"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "lsd_p (Zeo++ Dif) is the largest included sphere along the free-sphere path, NOT the global cavity diameter Di and NOT a measured cage volume; cubing it is an empirical cubic length-scale choice for a cage-scale volume proxy with no universal physical meaning. Vol is the van der Waals volume of a rigid molecule and ignores conformational flexibility. The packing contrast is a hard-sphere geometric proxy assumed to modulate how much local freedom a molecule retains inside cage-like regions of the connected pore network; equilibrium entropy loss is not determined by packing geometry alone.",
      "physical_interpretation": "Vol is the adsorbate van der Waals volume; lsd_p is the included-along-free-path diameter of the framework. q-normalization uses the fixed positive training-reference medians (Vol_ref = 67.24, lsd_p_ref = 6.38663); q-unity carries no physical threshold meaning and the descriptor is a dimensionless molecule-to-path-scale packing contrast, not an equality test.",
      "boundary_behavior": "Vol is strictly positive over the training domain (min 20.424 angstrom^3, zero_n = 0) and lsd_p is strictly positive (min 3.3452 angstrom, zero_n = 0), so q_lsd_p ** 3 > 0 for every row and the descriptor is finite for all 2361 training rows; no legitimate zero is divided by and no imputation is used. No rotor_proxy input enters the formula, so no rotor_case branches are required.",
      "vary_input": "Vol",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.7364361854222692,
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
    "name": "cage_window_path_contrast",
    "formula": "q_Vol / (q_lsd_p ** 3)",
    "hypothesis": "Frameworks whose included free-path diameter (Dif, lsd_p) greatly exceeds their passing bottleneck (Df, lsd_f) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom, and the pre-declared association is that increasing path contrast correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas).",
    "rationale": "The prior draft resubmitted log(q_lsd_p / q_lsd_f), which was already retained in round 1 and was correctly rejected as redundant. Since the stored cage-window connectivity hypothesis cannot be edited, this patch keeps the slot within the same connectivity family but replaces the duplicate with a complementary, non-redundant contrast: how much of the along-path included (cage-scale) volume proxy the adsorbate itself occupies. In frameworks where the included free-path diameter greatly exceeds the bottleneck (cage-like topology, retained separately via the Dif/Df contrast), a molecule that fills a larger fraction of the cage-scale volume is pre-declared to retain less local positional and orientational freedom, correlating with increasing entropy loss/R. Sources qualitatively support molecule-size-versus-available-cage-space contrasts (radius of gyration relative to available supercage space) as affecting adsorption entropy, but transfer to this benchmark is a hypothesis; no source coefficient becomes a constant, and association/perturbation diagnostics do not establish causality.",
    "falsification_criteria": "If the training Spearman association between q_Vol / (q_lsd_p ** 3) and entropy loss/R is opposite in sign to the declared increasing direction, or if the descriptor's marginal MAE contribution is non-positive relative to the retained model, or if stratifying by cage-vs-channel character (high vs low retained Dif/Df contrast) removes the association, the molecule-to-cage-scale packing modulation of the connectivity mechanism is falsified for this dataset. A competing mechanism is that accessible volume (AV) or bottleneck size (Df) alone, rather than the molecule-to-included-path packing contrast, controls the entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06",
      "E07",
      "E09"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "lsd_p (Zeo++ Dif) is the largest included sphere along the free-sphere path, NOT the global cavity diameter Di and NOT a measured cage volume; cubing it is an empirical cubic length-scale choice for a cage-scale volume proxy with no universal physical meaning. Vol is the van der Waals volume of a rigid molecule and ignores conformational flexibility. The packing contrast is a hard-sphere geometric proxy assumed to modulate how much local freedom a molecule retains inside cage-like regions of the connected pore network; equilibrium entropy loss is not determined by packing geometry alone.",
      "physical_interpretation": "Vol is the adsorbate van der Waals volume; lsd_p is the included-along-free-path diameter of the framework. q-normalization uses the fixed positive training-reference medians (Vol_ref = 67.24, lsd_p_ref = 6.38663); q-unity carries no physical threshold meaning and the descriptor is a dimensionless molecule-to-path-scale packing contrast, not an equality test.",
      "boundary_behavior": "Vol is strictly positive over the training domain (min 20.424 angstrom^3, zero_n = 0) and lsd_p is strictly positive (min 3.3452 angstrom, zero_n = 0), so q_lsd_p ** 3 > 0 for every row and the descriptor is finite for all 2361 training rows; no legitimate zero is divided by and no imputation is used. No rotor_proxy input enters the formula, so no rotor_case branches are required.",
      "vary_input": "Vol",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.7364361854222692,
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
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:234d54d6aae543beff87e7be",
        "paper_id": "doi:10.1039/b504006j",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a37b8c2c0d85816299df600a",
        "paper_id": "pmc:pmc12516733",
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
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b86d2d3284fbbe6696210c35",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:0f96db78126e98f8a456e03b",
        "paper_id": "doi:10.1039/c8cc06106h",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:281808f751362133796cb2fe",
        "paper_id": "doi:10.1021/ja105185r",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:46f247733ebb113afc9a8a26",
        "paper_id": "doi:10.1021/jp050434m",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:780c5f690f3ead9c996b9e32",
        "paper_id": "doi:10.1039/c4cp00109e",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:79eb54bd69f0d3c26a62cffa",
        "paper_id": "pmc:pmc7239313",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:899f3c42d1c6c876da906571",
        "paper_id": "pmc:pmc9888634",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd6885398e28529d477ac4c3",
        "paper_id": "doi:10.1021/acs.jpcb.4c02650",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:147fa339122edc3ff44ba658",
        "paper_id": "doi:10.1039/b819435c",
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
    "query": "adsorption entropy confinement For pure-silica rigid zeolites at infinite dilution, when the adsorbate's largest heavy-atom extent (GeDi) is large relative to the framework's passing free-sphere bottleneck (Df), the molecule experiences stronger translational confinement in the pore network, and the pre-declared association is that increasing GeDi/Df mismatch correlates with increasing entropy loss/R (reduced adsorbed-phase translational freedom relative to the gas). q_GeDi / q_lsd_f Adsorbates whose heavy-atom principal moment ratio PMI3/PMI1 is large (elongated or anisotropic shapes) have fewer accessible rotational orientations inside rigid pure-silica pore geometries at infinite dilution, because reorientation of a long axis is sterically restricted; the pre-declared association is that increasing inertial anisotropy correlates with increasing entropy loss/R through the rotational contribution. log(1.0 + q_PMI3) - log(1.0 + q_PMI1) Frameworks whose included free-path diameter (Dif, lsd_p) greatly exceeds their passing bottleneck (Df, lsd_f) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom, and the pre-declared association is that increasing path contrast correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas). log(q_lsd_p / q_lsd_f)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:e98dff054a73e56b28f6bdf3",
      "chunk:0d886a705a91409f8e891c53",
      "chunk:488a25074219dc1bb01f1486"
    ],
    "items": 10,
    "lexical_tokens": 4600,
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
      "record_id": "chunk:ae6e434cc894357276cba23f",
      "paper_id": "doi:10.1021/jp060657s",
      "document_id": "document:efa163ae1d6a7d3f748b3c99",
      "quote": "this case , both molecules have $ R_g/R_c $ values greater than unity for both the pockets and the central section , which means that the advantage of shorter length in terms of rotational entropy is lost . Indeed , heptane adsorbs preferentially over its branched isomer 2-MeC6 in contrast to the above-mentioned alkane couples ( Table 2 ) . The above considerations concerning supercage adsorption shed a light on the unusual decrease of adsorption enthalpy per carbon atom with increasing chain length (Figure 6). Short linear alkanes (from methane to butane) can reside as a whole inside the pockets where all of their end hydrogen atoms can interact closely with the pore walls, as shown in Figure 12. This results in large interaction energies (adsorption enthalpies) for these molecules and a large increment in adsorption enthalpy per additional carbon atom. But when the chain length increases, the molecule grows toward the central section of the supercage, where there is a much larger free space. As a result of this cage enlargement, the additional carbon atoms will interact to a lesser extent than the atoms residing in the depths of the pocket, explaining the aforementioned enthalpy effect. Whereas butane is at the limit, pentane is too long to reside completely in the pocket and has at least one methyl group in the central section, where the distance between the hydrogen atoms and the atoms of the framework is larger, explaining the lower difference in adsorption enthalpy between n-C4 and n-C5 (5.7 kJ/mol) compared to that of n-C4 and n-C3 (7.9 kJ/mol). The same reasoning is valid for n-C6. To explain the discontinuity between n-C6 and n-C7 in the compensation chart (Figure 8), a different adsorption configuration is proposed, in which the molecules remain as a whole in the central section of the supercage (see Figure 12), where the entropy loss is expected to be lower than in the pockets of the cage.",
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
      "id": "E07"
    },
    {
      "record_id": "chunk:0d886a705a91409f8e891c53",
      "paper_id": "doi:10.1021/acs.jpcc.0c02671",
      "document_id": "document:679638c993b24ed3004656c6",
      "quote": "$ expanded this idea to three-dimensional frameworks by compiling experimentally determined adsorption entropies for alkanes adsorbed in nine aluminosilicate zeolites . They showed that the entropic loss upon adsorption can be linearly correlated with the molecule ' s gas-phase translational and rotational entropies and that the occupiable volume of a zeolite is a useful descriptor in predicting such losses . While the simple elegance of this nearly linear correlation of entropies is suggestive of an underlying physical origin, the extent of its applicability is unknown. This is of special concern considering that the aforementioned data is almost entirely for industrially relevant alkanes. Therefore, within this paper, we avoid this practical constraint by using Monte Carlo simulations to quantify the adsorption entropies for a diverse assortment of molecules in zeolite-like materials. In particular, we use the transferable potentials for phase equilibria (TraPPE) $ ^{32} $ force fields to calculate the adsorption entropies for 37 molecules across 10 functional categories within five pure-silicate zeolites. Our simulation results for this broad set of adsorbate molecules reveal that the correlation of the adsorbed-phase and gas-phase entropies persists, suggesting that these correlations may be much more broadly applicable than reported thus far. As a result, such correlative relationships may be exploited to predict sensible adsorption entropies for a wide range of industrially relevant fluids in zeolites and possibly other host materials. The order of this paper is as follows: Section 2 briefly derives the thermodynamic and statistical mechanical expressions for the entropy that we use for our calculations (full derivations are in the Appendix 1 section). In Section 3, we describe the models of our adsorption systems (i.e., the adsorbates and adsorbents) and how the adsorption entropy was calculated. Section 4 presents the results of our model-based calculations of the adsorbed-phase entropy and discusses the correlation of this entropy with the bulk, gas-phase entropy. This section further presents how the entropy correlations can be cast primarily in terms of adsorbent characteristics and how a more detailed model can be generated based on physically intuitive arguments. Finally, in Section 5, we summarize the paper, offer conclusions, and discuss opportunities for future work.",
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
