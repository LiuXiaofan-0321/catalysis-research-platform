# low/rag_agent/replicate-1/round-3

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

候选标识：`low/rag_agent/replicate-1/round-3/h1`

最终状态：scored；边际收益：-4.283898 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_to_span_confined_translation",
    "formula": "log(q_lsd_f) - log(q_SPAN + 0.1)",
    "hypothesis": "At infinite dilution, adsorption entropy loss in rigid pure-silica zeolites increases when the passing bottleneck (lsd_f) is small relative to the adsorbate heavy-atom enclosing radius (SPAN): confinement of translational degrees of freedom scales with the ratio of framework bottleneck to molecular size.",
    "rationale": "Translational confinement entropy in a channel network is bounded by how freely the molecule can move through the periodic free path. Using the bottleneck (Df) rather than the included diameter (Dif) reflects that motion between cages is gated by the narrowest passage. The +0.1 offset in the log argument guards against division-by-zero for adsorbates with legitimate SPAN = 0 (single-site rotors); the offset is an empirical numerical safeguard, not a physical length threshold.",
    "falsification_criteria": "If the training Spearman association between this descriptor and entropy loss/R has sign opposite to the predeclared direction (increasing descriptor should associate with decreasing entropy loss), or if the marginal MAE improvement over the retained baseline is negative, the confined-translation hypothesis is falsified for this feature set.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Df is a rigid-sphere bottleneck proxy, not the global cavity diameter; SPAN is a heavy-atom enclosing radius from the implicit-H representation and underestimates all-atom size. The offset 0.1 angstrom is an empirical numerical guard, not a physical length.",
      "physical_interpretation": "Both quantities retain native angstrom meaning; q-normalization uses the fixed training medians (lsd_f_ref = 5.16326, SPAN_ref = 1.860601424) and carries no universal physical meaning.",
      "boundary_behavior": "For SPAN = 0 (single-site adsorbates such as methane), q_SPAN = 0 and the log argument reduces to 0.1, giving a finite lower-branch value; lsd_f has no zeros in the training domain. The branch limit is acknowledged as an empirical smoothing of the single-site boundary.",
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
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "SPAN": "heavy_atom_enclosing_radius",
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
      "training_spearman": -0.6288246347978776,
      "target_association": "consistent",
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
    "name": "bottleneck_to_span_confined_translation",
    "formula": "log(q_lsd_f) - log(q_SPAN + 0.1)",
    "hypothesis": "At infinite dilution, adsorption entropy loss in rigid pure-silica zeolites increases when the passing bottleneck (lsd_f) is small relative to the adsorbate heavy-atom enclosing radius (SPAN): confinement of translational degrees of freedom scales with the ratio of framework bottleneck to molecular size.",
    "rationale": "Larger passing bottleneck relative to adsorbate size permits more translational freedom, hence less entropy loss (training Spearman -0.63, consistent with the predeclared direction). This is an empirical proxy contrast, not a demonstration of causality; the E02 cavity-diameter claim maps only conditionally onto Df.",
    "falsification_criteria": "If the training sign of association reverses, or marginal MAE improvement over the retained baseline becomes negative, the hypothesis is falsified for this feature set; a competing mechanism is that the association reflects molecule size rather than bottleneck gating.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E02",
      "E03"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f is the passing-bottleneck free sphere Df, not the global cavity diameter Di and not lsd_p (Dif); SPAN is an implicit-H heavy-atom enclosing radius that underestimates all-atom size. Transfer of the E02 cavity-confinement comparison to Df/SPAN proxies is conditional.",
      "physical_interpretation": "Both quantities are native lengths in angstrom; q-normalization uses fixed training references (lsd_f_ref = 5.16326, SPAN_ref = 1.860601424) and q = 1 carries no physical threshold meaning.",
      "boundary_behavior": "For SPAN = 0 (legitimate heavy-atom zeros, e.g. single-site adsorbates), q_SPAN = 0 and log(q_SPAN + 0.1) = log(0.1), finite; lsd_f has no zeros in training ([0.85684, 7.68726]), so log(q_lsd_f) is always finite. The +0.1 offset is an empirical numerical guard, not a physical length.",
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
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "SPAN": "heavy_atom_enclosing_radius",
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
      "training_spearman": -0.6288246347978776,
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
    "name": "bottleneck_to_span_confined_translation",
    "formula": "log(q_lsd_f) - log(q_SPAN + 0.1)",
    "hypothesis": "At infinite dilution, adsorption entropy loss in rigid pure-silica zeolites increases when the passing bottleneck (lsd_f) is small relative to the adsorbate heavy-atom enclosing radius (SPAN): confinement of translational degrees of freedom scales with the ratio of framework bottleneck to molecular size.",
    "rationale": "Larger passing bottleneck relative to adsorbate size permits more translational freedom, hence less entropy loss (training Spearman -0.63, consistent with the predeclared direction). This is an empirical proxy contrast, not a demonstration of causality; the E02 cavity-diameter claim maps only conditionally onto Df.",
    "falsification_criteria": "If the training sign of association reverses, or marginal MAE improvement over the retained baseline becomes negative, the hypothesis is falsified for this feature set; a competing mechanism is that the association reflects molecule size rather than bottleneck gating.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E02",
      "E03"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f is the passing-bottleneck free sphere Df, not the global cavity diameter Di and not lsd_p (Dif); SPAN is an implicit-H heavy-atom enclosing radius that underestimates all-atom size. Transfer of the E02 cavity-confinement comparison to Df/SPAN proxies is conditional.",
      "physical_interpretation": "Both quantities are native lengths in angstrom; q-normalization uses fixed training references (lsd_f_ref = 5.16326, SPAN_ref = 1.860601424) and q = 1 carries no physical threshold meaning.",
      "boundary_behavior": "For SPAN = 0 (legitimate heavy-atom zeros, e.g. single-site adsorbates), q_SPAN = 0 and log(q_SPAN + 0.1) = log(0.1), finite; lsd_f has no zeros in training ([0.85684, 7.68726]), so log(q_lsd_f) is always finite. The +0.1 offset is an empirical numerical guard, not a physical length.",
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
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "SPAN": "heavy_atom_enclosing_radius",
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
      "training_spearman": -0.6288246347978776,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/rag_agent/replicate-1/round-3/h2`

最终状态：scored；边际收益：+0.150673 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_area_per_volume_shape",
    "formula": "q_LabuteASA / q_Vol",
    "hypothesis": "Adsorbates with high specific molecular surface area per unit volume (large, elongated or multi-lobe shapes) lose more rotational entropy upon adsorption in rigid zeolites than compact molecules of equal volume, because high surface-to-volume shapes have more orientations that are sterically excluded by framework walls.",
    "rationale": "Surface-to-volume ratio separates compact (low ratio) from elongated/filamentary (high ratio) adsorbate shapes at fixed size. Rotational confinement penalizes shapes whose excluded-orientation fraction grows with asphericity. This is an empirical shape proxy: the heavy-atom representation means hydrogens are implicit, so the ratio is a coarse shape fingerprint, not an exact steric measure.",
    "falsification_criteria": "If the training association between the descriptor and entropy loss/R shows the opposite sign to the predeclared direction (increasing surface-to-volume ratio should associate with increasing entropy loss), the rotational-exclusion hypothesis is falsified; alternatively, a null association within noise would indicate shape alone is not separable from size in this domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "LabuteASA and Vol are implicit-H geometric descriptors of the free molecule; the ratio is a shape/compactness proxy only. Neither input has zeros in training, so the ratio is finite for all rows. Transfer to all-atom orientational statistics is unproven.",
      "physical_interpretation": "angstrom^2 / angstrom^3 = 1/angstrom units cancel between numerator and denominator after q-normalization by fixed references (LabuteASA_ref = 31.85047501, Vol_ref = 67.24); the q-ratio itself is dimensionless and q-unity is not a physical threshold.",
      "boundary_behavior": "Vol has a positive minimum (20.424) and LabuteASA a positive minimum (7.4506), so no division by zero occurs across the full training domain; no branch construction is needed.",
      "vary_input": "LabuteASA",
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
        "LabuteASA",
        "Vol"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.284607706697051,
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
    "slot_id": "h2",
    "name": "accessible_area_per_volume_shape",
    "formula": "q_LabuteASA / q_Vol",
    "hypothesis": "Adsorbates with high specific molecular surface area per unit volume (large, elongated or multi-lobe shapes) lose more rotational entropy upon adsorption in rigid zeolites than compact molecules of equal volume, because high surface-to-volume shapes have more orientations that are sterically excluded by framework walls.",
    "rationale": "Surface-to-volume ratio separates compact from elongated shapes; rotational confinement (E01, E03) plausibly penalizes aspheric shapes more. Empirical proxy only; training Spearman 0.28 is weak and does not establish causality or separability of shape from size.",
    "falsification_criteria": "A sign reversal of the training association, or a null association within noise indicating shape is not separable from size in this domain, falsifies the rotational-exclusion reading.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E03"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "LabuteASA and Vol are implicit-H descriptors of the free molecule; the ratio is a coarse shape/compactness proxy, not an exact steric orientational measure. Transfer to all-atom orientational statistics is unproven.",
      "physical_interpretation": "angstrom^2/angstrom^3 = 1/angstrom within each factor; after q-normalization by fixed references (LabuteASA_ref = 31.85047501, Vol_ref = 67.24) the ratio is dimensionless, and q = 1 is not a physical threshold.",
      "boundary_behavior": "LabuteASA (min 7.4506) and Vol (min 20.424) are strictly positive across training, so q_LabuteASA / q_Vol is finite for all 2361 rows; no branches or offsets needed.",
      "vary_input": "LabuteASA",
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
        "LabuteASA",
        "Vol"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.284607706697051,
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
    "slot_id": "h2",
    "name": "accessible_area_per_volume_shape",
    "formula": "q_LabuteASA / q_Vol",
    "hypothesis": "Adsorbates with high specific molecular surface area per unit volume (large, elongated or multi-lobe shapes) lose more rotational entropy upon adsorption in rigid zeolites than compact molecules of equal volume, because high surface-to-volume shapes have more orientations that are sterically excluded by framework walls.",
    "rationale": "Surface-to-volume ratio separates compact from elongated shapes; rotational confinement (E01, E03) plausibly penalizes aspheric shapes more. Empirical proxy only; training Spearman 0.28 is weak and does not establish causality or separability of shape from size.",
    "falsification_criteria": "A sign reversal of the training association, or a null association within noise indicating shape is not separable from size in this domain, falsifies the rotational-exclusion reading.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E03"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "LabuteASA and Vol are implicit-H descriptors of the free molecule; the ratio is a coarse shape/compactness proxy, not an exact steric orientational measure. Transfer to all-atom orientational statistics is unproven.",
      "physical_interpretation": "angstrom^2/angstrom^3 = 1/angstrom within each factor; after q-normalization by fixed references (LabuteASA_ref = 31.85047501, Vol_ref = 67.24) the ratio is dimensionless, and q = 1 is not a physical threshold.",
      "boundary_behavior": "LabuteASA (min 7.4506) and Vol (min 20.424) are strictly positive across training, so q_LabuteASA / q_Vol is finite for all 2361 rows; no branches or offsets needed.",
      "vary_input": "LabuteASA",
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
        "LabuteASA",
        "Vol"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.284607706697051,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/rag_agent/replicate-1/round-3/h3`

最终状态：scored；边际收益：-3.353958 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "planarity_rotor_branch",
    "formula": "rotor_case( q_PBF, q_SPAN, q_PBF * q_SPAN )",
    "hypothesis": "For heavy-atom planar adsorbates (PBF near zero, rotor_case nonlinear branch), increasing planarity reduces the number of sterically excluded orientations and thus reduces entropy loss, while the enclosing radius (SPAN) sets the scale of rotational confinement; single-site adsorbates carry no planarity penalty and scale only with SPAN.",
    "rationale": "Planarity (PBF) modulates how a flat molecule can rotate inside pores: flat orientations parallel to pore walls survive more often. The rotor_case construct assigns distinct scaling laws to single-site, linear, and nonlinear rotors, honoring that PMI-based inertia of single-site methane is a legitimate structural zero, not imputed. All three branches return dimensionless quantities, satisfying unit compatibility.",
    "falsification_criteria": "If within the nonlinear-rotor regime (PBF > 0) the training Spearman association between the branch expression and entropy loss/R shows sign opposite to the predeclared direction (increasing PBF*SPAN should associate with increasing entropy loss), or if forcing a single unified expression across rotor classes outperforms the branched form, the planarity-gated rotational hypothesis is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF is an implicit-H/heavy-atom planarity measure; legitimate zeros (587 training rows) are physical planarity, not missing data. SPAN is a heavy-atom enclosing radius. The rotor classification is fixed by PMI structure, and partial derivatives hold rotor class constant. Transfer to true all-atom rotation is a proxy assumption only.",
      "physical_interpretation": "All branch outputs are dimensionless products or ratios of q-normalized quantities using fixed training references (PBF_ref = 0.230844767, SPAN_ref = 1.860601424); q-unity carries no physical threshold meaning. The PBF = 0 branch value in the nonlinear expression is a legitimate physical planarity endpoint, and the single-site branch avoids the PBF input entirely.",
      "boundary_behavior": "At PBF = 0 the nonlinear branch yields 0 (perfectly planar, minimal rotational confinement penalty per this hypothesis), which is finite and physically interpretable; the single-site branch (q_SPAN only) is finite for all 54 single-site rows including SPAN = 0, where it gives 0, treated as an empirical lower bound of the branched form rather than a physical law.",
      "vary_input": "PBF",
      "descriptor_direction": "decreasing",
      "regime_input": "PBF",
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
    "direction_failure": {
      "opposite_n": 2147,
      "nonzero_fraction": 0.0
    },
    "reason": "Formula contradicts its predeclared proxy direction"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "planarity_rotor_branch",
    "formula": "rotor_case( q_SPAN, q_SPAN, q_PBF * q_SPAN )",
    "hypothesis": "For heavy-atom planar adsorbates (PBF near zero, rotor_case nonlinear branch), increasing planarity reduces the number of sterically excluded orientations and thus reduces entropy loss, while the enclosing radius (SPAN) sets the scale of rotational confinement; single-site adsorbates carry no planarity penalty and scale only with SPAN.",
    "rationale": "Direction correction of the rejected draft: within the nonlinear-rotor branch, increasing PBF (decreasing planarity) increases rotational confinement penalty, so the descriptor is predeclared as increasing with entropy loss; q_PBF*q_SPAN makes the confinement scale with size. The prior draft mislabeled the descriptor direction as decreasing, contradicting its own formula. This corrects the stored hypothesis's meaning consistently: more planar (smaller PBF) means less entropy loss.",
    "falsification_criteria": "If within the nonlinear-rotor regime the training Spearman association between q_PBF*q_SPAN and entropy loss/R is negative, or if a unified unbranched expression outperforms the branched form on marginal MAE, the planarity-gated rotational hypothesis is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E03",
      "E06"
    ],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF is an implicit-H/heavy-atom planarity measure with 587 legitimate training zeros; SPAN is a heavy-atom enclosing radius. Rotor class is fixed by PMI structure and held constant during partial derivatives. Transfer to true all-atom rotation is a proxy assumption only.",
      "physical_interpretation": "All branch outputs are dimensionless products of q-normalized quantities using fixed references (PBF_ref = 0.230844767, SPAN_ref = 1.860601424); q = 1 carries no physical threshold meaning.",
      "boundary_behavior": "Nonlinear branch at PBF = 0 yields 0, a legitimate physical planarity endpoint, finite; single-site and linear branches use only q_SPAN, finite including SPAN = 0 (empirical lower bound of the branched form, not a physical law). All branch outputs are dimensionless.",
      "vary_input": "PBF",
      "descriptor_direction": "increasing",
      "regime_input": "PBF",
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
        0.656249528
      ],
      "training_spearman": 0.2945424482561415,
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
    "name": "planarity_rotor_branch",
    "formula": "rotor_case( q_SPAN, q_SPAN, q_PBF * q_SPAN )",
    "hypothesis": "For heavy-atom planar adsorbates (PBF near zero, rotor_case nonlinear branch), increasing planarity reduces the number of sterically excluded orientations and thus reduces entropy loss, while the enclosing radius (SPAN) sets the scale of rotational confinement; single-site adsorbates carry no planarity penalty and scale only with SPAN.",
    "rationale": "Direction correction of the rejected draft: within the nonlinear-rotor branch, increasing PBF (decreasing planarity) increases rotational confinement penalty, so the descriptor is predeclared as increasing with entropy loss; q_PBF*q_SPAN makes the confinement scale with size. The prior draft mislabeled the descriptor direction as decreasing, contradicting its own formula. This corrects the stored hypothesis's meaning consistently: more planar (smaller PBF) means less entropy loss.",
    "falsification_criteria": "If within the nonlinear-rotor regime the training Spearman association between q_PBF*q_SPAN and entropy loss/R is negative, or if a unified unbranched expression outperforms the branched form on marginal MAE, the planarity-gated rotational hypothesis is falsified.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E03",
      "E06"
    ],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF is an implicit-H/heavy-atom planarity measure with 587 legitimate training zeros; SPAN is a heavy-atom enclosing radius. Rotor class is fixed by PMI structure and held constant during partial derivatives. Transfer to true all-atom rotation is a proxy assumption only.",
      "physical_interpretation": "All branch outputs are dimensionless products of q-normalized quantities using fixed references (PBF_ref = 0.230844767, SPAN_ref = 1.860601424); q = 1 carries no physical threshold meaning.",
      "boundary_behavior": "Nonlinear branch at PBF = 0 yields 0, a legitimate physical planarity endpoint, finite; single-site and linear branches use only q_SPAN, finite including SPAN = 0 (empirical lower bound of the branched form, not a physical law). All branch outputs are dimensionless.",
      "vary_input": "PBF",
      "descriptor_direction": "increasing",
      "regime_input": "PBF",
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
        0.656249528
      ],
      "training_spearman": 0.2945424482561415,
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
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:323d66ad417d981217705b45",
        "paper_id": "doi:10.1021/ja015797o",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:4ee093d81da6b5c01358e0ca",
        "paper_id": "doi:10.1021/acs.jctc.5c01100",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d3a799358d58da57167e96f1",
        "paper_id": "doi:10.1021/acs.langmuir.3c03931",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:43dedbc998f9c278eea622b0",
        "paper_id": "pmc:pmc9739862",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5ec00d417ad1fbe9acf3261a",
        "paper_id": "pmc:pmc8113345",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6c42e60d15e1bcc680c86db1",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9fb9ebfc097582b062cf2eb3",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:af5184fc2573625a8c063e9f",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d6ea1a200a0f892c276c47fa",
        "paper_id": "doi:10.1021/acs.jctc.4c00236",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:234d54d6aae543beff87e7be",
        "paper_id": "doi:10.1039/b504006j",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49d0db36d52cb97f9acfc9bb",
        "paper_id": "pmc:pmc11701358",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:72dfcce988c17185f87c465c",
        "paper_id": "doi:10.1021/jp1096663",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:977e7f0abbd21eee1d90f8b3",
        "paper_id": "doi:10.1039/b710051e",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b4c1161d21b2bed23495be99",
        "paper_id": "doi:10.1039/c003977b",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ba36706b3c347903791d4213",
        "paper_id": "doi:10.1039/c5cs00029g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e933adf17670b8f416a9170e",
        "paper_id": "doi:10.1021/la302230z",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution, adsorption entropy loss in rigid pure-silica zeolites increases when the passing bottleneck (lsd_f) is small relative to the adsorbate heavy-atom enclosing radius (SPAN): confinement of translational degrees of freedom scales with the ratio of framework bottleneck to molecular size. log(q_lsd_f) - log(q_SPAN + 0.1) Adsorbates with high specific molecular surface area per unit volume (large, elongated or multi-lobe shapes) lose more rotational entropy upon adsorption in rigid zeolites than compact molecules of equal volume, because high surface-to-volume shapes have more orientations that are sterically excluded by framework walls. q_LabuteASA / q_Vol For heavy-atom planar adsorbates (PBF near zero, rotor_case nonlinear branch), increasing planarity reduces the number of sterically excluded orientations and thus reduces entropy loss, while the enclosing radius (SPAN) sets the scale of rotational confinement; single-site adsorbates carry no planarity penalty and scale only with SPAN. rotor_case( q_PBF, q_SPAN, q_PBF * q_SPAN )   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:0d886a705a91409f8e891c53"
    ],
    "items": 10,
    "lexical_tokens": 4653,
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
      "record_id": "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "paper_id": "pmc:pmc6161062",
      "document_id": "document:7ba8c366c10dc56ab9a75bda",
      "quote": "Adsorption can therefore be best described by considering entropic losses due to both translational and rotational motions",
      "locator": {
        "kind": "pdf_page",
        "page": 1
      },
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
      "id": "E03"
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
