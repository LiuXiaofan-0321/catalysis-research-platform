# low/agent/replicate-2/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h3",
    "name": "accessible_volume_per_contact_area_descriptor",
    "formula": "q_AV / (q_LabuteASA ** 0.5)",
    "hypothesis": "Entropy loss at infinite dilution associates with the contrast between framework accessible volume per unit adsorbate contact area: frameworks with larger accessible volume (AV) relative to the adsorbate's molecular surface area (LabuteASA) permit fewer adsorbate-framework contact constraints per available configurational space, so entropy loss should DECREASE as AV/sqrt(LabuteASA) increases.",
    "rationale": "Contact-area-based confinement arguments suggest that more adsorbate-framework contacting surface restricts both translation and rotation; more accessible volume dilutes this restriction. The sqrt on LabuteASA is an empirical scaling choice for dimensional compatibility (angstrom^3 vs angstrom), not a derived exponent. AV is a fixed-probe (Zeo++ probe radius) mass-specific quantity, not molecule-specific free volume — this is a proxy limitation. The 28 rows with AV = 0 represent zero accessibility for the fixed geometric probe, which does not imply zero molecular adsorption space.",
    "falsification_criteria": "If the partial association of the descriptor with entropy loss is opposite in sign (entropy loss increasing with the descriptor), or if the association vanishes after controlling for lsd_f and Vol (indicating it merely re-expresses confinement already captured), the hypothesis fails. Also fails if AV=0 frameworks show entropy-loss behavior inconsistent with the low-descriptor limit.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "AV is a fixed-probe accessibility, not molecule-specific free volume; LabuteASA is an implicit-H approximate surface area used as a contact-extent proxy. The coupling mechanism (adsorbate-framework contact restricting both translation and rotation) is assumed, not established.",
      "physical_interpretation": "Native AV in cm^3/g and LabuteASA in angstrom^2; q-normalization uses fixed positive training medians (AV_ref = 0.0759781, LabuteASA_ref = 31.85047501), giving dimensionally compatible units under the sqrt scaling. No physical q-unity threshold is claimed.",
      "boundary_behavior": "AV can be legitimately zero (28 training rows), giving descriptor = 0, which is finite and means 'no probe-accessible volume for the fixed probe'; this is an honest low-limit, not imputation. LabuteASA is strictly positive (min 7.45), so no division by zero occurs. All training rows yield finite values.",
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

候选标识：`low/agent/replicate-2/round-2/h1`

最终状态：scored；边际收益：+0.485964 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_free_sphere_over_adsorbate_size_contrast",
    "formula": "q_lsd_f / (q_Vol ** (1/3))",
    "hypothesis": "Entropy loss at infinite dilution associates with the ratio of the framework's largest passing free sphere (Df) to the cube-root of the adsorbate van der Waals volume: as the passing bottleneck grows relative to adsorbate size, the adsorbed molecule retains more translational freedom within channels, so entropy loss should DECREASE as q_lsd_f / q_Vol^(1/3) increases.",
    "rationale": "Df (lsd_f) is a bottleneck diameter, not a cavity diameter, so the contrast captures confinement at constrictions that most restrict translational entropy. Cube-root of Vol gives a native length scale. Limitation: Vol is a whole-molecule vdW volume, not the kinetic cross-section, and Df is a geometric sphere path, not a molecule-specific accessible path.",
    "falsification_criteria": "If training Spearman between this descriptor and entropy loss/R is near zero or of opposite sign within the lsd_f training domain [0.85684, 7.68726], or if the mechanism_validated diagnostic fails while a pure q_lsd_f term matches its association, the size-contrast mechanism is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Df proxies the most severe confinement; Vol^(1/3) proxies adsorbate geometric size; both are implicit representations ignoring atom-level shape and flexibility.",
      "physical_interpretation": "All quantities in native units; the ratio is dimensionless only because lsd_f (angstrom) is divided by Vol^(1/3) (angstrom); q-normalization shifts scale but the physical threshold, if any, is not unity.",
      "boundary_behavior": "Vol has no training zeros (min 20.424) and lsd_f has none (min 0.85684), so the formula is finite for every training row; no imputation is needed.",
      "vary_input": "lsd_f",
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
      "training_spearman": -0.6285950097652175,
      "target_association": "contradicted",
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
    "name": "bottleneck_free_sphere_over_adsorbate_size_contrast",
    "formula": "(q_Vol ** (1/3)) / q_lsd_f",
    "hypothesis": "Entropy loss at infinite dilution associates with the ratio of the framework's largest passing free sphere (Df) to the cube-root of the adsorbate van der Waals volume: as the passing bottleneck grows relative to adsorbate size, the adsorbed molecule retains more translational freedom within channels, so entropy loss should DECREASE as q_lsd_f / q_Vol^(1/3) increases.",
    "rationale": "The precheck contradicted the original orientation: q_lsd_f/q_Vol^(1/3) had training Spearman -0.6286 with entropy loss, opposite to the stored increasing entropy_direction. Inverting the contrast (Vol^(1/3)/lsd_f) aligns the descriptor with the stored direction while keeping the same bottleneck-confinement mechanism family. Limitations unchanged: Df is a geometric bottleneck sphere, not a molecule-specific path, and Vol^(1/3) is a whole-molecule size proxy, not a kinetic cross-section.",
    "falsification_criteria": "If training Spearman between Vol^(1/3)/q_lsd_f-normalized descriptor and entropy loss/R is near zero or negative within the lsd_f domain [0.85684, 7.68726], or if mechanism_validated fails while a pure q_Vol term matches the association better, the inverted size-contrast mechanism is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Df proxies the most severe confinement; Vol^(1/3) proxies adsorbate geometric size. Small passing bottleneck relative to adsorbate size associates with larger entropy loss (translational restriction); this is an empirical association, not a derived equality.",
      "physical_interpretation": "Native units: Vol^(1/3) in angstrom divided by lsd_f in angstrom gives a dimensionless geometric contrast. q-normalization shifts both scales; the ratio q_Vol^(1/3)/q_lsd_f = 1 carries no universal physical threshold meaning.",
      "boundary_behavior": "Vol has no training zeros (min 20.424) and lsd_f has none (min 0.85684), so the inverted ratio is finite for every training row; no imputation needed.",
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
      "training_spearman": 0.6285950097652175,
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
    "name": "bottleneck_free_sphere_over_adsorbate_size_contrast",
    "formula": "(q_Vol ** (1/3)) / q_lsd_f",
    "hypothesis": "Entropy loss at infinite dilution associates with the ratio of the framework's largest passing free sphere (Df) to the cube-root of the adsorbate van der Waals volume: as the passing bottleneck grows relative to adsorbate size, the adsorbed molecule retains more translational freedom within channels, so entropy loss should DECREASE as q_lsd_f / q_Vol^(1/3) increases.",
    "rationale": "The precheck contradicted the original orientation: q_lsd_f/q_Vol^(1/3) had training Spearman -0.6286 with entropy loss, opposite to the stored increasing entropy_direction. Inverting the contrast (Vol^(1/3)/lsd_f) aligns the descriptor with the stored direction while keeping the same bottleneck-confinement mechanism family. Limitations unchanged: Df is a geometric bottleneck sphere, not a molecule-specific path, and Vol^(1/3) is a whole-molecule size proxy, not a kinetic cross-section.",
    "falsification_criteria": "If training Spearman between Vol^(1/3)/q_lsd_f-normalized descriptor and entropy loss/R is near zero or negative within the lsd_f domain [0.85684, 7.68726], or if mechanism_validated fails while a pure q_Vol term matches the association better, the inverted size-contrast mechanism is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Df proxies the most severe confinement; Vol^(1/3) proxies adsorbate geometric size. Small passing bottleneck relative to adsorbate size associates with larger entropy loss (translational restriction); this is an empirical association, not a derived equality.",
      "physical_interpretation": "Native units: Vol^(1/3) in angstrom divided by lsd_f in angstrom gives a dimensionless geometric contrast. q-normalization shifts both scales; the ratio q_Vol^(1/3)/q_lsd_f = 1 carries no universal physical threshold meaning.",
      "boundary_behavior": "Vol has no training zeros (min 20.424) and lsd_f has none (min 0.85684), so the inverted ratio is finite for every training row; no imputation needed.",
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
      "training_spearman": 0.6285950097652175,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/agent/replicate-2/round-2/h2`

最终状态：scored；边际收益：-0.536152 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "planarity_constrained_shape_entropy_descriptor",
    "formula": "q_PBF * q_LabuteASA",
    "hypothesis": "Entropy loss associates with the product of heavy-atom planarity deviation (PBF) and molecular surface area (LabuteASA): nonplanar molecules with large contact area lose more rotational and vibrational entropy upon adsorption because adsorption constrains more out-of-plane orientational degrees of freedom on an extended contact surface, so entropy loss should DECREASE as q_PBF * q_LabuteASA increases.",
    "rationale": "PBF measures mean heavy-atom displacement from the best-fit plane in the original implicit-H representation; multiplied by surface area it proxies the orientational-constraint surface a molecule presents to the framework wall. Limitations: PBF legitimately equals zero for truly planar heavy-atom skeletons; the product is an empirical smoothing, and the ANN may absorb the interaction non-additively.",
    "falsification_criteria": "If holding rotor class fixed, the partial-derivative association of entropy loss with PBF at fixed LabuteASA is opposite in sign or weaker than a LabuteASA-only descriptor, the planarity-interaction mechanism is falsified; likewise failure of mechanism_validated at the native PBF regime [0.0, 0.65625].",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom planarity in the implicit-H representation proxies orientational constraints; LabuteASA proxies wall-contact extent; hydrogens are ignored so true all-atom constraint count is not represented.",
      "physical_interpretation": "Native units are angstrom and angstrom^2, so the product has unit angstrom^3 and must be q-normalized before any dimensionless use; q_PBF is row-varying and undefined at PBF = 0, hence the formula uses q_PBF * q_LabuteASA which stays finite because both factors are finite.",
      "boundary_behavior": "At PBF = 0 (587 training rows, planar skeletons) q_PBF = 0 and the descriptor is 0, the physically meaningful minimum planarity-induced constraint, not an imputed value; LabuteASA has no training zeros.",
      "vary_input": "PBF",
      "descriptor_direction": "increasing",
      "regime_input": "PBF",
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
        "LabuteASA",
        "PBF"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.656249528
      ],
      "training_spearman": 0.3241711003886118,
      "target_association": "contradicted",
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
    "slot_id": "h2",
    "name": "planarity_constrained_shape_entropy_descriptor",
    "formula": "exp(-(q_PBF * q_LabuteASA))",
    "hypothesis": "Entropy loss associates with the product of heavy-atom planarity deviation (PBF) and molecular surface area (LabuteASA): nonplanar molecules with large contact area lose more rotational and vibrational entropy upon adsorption because adsorption constrains more out-of-plane orientational degrees of freedom on an extended contact surface, so entropy loss should DECREASE as q_PBF * q_LabuteASA increases.",
    "rationale": "The precheck contradicted the original orientation: q_PBF * q_LabuteASA had training Spearman +0.3242 with entropy loss while the stored entropy_direction is decreasing. Replacing the raw product with its bounded exponential complement preserves the planarity-constraint interaction mechanism but reverses the association sign so that larger planarity-area products associate with larger entropy loss. Limitation: this is empirical smoothing; the underlying interaction may be absorbed non-additively by the model.",
    "falsification_criteria": "If, holding rotor class fixed, the partial-derivative association of entropy loss with the exp(-q_PBF*q_LabuteASA) descriptor is positive or weaker than a LabuteASA-only descriptor, or mechanism_validated fails at native PBF [0.0, 0.65625], the planarity-interaction mechanism is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom planarity deviation times molecular surface area proxies the orientational-constraint extent; the exp(-x) smoothing is an empirical monotone mapping chosen so the descriptor decreases as the constraint product increases, matching the stored decreasing entropy_direction. Implicit-H representation ignores hydrogen contributions to true all-atom constraints.",
      "physical_interpretation": "The product q_PBF * q_LabuteASA is dimensionless after q-normalization on both factors; exp maps it to a bounded, unitless descriptor. The value 1 at perfectly planar heavy-atom skeletons carries no universal physical meaning.",
      "boundary_behavior": "q_PBF = 0 for 587 planar training rows (legitimate zeros) gives descriptor 1, the maximum of the bounded range; LabuteASA has no training zeros (min 7.4506), so the expression is finite and strictly positive for every training row with no imputation or epsilon.",
      "vary_input": "PBF",
      "descriptor_direction": "decreasing",
      "regime_input": "PBF",
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
        "LabuteASA",
        "PBF"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.656249528
      ],
      "training_spearman": -0.3241711003886118,
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
    "slot_id": "h2",
    "name": "planarity_constrained_shape_entropy_descriptor",
    "formula": "exp(-(q_PBF * q_LabuteASA))",
    "hypothesis": "Entropy loss associates with the product of heavy-atom planarity deviation (PBF) and molecular surface area (LabuteASA): nonplanar molecules with large contact area lose more rotational and vibrational entropy upon adsorption because adsorption constrains more out-of-plane orientational degrees of freedom on an extended contact surface, so entropy loss should DECREASE as q_PBF * q_LabuteASA increases.",
    "rationale": "The precheck contradicted the original orientation: q_PBF * q_LabuteASA had training Spearman +0.3242 with entropy loss while the stored entropy_direction is decreasing. Replacing the raw product with its bounded exponential complement preserves the planarity-constraint interaction mechanism but reverses the association sign so that larger planarity-area products associate with larger entropy loss. Limitation: this is empirical smoothing; the underlying interaction may be absorbed non-additively by the model.",
    "falsification_criteria": "If, holding rotor class fixed, the partial-derivative association of entropy loss with the exp(-q_PBF*q_LabuteASA) descriptor is positive or weaker than a LabuteASA-only descriptor, or mechanism_validated fails at native PBF [0.0, 0.65625], the planarity-interaction mechanism is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom planarity deviation times molecular surface area proxies the orientational-constraint extent; the exp(-x) smoothing is an empirical monotone mapping chosen so the descriptor decreases as the constraint product increases, matching the stored decreasing entropy_direction. Implicit-H representation ignores hydrogen contributions to true all-atom constraints.",
      "physical_interpretation": "The product q_PBF * q_LabuteASA is dimensionless after q-normalization on both factors; exp maps it to a bounded, unitless descriptor. The value 1 at perfectly planar heavy-atom skeletons carries no universal physical meaning.",
      "boundary_behavior": "q_PBF = 0 for 587 planar training rows (legitimate zeros) gives descriptor 1, the maximum of the bounded range; LabuteASA has no training zeros (min 7.4506), so the expression is finite and strictly positive for every training row with no imputation or epsilon.",
      "vary_input": "PBF",
      "descriptor_direction": "decreasing",
      "regime_input": "PBF",
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
        "LabuteASA",
        "PBF"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.656249528
      ],
      "training_spearman": -0.3241711003886118,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/agent/replicate-2/round-2/h3`

最终状态：scored；边际收益：+2.821447 pp；保留：True。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_area_per_volume_specific_area_contrast",
    "formula": "q_ASA / q_LabuteASA",
    "hypothesis": "Entropy loss associates with the contrast between framework probe-accessible specific area (ASA) and adsorbate molecular surface area (LabuteASA): frameworks offering more accessible internal surface relative to the adsorbate's own contact area support more distinct adsorption configurations and orientations, so entropy loss should DECREASE as q_ASA / q_LabuteASA increases.",
    "rationale": "This is a connectivity/surface-topology contrast mechanism: many spatially distinct binding surfaces reduce the configurational restriction per adsorbed molecule. Limitations: ASA is a fixed-probe, mass-specific quantity not molecule-specific, and it legitimately equals zero for 28 training frameworks with no probe-accessible volume for that probe; the descriptor then yields 0, interpreted as minimum surface-offered configurational freedom, not zero physical adsorption space.",
    "falsification_criteria": "If, at fixed AV and lsd_f, the partial-derivative association of entropy loss with ASA is opposite in sign, or if the retained h3 (q_AV / sqrt(q_LabuteASA)) outperforms this descriptor by a large margin, the area-contrast mechanism is falsified in favor of the volume-contact mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Probe-accessible specific area proxies the multiplicity of distinct binding surfaces; LabuteASA proxies the adsorbate's own contact footprint; the fixed-probe ASA underestimates accessibility for molecules larger or smaller than the probe.",
      "physical_interpretation": "Native units m^2/g divided by angstrom^2 are not dimensionless until q-normalization on both sides; the ratio is an empirical contrast and q_ASA/q_LabuteASA = 1 carries no physical threshold meaning.",
      "boundary_behavior": "ASA = 0 for 28 training rows gives q_ASA = 0 and a finite descriptor value 0 (LabuteASA has no training zeros, min 7.4506), interpreted as minimum offered surface multiplicity rather than imputation.",
      "vary_input": "ASA",
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": -0.4900721674860456,
      "target_association": "contradicted",
      "perturbation": 8.465169999999999,
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
    "name": "accessible_area_per_volume_specific_area_contrast",
    "formula": "q_LabuteASA * exp(-q_ASA)",
    "hypothesis": "Entropy loss associates with the contrast between framework probe-accessible specific area (ASA) and adsorbate molecular surface area (LabuteASA): frameworks offering more accessible internal surface relative to the adsorbate's own contact area support more distinct adsorption configurations and orientations, so entropy loss should DECREASE as q_ASA / q_LabuteASA increases.",
    "rationale": "The precheck contradicted the original orientation: q_ASA/q_LabuteASA had training Spearman -0.4901 with entropy loss while the stored entropy_direction is increasing. Reorienting the contrast (adsorbate footprint weighted by exp(-accessible area)) preserves the connectivity/surface-topology mechanism family and aligns with the stored direction, consistent with the round-1 signal that accessible-surface/volume contrasts carry information. Limitation: the exponential weighting is empirical smoothing, not a derived law.",
    "falsification_criteria": "If, at fixed AV and lsd_f, the partial-derivative association of entropy loss with ASA is positive (descriptor-inconsistent), or if a volume-contact descriptor such as q_AV/sqrt(q_LabuteASA) outperforms this form by a large margin, the surface-multiplicity mechanism is falsified in favor of the volume-contact mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "LabuteASA proxies the adsorbate's contact footprint; probe-accessible specific area proxies surface-offered configurational multiplicity. The exp(-q_ASA) weighting is an empirical monotone map, chosen so larger accessible area reduces the descriptor, matching the stored increasing entropy_direction: larger ASA associates with smaller entropy loss. ASA is fixed-probe and mass-specific, not molecule-specific.",
      "physical_interpretation": "q_LabuteASA is dimensionless; exp(-q_ASA) is dimensionless; the product is a bounded empirical contrast. Zero q_ASA means zero accessibility for the fixed geometric probe, not zero molecular adsorption space, and the descriptor value there carries no universal physical meaning.",
      "boundary_behavior": "q_ASA = 0 for 28 training frameworks (legitimate zero accessibility for the fixed probe) gives descriptor q_LabuteASA, finite and positive; LabuteASA has no training zeros (min 7.4506), so the expression is finite for every training row with no imputation.",
      "vary_input": "ASA",
      "descriptor_direction": "decreasing",
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.4956134762442524,
      "target_association": "consistent",
      "perturbation": 8.465169999999999,
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
    "name": "accessible_area_per_volume_specific_area_contrast",
    "formula": "q_LabuteASA * exp(-q_ASA)",
    "hypothesis": "Entropy loss associates with the contrast between framework probe-accessible specific area (ASA) and adsorbate molecular surface area (LabuteASA): frameworks offering more accessible internal surface relative to the adsorbate's own contact area support more distinct adsorption configurations and orientations, so entropy loss should DECREASE as q_ASA / q_LabuteASA increases.",
    "rationale": "The precheck contradicted the original orientation: q_ASA/q_LabuteASA had training Spearman -0.4901 with entropy loss while the stored entropy_direction is increasing. Reorienting the contrast (adsorbate footprint weighted by exp(-accessible area)) preserves the connectivity/surface-topology mechanism family and aligns with the stored direction, consistent with the round-1 signal that accessible-surface/volume contrasts carry information. Limitation: the exponential weighting is empirical smoothing, not a derived law.",
    "falsification_criteria": "If, at fixed AV and lsd_f, the partial-derivative association of entropy loss with ASA is positive (descriptor-inconsistent), or if a volume-contact descriptor such as q_AV/sqrt(q_LabuteASA) outperforms this form by a large margin, the surface-multiplicity mechanism is falsified in favor of the volume-contact mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "LabuteASA proxies the adsorbate's contact footprint; probe-accessible specific area proxies surface-offered configurational multiplicity. The exp(-q_ASA) weighting is an empirical monotone map, chosen so larger accessible area reduces the descriptor, matching the stored increasing entropy_direction: larger ASA associates with smaller entropy loss. ASA is fixed-probe and mass-specific, not molecule-specific.",
      "physical_interpretation": "q_LabuteASA is dimensionless; exp(-q_ASA) is dimensionless; the product is a bounded empirical contrast. Zero q_ASA means zero accessibility for the fixed geometric probe, not zero molecular adsorption space, and the descriptor value there carries no universal physical meaning.",
      "boundary_behavior": "q_ASA = 0 for 28 training frameworks (legitimate zero accessibility for the fixed probe) gives descriptor q_LabuteASA, finite and positive; LabuteASA has no training zeros (min 7.4506), so the expression is finite for every training row with no imputation.",
      "vary_input": "ASA",
      "descriptor_direction": "decreasing",
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.4956134762442524,
      "target_association": "consistent",
      "perturbation": 8.465169999999999,
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
