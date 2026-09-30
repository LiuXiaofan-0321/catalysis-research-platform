# high/small_kg_rag_agent/replicate-1/round-3

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
  },
  {
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
  }
]
```

## h1

候选标识：`high/small_kg_rag_agent/replicate-1/round-3/h1`

最终状态：scored；边际收益：-5.083379 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "volume_confinement_logdiff",
    "formula": "log(1 + Vol / Vol_ref) - log(1 + AV / AV_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the entropy loss per R increases with the mismatch between the adsorbate's van der Waals volume scale and the framework's fixed-probe accessible specific volume scale: adsorbates with larger vdW volume relative to the training reference, adsorbed in frameworks with smaller probe-accessible specific volume relative to its reference, have a smaller accessible configurational volume and therefore a larger entropy loss (smaller s_ads/s_gas). The claim concerns association with entropy loss, not with the ratio itself.",
    "rationale": "Translational configurational space in a cavity scales with the volume available to the molecule; Vol is a whole-molecule vdW volume proxy (all-atom), while AV is a mass-specific accessibility computed for a fixed geometric probe, so a zero AV does not imply zero physical adsorption space for the actual molecule. The log(1+x) forms keep the expression finite across the full training domains (Vol: 20.424-161.144; AV: 0-0.661336 including 28 legitimate zeros) and avoid dividing by AV. Limitations: Vol/AV are proxy scales, the reference constants are training medians without universal physical meaning, and the additive log-difference is an empirical smoothing choice, not a free-volume identity.",
    "falsification_criteria": "If, within the training regime, the descriptor's rank association with entropy loss is not positive (e.g., frameworks with larger AV show larger entropy loss at fixed Vol, or Vol contributes in the opposite sign after controlling for retained descriptors), the free-volume-mismatch mechanism is falsified as stated. A competing mechanism is that fixed-probe accessibility is dominated by window connectivity rather than volume, in which case AV would act through connectivity and the volume term would add no marginal improvement over the retained surface-area-mismatch descriptor.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol proxies the molecular excluded volume that reduces accessible configuration space; AV proxies the framework's accessible free-volume scale for a fixed probe, not molecule-specific free volume; transferability across probe sizes is not assumed.",
      "physical_interpretation": "Native meanings only: larger molecular vdW volume and smaller probe-accessible specific volume correspond to stronger volumetric confinement; q-normalized and _ref terms are dimensionless scalings by training medians with no physical unity threshold.",
      "boundary_behavior": "At AV=0 (legitimate zero for the fixed probe), log(1+AV/AV_ref)=0 and the descriptor reduces to the volume term, finite for every training row; no division by AV occurs. Vol is strictly positive in the training domain so the first log is always defined.",
      "vary_input": "Vol",
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
      "training_spearman": 0.6647556270415259,
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
    "slot_id": "h1",
    "name": "volume_confinement_logdiff",
    "formula": "log(1 + Vol / Vol_ref) - log(1 + AV / AV_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the entropy loss per R increases with the mismatch between the adsorbate's van der Waals volume scale and the framework's fixed-probe accessible specific volume scale: adsorbates with larger vdW volume relative to the training reference, adsorbed in frameworks with smaller probe-accessible specific volume relative to its reference, have a smaller accessible configurational volume and therefore a larger entropy loss (smaller s_ads/s_gas). The claim concerns association with entropy loss, not with the ratio itself.",
    "rationale": "Translational configurational space in a cavity scales with the volume available to the molecule; Vol is a whole-molecule vdW volume proxy (all-atom), while AV is a mass-specific accessibility computed for a fixed geometric probe, so a zero AV does not imply zero physical adsorption space for the actual molecule. The log(1+x) forms keep the expression finite across the full training domains (Vol: 20.424-161.144; AV: 0-0.661336 including 28 legitimate zeros) and avoid dividing by AV. Limitations: Vol/AV are proxy scales, the reference constants are training medians without universal physical meaning, and the additive log-difference is an empirical smoothing choice, not a free-volume identity.",
    "falsification_criteria": "If, within the training regime, the descriptor's rank association with entropy loss is not positive (e.g., frameworks with larger AV show larger entropy loss at fixed Vol, or Vol contributes in the opposite sign after controlling for retained descriptors), the free-volume-mismatch mechanism is falsified as stated. A competing mechanism is that fixed-probe accessibility is dominated by window connectivity rather than volume, in which case AV would act through connectivity and the volume term would add no marginal improvement over the retained surface-area-mismatch descriptor.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol proxies the molecular excluded volume that reduces accessible configuration space; AV proxies the framework's accessible free-volume scale for a fixed probe, not molecule-specific free volume; transferability across probe sizes is not assumed.",
      "physical_interpretation": "Native meanings only: larger molecular vdW volume and smaller probe-accessible specific volume correspond to stronger volumetric confinement; q-normalized and _ref terms are dimensionless scalings by training medians with no physical unity threshold.",
      "boundary_behavior": "At AV=0 (legitimate zero for the fixed probe), log(1+AV/AV_ref)=0 and the descriptor reduces to the volume term, finite for every training row; no division by AV occurs. Vol is strictly positive in the training domain so the first log is always defined.",
      "vary_input": "Vol",
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
      "training_spearman": 0.6647556270415259,
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
    "slot_id": "h1",
    "name": "volume_confinement_logdiff",
    "formula": "log(1 + Vol / Vol_ref) - log(1 + AV / AV_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the entropy loss per R increases with the mismatch between the adsorbate's van der Waals volume scale and the framework's fixed-probe accessible specific volume scale: adsorbates with larger vdW volume relative to the training reference, adsorbed in frameworks with smaller probe-accessible specific volume relative to its reference, have a smaller accessible configurational volume and therefore a larger entropy loss (smaller s_ads/s_gas). The claim concerns association with entropy loss, not with the ratio itself.",
    "rationale": "Translational configurational space in a cavity scales with the volume available to the molecule; Vol is a whole-molecule vdW volume proxy (all-atom), while AV is a mass-specific accessibility computed for a fixed geometric probe, so a zero AV does not imply zero physical adsorption space for the actual molecule. The log(1+x) forms keep the expression finite across the full training domains (Vol: 20.424-161.144; AV: 0-0.661336 including 28 legitimate zeros) and avoid dividing by AV. Limitations: Vol/AV are proxy scales, the reference constants are training medians without universal physical meaning, and the additive log-difference is an empirical smoothing choice, not a free-volume identity.",
    "falsification_criteria": "If, within the training regime, the descriptor's rank association with entropy loss is not positive (e.g., frameworks with larger AV show larger entropy loss at fixed Vol, or Vol contributes in the opposite sign after controlling for retained descriptors), the free-volume-mismatch mechanism is falsified as stated. A competing mechanism is that fixed-probe accessibility is dominated by window connectivity rather than volume, in which case AV would act through connectivity and the volume term would add no marginal improvement over the retained surface-area-mismatch descriptor.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol proxies the molecular excluded volume that reduces accessible configuration space; AV proxies the framework's accessible free-volume scale for a fixed probe, not molecule-specific free volume; transferability across probe sizes is not assumed.",
      "physical_interpretation": "Native meanings only: larger molecular vdW volume and smaller probe-accessible specific volume correspond to stronger volumetric confinement; q-normalized and _ref terms are dimensionless scalings by training medians with no physical unity threshold.",
      "boundary_behavior": "At AV=0 (legitimate zero for the fixed probe), log(1+AV/AV_ref)=0 and the descriptor reduces to the volume term, finite for every training row; no division by AV occurs. Vol is strictly positive in the training domain so the first log is always defined.",
      "vary_input": "Vol",
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
      "training_spearman": 0.6647556270415259,
      "target_association": "consistent",
      "perturbation": 0.7023999999999999,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/small_kg_rag_agent/replicate-1/round-3/h2`

最终状态：scored；边际收益：-7.525267 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "size_cavity_mismatch_logdiff",
    "formula": "log(1 + GeDi / GeDi_ref) - log(1 + lsd_p / lsd_p_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the entropy loss per R increases with the mismatch between the adsorbate's largest heavy-atom pair distance and the framework's largest included sphere along the free-sphere path: molecules whose geometric span relative to the training reference exceeds the included-path diameter relative to its reference experience stronger confinement of orientational and translational configurations, hence larger entropy loss (smaller s_ads/s_gas).",
    "rationale": "GeDi is the largest distance between two molecular atoms in the original implicit-H/heavy-atom representation, a shape proxy, not all-atom geometry; lsd_p is Zeo++ Dif, the included sphere along the free-sphere path, explicitly not the bottleneck Df and not necessarily the global cavity Di. Comparing a molecular long-axis proxy against an included-path diameter tests whether molecule-to-cavity size mismatch restricts configurational freedom. Both inputs are strictly positive in training (GeDi: 0-10.97 with 54 legitimate zeros as numerator only; lsd_p: 3.3452-15.5604), so log(1+x/q) terms are finite everywhere. Limitations: heavy-atom proxies understate hydrogen extents, Dif is path-based rather than a global cavity measure, and the log-difference is an empirical smoothing choice.",
    "falsification_criteria": "If the descriptor's rank association with entropy loss within the training regime is not positive (e.g., larger GeDi at fixed lsd_p correlates with smaller entropy loss, or lsd_p dominates with the opposite sign), the size-mismatch mechanism is falsified. A competing mechanism is that entropy loss is governed by the passing bottleneck lsd_f rather than the included diameter lsd_p; if substituting lsd_f removes the association, the included-path interpretation fails.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi proxies the molecular long-axis extent relevant to orientational confinement; lsd_p proxies the largest confining cavity scale encountered along the percolating path; both are heavy-atom/path geometric proxies with known representation limits.",
      "physical_interpretation": "Largest atom-pair distance and included-along-path sphere diameter in native units; the _ref constants are fixed training medians used only for dimensionless scaling, with no claim that unity of any q-ratio is a physical fitting threshold.",
      "boundary_behavior": "GeDi=0 (legitimate heavy-atom representation zero, e.g., single-site-like entries) gives log(1+0)=0, leaving the finite negative lsd_p term; lsd_p is strictly positive in training so the second log is always defined; every training row yields a finite value without imputation.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
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
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.6550926245135775,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
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
    "name": "size_cavity_mismatch_logdiff",
    "formula": "log(1 + GeDi / GeDi_ref) - log(1 + lsd_p / lsd_p_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the entropy loss per R increases with the mismatch between the adsorbate's largest heavy-atom pair distance and the framework's largest included sphere along the free-sphere path: molecules whose geometric span relative to the training reference exceeds the included-path diameter relative to its reference experience stronger confinement of orientational and translational configurations, hence larger entropy loss (smaller s_ads/s_gas).",
    "rationale": "GeDi is the largest distance between two molecular atoms in the original implicit-H/heavy-atom representation, a shape proxy, not all-atom geometry; it has 54 legitimate zeros (single-site-like rows) in training, at which log(1 + GeDi/GeDi_ref) = 0, so GeDi is NOT strictly positive and the formula must remain finite at those zeros (it is, by the log(1+x) form). lsd_p is Zeo++ Dif, the largest included sphere along the free-sphere path, strictly positive in training (3.3452-15.5604), explicitly not the bottleneck Df and not necessarily the global cavity Di. Comparing a molecular long-axis proxy against an included-path diameter tests whether molecule-to-cavity size mismatch restricts configurational freedom; reported zeolite comparisons attribute larger rotational entropy losses to smaller-cavity frameworks (E01, E02) and motivate gyration-radius-to-cavity-size contrasts (E08), transferred here only conditionally. Both log(1 + x/q) terms are finite across the full training domains. Limitations: heavy-atom proxies understate hydrogen extents, Dif is path-based rather than a global cavity measure, the log-difference is an empirical smoothing choice, the _ref constants are training medians with no universal physical meaning, and training association does not establish causality.",
    "falsification_criteria": "If the descriptor's rank association with entropy loss within the training regime is not positive (e.g., larger GeDi at fixed lsd_p correlates with smaller entropy loss, or lsd_p dominates with the opposite sign), the size-mismatch mechanism is falsified. A competing mechanism is that entropy loss is governed by the passing bottleneck lsd_f rather than the included diameter lsd_p; if substituting lsd_f removes the association, the included-path interpretation fails.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E08"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi proxies the molecular long-axis extent relevant to orientational confinement; lsd_p proxies the largest confining cavity scale encountered along the percolating path; both are heavy-atom/path geometric proxies with known representation limits.",
      "physical_interpretation": "Largest atom-pair distance and included-along-path sphere diameter in native units; the _ref constants are fixed training medians used only for dimensionless scaling, with no claim that unity of any q-ratio is a physical fitting threshold.",
      "boundary_behavior": "GeDi=0 (legitimate heavy-atom representation zero, e.g., single-site-like entries) gives log(1+0)=0, leaving the finite negative lsd_p term; lsd_p is strictly positive in training so the second log is always defined; every training row yields a finite value without imputation.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
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
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.6550926245135775,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
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
    "name": "size_cavity_mismatch_logdiff",
    "formula": "log(1 + GeDi / GeDi_ref) - log(1 + lsd_p / lsd_p_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the entropy loss per R increases with the mismatch between the adsorbate's largest heavy-atom pair distance and the framework's largest included sphere along the free-sphere path: molecules whose geometric span relative to the training reference exceeds the included-path diameter relative to its reference experience stronger confinement of orientational and translational configurations, hence larger entropy loss (smaller s_ads/s_gas).",
    "rationale": "GeDi is the largest distance between two molecular atoms in the original implicit-H/heavy-atom representation, a shape proxy, not all-atom geometry; it has 54 legitimate zeros (single-site-like rows) in training, at which log(1 + GeDi/GeDi_ref) = 0, so GeDi is NOT strictly positive and the formula must remain finite at those zeros (it is, by the log(1+x) form). lsd_p is Zeo++ Dif, the largest included sphere along the free-sphere path, strictly positive in training (3.3452-15.5604), explicitly not the bottleneck Df and not necessarily the global cavity Di. Comparing a molecular long-axis proxy against an included-path diameter tests whether molecule-to-cavity size mismatch restricts configurational freedom; reported zeolite comparisons attribute larger rotational entropy losses to smaller-cavity frameworks (E01, E02) and motivate gyration-radius-to-cavity-size contrasts (E08), transferred here only conditionally. Both log(1 + x/q) terms are finite across the full training domains. Limitations: heavy-atom proxies understate hydrogen extents, Dif is path-based rather than a global cavity measure, the log-difference is an empirical smoothing choice, the _ref constants are training medians with no universal physical meaning, and training association does not establish causality.",
    "falsification_criteria": "If the descriptor's rank association with entropy loss within the training regime is not positive (e.g., larger GeDi at fixed lsd_p correlates with smaller entropy loss, or lsd_p dominates with the opposite sign), the size-mismatch mechanism is falsified. A competing mechanism is that entropy loss is governed by the passing bottleneck lsd_f rather than the included diameter lsd_p; if substituting lsd_f removes the association, the included-path interpretation fails.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E08"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi proxies the molecular long-axis extent relevant to orientational confinement; lsd_p proxies the largest confining cavity scale encountered along the percolating path; both are heavy-atom/path geometric proxies with known representation limits.",
      "physical_interpretation": "Largest atom-pair distance and included-along-path sphere diameter in native units; the _ref constants are fixed training medians used only for dimensionless scaling, with no claim that unity of any q-ratio is a physical fitting threshold.",
      "boundary_behavior": "GeDi=0 (legitimate heavy-atom representation zero, e.g., single-site-like entries) gives log(1+0)=0, leaving the finite negative lsd_p term; lsd_p is strictly positive in training so the second log is always defined; every training row yields a finite value without imputation.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
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
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.6550926245135775,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/small_kg_rag_agent/replicate-1/round-3/h3`

最终状态：scored；边际收益：-10.255891 pp；保留：False。

复核改动字段：scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "planarity_size_coupling",
    "formula": "(PBF / PBF_ref) * log(1 + SPAN / SPAN_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the entropy loss per R is positively associated with the product of the adsorbate's out-of-plane heavy-atom deviation (relative to the training reference) and its heavy-atom enclosing radius (relative to the reference): more nonplanar and larger molecules have more orientational configurations suppressed upon adsorption, so the descriptor increases with entropy loss (decreases s_ads/s_gas).",
    "rationale": "PBF measures mean atom distance from the best-fit molecular plane in the original implicit-H/heavy-atom representation, with legitimate zeros for planar molecules; SPAN is the center-of-mass enclosing radius in the same representation. The coupling term expresses that out-of-plane extent constrains rotational configuration space more strongly when the molecule is geometrically larger, giving a shape-rotation coupling family distinct from the retained surface-area and cavity-contrast descriptors. The derivative with respect to PBF is log(1+SPAN/SPAN_ref)/PBF_ref > 0, and with respect to SPAN is (PBF/PBF_ref)/(SPAN_ref*(1+SPAN/SPAN_ref)) >= 0, so the descriptor is weakly monotone in both inputs. Limitations: these are heavy-atom proxies, not all-atom inertia; the multiplicative coupling is an empirical smoothing choice; _ref constants carry no universal physical meaning; the association is not evidence of causality.",
    "falsification_criteria": "If the descriptor's rank association with entropy loss within the training regime is not positive, or if planar molecules (PBF=0) show entropy losses indistinguishable from nonplanar molecules at matched SPAN, the planarity-size coupling mechanism is falsified as stated. A competing mechanism is that rotational entropy loss is governed by principal moments (rotor class) rather than planarity; if rotor-class-stratified tests remove the association, the PBF-based coupling fails and a nonlinear_rotor_expression formulation would be required instead.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "PBF proxies out-of-plane geometric extent that limits orientational freedom; SPAN proxies overall molecular size amplifying that limitation; both are heavy-atom proxies where zeros are physical (planar molecules), and true all-atom inertia is not assumed to vanish.",
      "physical_interpretation": "Mean plane deviation and center-of-mass enclosing radius in native angstrom units; division by the fixed positive training medians PBF_ref and SPAN_ref makes the product dimensionless with no physical unity threshold.",
      "boundary_behavior": "At PBF=0 (legitimate planar-molecule zero, 587 training rows) the descriptor is exactly 0, finite and interpretable as the planar limit with no rotational suppression from out-of-plane extent; at SPAN=0 (54 legitimate single-site-like rows) the descriptor is 0 since PBF is also 0 for those rows; no division by a native input occurs, only by the fixed positive references, so every training row is finite without imputation.",
      "vary_input": "PBF",
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
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PBF",
        "SPAN"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        6.24082991
      ],
      "training_spearman": 0.3278130937154128,
      "target_association": "consistent",
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
    "slot_id": "h3",
    "name": "planarity_size_coupling",
    "formula": "(PBF / PBF_ref) * log(1 + SPAN / SPAN_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the entropy loss per R is positively associated with the product of the adsorbate's out-of-plane heavy-atom deviation (relative to the training reference) and its heavy-atom enclosing radius (relative to the reference): more nonplanar and larger molecules have more orientational configurations suppressed upon adsorption, so the descriptor increases with entropy loss (decreases s_ads/s_gas).",
    "rationale": "PBF measures mean atom distance from the best-fit molecular plane in the original implicit-H/heavy-atom representation, with legitimate zeros for planar molecules; SPAN is the center-of-mass enclosing radius in the same representation. The coupling term expresses that out-of-plane extent constrains rotational configuration space more strongly when the molecule is geometrically larger, giving a shape-rotation coupling family distinct from the retained surface-area and cavity-contrast descriptors. The derivative with respect to PBF is log(1+SPAN/SPAN_ref)/PBF_ref > 0, and with respect to SPAN is (PBF/PBF_ref)/(SPAN_ref*(1+SPAN/SPAN_ref)) >= 0, so the descriptor is weakly monotone in both inputs. Limitations: these are heavy-atom proxies, not all-atom inertia; the multiplicative coupling is an empirical smoothing choice; _ref constants carry no universal physical meaning; the association is not evidence of causality.",
    "falsification_criteria": "If the descriptor's rank association with entropy loss within the training regime is not positive, or if planar molecules (PBF=0) show entropy losses indistinguishable from nonplanar molecules at matched SPAN, the planarity-size coupling mechanism is falsified as stated. A competing mechanism is that rotational entropy loss is governed by principal moments (rotor class) rather than planarity; if rotor-class-stratified tests remove the association, the PBF-based coupling fails and a nonlinear_rotor_expression formulation would be required instead.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "PBF proxies out-of-plane geometric extent that limits orientational freedom; SPAN proxies overall molecular size amplifying that limitation; both are heavy-atom proxies where zeros are physical (planar molecules, single-site rows), and true all-atom inertia is not assumed to vanish. Transfer from reported cage-rotational comparisons is conditional; the multiplicative coupling is an empirical smoothing choice, not a free-volume or rotor identity.",
      "physical_interpretation": "Mean heavy-atom plane deviation and center-of-mass enclosing radius in native angstrom units; division by the fixed positive training medians PBF_ref and SPAN_ref makes the product dimensionless with no physical unity threshold and no claim that q-ratio = 1 is a fitting boundary.",
      "boundary_behavior": "PBF and SPAN zeros are legitimate physical zeros of the heavy-atom representation (planar molecules; single-site-like rows), not missing data. At SPAN = 0 the second factor is log(1 + 0) = 0, so the descriptor is exactly 0 for ANY PBF value; no claim about the PBF of those rows is needed. At PBF = 0 (587 training rows) the descriptor is also exactly 0. Only division by the fixed positive references PBF_ref and SPAN_ref occurs, never by a native input, so every training row yields a finite value without imputation.",
      "vary_input": "PBF",
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
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PBF",
        "SPAN"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        6.24082991
      ],
      "training_spearman": 0.3278130937154128,
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
    "slot_id": "h3",
    "name": "planarity_size_coupling",
    "formula": "(PBF / PBF_ref) * log(1 + SPAN / SPAN_ref)",
    "hypothesis": "For rigid pure-silica zeolites at infinite dilution, the entropy loss per R is positively associated with the product of the adsorbate's out-of-plane heavy-atom deviation (relative to the training reference) and its heavy-atom enclosing radius (relative to the reference): more nonplanar and larger molecules have more orientational configurations suppressed upon adsorption, so the descriptor increases with entropy loss (decreases s_ads/s_gas).",
    "rationale": "PBF measures mean atom distance from the best-fit molecular plane in the original implicit-H/heavy-atom representation, with legitimate zeros for planar molecules; SPAN is the center-of-mass enclosing radius in the same representation. The coupling term expresses that out-of-plane extent constrains rotational configuration space more strongly when the molecule is geometrically larger, giving a shape-rotation coupling family distinct from the retained surface-area and cavity-contrast descriptors. The derivative with respect to PBF is log(1+SPAN/SPAN_ref)/PBF_ref > 0, and with respect to SPAN is (PBF/PBF_ref)/(SPAN_ref*(1+SPAN/SPAN_ref)) >= 0, so the descriptor is weakly monotone in both inputs. Limitations: these are heavy-atom proxies, not all-atom inertia; the multiplicative coupling is an empirical smoothing choice; _ref constants carry no universal physical meaning; the association is not evidence of causality.",
    "falsification_criteria": "If the descriptor's rank association with entropy loss within the training regime is not positive, or if planar molecules (PBF=0) show entropy losses indistinguishable from nonplanar molecules at matched SPAN, the planarity-size coupling mechanism is falsified as stated. A competing mechanism is that rotational entropy loss is governed by principal moments (rotor class) rather than planarity; if rotor-class-stratified tests remove the association, the PBF-based coupling fails and a nonlinear_rotor_expression formulation would be required instead.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "PBF proxies out-of-plane geometric extent that limits orientational freedom; SPAN proxies overall molecular size amplifying that limitation; both are heavy-atom proxies where zeros are physical (planar molecules, single-site rows), and true all-atom inertia is not assumed to vanish. Transfer from reported cage-rotational comparisons is conditional; the multiplicative coupling is an empirical smoothing choice, not a free-volume or rotor identity.",
      "physical_interpretation": "Mean heavy-atom plane deviation and center-of-mass enclosing radius in native angstrom units; division by the fixed positive training medians PBF_ref and SPAN_ref makes the product dimensionless with no physical unity threshold and no claim that q-ratio = 1 is a fitting boundary.",
      "boundary_behavior": "PBF and SPAN zeros are legitimate physical zeros of the heavy-atom representation (planar molecules; single-site-like rows), not missing data. At SPAN = 0 the second factor is log(1 + 0) = 0, so the descriptor is exactly 0 for ANY PBF value; no claim about the PBF of those rows is needed. At PBF = 0 (587 training rows) the descriptor is also exactly 0. Only division by the fixed positive references PBF_ref and SPAN_ref occurs, never by a native input, so every training row yields a finite value without imputation.",
      "vary_input": "PBF",
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
    "status": "passed",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PBF",
        "SPAN"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        6.24082991
      ],
      "training_spearman": 0.3278130937154128,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
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
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a716c0f2d08195e0bc57308d",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd75db1400cf2ce6171ef0f6",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:522d58342ca7e271d4501291",
        "paper_id": "doi:10.26434/chemrxiv.11695482.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cfbfd9fb0705eed9a2a3f8e",
        "paper_id": "doi:10.1021/acs.langmuir.2c00923",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7213dc4ec87b787dea2346c6",
        "paper_id": "doi:10.1021/acs.jpcc.6b07811",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9805f0a944c903cd7580bbcb",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9fb9ebfc097582b062cf2eb3",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f778ee929c947fcc9e316c34",
        "paper_id": "pmc:pmc12559319",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1feac0dfc9ab0dc8a9a0c9eb",
        "paper_id": "doi:10.1063/1.4706520",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5d62cd81d1c76b19dcdcfff9",
        "paper_id": "doi:10.1021/acs.langmuir.2c00923",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cc904c61f240366bfe7825e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement For rigid pure-silica zeolites at infinite dilution, the entropy loss per R increases with the mismatch between the adsorbate's van der Waals volume scale and the framework's fixed-probe accessible specific volume scale: adsorbates with larger vdW volume relative to the training reference, adsorbed in frameworks with smaller probe-accessible specific volume relative to its reference, have a smaller accessible configurational volume and therefore a larger entropy loss (smaller s_ads/s_gas). The claim concerns association with entropy loss, not with the ratio itself. log(1 + Vol / Vol_ref) - log(1 + AV / AV_ref) For rigid pure-silica zeolites at infinite dilution, the entropy loss per R increases with the mismatch between the adsorbate's largest heavy-atom pair distance and the framework's largest included sphere along the free-sphere path: molecules whose geometric span relative to the training reference exceeds the included-path diameter relative to its reference experience stronger confinement of orientational and translational configurations, hence larger entropy loss (smaller s_ads/s_gas). log(1 + GeDi / GeDi_ref) - log(1 + lsd_p / lsd_p_ref) For rigid pure-silica zeolites at infinite dilution, the entropy loss per R is positively associated with the product of the adsorbate's out-of-plane heavy-atom deviation (relative to the training reference) and its heavy-atom enclosing radius (relative to the reference): more nonplanar and larger molecules have more orientational configurations suppressed upon adsorption, so the descriptor increases with entropy loss (decreases s_ads/s_gas). (PBF / PBF_ref) * log(1 + SPAN / SPAN_ref)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:8dd99e6f4fc8a3c4e46d940b",
      "chunk:8ffcc4698d37d4f5569d53f5",
      "chunk:488a25074219dc1bb01f1486"
    ],
    "items": 10,
    "lexical_tokens": 4773,
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
      "record_id": "chunk:8dd99e6f4fc8a3c4e46d940b",
      "paper_id": "doi:10.1021/acs.jpcc.0c02671",
      "document_id": "document:679638c993b24ed3004656c6",
      "quote": "infty } $ with $ s _ { gas } ^ { 0 } $ is , of course , a highly simplified model of the adsorbed-phase entropy and includes minimal physical insight or intuition . As shown in the next section , one can introduce physically intuitive arguments into more complicated models of entropy than that presented above . 4.3. Empirical Model of Entropy Based on Adsorbent Identity. While the linear entropy scaling in Figures 1 and 3 is quite successful for the TraPPE-based adsorption systems, it is ultimately an oversimplified correlation. We seek a physics-based structure—topology—entropy relationship that is generic and applicable across molecule classes and zeolites. As a first step to this end, motivated by the arguments in refs 13 and 27, we considered a simple linear model wherein each contributor to the entropy is affected differently. However, it has been argued that the translational contribution to the adsorbate entropy (for alkanes) is relatively uniform across frameworks, with the emphasis being on the disparate rotational contributions. $ ^{13,58} $ For example, Denayer et al. have demonstrated that the driving force behind the zeolitic separation of alkane/isoalkane mixtures is exclusively the difference in rotational loss, represented by a ratio between the molecule's radius of gyration with the cavity's largest inscribed van der Waals radius. $ ^{58} $ Therefore, we consider a model where $ s_{ads}^{\\infty} $ is composed of (1) two-third translational entropy (equivalent to the loss of one-third of the gas-phase translational entropy) and (2) a fraction of the gas-phase rotational entropy. As mentioned previously, the vibrational entropy is assumed to be unaffected by adsorption or confinement. We propose the simplest model consistent with the proposition that the adsorbed-phase entropy is composed of the translational and rotational entropies and all of the vibrational entropy of the gas state. Mathematically, this may be stated as $$ s_{\\mathrm{a d s}}^{\\quad\\infty}=\\alpha s_{\\mathrm{t r a n s}}^{0}+\\beta s_{\\mathrm{r o t}}^{0}+s_{\\mathrm{v i b}}^{0} $$ $$ where\\quad\\alpha=2/3\\quad and\\quad0<\\beta<1 $$",
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
