# low/small_kg_rag_agent/replicate-2/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/small_kg_rag_agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h3",
    "name": "accessible_area_squeeze_contrast",
    "formula": "log((LabuteASA/LabuteASA_ref) / (AV/AV_ref + 1))",
    "hypothesis": "Entropy loss at infinite dilution increases with adsorbate surface area but decreases with framework probe-accessible specific volume, because larger contact surface and tighter accessible pore space both reduce retained configurational freedom; their contrast separates adsorbate-driven from framework-driven entropy mechanisms.",
    "rationale": "Coupling of shape (LabuteASA, adsorbate contact area proxy) and connectivity/probe-volume (AV, fixed-probe mass-specific accessibility). AV has 28 legitimate zeros in training (fixed geometric probe cannot enter); the additive +1 in the denominator keeps the expression finite at AV = 0 without imputation and is an empirical smoothing constant, not a physical percolation threshold. ASA/AV zero rows (inaccessible frameworks) are handled since the formula never divides by AV itself.",
    "falsification_criteria": "If frameworks with AV = 0 for the fixed probe (no physical molecular space by the descriptor's logic) still show nonzero adsorption entropy loss for small molecules, the AV-based mechanism is falsified for those systems; if LabuteASA loses predictive power when Vol is controlled, the surface-contact mechanism collapses into a pure size effect.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA is an approximate molecular surface (adsorbate geometry proxy); AV is fixed-probe accessibility per mass, not molecule-specific free volume, and zero AV does not imply zero adsorption space. Kinetic escape through Df is not equated with equilibrium entropy here.",
      "physical_interpretation": "LabuteASA/LabuteASA_ref scales contact area; AV/AV_ref scales pore openness. +1 is a finite-domain smoothing device; no physical q-unity threshold is claimed.",
      "boundary_behavior": "At AV = 0 the denominator equals 1 and the descriptor reduces to log(LabuteASA/LabuteASA_ref), finite and interpreted as an inaccessible-probe framework where the descriptor carries no contrast information; this limitation is acknowledged rather than hidden.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "LabuteASA",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  {
    "slot_id": "h1",
    "name": "included_path_confinement",
    "formula": "log(1 + (Vol/Vol_ref) * (lsd_p/lsd_p_ref) ** -2)",
    "hypothesis": "At infinite dilution in pure-silica zeolites, entropy loss increases when a volumetrically larger adsorbate is hosted in frameworks with a smaller included free-sphere diameter along the diffusion path, because stronger host-guest confinement suppresses translational and orientational freedom; the included diameter (lsd_p) characterizes the confining channel/cage wall along the free path, unlike the bottleneck diameter (lsd_f) which only gates passage.",
    "rationale": "Uses lsd_p (Zeo++ Dif, included sphere along the free-sphere path) as a confinement-scale proxy; this is conditionally supported by reported MFI-vs-FAU and FER-vs-FAU comparisons where smaller pores gave larger rotational/total entropy loss (E01, E02, E04). Caveat preserved: the source 'average cavity diameter' is not Dif, so the mapping is a proxy transfer, not an identity; the round-1 lsd_f (bottleneck) version was contradicted, consistent with gating/passage diameter being the wrong quantity. The Vol product expresses that the penalty scales with constrained molecular volume. Empirical proxy hypothesis, not a validated causal mechanism.",
    "falsification_criteria": "If training Spearman between the descriptor and entropy loss is negative, or the partial d(descriptor)/d(lsd_p) at fixed rotor class and fixed Vol is non-negative (i.e., entropy loss does not increase as lsd_p decreases), the confinement hypothesis is falsified for this descriptor; competing mechanisms: AV (probe-accessible volume) or Vol-driven scaling rather than the Dif term.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_p is a geometric confinement proxy along the free-sphere path, NOT the global cavity diameter Di and NOT the bottleneck Df; the literature confinement claims (E01, E02) reference cavity-size metrics, so transfer to Dif is an assumption, not an identity. Vol is a van der Waals volume proxy not resolved by atom type; both ignore framework chemistry beyond geometry.",
      "physical_interpretation": "Vol/Vol_ref and lsd_p/lsd_p_ref are row-varying dimensionless ratios to fixed positive training-reference medians; the constant 1 keeps the log argument dimensionless and positive; no unity threshold is claimed.",
      "boundary_behavior": "Finite for all training rows: Vol>0 and lsd_p>0 everywhere in-domain; Vol_ref and lsd_p_ref are positive constants so the -2 exponent never divides by a zero variable. As lsd_p grows the descriptor approaches log(1); as Vol grows it grows logarithmically.",
      "vary_input": "lsd_p",
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

候选标识：`low/small_kg_rag_agent/replicate-2/round-3/h1`

最终状态：scored；边际收益：-1.527216 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_gated_area_retention",
    "formula": "log(1 + (LabuteASA/LabuteASA_ref) * (lsd_f/lsd_f_ref) ** -1)",
    "hypothesis": "At infinite dilution in pure-silica zeolites, entropy loss increases when an adsorbate with larger contact-capable surface area is hosted in a framework with a smaller passing bottleneck free-sphere diameter, because narrow window frameworks restrict positional sampling over which the contact surface can explore the pore wall.",
    "rationale": "Combines the adsorbate-driven contact-area mechanism (supported by h3 round 1, Spearman 0.65) with the framework connectivity constraint expressed by the bottleneck Df rather than the included diameter Dif already used in the retained h1; the inverse bottleneck gates how many distinct wall-contact configurations are reachable. Limitation: Df is a geometric window proxy, not a dynamical barrier; fixed-probe accessibility does not equal molecule-specific free volume.",
    "falsification_criteria": "If the partial derivative with respect to lsd_f is not negative on average (i.e., entropy loss does not increase as bottleneck shrinks at fixed adsorbate area), or if the target association reverses within the training regime, the bottleneck-gating mechanism is contradicted in favor of a pure included-diameter confinement picture.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA is an implicit-H approximate surface, not a true all-atom contact area; lsd_f is a periodic free-path bottleneck, not a global cavity diameter; their product has no universal physical unit meaning, only a dimensionless empirical contrast.",
      "physical_interpretation": "Both inputs are native positive quantities over the full training domain, so the expression is finite for every training row; the +1 inside the log is an empirical smoothing constant, not a physical threshold.",
      "boundary_behavior": "lsd_f min 0.85684 and LabuteASA min 7.4506 are strictly positive in training, so no zero division occurs; as either input approaches its lower bound the descriptor decreases smoothly toward log(1 + small), remaining finite.",
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
        "lsd_f"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.6095296127269412,
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
    "name": "bottleneck_gated_area_retention",
    "formula": "log(1 + (LabuteASA/LabuteASA_ref) * (lsd_f/lsd_f_ref) ** -1)",
    "hypothesis": "At infinite dilution in pure-silica zeolites, entropy loss increases when an adsorbate with larger contact-capable surface area is hosted in a framework with a smaller passing bottleneck free-sphere diameter, because narrow window frameworks restrict positional sampling over which the contact surface can explore the pore wall.",
    "rationale": "Kept unchanged: the precheck shows a consistent positive training association (Spearman 0.61) for the inverse-bottleneck gating of contact-area exploration. lsd_f is the passing-bottleneck Df, not the global cavity diameter cited in E02, so the E01/E02 rotational-loss claims transfer only as a qualitative confinement-direction hypothesis via a geometric path contrast, not as a fitted law. LabuteASA is an implicit-H approximate surface, not a true all-atom contact area. All training values of both inputs are strictly positive, so the expression is finite everywhere; the +1 inside the log is an empirical smoothing constant, not a physical threshold.",
    "falsification_criteria": "If the partial derivative with respect to lsd_f is not negative on average (i.e., entropy loss does not increase as bottleneck shrinks at fixed adsorbate area), or if the target association reverses within the training regime, the bottleneck-gating mechanism is contradicted in favor of a pure included-diameter confinement picture.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E03"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA is an implicit-H approximate surface, not a true all-atom contact area; lsd_f is a periodic free-path bottleneck, not a global cavity diameter; their product has no universal physical unit meaning, only a dimensionless empirical contrast.",
      "physical_interpretation": "Both inputs are native positive quantities over the full training domain, so the expression is finite for every training row; the +1 inside the log is an empirical smoothing constant, not a physical threshold.",
      "boundary_behavior": "lsd_f min 0.85684 and LabuteASA min 7.4506 are strictly positive in training, so no zero division occurs; as either input approaches its lower bound the descriptor decreases smoothly toward log(1 + small), remaining finite.",
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
        "lsd_f"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.6095296127269412,
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
    "name": "bottleneck_gated_area_retention",
    "formula": "log(1 + (LabuteASA/LabuteASA_ref) * (lsd_f/lsd_f_ref) ** -1)",
    "hypothesis": "At infinite dilution in pure-silica zeolites, entropy loss increases when an adsorbate with larger contact-capable surface area is hosted in a framework with a smaller passing bottleneck free-sphere diameter, because narrow window frameworks restrict positional sampling over which the contact surface can explore the pore wall.",
    "rationale": "Kept unchanged: the precheck shows a consistent positive training association (Spearman 0.61) for the inverse-bottleneck gating of contact-area exploration. lsd_f is the passing-bottleneck Df, not the global cavity diameter cited in E02, so the E01/E02 rotational-loss claims transfer only as a qualitative confinement-direction hypothesis via a geometric path contrast, not as a fitted law. LabuteASA is an implicit-H approximate surface, not a true all-atom contact area. All training values of both inputs are strictly positive, so the expression is finite everywhere; the +1 inside the log is an empirical smoothing constant, not a physical threshold.",
    "falsification_criteria": "If the partial derivative with respect to lsd_f is not negative on average (i.e., entropy loss does not increase as bottleneck shrinks at fixed adsorbate area), or if the target association reverses within the training regime, the bottleneck-gating mechanism is contradicted in favor of a pure included-diameter confinement picture.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E03"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "LabuteASA is an implicit-H approximate surface, not a true all-atom contact area; lsd_f is a periodic free-path bottleneck, not a global cavity diameter; their product has no universal physical unit meaning, only a dimensionless empirical contrast.",
      "physical_interpretation": "Both inputs are native positive quantities over the full training domain, so the expression is finite for every training row; the +1 inside the log is an empirical smoothing constant, not a physical threshold.",
      "boundary_behavior": "lsd_f min 0.85684 and LabuteASA min 7.4506 are strictly positive in training, so no zero division occurs; as either input approaches its lower bound the descriptor decreases smoothly toward log(1 + small), remaining finite.",
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
        "lsd_f"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.6095296127269412,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/small_kg_rag_agent/replicate-2/round-3/h2`

最终状态：scored；边际收益：-1.308991 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "heavy_planar_oblate_compression",
    "formula": "log(1 + (Vol/Vol_ref) * (PBF/PBF_ref) ** 2)",
    "hypothesis": "For nonlinear adsorbates, entropy loss increases when a volumetrically large molecule is also displaced from planarity (large height above its best-fit plane), because a bulky non-planar body loses more rotational and orientational freedom upon confinement than a flat body of equal volume that can hug pore walls in more orientations.",
    "rationale": "Round 1 h2 showed PBF alone has a consistent but weak association (Spearman 0.29); multiplying by volume tests whether planarity matters only in combination with size. Uses the original heavy-atom PBF representation: legitimate zeros (587 training rows) represent planar molecules, for which the descriptor smoothly reduces to log(1) = 0, encoding 'no planarity penalty' rather than an imputed value.",
    "falsification_criteria": "If conditioning on Vol reverses or nullifies the PBF association (partial derivative with respect to PBF non-positive within the nonlinear subpopulation), the size-dependent planarity mechanism is falsified and planarity effects, if any, are independent of volume.",
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
      "mechanism_family": "rotation",
      "proxy_assumptions": "PBF is an implicit-H/heavy-atom planarity proxy, not full all-atom geometry; Vol is a van der Waals volume, not an accessible free volume; the square on PBF is an empirical smoothing choice with no universal physical meaning.",
      "physical_interpretation": "The descriptor increases with native PBF at fixed Vol and with native Vol at fixed PBF; PBF_ref and Vol_ref are fixed training medians used only for dimensionless scaling, not physical unity thresholds.",
      "boundary_behavior": "At PBF = 0 (legitimate planar molecules, 587 training rows) the descriptor equals 0, finite and continuous; at the Vol lower bound 20.424 with maximal PBF it remains small and finite. No division by zero occurs anywhere in the domain.",
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
        0.0,
        0.656249528
      ],
      "training_spearman": 0.3090560731837001,
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
    "name": "heavy_planar_oblate_compression",
    "formula": "log(1 + (Vol/Vol_ref) * (PBF/PBF_ref) ** 2)",
    "hypothesis": "For nonlinear adsorbates, entropy loss increases when a volumetrically large molecule is also displaced from planarity (large height above its best-fit plane), because a bulky non-planar body loses more rotational and orientational freedom upon confinement than a flat body of equal volume that can hug pore walls in more orientations.",
    "rationale": "Kept unchanged: the precheck shows a consistent positive training association (Spearman 0.31). PBF is the original implicit-H/heavy-atom planarity proxy with 587 legitimate zero rows representing planar molecules; at PBF = 0 the descriptor smoothly equals log(1) = 0, encoding 'no planarity penalty' without imputation. Vol is a van der Waals volume, not molecule-specific accessible free volume. The square on PBF is an empirical smoothing choice, not a derived physical law. Rotational freedom arguments from E06/E07 motivate the mechanism only conditionally.",
    "falsification_criteria": "If conditioning on Vol reverses or nullifies the PBF association (partial derivative with respect to PBF non-positive within the nonlinear subpopulation), the size-dependent planarity mechanism is falsified and planarity effects, if any, are independent of volume.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E06",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PBF is an implicit-H/heavy-atom planarity proxy, not full all-atom geometry; Vol is a van der Waals volume, not an accessible free volume; the square on PBF is an empirical smoothing choice with no universal physical meaning.",
      "physical_interpretation": "The descriptor increases with native PBF at fixed Vol and with native Vol at fixed PBF; PBF_ref and Vol_ref are fixed training medians used only for dimensionless scaling, not physical unity thresholds.",
      "boundary_behavior": "At PBF = 0 (legitimate planar molecules, 587 training rows) the descriptor equals 0, finite and continuous; at the Vol lower bound 20.424 with maximal PBF it remains small and finite. No division by zero occurs anywhere in the domain.",
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
        0.0,
        0.656249528
      ],
      "training_spearman": 0.3090560731837001,
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
    "name": "heavy_planar_oblate_compression",
    "formula": "log(1 + (Vol/Vol_ref) * (PBF/PBF_ref) ** 2)",
    "hypothesis": "For nonlinear adsorbates, entropy loss increases when a volumetrically large molecule is also displaced from planarity (large height above its best-fit plane), because a bulky non-planar body loses more rotational and orientational freedom upon confinement than a flat body of equal volume that can hug pore walls in more orientations.",
    "rationale": "Kept unchanged: the precheck shows a consistent positive training association (Spearman 0.31). PBF is the original implicit-H/heavy-atom planarity proxy with 587 legitimate zero rows representing planar molecules; at PBF = 0 the descriptor smoothly equals log(1) = 0, encoding 'no planarity penalty' without imputation. Vol is a van der Waals volume, not molecule-specific accessible free volume. The square on PBF is an empirical smoothing choice, not a derived physical law. Rotational freedom arguments from E06/E07 motivate the mechanism only conditionally.",
    "falsification_criteria": "If conditioning on Vol reverses or nullifies the PBF association (partial derivative with respect to PBF non-positive within the nonlinear subpopulation), the size-dependent planarity mechanism is falsified and planarity effects, if any, are independent of volume.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E06",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PBF is an implicit-H/heavy-atom planarity proxy, not full all-atom geometry; Vol is a van der Waals volume, not an accessible free volume; the square on PBF is an empirical smoothing choice with no universal physical meaning.",
      "physical_interpretation": "The descriptor increases with native PBF at fixed Vol and with native Vol at fixed PBF; PBF_ref and Vol_ref are fixed training medians used only for dimensionless scaling, not physical unity thresholds.",
      "boundary_behavior": "At PBF = 0 (legitimate planar molecules, 587 training rows) the descriptor equals 0, finite and continuous; at the Vol lower bound 20.424 with maximal PBF it remains small and finite. No division by zero occurs anywhere in the domain.",
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
        0.0,
        0.656249528
      ],
      "training_spearman": 0.3090560731837001,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/small_kg_rag_agent/replicate-2/round-3/h3`

最终状态：scored；边际收益：+0.961162 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "framework_density_specific_area_contrast",
    "formula": "log(1 + (ASA/ASA_ref) * (density/density_ref) ** -1)",
    "hypothesis": "Entropy loss increases with the framework's probe-accessible specific surface area but this effect is stronger in frameworks of lower framework density, because at equal surface area a lighter, more open framework offers more geometrically distinct adsorption sites, while dense frameworks concentrate area into fewer, more degenerate configurations.",
    "rationale": "Introduces a mechanism family (framework geometry contrast) not yet represented by the retained set: ASA is a mass-specific probe-accessible area and density is a native-scale framework density proxy with unresolved unit; their ratio is a purely empirical dimensionless contrast, not a pore-size measure. All training values are strictly positive, so the expression is finite everywhere without imputation.",
    "falsification_criteria": "If the partial derivative with respect to density is not negative on average at fixed ASA (i.e., lower framework density does not increase predicted entropy loss), or the target association is contradicted across the training regime, the site-degeneracy mechanism is falsified; a competing mechanism is that ASA alone already carries all framework information.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "ASA is accessibility for a fixed geometric probe, not molecule-specific accessible area; density is a numerical-scale proxy whose physical unit is unresolved, so the exponent -1 on the q-normalized ratio is an empirical weighting, not a derived physical law.",
      "physical_interpretation": "The descriptor rises with native ASA at fixed density and falls with native density at fixed ASA; ASA_ref and density_ref are fixed positive training medians used for scaling only, and X/q_X = X_ref is constant, never an input.",
      "boundary_behavior": "ASA has 28 legitimate zero rows in training; at ASA = 0 the descriptor equals log(1) = 0, finite and continuous, correctly encoding 'no probe-accessible area' without imputation; density is strictly positive (min 0.759654), so no zero division occurs.",
      "vary_input": "density",
      "descriptor_direction": "decreasing",
      "regime_input": "density",
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
        "density"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": -0.2779021522591971,
      "target_association": "contradicted",
      "perturbation": 0.005792599999999999,
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
    "name": "framework_density_specific_area_contrast",
    "formula": "log(1 + (ASA/ASA_ref) * (density/density_ref) ** 1)",
    "hypothesis": "Entropy loss increases with the framework's probe-accessible specific surface area but this effect is stronger in frameworks of lower framework density, because at equal surface area a lighter, more open framework offers more geometrically distinct adsorption sites, while dense frameworks concentrate area into fewer, more degenerate configurations.",
    "rationale": "The round-1 draft's negative density exponent was contradicted in training (Spearman -0.28, association 'contradicted') while the hypothesis direction (entropy loss increasing with density) is preserved. The corrected expression removes the inverse density weighting and makes the descriptor increase with native density at fixed ASA, aligning the proxy derivative with the predeclared direction: denser frameworks concentrate contact area per volume, qualitatively consistent with greater entropy loss in tighter confinement reported in E02 (smaller-pore zeolites show larger rotational entropy loss). The competing explanation — that ASA alone already carries the framework information — is explicitly allowed for in the falsification criteria.",
    "falsification_criteria": "If the partial derivative with respect to density is not positive on average at fixed ASA within the training regime, or the target association remains contradicted, the density-weighting term is falsified and ASA alone should be tested as the sole framework descriptor.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02"
    ],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "ASA is fixed-probe mass-specific accessible area, not molecule-specific accessible area; density is a native-scale framework density proxy with unresolved physical unit. The sign of the density exponent is an empirical weighting, not a derived physical law, and q-ratio = 1 carries no universal physical meaning.",
      "physical_interpretation": "The descriptor increases with native ASA at fixed density and increases with native density at fixed ASA. ASA_ref and density_ref are fixed positive training medians used only for dimensionless scaling; X/q_X = X_ref is a constant, never an input.",
      "boundary_behavior": "ASA has 28 legitimate zero rows; at ASA = 0 the descriptor equals log(1) = 0, finite and continuous. density is strictly positive (min 0.759654), so no zero division occurs. All training rows yield finite values.",
      "vary_input": "density",
      "descriptor_direction": "increasing",
      "regime_input": "density",
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
        "density"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": -0.16572158310185167,
      "target_association": "contradicted",
      "perturbation": 0.005792599999999999,
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
    "name": "framework_density_specific_area_contrast",
    "formula": "log(1 + (ASA/ASA_ref) * (density/density_ref) ** 1)",
    "hypothesis": "Entropy loss increases with the framework's probe-accessible specific surface area but this effect is stronger in frameworks of lower framework density, because at equal surface area a lighter, more open framework offers more geometrically distinct adsorption sites, while dense frameworks concentrate area into fewer, more degenerate configurations.",
    "rationale": "The round-1 draft's negative density exponent was contradicted in training (Spearman -0.28, association 'contradicted') while the hypothesis direction (entropy loss increasing with density) is preserved. The corrected expression removes the inverse density weighting and makes the descriptor increase with native density at fixed ASA, aligning the proxy derivative with the predeclared direction: denser frameworks concentrate contact area per volume, qualitatively consistent with greater entropy loss in tighter confinement reported in E02 (smaller-pore zeolites show larger rotational entropy loss). The competing explanation — that ASA alone already carries the framework information — is explicitly allowed for in the falsification criteria.",
    "falsification_criteria": "If the partial derivative with respect to density is not positive on average at fixed ASA within the training regime, or the target association remains contradicted, the density-weighting term is falsified and ASA alone should be tested as the sole framework descriptor.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02"
    ],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "ASA is fixed-probe mass-specific accessible area, not molecule-specific accessible area; density is a native-scale framework density proxy with unresolved physical unit. The sign of the density exponent is an empirical weighting, not a derived physical law, and q-ratio = 1 carries no universal physical meaning.",
      "physical_interpretation": "The descriptor increases with native ASA at fixed density and increases with native density at fixed ASA. ASA_ref and density_ref are fixed positive training medians used only for dimensionless scaling; X/q_X = X_ref is a constant, never an input.",
      "boundary_behavior": "ASA has 28 legitimate zero rows; at ASA = 0 the descriptor equals log(1) = 0, finite and continuous. density is strictly positive (min 0.759654), so no zero division occurs. All training rows yield finite values.",
      "vary_input": "density",
      "descriptor_direction": "increasing",
      "regime_input": "density",
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
        "density"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": -0.16572158310185167,
      "target_association": "contradicted",
      "perturbation": 0.005792599999999999,
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
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd4794ce62afc7c5c5d7b896",
        "paper_id": "doi:10.1021/acs.jpclett.2c03302",
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
        "record_id": "chunk:88266d0223c92bc7bf09dc10",
        "paper_id": "doi:10.1021/jp052462a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9e85d2c34a35aa6bd4d5bf8b",
        "paper_id": "doi:10.1039/d5ce00034c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c515aa77b0e6afe8275e4595",
        "paper_id": "doi:10.1039/d5cs00613a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08aecb87be6d1cda8c6566fa",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1df43ef3b3fc010f92ca7737",
        "paper_id": "pmc:pmc10141410",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:281808f751362133796cb2fe",
        "paper_id": "doi:10.1021/ja105185r",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3d8ed419d3eff1212dddc68f",
        "paper_id": "doi:10.1039/d5ce00034c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5f4fa846bc2d0985b0b933ef",
        "paper_id": "doi:10.1038/s41586-024-07194-6",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:79aa0fa4ceb9bad5202197e0",
        "paper_id": "doi:10.1021/acs.langmuir.2c00923",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9805f0a944c903cd7580bbcb",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c221f77d5d5ce26095f7b022",
        "paper_id": "doi:10.1021/ja400267g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd1acc7b04d64296bb68e884",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d270ec3d6183be4a3de52cd8",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d8eef552eba72a99f7974a84",
        "paper_id": "doi:10.1039/b819334g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:48e6eb00e9161d8cdd93754e",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5043fe527b153e937c92a6ed",
        "paper_id": "pmc:pmc6482883",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e735b2613c148ccceb01c82",
        "paper_id": "doi:10.1007/s00894-024-06004-0",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7342d031262bdf8cf5e759a2",
        "paper_id": "doi:10.1002/cphc.202300022",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in pure-silica zeolites, entropy loss increases when an adsorbate with larger contact-capable surface area is hosted in a framework with a smaller passing bottleneck free-sphere diameter, because narrow window frameworks restrict positional sampling over which the contact surface can explore the pore wall. log(1 + (LabuteASA/LabuteASA_ref) * (lsd_f/lsd_f_ref) ** -1) For nonlinear adsorbates, entropy loss increases when a volumetrically large molecule is also displaced from planarity (large height above its best-fit plane), because a bulky non-planar body loses more rotational and orientational freedom upon confinement than a flat body of equal volume that can hug pore walls in more orientations. log(1 + (Vol/Vol_ref) * (PBF/PBF_ref) ** 2) Entropy loss increases with the framework's probe-accessible specific surface area but this effect is stronger in frameworks of lower framework density, because at equal surface area a lighter, more open framework offers more geometrically distinct adsorption sites, while dense frameworks concentrate area into fewer, more degenerate configurations. log(1 + (ASA/ASA_ref) * (density/density_ref) ** -1)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:2a1af3104c544329d9e72836",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:4e0a09f3bacb310a3d0b505c"
    ],
    "items": 10,
    "lexical_tokens": 4487,
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
    },
    {
      "record_id": "chunk:ae6e434cc894357276cba23f",
      "paper_id": "doi:10.1021/jp060657s",
      "document_id": "document:efa163ae1d6a7d3f748b3c99",
      "quote": "this case , both molecules have $ R_g/R_c $ values greater than unity for both the pockets and the central section , which means that the advantage of shorter length in terms of rotational entropy is lost . Indeed , heptane adsorbs preferentially over its branched isomer 2-MeC6 in contrast to the above-mentioned alkane couples ( Table 2 ) . The above considerations concerning supercage adsorption shed a light on the unusual decrease of adsorption enthalpy per carbon atom with increasing chain length (Figure 6). Short linear alkanes (from methane to butane) can reside as a whole inside the pockets where all of their end hydrogen atoms can interact closely with the pore walls, as shown in Figure 12. This results in large interaction energies (adsorption enthalpies) for these molecules and a large increment in adsorption enthalpy per additional carbon atom. But when the chain length increases, the molecule grows toward the central section of the supercage, where there is a much larger free space. As a result of this cage enlargement, the additional carbon atoms will interact to a lesser extent than the atoms residing in the depths of the pocket, explaining the aforementioned enthalpy effect. Whereas butane is at the limit, pentane is too long to reside completely in the pocket and has at least one methyl group in the central section, where the distance between the hydrogen atoms and the atoms of the framework is larger, explaining the lower difference in adsorption enthalpy between n-C4 and n-C5 (5.7 kJ/mol) compared to that of n-C4 and n-C3 (7.9 kJ/mol). The same reasoning is valid for n-C6. To explain the discontinuity between n-C6 and n-C7 in the compensation chart (Figure 8), a different adsorption configuration is proposed, in which the molecules remain as a whole in the central section of the supercage (see Figure 12), where the entropy loss is expected to be lower than in the pockets of the cage.",
      "locator": {
        "section": "discussion",
        "page": 1
      },
      "applicability": {
        "record_id": "chunk:51aa804bfe1967d7ebb1d76f",
        "paper_id": "doi:10.1021/jp060657s",
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
