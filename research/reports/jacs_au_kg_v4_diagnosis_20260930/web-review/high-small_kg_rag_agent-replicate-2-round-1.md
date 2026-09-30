# high/small_kg_rag_agent/replicate-2/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/small_kg_rag_agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`high/small_kg_rag_agent/replicate-2/round-1/h1`

最终状态：scored；边际收益：+0.049829 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "vol_bottleneck_confinement",
    "formula": "log(q_Vol) - 2.0 * log(q_lsd_f)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the translational part of the adsorption entropy loss grows with the ratio of adsorbate van der Waals volume to the square of the framework free-path bottleneck diameter: molecules that are large relative to the passing window lose more translational freedom upon adsorption, so the descriptor associates positively with entropy loss/R.",
    "rationale": "Translational confinement picture: the accessible configurational volume of a molecule inside a channel scales with the pore cross-section (here proxied by Df squared) and the molecule's own size (vdW volume). Vol and lsd_f are strictly positive over the whole training domain, so the log terms are finite on every row. This is a mechanistic recombination of existing published inputs, not a new source of information beyond the D0 set.",
    "falsification_criteria": "If the empirical association of the descriptor with entropy loss/R is not monotone, or if it weakens or reverses within the sub-domain where lsd_f exceeds roughly twice the adsorbate GeDi (window not rate-limiting for confinement), the bottleneck-square scaling hypothesis is falsified; a competing mechanism is that bottleneck passage controls kinetics only, while equilibrium entropy is set by cavity size (lsd_p) instead.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Df (lsd_f) is a bottleneck diameter, not the global cavity diameter; vdW volume is a rigid-molecule size proxy. Both ignore framework flexibility and adsorbate deformation; the square-law cross-section dependence is an assumed geometric smoothing, not a derived law.",
      "physical_interpretation": "q_Vol and q_lsd_f are row-varying ratios to fixed training-reference medians; they carry no physical unity threshold, and the exponent 2.0 is an empirical geometric choice, not a fitted constant with universal meaning.",
      "boundary_behavior": "Vol and lsd_f are positive on all training rows (zero_n = 0), so the expression is finite everywhere; no zero division or zero log argument arises, and no imputation is used.",
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
        "Vol",
        "lsd_f"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
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
      "training_spearman": 0.6703897107878907,
      "target_association": "contradicted",
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
    "name": "vol_bottleneck_confinement",
    "formula": "2.0 * log(q_lsd_f) - log(q_Vol)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the translational part of the adsorption entropy loss grows with the ratio of adsorbate van der Waals volume to the square of the framework free-path bottleneck diameter: molecules that are large relative to the passing window lose more translational freedom upon adsorption, so the descriptor associates positively with entropy loss/R.",
    "rationale": "Translational-confinement picture retained with the executable sign corrected. The draft wrote log(q_Vol) - 2.0*log(q_lsd_f) while pre-declaring entropy_direction 'decreasing'; the training-only precheck returned spearman +0.67 between that descriptor and entropy loss/R, contradicting the pre-declaration. Since entropy_direction is fixed by the program, the descriptor is re-expressed in the inverse free-space convention, 2.0*log(q_lsd_f) - log(q_Vol), whose association with entropy loss/R is about -0.67 and therefore consistent with the pre-declaration. Mechanistically, molecules large relative to the passing window lose more translational freedom upon adsorption (E04, E07); this is a recombination of existing D0 inputs, and the exponent 2.0 is an empirical geometric choice, not a universal constant.",
    "falsification_criteria": "If the empirical association of the free-space descriptor 2.0*log(q_lsd_f) - log(q_Vol) with entropy loss/R is not negative (entropy loss does not decrease as q_lsd_f**2/q_Vol increases), or if the association weakens or reverses in the sub-domain where lsd_f exceeds roughly twice the adsorbate GeDi (window not rate-limiting for confinement), the bottleneck-square scaling is falsified; the competing mechanism is that bottleneck passage controls kinetics only while equilibrium entropy is set by cavity-size proxies (lsd_p) instead.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Df (lsd_f) is a passing-bottleneck diameter, not the global cavity diameter Di and not the included diameter Dif (lsd_p); q_lsd_f squared empirically proxies the window cross-section and q_Vol proxies rigid-molecule size. The square-law cross-section dependence is an assumed geometric smoothing, not a derived law. Framework flexibility and adsorbate deformation are ignored.",
      "physical_interpretation": "The corrected descriptor is a free-space ratio: available bottleneck cross-section (q_lsd_f**2) relative to molecular vdW volume (q_Vol). q_Vol and q_lsd_f are row-varying ratios to fixed positive training-reference medians (Vol_ref = 67.24, lsd_f_ref = 5.16326); q-unity carries no physical threshold meaning. The enforced entropy_direction 'decreasing' means entropy loss decreases as this free-space descriptor increases; equivalently, the confinement ratio q_Vol/q_lsd_f**2 (the exact negation of this descriptor) increases with entropy loss, consistent with the training precheck spearman of about +0.67 for the confinement ratio.",
      "boundary_behavior": "Vol (min 20.424) and lsd_f (min 0.85684) have zero_n = 0 across all 2361 training rows, so q_Vol and q_lsd_f are strictly positive and both log arguments are strictly positive; the expression is finite on every row with no imputation or epsilon shifting. Behavior outside the positive domain is undefined and not claimed.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
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
        "Vol",
        "lsd_f"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
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
      "training_spearman": -0.6703897107878907,
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
    "name": "vol_bottleneck_confinement",
    "formula": "2.0 * log(q_lsd_f) - log(q_Vol)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the translational part of the adsorption entropy loss grows with the ratio of adsorbate van der Waals volume to the square of the framework free-path bottleneck diameter: molecules that are large relative to the passing window lose more translational freedom upon adsorption, so the descriptor associates positively with entropy loss/R.",
    "rationale": "Translational-confinement picture retained with the executable sign corrected. The draft wrote log(q_Vol) - 2.0*log(q_lsd_f) while pre-declaring entropy_direction 'decreasing'; the training-only precheck returned spearman +0.67 between that descriptor and entropy loss/R, contradicting the pre-declaration. Since entropy_direction is fixed by the program, the descriptor is re-expressed in the inverse free-space convention, 2.0*log(q_lsd_f) - log(q_Vol), whose association with entropy loss/R is about -0.67 and therefore consistent with the pre-declaration. Mechanistically, molecules large relative to the passing window lose more translational freedom upon adsorption (E04, E07); this is a recombination of existing D0 inputs, and the exponent 2.0 is an empirical geometric choice, not a universal constant.",
    "falsification_criteria": "If the empirical association of the free-space descriptor 2.0*log(q_lsd_f) - log(q_Vol) with entropy loss/R is not negative (entropy loss does not decrease as q_lsd_f**2/q_Vol increases), or if the association weakens or reverses in the sub-domain where lsd_f exceeds roughly twice the adsorbate GeDi (window not rate-limiting for confinement), the bottleneck-square scaling is falsified; the competing mechanism is that bottleneck passage controls kinetics only while equilibrium entropy is set by cavity-size proxies (lsd_p) instead.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Df (lsd_f) is a passing-bottleneck diameter, not the global cavity diameter Di and not the included diameter Dif (lsd_p); q_lsd_f squared empirically proxies the window cross-section and q_Vol proxies rigid-molecule size. The square-law cross-section dependence is an assumed geometric smoothing, not a derived law. Framework flexibility and adsorbate deformation are ignored.",
      "physical_interpretation": "The corrected descriptor is a free-space ratio: available bottleneck cross-section (q_lsd_f**2) relative to molecular vdW volume (q_Vol). q_Vol and q_lsd_f are row-varying ratios to fixed positive training-reference medians (Vol_ref = 67.24, lsd_f_ref = 5.16326); q-unity carries no physical threshold meaning. The enforced entropy_direction 'decreasing' means entropy loss decreases as this free-space descriptor increases; equivalently, the confinement ratio q_Vol/q_lsd_f**2 (the exact negation of this descriptor) increases with entropy loss, consistent with the training precheck spearman of about +0.67 for the confinement ratio.",
      "boundary_behavior": "Vol (min 20.424) and lsd_f (min 0.85684) have zero_n = 0 across all 2361 training rows, so q_Vol and q_lsd_f are strictly positive and both log arguments are strictly positive; the expression is finite on every row with no imputation or epsilon shifting. Behavior outside the positive domain is undefined and not claimed.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
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
        "Vol",
        "lsd_f"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
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
      "training_spearman": -0.6703897107878907,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/small_kg_rag_agent/replicate-2/round-1/h2`

最终状态：scored；边际收益：+1.221454 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "heavy_atom_inertia_rotor_hindrance",
    "formula": "q_PMI3 * q_Vol",
    "hypothesis": "At infinite dilution, adsorption suppresses rotational degrees of freedom of polyatomic adsorbates; the heavier and larger the molecule (proxied by the largest heavy-atom principal moment of inertia times vdW volume), the greater the rotational contribution to entropy loss, so the descriptor associates positively with entropy loss/R while vanishing for single-site adsorbates.",
    "rationale": "Rotational entropy loss upon immobilization should scale with the molecule's moment of inertia and size. PMI3 is the largest heavy-atom principal moment and is nonzero for all non-single-site rows in the training domain; the product with normalized volume vanishes exactly on the 54 single-site rows, where no internal-rotor suppression is expected. Limitations: PMI proxies are computed on the original implicit-H/heavy-atom representation, so a zero value reflects the representation, not true zero all-atom inertia.",
    "falsification_criteria": "If entropy loss/R for near-linear or small-inertia polyatomic adsorbates matches that of size-matched large-inertia adsorbates (no residual PMI3 association after volume is accounted for), the rotational-hindrance mechanism is not supported and the descriptor reduces to a redundant size proxy.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI3 is a proxy for rotational hindrance, not true all-atom inertia; vdW volume is a size co-proxy. Both are rigid-molecule, single-conformer descriptors and transfer poorly to flexible adsorbates with conformational entropy.",
      "physical_interpretation": "q_PMI3 and q_Vol are dimensionless row-varying ratios to fixed positive training-reference medians; legitimate zeros of PMI3 (single-site rows) map to descriptor zero and are not imputed, and no q-unity value is interpreted as a physical equality threshold.",
      "boundary_behavior": "On the 54 single-site rows (PMI3 = 0) the descriptor equals 0 exactly, encoding 'no rotor hindrance'; this is a representation-level boundary, and the true monatomic rotational partition function is not asserted to be zero.",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI3",
        "Vol"
      ],
      "quantity_roles": {
        "PMI3": "heavy_atom_inertia_proxy",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2414.631462
      ],
      "training_spearman": 0.4043706291099055,
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
    "name": "heavy_atom_inertia_rotor_hindrance",
    "formula": "q_PMI3 * q_Vol",
    "hypothesis": "At infinite dilution, adsorption suppresses rotational degrees of freedom of polyatomic adsorbates; the heavier and larger the molecule (proxied by the largest heavy-atom principal moment of inertia times vdW volume), the greater the rotational contribution to entropy loss, so the descriptor associates positively with entropy loss/R while vanishing for single-site adsorbates.",
    "rationale": "Rotational entropy loss upon immobilization should scale with the molecule's moment of inertia and size. PMI3 is the largest heavy-atom principal moment and is nonzero for all non-single-site rows in the training domain; the product with normalized volume vanishes exactly on the 54 single-site rows, where no internal-rotor suppression is expected. Limitations: PMI proxies are computed on the original implicit-H/heavy-atom representation, so a zero value reflects the representation, not true zero all-atom inertia.",
    "falsification_criteria": "If entropy loss/R for near-linear or small-inertia polyatomic adsorbates matches that of size-matched large-inertia adsorbates (no residual PMI3 association after volume is accounted for), the rotational-hindrance mechanism is not supported and the descriptor reduces to a redundant size proxy.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI3 is a proxy for rotational hindrance, not true all-atom inertia; vdW volume is a size co-proxy. Both are rigid-molecule, single-conformer descriptors and transfer poorly to flexible adsorbates with conformational entropy.",
      "physical_interpretation": "q_PMI3 and q_Vol are dimensionless row-varying ratios to fixed positive training-reference medians; legitimate zeros of PMI3 (single-site rows) map to descriptor zero and are not imputed, and no q-unity value is interpreted as a physical equality threshold.",
      "boundary_behavior": "On the 54 single-site rows (PMI3 = 0) the descriptor equals 0 exactly, encoding 'no rotor hindrance'; this is a representation-level boundary, and the true monatomic rotational partition function is not asserted to be zero.",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI3",
        "Vol"
      ],
      "quantity_roles": {
        "PMI3": "heavy_atom_inertia_proxy",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2414.631462
      ],
      "training_spearman": 0.4043706291099055,
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
    "name": "heavy_atom_inertia_rotor_hindrance",
    "formula": "q_PMI3 * q_Vol",
    "hypothesis": "At infinite dilution, adsorption suppresses rotational degrees of freedom of polyatomic adsorbates; the heavier and larger the molecule (proxied by the largest heavy-atom principal moment of inertia times vdW volume), the greater the rotational contribution to entropy loss, so the descriptor associates positively with entropy loss/R while vanishing for single-site adsorbates.",
    "rationale": "Rotational entropy loss upon immobilization should scale with the molecule's moment of inertia and size. PMI3 is the largest heavy-atom principal moment and is nonzero for all non-single-site rows in the training domain; the product with normalized volume vanishes exactly on the 54 single-site rows, where no internal-rotor suppression is expected. Limitations: PMI proxies are computed on the original implicit-H/heavy-atom representation, so a zero value reflects the representation, not true zero all-atom inertia.",
    "falsification_criteria": "If entropy loss/R for near-linear or small-inertia polyatomic adsorbates matches that of size-matched large-inertia adsorbates (no residual PMI3 association after volume is accounted for), the rotational-hindrance mechanism is not supported and the descriptor reduces to a redundant size proxy.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI3 is a proxy for rotational hindrance, not true all-atom inertia; vdW volume is a size co-proxy. Both are rigid-molecule, single-conformer descriptors and transfer poorly to flexible adsorbates with conformational entropy.",
      "physical_interpretation": "q_PMI3 and q_Vol are dimensionless row-varying ratios to fixed positive training-reference medians; legitimate zeros of PMI3 (single-site rows) map to descriptor zero and are not imputed, and no q-unity value is interpreted as a physical equality threshold.",
      "boundary_behavior": "On the 54 single-site rows (PMI3 = 0) the descriptor equals 0 exactly, encoding 'no rotor hindrance'; this is a representation-level boundary, and the true monatomic rotational partition function is not asserted to be zero.",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI3",
        "Vol"
      ],
      "quantity_roles": {
        "PMI3": "heavy_atom_inertia_proxy",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2414.631462
      ],
      "training_spearman": 0.4043706291099055,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/small_kg_rag_agent/replicate-2/round-1/h3`

最终状态：scored；边际收益：+3.278410 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "cage_window_path_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "Frameworks whose included free-path diameter (Dif) greatly exceeds their passing bottleneck (Df) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom, and the pre-declared association is that increasing contrast correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas).",
    "rationale": "Connectivity-family hypothesis: the contrast Dif/Df distinguishes cage-window topologies from open channels. lsd_p is the included sphere along the free-sphere path and lsd_f is the passing bottleneck; neither equals the global cavity diameter Di. Both quantities are strictly positive in the training domain, so the log-ratio is finite on every row. The sign of the association is pre-declared and must be tested empirically; the competing sign (large contrast gives rattling freedom and lower entropy loss) is an explicit alternative.",
    "falsification_criteria": "If the empirical association of log(q_lsd_p/q_lsd_f) with entropy loss/R has the opposite sign to the pre-declared direction, or vanishes within the training quantile range once lsd_f alone is controlled for, the cage-window contrast mechanism is falsified in favor of a pure bottleneck (kinetic/confinement) explanation.",
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
      "proxy_assumptions": "Zeo++ Df/Dif geometric probes are rigid, fixed-radius proxies on the published numerical scale; they ignore framework flexibility, defects, and molecule-specific probe sizes. The contrast is a topology proxy, not a direct measure of adsorbed-phase configurational entropy.",
      "physical_interpretation": "q_lsd_p and q_lsd_f are row-varying ratios to fixed positive training-reference medians; their ratio being 1 (q-unity) carries no physical meaning as an equality threshold, and the log-ratio is used only as a dimensionless contrast coordinate.",
      "boundary_behavior": "lsd_p and lsd_f have zero_n = 0 over the training domain (min 3.3452 and 0.85684 respectively), so the log-ratio is finite on every row; no epsilon shifting or imputation is invoked, and behavior outside the positive domain is undefined and not claimed.",
      "vary_input": "lsd_p",
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
    "slot_id": "h3",
    "name": "cage_window_path_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "Frameworks whose included free-path diameter (Dif) greatly exceeds their passing bottleneck (Df) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom, and the pre-declared association is that increasing contrast correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas).",
    "rationale": "Connectivity-family hypothesis retained with an honest status update. The contrast Dif/Df distinguishes cage-window topologies from open channels: lsd_p is the included diameter along the free path and lsd_f the passing bottleneck; neither equals the global cavity diameter Di. The training-only precheck finds essentially no marginal association with entropy loss/R (spearman about -0.02), so the pre-declared increasing direction is neither confirmed nor contradicted, and the competing rattling-freedom explanation (large contrast yields local freedom and lower loss) remains live. Sources report cavity-size-dependent entropy losses (E02, E04) and propose cage rotational effects on equilibrium (E06), but these are conditional reports that supply no fitted coefficients for this benchmark.",
    "falsification_criteria": "If, once lsd_f (or lsd_p alone) is controlled for, the contrast log(q_lsd_p/q_lsd_f) shows no association with entropy loss/R within the training quantile range — as the current marginal spearman of about -0.02 already suggests — or shows the sign opposite to the pre-declared increasing direction, the cage-window contrast mechanism is falsified in favor of a pure bottleneck/kinetic or cavity-size explanation.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E06"
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
      "proxy_assumptions": "Zeo++ Df (lsd_f, passing bottleneck) and Dif (lsd_p, largest included sphere along the free-sphere path) are rigid fixed-probe geometric outputs on the published numerical scale; neither is the global cavity diameter Di, and neither measures adsorbed-phase configurational entropy. Framework flexibility, defects and molecule-specific probe sizes are ignored.",
      "physical_interpretation": "q_lsd_p and q_lsd_f are row-varying ratios to fixed positive training-reference medians (6.38663 and 5.16326); a q-ratio of 1 is not a native equality threshold. The log-ratio is only a dimensionless cage-window contrast coordinate. The training-only precheck returns spearman about -0.02 with entropy loss/R, so the pre-declared increasing association is currently unconfirmed on training data; the descriptor is retained as a pre-registered falsification test, not a validated predictor.",
      "boundary_behavior": "lsd_f (min 0.85684) and lsd_p (min 3.3452) have zero_n = 0 over all 2361 training rows, so q_lsd_p/q_lsd_f is strictly positive and the log-ratio is finite on every row; no epsilon shifting or imputation is invoked. Behavior outside the positive domain is undefined and not claimed.",
      "vary_input": "lsd_p",
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
    "slot_id": "h3",
    "name": "cage_window_path_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "Frameworks whose included free-path diameter (Dif) greatly exceeds their passing bottleneck (Df) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom, and the pre-declared association is that increasing contrast correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas).",
    "rationale": "Connectivity-family hypothesis retained with an honest status update. The contrast Dif/Df distinguishes cage-window topologies from open channels: lsd_p is the included diameter along the free path and lsd_f the passing bottleneck; neither equals the global cavity diameter Di. The training-only precheck finds essentially no marginal association with entropy loss/R (spearman about -0.02), so the pre-declared increasing direction is neither confirmed nor contradicted, and the competing rattling-freedom explanation (large contrast yields local freedom and lower loss) remains live. Sources report cavity-size-dependent entropy losses (E02, E04) and propose cage rotational effects on equilibrium (E06), but these are conditional reports that supply no fitted coefficients for this benchmark.",
    "falsification_criteria": "If, once lsd_f (or lsd_p alone) is controlled for, the contrast log(q_lsd_p/q_lsd_f) shows no association with entropy loss/R within the training quantile range — as the current marginal spearman of about -0.02 already suggests — or shows the sign opposite to the pre-declared increasing direction, the cage-window contrast mechanism is falsified in favor of a pure bottleneck/kinetic or cavity-size explanation.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E06"
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
      "proxy_assumptions": "Zeo++ Df (lsd_f, passing bottleneck) and Dif (lsd_p, largest included sphere along the free-sphere path) are rigid fixed-probe geometric outputs on the published numerical scale; neither is the global cavity diameter Di, and neither measures adsorbed-phase configurational entropy. Framework flexibility, defects and molecule-specific probe sizes are ignored.",
      "physical_interpretation": "q_lsd_p and q_lsd_f are row-varying ratios to fixed positive training-reference medians (6.38663 and 5.16326); a q-ratio of 1 is not a native equality threshold. The log-ratio is only a dimensionless cage-window contrast coordinate. The training-only precheck returns spearman about -0.02 with entropy loss/R, so the pre-declared increasing association is currently unconfirmed on training data; the descriptor is retained as a pre-registered falsification test, not a validated predictor.",
      "boundary_behavior": "lsd_f (min 0.85684) and lsd_p (min 3.3452) have zero_n = 0 over all 2361 training rows, so q_lsd_p/q_lsd_f is strictly positive and the log-ratio is finite on every row; no epsilon shifting or imputation is invoked. Behavior outside the positive domain is undefined and not claimed.",
      "vary_input": "lsd_p",
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
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
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
        "record_id": "chunk:147fa339122edc3ff44ba658",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:34c22cc63f163aed817525fd",
        "paper_id": "doi:10.1039/d5cs00613a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:682b714f21fe17245939e4e3",
        "paper_id": "doi:10.1063/1.2790903",
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
        "record_id": "chunk:06a26a29dca2516a90c93ace",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:234d54d6aae543beff87e7be",
        "paper_id": "doi:10.1039/b504006j",
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
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, the translational part of the adsorption entropy loss grows with the ratio of adsorbate van der Waals volume to the square of the framework free-path bottleneck diameter: molecules that are large relative to the passing window lose more translational freedom upon adsorption, so the descriptor associates positively with entropy loss/R. log(q_Vol) - 2.0 * log(q_lsd_f) At infinite dilution, adsorption suppresses rotational degrees of freedom of polyatomic adsorbates; the heavier and larger the molecule (proxied by the largest heavy-atom principal moment of inertia times vdW volume), the greater the rotational contribution to entropy loss, so the descriptor associates positively with entropy loss/R while vanishing for single-site adsorbates. q_PMI3 * q_Vol Frameworks whose included free-path diameter (Dif) greatly exceeds their passing bottleneck (Df) are cage-like with narrow windows; adsorbates in such structures retain local positional freedom inside cages but lose long-range translational freedom, and the pre-declared association is that increasing contrast correlates with increasing entropy loss/R (deeper configurational restriction relative to the gas). log(q_lsd_p / q_lsd_f)",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:0d886a705a91409f8e891c53",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e98dff054a73e56b28f6bdf3"
    ],
    "items": 10,
    "lexical_tokens": 4685,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [
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
      "id": "E07"
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
