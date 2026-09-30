# low/small_kg_rag_agent/replicate-1/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/small_kg_rag_agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`low/small_kg_rag_agent/replicate-1/round-1/h1`

最终状态：scored；边际收益：+0.657642 pp；保留：False。

复核改动字段：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confined_translator",
    "formula": "log(1 + (Vol/Vol_ref) * (lsd_f/lsd_f_ref)**-2) - (lsd_f/lsd_f_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, translational entropy loss grows with adsorbate volume relative to the framework passing bottleneck: adsorbates with large van der Waals volume confined by small Df bottlenecks lose more translational entropy, so the descriptor increases as entropy loss increases.",
    "rationale": "Translational confinement in a narrow channel reduces accessible configurational volume; volume-to-bottleneck contrast is an empirical proxy for that loss. The log term bounds growth; the negative linear bottleneck term captures monotone relief of confinement as Df grows. Limitations: Df is a passing-sphere bottleneck, not the cavity where the molecule sits; Vol is a bulk vdw volume, not a free-volume measure.",
    "falsification_criteria": "If entropy loss does not increase with (Vol/Vol_ref)*(lsd_f/lsd_f_ref)**-2 across the full training quantile range of lsd_f, or if large-cavity/small-bottleneck frameworks behave oppositely (molecules residing in large cages while Df only gates migration), the hypothesis is falsified in favor of a cavity-size (included-sphere) mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol proxies molecular excluded volume; lsd_f proxies geometric confinement. Transfer limited because bottleneck diameter governs passage, not the local adsorption site; fixed-probe AV and molecule-specific free volume differ.",
      "physical_interpretation": "Native lsd_f is Zeo++ Df (largest sphere passing through a periodic free path), not global cavity Di; q_lsd_f is a row-varying normalized input against a fixed training reference, not a physical equality threshold.",
      "boundary_behavior": "Vol and lsd_f are strictly positive over the training domain (zero_n = 0), so the expression is finite on every row; as lsd_f -> large values the log term decays toward log(1+small) and the descriptor decreases monotonically, reflecting weak confinement.",
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
      "training_spearman": 0.5868055095752168,
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
    "formula": "log(1 + (Vol/Vol_ref) * (lsd_f/lsd_f_ref)**-2) - (lsd_f/lsd_f_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, translational entropy loss grows with adsorbate volume relative to the framework passing bottleneck: adsorbates with large van der Waals volume confined by small Df bottlenecks lose more translational entropy, so the descriptor increases as entropy loss increases.",
    "rationale": "Translational confinement reduces accessible configurational volume; the volume-to-bottleneck contrast is an empirical proxy for that loss. The log term bounds growth; the negative linear bottleneck term captures monotone relief as Df grows. Limitations: Df is a passing-sphere bottleneck, not the adsorption cavity (E02's confinement descriptor is cavity diameter, a different quantity); Vol is a bulk vdw volume, not a free-volume measure; the training Spearman is positive and consistent with the declared entropy-loss-increasing direction but does not validate causality.",
    "falsification_criteria": "If entropy loss does not increase with (Vol/Vol_ref)*(lsd_f/lsd_f_ref)**-2 across the full training quantile range of lsd_f, or if large-cavity/small-bottleneck frameworks behave oppositely (molecules residing in large cages while Df only gates migration), the hypothesis is falsified in favor of a cavity-size (included-sphere) mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol proxies molecular excluded volume; lsd_f proxies geometric confinement via the migration bottleneck, which may mismatch the cavity where the molecule actually resides (large-cage/small-bottleneck frameworks are the key competing case). AV is fixed-probe and mass-specific and is deliberately not used here.",
      "physical_interpretation": "Native lsd_f is Zeo++ Df, the largest sphere passing through a periodic free path (a bottleneck), NOT the global cavity diameter Di cited in the FER/FAU rotational-entropy comparison (E02); the Df-to-cavity proxy mapping is an assumption, not an equality. q_lsd_f is a row-varying normalized input against the fixed training reference, and q_lsd_f = 1 carries no universal physical meaning.",
      "boundary_behavior": "Vol and lsd_f are strictly positive over the training domain (zero_n = 0), so every row is finite without imputation; as q_lsd_f grows the descriptor decreases monotonically, reflecting relief of confinement.",
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
      "training_spearman": 0.5868055095752168,
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
    "formula": "log(1 + (Vol/Vol_ref) * (lsd_f/lsd_f_ref)**-2) - (lsd_f/lsd_f_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, translational entropy loss grows with adsorbate volume relative to the framework passing bottleneck: adsorbates with large van der Waals volume confined by small Df bottlenecks lose more translational entropy, so the descriptor increases as entropy loss increases.",
    "rationale": "Translational confinement reduces accessible configurational volume; the volume-to-bottleneck contrast is an empirical proxy for that loss. The log term bounds growth; the negative linear bottleneck term captures monotone relief as Df grows. Limitations: Df is a passing-sphere bottleneck, not the adsorption cavity (E02's confinement descriptor is cavity diameter, a different quantity); Vol is a bulk vdw volume, not a free-volume measure; the training Spearman is positive and consistent with the declared entropy-loss-increasing direction but does not validate causality.",
    "falsification_criteria": "If entropy loss does not increase with (Vol/Vol_ref)*(lsd_f/lsd_f_ref)**-2 across the full training quantile range of lsd_f, or if large-cavity/small-bottleneck frameworks behave oppositely (molecules residing in large cages while Df only gates migration), the hypothesis is falsified in favor of a cavity-size (included-sphere) mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol proxies molecular excluded volume; lsd_f proxies geometric confinement via the migration bottleneck, which may mismatch the cavity where the molecule actually resides (large-cage/small-bottleneck frameworks are the key competing case). AV is fixed-probe and mass-specific and is deliberately not used here.",
      "physical_interpretation": "Native lsd_f is Zeo++ Df, the largest sphere passing through a periodic free path (a bottleneck), NOT the global cavity diameter Di cited in the FER/FAU rotational-entropy comparison (E02); the Df-to-cavity proxy mapping is an assumption, not an equality. q_lsd_f is a row-varying normalized input against the fixed training reference, and q_lsd_f = 1 carries no universal physical meaning.",
      "boundary_behavior": "Vol and lsd_f are strictly positive over the training domain (zero_n = 0), so every row is finite without imputation; as q_lsd_f grows the descriptor decreases monotonically, reflecting relief of confinement.",
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
      "training_spearman": 0.5868055095752168,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/small_kg_rag_agent/replicate-1/round-1/h2`

最终状态：scored；边际收益：-2.918472 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotational_freedom_contrast",
    "formula": "rotor_case(log(1 + 1e-8), log(1 + (PMI2/PMI2_ref)**0.5 / (SPAN/SPAN_ref + 1.0)), log(1 + (PMI3/PMI3_ref)**0.5 / (SPAN/SPAN_ref + 1.0)))",
    "hypothesis": "Rotational entropy loss upon adsorption depends on rotor class: single-site rotors (e.g., methane) lose little rotational entropy, while linear and nonlinear rotors lose more in proportion to their heavy-atom inertia extent relative to molecular span; the descriptor increases with expected rotational entropy loss.",
    "rationale": "Heavy-atom PMI proxies (original implicit-H representation) scale the moment of inertia governing rotational partition-function reduction on adsorption; dividing by span-related size keeps the contrast dimensionless. Limitation: PMI proxies are heavy-atom only; methane is single-site though its true all-atom inertia is nonzero, hence the constant small branch value rather than zero.",
    "falsification_criteria": "If entropy loss of linear rotors does not scale with sqrt(PMI2)/size contrast, or if single-site rotors show entropy losses comparable to nonlinear ones at fixed framework, the rotor-class branching (and its claimed ordering single < linear < nonlinear) is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2/PMI3 in the heavy-atom representation proxy rotational inertia; SPAN proxies molecular size. Legitimate zeros in PMI/SPAN would break ratio-only expressions, so +1.0 on the span term and the additive log(1+...) keep every row finite including zero-PMI and zero-SPAN rows.",
      "physical_interpretation": "PMI values are original-representation heavy-atom moments, not true all-atom inertia; the +1.0 constant is a numerical smoother with no universal physical meaning, and q-normalized quantities are row-varying inputs, not physical thresholds.",
      "boundary_behavior": "At PMI or SPAN equal to legitimate zero the numerator/denominator remain finite (sqrt of zero is zero; denominator >= 1), giving the log floor log(1) = 0; single-site branch is a fixed small constant encoding near-zero rotational entropy loss.",
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
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.3840341043705572,
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
    "name": "rotational_freedom_contrast",
    "formula": "rotor_case(log(1 + 1e-8), log(1 + (PMI2/PMI2_ref)**0.5 / (SPAN/SPAN_ref + 1.0)), log(1 + (PMI3/PMI3_ref)**0.5 / (SPAN/SPAN_ref + 1.0)))",
    "hypothesis": "Rotational entropy loss upon adsorption depends on rotor class: single-site rotors (e.g., methane) lose little rotational entropy, while linear and nonlinear rotors lose more in proportion to their heavy-atom inertia extent relative to molecular span; the descriptor increases with expected rotational entropy loss.",
    "rationale": "Heavy-atom PMI proxies (original implicit-H representation) scale the moment of inertia governing rotational partition-function reduction on adsorption; dividing by span-related size keeps the contrast dimensionless. Limitation: PMI proxies are heavy-atom only; methane is single-site though its true all-atom inertia is nonzero, hence the constant small branch value rather than zero.",
    "falsification_criteria": "If entropy loss of linear rotors does not scale with sqrt(PMI2)/size contrast, or if single-site rotors show entropy losses comparable to nonlinear ones at fixed framework, the rotor-class branching (and its claimed ordering single < linear < nonlinear) is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2/PMI3 in the heavy-atom representation proxy rotational inertia; SPAN proxies molecular size. Legitimate zeros in PMI/SPAN would break ratio-only expressions, so +1.0 on the span term and the additive log(1+...) keep every row finite including zero-PMI and zero-SPAN rows.",
      "physical_interpretation": "PMI values are original-representation heavy-atom moments, not true all-atom inertia; the +1.0 constant is a numerical smoother with no universal physical meaning, and q-normalized quantities are row-varying inputs, not physical thresholds.",
      "boundary_behavior": "At PMI or SPAN equal to legitimate zero the numerator/denominator remain finite (sqrt of zero is zero; denominator >= 1), giving the log floor log(1) = 0; single-site branch is a fixed small constant encoding near-zero rotational entropy loss.",
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
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.3840341043705572,
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
    "name": "rotational_freedom_contrast",
    "formula": "rotor_case(log(1 + 1e-8), log(1 + (PMI2/PMI2_ref)**0.5 / (SPAN/SPAN_ref + 1.0)), log(1 + (PMI3/PMI3_ref)**0.5 / (SPAN/SPAN_ref + 1.0)))",
    "hypothesis": "Rotational entropy loss upon adsorption depends on rotor class: single-site rotors (e.g., methane) lose little rotational entropy, while linear and nonlinear rotors lose more in proportion to their heavy-atom inertia extent relative to molecular span; the descriptor increases with expected rotational entropy loss.",
    "rationale": "Heavy-atom PMI proxies (original implicit-H representation) scale the moment of inertia governing rotational partition-function reduction on adsorption; dividing by span-related size keeps the contrast dimensionless. Limitation: PMI proxies are heavy-atom only; methane is single-site though its true all-atom inertia is nonzero, hence the constant small branch value rather than zero.",
    "falsification_criteria": "If entropy loss of linear rotors does not scale with sqrt(PMI2)/size contrast, or if single-site rotors show entropy losses comparable to nonlinear ones at fixed framework, the rotor-class branching (and its claimed ordering single < linear < nonlinear) is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2/PMI3 in the heavy-atom representation proxy rotational inertia; SPAN proxies molecular size. Legitimate zeros in PMI/SPAN would break ratio-only expressions, so +1.0 on the span term and the additive log(1+...) keep every row finite including zero-PMI and zero-SPAN rows.",
      "physical_interpretation": "PMI values are original-representation heavy-atom moments, not true all-atom inertia; the +1.0 constant is a numerical smoother with no universal physical meaning, and q-normalized quantities are row-varying inputs, not physical thresholds.",
      "boundary_behavior": "At PMI or SPAN equal to legitimate zero the numerator/denominator remain finite (sqrt of zero is zero; denominator >= 1), giving the log floor log(1) = 0; single-site branch is a fixed small constant encoding near-zero rotational entropy loss.",
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
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.3840341043705572,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/small_kg_rag_agent/replicate-1/round-1/h3`

最终状态：scored；边际收益：+2.895950 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_shaping",
    "formula": "(AV/AV_ref) * ((LabuteASA/LabuteASA_ref) / (GeDi/GeDi_ref + 0.5))",
    "hypothesis": "Adsorption configurational entropy loss decreases with the amount of probe-accessible framework volume per mass (more accessible space retains more configurational freedom), but is modulated by adsorbate shape: elongated adsorbates (large GeDi relative to surface area) lose entropy faster as accessibility shrinks; the descriptor increases with retained entropy, so entropy loss decreases with it.",
    "rationale": "AV is a fixed-probe mass-specific accessibility proxy for the available configurational space; the shape contrast (area-to-length) captures how effectively a molecule can exploit that space orientationally. Limitations: AV is probe-specific and mass-specific, not molecule-specific free volume; zero AV does not mean zero physical adsorption space.",
    "falsification_criteria": "If entropy loss is uncorrelated or positively correlated with AV across the training quantile range (e.g., strong confinement entropy loss dominates even in high-AV frameworks), or if elongation contrast does not modulate the association, the accessibility-volume mechanism is falsified in favor of a pure bottleneck or site-geometry mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "LabuteASA": "adsorbate_geometry_proxy",
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV proxies accessible configurational space despite fixed-probe bias; LabuteASA and GeDi (heavy-atom representation) proxy adsorbate shape. The +0.5 constant is an empirical smoother preventing amplification near legitimate GeDi zeros, carrying no universal physical meaning.",
      "physical_interpretation": "AV is fixed-probe, mass-specific accessibility (cm^3/g), not molecule-specific free volume; GeDi is the largest heavy-atom pair distance; q-normalization is row-varying against fixed training references, not a physical equality threshold.",
      "boundary_behavior": "At AV = 0 (28 legitimate training zeros) the descriptor is exactly 0, finite by construction, encoding no accessibility benefit; at GeDi = 0 the denominator >= 0.5 keeps the expression finite.",
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
        "GeDi",
        "LabuteASA"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": -0.31563670987143616,
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
    "slot_id": "h3",
    "name": "accessible_volume_shaping",
    "formula": "(AV/AV_ref) * ((LabuteASA/LabuteASA_ref) / (GeDi/GeDi_ref + 0.5))",
    "hypothesis": "Adsorption configurational entropy loss decreases with the amount of probe-accessible framework volume per mass (more accessible space retains more configurational freedom), but is modulated by adsorbate shape: elongated adsorbates (large GeDi relative to surface area) lose entropy faster as accessibility shrinks; the descriptor increases with retained entropy, so entropy loss decreases with it.",
    "rationale": "AV is a fixed-probe mass-specific accessibility proxy for the available configurational space; the shape contrast (area-to-length) captures how effectively a molecule can exploit that space orientationally. Limitations: AV is probe-specific and mass-specific, not molecule-specific free volume; zero AV does not mean zero physical adsorption space.",
    "falsification_criteria": "If entropy loss is uncorrelated or positively associated with AV across the training quantile range (e.g., confinement-dominated losses even in high-AV frameworks), or if the elongation contrast does not modulate the association, the accessibility-volume mechanism is falsified in favor of a bottleneck or site-geometry mechanism (E02, E04).",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E07"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "LabuteASA": "adsorbate_geometry_proxy",
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV proxies accessible configurational space despite fixed-probe and mass-specific bias; LabuteASA and GeDi proxy adsorbate shape. Retained-mobility effects (E05, E09) mean even high-AV frameworks can show large losses; kinetic escape arguments do not determine equilibrium entropy.",
      "physical_interpretation": "AV is fixed-probe, mass-specific accessibility (cm^3/g), not molecule-specific free volume, so no literal AV/Vol free-volume equality is claimed. GeDi is the largest heavy-atom pair distance and LabuteASA the approximate molecular surface area, both in the original heavy-atom representation with legitimate zeros. q-ratios are row-varying normalizations against fixed training references; q = 1 is not a physical threshold, and the +0.5 constant is an empirical smoother with no universal meaning.",
      "boundary_behavior": "At AV = 0 (28 legitimate training zeros) the descriptor is exactly 0 and finite by construction, encoding no accessibility benefit — AV = 0 does not imply zero physical adsorption space; at GeDi = 0 the denominator floor 0.5 keeps the expression finite; LabuteASA is strictly positive on the training domain.",
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
        "GeDi",
        "LabuteASA"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": -0.31563670987143616,
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
    "name": "accessible_volume_shaping",
    "formula": "(AV/AV_ref) * ((LabuteASA/LabuteASA_ref) / (GeDi/GeDi_ref + 0.5))",
    "hypothesis": "Adsorption configurational entropy loss decreases with the amount of probe-accessible framework volume per mass (more accessible space retains more configurational freedom), but is modulated by adsorbate shape: elongated adsorbates (large GeDi relative to surface area) lose entropy faster as accessibility shrinks; the descriptor increases with retained entropy, so entropy loss decreases with it.",
    "rationale": "AV is a fixed-probe mass-specific accessibility proxy for the available configurational space; the shape contrast (area-to-length) captures how effectively a molecule can exploit that space orientationally. Limitations: AV is probe-specific and mass-specific, not molecule-specific free volume; zero AV does not mean zero physical adsorption space.",
    "falsification_criteria": "If entropy loss is uncorrelated or positively associated with AV across the training quantile range (e.g., confinement-dominated losses even in high-AV frameworks), or if the elongation contrast does not modulate the association, the accessibility-volume mechanism is falsified in favor of a bottleneck or site-geometry mechanism (E02, E04).",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E07"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "LabuteASA": "adsorbate_geometry_proxy",
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV proxies accessible configurational space despite fixed-probe and mass-specific bias; LabuteASA and GeDi proxy adsorbate shape. Retained-mobility effects (E05, E09) mean even high-AV frameworks can show large losses; kinetic escape arguments do not determine equilibrium entropy.",
      "physical_interpretation": "AV is fixed-probe, mass-specific accessibility (cm^3/g), not molecule-specific free volume, so no literal AV/Vol free-volume equality is claimed. GeDi is the largest heavy-atom pair distance and LabuteASA the approximate molecular surface area, both in the original heavy-atom representation with legitimate zeros. q-ratios are row-varying normalizations against fixed training references; q = 1 is not a physical threshold, and the +0.5 constant is an empirical smoother with no universal meaning.",
      "boundary_behavior": "At AV = 0 (28 legitimate training zeros) the descriptor is exactly 0 and finite by construction, encoding no accessibility benefit — AV = 0 does not imply zero physical adsorption space; at GeDi = 0 the denominator floor 0.5 keeps the expression finite; LabuteASA is strictly positive on the training domain.",
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
        "GeDi",
        "LabuteASA"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": -0.31563670987143616,
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
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:43dedbc998f9c278eea622b0",
        "paper_id": "pmc:pmc9739862",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d3a799358d58da57167e96f1",
        "paper_id": "doi:10.1021/acs.langmuir.3c03931",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:06a26a29dca2516a90c93ace",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:323d66ad417d981217705b45",
        "paper_id": "doi:10.1021/ja015797o",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:560d540c09c85dfa3faa0e8c",
        "paper_id": "doi:10.1021/acs.jpcb.1c02929",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:682b714f21fe17245939e4e3",
        "paper_id": "doi:10.1063/1.2790903",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, translational entropy loss grows with adsorbate volume relative to the framework passing bottleneck: adsorbates with large van der Waals volume confined by small Df bottlenecks lose more translational entropy, so the descriptor increases as entropy loss increases. log(1 + (Vol/Vol_ref) * (lsd_f/lsd_f_ref)**-2) - (lsd_f/lsd_f_ref) Rotational entropy loss upon adsorption depends on rotor class: single-site rotors (e.g., methane) lose little rotational entropy, while linear and nonlinear rotors lose more in proportion to their heavy-atom inertia extent relative to molecular span; the descriptor increases with expected rotational entropy loss. rotor_case(log(1 + 1e-8), log(1 + (PMI2/PMI2_ref)**0.5 / (SPAN/SPAN_ref + 1.0)), log(1 + (PMI3/PMI3_ref)**0.5 / (SPAN/SPAN_ref + 1.0))) Adsorption configurational entropy loss decreases with the amount of probe-accessible framework volume per mass (more accessible space retains more configurational freedom), but is modulated by adsorbate shape: elongated adsorbates (large GeDi relative to surface area) lose entropy faster as accessibility shrinks; the descriptor increases with retained entropy, so entropy loss decreases with it. (AV/AV_ref) * ((LabuteASA/LabuteASA_ref) / (GeDi/GeDi_ref + 0.5))",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e98dff054a73e56b28f6bdf3"
    ],
    "items": 10,
    "lexical_tokens": 4655,
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
