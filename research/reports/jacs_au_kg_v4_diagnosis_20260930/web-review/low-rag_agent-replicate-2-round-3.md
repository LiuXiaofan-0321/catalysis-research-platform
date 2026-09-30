# low/rag_agent/replicate-2/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/rag_agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h3",
    "name": "planarity_shape_locking",
    "formula": "q_PBF * sqrt(q_SPAN * q_GeDi) / maximum(q_ASA, 0.01)",
    "hypothesis": "Entropy loss rises when adsorbates are planar or elongated (large PBF, SPAN, GeDi) relative to the framework's accessible specific surface area, because flat/extended shapes lose more orientational/configurational entropy when pinned against framework surfaces.",
    "rationale": "Shape-matching argument: planar/extended adsorbates pinned on framework walls lose more orientational/configurational entropy, with ASA per mass as a connectivity proxy (E06, E08 context). Association test only; the competing explanation that PBF merely correlates with Vol is explicitly declared.",
    "falsification_criteria": "If MAE worsens versus a mass-only baseline, or if the PBF association is not monotonic within ASA quartiles, the shape-locking mechanism is rejected; the competing Vol-correlation mechanism then stands.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06"
    ],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "SPAN": "heavy_atom_enclosing_radius",
      "GeDi": "heavy_atom_pair_distance",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF/SPAN/GeDi are implicit-H heavy-atom proxies, not full all-atom geometry; ASA is fixed-probe specific area, and ASA=0 does not imply zero molecular adsorption space. The 0.01 cap affects only the 28 zero-ASA rows and its value is a numerical convention.",
      "physical_interpretation": "q_* are dimensionless ratios to fixed positive training-reference medians (or 0 for legitimate zeros); no physical unity threshold.",
      "boundary_behavior": "ASA=0 occurs in 28 training rows; dividing by q_ASA there is undefined. The guard maximum(q_ASA, 0.01) substitutes a fixed positive cap on 28 rows (1.19% of training), declared as an empirical smoothing device with no physical meaning; it keeps every row finite without imputing a physical ASA value. PBF=0 (587 rows), SPAN=0 and GeDi=0 (54 rows) are legitimate heavy-atom zeros and make the descriptor 0, the declared unlocked-shape limit.",
      "vary_input": "PBF",
      "descriptor_direction": "increasing",
      "regime_input": "ASA",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  {
    "slot_id": "h3",
    "name": "volume_accessibility_coupling",
    "formula": "q_Vol * q_LabuteASA * q_AV",
    "hypothesis": "Entropy loss increases when the adsorbate's Van der Waals volume times its molecular surface area is large relative to the framework's probe-accessible specific pore volume, because bulky, high-surface-area molecules have fewer accessible configurations in a fixed-probe pore volume, amplifying configurational entropy loss at infinite dilution.",
    "rationale": "Direction correction: the previous ratio against maximum(q_AV, 0.05) was contradicted by the training target association (Spearman +0.676 with the declared decreasing direction). The patched descriptor multiplies the adsorbate size-shape product by the fixed-probe accessible specific volume, predeclaring an increasing dependence on AV: frameworks with larger probe-accessible volume provide more retained configurational freedom per adsorbate, so the predicted entropy loss decreases as AV grows, while bulky, high-surface-area adsorbates amplify the loss. The arbitrary 0.05 floor and its implied constant 20 are removed. Limitations: AV is a fixed-geometric-probe, mass-specific accessibility, not molecule-specific free volume; the Vol*LabuteASA product is an empirical size-shape proxy, not a physical equality; legitimate AV zeros are preserved (product is then zero), not imputed.",
    "falsification_criteria": "If the training Spearman of the descriptor against entropy loss/R shows an association opposite to the predeclared direction (descriptor increasing in AV should correspond to decreasing entropy loss), or if the marginal MAE improvement over the retained set is non-positive, the volume-accessibility coupling hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "LabuteASA": "adsorbate_geometry_proxy",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "AV is a fixed-probe accessibility proxy; zero fixed-probe accessibility does not imply zero physical adsorption space. LabuteASA is an implicit-H surface approximation. These proxies transfer across adsorbates only qualitatively.",
      "physical_interpretation": "Native quantities: Van der Waals volume (angstrom^3), Labute approximate surface (angstrom^2), fixed-probe accessible specific volume (cm^3/g). The product is an empirical coupling proxy with mixed native units, not a dimensionally derived physical quantity.",
      "boundary_behavior": "Vol and LabuteASA are strictly positive on training (min 20.424 and 7.45), so the product is finite for all 2361 rows; for the 28 AV = 0 rows the descriptor is exactly zero (pure loss of the coupling term), which is a finite legitimate value, not an imputation.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
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

候选标识：`low/rag_agent/replicate-2/round-3/h1`

最终状态：scored；边际收益：-5.427646 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_translation_restriction",
    "formula": "q_Vol / q_lsd_f",
    "hypothesis": "At infinite dilution, entropy loss rises when the adsorbate's van der Waals volume is large relative to the framework's bottleneck free-sphere diameter, because tighter confinement restricts translational configurational freedom.",
    "rationale": "The descriptor couples a fixed-probe bottleneck proxy (Zeo++ Df) with adsorbate size; it does not encode global cavity diameter Di or molecule-specific free volume. Scaling by the fixed training reference gives a dimensionless ratio; q_lsd_f is positive throughout the training domain, so the ratio is finite for all rows.",
    "falsification_criteria": "If training Spearman association between q_Vol/q_lsd_f and entropy loss/R is near zero or opposite sign to the predeclared increasing direction, or if the association is fully explained by q_Vol alone, the hypothesis is falsified as a distinct mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
      "proxy_assumptions": "Df from a hard-sphere probe approximates the narrowest passage; molecular volume is a size proxy, not the kinetic diameter; transferability across zeolite topologies is limited by fixed-probe definitions.",
      "physical_interpretation": "q_Vol/q_lsd_f expresses adsorbate size relative to bottleneck passage on dimensionless training-reference scales; no physical unity threshold is implied.",
      "boundary_behavior": "q_lsd_f ranges over [0.857/5.163, 7.687/5.163] and is strictly positive in training, so the ratio is finite everywhere; no zero-division arises in the native regime.",
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
      "training_spearman": 0.6317416420940126,
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
    "name": "bottleneck_translation_restriction",
    "formula": "q_Vol / q_lsd_f",
    "hypothesis": "At infinite dilution, entropy loss rises when the adsorbate's van der Waals volume is large relative to the framework's bottleneck free-sphere diameter, because tighter confinement restricts translational configurational freedom.",
    "rationale": "The descriptor couples a fixed-probe bottleneck proxy (Zeo++ Df) with adsorbate size; it does not encode global cavity diameter Di or molecule-specific free volume. Scaling by the fixed training reference gives a dimensionless ratio; q_lsd_f is positive throughout the training domain, so the ratio is finite for all rows.",
    "falsification_criteria": "If training Spearman association between q_Vol/q_lsd_f and entropy loss/R is near zero or opposite sign to the predeclared increasing direction, or if the association is fully explained by q_Vol alone, the hypothesis is falsified as a distinct mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
      "proxy_assumptions": "Df from a hard-sphere probe approximates the narrowest passage; molecular volume is a size proxy, not the kinetic diameter; transferability across zeolite topologies is limited by fixed-probe definitions.",
      "physical_interpretation": "q_Vol/q_lsd_f expresses adsorbate size relative to bottleneck passage on dimensionless training-reference scales; no physical unity threshold is implied.",
      "boundary_behavior": "q_lsd_f ranges over [0.857/5.163, 7.687/5.163] and is strictly positive in training, so the ratio is finite everywhere; no zero-division arises in the native regime.",
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
      "training_spearman": 0.6317416420940126,
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
    "name": "bottleneck_translation_restriction",
    "formula": "q_Vol / q_lsd_f",
    "hypothesis": "At infinite dilution, entropy loss rises when the adsorbate's van der Waals volume is large relative to the framework's bottleneck free-sphere diameter, because tighter confinement restricts translational configurational freedom.",
    "rationale": "The descriptor couples a fixed-probe bottleneck proxy (Zeo++ Df) with adsorbate size; it does not encode global cavity diameter Di or molecule-specific free volume. Scaling by the fixed training reference gives a dimensionless ratio; q_lsd_f is positive throughout the training domain, so the ratio is finite for all rows.",
    "falsification_criteria": "If training Spearman association between q_Vol/q_lsd_f and entropy loss/R is near zero or opposite sign to the predeclared increasing direction, or if the association is fully explained by q_Vol alone, the hypothesis is falsified as a distinct mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
      "proxy_assumptions": "Df from a hard-sphere probe approximates the narrowest passage; molecular volume is a size proxy, not the kinetic diameter; transferability across zeolite topologies is limited by fixed-probe definitions.",
      "physical_interpretation": "q_Vol/q_lsd_f expresses adsorbate size relative to bottleneck passage on dimensionless training-reference scales; no physical unity threshold is implied.",
      "boundary_behavior": "q_lsd_f ranges over [0.857/5.163, 7.687/5.163] and is strictly positive in training, so the ratio is finite everywhere; no zero-division arises in the native regime.",
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
      "training_spearman": 0.6317416420940126,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/rag_agent/replicate-2/round-3/h2`

最终状态：scored；边际收益：-4.239251 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "included_path_rotational_confinement",
    "formula": "rotor_case(q_LabuteASA / q_lsd_p, q_LabuteASA / q_lsd_p, q_LabuteASA / q_lsd_p)",
    "hypothesis": "Entropy loss increases when adsorbate molecular surface area is large relative to the largest included sphere along the free-sphere path, because large surface contact within channel-like confinement suppresses rotational configurational freedom for multi-atom adsorbates.",
    "rationale": "Uses lsd_p (Dif), explicitly not the bottleneck Df and not global cavity Di, contrasted with the molecular surface area proxy. The single rotor_case branch is applied uniformly because this hypothesis does not claim rotor-class-specific behavior; predeclaring a constant branch avoids spurious class splits. Dif is positive across the full training domain, guaranteeing finite values.",
    "falsification_criteria": "If the training association is negative or negligible, or if adding an explicit rotor-case split changes the sign of the association, the uniform-confinement hypothesis is falsified; a competing mechanism would be rotor-class-specific freezing by inertia proxies.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Labute surface area proxies molecular extent for surface-contact pinning; Dif along the free-sphere path proxies channel confinement; heavy-atom representation for PMI/geometry does not mean all-atom inertia is zero; correlations cannot establish causality.",
      "physical_interpretation": "Ratio of molecular surface area to included-sphere confinement on training-reference-normalized scales; no unity threshold has physical meaning.",
      "boundary_behavior": "lsd_p ranges over [3.345, 15.560] and is strictly positive; LabuteASA is strictly positive; the ratio is finite for all 2361 training rows, including single-site species where the small molecular proxy keeps the ratio small.",
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
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "LabuteASA",
        "lsd_p"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.6558417394590412,
      "target_association": "consistent",
      "perturbation": 0.0452717,
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
    "name": "included_path_rotational_confinement",
    "formula": "q_LabuteASA / q_lsd_p",
    "hypothesis": "Entropy loss increases when adsorbate molecular surface area is large relative to the largest included sphere along the free-sphere path, because large surface contact within channel-like confinement suppresses rotational configurational freedom for multi-atom adsorbates.",
    "rationale": "The uniform rotor_case wrapper with three identical branches is redundant (identical expressions in all branches collapse to the base expression), so the formula is simplified to the single ratio. The hypothesis does not claim rotor-class-specific behavior, and methane (single-site) is included with a small molecular proxy, keeping the ratio small. Smaller-pore confinement showing greater rotational entropy loss (E01, E02) motivates the increasing direction, but lsd_p is a proxy for, not a measure of, cavity diameter.",
    "falsification_criteria": "If the training association between q_LabuteASA/q_lsd_p and entropy loss/R is negative or negligible, or if the association is fully explained by q_LabuteASA alone, the confinement-contrast mechanism is falsified as distinct; a competing mechanism would be rotor-class-specific rotational freezing via inertia proxies.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "LabuteASA proxies molecular contact extent; lsd_p (Dif, largest included sphere along the free-sphere path) proxies confinement extent along the diffusion path. Dif is neither the bottleneck Df nor the global cavity diameter Di cited in E02; the mapping from cavity diameter to Dif is a proxy transfer with unquantified error. The heavy-atom/implicit-H representation of adsorbate geometry is legitimate and does not imply zero all-atom inertia. Correlation with entropy loss does not establish causality.",
      "physical_interpretation": "Adsorbate surface-contact extent relative to included-sphere confinement along the free path, both on fixed training-reference scales; no physical unity threshold is implied by the dimensionless ratio.",
      "boundary_behavior": "lsd_p is strictly positive over [3.3452, 15.5604] and LabuteASA is strictly positive, so the ratio is finite on all 2361 training rows; the ratio decreases as lsd_p grows toward 15.56/ref and increases as surface area grows, with no division-by-zero anywhere in the native regime.",
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
        "LabuteASA",
        "lsd_p"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.6558417394590412,
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
    "slot_id": "h2",
    "name": "included_path_rotational_confinement",
    "formula": "q_LabuteASA / q_lsd_p",
    "hypothesis": "Entropy loss increases when adsorbate molecular surface area is large relative to the largest included sphere along the free-sphere path, because large surface contact within channel-like confinement suppresses rotational configurational freedom for multi-atom adsorbates.",
    "rationale": "The uniform rotor_case wrapper with three identical branches is redundant (identical expressions in all branches collapse to the base expression), so the formula is simplified to the single ratio. The hypothesis does not claim rotor-class-specific behavior, and methane (single-site) is included with a small molecular proxy, keeping the ratio small. Smaller-pore confinement showing greater rotational entropy loss (E01, E02) motivates the increasing direction, but lsd_p is a proxy for, not a measure of, cavity diameter.",
    "falsification_criteria": "If the training association between q_LabuteASA/q_lsd_p and entropy loss/R is negative or negligible, or if the association is fully explained by q_LabuteASA alone, the confinement-contrast mechanism is falsified as distinct; a competing mechanism would be rotor-class-specific rotational freezing via inertia proxies.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "LabuteASA proxies molecular contact extent; lsd_p (Dif, largest included sphere along the free-sphere path) proxies confinement extent along the diffusion path. Dif is neither the bottleneck Df nor the global cavity diameter Di cited in E02; the mapping from cavity diameter to Dif is a proxy transfer with unquantified error. The heavy-atom/implicit-H representation of adsorbate geometry is legitimate and does not imply zero all-atom inertia. Correlation with entropy loss does not establish causality.",
      "physical_interpretation": "Adsorbate surface-contact extent relative to included-sphere confinement along the free path, both on fixed training-reference scales; no physical unity threshold is implied by the dimensionless ratio.",
      "boundary_behavior": "lsd_p is strictly positive over [3.3452, 15.5604] and LabuteASA is strictly positive, so the ratio is finite on all 2361 training rows; the ratio decreases as lsd_p grows toward 15.56/ref and increases as surface area grows, with no division-by-zero anywhere in the native regime.",
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
        "LabuteASA",
        "lsd_p"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.6558417394590412,
      "target_association": "consistent",
      "perturbation": 0.0452717,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/rag_agent/replicate-2/round-3/h3`

最终状态：scored；边际收益：-4.779796 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "shape_locking_per_pore_surface",
    "formula": "q_PBF * q_GeDi / (q_ASA + 0.5)",
    "hypothesis": "Entropy loss increases when planar or extended adsorbates (large PBF, GeDi) sit in frameworks with low probe-accessible specific surface area, because extended shapes pinned inside low-area pore systems have the fewest orientational configurations available.",
    "rationale": "Refines the retained round-1 descriptor by replacing the maximum() floor with an additive smoothing constant (0.5 on the q_ASA scale) so the denominator is strictly positive even at ASA = 0 (28 training rows with zero accessibility); the additive constant is an empirical smoothing choice, not a physical law. PBF zeros are legitimate planarity values, so numerator zero is finite and physically meaningful (planar molecules).",
    "falsification_criteria": "If training association flips sign relative to the predeclared increasing direction, or if performance is not distinguishable from the previously retained max(q_ASA,0.01) form, the smoothed reformulation is falsified as an improvement and the shape-locking mechanism must be tested against an alternative coupling via pore volume rather than surface area.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "GeDi": "heavy_atom_pair_distance",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF and GeDi are heavy-atom (implicit-H) shape proxies; for single-molecule single-site species they can legitimately be zero and are not all-atom geometry; ASA is a fixed-probe accessibility whose zero does not imply zero molecular adsorption space.",
      "physical_interpretation": "Shape-extent proxies per unit probe-accessible specific surface area on dimensionless reference scales; the 0.5 additive constant only prevents division by zero in the fixed-probe zero-accessibility regime.",
      "boundary_behavior": "Numerator is finite (zero when PBF = 0 for planar adsorbates); denominator is bounded below by 0.5 since q_ASA >= 0, so the descriptor is finite on all 2361 training rows including the 28 zero-ASA rows and 587 zero-PBF rows.",
      "vary_input": "PBF",
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
        "GeDi",
        "PBF"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "GeDi": "heavy_atom_pair_distance",
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.36991536563981636,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
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
    "name": "shape_locking_per_pore_surface",
    "formula": "q_PBF * q_GeDi / (q_ASA + 0.5)",
    "hypothesis": "Entropy loss increases when planar or extended adsorbates (large PBF, GeDi) sit in frameworks with low probe-accessible specific surface area, because extended shapes pinned inside low-area pore systems have the fewest orientational configurations available.",
    "rationale": "Refines the retained round-1 descriptor by replacing the maximum() floor with an additive smoothing constant (0.5 on the q_ASA scale) so the denominator is strictly positive even at ASA = 0 (28 training rows with zero accessibility); the additive constant is an empirical smoothing choice, not a physical law. PBF zeros are legitimate planarity values, so numerator zero is finite and physically meaningful (planar molecules).",
    "falsification_criteria": "If training association flips sign relative to the predeclared increasing direction, or if performance is not distinguishable from the previously retained max(q_ASA,0.01) form, the smoothed reformulation is falsified as an improvement and the shape-locking mechanism must be tested against an alternative coupling via pore volume rather than surface area.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "GeDi": "heavy_atom_pair_distance",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF and GeDi are heavy-atom (implicit-H) shape proxies; for single-molecule single-site species they can legitimately be zero and are not all-atom geometry; ASA is a fixed-probe accessibility whose zero does not imply zero molecular adsorption space.",
      "physical_interpretation": "Shape-extent proxies per unit probe-accessible specific surface area on dimensionless reference scales; the 0.5 additive constant only prevents division by zero in the fixed-probe zero-accessibility regime.",
      "boundary_behavior": "Numerator is finite (zero when PBF = 0 for planar adsorbates); denominator is bounded below by 0.5 since q_ASA >= 0, so the descriptor is finite on all 2361 training rows including the 28 zero-ASA rows and 587 zero-PBF rows.",
      "vary_input": "PBF",
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
        "GeDi",
        "PBF"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "GeDi": "heavy_atom_pair_distance",
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.36991536563981636,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
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
    "name": "shape_locking_per_pore_surface",
    "formula": "q_PBF * q_GeDi / (q_ASA + 0.5)",
    "hypothesis": "Entropy loss increases when planar or extended adsorbates (large PBF, GeDi) sit in frameworks with low probe-accessible specific surface area, because extended shapes pinned inside low-area pore systems have the fewest orientational configurations available.",
    "rationale": "Refines the retained round-1 descriptor by replacing the maximum() floor with an additive smoothing constant (0.5 on the q_ASA scale) so the denominator is strictly positive even at ASA = 0 (28 training rows with zero accessibility); the additive constant is an empirical smoothing choice, not a physical law. PBF zeros are legitimate planarity values, so numerator zero is finite and physically meaningful (planar molecules).",
    "falsification_criteria": "If training association flips sign relative to the predeclared increasing direction, or if performance is not distinguishable from the previously retained max(q_ASA,0.01) form, the smoothed reformulation is falsified as an improvement and the shape-locking mechanism must be tested against an alternative coupling via pore volume rather than surface area.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "GeDi": "heavy_atom_pair_distance",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF and GeDi are heavy-atom (implicit-H) shape proxies; for single-molecule single-site species they can legitimately be zero and are not all-atom geometry; ASA is a fixed-probe accessibility whose zero does not imply zero molecular adsorption space.",
      "physical_interpretation": "Shape-extent proxies per unit probe-accessible specific surface area on dimensionless reference scales; the 0.5 additive constant only prevents division by zero in the fixed-probe zero-accessibility regime.",
      "boundary_behavior": "Numerator is finite (zero when PBF = 0 for planar adsorbates); denominator is bounded below by 0.5 since q_ASA >= 0, so the descriptor is finite on all 2361 training rows including the 28 zero-ASA rows and 587 zero-PBF rows.",
      "vary_input": "PBF",
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
        "GeDi",
        "PBF"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "GeDi": "heavy_atom_pair_distance",
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.36991536563981636,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
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
        "record_id": "chunk:166106b9d0f41731d2d72c4f",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:aec11c5a588f125ea377fc95",
        "paper_id": "doi:10.1021/acs.est.9b04154",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:43dedbc998f9c278eea622b0",
        "paper_id": "pmc:pmc9739862",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cc904c61f240366bfe7825e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ecf3b350af8d5c09a9a10048",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ed8e9522e2126c70abdc9760",
        "paper_id": "pmc:pmc7898603",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3f5768387a8e2dd4104cc2f6",
        "paper_id": "doi:10.1039/c3cc40731d",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a716c0f2d08195e0bc57308d",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c3607df07f87ae637dfc8075",
        "paper_id": "doi:10.1021/la104245c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ec1e8193a4e127c7e5a5ba8d",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:00992287f63e5424d7a6b927",
        "paper_id": "doi:10.26434/chemrxiv.7538720.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08aecb87be6d1cda8c6566fa",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:18de89f2a91a2afad96e693e",
        "paper_id": "doi:10.1007/s00894-024-06004-0",
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
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution, entropy loss rises when the adsorbate's van der Waals volume is large relative to the framework's bottleneck free-sphere diameter, because tighter confinement restricts translational configurational freedom. q_Vol / q_lsd_f Entropy loss increases when adsorbate molecular surface area is large relative to the largest included sphere along the free-sphere path, because large surface contact within channel-like confinement suppresses rotational configurational freedom for multi-atom adsorbates. rotor_case(q_LabuteASA / q_lsd_p, q_LabuteASA / q_lsd_p, q_LabuteASA / q_lsd_p) Entropy loss increases when planar or extended adsorbates (large PBF, GeDi) sit in frameworks with low probe-accessible specific surface area, because extended shapes pinned inside low-area pore systems have the fewest orientational configurations available. q_PBF * q_GeDi / (q_ASA + 0.5)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:8ffcc4698d37d4f5569d53f5",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:e98dff054a73e56b28f6bdf3"
    ],
    "items": 10,
    "lexical_tokens": 4801,
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
