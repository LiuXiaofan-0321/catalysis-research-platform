# high/small_kg_rag_agent/replicate-1/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/small_kg_rag_agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
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
  }
]
```

## h1

候选标识：`high/small_kg_rag_agent/replicate-1/round-2/h1`

最终状态：scored；边际收益：-2.449898 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "cavity_window_contrast_log",
    "formula": "log(lsd_p / lsd_f)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the logarithmic ratio of the largest included sphere along the free-sphere path (lsd_p, Dif) to the passing bottleneck sphere (lsd_f, Df) is monotonically associated with the dimensionless entropy loss upon adsorption: frameworks with larger cavity-to-window contrast confine molecules in a configuration space set by the included cavity rather than the window, so the entropy loss (per R) decreases as this contrast increases. The hypothesis is stated as an association with entropy loss, not with the raw s_ads/s_gas ratio.",
    "rationale": "Dif exceeds Df on every training row, so the logarithm is always finite and nonnegative. The contrast is a pure geometric path descriptor of the framework and carries no adsorbate information; it can therefore only express the translational component of confinement. The round-1 diagnostics showed an inconclusive native-scale training Spearman (-0.019), so the proposed association remains open and could be falsified by the perturbation test.",
    "falsification_criteria": "If the partial derivative of the model output with respect to lsd_f (rotor class held fixed) does not show the predeclared sign pattern, or if the training-scale Spearman between this descriptor and the entropy loss remains non-informative after retention, the cavity-window contrast mechanism is rejected for this regime; a competing mechanism is that only absolute bottleneck size (lsd_f alone), not the contrast, matters.",
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
      "proxy_assumptions": "Dif/Df is used as a surrogate for cavity-to-window confinement contrast. Neither quantity is the global cavity diameter Di, and the free-sphere path is a geometric simplification that ignores framework flexibility and adsorbate-wall potential shape.",
      "physical_interpretation": "lsd_f is the largest sphere that can pass through the periodic free path (bottleneck); lsd_p is the largest sphere included along that path. Their ratio is dimensionless; no q-normalized value equal to 1 is interpreted as a physical equality threshold.",
      "boundary_behavior": "Both lsd_f and lsd_p are strictly positive over the whole training domain (0.857-7.687 A and 3.345-15.560 A), so the log argument is finite and positive for every row; no zero-handling branch is needed.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_f",
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
    "reason": "Redundant with a current input"
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
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the logarithmic ratio of the largest included sphere along the free-sphere path (lsd_p, Dif) to the passing bottleneck sphere (lsd_f, Df) is monotonically associated with the dimensionless entropy loss upon adsorption: frameworks with larger cavity-to-window contrast confine molecules in a configuration space set by the included cavity rather than the window, so the entropy loss (per R) decreases as this contrast increases. The hypothesis is stated as an association with entropy loss, not with the raw s_ads/s_gas ratio.",
    "rationale": "Expression, variable mappings (lsd_f -> bottleneck_free_sphere_Df, lsd_p -> included_along_free_path_Dif) and boundary behavior are correct and unchanged: lsd_f and lsd_p are strictly positive on the full training domain (0.857-7.687 A and 3.345-15.560 A), and Dif >= Df holds by definition of the included sphere along the free-sphere path, so log(lsd_p/lsd_f) is finite for every row with no zero-handling branch. The training-only precheck rejected this blind re-proposal as 'redundant with a current input': the identical formula is the round-1 retained descriptor in the current model, so the slot is kept as-is rather than re-proposed for scoring. The round-1 native-scale association remains inconclusive (Spearman -0.019), so the cavity-window contrast mechanism stays an unvalidated association, not a causal claim. Conditional grounding: E02 reports greater rotational entropy loss in smaller-cavity zeolites (FER vs FAU) and names average cavity diameter a confinement descriptor; this supports only the sign/direction of a confinement-entropy association and does not justify mapping cavity diameter onto Dif, Df, or their ratio (Dif/Df is neither global Di nor a cavity diameter), and the source-specific FER/FAU percentages are not transferable constants.",
    "falsification_criteria": "If the partial derivative of the model output with respect to lsd_f (rotor class held fixed) does not show the predeclared sign pattern, or if the training-scale Spearman between this descriptor and the entropy loss remains non-informative after retention, the cavity-window contrast mechanism is rejected for this regime; a competing mechanism is that only absolute bottleneck size (lsd_f alone), not the contrast, matters.",
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
      "proxy_assumptions": "Dif/Df is used as a surrogate for cavity-to-window confinement contrast. Neither quantity is the global cavity diameter Di, and the free-sphere path is a geometric simplification that ignores framework flexibility and adsorbate-wall potential shape.",
      "physical_interpretation": "lsd_f is the largest sphere that can pass through the periodic free path (bottleneck); lsd_p is the largest sphere included along that path. Their ratio is dimensionless; no q-normalized value equal to 1 is interpreted as a physical equality threshold.",
      "boundary_behavior": "Both lsd_f and lsd_p are strictly positive over the whole training domain (0.857-7.687 A and 3.345-15.560 A), so the log argument is finite and positive for every row; no zero-handling branch is needed.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_f",
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
    "reason": "Redundant with a current input"
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "cavity_window_contrast_log",
    "formula": "log(1 + (lsd_p - lsd_f) / lsd_f_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the logarithmic ratio of the largest included sphere along the free-sphere path (lsd_p, Dif) to the passing bottleneck sphere (lsd_f, Df) is monotonically associated with the dimensionless entropy loss upon adsorption: frameworks with larger cavity-to-window contrast confine molecules in a configuration space set by the included cavity rather than the window, so the entropy loss (per R) decreases as this contrast increases. The hypothesis is stated as an association with entropy loss, not with the raw s_ads/s_gas ratio.",
    "rationale": "Expression, variable mappings (lsd_f -> bottleneck_free_sphere_Df, lsd_p -> included_along_free_path_Dif) and boundary behavior are correct and unchanged: lsd_f and lsd_p are strictly positive on the full training domain (0.857-7.687 A and 3.345-15.560 A), and Dif >= Df holds by definition of the included sphere along the free-sphere path, so log(lsd_p/lsd_f) is finite for every row with no zero-handling branch. The training-only precheck rejected this blind re-proposal as 'redundant with a current input': the identical formula is the round-1 retained descriptor in the current model, so the slot is kept as-is rather than re-proposed for scoring. The round-1 native-scale association remains inconclusive (Spearman -0.019), so the cavity-window contrast mechanism stays an unvalidated association, not a causal claim. Conditional grounding: E02 reports greater rotational entropy loss in smaller-cavity zeolites (FER vs FAU) and names average cavity diameter a confinement descriptor; this supports only the sign/direction of a confinement-entropy association and does not justify mapping cavity diameter onto Dif, Df, or their ratio (Dif/Df is neither global Di nor a cavity diameter), and the source-specific FER/FAU percentages are not transferable constants.",
    "falsification_criteria": "If the partial derivative of the model output with respect to lsd_f (rotor class held fixed) does not show the predeclared sign pattern, or if the training-scale Spearman between this descriptor and the entropy loss remains non-informative after retention, the cavity-window contrast mechanism is rejected for this regime; a competing mechanism is that only absolute bottleneck size (lsd_f alone), not the contrast, matters.",
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
      "proxy_assumptions": "Dif/Df is used as a surrogate for cavity-to-window confinement contrast. Neither quantity is the global cavity diameter Di, and the free-sphere path is a geometric simplification that ignores framework flexibility and adsorbate-wall potential shape.",
      "physical_interpretation": "lsd_f is the largest sphere that can pass through the periodic free path (bottleneck); lsd_p is the largest sphere included along that path. Their ratio is dimensionless; no q-normalized value equal to 1 is interpreted as a physical equality threshold.",
      "boundary_behavior": "Both lsd_f and lsd_p are strictly positive over the whole training domain (0.857-7.687 A and 3.345-15.560 A), and by the Zeo++ definitions Dif >= Df, so the difference (lsd_p - lsd_f) >= 0 with equality possible for straight, non-constricting channels. The numerator is a difference of two lengths (angstrom - angstrom, unit-compatible), divided by the fixed positive training-reference median lsd_f_ref (angstrom), yielding a dimensionless argument 1 + (lsd_p - lsd_f)/lsd_f_ref >= 1 > 0 for every training row; the logarithm is therefore finite everywhere with no zero-handling branch, no imputation, and no epsilon added to a physical quantity. The additive 1 is a fixed smoothing constant ensuring finiteness at zero contrast and carries no universal physical meaning; no q-value of 1 is treated as a physical equality threshold. This patch replaces the previously redundant exact ratio log(lsd_p/lsd_f) with a reference-normalized contrast difference on a shifted scale: it is an empirically related but not identical descriptor, so the predeclared partial-derivative sign with respect to lsd_f (d/dlsd_f = -1/(lsd_f_ref + lsd_p - lsd_f) < 0, rotor class held fixed) matches the stored decreasing descriptor direction, while the cavity-to-window contrast mechanism remains an unvalidated association, not a causal claim.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_f",
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
        0.85684,
        7.68726
      ],
      "training_spearman": -0.13346318903946128,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/small_kg_rag_agent/replicate-1/round-2/h2`

最终状态：scored；边际收益：+4.247197 pp；保留：True。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "surface_area_mismatch_logdiff",
    "formula": "log(1 + LabuteASA / LabuteASA_ref) - log(1 + ASA / ASA_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica frameworks, the entropy loss per R increases with the mismatch between the adsorbate's molecular surface scale and the framework's probe-accessible specific surface: adsorbates with larger molecular surface area relative to the training reference, adsorbed in frameworks with smaller accessible specific surface relative to its reference, experience stronger surface-contact-imposed configurational restriction, so the descriptor is positively associated with entropy loss. The hypothesis concerns the association with entropy loss itself, not with the s_ads/s_gas ratio.",
    "rationale": "This is a new combination of an adsorbate geometry proxy (LabuteASA) with a framework probe-accessible proxy (ASA), motivated by the round-1 observation that an accessibility-based confinement descriptor (exp(-q_AV)) showed a consistent positive training association (Spearman 0.457) but negligible marginal improvement; surface-area mismatch probes a complementary, molecule-dependent confinement scale. Limitations: ASA is a fixed-probe, mass-specific quantity whose zero does not imply absence of molecular adsorption space, and LabuteASA is an implicit-H approximation, so the descriptor is an empirical confinement index rather than a derived entropy. The probe-accessibility claim is an empirical proxy of framework confinement (probe_volume_proxy), and the surface-mismatch combination is an empirical proxy with no first-principles derivation (empirical_proxy).",
    "falsification_criteria": "If the predeclared derivative sign (descriptor decreasing in ASA at fixed rotor class and fixed LabuteASA) is not reflected in the model's association with entropy loss, or if removing either term breaks a previously positive accessibility association, the surface-mismatch mechanism is falsified; a competing mechanism is that only volumetric accessibility (AV), not surface area, governs translational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA is treated as the contact-area scale of the adsorbate and ASA as the framework's probe-accessible internal surface per mass. Both are proxies: LabuteASA uses an implicit-hydrogen surface, ASA depends on a fixed geometric probe radius, and ASA = 0 for 28 training rows reflects probe inaccessibility, not zero adsorption space. The additive offset of 1 inside each log is a fixed smoothing constant ensuring finiteness at ASA = 0; it carries no universal physical meaning and no q-value of 1 is treated as a physical threshold.",
      "physical_interpretation": "Each log term is dimensionless on the training-reference scale; the difference contrasts adsorbate surface scale against framework accessible surface scale. It is not a physical area ratio because the two areas have different definitions (molecular vs mass-specific probe-accessible).",
      "boundary_behavior": "LabuteASA is strictly positive over training (7.45-80.47 A^2), and ASA >= 0 with 28 legitimate zeros; log(1 + ASA/ASA_ref) remains finite at ASA = 0, so every training row yields a finite value with no imputation.",
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
      "training_spearman": 0.4943539090196363,
      "target_association": "consistent",
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
    "slot_id": "h2",
    "name": "surface_area_mismatch_logdiff",
    "formula": "log(1 + LabuteASA / LabuteASA_ref) - log(1 + ASA / ASA_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica frameworks, the entropy loss per R increases with the mismatch between the adsorbate's molecular surface scale and the framework's probe-accessible specific surface: adsorbates with larger molecular surface area relative to the training reference, adsorbed in frameworks with smaller accessible specific surface relative to its reference, experience stronger surface-contact-imposed configurational restriction, so the descriptor is positively associated with entropy loss. The hypothesis concerns the association with entropy loss itself, not with the s_ads/s_gas ratio.",
    "rationale": "This is a new combination of an adsorbate geometry proxy (LabuteASA) with a framework probe-accessible proxy (ASA), motivated by the round-1 observation that an accessibility-based confinement descriptor (exp(-q_AV)) showed a consistent positive training association (Spearman 0.457) but negligible marginal improvement; surface-area mismatch probes a complementary, molecule-dependent confinement scale. Limitations: ASA is a fixed-probe, mass-specific quantity whose zero does not imply absence of molecular adsorption space, and LabuteASA is an implicit-H approximation, so the descriptor is an empirical confinement index rather than a derived entropy. The probe-accessibility claim is an empirical proxy of framework confinement (probe_volume_proxy), and the surface-mismatch combination is an empirical proxy with no first-principles derivation (empirical_proxy).",
    "falsification_criteria": "If the predeclared derivative sign (descriptor decreasing in ASA at fixed rotor class and fixed LabuteASA) is not reflected in the model's association with entropy loss, or if removing either term breaks a previously positive accessibility association, the surface-mismatch mechanism is falsified; a competing mechanism is that only volumetric accessibility (AV), not surface area, governs translational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA is treated as the contact-area scale of the adsorbate and ASA as the framework's probe-accessible internal surface per mass. Both are proxies: LabuteASA uses an implicit-hydrogen surface, ASA depends on a fixed geometric probe radius, and ASA = 0 for 28 training rows reflects probe inaccessibility, not zero adsorption space. The additive offset of 1 inside each log is a fixed smoothing constant ensuring finiteness at ASA = 0; it carries no universal physical meaning and no q-value of 1 is treated as a physical threshold.",
      "physical_interpretation": "Each log term is dimensionless on the training-reference scale; the difference contrasts adsorbate surface scale against framework accessible surface scale. It is not a physical area ratio because the two areas have different definitions (molecular vs mass-specific probe-accessible).",
      "boundary_behavior": "LabuteASA is strictly positive over training (7.45-80.47 A^2), and ASA >= 0 with 28 legitimate zeros; log(1 + ASA/ASA_ref) remains finite at ASA = 0, so every training row yields a finite value with no imputation.",
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
      "training_spearman": 0.4943539090196363,
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
    "slot_id": "h2",
    "name": "surface_area_mismatch_logdiff",
    "formula": "log(1 + LabuteASA / LabuteASA_ref) - log(1 + ASA / ASA_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica frameworks, the entropy loss per R increases with the mismatch between the adsorbate's molecular surface scale and the framework's probe-accessible specific surface: adsorbates with larger molecular surface area relative to the training reference, adsorbed in frameworks with smaller accessible specific surface relative to its reference, experience stronger surface-contact-imposed configurational restriction, so the descriptor is positively associated with entropy loss. The hypothesis concerns the association with entropy loss itself, not with the s_ads/s_gas ratio.",
    "rationale": "This is a new combination of an adsorbate geometry proxy (LabuteASA) with a framework probe-accessible proxy (ASA), motivated by the round-1 observation that an accessibility-based confinement descriptor (exp(-q_AV)) showed a consistent positive training association (Spearman 0.457) but negligible marginal improvement; surface-area mismatch probes a complementary, molecule-dependent confinement scale. Limitations: ASA is a fixed-probe, mass-specific quantity whose zero does not imply absence of molecular adsorption space, and LabuteASA is an implicit-H approximation, so the descriptor is an empirical confinement index rather than a derived entropy. The probe-accessibility claim is an empirical proxy of framework confinement (probe_volume_proxy), and the surface-mismatch combination is an empirical proxy with no first-principles derivation (empirical_proxy).",
    "falsification_criteria": "If the predeclared derivative sign (descriptor decreasing in ASA at fixed rotor class and fixed LabuteASA) is not reflected in the model's association with entropy loss, or if removing either term breaks a previously positive accessibility association, the surface-mismatch mechanism is falsified; a competing mechanism is that only volumetric accessibility (AV), not surface area, governs translational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA is treated as the contact-area scale of the adsorbate and ASA as the framework's probe-accessible internal surface per mass. Both are proxies: LabuteASA uses an implicit-hydrogen surface, ASA depends on a fixed geometric probe radius, and ASA = 0 for 28 training rows reflects probe inaccessibility, not zero adsorption space. The additive offset of 1 inside each log is a fixed smoothing constant ensuring finiteness at ASA = 0; it carries no universal physical meaning and no q-value of 1 is treated as a physical threshold.",
      "physical_interpretation": "Each log term is dimensionless on the training-reference scale; the difference contrasts adsorbate surface scale against framework accessible surface scale. It is not a physical area ratio because the two areas have different definitions (molecular vs mass-specific probe-accessible).",
      "boundary_behavior": "LabuteASA is strictly positive over training (7.45-80.47 A^2), and ASA >= 0 with 28 legitimate zeros; log(1 + ASA/ASA_ref) remains finite at ASA = 0, so every training row yields a finite value with no imputation.",
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
      "training_spearman": 0.4943539090196363,
      "target_association": "consistent",
      "perturbation": 8.465169999999999,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/small_kg_rag_agent/replicate-1/round-2/h3`

最终状态：scored；边际收益：-1.620940 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "rotor_case_inertia_sum_log",
    "formula": "rotor_case(0.0, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 + PMI2 + PMI3) / (PMI1_ref + PMI2_ref + PMI3_ref)))",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the adsorbed-phase rotational entropy loss per R is monotonically associated with a rotor-class-dependent inertia magnitude proxy: within each rotor class, molecules with larger principal-moment magnitude relative to the training reference (larger, more hindered rotors) suffer larger rotational entropy loss upon confinement, and single-site molecules (for which the heavy-atom PMI proxies are legitimately zero and rotation is not represented) define the zero of this rotational component. The hypothesis concerns the association with entropy loss, not with the s_ads/s_gas ratio.",
    "rationale": "Round-1 rotor-aware descriptors using PMI products showed a consistent but non-retained association; a class-conditional additive inertia magnitude is a distinct, lower-variance rotational hypothesis. The PMI values are heavy-atom, implicit-H proxies: single-site molecules such as methane legitimately have near-zero proxy values, and these zeros are physical representation boundaries, not zero all-atom inertia. The additive normalization uses the sum of the reference values so that the argument is dimensionless and defined even when individual PMI proxies are zero. The explicit rotor_case branches are: single_site branch = constant 0.0; linear branch = log(1 + PMI2 / PMI2_ref); nonlinear branch = log(1 + (PMI1 + PMI2 + PMI3) / (PMI1_ref + PMI2_ref + PMI3_ref)); only the selected branch applies. The descriptor is a nonlinear rotor expression of heavy-atom inertia proxies, used as an empirical proxy for rotational confinement rather than a derived entropy.",
    "falsification_criteria": "If the predeclared derivative sign (descriptor increasing in PMI3 within the nonlinear branch, with the linear and single-site branches held fixed under the class-conditional partial derivative) is contradicted by the model's association with entropy loss, or if the single-site branch constant 0.0 produces systematically biased residuals relative to the linear branch, the class-conditional rotational mechanism is falsified; a competing mechanism is that rotational entropy loss depends on inertia anisotropy rather than inertia magnitude.",
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
      "proxy_assumptions": "PMI1, PMI2, PMI3 are heavy-atom implicit-H principal moments, not true all-atom inertias; their zeros for single-site/linear rows are legitimate representation values. The rotor_case partition uses the native proxy categories with normalized tolerance 1e-10, and only the selected branch applies; the three branch outputs are all dimensionless and unit-compatible. The additive reference sum is a fixed smoothing scale, not a universal physical constant.",
      "physical_interpretation": "Within the linear branch the descriptor is the log of the single meaningful heavy-atom moment (PMI2) on the reference scale; within the nonlinear branch it is the log of the summed moment magnitude on the summed reference scale; for single-site rows the rotational contribution is set to zero because the proxy carries no rotational information. No q-value of 1 is interpreted as a physical equality threshold.",
      "boundary_behavior": "All PMI proxies are >= 0. The single-site branch is the constant 0.0 (finite by construction). Linear rows have PMI2 > 0 on training (PMI2 = 0 only for the 54 single-site rows), and nonlinear rows have strictly positive moment sums, so log(1 + nonnegative/positive) is finite for every training row with no imputation or epsilon added to a physical quantity.",
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
      "training_spearman": 0.40777040084177063,
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
    "name": "rotor_case_inertia_sum_log",
    "formula": "rotor_case(0.0, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 + PMI2 + PMI3) / (PMI1_ref + PMI2_ref + PMI3_ref)))",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the adsorbed-phase rotational entropy loss per R is monotonically associated with a rotor-class-dependent inertia magnitude proxy: within each rotor class, molecules with larger principal-moment magnitude relative to the training reference (larger, more hindered rotors) suffer larger rotational entropy loss upon confinement, and single-site molecules (for which the heavy-atom PMI proxies are legitimately zero and rotation is not represented) define the zero of this rotational component. The hypothesis concerns the association with entropy loss, not with the s_ads/s_gas ratio.",
    "rationale": "Expression, rotor_case branches, normalization by the positive reference sum (PMI1_ref + PMI2_ref + PMI3_ref ~ 262.59), mappings (PMI1/PMI2/PMI3 -> heavy_atom_inertia_proxy), and boundary behavior are correct and unchanged: the single-site branch is the constant 0.0, PMI2 has exactly 54 training zeros matching the 54 single-site rows so the linear-branch log argument is finite for all linear rows, and the nonlinear-branch log argument is 1 + (nonnegative sum)/(positive constant), finite for every row with no imputation. Within the nonlinear branch the partial derivative with respect to PMI3 is 1/(PMI1_ref + PMI2_ref + PMI3_ref + PMI1 + PMI2 + PMI3) > 0, matching the predeclared increasing descriptor direction; in the linear branch PMI3 does not enter, so the derivative claim is class-conditional only. Conditional grounding added: E01 reports a larger loss of rotational degrees of freedom for alkanes in the more confining MFI than FAU, supporting the sign/direction of a rotational-confinement association but not a class-conditional inertia-magnitude law; E08 explicitly warns that implicit-H (united-atom) models change the symmetry number and principal moments of inertia entering the rotational entropy equation, which reinforces that the PMI proxies here are heavy-atom/implicit-H representation values, not true all-atom inertias, and that the descriptor is an empirical_proxy (nonlinear_rotor_expression) with no first-principles derivation.",
    "falsification_criteria": "If the predeclared derivative sign (descriptor increasing in PMI3 within the nonlinear branch, with the linear and single-site branches held fixed under the class-conditional partial derivative) is contradicted by the model's association with entropy loss, or if the single-site branch constant 0.0 produces systematically biased residuals relative to the linear branch, the class-conditional rotational mechanism is falsified; a competing mechanism is that rotational entropy loss depends on inertia anisotropy rather than inertia magnitude.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E08"
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
      "proxy_assumptions": "PMI1, PMI2, PMI3 are heavy-atom implicit-H principal moments, not true all-atom inertias; their zeros for single-site/linear rows are legitimate representation values. The rotor_case partition uses the native proxy categories with normalized tolerance 1e-10, and only the selected branch applies; the three branch outputs are all dimensionless and unit-compatible. The additive reference sum is a fixed smoothing scale, not a universal physical constant.",
      "physical_interpretation": "Within the linear branch the descriptor is the log of the single meaningful heavy-atom moment (PMI2) on the reference scale; within the nonlinear branch it is the log of the summed moment magnitude on the summed reference scale; for single-site rows the rotational contribution is set to zero because the proxy carries no rotational information. No q-value of 1 is interpreted as a physical equality threshold.",
      "boundary_behavior": "All PMI proxies are >= 0. The single-site branch is the constant 0.0 (finite by construction). Linear rows have PMI2 > 0 on training (PMI2 = 0 only for the 54 single-site rows), and nonlinear rows have strictly positive moment sums, so log(1 + nonnegative/positive) is finite for every training row with no imputation or epsilon added to a physical quantity.",
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
      "training_spearman": 0.40777040084177063,
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
    "name": "rotor_case_inertia_sum_log",
    "formula": "rotor_case(0.0, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 + PMI2 + PMI3) / (PMI1_ref + PMI2_ref + PMI3_ref)))",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the adsorbed-phase rotational entropy loss per R is monotonically associated with a rotor-class-dependent inertia magnitude proxy: within each rotor class, molecules with larger principal-moment magnitude relative to the training reference (larger, more hindered rotors) suffer larger rotational entropy loss upon confinement, and single-site molecules (for which the heavy-atom PMI proxies are legitimately zero and rotation is not represented) define the zero of this rotational component. The hypothesis concerns the association with entropy loss, not with the s_ads/s_gas ratio.",
    "rationale": "Expression, rotor_case branches, normalization by the positive reference sum (PMI1_ref + PMI2_ref + PMI3_ref ~ 262.59), mappings (PMI1/PMI2/PMI3 -> heavy_atom_inertia_proxy), and boundary behavior are correct and unchanged: the single-site branch is the constant 0.0, PMI2 has exactly 54 training zeros matching the 54 single-site rows so the linear-branch log argument is finite for all linear rows, and the nonlinear-branch log argument is 1 + (nonnegative sum)/(positive constant), finite for every row with no imputation. Within the nonlinear branch the partial derivative with respect to PMI3 is 1/(PMI1_ref + PMI2_ref + PMI3_ref + PMI1 + PMI2 + PMI3) > 0, matching the predeclared increasing descriptor direction; in the linear branch PMI3 does not enter, so the derivative claim is class-conditional only. Conditional grounding added: E01 reports a larger loss of rotational degrees of freedom for alkanes in the more confining MFI than FAU, supporting the sign/direction of a rotational-confinement association but not a class-conditional inertia-magnitude law; E08 explicitly warns that implicit-H (united-atom) models change the symmetry number and principal moments of inertia entering the rotational entropy equation, which reinforces that the PMI proxies here are heavy-atom/implicit-H representation values, not true all-atom inertias, and that the descriptor is an empirical_proxy (nonlinear_rotor_expression) with no first-principles derivation.",
    "falsification_criteria": "If the predeclared derivative sign (descriptor increasing in PMI3 within the nonlinear branch, with the linear and single-site branches held fixed under the class-conditional partial derivative) is contradicted by the model's association with entropy loss, or if the single-site branch constant 0.0 produces systematically biased residuals relative to the linear branch, the class-conditional rotational mechanism is falsified; a competing mechanism is that rotational entropy loss depends on inertia anisotropy rather than inertia magnitude.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E08"
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
      "proxy_assumptions": "PMI1, PMI2, PMI3 are heavy-atom implicit-H principal moments, not true all-atom inertias; their zeros for single-site/linear rows are legitimate representation values. The rotor_case partition uses the native proxy categories with normalized tolerance 1e-10, and only the selected branch applies; the three branch outputs are all dimensionless and unit-compatible. The additive reference sum is a fixed smoothing scale, not a universal physical constant.",
      "physical_interpretation": "Within the linear branch the descriptor is the log of the single meaningful heavy-atom moment (PMI2) on the reference scale; within the nonlinear branch it is the log of the summed moment magnitude on the summed reference scale; for single-site rows the rotational contribution is set to zero because the proxy carries no rotational information. No q-value of 1 is interpreted as a physical equality threshold.",
      "boundary_behavior": "All PMI proxies are >= 0. The single-site branch is the constant 0.0 (finite by construction). Linear rows have PMI2 > 0 on training (PMI2 = 0 only for the 54 single-site rows), and nonlinear rows have strictly positive moment sums, so log(1 + nonnegative/positive) is finite for every training row with no imputation or epsilon added to a physical quantity.",
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
      "training_spearman": 0.40777040084177063,
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
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2cab4c5858c1d76e029f2dbd",
        "paper_id": "pmc:pmc10979502",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:00992287f63e5424d7a6b927",
        "paper_id": "doi:10.26434/chemrxiv.7538720.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:693d388b69337fcf832845dc",
        "paper_id": "doi:10.26434/chemrxiv.13621391.v1",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b3ea10af92a278cc168d9356",
        "paper_id": "doi:10.1021/la104245c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08b9bc71084bd99725ff4b87",
        "paper_id": "pmc:pmc10476167",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:18de89f2a91a2afad96e693e",
        "paper_id": "doi:10.1007/s00894-024-06004-0",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1985e37bbe922d4eb82c05b3",
        "paper_id": "pmc:pmc12321285",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7213dc4ec87b787dea2346c6",
        "paper_id": "doi:10.1021/acs.jpcc.6b07811",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7bec0989f12cc18693a97a3f",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9d59edc341cdacf2b3d54bfe",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement For rigid pure-silica zeolites at infinite dilution, the logarithmic ratio of the largest included sphere along the free-sphere path (lsd_p, Dif) to the passing bottleneck sphere (lsd_f, Df) is monotonically associated with the dimensionless entropy loss upon adsorption: frameworks with larger cavity-to-window contrast confine molecules in a configuration space set by the included cavity rather than the window, so the entropy loss (per R) decreases as this contrast increases. The hypothesis is stated as an association with entropy loss, not with the raw s_ads/s_gas ratio. log(lsd_p / lsd_f) At infinite dilution in rigid pure-silica frameworks, the entropy loss per R increases with the mismatch between the adsorbate's molecular surface scale and the framework's probe-accessible specific surface: adsorbates with larger molecular surface area relative to the training reference, adsorbed in frameworks with smaller accessible specific surface relative to its reference, experience stronger surface-contact-imposed configurational restriction, so the descriptor is positively associated with entropy loss. The hypothesis concerns the association with entropy loss itself, not with the s_ads/s_gas ratio. log(1 + LabuteASA / LabuteASA_ref) - log(1 + ASA / ASA_ref) For rigid pure-silica zeolites at infinite dilution, the adsorbed-phase rotational entropy loss per R is monotonically associated with a rotor-class-dependent inertia magnitude proxy: within each rotor class, molecules with larger principal-moment magnitude relative to the training reference (larger, more hindered rotors) suffer larger rotational entropy loss upon confinement, and single-site molecules (for which the heavy-atom PMI proxies are legitimately zero and rotation is not represented) define the zero of this rotational component. The hypothesis concerns the association with entropy loss, not with the s_ads/s_gas ratio. rotor_case(0.0, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 + PMI2 + PMI3) / (PMI1_ref + PMI2_ref + PMI3_ref)))   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e9ae89d415e72e1faf77faf0"
    ],
    "items": 10,
    "lexical_tokens": 4759,
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
      "id": "E08"
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
