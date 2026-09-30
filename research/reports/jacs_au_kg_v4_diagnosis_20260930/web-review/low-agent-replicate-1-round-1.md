# low/agent/replicate-1/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`low/agent/replicate-1/round-1/h1`

最终状态：scored；边际收益：-0.202385 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confined_translation",
    "formula": "(MW / MW_ref) * (lsd_f_ref / lsd_f) ** 2",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss grows quadratically with confinement relative to the gas phase; frameworks with smaller passing free-sphere bottlenecks (Df/lsd_f) impose greater translational restriction, so the entropy loss (and hence the MAE-scored association) increases as lsd_f decreases and as adsorbate mass increases.",
    "rationale": "Adsorbed translational degrees of freedom in a narrow channel resemble motion in a tighter effective cell; harmonic/confinement models give entropy loss scaling with the square of the inverse characteristic length. lsd_f (Zeo++ Df) is the largest sphere that can traverse the framework, an empirical bottleneck proxy, not a measured cavity diameter. MW proxies the gas-phase translational reference scale. Limitations: lsd_f is geometry-only, ignores framework chemistry (pure silica so chemistry is uniform), and no claim is made that Df equals the global included diameter Di.",
    "falsification_criteria": "If measured entropy loss is flat or decreasing in lsd_f across frameworks with similar AV, or if the lsd_f^2 power dependence is rejected (e.g., linear or saturating dependence fits better on held-out D0 data), the hypothesis is falsified. Competing mechanism: rotational entropy loss dominating over translational loss for large adsorbates.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f proxies confinement length; MW proxies mass-dependent entropy scale; heavy-atom-derived quantities are not used; transfer across adsorbates assumes shape effects are secondary to mass and bottleneck size.",
      "physical_interpretation": "Native meanings: Df is a passing bottleneck, MW is molecular weight; q-normalization uses fixed positive training-reference medians, and no q-unity physical threshold is asserted.",
      "boundary_behavior": "MW ranges [16.03, 184.15] and lsd_f ranges [0.857, 7.687] in training, both strictly positive, so the expression is finite on every row; no division by zero occurs.",
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.6601115891161025,
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
    "name": "bottleneck_confined_translation",
    "formula": "(MW / MW_ref) * (lsd_f_ref / lsd_f) ** 2",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss grows quadratically with confinement relative to the gas phase; frameworks with smaller passing free-sphere bottlenecks (Df/lsd_f) impose greater translational restriction, so the entropy loss (and hence the MAE-scored association) increases as lsd_f decreases and as adsorbate mass increases.",
    "rationale": "Adsorbed translational degrees of freedom in a narrow channel resemble motion in a tighter effective cell; harmonic/confinement models give entropy loss scaling with the square of the inverse characteristic length. lsd_f (Zeo++ Df) is the largest sphere that can traverse the framework, an empirical bottleneck proxy, not a measured cavity diameter. MW proxies the gas-phase translational reference scale. Limitations: lsd_f is geometry-only, ignores framework chemistry (pure silica so chemistry is uniform), and no claim is made that Df equals the global included diameter Di.",
    "falsification_criteria": "If measured entropy loss is flat or decreasing in lsd_f across frameworks with similar AV, or if the lsd_f^2 power dependence is rejected (e.g., linear or saturating dependence fits better on held-out D0 data), the hypothesis is falsified. Competing mechanism: rotational entropy loss dominating over translational loss for large adsorbates.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f proxies confinement length; MW proxies mass-dependent entropy scale; heavy-atom-derived quantities are not used; transfer across adsorbates assumes shape effects are secondary to mass and bottleneck size.",
      "physical_interpretation": "Native meanings: Df is a passing bottleneck, MW is molecular weight; q-normalization uses fixed positive training-reference medians, and no q-unity physical threshold is asserted.",
      "boundary_behavior": "MW ranges [16.03, 184.15] and lsd_f ranges [0.857, 7.687] in training, both strictly positive, so the expression is finite on every row; no division by zero occurs.",
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.6601115891161025,
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
    "name": "bottleneck_confined_translation",
    "formula": "(MW / MW_ref) * (lsd_f_ref / lsd_f) ** 2",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss grows quadratically with confinement relative to the gas phase; frameworks with smaller passing free-sphere bottlenecks (Df/lsd_f) impose greater translational restriction, so the entropy loss (and hence the MAE-scored association) increases as lsd_f decreases and as adsorbate mass increases.",
    "rationale": "Adsorbed translational degrees of freedom in a narrow channel resemble motion in a tighter effective cell; harmonic/confinement models give entropy loss scaling with the square of the inverse characteristic length. lsd_f (Zeo++ Df) is the largest sphere that can traverse the framework, an empirical bottleneck proxy, not a measured cavity diameter. MW proxies the gas-phase translational reference scale. Limitations: lsd_f is geometry-only, ignores framework chemistry (pure silica so chemistry is uniform), and no claim is made that Df equals the global included diameter Di.",
    "falsification_criteria": "If measured entropy loss is flat or decreasing in lsd_f across frameworks with similar AV, or if the lsd_f^2 power dependence is rejected (e.g., linear or saturating dependence fits better on held-out D0 data), the hypothesis is falsified. Competing mechanism: rotational entropy loss dominating over translational loss for large adsorbates.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f proxies confinement length; MW proxies mass-dependent entropy scale; heavy-atom-derived quantities are not used; transfer across adsorbates assumes shape effects are secondary to mass and bottleneck size.",
      "physical_interpretation": "Native meanings: Df is a passing bottleneck, MW is molecular weight; q-normalization uses fixed positive training-reference medians, and no q-unity physical threshold is asserted.",
      "boundary_behavior": "MW ranges [16.03, 184.15] and lsd_f ranges [0.857, 7.687] in training, both strictly positive, so the expression is finite on every row; no division by zero occurs.",
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.6601115891161025,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/agent/replicate-1/round-1/h2`

最终状态：scored；边际收益：+2.986635 pp；保留：True。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_volume_crowding_entropy",
    "formula": "log(AV_ref / AV) * (Vol / Vol_ref)",
    "hypothesis": "Adsorption entropy loss increases with the logarithm of the inverse of probe-accessible specific framework volume (AV) multiplied by adsorbate van der Waals volume: molecules large relative to the accessible free volume lose more configurational (positional) entropy upon adsorption, independent of bottleneck shape.",
    "rationale": "Configurational entropy of a confined particle scales with accessible phase-space volume; a log-volume contrast is the classical free-volume form. AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume, so the adsorbate volume Vol enters as an explicit multiplicative proxy for relative crowding. Limitations: AV = 0 for 28 training rows (probe inaccessible) would make the log diverge; the hypothesis is therefore declared only for AV > 0 rows and must be branched or excluded for AV = 0 frameworks — this is an honest empirical boundary, not a physical law.",
    "falsification_criteria": "If entropy loss is uncorrelated (or anti-correlated) with the AV-contrast term on frameworks with AV > 0 at matched adsorbate size, the positional-crowding mechanism is falsified. Competing mechanism: adsorbate–surface contact-area effects (LabuteASA-like terms) dominating over free-volume crowding.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Fixed-probe AV approximates the accessible free-volume scale for all adsorbates; Vol/Vol_ref proxies relative crowding; zero-AV frameworks cannot be described and are explicitly excluded from this hypothesis.",
      "physical_interpretation": "AV is probe-accessible specific volume (cm^3/g), Vol is van der Waals volume; the ratio AV_ref/AV is dimensionless via the fixed training-reference median; no physical meaning is assigned to AV = AV_ref.",
      "boundary_behavior": "For AV > 0 the expression is finite for all training Vol; at AV = 0 (28 rows) the descriptor is undefined — the hypothesis predeclares this boundary and requires an explicit rotor/branch or row exclusion rather than median imputation or an arbitrary epsilon.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        0.9
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
    "domain_failure": {
      "invalid_n": 28,
      "invalid_fraction": 0.011859381617958492,
      "zero_variables_on_invalid_rows": {
        "Vol": 0,
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
    "slot_id": "h2",
    "name": "accessible_volume_crowding_entropy",
    "formula": "-log(AV / AV_ref + 1) * (Vol / Vol_ref)",
    "hypothesis": "Adsorption entropy loss increases with the logarithm of the inverse of probe-accessible specific framework volume (AV) multiplied by adsorbate van der Waals volume: molecules large relative to the accessible free volume lose more configurational (positional) entropy upon adsorption, independent of bottleneck shape.",
    "rationale": "Configurational entropy of a confined particle scales with accessible phase-space volume; the descriptor is the negative log of (dimensionless AV contrast + 1), which increases as probe-accessible volume decreases, multiplied by adsorbate van der Waals volume as an explicit crowding proxy. AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume. Limitation: the +1 shift is an empirical smoothing device for AV = 0 rows, not a physical length scale, and the log form is a free-volume-like ansatz, not a derived law.",
    "falsification_criteria": "If entropy loss is uncorrelated (or anti-correlated) with the AV-contrast term on frameworks with AV > 0 at matched adsorbate size, the positional-crowding mechanism is falsified. Also falsified if the compressed-log dependence (saturating in AV) fits worse than a linear AV contrast on held-out data. Competing mechanism: adsorbate–surface contact-area effects dominating over free-volume crowding.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Fixed-probe AV approximates the accessible free-volume scale for all adsorbates; Vol/Vol_ref proxies relative crowding; zero-AV frameworks map to zero descriptor magnitude, an empirical smoothing of an inaccessible-probe boundary, not a physical claim of zero crowding.",
      "physical_interpretation": "AV is probe-accessible specific volume (cm^3/g), Vol is van der Waals volume; AV_ref is the fixed positive training-reference median, so AV/AV_ref is dimensionless and row-varying; no physical meaning is assigned to AV = AV_ref.",
      "boundary_behavior": "AV/AV_ref + 1 >= 1 for all AV >= 0, so the log is defined and finite on every training row, including the 28 zero-AV rows where log(1) = 0 (descriptor vanishes at zero accessibility rather than diverging). Vol is strictly positive. No imputation and no arbitrary epsilon: the +1 is a dimensionless additive constant guaranteeing finiteness on the full observed support.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        0.9
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
      "regime_n": 2162,
      "native_regime_bounds": [
        0.0,
        0.192183
      ],
      "training_spearman": -0.05503466819108541,
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
    "slot_id": "h2",
    "name": "accessible_volume_crowding_entropy",
    "formula": "-log(AV / AV_ref + 1) * (Vol / Vol_ref)",
    "hypothesis": "Adsorption entropy loss increases with the logarithm of the inverse of probe-accessible specific framework volume (AV) multiplied by adsorbate van der Waals volume: molecules large relative to the accessible free volume lose more configurational (positional) entropy upon adsorption, independent of bottleneck shape.",
    "rationale": "Configurational entropy of a confined particle scales with accessible phase-space volume; the descriptor is the negative log of (dimensionless AV contrast + 1), which increases as probe-accessible volume decreases, multiplied by adsorbate van der Waals volume as an explicit crowding proxy. AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume. Limitation: the +1 shift is an empirical smoothing device for AV = 0 rows, not a physical length scale, and the log form is a free-volume-like ansatz, not a derived law.",
    "falsification_criteria": "If entropy loss is uncorrelated (or anti-correlated) with the AV-contrast term on frameworks with AV > 0 at matched adsorbate size, the positional-crowding mechanism is falsified. Also falsified if the compressed-log dependence (saturating in AV) fits worse than a linear AV contrast on held-out data. Competing mechanism: adsorbate–surface contact-area effects dominating over free-volume crowding.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Fixed-probe AV approximates the accessible free-volume scale for all adsorbates; Vol/Vol_ref proxies relative crowding; zero-AV frameworks map to zero descriptor magnitude, an empirical smoothing of an inaccessible-probe boundary, not a physical claim of zero crowding.",
      "physical_interpretation": "AV is probe-accessible specific volume (cm^3/g), Vol is van der Waals volume; AV_ref is the fixed positive training-reference median, so AV/AV_ref is dimensionless and row-varying; no physical meaning is assigned to AV = AV_ref.",
      "boundary_behavior": "AV/AV_ref + 1 >= 1 for all AV >= 0, so the log is defined and finite on every training row, including the 28 zero-AV rows where log(1) = 0 (descriptor vanishes at zero accessibility rather than diverging). Vol is strictly positive. No imputation and no arbitrary epsilon: the +1 is a dimensionless additive constant guaranteeing finiteness on the full observed support.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        0.9
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
      "regime_n": 2162,
      "native_regime_bounds": [
        0.0,
        0.192183
      ],
      "training_spearman": -0.05503466819108541,
      "target_association": "contradicted",
      "perturbation": 0.001538232,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/agent/replicate-1/round-1/h3`

最终状态：scored；边际收益：-2.962924 pp；保留：False。

复核改动字段：rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.regime_input, scientific_test.vary_input

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "planarity_rotor_branch_descriptor",
    "formula": "rotor_case(PBF / PBF_ref, (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref) ** 0.5, log(SPAN / SPAN_ref + 1) * (LabuteASA / LabuteASA_ref))",
    "hypothesis": "Adsorption entropy loss is rotor-class dependent: single-site adsorbates (e.g., methane) lose entropy mainly through positional confinement and scale with a planarity proxy (heavy-atom PBF); linear rotors lose entropy with the geometric mean of their two nontrivial heavy-atom principal moments (PMI2, PMI3); nonlinear rotors lose entropy with a combined extent–surface term (SPAN × LabuteASA in log form). The three branches predeclare distinct entropy-loss mechanisms rather than one universal scaling.",
    "rationale": "Rotational partition functions differ by rotor class (linear has 2 rotational DOF, nonlinear 3), so a single descriptor should misfit; branching by rotor class is the predeclared mechanism separation. PBF, PMI1–3, SPAN, LabuteASA are original heavy-atom/implicit-H proxies: zero PMI or PBF values are legitimate (e.g., single atoms, linear molecules), and zero true all-atom inertia is NOT claimed. The single-site branch uses PBF only (defined and finite for all 54 single-site rows, including zero). The linear branch uses PMI2/PMI3 which are positive for linear molecules (PMI1 near zero is avoided). The nonlinear branch uses log(SPAN_ref-normalized SPAN + 1), finite even at SPAN = 0. Limitations: rotor classification thresholds carry a 1e-10 normalized tolerance and are empirical; heavy-atom moments are not all-atom moments, so hydrogen-rotor contributions are unmodeled.",
    "falsification_criteria": "If a single unbranched descriptor fits held-out D0 entropy losses across rotor classes as well as the branched descriptor (nested model comparison), the rotor-class mechanism separation is falsified. Also falsified if the linear-branch geometric-mean moment dependence has the wrong sign on held-out data. Competing mechanism: framework connectivity (lsd_f/lsd_p contrast), not adsorbate rotor class, driving the residual entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "SPAN": "heavy_atom_enclosing_radius",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies all-atom moments (not equal); rotor_case categories with 1e-10 tolerance are empirical classifications; single-site branch assumes methane-like adsorbates have no meaningful rotational entropy loss captured by heavy-atom inertia, so planarity (PBF) is used instead.",
      "physical_interpretation": "All quantities retain native meanings: PBF is mean atom height above best-fit plane, PMI2/PMI3 are principal moments (Å²·amu) of the implicit-H representation, SPAN is enclosing radius, LabuteASA is approximate surface area; q-normalizations use fixed positive training-reference medians; the +1 inside the log is an empirical smoothing device for zero SPAN rows, not a physical length scale.",
      "boundary_behavior": "Single-site branch: PBF ≥ 0 including legitimate zeros (587 training rows), finite everywhere. Linear branch: PMI2, PMI3 > 0 for linear rotors by construction. Nonlinear branch: log(SPAN/SPAN_ref + 1) finite at SPAN = 0; LabuteASA strictly positive (min 7.45). All branches finite on all 2361 training rows.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "LabuteASA",
        "PBF",
        "PMI2",
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 0,
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
    "name": "planarity_rotor_branch_descriptor",
    "formula": "rotor_case(PBF / PBF_ref, (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref) ** 0.5, log(SPAN / SPAN_ref + 1) * (LabuteASA / LabuteASA_ref))",
    "hypothesis": "Adsorption entropy loss is rotor-class dependent: single-site adsorbates (e.g., methane) lose entropy mainly through positional confinement and scale with a planarity proxy (heavy-atom PBF); linear rotors lose entropy with the geometric mean of their two nontrivial heavy-atom principal moments (PMI2, PMI3); nonlinear rotors lose entropy with a combined extent–surface term (SPAN × LabuteASA in log form). The three branches predeclare distinct entropy-loss mechanisms rather than one universal scaling.",
    "rationale": "Rotational partition functions differ by rotor class (linear has 2 rotational DOF, nonlinear 3), so a single descriptor should misfit; branching by rotor class is the predeclared mechanism separation. PBF, PMI1–3, SPAN, LabuteASA are original heavy-atom/implicit-H proxies: zero PMI or PBF values are legitimate, and zero true all-atom inertia is NOT claimed. The predeclared probe direction is stated on SPAN, which enters the nonlinear branch monotonically increasing; PMI3 enters only the linear branch and is not the declared vary_input. Limitations: rotor classification thresholds are empirical; heavy-atom moments are not all-atom moments, so hydrogen-rotor contributions are unmodeled.",
    "falsification_criteria": "If a single unbranched descriptor fits held-out D0 entropy losses across rotor classes as well as the branched descriptor (nested model comparison), the rotor-class mechanism separation is falsified. Also falsified if the linear-branch geometric-mean moment dependence has the wrong sign on held-out data. Competing mechanism: framework connectivity (lsd_f/lsd_p contrast), not adsorbate rotor class, driving the residual entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "SPAN": "heavy_atom_enclosing_radius",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies all-atom moments (not equal); rotor_case categories with 1e-10 tolerance are empirical classifications; single-site branch assumes methane-like adsorbates have no meaningful rotational entropy loss captured by heavy-atom inertia, so planarity (PBF) is used instead.",
      "physical_interpretation": "All quantities retain native meanings: PBF is mean atom height above best-fit plane, PMI2/PMI3 are principal moments (Å^2·amu) of the implicit-H representation, SPAN is enclosing radius, LabuteASA is approximate surface area; q-normalizations use fixed positive training-reference medians; the +1 inside the log is an empirical smoothing device for zero SPAN rows, not a physical length scale.",
      "boundary_behavior": "Single-site branch: PBF >= 0 including legitimate zeros, finite everywhere. Linear branch: PMI2, PMI3 > 0 for linear rotors by construction. Nonlinear branch: log(SPAN/SPAN_ref + 1) finite at SPAN = 0; LabuteASA strictly positive (min 7.45). All branches finite on all 2361 training rows.",
      "vary_input": "SPAN",
      "descriptor_direction": "increasing",
      "regime_input": "SPAN",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "PBF",
        "PMI2",
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1568,
      "native_regime_bounds": [
        1.432997796,
        3.343750962
      ],
      "training_spearman": 0.2513259677597933,
      "target_association": "consistent",
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
    "slot_id": "h3",
    "name": "planarity_rotor_branch_descriptor",
    "formula": "rotor_case(PBF / PBF_ref, (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref) ** 0.5, log(SPAN / SPAN_ref + 1) * (LabuteASA / LabuteASA_ref))",
    "hypothesis": "Adsorption entropy loss is rotor-class dependent: single-site adsorbates (e.g., methane) lose entropy mainly through positional confinement and scale with a planarity proxy (heavy-atom PBF); linear rotors lose entropy with the geometric mean of their two nontrivial heavy-atom principal moments (PMI2, PMI3); nonlinear rotors lose entropy with a combined extent–surface term (SPAN × LabuteASA in log form). The three branches predeclare distinct entropy-loss mechanisms rather than one universal scaling.",
    "rationale": "Rotational partition functions differ by rotor class (linear has 2 rotational DOF, nonlinear 3), so a single descriptor should misfit; branching by rotor class is the predeclared mechanism separation. PBF, PMI1–3, SPAN, LabuteASA are original heavy-atom/implicit-H proxies: zero PMI or PBF values are legitimate, and zero true all-atom inertia is NOT claimed. The predeclared probe direction is stated on SPAN, which enters the nonlinear branch monotonically increasing; PMI3 enters only the linear branch and is not the declared vary_input. Limitations: rotor classification thresholds are empirical; heavy-atom moments are not all-atom moments, so hydrogen-rotor contributions are unmodeled.",
    "falsification_criteria": "If a single unbranched descriptor fits held-out D0 entropy losses across rotor classes as well as the branched descriptor (nested model comparison), the rotor-class mechanism separation is falsified. Also falsified if the linear-branch geometric-mean moment dependence has the wrong sign on held-out data. Competing mechanism: framework connectivity (lsd_f/lsd_p contrast), not adsorbate rotor class, driving the residual entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "SPAN": "heavy_atom_enclosing_radius",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies all-atom moments (not equal); rotor_case categories with 1e-10 tolerance are empirical classifications; single-site branch assumes methane-like adsorbates have no meaningful rotational entropy loss captured by heavy-atom inertia, so planarity (PBF) is used instead.",
      "physical_interpretation": "All quantities retain native meanings: PBF is mean atom height above best-fit plane, PMI2/PMI3 are principal moments (Å^2·amu) of the implicit-H representation, SPAN is enclosing radius, LabuteASA is approximate surface area; q-normalizations use fixed positive training-reference medians; the +1 inside the log is an empirical smoothing device for zero SPAN rows, not a physical length scale.",
      "boundary_behavior": "Single-site branch: PBF >= 0 including legitimate zeros, finite everywhere. Linear branch: PMI2, PMI3 > 0 for linear rotors by construction. Nonlinear branch: log(SPAN/SPAN_ref + 1) finite at SPAN = 0; LabuteASA strictly positive (min 7.45). All branches finite on all 2361 training rows.",
      "vary_input": "SPAN",
      "descriptor_direction": "increasing",
      "regime_input": "SPAN",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "PBF",
        "PMI2",
        "PMI3",
        "SPAN"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1568,
      "native_regime_bounds": [
        1.432997796,
        3.343750962
      ],
      "training_spearman": 0.2513259677597933,
      "target_association": "consistent",
      "perturbation": 0.02159332416,
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
