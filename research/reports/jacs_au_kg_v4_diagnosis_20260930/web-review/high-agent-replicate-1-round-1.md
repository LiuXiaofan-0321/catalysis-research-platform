# high/agent/replicate-1/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`high/agent/replicate-1/round-1/h1`

最终状态：scored；边际收益：+3.046761 pp；保留：True。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "volume_accessibility_confinement_loss",
    "formula": "log10(1 + q_Vol / (1 + q_AV))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with adsorbate van der Waals volume and decreases with the fixed-probe accessible specific volume of the framework: bulky adsorbates in frameworks with small probe-accessible volume lose the largest fraction of translational/configurational entropy.",
    "rationale": "Translational entropy loss upon confinement is expected to scale with how much molecular volume must be accommodated in a restricted pore space. AV is a fixed-probe, mass-specific accessibility proxy, not a molecule-specific free volume, so the ratio q_Vol/(1+q_AV) is an empirical confinement index: it grows with adsorbate size and shrinks as the framework offers more probe-accessible volume. The log10(1+.) form is a monotone empirical smoothing that keeps the descriptor finite and bounded for all training rows; its scale has no universal physical meaning.",
    "falsification_criteria": "If entropy loss (MAE-scored as s_ads/s_gas deviation) shows no monotone association with this descriptor across the training domain, or if frameworks with equal AV but different connectivity (e.g., different lsd_f at matched AV) systematically invert the predicted ordering, the volume-accessibility confinement mechanism is falsified for this dataset and a connectivity- or shape-dominated mechanism should be tested instead.",
    "novelty_status": "known_relation",
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
      "proxy_assumptions": "AV is a fixed-geometric-probe accessibility proxy; zero AV for the fixed probe does not imply zero molecular adsorption space, so AV enters only through the finite, monotone factor 1/(1+q_AV). Vol is an all-atom van der Waals volume proxy. Neither proxy captures framework chemistry beyond geometry.",
      "physical_interpretation": "q_Vol normalizes adsorbate size by the fixed training-reference median Vol_ref; q_AV normalizes fixed-probe accessibility by AV_ref. Both are dimensionless row-varying inputs. No unity threshold in q carries physical meaning; the descriptor is an empirical monotone index.",
      "boundary_behavior": "At AV=0 (28 training rows), q_AV=0 and the descriptor reduces to log10(1+q_Vol), finite and positive; this is justified because zero fixed-probe accessibility is a probe limitation, not proof of zero adsorption entropy loss. q_Vol is bounded away from zero in training (Vol min 20.424), so the descriptor is finite everywhere.",
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

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "volume_accessibility_confinement_loss",
    "formula": "log10(1 + q_Vol / (1 + q_AV))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with adsorbate van der Waals volume and decreases with the fixed-probe accessible specific volume of the framework: bulky adsorbates in frameworks with small probe-accessible volume lose the largest fraction of translational/configurational entropy.",
    "rationale": "Translational entropy loss upon confinement is expected to scale with how much molecular volume must be accommodated in a restricted pore space. AV is a fixed-probe, mass-specific accessibility proxy, not a molecule-specific free volume, so the ratio q_Vol/(1+q_AV) is an empirical confinement index: it grows with adsorbate size and shrinks as the framework offers more probe-accessible volume. The log10(1+.) form is a monotone empirical smoothing that keeps the descriptor finite and bounded for all training rows; its scale has no universal physical meaning.",
    "falsification_criteria": "If entropy loss (MAE-scored as s_ads/s_gas deviation) shows no monotone association with this descriptor across the training domain, or if frameworks with equal AV but different connectivity (e.g., different lsd_f at matched AV) systematically invert the predicted ordering, the volume-accessibility confinement mechanism is falsified for this dataset and a connectivity- or shape-dominated mechanism should be tested instead.",
    "novelty_status": "known_relation",
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
      "proxy_assumptions": "AV is a fixed-geometric-probe accessibility proxy; zero AV for the fixed probe does not imply zero molecular adsorption space, so AV enters only through the finite, monotone factor 1/(1+q_AV). Vol is an all-atom van der Waals volume proxy. Neither proxy captures framework chemistry beyond geometry.",
      "physical_interpretation": "q_Vol normalizes adsorbate size by the fixed training-reference median Vol_ref; q_AV normalizes fixed-probe accessibility by AV_ref. Both are dimensionless row-varying inputs. No unity threshold in q carries physical meaning; the descriptor is an empirical monotone index.",
      "boundary_behavior": "At AV=0 (28 training rows), q_AV=0 and the descriptor reduces to log10(1+q_Vol), finite and positive; this is justified because zero fixed-probe accessibility is a probe limitation, not proof of zero adsorption entropy loss. q_Vol is bounded away from zero in training (Vol min 20.424), so the descriptor is finite everywhere.",
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
    "slot_id": "h1",
    "name": "volume_accessibility_confinement_loss",
    "formula": "log10(1 + q_Vol / (1 + q_AV))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with adsorbate van der Waals volume and decreases with the fixed-probe accessible specific volume of the framework: bulky adsorbates in frameworks with small probe-accessible volume lose the largest fraction of translational/configurational entropy.",
    "rationale": "Translational entropy loss upon confinement is expected to scale with how much molecular volume must be accommodated in a restricted pore space. AV is a fixed-probe, mass-specific accessibility proxy, not a molecule-specific free volume, so the ratio q_Vol/(1+q_AV) is an empirical confinement index: it grows with adsorbate size and shrinks as the framework offers more probe-accessible volume. The log10(1+.) form is a monotone empirical smoothing that keeps the descriptor finite and bounded for all training rows; its scale has no universal physical meaning.",
    "falsification_criteria": "If entropy loss (MAE-scored as s_ads/s_gas deviation) shows no monotone association with this descriptor across the training domain, or if frameworks with equal AV but different connectivity (e.g., different lsd_f at matched AV) systematically invert the predicted ordering, the volume-accessibility confinement mechanism is falsified for this dataset and a connectivity- or shape-dominated mechanism should be tested instead.",
    "novelty_status": "known_relation",
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
      "proxy_assumptions": "AV is a fixed-geometric-probe accessibility proxy; zero AV for the fixed probe does not imply zero molecular adsorption space, so AV enters only through the finite, monotone factor 1/(1+q_AV). Vol is an all-atom van der Waals volume proxy. Neither proxy captures framework chemistry beyond geometry.",
      "physical_interpretation": "q_Vol normalizes adsorbate size by the fixed training-reference median Vol_ref; q_AV normalizes fixed-probe accessibility by AV_ref. Both are dimensionless row-varying inputs. No unity threshold in q carries physical meaning; the descriptor is an empirical monotone index.",
      "boundary_behavior": "At AV=0 (28 training rows), q_AV=0 and the descriptor reduces to log10(1+q_Vol), finite and positive; this is justified because zero fixed-probe accessibility is a probe limitation, not proof of zero adsorption entropy loss. q_Vol is bounded away from zero in training (Vol min 20.424), so the descriptor is finite everywhere.",
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

## h2

候选标识：`high/agent/replicate-1/round-1/h2`

最终状态：scored；边际收益：-4.495879 pp；保留：False。

复核改动字段：formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_case_inertia_loss",
    "formula": "rotor_case(0, log10(1 + q_PMI1), log10(1 + (q_PMI2 + q_PMI3)/2))",
    "hypothesis": "Rotational configurational entropy loss upon confinement depends on rotor class: single-site adsorbates lose no rotationally resolved entropy under this descriptor, linear adsorbates lose an amount increasing with their heavy-atom first principal moment proxy, and nonlinear adsorbates lose an amount increasing with the mean of their second and third heavy-atom moment proxies.",
    "rationale": "Rotation of an adsorbate inside a pore is restricted by steric fit; heavier-atom inertia proxies should correlate with the magnitude of rotational entropy loss. The three rotor classes are treated with distinct branches because the dimensional and symmetry structure of rotational entropy loss differs between single-site, linear, and nonlinear rotors. PMI values are original implicit-H/heavy-atom proxies, not true all-atom inertias; legitimate zeros in these proxies reflect the representation and the branch structure, not physically zero all-atom inertia.",
    "falsification_criteria": "If the nonlinear branch fails to outperform a single pooled inertia descriptor (e.g., log10(1+q_PMI1) applied to all rows) on entropy-loss MAE, or if single-site adsorbates show entropy-loss variation that tracks adsorbate-only proxies (impossible under the constant single-site branch), the class-dependent rotational mechanism as encoded is falsified and a unified shape-based mechanism should be tested.",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom principal-moment proxies in the original implicit-H representation; they are not true all-atom inertias and can be legitimately zero. rotor_case categories (54 single_site, 214 linear, 2093 nonlinear in training) are taken as given, with normalized tolerance 1e-10; no imputation of zeros is performed.",
      "physical_interpretation": "q_PMI1, q_PMI2, q_PMI3 are row-varying dimensionless normalizations by the fixed training-reference medians. The constants 0 and the coefficient 1/2 inside the nonlinear branch are fixed structural choices of the descriptor, not fitted parameters and not universal physical constants. log10(1+.) is monotone empirical smoothing with no physical unity threshold.",
      "boundary_behavior": "The single-site branch returns the constant 0 (dimensionless, compatible with the log outputs of the other branches), encoding zero rotationally resolved loss under this descriptor. The linear branch equals 0 when q_PMI1=0 (legitimate zero in the heavy-atom proxy), finite and justified as the lower bound of the monotone smoothing. The nonlinear branch is finite when q_PMI2=q_PMI3=0 for the same reason. All three branch outputs are dimensionless and finite on every training row.",
      "vary_input": "PMI3",
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
      "training_spearman": 0.4074022414180155,
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
    "name": "rotor_case_inertia_loss",
    "formula": "rotor_case(0, log10(1 + (q_PMI2 + q_PMI3)/2), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3)/3))",
    "hypothesis": "Rotational configurational entropy loss upon confinement depends on rotor class: single-site adsorbates lose no rotationally resolved entropy under this descriptor, linear adsorbates lose an amount increasing with their heavy-atom first principal moment proxy, and nonlinear adsorbates lose an amount increasing with the mean of their second and third heavy-atom moment proxies.",
    "rationale": "Rotation of an adsorbate inside a pore is restricted by steric fit; heavier-atom inertia proxies should correlate with the magnitude of rotational entropy loss. The three rotor classes are treated with distinct branches because the symmetry structure of rotational entropy loss differs between single-site, linear, and nonlinear rotors. Domain correction relative to the draft: the linear branch previously used q_PMI1, which is the near-zero axis moment for linear heavy-atom representations and therefore carried essentially no signal for the 214 linear training rows; the corrected linear branch uses the mean of the two perpendicular-moment proxies, and the nonlinear branch averages all three moments. PMI values are original implicit-H/heavy-atom proxies, not true all-atom inertias; legitimate zeros reflect the representation and the branch structure, not physically zero all-atom inertia.",
    "falsification_criteria": "If the nonlinear branch fails to outperform a single pooled inertia descriptor (e.g., log10(1+q_PMI1) applied to all rows) on entropy-loss MAE, or if single-site adsorbates show entropy-loss variation that tracks adsorbate-only proxies (impossible under the constant single-site branch), the class-dependent rotational mechanism as encoded is falsified and a unified shape-based mechanism should be tested.",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom principal-moment proxies in the original implicit-H representation; they are not true all-atom inertias and can be legitimately zero. rotor_case categories (54 single_site, 214 linear, 2093 nonlinear in training) are taken as given, with normalized tolerance 1e-10; no imputation of zeros is performed.",
      "physical_interpretation": "q_PMI1, q_PMI2, q_PMI3 are row-varying dimensionless normalizations by the fixed training-reference medians. Domain correction: for a linear heavy-atom arrangement PMI1 is the moment about the molecular axis and is near zero by representation, so it carries no rotational-restriction signal for linear rotors; the linear branch therefore uses the two perpendicular-moment proxies (PMI2, PMI3). The nonlinear branch averages all three moments. The constant 0 and the fixed coefficients 1/2 and 1/3 are structural descriptor choices, not fitted parameters and not universal physical constants. log10(1+.) is monotone empirical smoothing with no physical unity threshold.",
      "boundary_behavior": "The single-site branch returns the constant 0 (dimensionless, compatible with the log outputs of the other branches), encoding zero rotationally resolved loss under this descriptor. The linear branch equals 0 when q_PMI2 = q_PMI3 = 0 (legitimate heavy-atom proxy zeros), finite and justified as the lower bound of the monotone smoothing. The nonlinear branch is finite when q_PMI1 = q_PMI2 = q_PMI3 = 0 for the same reason. All three branch outputs are dimensionless and finite on every training row.",
      "vary_input": "PMI3",
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
      "training_spearman": 0.401039610660845,
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
    "name": "rotor_case_inertia_loss",
    "formula": "rotor_case(0, log10(1 + (q_PMI2 + q_PMI3)/2), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3)/3))",
    "hypothesis": "Rotational configurational entropy loss upon confinement depends on rotor class: single-site adsorbates lose no rotationally resolved entropy under this descriptor, linear adsorbates lose an amount increasing with their heavy-atom first principal moment proxy, and nonlinear adsorbates lose an amount increasing with the mean of their second and third heavy-atom moment proxies.",
    "rationale": "Rotation of an adsorbate inside a pore is restricted by steric fit; heavier-atom inertia proxies should correlate with the magnitude of rotational entropy loss. The three rotor classes are treated with distinct branches because the symmetry structure of rotational entropy loss differs between single-site, linear, and nonlinear rotors. Domain correction relative to the draft: the linear branch previously used q_PMI1, which is the near-zero axis moment for linear heavy-atom representations and therefore carried essentially no signal for the 214 linear training rows; the corrected linear branch uses the mean of the two perpendicular-moment proxies, and the nonlinear branch averages all three moments. PMI values are original implicit-H/heavy-atom proxies, not true all-atom inertias; legitimate zeros reflect the representation and the branch structure, not physically zero all-atom inertia.",
    "falsification_criteria": "If the nonlinear branch fails to outperform a single pooled inertia descriptor (e.g., log10(1+q_PMI1) applied to all rows) on entropy-loss MAE, or if single-site adsorbates show entropy-loss variation that tracks adsorbate-only proxies (impossible under the constant single-site branch), the class-dependent rotational mechanism as encoded is falsified and a unified shape-based mechanism should be tested.",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom principal-moment proxies in the original implicit-H representation; they are not true all-atom inertias and can be legitimately zero. rotor_case categories (54 single_site, 214 linear, 2093 nonlinear in training) are taken as given, with normalized tolerance 1e-10; no imputation of zeros is performed.",
      "physical_interpretation": "q_PMI1, q_PMI2, q_PMI3 are row-varying dimensionless normalizations by the fixed training-reference medians. Domain correction: for a linear heavy-atom arrangement PMI1 is the moment about the molecular axis and is near zero by representation, so it carries no rotational-restriction signal for linear rotors; the linear branch therefore uses the two perpendicular-moment proxies (PMI2, PMI3). The nonlinear branch averages all three moments. The constant 0 and the fixed coefficients 1/2 and 1/3 are structural descriptor choices, not fitted parameters and not universal physical constants. log10(1+.) is monotone empirical smoothing with no physical unity threshold.",
      "boundary_behavior": "The single-site branch returns the constant 0 (dimensionless, compatible with the log outputs of the other branches), encoding zero rotationally resolved loss under this descriptor. The linear branch equals 0 when q_PMI2 = q_PMI3 = 0 (legitimate heavy-atom proxy zeros), finite and justified as the lower bound of the monotone smoothing. The nonlinear branch is finite when q_PMI1 = q_PMI2 = q_PMI3 = 0 for the same reason. All three branch outputs are dimensionless and finite on every training row.",
      "vary_input": "PMI3",
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
      "training_spearman": 0.401039610660845,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/agent/replicate-1/round-1/h3`

最终状态：scored；边际收益：-1.540837 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "bottleneck_size_contrast_loss",
    "formula": "log10(1 + q_GeDi / q_lsd_f)",
    "hypothesis": "Adsorption entropy loss increases with the contrast between the adsorbate's largest heavy-atom pair distance and the framework's largest passing free sphere: as the adsorbate's greatest dimension approaches the bottleneck free-sphere diameter of the periodic free path, configurational freedom in the adsorbed phase is most restricted and entropy loss is largest; when the adsorbate is much smaller than the bottleneck, the descriptor plateaus near its smoothed lower bound.",
    "rationale": "GeDi is a heavy-atom maximum-extent proxy for the adsorbate; lsd_f (Zeo++ Df) is the largest sphere that can pass through a periodic free path, i.e., a bottleneck measure, not a global cavity diameter. Their ratio is a geometric path-contrast index: near-bottleneck-sized adsorbates plausibly sample fewer accessible configurations. lsd_f is strictly positive in training (min 0.85684), so the ratio is always defined; q_GeDi may be legitimately zero (54 rows), giving descriptor value 0. The log10(1+.) form is monotone empirical smoothing; the ratio carries no universal physical unity threshold.",
    "falsification_criteria": "If entropy loss does not decrease with increasing lsd_f at matched GeDi (i.e., frameworks with wider bottlenecks do not retain more adsorbed-phase configurational entropy for similarly sized adsorbates), or if included-diameter-along-path lsd_p substitutes for lsd_f with equal or better association (suggesting cavity volume rather than bottleneck passage governs entropy loss), the bottleneck-contrast mechanism is falsified in favor of a cavity-volume or shape-matching mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "GeDi is an original implicit-H/heavy-atom maximum pair-distance proxy and can be legitimately zero; it is not an all-atom kinetic diameter. lsd_f is the Df bottleneck free sphere along a periodic free path, not the global included cavity diameter Di and not lsd_p; D0 data do not contain Di. The contrast is a geometric proxy for configurational restriction, with no assertion about kinetic escape determining equilibrium entropy.",
      "physical_interpretation": "q_GeDi and q_lsd_f are row-varying dimensionless normalizations by fixed training-reference medians (GeDi_ref, lsd_f_ref). The descriptor is largest when heavy-atom extent is large relative to the passing bottleneck; the smoothed log form bounds the lower end but has no physical unity threshold in q_GeDi/q_lsd_f.",
      "boundary_behavior": "At GeDi=0 (54 training rows, legitimate heavy-atom proxy zero, e.g., single-site adsorbates), q_GeDi=0 and the descriptor equals log10(1+0)=0, finite; this encodes the plateau of negligible size contrast. q_lsd_f is strictly positive on all training rows (lsd_f min 0.85684), so no division by zero occurs and no imputation is needed. The descriptor is finite on every training row.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
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
        "GeDi",
        "lsd_f"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.608006859917338,
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
    "slot_id": "h3",
    "name": "bottleneck_size_contrast_loss",
    "formula": "log10(1 + q_GeDi / q_lsd_f)",
    "hypothesis": "Adsorption entropy loss increases with the contrast between the adsorbate's largest heavy-atom pair distance and the framework's largest passing free sphere: as the adsorbate's greatest dimension approaches the bottleneck free-sphere diameter of the periodic free path, configurational freedom in the adsorbed phase is most restricted and entropy loss is largest; when the adsorbate is much smaller than the bottleneck, the descriptor plateaus near its smoothed lower bound.",
    "rationale": "GeDi is a heavy-atom maximum-extent proxy for the adsorbate; lsd_f (Zeo++ Df) is the largest sphere that can pass through a periodic free path, i.e., a bottleneck measure, not a global cavity diameter. Their ratio is a geometric path-contrast index: near-bottleneck-sized adsorbates plausibly sample fewer accessible configurations. lsd_f is strictly positive in training (min 0.85684), so the ratio is always defined; q_GeDi may be legitimately zero (54 rows), giving descriptor value 0. The log10(1+.) form is monotone empirical smoothing; the ratio carries no universal physical unity threshold.",
    "falsification_criteria": "If entropy loss does not decrease with increasing lsd_f at matched GeDi (i.e., frameworks with wider bottlenecks do not retain more adsorbed-phase configurational entropy for similarly sized adsorbates), or if included-diameter-along-path lsd_p substitutes for lsd_f with equal or better association (suggesting cavity volume rather than bottleneck passage governs entropy loss), the bottleneck-contrast mechanism is falsified in favor of a cavity-volume or shape-matching mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "GeDi is an original implicit-H/heavy-atom maximum pair-distance proxy and can be legitimately zero; it is not an all-atom kinetic diameter. lsd_f is the Df bottleneck free sphere along a periodic free path, not the global included cavity diameter Di and not lsd_p; D0 data do not contain Di. The contrast is a geometric proxy for configurational restriction, with no assertion about kinetic escape determining equilibrium entropy.",
      "physical_interpretation": "q_GeDi and q_lsd_f are row-varying dimensionless normalizations by fixed training-reference medians (GeDi_ref, lsd_f_ref). The descriptor is largest when heavy-atom extent is large relative to the passing bottleneck; the smoothed log form bounds the lower end but has no physical unity threshold in q_GeDi/q_lsd_f.",
      "boundary_behavior": "At GeDi=0 (54 training rows, legitimate heavy-atom proxy zero, e.g., single-site adsorbates), q_GeDi=0 and the descriptor equals log10(1+0)=0, finite; this encodes the plateau of negligible size contrast. q_lsd_f is strictly positive on all training rows (lsd_f min 0.85684), so no division by zero occurs and no imputation is needed. The descriptor is finite on every training row.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
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
        "GeDi",
        "lsd_f"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.608006859917338,
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
    "name": "bottleneck_size_contrast_loss",
    "formula": "log10(1 + q_GeDi / q_lsd_f)",
    "hypothesis": "Adsorption entropy loss increases with the contrast between the adsorbate's largest heavy-atom pair distance and the framework's largest passing free sphere: as the adsorbate's greatest dimension approaches the bottleneck free-sphere diameter of the periodic free path, configurational freedom in the adsorbed phase is most restricted and entropy loss is largest; when the adsorbate is much smaller than the bottleneck, the descriptor plateaus near its smoothed lower bound.",
    "rationale": "GeDi is a heavy-atom maximum-extent proxy for the adsorbate; lsd_f (Zeo++ Df) is the largest sphere that can pass through a periodic free path, i.e., a bottleneck measure, not a global cavity diameter. Their ratio is a geometric path-contrast index: near-bottleneck-sized adsorbates plausibly sample fewer accessible configurations. lsd_f is strictly positive in training (min 0.85684), so the ratio is always defined; q_GeDi may be legitimately zero (54 rows), giving descriptor value 0. The log10(1+.) form is monotone empirical smoothing; the ratio carries no universal physical unity threshold.",
    "falsification_criteria": "If entropy loss does not decrease with increasing lsd_f at matched GeDi (i.e., frameworks with wider bottlenecks do not retain more adsorbed-phase configurational entropy for similarly sized adsorbates), or if included-diameter-along-path lsd_p substitutes for lsd_f with equal or better association (suggesting cavity volume rather than bottleneck passage governs entropy loss), the bottleneck-contrast mechanism is falsified in favor of a cavity-volume or shape-matching mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "GeDi is an original implicit-H/heavy-atom maximum pair-distance proxy and can be legitimately zero; it is not an all-atom kinetic diameter. lsd_f is the Df bottleneck free sphere along a periodic free path, not the global included cavity diameter Di and not lsd_p; D0 data do not contain Di. The contrast is a geometric proxy for configurational restriction, with no assertion about kinetic escape determining equilibrium entropy.",
      "physical_interpretation": "q_GeDi and q_lsd_f are row-varying dimensionless normalizations by fixed training-reference medians (GeDi_ref, lsd_f_ref). The descriptor is largest when heavy-atom extent is large relative to the passing bottleneck; the smoothed log form bounds the lower end but has no physical unity threshold in q_GeDi/q_lsd_f.",
      "boundary_behavior": "At GeDi=0 (54 training rows, legitimate heavy-atom proxy zero, e.g., single-site adsorbates), q_GeDi=0 and the descriptor equals log10(1+0)=0, finite; this encodes the plateau of negligible size contrast. q_lsd_f is strictly positive on all training rows (lsd_f min 0.85684), so no division by zero occurs and no imputation is needed. The descriptor is finite on every training row.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
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
        "GeDi",
        "lsd_f"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.608006859917338,
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
