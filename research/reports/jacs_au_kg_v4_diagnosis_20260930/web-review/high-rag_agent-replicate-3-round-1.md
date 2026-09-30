# high/rag_agent/replicate-3/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`high/rag_agent/replicate-3/round-1/h1`

最终状态：scored；边际收益：-2.887550 pp；保留：False。

复核改动字段：variable_mappings.GeDi, variable_mappings.q_GeDi

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "elongation_entropy_proxy",
    "formula": "log(1 + q_GeDi)",
    "hypothesis": "At infinite dilution in rigid pure-silica frameworks, adsorbates with larger heavy-atom pair distance (more elongated molecules) lose a larger fraction of their gas-phase rotational/librational entropy upon confinement, so the entropy loss (in units of R) increases monotonically with GeDi even after molecular-weight and volume effects are accounted for elsewhere.",
    "rationale": "Elongated molecules have more low-frequency orientational degrees of freedom that become hindered inside channel/cavity geometries; GeDi is the largest interatomic distance in the original implicit-H/heavy-atom representation and acts as a shape proxy only. The log(1+q) form smooths the heavy-atom proxy across small values and keeps every row finite because q_GeDi >= 0 for all training rows, including the 54 legitimate single-site zeros where the descriptor equals log(1) = 0. This is an empirical association claim, not a validated causal mechanism.",
    "falsification_criteria": "If residual entropy loss at fixed MW and Vol shows no positive association with GeDi (or shows a negative association driven by planarity confounds), or if the association reverses within the linear-rotor subset (rotor_proxy_counts linear n=214), the proposed elongation mechanism is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "q_GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi in the implicit-H/heavy-atom representation proxies molecular elongation relevant to orientational confinement; it is not all-atom geometry and zero values for single-site species are legitimate physical limits, not missing data.",
      "physical_interpretation": "Largest heavy-atom pair distance measures molecular elongation; q_GeDi = GeDi/3.302656784 is a dimensionless row-varying input relative to the fixed training median, carrying no physical unity threshold.",
      "boundary_behavior": "At GeDi = 0 (legitimate single-site zeros), q_GeDi = 0 and the descriptor equals 0; no division by the proxy occurs, so all rows remain finite without imputation.",
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
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "reason": "Wrong physical variable mapping: GeDi requires heavy_atom_pair_distance"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "elongation_entropy_proxy",
    "formula": "log(1 + q_GeDi)",
    "hypothesis": "At infinite dilution in rigid pure-silica frameworks, adsorbates with larger heavy-atom pair distance (more elongated molecules) lose a larger fraction of their gas-phase rotational/librational entropy upon confinement, so the entropy loss (in units of R) increases monotonically with GeDi even after molecular-weight and volume effects are accounted for elsewhere.",
    "rationale": "Elongated molecules have more low-frequency orientational degrees of freedom that become hindered inside channel/cavity geometries; GeDi is the largest interatomic distance in the original implicit-H/heavy-atom representation and acts as a shape proxy only. The log(1+q) form smooths the heavy-atom proxy across small values and keeps every row finite because q_GeDi >= 0 for all training rows, including the 54 legitimate single-site zeros where the descriptor equals log(1) = 0. This is an empirical association claim, not a validated causal mechanism.",
    "falsification_criteria": "If residual entropy loss at fixed MW and Vol shows no positive association with GeDi (or shows a negative association driven by planarity confounds), or if the association reverses within the linear-rotor subset (rotor_proxy_counts linear n=214), the proposed elongation mechanism is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi in the implicit-H/heavy-atom representation proxies molecular elongation relevant to orientational confinement; it is not all-atom geometry and zero values for single-site species are legitimate physical limits, not missing data.",
      "physical_interpretation": "Largest heavy-atom pair distance measures molecular elongation; q_GeDi = GeDi/3.302656784 is a dimensionless row-varying input relative to the fixed training median, carrying no physical unity threshold.",
      "boundary_behavior": "At GeDi = 0 (legitimate single-site zeros), q_GeDi = 0 and the descriptor equals 0; no division by the proxy occurs, so all rows remain finite without imputation.",
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
        "GeDi"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.3982440794031573,
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
    "slot_id": "h1",
    "name": "elongation_entropy_proxy",
    "formula": "log(1 + q_GeDi)",
    "hypothesis": "At infinite dilution in rigid pure-silica frameworks, adsorbates with larger heavy-atom pair distance (more elongated molecules) lose a larger fraction of their gas-phase rotational/librational entropy upon confinement, so the entropy loss (in units of R) increases monotonically with GeDi even after molecular-weight and volume effects are accounted for elsewhere.",
    "rationale": "Elongated molecules have more low-frequency orientational degrees of freedom that become hindered inside channel/cavity geometries; GeDi is the largest interatomic distance in the original implicit-H/heavy-atom representation and acts as a shape proxy only. The log(1+q) form smooths the heavy-atom proxy across small values and keeps every row finite because q_GeDi >= 0 for all training rows, including the 54 legitimate single-site zeros where the descriptor equals log(1) = 0. This is an empirical association claim, not a validated causal mechanism.",
    "falsification_criteria": "If residual entropy loss at fixed MW and Vol shows no positive association with GeDi (or shows a negative association driven by planarity confounds), or if the association reverses within the linear-rotor subset (rotor_proxy_counts linear n=214), the proposed elongation mechanism is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi in the implicit-H/heavy-atom representation proxies molecular elongation relevant to orientational confinement; it is not all-atom geometry and zero values for single-site species are legitimate physical limits, not missing data.",
      "physical_interpretation": "Largest heavy-atom pair distance measures molecular elongation; q_GeDi = GeDi/3.302656784 is a dimensionless row-varying input relative to the fixed training median, carrying no physical unity threshold.",
      "boundary_behavior": "At GeDi = 0 (legitimate single-site zeros), q_GeDi = 0 and the descriptor equals 0; no division by the proxy occurs, so all rows remain finite without imputation.",
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
        "GeDi"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.3982440794031573,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/rag_agent/replicate-3/round-1/h2`

最终状态：scored；边际收益：+3.879555 pp；保留：True。

复核改动字段：variable_mappings.lsd_f, variable_mappings.q_lsd_f

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "bottleneck_confinement_inverse",
    "formula": "1 / q_lsd_f**2",
    "hypothesis": "Frameworks with smaller passing free-sphere bottlenecks (smaller lsd_f, the Zeo++ Df largest sphere through a periodic free path) impose stronger geometric confinement gradients at adsorption sites, producing larger adsorbed-phase entropy loss at infinite dilution; the entropy loss is inversely associated with the bottleneck diameter squared.",
    "rationale": "Df/lsd_f is strictly positive in training (min 0.85684), so 1/q_lsd_f**2 is finite for every row with no imputation. The exponent 2 lies within the allowed fixed-numeric range. This descriptor deliberately uses the bottleneck, not the included-along-path diameter lsd_p and not a global cavity Di, because Df is the quantity in D0 that gates access to adsorption space. The association is hypothesized, not established; a known qualitative confinement relation is re-expressed here in normalized proxy form, and the D0 inputs already present in the nonlinear ANN may re-express part of this signal.",
    "falsification_criteria": "If, holding AV and adsorbate shape fixed, entropy loss shows no inverse association with lsd_f, or if the association is dominated by lsd_p (included diameter along the free path) rather than lsd_f, the bottleneck-gradient mechanism is falsified and an alternative included-cavity mechanism should be tested instead.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "q_lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Zeo++ Df computed with a fixed probe geometry proxies the geometric confinement gradient felt by diverse adsorbates; the transfer from a hard-sphere path measure to molecule-specific entropy loss is approximate and unresolved for flexible or off-path adsorption sites.",
      "physical_interpretation": "lsd_f is the largest sphere able to pass through a periodic free path (bottleneck), not the global included cavity diameter; q_lsd_f = lsd_f/5.16326 is a dimensionless row-varying input with no physical unity threshold.",
      "boundary_behavior": "lsd_f is strictly positive on the training domain (0.85684 to 7.68726), so 1/q_lsd_f**2 is finite and well-defined everywhere; the descriptor grows steeply as the bottleneck approaches its lower domain bound, which is an extrapolation regime flagged for honest uncertainty.",
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
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "reason": "Wrong physical variable mapping: lsd_f requires bottleneck_free_sphere_Df"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "bottleneck_confinement_inverse",
    "formula": "1 / q_lsd_f**2",
    "hypothesis": "Frameworks with smaller passing free-sphere bottlenecks (smaller lsd_f, the Zeo++ Df largest sphere through a periodic free path) impose stronger geometric confinement gradients at adsorption sites, producing larger adsorbed-phase entropy loss at infinite dilution; the entropy loss is inversely associated with the bottleneck diameter squared.",
    "rationale": "Df/lsd_f is strictly positive in training (min 0.85684), so 1/q_lsd_f**2 is finite for every row with no imputation. The exponent 2 lies within the allowed fixed-numeric range. This descriptor deliberately uses the bottleneck, not the included-along-path diameter lsd_p and not a global cavity Di, because Df is the quantity in D0 that gates access to adsorption space. The association is hypothesized, not established; a known qualitative confinement relation is re-expressed here in normalized proxy form, and the D0 inputs already present in the nonlinear ANN may re-express part of this signal.",
    "falsification_criteria": "If, holding AV and adsorbate shape fixed, entropy loss shows no inverse association with lsd_f, or if the association is dominated by lsd_p (included diameter along the free path) rather than lsd_f, the bottleneck-gradient mechanism is falsified and an alternative included-cavity mechanism should be tested instead.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Zeo++ Df computed with a fixed probe geometry proxies the geometric confinement gradient felt by diverse adsorbates; the transfer from a hard-sphere path measure to molecule-specific entropy loss is approximate and unresolved for flexible or off-path adsorption sites.",
      "physical_interpretation": "lsd_f is the largest sphere able to pass through a periodic free path (bottleneck), not the global included cavity diameter; q_lsd_f = lsd_f/5.16326 is a dimensionless row-varying input with no physical unity threshold.",
      "boundary_behavior": "lsd_f is strictly positive on the training domain (0.85684 to 7.68726), so 1/q_lsd_f**2 is finite and well-defined everywhere; the descriptor grows steeply as the bottleneck approaches its lower domain bound, which is an extrapolation regime flagged for honest uncertainty.",
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
        "lsd_f"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.38676779917113346,
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
    "slot_id": "h2",
    "name": "bottleneck_confinement_inverse",
    "formula": "1 / q_lsd_f**2",
    "hypothesis": "Frameworks with smaller passing free-sphere bottlenecks (smaller lsd_f, the Zeo++ Df largest sphere through a periodic free path) impose stronger geometric confinement gradients at adsorption sites, producing larger adsorbed-phase entropy loss at infinite dilution; the entropy loss is inversely associated with the bottleneck diameter squared.",
    "rationale": "Df/lsd_f is strictly positive in training (min 0.85684), so 1/q_lsd_f**2 is finite for every row with no imputation. The exponent 2 lies within the allowed fixed-numeric range. This descriptor deliberately uses the bottleneck, not the included-along-path diameter lsd_p and not a global cavity Di, because Df is the quantity in D0 that gates access to adsorption space. The association is hypothesized, not established; a known qualitative confinement relation is re-expressed here in normalized proxy form, and the D0 inputs already present in the nonlinear ANN may re-express part of this signal.",
    "falsification_criteria": "If, holding AV and adsorbate shape fixed, entropy loss shows no inverse association with lsd_f, or if the association is dominated by lsd_p (included diameter along the free path) rather than lsd_f, the bottleneck-gradient mechanism is falsified and an alternative included-cavity mechanism should be tested instead.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Zeo++ Df computed with a fixed probe geometry proxies the geometric confinement gradient felt by diverse adsorbates; the transfer from a hard-sphere path measure to molecule-specific entropy loss is approximate and unresolved for flexible or off-path adsorption sites.",
      "physical_interpretation": "lsd_f is the largest sphere able to pass through a periodic free path (bottleneck), not the global included cavity diameter; q_lsd_f = lsd_f/5.16326 is a dimensionless row-varying input with no physical unity threshold.",
      "boundary_behavior": "lsd_f is strictly positive on the training domain (0.85684 to 7.68726), so 1/q_lsd_f**2 is finite and well-defined everywhere; the descriptor grows steeply as the bottleneck approaches its lower domain bound, which is an extrapolation regime flagged for honest uncertainty.",
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
        "lsd_f"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.38676779917113346,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/rag_agent/replicate-3/round-1/h3`

最终状态：scored；边际收益：+0.155544 pp；保留：False。

复核改动字段：variable_mappings.AV, variable_mappings.Vol, variable_mappings.q_AV, variable_mappings.q_Vol

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "molecule_accessibility_ratio",
    "formula": "q_Vol / (q_AV + 1)",
    "hypothesis": "At infinite dilution, adsorbed-phase translational entropy loss scales with the ratio of adsorbate van der Waals volume to framework probe-accessible specific volume: molecules that are large relative to the framework's accessible space lose proportionally more translational entropy, and the entropy loss increases with this ratio.",
    "rationale": "The +1 in the denominator guarantees finiteness for the 28 legitimate AV = 0 rows (fixed-probe inaccessibility does not imply zero physical adsorption space), and it is an explicit smoothing choice, not a claim of a physical unity threshold. The ratio couples an adsorbate geometry proxy (Vol) with a framework accessibility proxy (AV), forming a two-family combination not reducible to any single native input. AV is a fixed-probe, mass-specific accessibility, so the ratio is a proxy contrast rather than a molecule-specific free-volume fraction.",
    "falsification_criteria": "If entropy loss at fixed Vol is independent of AV (no contrast effect), or if the association is fully absorbed by AV alone in the nonlinear ANN's existing D0 inputs, the proposed molecule-to-accessibility coupling is falsified and a pure-framework mechanism should be preferred.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "q_Vol": "molecular_vdw_volume",
      "q_AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Van der Waals volume proxies the excluded translational footprint of the adsorbate, and fixed-probe AV proxies the available confinement space; both are geometry-only surrogates that ignore adsorbate-specific interactions and framework flexibility, limiting transferability.",
      "physical_interpretation": "q_Vol = Vol/67.24 and q_AV = AV/0.0759781 are dimensionless row-varying inputs relative to fixed training-reference medians; the constant 1 added to q_AV is an empirical smoothing constant with no physical unity meaning.",
      "boundary_behavior": "At AV = 0 (28 legitimate rows), q_AV = 0 and the descriptor reduces to q_Vol, which is finite and positive for all rows since Vol has no zeros; this treats probe-inaccessible frameworks as the limiting high-contrast case rather than imputing a value.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
    "reason": "Wrong physical variable mapping: Vol requires molecular_vdw_volume"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "molecule_accessibility_ratio",
    "formula": "q_Vol / (q_AV + 1)",
    "hypothesis": "At infinite dilution, adsorbed-phase translational entropy loss scales with the ratio of adsorbate van der Waals volume to framework probe-accessible specific volume: molecules that are large relative to the framework's accessible space lose proportionally more translational entropy, and the entropy loss increases with this ratio.",
    "rationale": "The +1 in the denominator guarantees finiteness for the 28 legitimate AV = 0 rows (fixed-probe inaccessibility does not imply zero physical adsorption space), and it is an explicit smoothing choice, not a claim of a physical unity threshold. The ratio couples an adsorbate geometry proxy (Vol) with a framework accessibility proxy (AV), forming a two-family combination not reducible to any single native input. AV is a fixed-probe, mass-specific accessibility, so the ratio is a proxy contrast rather than a molecule-specific free-volume fraction.",
    "falsification_criteria": "If entropy loss at fixed Vol is independent of AV (no contrast effect), or if the association is fully absorbed by AV alone in the nonlinear ANN's existing D0 inputs, the proposed molecule-to-accessibility coupling is falsified and a pure-framework mechanism should be preferred.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Van der Waals volume proxies the excluded translational footprint of the adsorbate, and fixed-probe AV proxies the available confinement space; both are geometry-only surrogates that ignore adsorbate-specific interactions and framework flexibility, limiting transferability.",
      "physical_interpretation": "q_Vol = Vol/67.24 and q_AV = AV/0.0759781 are dimensionless row-varying inputs relative to fixed training-reference medians; the constant 1 added to q_AV is an empirical smoothing constant with no physical unity meaning.",
      "boundary_behavior": "At AV = 0 (28 legitimate rows), q_AV = 0 and the descriptor reduces to q_Vol, which is finite and positive for all rows since Vol has no zeros; this treats probe-inaccessible frameworks as the limiting high-contrast case rather than imputing a value.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
      "training_spearman": 0.6670225864977195,
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
    "slot_id": "h3",
    "name": "molecule_accessibility_ratio",
    "formula": "q_Vol / (q_AV + 1)",
    "hypothesis": "At infinite dilution, adsorbed-phase translational entropy loss scales with the ratio of adsorbate van der Waals volume to framework probe-accessible specific volume: molecules that are large relative to the framework's accessible space lose proportionally more translational entropy, and the entropy loss increases with this ratio.",
    "rationale": "The +1 in the denominator guarantees finiteness for the 28 legitimate AV = 0 rows (fixed-probe inaccessibility does not imply zero physical adsorption space), and it is an explicit smoothing choice, not a claim of a physical unity threshold. The ratio couples an adsorbate geometry proxy (Vol) with a framework accessibility proxy (AV), forming a two-family combination not reducible to any single native input. AV is a fixed-probe, mass-specific accessibility, so the ratio is a proxy contrast rather than a molecule-specific free-volume fraction.",
    "falsification_criteria": "If entropy loss at fixed Vol is independent of AV (no contrast effect), or if the association is fully absorbed by AV alone in the nonlinear ANN's existing D0 inputs, the proposed molecule-to-accessibility coupling is falsified and a pure-framework mechanism should be preferred.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Van der Waals volume proxies the excluded translational footprint of the adsorbate, and fixed-probe AV proxies the available confinement space; both are geometry-only surrogates that ignore adsorbate-specific interactions and framework flexibility, limiting transferability.",
      "physical_interpretation": "q_Vol = Vol/67.24 and q_AV = AV/0.0759781 are dimensionless row-varying inputs relative to fixed training-reference medians; the constant 1 added to q_AV is an empirical smoothing constant with no physical unity meaning.",
      "boundary_behavior": "At AV = 0 (28 legitimate rows), q_AV = 0 and the descriptor reduces to q_Vol, which is finite and positive for all rows since Vol has no zeros; this treats probe-inaccessible frameworks as the limiting high-contrast case rather than imputing a value.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
      "training_spearman": 0.6670225864977195,
      "target_association": "consistent",
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
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ec1e8193a4e127c7e5a5ba8d",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:4ee093d81da6b5c01358e0ca",
        "paper_id": "doi:10.1021/acs.jctc.5c01100",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9805f0a944c903cd7580bbcb",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08aecb87be6d1cda8c6566fa",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:0cf2190b50453d52d7cdf194",
        "paper_id": "pmc:pmc6179455",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:147fa339122edc3ff44ba658",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:166106b9d0f41731d2d72c4f",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:16e2b39b6d98fe8886d05f3e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:94478c262e1be8498b9fcc39",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9a3907e626bcdef0bc5bb0cb",
        "paper_id": "doi:10.1002/chem.201705627",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica frameworks, adsorbates with larger heavy-atom pair distance (more elongated molecules) lose a larger fraction of their gas-phase rotational/librational entropy upon confinement, so the entropy loss (in units of R) increases monotonically with GeDi even after molecular-weight and volume effects are accounted for elsewhere. log(1 + q_GeDi) Frameworks with smaller passing free-sphere bottlenecks (smaller lsd_f, the Zeo++ Df largest sphere through a periodic free path) impose stronger geometric confinement gradients at adsorption sites, producing larger adsorbed-phase entropy loss at infinite dilution; the entropy loss is inversely associated with the bottleneck diameter squared. 1 / q_lsd_f**2 At infinite dilution, adsorbed-phase translational entropy loss scales with the ratio of adsorbate van der Waals volume to framework probe-accessible specific volume: molecules that are large relative to the framework's accessible space lose proportionally more translational entropy, and the entropy loss increases with this ratio. q_Vol / (q_AV + 1)",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:28331648a2c381e7802dd8ad",
      "chunk:8dd99e6f4fc8a3c4e46d940b",
      "chunk:488a25074219dc1bb01f1486"
    ],
    "items": 10,
    "lexical_tokens": 4746,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [],
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
