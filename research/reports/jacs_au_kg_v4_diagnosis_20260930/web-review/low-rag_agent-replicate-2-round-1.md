# low/rag_agent/replicate-2/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/rag_agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`low/rag_agent/replicate-2/round-1/h1`

最终状态：scored；边际收益：+0.495242 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confined_translation",
    "formula": "log(q_lsd_f * q_Vol / q_MW)",
    "hypothesis": "At infinite dilution, entropy loss increases as the adsorbate translational freedom is confined by narrow framework bottlenecks relative to the molecule's size per unit mass, so the entropy-loss proxy decreases with the bottleneck-per-mass dimensionless group lsd_f * AV / MW.",
    "rationale": "Translational confinement in channels narrower than molecular scale reduces translational entropy; the bottleneck free-sphere Df (lsd_f) and mass-specific accessible volume (AV) jointly proxy channel confinement, while MW proxies molecular translational mass/entropy scale in the gas. This is a new_combination of existing physical intuitions (Fst/Sunar-style free-sphere heuristics) re-expressed from native inputs; it is a proxy association only, not a causal equality.",
    "falsification_criteria": "If MAE does not improve relative to a null descriptor, or if the association sign flips within lsd_f training quartiles, the bottleneck-confinement mechanism is rejected for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "AV": "probe_accessible_specific_volume",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f proxies channel confinement but is not the global cavity Di; AV is fixed-probe specific volume, not molecule-specific free volume; MW proxies gas translational entropy scale only for monatomic-like single sites.",
      "physical_interpretation": "All quantities are native; q_* are dimensionless ratios to fixed training-reference medians with no physical unity threshold.",
      "boundary_behavior": "lsd_f and MW have strictly positive training domains, so the expression is finite for every training row; no zero division occurs.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "decreasing"
    }
  },
  "precheck": {
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "reason": "Wrong physical variable mapping: Vol requires molecular_vdw_volume"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confined_translation",
    "formula": "log(q_lsd_f * q_AV / q_MW)",
    "hypothesis": "At infinite dilution, entropy loss increases as the adsorbate translational freedom is confined by narrow framework bottlenecks relative to the molecule's size per unit mass, so the entropy-loss proxy decreases with the bottleneck-per-mass dimensionless group lsd_f * AV / MW.",
    "rationale": "Smaller passing bottlenecks (lsd_f) at fixed molecule size are empirically associated with larger entropy loss (E01–E04: smaller-pore frameworks show larger entropy-loss fractions); AV enters additively as a mass-specific accessibility proxy. Proxy association only; Df is not cavity diameter Di and no causality is claimed.",
    "falsification_criteria": "If MAE does not improve over a null descriptor, or if the lsd_f association sign flips within lsd_f training quartiles, the bottleneck-confinement mechanism is rejected for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "AV": "probe_accessible_specific_volume",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f is the passing-bottleneck free sphere (Df), not global cavity Di and not lsd_p; AV is fixed-probe mass-specific accessibility, not molecule-specific free volume; MW proxies the gas-phase translational entropy scale only for single-site species. Evidence E01–E04 concerns cavity-size confinement; lsd_f is only a proxy for that geometry.",
      "physical_interpretation": "All quantities native; q_* are dimensionless ratios to fixed positive training-reference medians; no physical unity threshold is implied.",
      "boundary_behavior": "lsd_f (0.857–7.687 Å), AV (0–0.661 cm^3/g) and MW (16.0–184.1 g/mol) are all strictly positive in the training domain, so every training row yields a finite value; no zero division occurs. q_AV=0 rows give descriptor -infinity only if AV=0 were divided; instead AV appears as a numerator, so AV=0 rows give log(0) — correction: use the form log(q_lsd_f / q_MW) + q_AV, or equivalently keep q_AV in a log-safe additive form. Final executable form: log(q_lsd_f / q_MW) + q_AV, finite for all rows including AV=0.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "decreasing"
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "MW": "adsorbate_geometry_proxy",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "domain_failure": {
      "invalid_n": 28,
      "invalid_fraction": 0.011859381617958492,
      "zero_variables_on_invalid_rows": {
        "MW": 0,
        "AV": 28,
        "lsd_f": 0
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
    "slot_id": "h1",
    "name": "bottleneck_confined_translation",
    "formula": "log(q_lsd_f / q_MW) + q_AV",
    "hypothesis": "At infinite dilution, entropy loss increases as the adsorbate translational freedom is confined by narrow framework bottlenecks relative to the molecule's size per unit mass, so the entropy-loss proxy decreases with the bottleneck-per-mass dimensionless group lsd_f * AV / MW.",
    "rationale": "Smaller passing bottlenecks (lsd_f) at fixed molecule size are empirically associated with larger entropy loss (E01–E04: smaller-pore frameworks show larger entropy-loss fractions); AV enters additively as a mass-specific accessibility proxy. Proxy association only; Df is not cavity diameter Di and no causality is claimed.",
    "falsification_criteria": "If MAE does not improve over a null descriptor, or if the lsd_f association sign flips within lsd_f training quartiles, the bottleneck-confinement mechanism is rejected for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "AV": "probe_accessible_specific_volume",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f is the passing-bottleneck free sphere (Df), not global cavity Di and not lsd_p; AV is fixed-probe mass-specific accessibility, not molecule-specific free volume; MW proxies the gas-phase translational entropy scale only for single-site species. Evidence E01–E04 concerns cavity-size confinement; lsd_f is only a proxy for that geometry.",
      "physical_interpretation": "All quantities native; q_* are dimensionless ratios to fixed positive training-reference medians; no physical unity threshold is implied.",
      "boundary_behavior": "lsd_f (0.857–7.687 Å) and MW (16.0–184.1 g/mol) are strictly positive in training, so log(q_lsd_f / q_MW) is finite on every row; no division by zero occurs. AV (0–0.661 cm^3/g) enters as an additive term, so the 28 AV=0 rows (legitimate fixed-probe zero-accessibility, not imputed) simply contribute 0 and remain finite. The AV-in-log original form was replaced because AV=0 made log(q_AV) undefined; the additive form preserves the same bottleneck-per-mass confinement mechanism with an empirical linear accessibility offset, declared as proxy association with no causality or unity-threshold claim.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "MW": "adsorbate_geometry_proxy",
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
      "training_spearman": -0.714369627287821,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/rag_agent/replicate-2/round-1/h2`

最终状态：scored；边际收益：-6.772808 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotational_freezing_by_inertia",
    "formula": "rotor_case(log(q_MW), log(q_MW) - 0.2 * q_PMI2 / q_PMI3, log(q_MW) - 0.2 * q_PMI2 / q_PMI3)",
    "hypothesis": "Rotational entropy loss on adsorption grows with molecular inertia asymmetry: for nonlinear (and separately linear) rotors, adsorbed-phase rotational restriction increases as the intermediate-to-largest principal moment ratio PMI2/PMI3 rises, partially offsetting the mass-driven rotational entropy scale; single-site species (methane-like) have no rotational loss branch.",
    "rationale": "Classical rotor entropy depends on moments of inertia; a molecule whose moments are comparable but large experiences greater rotational confinement in cages. PMI2/PMI3 is a heavy-atom proxy, not true all-atom inertia; the 0.2 coefficient is an empirical smoothing constant with no universal meaning. Nonlinear rotors dominate training (2093 of 2361), so the single-site branch (methane and similar, 54 rows) is declared as an identity-mass reference.",
    "falsification_criteria": "If residual entropy-loss association does not correlate positively with PMI2/PMI3 within nonlinear rotors at fixed MW, or if the linear branch (214 rows) shows the opposite sign, the rotational-freezing hypothesis is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI2/PMI3 proxies rotational anisotropy of the full molecule; implicit-H representation means true all-atom inertia is not zero even where proxies are zero; rotor_case categories are fixed proxy classifications, not spectroscopic rotor classes.",
      "physical_interpretation": "PMI ratio is dimensionless via q-normalization; no physical threshold at q=1.",
      "boundary_behavior": "Legitimate zero PMI values (linear/single-site rows) occur only in branches where PMI2/PMI3 is not evaluated: the single-site branch uses only q_MW; linear molecules have PMI1=0 with PMI2=PMI3>0 in principle, but rows with PMI2=0 (near-zero proxies) could divide by zero in the linear branch, so the linear branch is restricted to the PMI-ratio term only when finite — implementation must guard: use minimum(abs ratio, constant cap) or verify no zero-PMI2 rows fall in the linear branch; declaration here: linear branch uses log(q_MW) alone if any linear row has PMI2 near zero.",
      "vary_input": "PMI2",
      "descriptor_direction": "decreasing",
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
        "MW",
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.37581194417197566,
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
    "name": "rotational_freezing_by_inertia",
    "formula": "rotor_case(log(q_MW), log(q_MW), log(q_MW) - 0.2 * q_PMI2 / q_PMI3)",
    "hypothesis": "Rotational entropy loss on adsorption grows with molecular inertia asymmetry: for nonlinear (and separately linear) rotors, adsorbed-phase rotational restriction increases as the intermediate-to-largest principal moment ratio PMI2/PMI3 rises, partially offsetting the mass-driven rotational entropy scale; single-site species (methane-like) have no rotational loss branch.",
    "rationale": "Rotational entropy loss grows with molecular inertia and confinement (E01–E06); for nonlinear rotors a rising PMI2/PMI3 anisotropy ratio is predeclared as reducing the descriptor (increasing entropy loss). Training-only check found a consistent positive association (Spearman 0.376) with rotor class fixed during the partial derivative; this is association, not validated causality.",
    "falsification_criteria": "If residual entropy-loss association does not correlate positively with PMI2/PMI3 within nonlinear rotors at fixed MW, the rotational-freezing hypothesis is falsified; the linear branch (214 rows) is not independently tested since it carries no PMI term.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E02",
      "E05",
      "E06"
    ],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI values are heavy-atom implicit-H proxies; true all-atom inertia is not zero where proxies are zero. rotor_case categories are fixed proxy classifications, not spectroscopic rotor classes. The 0.2 coefficient is an empirical smoothing constant with no universal meaning.",
      "physical_interpretation": "q_PMI2/q_PMI3 is dimensionless; no physical threshold at 1. The linear branch is set equal to the single-site branch because heavy-atom PMI2/PMI3 for linear proxies is not a reliable anisotropy measure at zero PMI1.",
      "boundary_behavior": "Single-site and linear branches use only log(q_MW) (MW strictly positive, finite everywhere), so legitimate zero PMI values on those branches are never divided by. The nonlinear branch is applied only to rows classified nonlinear (2093 of 2361); zero or near-zero PMI2/PMI3 values belong to the linear/single-site categories (54 single-site, 214 linear account for PMI1=0 rows; PMI2=PMI3=0 rows are single-site), so the ratio q_PMI2/q_PMI3 is evaluated only on the nonlinear branch where PMI3>0 in the training support. If any nonlinear row had PMI3 near zero the formula would be non-finite and the slot would fail the domain check.",
      "vary_input": "PMI2",
      "descriptor_direction": "decreasing",
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
        "MW",
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.37392050622714723,
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
    "name": "rotational_freezing_by_inertia",
    "formula": "rotor_case(log(q_MW), log(q_MW), log(q_MW) - 0.2 * q_PMI2 / q_PMI3)",
    "hypothesis": "Rotational entropy loss on adsorption grows with molecular inertia asymmetry: for nonlinear (and separately linear) rotors, adsorbed-phase rotational restriction increases as the intermediate-to-largest principal moment ratio PMI2/PMI3 rises, partially offsetting the mass-driven rotational entropy scale; single-site species (methane-like) have no rotational loss branch.",
    "rationale": "Rotational entropy loss grows with molecular inertia and confinement (E01–E06); for nonlinear rotors a rising PMI2/PMI3 anisotropy ratio is predeclared as reducing the descriptor (increasing entropy loss). Training-only check found a consistent positive association (Spearman 0.376) with rotor class fixed during the partial derivative; this is association, not validated causality.",
    "falsification_criteria": "If residual entropy-loss association does not correlate positively with PMI2/PMI3 within nonlinear rotors at fixed MW, the rotational-freezing hypothesis is falsified; the linear branch (214 rows) is not independently tested since it carries no PMI term.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E02",
      "E05",
      "E06"
    ],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI values are heavy-atom implicit-H proxies; true all-atom inertia is not zero where proxies are zero. rotor_case categories are fixed proxy classifications, not spectroscopic rotor classes. The 0.2 coefficient is an empirical smoothing constant with no universal meaning.",
      "physical_interpretation": "q_PMI2/q_PMI3 is dimensionless; no physical threshold at 1. The linear branch is set equal to the single-site branch because heavy-atom PMI2/PMI3 for linear proxies is not a reliable anisotropy measure at zero PMI1.",
      "boundary_behavior": "Single-site and linear branches use only log(q_MW) (MW strictly positive, finite everywhere), so legitimate zero PMI values on those branches are never divided by. The nonlinear branch is applied only to rows classified nonlinear (2093 of 2361); zero or near-zero PMI2/PMI3 values belong to the linear/single-site categories (54 single-site, 214 linear account for PMI1=0 rows; PMI2=PMI3=0 rows are single-site), so the ratio q_PMI2/q_PMI3 is evaluated only on the nonlinear branch where PMI3>0 in the training support. If any nonlinear row had PMI3 near zero the formula would be non-finite and the slot would fail the domain check.",
      "vary_input": "PMI2",
      "descriptor_direction": "decreasing",
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
        "MW",
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.37392050622714723,
      "target_association": "consistent",
      "perturbation": 3.956905037,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/rag_agent/replicate-2/round-1/h3`

最终状态：scored；边际收益：+4.884429 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "planarity_shape_locking",
    "formula": "q_PBF * sqrt(q_SPAN * q_GeDi) / q_ASA",
    "hypothesis": "Entropy loss rises when adsorbates are planar or elongated (large PBF, SPAN, GeDi) relative to the framework's accessible specific surface area, because flat/extended shapes lose more orientational/configurational entropy when pinned against framework surfaces.",
    "rationale": "Shape-matching arguments suggest molecules that can lie flat on channel walls lose orientational entropy; ASA per mass normalizes for the amount of accessible wall available. This is an empirical proxy combination of shape (PBF, SPAN, GeDi from heavy-atom representation) and connectivity (ASA); it is a predeclared association test, not established causality.",
    "falsification_criteria": "If MAE worsens versus a mass-only baseline, or if the PBF association is not monotonic within ASA quartiles, the shape-locking mechanism is rejected; a competing mechanism is that PBF merely correlates with Vol.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
      "proxy_assumptions": "PBF/SPAN/GeDi are heavy-atom proxies with legitimate zeros (587 rows with PBF=0, 54 with SPAN/GeDi=0); ASA is a fixed-probe specific area, and ASA=0 rows (28) do not imply zero adsorption space, only zero fixed-probe accessibility.",
      "physical_interpretation": "q_PBF=0 rows make the whole expression 0, encoding 'no planarity locking', a declared convention, not a physical law; division by q_ASA is finite only when ASA>0.",
      "boundary_behavior": "ASA=0 in 28 training rows would make the expression infinite; to keep every row finite the executable form must branch: use the guard maximum(q_ASA, c) with a small fixed positive constant c, honestly declared as an empirical smoothing device with no physical meaning; alternatively the formula is declared invalid for ASA=0 rows. Zero PBF/SPAN/GeDi give descriptor value 0, treated as the unlocked-shape limit.",
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
    "status": "rejected",
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
        "PBF",
        "SPAN"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "GeDi": "heavy_atom_pair_distance",
        "PBF": "heavy_atom_planarity",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "domain_failure": {
      "invalid_n": 28,
      "invalid_fraction": 0.011859381617958492,
      "zero_variables_on_invalid_rows": {
        "PBF": 23,
        "SPAN": 3,
        "GeDi": 3,
        "ASA": 28
      },
      "nonfinite_rule": "Every training row must have a finite feature; physical zeros are not imputed."
    },
    "reason": "Formula undefined on observed training support; use a justified finite proxy or explicit rotor branches"
  }
}
```

### 复核稿

```json
{
  "candidate": {
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
        "PBF",
        "SPAN"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "GeDi": "heavy_atom_pair_distance",
        "PBF": "heavy_atom_planarity",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.38101054090277503,
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
        "PBF",
        "SPAN"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "GeDi": "heavy_atom_pair_distance",
        "PBF": "heavy_atom_planarity",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.38101054090277503,
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
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49d0db36d52cb97f9acfc9bb",
        "paper_id": "pmc:pmc11701358",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:8c01dc8f239cddb9baf4250d",
        "paper_id": "doi:10.1021/acs.jctc.0c01022",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:00992287f63e5424d7a6b927",
        "paper_id": "doi:10.26434/chemrxiv.7538720.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3dd1e3b89a0f8f43f056aaa3",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:43dedbc998f9c278eea622b0",
        "paper_id": "pmc:pmc9739862",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:72dfcce988c17185f87c465c",
        "paper_id": "doi:10.1021/jp1096663",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9aab4de7b4ab953c17269154",
        "paper_id": "doi:10.1021/jp0534380",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:af5184fc2573625a8c063e9f",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b373d933897a49c30da36477",
        "paper_id": "doi:10.1021/acs.langmuir.2c01491",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08aecb87be6d1cda8c6566fa",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:11be810dd4f785538d11302c",
        "paper_id": "doi:10.1063/5.0123434",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:16aa7d98e225b8fa29f2d598",
        "paper_id": "doi:10.1063/5.0123434",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution, entropy loss increases as the adsorbate translational freedom is confined by narrow framework bottlenecks relative to the molecule's size per unit mass, so the entropy-loss proxy decreases with the bottleneck-per-mass dimensionless group lsd_f * AV / MW. log(q_lsd_f * q_Vol / q_MW) Rotational entropy loss on adsorption grows with molecular inertia asymmetry: for nonlinear (and separately linear) rotors, adsorbed-phase rotational restriction increases as the intermediate-to-largest principal moment ratio PMI2/PMI3 rises, partially offsetting the mass-driven rotational entropy scale; single-site species (methane-like) have no rotational loss branch. rotor_case(log(q_MW), log(q_MW) - 0.2 * q_PMI2 / q_PMI3, log(q_MW) - 0.2 * q_PMI2 / q_PMI3) Entropy loss rises when adsorbates are planar or elongated (large PBF, SPAN, GeDi) relative to the framework's accessible specific surface area, because flat/extended shapes lose more orientational/configurational entropy when pinned against framework surfaces. q_PBF * sqrt(q_SPAN * q_GeDi) / q_ASA",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:01d0cb8bf43d75bbc448e004",
      "chunk:4e0a09f3bacb310a3d0b505c"
    ],
    "items": 10,
    "lexical_tokens": 4724,
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
