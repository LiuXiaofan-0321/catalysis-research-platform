# high/rag_agent/replicate-3/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
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
  }
]
```

## h1

候选标识：`high/rag_agent/replicate-3/round-2/h1`

最终状态：scored；边际收益：+0.499054 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.Vol

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "path_contrast_localization",
    "formula": "(lsd_p / lsd_f)**2",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases when the largest included sphere along the free-sphere path (lsd_p, Zeo++ Dif) is large relative to the passing bottleneck (lsd_f, Zeo++ Df). A large included-region-to-bottleneck contrast indicates adsorbates localizing in spacious cavities behind narrow windows, which plausibly increases the site-localization entropy penalty; entropy loss is monotonically associated with (lsd_p/lsd_f)**2.",
    "rationale": "Dif/Df contrasts cavity capacity against window restriction within the same pore network; the square emphasizes frameworks where modest windows open into large cavities. Both lsd_p and lsd_f are strictly positive in training (min 3.3452 A and 0.85684 A), so the ratio is finite for every row without imputation. Limitation: Dif and Df are hard-sphere geometric extremes on one representative path; they ignore surface chemistry, multiple windows, and real molecular flexibility. The association is statistical, not a derived equality.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(lsd_p/lsd_f)**2 > 0 within rotor-class-stratified training data. Falsified if the sign flips or the association is not significant when stratifying by lsd_f bins (i.e., if contrast carries no information beyond bottleneck size alone), or if frameworks with near-equal Dif and Df (contrast ~ 1) show entropy losses statistically indistinguishable from high-contrast frameworks at matched lsd_f.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif along the free path and the passing bottleneck Df jointly proxy the cavity-window geometry that governs site localization; the hard-sphere path model transfers imperfectly to real adsorbates with finite size and soft potentials, and Di (global cavity diameter) is not available and is not claimed.",
      "physical_interpretation": "lsd_f is the largest sphere that can pass through a periodic free path (window bottleneck); lsd_p is the largest included sphere along that path (cavity scale on the path). Their ratio is dimensionless; no q-unity threshold is asserted as a physical transition.",
      "boundary_behavior": "Both inputs are strictly positive in training, so the ratio is finite for all 2361 rows; as contrast approaches 1 the descriptor approaches 1 (uniform channel), which is a limit of the proxy, not a phase boundary.",
      "vary_input": "lsd_p",
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
        0.85684,
        7.68726
      ],
      "training_spearman": -0.01948972800795131,
      "target_association": "inconclusive",
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
    "name": "path_contrast_localization",
    "formula": "q_Vol * (lsd_p / lsd_f)**2",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases when the largest included sphere along the free-sphere path (lsd_p, Zeo++ Dif) is large relative to the passing bottleneck (lsd_f, Zeo++ Df). A large included-region-to-bottleneck contrast indicates adsorbates localizing in spacious cavities behind narrow windows, which plausibly increases the site-localization entropy penalty; entropy loss is monotonically associated with (lsd_p/lsd_f)**2.",
    "rationale": "Keeps the preserved cavity-behind-narrow-window localization story but corrects the expression: the round-2 precheck found the bare contrast (lsd_p/lsd_f)**2 essentially unassociated with entropy loss (Spearman -0.019, inconclusive), violating its own predeclared falsification condition. The contrast is therefore weighted by q_Vol, since a localization entropy penalty should scale with how much molecular volume must be accommodated inside the cavity; this is consistent with reported reasoning that rotational freedom depends on molecular size relative to available cage space (E06, E07). Limitations: hard-sphere geometric extremes, an empirical combination blind to surface chemistry, window multiplicity and molecular flexibility; mechanism_validated remains false and the association is statistical, not derived.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(q_Vol * (lsd_p/lsd_f)**2) > 0 within rotor-class-stratified training data. Falsified if the size-weighted contrast shows no residual association after conditioning on q_Vol and lsd_f (i.e., it adds nothing beyond molecular size and bottleneck confinement), if the sign flips, or if high-contrast frameworks with small adsorbates show entropy losses statistically indistinguishable from low-contrast frameworks at matched q_Vol and lsd_f.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06",
      "E07"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif (largest included sphere along the free-sphere path) and Df (largest passing bottleneck sphere) are hard-sphere geometric extremes on representative paths, not the global cavity diameter Di, and transfer imperfectly to real adsorbates with finite size and soft potentials; Vol ignores shape anisotropy. The unweighted contrast (lsd_p/lsd_f)**2 showed an inconclusive global training association (Spearman -0.019), so the size weighting is a predeclared expression correction, not a validated mechanism.",
      "physical_interpretation": "lsd_f is the largest sphere that can pass through a periodic free path (window bottleneck); lsd_p is the largest included sphere along that path (cavity scale on the path); Vol is the adsorbate van der Waals volume. q_Vol = Vol / Vol_ref is a dimensionless row-varying input relative to the fixed positive reference median 67.24 A^3; the full descriptor is dimensionless and no physical threshold is asserted at descriptor value 1.",
      "boundary_behavior": "lsd_p (min 3.3452 A), lsd_f (min 0.85684 A) and Vol (min 20.424 A^3) are strictly positive across all 2361 training rows with strictly positive reference medians, so q_Vol and the squared contrast ratio are finite for every row without imputation; the descriptor grows only outside the native domain, which the regime bounds exclude. No zero branch or rotor_case is invoked.",
      "vary_input": "lsd_p",
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
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "lsd_f": "bottleneck_free_sphere_Df",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.85684,
        7.68726
      ],
      "training_spearman": 0.23975676276369534,
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
    "name": "path_contrast_localization",
    "formula": "q_Vol * (lsd_p / lsd_f)**2",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases when the largest included sphere along the free-sphere path (lsd_p, Zeo++ Dif) is large relative to the passing bottleneck (lsd_f, Zeo++ Df). A large included-region-to-bottleneck contrast indicates adsorbates localizing in spacious cavities behind narrow windows, which plausibly increases the site-localization entropy penalty; entropy loss is monotonically associated with (lsd_p/lsd_f)**2.",
    "rationale": "Keeps the preserved cavity-behind-narrow-window localization story but corrects the expression: the round-2 precheck found the bare contrast (lsd_p/lsd_f)**2 essentially unassociated with entropy loss (Spearman -0.019, inconclusive), violating its own predeclared falsification condition. The contrast is therefore weighted by q_Vol, since a localization entropy penalty should scale with how much molecular volume must be accommodated inside the cavity; this is consistent with reported reasoning that rotational freedom depends on molecular size relative to available cage space (E06, E07). Limitations: hard-sphere geometric extremes, an empirical combination blind to surface chemistry, window multiplicity and molecular flexibility; mechanism_validated remains false and the association is statistical, not derived.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(q_Vol * (lsd_p/lsd_f)**2) > 0 within rotor-class-stratified training data. Falsified if the size-weighted contrast shows no residual association after conditioning on q_Vol and lsd_f (i.e., it adds nothing beyond molecular size and bottleneck confinement), if the sign flips, or if high-contrast frameworks with small adsorbates show entropy losses statistically indistinguishable from low-contrast frameworks at matched q_Vol and lsd_f.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06",
      "E07"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif (largest included sphere along the free-sphere path) and Df (largest passing bottleneck sphere) are hard-sphere geometric extremes on representative paths, not the global cavity diameter Di, and transfer imperfectly to real adsorbates with finite size and soft potentials; Vol ignores shape anisotropy. The unweighted contrast (lsd_p/lsd_f)**2 showed an inconclusive global training association (Spearman -0.019), so the size weighting is a predeclared expression correction, not a validated mechanism.",
      "physical_interpretation": "lsd_f is the largest sphere that can pass through a periodic free path (window bottleneck); lsd_p is the largest included sphere along that path (cavity scale on the path); Vol is the adsorbate van der Waals volume. q_Vol = Vol / Vol_ref is a dimensionless row-varying input relative to the fixed positive reference median 67.24 A^3; the full descriptor is dimensionless and no physical threshold is asserted at descriptor value 1.",
      "boundary_behavior": "lsd_p (min 3.3452 A), lsd_f (min 0.85684 A) and Vol (min 20.424 A^3) are strictly positive across all 2361 training rows with strictly positive reference medians, so q_Vol and the squared contrast ratio are finite for every row without imputation; the descriptor grows only outside the native domain, which the regime bounds exclude. No zero branch or rotor_case is invoked.",
      "vary_input": "lsd_p",
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
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "lsd_f": "bottleneck_free_sphere_Df",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.85684,
        7.68726
      ],
      "training_spearman": 0.23975676276369534,
      "target_association": "consistent",
      "perturbation": 0.0452717,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/rag_agent/replicate-3/round-2/h2`

最终状态：scored；边际收益：-2.194975 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.AV, variable_mappings.lsd_f

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "bottleneck_confinement_inverse",
    "formula": "1 / q_lsd_f**2",
    "hypothesis": "Frameworks with smaller passing free-sphere bottlenecks (smaller lsd_f, the Zeo++ Df largest sphere through a periodic free path) impose stronger geometric confinement gradients at adsorption sites, producing larger adsorbed-phase entropy loss at infinite dilution; the entropy loss is inversely associated with the bottleneck diameter squared.",
    "rationale": "Retained from round 1 with positive marginal improvement (0.0223) and consistent target association (training Spearman 0.387). The inverse-square form proxies the scaling of translational free-volume loss with a characteristic confinement length. Limitation: Df is a hard-sphere window extreme, not a site-level free volume; mechanism_validated remains false and the association is empirical.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(q_lsd_f**-2) > 0 within rotor-class-stratified training data. Falsified if, after conditioning on the h1 path contrast and accessible volume, the residual association with lsd_f changes sign or vanishes, indicating the retained signal was confounded with overall pore size.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Df proxies the confinement length scale controlling translational entropy loss; transfer limited because real adsorbate confinement depends on the molecular minimum dimension relative to windows, and Df is a single hard-sphere extreme per framework.",
      "physical_interpretation": "q_lsd_f = lsd_f / lsd_f_ref is a dimensionless row-varying input with fixed positive reference median 5.16326 A in the training domain; the inverse square is dimensionless. No physical transition is claimed at q_lsd_f = 1.",
      "boundary_behavior": "lsd_f is strictly positive in training (min 0.85684 A) and the reference median is positive, so q_lsd_f > 0 for every row and the expression is finite without imputation; the descriptor diverges only outside the native domain, which the regime bounds exclude.",
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
    "reason": "Redundant with a current input"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "bottleneck_confinement_inverse",
    "formula": "1 / (1 + q_AV)",
    "hypothesis": "Frameworks with smaller passing free-sphere bottlenecks (smaller lsd_f, the Zeo++ Df largest sphere through a periodic free path) impose stronger geometric confinement gradients at adsorption sites, producing larger adsorbed-phase entropy loss at infinite dilution; the entropy loss is inversely associated with the bottleneck diameter squared.",
    "rationale": "Replaces the rejected 1/q_lsd_f**2 (flagged redundant with a current input) with an accessibility-based translational free-volume proxy: frameworks with less probe-accessible volume per mass constrain adsorbate translation more strongly, plausibly increasing adsorbed-phase entropy loss at infinite dilution. Consistent with reported use of occupiable volume as a useful descriptor for predicting adsorption entropy losses (E09) and with the common trend of entropy-loss metrics against occupiable-volume pore descriptors (E08). Limitation: AV is fixed-probe and mass-specific; the association is empirical and partially confounded with overall pore size, so it must be checked against the retained bottleneck descriptor.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(1/(1 + q_AV)) > 0 within rotor-class-stratified training data. Falsified if, after conditioning on the retained bottleneck descriptor lsd_f and adsorbate size, the residual association with 1/(1 + q_AV) changes sign or vanishes (indicating the signal was confounded with overall pore size), or if zero-accessibility rows (q_AV = 0) show entropy losses systematically lower than low-but-nonzero-accessibility rows at matched lsd_f, indicating the descriptor reflects probe-exclusion artifacts rather than translational confinement.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E08",
      "E09"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "AV is probe-accessible volume per framework mass on the native scale, not molecule-specific free volume; it is a fixed-probe, mass-specific quantity that partially confounds pore size with framework amount, and kinetic accessibility does not by itself determine equilibrium entropy. Transfer to real adsorbates is limited because the relevant translational free volume depends on the specific molecule, not the probe.",
      "physical_interpretation": "q_AV = AV / AV_ref is a dimensionless row-varying input relative to the fixed positive training-reference median; the descriptor decreases monotonically with probe-accessible volume, proxying the loss of translational free volume on adsorption. No physical transition is claimed at q_AV = 1 or descriptor value 1.",
      "boundary_behavior": "AV has 28 legitimate zero values in training (zero accessibility for the fixed geometric probe does not imply zero physical molecular adsorption space) and a strictly positive reference median 0.0759781 cm^3/g, so q_AV >= 0 and 1 + q_AV >= 1; the expression is finite for all 2361 rows without imputation. q_AV = 0 maps to the descriptor maximum 1, which is a bounding proxy value, not a physical singularity.",
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
        "AV"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": 0.4572606532712195,
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
    "slot_id": "h2",
    "name": "bottleneck_confinement_inverse",
    "formula": "1 / (1 + q_AV)",
    "hypothesis": "Frameworks with smaller passing free-sphere bottlenecks (smaller lsd_f, the Zeo++ Df largest sphere through a periodic free path) impose stronger geometric confinement gradients at adsorption sites, producing larger adsorbed-phase entropy loss at infinite dilution; the entropy loss is inversely associated with the bottleneck diameter squared.",
    "rationale": "Replaces the rejected 1/q_lsd_f**2 (flagged redundant with a current input) with an accessibility-based translational free-volume proxy: frameworks with less probe-accessible volume per mass constrain adsorbate translation more strongly, plausibly increasing adsorbed-phase entropy loss at infinite dilution. Consistent with reported use of occupiable volume as a useful descriptor for predicting adsorption entropy losses (E09) and with the common trend of entropy-loss metrics against occupiable-volume pore descriptors (E08). Limitation: AV is fixed-probe and mass-specific; the association is empirical and partially confounded with overall pore size, so it must be checked against the retained bottleneck descriptor.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(1/(1 + q_AV)) > 0 within rotor-class-stratified training data. Falsified if, after conditioning on the retained bottleneck descriptor lsd_f and adsorbate size, the residual association with 1/(1 + q_AV) changes sign or vanishes (indicating the signal was confounded with overall pore size), or if zero-accessibility rows (q_AV = 0) show entropy losses systematically lower than low-but-nonzero-accessibility rows at matched lsd_f, indicating the descriptor reflects probe-exclusion artifacts rather than translational confinement.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E08",
      "E09"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "AV is probe-accessible volume per framework mass on the native scale, not molecule-specific free volume; it is a fixed-probe, mass-specific quantity that partially confounds pore size with framework amount, and kinetic accessibility does not by itself determine equilibrium entropy. Transfer to real adsorbates is limited because the relevant translational free volume depends on the specific molecule, not the probe.",
      "physical_interpretation": "q_AV = AV / AV_ref is a dimensionless row-varying input relative to the fixed positive training-reference median; the descriptor decreases monotonically with probe-accessible volume, proxying the loss of translational free volume on adsorption. No physical transition is claimed at q_AV = 1 or descriptor value 1.",
      "boundary_behavior": "AV has 28 legitimate zero values in training (zero accessibility for the fixed geometric probe does not imply zero physical molecular adsorption space) and a strictly positive reference median 0.0759781 cm^3/g, so q_AV >= 0 and 1 + q_AV >= 1; the expression is finite for all 2361 rows without imputation. q_AV = 0 maps to the descriptor maximum 1, which is a bounding proxy value, not a physical singularity.",
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
        "AV"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": 0.4572606532712195,
      "target_association": "consistent",
      "perturbation": 0.001538232,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/rag_agent/replicate-3/round-2/h3`

最终状态：scored；边际收益：-1.410153 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "size_density_coupling",
    "formula": "q_Vol * q_density",
    "hypothesis": "At infinite dilution in rigid pure-silica frameworks, adsorbed-phase entropy loss grows with the product of adsorbate van der Waals volume and framework density: larger molecules packed into denser (lower-porosity) frameworks experience a tighter molecule-to-pore size mismatch, plausibly increasing the site-localization entropy penalty; entropy loss increases monotonically with q_Vol * q_density.",
    "rationale": "Couples an adsorbate geometric proxy (Vol, strictly positive, native range 20.424-161.144 A^3) with a framework packing proxy (density on the published numerical scale, strictly positive, native range 0.759654-2.11908). Higher framework density at fixed chemistry typically implies smaller accessible pore space, amplifying confinement of larger adsorbates; neither factor alone distinguishes a large molecule in a roomy framework from a small molecule in a dense one. Limitation: the density unit is unresolved on the native scale and q-constants carry no universal physical meaning; the product is an empirical interaction proxy, not a derived free-volume quantity, and it is blind to surface chemistry and window topology.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(q_Vol * q_density) > 0 within rotor-class-stratified training data. Falsified if the association is not significant after stratifying on lsd_f (i.e., the product adds nothing beyond bottleneck confinement), or if large-molecule/dense-framework rows show entropy losses lower than small-molecule/open-framework rows at matched accessibility, indicating a competing energetic or accessibility mechanism dominates.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Van der Waals volume proxies adsorbate size and framework density proxies inverse pore space; both are transfer-limited because Vol ignores shape anisotropy (captured elsewhere by heavy-atom proxies) and density is a mass-based packing proxy with unresolved unit scale, not a molecule-specific free volume.",
      "physical_interpretation": "q_Vol = Vol / Vol_ref and q_density = density / density_ref are dimensionless row-varying inputs with fixed positive training-reference medians (67.24 A^3, 1.73742); the product is dimensionless. No physical threshold is asserted at product value 1.",
      "boundary_behavior": "Vol and density have zero_n = 0 and strictly positive reference medians in training, so q_Vol > 0 and q_density > 0 for all 2361 rows and the product is finite without imputation; no zero or single-site/linear rotor branch is invoked.",
      "vary_input": "Vol",
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
        "Vol",
        "density"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
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
      "training_spearman": 0.5366404450457583,
      "target_association": "consistent",
      "perturbation": 0.7023999999999999,
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
    "name": "size_density_coupling",
    "formula": "q_Vol * q_density",
    "hypothesis": "At infinite dilution in rigid pure-silica frameworks, adsorbed-phase entropy loss grows with the product of adsorbate van der Waals volume and framework density: larger molecules packed into denser (lower-porosity) frameworks experience a tighter molecule-to-pore size mismatch, plausibly increasing the site-localization entropy penalty; entropy loss increases monotonically with q_Vol * q_density.",
    "rationale": "Couples an adsorbate geometric proxy (Vol, strictly positive, native range 20.424-161.144 A^3) with a framework packing proxy (density on the published numerical scale, strictly positive, native range 0.759654-2.11908). Higher framework density at fixed chemistry typically implies smaller accessible pore space, amplifying confinement of larger adsorbates; neither factor alone distinguishes a large molecule in a roomy framework from a small molecule in a dense one. Limitation: the density unit is unresolved on the native scale and q-constants carry no universal physical meaning; the product is an empirical interaction proxy, not a derived free-volume quantity, and it is blind to surface chemistry and window topology.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(q_Vol * q_density) > 0 within rotor-class-stratified training data. Falsified if the association is not significant after stratifying on lsd_f (i.e., the product adds nothing beyond bottleneck confinement), or if large-molecule/dense-framework rows show entropy losses lower than small-molecule/open-framework rows at matched accessibility, indicating a competing energetic or accessibility mechanism dominates.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Van der Waals volume proxies adsorbate size and framework density proxies inverse pore space; both are transfer-limited because Vol ignores shape anisotropy (captured elsewhere by heavy-atom proxies) and density is a mass-based packing proxy with unresolved unit scale, not a molecule-specific free volume.",
      "physical_interpretation": "q_Vol = Vol / Vol_ref and q_density = density / density_ref are dimensionless row-varying inputs with fixed positive training-reference medians (67.24 A^3, 1.73742); the product is dimensionless. No physical threshold is asserted at product value 1.",
      "boundary_behavior": "Vol and density have zero_n = 0 and strictly positive reference medians in training, so q_Vol > 0 and q_density > 0 for all 2361 rows and the product is finite without imputation; no zero or single-site/linear rotor branch is invoked.",
      "vary_input": "Vol",
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
        "Vol",
        "density"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
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
      "training_spearman": 0.5366404450457583,
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
    "name": "size_density_coupling",
    "formula": "q_Vol * q_density",
    "hypothesis": "At infinite dilution in rigid pure-silica frameworks, adsorbed-phase entropy loss grows with the product of adsorbate van der Waals volume and framework density: larger molecules packed into denser (lower-porosity) frameworks experience a tighter molecule-to-pore size mismatch, plausibly increasing the site-localization entropy penalty; entropy loss increases monotonically with q_Vol * q_density.",
    "rationale": "Couples an adsorbate geometric proxy (Vol, strictly positive, native range 20.424-161.144 A^3) with a framework packing proxy (density on the published numerical scale, strictly positive, native range 0.759654-2.11908). Higher framework density at fixed chemistry typically implies smaller accessible pore space, amplifying confinement of larger adsorbates; neither factor alone distinguishes a large molecule in a roomy framework from a small molecule in a dense one. Limitation: the density unit is unresolved on the native scale and q-constants carry no universal physical meaning; the product is an empirical interaction proxy, not a derived free-volume quantity, and it is blind to surface chemistry and window topology.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(q_Vol * q_density) > 0 within rotor-class-stratified training data. Falsified if the association is not significant after stratifying on lsd_f (i.e., the product adds nothing beyond bottleneck confinement), or if large-molecule/dense-framework rows show entropy losses lower than small-molecule/open-framework rows at matched accessibility, indicating a competing energetic or accessibility mechanism dominates.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Van der Waals volume proxies adsorbate size and framework density proxies inverse pore space; both are transfer-limited because Vol ignores shape anisotropy (captured elsewhere by heavy-atom proxies) and density is a mass-based packing proxy with unresolved unit scale, not a molecule-specific free volume.",
      "physical_interpretation": "q_Vol = Vol / Vol_ref and q_density = density / density_ref are dimensionless row-varying inputs with fixed positive training-reference medians (67.24 A^3, 1.73742); the product is dimensionless. No physical threshold is asserted at product value 1.",
      "boundary_behavior": "Vol and density have zero_n = 0 and strictly positive reference medians in training, so q_Vol > 0 and q_density > 0 for all 2361 rows and the product is finite without imputation; no zero or single-site/linear rotor branch is invoked.",
      "vary_input": "Vol",
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
        "Vol",
        "density"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
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
      "training_spearman": 0.5366404450457583,
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
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:0db59549906f2790c6f859bb",
        "paper_id": "doi:10.1021/jp055190k",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7bec0989f12cc18693a97a3f",
        "paper_id": "doi:10.1039/d5cs00220f",
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
        "record_id": "chunk:aec11c5a588f125ea377fc95",
        "paper_id": "doi:10.1021/acs.est.9b04154",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd75db1400cf2ce6171ef0f6",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c221f77d5d5ce26095f7b022",
        "paper_id": "doi:10.1021/ja400267g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2a768b44ce1affefa97fabed",
        "paper_id": "doi:10.1007/s10853-019-03451-6",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3f393dae0a18a5310296642a",
        "paper_id": "doi:10.1039/d3cs00404j",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3fafeec67e45249e321c1bac",
        "paper_id": "doi:10.1002/cphc.202400347",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5aff3d9da9c035dec7cb74e7",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6548d8cfcf6b0a54557fd663",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9149465393580d1d53d84d0f",
        "paper_id": "doi:10.1002/cphc.202400347",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9a3907e626bcdef0bc5bb0cb",
        "paper_id": "doi:10.1002/chem.201705627",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:acfc65161a03f5a1c235bacc",
        "paper_id": "doi:10.1002/cphc.201000995",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e1b683dc5917739326965133",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e933adf17670b8f416a9170e",
        "paper_id": "doi:10.1021/la302230z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ecf3b350af8d5c09a9a10048",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f930a6fc9a290a46087a609e",
        "paper_id": "doi:10.1021/jacs.0c09825",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:166106b9d0f41731d2d72c4f",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1d31f4f7e46b887f464a699d",
        "paper_id": "doi:10.1021/jacs.0c09825",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases when the largest included sphere along the free-sphere path (lsd_p, Zeo++ Dif) is large relative to the passing bottleneck (lsd_f, Zeo++ Df). A large included-region-to-bottleneck contrast indicates adsorbates localizing in spacious cavities behind narrow windows, which plausibly increases the site-localization entropy penalty; entropy loss is monotonically associated with (lsd_p/lsd_f)**2. (lsd_p / lsd_f)**2 Frameworks with smaller passing free-sphere bottlenecks (smaller lsd_f, the Zeo++ Df largest sphere through a periodic free path) impose stronger geometric confinement gradients at adsorption sites, producing larger adsorbed-phase entropy loss at infinite dilution; the entropy loss is inversely associated with the bottleneck diameter squared. 1 / q_lsd_f**2 At infinite dilution in rigid pure-silica frameworks, adsorbed-phase entropy loss grows with the product of adsorbate van der Waals volume and framework density: larger molecules packed into denser (lower-porosity) frameworks experience a tighter molecule-to-pore size mismatch, plausibly increasing the site-localization entropy penalty; entropy loss increases monotonically with q_Vol * q_density. q_Vol * q_density   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:8ffcc4698d37d4f5569d53f5",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:4d61464df6d3ab3bd0198cd4"
    ],
    "items": 10,
    "lexical_tokens": 4683,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [
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
      "id": "E08"
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
