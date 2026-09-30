# high/agent/replicate-2/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h2",
    "name": "heavy_atom_rotor_anisotropy_descriptor",
    "formula": "log(1 + q_PMI3) - log(1 + q_PMI1)",
    "hypothesis": "At infinite dilution in pure-silica (nearly isopotential) frameworks, adsorbates whose heavy-atom principal moments are anisotropic (PMI3 much larger than PMI1, i.e., elongated or disc-like rotors) retain fewer degenerate orientations inside pores than near-spherical rotors of comparable size, so the predeclared association is: entropy loss (s_gas - s_ads)/R INCREASES with this heavy-atom anisotropy descriptor, hence s_ads/s_gas decreases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: in an approximately uniform van der Waals potential, rotational entropy loss on adsorption is governed by how many orientations remain accessible; anisotropic rotors have orientation-dependent excluded volume, so confinement removes more orientational microstates. The anisotropy contrast log(1+q_PMI3) - log(1+q_PMI1) is zero for isotropic heavy-atom tops and grows with elongation/oblateness. Limitations: PMI1 and PMI3 are original implicit-H/heavy-atom proxies; legitimate zeros (linear and single-site species, e.g., methane as single-site) do NOT mean true all-atom inertia or hydrogen-rotor contributions are zero, and symmetry-number effects are not captured. The descriptor re-expresses inputs already in the ANN.",
    "falsification_criteria": "The increasing association fails if (a) rotational entropy loss is dominated by symmetry numbers or all-atom hydrogen rotations uncorrelated with heavy-atom anisotropy, (b) stratifying on rotor_case shows the association vanishes in the single_site branch (where the descriptor is identically 0) yet persists for reasons unrelated to anisotropy in the linear branch, or (c) isotropic rotors in tight bottlenecks lose as much entropy as anisotropic ones, indicating size rather than anisotropy is the operative variable.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI1": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments are assumed monotone proxies for the steric anisotropy that controls orientational degeneracy; all-atom inertia, hydrogen rotations, and symmetry numbers are outside the proxy. Transfer across adsorbate chemistry (pure-silica, no specific binding) is assumed. No physical q-unity threshold is implied.",
      "physical_interpretation": "q_PMI3 = PMI3/PMI3_ref and q_PMI1 = PMI1/PMI1_ref are dimensionless row-varying inputs normalized by fixed training-reference medians (125.4948325 and 43.29513794 angstrom^2*amu); the references are constants and the formula never divides by a native value. Entropy_direction 'increasing' means entropy loss (s_gas - s_ads)/R increases with the descriptor (s_ads/s_gas decreases).",
      "boundary_behavior": "For linear species with legitimate PMI1 = 0, log(1 + q_PMI1) = 0 and the descriptor reduces to log(1 + q_PMI3) > 0, correctly flagging maximal heavy-atom anisotropy. For single-site species with PMI1 = PMI3 = 0, the descriptor is exactly 0, encoding a spherical rotor with no anisotropy term. The descriptor is finite on every training row; the +1 offsets are smoothing constants, not physical moments.",
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
  {
    "slot_id": "h1",
    "name": "cavity_window_contrast_descriptor",
    "formula": "log(q_lsd_p) - log(q_lsd_f)",
    "hypothesis": "In pure-silica frameworks at infinite dilution, the entropy loss (s_gas - s_ads)/R increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, cavity-scale proxy) and the largest passing sphere through the bottleneck (lsd_f, window-scale proxy). Frameworks where lsd_p >> lsd_f confine adsorbates to discrete wide cavities separated by narrow windows, reducing accessible positional/rotational phase space relative to gas; hence s_ads/s_gas decreases as this descriptor increases. This is a predeclared proxy association, not a validated causal mechanism.",
    "rationale": "The original expression combined two different reference medians through q and arbitrary +1 offsets, compressing the contrast and making its magnitude reference-dependent; log(q_lsd_p) - log(q_lsd_f) is the pure dimensionless structural contrast log(lsd_p/lsd_f), which equals 0 for uniform channels and grows with cavity-window disparity. The blind precheck found the offset descriptor's association with entropy loss/R inconclusive (Spearman ~ -0.013), so the predeclared increasing entropy direction remains an open proxy association, not a validated mechanism; the precheck's small perturbation also reflects the compressed dynamic range that this correction removes.",
    "falsification_criteria": "The hypothesis fails if the training Spearman association between log(lsd_p/lsd_f) and entropy loss/R is negligible or opposite to the predeclared increasing direction, or if the marginal MAE improvement over the retained set is non-positive. Competing mechanism: frameworks with high geometric contrast but highly connected window networks (many equivalent paths, not captured by a single Df bottleneck) may retain adsorbed entropy, showing that a single-bottleneck contrast proxy is insufficient.",
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
      "proxy_assumptions": "lsd_p (Zeo++ Dif) is the largest included sphere along the free-sphere path and lsd_f (Df) is the largest passing bottleneck; both are rigid hard-sphere proxies. Neither measures the global cavity diameter Di, wall chemistry, defects, window-network multiplicity, or adsorbate flexibility. The blind precheck on the offset version log(1 + q_lsd_p) - log(1 + q_lsd_f) returned a negligible training association (Spearman ~ -0.013, inconclusive); this offset-free reparameterization is closely rank-related, so its association with entropy loss/R must be treated as open and unvalidated, not established.",
      "physical_interpretation": "Descriptor is the scale-free log contrast between the along-path included sphere and the passing bottleneck; larger values indicate relatively wide included regions accessible behind relatively tight windows in the free-sphere path graph. The training-reference medians cancel exactly, so unlike the offset version the descriptor is independent of the arbitrary reference values, and the +1 constants (which carried no universal physical meaning) are removed. The original draft's description of lsd_p as a 'cavity-scale proxy' is corrected: lsd_p is the included sphere along the free-sphere path, not the global cavity diameter Di.",
      "boundary_behavior": "lsd_f and lsd_p are strictly positive on every training row (min 0.85684 A and 3.3452 A), so q_lsd_f and q_lsd_f-derived quantities are strictly positive and both log arguments are valid; the descriptor is finite on every row with no zero branch and no added epsilon. Since the along-path included sphere Dif satisfies Dif >= Df for every framework, log(q_lsd_p) - log(q_lsd_f) = log(lsd_p/lsd_f) >= 0, and it equals 0 exactly for uniform channels where the included sphere along the path equals the passing bottleneck.",
      "vary_input": "lsd_p",
      "descriptor_direction": "increasing",
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

候选标识：`high/agent/replicate-2/round-3/h1`

最终状态：scored；边际收益：-5.003042 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "size_accessibility_contrast_descriptor",
    "formula": "log(1 + q_Vol) - log(1 + q_AV)",
    "hypothesis": "At infinite dilution in pure-silica (nearly isopotential) frameworks, the entropy loss (s_gas - s_ads)/R increases with the adsorbate van der Waals volume relative to the framework's probe-accessible specific volume: molecules large compared with the accessible void space retain fewer adsorbed positional microstates relative to the gas. The predeclared proxy derivative of entropy loss with respect to this descriptor is positive (descriptor_direction increasing in q_Vol at fixed framework accessibility), so entropy loss increases and s_ads/s_gas decreases as the descriptor increases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: translational phase-space restriction scales with excluded-volume demand relative to available free space. q_Vol and q_AV are row-varying dimensionless inputs normalized by fixed training-reference medians (Vol_ref = 67.24 angstrom^3, AV_ref = 0.0759781 cm^3/g); their difference is dimensionless and carries no physical meaning at q = 1. Limitation: all 14 published D0 inputs already enter the nonlinear ANN, so this descriptor only re-expresses existing inputs; the open question is whether this physically motivated re-expression exposes association structure the model otherwise misses. AV is a fixed-probe, mass-specific accessibility, not a molecule-specific free volume, so the contrast is a geometric surrogate only.",
    "falsification_criteria": "Falsified if, within a fixed framework (q_AV fixed), the training association of entropy loss with q_Vol is negative, or if replacing q_AV with q_lsd_f in the same difference yields an equal-or-better association and the AV term adds no marginal improvement (i.e., bottleneck geometry rather than accessible volume governs confinement). Competing mechanism: window/bottleneck control of translational entropy loss.",
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
      "proxy_assumptions": "Vol proxies the molecule's translational excluded-volume demand; AV proxies framework free space for a fixed geometric probe. Both are static geometric surrogates; transfer across adsorbate sizes is limited because the probe is not molecule-specific, and zero AV does not imply zero physical adsorption space.",
      "physical_interpretation": "Native meanings: Vol is the adsorbate van der Waals volume; AV is probe-accessible volume per framework mass. Normalization by fixed reference medians makes the terms dimensionless and row-varying; q = 1 is a bookkeeping reference, not an equality threshold.",
      "boundary_behavior": "AV = 0 occurs for 28 training rows (fixed-probe inaccessibility); there log(1 + q_AV) = 0 and the descriptor reduces to log(1 + q_Vol), which is finite and carries no accessibility information rather than an imputed value. Vol has no zeros in the training domain (min 20.424 angstrom^3).",
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
    "name": "size_accessibility_contrast_descriptor",
    "formula": "log(1 + q_Vol) - log(1 + q_AV)",
    "hypothesis": "At infinite dilution in pure-silica (nearly isopotential) frameworks, the entropy loss (s_gas - s_ads)/R increases with the adsorbate van der Waals volume relative to the framework's probe-accessible specific volume: molecules large compared with the accessible void space retain fewer adsorbed positional microstates relative to the gas. The predeclared proxy derivative of entropy loss with respect to this descriptor is positive (descriptor_direction increasing in q_Vol at fixed framework accessibility), so entropy loss increases and s_ads/s_gas decreases as the descriptor increases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: translational phase-space restriction scales with excluded-volume demand relative to available free space. q_Vol and q_AV are row-varying dimensionless inputs normalized by fixed training-reference medians (Vol_ref = 67.24 angstrom^3, AV_ref = 0.0759781 cm^3/g); their difference is dimensionless and carries no physical meaning at q = 1. Limitation: all 14 published D0 inputs already enter the nonlinear ANN, so this descriptor only re-expresses existing inputs; the open question is whether this physically motivated re-expression exposes association structure the model otherwise misses. AV is a fixed-probe, mass-specific accessibility, not a molecule-specific free volume, so the contrast is a geometric surrogate only.",
    "falsification_criteria": "Falsified if, within a fixed framework (q_AV fixed), the training association of entropy loss with q_Vol is negative, or if replacing q_AV with q_lsd_f in the same difference yields an equal-or-better association and the AV term adds no marginal improvement (i.e., bottleneck geometry rather than accessible volume governs confinement). Competing mechanism: window/bottleneck control of translational entropy loss.",
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
      "proxy_assumptions": "Vol proxies the molecule's translational excluded-volume demand; AV proxies framework free space for a fixed geometric probe. Both are static geometric surrogates; transfer across adsorbate sizes is limited because the probe is not molecule-specific, and zero AV does not imply zero physical adsorption space.",
      "physical_interpretation": "Native meanings: Vol is the adsorbate van der Waals volume; AV is probe-accessible volume per framework mass. Normalization by fixed reference medians makes the terms dimensionless and row-varying; q = 1 is a bookkeeping reference, not an equality threshold.",
      "boundary_behavior": "AV = 0 occurs for 28 training rows (fixed-probe inaccessibility); there log(1 + q_AV) = 0 and the descriptor reduces to log(1 + q_Vol), which is finite and carries no accessibility information rather than an imputed value. Vol has no zeros in the training domain (min 20.424 angstrom^3).",
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
    "name": "size_accessibility_contrast_descriptor",
    "formula": "log(1 + q_Vol) - log(1 + q_AV)",
    "hypothesis": "At infinite dilution in pure-silica (nearly isopotential) frameworks, the entropy loss (s_gas - s_ads)/R increases with the adsorbate van der Waals volume relative to the framework's probe-accessible specific volume: molecules large compared with the accessible void space retain fewer adsorbed positional microstates relative to the gas. The predeclared proxy derivative of entropy loss with respect to this descriptor is positive (descriptor_direction increasing in q_Vol at fixed framework accessibility), so entropy loss increases and s_ads/s_gas decreases as the descriptor increases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: translational phase-space restriction scales with excluded-volume demand relative to available free space. q_Vol and q_AV are row-varying dimensionless inputs normalized by fixed training-reference medians (Vol_ref = 67.24 angstrom^3, AV_ref = 0.0759781 cm^3/g); their difference is dimensionless and carries no physical meaning at q = 1. Limitation: all 14 published D0 inputs already enter the nonlinear ANN, so this descriptor only re-expresses existing inputs; the open question is whether this physically motivated re-expression exposes association structure the model otherwise misses. AV is a fixed-probe, mass-specific accessibility, not a molecule-specific free volume, so the contrast is a geometric surrogate only.",
    "falsification_criteria": "Falsified if, within a fixed framework (q_AV fixed), the training association of entropy loss with q_Vol is negative, or if replacing q_AV with q_lsd_f in the same difference yields an equal-or-better association and the AV term adds no marginal improvement (i.e., bottleneck geometry rather than accessible volume governs confinement). Competing mechanism: window/bottleneck control of translational entropy loss.",
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
      "proxy_assumptions": "Vol proxies the molecule's translational excluded-volume demand; AV proxies framework free space for a fixed geometric probe. Both are static geometric surrogates; transfer across adsorbate sizes is limited because the probe is not molecule-specific, and zero AV does not imply zero physical adsorption space.",
      "physical_interpretation": "Native meanings: Vol is the adsorbate van der Waals volume; AV is probe-accessible volume per framework mass. Normalization by fixed reference medians makes the terms dimensionless and row-varying; q = 1 is a bookkeeping reference, not an equality threshold.",
      "boundary_behavior": "AV = 0 occurs for 28 training rows (fixed-probe inaccessibility); there log(1 + q_AV) = 0 and the descriptor reduces to log(1 + q_Vol), which is finite and carries no accessibility information rather than an imputed value. Vol has no zeros in the training domain (min 20.424 angstrom^3).",
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

候选标识：`high/agent/replicate-2/round-3/h2`

最终状态：scored；边际收益：-1.751154 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "heavy_atom_rotor_magnitude_descriptor",
    "formula": "rotor_case(0, log(1 + q_PMI1 + q_PMI2 + q_PMI3), log(1 + q_PMI1 + q_PMI2 + q_PMI3))",
    "hypothesis": "At infinite dilution in pure-silica frameworks, gas-phase rotational entropy grows with the principal moments of inertia, while the adsorbed rotational phase space in a nearly isopotential pore quenches toward a configuration count that saturates with size; therefore the entropy loss (s_gas - s_ads)/R increases with the overall heavy-atom moment magnitude. The predeclared proxy derivative of entropy loss with respect to the descriptor is positive within each rotor class (rotor class held fixed), so entropy loss increases and s_ads/s_gas decreases as the descriptor increases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: rotational family, complementary to the retained anisotropy descriptor (which contrasts PMI3 against PMI1); here the hypothesis concerns total inertia magnitude, not anisotropy. The log(1 + sum of q-PMI) is an empirical, monotone, dimensionless smoothing chosen so all rows are finite and the descriptor is comparable across rotor classes; the fixed constants carry no universal physical meaning. Limitation: heavy-atom PMIs are representation-level proxies of the true all-atom inertia tensor, and magnitude is collinear with molecular size, so the test is whether magnitude adds association signal beyond anisotropy and volume proxies.",
    "falsification_criteria": "Falsified if, within a fixed rotor class and framework, the training association of entropy loss with the descriptor is negative, or if the retained anisotropy descriptor plus size proxies fully explain the association and this magnitude term contributes no marginal improvement (i.e., rotational quenching depends on shape anisotropy rather than inertia magnitude). Competing mechanism: anisotropy-controlled rotational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI1/PMI2/PMI3 proxy the adsorbate's rotational inertia; single-site molecules such as methane have legitimate zero heavy-atom moments by representation, which must not be read as zero physical inertia. The nonlinear rotor expression is a proxy aggregate; rotor classes are never mixed within a derivative evaluation.",
      "physical_interpretation": "Native meanings: PMI1/2/3 are the heavy-atom principal moments of inertia of the adsorbate in the original implicit-H representation. q_PMI values are row-varying dimensionless inputs; the reference median is not a physical rotational threshold.",
      "boundary_behavior": "Explicit rotor_case branches: single_site branch returns the constant 0 (neutral value, no heavy-atom rotor information, no imputation of physical zeros); linear and nonlinear branches share log(1 + q_PMI1 + q_PMI2 + q_PMI3), which is finite for all rows including rows with legitimate zero PMI components (log(1 + 0) = 0 contributions). All three branch outputs are dimensionless and unit-compatible.",
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
      "training_spearman": 0.40093653681747526,
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
    "name": "heavy_atom_rotor_magnitude_descriptor",
    "formula": "rotor_case(0, log(1 + q_PMI1 + q_PMI2 + q_PMI3), log(1 + q_PMI1 + q_PMI2 + q_PMI3))",
    "hypothesis": "At infinite dilution in pure-silica frameworks, gas-phase rotational entropy grows with the principal moments of inertia, while the adsorbed rotational phase space in a nearly isopotential pore quenches toward a configuration count that saturates with size; therefore the entropy loss (s_gas - s_ads)/R increases with the overall heavy-atom moment magnitude. The predeclared proxy derivative of entropy loss with respect to the descriptor is positive within each rotor class (rotor class held fixed), so entropy loss increases and s_ads/s_gas decreases as the descriptor increases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: rotational family, complementary to the retained anisotropy descriptor (which contrasts PMI3 against PMI1); here the hypothesis concerns total inertia magnitude, not anisotropy. The log(1 + sum of q-PMI) is an empirical, monotone, dimensionless smoothing chosen so all rows are finite and the descriptor is comparable across rotor classes; the fixed constants carry no universal physical meaning. Limitation: heavy-atom PMIs are representation-level proxies of the true all-atom inertia tensor, and magnitude is collinear with molecular size, so the test is whether magnitude adds association signal beyond anisotropy and volume proxies.",
    "falsification_criteria": "Falsified if, within a fixed rotor class and framework, the training association of entropy loss with the descriptor is negative, or if the retained anisotropy descriptor plus size proxies fully explain the association and this magnitude term contributes no marginal improvement (i.e., rotational quenching depends on shape anisotropy rather than inertia magnitude). Competing mechanism: anisotropy-controlled rotational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI1/PMI2/PMI3 proxy the adsorbate's rotational inertia; single-site molecules such as methane have legitimate zero heavy-atom moments by representation, which must not be read as zero physical inertia. The nonlinear rotor expression is a proxy aggregate; rotor classes are never mixed within a derivative evaluation.",
      "physical_interpretation": "Native meanings: PMI1/2/3 are the heavy-atom principal moments of inertia of the adsorbate in the original implicit-H representation. q_PMI values are row-varying dimensionless inputs; the reference median is not a physical rotational threshold.",
      "boundary_behavior": "Explicit rotor_case branches: single_site branch returns the constant 0 (neutral value, no heavy-atom rotor information, no imputation of physical zeros); linear and nonlinear branches share log(1 + q_PMI1 + q_PMI2 + q_PMI3), which is finite for all rows including rows with legitimate zero PMI components (log(1 + 0) = 0 contributions). All three branch outputs are dimensionless and unit-compatible.",
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
      "training_spearman": 0.40093653681747526,
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
    "name": "heavy_atom_rotor_magnitude_descriptor",
    "formula": "rotor_case(0, log(1 + q_PMI1 + q_PMI2 + q_PMI3), log(1 + q_PMI1 + q_PMI2 + q_PMI3))",
    "hypothesis": "At infinite dilution in pure-silica frameworks, gas-phase rotational entropy grows with the principal moments of inertia, while the adsorbed rotational phase space in a nearly isopotential pore quenches toward a configuration count that saturates with size; therefore the entropy loss (s_gas - s_ads)/R increases with the overall heavy-atom moment magnitude. The predeclared proxy derivative of entropy loss with respect to the descriptor is positive within each rotor class (rotor class held fixed), so entropy loss increases and s_ads/s_gas decreases as the descriptor increases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: rotational family, complementary to the retained anisotropy descriptor (which contrasts PMI3 against PMI1); here the hypothesis concerns total inertia magnitude, not anisotropy. The log(1 + sum of q-PMI) is an empirical, monotone, dimensionless smoothing chosen so all rows are finite and the descriptor is comparable across rotor classes; the fixed constants carry no universal physical meaning. Limitation: heavy-atom PMIs are representation-level proxies of the true all-atom inertia tensor, and magnitude is collinear with molecular size, so the test is whether magnitude adds association signal beyond anisotropy and volume proxies.",
    "falsification_criteria": "Falsified if, within a fixed rotor class and framework, the training association of entropy loss with the descriptor is negative, or if the retained anisotropy descriptor plus size proxies fully explain the association and this magnitude term contributes no marginal improvement (i.e., rotational quenching depends on shape anisotropy rather than inertia magnitude). Competing mechanism: anisotropy-controlled rotational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI1/PMI2/PMI3 proxy the adsorbate's rotational inertia; single-site molecules such as methane have legitimate zero heavy-atom moments by representation, which must not be read as zero physical inertia. The nonlinear rotor expression is a proxy aggregate; rotor classes are never mixed within a derivative evaluation.",
      "physical_interpretation": "Native meanings: PMI1/2/3 are the heavy-atom principal moments of inertia of the adsorbate in the original implicit-H representation. q_PMI values are row-varying dimensionless inputs; the reference median is not a physical rotational threshold.",
      "boundary_behavior": "Explicit rotor_case branches: single_site branch returns the constant 0 (neutral value, no heavy-atom rotor information, no imputation of physical zeros); linear and nonlinear branches share log(1 + q_PMI1 + q_PMI2 + q_PMI3), which is finite for all rows including rows with legitimate zero PMI components (log(1 + 0) = 0 contributions). All three branch outputs are dimensionless and unit-compatible.",
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
      "training_spearman": 0.40093653681747526,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/agent/replicate-2/round-3/h3`

最终状态：scored；边际收益：-8.405242 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "contact_area_contrast_descriptor",
    "formula": "log(1 + q_LabuteASA) - log(1 + q_ASA)",
    "hypothesis": "At infinite dilution in pure-silica frameworks, the entropy loss (s_gas - s_ads)/R increases with the adsorbate molecular surface area relative to the framework's probe-accessible specific surface area: a larger molecular contact area constrains positional and orientational microstates against the walls, while frameworks offering more accessible surface per mass provide more distinct adsorption microstates that mitigate the loss. The predeclared proxy derivative of entropy loss with respect to the descriptor is positive (increasing in q_LabuteASA at fixed framework surface), so entropy loss increases and s_ads/s_gas decreases as the descriptor increases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: coupling of adsorbate shape (molecular contact area) with framework connectivity (accessible specific surface), distinct from the volume/translation contrast in h1 and the rotation family in h2. q_LabuteASA and q_ASA are row-varying dimensionless inputs normalized by fixed training-reference medians (LabuteASA_ref = 31.85047501 angstrom^2, ASA_ref = 905.715 m^2/g); q = 1 is not a physical equality threshold. Limitation: all inputs are published D0 quantities re-expressed; LabuteASA is an approximate surface proxy and is collinear with Vol, so the open test is whether a surface-based contrast carries association signal beyond a volume-based one.",
    "falsification_criteria": "Falsified if, within a fixed adsorbate, the training association of entropy loss with q_ASA is positive with a sign that overwhelms the molecular term (i.e., more accessible surface increases, not decreases, entropy loss), or if the association is fully explained by volume-contrast proxies (q_Vol-based differences) with no marginal improvement from the surface contrast. Competing mechanism: accessible volume, not accessible surface, governs the adsorbed phase-space loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA proxies the adsorbate's wall-contact footprint; ASA proxies the framework's probe-accessible specific surface. Both are fixed-geometry surrogates with no chemistry specificity (pure silica, isopotential walls), and transfer across probe sizes is limited because the framework ASA probe is not the adsorbate.",
      "physical_interpretation": "Native meanings: LabuteASA is the adsorbate's approximate molecular surface area; ASA is framework surface accessible to a probe per framework mass. The q-normalized difference is a dimensionless row-varying descriptor; the reference medians are bookkeeping constants only.",
      "boundary_behavior": "ASA = 0 occurs for 28 training rows (no probe-accessible surface for the fixed geometric probe); there log(1 + q_ASA) = 0 and the descriptor reduces to log(1 + q_LabuteASA), which is finite and carries no framework-surface information rather than an imputed value. LabuteASA has no zeros in the training domain (min 7.450601137 angstrom^2).",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "LabuteASA",
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
        7.450601137,
        80.47008049
      ],
      "training_spearman": 0.4943539090196363,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
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
    "name": "contact_area_contrast_descriptor",
    "formula": "log(1 + q_LabuteASA) - log(1 + q_ASA)",
    "hypothesis": "At infinite dilution in pure-silica frameworks, the entropy loss (s_gas - s_ads)/R increases with the adsorbate molecular surface area relative to the framework's probe-accessible specific surface area: a larger molecular contact area constrains positional and orientational microstates against the walls, while frameworks offering more accessible surface per mass provide more distinct adsorption microstates that mitigate the loss. The predeclared proxy derivative of entropy loss with respect to the descriptor is positive (increasing in q_LabuteASA at fixed framework surface), so entropy loss increases and s_ads/s_gas decreases as the descriptor increases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: coupling of adsorbate shape (molecular contact area) with framework connectivity (accessible specific surface), distinct from the volume/translation contrast in h1 and the rotation family in h2. q_LabuteASA and q_ASA are row-varying dimensionless inputs normalized by fixed training-reference medians (LabuteASA_ref = 31.85047501 angstrom^2, ASA_ref = 905.715 m^2/g); q = 1 is not a physical equality threshold. Limitation: all inputs are published D0 quantities re-expressed; LabuteASA is an approximate surface proxy and is collinear with Vol, so the open test is whether a surface-based contrast carries association signal beyond a volume-based one.",
    "falsification_criteria": "Falsified if, within a fixed adsorbate, the training association of entropy loss with q_ASA is positive with a sign that overwhelms the molecular term (i.e., more accessible surface increases, not decreases, entropy loss), or if the association is fully explained by volume-contrast proxies (q_Vol-based differences) with no marginal improvement from the surface contrast. Competing mechanism: accessible volume, not accessible surface, governs the adsorbed phase-space loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA proxies the adsorbate's wall-contact footprint; ASA proxies the framework's probe-accessible specific surface. Both are fixed-geometry surrogates with no chemistry specificity (pure silica, isopotential walls), and transfer across probe sizes is limited because the framework ASA probe is not the adsorbate.",
      "physical_interpretation": "Native meanings: LabuteASA is the adsorbate's approximate molecular surface area; ASA is framework surface accessible to a probe per framework mass. The q-normalized difference is a dimensionless row-varying descriptor; the reference medians are bookkeeping constants only.",
      "boundary_behavior": "ASA = 0 occurs for 28 training rows (no probe-accessible surface for the fixed geometric probe); there log(1 + q_ASA) = 0 and the descriptor reduces to log(1 + q_LabuteASA), which is finite and carries no framework-surface information rather than an imputed value. LabuteASA has no zeros in the training domain (min 7.450601137 angstrom^2).",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "LabuteASA",
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
        7.450601137,
        80.47008049
      ],
      "training_spearman": 0.4943539090196363,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
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
    "name": "contact_area_contrast_descriptor",
    "formula": "log(1 + q_LabuteASA) - log(1 + q_ASA)",
    "hypothesis": "At infinite dilution in pure-silica frameworks, the entropy loss (s_gas - s_ads)/R increases with the adsorbate molecular surface area relative to the framework's probe-accessible specific surface area: a larger molecular contact area constrains positional and orientational microstates against the walls, while frameworks offering more accessible surface per mass provide more distinct adsorption microstates that mitigate the loss. The predeclared proxy derivative of entropy loss with respect to the descriptor is positive (increasing in q_LabuteASA at fixed framework surface), so entropy loss increases and s_ads/s_gas decreases as the descriptor increases. This is a predeclared proxy association; no causality or verified novelty is claimed.",
    "rationale": "Mechanism: coupling of adsorbate shape (molecular contact area) with framework connectivity (accessible specific surface), distinct from the volume/translation contrast in h1 and the rotation family in h2. q_LabuteASA and q_ASA are row-varying dimensionless inputs normalized by fixed training-reference medians (LabuteASA_ref = 31.85047501 angstrom^2, ASA_ref = 905.715 m^2/g); q = 1 is not a physical equality threshold. Limitation: all inputs are published D0 quantities re-expressed; LabuteASA is an approximate surface proxy and is collinear with Vol, so the open test is whether a surface-based contrast carries association signal beyond a volume-based one.",
    "falsification_criteria": "Falsified if, within a fixed adsorbate, the training association of entropy loss with q_ASA is positive with a sign that overwhelms the molecular term (i.e., more accessible surface increases, not decreases, entropy loss), or if the association is fully explained by volume-contrast proxies (q_Vol-based differences) with no marginal improvement from the surface contrast. Competing mechanism: accessible volume, not accessible surface, governs the adsorbed phase-space loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA proxies the adsorbate's wall-contact footprint; ASA proxies the framework's probe-accessible specific surface. Both are fixed-geometry surrogates with no chemistry specificity (pure silica, isopotential walls), and transfer across probe sizes is limited because the framework ASA probe is not the adsorbate.",
      "physical_interpretation": "Native meanings: LabuteASA is the adsorbate's approximate molecular surface area; ASA is framework surface accessible to a probe per framework mass. The q-normalized difference is a dimensionless row-varying descriptor; the reference medians are bookkeeping constants only.",
      "boundary_behavior": "ASA = 0 occurs for 28 training rows (no probe-accessible surface for the fixed geometric probe); there log(1 + q_ASA) = 0 and the descriptor reduces to log(1 + q_LabuteASA), which is finite and carries no framework-surface information rather than an imputed value. LabuteASA has no zeros in the training domain (min 7.450601137 angstrom^2).",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "LabuteASA",
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
        7.450601137,
        80.47008049
      ],
      "training_spearman": 0.4943539090196363,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
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
