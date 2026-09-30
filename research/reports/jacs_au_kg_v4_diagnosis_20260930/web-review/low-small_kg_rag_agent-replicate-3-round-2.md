# low/small_kg_rag_agent/replicate-3/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/small_kg_rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h3",
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks (large AV) the same molecule retains more configurational freedom.",
    "rationale": "Entropy loss plausibly increases with the empirical contrast between adsorbate van der Waals volume and framework probe-accessible specific volume: in frameworks with small fixed-probe accessibility a large molecule is more spatially constrained, while open frameworks allow more configurational freedom, consistent with reported use of occupiable volume as an entropy-loss descriptor (E07). Limitations: AV is fixed-probe and mass-specific, not molecule-specific free volume, so no literal Vol/AV free-volume claim is made.",
    "falsification_criteria": "If entropy loss correlates with Vol alone equally well as with this ratio across frameworks spanning the AV range (including AV = 0 frameworks, where the fixed-probe accessibility may still permit molecular adsorption), the AV-contrast mechanism adds no explanatory power and should be rejected in favor of a pure molecular-size mechanism.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E03",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe AV ranks framework openness but is mass-specific and not molecule-specific; AV = 0 for the fixed geometric probe does not imply zero molecular adsorption space, so the ratio remains a smooth empirical proxy at AV = 0. Transferring the Vol/AV contrast to molecules smaller or larger than the probe is an empirical assumption.",
      "physical_interpretation": "Native Vol (van der Waals volume of the adsorbate) against native AV (probe-accessible specific volume of the framework, cm^3/g); the units do not form a physical free-volume equality, only a dimensionless empirical contrast after reference normalization. The additive 0.1 is a fixed smoothing constant without universal physical meaning. The precheck (Spearman +0.68, consistent) supports the declared decreasing-in-AV / increasing-in-Vol descriptor-to-loss direction but does not validate causality.",
      "boundary_behavior": "At AV = 0 the expression is finite, log(1 + 10 * Vol/Vol_ref); as AV grows, (Vol/Vol_ref)/(0.1 + AV/AV_ref) decreases monotonically toward 0, so the descriptor tends to log(1 + 0) = 0, NOT toward log(1 + Vol/Vol_ref). Vol training domain is strictly positive, so no division by zero occurs; the additive 0.1 only guards the legitimate AV zeros (28 training frameworks).",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_p",
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

候选标识：`low/small_kg_rag_agent/replicate-3/round-2/h1`

最终状态：scored；边际收益：+2.216599 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "span_bottleneck_configurational_crush",
    "formula": "log(1 + (SPAN / SPAN_ref) * exp(-(lsd_f / lsd_f_ref)))",
    "hypothesis": "Adsorption entropy loss increases with molecular enclosing radius and decreases with the framework's passing bottleneck diameter: a large-span molecule confined in a narrow-window framework loses translational/configurational freedom, while frameworks with wide free-sphere paths impose less confinement for the same molecule.",
    "rationale": "Uses native heavy-atom enclosing radius SPAN as a confinement-demand proxy and Zeo++ Df (lsd_f) as a confinement-supply proxy. The exponential decay of the supply term is an empirical smoothing choice, not a physical law; lsd_f is a bottleneck (largest passing sphere along a periodic free path), not a global cavity diameter, so it understates large-cage confinement. SPAN is a heavy-atom representation value; molecules with legitimate SPAN zero in training are single-site/linear cases where this confinement picture degenerates but the formula remains finite.",
    "falsification_criteria": "If training Spearman between this descriptor and entropy loss is negative or near zero within the full training domain, or if the derivative of the target with respect to lsd_f (rotor class fixed) is positive rather than negative, the confinement-supply mechanism is contradicted. Round-1 h1 (multiplicative lsd_f without decay) was contradicted (Spearman 0.286, target association contradicted), so the opposite monotonicity of lsd_f is the specific falsifiable prediction here.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "SPAN proxies molecular spatial demand from heavy-atom geometry only (implicit H); lsd_f proxies confinement supply but misses global cavity size (Di not available in D0 inputs); both are static geometric proxies, not dynamical measures.",
      "physical_interpretation": "All quantities are native dimensionless via fixed training-reference medians; ratios near 1 carry no universal physical meaning.",
      "boundary_behavior": "At SPAN = 0 (legitimate heavy-atom zero for some rotor classes), the descriptor equals log(1 + 0) = 0, finite; at large lsd_f the exponential decays, descriptor approaches log(2) * (SPAN/SPAN_ref)-dependent but bounded growth, finite everywhere.",
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
      "training_spearman": 0.6110581567151921,
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
    "name": "span_bottleneck_configurational_crush",
    "formula": "log(1 + (SPAN / SPAN_ref) * (lsd_f_ref / lsd_f))",
    "hypothesis": "Adsorption entropy loss increases with molecular enclosing radius and decreases with the framework's passing bottleneck diameter: a large-span molecule confined in a narrow-window framework loses translational/configurational freedom, while frameworks with wide free-sphere paths impose less confinement for the same molecule.",
    "rationale": "Confinement-demand vs confinement-supply contrast: entropy loss should increase with molecular enclosing radius and decrease with the framework passing bottleneck. The exp(-(lsd_f/lsd_f_ref)) draft was scored with target_association 'contradicted' despite positive rank correlation, so the monotone inverse form is substituted as the explicit falsifiable prediction; this is an empirical proxy association, not demonstrated causality, and the bottleneck Df understates large-cage confinement.",
    "falsification_criteria": "If the training Spearman between this descriptor and entropy loss is non-positive, or the partial derivative of the target with respect to lsd_f (rotor class fixed) is positive, the confinement-supply mechanism is contradicted. Competing mechanism: the association may be driven by a hidden framework-density/pore-size variable; test against density-residualized entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "SPAN is an implicit-H/heavy-atom enclosing-radius proxy, not full all-atom geometry; lsd_f is the Zeo++ passing bottleneck (Df), not the global cavity diameter Di, so cage-level confinement is systematically understated; both are static geometric proxies. The exponential decay form of the previous draft was replaced by a monotone inverse because the precheck reported the mechanism contradicted; the inverse form makes the negative derivative with respect to lsd_f explicit and unconditional rather than relying on an empirical decay constant.",
      "physical_interpretation": "SPAN/SPAN_ref and lsd_f/lsd_f_ref are dimensionless q-normalizations against fixed positive training-reference medians; ratios equal to 1 carry no universal physical meaning, and lsd_f_ref/lsd_f must not be read as a physical threshold.",
      "boundary_behavior": "lsd_f training domain is strictly positive (min 0.85684), so lsd_f_ref/lsd_f is finite on every row; at SPAN = 0 (legitimate heavy-atom zero) the descriptor is log(1) = 0; finite everywhere with no epsilon needed.",
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
      "training_spearman": 0.615234256097336,
      "target_association": "contradicted",
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
    "name": "span_bottleneck_configurational_crush",
    "formula": "log(1 + (SPAN / SPAN_ref) * (lsd_f_ref / lsd_f))",
    "hypothesis": "Adsorption entropy loss increases with molecular enclosing radius and decreases with the framework's passing bottleneck diameter: a large-span molecule confined in a narrow-window framework loses translational/configurational freedom, while frameworks with wide free-sphere paths impose less confinement for the same molecule.",
    "rationale": "Confinement-demand vs confinement-supply contrast: entropy loss should increase with molecular enclosing radius and decrease with the framework passing bottleneck. The exp(-(lsd_f/lsd_f_ref)) draft was scored with target_association 'contradicted' despite positive rank correlation, so the monotone inverse form is substituted as the explicit falsifiable prediction; this is an empirical proxy association, not demonstrated causality, and the bottleneck Df understates large-cage confinement.",
    "falsification_criteria": "If the training Spearman between this descriptor and entropy loss is non-positive, or the partial derivative of the target with respect to lsd_f (rotor class fixed) is positive, the confinement-supply mechanism is contradicted. Competing mechanism: the association may be driven by a hidden framework-density/pore-size variable; test against density-residualized entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "SPAN is an implicit-H/heavy-atom enclosing-radius proxy, not full all-atom geometry; lsd_f is the Zeo++ passing bottleneck (Df), not the global cavity diameter Di, so cage-level confinement is systematically understated; both are static geometric proxies. The exponential decay form of the previous draft was replaced by a monotone inverse because the precheck reported the mechanism contradicted; the inverse form makes the negative derivative with respect to lsd_f explicit and unconditional rather than relying on an empirical decay constant.",
      "physical_interpretation": "SPAN/SPAN_ref and lsd_f/lsd_f_ref are dimensionless q-normalizations against fixed positive training-reference medians; ratios equal to 1 carry no universal physical meaning, and lsd_f_ref/lsd_f must not be read as a physical threshold.",
      "boundary_behavior": "lsd_f training domain is strictly positive (min 0.85684), so lsd_f_ref/lsd_f is finite on every row; at SPAN = 0 (legitimate heavy-atom zero) the descriptor is log(1) = 0; finite everywhere with no epsilon needed.",
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
      "training_spearman": 0.615234256097336,
      "target_association": "contradicted",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/small_kg_rag_agent/replicate-3/round-2/h2`

最终状态：scored；边际收益：+3.042030 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.LabuteASA

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "planarity_rotor_braked_confinement",
    "formula": "rotor_case(log(1 + PBF / PBF_ref), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref) / (0.1 + LabuteASA / LabuteASA_ref)), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref) / (0.1 + LabuteASA / LabuteASA_ref)))",
    "hypothesis": "Rotational entropy loss upon adsorption grows with heavy-atom non-planarity (PBF) weighted by the third heavy-atom principal moment (PMI3) relative to the molecular surface area: non-planar, rotationally bulky molecules adsorbed on framework surfaces lose more rotational freedom per unit of contact area than flat molecules, whose planar orientation already matches the confining geometry. Single-site adsorbates (e.g., methane) have no meaningful heavy-atom rotational structure, so the branch reduces to a planarity-only offset.",
    "rationale": "PMI3 and PBF are original implicit-H/heavy-atom proxies; zero PMI1-3 values for some rotor classes are legitimate representation zeros, not claims that true all-atom inertia vanishes. LabuteASA in the denominator is a contact-area proxy (rotational freedom is restored proportionally to accessible surface interaction area). The 0.1 constant prevents division blowup for high-surface-area molecules and is an empirical smoother, not a physical threshold. The single-site branch uses PBF alone because PMI3 is not meaningful there; the linear and nonlinear branches share the coupling expression. Branch assignment uses native PMI proxy categories with fixed tolerance.",
    "falsification_criteria": "If the partial derivative of the target with respect to PBF (PMI3, rotor class fixed) is negative in the nonlinear branch, or the training Spearman between the descriptor and entropy loss is not positive, the planarity-rotor-coupling mechanism is falsified. Round-1 h2 (same coupling without the area normalization) showed a consistent but weak association (Spearman 0.351) and negative marginal improvement; if area normalization does not improve mechanism validation, the refinement is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "PMI3": "heavy_atom_inertia_proxy",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI3 is a shape/inertia proxy, not true all-atom inertia; PBF measures mean heavy-atom deviation from best-fit plane and does not encode all-atom geometry; LabuteASA is an approximate surface proxy. Transfer across zeolite topologies assumed because no chemistry-specific terms enter.",
      "physical_interpretation": "q-normalization by fixed training-reference medians is dimensionless bookkeeping; ratios equal to 1 are not physical equality thresholds.",
      "boundary_behavior": "At PBF = 0 (legitimate planar heavy-atom zero), all branches give log(1 + 0) = 0, finite; at PMI3 = 0 (legitimate proxy zero in linear/small cases) the coupled expression equals log(1) = 0; the 0.1 + LabuteASA/LabuteASA_ref denominator is strictly positive, so no division by zero occurs.",
      "vary_input": "PBF",
      "descriptor_direction": "increasing",
      "regime_input": "PBF",
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
        "LabuteASA",
        "PBF",
        "PMI3"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity",
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.656249528
      ],
      "training_spearman": 0.3484941180540418,
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
    "name": "planarity_rotor_braked_confinement",
    "formula": "rotor_case(log(1 + PBF / PBF_ref), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref)), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref)))",
    "hypothesis": "Rotational entropy loss upon adsorption grows with heavy-atom non-planarity (PBF) weighted by the third heavy-atom principal moment (PMI3) relative to the molecular surface area: non-planar, rotationally bulky molecules adsorbed on framework surfaces lose more rotational freedom per unit of contact area than flat molecules, whose planar orientation already matches the confining geometry. Single-site adsorbates (e.g., methane) have no meaningful heavy-atom rotational structure, so the branch reduces to a planarity-only offset.",
    "rationale": "Rotational entropy loss grows with heavy-atom non-planarity weighted by the third heavy-atom principal moment: non-planar, rotationally bulky molecules lose more rotational freedom per contact than flat molecules whose planar orientation already matches the confining geometry (conditional on reported MFI-vs-FAU rotational-loss contrasts). Single-site branch reduces to a planarity-only offset; linear and nonlinear branches share the coupling. This remains an empirical proxy association; the previous mechanism check was not validated.",
    "falsification_criteria": "If the partial derivative of the target with respect to PBF (PMI3, rotor class fixed) is negative in the nonlinear branch, or the training Spearman turns non-positive, the planarity-rotor coupling is falsified. Competing mechanism: the association may reflect molecule size (Vol/MW) rather than rotational shape; test against size-residualized entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E03"
    ],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI3 and PBF are original implicit-H/heavy-atom proxies; zero proxy values are representation zeros, not claims that true all-atom inertia vanishes. The LabuteASA area normalization of the previous draft was removed because its precheck was 'contradicted' and round-1 area-coupling showed negative marginal improvement; the reverted coupling is the specific falsifiable claim. Transfer across zeolite topologies is assumed because no chemistry-specific terms enter.",
      "physical_interpretation": "q-normalizations are dimensionless bookkeeping against fixed positive training medians; q-ratio = 1 is not a native equality or physical threshold. All three rotor_case outputs are dimensionless logs of 1 + a dimensionless product.",
      "boundary_behavior": "At PBF = 0 (legitimate planar heavy-atom zero) all branches give log(1) = 0; at PMI3 = 0 (legitimate proxy zero for small/linear cases) the coupled branches give log(1) = 0; all arguments are finite over the full training domain with no division at all, so no epsilon is required.",
      "vary_input": "PBF",
      "descriptor_direction": "increasing",
      "regime_input": "PBF",
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
        "PBF",
        "PMI3"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.656249528
      ],
      "training_spearman": 0.35165096468908985,
      "target_association": "contradicted",
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
    "name": "planarity_rotor_braked_confinement",
    "formula": "rotor_case(log(1 + PBF / PBF_ref), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref)), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref)))",
    "hypothesis": "Rotational entropy loss upon adsorption grows with heavy-atom non-planarity (PBF) weighted by the third heavy-atom principal moment (PMI3) relative to the molecular surface area: non-planar, rotationally bulky molecules adsorbed on framework surfaces lose more rotational freedom per unit of contact area than flat molecules, whose planar orientation already matches the confining geometry. Single-site adsorbates (e.g., methane) have no meaningful heavy-atom rotational structure, so the branch reduces to a planarity-only offset.",
    "rationale": "Rotational entropy loss grows with heavy-atom non-planarity weighted by the third heavy-atom principal moment: non-planar, rotationally bulky molecules lose more rotational freedom per contact than flat molecules whose planar orientation already matches the confining geometry (conditional on reported MFI-vs-FAU rotational-loss contrasts). Single-site branch reduces to a planarity-only offset; linear and nonlinear branches share the coupling. This remains an empirical proxy association; the previous mechanism check was not validated.",
    "falsification_criteria": "If the partial derivative of the target with respect to PBF (PMI3, rotor class fixed) is negative in the nonlinear branch, or the training Spearman turns non-positive, the planarity-rotor coupling is falsified. Competing mechanism: the association may reflect molecule size (Vol/MW) rather than rotational shape; test against size-residualized entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E03"
    ],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI3 and PBF are original implicit-H/heavy-atom proxies; zero proxy values are representation zeros, not claims that true all-atom inertia vanishes. The LabuteASA area normalization of the previous draft was removed because its precheck was 'contradicted' and round-1 area-coupling showed negative marginal improvement; the reverted coupling is the specific falsifiable claim. Transfer across zeolite topologies is assumed because no chemistry-specific terms enter.",
      "physical_interpretation": "q-normalizations are dimensionless bookkeeping against fixed positive training medians; q-ratio = 1 is not a native equality or physical threshold. All three rotor_case outputs are dimensionless logs of 1 + a dimensionless product.",
      "boundary_behavior": "At PBF = 0 (legitimate planar heavy-atom zero) all branches give log(1) = 0; at PMI3 = 0 (legitimate proxy zero for small/linear cases) the coupled branches give log(1) = 0; all arguments are finite over the full training domain with no division at all, so no epsilon is required.",
      "vary_input": "PBF",
      "descriptor_direction": "increasing",
      "regime_input": "PBF",
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
        "PBF",
        "PMI3"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.656249528
      ],
      "training_spearman": 0.35165096468908985,
      "target_association": "contradicted",
      "perturbation": 0.0046290119000000005,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/small_kg_rag_agent/replicate-3/round-2/h3`

最终状态：scored；边际收益：+6.102508 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, formula, novelty_status, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.AV, variable_mappings.lsd_p

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's fixed-probe accessible specific volume: in frameworks with small probe accessibility, a large molecule has fewer accessible configurations (higher entropy loss), whereas in open frameworks the same molecule retains more configurational freedom.",
    "rationale": "Retained from round 1 with positive marginal improvement (0.0069) and consistent training association (Spearman 0.681). AV is a fixed-probe, mass-specific accessibility measure, not molecule-specific free volume; zero AV for the fixed probe does not imply zero physical adsorption space for a differently sized molecule, so the 0.1 constant is an empirical smoother that keeps the expression finite at legitimate AV = 0 rather than a physical threshold. Mechanism validation numerically was not achieved (perturbation test false), so this remains an empirical proxy association, not demonstrated causality.",
    "falsification_criteria": "If partial derivative of the target with respect to AV (rotor class fixed) is positive, or the training Spearman turns non-positive, the accessible-volume-contrast mechanism is contradicted. A competing mechanism is that correlation is driven by a hidden framework-density variable rather than accessibility per se; testing descriptor value against density-residualized entropy loss distinguishes these.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Fixed-probe AV is assumed to rank molecule-specific free volume monotonically for the adsorbate size range in the training domain; this fails when adsorbate size distribution differs strongly from the probe size.",
      "physical_interpretation": "Vol/Vol_ref and AV/AV_ref are dimensionless q-normalizations against fixed training-reference medians; the ratio is row-varying, and X/q_X equals the constant X_ref, which must never be used as an input.",
      "boundary_behavior": "At AV = 0 (legitimate zero accessibility for the fixed probe, 28 training rows), the descriptor is log(1 + (Vol/Vol_ref)/0.1), finite and large but bounded; at large AV it decays toward log(2); no division by zero occurs because of the positive constant.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "AV",
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
    "reason": "Redundant with a current input"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + lsd_p / lsd_p_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's fixed-probe accessible specific volume: in frameworks with small probe accessibility, a large molecule has fewer accessible configurations (higher entropy loss), whereas in open frameworks the same molecule retains more configurational freedom.",
    "rationale": "Entropy loss increases with the ratio of molecular volume to the included free-path diameter: large molecules in frameworks with small included diameters along the diffusion path have fewer accessible configurations, while open frameworks preserve more configurational freedom (consistent with reported smaller-pore frameworks showing larger entropy-loss fractions). This replaces the redundant Vol/AV contrast with a non-redundant free-path descriptor; it remains an empirical proxy association, not demonstrated causality.",
    "falsification_criteria": "If the partial derivative of the target with respect to lsd_p (rotor class fixed) is positive, or the training Spearman turns non-positive, the free-path confinement mechanism is contradicted. Competing mechanism: the association may be driven by a hidden framework-density variable; test against density-residualized entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04",
      "E08"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Vol is the molecular van der Waals volume; lsd_p is the largest included sphere along the free-sphere path (Dif), NOT the passing bottleneck Df and NOT necessarily the global cavity Di. The previous resubmission of the Vol-vs-AV contrast was rejected as redundant with the already-retained round-1 input, so accessibility is now proxied by the free-path included diameter instead. The 0.1 constant is an empirical smoother, not a physical threshold.",
      "physical_interpretation": "Vol/Vol_ref and lsd_p/lsd_p_ref are dimensionless q-normalizations against fixed positive training medians; the ratio is row-varying and X/q_X equals the constant X_ref, which must never be used as an input. q-ratio = 1 is not native equality.",
      "boundary_behavior": "lsd_p training domain is strictly positive (min 3.3452), so the denominator 0.1 + lsd_p/lsd_p_ref is strictly positive on every row and the descriptor is finite everywhere; at small lsd_p the descriptor grows boundedly as log(1 + (Vol/Vol_ref)/0.1); at large lsd_p it decays toward log(2).",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
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
        3.3452,
        15.5604
      ],
      "training_spearman": 0.6624332099943495,
      "target_association": "contradicted",
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
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + lsd_p / lsd_p_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's fixed-probe accessible specific volume: in frameworks with small probe accessibility, a large molecule has fewer accessible configurations (higher entropy loss), whereas in open frameworks the same molecule retains more configurational freedom.",
    "rationale": "Entropy loss increases with the ratio of molecular volume to the included free-path diameter: large molecules in frameworks with small included diameters along the diffusion path have fewer accessible configurations, while open frameworks preserve more configurational freedom (consistent with reported smaller-pore frameworks showing larger entropy-loss fractions). This replaces the redundant Vol/AV contrast with a non-redundant free-path descriptor; it remains an empirical proxy association, not demonstrated causality.",
    "falsification_criteria": "If the partial derivative of the target with respect to lsd_p (rotor class fixed) is positive, or the training Spearman turns non-positive, the free-path confinement mechanism is contradicted. Competing mechanism: the association may be driven by a hidden framework-density variable; test against density-residualized entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04",
      "E08"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Vol is the molecular van der Waals volume; lsd_p is the largest included sphere along the free-sphere path (Dif), NOT the passing bottleneck Df and NOT necessarily the global cavity Di. The previous resubmission of the Vol-vs-AV contrast was rejected as redundant with the already-retained round-1 input, so accessibility is now proxied by the free-path included diameter instead. The 0.1 constant is an empirical smoother, not a physical threshold.",
      "physical_interpretation": "Vol/Vol_ref and lsd_p/lsd_p_ref are dimensionless q-normalizations against fixed positive training medians; the ratio is row-varying and X/q_X equals the constant X_ref, which must never be used as an input. q-ratio = 1 is not native equality.",
      "boundary_behavior": "lsd_p training domain is strictly positive (min 3.3452), so the denominator 0.1 + lsd_p/lsd_p_ref is strictly positive on every row and the descriptor is finite everywhere; at small lsd_p the descriptor grows boundedly as log(1 + (Vol/Vol_ref)/0.1); at large lsd_p it decays toward log(2).",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
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
        3.3452,
        15.5604
      ],
      "training_spearman": 0.6624332099943495,
      "target_association": "contradicted",
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
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
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
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3d8ed419d3eff1212dddc68f",
        "paper_id": "doi:10.1039/d5ce00034c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:43dedbc998f9c278eea622b0",
        "paper_id": "pmc:pmc9739862",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:72dfcce988c17185f87c465c",
        "paper_id": "doi:10.1021/jp1096663",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e1b683dc5917739326965133",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:16c6127c51dffcae786df6ce",
        "paper_id": "doi:10.1038/nmat2530",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:63a944566fa9e4d1bde391c6",
        "paper_id": "doi:10.1063/1.1781119",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:682b714f21fe17245939e4e3",
        "paper_id": "doi:10.1063/1.2790903",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6c42e60d15e1bcc680c86db1",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cfbfd9fb0705eed9a2a3f8e",
        "paper_id": "doi:10.1021/acs.langmuir.2c00923",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:8dc09a802942ff3d455ea3a8",
        "paper_id": "doi:10.26434/chemrxiv.9725948.v2",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement Adsorption entropy loss increases with molecular enclosing radius and decreases with the framework's passing bottleneck diameter: a large-span molecule confined in a narrow-window framework loses translational/configurational freedom, while frameworks with wide free-sphere paths impose less confinement for the same molecule. log(1 + (SPAN / SPAN_ref) * exp(-(lsd_f / lsd_f_ref))) Rotational entropy loss upon adsorption grows with heavy-atom non-planarity (PBF) weighted by the third heavy-atom principal moment (PMI3) relative to the molecular surface area: non-planar, rotationally bulky molecules adsorbed on framework surfaces lose more rotational freedom per unit of contact area than flat molecules, whose planar orientation already matches the confining geometry. Single-site adsorbates (e.g., methane) have no meaningful heavy-atom rotational structure, so the branch reduces to a planarity-only offset. rotor_case(log(1 + PBF / PBF_ref), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref) / (0.1 + LabuteASA / LabuteASA_ref)), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref) / (0.1 + LabuteASA / LabuteASA_ref))) Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's fixed-probe accessible specific volume: in frameworks with small probe accessibility, a large molecule has fewer accessible configurations (higher entropy loss), whereas in open frameworks the same molecule retains more configurational freedom. log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:8dd99e6f4fc8a3c4e46d940b",
      "chunk:e98dff054a73e56b28f6bdf3"
    ],
    "items": 10,
    "lexical_tokens": 4774,
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
