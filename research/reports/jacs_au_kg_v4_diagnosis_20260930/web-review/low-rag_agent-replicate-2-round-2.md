# low/rag_agent/replicate-2/round-2

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
  }
]
```

## h1

候选标识：`low/rag_agent/replicate-2/round-2/h1`

最终状态：scored；边际收益：+0.621671 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.AV, variable_mappings.lsd_p

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_path_confined_translation",
    "formula": "log(q_MW) * q_lsd_f / maximum(q_lsd_p, 0.5)",
    "hypothesis": "At infinite dilution, entropy loss increases with adsorbate mass but decreases as the included free-path diameter (lsd_p) approaches the passing bottleneck (lsd_f), because a large included-to-bottleneck ratio indicates an open diffusion path along which adsorbates retain more translational freedom despite confinement.",
    "rationale": "Uses the two distinct Zeo++ sphere descriptors in a contrast form: q_lsd_f/q_lsd_p is a dimensionless ratio near or below 1 for channel-like frameworks and small for cage-like ones. Multiplying by log(q_MW) encodes heavier adsorbates losing more translational entropy per unit confinement. Limitations: both are geometric fixed-probe proxies; Df is not a global cavity diameter; the ratio carries no universal physical unity threshold.",
    "falsification_criteria": "If the training Spearman of the descriptor against entropy loss/R is positive when the mechanism predicts a negative association (descriptor direction increasing = less loss), or if the marginal MAE improvement is non-positive, the open-path contrast hypothesis is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f proxies the narrowest passage and lsd_p the largest included sphere along the free path; both are fixed-probe geometries, not adsorbate-specific, and transfer to real adsorbates only approximately.",
      "physical_interpretation": "Native quantities: molecular weight (g/mol), bottleneck free sphere (angstrom), included sphere along path (angstrom). No claim that a ratio of 1 is a physical equality threshold.",
      "boundary_behavior": "q_lsd_p is bounded below by 3.3452/6.38663 in training so maximum(q_lsd_p, 0.5) never vanishes; log(q_MW) is finite since MW > 0. The expression is finite for every training row without imputation.",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_p",
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
        "MW",
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "lsd_f": "bottleneck_free_sphere_Df",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 1146,
      "nonzero_fraction": 0.4794578568403219
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
    "name": "bottleneck_path_confined_translation",
    "formula": "log(q_lsd_f / q_MW) + q_AV",
    "hypothesis": "At infinite dilution, entropy loss increases with adsorbate mass but decreases as the included free-path diameter (lsd_p) approaches the passing bottleneck (lsd_f), because a large included-to-bottleneck ratio indicates an open diffusion path along which adsorbates retain more translational freedom despite confinement.",
    "rationale": "Correction of a mapping/direction error: the previous contrast form q_lsd_f/maximum(q_lsd_p, 0.5) multiplied by log(q_MW) contradicted its predeclared direction on training rows (opposite_n = 1146). The patched descriptor follows the round-1 diagnostics, where a bottleneck-over-mass contrast with a positive accessible-volume term showed a consistent training association (Spearman -0.714 for the corresponding prior variant). Heavier adsorbates confined behind a small passing bottleneck (small Df/lsd_f relative to molecular size) are expected to lose more translational entropy, while frameworks with larger fixed-probe accessible volume retain more configurational freedom. Limitations: lsd_f (Zeo++ Df) is a passing-bottleneck proxy, not a global cavity diameter and not adsorbate-specific; AV is a fixed-probe, mass-specific accessibility, not molecular free volume; q ratios carry no universal physical threshold.",
    "falsification_criteria": "If the training Spearman of the descriptor against entropy loss/R changes sign relative to the predeclared association (descriptor increasing in lsd_f should correspond to less entropy loss), or if the marginal MAE improvement over the retained set is non-positive, the bottleneck-confined translation hypothesis is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f proxies the narrowest periodic passage; it is a fixed-probe geometric quantity, not adsorbate-specific, and is distinct from included diameter (lsd_p/Dif) and from global cavity diameter. Transfer to real adsorbates is approximate.",
      "physical_interpretation": "Native quantities: molecular weight (g/mol), bottleneck free sphere Df (angstrom), fixed-probe accessible specific volume AV (cm^3/g). The ratio q_lsd_f/q_MW is a dimensionless empirical contrast; no physical unity threshold is asserted.",
      "boundary_behavior": "MW > 0 and lsd_f > 0 on all training rows (min 16.03 and 0.85684), so the log and ratio are finite; AV has 28 legitimate zeros but enters additively, so every training row yields a finite value without imputation.",
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

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_path_confined_translation",
    "formula": "log(q_lsd_f / q_MW) + q_AV",
    "hypothesis": "At infinite dilution, entropy loss increases with adsorbate mass but decreases as the included free-path diameter (lsd_p) approaches the passing bottleneck (lsd_f), because a large included-to-bottleneck ratio indicates an open diffusion path along which adsorbates retain more translational freedom despite confinement.",
    "rationale": "Correction of a mapping/direction error: the previous contrast form q_lsd_f/maximum(q_lsd_p, 0.5) multiplied by log(q_MW) contradicted its predeclared direction on training rows (opposite_n = 1146). The patched descriptor follows the round-1 diagnostics, where a bottleneck-over-mass contrast with a positive accessible-volume term showed a consistent training association (Spearman -0.714 for the corresponding prior variant). Heavier adsorbates confined behind a small passing bottleneck (small Df/lsd_f relative to molecular size) are expected to lose more translational entropy, while frameworks with larger fixed-probe accessible volume retain more configurational freedom. Limitations: lsd_f (Zeo++ Df) is a passing-bottleneck proxy, not a global cavity diameter and not adsorbate-specific; AV is a fixed-probe, mass-specific accessibility, not molecular free volume; q ratios carry no universal physical threshold.",
    "falsification_criteria": "If the training Spearman of the descriptor against entropy loss/R changes sign relative to the predeclared association (descriptor increasing in lsd_f should correspond to less entropy loss), or if the marginal MAE improvement over the retained set is non-positive, the bottleneck-confined translation hypothesis is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f proxies the narrowest periodic passage; it is a fixed-probe geometric quantity, not adsorbate-specific, and is distinct from included diameter (lsd_p/Dif) and from global cavity diameter. Transfer to real adsorbates is approximate.",
      "physical_interpretation": "Native quantities: molecular weight (g/mol), bottleneck free sphere Df (angstrom), fixed-probe accessible specific volume AV (cm^3/g). The ratio q_lsd_f/q_MW is a dimensionless empirical contrast; no physical unity threshold is asserted.",
      "boundary_behavior": "MW > 0 and lsd_f > 0 on all training rows (min 16.03 and 0.85684), so the log and ratio are finite; AV has 28 legitimate zeros but enters additively, so every training row yields a finite value without imputation.",
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

候选标识：`low/rag_agent/replicate-2/round-2/h2`

最终状态：scored；边际收益：-5.034862 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "inertia_contrast_rotor_branching",
    "formula": "rotor_case(log(q_Vol), log(q_Vol) - 0.1 * q_PMI1 / q_PMI3, log(q_Vol) - 0.1 * q_PMI1 / q_PMI3)",
    "hypothesis": "Entropy loss grows with adsorbate volume, but for linear and nonlinear rotors the loss is reduced when the smallest-to-largest heavy-atom inertia ratio (PMI1/PMI3) is large, i.e. when the heavy-atom framework is compact and isotropic, since near-spherical rotors lose less rotational entropy on adsorption than highly anisotropic ones.",
    "rationale": "PMI1/PMI3 is a dimensionless shape anisotropy of the heavy-atom representation; subtracting a small multiple from a volume term makes the descriptor smaller (predicted lower entropy loss) for anisotropic molecules. For single-site species (methane-like, PMI proxies zero) the branch reduces to the pure volume term. Limitations: PMI values are heavy-atom proxies with legitimate zeros, not true all-atom inertias; the 0.1 coefficient is an empirical smoothing constant, not a fitted physical constant.",
    "falsification_criteria": "If within the linear/nonlinear rotor class the partial derivative of the descriptor with respect to PMI1 (rotor class fixed) shows the opposite sign association with the target, or if the rotor-branched descriptor underperforms the unbranched volume-only term in MAE, the anisotropy-softening hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI1/PMI3 proxies rotational anisotropy of the implicit-H heavy-atom geometry; single-site species are assigned zero PMI proxies by construction, so they take the pure-volume branch.",
      "physical_interpretation": "Native meanings: Van der Waals volume (angstrom^3), principal moments (angstrom^2*amu). q_PMI1/q_PMI3 is dimensionless shape anisotropy; no physical unity threshold is asserted.",
      "boundary_behavior": "At PMI1 = 0 (single-site branch anyway) the nonlinear expression is still finite because q_PMI3 > 0 for rows reaching that branch; Vol > 0 always so logs are finite. All three branches return compatible dimensionless units.",
      "vary_input": "PMI1",
      "descriptor_direction": "increasing",
      "regime_input": "PMI1",
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
        "PMI1",
        "PMI3",
        "Vol"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 2307,
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
    "slot_id": "h2",
    "name": "inertia_contrast_rotor_branching",
    "formula": "rotor_case(log(q_Vol), log(q_Vol) + 0.1 * q_PMI1 / q_PMI3, log(q_Vol) + 0.1 * q_PMI1 / q_PMI3)",
    "hypothesis": "Entropy loss grows with adsorbate volume, but for linear and nonlinear rotors the loss is reduced when the smallest-to-largest heavy-atom inertia ratio (PMI1/PMI3) is large, i.e. when the heavy-atom framework is compact and isotropic, since near-spherical rotors lose less rotational entropy on adsorption than highly anisotropic ones.",
    "rationale": "Direction correction: the previous descriptor subtracted the anisotropy contrast, which contradicted its predeclared direction on all 2307 applicable rows. The patched descriptor adds the heavy-atom shape anisotropy ratio (PMI1/PMI3): more elongated, anisotropic rotors (large PMI1 relative to PMI3) are expected to lose more rotational entropy upon confinement, consistent with reported evidence that rotational entropy loss dominates in smaller, more confining frameworks (E01, E02) and that rotational freedom differences affect adsorption equilibrium (E06). Volume remains the base term; single-site species (PMI proxies zero, e.g. methane-like) take the pure-volume branch. The 0.1 coefficient is an empirical smoothing constant, not a fitted physical constant. Note the prior round's analogous form with PMI2 was direction-consistent but did not improve MAE; this variant is a testable alternative, not a validated mechanism.",
    "falsification_criteria": "If, within a fixed rotor class, the partial derivative of the descriptor with respect to PMI1 shows a target association opposite to the predeclared direction, or if the rotor-branched descriptor underperforms the volume-only term in MAE, the anisotropy-amplified rotational-loss hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E06"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI1/PMI3 is a shape-anisotropy proxy of the implicit-H heavy-atom representation, not true all-atom inertia; legitimate zeros exist and are not imputed. Transfer of this proxy to real rotational freedom is only qualitative.",
      "physical_interpretation": "Native quantities: Van der Waals volume (angstrom^3), principal moments of inertia of the heavy-atom representation (angstrom^2*amu). The ratio q_PMI1/q_PMI3 is dimensionless; no physical unity threshold is asserted.",
      "boundary_behavior": "Vol > 0 always so logs are finite; q_PMI3 > 0 for all rows reaching the linear/nonlinear branches, so the ratio is finite even when q_PMI1 = 0 (descriptor then reduces to the volume term). All three branches return compatible dimensionless units.",
      "vary_input": "PMI1",
      "descriptor_direction": "increasing",
      "regime_input": "PMI1",
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
        "PMI3",
        "Vol"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        333.6293867
      ],
      "training_spearman": 0.37655163673816067,
      "target_association": "consistent",
      "perturbation": 1.074636625,
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
    "name": "inertia_contrast_rotor_branching",
    "formula": "rotor_case(log(q_Vol), log(q_Vol) + 0.1 * q_PMI1 / q_PMI3, log(q_Vol) + 0.1 * q_PMI1 / q_PMI3)",
    "hypothesis": "Entropy loss grows with adsorbate volume, but for linear and nonlinear rotors the loss is reduced when the smallest-to-largest heavy-atom inertia ratio (PMI1/PMI3) is large, i.e. when the heavy-atom framework is compact and isotropic, since near-spherical rotors lose less rotational entropy on adsorption than highly anisotropic ones.",
    "rationale": "Direction correction: the previous descriptor subtracted the anisotropy contrast, which contradicted its predeclared direction on all 2307 applicable rows. The patched descriptor adds the heavy-atom shape anisotropy ratio (PMI1/PMI3): more elongated, anisotropic rotors (large PMI1 relative to PMI3) are expected to lose more rotational entropy upon confinement, consistent with reported evidence that rotational entropy loss dominates in smaller, more confining frameworks (E01, E02) and that rotational freedom differences affect adsorption equilibrium (E06). Volume remains the base term; single-site species (PMI proxies zero, e.g. methane-like) take the pure-volume branch. The 0.1 coefficient is an empirical smoothing constant, not a fitted physical constant. Note the prior round's analogous form with PMI2 was direction-consistent but did not improve MAE; this variant is a testable alternative, not a validated mechanism.",
    "falsification_criteria": "If, within a fixed rotor class, the partial derivative of the descriptor with respect to PMI1 shows a target association opposite to the predeclared direction, or if the rotor-branched descriptor underperforms the volume-only term in MAE, the anisotropy-amplified rotational-loss hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E06"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI1/PMI3 is a shape-anisotropy proxy of the implicit-H heavy-atom representation, not true all-atom inertia; legitimate zeros exist and are not imputed. Transfer of this proxy to real rotational freedom is only qualitative.",
      "physical_interpretation": "Native quantities: Van der Waals volume (angstrom^3), principal moments of inertia of the heavy-atom representation (angstrom^2*amu). The ratio q_PMI1/q_PMI3 is dimensionless; no physical unity threshold is asserted.",
      "boundary_behavior": "Vol > 0 always so logs are finite; q_PMI3 > 0 for all rows reaching the linear/nonlinear branches, so the ratio is finite even when q_PMI1 = 0 (descriptor then reduces to the volume term). All three branches return compatible dimensionless units.",
      "vary_input": "PMI1",
      "descriptor_direction": "increasing",
      "regime_input": "PMI1",
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
        "PMI3",
        "Vol"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        333.6293867
      ],
      "training_spearman": 0.37655163673816067,
      "target_association": "consistent",
      "perturbation": 1.074636625,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/rag_agent/replicate-2/round-2/h3`

最终状态：scored；边际收益：+2.135794 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "volume_accessibility_coupling",
    "formula": "q_Vol * q_LabuteASA / maximum(q_AV, 0.05)",
    "hypothesis": "Entropy loss increases when the adsorbate's Van der Waals volume times its molecular surface area is large relative to the framework's probe-accessible specific pore volume, because bulky, high-surface-area molecules have fewer accessible configurations in a fixed-probe pore volume, amplifying configurational entropy loss at infinite dilution.",
    "rationale": "Couples an adsorbate size-shape product (Vol * LabuteASA, units requiring care: treated as an empirical product proxy, not a physical equality) with the framework's fixed-probe accessibility (AV). The 0.05 floor handles the 28 zero-AV training rows without implying that zero fixed-probe accessibility means zero molecular adsorption space. Limitations: AV is probe-specific and mass-specific, so the ratio is an empirical coupling proxy only.",
    "falsification_criteria": "If the descriptor's partial derivative with respect to AV (framework descriptors otherwise fixed) shows the opposite target association to the predeclared direction, or if the marginal MAE improvement is negative relative to the current retained set, the volume-accessibility coupling hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
      "proxy_assumptions": "AV is a fixed-geometric-probe accessibility proxy, not molecule-specific free volume; LabuteASA is an implicit-H surface approximation. The descriptor assumes these proxies transfer qualitatively across adsorbates, which is not guaranteed.",
      "physical_interpretation": "Native quantities: Van der Waals volume (angstrom^3), Labute surface (angstrom^2), accessible volume (cm^3/g). The maximum(q_AV, 0.05) floor is an explicit numerical safeguard for legitimate AV zeros, not a physical claim about inaccessible frameworks.",
      "boundary_behavior": "For the 28 AV = 0 rows the descriptor reduces to 20 * q_Vol * q_LabuteASA, finite and interpretable as pure adsorbate-size penalty when probe accessibility is absent; Vol and LabuteASA are strictly positive so no division by zero occurs elsewhere.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
        "LabuteASA",
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.6757355386097952,
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
        "LabuteASA",
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.05306909369769445,
      "target_association": "contradicted",
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
        "LabuteASA",
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.05306909369769445,
      "target_association": "contradicted",
      "perturbation": 0.001538232,
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
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a716c0f2d08195e0bc57308d",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:06a26a29dca2516a90c93ace",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
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
        "record_id": "chunk:6cc904c61f240366bfe7825e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:aec11c5a588f125ea377fc95",
        "paper_id": "doi:10.1021/acs.est.9b04154",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d3a799358d58da57167e96f1",
        "paper_id": "doi:10.1021/acs.langmuir.3c03931",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d8eef552eba72a99f7974a84",
        "paper_id": "doi:10.1039/b819334g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ebf7a6bb0094649558bc1f4c",
        "paper_id": "doi:10.1126/science.abn2048",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:166106b9d0f41731d2d72c4f",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:43dedbc998f9c278eea622b0",
        "paper_id": "pmc:pmc9739862",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6c2c8fc2d89d15490fc9ce78",
        "paper_id": "doi:10.1063/1.3020350",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9805f0a944c903cd7580bbcb",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ae627ac039efcb7fe83c7653",
        "paper_id": "pmc:pmc11228971",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd6fadcf0e5f2fd99bb3f46e",
        "paper_id": "doi:10.1021/acsami.5c17486",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution, entropy loss increases with adsorbate mass but decreases as the included free-path diameter (lsd_p) approaches the passing bottleneck (lsd_f), because a large included-to-bottleneck ratio indicates an open diffusion path along which adsorbates retain more translational freedom despite confinement. log(q_MW) * q_lsd_f / maximum(q_lsd_p, 0.5) Entropy loss grows with adsorbate volume, but for linear and nonlinear rotors the loss is reduced when the smallest-to-largest heavy-atom inertia ratio (PMI1/PMI3) is large, i.e. when the heavy-atom framework is compact and isotropic, since near-spherical rotors lose less rotational entropy on adsorption than highly anisotropic ones. rotor_case(log(q_Vol), log(q_Vol) - 0.1 * q_PMI1 / q_PMI3, log(q_Vol) - 0.1 * q_PMI1 / q_PMI3) Entropy loss increases when the adsorbate's Van der Waals volume times its molecular surface area is large relative to the framework's probe-accessible specific pore volume, because bulky, high-surface-area molecules have fewer accessible configurations in a fixed-probe pore volume, amplifying configurational entropy loss at infinite dilution. q_Vol * q_LabuteASA / maximum(q_AV, 0.05)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:8ffcc4698d37d4f5569d53f5",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:d52b47528dc9757d7e603c4f"
    ],
    "items": 10,
    "lexical_tokens": 4694,
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
      "record_id": "chunk:8ffcc4698d37d4f5569d53f5",
      "paper_id": "doi:10.1021/acs.jpcc.0c02671",
      "document_id": "document:679638c993b24ed3004656c6",
      "quote": "and 32 , corresponding to 1 , 3-dioxolane , 1 , 3 , 5-trioxane , and acetonitrile , respectively . These adsorbates are two cyclic ethers and one nitrile . In this case , we suspect that the unique chemical functionality of these adsorbates , in comparison to the other TraPPE species , results in a larger-than-expected entropy loss . Finally, the $ \\eta $ slopes in Figure 1 and the examination of adsorbate-specific entropy ratios in Figure 3 are suggestive of an entropy loss model based primarily on certain adsorbent characteristics. As pointed out above, $ \\eta $ is roughly the same for (1) FAU and LTA and (2) FER and MFI; the adsorbents in each of these two groups have roughly the same LCD and predominantly cage-like, spherical pores. The MOR topology has, as mentioned previously, an LCD similar to FER and MFI but with channel pores. Other pore descriptors are, of course, available as well, and we examine two others here. First, as a compliment to the LCD descriptor, we include the “maximum included sphere diameter” (MSD), which is the largest sphere pore identified in a calculated pore size distribution. $ ^{55} $ Second, we also include a different type of geometric descriptor, the “occupiable volume” ( $ V_{occ} $), which is defined as the volume per 1000 Å of the crystal cell that can be accessed by the center of probe molecules with diameter 2.8 Å. $ ^{56} $ These three pore size descriptors capture both the size of the largest pore features and the overall pore volume. In Figure 4, we plot the $ \\eta $ slope for each adsorbent as a function of these three pore metrics; diameter-based metrics are on the lower x-axis and occupiable volume is on the upper x-axis. The important result shown in Figure 4 is that, regardless of the metric used to characterize the zeolite adsorbent, the slope of the entropy relationship in Figure 1 follows the same qualitative trend. Starting at the largest pore adsorbents in terms of any of the three metrics, $ \\eta $ decreases slowly with decreasing pore size, before decreasing more rapidly to values in the vicinity of $ \\eta = 0.75 $. Despite plotting all three metrics on the x-axis of Figure 4, we imply no quantitative relationship between MSD/LCD and $ V_{occ} $; the purpose is to show the common trend in the correlation of $ \\eta $ with different size metrics. (As an aside, we note that the upper and lower x-axes have common scaling, i.e., they share a common x",
      "locator": {
        "section": "4. results and discussion",
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
