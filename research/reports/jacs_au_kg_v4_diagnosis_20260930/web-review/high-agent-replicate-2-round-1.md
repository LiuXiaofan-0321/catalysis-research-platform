# high/agent/replicate-2/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`high/agent/replicate-2/round-1/h1`

最终状态：scored；边际收益：+2.738553 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "confinement_accessibility_descriptor",
    "formula": "log(1 + q_AV) + 0.5 * log(1 + q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, frameworks that offer more fixed-probe accessible specific volume (AV) and a wider passing bottleneck (lsd_f = Zeo++ Df) confine adsorbates less translationally, so the predeclared association is: entropy loss on adsorption (s_gas - s_ads)/R DECREASES as this descriptor increases; equivalently s_ads/s_gas increases. This is a predeclared proxy-derivative association claim, not a causal or novelty claim, and the descriptor only re-expresses inputs already present in the nonlinear ANN.",
    "rationale": "Mechanism: translational/configurational entropy of the adsorbed phase scales with accessible free space and with the width of channel windows that permit diffusion between cages. AV is a mass-specific fixed-probe accessibility and is used here only as a proxy for translational free space, not as molecule-specific free volume; lsd_f is the bottleneck free sphere along a periodic free path, explicitly NOT the global cavity diameter Di. Limitations: AV=0 for the fixed geometric probe does not imply zero physical adsorption space, so the +1 offset inside the log (a smoothing constant with no universal physical meaning) keeps the descriptor finite and continuous at legitimate zeros. Both native inputs already enter the published nonlinear ANN; this formula is a monotone re-expression whose value lies in making a falsifiable directional prediction.",
    "falsification_criteria": "The predeclared decreasing association of entropy loss fails if (a) entropy loss instead increases with AV (e.g., if larger accessible surface-to-volume ratios enhance adsorbate-surface vibrational coupling that removes more entropy than the added translational free volume restores), (b) the dominant control is the included diameter along the path (lsd_p) or framework density rather than accessibility plus bottleneck, or (c) the association holds only within zeolite families and reverses across low-density frameworks near the training minimum (density 0.7597, AV up to 0.6613).",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV and lsd_f computed with one fixed geometric probe are assumed monotone proxies for translational free space and window width for diverse adsorbates; transferability across adsorbate sizes is an assumption, not a derived equality. No physical q-unity threshold is asserted.",
      "physical_interpretation": "q_AV = AV/AV_ref and q_lsd_f = lsd_f/lsd_f_ref are dimensionless row-varying inputs normalized by fixed training-reference medians (0.0759781 cm^3/g and 5.16326 angstrom); AV_ref and lsd_f_ref are constants, and the descriptor never divides by a native value. Entropy_direction 'decreasing' means the entropy loss (s_gas - s_ads)/R decreases with the descriptor (s_ads/s_gas increases).",
      "boundary_behavior": "AV has 28 legitimate zeros in training; log(1 + q_AV) = 0 there, which encodes 'fixed-probe sees no accessible volume' without imputing a fake positive value. lsd_f is strictly positive in the training domain (min 0.85684), so q_lsd_f > 0 on every row. The descriptor is finite for every training row; the +1 offsets are empirical smoothing constants, not physical length scales.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
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
        "AV",
        "lsd_f"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.48066584979265486,
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
    "name": "confinement_accessibility_descriptor",
    "formula": "log(1 + q_AV) + 0.5 * log(1 + q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, frameworks that offer more fixed-probe accessible specific volume (AV) and a wider passing bottleneck (lsd_f = Zeo++ Df) confine adsorbates less translationally, so the predeclared association is: entropy loss on adsorption (s_gas - s_ads)/R DECREASES as this descriptor increases; equivalently s_ads/s_gas increases. This is a predeclared proxy-derivative association claim, not a causal or novelty claim, and the descriptor only re-expresses inputs already present in the nonlinear ANN.",
    "rationale": "Mechanism: translational/configurational entropy of the adsorbed phase scales with accessible free space and with the width of channel windows that permit diffusion between cages. AV is a mass-specific fixed-probe accessibility and is used here only as a proxy for translational free space, not as molecule-specific free volume; lsd_f is the bottleneck free sphere along a periodic free path, explicitly NOT the global cavity diameter Di. Limitations: AV=0 for the fixed geometric probe does not imply zero physical adsorption space, so the +1 offset inside the log (a smoothing constant with no universal physical meaning) keeps the descriptor finite and continuous at legitimate zeros. Both native inputs already enter the published nonlinear ANN; this formula is a monotone re-expression whose value lies in making a falsifiable directional prediction.",
    "falsification_criteria": "The predeclared decreasing association of entropy loss fails if (a) entropy loss instead increases with AV (e.g., if larger accessible surface-to-volume ratios enhance adsorbate-surface vibrational coupling that removes more entropy than the added translational free volume restores), (b) the dominant control is the included diameter along the path (lsd_p) or framework density rather than accessibility plus bottleneck, or (c) the association holds only within zeolite families and reverses across low-density frameworks near the training minimum (density 0.7597, AV up to 0.6613).",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV and lsd_f computed with one fixed geometric probe are assumed monotone proxies for translational free space and window width for diverse adsorbates; transferability across adsorbate sizes is an assumption, not a derived equality. No physical q-unity threshold is asserted.",
      "physical_interpretation": "q_AV = AV/AV_ref and q_lsd_f = lsd_f/lsd_f_ref are dimensionless row-varying inputs normalized by fixed training-reference medians (0.0759781 cm^3/g and 5.16326 angstrom); AV_ref and lsd_f_ref are constants, and the descriptor never divides by a native value. Entropy_direction 'decreasing' means the entropy loss (s_gas - s_ads)/R decreases with the descriptor (s_ads/s_gas increases).",
      "boundary_behavior": "AV has 28 legitimate zeros in training; log(1 + q_AV) = 0 there, which encodes 'fixed-probe sees no accessible volume' without imputing a fake positive value. lsd_f is strictly positive in the training domain (min 0.85684), so q_lsd_f > 0 on every row. The descriptor is finite for every training row; the +1 offsets are empirical smoothing constants, not physical length scales.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
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
        "AV",
        "lsd_f"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.48066584979265486,
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
    "name": "confinement_accessibility_descriptor",
    "formula": "log(1 + q_AV) + 0.5 * log(1 + q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, frameworks that offer more fixed-probe accessible specific volume (AV) and a wider passing bottleneck (lsd_f = Zeo++ Df) confine adsorbates less translationally, so the predeclared association is: entropy loss on adsorption (s_gas - s_ads)/R DECREASES as this descriptor increases; equivalently s_ads/s_gas increases. This is a predeclared proxy-derivative association claim, not a causal or novelty claim, and the descriptor only re-expresses inputs already present in the nonlinear ANN.",
    "rationale": "Mechanism: translational/configurational entropy of the adsorbed phase scales with accessible free space and with the width of channel windows that permit diffusion between cages. AV is a mass-specific fixed-probe accessibility and is used here only as a proxy for translational free space, not as molecule-specific free volume; lsd_f is the bottleneck free sphere along a periodic free path, explicitly NOT the global cavity diameter Di. Limitations: AV=0 for the fixed geometric probe does not imply zero physical adsorption space, so the +1 offset inside the log (a smoothing constant with no universal physical meaning) keeps the descriptor finite and continuous at legitimate zeros. Both native inputs already enter the published nonlinear ANN; this formula is a monotone re-expression whose value lies in making a falsifiable directional prediction.",
    "falsification_criteria": "The predeclared decreasing association of entropy loss fails if (a) entropy loss instead increases with AV (e.g., if larger accessible surface-to-volume ratios enhance adsorbate-surface vibrational coupling that removes more entropy than the added translational free volume restores), (b) the dominant control is the included diameter along the path (lsd_p) or framework density rather than accessibility plus bottleneck, or (c) the association holds only within zeolite families and reverses across low-density frameworks near the training minimum (density 0.7597, AV up to 0.6613).",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV and lsd_f computed with one fixed geometric probe are assumed monotone proxies for translational free space and window width for diverse adsorbates; transferability across adsorbate sizes is an assumption, not a derived equality. No physical q-unity threshold is asserted.",
      "physical_interpretation": "q_AV = AV/AV_ref and q_lsd_f = lsd_f/lsd_f_ref are dimensionless row-varying inputs normalized by fixed training-reference medians (0.0759781 cm^3/g and 5.16326 angstrom); AV_ref and lsd_f_ref are constants, and the descriptor never divides by a native value. Entropy_direction 'decreasing' means the entropy loss (s_gas - s_ads)/R decreases with the descriptor (s_ads/s_gas increases).",
      "boundary_behavior": "AV has 28 legitimate zeros in training; log(1 + q_AV) = 0 there, which encodes 'fixed-probe sees no accessible volume' without imputing a fake positive value. lsd_f is strictly positive in the training domain (min 0.85684), so q_lsd_f > 0 on every row. The descriptor is finite for every training row; the +1 offsets are empirical smoothing constants, not physical length scales.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
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
        "AV",
        "lsd_f"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.48066584979265486,
      "target_association": "consistent",
      "perturbation": 0.001538232,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/agent/replicate-2/round-1/h2`

最终状态：scored；边际收益：+4.123678 pp；保留：True。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
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
        "PMI1",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.205832341455294,
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
        "PMI1",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.205832341455294,
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
        "PMI1",
        "PMI3"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.205832341455294,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/agent/replicate-2/round-1/h3`

最终状态：scored；边际收益：+0.789011 pp；保留：False。

复核改动字段：falsification_criteria, physical_claims, rationale, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "size_bottleneck_mismatch_descriptor",
    "formula": "log(1 + q_Vol) - log(1 + q_lsd_f)",
    "hypothesis": "At infinite dilution in pure-silica rigid zeolites, entropy loss is controlled by the mismatch between adsorbate van der Waals volume and the framework passing bottleneck: the predeclared association is that entropy loss (s_gas - s_ads)/R INCREASES when adsorbate Vol is large relative to lsd_f (Zeo++ Df), and DECREASES with lsd_f at fixed Vol; hence s_ads/s_gas decreases with this descriptor. This is a coupling-association hypothesis over inputs already present in the ANN, not new information and not a causal claim.",
    "rationale": "Mechanism: a large molecule propagating through narrow windows samples fewer accessible translational microstates; the operative geometric comparison is molecule volume against the bottleneck (Df), not the global cavity diameter Di (not among the inputs). The difference of dimensionless logarithms expresses this mismatch symmetrically: it rises with Vol and falls with lsd_f, so a single increasing descriptor tracks an entropy-loss-increasing direction for the predeclared vary_input Vol. Limitations: Vol is a molecular vdW volume and lsd_f a hard-sphere geometric bottleneck; neither captures framework flexibility, specific dispersion anisotropy, or the true molecule-specific free volume, so the coupling is a proxy association with assumed transferability across the training domain (Vol 20.424-161.144 angstrom^3, lsd_f 0.85684-7.68726 angstrom).",
    "falsification_criteria": "The coupling hypothesis fails if (a) entropy loss depends on the included-along-path diameter lsd_p or framework density instead of the bottleneck contrast, (b) adding Vol alone to the existing ANN removes all incremental value of the mismatch term (no interaction), or (c) at large openings (lsd_f near its maximum 7.68726) entropy loss still increases with Vol at the same rate, implying a size-only mechanism rather than size-vs-bottleneck coupling.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Molecular vdW volume and Zeo++ Df bottleneck are assumed to jointly proxy the geometric crowding that removes translational entropy at infinite dilution; the proxy ignores framework relaxation, all-atom shape, and molecule-specific accessible volume. No physical q-unity threshold is asserted; the ratio of the two normalized terms carries no universal equality meaning.",
      "physical_interpretation": "q_Vol = Vol/Vol_ref and q_lsd_f = lsd_f/lsd_f_ref are dimensionless row-varying inputs normalized by fixed training-reference medians (67.24 angstrom^3 and 5.16326 angstrom); references are constants, and lsd_f is strictly positive in the training domain so no division by zero occurs. Entropy_direction 'increasing' means entropy loss (s_gas - s_ads)/R increases with the descriptor as Vol grows (s_ads/s_gas decreases).",
      "boundary_behavior": "Vol has zero_n = 0 (minimum 20.424), and lsd_f has zero_n = 0 (minimum 0.85684), so log(1 + q_Vol) and log(1 + q_lsd_f) are finite and strictly positive on every training row; the +1 offsets are smoothing constants without physical meaning and are not needed to avoid legitimate zeros here. The descriptor is finite for all 2361 training rows and varies smoothly across the full [0,1] quantile regime of Vol.",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6384521823948741,
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
    "name": "size_bottleneck_mismatch_descriptor",
    "formula": "log(1 + q_Vol) - log(1 + q_lsd_f)",
    "hypothesis": "At infinite dilution in pure-silica rigid zeolites, entropy loss is controlled by the mismatch between adsorbate van der Waals volume and the framework passing bottleneck: the predeclared association is that entropy loss (s_gas - s_ads)/R INCREASES when adsorbate Vol is large relative to lsd_f (Zeo++ Df), and DECREASES with lsd_f at fixed Vol; hence s_ads/s_gas decreases with this descriptor. This is a coupling-association hypothesis over inputs already present in the ANN, not new information and not a causal claim.",
    "rationale": "Mechanism: a large molecule propagating through narrow windows samples fewer accessible translational microstates; the operative geometric comparison is adsorbate size against the periodic-path bottleneck (Df), not the global cavity diameter Di (not among the inputs) and not a probe-accessible volume. The difference of dimensionless logarithms expresses this mismatch: it rises with Vol and falls with lsd_f, so a single increasing descriptor tracks the entropy-loss-increasing direction for the predeclared vary_input Vol. Correction applied: the physical-claim tag is geometric_path_contrast (a size-vs-bottleneck geometric contrast between a molecular vdW volume and a passing-sphere diameter), not probe_volume_proxy, since no fixed-probe accessibility quantity (AV/ASA) enters this descriptor. Limitations: Vol and lsd_f are hard-sphere/geometric proxies that capture neither framework flexibility nor specific dispersion anisotropy, so the coupling is a proxy association with assumed transferability across the training domain.",
    "falsification_criteria": "The coupling hypothesis fails if (a) entropy loss depends on the included-along-path diameter lsd_p or framework density instead of the bottleneck contrast, (b) adding Vol alone to the existing ANN removes all incremental value of the mismatch term (no interaction), or (c) at large openings (lsd_f near its maximum 7.68726 angstrom) entropy loss still increases with Vol at the same rate, implying a size-only mechanism rather than a size-vs-bottleneck geometric path contrast.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Molecular vdW volume (a molecule-intrinsic property) and Zeo++ Df (the largest sphere that can pass through a periodic free path, i.e., a bottleneck/window width, NOT the global cavity diameter Di and NOT a probe-accessible volume) are assumed to jointly proxy the geometric crowding that removes translational entropy at infinite dilution. This is a size-versus-passage contrast between two geometric quantities of different character; it ignores framework relaxation, all-atom adsorbate shape, symmetry numbers, and molecule-specific accessible volume. Transferability across the training domain (Vol 20.424-161.144 angstrom^3, lsd_f 0.85684-7.68726 angstrom) is assumed, not derived. No physical q-unity threshold is asserted; the difference of normalized logarithms carries no universal equality meaning.",
      "physical_interpretation": "Vol is the adsorbate van der Waals volume (angstrom^3); lsd_f is the Zeo++ Df passing-bottleneck free-sphere diameter (angstrom), explicitly not the included-along-path diameter Dif (lsd_p) and not the global cavity Di. q_Vol = Vol/Vol_ref and q_lsd_f = lsd_f/lsd_f_ref are dimensionless row-varying inputs normalized by fixed training-reference medians (67.24 angstrom^3 and 5.16326 angstrom); the references are constants and the formula never divides by a native value. Both lsd_f and lsd_p are strictly positive in the training domain, so no division by zero occurs. Entropy_direction 'increasing' means entropy loss (s_gas - s_ads)/R increases with the descriptor as Vol grows relative to the bottleneck (s_ads/s_gas decreases).",
      "boundary_behavior": "Vol has zero_n = 0 (minimum 20.424), and lsd_f has zero_n = 0 (minimum 0.85684), so log(1 + q_Vol) and log(1 + q_lsd_f) are finite and strictly positive on every training row; the +1 offsets are smoothing constants without physical meaning and are not needed to avoid legitimate zeros here. The descriptor is finite for all 2361 training rows and varies smoothly across the full [0,1] quantile regime of Vol.",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6384521823948741,
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
    "name": "size_bottleneck_mismatch_descriptor",
    "formula": "log(1 + q_Vol) - log(1 + q_lsd_f)",
    "hypothesis": "At infinite dilution in pure-silica rigid zeolites, entropy loss is controlled by the mismatch between adsorbate van der Waals volume and the framework passing bottleneck: the predeclared association is that entropy loss (s_gas - s_ads)/R INCREASES when adsorbate Vol is large relative to lsd_f (Zeo++ Df), and DECREASES with lsd_f at fixed Vol; hence s_ads/s_gas decreases with this descriptor. This is a coupling-association hypothesis over inputs already present in the ANN, not new information and not a causal claim.",
    "rationale": "Mechanism: a large molecule propagating through narrow windows samples fewer accessible translational microstates; the operative geometric comparison is adsorbate size against the periodic-path bottleneck (Df), not the global cavity diameter Di (not among the inputs) and not a probe-accessible volume. The difference of dimensionless logarithms expresses this mismatch: it rises with Vol and falls with lsd_f, so a single increasing descriptor tracks the entropy-loss-increasing direction for the predeclared vary_input Vol. Correction applied: the physical-claim tag is geometric_path_contrast (a size-vs-bottleneck geometric contrast between a molecular vdW volume and a passing-sphere diameter), not probe_volume_proxy, since no fixed-probe accessibility quantity (AV/ASA) enters this descriptor. Limitations: Vol and lsd_f are hard-sphere/geometric proxies that capture neither framework flexibility nor specific dispersion anisotropy, so the coupling is a proxy association with assumed transferability across the training domain.",
    "falsification_criteria": "The coupling hypothesis fails if (a) entropy loss depends on the included-along-path diameter lsd_p or framework density instead of the bottleneck contrast, (b) adding Vol alone to the existing ANN removes all incremental value of the mismatch term (no interaction), or (c) at large openings (lsd_f near its maximum 7.68726 angstrom) entropy loss still increases with Vol at the same rate, implying a size-only mechanism rather than a size-vs-bottleneck geometric path contrast.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Molecular vdW volume (a molecule-intrinsic property) and Zeo++ Df (the largest sphere that can pass through a periodic free path, i.e., a bottleneck/window width, NOT the global cavity diameter Di and NOT a probe-accessible volume) are assumed to jointly proxy the geometric crowding that removes translational entropy at infinite dilution. This is a size-versus-passage contrast between two geometric quantities of different character; it ignores framework relaxation, all-atom adsorbate shape, symmetry numbers, and molecule-specific accessible volume. Transferability across the training domain (Vol 20.424-161.144 angstrom^3, lsd_f 0.85684-7.68726 angstrom) is assumed, not derived. No physical q-unity threshold is asserted; the difference of normalized logarithms carries no universal equality meaning.",
      "physical_interpretation": "Vol is the adsorbate van der Waals volume (angstrom^3); lsd_f is the Zeo++ Df passing-bottleneck free-sphere diameter (angstrom), explicitly not the included-along-path diameter Dif (lsd_p) and not the global cavity Di. q_Vol = Vol/Vol_ref and q_lsd_f = lsd_f/lsd_f_ref are dimensionless row-varying inputs normalized by fixed training-reference medians (67.24 angstrom^3 and 5.16326 angstrom); the references are constants and the formula never divides by a native value. Both lsd_f and lsd_p are strictly positive in the training domain, so no division by zero occurs. Entropy_direction 'increasing' means entropy loss (s_gas - s_ads)/R increases with the descriptor as Vol grows relative to the bottleneck (s_ads/s_gas decreases).",
      "boundary_behavior": "Vol has zero_n = 0 (minimum 20.424), and lsd_f has zero_n = 0 (minimum 0.85684), so log(1 + q_Vol) and log(1 + q_lsd_f) are finite and strictly positive on every training row; the +1 offsets are smoothing constants without physical meaning and are not needed to avoid legitimate zeros here. The descriptor is finite for all 2361 training rows and varies smoothly across the full [0,1] quantile regime of Vol.",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6384521823948741,
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
