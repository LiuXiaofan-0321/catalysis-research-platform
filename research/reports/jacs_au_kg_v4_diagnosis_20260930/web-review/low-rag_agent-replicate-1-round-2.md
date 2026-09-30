# low/rag_agent/replicate-1/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/rag_agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
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
  }
]
```

## h1

候选标识：`low/rag_agent/replicate-1/round-2/h1`

最终状态：scored；边际收益：-2.022208 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "confined_translation_size_ratio",
    "formula": "log(q_Vol) - log(q_lsd_f)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, translational entropy loss scales with the ratio of adsorbate van der Waals volume to the framework's passing-bottleneck free-sphere diameter (as a confinement proxy): adsorbates large relative to the bottleneck free path lose more translational entropy, so the dimensionless volume-to-bottleneck contrast monotonically predicts the entropy-loss ratio s_ads/s_gas direction.",
    "rationale": "Vol is a whole-molecule vdw volume; lsd_f (Zeo++ Df) is the largest sphere that can pass through the periodic free path, used here only as a fixed-geometry confinement proxy, not as a cavity diameter. q_Vol and q_lsd_f are each positive row-varying dimensionless ratios to fixed positive training-reference medians, so their log difference is finite for every training row (both domains have zero_n = 0). This is a translational-confinement family descriptor, complementary to the retained accessibility-contrast slot h3.",
    "falsification_criteria": "If within fixed framework (fixed lsd_f) the entropy-loss ratio does not increase with Vol across the training range (Spearman near zero or negative within the regime), or if lsd_f variation at fixed adsorbate shows no consistent association, the confinement-ratio mechanism is falsified for this descriptor; a competing shape-rotational mechanism would then dominate.",
    "novelty_status": "new_combination",
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
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol proxies the confined molecular size; lsd_f proxies the narrowest free passage; both are fixed-geometry descriptors that ignore framework flexibility, thermal breathing, and adsorbate-specific interaction energetics.",
      "physical_interpretation": "Larger molecule volume relative to a framework with a smaller passing bottleneck means tighter confinement and larger translational entropy loss; the descriptor is a dimensionless contrast, and no q-unity value is a physical equality threshold.",
      "boundary_behavior": "Both Vol and lsd_f have strictly positive training domains (min 20.424 A^3 and 0.85684 A), so the formula is finite on every training row; no zero-division or epsilon is needed. Extremes remain finite: max log ratio is bounded by log(161.144/67.24) + log(5.16326/0.85684).",
      "vary_input": "Vol",
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
      "training_spearman": 0.6317416420940126,
      "target_association": "contradicted",
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
    "name": "confined_translation_size_ratio",
    "formula": "log(q_lsd_f) - log(q_Vol)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, translational entropy loss scales with the ratio of adsorbate van der Waals volume to the framework's passing-bottleneck free-sphere diameter (as a confinement proxy): adsorbates large relative to the bottleneck free path lose more translational entropy, so the dimensionless volume-to-bottleneck contrast monotonically predicts the entropy-loss ratio s_ads/s_gas direction.",
    "rationale": "Empirical sign-corrected translational-confinement contrast: frameworks with wider passing bottlenecks and smaller adsorbates should lose less translational entropy. The reversal is motivated by the training-only direction diagnostic; it remains an empirical proxy relation, not a validated physical law (cf. E02/E04: larger-pore frameworks show smaller reported entropy losses, but cavity diameter is not Df).",
    "falsification_criteria": "If the reversed contrast still fails the direction diagnostic within fixed-adsorbate or fixed-framework regimes, or if lsd_f shows no stable association once Vol is held fixed, the bottleneck-confined-translation mechanism is falsified for this descriptor and a rotational/cavity mechanism (E01, E02) would dominate.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f (Zeo++ Df) proxies the narrowest passing free path, not the global cavity diameter Di; Vol proxies whole-molecule confinement size. Both ignore framework flexibility, thermal breathing and adsorbate-specific energetics. The training-only precheck showed the original contrast log(q_Vol)-log(q_lsd_f) associated positively with entropy loss (Spearman ~ 0.63), contradicting the predeclared direction, so the sign of the contrast is reversed; this is an empirical sign correction, not a new mechanism.",
      "physical_interpretation": "Larger passing-bottleneck free spheres (larger lsd_f) and smaller adsorbate volume correspond to weaker translational confinement and less translational entropy loss at infinite dilution. lsd_f_ref = 5.16326 A and Vol_ref = 67.24 A^3 are fixed training medians; no q-unity value is a physical threshold.",
      "boundary_behavior": "Vol (min 20.424 A^3) and lsd_f (min 0.85684 A) have strictly positive training domains, so both logs are finite on every training row; no epsilon or division by zero occurs. The descriptor is bounded by log(7.68726/0.85684) - log(161.144/20.424) at the extremes.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        20.424,
        161.144
      ],
      "training_spearman": -0.6317416420940126,
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
    "name": "confined_translation_size_ratio",
    "formula": "log(q_lsd_f) - log(q_Vol)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, translational entropy loss scales with the ratio of adsorbate van der Waals volume to the framework's passing-bottleneck free-sphere diameter (as a confinement proxy): adsorbates large relative to the bottleneck free path lose more translational entropy, so the dimensionless volume-to-bottleneck contrast monotonically predicts the entropy-loss ratio s_ads/s_gas direction.",
    "rationale": "Empirical sign-corrected translational-confinement contrast: frameworks with wider passing bottlenecks and smaller adsorbates should lose less translational entropy. The reversal is motivated by the training-only direction diagnostic; it remains an empirical proxy relation, not a validated physical law (cf. E02/E04: larger-pore frameworks show smaller reported entropy losses, but cavity diameter is not Df).",
    "falsification_criteria": "If the reversed contrast still fails the direction diagnostic within fixed-adsorbate or fixed-framework regimes, or if lsd_f shows no stable association once Vol is held fixed, the bottleneck-confined-translation mechanism is falsified for this descriptor and a rotational/cavity mechanism (E01, E02) would dominate.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f (Zeo++ Df) proxies the narrowest passing free path, not the global cavity diameter Di; Vol proxies whole-molecule confinement size. Both ignore framework flexibility, thermal breathing and adsorbate-specific energetics. The training-only precheck showed the original contrast log(q_Vol)-log(q_lsd_f) associated positively with entropy loss (Spearman ~ 0.63), contradicting the predeclared direction, so the sign of the contrast is reversed; this is an empirical sign correction, not a new mechanism.",
      "physical_interpretation": "Larger passing-bottleneck free spheres (larger lsd_f) and smaller adsorbate volume correspond to weaker translational confinement and less translational entropy loss at infinite dilution. lsd_f_ref = 5.16326 A and Vol_ref = 67.24 A^3 are fixed training medians; no q-unity value is a physical threshold.",
      "boundary_behavior": "Vol (min 20.424 A^3) and lsd_f (min 0.85684 A) have strictly positive training domains, so both logs are finite on every training row; no epsilon or division by zero occurs. The descriptor is bounded by log(7.68726/0.85684) - log(161.144/20.424) at the extremes.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        20.424,
        161.144
      ],
      "training_spearman": -0.6317416420940126,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/rag_agent/replicate-1/round-2/h2`

最终状态：scored；边际收益：-3.740370 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_case_planarity_entropy",
    "formula": "rotor_case( q_SPAN, q_SPAN, q_SPAN * q_PBF )",
    "hypothesis": "Rotational and orientational entropy loss at infinite dilution depends on how anisotropically extended and non-planar the adsorbate is: for nonlinear molecules, the product of heavy-atom enclosing radius (SPAN) with best-fit-plane excursion (PBF) proxies the number of restricted orientational degrees of freedom, so more extended, less planar molecules lose more rotational entropy in cage confinement; single-site (e.g., methane) and linear molecules have reduced or different orientational restriction, handled by explicit rotor branches.",
    "rationale": "SPAN and PBF are heavy-atom implicit-H representation proxies with legitimate zeros (SPAN zero only for the 54 single-site rows; PBF zero for 587 planar rows). The nonlinear branch multiplies q_SPAN by q_PBF, which is zero exactly when the molecule is planar (PBF = 0), a physically meaningful boundary: a perfectly planar heavy-atom skeleton has a distinct orientational restriction pattern. Single-site and linear branches use q_SPAN alone to keep units compatible and avoid dividing by legitimate zeros. rotor_case with tolerance 1e-10 selects exactly one branch; every row yields a finite value.",
    "falsification_criteria": "If, within the nonlinear rotor regime at fixed rotor class, the partial derivative of the descriptor with respect to PBF (or SPAN) shows an association with entropy loss opposite to the predeclared decreasing-entropy direction (as occurred for the round-1 PMI descriptor), or if planar (PBF = 0) and non-planar molecules show no systematic entropy-loss difference at matched size, the planarity-orientational-restriction hypothesis is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "SPAN proxies molecular extension and PBF proxies deviation from planarity in the original implicit-H representation; neither equals the true all-atom inertia tensor, and zero PBF is a real planar geometry, not missing data. Rotor class is fixed during any partial-derivative test.",
      "physical_interpretation": "Native SPAN and PBF measure size and non-planarity; their normalized product is a dimensionless orientational-restriction proxy. The q-reference constants (SPAN_ref = 1.860601424 A, PBF_ref = 0.230844767 A) are training medians, not physical thresholds.",
      "boundary_behavior": "At PBF = 0 (planar heavy-atom skeletons, 587 training rows) the nonlinear branch descriptor is exactly 0, a finite and physically interpretable limit (no out-of-plane excursion), not an imputation; single-site rows with SPAN = 0 give 0 in the first branch, again finite and meaningful (no extended orientational restriction).",
      "vary_input": "PBF",
      "descriptor_direction": "increasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.75,
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
      "regime_n": 609,
      "native_regime_bounds": [
        285.0961576,
        2414.631462
      ],
      "training_spearman": 0.1905261119321948,
      "target_association": "contradicted",
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
    "name": "rotor_case_planarity_entropy",
    "formula": "rotor_case( q_SPAN, q_SPAN, q_SPAN * (1 - q_PBF) )",
    "hypothesis": "Rotational and orientational entropy loss at infinite dilution depends on how anisotropically extended and non-planar the adsorbate is: for nonlinear molecules, the product of heavy-atom enclosing radius (SPAN) with best-fit-plane excursion (PBF) proxies the number of restricted orientational degrees of freedom, so more extended, less planar molecules lose more rotational entropy in cage confinement; single-site (e.g., methane) and linear molecules have reduced or different orientational restriction, handled by explicit rotor branches.",
    "rationale": "Sign-corrected orientational-restriction proxy with explicit rotor branches. The prior PMI-based and planarity-product forms were contradicted by the training direction diagnostic; the reversed contrast (planar-extended molecules lose less rotational entropy in this dataset) is an empirical correction consistent in spirit with confinement-driven rotational restriction (E01, E02), but the mechanism is not validated and the sign is dataset-specific.",
    "falsification_criteria": "If the corrected descriptor's partial derivative with respect to PBF (or SPAN) at fixed rotor class again shows an association opposite to the predeclared direction, or if planar (PBF = 0) and non-planar molecules show no systematic entropy-loss difference at matched size, the planarity-orientational-restriction mechanism is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E02"
    ],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "SPAN proxies heavy-atom extension; PBF proxies deviation from planarity in the original implicit-H representation; neither equals the true all-atom inertia tensor, and zero PBF is a real planar geometry, not missing data. Rotor class is fixed during any partial-derivative test.",
      "physical_interpretation": "The nonlinear branch contrasts extension (SPAN) against non-planarity (PBF): more extended, more planar molecules are empirically associated with smaller orientational entropy loss, opposite to the round-1 planarity-product direction that the training precheck contradicted (Spearman ~ +0.19). SPAN_ref = 1.860601424 A and PBF_ref = 0.230844767 A are training medians, not physical thresholds.",
      "boundary_behavior": "Single-site rows (SPAN = 0, 54 rows) give exactly 0 in the first branch; planar heavy-atom skeletons (PBF = 0, 587 rows) give q_SPAN in the nonlinear branch, finite and interpretable as no out-of-plane correction. q_PBF can exceed 1 for non-planar molecules (PBF max 0.656 > PBF_ref 0.2308), making the descriptor negative but finite; this is an empirical contrast, not a probability, and no branch divides by a legitimate zero.",
      "vary_input": "PBF",
      "descriptor_direction": "decreasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.75,
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
      "regime_n": 609,
      "native_regime_bounds": [
        285.0961576,
        2414.631462
      ],
      "training_spearman": -0.11532361411815488,
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
    "name": "rotor_case_planarity_entropy",
    "formula": "rotor_case( q_SPAN, q_SPAN, q_SPAN * (1 - q_PBF) )",
    "hypothesis": "Rotational and orientational entropy loss at infinite dilution depends on how anisotropically extended and non-planar the adsorbate is: for nonlinear molecules, the product of heavy-atom enclosing radius (SPAN) with best-fit-plane excursion (PBF) proxies the number of restricted orientational degrees of freedom, so more extended, less planar molecules lose more rotational entropy in cage confinement; single-site (e.g., methane) and linear molecules have reduced or different orientational restriction, handled by explicit rotor branches.",
    "rationale": "Sign-corrected orientational-restriction proxy with explicit rotor branches. The prior PMI-based and planarity-product forms were contradicted by the training direction diagnostic; the reversed contrast (planar-extended molecules lose less rotational entropy in this dataset) is an empirical correction consistent in spirit with confinement-driven rotational restriction (E01, E02), but the mechanism is not validated and the sign is dataset-specific.",
    "falsification_criteria": "If the corrected descriptor's partial derivative with respect to PBF (or SPAN) at fixed rotor class again shows an association opposite to the predeclared direction, or if planar (PBF = 0) and non-planar molecules show no systematic entropy-loss difference at matched size, the planarity-orientational-restriction mechanism is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E02"
    ],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "SPAN proxies heavy-atom extension; PBF proxies deviation from planarity in the original implicit-H representation; neither equals the true all-atom inertia tensor, and zero PBF is a real planar geometry, not missing data. Rotor class is fixed during any partial-derivative test.",
      "physical_interpretation": "The nonlinear branch contrasts extension (SPAN) against non-planarity (PBF): more extended, more planar molecules are empirically associated with smaller orientational entropy loss, opposite to the round-1 planarity-product direction that the training precheck contradicted (Spearman ~ +0.19). SPAN_ref = 1.860601424 A and PBF_ref = 0.230844767 A are training medians, not physical thresholds.",
      "boundary_behavior": "Single-site rows (SPAN = 0, 54 rows) give exactly 0 in the first branch; planar heavy-atom skeletons (PBF = 0, 587 rows) give q_SPAN in the nonlinear branch, finite and interpretable as no out-of-plane correction. q_PBF can exceed 1 for non-planar molecules (PBF max 0.656 > PBF_ref 0.2308), making the descriptor negative but finite; this is an empirical contrast, not a probability, and no branch divides by a legitimate zero.",
      "vary_input": "PBF",
      "descriptor_direction": "decreasing",
      "regime_input": "PMI3",
      "regime_train_quantiles": [
        0.75,
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
      "regime_n": 609,
      "native_regime_bounds": [
        285.0961576,
        2414.631462
      ],
      "training_spearman": -0.11532361411815488,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/rag_agent/replicate-1/round-2/h3`

最终状态：scored；边际收益：-2.439369 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_included_path_contrast",
    "formula": "q_AV * q_lsd_p",
    "hypothesis": "At infinite dilution, configurational entropy loss depends jointly on how much probe-accessible volume the framework offers per mass (AV) and how large an included sphere the free path accommodates (lsd_p, Dif): frameworks that are both volume-rich and wide along the free path impose less positional and orientational restriction, so the product of normalized accessibility and included-path diameter predicts lower entropy loss (higher s_ads/s_gas); this extends the retained AV-based contrast with a distinct connectivity/geometric-path mechanism.",
    "rationale": "AV is the fixed-probe mass-specific accessible volume (not molecule-specific free volume); lsd_p is the largest included sphere along the free-sphere path, distinct from the bottleneck lsd_f. Both quantities are positive except for the 28 rows with AV = 0 (inaccessible to the fixed geometric probe); the product is exactly 0 there, a finite boundary meaning the fixed-probe pathway proxy offers no measurable accessible volume, not an imputation. This is a connectivity/coupling family descriptor and is distinct from the retained h3 form q_AV/q_Vol because it uses framework-only quantities and the included-path (not bottleneck) diameter.",
    "falsification_criteria": "If the descriptor's association with entropy loss at fixed AV (varying lsd_p) is opposite to the predeclared increasing-descriptor / decreasing-entropy direction, or if AV = 0 rows show entropy losses indistinguishable from high-AV rows at matched adsorbate size, the joint accessibility-included-path mechanism is falsified; a pure adsorbate-geometry mechanism would then be favored.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV from a fixed probe does not equal free volume for a specific adsorbate, and zero AV does not imply zero physical adsorption; lsd_p is the included diameter along the free path, not the bottleneck Df and not the global cavity Di. Both are rigid-framework, fixed-geometry proxies ignoring flexibility and energetics.",
      "physical_interpretation": "Larger probe-accessible volume per mass and wider included spheres along diffusion paths mean more spatial configurations available to an adsorbate at infinite dilution, hence less entropy loss; q_AV and q_lsd_p are row-varying dimensionless ratios to fixed positive training medians (AV_ref = 0.0759781 cm^3/g, lsd_p_ref = 6.38663 A) carrying no universal physical meaning.",
      "boundary_behavior": "For the 28 AV = 0 training rows the descriptor is exactly 0, finite and honest (fixed probe finds no accessible volume); lsd_p is strictly positive (min 3.3452 A), so no division or epsilon is involved anywhere in the formula.",
      "vary_input": "AV",
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
        "AV",
        "lsd_p"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
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
      "training_spearman": -0.4846124738077094,
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
    "slot_id": "h3",
    "name": "accessible_volume_included_path_contrast",
    "formula": "q_AV * q_lsd_p",
    "hypothesis": "At infinite dilution, configurational entropy loss depends jointly on how much probe-accessible volume the framework offers per mass (AV) and how large an included sphere the free path accommodates (lsd_p, Dif): frameworks that are both volume-rich and wide along the free path impose less positional and orientational restriction, so the product of normalized accessibility and included-path diameter predicts lower entropy loss (higher s_ads/s_gas); this extends the retained AV-based contrast with a distinct connectivity/geometric-path mechanism.",
    "rationale": "AV is the fixed-probe mass-specific accessible volume (not molecule-specific free volume); lsd_p is the largest included sphere along the free-sphere path, distinct from the bottleneck lsd_f. Both quantities are positive except for the 28 rows with AV = 0 (inaccessible to the fixed geometric probe); the product is exactly 0 there, a finite boundary meaning the fixed-probe pathway proxy offers no measurable accessible volume, not an imputation. This is a connectivity/coupling family descriptor and is distinct from the retained h3 form q_AV/q_Vol because it uses framework-only quantities and the included-path (not bottleneck) diameter.",
    "falsification_criteria": "If the descriptor's association with entropy loss at fixed AV (varying lsd_p) is opposite to the predeclared increasing-descriptor / decreasing-entropy direction, or if AV = 0 rows show entropy losses indistinguishable from high-AV rows at matched adsorbate size, the joint accessibility-included-path mechanism is falsified; a pure adsorbate-geometry mechanism would then be favored.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV from a fixed probe does not equal free volume for a specific adsorbate, and zero AV does not imply zero physical adsorption; lsd_p is the included diameter along the free path, not the bottleneck Df and not the global cavity Di. Both are rigid-framework, fixed-geometry proxies ignoring flexibility and energetics.",
      "physical_interpretation": "Larger probe-accessible volume per mass and wider included spheres along diffusion paths mean more spatial configurations available to an adsorbate at infinite dilution, hence less entropy loss; q_AV and q_lsd_p are row-varying dimensionless ratios to fixed positive training medians (AV_ref = 0.0759781 cm^3/g, lsd_p_ref = 6.38663 A) carrying no universal physical meaning.",
      "boundary_behavior": "For the 28 AV = 0 training rows the descriptor is exactly 0, finite and honest (fixed probe finds no accessible volume); lsd_p is strictly positive (min 3.3452 A), so no division or epsilon is involved anywhere in the formula.",
      "vary_input": "AV",
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
        "AV",
        "lsd_p"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
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
      "training_spearman": -0.4846124738077094,
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
    "slot_id": "h3",
    "name": "accessible_volume_included_path_contrast",
    "formula": "q_AV * q_lsd_p",
    "hypothesis": "At infinite dilution, configurational entropy loss depends jointly on how much probe-accessible volume the framework offers per mass (AV) and how large an included sphere the free path accommodates (lsd_p, Dif): frameworks that are both volume-rich and wide along the free path impose less positional and orientational restriction, so the product of normalized accessibility and included-path diameter predicts lower entropy loss (higher s_ads/s_gas); this extends the retained AV-based contrast with a distinct connectivity/geometric-path mechanism.",
    "rationale": "AV is the fixed-probe mass-specific accessible volume (not molecule-specific free volume); lsd_p is the largest included sphere along the free-sphere path, distinct from the bottleneck lsd_f. Both quantities are positive except for the 28 rows with AV = 0 (inaccessible to the fixed geometric probe); the product is exactly 0 there, a finite boundary meaning the fixed-probe pathway proxy offers no measurable accessible volume, not an imputation. This is a connectivity/coupling family descriptor and is distinct from the retained h3 form q_AV/q_Vol because it uses framework-only quantities and the included-path (not bottleneck) diameter.",
    "falsification_criteria": "If the descriptor's association with entropy loss at fixed AV (varying lsd_p) is opposite to the predeclared increasing-descriptor / decreasing-entropy direction, or if AV = 0 rows show entropy losses indistinguishable from high-AV rows at matched adsorbate size, the joint accessibility-included-path mechanism is falsified; a pure adsorbate-geometry mechanism would then be favored.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV from a fixed probe does not equal free volume for a specific adsorbate, and zero AV does not imply zero physical adsorption; lsd_p is the included diameter along the free path, not the bottleneck Df and not the global cavity Di. Both are rigid-framework, fixed-geometry proxies ignoring flexibility and energetics.",
      "physical_interpretation": "Larger probe-accessible volume per mass and wider included spheres along diffusion paths mean more spatial configurations available to an adsorbate at infinite dilution, hence less entropy loss; q_AV and q_lsd_p are row-varying dimensionless ratios to fixed positive training medians (AV_ref = 0.0759781 cm^3/g, lsd_p_ref = 6.38663 A) carrying no universal physical meaning.",
      "boundary_behavior": "For the 28 AV = 0 training rows the descriptor is exactly 0, finite and honest (fixed probe finds no accessible volume); lsd_p is strictly positive (min 3.3452 A), so no division or epsilon is involved anywhere in the formula.",
      "vary_input": "AV",
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
        "AV",
        "lsd_p"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
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
      "training_spearman": -0.4846124738077094,
      "target_association": "consistent",
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
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
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
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:323d66ad417d981217705b45",
        "paper_id": "doi:10.1021/ja015797o",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:560d540c09c85dfa3faa0e8c",
        "paper_id": "doi:10.1021/acs.jpcb.1c02929",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2cab4c5858c1d76e029f2dbd",
        "paper_id": "pmc:pmc10979502",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:57ee5f72df780c7e9698cbc9",
        "paper_id": "doi:10.1021/ja0481474",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:63a944566fa9e4d1bde391c6",
        "paper_id": "doi:10.1063/1.1781119",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:96428eec0013baa07b445d50",
        "paper_id": "doi:10.1039/d4cy00973h",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9fb9ebfc097582b062cf2eb3",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd6885398e28529d477ac4c3",
        "paper_id": "doi:10.1021/acs.jpcb.4c02650",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:147fa339122edc3ff44ba658",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, translational entropy loss scales with the ratio of adsorbate van der Waals volume to the framework's passing-bottleneck free-sphere diameter (as a confinement proxy): adsorbates large relative to the bottleneck free path lose more translational entropy, so the dimensionless volume-to-bottleneck contrast monotonically predicts the entropy-loss ratio s_ads/s_gas direction. log(q_Vol) - log(q_lsd_f) Rotational and orientational entropy loss at infinite dilution depends on how anisotropically extended and non-planar the adsorbate is: for nonlinear molecules, the product of heavy-atom enclosing radius (SPAN) with best-fit-plane excursion (PBF) proxies the number of restricted orientational degrees of freedom, so more extended, less planar molecules lose more rotational entropy in cage confinement; single-site (e.g., methane) and linear molecules have reduced or different orientational restriction, handled by explicit rotor branches. rotor_case( q_SPAN, q_SPAN, q_SPAN * q_PBF ) At infinite dilution, configurational entropy loss depends jointly on how much probe-accessible volume the framework offers per mass (AV) and how large an included sphere the free path accommodates (lsd_p, Dif): frameworks that are both volume-rich and wide along the free path impose less positional and orientational restriction, so the product of normalized accessibility and included-path diameter predicts lower entropy loss (higher s_ads/s_gas); this extends the retained AV-based contrast with a distinct connectivity/geometric-path mechanism. q_AV * q_lsd_p Formula contradicts its predeclared proxy direction  ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e98dff054a73e56b28f6bdf3",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:11077178fd4d765fcf20a5a1",
      "chunk:d52b47528dc9757d7e603c4f"
    ],
    "items": 10,
    "lexical_tokens": 4650,
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
