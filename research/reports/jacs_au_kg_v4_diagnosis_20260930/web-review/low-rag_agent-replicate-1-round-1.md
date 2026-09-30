# low/rag_agent/replicate-1/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/rag_agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`low/rag_agent/replicate-1/round-1/h1`

最终状态：rejected；边际收益：未评分；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confined_translation",
    "formula": "log( (lsd_f / 5.16326) * (lsd_p / 6.38663) )",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss increases as the framework bottleneck diameter (lsd_f) and the included diameter along the free path (lsd_p) both shrink relative to training medians, because tighter confining channels restrict translational freedom of the adsorbate within the pore.",
    "rationale": "This is an empirical_proxy combining two native geometric path descriptors on a log scale so the descriptor is symmetric to proportional changes in both bottleneck and channel diameter. It assumes lsd_f and lsd_p jointly capture confinement relevant to translational entropy loss. Limitations: lsd_f is a passing-sphere bottleneck, not the global cavity diameter; lsd_p is the included sphere along the free path, not necessarily the largest cavity. Both inputs are strictly positive across the training domain (min 0.857 and 3.345 angstrom), so the log argument is finite and positive for every training row; no imputation is needed. The fixed reference values 5.16326 and 6.38663 are training medians and carry no universal physical meaning.",
    "falsification_criteria": "If measured entropy loss shows no monotonic association with either lsd_f or lsd_p (partial correlation near zero) when molecular size proxies are held fixed, or if entropy loss is dominated by molecular shape/rotation descriptors rather than path confinement, the hypothesis is falsified for this domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f and lsd_p are geometric proxies for confinement strength; they do not encode framework chemistry, adsorbate identity, or thermal motion. Transfer to other framework compositions is not assumed.",
      "physical_interpretation": "lsd_f is the largest sphere passing through the periodic free path; lsd_p is the largest included sphere along that path. Smaller values mean tighter confinement. The ratio to training medians is a dimensionless normalization only; q = 1 has no physical unity threshold meaning.",
      "boundary_behavior": "Both lsd_f and lsd_p have strictly positive training minima (0.857, 3.345), so the log argument is always finite and positive across all training rows; no zero-division or log-of-zero occurs. Below the training range the descriptor remains finite as long as inputs stay positive.",
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
    "reason": "log requires a dimensionless argument; divide by a matching reference"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confined_translation",
    "formula": "log( (lsd_f / 5.16326) * (lsd_p / 6.38663) )",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss increases as the framework bottleneck diameter (lsd_f) and the included diameter along the free path (lsd_p) both shrink relative to training medians, because tighter confining channels restrict translational freedom of the adsorbate within the pore.",
    "rationale": "Empirical_proxy combining two native geometric path descriptors on a log scale so the descriptor is symmetric to proportional changes in bottleneck and channel diameter. The formula is dimensionally valid: each ratio is dimensionless, so the log argument is dimensionless. lsd_f is the passing-sphere bottleneck (Df), not the global cavity diameter; lsd_p is the included sphere along the free path (Dif), not necessarily the largest cavity Di. Evidence E02/E04 report greater entropy loss in smaller-pore frameworks (FER vs FAU; MFI vs FAU), motivating the confinement direction, but those sources use cavity diameter, not Df/Dif, so the proxy mapping is a hypothesis, not a validated identity. Both inputs are strictly positive across the training domain (min 0.857 and 3.345 angstrom), so the log argument is finite and positive for every training row; no imputation needed. Fixed references 5.16326 and 6.38663 are training medians with no universal physical meaning.",
    "falsification_criteria": "If measured entropy loss shows no monotonic association with either lsd_f or lsd_p (partial correlation near zero) when molecular size proxies are held fixed, or if entropy loss is dominated by molecular shape/rotation descriptors rather than path confinement, the hypothesis is falsified for this domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f and lsd_p are geometric proxies for confinement strength; they do not encode framework chemistry, adsorbate identity, or thermal motion. Transfer to other framework compositions is not assumed.",
      "physical_interpretation": "lsd_f is the largest sphere passing through the periodic free path; lsd_p is the largest included sphere along that path. Smaller values mean tighter confinement. The ratio to training medians is a dimensionless normalization only; q = 1 has no physical unity threshold meaning.",
      "boundary_behavior": "Both lsd_f and lsd_p have strictly positive training minima (0.857, 3.345), so the log argument is always finite and positive across all training rows; no zero-division or log-of-zero occurs. Below the training range the descriptor remains finite as long as inputs stay positive.",
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
    "reason": "log requires a dimensionless argument; divide by a matching reference"
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confined_translation",
    "formula": "log(q_lsd_f * q_lsd_p)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss increases as the framework bottleneck diameter (lsd_f) and the included diameter along the free path (lsd_p) both shrink relative to training medians, because tighter confining channels restrict translational freedom of the adsorbate within the pore.",
    "rationale": "Empirical_proxy combining two native geometric path descriptors on a log scale so the descriptor is symmetric to proportional changes in bottleneck and channel diameter. The formula is dimensionally valid: each ratio is dimensionless, so the log argument is dimensionless. lsd_f is the passing-sphere bottleneck (Df), not the global cavity diameter; lsd_p is the included sphere along the free path (Dif), not necessarily the largest cavity Di. Evidence E02/E04 report greater entropy loss in smaller-pore frameworks (FER vs FAU; MFI vs FAU), motivating the confinement direction, but those sources use cavity diameter, not Df/Dif, so the proxy mapping is a hypothesis, not a validated identity. Both inputs are strictly positive across the training domain (min 0.857 and 3.345 angstrom), so the log argument is finite and positive for every training row; no imputation needed. Fixed references 5.16326 and 6.38663 are training medians with no universal physical meaning.",
    "falsification_criteria": "If measured entropy loss shows no monotonic association with either lsd_f or lsd_p (partial correlation near zero) when molecular size proxies are held fixed, or if entropy loss is dominated by molecular shape/rotation descriptors rather than path confinement, the hypothesis is falsified for this domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f and lsd_p are geometric proxies for confinement strength; they do not encode framework chemistry, adsorbate identity, or thermal motion. Transfer to other framework compositions is not assumed.",
      "physical_interpretation": "lsd_f is the largest sphere passing through the periodic free path; lsd_p is the largest included sphere along that path. Smaller values mean tighter confinement. The ratio to training medians is a dimensionless normalization only; q = 1 has no physical unity threshold meaning.",
      "boundary_behavior": "q_lsd_f = lsd_f/5.16326 and q_lsd_p = lsd_p/6.38663 are dimensionless row-varying ratios with strictly positive training minima (lsd_f >= 0.85684, lsd_p >= 3.3452), so the product is strictly positive and the log argument is dimensionless, finite and positive on every training row; no zero-division, no log-of-nonpositive, no imputation. Fixed references are training medians with no universal physical meaning.",
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

## h2

候选标识：`low/rag_agent/replicate-1/round-1/h2`

最终状态：scored；边际收益：-2.681713 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_case_inertia_entropy",
    "formula": "rotor_case( log(1 + (PMI1 / 43.29513794)**0.5), log(1 + (PMI2 / 93.79729089)**0.5), log(1 + (PMI3 / 125.4948325)**0.5) )",
    "hypothesis": "At infinite dilution, adsorbed-phase rotational entropy loss scales with the smallest principal moment of inertia relevant to the adsorbate's rotor class: single-site molecules (PMI1 near zero, e.g. methane) lose the most rotational entropy upon confinement, linear molecules are governed by PMI2, and nonlinear molecules by PMI3; larger normalized principal moments correspond to less rotational entropy loss.",
    "rationale": "This is a nonlinear_rotor_expression using rotor_case branches keyed on native PMI proxy categories. Each branch uses the principal moment governing the dominant rotational degrees of freedom for that class. sqrt of the normalized moment smooths the wide dynamic range (PMI spans 0 to 2414.6). Limitations: PMI values are computed from the original implicit-H/heavy-atom representation and are NOT true all-atom inertias; zero PMI values for single-site molecules are legitimate proxy zeros, not claims that physical inertia is zero. log(1 + x) keeps each branch finite and non-negative at x = 0. Reference constants are training medians with no universal physical meaning. The branch selection uses the native rotor proxy categories (54 single-site, 214 linear, 2093 nonlinear training rows) with normalized tolerance 1e-10.",
    "falsification_criteria": "If entropy loss for nonlinear adsorbates correlates equally well with PMI1 as with PMI3 (i.e., the choice of branch moment does not improve association), or if shape descriptors (SPAN, PBF) outperform any PMI branch, the rotor-class hypothesis is falsified.",
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
      "proxy_assumptions": "Heavy-atom PMI proxies stand in for true all-atom moments of inertia; the mapping from proxy to physical rotation is empirical and representation-dependent. Single-site molecules (e.g. methane) have legitimate near-zero heavy-atom PMI but nonzero physical rotational entropy in the gas phase.",
      "physical_interpretation": "PMI1/PMI2/PMI3 are the three principal moments from the heavy-atom representation. Branch selection encodes which moment governs active rotational degrees of freedom per rotor class. Normalization by training medians is dimensionless scaling only.",
      "boundary_behavior": "At PMI1 = 0 (single-site branch, 54 training rows), log(1 + 0) = 0, finite. At PMI2 = 0 or PMI3 = 0 (linear/nonlinear branches, 54 rows each), log(1 + 0) = 0, finite. All branches return values in [0, log(1 + max_ratio^0.5)] across the training domain; no imputation or epsilon is added.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.5,
        1.0
      ],
      "entropy_direction": "decreasing"
    }
  },
  "precheck": {
    "status": "rejected",
    "reason": "Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_case_inertia_entropy",
    "formula": "rotor_case( log(1 + (PMI1 / 43.29513794)**0.5), log(1 + (PMI2 / 93.79729089)**0.5), log(1 + (PMI3 / 125.4948325)**0.5) )",
    "hypothesis": "At infinite dilution, adsorbed-phase rotational entropy loss scales with the smallest principal moment of inertia relevant to the adsorbate's rotor class: single-site molecules (PMI1 near zero, e.g. methane) lose the most rotational entropy upon confinement, linear molecules are governed by PMI2, and nonlinear molecules by PMI3; larger normalized principal moments correspond to less rotational entropy loss.",
    "rationale": "nonlinear_rotor_expression using rotor_case branches keyed on native PMI proxy categories. Formula is dimensionless: each branch is log(1 + (PMI/PMI_ref)**0.5) with PMI in angstrom^2*amu divided by a training median in the same unit. PMI values come from the original implicit-H/heavy-atom representation and are NOT true all-atom inertias; legitimate proxy zeros (e.g. methane, single-site) do not mean physical inertia is zero, consistent with E07 noting TraPPE implicit-H models change principal moments of inertia. sqrt smooths the wide dynamic range (PMI3 spans 0 to 2414.6). log(1 + x) keeps each branch finite and non-negative at x = 0. Reference constants are training medians with no universal physical meaning. Branch selection uses native rotor proxy categories (54 single-site, 214 linear, 2093 nonlinear) with normalized tolerance 1e-10. E01 motivates confinement-dependent rotational entropy loss but concerns framework pore size, not PMI magnitude, so the PMI-to-loss association remains a hypothesis.",
    "falsification_criteria": "If entropy loss for nonlinear adsorbates correlates equally well with PMI1 as with PMI3 (i.e., the choice of branch moment does not improve association), or if shape descriptors (SPAN, PBF) outperform any PMI branch, the rotor-class hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E07"
    ],
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
      "proxy_assumptions": "Heavy-atom PMI proxies stand in for true all-atom moments of inertia; the mapping from proxy to physical rotation is empirical and representation-dependent. Single-site molecules (e.g. methane) have legitimate near-zero heavy-atom PMI but nonzero physical rotational entropy in the gas phase.",
      "physical_interpretation": "PMI1/PMI2/PMI3 are the three principal moments from the heavy-atom representation. Branch selection encodes which moment governs active rotational degrees of freedom per rotor class. Normalization by training medians is dimensionless scaling only.",
      "boundary_behavior": "At PMI1 = 0 (single-site branch, 54 training rows), log(1 + 0) = 0, finite. At PMI2 = 0 or PMI3 = 0 (linear/nonlinear branches, 54 rows each), log(1 + 0) = 0, finite. All branches return values in [0, log(1 + max_ratio^0.5)] across the training domain; no imputation or epsilon is added.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.5,
        1.0
      ],
      "entropy_direction": "decreasing"
    }
  },
  "precheck": {
    "status": "rejected",
    "reason": "Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references"
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_case_inertia_entropy",
    "formula": "rotor_case( q_PMI1**0.5, q_PMI2**0.5, q_PMI3**0.5 )",
    "hypothesis": "At infinite dilution, adsorbed-phase rotational entropy loss scales with the smallest principal moment of inertia relevant to the adsorbate's rotor class: single-site molecules (PMI1 near zero, e.g. methane) lose the most rotational entropy upon confinement, linear molecules are governed by PMI2, and nonlinear molecules by PMI3; larger normalized principal moments correspond to less rotational entropy loss.",
    "rationale": "nonlinear_rotor_expression using rotor_case branches keyed on native PMI proxy categories. Formula is dimensionless: each branch is log(1 + (PMI/PMI_ref)**0.5) with PMI in angstrom^2*amu divided by a training median in the same unit. PMI values come from the original implicit-H/heavy-atom representation and are NOT true all-atom inertias; legitimate proxy zeros (e.g. methane, single-site) do not mean physical inertia is zero, consistent with E07 noting TraPPE implicit-H models change principal moments of inertia. sqrt smooths the wide dynamic range (PMI3 spans 0 to 2414.6). log(1 + x) keeps each branch finite and non-negative at x = 0. Reference constants are training medians with no universal physical meaning. Branch selection uses native rotor proxy categories (54 single-site, 214 linear, 2093 nonlinear) with normalized tolerance 1e-10. E01 motivates confinement-dependent rotational entropy loss but concerns framework pore size, not PMI magnitude, so the PMI-to-loss association remains a hypothesis.",
    "falsification_criteria": "If entropy loss for nonlinear adsorbates correlates equally well with PMI1 as with PMI3 (i.e., the choice of branch moment does not improve association), or if shape descriptors (SPAN, PBF) outperform any PMI branch, the rotor-class hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E07"
    ],
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
      "proxy_assumptions": "Heavy-atom PMI proxies stand in for true all-atom moments of inertia; the mapping from proxy to physical rotation is empirical and representation-dependent. Single-site molecules (e.g. methane) have legitimate near-zero heavy-atom PMI but nonzero physical rotational entropy in the gas phase.",
      "physical_interpretation": "PMI1/PMI2/PMI3 are the three principal moments from the heavy-atom representation. Branch selection encodes which moment governs active rotational degrees of freedom per rotor class. Normalization by training medians is dimensionless scaling only.",
      "boundary_behavior": "Each branch is sqrt(PMI/PMI_ref) with PMI and the training-median reference in the same unit (angstrom^2*amu), so each branch is dimensionless. At PMI = 0 (legitimate heavy-atom proxy zeros: 54 single-site rows for PMI1; 54 rows each at PMI2 = 0 or PMI3 = 0 in their branches), sqrt(0) = 0, finite; no epsilon or imputation is added. sqrt smooths the wide PMI3 range (0 to 2414.63). Branch selection uses native rotor proxy categories with tolerance 1e-10; references carry no universal physical meaning. Removing log(1 + ...) avoids any dimensional addition inside the branches.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.5,
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
      "regime_n": 1186,
      "native_regime_bounds": [
        125.4948325,
        2414.631462
      ],
      "training_spearman": 0.2744727202522179,
      "target_association": "contradicted",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/rag_agent/replicate-1/round-1/h3`

最终状态：scored；边际收益：+5.648520 pp；保留：True。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_surface_contrast",
    "formula": "log(1 + (AV / 0.0759781)) - log(1 + (Vol / 67.24))",
    "hypothesis": "At infinite dilution, the balance between probe-accessible framework volume per mass (AV) and adsorbate van der Waals volume (Vol) governs entropy loss: frameworks with more accessible volume relative to the adsorbate's molecular size impose less configurational restriction, so the difference of normalized log accessibilities correlates with entropy loss direction.",
    "rationale": "This is a probe_volume_proxy: the first term grows with framework accessibility (mass-specific, fixed-probe), the second with adsorbate size (Vol), and their contrast encodes the free-space-to-molecule ratio. Limitations: AV is measured with a fixed geometric probe and zero AV (28 training rows) means zero accessibility for that probe, not zero physical adsorption space; the descriptor handles AV = 0 gracefully because log(1 + 0) = 0. Vol is strictly positive (min 20.424), so the second log argument is always > 1. The descriptor is finite for all training rows without imputation. Reference constants are training medians with no universal physical meaning. This contrast does not encode connectivity or kinetic escape explicitly.",
    "falsification_criteria": "If entropy loss association is unchanged when AV is replaced by ASA (surface-area-only term), the volume-specific mechanism claim is falsified in favor of a pure surface-area mechanism. If frameworks with AV = 0 for the fixed probe show the same entropy loss as high-AV frameworks of equal Vol, the accessibility proxy is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV with a fixed probe approximates relative free space available to molecules of varying size; this is a proxy, not a molecule-specific free volume. Vol is the adsorbate's van der Waals volume from the same representation family. Kinetic escape is explicitly excluded as a mechanism here.",
      "physical_interpretation": "AV is probe-accessible volume per framework mass; Vol is adsorbate van der Waals volume. The log-difference measures relative confinement: positive when framework offers more normalized accessibility than the molecule occupies. No unity threshold in q-space is assumed; normalization is scaling only.",
      "boundary_behavior": "At AV = 0 (28 training rows), first term = 0, descriptor = -log(1 + Vol/67.24), finite and negative; this is justified because zero probe accessibility is a legitimate measurement outcome, and the descriptor reports maximal confinement for the fixed probe. Vol is strictly positive so the second term is always finite. No division by zero occurs anywhere in the expression.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "rejected",
    "reason": "Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_surface_contrast",
    "formula": "log(1 + (AV / 0.0759781)) - log(1 + (Vol / 67.24))",
    "hypothesis": "At infinite dilution, the balance between probe-accessible framework volume per mass (AV) and adsorbate van der Waals volume (Vol) governs entropy loss: frameworks with more accessible volume relative to the adsorbate's molecular size impose less configurational restriction, so the difference of normalized log accessibilities correlates with entropy loss direction.",
    "rationale": "probe_volume_proxy: the first term grows with framework probe-accessible volume per mass, the second with adsorbate van der Waals volume; their log-difference is a dimensionless contrast encoding relative confinement. Each ratio is dimensionless, so the subtraction is unit-compatible. Limitations: AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume; zero AV (28 training rows) means zero accessibility for that fixed probe, not zero physical adsorption space, and log(1 + 0) = 0 keeps the descriptor finite there. Vol is strictly positive (min 20.424), so the second log argument is always > 1. No division by zero occurs. Reference constants are training medians with no universal physical meaning. E10 reports that occupiable zeolite volume is a useful descriptor for adsorption entropy losses of alkanes, supporting the direction of association but not validating this exact proxy or causality. The descriptor does not encode pore connectivity or kinetic escape.",
    "falsification_criteria": "If entropy loss association is unchanged when AV is replaced by ASA (surface-area-only term), the volume-specific mechanism claim is falsified in favor of a pure surface-area mechanism. If frameworks with AV = 0 for the fixed probe show the same entropy loss as high-AV frameworks of equal Vol, the accessibility proxy is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E10"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV with a fixed probe approximates relative free space available to molecules of varying size; this is a proxy, not a molecule-specific free volume. Vol is the adsorbate's van der Waals volume from the same representation family. Kinetic escape is explicitly excluded as a mechanism here.",
      "physical_interpretation": "AV is probe-accessible volume per framework mass; Vol is adsorbate van der Waals volume. The log-difference measures relative confinement: positive when framework offers more normalized accessibility than the molecule occupies. No unity threshold in q-space is assumed; normalization is scaling only.",
      "boundary_behavior": "At AV = 0 (28 training rows), first term = 0, descriptor = -log(1 + Vol/67.24), finite and negative; this is justified because zero probe accessibility is a legitimate measurement outcome, and the descriptor reports maximal confinement for the fixed probe. Vol is strictly positive so the second term is always finite. No division by zero occurs anywhere in the expression.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  "precheck": {
    "status": "rejected",
    "reason": "Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references"
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_surface_contrast",
    "formula": "q_AV / q_Vol",
    "hypothesis": "At infinite dilution, the balance between probe-accessible framework volume per mass (AV) and adsorbate van der Waals volume (Vol) governs entropy loss: frameworks with more accessible volume relative to the adsorbate's molecular size impose less configurational restriction, so the difference of normalized log accessibilities correlates with entropy loss direction.",
    "rationale": "probe_volume_proxy: the first term grows with framework probe-accessible volume per mass, the second with adsorbate van der Waals volume; their log-difference is a dimensionless contrast encoding relative confinement. Each ratio is dimensionless, so the subtraction is unit-compatible. Limitations: AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume; zero AV (28 training rows) means zero accessibility for that fixed probe, not zero physical adsorption space, and log(1 + 0) = 0 keeps the descriptor finite there. Vol is strictly positive (min 20.424), so the second log argument is always > 1. No division by zero occurs. Reference constants are training medians with no universal physical meaning. E10 reports that occupiable zeolite volume is a useful descriptor for adsorption entropy losses of alkanes, supporting the direction of association but not validating this exact proxy or causality. The descriptor does not encode pore connectivity or kinetic escape.",
    "falsification_criteria": "If entropy loss association is unchanged when AV is replaced by ASA (surface-area-only term), the volume-specific mechanism claim is falsified in favor of a pure surface-area mechanism. If frameworks with AV = 0 for the fixed probe show the same entropy loss as high-AV frameworks of equal Vol, the accessibility proxy is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E10"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV with a fixed probe approximates relative free space available to molecules of varying size; this is a proxy, not a molecule-specific free volume. Vol is the adsorbate's van der Waals volume from the same representation family. Kinetic escape is explicitly excluded as a mechanism here.",
      "physical_interpretation": "AV is probe-accessible volume per framework mass; Vol is adsorbate van der Waals volume. The log-difference measures relative confinement: positive when framework offers more normalized accessibility than the molecule occupies. No unity threshold in q-space is assumed; normalization is scaling only.",
      "boundary_behavior": "q_AV = AV/0.0759781 and q_Vol = Vol/67.24 are each dimensionless ratios of quantities to same-unit training medians, so the quotient is dimensionless and involves no cross-unit addition or subtraction. Vol is strictly positive (min 20.424 angstrom^3), so no division by zero. At AV = 0 (28 training rows; zero accessibility for the fixed geometric probe, not zero physical adsorption space) the descriptor equals 0, finite, reporting maximal fixed-probe confinement; the descriptor is monotone increasing in AV with Vol fixed, consistent with the hypothesis direction. No log is taken, so the AV = 0 case cannot produce log(0). References are training medians with no universal physical meaning.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
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
      "training_spearman": -0.6742603187530807,
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
    "full_index_rows_in_task_scope": 6004,
    "pending_source_review": [
      {
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd75db1400cf2ce6171ef0f6",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cc904c61f240366bfe7825e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b3ea10af92a278cc168d9356",
        "paper_id": "doi:10.1021/la104245c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e4279277e461f6b17ffc1e17",
        "paper_id": "doi:10.1021/ar200138n",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:166106b9d0f41731d2d72c4f",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3f5768387a8e2dd4104cc2f6",
        "paper_id": "doi:10.1039/c3cc40731d",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f930a6fc9a290a46087a609e",
        "paper_id": "doi:10.1021/jacs.0c09825",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:00992287f63e5424d7a6b927",
        "paper_id": "doi:10.26434/chemrxiv.7538720.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3dd1e3b89a0f8f43f056aaa3",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c515aa77b0e6afe8275e4595",
        "paper_id": "doi:10.1039/d5cs00613a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:dc999f7dfe8539efd7431441",
        "paper_id": "doi:10.1039/d5cs00159e",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:06a26a29dca2516a90c93ace",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, adsorbed-phase translational entropy loss increases as the framework bottleneck diameter (lsd_f) and the included diameter along the free path (lsd_p) both shrink relative to training medians, because tighter confining channels restrict translational freedom of the adsorbate within the pore. log( (lsd_f / 5.16326) * (lsd_p / 6.38663) ) At infinite dilution, adsorbed-phase rotational entropy loss scales with the smallest principal moment of inertia relevant to the adsorbate's rotor class: single-site molecules (PMI1 near zero, e.g. methane) lose the most rotational entropy upon confinement, linear molecules are governed by PMI2, and nonlinear molecules by PMI3; larger normalized principal moments correspond to less rotational entropy loss. rotor_case( log(1 + (PMI1 / 43.29513794)**0.5), log(1 + (PMI2 / 93.79729089)**0.5), log(1 + (PMI3 / 125.4948325)**0.5) ) At infinite dilution, the balance between probe-accessible framework volume per mass (AV) and adsorbate van der Waals volume (Vol) governs entropy loss: frameworks with more accessible volume relative to the adsorbate's molecular size impose less configurational restriction, so the difference of normalized log accessibilities correlates with entropy loss direction. log(1 + (AV / 0.0759781)) - log(1 + (Vol / 67.24))",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e98dff054a73e56b28f6bdf3",
      "chunk:e9ae89d415e72e1faf77faf0"
    ],
    "items": 10,
    "lexical_tokens": 4791,
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
      "id": "E10"
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
