# low/small_kg_rag_agent/replicate-2/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/small_kg_rag_agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`low/small_kg_rag_agent/replicate-2/round-1/h1`

最终状态：scored；边际收益：-3.689465 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "size_gated_configurational_retention",
    "formula": "log((Vol/Vol_ref) ** 2 * (lsd_f/lsd_f_ref))",
    "hypothesis": "At infinite dilution in pure-silica zeolites, the ratio of adsorbed to gas-phase entropy loss grows when adsorbate volume relative to the framework passing bottleneck shrinks, because small molecules relative to Df retain more translational/configurational freedom in the pore; thus entropy loss decreases with increasing lsd_f and increases with molecular Vol.",
    "rationale": "Volume-vs-bottleneck contrast is a shape/connectivity mechanism: a bulky molecule confined by a narrow Df loses more translational entropy than a compact one in an open channel. The descriptor is a dimensionless log product of two q-normalized ratios, so it is finite for all training rows (Vol, lsd_f have no zeros). It is an empirical proxy combination, not a free-energy relation; the exponent 2 encodes an assumed stronger-than-linear confinement effect and carries no universal physical meaning.",
    "falsification_criteria": "If measured entropy loss does not decrease with lsd_f/lsd_f_ref at fixed Vol within a fixed framework topology family (e.g., MFI with varied adsorbates), or if Vol alone at fixed bottleneck explains the correlation equally well, the confinement-contrast mechanism is refuted in favor of a pure size effect.",
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
      "mechanism_family": "coupling",
      "proxy_assumptions": "Van der Waals volume is a proxy for excluded translational volume; Df is a passing-bottleneck proxy, not global cavity diameter Di, so pore interiors wider than Df are not resolved. Fixed-probe AV is deliberately not used since it is not molecule-specific free volume.",
      "physical_interpretation": "Vol/Vol_ref scales excluded volume; lsd_f/lsd_f_ref scales confinement severity. Both are dimensionless row-varying inputs; no q-unity threshold is asserted.",
      "boundary_behavior": "Vol and lsd_f are strictly positive over the training domain, so the expression is finite everywhere; no zero-branch needed. The log stays within a bounded range for the given quantiles.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
      "regime_input": "Vol",
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
        "Vol",
        "lsd_f"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 2361,
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
    "slot_id": "h1",
    "name": "size_gated_configurational_retention",
    "formula": "log((Vol/Vol_ref) ** 2 / (lsd_f/lsd_f_ref))",
    "hypothesis": "At infinite dilution in pure-silica zeolites, the ratio of adsorbed to gas-phase entropy loss grows when adsorbate volume relative to the framework passing bottleneck shrinks, because small molecules relative to Df retain more translational/configurational freedom in the pore; thus entropy loss decreases with increasing lsd_f and increases with molecular Vol.",
    "rationale": "Corrected the sign of the bottleneck contrast: the draft formula increased with lsd_f, contradicting the predeclared decreasing descriptor direction and the predeclared entropy direction. Dividing by lsd_f/lsd_f_ref makes the descriptor decrease with the passing bottleneck (larger free-sphere path, less confinement severity, less entropy loss) and increase with molecular Vol, consistent with the volume-vs-bottleneck confinement-contrast mechanism (E04: larger-pore FAU shows smaller fractional entropy loss than MFI). Both Vol and lsd_f are strictly positive over the training domain, so the expression is finite for every training row. The exponent 2 and all q-ratios are empirical proxy combinations with no universal physical meaning; lsd_f is a bottleneck (Df) proxy, not global cavity diameter Di, so pore interiors wider than Df are unresolved.",
    "falsification_criteria": "If measured entropy loss does not decrease with lsd_f/lsd_f_ref at fixed Vol within a fixed framework topology family, or if Vol alone at fixed bottleneck explains the correlation equally well, the confinement-contrast mechanism is refuted in favor of a pure size effect.",
    "novelty_status": "new_combination",
    "evidence_ids": [
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
      "mechanism_family": "coupling",
      "proxy_assumptions": "Vol proxies excluded translational volume; lsd_f (Zeo++ Df) proxies the passing bottleneck, not global cavity diameter Di; fixed-probe AV is deliberately not used since it is not molecule-specific free volume.",
      "physical_interpretation": "Vol/Vol_ref scales excluded volume; lsd_f/lsd_f_ref scales confinement severity; both are dimensionless row-varying inputs and no q-unity threshold is asserted.",
      "boundary_behavior": "Vol (20.424–161.144) and lsd_f (0.85684–7.68726) are strictly positive on training; the log argument is positive and finite everywhere; no zero branch needed.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
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
      "training_spearman": 0.5357155930050844,
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
    "name": "size_gated_configurational_retention",
    "formula": "log((Vol/Vol_ref) ** 2 / (lsd_f/lsd_f_ref))",
    "hypothesis": "At infinite dilution in pure-silica zeolites, the ratio of adsorbed to gas-phase entropy loss grows when adsorbate volume relative to the framework passing bottleneck shrinks, because small molecules relative to Df retain more translational/configurational freedom in the pore; thus entropy loss decreases with increasing lsd_f and increases with molecular Vol.",
    "rationale": "Corrected the sign of the bottleneck contrast: the draft formula increased with lsd_f, contradicting the predeclared decreasing descriptor direction and the predeclared entropy direction. Dividing by lsd_f/lsd_f_ref makes the descriptor decrease with the passing bottleneck (larger free-sphere path, less confinement severity, less entropy loss) and increase with molecular Vol, consistent with the volume-vs-bottleneck confinement-contrast mechanism (E04: larger-pore FAU shows smaller fractional entropy loss than MFI). Both Vol and lsd_f are strictly positive over the training domain, so the expression is finite for every training row. The exponent 2 and all q-ratios are empirical proxy combinations with no universal physical meaning; lsd_f is a bottleneck (Df) proxy, not global cavity diameter Di, so pore interiors wider than Df are unresolved.",
    "falsification_criteria": "If measured entropy loss does not decrease with lsd_f/lsd_f_ref at fixed Vol within a fixed framework topology family, or if Vol alone at fixed bottleneck explains the correlation equally well, the confinement-contrast mechanism is refuted in favor of a pure size effect.",
    "novelty_status": "new_combination",
    "evidence_ids": [
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
      "mechanism_family": "coupling",
      "proxy_assumptions": "Vol proxies excluded translational volume; lsd_f (Zeo++ Df) proxies the passing bottleneck, not global cavity diameter Di; fixed-probe AV is deliberately not used since it is not molecule-specific free volume.",
      "physical_interpretation": "Vol/Vol_ref scales excluded volume; lsd_f/lsd_f_ref scales confinement severity; both are dimensionless row-varying inputs and no q-unity threshold is asserted.",
      "boundary_behavior": "Vol (20.424–161.144) and lsd_f (0.85684–7.68726) are strictly positive on training; the log argument is positive and finite everywhere; no zero branch needed.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
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
      "training_spearman": 0.5357155930050844,
      "target_association": "contradicted",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/small_kg_rag_agent/replicate-2/round-1/h2`

最终状态：scored；边际收益：-4.714350 pp；保留：False。

复核改动字段：evidence_ids, formula, rationale, scientific_test.boundary_behavior, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "planarity_loss_of_rotational_freedom",
    "formula": "rotor_case(log1p_style_placeholder_removed, log1p_style_placeholder_removed, log((PBF/PBF_ref) ** 2 + 1))",
    "hypothesis": "For nonlinear adsorbates, loss of rotational entropy at adsorption increases with heavy-atom planarity departure (PBF): nonplanar molecules experience stronger orientational constraints in narrow channels, so entropy loss rises with PBF, while linear and single-site rotors show progressively weaker dependence.",
    "rationale": "Rotational mechanism family. PBF measures out-of-plane heavy-atom spread on the original implicit-H representation; legitimate zeros (planar molecules, e.g., aromatics) must not be imputed. Using log(1 + (PBF/PBF_ref)**2) keeps the value finite and smooth at PBF = 0 without adding an arbitrary epsilon to claim a physical law; it is an empirical smoothing choice with no universal meaning. Rotor_case branches are declared explicitly; linear and single-site branches are constant placeholders flagged as untested since the hypothesis only concerns nonlinear rotors.",
    "falsification_criteria": "If, at matched Vol and framework density, planar and nonplanar nonlinear adsorbates show indistinguishable entropy loss, or if PMI3/PMI1 anisotropy outperforms PBF as predictor, the planarity-orientational-constraint mechanism fails.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PBF is a heavy-atom planarity proxy, not all-atom geometry; methane is single-site and its PMI proxies are near-zero by convention, not physically zero inertia. Branch applicability limited to nonlinear rotors in training (n=2093).",
      "physical_interpretation": "PBF/PBF_ref is a dimensionless row-varying planarity ratio; PBF/q_PBF = PBF_ref is constant and never used as a threshold.",
      "boundary_behavior": "At PBF = 0 the expression equals 0 (log of 1), finite by construction; this is an empirical smoothing convention, not a claim that planar molecules lose zero rotational entropy.",
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
    "status": "rejected",
    "reason": "Unsupported formula symbol or syntax"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "planarity_loss_of_rotational_freedom",
    "formula": "rotor_case(0, log((PBF/PBF_ref) ** 2 + 1), log((PBF/PBF_ref) ** 2 + 1))",
    "hypothesis": "For nonlinear adsorbates, loss of rotational entropy at adsorption increases with heavy-atom planarity departure (PBF): nonplanar molecules experience stronger orientational constraints in narrow channels, so entropy loss rises with PBF, while linear and single-site rotors show progressively weaker dependence.",
    "rationale": "Replaced the invalid placeholder tokens in the single-site and linear branches with executable expressions: 0 for single-site rotors (methane-like, no heavy-atom planarity contrast) and the same smoothed planarity term for linear rotors, with the full term for nonlinear rotors as hypothesized. PBF has legitimate zeros (planar molecules); log(1 + (PBF/PBF_ref)**2) is finite and smooth at PBF = 0 and is an empirical smoothing choice, not a physical law or an added epsilon claiming one. Rotor_case branches are declared explicitly with compatible dimensionless units; the hypothesis concerns nonlinear rotors, so the linear and single-site branches are weakened/zero empirically and flagged as untested.",
    "falsification_criteria": "If, at matched Vol and framework density, planar and nonplanar nonlinear adsorbates show indistinguishable entropy loss, or if PMI3/PMI1 anisotropy outperforms PBF as predictor, the planarity-orientational-constraint mechanism fails.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01"
    ],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PBF is a heavy-atom planarity proxy on the original implicit-H representation, not all-atom geometry; methane is single-site with near-zero PMI proxies by convention, not physically zero inertia; nonlinear rotor branch applies to n=2093 training rows.",
      "physical_interpretation": "PBF/PBF_ref is a dimensionless row-varying planarity ratio; PBF/q_PBF = PBF_ref is constant and never used as a threshold.",
      "boundary_behavior": "At PBF = 0 each nonzero branch equals log(1) = 0, finite by construction; this is an empirical smoothing convention, not a claim that planar molecules lose zero rotational entropy.",
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
        "PBF"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.656249528
      ],
      "training_spearman": 0.2917049313081072,
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
    "name": "planarity_loss_of_rotational_freedom",
    "formula": "rotor_case(0, log((PBF/PBF_ref) ** 2 + 1), log((PBF/PBF_ref) ** 2 + 1))",
    "hypothesis": "For nonlinear adsorbates, loss of rotational entropy at adsorption increases with heavy-atom planarity departure (PBF): nonplanar molecules experience stronger orientational constraints in narrow channels, so entropy loss rises with PBF, while linear and single-site rotors show progressively weaker dependence.",
    "rationale": "Replaced the invalid placeholder tokens in the single-site and linear branches with executable expressions: 0 for single-site rotors (methane-like, no heavy-atom planarity contrast) and the same smoothed planarity term for linear rotors, with the full term for nonlinear rotors as hypothesized. PBF has legitimate zeros (planar molecules); log(1 + (PBF/PBF_ref)**2) is finite and smooth at PBF = 0 and is an empirical smoothing choice, not a physical law or an added epsilon claiming one. Rotor_case branches are declared explicitly with compatible dimensionless units; the hypothesis concerns nonlinear rotors, so the linear and single-site branches are weakened/zero empirically and flagged as untested.",
    "falsification_criteria": "If, at matched Vol and framework density, planar and nonplanar nonlinear adsorbates show indistinguishable entropy loss, or if PMI3/PMI1 anisotropy outperforms PBF as predictor, the planarity-orientational-constraint mechanism fails.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01"
    ],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PBF is a heavy-atom planarity proxy on the original implicit-H representation, not all-atom geometry; methane is single-site with near-zero PMI proxies by convention, not physically zero inertia; nonlinear rotor branch applies to n=2093 training rows.",
      "physical_interpretation": "PBF/PBF_ref is a dimensionless row-varying planarity ratio; PBF/q_PBF = PBF_ref is constant and never used as a threshold.",
      "boundary_behavior": "At PBF = 0 each nonzero branch equals log(1) = 0, finite by construction; this is an empirical smoothing convention, not a claim that planar molecules lose zero rotational entropy.",
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
        "PBF"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.656249528
      ],
      "training_spearman": 0.2917049313081072,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/small_kg_rag_agent/replicate-2/round-1/h3`

最终状态：scored；边际收益：+1.420495 pp；保留：True。

复核改动字段：evidence_ids

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_area_squeeze_contrast",
    "formula": "log((LabuteASA/LabuteASA_ref) / (AV/AV_ref + 1))",
    "hypothesis": "Entropy loss at infinite dilution increases with adsorbate surface area but decreases with framework probe-accessible specific volume, because larger contact surface and tighter accessible pore space both reduce retained configurational freedom; their contrast separates adsorbate-driven from framework-driven entropy mechanisms.",
    "rationale": "Coupling of shape (LabuteASA, adsorbate contact area proxy) and connectivity/probe-volume (AV, fixed-probe mass-specific accessibility). AV has 28 legitimate zeros in training (fixed geometric probe cannot enter); the additive +1 in the denominator keeps the expression finite at AV = 0 without imputation and is an empirical smoothing constant, not a physical percolation threshold. ASA/AV zero rows (inaccessible frameworks) are handled since the formula never divides by AV itself.",
    "falsification_criteria": "If frameworks with AV = 0 for the fixed probe (no physical molecular space by the descriptor's logic) still show nonzero adsorption entropy loss for small molecules, the AV-based mechanism is falsified for those systems; if LabuteASA loses predictive power when Vol is controlled, the surface-contact mechanism collapses into a pure size effect.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        7.450601137,
        80.47008049
      ],
      "training_spearman": 0.6521982457057977,
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        7.450601137,
        80.47008049
      ],
      "training_spearman": 0.6521982457057977,
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        7.450601137,
        80.47008049
      ],
      "training_spearman": 0.6521982457057977,
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
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:234d54d6aae543beff87e7be",
        "paper_id": "doi:10.1039/b504006j",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b86d2d3284fbbe6696210c35",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:79eb54bd69f0d3c26a62cffa",
        "paper_id": "pmc:pmc7239313",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:869af4527dd765744b7ebc76",
        "paper_id": "pmc:pmc8659101",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c515aa77b0e6afe8275e4595",
        "paper_id": "doi:10.1039/d5cs00613a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:45c6c30e39c58cf298acb495",
        "paper_id": "pmc:pmc8113345",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5a112468ad141199e895aef6",
        "paper_id": "pmc:pmc7915720",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5aff3d9da9c035dec7cb74e7",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:72dfcce988c17185f87c465c",
        "paper_id": "doi:10.1021/jp1096663",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:780c5f690f3ead9c996b9e32",
        "paper_id": "doi:10.1039/c4cp00109e",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in pure-silica zeolites, the ratio of adsorbed to gas-phase entropy loss grows when adsorbate volume relative to the framework passing bottleneck shrinks, because small molecules relative to Df retain more translational/configurational freedom in the pore; thus entropy loss decreases with increasing lsd_f and increases with molecular Vol. log((Vol/Vol_ref) ** 2 * (lsd_f/lsd_f_ref)) For nonlinear adsorbates, loss of rotational entropy at adsorption increases with heavy-atom planarity departure (PBF): nonplanar molecules experience stronger orientational constraints in narrow channels, so entropy loss rises with PBF, while linear and single-site rotors show progressively weaker dependence. rotor_case(log1p_style_placeholder_removed, log1p_style_placeholder_removed, log((PBF/PBF_ref) ** 2 + 1)) Entropy loss at infinite dilution increases with adsorbate surface area but decreases with framework probe-accessible specific volume, because larger contact surface and tighter accessible pore space both reduce retained configurational freedom; their contrast separates adsorbate-driven from framework-driven entropy mechanisms. log((LabuteASA/LabuteASA_ref) / (AV/AV_ref + 1))",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:01d0cb8bf43d75bbc448e004",
      "chunk:488a25074219dc1bb01f1486"
    ],
    "items": 10,
    "lexical_tokens": 4724,
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
