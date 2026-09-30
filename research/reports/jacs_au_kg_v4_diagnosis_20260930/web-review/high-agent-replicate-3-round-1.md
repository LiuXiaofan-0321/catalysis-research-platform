# high/agent/replicate-3/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`high/agent/replicate-3/round-1/h1`

最终状态：scored；边际收益：+3.999999 pp；保留：True。

复核改动字段：rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "translational_confinement_volume_contrast",
    "formula": "log10(q_Vol / maximum(q_AV, 0.01))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dominant translational entropy loss of an adsorbate scales with the ratio of its molecular van der Waals volume to the framework's probe-accessible specific pore volume: adsorbates with larger molecular volume confined in frameworks with smaller accessible volume lose more translational entropy (smaller s_ads/s_gas).",
    "rationale": "Translational confinement reduces the configurational volume available to the adsorbate relative to the gas phase; a volume contrast between molecule and accessible pore space is the simplest monotonically increasing proxy for that reduction. Limitations: AV is a fixed-probe, mass-specific geometric accessibility, not molecule-specific free volume; density units are unresolved; the maximum(q_AV, 0.01) floor is an empirical smoothing branch for the 28 training rows with zero fixed-probe accessibility (zero probe accessibility does not imply zero molecular adsorption space) and carries no universal physical meaning. Correlation of this proxy with entropy loss does not establish causality.",
    "falsification_criteria": "If measured or high-level-simulation entropy losses at infinite dilution fail to increase with q_Vol/q_AV within a family of frameworks of fixed ASA, or if frameworks with identical AV but different lsd_f/lsd_p connectivity show systematically different entropy losses not captured by this descriptor, the pure translational-volume mechanism is falsified and a connectivity-coupled mechanism must dominate.",
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
      "proxy_assumptions": "Van der Waals volume proxies the excluded configurational volume; fixed-probe AV proxies the accessible configurational volume. Both are transfer-limited: AV depends on the specific probe geometry, and Vol ignores framework-adapted conformations. The 0.01 floor on q_AV is an empirical numerical branch, not a physical threshold.",
      "physical_interpretation": "q_Vol compares adsorbate volume to the training-reference median (Vol_ref = 67.24 angstrom^3); q_AV compares fixed-probe accessible specific volume to its reference median (AV_ref). No q-value of 1 is interpreted as a physical equality or unity threshold.",
      "boundary_behavior": "Vol is strictly positive in training (q_Vol > 0 everywhere). AV = 0 rows (zero fixed-probe accessibility) are floored at q_AV = 0.01 by maximum(), yielding a large but finite descriptor; this is an admitted smoothing convention for an unresolvable geometry regime, not a physical claim about zero pore space.",
      "vary_input": "AV",
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
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "Vol": "molecular_vdw_volume"
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
    "name": "translational_confinement_volume_contrast",
    "formula": "log10(q_Vol / maximum(q_AV, 0.01))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dominant translational entropy loss of an adsorbate scales with the ratio of its molecular van der Waals volume to the framework's probe-accessible specific pore volume: adsorbates with larger molecular volume confined in frameworks with smaller accessible volume lose more translational entropy (smaller s_ads/s_gas).",
    "rationale": "Translational confinement reduces the configurational volume available to the adsorbate relative to the gas phase; a volume contrast between molecule and accessible pore space is the simplest monotonically increasing proxy for that reduction. Correction of the predeclared direction: the descriptor log10(q_Vol / maximum(q_AV, 0.01)) is INCREASING in q_Vol and DECREASING in q_AV (increasing accessible pore volume reduces confinement and hence entropy loss), so with vary_input = AV the descriptor direction is decreasing while entropy loss still increases with the descriptor (entropy_direction unchanged). Limitations: AV is a fixed-probe, mass-specific geometric accessibility, not molecule-specific free volume; density units are unresolved; the maximum(q_AV, 0.01) floor is an empirical smoothing branch for the 28 training rows with zero fixed-probe accessibility (zero probe accessibility does not imply zero molecular adsorption space) and carries no universal physical meaning. Correlation of this proxy with entropy loss does not establish causality.",
    "falsification_criteria": "If measured or high-level-simulation entropy losses at infinite dilution fail to increase with q_Vol/q_AV within a family of frameworks of fixed ASA, or if frameworks with identical AV but different lsd_f/lsd_p connectivity show systematically different entropy losses not captured by this descriptor, the pure translational-volume mechanism is falsified and a connectivity-coupled mechanism must dominate.",
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
      "proxy_assumptions": "Van der Waals volume proxies the excluded configurational volume; fixed-probe AV proxies the accessible configurational volume. Both are transfer-limited: AV depends on the specific probe geometry, and Vol ignores framework-adapted conformations. The 0.01 floor on q_AV is an empirical numerical branch, not a physical threshold.",
      "physical_interpretation": "q_Vol compares adsorbate volume to the training-reference median (Vol_ref = 67.24 angstrom^3); q_AV compares fixed-probe accessible specific volume to its reference median (AV_ref). No q-value of 1 is interpreted as a physical equality or unity threshold.",
      "boundary_behavior": "Vol is strictly positive in training (q_Vol > 0 everywhere), so the log10 argument is always positive and finite. AV = 0 rows (28 training rows with zero fixed-probe accessibility) are floored at q_AV = 0.01 by maximum(), yielding a large but finite descriptor; this is an admitted smoothing convention for an unresolvable geometry regime, not a physical claim about zero pore space.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6743096907523123,
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
    "name": "translational_confinement_volume_contrast",
    "formula": "log10(q_Vol / maximum(q_AV, 0.01))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dominant translational entropy loss of an adsorbate scales with the ratio of its molecular van der Waals volume to the framework's probe-accessible specific pore volume: adsorbates with larger molecular volume confined in frameworks with smaller accessible volume lose more translational entropy (smaller s_ads/s_gas).",
    "rationale": "Translational confinement reduces the configurational volume available to the adsorbate relative to the gas phase; a volume contrast between molecule and accessible pore space is the simplest monotonically increasing proxy for that reduction. Correction of the predeclared direction: the descriptor log10(q_Vol / maximum(q_AV, 0.01)) is INCREASING in q_Vol and DECREASING in q_AV (increasing accessible pore volume reduces confinement and hence entropy loss), so with vary_input = AV the descriptor direction is decreasing while entropy loss still increases with the descriptor (entropy_direction unchanged). Limitations: AV is a fixed-probe, mass-specific geometric accessibility, not molecule-specific free volume; density units are unresolved; the maximum(q_AV, 0.01) floor is an empirical smoothing branch for the 28 training rows with zero fixed-probe accessibility (zero probe accessibility does not imply zero molecular adsorption space) and carries no universal physical meaning. Correlation of this proxy with entropy loss does not establish causality.",
    "falsification_criteria": "If measured or high-level-simulation entropy losses at infinite dilution fail to increase with q_Vol/q_AV within a family of frameworks of fixed ASA, or if frameworks with identical AV but different lsd_f/lsd_p connectivity show systematically different entropy losses not captured by this descriptor, the pure translational-volume mechanism is falsified and a connectivity-coupled mechanism must dominate.",
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
      "proxy_assumptions": "Van der Waals volume proxies the excluded configurational volume; fixed-probe AV proxies the accessible configurational volume. Both are transfer-limited: AV depends on the specific probe geometry, and Vol ignores framework-adapted conformations. The 0.01 floor on q_AV is an empirical numerical branch, not a physical threshold.",
      "physical_interpretation": "q_Vol compares adsorbate volume to the training-reference median (Vol_ref = 67.24 angstrom^3); q_AV compares fixed-probe accessible specific volume to its reference median (AV_ref). No q-value of 1 is interpreted as a physical equality or unity threshold.",
      "boundary_behavior": "Vol is strictly positive in training (q_Vol > 0 everywhere), so the log10 argument is always positive and finite. AV = 0 rows (28 training rows with zero fixed-probe accessibility) are floored at q_AV = 0.01 by maximum(), yielding a large but finite descriptor; this is an admitted smoothing convention for an unresolvable geometry regime, not a physical claim about zero pore space.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6743096907523123,
      "target_association": "consistent",
      "perturbation": 0.001538232,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/agent/replicate-3/round-1/h2`

最终状态：scored；边际收益：-3.948980 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_inertia_anisotropy_loss",
    "formula": "rotor_case(0, log10(q_PMI3), log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3))",
    "hypothesis": "Rotational entropy loss upon adsorption at infinite dilution increases with the magnitude of the heavy-atom principal moment of inertia for linear adsorbates, and increases further with inertial anisotropy (excess of the largest over the middle principal moment) for nonlinear adsorbates; single-site adsorbates (single heavy atom in the representation) are treated as having no heavy-atom rotational descriptor and are assigned a zero anisotropy contribution.",
    "rationale": "Larger and more anisotropic rotors have a denser gas-phase rotational state spectrum and more orientation-dependent framework interactions, so adsorption plausibly removes more rotational entropy for them. Limitations: PMI1-3 are heavy-atom (implicit-H) inertia proxies, not true all-atom moments; methane is single-site and its zero PMIs are legitimate representation zeros, not physical zero inertia, hence the constant single-site branch. The anisotropy term is bounded in (-1, 1) by construction and is an empirical shape proxy, not a rigid-rotor partition-function calculation. Correlation does not validate causality.",
    "falsification_criteria": "If entropy loss for linear adsorbates is found to decrease (or be invariant) with q_PMI3 at fixed framework, or if nonlinear adsorbates with high anisotropy (PMI3 >> PMI2) show lower entropy loss than near-spherical nonlinear adsorbates of equal q_PMI3 in the same framework, the inertia-magnitude/anisotropy mechanism is falsified in favor of, e.g., a contact-geometry or free-rotation-retention mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMIs proxy rotational hindrance; the PMI3/PMI2 contrast proxies anisotropy of orientational restriction. This ignores hydrogen-atom inertia, framework-specific orientational potentials, and coupling between rotation and translation; transfer across chemistry is therefore limited.",
      "physical_interpretation": "q_PMI3 = PMI3 / PMI3_ref compares the largest heavy-atom principal moment to the training-reference median (125.4948325 angstrom^2*amu); the anisotropy fraction (PMI3 - PMI2)/(PMI1 + PMI2 + PMI3) is dimensionless. q_PMI3 = 1 is a reference normalization, not a physical unity threshold.",
      "boundary_behavior": "Single-site rows (54, e.g., methane) have legitimate zero PMIs and take the constant branch 0, finite by construction. Linear rows have PMI1 ~ 0 (legitimate) but PMI3 > 0, so the linear branch log10(q_PMI3) is finite and never divides by the zero moment. Nonlinear rows have strictly positive PMI1 + PMI2 + PMI3 (all near-zero PMI rows in training are single-site or linear), so the nonlinear branch is finite.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    },
    "physical_claims_original": [
      "nonlinear_rotor_expression",
      "rotor_case branches: single_site -> 0; linear -> log10(q_PMI3); nonlinear -> log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3)"
    ],
    "physical_claim_annotations": [
      "rotor_case branches: single_site -> 0; linear -> log10(q_PMI3); nonlinear -> log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3)"
    ]
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
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.38143143192086937,
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
    "name": "rotor_inertia_anisotropy_loss",
    "formula": "rotor_case(0, log10(q_PMI3), log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3))",
    "hypothesis": "Rotational entropy loss upon adsorption at infinite dilution increases with the magnitude of the heavy-atom principal moment of inertia for linear adsorbates, and increases further with inertial anisotropy (excess of the largest over the middle principal moment) for nonlinear adsorbates; single-site adsorbates (single heavy atom in the representation) are treated as having no heavy-atom rotational descriptor and are assigned a zero anisotropy contribution.",
    "rationale": "Larger and more anisotropic rotors have a denser gas-phase rotational state spectrum and more orientation-dependent framework interactions, so adsorption plausibly removes more rotational entropy for them. Limitations: PMI1-3 are heavy-atom (implicit-H) inertia proxies, not true all-atom moments; methane is single-site and its zero PMIs are legitimate representation zeros, not physical zero inertia, hence the constant single-site branch. The anisotropy term is bounded in (-1, 1) by construction and is an empirical shape proxy, not a rigid-rotor partition-function calculation. Correlation does not validate causality.",
    "falsification_criteria": "If entropy loss for linear adsorbates is found to decrease (or be invariant) with q_PMI3 at fixed framework, or if nonlinear adsorbates with high anisotropy (PMI3 >> PMI2) show lower entropy loss than near-spherical nonlinear adsorbates of equal q_PMI3 in the same framework, the inertia-magnitude/anisotropy mechanism is falsified in favor of, e.g., a contact-geometry or free-rotation-retention mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMIs proxy rotational hindrance; the PMI3/PMI2 contrast proxies anisotropy of orientational restriction. This ignores hydrogen-atom inertia, framework-specific orientational potentials, and coupling between rotation and translation; transfer across chemistry is therefore limited.",
      "physical_interpretation": "q_PMI3 = PMI3 / PMI3_ref compares the largest heavy-atom principal moment to the training-reference median (125.4948325 angstrom^2*amu); the anisotropy fraction (PMI3 - PMI2)/(PMI1 + PMI2 + PMI3) is dimensionless. q_PMI3 = 1 is a reference normalization, not a physical unity threshold.",
      "boundary_behavior": "Single-site rows (54, e.g., methane) have legitimate zero PMIs and take the constant branch 0, finite by construction. Linear rows have PMI1 ~ 0 (legitimate) but PMI3 > 0, so the linear branch log10(q_PMI3) is finite and never divides by the zero moment. Nonlinear rows have strictly positive PMI1 + PMI2 + PMI3 (all near-zero PMI rows in training are single-site or linear), so the nonlinear branch is finite.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    },
    "physical_claims_original": [
      "nonlinear_rotor_expression",
      "rotor_case branches: single_site -> 0; linear -> log10(q_PMI3); nonlinear -> log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3)"
    ],
    "physical_claim_annotations": [
      "rotor_case branches: single_site -> 0; linear -> log10(q_PMI3); nonlinear -> log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3)"
    ]
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
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.38143143192086937,
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
    "name": "rotor_inertia_anisotropy_loss",
    "formula": "rotor_case(0, log10(q_PMI3), log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3))",
    "hypothesis": "Rotational entropy loss upon adsorption at infinite dilution increases with the magnitude of the heavy-atom principal moment of inertia for linear adsorbates, and increases further with inertial anisotropy (excess of the largest over the middle principal moment) for nonlinear adsorbates; single-site adsorbates (single heavy atom in the representation) are treated as having no heavy-atom rotational descriptor and are assigned a zero anisotropy contribution.",
    "rationale": "Larger and more anisotropic rotors have a denser gas-phase rotational state spectrum and more orientation-dependent framework interactions, so adsorption plausibly removes more rotational entropy for them. Limitations: PMI1-3 are heavy-atom (implicit-H) inertia proxies, not true all-atom moments; methane is single-site and its zero PMIs are legitimate representation zeros, not physical zero inertia, hence the constant single-site branch. The anisotropy term is bounded in (-1, 1) by construction and is an empirical shape proxy, not a rigid-rotor partition-function calculation. Correlation does not validate causality.",
    "falsification_criteria": "If entropy loss for linear adsorbates is found to decrease (or be invariant) with q_PMI3 at fixed framework, or if nonlinear adsorbates with high anisotropy (PMI3 >> PMI2) show lower entropy loss than near-spherical nonlinear adsorbates of equal q_PMI3 in the same framework, the inertia-magnitude/anisotropy mechanism is falsified in favor of, e.g., a contact-geometry or free-rotation-retention mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMIs proxy rotational hindrance; the PMI3/PMI2 contrast proxies anisotropy of orientational restriction. This ignores hydrogen-atom inertia, framework-specific orientational potentials, and coupling between rotation and translation; transfer across chemistry is therefore limited.",
      "physical_interpretation": "q_PMI3 = PMI3 / PMI3_ref compares the largest heavy-atom principal moment to the training-reference median (125.4948325 angstrom^2*amu); the anisotropy fraction (PMI3 - PMI2)/(PMI1 + PMI2 + PMI3) is dimensionless. q_PMI3 = 1 is a reference normalization, not a physical unity threshold.",
      "boundary_behavior": "Single-site rows (54, e.g., methane) have legitimate zero PMIs and take the constant branch 0, finite by construction. Linear rows have PMI1 ~ 0 (legitimate) but PMI3 > 0, so the linear branch log10(q_PMI3) is finite and never divides by the zero moment. Nonlinear rows have strictly positive PMI1 + PMI2 + PMI3 (all near-zero PMI rows in training are single-site or linear), so the nonlinear branch is finite.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    },
    "physical_claims_original": [
      "nonlinear_rotor_expression",
      "rotor_case branches: single_site -> 0; linear -> log10(q_PMI3); nonlinear -> log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3)"
    ],
    "physical_claim_annotations": [
      "rotor_case branches: single_site -> 0; linear -> log10(q_PMI3); nonlinear -> log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3)"
    ]
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
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.38143143192086937,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/agent/replicate-3/round-1/h3`

最终状态：scored；边际收益：-0.613093 pp；保留：False。

复核改动字段：rationale, scientific_test.descriptor_direction

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "bottleneck_span_contact_contrast",
    "formula": "(q_SPAN * q_LabuteASA) / q_lsd_f ** 1",
    "hypothesis": "Entropy loss at infinite dilution increases with the geometric contrast between an adsorbate's extension/contact area and the framework's transport bottleneck: adsorbates with larger heavy-atom enclosing span and larger molecular surface area relative to the largest free passing sphere (Df) experience stronger steric and contact restriction, hence larger entropy loss (smaller s_ads/s_gas).",
    "rationale": "A molecule whose spatial extension and contact surface are large relative to the periodic free-path bottleneck has fewer compatible positions and orientations in the framework, reducing configurational entropy. Limitations: lsd_f is the bottleneck free sphere Df, not the global cavity diameter Di and not the included sphere Dif; SPAN, GeDi-class and LabuteASA are heavy-atom/implicit-H geometric proxies; SPAN = 0 for single-site adsorbates is a legitimate representation zero driving the descriptor to 0, which is an admitted branch limit (not a claim of zero physical entropy loss). Correlation with entropy loss does not establish causality, and kinetic escape through the bottleneck does not by itself determine equilibrium entropy.",
    "falsification_criteria": "If entropy loss at infinite dilution is invariant to q_SPAN*q_LabuteASA/q_lsd_f across frameworks with matched AV (i.e., bottleneck contrast matters only for transport, not equilibrium), or if frameworks with large Di but small Df show entropy losses opposite to the predicted direction, the bottleneck-contrast hypothesis is falsified in favor of a cavity-volume (Di-like) mechanism not represented here.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "LabuteASA": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "SPAN proxies molecular extension; LabuteASA proxies potential framework contact area; lsd_f (Df) proxies the connectivity constraint of the periodic free path. All are fixed-representation geometric proxies: hydrogen atoms are implicit, Df is a bottleneck not a cavity size, and probe-independent molecular flexibility is ignored.",
      "physical_interpretation": "q_SPAN, q_LabuteASA and q_lsd_f compare each native quantity to its training-reference median (SPAN_ref = 1.860601424 angstrom, LabuteASA_ref = 31.85047501 angstrom^2, lsd_f_ref = 5.16326 angstrom); q = 1 is a normalization reference, not a physical passage threshold. The descriptor is dimensionless.",
      "boundary_behavior": "lsd_f and LabuteASA are strictly positive in training, so the denominator and multiplicative surface factor are always finite and nonzero. SPAN = 0 for the 54 single-site rows is a legitimate zero: the descriptor evaluates exactly to 0 (finite), interpreted honestly as absence of a heavy-atom enclosing-radius signal rather than zero entropy loss.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "SPAN",
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
        "LabuteASA",
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "SPAN": "heavy_atom_enclosing_radius",
        "lsd_f": "bottleneck_free_sphere_Df"
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
    "slot_id": "h3",
    "name": "bottleneck_span_contact_contrast",
    "formula": "(q_SPAN * q_LabuteASA) / q_lsd_f ** 1",
    "hypothesis": "Entropy loss at infinite dilution increases with the geometric contrast between an adsorbate's extension/contact area and the framework's transport bottleneck: adsorbates with larger heavy-atom enclosing span and larger molecular surface area relative to the largest free passing sphere (Df) experience stronger steric and contact restriction, hence larger entropy loss (smaller s_ads/s_gas).",
    "rationale": "A molecule whose spatial extension and contact surface are large relative to the periodic free-path bottleneck has fewer compatible positions and orientations in the framework, reducing configurational entropy. Correction of the predeclared direction: the descriptor (q_SPAN * q_LabuteASA) / q_lsd_f is DECREASING in q_lsd_f (a larger passing bottleneck Df relaxes the steric/contact restriction and reduces entropy loss) and increasing in q_SPAN and q_LabuteASA; with vary_input = lsd_f the descriptor direction is decreasing while entropy loss still increases with the descriptor (entropy_direction unchanged). Limitations: lsd_f is the bottleneck free sphere Df, not the global cavity diameter Di and not the included sphere Dif; SPAN and LabuteASA are heavy-atom/implicit-H geometric proxies; SPAN = 0 for single-site adsorbates is a legitimate representation zero driving the descriptor to 0, which is an admitted branch limit (not a claim of zero physical entropy loss). Correlation with entropy loss does not establish causality, and kinetic escape through the bottleneck does not by itself determine equilibrium entropy.",
    "falsification_criteria": "If entropy loss at infinite dilution is invariant to q_SPAN*q_LabuteASA/q_lsd_f across frameworks with matched AV (i.e., bottleneck contrast matters only for transport, not equilibrium), or if frameworks with large Di but small Df show entropy losses opposite to the predicted direction, the bottleneck-contrast hypothesis is falsified in favor of a cavity-volume (Di-like) mechanism not represented here.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "LabuteASA": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "SPAN proxies molecular extension; LabuteASA proxies potential framework contact area; lsd_f (Df) proxies the connectivity constraint of the periodic free path. All are fixed-representation geometric proxies: hydrogen atoms are implicit, Df is a bottleneck not a cavity size, and probe-independent molecular flexibility is ignored.",
      "physical_interpretation": "q_SPAN, q_LabuteASA and q_lsd_f compare each native quantity to its training-reference median (SPAN_ref = 1.860601424 angstrom, LabuteASA_ref = 31.85047501 angstrom^2, lsd_f_ref = 5.16326 angstrom); q = 1 is a normalization reference, not a physical passage threshold. The descriptor is dimensionless.",
      "boundary_behavior": "lsd_f and LabuteASA are strictly positive in training, so the denominator and multiplicative surface factor are always finite and nonzero. SPAN = 0 for the 54 single-site rows is a legitimate zero: the descriptor evaluates exactly to 0 (finite), interpreted honestly as absence of a heavy-atom enclosing-radius signal rather than zero entropy loss.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
      "regime_input": "SPAN",
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
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "SPAN": "heavy_atom_enclosing_radius",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        6.24082991
      ],
      "training_spearman": 0.5405609819373928,
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
    "slot_id": "h3",
    "name": "bottleneck_span_contact_contrast",
    "formula": "(q_SPAN * q_LabuteASA) / q_lsd_f ** 1",
    "hypothesis": "Entropy loss at infinite dilution increases with the geometric contrast between an adsorbate's extension/contact area and the framework's transport bottleneck: adsorbates with larger heavy-atom enclosing span and larger molecular surface area relative to the largest free passing sphere (Df) experience stronger steric and contact restriction, hence larger entropy loss (smaller s_ads/s_gas).",
    "rationale": "A molecule whose spatial extension and contact surface are large relative to the periodic free-path bottleneck has fewer compatible positions and orientations in the framework, reducing configurational entropy. Correction of the predeclared direction: the descriptor (q_SPAN * q_LabuteASA) / q_lsd_f is DECREASING in q_lsd_f (a larger passing bottleneck Df relaxes the steric/contact restriction and reduces entropy loss) and increasing in q_SPAN and q_LabuteASA; with vary_input = lsd_f the descriptor direction is decreasing while entropy loss still increases with the descriptor (entropy_direction unchanged). Limitations: lsd_f is the bottleneck free sphere Df, not the global cavity diameter Di and not the included sphere Dif; SPAN and LabuteASA are heavy-atom/implicit-H geometric proxies; SPAN = 0 for single-site adsorbates is a legitimate representation zero driving the descriptor to 0, which is an admitted branch limit (not a claim of zero physical entropy loss). Correlation with entropy loss does not establish causality, and kinetic escape through the bottleneck does not by itself determine equilibrium entropy.",
    "falsification_criteria": "If entropy loss at infinite dilution is invariant to q_SPAN*q_LabuteASA/q_lsd_f across frameworks with matched AV (i.e., bottleneck contrast matters only for transport, not equilibrium), or if frameworks with large Di but small Df show entropy losses opposite to the predicted direction, the bottleneck-contrast hypothesis is falsified in favor of a cavity-volume (Di-like) mechanism not represented here.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "LabuteASA": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "SPAN proxies molecular extension; LabuteASA proxies potential framework contact area; lsd_f (Df) proxies the connectivity constraint of the periodic free path. All are fixed-representation geometric proxies: hydrogen atoms are implicit, Df is a bottleneck not a cavity size, and probe-independent molecular flexibility is ignored.",
      "physical_interpretation": "q_SPAN, q_LabuteASA and q_lsd_f compare each native quantity to its training-reference median (SPAN_ref = 1.860601424 angstrom, LabuteASA_ref = 31.85047501 angstrom^2, lsd_f_ref = 5.16326 angstrom); q = 1 is a normalization reference, not a physical passage threshold. The descriptor is dimensionless.",
      "boundary_behavior": "lsd_f and LabuteASA are strictly positive in training, so the denominator and multiplicative surface factor are always finite and nonzero. SPAN = 0 for the 54 single-site rows is a legitimate zero: the descriptor evaluates exactly to 0 (finite), interpreted honestly as absence of a heavy-atom enclosing-radius signal rather than zero entropy loss.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
      "regime_input": "SPAN",
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
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "SPAN": "heavy_atom_enclosing_radius",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        6.24082991
      ],
      "training_spearman": 0.5405609819373928,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
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
