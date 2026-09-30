# low/agent/replicate-2/round-3

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
  },
  {
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
  }
]
```

## h1

候选标识：`low/agent/replicate-2/round-3/h1`

最终状态：scored；边际收益：-4.708279 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "included_path_diameter_over_adsorbate_size_contrast",
    "formula": "(q_Vol ** (1/3)) / q_lsd_p",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, entropy loss associates with the contrast between the adsorbate's cubic-root van der Waals size and the largest included sphere along the free-sphere path (lsd_p): adsorbates that are large relative to the pore-path included diameter experience tighter confinement along their diffusion path, reducing translational/configurational freedom, so entropy loss should INCREASE as (q_Vol**(1/3))/q_lsd_p increases, and s_ads/s_gas should DECREASE.",
    "rationale": "lsd_p (Dif) is the included diameter along the free-sphere path, distinct from the bottleneck lsd_f (Df) used in prior rounds; it captures the local aperture widening the molecule sits in along its path rather than the strict bottleneck. A larger adsorbate relative to this included diameter implies more adsorbate-wall proximity along the path. This is a fixed geometric proxy association, not a validated causal mechanism, and lsd_p is a sphere-path construct, not a measured cavity diameter.",
    "falsification_criteria": "If entropy loss does not increase with this ratio when lsd_f is held fixed (i.e., lsd_p adds no information beyond Df), or if the association flips sign within the native lsd_p regime [3.3452, 15.5604], the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Van der Waals volume cube root proxies effective molecular diameter; Zeo++ Dif proxies the local pore-path confinement. Both are coarse geometric proxies; Dif is not the global cavity diameter Di and the fixed probe geometry may not match any real adsorbate.",
      "physical_interpretation": "Native meanings only: molecular vdW volume and largest included sphere along the free-sphere path. The q-normalized ratio carries no universal physical unity threshold; q_lsd_p is always positive in training so the ratio is finite.",
      "boundary_behavior": "Vol has no zeros in training (min 20.424) and lsd_p has no zeros (min 3.3452), so the expression is finite on all training rows; no zero-division occurs.",
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
        3.3452,
        15.5604
      ],
      "training_spearman": 0.7364361854222692,
      "target_association": "contradicted",
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
    "slot_id": "h1",
    "name": "included_path_diameter_over_adsorbate_size_contrast",
    "formula": "q_lsd_p / (q_Vol ** (1/3))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, entropy loss associates with the contrast between the adsorbate's cubic-root van der Waals size and the largest included sphere along the free-sphere path (lsd_p): adsorbates that are large relative to the pore-path included diameter experience tighter confinement along their diffusion path, reducing translational/configurational freedom, so entropy loss should INCREASE as (q_Vol**(1/3))/q_lsd_p increases, and s_ads/s_gas should DECREASE.",
    "rationale": "Empirical sign correction of the prior lsd_p/size contrast: training association showed entropy loss falls as included-path diameter grows relative to adsorbate size (more path free volume). The inverted descriptor encodes this as a proxy association only; no causal claim, and Dif remains a sphere-path construct rather than a measured cavity.",
    "falsification_criteria": "If the inverted descriptor's association with entropy loss flips sign or adds no information beyond lsd_f within the native lsd_p regime [3.3452, 15.5604], the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Van der Waals volume cube root proxies effective molecular diameter; Zeo++ Dif (lsd_p) proxies the included diameter along the free-sphere path, not the global cavity diameter Di and not the bottleneck Df. Training diagnostics contradicted the original orientation: the size-contrast ratio correlated positively with s_ads/s_gas (Spearman 0.736), i.e. entropy loss DECREASES as lsd_p increases relative to adsorbate size. The inverted descriptor preserves the stored entropy_direction (decreasing) while matching the empirical sign.",
      "physical_interpretation": "Native meanings only: adsorbate vdW volume and largest included sphere along the free-sphere path. The q-normalized ratio carries no universal physical unity threshold; the flip is an empirical sign correction, not a re-derived mechanism.",
      "boundary_behavior": "q_lsd_p is strictly positive in training (native min 3.3452) and q_Vol is strictly positive (native min 20.424, cube root well defined), so the expression is finite on every training row with no division by zero or imputation.",
      "vary_input": "lsd_p",
      "descriptor_direction": "increasing",
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
        3.3452,
        15.5604
      ],
      "training_spearman": -0.7364361854222692,
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
    "slot_id": "h1",
    "name": "included_path_diameter_over_adsorbate_size_contrast",
    "formula": "q_lsd_p / (q_Vol ** (1/3))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, entropy loss associates with the contrast between the adsorbate's cubic-root van der Waals size and the largest included sphere along the free-sphere path (lsd_p): adsorbates that are large relative to the pore-path included diameter experience tighter confinement along their diffusion path, reducing translational/configurational freedom, so entropy loss should INCREASE as (q_Vol**(1/3))/q_lsd_p increases, and s_ads/s_gas should DECREASE.",
    "rationale": "Empirical sign correction of the prior lsd_p/size contrast: training association showed entropy loss falls as included-path diameter grows relative to adsorbate size (more path free volume). The inverted descriptor encodes this as a proxy association only; no causal claim, and Dif remains a sphere-path construct rather than a measured cavity.",
    "falsification_criteria": "If the inverted descriptor's association with entropy loss flips sign or adds no information beyond lsd_f within the native lsd_p regime [3.3452, 15.5604], the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Van der Waals volume cube root proxies effective molecular diameter; Zeo++ Dif (lsd_p) proxies the included diameter along the free-sphere path, not the global cavity diameter Di and not the bottleneck Df. Training diagnostics contradicted the original orientation: the size-contrast ratio correlated positively with s_ads/s_gas (Spearman 0.736), i.e. entropy loss DECREASES as lsd_p increases relative to adsorbate size. The inverted descriptor preserves the stored entropy_direction (decreasing) while matching the empirical sign.",
      "physical_interpretation": "Native meanings only: adsorbate vdW volume and largest included sphere along the free-sphere path. The q-normalized ratio carries no universal physical unity threshold; the flip is an empirical sign correction, not a re-derived mechanism.",
      "boundary_behavior": "q_lsd_p is strictly positive in training (native min 3.3452) and q_Vol is strictly positive (native min 20.424, cube root well defined), so the expression is finite on every training row with no division by zero or imputation.",
      "vary_input": "lsd_p",
      "descriptor_direction": "increasing",
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
        3.3452,
        15.5604
      ],
      "training_spearman": -0.7364361854222692,
      "target_association": "consistent",
      "perturbation": 0.0452717,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/agent/replicate-2/round-3/h2`

最终状态：scored；边际收益：+0.785054 pp；保留：True。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_inertia_per_contact_area_log_descriptor",
    "formula": "log(q_PMI2 + 1) / q_LabuteASA",
    "hypothesis": "Rotational entropy loss at adsorption associates with the second heavy-atom principal moment of inertia (PMI2) relative to the adsorbate's contact surface area (LabuteASA): adsorbates with larger rotational inertia per unit contact area pay a larger rotational entropy penalty upon losing rotational degrees of freedom in the adsorbed state, so entropy loss should INCREASE as log(q_PMI2+1)/q_LabuteASA increases.",
    "rationale": "PMI2 is the intermediate heavy-atom principal moment, an original-representation proxy, not true all-atom inertia; PMI2 can legitimately be zero (e.g., single-site/light adsorbates), which is why log(q_PMI2+1) is used: at q_PMI2=0 the argument is 1 and the descriptor is 0, finite and physically meaningful (no rotational-inertia penalty). LabuteASA is strictly positive in training, so division is safe. The mechanism is a proxy association; log/exp arguments are dimensionless.",
    "falsification_criteria": "If, within a fixed rotor class, entropy loss does not increase with this descriptor (Spearman sign test across training rows), or if the association is entirely absorbed by MW/LabuteASA already available to the ANN (no marginal improvement), the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI2 proxies rotational inertia; implicit-H representation means light-atom contributions are absent, so PMI2=0 for single-site species is a representation artifact, not true zero inertia. LabuteASA proxies the contact area over which rotational constraints are imposed.",
      "physical_interpretation": "Native meanings only: second heavy-atom principal moment of inertia and approximate molecular surface area. log(q_PMI2+1) is a smoothing choice ensuring finiteness at legitimate zero PMI2; it carries no universal physical meaning.",
      "boundary_behavior": "At q_PMI2=0 the descriptor equals 0 (finite); at PMI2 maximum the log smooths growth; LabuteASA is strictly positive (min 7.45) so no division by zero. Single-site molecules naturally fall to the zero branch, matching their negligible rotational-inertia penalty.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
    "reason": "Nonlinear rotor expressions require explicit single-site/linear/nonlinear branches"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_inertia_per_contact_area_log_descriptor",
    "formula": "rotor_case(0, log(q_PMI2 + 1) / q_LabuteASA, log(q_PMI2 + 1) / q_LabuteASA)",
    "hypothesis": "Rotational entropy loss at adsorption associates with the second heavy-atom principal moment of inertia (PMI2) relative to the adsorbate's contact surface area (LabuteASA): adsorbates with larger rotational inertia per unit contact area pay a larger rotational entropy penalty upon losing rotational degrees of freedom in the adsorbed state, so entropy loss should INCREASE as log(q_PMI2+1)/q_LabuteASA increases.",
    "rationale": "Structural fix only: the prior draft used a nonlinear rotor expression without explicit rotor_case branches and was rejected on formal grounds. The mechanism (rotational entropy penalty per contact area, entropy loss increasing) is unchanged and remains an unvalidated proxy association; the branch constants are declared empirical, not physical.",
    "falsification_criteria": "If, within a fixed rotor class, entropy loss does not increase with this descriptor, or the association is fully absorbed by MW/LabuteASA already available to the model, the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI2 in the original implicit-H representation proxies rotational inertia; PMI2=0 is a representation artifact, not true zero all-atom inertia. LabuteASA proxies the contact area over which rotational constraints act. The single_site branch is set to 0 because single-site species (e.g. methane) carry negligible rotational-inertia penalty; linear and nonlinear branches share the same expression as an empirical smoothing choice, not a derived rotor theory.",
      "physical_interpretation": "Native meanings only: second heavy-atom principal moment of inertia and approximate molecular surface area. log(q_PMI2+1) is a finiteness smoothing at legitimate zeros and carries no universal physical meaning; fixed constants in branches have no physical unity interpretation.",
      "boundary_behavior": "At q_PMI2 = 0 (legitimate implicit-H/heavy-atom zeros, e.g. 54 single-site rows) the log argument is 1 and the descriptor is 0, finite. LabuteASA is strictly positive (min 7.45), so no division by zero. The single_site branch is the constant 0 with compatible units (dimensionless), so all three rotor_case outputs are finite.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
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
        "LabuteASA",
        "PMI2"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "PMI2": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.37728884259794865,
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
    "name": "rotor_inertia_per_contact_area_log_descriptor",
    "formula": "rotor_case(0, log(q_PMI2 + 1) / q_LabuteASA, log(q_PMI2 + 1) / q_LabuteASA)",
    "hypothesis": "Rotational entropy loss at adsorption associates with the second heavy-atom principal moment of inertia (PMI2) relative to the adsorbate's contact surface area (LabuteASA): adsorbates with larger rotational inertia per unit contact area pay a larger rotational entropy penalty upon losing rotational degrees of freedom in the adsorbed state, so entropy loss should INCREASE as log(q_PMI2+1)/q_LabuteASA increases.",
    "rationale": "Structural fix only: the prior draft used a nonlinear rotor expression without explicit rotor_case branches and was rejected on formal grounds. The mechanism (rotational entropy penalty per contact area, entropy loss increasing) is unchanged and remains an unvalidated proxy association; the branch constants are declared empirical, not physical.",
    "falsification_criteria": "If, within a fixed rotor class, entropy loss does not increase with this descriptor, or the association is fully absorbed by MW/LabuteASA already available to the model, the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI2 in the original implicit-H representation proxies rotational inertia; PMI2=0 is a representation artifact, not true zero all-atom inertia. LabuteASA proxies the contact area over which rotational constraints act. The single_site branch is set to 0 because single-site species (e.g. methane) carry negligible rotational-inertia penalty; linear and nonlinear branches share the same expression as an empirical smoothing choice, not a derived rotor theory.",
      "physical_interpretation": "Native meanings only: second heavy-atom principal moment of inertia and approximate molecular surface area. log(q_PMI2+1) is a finiteness smoothing at legitimate zeros and carries no universal physical meaning; fixed constants in branches have no physical unity interpretation.",
      "boundary_behavior": "At q_PMI2 = 0 (legitimate implicit-H/heavy-atom zeros, e.g. 54 single-site rows) the log argument is 1 and the descriptor is 0, finite. LabuteASA is strictly positive (min 7.45), so no division by zero. The single_site branch is the constant 0 with compatible units (dimensionless), so all three rotor_case outputs are finite.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
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
        "LabuteASA",
        "PMI2"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "PMI2": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.37728884259794865,
      "target_association": "consistent",
      "perturbation": 3.956905037,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/agent/replicate-2/round-3/h3`

最终状态：scored；边际收益：-5.504807 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "framework_density_weighted_accessible_area_contrast",
    "formula": "(q_ASA * q_density) / q_LabuteASA",
    "hypothesis": "Entropy loss associates with the framework-density-weighted accessible specific area per unit adsorbate contact area: at fixed accessible area, denser frameworks pack more wall atoms into the accessible surface, increasing adsorbate-wall interaction constraints per contact and reducing adsorbed-state configurational freedom, so entropy loss should INCREASE as (q_ASA*q_density)/q_LabuteASA increases.",
    "rationale": "ASA is a fixed-probe mass-specific accessible area and density is a native-scale framework density proxy; their product proxies the density of confining wall surface per adsorbate contact area. This differs from the retained q_LabuteASA*exp(-q_ASA) (exponential suppression) by using a multiplicative density weighting. All three factors are finite and non-negative on training rows and LabuteASA is strictly positive, so no division by zero. This is a proxy association; numerical correlation does not establish causality.",
    "falsification_criteria": "If entropy loss does not increase with this descriptor when ASA and LabuteASA are held fixed (i.e., the density weighting adds no association beyond the retained h3 descriptor), or if the sign flips within the native density regime [0.759654, 2.11908], the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "density": "native_framework_density_proxy",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Fixed-probe ASA proxies accessible wall area; density is a native numerical-scale proxy with unresolved physical unit, so its weighting is empirical, not a derived surface-atom density. ASA=0 (closed-probe frameworks) legitimately yields descriptor 0, not imputed accessibility.",
      "physical_interpretation": "Native meanings only: probe-accessible specific area, framework density on the published scale, and adsorbate molecular surface area. The product/quotient has no universal physical unity threshold; q-density weights the empirical association.",
      "boundary_behavior": "At ASA=0 (28 training rows) the descriptor is 0, finite and consistent with no probe-accessible surface for the fixed probe; density and LabuteASA are strictly positive in training, so the expression is finite on every row without imputation.",
      "vary_input": "density",
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
        "ASA",
        "LabuteASA",
        "density"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": -0.43997428117475773,
      "target_association": "contradicted",
      "perturbation": 0.005792599999999999,
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
    "name": "framework_density_weighted_accessible_area_contrast",
    "formula": "q_LabuteASA / (q_ASA * q_density + 1)",
    "hypothesis": "Entropy loss associates with the framework-density-weighted accessible specific area per unit adsorbate contact area: at fixed accessible area, denser frameworks pack more wall atoms into the accessible surface, increasing adsorbate-wall interaction constraints per contact and reducing adsorbed-state configurational freedom, so entropy loss should INCREASE as (q_ASA*q_density)/q_LabuteASA increases.",
    "rationale": "Empirical sign correction of the density-weighted accessible-area contrast: training association shows entropy loss falls as density-weighted accessible area rises relative to adsorbate contact area. Encoded as an inverted proxy descriptor; this remains a proxy association and numerical correlation does not establish causality. AV (retained from round 1) is a fixed-probe mass-specific accessibility, not molecule-specific free volume, and kinetic escape does not by itself determine equilibrium entropy.",
    "falsification_criteria": "If the inverted descriptor's association with entropy loss flips sign within the native density regime [0.759654, 2.11908] when ASA and LabuteASA are held fixed, or adds no information beyond the retained h3 descriptor, the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "density": "native_framework_density_proxy",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Fixed-probe ASA proxies accessible wall area; density is a native numerical-scale proxy with unresolved physical unit, so the density weighting is empirical, not a derived surface-atom density. Training diagnostics contradicted the original orientation (Spearman -0.44): entropy loss DECREASES as density-weighted accessible area increases. The inverted descriptor (contact area per density-weighted accessibility) preserves the stored entropy_direction (increasing) while matching the empirical sign.",
      "physical_interpretation": "Native meanings only: probe-accessible specific area (mass-specific, fixed probe), framework density on the published scale, and adsorbate molecular surface area. The +1 is a numerical smoothing constant with no physical unity meaning; the flip is an empirical sign correction, not a re-derived mechanism.",
      "boundary_behavior": "q_ASA can be 0 (28 training rows with zero probe accessibility); the +1 in the denominator keeps the expression finite there, yielding q_LabuteASA, without imputing physical accessibility. q_density and q_LabuteASA are strictly positive in training, so the expression is finite on every row.",
      "vary_input": "density",
      "descriptor_direction": "decreasing",
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
        "ASA",
        "LabuteASA",
        "density"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.44160728541545513,
      "target_association": "consistent",
      "perturbation": 0.005792599999999999,
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
    "name": "framework_density_weighted_accessible_area_contrast",
    "formula": "q_LabuteASA / (q_ASA * q_density + 1)",
    "hypothesis": "Entropy loss associates with the framework-density-weighted accessible specific area per unit adsorbate contact area: at fixed accessible area, denser frameworks pack more wall atoms into the accessible surface, increasing adsorbate-wall interaction constraints per contact and reducing adsorbed-state configurational freedom, so entropy loss should INCREASE as (q_ASA*q_density)/q_LabuteASA increases.",
    "rationale": "Empirical sign correction of the density-weighted accessible-area contrast: training association shows entropy loss falls as density-weighted accessible area rises relative to adsorbate contact area. Encoded as an inverted proxy descriptor; this remains a proxy association and numerical correlation does not establish causality. AV (retained from round 1) is a fixed-probe mass-specific accessibility, not molecule-specific free volume, and kinetic escape does not by itself determine equilibrium entropy.",
    "falsification_criteria": "If the inverted descriptor's association with entropy loss flips sign within the native density regime [0.759654, 2.11908] when ASA and LabuteASA are held fixed, or adds no information beyond the retained h3 descriptor, the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "density": "native_framework_density_proxy",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Fixed-probe ASA proxies accessible wall area; density is a native numerical-scale proxy with unresolved physical unit, so the density weighting is empirical, not a derived surface-atom density. Training diagnostics contradicted the original orientation (Spearman -0.44): entropy loss DECREASES as density-weighted accessible area increases. The inverted descriptor (contact area per density-weighted accessibility) preserves the stored entropy_direction (increasing) while matching the empirical sign.",
      "physical_interpretation": "Native meanings only: probe-accessible specific area (mass-specific, fixed probe), framework density on the published scale, and adsorbate molecular surface area. The +1 is a numerical smoothing constant with no physical unity meaning; the flip is an empirical sign correction, not a re-derived mechanism.",
      "boundary_behavior": "q_ASA can be 0 (28 training rows with zero probe accessibility); the +1 in the denominator keeps the expression finite there, yielding q_LabuteASA, without imputing physical accessibility. q_density and q_LabuteASA are strictly positive in training, so the expression is finite on every row.",
      "vary_input": "density",
      "descriptor_direction": "decreasing",
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
        "ASA",
        "LabuteASA",
        "density"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.44160728541545513,
      "target_association": "consistent",
      "perturbation": 0.005792599999999999,
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
