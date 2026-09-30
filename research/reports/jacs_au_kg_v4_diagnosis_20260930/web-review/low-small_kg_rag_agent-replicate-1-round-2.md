# low/small_kg_rag_agent/replicate-1/round-2

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

候选标识：`low/small_kg_rag_agent/replicate-1/round-2/h1`

最终状态：scored；边际收益：-0.024252 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_cavity_capacity",
    "formula": "log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)",
    "hypothesis": "At infinite dilution, entropy loss on adsorption decreases when the included free-sphere diameter along the diffusion path (lsd_p) is large relative to the bottleneck (lsd_f): a large included region behind a comparable bottleneck gives the molecule more positional freedom in the sorbate pocket, so the descriptor increases with retained entropy and entropy loss decreases with it. Molecular volume acts as a size penalty: bulkier adsorbates lose translational/configurational freedom faster in the same framework.",
    "rationale": "Uses lsd_p (included along path) and lsd_f (bottleneck) as complementary geometric contrasts, explicitly not conflating either with a global cavity diameter Di. Vol is a van der Waals volume proxy for molecular size, not a free-volume equality. The product form is an empirical proxy combination; log keeps the descriptor finite and dimensionless. Limitations: fixed-probe geometric descriptors may miss framework flexibility and chemical specificity (pure-silica, no energetic heterogeneity).",
    "falsification_criteria": "If entropy loss increases with lsd_p for fixed lsd_f and Vol in held-out frameworks, the 'larger included region retains entropy' mechanism is falsified in favor of a strong-confinement/entropy-trap mechanism. Partial derivative of the descriptor w.r.t. lsd_f must be positive (regime_input lsd_f, native bounds [0.85684, 7.68726]); if the target association with this derivative is opposite, the hypothesis fails.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
      "proxy_assumptions": "lsd_p and lsd_f are rigid-framework geometric extremes on a fixed probe; they proxy accessible configurational extent but not energetics. Vol proxies molecular size; heavy-atom-based Vol may undercount small adsorbates.",
      "physical_interpretation": "All ratios are q-normalized against fixed training medians; no q-unity value is treated as a physical equality threshold. Log argument is dimensionless.",
      "boundary_behavior": "lsd_p, lsd_f, and Vol have strictly positive training ranges, so log(1 + positive) is always finite; no zero-division occurs. Descriptor approaches 0 as sizes shrink to the lower training bounds, which is a limiting artifact of the proxy, not a physical singularity.",
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

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_cavity_capacity",
    "formula": "log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)",
    "hypothesis": "At infinite dilution, entropy loss on adsorption decreases when the included free-sphere diameter along the diffusion path (lsd_p) is large relative to the bottleneck (lsd_f): a large included region behind a comparable bottleneck gives the molecule more positional freedom in the sorbate pocket, so the descriptor increases with retained entropy and entropy loss decreases with it. Molecular volume acts as a size penalty: bulkier adsorbates lose translational/configurational freedom faster in the same framework.",
    "rationale": "Uses lsd_p (included along path) and lsd_f (bottleneck) as complementary geometric contrasts, explicitly not conflating either with a global cavity diameter Di. Vol is a van der Waals volume proxy for molecular size, not a free-volume equality. The product form is an empirical proxy combination; log keeps the descriptor finite and dimensionless. Limitations: fixed-probe geometric descriptors may miss framework flexibility and chemical specificity (pure-silica, no energetic heterogeneity).",
    "falsification_criteria": "If entropy loss increases with lsd_p for fixed lsd_f and Vol in held-out frameworks, the 'larger included region retains entropy' mechanism is falsified in favor of a strong-confinement/entropy-trap mechanism. Partial derivative of the descriptor w.r.t. lsd_f must be positive (regime_input lsd_f, native bounds [0.85684, 7.68726]); if the target association with this derivative is opposite, the hypothesis fails.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
      "proxy_assumptions": "lsd_p and lsd_f are rigid-framework geometric extremes on a fixed probe; they proxy accessible configurational extent but not energetics. Vol proxies molecular size; heavy-atom-based Vol may undercount small adsorbates.",
      "physical_interpretation": "All ratios are q-normalized against fixed training medians; no q-unity value is treated as a physical equality threshold. Log argument is dimensionless.",
      "boundary_behavior": "lsd_p, lsd_f, and Vol have strictly positive training ranges, so log(1 + positive) is always finite; no zero-division occurs. Descriptor approaches 0 as sizes shrink to the lower training bounds, which is a limiting artifact of the proxy, not a physical singularity.",
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
    "name": "bottleneck_cavity_capacity",
    "formula": "log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)",
    "hypothesis": "At infinite dilution, entropy loss on adsorption decreases when the included free-sphere diameter along the diffusion path (lsd_p) is large relative to the bottleneck (lsd_f): a large included region behind a comparable bottleneck gives the molecule more positional freedom in the sorbate pocket, so the descriptor increases with retained entropy and entropy loss decreases with it. Molecular volume acts as a size penalty: bulkier adsorbates lose translational/configurational freedom faster in the same framework.",
    "rationale": "Uses lsd_p (included along path) and lsd_f (bottleneck) as complementary geometric contrasts, explicitly not conflating either with a global cavity diameter Di. Vol is a van der Waals volume proxy for molecular size, not a free-volume equality. The product form is an empirical proxy combination; log keeps the descriptor finite and dimensionless. Limitations: fixed-probe geometric descriptors may miss framework flexibility and chemical specificity (pure-silica, no energetic heterogeneity).",
    "falsification_criteria": "If entropy loss increases with lsd_p for fixed lsd_f and Vol in held-out frameworks, the 'larger included region retains entropy' mechanism is falsified in favor of a strong-confinement/entropy-trap mechanism. Partial derivative of the descriptor w.r.t. lsd_f must be positive (regime_input lsd_f, native bounds [0.85684, 7.68726]); if the target association with this derivative is opposite, the hypothesis fails.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
      "proxy_assumptions": "lsd_p and lsd_f are rigid-framework geometric extremes on a fixed probe; they proxy accessible configurational extent but not energetics. Vol proxies molecular size; heavy-atom-based Vol may undercount small adsorbates.",
      "physical_interpretation": "All ratios are q-normalized against fixed training medians; no q-unity value is treated as a physical equality threshold. Log argument is dimensionless.",
      "boundary_behavior": "lsd_p, lsd_f, and Vol have strictly positive training ranges, so log(1 + positive) is always finite; no zero-division occurs. Descriptor approaches 0 as sizes shrink to the lower training bounds, which is a limiting artifact of the proxy, not a physical singularity.",
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

候选标识：`low/small_kg_rag_agent/replicate-1/round-2/h2`

最终状态：scored；边际收益：-0.355884 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotational_anisotropy_freedom",
    "formula": "rotor_case(0.0, log(1 + (PMI2/maximum(PMI1, 1.0)))**0.5, log(1 + (PMI2/maximum(PMI1, 1.0)))**0.5 + log(1 + (PMI3/maximum(PMI2, 1.0)))**0.5)",
    "hypothesis": "Adsorption entropy loss increases with rotational anisotropy of the adsorbate: molecules with strongly unequal principal moments (large PMI2/PMI1 and PMI3/PMI2 ratios) have fewer orientationally equivalent adsorbed configurations in rigid pure-silica channels, losing more rotational entropy than near-spherical rotors. Single-site molecules (e.g., methane proxies) carry no orientational entropy and contribute zero anisotropy. The descriptor increases with anisotropy, so entropy loss increases with it.",
    "rationale": "PMI1/PMI2/PMI3 are original heavy-atom implicit-H representation proxies; a legitimate PMI1 of 0 (e.g., linear or single-site geometry in that representation) does not mean true all-atom inertia is zero, hence the maximum(PMI, 1.0) guard in amu*angstrom^2 units is an empirical numerical stabilizer with fixed constant, not a physical law. Rotor-case branches are declared explicitly. Limitation: heavy-atom PMIs misrepresent hydrogen rotation and small-molecule tumbling; the single_site/linear branch assignment comes from the dataset's proxy counts (54/214/2093), not from true moments of inertia.",
    "falsification_criteria": "If, at fixed framework descriptors, near-isotropic nonlinear adsorbates (PMI ratios near 1) show entropy loss equal to or greater than anisotropic ones, the orientational-restriction hypothesis is falsified. Predeclared proxy derivative: descriptor increases with PMI3 at fixed PMI2 (rotor_class fixed during partial differentiation); if the target association with that derivative is negative (entropy loss decreasing), reject.",
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
      "proxy_assumptions": "Heavy-atom implicit-H PMIs stand in for true molecular inertia; rotor_case classes are proxy labels with 1e-10 normalized tolerance. Anisotropy ratios proxy the degeneracy loss of orientational states, which is only approximate for flexible adsorbates.",
      "physical_interpretation": "Ratios of PMIs are dimensionless; the fixed constants 1.0 (amu*angstrom^2) inside maximum() are numerical guards for legitimate zeros in the heavy-atom representation, not physical equality thresholds.",
      "boundary_behavior": "Single-site branch returns 0 (no orientational freedom to lose). Linear branch uses only PMI2/PMI1 since PMI3/PMI2 is redundant for linear geometry. Nonlinear branch is finite for all training rows because maximum(PMI1,1.0) and maximum(PMI2,1.0) prevent division by legitimate zero; legitimate-zero PMI1 rows map to the large but finite ratio bounded by PMI2/1.0 within training maxima.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
    "slot_id": "h2",
    "name": "rotational_anisotropy_freedom",
    "formula": "rotor_case(0.0, (q_PMI2/maximum(q_PMI1, 0.001))**0.5, (q_PMI2/maximum(q_PMI1, 0.001))**0.5 + (q_PMI3/maximum(q_PMI2, 0.001))**0.5)",
    "hypothesis": "Adsorption entropy loss increases with rotational anisotropy of the adsorbate: molecules with strongly unequal principal moments (large PMI2/PMI1 and PMI3/PMI2 ratios) have fewer orientationally equivalent adsorbed configurations in rigid pure-silica channels, losing more rotational entropy than near-spherical rotors. Single-site molecules (e.g., methane proxies) carry no orientational entropy and contribute zero anisotropy. The descriptor increases with anisotropy, so entropy loss increases with it.",
    "rationale": "Adsorption entropy loss is hypothesized to increase with heavy-atom rotational anisotropy: unequal principal moments (PMI2/PMI1, PMI3/PMI2) proxy fewer orientationally equivalent adsorbed configurations in rigid channels, consistent with reported greater rotational entropy loss in more confined frameworks (E01, E02, E03). This revision replaces the earlier mixed-unit form with a purely dimensionless q-normalized expression, fixing the prior dimensional rejection. Limitations: heavy-atom PMIs misrepresent hydrogen rotation; RRHO-style treatments of guest rotations are known to overestimate entropy loss (E05), so this is an empirical geometric proxy, not a partition-function calculation.",
    "falsification_criteria": "If, at fixed framework descriptors, near-isotropic nonlinear adsorbates show entropy loss equal to or greater than anisotropic ones, the orientational-restriction hypothesis is falsified. Predeclared proxy derivative: descriptor increases with PMI3 at fixed PMI2 (rotor_class fixed during partial differentiation); if target association with that derivative is negative (entropy loss decreasing), reject.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E05"
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
      "proxy_assumptions": "Heavy-atom implicit-H PMIs proxy true molecular inertia; rotor_case classes (54/214/2093 in training) are proxy labels with 1e-10 tolerance. q-normalization against fixed training medians does not turn ratio unity into a physical threshold; anisotropy ratios only approximate orientational degeneracy loss for flexible adsorbates (E05, E06).",
      "physical_interpretation": "PMI1/PMI2/PMI3 are heavy-atom principal moments of the original representation; a legitimate PMI of 0 does not mean true all-atom inertia is zero. q_PMI are row-varying normalized inputs against fixed training references.",
      "boundary_behavior": "Single-site branch returns constant 0.0. All nonlinear-branch terms are dimensionless q-ratios; the fixed guard 0.001 is a dimensionless numerical stabilizer for legitimate zero PMI rows in the heavy-atom representation (not a physical equality threshold), bounding the ratio by q_PMI2/0.001 which is finite over training maxima; all three branch outputs are dimensionless and compatible.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
        2299.281763
      ],
      "training_spearman": -0.019728206777949026,
      "target_association": "inconclusive",
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
    "name": "rotational_anisotropy_freedom",
    "formula": "rotor_case(0.0, (q_PMI2/maximum(q_PMI1, 0.001))**0.5, (q_PMI2/maximum(q_PMI1, 0.001))**0.5 + (q_PMI3/maximum(q_PMI2, 0.001))**0.5)",
    "hypothesis": "Adsorption entropy loss increases with rotational anisotropy of the adsorbate: molecules with strongly unequal principal moments (large PMI2/PMI1 and PMI3/PMI2 ratios) have fewer orientationally equivalent adsorbed configurations in rigid pure-silica channels, losing more rotational entropy than near-spherical rotors. Single-site molecules (e.g., methane proxies) carry no orientational entropy and contribute zero anisotropy. The descriptor increases with anisotropy, so entropy loss increases with it.",
    "rationale": "Adsorption entropy loss is hypothesized to increase with heavy-atom rotational anisotropy: unequal principal moments (PMI2/PMI1, PMI3/PMI2) proxy fewer orientationally equivalent adsorbed configurations in rigid channels, consistent with reported greater rotational entropy loss in more confined frameworks (E01, E02, E03). This revision replaces the earlier mixed-unit form with a purely dimensionless q-normalized expression, fixing the prior dimensional rejection. Limitations: heavy-atom PMIs misrepresent hydrogen rotation; RRHO-style treatments of guest rotations are known to overestimate entropy loss (E05), so this is an empirical geometric proxy, not a partition-function calculation.",
    "falsification_criteria": "If, at fixed framework descriptors, near-isotropic nonlinear adsorbates show entropy loss equal to or greater than anisotropic ones, the orientational-restriction hypothesis is falsified. Predeclared proxy derivative: descriptor increases with PMI3 at fixed PMI2 (rotor_class fixed during partial differentiation); if target association with that derivative is negative (entropy loss decreasing), reject.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E05"
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
      "proxy_assumptions": "Heavy-atom implicit-H PMIs proxy true molecular inertia; rotor_case classes (54/214/2093 in training) are proxy labels with 1e-10 tolerance. q-normalization against fixed training medians does not turn ratio unity into a physical threshold; anisotropy ratios only approximate orientational degeneracy loss for flexible adsorbates (E05, E06).",
      "physical_interpretation": "PMI1/PMI2/PMI3 are heavy-atom principal moments of the original representation; a legitimate PMI of 0 does not mean true all-atom inertia is zero. q_PMI are row-varying normalized inputs against fixed training references.",
      "boundary_behavior": "Single-site branch returns constant 0.0. All nonlinear-branch terms are dimensionless q-ratios; the fixed guard 0.001 is a dimensionless numerical stabilizer for legitimate zero PMI rows in the heavy-atom representation (not a physical equality threshold), bounding the ratio by q_PMI2/0.001 which is finite over training maxima; all three branch outputs are dimensionless and compatible.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
        2299.281763
      ],
      "training_spearman": -0.019728206777949026,
      "target_association": "inconclusive",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/small_kg_rag_agent/replicate-1/round-2/h3`

最终状态：scored；边际收益：-0.912274 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.MW

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "specific_area_per_mass_contrast",
    "formula": "(ASA/ASA_ref) / (MW/MW_ref)",
    "hypothesis": "Entropy loss on adsorption decreases with the probe-accessible specific surface area per unit adsorbate molecular weight: frameworks exposing more accessible surface per mass offer more distinct near-surface configurations to a given adsorbate, so heavier or more compact adsorbates in high-ASA frameworks retain more configurational entropy. The descriptor increases with retained entropy; entropy loss decreases with it.",
    "rationale": "ASA is a fixed-probe, mass-specific geometric quantity, not molecule-specific; using MW as a mass-scale contrast is an empirical normalization choice, not a statement that ASA scales linearly with anything physical. Mechanism is configurational degeneracy: more accessible area provides more inequivalent adsorption geometries. Limitations: fixed-probe ASA understates accessibility for molecules smaller than the probe and overstates it for larger ones; zero ASA rows (28 in training) represent zero fixed-probe accessibility, not zero physical adsorption space, and the descriptor remains finite (zero) there rather than being imputed.",
    "falsification_criteria": "If entropy loss instead increases with ASA/MW within a fixed framework family (e.g., high-ASA frameworks restrict adsorbates to surface-wetting geometries with fewer configurations than dense frameworks with large cages), the degeneracy hypothesis is falsified. Predeclared derivative: descriptor increases with ASA at fixed MW; the target association with that derivative must be negative (entropy loss decreasing) or the hypothesis is rejected.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "MW": "molecular_weight_of_adsorbate"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "Fixed-probe ASA proxies the number of distinct adsorption sites; MW proxies adsorbate mass/size scale. The ratio is an empirical contrast, not a physical surface-area-per-molecule law, because ASA is framework-mass-specific and MW is adsorbate-specific.",
      "physical_interpretation": "q_ASA and q_MW are row-varying normalized inputs against fixed training medians; their ratio is dimensionless. No q value of 1 is interpreted as a physical threshold.",
      "boundary_behavior": "MW is strictly positive in training (min 16.03), so no zero division. Legitimate zero ASA rows yield descriptor exactly 0, retained without imputation, interpreted as zero fixed-probe accessible area and flagged as a known proxy blind spot for physically adsorbing molecules smaller than the probe.",
      "vary_input": "ASA",
      "descriptor_direction": "increasing",
      "regime_input": "MW",
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
    "reason": "Wrong physical variable mapping: MW requires adsorbate_geometry_proxy"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "specific_area_per_mass_contrast",
    "formula": "(ASA/ASA_ref) / (MW/MW_ref)",
    "hypothesis": "Entropy loss on adsorption decreases with the probe-accessible specific surface area per unit adsorbate molecular weight: frameworks exposing more accessible surface per mass offer more distinct near-surface configurations to a given adsorbate, so heavier or more compact adsorbates in high-ASA frameworks retain more configurational entropy. The descriptor increases with retained entropy; entropy loss decreases with it.",
    "rationale": "Entropy loss on adsorption is hypothesized to decrease with probe-accessible specific surface area relative to adsorbate size: frameworks exposing more accessible surface per unit of adsorbate geometric scale offer more distinct near-surface configurations, consistent with reported entropy-loss decreases in larger-pore frameworks (E02, E04, E07). This revision corrects the variable mapping only: MW is an adsorbate geometry proxy, not a molecular-weight thermodynamic quantity. Limitations: fixed-probe ASA understates accessibility for adsorbates smaller than the probe; zero-ASA rows are a known proxy blind spot, not zero physical adsorption space.",
    "falsification_criteria": "If entropy loss instead increases with (ASA/ASA_ref)/(MW/MW_ref) within a fixed framework family (e.g., high-ASA frameworks restrict adsorbates to surface-wetting geometries with fewer configurations), the degeneracy hypothesis is falsified. Predeclared derivative: descriptor increases with ASA at fixed MW; the target association with that derivative must be negative (entropy loss decreasing) or the hypothesis is rejected.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "Fixed-probe ASA proxies the number of distinct adsorption sites; MW is used here as an adsorbate geometry/size proxy (per the required role mapping), not as a thermodynamic mass variable. The ratio is an empirical contrast; ASA is framework-mass-specific and MW is adsorbate-specific, so this is not a physical surface-area-per-molecule law.",
      "physical_interpretation": "q_ASA and q_MW are row-varying normalized inputs against fixed training medians (ASA_ref, MW_ref); their ratio is dimensionless. No q value of 1 is interpreted as a physical threshold; X/q_X would be constant X_ref and is not used.",
      "boundary_behavior": "MW is strictly positive in training (min 16.03), so no zero division. Legitimate zero ASA rows (28 in training) yield descriptor exactly 0, retained without imputation; the descriptor is finite for all training rows.",
      "vary_input": "ASA",
      "descriptor_direction": "increasing",
      "regime_input": "MW",
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
        "ASA",
        "MW"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "MW": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        16.03130013,
        184.1463299
      ],
      "training_spearman": -0.4832997803846041,
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
    "slot_id": "h3",
    "name": "specific_area_per_mass_contrast",
    "formula": "(ASA/ASA_ref) / (MW/MW_ref)",
    "hypothesis": "Entropy loss on adsorption decreases with the probe-accessible specific surface area per unit adsorbate molecular weight: frameworks exposing more accessible surface per mass offer more distinct near-surface configurations to a given adsorbate, so heavier or more compact adsorbates in high-ASA frameworks retain more configurational entropy. The descriptor increases with retained entropy; entropy loss decreases with it.",
    "rationale": "Entropy loss on adsorption is hypothesized to decrease with probe-accessible specific surface area relative to adsorbate size: frameworks exposing more accessible surface per unit of adsorbate geometric scale offer more distinct near-surface configurations, consistent with reported entropy-loss decreases in larger-pore frameworks (E02, E04, E07). This revision corrects the variable mapping only: MW is an adsorbate geometry proxy, not a molecular-weight thermodynamic quantity. Limitations: fixed-probe ASA understates accessibility for adsorbates smaller than the probe; zero-ASA rows are a known proxy blind spot, not zero physical adsorption space.",
    "falsification_criteria": "If entropy loss instead increases with (ASA/ASA_ref)/(MW/MW_ref) within a fixed framework family (e.g., high-ASA frameworks restrict adsorbates to surface-wetting geometries with fewer configurations), the degeneracy hypothesis is falsified. Predeclared derivative: descriptor increases with ASA at fixed MW; the target association with that derivative must be negative (entropy loss decreasing) or the hypothesis is rejected.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "MW": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "Fixed-probe ASA proxies the number of distinct adsorption sites; MW is used here as an adsorbate geometry/size proxy (per the required role mapping), not as a thermodynamic mass variable. The ratio is an empirical contrast; ASA is framework-mass-specific and MW is adsorbate-specific, so this is not a physical surface-area-per-molecule law.",
      "physical_interpretation": "q_ASA and q_MW are row-varying normalized inputs against fixed training medians (ASA_ref, MW_ref); their ratio is dimensionless. No q value of 1 is interpreted as a physical threshold; X/q_X would be constant X_ref and is not used.",
      "boundary_behavior": "MW is strictly positive in training (min 16.03), so no zero division. Legitimate zero ASA rows (28 in training) yield descriptor exactly 0, retained without imputation; the descriptor is finite for all training rows.",
      "vary_input": "ASA",
      "descriptor_direction": "increasing",
      "regime_input": "MW",
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
        "ASA",
        "MW"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "MW": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        16.03130013,
        184.1463299
      ],
      "training_spearman": -0.4832997803846041,
      "target_association": "consistent",
      "perturbation": 8.465169999999999,
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
        "record_id": "chunk:31581596e6cea285171393ae",
        "paper_id": "doi:10.1063/1.4706520",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:72dfcce988c17185f87c465c",
        "paper_id": "doi:10.1021/jp1096663",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:773590832eac6c7df0ec1cd5",
        "paper_id": "doi:10.1021/jp9014405",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:17cc4a1a602b364ef44e2b12",
        "paper_id": "doi:10.1063/1.4706520",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3a78ee27873e65622adfaf3b",
        "paper_id": "doi:10.1002/chem.201602653",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd1acc7b04d64296bb68e884",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08aecb87be6d1cda8c6566fa",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:24b461a96e47499c10b44d0f",
        "paper_id": "doi:10.1021/acs.jctc.7b00716",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7765ca1d2f5ad252ac5811bd",
        "paper_id": "doi:10.1063/1.2790903",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd4794ce62afc7c5c5d7b896",
        "paper_id": "doi:10.1021/acs.jpclett.2c03302",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d3a799358d58da57167e96f1",
        "paper_id": "doi:10.1021/acs.langmuir.3c03931",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e78f3f59380c81fc6502c69e",
        "paper_id": "pmc:pmc11868592",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e933adf17670b8f416a9170e",
        "paper_id": "doi:10.1021/la302230z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:06a26a29dca2516a90c93ace",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:0afdfcf5d5acc40ea8c052d9",
        "paper_id": "doi:10.1021/jp9014405",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1d31f4f7e46b887f464a699d",
        "paper_id": "doi:10.1021/jacs.0c09825",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:323d66ad417d981217705b45",
        "paper_id": "doi:10.1021/ja015797o",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution, entropy loss on adsorption decreases when the included free-sphere diameter along the diffusion path (lsd_p) is large relative to the bottleneck (lsd_f): a large included region behind a comparable bottleneck gives the molecule more positional freedom in the sorbate pocket, so the descriptor increases with retained entropy and entropy loss decreases with it. Molecular volume acts as a size penalty: bulkier adsorbates lose translational/configurational freedom faster in the same framework. log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5) Adsorption entropy loss increases with rotational anisotropy of the adsorbate: molecules with strongly unequal principal moments (large PMI2/PMI1 and PMI3/PMI2 ratios) have fewer orientationally equivalent adsorbed configurations in rigid pure-silica channels, losing more rotational entropy than near-spherical rotors. Single-site molecules (e.g., methane proxies) carry no orientational entropy and contribute zero anisotropy. The descriptor increases with anisotropy, so entropy loss increases with it. rotor_case(0.0, log(1 + (PMI2/maximum(PMI1, 1.0)))**0.5, log(1 + (PMI2/maximum(PMI1, 1.0)))**0.5 + log(1 + (PMI3/maximum(PMI2, 1.0)))**0.5) Entropy loss on adsorption decreases with the probe-accessible specific surface area per unit adsorbate molecular weight: frameworks exposing more accessible surface per mass offer more distinct near-surface configurations to a given adsorbate, so heavier or more compact adsorbates in high-ASA frameworks retain more configurational entropy. The descriptor increases with retained entropy; entropy loss decreases with it. (ASA/ASA_ref) / (MW/MW_ref)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:8ffcc4698d37d4f5569d53f5",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:01d0cb8bf43d75bbc448e004",
      "chunk:ae6e434cc894357276cba23f"
    ],
    "items": 10,
    "lexical_tokens": 4659,
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
