# low/small_kg_rag_agent/replicate-1/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/small_kg_rag_agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h3",
    "name": "accessible_volume_shaping",
    "formula": "(AV/AV_ref) * ((LabuteASA/LabuteASA_ref) / (GeDi/GeDi_ref + 0.5))",
    "hypothesis": "Adsorption configurational entropy loss decreases with the amount of probe-accessible framework volume per mass (more accessible space retains more configurational freedom), but is modulated by adsorbate shape: elongated adsorbates (large GeDi relative to surface area) lose entropy faster as accessibility shrinks; the descriptor increases with retained entropy, so entropy loss decreases with it.",
    "rationale": "AV is a fixed-probe mass-specific accessibility proxy for the available configurational space; the shape contrast (area-to-length) captures how effectively a molecule can exploit that space orientationally. Limitations: AV is probe-specific and mass-specific, not molecule-specific free volume; zero AV does not mean zero physical adsorption space.",
    "falsification_criteria": "If entropy loss is uncorrelated or positively associated with AV across the training quantile range (e.g., confinement-dominated losses even in high-AV frameworks), or if the elongation contrast does not modulate the association, the accessibility-volume mechanism is falsified in favor of a bottleneck or site-geometry mechanism (E02, E04).",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E07"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "LabuteASA": "adsorbate_geometry_proxy",
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV proxies accessible configurational space despite fixed-probe and mass-specific bias; LabuteASA and GeDi proxy adsorbate shape. Retained-mobility effects (E05, E09) mean even high-AV frameworks can show large losses; kinetic escape arguments do not determine equilibrium entropy.",
      "physical_interpretation": "AV is fixed-probe, mass-specific accessibility (cm^3/g), not molecule-specific free volume, so no literal AV/Vol free-volume equality is claimed. GeDi is the largest heavy-atom pair distance and LabuteASA the approximate molecular surface area, both in the original heavy-atom representation with legitimate zeros. q-ratios are row-varying normalizations against fixed training references; q = 1 is not a physical threshold, and the +0.5 constant is an empirical smoother with no universal meaning.",
      "boundary_behavior": "At AV = 0 (28 legitimate training zeros) the descriptor is exactly 0 and finite by construction, encoding no accessibility benefit — AV = 0 does not imply zero physical adsorption space; at GeDi = 0 the denominator floor 0.5 keeps the expression finite; LabuteASA is strictly positive on the training domain.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
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

候选标识：`low/small_kg_rag_agent/replicate-1/round-3/h1`

最终状态：scored；边际收益：-0.024252 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.Vol

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_path_contrast",
    "formula": "(lsd_p/lsd_p_ref) - (lsd_f/lsd_f_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the difference between the largest included sphere along the free-sphere path and the passing bottleneck diameter proxies how much local conformational/configurational space a molecule retains relative to the constriction it must traverse; larger contrast (wider internal region relative to bottleneck) means more retained freedom in the adsorbed state, hence smaller entropy loss (s_ads/s_gas larger). Descriptor is expected to associate negatively with entropy loss.",
    "rationale": "Uses Dif and Df in their exact Zeo++ meanings: lsd_p is the included diameter along the free path, lsd_f the passing bottleneck. Their difference is dimensionless after q-normalization and isolates the confinement gradient along the diffusion path. This is an empirical proxy; it does not measure cavity Di and cannot establish causality. Correlations with entropy loss may be mediated by framework density or accessible volume.",
    "falsification_criteria": "If training Spearman between this descriptor and entropy loss is near zero or flips sign after controlling for AV and density (e.g., partial correlation), the path-contrast proxy fails and the association is better explained by pore volume alone. Also fails if the association is not monotone within the native lsd_f range [0.85684, 7.68726].",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif-Df contrast in fixed-probe geometry is a valid stand-in for the adsorbed-state configurational-space gradient; both are probe-geometry quantities, not molecule-specific free volumes.",
      "physical_interpretation": "Both terms are normalized by fixed training-reference medians (5.16326 A for lsd_f, 6.38663 A for lsd_p); q-unity carries no physical threshold meaning.",
      "boundary_behavior": "Both inputs are strictly positive over the training domain (no zeros), so the expression is finite for all 2361 rows; the difference can be negative, which is admissible since the descriptor is a monotone signed proxy, not a probability.",
      "vary_input": "lsd_p",
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
      "training_spearman": -0.015389337008441922,
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
    "name": "bottleneck_path_contrast",
    "formula": "log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the difference between the largest included sphere along the free-sphere path and the passing bottleneck diameter proxies how much local conformational/configurational space a molecule retains relative to the constriction it must traverse; larger contrast (wider internal region relative to bottleneck) means more retained freedom in the adsorbed state, hence smaller entropy loss (s_ads/s_gas larger). Descriptor is expected to associate negatively with entropy loss.",
    "rationale": "Replaces the signed Dif-Df contrast, which was training-inconclusive (Spearman ~ -0.015), with a multiplicative pore-capacity term (q_lsd_p * q_lsd_f) damped by molecular size (q_Vol^-0.5). Prior-round training diagnostics for this form showed a strong negative association with entropy loss (Spearman ~ -0.79), consistent with the predeclared decreasing entropy direction; this is a training-set association, not validated causality, and may be mediated by accessible volume or framework density.",
    "falsification_criteria": "Fails if the negative association disappears or flips after controlling for AV and density (partial correlation), or if it is not monotone within the native lsd_f range [0.85684, 7.68726]; also fails if the association is entirely explained by q_Vol alone (redundancy with molecular size).",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04",
      "E08"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif (included sphere along free path) and Df (passing bottleneck) are probe-geometry quantities, not global cavity Di; Vol is molecular vdW volume, not a framework free volume. The product is an empirical confinement-capacity proxy, not a molecule-specific free-volume ratio.",
      "physical_interpretation": "All three terms are normalized by fixed training references (6.38663 A, 5.16326 A, 67.24 A^3); q-unity carries no physical threshold meaning. Larger pore-path capacity relative to molecular volume is hypothesized to retain more adsorbed-state freedom, associating with smaller entropy loss.",
      "boundary_behavior": "lsd_p, lsd_f and Vol are strictly positive over the training domain, so the expression is finite for all 2361 rows; the log(1+.) squash keeps output positive and dimensionless.",
      "vary_input": "lsd_p",
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
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
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
      "training_spearman": -0.788415943126845,
      "target_association": "consistent",
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
    "name": "bottleneck_path_contrast",
    "formula": "log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the difference between the largest included sphere along the free-sphere path and the passing bottleneck diameter proxies how much local conformational/configurational space a molecule retains relative to the constriction it must traverse; larger contrast (wider internal region relative to bottleneck) means more retained freedom in the adsorbed state, hence smaller entropy loss (s_ads/s_gas larger). Descriptor is expected to associate negatively with entropy loss.",
    "rationale": "Replaces the signed Dif-Df contrast, which was training-inconclusive (Spearman ~ -0.015), with a multiplicative pore-capacity term (q_lsd_p * q_lsd_f) damped by molecular size (q_Vol^-0.5). Prior-round training diagnostics for this form showed a strong negative association with entropy loss (Spearman ~ -0.79), consistent with the predeclared decreasing entropy direction; this is a training-set association, not validated causality, and may be mediated by accessible volume or framework density.",
    "falsification_criteria": "Fails if the negative association disappears or flips after controlling for AV and density (partial correlation), or if it is not monotone within the native lsd_f range [0.85684, 7.68726]; also fails if the association is entirely explained by q_Vol alone (redundancy with molecular size).",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04",
      "E08"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif (included sphere along free path) and Df (passing bottleneck) are probe-geometry quantities, not global cavity Di; Vol is molecular vdW volume, not a framework free volume. The product is an empirical confinement-capacity proxy, not a molecule-specific free-volume ratio.",
      "physical_interpretation": "All three terms are normalized by fixed training references (6.38663 A, 5.16326 A, 67.24 A^3); q-unity carries no physical threshold meaning. Larger pore-path capacity relative to molecular volume is hypothesized to retain more adsorbed-state freedom, associating with smaller entropy loss.",
      "boundary_behavior": "lsd_p, lsd_f and Vol are strictly positive over the training domain, so the expression is finite for all 2361 rows; the log(1+.) squash keeps output positive and dimensionless.",
      "vary_input": "lsd_p",
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
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
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
      "training_spearman": -0.788415943126845,
      "target_association": "consistent",
      "perturbation": 0.0452717,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/small_kg_rag_agent/replicate-1/round-3/h2`

最终状态：scored；边际收益：-2.343077 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "planarity_confined_translation",
    "formula": "log(1 + (Vol/Vol_ref) * (PBF/PBF_ref + 0.1))",
    "hypothesis": "For adsorbates with nonzero heavy-atom planarity deviation (PBF > 0), larger molecular volume combined with larger out-of-plane thickness increases the fraction of translational modes suppressed inside zeolite channels, so entropy loss grows with Vol * PBF; planar molecules (PBF near 0) are hypothesized to lose less entropy in slit-like channel apertures because they can orient flat against framework walls. The descriptor therefore associates positively with entropy loss.",
    "rationale": "PBF is an original implicit-H/heavy-atom representation proxy with legitimate zeros (587 training rows); the +0.1 offset inside log keeps the argument strictly positive and finite for PBF=0 rows, and is an empirical smoothing constant, not a physical planarity threshold. Vol is the full molecular vdW volume (always positive). The product is a shape-size interaction term, claimed only as an empirical proxy for confined-translation suppression.",
    "falsification_criteria": "If within the PBF>0 subpopulation the association of this descriptor with entropy loss is not positive (Spearman <= 0), the planar-orientation hypothesis is falsified. Also falsified if adding MW as a control removes the association entirely (redundant with molecular size).",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "Heavy-atom PBF thickness proxies the ability to orient against channel walls; it is not all-atom molecular geometry, and zero PBF does not mean zero molecular thickness of hydrogens.",
      "physical_interpretation": "Vol is normalized by its fixed reference median 67.24 A^3 and PBF by 0.230845 A; log(1+·) is a dimensionless monotone squash. The 0.1 constant only guarantees finiteness at PBF=0.",
      "boundary_behavior": "At PBF=0 the descriptor reduces to log(1 + q_Vol), finite and positive for all rows; Vol has no zeros in training. No imputation is performed; the branch is analytic rather than rotor_case-segmented.",
      "vary_input": "PBF",
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
        "PBF",
        "Vol"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
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
      "training_spearman": 0.3363077479189018,
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
    "slot_id": "h2",
    "name": "planarity_confined_translation",
    "formula": "log(1 + (Vol/Vol_ref) * (PBF/PBF_ref + 0.1))",
    "hypothesis": "For adsorbates with nonzero heavy-atom planarity deviation (PBF > 0), larger molecular volume combined with larger out-of-plane thickness increases the fraction of translational modes suppressed inside zeolite channels, so entropy loss grows with Vol * PBF; planar molecules (PBF near 0) are hypothesized to lose less entropy in slit-like channel apertures because they can orient flat against framework walls. The descriptor therefore associates positively with entropy loss.",
    "rationale": "PBF is an original implicit-H/heavy-atom representation proxy with legitimate zeros (587 training rows); the +0.1 offset inside log keeps the argument strictly positive and finite for PBF=0 rows, and is an empirical smoothing constant, not a physical planarity threshold. Vol is the full molecular vdW volume (always positive). The product is a shape-size interaction term, claimed only as an empirical proxy for confined-translation suppression.",
    "falsification_criteria": "If within the PBF>0 subpopulation the association of this descriptor with entropy loss is not positive (Spearman <= 0), the planar-orientation hypothesis is falsified. Also falsified if adding MW as a control removes the association entirely (redundant with molecular size).",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "Heavy-atom PBF thickness proxies the ability to orient against channel walls; it is not all-atom molecular geometry, and zero PBF does not mean zero molecular thickness of hydrogens.",
      "physical_interpretation": "Vol is normalized by its fixed reference median 67.24 A^3 and PBF by 0.230845 A; log(1+·) is a dimensionless monotone squash. The 0.1 constant only guarantees finiteness at PBF=0.",
      "boundary_behavior": "At PBF=0 the descriptor reduces to log(1 + q_Vol), finite and positive for all rows; Vol has no zeros in training. No imputation is performed; the branch is analytic rather than rotor_case-segmented.",
      "vary_input": "PBF",
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
        "PBF",
        "Vol"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
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
      "training_spearman": 0.3363077479189018,
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
    "slot_id": "h2",
    "name": "planarity_confined_translation",
    "formula": "log(1 + (Vol/Vol_ref) * (PBF/PBF_ref + 0.1))",
    "hypothesis": "For adsorbates with nonzero heavy-atom planarity deviation (PBF > 0), larger molecular volume combined with larger out-of-plane thickness increases the fraction of translational modes suppressed inside zeolite channels, so entropy loss grows with Vol * PBF; planar molecules (PBF near 0) are hypothesized to lose less entropy in slit-like channel apertures because they can orient flat against framework walls. The descriptor therefore associates positively with entropy loss.",
    "rationale": "PBF is an original implicit-H/heavy-atom representation proxy with legitimate zeros (587 training rows); the +0.1 offset inside log keeps the argument strictly positive and finite for PBF=0 rows, and is an empirical smoothing constant, not a physical planarity threshold. Vol is the full molecular vdW volume (always positive). The product is a shape-size interaction term, claimed only as an empirical proxy for confined-translation suppression.",
    "falsification_criteria": "If within the PBF>0 subpopulation the association of this descriptor with entropy loss is not positive (Spearman <= 0), the planar-orientation hypothesis is falsified. Also falsified if adding MW as a control removes the association entirely (redundant with molecular size).",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "Heavy-atom PBF thickness proxies the ability to orient against channel walls; it is not all-atom molecular geometry, and zero PBF does not mean zero molecular thickness of hydrogens.",
      "physical_interpretation": "Vol is normalized by its fixed reference median 67.24 A^3 and PBF by 0.230845 A; log(1+·) is a dimensionless monotone squash. The 0.1 constant only guarantees finiteness at PBF=0.",
      "boundary_behavior": "At PBF=0 the descriptor reduces to log(1 + q_Vol), finite and positive for all rows; Vol has no zeros in training. No imputation is performed; the branch is analytic rather than rotor_case-segmented.",
      "vary_input": "PBF",
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
        "PBF",
        "Vol"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
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
      "training_spearman": 0.3363077479189018,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/small_kg_rag_agent/replicate-1/round-3/h3`

最终状态：scored；边际收益：-3.343483 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "rotational_anisotropy_ratio",
    "formula": "rotor_case(log(1 + q_PMI1), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5))",
    "hypothesis": "Rotational entropy loss at infinite dilution depends on how anisotropic the adsorbate's heavy-atom inertia tensor is: linear molecules (one negligible heavy-atom PMI) and near-linear nonlinear molecules with high PMI2/PMI1 aspect ratio retain more rotational freedom when confined (fewer restricted rotational coordinates align with channel axes) than isotropic rotors of equal size. The descriptor, an anisotropy aspect ratio (with PMI1 magnitude for single-site methane), is hypothesized to associate negatively with entropy loss (larger anisotropy, smaller entropy loss).",
    "rationale": "Uses only the original heavy-atom PMI proxies with the mandated rotor_case branching: single-site methane (54 rows) has zero heavy-atom PMI1 by construction, so its branch uses q_PMI1 = 0 and log(1+0)=0, finite without imputation; the linear branch uses the maximum(q_PMI1, 1e-10) guard only as a numerical finiteness safeguard, which coincides with legitimate zero PMI1 for linear rows (214 rows), not as a physical epsilon. The nonlinear branch uses the same aspect ratio. All branch outputs are dimensionless.",
    "falsification_criteria": "If the training Spearman between this descriptor and entropy loss within the nonlinear subpopulation alone is near zero or positive, the anisotropy-retention hypothesis is falsified. Also falsified if the linear-branch rows do not follow the same direction as nonlinear rows after stratification, indicating the rotor_case split does not represent a shared mechanism.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments approximate rotational anisotropy relevant to confinement but omit hydrogen contributions; single-site categorization is a dataset proxy, not a statement that all-atom inertia vanishes.",
      "physical_interpretation": "q_PMI1 and q_PMI2 are row-varying normalized inputs relative to fixed references (43.29514 and 93.79729 angstrom^2*amu); the aspect ratio is a dimensionless shape measure, and q-unity is not a physical threshold.",
      "boundary_behavior": "Single-site branch: q_PMI1 = 0 gives exactly 0. Linear branch: q_PMI1 = 0 is legitimate, and the 1e-10 maximum guard prevents division by zero while leaving the ratio large-but-finite; this is a numerical guard, not a physical law. Nonlinear branch: q_PMI1 > 0 for all 2093 nonlinear rows, ratio finite. Every row yields a finite value.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI1",
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
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI1",
        "PMI2"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI2": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        333.6293867
      ],
      "training_spearman": -0.016173301771764504,
      "target_association": "inconclusive",
      "perturbation": 3.956905037,
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
    "name": "rotational_anisotropy_ratio",
    "formula": "rotor_case(0.0, log(1 + (PMI2/PMI2_ref)**0.5), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5))",
    "hypothesis": "Rotational entropy loss at infinite dilution depends on how anisotropic the adsorbate's heavy-atom inertia tensor is: linear molecules (one negligible heavy-atom PMI) and near-linear nonlinear molecules with high PMI2/PMI1 aspect ratio retain more rotational freedom when confined (fewer restricted rotational coordinates align with channel axes) than isotropic rotors of equal size. The descriptor, an anisotropy aspect ratio (with PMI1 magnitude for single-site methane), is hypothesized to associate negatively with entropy loss (larger anisotropy, smaller entropy loss).",
    "rationale": "Corrects the degenerate linear-branch expression: in the original draft the ratio (q_PMI2/maximum(q_PMI1,1e-10))**0.5 was evaluated on linear rows where legitimate zero PMI1 makes the descriptor an uncontrolled branch artifact rather than an anisotropy measure. The aspect ratio is retained only in the nonlinear branch where the mechanism is defined; the linear branch uses a monotone rotational size term. Training association for the anisotropy family remains inconclusive (Spearman ~ -0.016); this is an empirical proxy without validated causality.",
    "falsification_criteria": "Fails if the training Spearman within the nonlinear subpopulation is near zero or positive, or if linear-branch rows do not follow the same direction as nonlinear rows after stratification, indicating the rotor_case split does not represent a shared mechanism.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E05",
      "E06"
    ],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies omit hydrogen contributions; single-site categorization is a dataset proxy, not a claim that all-atom inertia vanishes. The PMI2/PMI1 aspect ratio is meaningful only where PMI1 > 0, so it is confined to the nonlinear branch; applying it to linear rows was a domain mistake in the prior draft.",
      "physical_interpretation": "q_PMI1 and q_PMI2 are row-varying normalized inputs relative to fixed references (43.29514 and 93.79729 angstrom^2*amu); the aspect ratio is a dimensionless shape measure and q-unity is not a physical threshold. The 1e-10 maximum guard is a numerical finiteness safeguard only, not a physical epsilon or law.",
      "boundary_behavior": "Single-site branch (54 rows): exactly 0. Linear branch (214 rows): PMI1 is legitimately zero for linear heavy-atom representation, so the anisotropy ratio would be a division-by-zero artifact; the corrected linear branch uses only the positive q_PMI2 size term, finite for all rows. Nonlinear branch (2093 rows): q_PMI1 > 0, ratio finite. Every row yields a finite value without imputation.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI1",
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
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI1",
        "PMI2"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI2": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        333.6293867
      ],
      "training_spearman": 0.17298810756530156,
      "target_association": "contradicted",
      "perturbation": 3.956905037,
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
    "name": "rotational_anisotropy_ratio",
    "formula": "rotor_case(0.0, log(1 + (PMI2/PMI2_ref)**0.5), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5))",
    "hypothesis": "Rotational entropy loss at infinite dilution depends on how anisotropic the adsorbate's heavy-atom inertia tensor is: linear molecules (one negligible heavy-atom PMI) and near-linear nonlinear molecules with high PMI2/PMI1 aspect ratio retain more rotational freedom when confined (fewer restricted rotational coordinates align with channel axes) than isotropic rotors of equal size. The descriptor, an anisotropy aspect ratio (with PMI1 magnitude for single-site methane), is hypothesized to associate negatively with entropy loss (larger anisotropy, smaller entropy loss).",
    "rationale": "Corrects the degenerate linear-branch expression: in the original draft the ratio (q_PMI2/maximum(q_PMI1,1e-10))**0.5 was evaluated on linear rows where legitimate zero PMI1 makes the descriptor an uncontrolled branch artifact rather than an anisotropy measure. The aspect ratio is retained only in the nonlinear branch where the mechanism is defined; the linear branch uses a monotone rotational size term. Training association for the anisotropy family remains inconclusive (Spearman ~ -0.016); this is an empirical proxy without validated causality.",
    "falsification_criteria": "Fails if the training Spearman within the nonlinear subpopulation is near zero or positive, or if linear-branch rows do not follow the same direction as nonlinear rows after stratification, indicating the rotor_case split does not represent a shared mechanism.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E05",
      "E06"
    ],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies omit hydrogen contributions; single-site categorization is a dataset proxy, not a claim that all-atom inertia vanishes. The PMI2/PMI1 aspect ratio is meaningful only where PMI1 > 0, so it is confined to the nonlinear branch; applying it to linear rows was a domain mistake in the prior draft.",
      "physical_interpretation": "q_PMI1 and q_PMI2 are row-varying normalized inputs relative to fixed references (43.29514 and 93.79729 angstrom^2*amu); the aspect ratio is a dimensionless shape measure and q-unity is not a physical threshold. The 1e-10 maximum guard is a numerical finiteness safeguard only, not a physical epsilon or law.",
      "boundary_behavior": "Single-site branch (54 rows): exactly 0. Linear branch (214 rows): PMI1 is legitimately zero for linear heavy-atom representation, so the anisotropy ratio would be a division-by-zero artifact; the corrected linear branch uses only the positive q_PMI2 size term, finite for all rows. Nonlinear branch (2093 rows): q_PMI1 > 0, ratio finite. Every row yields a finite value without imputation.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI1",
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
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI1",
        "PMI2"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI2": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        333.6293867
      ],
      "training_spearman": 0.17298810756530156,
      "target_association": "contradicted",
      "perturbation": 3.956905037,
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
        "record_id": "chunk:7342d031262bdf8cf5e759a2",
        "paper_id": "doi:10.1002/cphc.202300022",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d3a799358d58da57167e96f1",
        "paper_id": "doi:10.1021/acs.langmuir.3c03931",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:234d54d6aae543beff87e7be",
        "paper_id": "doi:10.1039/b504006j",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3dd1e3b89a0f8f43f056aaa3",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:4151da1ef2dd52bfcabf82ce",
        "paper_id": "doi:10.1021/jp9014405",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6ca1143916b8e66b0a19e889",
        "paper_id": "pmc:pmc8879942",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:773590832eac6c7df0ec1cd5",
        "paper_id": "doi:10.1021/jp9014405",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd6885398e28529d477ac4c3",
        "paper_id": "doi:10.1021/acs.jpcb.4c02650",
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
        "record_id": "chunk:46f247733ebb113afc9a8a26",
        "paper_id": "doi:10.1021/jp050434m",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:72dfcce988c17185f87c465c",
        "paper_id": "doi:10.1021/jp1096663",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7765ca1d2f5ad252ac5811bd",
        "paper_id": "doi:10.1063/1.2790903",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, the difference between the largest included sphere along the free-sphere path and the passing bottleneck diameter proxies how much local conformational/configurational space a molecule retains relative to the constriction it must traverse; larger contrast (wider internal region relative to bottleneck) means more retained freedom in the adsorbed state, hence smaller entropy loss (s_ads/s_gas larger). Descriptor is expected to associate negatively with entropy loss. (lsd_p/lsd_p_ref) - (lsd_f/lsd_f_ref) For adsorbates with nonzero heavy-atom planarity deviation (PBF > 0), larger molecular volume combined with larger out-of-plane thickness increases the fraction of translational modes suppressed inside zeolite channels, so entropy loss grows with Vol * PBF; planar molecules (PBF near 0) are hypothesized to lose less entropy in slit-like channel apertures because they can orient flat against framework walls. The descriptor therefore associates positively with entropy loss. log(1 + (Vol/Vol_ref) * (PBF/PBF_ref + 0.1)) Rotational entropy loss at infinite dilution depends on how anisotropic the adsorbate's heavy-atom inertia tensor is: linear molecules (one negligible heavy-atom PMI) and near-linear nonlinear molecules with high PMI2/PMI1 aspect ratio retain more rotational freedom when confined (fewer restricted rotational coordinates align with channel axes) than isotropic rotors of equal size. The descriptor, an anisotropy aspect ratio (with PMI1 magnitude for single-site methane), is hypothesized to associate negatively with entropy loss (larger anisotropy, smaller entropy loss). rotor_case(log(1 + q_PMI1), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5))   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:8ffcc4698d37d4f5569d53f5",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:0d886a705a91409f8e891c53"
    ],
    "items": 10,
    "lexical_tokens": 4604,
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
      "record_id": "chunk:8ffcc4698d37d4f5569d53f5",
      "paper_id": "doi:10.1021/acs.jpcc.0c02671",
      "document_id": "document:679638c993b24ed3004656c6",
      "quote": "and 32 , corresponding to 1 , 3-dioxolane , 1 , 3 , 5-trioxane , and acetonitrile , respectively . These adsorbates are two cyclic ethers and one nitrile . In this case , we suspect that the unique chemical functionality of these adsorbates , in comparison to the other TraPPE species , results in a larger-than-expected entropy loss . Finally, the $ \\eta $ slopes in Figure 1 and the examination of adsorbate-specific entropy ratios in Figure 3 are suggestive of an entropy loss model based primarily on certain adsorbent characteristics. As pointed out above, $ \\eta $ is roughly the same for (1) FAU and LTA and (2) FER and MFI; the adsorbents in each of these two groups have roughly the same LCD and predominantly cage-like, spherical pores. The MOR topology has, as mentioned previously, an LCD similar to FER and MFI but with channel pores. Other pore descriptors are, of course, available as well, and we examine two others here. First, as a compliment to the LCD descriptor, we include the “maximum included sphere diameter” (MSD), which is the largest sphere pore identified in a calculated pore size distribution. $ ^{55} $ Second, we also include a different type of geometric descriptor, the “occupiable volume” ( $ V_{occ} $), which is defined as the volume per 1000 Å of the crystal cell that can be accessed by the center of probe molecules with diameter 2.8 Å. $ ^{56} $ These three pore size descriptors capture both the size of the largest pore features and the overall pore volume. In Figure 4, we plot the $ \\eta $ slope for each adsorbent as a function of these three pore metrics; diameter-based metrics are on the lower x-axis and occupiable volume is on the upper x-axis. The important result shown in Figure 4 is that, regardless of the metric used to characterize the zeolite adsorbent, the slope of the entropy relationship in Figure 1 follows the same qualitative trend. Starting at the largest pore adsorbents in terms of any of the three metrics, $ \\eta $ decreases slowly with decreasing pore size, before decreasing more rapidly to values in the vicinity of $ \\eta = 0.75 $. Despite plotting all three metrics on the x-axis of Figure 4, we imply no quantitative relationship between MSD/LCD and $ V_{occ} $; the purpose is to show the common trend in the correlation of $ \\eta $ with different size metrics. (As an aside, we note that the upper and lower x-axes have common scaling, i.e., they share a common x",
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
