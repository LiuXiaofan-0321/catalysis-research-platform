# high/agent/replicate-2/round-2

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
  }
]
```

## h1

候选标识：`high/agent/replicate-2/round-2/h1`

最终状态：scored；边际收益：+3.873869 pp；保留：True。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "cavity_window_contrast_descriptor",
    "formula": "log(1 + q_lsd_p) - log(1 + q_lsd_f)",
    "hypothesis": "In pure-silica frameworks at infinite dilution, the entropy loss (s_gas - s_ads)/R increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, cavity-scale proxy) and the largest passing sphere through the bottleneck (lsd_f, window-scale proxy). Frameworks where lsd_p >> lsd_f confine adsorbates to discrete wide cavities separated by narrow windows, reducing accessible positional/rotational phase space relative to gas; hence s_ads/s_gas decreases as this descriptor increases. This is a predeclared proxy association, not a validated causal mechanism.",
    "rationale": "lsd_p and lsd_f are distinct Zeo++ geometric quantities (Dif along-path included sphere vs Df passing bottleneck), so their q-normalized difference measures cavity-window contrast rather than re-expressing a single input. Both inputs are strictly positive in training (min 3.3452 A and 0.85684 A), so log arguments are positive and every row yields a finite value. Limitation: both are hard-sphere geometric proxies of a potential-energy landscape; neither resolves wall chemistry or adsorbate flexibility, and the +1 offsets are fixed numeric constants with no universal physical meaning.",
    "falsification_criteria": "If the training Spearman association between this descriptor and entropy loss/R is not positive in the predicted direction (e.g., sign flips or is statistically negligible), or if the marginal MAE improvement over the current retained set is non-positive, the hypothesis fails for this dataset. A competing mechanism that would falsify the interpretation: frameworks with high contrast but highly connected window networks (many equivalent paths, not captured by a single lsd_f) may retain adsorbed entropy, showing the contrast proxy alone is insufficient.",
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
      "proxy_assumptions": "lsd_p proxies cavity confinement scale and lsd_f proxies window restriction; both are rigid-probe geometric quantities and neither captures framework chemistry, defect structure, or adsorbate conformational flexibility. The q-normalization uses fixed positive training medians (q_lsd_p = lsd_p/6.38663, q_lsd_f = lsd_f/5.16326) and carries no physical unity threshold.",
      "physical_interpretation": "Descriptor is the log-ratio of (1 + cavity-scale proxy) to (1 + window-scale proxy); larger values indicate relatively wider cavities behind relatively tighter windows in the free-sphere path graph.",
      "boundary_behavior": "All training lsd_p and lsd_f values are strictly positive, so q values are positive and the descriptor is finite on every row; no zero-division branch is needed. As lsd_p -> lsd_f (uniform channel), the descriptor -> log((1+q_p)/(1+q_f)) -> small values, consistent with weak contrast.",
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
      "training_spearman": -0.013476942883289352,
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

### 最终/修复稿

```json
{
  "candidate": {
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

## h2

候选标识：`high/agent/replicate-2/round-2/h2`

最终状态：rejected；边际收益：未评分；保留：False。

复核改动字段：

训练前修复改动字段：formula, scientific_test.boundary_behavior, variable_mappings.PMI2

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "heavy_atom_rotor_anisotropy_descriptor",
    "formula": "log(1 + q_PMI3) - log(1 + q_PMI1)",
    "hypothesis": "At infinite dilution in nearly isopotential pure-silica frameworks, adsorbates whose heavy-atom principal moments are anisotropic (PMI3 much larger than PMI1, i.e., elongated or disc-like heavy-atom rotors) retain fewer degenerate orientations inside pores than near-isotropic rotors of comparable size, so the predeclared association is: entropy loss (s_gas - s_ads)/R INCREASES with this anisotropy descriptor, and s_ads/s_gas decreases. This descriptor was retained in round 1 (positive training Spearman, target-association consistent); it is re-proposed as an open, unvalidated proxy association, not a confirmed mechanism.",
    "rationale": "PMI1 and PMI3 are original heavy-atom (implicit-H) inertia proxies, not true all-atom moments; zero values are legitimate (linear/single-site molecules) and log(1+q) keeps the descriptor finite at zero (both terms collapse to 0 for single-site species such as methane). The q-normalization uses fixed positive training medians (q_PMI3 = PMI3/125.4948325, q_PMI1 = PMI1/43.29513794); the unity point of q has no physical meaning. No rotor_case branching is used; the same expression applies to all rotor classes.",
    "falsification_criteria": "The association fails if, holding rotor class fixed, the partial-derivative perturbation test shows the descriptor does not move entropy loss in the predeclared increasing direction, or if the marginal MAE improvement over the retained set becomes non-positive. A competing mechanism: anisotropic molecules may also have stronger dispersion contact with walls (energetic anchoring), which would reduce adsorbed entropy for energetic rather than orientational-degeneracy reasons; distinguishing these requires energy-decomposition data not available here.",
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
      "proxy_assumptions": "Heavy-atom principal moment anisotropy proxies the degeneracy of adsorbed orientations; the proxy ignores hydrogen-atom inertia, so linear and single-site molecules have legitimate zero or near-zero PMI1 that does not mean true all-atom inertia is zero. Transfer across rotor classes is empirical, not guaranteed.",
      "physical_interpretation": "Descriptor is the log-ratio of (1 + largest heavy-atom moment proxy) to (1 + smallest heavy-atom moment proxy); larger values indicate more elongated or disc-like heavy-atom distributions.",
      "boundary_behavior": "At PMI1 = 0 or PMI3 = 0 (legitimate for single-site/linear species), log(1+q) terms are finite (0 or log(1+q of the other moment)), so every training row yields a finite value without imputation or added epsilons.",
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
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI1",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy"
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
    "name": "heavy_atom_rotor_anisotropy_descriptor",
    "formula": "log(1 + q_PMI3) - log(1 + q_PMI1)",
    "hypothesis": "At infinite dilution in nearly isopotential pure-silica frameworks, adsorbates whose heavy-atom principal moments are anisotropic (PMI3 much larger than PMI1, i.e., elongated or disc-like heavy-atom rotors) retain fewer degenerate orientations inside pores than near-isotropic rotors of comparable size, so the predeclared association is: entropy loss (s_gas - s_ads)/R INCREASES with this anisotropy descriptor, and s_ads/s_gas decreases. This descriptor was retained in round 1 (positive training Spearman, target-association consistent); it is re-proposed as an open, unvalidated proxy association, not a confirmed mechanism.",
    "rationale": "PMI1 and PMI3 are original heavy-atom (implicit-H) inertia proxies, not true all-atom moments; zero values are legitimate (linear/single-site molecules) and log(1+q) keeps the descriptor finite at zero (both terms collapse to 0 for single-site species such as methane). The q-normalization uses fixed positive training medians (q_PMI3 = PMI3/125.4948325, q_PMI1 = PMI1/43.29513794); the unity point of q has no physical meaning. No rotor_case branching is used; the same expression applies to all rotor classes.",
    "falsification_criteria": "The association fails if, holding rotor class fixed, the partial-derivative perturbation test shows the descriptor does not move entropy loss in the predeclared increasing direction, or if the marginal MAE improvement over the retained set becomes non-positive. A competing mechanism: anisotropic molecules may also have stronger dispersion contact with walls (energetic anchoring), which would reduce adsorbed entropy for energetic rather than orientational-degeneracy reasons; distinguishing these requires energy-decomposition data not available here.",
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
      "proxy_assumptions": "Heavy-atom principal moment anisotropy proxies the degeneracy of adsorbed orientations; the proxy ignores hydrogen-atom inertia, so linear and single-site molecules have legitimate zero or near-zero PMI1 that does not mean true all-atom inertia is zero. Transfer across rotor classes is empirical, not guaranteed.",
      "physical_interpretation": "Descriptor is the log-ratio of (1 + largest heavy-atom moment proxy) to (1 + smallest heavy-atom moment proxy); larger values indicate more elongated or disc-like heavy-atom distributions.",
      "boundary_behavior": "At PMI1 = 0 or PMI3 = 0 (legitimate for single-site/linear species), log(1+q) terms are finite (0 or log(1+q of the other moment)), so every training row yields a finite value without imputation or added epsilons.",
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
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI1",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy"
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
    "slot_id": "h2",
    "name": "heavy_atom_rotor_anisotropy_descriptor",
    "formula": "((q_PMI1 - q_PMI2)**2 + (q_PMI2 - q_PMI3)**2 + (q_PMI3 - q_PMI1)**2) / (1 + (q_PMI1 + q_PMI2 + q_PMI3)**2 + (q_PMI1 - q_PMI2)**2 + (q_PMI2 - q_PMI3)**2 + (q_PMI3 - q_PMI1)**2)",
    "hypothesis": "At infinite dilution in nearly isopotential pure-silica frameworks, adsorbates whose heavy-atom principal moments are anisotropic (PMI3 much larger than PMI1, i.e., elongated or disc-like heavy-atom rotors) retain fewer degenerate orientations inside pores than near-isotropic rotors of comparable size, so the predeclared association is: entropy loss (s_gas - s_ads)/R INCREASES with this anisotropy descriptor, and s_ads/s_gas decreases. This descriptor was retained in round 1 (positive training Spearman, target-association consistent); it is re-proposed as an open, unvalidated proxy association, not a confirmed mechanism.",
    "rationale": "PMI1 and PMI3 are original heavy-atom (implicit-H) inertia proxies, not true all-atom moments; zero values are legitimate (linear/single-site molecules) and log(1+q) keeps the descriptor finite at zero (both terms collapse to 0 for single-site species such as methane). The q-normalization uses fixed positive training medians (q_PMI3 = PMI3/125.4948325, q_PMI1 = PMI1/43.29513794); the unity point of q has no physical meaning. No rotor_case branching is used; the same expression applies to all rotor classes.",
    "falsification_criteria": "The association fails if, holding rotor class fixed, the partial-derivative perturbation test shows the descriptor does not move entropy loss in the predeclared increasing direction, or if the marginal MAE improvement over the retained set becomes non-positive. A competing mechanism: anisotropic molecules may also have stronger dispersion contact with walls (energetic anchoring), which would reduce adsorbed entropy for energetic rather than orientational-degeneracy reasons; distinguishing these requires energy-decomposition data not available here.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moment anisotropy proxies the degeneracy of adsorbed orientations; the proxy ignores hydrogen-atom inertia, so linear and single-site molecules have legitimate zero or near-zero PMI1 that does not mean true all-atom inertia is zero. Transfer across rotor classes is empirical, not guaranteed.",
      "physical_interpretation": "Descriptor is the log-ratio of (1 + largest heavy-atom moment proxy) to (1 + smallest heavy-atom moment proxy); larger values indicate more elongated or disc-like heavy-atom distributions.",
      "boundary_behavior": "The descriptor is a bounded, size-reduced heavy-atom inertia-anisotropy invariant: N = sum of squared pairwise differences of q_PMI1, q_PMI2, q_PMI3, normalized by 1 + (q_PMI1 + q_PMI2 + q_PMI3)**2 + N. It is zero for exactly isotropic heavy-atom distributions and grows toward the fully anisotropic limit, so the predeclared increasing direction (more anisotropy -> more entropy loss) is preserved while the descriptor is no longer a near-monotone re-expression of any single input moment (the previous log(1 + q_PMI3) - log(1 + q_PMI1) form was dominated by the PMI3 magnitude, which is why the slot was rejected as redundant with a current input). Finiteness: all q_PMI values are nonnegative and finite on every training row; zeros are legitimate (single-site species have all three heavy-atom PMIs = 0, linear species have PMI1 and PMI2 = 0). At all-zero PMIs, N = 0 and (q_PMI1 + q_PMI2 + q_PMI3)**2 = 0, so the descriptor equals 0/(1) = 0, finite with no imputation and no division by zero. For linear species with only q_PMI3 > 0, the descriptor reduces to 3*q_PMI3**2 / (1 + q_PMI3**2 + 3*q_PMI3**2), which is finite and saturates below 1. The additive constant 1 in the denominator is an empirical regularizer that guarantees finiteness at legitimate zero PMIs; it carries no universal physical meaning and is not claimed as a physical scale. Honest limitations: PMI1, PMI2, PMI3 are implicit-H/heavy-atom proxies, not all-atom moments, so hydrogen inertia is ignored; the +1 constant blends pure shape anisotropy with a magnitude dependence for very small moments; the association with entropy loss remains an open, unvalidated proxy association (mechanism_validated is false) and must be re-audited for redundancy and association direction under this reparameterization.",
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
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
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
    "direction_failure": {
      "opposite_n": 1035,
      "nonzero_fraction": 0.5616264294790343
    },
    "reason": "Formula contradicts its predeclared proxy direction"
  }
}
```

## h3

候选标识：`high/agent/replicate-2/round-2/h3`

最终状态：scored；边际收益：-2.105352 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "size_included_path_mismatch_descriptor",
    "formula": "log(1 + q_Vol) - log(1 + q_lsd_p)",
    "hypothesis": "At infinite dilution in pure-silica frameworks, entropy loss (s_gas - s_ads)/R increases when the adsorbate van der Waals volume is large relative to the largest included sphere along the framework free-sphere path: large molecules in frameworks whose along-path included diameter is small experience strongly restricted positional configurations and lose more translational/orientational entropy than the same molecules in frameworks with wide included paths. Predeclared association: the descriptor increases, entropy loss increases, and s_ads/s_gas decreases. This is a proxy association; round 1 showed a related Vol-vs-lsd_f mismatch had the consistent positive training association (Spearman ~0.64) but negligible marginal MAE gain, so this variant remains open and unvalidated.",
    "rationale": "Vol is a molecule property and lsd_p a framework property, so their q-normalized difference is a genuine cross-object mismatch rather than a re-expression of one input; it differs from the round-1 h3 by using the along-path included sphere (lsd_p >= lsd_f always) instead of the bottleneck. Both inputs are strictly positive in training (Vol min 20.424 A^3, lsd_p min 3.3452 A), so the descriptor is finite on every row. Limitations: Vol is a whole-molecule vdW volume that does not encode shape; lsd_p is a hard-sphere path quantity, not the global cavity diameter Di, and neither quantity enters the published D0 set as a new D0 input.",
    "falsification_criteria": "The hypothesis fails if the training Spearman association between this descriptor and entropy loss/R is not positive in the predeclared direction, or if the marginal MAE improvement over the current retained set (including the round-1 h2 anisotropy descriptor) is non-positive, indicating the descriptor only re-expresses retained information. A competing mechanism: large Vol may correlate with more gas-phase degrees of freedom (raising s_gas) rather than lower s_ads; if the association is driven entirely by s_gas scaling, the confinement interpretation is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Whole-molecule vdW volume proxies steric footprint and lsd_p proxies the widest accessible along-path confinement; neither captures molecular shape anisotropy (delegated to h2), framework chemistry, or soft-potential squeezing. The AV accessibility volume is deliberately not used here because it is a fixed-probe, mass-specific quantity, not a molecule-specific free volume.",
      "physical_interpretation": "Descriptor is the log-ratio of (1 + normalized adsorbate volume) to (1 + normalized along-path included sphere); larger values indicate a relatively bulky adsorbate inside a relatively tight included path, i.e., a steric mismatch. The q-unity points (Vol_ref = 67.24 A^3, lsd_p_ref = 6.38663 A) are fixed training medians with no physical threshold meaning.",
      "boundary_behavior": "All training Vol and lsd_p values are strictly positive, so q values are positive and the descriptor is finite on every row; no zero branch is required. As Vol approaches small values relative to lsd_p the descriptor becomes negative but remains finite, corresponding to a spacious pore environment.",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6791653208444576,
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
    "name": "size_included_path_mismatch_descriptor",
    "formula": "log(1 + q_Vol) - log(1 + q_lsd_p)",
    "hypothesis": "At infinite dilution in pure-silica frameworks, entropy loss (s_gas - s_ads)/R increases when the adsorbate van der Waals volume is large relative to the largest included sphere along the framework free-sphere path: large molecules in frameworks whose along-path included diameter is small experience strongly restricted positional configurations and lose more translational/orientational entropy than the same molecules in frameworks with wide included paths. Predeclared association: the descriptor increases, entropy loss increases, and s_ads/s_gas decreases. This is a proxy association; round 1 showed a related Vol-vs-lsd_f mismatch had the consistent positive training association (Spearman ~0.64) but negligible marginal MAE gain, so this variant remains open and unvalidated.",
    "rationale": "Vol is a molecule property and lsd_p a framework property, so their q-normalized difference is a genuine cross-object mismatch rather than a re-expression of one input; it differs from the round-1 h3 by using the along-path included sphere (lsd_p >= lsd_f always) instead of the bottleneck. Both inputs are strictly positive in training (Vol min 20.424 A^3, lsd_p min 3.3452 A), so the descriptor is finite on every row. Limitations: Vol is a whole-molecule vdW volume that does not encode shape; lsd_p is a hard-sphere path quantity, not the global cavity diameter Di, and neither quantity enters the published D0 set as a new D0 input.",
    "falsification_criteria": "The hypothesis fails if the training Spearman association between this descriptor and entropy loss/R is not positive in the predeclared direction, or if the marginal MAE improvement over the current retained set (including the round-1 h2 anisotropy descriptor) is non-positive, indicating the descriptor only re-expresses retained information. A competing mechanism: large Vol may correlate with more gas-phase degrees of freedom (raising s_gas) rather than lower s_ads; if the association is driven entirely by s_gas scaling, the confinement interpretation is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Whole-molecule vdW volume proxies steric footprint and lsd_p proxies the widest accessible along-path confinement; neither captures molecular shape anisotropy (delegated to h2), framework chemistry, or soft-potential squeezing. The AV accessibility volume is deliberately not used here because it is a fixed-probe, mass-specific quantity, not a molecule-specific free volume.",
      "physical_interpretation": "Descriptor is the log-ratio of (1 + normalized adsorbate volume) to (1 + normalized along-path included sphere); larger values indicate a relatively bulky adsorbate inside a relatively tight included path, i.e., a steric mismatch. The q-unity points (Vol_ref = 67.24 A^3, lsd_p_ref = 6.38663 A) are fixed training medians with no physical threshold meaning.",
      "boundary_behavior": "All training Vol and lsd_p values are strictly positive, so q values are positive and the descriptor is finite on every row; no zero branch is required. As Vol approaches small values relative to lsd_p the descriptor becomes negative but remains finite, corresponding to a spacious pore environment.",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6791653208444576,
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
    "name": "size_included_path_mismatch_descriptor",
    "formula": "log(1 + q_Vol) - log(1 + q_lsd_p)",
    "hypothesis": "At infinite dilution in pure-silica frameworks, entropy loss (s_gas - s_ads)/R increases when the adsorbate van der Waals volume is large relative to the largest included sphere along the framework free-sphere path: large molecules in frameworks whose along-path included diameter is small experience strongly restricted positional configurations and lose more translational/orientational entropy than the same molecules in frameworks with wide included paths. Predeclared association: the descriptor increases, entropy loss increases, and s_ads/s_gas decreases. This is a proxy association; round 1 showed a related Vol-vs-lsd_f mismatch had the consistent positive training association (Spearman ~0.64) but negligible marginal MAE gain, so this variant remains open and unvalidated.",
    "rationale": "Vol is a molecule property and lsd_p a framework property, so their q-normalized difference is a genuine cross-object mismatch rather than a re-expression of one input; it differs from the round-1 h3 by using the along-path included sphere (lsd_p >= lsd_f always) instead of the bottleneck. Both inputs are strictly positive in training (Vol min 20.424 A^3, lsd_p min 3.3452 A), so the descriptor is finite on every row. Limitations: Vol is a whole-molecule vdW volume that does not encode shape; lsd_p is a hard-sphere path quantity, not the global cavity diameter Di, and neither quantity enters the published D0 set as a new D0 input.",
    "falsification_criteria": "The hypothesis fails if the training Spearman association between this descriptor and entropy loss/R is not positive in the predeclared direction, or if the marginal MAE improvement over the current retained set (including the round-1 h2 anisotropy descriptor) is non-positive, indicating the descriptor only re-expresses retained information. A competing mechanism: large Vol may correlate with more gas-phase degrees of freedom (raising s_gas) rather than lower s_ads; if the association is driven entirely by s_gas scaling, the confinement interpretation is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Whole-molecule vdW volume proxies steric footprint and lsd_p proxies the widest accessible along-path confinement; neither captures molecular shape anisotropy (delegated to h2), framework chemistry, or soft-potential squeezing. The AV accessibility volume is deliberately not used here because it is a fixed-probe, mass-specific quantity, not a molecule-specific free volume.",
      "physical_interpretation": "Descriptor is the log-ratio of (1 + normalized adsorbate volume) to (1 + normalized along-path included sphere); larger values indicate a relatively bulky adsorbate inside a relatively tight included path, i.e., a steric mismatch. The q-unity points (Vol_ref = 67.24 A^3, lsd_p_ref = 6.38663 A) are fixed training medians with no physical threshold meaning.",
      "boundary_behavior": "All training Vol and lsd_p values are strictly positive, so q values are positive and the descriptor is finite on every row; no zero branch is required. As Vol approaches small values relative to lsd_p the descriptor becomes negative but remains finite, corresponding to a spacious pore environment.",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6791653208444576,
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
    "mode": "no_retrieval",
    "items": 0,
    "lexical_tokens": 0
  },
  "cited_items": [],
  "mechanism_cards": []
}
```
