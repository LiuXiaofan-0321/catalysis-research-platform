# high/small_kg_rag_agent/replicate-1/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/small_kg_rag_agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`high/small_kg_rag_agent/replicate-1/round-1/h1`

最终状态：scored；边际收益：+3.278410 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, rationale, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "cavity_window_contrast_log",
    "formula": "log(lsd_p / lsd_f)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the logarithmic ratio of the largest included sphere along the free-sphere path (lsd_p, Dif) to the passing bottleneck sphere (lsd_f, Df) is monotonically associated with the dimensionless adsorbed-vs-gas entropy ratio: frameworks with larger cavity-to-window contrast adsorb molecules with smaller translational entropy loss (higher s_ads/s_gas), because the accessible configuration space scales with the included cavity diameter rather than with the window diameter.",
    "rationale": "Mechanism (correlational, not causal): at infinite dilution, the adsorbed translational partition function is governed by the accessible pore space the molecule can explore, which Zeo++ summarizes through Dif along the free path; Df instead measures connectivity windows. A log transform makes the descriptor scale-free and symmetric under proportional changes of both geometric spheres. Limitations: Dif is not the global cavity diameter Di, Df is not a cavity size, both are hard-sphere geometric constructs on a fixed probe definition, and the association is asserted only within the training domain lsd_f in [0.857, 7.687] A and lsd_p in [3.345, 15.560] A. Per the stated baseline, this descriptor only re-expresses published D0-relevant geometric inputs; no independent information is added.",
    "falsification_criteria": "If, holding other inputs fixed in the trained model or in an independent validation set of pure-silica frameworks, the partial association between log(lsd_p/lsd_f) and the entropy loss (in units of R) is not significantly negative (equivalently s_ads/s_gas does not increase with the descriptor), or if the sign flips across framework density strata, the hypothesis is falsified. A competing mechanism would be that entropy loss is governed instead by framework density or accessible volume, with Df/Dif acting only as a correlate.",
    "novelty_status": "uncertain",
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
      "proxy_assumptions": "lsd_p is assumed to track the molecule-accessible configuration space and lsd_f the confinement imposed by periodic windows; both are hard-sphere geometric proxies for a fixed probe and may deviate from the accessible volume of a specific adsorbate with its own van der Waals radius. Transfer beyond pure-silica rigid frameworks or outside the training lsd ranges is not asserted.",
      "physical_interpretation": "lsd_p/lsd_f is a dimensionless geometric contrast between included-along-path and bottleneck spheres on their native Zeo++ definitions. The value 1 has no universal physical meaning as a threshold; it only denotes a channel with no included-cavity widening along the free path.",
      "boundary_behavior": "Both lsd_p (min 3.345 A) and lsd_f (min 0.857 A) are strictly positive across the training domain, so the ratio is positive and the log is finite for every training row; the descriptor approaches 0 as the two spheres coincide (uniform channel) and grows without an imposed cap as contrast grows, with no zero or negative-argument regimes present.",
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
    "name": "cavity_window_contrast_log",
    "formula": "log(lsd_p / lsd_f)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the logarithmic ratio of the largest included sphere along the free-sphere path (lsd_p, Dif) to the passing bottleneck sphere (lsd_f, Df) is monotonically associated with the dimensionless adsorbed-vs-gas entropy ratio: frameworks with larger cavity-to-window contrast adsorb molecules with smaller translational entropy loss (higher s_ads/s_gas), because the accessible configuration space scales with the included cavity diameter rather than with the window diameter.",
    "rationale": "Mechanism (correlational, not causal): the contrast log(lsd_p/lsd_f) compares the largest included sphere ALONG the free-sphere path (Dif) with the passing bottleneck sphere (Df); neither is the global cavity diameter Di, and the hypothesis's reference to a 'cavity diameter' is a conditional proxy mapping, not an equality. Literature reports that smaller average cavity diameter indicates greater confinement and greater rotational entropy loss in a FER/FAU comparison (E02), which motivates — under explicit assumptions — using an included-sphere proxy directionally, but this source does not establish the translational-entropy contrast claimed here. Critically, the training precheck at fixed rotor class found a near-zero Spearman association (-0.019, target_association 'inconclusive') between this descriptor and entropy loss, so the asserted monotone association is currently unsupported in-training and the descriptor may add little beyond collinearity with other framework descriptors. Limitations: hard-sphere geometric constructs for a fixed probe; asserted only within training domains lsd_f in [0.857, 7.687] A and lsd_p in [3.345, 15.560] A; no independent information beyond published D0 inputs.",
    "falsification_criteria": "Given the already inconclusive training association (Spearman -0.019 at fixed rotor class), the hypothesis requires a significantly negative partial association between log(lsd_p/lsd_f) and entropy loss (in units of R) in an independent validation set of pure-silica frameworks; absence of such an association, or a sign flip across framework-density strata, falsifies it. Competing mechanism: entropy loss is governed by accessible volume (AV) or window/bottleneck size, with Df/Dif acting only as correlates.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E02"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "lsd_p is assumed, conditionally, to track the molecule-accessible configuration space along the free path and lsd_f the confinement imposed by periodic windows; both are hard-sphere geometric proxies for a fixed probe and may deviate from the accessible volume of a specific adsorbate. The training precheck association is inconclusive (Spearman -0.019 at fixed rotor class), so transfer of the asserted direction is explicitly not supported by in-training evidence. Transfer beyond pure-silica rigid frameworks or outside the training lsd ranges is not asserted.",
      "physical_interpretation": "lsd_p/lsd_f is a dimensionless geometric contrast between the included-along-path sphere (Dif) and the bottleneck sphere (Df) on their native Zeo++ definitions; since Dif is the largest included sphere along a path that must pass the Df bottleneck, the ratio is expected to be at least 1 along free paths, but the value 1 has no universal physical meaning as a threshold and q-normalization constants are not involved here.",
      "boundary_behavior": "Both lsd_p (min 3.345 A) and lsd_f (min 0.857 A) are strictly positive across the training domain, so the ratio is positive and the log is finite for every training row; the descriptor approaches 0 as the two spheres coincide (uniform channel) and grows without an imposed cap as contrast grows, with no zero or negative-argument regimes present.",
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
    "name": "cavity_window_contrast_log",
    "formula": "log(lsd_p / lsd_f)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the logarithmic ratio of the largest included sphere along the free-sphere path (lsd_p, Dif) to the passing bottleneck sphere (lsd_f, Df) is monotonically associated with the dimensionless adsorbed-vs-gas entropy ratio: frameworks with larger cavity-to-window contrast adsorb molecules with smaller translational entropy loss (higher s_ads/s_gas), because the accessible configuration space scales with the included cavity diameter rather than with the window diameter.",
    "rationale": "Mechanism (correlational, not causal): the contrast log(lsd_p/lsd_f) compares the largest included sphere ALONG the free-sphere path (Dif) with the passing bottleneck sphere (Df); neither is the global cavity diameter Di, and the hypothesis's reference to a 'cavity diameter' is a conditional proxy mapping, not an equality. Literature reports that smaller average cavity diameter indicates greater confinement and greater rotational entropy loss in a FER/FAU comparison (E02), which motivates — under explicit assumptions — using an included-sphere proxy directionally, but this source does not establish the translational-entropy contrast claimed here. Critically, the training precheck at fixed rotor class found a near-zero Spearman association (-0.019, target_association 'inconclusive') between this descriptor and entropy loss, so the asserted monotone association is currently unsupported in-training and the descriptor may add little beyond collinearity with other framework descriptors. Limitations: hard-sphere geometric constructs for a fixed probe; asserted only within training domains lsd_f in [0.857, 7.687] A and lsd_p in [3.345, 15.560] A; no independent information beyond published D0 inputs.",
    "falsification_criteria": "Given the already inconclusive training association (Spearman -0.019 at fixed rotor class), the hypothesis requires a significantly negative partial association between log(lsd_p/lsd_f) and entropy loss (in units of R) in an independent validation set of pure-silica frameworks; absence of such an association, or a sign flip across framework-density strata, falsifies it. Competing mechanism: entropy loss is governed by accessible volume (AV) or window/bottleneck size, with Df/Dif acting only as correlates.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E02"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "lsd_p is assumed, conditionally, to track the molecule-accessible configuration space along the free path and lsd_f the confinement imposed by periodic windows; both are hard-sphere geometric proxies for a fixed probe and may deviate from the accessible volume of a specific adsorbate. The training precheck association is inconclusive (Spearman -0.019 at fixed rotor class), so transfer of the asserted direction is explicitly not supported by in-training evidence. Transfer beyond pure-silica rigid frameworks or outside the training lsd ranges is not asserted.",
      "physical_interpretation": "lsd_p/lsd_f is a dimensionless geometric contrast between the included-along-path sphere (Dif) and the bottleneck sphere (Df) on their native Zeo++ definitions; since Dif is the largest included sphere along a path that must pass the Df bottleneck, the ratio is expected to be at least 1 along free paths, but the value 1 has no universal physical meaning as a threshold and q-normalization constants are not involved here.",
      "boundary_behavior": "Both lsd_p (min 3.345 A) and lsd_f (min 0.857 A) are strictly positive across the training domain, so the ratio is positive and the log is finite for every training row; the descriptor approaches 0 as the two spheres coincide (uniform channel) and grows without an imposed cap as contrast grows, with no zero or negative-argument regimes present.",
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
      "perturbation": 0.0452717,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/small_kg_rag_agent/replicate-1/round-1/h2`

最终状态：scored；边际收益：+0.220146 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "probe_accessibility_confinement_exp",
    "formula": "exp(-(AV / AV_ref))",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the fixed-probe accessible specific volume AV is inversely associated with adsorption entropy loss: frameworks with larger probe-accessible specific volume adsorb molecules with smaller translational entropy loss (higher s_ads/s_gas), so the descriptor exp(-AV/AV_ref) is positively associated with entropy loss (in units of R) and negatively associated with s_ads/s_gas.",
    "rationale": "Mechanism (correlational, not causal): a larger probe-accessible volume per framework mass implies, for a given adsorbate, a larger accessible configuration space and hence less confinement-induced translational entropy loss. The exponential of the negatively signed, q-normalized volume yields a smooth, bounded, monotonically decreasing confinement-type descriptor. Limitations: AV is a fixed-geometric-probe, mass-specific accessibility and is not molecule-specific free volume; its zeros (28 training rows) reflect zero accessibility for that probe and explicitly do not imply zero physical molecular adsorption space, so the descriptor value 1 at AV=0 is a proxy artifact, not a physical saturation of entropy loss. Kinetic escape difficulty does not by itself determine equilibrium entropy. Per the stated baseline, this descriptor only re-expresses a published D0 input.",
    "falsification_criteria": "If the partial association between AV and entropy loss (in units of R) in the trained model or an independent validation set is not significantly negative (equivalently, s_ads/s_gas does not decrease with exp(-AV/AV_ref)), or if the association is dominated by frameworks with AV near zero where the probe metric is uninformative, the hypothesis is falsified. A competing mechanism is that entropy loss is set by bottleneck or molecule-window size effects rather than by probe-accessible volume.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "AV is assumed to be a monotone proxy for the adsorbate-accessible configuration space per framework mass at infinite dilution. It is a fixed-probe quantity; for adsorbates larger or smaller than the probe the proxy degrades, and AV=0 rows are treated as maximally confining by the proxy only, which is an explicit limitation rather than a physical claim.",
      "physical_interpretation": "AV/AV_ref is a dimensionless scaling of the native probe-accessible specific volume by the fixed positive training-reference median; AV_ref carries no universal physical meaning and the exponent -1 is an empirical smoothing choice, not a derived physical law.",
      "boundary_behavior": "AV is non-negative on the training domain [0, 0.661336] cm^3/g. At AV=0 (28 rows) the descriptor equals exp(0)=1, finite and well-defined; as AV grows the descriptor decays smoothly toward 0 with no divergence. No division by AV is performed anywhere in the formula.",
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

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "probe_accessibility_confinement_exp",
    "formula": "exp(-(AV / AV_ref))",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the fixed-probe accessible specific volume AV is inversely associated with adsorption entropy loss: frameworks with larger probe-accessible specific volume adsorb molecules with smaller translational entropy loss (higher s_ads/s_gas), so the descriptor exp(-AV/AV_ref) is positively associated with entropy loss (in units of R) and negatively associated with s_ads/s_gas.",
    "rationale": "Mechanism (correlational, not causal): a larger fixed-probe accessible specific volume AV implies, for a given adsorbate, a larger accessible configuration space and hence less confinement-induced translational entropy loss; the descriptor exp(-AV/AV_ref) decreases with AV, and the training precheck at fixed rotor class shows a consistent positive association between the descriptor and entropy loss (Spearman +0.457), which is consistent with — but does not prove — the proxy mechanism. Literature reports occupiable volume as a useful descriptor of adsorption entropy losses in zeolites (E09) and larger entropy losses in smaller-pore frameworks (E04), supporting conditional use of a volume-type proxy. Limitations: AV is a fixed-geometric-probe, mass-specific accessibility and is not molecule-specific free volume; its zeros (28 training rows) reflect zero accessibility for that probe and do not imply zero physical molecular adsorption space, so the descriptor value 1 at AV=0 is a proxy artifact, not physical saturation of entropy loss. Kinetic escape difficulty does not by itself determine equilibrium entropy. No independent information beyond published D0 inputs.",
    "falsification_criteria": "If the partial association between AV and entropy loss (in units of R) in the trained model or an independent validation set is not significantly negative (equivalently, s_ads/s_gas does not decrease with exp(-AV/AV_ref)), or if the association is dominated by frameworks with AV near zero where the probe metric is uninformative, the hypothesis is falsified. A competing mechanism is that entropy loss is set by bottleneck or molecule-window size effects rather than by probe-accessible volume.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E04",
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
      "proxy_assumptions": "AV is assumed to be a monotone proxy for the adsorbate-accessible configuration space per framework mass at infinite dilution. It is a fixed-probe quantity; for adsorbates larger or smaller than the probe the proxy degrades, and AV=0 rows are treated as maximally confining by the proxy only, which is an explicit limitation rather than a physical claim.",
      "physical_interpretation": "AV/AV_ref is a dimensionless scaling of the native probe-accessible specific volume by the fixed positive training-reference median; AV_ref carries no universal physical meaning and the exponent -1 is an empirical smoothing choice, not a derived physical law.",
      "boundary_behavior": "AV is non-negative on the training domain [0, 0.661336] cm^3/g. At AV=0 (28 rows) the descriptor equals exp(0)=1, finite and well-defined; as AV grows the descriptor decays smoothly toward 0 with no divergence. No division by AV is performed anywhere in the formula.",
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
    "name": "probe_accessibility_confinement_exp",
    "formula": "exp(-(AV / AV_ref))",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the fixed-probe accessible specific volume AV is inversely associated with adsorption entropy loss: frameworks with larger probe-accessible specific volume adsorb molecules with smaller translational entropy loss (higher s_ads/s_gas), so the descriptor exp(-AV/AV_ref) is positively associated with entropy loss (in units of R) and negatively associated with s_ads/s_gas.",
    "rationale": "Mechanism (correlational, not causal): a larger fixed-probe accessible specific volume AV implies, for a given adsorbate, a larger accessible configuration space and hence less confinement-induced translational entropy loss; the descriptor exp(-AV/AV_ref) decreases with AV, and the training precheck at fixed rotor class shows a consistent positive association between the descriptor and entropy loss (Spearman +0.457), which is consistent with — but does not prove — the proxy mechanism. Literature reports occupiable volume as a useful descriptor of adsorption entropy losses in zeolites (E09) and larger entropy losses in smaller-pore frameworks (E04), supporting conditional use of a volume-type proxy. Limitations: AV is a fixed-geometric-probe, mass-specific accessibility and is not molecule-specific free volume; its zeros (28 training rows) reflect zero accessibility for that probe and do not imply zero physical molecular adsorption space, so the descriptor value 1 at AV=0 is a proxy artifact, not physical saturation of entropy loss. Kinetic escape difficulty does not by itself determine equilibrium entropy. No independent information beyond published D0 inputs.",
    "falsification_criteria": "If the partial association between AV and entropy loss (in units of R) in the trained model or an independent validation set is not significantly negative (equivalently, s_ads/s_gas does not decrease with exp(-AV/AV_ref)), or if the association is dominated by frameworks with AV near zero where the probe metric is uninformative, the hypothesis is falsified. A competing mechanism is that entropy loss is set by bottleneck or molecule-window size effects rather than by probe-accessible volume.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E04",
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
      "proxy_assumptions": "AV is assumed to be a monotone proxy for the adsorbate-accessible configuration space per framework mass at infinite dilution. It is a fixed-probe quantity; for adsorbates larger or smaller than the probe the proxy degrades, and AV=0 rows are treated as maximally confining by the proxy only, which is an explicit limitation rather than a physical claim.",
      "physical_interpretation": "AV/AV_ref is a dimensionless scaling of the native probe-accessible specific volume by the fixed positive training-reference median; AV_ref carries no universal physical meaning and the exponent -1 is an empirical smoothing choice, not a derived physical law.",
      "boundary_behavior": "AV is non-negative on the training domain [0, 0.661336] cm^3/g. At AV=0 (28 rows) the descriptor equals exp(0)=1, finite and well-defined; as AV grows the descriptor decays smoothly toward 0 with no divergence. No division by AV is performed anywhere in the formula.",
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

候选标识：`high/small_kg_rag_agent/replicate-1/round-1/h3`

最终状态：scored；边际收益：-2.214554 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "rotor_case_pmi_confinement_log",
    "formula": "rotor_case(1, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 / PMI1_ref) * (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref)))",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the rotational contribution to adsorption entropy loss scales with heavy-atom principal moment-of-inertia proxies in a rotor-class-dependent way: single-site species have no rotational entropy loss term, linear species associate with their single large in-plane moment (PMI2), and nonlinear species associate with the product of all three heavy-atom moments; larger moment proxies predict larger rotational entropy loss (lower s_ads/s_gas) under fixed framework confinement.",
    "rationale": "Mechanism (correlational, not causal): heavier and more extended rotors possess larger gas-phase rotational partition functions, so confining them in a fixed pore geometry removes more rotational entropy than confining light, compact rotors; the log(1+x) form gives a smooth, saturating dimensionless response. The rotor_case branches encode that the relevant number of hindered rotational degrees of freedom differs by rotor class. Limitations: PMI1/PMI2/PMI3 are original implicit-H/heavy-atom proxies, not true all-atom inertias; legitimate zeros exist (54 single-site rows with zero SPAN/PMI proxies, 113 rows with PMI1=0, including linear species with a near-zero small-axis moment), so the single-site branch is a constant and the linear branch deliberately avoids PMI1. The branch assignment uses the stated tolerance of 1e-10 on the native PMI proxy categories. Per the stated baseline, this descriptor only re-expresses published D0 inputs.",
    "falsification_criteria": "If a rotor-class-agnostic formula using a single moment proxy achieves equal or lower entropy-loss MAE than the branched descriptor in cross-validation, or if the sign of the PMI-to-entropy-loss association within any rotor class is non-positive in an independent validation set, the branched hypothesis is falsified. A competing mechanism is that apparent PMI association merely reflects molecular weight or volume collinearity; falsification requires the PMI-product term to add no predictive value after controlling for MW and Vol.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments are assumed to proxy the true all-atom rotational inertia relevant to hindered rotation in pores; this is explicitly a proxy, and no claim is made that true single-atom inertia is zero. Rotor-class branches are the given native PMI proxy categories with 1e-10 tolerance, not quantum-rotor classifications derived here. Transfer across temperature or to flexible frameworks is not asserted.",
      "physical_interpretation": "Each PMI/PMI_ref ratio is a dimensionless scaling of a heavy-atom moment proxy by the fixed positive training-reference median; the reference constants and the exponent 1 carry no universal physical meaning, and log(1+x) is an empirical smoothing choice, not a derived partition-function identity.",
      "boundary_behavior": "Single-site branch: constant 1, finite and independent of zero PMI proxies for the 54 single-site rows. Linear branch: PMI2/PMI2_ref is positive for linear training rows, and log(1+x) is finite even if the moment approaches 0, giving 0. Nonlinear branch: each factor is finite (zero numerator only yields a zero factor, never division by zero since all PMI_ref are positive constants), so log(1+product) is finite for every training row, including rows where any heavy-atom PMI proxy is legitimately zero; the descriptor then smoothly tends to 0, reflecting absence of a rotational-confinement signal from the proxy rather than a physical threshold.",
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
        2414.631462
      ],
      "training_spearman": 0.3493299353761815,
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
    "slot_id": "h3",
    "name": "rotor_case_pmi_confinement_log",
    "formula": "rotor_case(1, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 / PMI1_ref) * (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref)))",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the rotational contribution to adsorption entropy loss scales with heavy-atom principal moment-of-inertia proxies in a rotor-class-dependent way: single-site species have no rotational entropy loss term, linear species associate with their single large in-plane moment (PMI2), and nonlinear species associate with the product of all three heavy-atom moments; larger moment proxies predict larger rotational entropy loss (lower s_ads/s_gas) under fixed framework confinement.",
    "rationale": "Mechanism (correlational, not causal): heavier and more extended rotors possess larger gas-phase rotational partition functions, so confining them in a fixed pore geometry removes more rotational entropy than confining light, compact rotors; the log(1+x) form gives a smooth, saturating dimensionless response. The training precheck at fixed rotor class shows a consistent positive association between the branched descriptor and entropy loss (Spearman +0.349), consistent with — but not proof of — the proxy mechanism. Literature reports greater rotational-degree-of-freedom losses in smaller-pore MFI than FAU (E01) and proposes that rotational freedom relative to available cage space affects adsorption equilibrium (E06); the same literature warns that treating guest molecules as immobile under RRHO overestimates entropy losses (E05), and that implicit-H pseudo-atom models change symmetry numbers and principal moments relative to experiment (E07). The rotor_case branches encode that the number of hindered rotational degrees of freedom differs by rotor class. Limitations: PMI1/PMI2/PMI3 are original implicit-H/heavy-atom proxies, not true all-atom inertias; legitimate zeros exist (54 single-site rows; 113 rows with PMI1=0 including linear species with a near-zero small-axis moment), so the single-site branch is a constant and the linear branch deliberately avoids PMI1. Branch assignment uses the stated 1e-10 tolerance on native PMI proxy categories. No independent information beyond published D0 inputs.",
    "falsification_criteria": "If a rotor-class-agnostic formula using a single moment proxy achieves equal or lower entropy-loss MAE than the branched descriptor in cross-validation, or if the sign of the PMI-to-entropy-loss association within any rotor class is non-positive in an independent validation set, the branched hypothesis is falsified. A competing mechanism is that apparent PMI association merely reflects molecular weight or volume collinearity; falsification requires the PMI-product term to add no predictive value after controlling for MW and Vol.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E05",
      "E06",
      "E07"
    ],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments are assumed to proxy the true all-atom rotational inertia relevant to hindered rotation in pores; this is explicitly a proxy, and no claim is made that true single-atom inertia is zero. Rotor-class branches are the given native PMI proxy categories with 1e-10 tolerance, not quantum-rotor classifications derived here. Transfer across temperature or to flexible frameworks is not asserted.",
      "physical_interpretation": "Each PMI/PMI_ref ratio is a dimensionless scaling of a heavy-atom moment proxy by the fixed positive training-reference median; the reference constants and the exponent 1 carry no universal physical meaning, and log(1+x) is an empirical smoothing choice, not a derived partition-function identity.",
      "boundary_behavior": "Single-site branch: constant 1, finite and independent of zero PMI proxies for the 54 single-site rows. Linear branch: PMI2/PMI2_ref is positive for linear training rows, and log(1+x) is finite even if the moment approaches 0, giving 0. Nonlinear branch: each factor is finite (zero numerator only yields a zero factor, never division by zero since all PMI_ref are positive constants), so log(1+product) is finite for every training row, including rows where any heavy-atom PMI proxy is legitimately zero; the descriptor then smoothly tends to 0, reflecting absence of a rotational-confinement signal from the proxy rather than a physical threshold.",
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
        2414.631462
      ],
      "training_spearman": 0.3493299353761815,
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
    "slot_id": "h3",
    "name": "rotor_case_pmi_confinement_log",
    "formula": "rotor_case(1, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 / PMI1_ref) * (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref)))",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the rotational contribution to adsorption entropy loss scales with heavy-atom principal moment-of-inertia proxies in a rotor-class-dependent way: single-site species have no rotational entropy loss term, linear species associate with their single large in-plane moment (PMI2), and nonlinear species associate with the product of all three heavy-atom moments; larger moment proxies predict larger rotational entropy loss (lower s_ads/s_gas) under fixed framework confinement.",
    "rationale": "Mechanism (correlational, not causal): heavier and more extended rotors possess larger gas-phase rotational partition functions, so confining them in a fixed pore geometry removes more rotational entropy than confining light, compact rotors; the log(1+x) form gives a smooth, saturating dimensionless response. The training precheck at fixed rotor class shows a consistent positive association between the branched descriptor and entropy loss (Spearman +0.349), consistent with — but not proof of — the proxy mechanism. Literature reports greater rotational-degree-of-freedom losses in smaller-pore MFI than FAU (E01) and proposes that rotational freedom relative to available cage space affects adsorption equilibrium (E06); the same literature warns that treating guest molecules as immobile under RRHO overestimates entropy losses (E05), and that implicit-H pseudo-atom models change symmetry numbers and principal moments relative to experiment (E07). The rotor_case branches encode that the number of hindered rotational degrees of freedom differs by rotor class. Limitations: PMI1/PMI2/PMI3 are original implicit-H/heavy-atom proxies, not true all-atom inertias; legitimate zeros exist (54 single-site rows; 113 rows with PMI1=0 including linear species with a near-zero small-axis moment), so the single-site branch is a constant and the linear branch deliberately avoids PMI1. Branch assignment uses the stated 1e-10 tolerance on native PMI proxy categories. No independent information beyond published D0 inputs.",
    "falsification_criteria": "If a rotor-class-agnostic formula using a single moment proxy achieves equal or lower entropy-loss MAE than the branched descriptor in cross-validation, or if the sign of the PMI-to-entropy-loss association within any rotor class is non-positive in an independent validation set, the branched hypothesis is falsified. A competing mechanism is that apparent PMI association merely reflects molecular weight or volume collinearity; falsification requires the PMI-product term to add no predictive value after controlling for MW and Vol.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E05",
      "E06",
      "E07"
    ],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments are assumed to proxy the true all-atom rotational inertia relevant to hindered rotation in pores; this is explicitly a proxy, and no claim is made that true single-atom inertia is zero. Rotor-class branches are the given native PMI proxy categories with 1e-10 tolerance, not quantum-rotor classifications derived here. Transfer across temperature or to flexible frameworks is not asserted.",
      "physical_interpretation": "Each PMI/PMI_ref ratio is a dimensionless scaling of a heavy-atom moment proxy by the fixed positive training-reference median; the reference constants and the exponent 1 carry no universal physical meaning, and log(1+x) is an empirical smoothing choice, not a derived partition-function identity.",
      "boundary_behavior": "Single-site branch: constant 1, finite and independent of zero PMI proxies for the 54 single-site rows. Linear branch: PMI2/PMI2_ref is positive for linear training rows, and log(1+x) is finite even if the moment approaches 0, giving 0. Nonlinear branch: each factor is finite (zero numerator only yields a zero factor, never division by zero since all PMI_ref are positive constants), so log(1+product) is finite for every training row, including rows where any heavy-atom PMI proxy is legitimately zero; the descriptor then smoothly tends to 0, reflecting absence of a rotational-confinement signal from the proxy rather than a physical threshold.",
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
        2414.631462
      ],
      "training_spearman": 0.3493299353761815,
      "target_association": "consistent",
      "perturbation": 4.425680816,
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
        "record_id": "chunk:869af4527dd765744b7ebc76",
        "paper_id": "pmc:pmc8659101",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:8dc09a802942ff3d455ea3a8",
        "paper_id": "doi:10.26434/chemrxiv.9725948.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08aecb87be6d1cda8c6566fa",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08b9bc71084bd99725ff4b87",
        "paper_id": "pmc:pmc10476167",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9fb9ebfc097582b062cf2eb3",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ec1e8193a4e127c7e5a5ba8d",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2a36986d9ba7dbe05f02c0d2",
        "paper_id": "doi:10.1021/acs.langmuir.5b03015",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2cab4c5858c1d76e029f2dbd",
        "paper_id": "pmc:pmc10979502",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2faaf43c7eca6badaaaf64e6",
        "paper_id": "doi:10.1039/d5cp02704g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:50ff57b3007b9882f9485c6b",
        "paper_id": "doi:10.1039/c5cy02140e",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:63a944566fa9e4d1bde391c6",
        "paper_id": "doi:10.1063/1.1781119",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:8c01dc8f239cddb9baf4250d",
        "paper_id": "doi:10.1021/acs.jctc.0c01022",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:977e7f0abbd21eee1d90f8b3",
        "paper_id": "doi:10.1039/b710051e",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9e85d2c34a35aa6bd4d5bf8b",
        "paper_id": "doi:10.1039/d5ce00034c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a37b8c2c0d85816299df600a",
        "paper_id": "pmc:pmc12516733",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d8eef552eba72a99f7974a84",
        "paper_id": "doi:10.1039/b819334g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:00992287f63e5424d7a6b927",
        "paper_id": "doi:10.26434/chemrxiv.7538720.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:0c5531887332394615f4d2ca",
        "paper_id": "doi:10.1002/anie.202007147",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement For rigid pure-silica zeolites at infinite dilution, the logarithmic ratio of the largest included sphere along the free-sphere path (lsd_p, Dif) to the passing bottleneck sphere (lsd_f, Df) is monotonically associated with the dimensionless adsorbed-vs-gas entropy ratio: frameworks with larger cavity-to-window contrast adsorb molecules with smaller translational entropy loss (higher s_ads/s_gas), because the accessible configuration space scales with the included cavity diameter rather than with the window diameter. log(lsd_p / lsd_f) For rigid pure-silica zeolites at infinite dilution, the fixed-probe accessible specific volume AV is inversely associated with adsorption entropy loss: frameworks with larger probe-accessible specific volume adsorb molecules with smaller translational entropy loss (higher s_ads/s_gas), so the descriptor exp(-AV/AV_ref) is positively associated with entropy loss (in units of R) and negatively associated with s_ads/s_gas. exp(-(AV / AV_ref)) For rigid pure-silica zeolites at infinite dilution, the rotational contribution to adsorption entropy loss scales with heavy-atom principal moment-of-inertia proxies in a rotor-class-dependent way: single-site species have no rotational entropy loss term, linear species associate with their single large in-plane moment (PMI2), and nonlinear species associate with the product of all three heavy-atom moments; larger moment proxies predict larger rotational entropy loss (lower s_ads/s_gas) under fixed framework confinement. rotor_case(1, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 / PMI1_ref) * (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref)))",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:01d0cb8bf43d75bbc448e004"
    ],
    "items": 10,
    "lexical_tokens": 4609,
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
      "record_id": "chunk:878e3cf9557831b0616715f9",
      "paper_id": "doi:10.1002/cphc.201701084",
      "document_id": "document:2599bae9c40111b40c45ccef",
      "quote": "and rotational movements of the guest molecule relative to the zeolite host as vibrations under the rigid rotor-harmonic oscillator ( RRHO ) approximation has been shown to overestimate the entropy losses associated with the adsorption of the guest molecules from the gas phase into the zeolite pores . $ ^ { [ 59 , 84 , 85 ] } $ In their study of hydrocarbon adsorption in zeolites, De Moor et al. demonstrated that the entropy cannot be calculated correctly by treating the guest molecules as immobile adsorbates in the RRHO approximation, and that the remaining mobility of the adsorbed species at the active sites needs to be taken into account. $ ^{[85]} $ The authors suggested an alternative, mobile adsorbate calculation, which uses a so-called mobile block analysis of the Hessian (MBH) $ ^{[86,87]} $ to identify those low-frequency modes corresponding to overall global translations and rotations of the guest molecule relative to the framework. Once identified, the contributions of the modes to the partition function are replaced by the correct ones for translational or rotational motions.",
      "locator": {
        "kind": "markdown_section",
        "section": "3.3. thermochemical calculations"
      },
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
      "id": "E05"
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
      "record_id": "chunk:4e0a09f3bacb310a3d0b505c",
      "paper_id": "doi:10.1021/acs.jpcc.0c02671",
      "document_id": "document:679638c993b24ed3004656c6",
      "quote": "gas-phase entropy , i.e . , $ 0 < \\ eta _ { i } < 1 $ . The $ R ^ { 2 } $ correlation coefficients , except for that of FAU , are close to unity , indicating low deviation from the linear trend lines ; the notable deviations for FAU will be discussed later . Linearity in the correlation of $ s_{ads}^{\\infty} $ with $ s_{gas}^{0} $ is the key feature of the results in Figure 1, as it corresponds to qualitatively similar observations in the entropy correlations disclosed in refs 13, 31, and 27. More importantly, though, our results show that the apparent linearity in the correlation of $ s_{ads}^{\\infty} $ with $ s_{gas}^{0} $ persists for a larger set of chemically diverse adsorbates than was previously seen. As discussed in those references, such a simple correlation is an obvious opportunity for the development of an engineering correlation that allows for prediction of the adsorption entropy from a limited set of measurements (whether experimentally or computationally derived). Furthermore, we aim to build on the conclusions in refs 13, 31, and 27 by examining our own data in light of the physical arguments presented previously. As a brief review, the apparent linearity in adsorption entropy correlations derives from fundamental physical considerations. In ref 27, where their linear trend in the entropy correlations was approximately two-third, the authors offered a simplified explanation that the linear trend reflected a loss of approximately one-third of the translational and rotational entropies owing to adsorption. Dauenhauer and Abdelrahman $ ^{13} $ extended this argument to acidic zeolites by considering an additional loss of rotational entropy dependent on the adsorbate size and the pore volume. (Pure linear correlation of $ s_{ads}^{\\infty} $ with $ s_{gas}^{0} $ is broken by the arguments in ref 13, but a visual linear correlation persists. We return to this point later in our work.) Before proceeding, we also note that a numerical comparison between our entropy values and those of ref 13 must be done with care; the gas-phase rotational and translational entropies (i.e., the x-axis of Figure 1) of our TraPPE-model molecules differ from experimental values. This is because the TraPPE molecules include pseudo-atoms, which represent hydrogens implicitly. Although the mass of the TraPPE-model molecules does not change, the symmetry number and principal moments of inertia within the rotational entropy equation are different.",
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
