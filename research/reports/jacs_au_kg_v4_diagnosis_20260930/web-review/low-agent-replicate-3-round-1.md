# low/agent/replicate-3/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`low/agent/replicate-3/round-1/h1`

最终状态：scored；边际收益：+3.278410 pp；保留：True。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confinement_entropy_proxy",
    "formula": "log(lsd_f / lsd_f_ref) - log(lsd_p / lsd_p_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss of adsorption relative to the gas phase increases (s_ads/s_gas decreases) as the contrast between the included-sphere diameter along the free path (lsd_p) and the passing bottleneck (lsd_f) grows, because a large internal cavity reached through a narrow window imposes stronger positional confinement on the adsorbed molecule than the window itself.",
    "rationale": "The difference log(lsd_p/lsd_p_ref) - log(lsd_f/lsd_f_ref) is a dimensionless geometric contrast: large lsd_p with small lsd_f indicates cage-like confinement, expected to reduce adsorbed-phase translational/configurational entropy. This is an empirical proxy claim only; D0 inputs already carry this information, so the descriptor re-expresses it. It cannot establish causality and Di is not measured.",
    "falsification_criteria": "If measured entropy loss at infinite dilution does not increase with (lsd_p - lsd_f) across frameworks holding adsorbate fixed (e.g., methane), or if open-channel frameworks with lsd_p ≈ lsd_f show comparable entropy loss to caged frameworks, the confinement-contrast mechanism is falsified for that regime.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Zeo++ Df/Dif on a fixed probe reflect the true pore architecture; rigid all-silica frameworks; entropy loss dominated by confinement geometry rather than specific SiO2 chemistry.",
      "physical_interpretation": "lsd_f is the passing bottleneck, lsd_p is the included diameter along the free-sphere path; the contrast signals cage-vs-channel topology, not a physical unity threshold.",
      "boundary_behavior": "When lsd_p = lsd_f (channel-like pores) the contrast term vanishes to the reference-log offset, giving a finite neutral value; both inputs are strictly positive over the training domain so the expression is finite for every row.",
      "vary_input": "lsd_f",
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
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "lsd_f": "bottleneck_free_sphere_Df",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 2361,
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
    "slot_id": "h1",
    "name": "bottleneck_confinement_entropy_proxy",
    "formula": "log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss of adsorption relative to the gas phase increases (s_ads/s_gas decreases) as the contrast between the included-sphere diameter along the free path (lsd_p) and the passing bottleneck (lsd_f) grows, because a large internal cavity reached through a narrow window imposes stronger positional confinement on the adsorbed molecule than the window itself.",
    "rationale": "Sign-corrected to match the predeclared direction: a smaller passing bottleneck (lsd_f) relative to the included sphere along the path (lsd_p) indicates stronger cage-like confinement; the descriptor log(lsd_p/lsd_p_ref) - log(lsd_f/lsd_f_ref) increases as lsd_f decreases, consistent with increasing entropy loss (decreasing s_ads/s_gas). Empirical proxy only; re-expresses inputs already available to the model; Di is not measured.",
    "falsification_criteria": "If measured entropy loss at infinite dilution does not increase with the lsd_p/lsd_f contrast across frameworks at fixed adsorbate (e.g., methane), or if open-channel frameworks with lsd_p ≈ lsd_f show comparable entropy loss to caged frameworks, the confinement-contrast mechanism is falsified for that regime.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Zeo++ Df (passing bottleneck) and Dif (included sphere along the free-sphere path) on a fixed probe reflect pore architecture; rigid all-silica frameworks; entropy loss dominated by confinement geometry rather than specific chemistry. Dif is not the global cavity diameter Di.",
      "physical_interpretation": "lsd_f is the bottleneck free sphere; lsd_p is the included diameter along the free path. The log contrast is a dimensionless cage-vs-channel topology proxy; no causal claim and no physical equality threshold.",
      "boundary_behavior": "Both lsd_f and lsd_p are strictly positive over the training domain (min 0.85684 Å and 3.3452 Å), so the expression is finite for every training row. When lsd_p = lsd_f the descriptor reduces to a constant reference offset (log(lsd_f_ref/lsd_p_ref)), a finite neutral value, not a physical unity threshold.",
      "vary_input": "lsd_f",
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
    "status": "passed",
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
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        3.3452,
        15.5604
      ],
      "training_spearman": -0.01948972800795131,
      "target_association": "inconclusive",
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
    "name": "bottleneck_confinement_entropy_proxy",
    "formula": "log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss of adsorption relative to the gas phase increases (s_ads/s_gas decreases) as the contrast between the included-sphere diameter along the free path (lsd_p) and the passing bottleneck (lsd_f) grows, because a large internal cavity reached through a narrow window imposes stronger positional confinement on the adsorbed molecule than the window itself.",
    "rationale": "Sign-corrected to match the predeclared direction: a smaller passing bottleneck (lsd_f) relative to the included sphere along the path (lsd_p) indicates stronger cage-like confinement; the descriptor log(lsd_p/lsd_p_ref) - log(lsd_f/lsd_f_ref) increases as lsd_f decreases, consistent with increasing entropy loss (decreasing s_ads/s_gas). Empirical proxy only; re-expresses inputs already available to the model; Di is not measured.",
    "falsification_criteria": "If measured entropy loss at infinite dilution does not increase with the lsd_p/lsd_f contrast across frameworks at fixed adsorbate (e.g., methane), or if open-channel frameworks with lsd_p ≈ lsd_f show comparable entropy loss to caged frameworks, the confinement-contrast mechanism is falsified for that regime.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Zeo++ Df (passing bottleneck) and Dif (included sphere along the free-sphere path) on a fixed probe reflect pore architecture; rigid all-silica frameworks; entropy loss dominated by confinement geometry rather than specific chemistry. Dif is not the global cavity diameter Di.",
      "physical_interpretation": "lsd_f is the bottleneck free sphere; lsd_p is the included diameter along the free path. The log contrast is a dimensionless cage-vs-channel topology proxy; no causal claim and no physical equality threshold.",
      "boundary_behavior": "Both lsd_f and lsd_p are strictly positive over the training domain (min 0.85684 Å and 3.3452 Å), so the expression is finite for every training row. When lsd_p = lsd_f the descriptor reduces to a constant reference offset (log(lsd_f_ref/lsd_p_ref)), a finite neutral value, not a physical unity threshold.",
      "vary_input": "lsd_f",
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
    "status": "passed",
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
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        3.3452,
        15.5604
      ],
      "training_spearman": -0.01948972800795131,
      "target_association": "inconclusive",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/agent/replicate-3/round-1/h2`

最终状态：scored；边际收益：+1.038254 pp；保留：False。

复核改动字段：formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "heavy_atom_shape_confinement_proxy",
    "formula": "log(SPAN / SPAN_ref) + log(GeDi / GeDi_ref) - log(Vol / Vol_ref)",
    "hypothesis": "For a fixed framework, adsorption entropy loss at infinite dilution grows with an adsorbate's elongated heavy-atom shape: molecules with large enclosing radius (SPAN) and largest atom pair distance (GeDi) relative to their van der Waals volume (Vol) lose more translational and orientational entropy upon confinement because elongated molecules have fewer compatible orientations inside pores.",
    "rationale": "The ratio (SPAN·GeDi)/Vol is a dimensionless shape-asphericity proxy: linear/rod-like molecules score high, compact molecules low. The log of this ratio, offset by reference logs, is a dimensionless descriptor. This is an empirical proxy claim using heavy-atom representations; true all-atom geometry (including hydrogens) is not captured, and no causal claim is made. The descriptor is redundant with geometry inputs already entering the ANN.",
    "falsification_criteria": "If, at fixed molecular volume, entropy loss does not increase with SPAN·GeDi/Vol across adsorbates in a fixed framework, or if compact high-volume molecules show equal or greater entropy loss, the shape-asphericity mechanism is rejected. Rotational entropy dominance for near-spherical adsorbates (e.g., methane) outside the model would also falsify generality.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "GeDi": "heavy_atom_pair_distance",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "Heavy-atom (implicit-H) geometry proxies rank shape asphericity relevant to confinement; van der Waals volume approximates excluded volume; transfer across adsorbate chemistries holds only for non-specific (silica) interactions.",
      "physical_interpretation": "SPAN, GeDi, Vol retain native meanings; ratios to fixed training-reference medians (SPAN_ref = 1.8606 Å, GeDi_ref = 3.3027 Å, Vol_ref = 67.24 Å^3) are row-varying dimensionless scalings, not physical unity thresholds.",
      "boundary_behavior": "Vol is strictly positive in training so division is safe; for a hypothetical single-atom/small molecule SPAN and GeDi can be legitimately near zero, making the log argument approach zero and the descriptor go to negative infinity — the descriptor is therefore declared invalid for such rows and is restricted to the finite training domain where SPAN, GeDi > 0 for the branch used; no epsilon is added.",
      "vary_input": "SPAN",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        "GeDi",
        "SPAN",
        "Vol"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "SPAN": "heavy_atom_enclosing_radius",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "domain_failure": {
      "invalid_n": 54,
      "invalid_fraction": 0.022871664548919948,
      "zero_variables_on_invalid_rows": {
        "SPAN": 54,
        "GeDi": 54,
        "Vol": 0
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
    "slot_id": "h2",
    "name": "heavy_atom_shape_confinement_proxy",
    "formula": "log(1 + SPAN / SPAN_ref) + log(1 + GeDi / GeDi_ref) - log(Vol / Vol_ref)",
    "hypothesis": "For a fixed framework, adsorption entropy loss at infinite dilution grows with an adsorbate's elongated heavy-atom shape: molecules with large enclosing radius (SPAN) and largest atom pair distance (GeDi) relative to their van der Waals volume (Vol) lose more translational and orientational entropy upon confinement because elongated molecules have fewer compatible orientations inside pores.",
    "rationale": "Shifted-log form keeps the shape-asphericity mechanism (SPAN·GeDi relative to Vol) while remaining finite on the 54 rows where SPAN and GeDi are legitimately zero. For a fixed framework, more elongated heavy-atom shape relative to volume is empirically associated with larger entropy loss (lower s_ads/s_gas). Proxy claim only; redundant with geometry inputs already entering the ANN; no causal claim.",
    "falsification_criteria": "If, at fixed molecular volume, entropy loss does not increase with SPAN·GeDi/Vol across adsorbates in a fixed framework, or if compact high-volume molecules show equal or greater entropy loss, the shape-asphericity mechanism is rejected. Rotational entropy dominance for near-spherical adsorbates (e.g., methane) outside the model would also falsify generality.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "GeDi": "heavy_atom_pair_distance",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "Heavy-atom (implicit-H) geometry proxies rank shape asphericity relevant to confinement; van der Waals volume approximates excluded volume; transfer across adsorbate chemistries holds only for non-specific (silica) interactions. Legitimate heavy-atom zeros are not asserted to be zero all-atom inertia or geometry.",
      "physical_interpretation": "SPAN (enclosing radius), GeDi (largest heavy-atom pair distance) and Vol (vdw volume) retain native meanings; SPAN_ref = 1.8606 Å, GeDi_ref = 3.3027 Å, Vol_ref = 67.24 Å^3 are fixed training-reference medians forming row-varying dimensionless scalings, not physical unity thresholds.",
      "boundary_behavior": "Vol is strictly positive in training. SPAN and GeDi are legitimately zero on 54 training rows (compact/single-site heavy-atom representations); the shifted log arguments 1 + SPAN/SPAN_ref and 1 + GeDi/GeDi_ref are ≥ 1 there, so the descriptor is finite for every training row without imputation or epsilon. The +1 shift is a declared empirical smoothing device, not a physical law.",
      "vary_input": "SPAN",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        "GeDi",
        "SPAN",
        "Vol"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "SPAN": "heavy_atom_enclosing_radius",
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
      "training_spearman": 0.21572804502828102,
      "target_association": "contradicted",
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
    "slot_id": "h2",
    "name": "heavy_atom_shape_confinement_proxy",
    "formula": "log(1 + SPAN / SPAN_ref) + log(1 + GeDi / GeDi_ref) - log(Vol / Vol_ref)",
    "hypothesis": "For a fixed framework, adsorption entropy loss at infinite dilution grows with an adsorbate's elongated heavy-atom shape: molecules with large enclosing radius (SPAN) and largest atom pair distance (GeDi) relative to their van der Waals volume (Vol) lose more translational and orientational entropy upon confinement because elongated molecules have fewer compatible orientations inside pores.",
    "rationale": "Shifted-log form keeps the shape-asphericity mechanism (SPAN·GeDi relative to Vol) while remaining finite on the 54 rows where SPAN and GeDi are legitimately zero. For a fixed framework, more elongated heavy-atom shape relative to volume is empirically associated with larger entropy loss (lower s_ads/s_gas). Proxy claim only; redundant with geometry inputs already entering the ANN; no causal claim.",
    "falsification_criteria": "If, at fixed molecular volume, entropy loss does not increase with SPAN·GeDi/Vol across adsorbates in a fixed framework, or if compact high-volume molecules show equal or greater entropy loss, the shape-asphericity mechanism is rejected. Rotational entropy dominance for near-spherical adsorbates (e.g., methane) outside the model would also falsify generality.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "GeDi": "heavy_atom_pair_distance",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "Heavy-atom (implicit-H) geometry proxies rank shape asphericity relevant to confinement; van der Waals volume approximates excluded volume; transfer across adsorbate chemistries holds only for non-specific (silica) interactions. Legitimate heavy-atom zeros are not asserted to be zero all-atom inertia or geometry.",
      "physical_interpretation": "SPAN (enclosing radius), GeDi (largest heavy-atom pair distance) and Vol (vdw volume) retain native meanings; SPAN_ref = 1.8606 Å, GeDi_ref = 3.3027 Å, Vol_ref = 67.24 Å^3 are fixed training-reference medians forming row-varying dimensionless scalings, not physical unity thresholds.",
      "boundary_behavior": "Vol is strictly positive in training. SPAN and GeDi are legitimately zero on 54 training rows (compact/single-site heavy-atom representations); the shifted log arguments 1 + SPAN/SPAN_ref and 1 + GeDi/GeDi_ref are ≥ 1 there, so the descriptor is finite for every training row without imputation or epsilon. The +1 shift is a declared empirical smoothing device, not a physical law.",
      "vary_input": "SPAN",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        "GeDi",
        "SPAN",
        "Vol"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "SPAN": "heavy_atom_enclosing_radius",
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
      "training_spearman": 0.21572804502828102,
      "target_association": "contradicted",
      "perturbation": 0.02159332416,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/agent/replicate-3/round-1/h3`

最终状态：scored；边际收益：+2.484025 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_density_proxy",
    "formula": "log((AV / AV_ref) / (density / density_ref))",
    "hypothesis": "At infinite dilution, frameworks combining high probe-accessible specific volume (AV) with low framework density offer weaker confinement per unit pore wall contact, so adsorption entropy loss decreases (s_ads/s_gas increases) as AV/density rises; conversely, dense frameworks with small accessible volume confine molecules more tightly and increase entropy loss.",
    "rationale": "AV per framework mass scaled by inverse density is an empirical proxy for openness/porosity contrast on a fixed-probe basis. It is a known-style volumetric correlation recombined with density; the descriptor only re-expresses inputs already available to the ANN. It does not measure molecule-specific free volume and carries no causal claim.",
    "falsification_criteria": "If, holding adsorbate fixed, entropy loss does not decrease monotonically (within noise) with AV/density across pure-silica frameworks — e.g., if large-pore frameworks with strong wall-contact geometry show equal entropy loss to dense frameworks — the porosity proxy mechanism is falsified; a competing surface-area-controlled mechanism (ASA) would then be the better explanation.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Fixed-probe accessibility (AV) approximates relative molecular adsorption space; framework density on its native numerical scale ranks compactness; rigid pure-silica frameworks only; AV = 0 for the fixed probe does not imply zero molecular space, so the proxy is invalid at AV = 0 rows.",
      "physical_interpretation": "AV_ref = 0.0759781 cm^3/g and density_ref = 1.73742 are fixed training-reference medians used only to form row-varying dimensionless ratios; the log argument is dimensionless; no q-unity physical threshold is asserted.",
      "boundary_behavior": "For the 28 training rows with AV = 0 (probe-inaccessible), the log argument is zero and the descriptor diverges; therefore this descriptor is declared valid only on rows with AV > 0, and on AV = 0 rows the branch value is set to the finite limit of minimum log argument via the allowed expression minimum(log((AV/AV_ref)/(density/density_ref)), c) with fixed constant c = -8, i.e., minimum(..., -8) as a declared empirical clamp, not a physical law.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "density",
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
        "density"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "domain_failure": {
      "invalid_n": 28,
      "invalid_fraction": 0.011859381617958492,
      "zero_variables_on_invalid_rows": {
        "density": 0,
        "AV": 28
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
    "name": "accessible_volume_density_proxy",
    "formula": "log(1 + AV / AV_ref) - log(density / density_ref)",
    "hypothesis": "At infinite dilution, frameworks combining high probe-accessible specific volume (AV) with low framework density offer weaker confinement per unit pore wall contact, so adsorption entropy loss decreases (s_ads/s_gas increases) as AV/density rises; conversely, dense frameworks with small accessible volume confine molecules more tightly and increase entropy loss.",
    "rationale": "Shifted-log form keeps the porosity/compactness contrast mechanism while remaining finite on the 28 AV = 0 rows. Higher AV relative to density is empirically associated with weaker confinement per wall contact and thus smaller entropy loss (higher s_ads/s_gas). Known-style volumetric correlation; no causal claim.",
    "falsification_criteria": "If, holding adsorbate fixed, entropy loss does not decrease with AV/density across pure-silica frameworks — e.g., if large-pore frameworks with strong wall-contact geometry show equal entropy loss to dense frameworks — the porosity proxy mechanism is falsified; a competing surface-area-controlled mechanism (ASA) would then be the better explanation.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Fixed-probe accessibility (AV) only approximates relative molecular adsorption space; framework density is a native-scale proxy for compactness with unresolved physical unit; rigid pure-silica frameworks only. Kinetic escape does not by itself determine equilibrium entropy.",
      "physical_interpretation": "AV (cm^3/g, fixed-probe mass-specific accessibility) and density (native scale) retain native meanings; AV_ref = 0.0759781 cm^3/g and density_ref = 1.73742 are fixed training-reference medians forming row-varying dimensionless ratios; the log arguments are dimensionless and no q-unity physical threshold is asserted.",
      "boundary_behavior": "density is strictly positive over training (min 0.759654). AV is legitimately zero on 28 training rows (fixed-probe inaccessibility), where the shifted argument 1 + AV/AV_ref = 1 gives a finite descriptor value of -log(density/density_ref); zero AV does not imply zero molecular adsorption space. The +1 shift is a declared empirical smoothing device, not a physical law.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "density",
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
        "density"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": -0.4389060113545995,
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
    "name": "accessible_volume_density_proxy",
    "formula": "log(1 + AV / AV_ref) - log(density / density_ref)",
    "hypothesis": "At infinite dilution, frameworks combining high probe-accessible specific volume (AV) with low framework density offer weaker confinement per unit pore wall contact, so adsorption entropy loss decreases (s_ads/s_gas increases) as AV/density rises; conversely, dense frameworks with small accessible volume confine molecules more tightly and increase entropy loss.",
    "rationale": "Shifted-log form keeps the porosity/compactness contrast mechanism while remaining finite on the 28 AV = 0 rows. Higher AV relative to density is empirically associated with weaker confinement per wall contact and thus smaller entropy loss (higher s_ads/s_gas). Known-style volumetric correlation; no causal claim.",
    "falsification_criteria": "If, holding adsorbate fixed, entropy loss does not decrease with AV/density across pure-silica frameworks — e.g., if large-pore frameworks with strong wall-contact geometry show equal entropy loss to dense frameworks — the porosity proxy mechanism is falsified; a competing surface-area-controlled mechanism (ASA) would then be the better explanation.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Fixed-probe accessibility (AV) only approximates relative molecular adsorption space; framework density is a native-scale proxy for compactness with unresolved physical unit; rigid pure-silica frameworks only. Kinetic escape does not by itself determine equilibrium entropy.",
      "physical_interpretation": "AV (cm^3/g, fixed-probe mass-specific accessibility) and density (native scale) retain native meanings; AV_ref = 0.0759781 cm^3/g and density_ref = 1.73742 are fixed training-reference medians forming row-varying dimensionless ratios; the log arguments are dimensionless and no q-unity physical threshold is asserted.",
      "boundary_behavior": "density is strictly positive over training (min 0.759654). AV is legitimately zero on 28 training rows (fixed-probe inaccessibility), where the shifted argument 1 + AV/AV_ref = 1 gives a finite descriptor value of -log(density/density_ref); zero AV does not imply zero molecular adsorption space. The +1 shift is a declared empirical smoothing device, not a physical law.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "density",
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
        "density"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": -0.4389060113545995,
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
    "mode": "no_retrieval",
    "items": 0,
    "lexical_tokens": 0
  },
  "cited_items": [],
  "mechanism_cards": []
}
```
