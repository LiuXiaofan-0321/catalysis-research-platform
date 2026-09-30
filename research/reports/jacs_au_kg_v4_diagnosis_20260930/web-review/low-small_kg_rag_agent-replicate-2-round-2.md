# low/small_kg_rag_agent/replicate-2/round-2

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
  }
]
```

## h1

候选标识：`low/small_kg_rag_agent/replicate-2/round-2/h1`

最终状态：scored；边际收益：+0.299432 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "included_path_confinement",
    "formula": "log(1 + (Vol/Vol_ref) * (lsd_p/lsd_p_ref) ** -2)",
    "hypothesis": "At infinite dilution in pure-silica zeolites, entropy loss increases when a volumetrically larger adsorbate is hosted in frameworks with a smaller included free-sphere diameter along the diffusion path, because stronger host-guest confinement suppresses translational and orientational freedom; the included diameter (lsd_p) characterizes the confining channel/cage wall along the free path, unlike the bottleneck diameter (lsd_f) which only gates passage.",
    "rationale": "Uses lsd_p as a confinement-scale proxy rather than a passage gate; the Vol product expresses that confinement entropy penalty scales with the amount of molecular volume being constrained. Round-1 evidence showed size gating by lsd_f gave a contradicted association, so this candidate swaps the gate for the included-diameter proxy and predicts the opposite dependence direction on the framework term. This is an empirical proxy hypothesis, not a validated causal mechanism.",
    "falsification_criteria": "If training Spearman between the descriptor and entropy loss is negative or the sign of the d(descriptor)/d(lsd_p) partial at fixed rotor class and fixed Vol implies entropy loss decreases with decreasing lsd_p, the confinement hypothesis is falsified for this descriptor; a competing mechanism would be that AV (probe-accessible volume) rather than lsd_p drives framework entropy effects.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
      "proxy_assumptions": "lsd_p (Zeo++ Dif) is a geometric confinement proxy along the free-sphere path, not the global cavity diameter; Vol is a van der Waals volume proxy not resolved by atom type; both ignore framework chemistry beyond geometry.",
      "physical_interpretation": "Vol/Vol_ref and lsd_p/lsd_p_ref are dimensionless ratios to fixed training-reference medians; the constant 1 inside log keeps the argument dimensionless and positive; no unity threshold is claimed.",
      "boundary_behavior": "Finite for all training rows: Vol>0 and lsd_p>0 everywhere in-domain; lsd_pRef is a positive constant so the negative exponent never divides by a zero variable. As lsd_p grows the descriptor approaches 0 (no confinement penalty); as Vol grows it grows logarithmically.",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
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
      "training_spearman": 0.7498133917485073,
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
      "training_spearman": 0.7498133917485073,
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
      "training_spearman": 0.7498133917485073,
      "target_association": "consistent",
      "perturbation": 0.0452717,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/small_kg_rag_agent/replicate-2/round-2/h2`

最终状态：scored；边际收益：-0.132233 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "elongation_translational_suppression",
    "formula": "log(1 + (GeDi/GeDi_ref) * (LabuteASA/LabuteASA_ref) / (1 + (PBF/PBF_ref)))",
    "hypothesis": "Entropy loss increases with the heavy-atom maximum extent (GeDi) of the adsorbate relative to the heavy-atom planarity proxy (PBF): elongated, extended molecules lose more configurational entropy upon adsorption than compact or planar ones of equal surface area, because an elongated shape restricts orientational sampling in pores even when planarity offers some rotational freedom.",
    "rationale": "GeDi is the largest heavy-atom pair distance (shape elongation proxy); dividing by (1 + PBF/PBF_ref) lets near-planar molecules (legitimate PBF near zero, 587 training rows) retain a finite descriptor while nonplanar, more three-dimensionally extended molecules score higher at equal area. LabuteASA carries the contact-area entropy mechanism retained in round 1 (h3 was the only retained candidate, Spearman 0.65, association consistent). This is an empirical proxy combination, not a validated causal relation.",
    "falsification_criteria": "If the training Spearman is inconsistent with increasing entropy loss, or if the partial derivative with respect to GeDi at fixed rotor class and fixed LabuteASA is not positive, the elongation mechanism is falsified; a competing mechanism is that volumetric compactness (Vol) rather than linear extent controls orientational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "LabuteASA": "adsorbate_geometry_proxy",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi, LabuteASA, and PBF are computed in the original implicit-H/heavy-atom representation; they are not true all-atom geometry; legitimate zeros in PBF are treated via the additive 1 so no division by zero occurs.",
      "physical_interpretation": "All ratios are to fixed positive training-reference medians; the additive constants 1 are numerical smoothing devices carrying no universal physical meaning; the log argument is dimensionless and strictly positive for every training row.",
      "boundary_behavior": "At PBF=0 (planar molecules, 587 rows) the descriptor reduces to log(1 + q_GeDi*q_LabuteASA), finite and positive; single-site molecules (54 rows) may have legitimate zero heavy-atom proxies, and the +1 terms keep the descriptor finite there as well, reflecting that a single-site species has minimal shape-driven entropy loss.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
      "regime_input": "GeDi",
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
        "GeDi",
        "LabuteASA",
        "PBF"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.32608647456781037,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
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
    "name": "elongation_translational_suppression",
    "formula": "log(1 + (GeDi/GeDi_ref) * (LabuteASA/LabuteASA_ref) / (1 + (PBF/PBF_ref)))",
    "hypothesis": "Entropy loss increases with the heavy-atom maximum extent (GeDi) of the adsorbate relative to the heavy-atom planarity proxy (PBF): elongated, extended molecules lose more configurational entropy upon adsorption than compact or planar ones of equal surface area, because an elongated shape restricts orientational sampling in pores even when planarity offers some rotational freedom.",
    "rationale": "GeDi (largest heavy-atom pair distance) proxies linear extent; LabuteASA retains the contact-area entropy association retained in round 1 (Spearman 0.65, consistent). Dividing by (1 + q_PBF) is an empirical smoothing so legitimate PBF zeros (587 rows) remain finite; source E06 qualitatively links molecular size/shape (radius of gyration) to retained rotational freedom in cages, conditionally supporting a shape dependence. All quantities are original implicit-H/heavy-atom proxies, not all-atom geometry. Empirical proxy combination, not a validated causal relation.",
    "falsification_criteria": "If training Spearman is inconsistent with increasing entropy loss, or the partial d(descriptor)/d(GeDi) at fixed rotor class and fixed LabuteASA is not positive, the elongation mechanism is falsified; competing mechanism: volumetric compactness (Vol) rather than linear extent controls orientational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "LabuteASA": "adsorbate_geometry_proxy",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi, LabuteASA, PBF computed in the original implicit-H/heavy-atom representation; legitimate zeros exist (PBF=0 for 587 rows; GeDi=0 for 54 single-site rows). Source support (E06) is cage-specific (MCM-22 supercages) and does not establish the relation across all frameworks.",
      "physical_interpretation": "q_GeDi, q_LabuteASA, q_PBF are row-varying dimensionless ratios to fixed positive training-reference medians; the additive 1s are numerical smoothing devices with no universal physical meaning; the log argument is dimensionless and strictly positive for every training row.",
      "boundary_behavior": "At PBF=0 the descriptor reduces to log(1 + q_GeDi*q_LabuteASA), finite and positive; at GeDi=0 (single-site rows) the descriptor reduces to log(1 + q_LabuteASA/(1+q_PBF)), finite. No division by a legitimate zero occurs.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
      "regime_input": "GeDi",
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
        "GeDi",
        "LabuteASA",
        "PBF"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.32608647456781037,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
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
    "name": "elongation_translational_suppression",
    "formula": "log(1 + (GeDi/GeDi_ref) * (LabuteASA/LabuteASA_ref) / (1 + (PBF/PBF_ref)))",
    "hypothesis": "Entropy loss increases with the heavy-atom maximum extent (GeDi) of the adsorbate relative to the heavy-atom planarity proxy (PBF): elongated, extended molecules lose more configurational entropy upon adsorption than compact or planar ones of equal surface area, because an elongated shape restricts orientational sampling in pores even when planarity offers some rotational freedom.",
    "rationale": "GeDi (largest heavy-atom pair distance) proxies linear extent; LabuteASA retains the contact-area entropy association retained in round 1 (Spearman 0.65, consistent). Dividing by (1 + q_PBF) is an empirical smoothing so legitimate PBF zeros (587 rows) remain finite; source E06 qualitatively links molecular size/shape (radius of gyration) to retained rotational freedom in cages, conditionally supporting a shape dependence. All quantities are original implicit-H/heavy-atom proxies, not all-atom geometry. Empirical proxy combination, not a validated causal relation.",
    "falsification_criteria": "If training Spearman is inconsistent with increasing entropy loss, or the partial d(descriptor)/d(GeDi) at fixed rotor class and fixed LabuteASA is not positive, the elongation mechanism is falsified; competing mechanism: volumetric compactness (Vol) rather than linear extent controls orientational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "LabuteASA": "adsorbate_geometry_proxy",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi, LabuteASA, PBF computed in the original implicit-H/heavy-atom representation; legitimate zeros exist (PBF=0 for 587 rows; GeDi=0 for 54 single-site rows). Source support (E06) is cage-specific (MCM-22 supercages) and does not establish the relation across all frameworks.",
      "physical_interpretation": "q_GeDi, q_LabuteASA, q_PBF are row-varying dimensionless ratios to fixed positive training-reference medians; the additive 1s are numerical smoothing devices with no universal physical meaning; the log argument is dimensionless and strictly positive for every training row.",
      "boundary_behavior": "At PBF=0 the descriptor reduces to log(1 + q_GeDi*q_LabuteASA), finite and positive; at GeDi=0 (single-site rows) the descriptor reduces to log(1 + q_LabuteASA/(1+q_PBF)), finite. No division by a legitimate zero occurs.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
      "regime_input": "GeDi",
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
        "GeDi",
        "LabuteASA",
        "PBF"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "LabuteASA": "adsorbate_geometry_proxy",
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.32608647456781037,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/small_kg_rag_agent/replicate-2/round-2/h3`

最终状态：scored；边际收益：-2.503443 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "rotor_class_weighted_inertia_area",
    "formula": "rotor_case(log(1 + (LabuteASA/LabuteASA_ref)), log(1 + (PMI2/PMI2_ref) * (LabuteASA/LabuteASA_ref) ** -1), log(1 + (PMI3/PMI3_ref) * (LabuteASA/LabuteASA_ref) ** -1))",
    "hypothesis": "Rotational entropy loss upon adsorption is rotor-class dependent: single-site species lose entropy mainly through contact area; linear rotors lose rotational freedom in proportion to their intermediate-to-small inertia ratio (PMI2, the free rotation axis of a linear molecule scaled by contact area); nonlinear rotors lose rotational freedom through their largest inertia (PMI3) relative to contact area, since all three rotational degrees of freedom are hindered by the pore wall.",
    "rationale": "PMI1, PMI2, PMI3 are heavy-atom principal moments in the original implicit-H representation; legitimate zeros (113 rows with PMI1=0, 54 single-site rows) are handled by the additive 1 inside log so every branch is finite without imputation. The area-normalized inertia expresses rotational hindrance per unit of retained contact entropy. Round-1 diagnostics fixed the rotor class during partial derivatives, so class-branching is decorrelated from the within-branch derivative test. This is an empirical proxy hypothesis; the branch structure is an empirical smoothing choice, not a universal rotor law.",
    "falsification_criteria": "If the training Spearman within any rotor class branch is inconsistent with increasing entropy loss, or if the partial derivative with respect to the branch's native inertia input at fixed rotor class is non-positive, that branch's rotational-hindrance mechanism is falsified; a competing mechanism is that rotational entropy loss is governed by molecular volume rather than inertia-to-area ratio.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI values are heavy-atom proxies, not true all-atom inertias; single-site molecules (e.g., methane) are classified by the rotor_case tolerance, and their branch uses only LabuteASA; inertia-to-area ratios are assumed transferable across frameworks, which the framework inputs in this descriptor do not capture.",
      "physical_interpretation": "Each branch output is dimensionless via ratios to fixed positive training-reference medians plus additive 1 inside log; q-normalized or ref-ratio inputs are row-varying dimensionless inputs, and no q-unity physical threshold is asserted.",
      "boundary_behavior": "Single-site branch: log(1 + q_LabuteASA), finite for all rows since LabuteASA>0 in-domain. Linear branch: PMI2 can be legitimately near zero for symmetric linear species; the additive 1 keeps the descriptor finite and near zero, correctly implying minimal inertia-driven rotational loss. Nonlinear branch analogous with PMI3. No division by a variable that can be zero occurs because the area term appears only in a denominator inside a ratio that is itself added to 1 in log form.",
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
        "LabuteASA",
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.40474638075076336,
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
    "slot_id": "h3",
    "name": "rotor_class_weighted_inertia_area",
    "formula": "rotor_case(log(1 + (LabuteASA/LabuteASA_ref)), log(1 + (PMI2/PMI2_ref) * (LabuteASA/LabuteASA_ref) ** -1), log(1 + (PMI3/PMI3_ref) * (LabuteASA/LabuteASA_ref) ** -1))",
    "hypothesis": "Rotational entropy loss upon adsorption is rotor-class dependent: single-site species lose entropy mainly through contact area; linear rotors lose rotational freedom in proportion to their intermediate-to-small inertia ratio (PMI2, the free rotation axis of a linear molecule scaled by contact area); nonlinear rotors lose rotational freedom through their largest inertia (PMI3) relative to contact area, since all three rotational degrees of freedom are hindered by the pore wall.",
    "rationale": "Rotational entropy loss is rotor-class dependent: single-site species via contact area; linear rotors via transverse inertia (PMI2) per unit area; nonlinear rotors via largest inertia (PMI3) per unit area. Conditionally supported by reported larger rotational entropy loss in more confining frameworks (E01) and cage-shape dependence of rotational freedom (E06); E09 warns that implicit-H models change symmetry numbers and principal moments, limiting transferability. The branch structure is an empirical smoothing choice, not a universal rotor law.",
    "falsification_criteria": "If training Spearman within any rotor-class branch is inconsistent with increasing entropy loss, or the partial derivative with respect to the branch's inertia input (PMI2 for linear, PMI3 for nonlinear) at fixed rotor class and fixed LabuteASA is non-positive, that branch's mechanism is falsified; competing mechanism: rotational entropy loss governed by molecular volume (Vol) rather than inertia-to-area ratio.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E06",
      "E09"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom principal moments in the original implicit-H representation, not true all-atom inertias (E09 notes implicit-H pseudo-atoms alter principal moments); legitimate zeros (113 rows PMI1=0, 54 single-site rows) are handled by additive 1 inside log. For linear rotors PMI1 is the near-zero moment about the molecular axis and PMI2 is a transverse moment (PMI2=PMI3 by symmetry for ideal linear species); the linear branch uses PMI2 as the hindered transverse rotation proxy. Rotor classification follows the native rotor_case tolerance.",
      "physical_interpretation": "Each branch is dimensionless via ratios to fixed positive training-reference medians plus additive 1 inside log; the area exponent -1 is applied to q_LabuteASA (strictly positive in-domain), so no division by zero occurs; no q-unity physical threshold is asserted.",
      "boundary_behavior": "Single-site branch: log(1 + q_LabuteASA), finite for all rows since LabuteASA>0 in-domain. Linear branch: PMI2 can be legitimately near zero; the additive 1 keeps the descriptor finite and near zero. Nonlinear branch analogous with PMI3. Every training row yields a finite value in exactly one branch.",
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
        "LabuteASA",
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.40474638075076336,
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
    "slot_id": "h3",
    "name": "rotor_class_weighted_inertia_area",
    "formula": "rotor_case(log(1 + (LabuteASA/LabuteASA_ref)), log(1 + (PMI2/PMI2_ref) * (LabuteASA/LabuteASA_ref) ** -1), log(1 + (PMI3/PMI3_ref) * (LabuteASA/LabuteASA_ref) ** -1))",
    "hypothesis": "Rotational entropy loss upon adsorption is rotor-class dependent: single-site species lose entropy mainly through contact area; linear rotors lose rotational freedom in proportion to their intermediate-to-small inertia ratio (PMI2, the free rotation axis of a linear molecule scaled by contact area); nonlinear rotors lose rotational freedom through their largest inertia (PMI3) relative to contact area, since all three rotational degrees of freedom are hindered by the pore wall.",
    "rationale": "Rotational entropy loss is rotor-class dependent: single-site species via contact area; linear rotors via transverse inertia (PMI2) per unit area; nonlinear rotors via largest inertia (PMI3) per unit area. Conditionally supported by reported larger rotational entropy loss in more confining frameworks (E01) and cage-shape dependence of rotational freedom (E06); E09 warns that implicit-H models change symmetry numbers and principal moments, limiting transferability. The branch structure is an empirical smoothing choice, not a universal rotor law.",
    "falsification_criteria": "If training Spearman within any rotor-class branch is inconsistent with increasing entropy loss, or the partial derivative with respect to the branch's inertia input (PMI2 for linear, PMI3 for nonlinear) at fixed rotor class and fixed LabuteASA is non-positive, that branch's mechanism is falsified; competing mechanism: rotational entropy loss governed by molecular volume (Vol) rather than inertia-to-area ratio.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E06",
      "E09"
    ],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom principal moments in the original implicit-H representation, not true all-atom inertias (E09 notes implicit-H pseudo-atoms alter principal moments); legitimate zeros (113 rows PMI1=0, 54 single-site rows) are handled by additive 1 inside log. For linear rotors PMI1 is the near-zero moment about the molecular axis and PMI2 is a transverse moment (PMI2=PMI3 by symmetry for ideal linear species); the linear branch uses PMI2 as the hindered transverse rotation proxy. Rotor classification follows the native rotor_case tolerance.",
      "physical_interpretation": "Each branch is dimensionless via ratios to fixed positive training-reference medians plus additive 1 inside log; the area exponent -1 is applied to q_LabuteASA (strictly positive in-domain), so no division by zero occurs; no q-unity physical threshold is asserted.",
      "boundary_behavior": "Single-site branch: log(1 + q_LabuteASA), finite for all rows since LabuteASA>0 in-domain. Linear branch: PMI2 can be legitimately near zero; the additive 1 keeps the descriptor finite and near zero. Nonlinear branch analogous with PMI3. Every training row yields a finite value in exactly one branch.",
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
        "LabuteASA",
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.40474638075076336,
      "target_association": "consistent",
      "perturbation": 4.425680816,
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
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
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
        "record_id": "chunk:869af4527dd765744b7ebc76",
        "paper_id": "pmc:pmc8659101",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd4794ce62afc7c5c5d7b896",
        "paper_id": "doi:10.1021/acs.jpclett.2c03302",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c1b6ac162c7c9a1d0db4fb1d",
        "paper_id": "doi:10.1021/ja101614w",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:147fa339122edc3ff44ba658",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:304ba9cab14ca17db59c3774",
        "paper_id": "doi:10.1021/ja209832y",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:472c89f72d857bbcf16ff16e",
        "paper_id": "doi:10.1002/asia.202400973",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:4be89b7d54bb527e95cbfda0",
        "paper_id": "doi:10.1039/c5cp04265h",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5d62cd81d1c76b19dcdcfff9",
        "paper_id": "doi:10.1021/acs.langmuir.2c00923",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
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
        "record_id": "chunk:7cb746b40fc95fee791061d4",
        "paper_id": "doi:10.1021/acsnano.6b02856",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:97cb91ac45ab76508e37525b",
        "paper_id": "doi:10.1002/anie.201904825",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c21efedd90985975547b696b",
        "paper_id": "doi:10.1063/1.3367894",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c515aa77b0e6afe8275e4595",
        "paper_id": "doi:10.1039/d5cs00613a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ce288b499ad7b4dd216da362",
        "paper_id": "doi:10.1038/nmat1213",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in pure-silica zeolites, entropy loss increases when a volumetrically larger adsorbate is hosted in frameworks with a smaller included free-sphere diameter along the diffusion path, because stronger host-guest confinement suppresses translational and orientational freedom; the included diameter (lsd_p) characterizes the confining channel/cage wall along the free path, unlike the bottleneck diameter (lsd_f) which only gates passage. log(1 + (Vol/Vol_ref) * (lsd_p/lsd_p_ref) ** -2) Entropy loss increases with the heavy-atom maximum extent (GeDi) of the adsorbate relative to the heavy-atom planarity proxy (PBF): elongated, extended molecules lose more configurational entropy upon adsorption than compact or planar ones of equal surface area, because an elongated shape restricts orientational sampling in pores even when planarity offers some rotational freedom. log(1 + (GeDi/GeDi_ref) * (LabuteASA/LabuteASA_ref) / (1 + (PBF/PBF_ref))) Rotational entropy loss upon adsorption is rotor-class dependent: single-site species lose entropy mainly through contact area; linear rotors lose rotational freedom in proportion to their intermediate-to-small inertia ratio (PMI2, the free rotation axis of a linear molecule scaled by contact area); nonlinear rotors lose rotational freedom through their largest inertia (PMI3) relative to contact area, since all three rotational degrees of freedom are hindered by the pore wall. rotor_case(log(1 + (LabuteASA/LabuteASA_ref)), log(1 + (PMI2/PMI2_ref) * (LabuteASA/LabuteASA_ref) ** -1), log(1 + (PMI3/PMI3_ref) * (LabuteASA/LabuteASA_ref) ** -1))   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e98dff054a73e56b28f6bdf3",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:8ffcc4698d37d4f5569d53f5"
    ],
    "items": 10,
    "lexical_tokens": 4862,
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
      "record_id": "chunk:4e0a09f3bacb310a3d0b505c",
      "paper_id": "doi:10.1021/acs.jpcc.0c02671",
      "document_id": "document:679638c993b24ed3004656c6",
      "quote": "gas-phase entropy , i.e . , $ 0 < \\ eta _ { i } < 1 $ . The $ R ^ { 2 } $ correlation coefficients , except for that of FAU , are close to unity , indicating low deviation from the linear trend lines ; the notable deviations for FAU will be discussed later . Linearity in the correlation of $ s_{ads}^{\\infty} $ with $ s_{gas}^{0} $ is the key feature of the results in Figure 1, as it corresponds to qualitatively similar observations in the entropy correlations disclosed in refs 13, 31, and 27. More importantly, though, our results show that the apparent linearity in the correlation of $ s_{ads}^{\\infty} $ with $ s_{gas}^{0} $ persists for a larger set of chemically diverse adsorbates than was previously seen. As discussed in those references, such a simple correlation is an obvious opportunity for the development of an engineering correlation that allows for prediction of the adsorption entropy from a limited set of measurements (whether experimentally or computationally derived). Furthermore, we aim to build on the conclusions in refs 13, 31, and 27 by examining our own data in light of the physical arguments presented previously. As a brief review, the apparent linearity in adsorption entropy correlations derives from fundamental physical considerations. In ref 27, where their linear trend in the entropy correlations was approximately two-third, the authors offered a simplified explanation that the linear trend reflected a loss of approximately one-third of the translational and rotational entropies owing to adsorption. Dauenhauer and Abdelrahman $ ^{13} $ extended this argument to acidic zeolites by considering an additional loss of rotational entropy dependent on the adsorbate size and the pore volume. (Pure linear correlation of $ s_{ads}^{\\infty} $ with $ s_{gas}^{0} $ is broken by the arguments in ref 13, but a visual linear correlation persists. We return to this point later in our work.) Before proceeding, we also note that a numerical comparison between our entropy values and those of ref 13 must be done with care; the gas-phase rotational and translational entropies (i.e., the x-axis of Figure 1) of our TraPPE-model molecules differ from experimental values. This is because the TraPPE molecules include pseudo-atoms, which represent hydrogens implicitly. Although the mass of the TraPPE-model molecules does not change, the symmetry number and principal moments of inertia within the rotational entropy equation are different.",
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
      "id": "E09"
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
