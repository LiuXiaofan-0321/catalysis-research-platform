# high/rag_agent/replicate-1/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/rag_agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`high/rag_agent/replicate-1/round-1/h1`

最终状态：scored；边际收益：+3.989349 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_size_translation_descriptor",
    "formula": "(q_lsd_f ** 0.5) * (MW_ref / MW ** 1.0) ** 0.25 * (Vol_ref / Vol ** 1.0) ** 0.125",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the adsorbed-phase/gas entropy ratio s_ads/s_gas decreases with adsorbate translational confinement: it increases with the framework free-path bottleneck (lsd_f, Df) and decreases with adsorbate mass and van der Waals volume. Equivalently, the dimensionless entropy loss -ln(s_ads/s_gas) is monotonically decreasing in q_lsd_f and monotonically increasing in MW and Vol.",
    "rationale": "Translational confinement of a molecule in a channel/cavity reduces accessible translational states roughly in proportion to the ratio of accessible to free volume; a larger passing bottleneck (Df) relaxes confinement while a larger/heavier adsorbate is more strongly confined. This is an empirical proxy hypothesis, not a derived partition-function identity: lsd_f is a fixed-probe bottleneck sphere, not a global cavity diameter, and MW/Vol are crude confinement proxies that ignore adsorbate-framework potential shape. Exponents 0.5/0.25/0.125 are fixed smoothing choices within the allowed range, carrying no universal physical meaning.",
    "falsification_criteria": "If, within a fixed framework-density and accessibility stratum, entropy loss shows no monotone association with q_lsd_f (e.g., partial correlation of the pre-declared derivative d(descriptor)/d(lsd_f) against residual entropy loss is not positive across training rows), or if Vol/MW dependence dominates only through shape descriptors rather than size, the translational-confinement hypothesis is falsified in favor of a shape- or connectivity-dominated mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "MW": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f (Df) proxies the confinement-relevant geometric bottleneck; MW and Vol proxy the degree to which the adsorbate experiences that bottleneck. Both proxies are transfer-limited: Df is computed for a fixed probe geometry, and Vol is a van der Waals estimate, so neither equals the molecule-specific free volume or the true potential-energy accessible region.",
      "physical_interpretation": "All factors are dimensionless q-normalized ratios against fixed training-reference medians; no factor equals 1 at any claimed physical transition, and the fixed exponents are empirical smoothing constants only.",
      "boundary_behavior": "MW, Vol, and lsd_f are strictly positive over the full training domain (min 16.03 g/mol, 20.424 A^3, 0.85684 A), so every row yields a finite positive descriptor; no legitimate-zero input is divided by.",
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
        "MW",
        "Vol",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
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
      "training_spearman": -0.6459922819488138,
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
    "name": "bottleneck_size_translation_descriptor",
    "formula": "(q_lsd_f ** 0.5) * (MW_ref / MW ** 1.0) ** 0.25 * (Vol_ref / Vol ** 1.0) ** 0.125",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the adsorbed-phase/gas entropy ratio s_ads/s_gas decreases with adsorbate translational confinement: it increases with the framework free-path bottleneck (lsd_f, Df) and decreases with adsorbate mass and van der Waals volume. Equivalently, the dimensionless entropy loss -ln(s_ads/s_gas) is monotonically decreasing in q_lsd_f and monotonically increasing in MW and Vol.",
    "rationale": "Translational confinement of a molecule in a channel/cavity reduces accessible translational states roughly in proportion to the ratio of accessible to free volume; a larger passing bottleneck (Df) relaxes confinement while a larger/heavier adsorbate is more strongly confined. This is an empirical proxy hypothesis, not a derived partition-function identity: lsd_f is a fixed-probe bottleneck sphere, not a global cavity diameter, and MW/Vol are crude confinement proxies that ignore adsorbate-framework potential shape. Exponents 0.5/0.25/0.125 are fixed smoothing choices within the allowed range, carrying no universal physical meaning.",
    "falsification_criteria": "If, within a fixed framework-density and accessibility stratum, the pre-declared partial association of residual entropy loss with d(descriptor)/d(lsd_f) is not negative (the descriptor increases with lsd_f while entropy loss is pre-declared to decrease, consistent with the training precheck Spearman of about -0.65), or if MW or Vol enter with the sign opposite to the declared confinement direction, or if connectivity-contrast descriptors (e.g., Dif/Df) dominate over absolute bottleneck size, the translational-confinement hypothesis is falsified in favor of a shape- or connectivity-dominated mechanism. Note: only the lsd_f partial was covered by the training-only precheck; the MW and Vol partial derivatives remain explicitly to be tested.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E08"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "MW": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f (Df) proxies the confinement-relevant geometric bottleneck; MW and Vol proxy the degree to which the adsorbate experiences that bottleneck. Both proxies are transfer-limited: Df is computed for a fixed probe geometry, and Vol is a van der Waals estimate, so neither equals the molecule-specific free volume or the true potential-energy accessible region.",
      "physical_interpretation": "All factors are dimensionless q-normalized ratios against fixed training-reference medians; no factor equals 1 at any claimed physical transition, and the fixed exponents are empirical smoothing constants only.",
      "boundary_behavior": "MW, Vol, and lsd_f are strictly positive over the full training domain (min 16.03 g/mol, 20.424 A^3, 0.85684 A), so every row yields a finite positive descriptor; no legitimate-zero input is divided by.",
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
        "MW",
        "Vol",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
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
      "training_spearman": -0.6459922819488138,
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
    "name": "bottleneck_size_translation_descriptor",
    "formula": "(q_lsd_f ** 0.5) * (MW_ref / MW ** 1.0) ** 0.25 * (Vol_ref / Vol ** 1.0) ** 0.125",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the adsorbed-phase/gas entropy ratio s_ads/s_gas decreases with adsorbate translational confinement: it increases with the framework free-path bottleneck (lsd_f, Df) and decreases with adsorbate mass and van der Waals volume. Equivalently, the dimensionless entropy loss -ln(s_ads/s_gas) is monotonically decreasing in q_lsd_f and monotonically increasing in MW and Vol.",
    "rationale": "Translational confinement of a molecule in a channel/cavity reduces accessible translational states roughly in proportion to the ratio of accessible to free volume; a larger passing bottleneck (Df) relaxes confinement while a larger/heavier adsorbate is more strongly confined. This is an empirical proxy hypothesis, not a derived partition-function identity: lsd_f is a fixed-probe bottleneck sphere, not a global cavity diameter, and MW/Vol are crude confinement proxies that ignore adsorbate-framework potential shape. Exponents 0.5/0.25/0.125 are fixed smoothing choices within the allowed range, carrying no universal physical meaning.",
    "falsification_criteria": "If, within a fixed framework-density and accessibility stratum, the pre-declared partial association of residual entropy loss with d(descriptor)/d(lsd_f) is not negative (the descriptor increases with lsd_f while entropy loss is pre-declared to decrease, consistent with the training precheck Spearman of about -0.65), or if MW or Vol enter with the sign opposite to the declared confinement direction, or if connectivity-contrast descriptors (e.g., Dif/Df) dominate over absolute bottleneck size, the translational-confinement hypothesis is falsified in favor of a shape- or connectivity-dominated mechanism. Note: only the lsd_f partial was covered by the training-only precheck; the MW and Vol partial derivatives remain explicitly to be tested.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E08"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "MW": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f (Df) proxies the confinement-relevant geometric bottleneck; MW and Vol proxy the degree to which the adsorbate experiences that bottleneck. Both proxies are transfer-limited: Df is computed for a fixed probe geometry, and Vol is a van der Waals estimate, so neither equals the molecule-specific free volume or the true potential-energy accessible region.",
      "physical_interpretation": "All factors are dimensionless q-normalized ratios against fixed training-reference medians; no factor equals 1 at any claimed physical transition, and the fixed exponents are empirical smoothing constants only.",
      "boundary_behavior": "MW, Vol, and lsd_f are strictly positive over the full training domain (min 16.03 g/mol, 20.424 A^3, 0.85684 A), so every row yields a finite positive descriptor; no legitimate-zero input is divided by.",
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
        "MW",
        "Vol",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
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
      "training_spearman": -0.6459922819488138,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/rag_agent/replicate-1/round-1/h2`

最终状态：scored；边际收益：-0.561669 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_class_inertia_descriptor",
    "formula": "rotor_case(1.0, (q_PMI2 ** 0.25), ((q_PMI2 * q_PMI3) ** 0.125))",
    "hypothesis": "At infinite dilution, s_ads/s_gas decreases with the adsorbate's rotational state suppression in the confined phase, which scales with heavy-atom principal moments of inertia in a rotor-class-dependent way: single-site molecules (methane-like, PMI1=PMI2=PMI3=0 in the heavy-atom representation) are assigned a constant descriptor (no rotational entropy-loss gradient), near-linear molecules depend on the intermediate/heavy-axis moment PMI2, and nonlinear molecules depend on the geometric-mean-like combination of PMI2 and PMI3. Pre-declared association: entropy loss increases with the descriptor value within the linear and nonlinear branches.",
    "rationale": "Confined rotation loses fewer states when the molecule's rotational degrees of freedom are already restricted (near-linear, small transverse moments). The descriptor uses heavy-atom implicit-H moments, which are legitimate structural proxies with true zeros for single-site molecules; these zeros are NOT claims about all-atom inertia being zero, which is why the single_site branch is a constant and never evaluates PMI expressions. Rotor_case branches: single_site -> constant 1.0 (finite at PMI zeros); linear -> (q_PMI2)**0.25, finite because PMI2 > 0 for all linear rows (54 zero rows are exactly the single-site class routed to the first branch); nonlinear -> (q_PMI2 * q_PMI3)**0.125, finite because PMI2, PMI3 > 0 for nonlinear rows. The exponents are fixed empirical smoothing choices, not derived constants.",
    "falsification_criteria": "If within-branch residual entropy loss does not increase with the branch expression (pre-declared positive association), or if a single unified PMI power law without rotor classes fits equally well, the rotor-class-dependent hypothesis is falsified. If rotational proxies add no association beyond translational/shape proxies (h1), the rotation mechanism family is unsupported for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2 and PMI3 in the implicit-H/heavy-atom representation proxy rotational confinement; hydrogen contributions are ignored by construction. Branch membership is defined by the proxy categories (single_site/linear/nonlinear, tolerance 1e-10), not by measured rotational spectra; transfer to true all-atom rotational partition functions is limited.",
      "physical_interpretation": "q_PMI2 and q_PMI3 are dimensionless ratios to fixed training-reference medians (93.79729089 and 125.4948325); q = 1 is a normalization convention with no physical unity threshold. All three branch outputs are dimensionless and unit-compatible.",
      "boundary_behavior": "Single-site rows (PMI1=PMI2=PMI3=0, 54 training rows) evaluate the constant branch 1.0, so legitimate PMI zeros never enter a division, log, or negative power; the linear and nonlinear branches are evaluated only on rows where PMI2 and PMI3 are strictly positive, so every training row yields a finite value.",
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
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.3833888747315314,
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
    "name": "rotor_class_inertia_descriptor",
    "formula": "rotor_case(1.0, (q_PMI2 ** 0.25), ((q_PMI2 * q_PMI3) ** 0.125))",
    "hypothesis": "At infinite dilution, s_ads/s_gas decreases with the adsorbate's rotational state suppression in the confined phase, which scales with heavy-atom principal moments of inertia in a rotor-class-dependent way: single-site molecules (methane-like, PMI1=PMI2=PMI3=0 in the heavy-atom representation) are assigned a constant descriptor (no rotational entropy-loss gradient), near-linear molecules depend on the intermediate/heavy-axis moment PMI2, and nonlinear molecules depend on the geometric-mean-like combination of PMI2 and PMI3. Pre-declared association: entropy loss increases with the descriptor value within the linear and nonlinear branches.",
    "rationale": "Confined rotation loses fewer states when the molecule's rotational degrees of freedom are already restricted. The descriptor uses heavy-atom implicit-H moments, which are legitimate structural proxies with true zeros for single-site molecules; these zeros are NOT claims about all-atom inertia being zero, which is why the single_site branch is a constant and never evaluates PMI expressions. Reported evidence that rotational degrees of freedom are lost more strongly in smaller-pore frameworks (E01) and that both translational and rotational motions contribute to adsorption entropy loss (E03) motivate the mechanism without fixing any coefficient. Rotor_case branches: single_site -> constant 1.0 (finite at PMI zeros); linear -> (q_PMI2)**0.25, finite because PMI2 > 0 for all linear rows (the 54 PMI2/PMI3 zero rows match the single_site class routed to the first branch); nonlinear -> (q_PMI2 * q_PMI3)**0.125, finite because PMI2, PMI3 > 0 for nonlinear rows. For strictly linear rows PMI2 = PMI3, so the linear branch coincides with the geometric-mean form evaluated there; the branch split exists only to protect the legitimate PMI zeros. The exponents are fixed empirical smoothing choices, not derived constants, and the training precheck (Spearman about 0.38, mechanism not validated) shows association, not causality.",
    "falsification_criteria": "If within-branch residual entropy loss does not increase with the branch expression (pre-declared positive association), or if a single unified PMI power law without rotor classes fits equally well, the rotor-class-dependent hypothesis is falsified. If rotational proxies add no association beyond translational/shape proxies (h1), the rotation mechanism family is unsupported for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E03"
    ],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2 and PMI3 in the implicit-H/heavy-atom representation proxy rotational confinement; hydrogen contributions are ignored by construction. Branch membership is defined by the proxy categories (single_site/linear/nonlinear, tolerance 1e-10), not by measured rotational spectra; transfer to true all-atom rotational partition functions is limited.",
      "physical_interpretation": "q_PMI2 and q_PMI3 are dimensionless ratios to fixed training-reference medians (93.79729089 and 125.4948325); q = 1 is a normalization convention with no physical unity threshold. All three branch outputs are dimensionless and unit-compatible.",
      "boundary_behavior": "Single-site rows (PMI1=PMI2=PMI3=0, 54 training rows) evaluate the constant branch 1.0, so legitimate PMI zeros never enter a division, log, or negative power; the linear and nonlinear branches are evaluated only on rows where PMI2 and PMI3 are strictly positive, so every training row yields a finite value.",
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
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.3833888747315314,
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
    "name": "rotor_class_inertia_descriptor",
    "formula": "rotor_case(1.0, (q_PMI2 ** 0.25), ((q_PMI2 * q_PMI3) ** 0.125))",
    "hypothesis": "At infinite dilution, s_ads/s_gas decreases with the adsorbate's rotational state suppression in the confined phase, which scales with heavy-atom principal moments of inertia in a rotor-class-dependent way: single-site molecules (methane-like, PMI1=PMI2=PMI3=0 in the heavy-atom representation) are assigned a constant descriptor (no rotational entropy-loss gradient), near-linear molecules depend on the intermediate/heavy-axis moment PMI2, and nonlinear molecules depend on the geometric-mean-like combination of PMI2 and PMI3. Pre-declared association: entropy loss increases with the descriptor value within the linear and nonlinear branches.",
    "rationale": "Confined rotation loses fewer states when the molecule's rotational degrees of freedom are already restricted. The descriptor uses heavy-atom implicit-H moments, which are legitimate structural proxies with true zeros for single-site molecules; these zeros are NOT claims about all-atom inertia being zero, which is why the single_site branch is a constant and never evaluates PMI expressions. Reported evidence that rotational degrees of freedom are lost more strongly in smaller-pore frameworks (E01) and that both translational and rotational motions contribute to adsorption entropy loss (E03) motivate the mechanism without fixing any coefficient. Rotor_case branches: single_site -> constant 1.0 (finite at PMI zeros); linear -> (q_PMI2)**0.25, finite because PMI2 > 0 for all linear rows (the 54 PMI2/PMI3 zero rows match the single_site class routed to the first branch); nonlinear -> (q_PMI2 * q_PMI3)**0.125, finite because PMI2, PMI3 > 0 for nonlinear rows. For strictly linear rows PMI2 = PMI3, so the linear branch coincides with the geometric-mean form evaluated there; the branch split exists only to protect the legitimate PMI zeros. The exponents are fixed empirical smoothing choices, not derived constants, and the training precheck (Spearman about 0.38, mechanism not validated) shows association, not causality.",
    "falsification_criteria": "If within-branch residual entropy loss does not increase with the branch expression (pre-declared positive association), or if a single unified PMI power law without rotor classes fits equally well, the rotor-class-dependent hypothesis is falsified. If rotational proxies add no association beyond translational/shape proxies (h1), the rotation mechanism family is unsupported for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E03"
    ],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2 and PMI3 in the implicit-H/heavy-atom representation proxy rotational confinement; hydrogen contributions are ignored by construction. Branch membership is defined by the proxy categories (single_site/linear/nonlinear, tolerance 1e-10), not by measured rotational spectra; transfer to true all-atom rotational partition functions is limited.",
      "physical_interpretation": "q_PMI2 and q_PMI3 are dimensionless ratios to fixed training-reference medians (93.79729089 and 125.4948325); q = 1 is a normalization convention with no physical unity threshold. All three branch outputs are dimensionless and unit-compatible.",
      "boundary_behavior": "Single-site rows (PMI1=PMI2=PMI3=0, 54 training rows) evaluate the constant branch 1.0, so legitimate PMI zeros never enter a division, log, or negative power; the linear and nonlinear branches are evaluated only on rows where PMI2 and PMI3 are strictly positive, so every training row yields a finite value.",
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
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.3833888747315314,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/rag_agent/replicate-1/round-1/h3`

最终状态：scored；边际收益：+2.612934 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "path_contrast_connectivity_descriptor",
    "formula": "(q_lsd_p / q_lsd_f) ** 0.5",
    "hypothesis": "At infinite dilution, the ratio between the largest included sphere along the free-sphere path (lsd_p, Dif) and the passing bottleneck sphere (lsd_f, Df) encodes a pore connectivity contrast: frameworks whose local cavities (Dif) are large relative to their windows (Df) impose a stronger window-to-cavity entropy gradient on the adsorbate. Pre-declared association: entropy loss -ln(s_ads/s_gas) increases with the descriptor (Dif/Df contrast); equivalently s_ads/s_gas decreases with increasing Dif/Df at fixed accessibility.",
    "rationale": "The Dif/Df contrast distinguishes cage-like frameworks (large included spheres behind small windows) from channel-like frameworks (included sphere close to bottleneck), a connectivity-driven geometric mechanism distinct from h1's absolute bottleneck scale and h2's rotational suppression. This is explicitly a proxy contrast: Dif is the included sphere along the free path, not the global maximum cavity diameter Di, and Df is a fixed-probe passing sphere; neither alone nor their ratio equals a molecular free-volume quantity. The fixed exponent 0.5 is an empirical smoothing choice with no universal meaning.",
    "falsification_criteria": "If residual entropy loss at fixed lsd_f and fixed accessibility (ASA/AV strata) shows no increasing association with the Dif/Df contrast, or if the contrast carries no information beyond lsd_f alone, the window-cavity connectivity mechanism is falsified for this dataset. A competing mechanism would attribute all connectivity effects to probe-accessible volume (AV/ASA) rather than path geometry.",
    "novelty_status": "uncertain",
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
      "proxy_assumptions": "Dif/Df from fixed-probe sphere calculations proxies the window-to-cavity confinement gradient experienced by real adsorbates; the mapping from hard-sphere path geometry to molecule-specific entropy loss is approximate and transfer-limited, especially for molecules comparable to the bottleneck size.",
      "physical_interpretation": "The ratio q_lsd_p/q_lsd_f is dimensionless and equals (lsd_p/lsd_f) * (lsd_f_ref/lsd_p_ref); it is a normalization-rescaled contrast, not a physical equality threshold at value 1. Only the product's ordering across rows is interpreted.",
      "boundary_behavior": "Both lsd_f (min 0.85684 A) and lsd_p (min 3.3452 A) are strictly positive across the training domain with no zero rows, so the quotient and the 0.5 power are finite for every training row; the fixed reference medians (5.16326 A and 6.38663 A) are constants of normalization, not fitted parameters.",
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
    "name": "path_contrast_connectivity_descriptor",
    "formula": "(q_lsd_p / q_lsd_f) ** 0.5",
    "hypothesis": "At infinite dilution, the ratio between the largest included sphere along the free-sphere path (lsd_p, Dif) and the passing bottleneck sphere (lsd_f, Df) encodes a pore connectivity contrast: frameworks whose local cavities (Dif) are large relative to their windows (Df) impose a stronger window-to-cavity entropy gradient on the adsorbate. Pre-declared association: entropy loss -ln(s_ads/s_gas) increases with the descriptor (Dif/Df contrast); equivalently s_ads/s_gas decreases with increasing Dif/Df at fixed accessibility.",
    "rationale": "The Dif/Df contrast distinguishes cage-like frameworks (large included spheres behind small windows) from channel-like frameworks (included sphere close to bottleneck), a connectivity-driven geometric mechanism distinct from h1's absolute bottleneck scale and h2's rotational suppression. This is explicitly a proxy contrast: Dif is the included sphere along the free path, not the global maximum cavity diameter Di, and Df is a fixed-probe passing sphere; neither alone nor their ratio equals a molecular free-volume quantity. The fixed exponent 0.5 is an empirical smoothing choice with no universal meaning. Direction risk is pre-declared and honest: the training-only precheck was inconclusive (Spearman about -0.02), and the cited sources report that larger pores/cavities show SMALLER entropy losses (E02; consistent with E04 and E09), which at fixed Df would predict the OPPOSITE sign for the Dif/Df contrast to the one declared here. A trapping-behind-windows reading of the contrast is a kinetic argument, and kinetic escape does not by itself determine equilibrium entropy, so the declared positive direction is retained as an at-risk empirical hypothesis that the current precheck cannot discriminate from its negative competitor.",
    "falsification_criteria": "If residual entropy loss at fixed lsd_f and fixed ASA/AV strata shows no monotone association with the Dif/Df contrast, or shows the opposite (negative) sign to the pre-declared direction — i.e., entropy loss DECREASES with Dif/Df, as the reported larger-cavity/smaller-loss trend (E02, E09) would predict at fixed bottleneck — the window-to-cavity contrast mechanism as declared is falsified. A competing mechanism would attribute the effect to absolute included-sphere/cavity size (Dif) or to probe-accessible volume (AV/ASA) rather than to the contrast ratio; the essentially zero training precheck correlation means neither sign is currently supported.",
    "novelty_status": "uncertain",
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
      "proxy_assumptions": "Dif/Df from fixed-probe sphere calculations proxies the window-to-cavity confinement gradient experienced by real adsorbates; the mapping from hard-sphere path geometry to molecule-specific entropy loss is approximate and transfer-limited, especially for molecules comparable to the bottleneck size.",
      "physical_interpretation": "The ratio q_lsd_p/q_lsd_f is dimensionless and equals (lsd_p/lsd_f) * (lsd_f_ref/lsd_p_ref); it is a normalization-rescaled contrast, not a physical equality threshold at value 1. Only the product's ordering across rows is interpreted.",
      "boundary_behavior": "Both lsd_f (min 0.85684 A) and lsd_p (min 3.3452 A) are strictly positive across the training domain with no zero rows, so the quotient and the 0.5 power are finite for every training row; the fixed reference medians (5.16326 A and 6.38663 A) are constants of normalization, not fitted parameters.",
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
    "name": "path_contrast_connectivity_descriptor",
    "formula": "(q_lsd_p / q_lsd_f) ** 0.5",
    "hypothesis": "At infinite dilution, the ratio between the largest included sphere along the free-sphere path (lsd_p, Dif) and the passing bottleneck sphere (lsd_f, Df) encodes a pore connectivity contrast: frameworks whose local cavities (Dif) are large relative to their windows (Df) impose a stronger window-to-cavity entropy gradient on the adsorbate. Pre-declared association: entropy loss -ln(s_ads/s_gas) increases with the descriptor (Dif/Df contrast); equivalently s_ads/s_gas decreases with increasing Dif/Df at fixed accessibility.",
    "rationale": "The Dif/Df contrast distinguishes cage-like frameworks (large included spheres behind small windows) from channel-like frameworks (included sphere close to bottleneck), a connectivity-driven geometric mechanism distinct from h1's absolute bottleneck scale and h2's rotational suppression. This is explicitly a proxy contrast: Dif is the included sphere along the free path, not the global maximum cavity diameter Di, and Df is a fixed-probe passing sphere; neither alone nor their ratio equals a molecular free-volume quantity. The fixed exponent 0.5 is an empirical smoothing choice with no universal meaning. Direction risk is pre-declared and honest: the training-only precheck was inconclusive (Spearman about -0.02), and the cited sources report that larger pores/cavities show SMALLER entropy losses (E02; consistent with E04 and E09), which at fixed Df would predict the OPPOSITE sign for the Dif/Df contrast to the one declared here. A trapping-behind-windows reading of the contrast is a kinetic argument, and kinetic escape does not by itself determine equilibrium entropy, so the declared positive direction is retained as an at-risk empirical hypothesis that the current precheck cannot discriminate from its negative competitor.",
    "falsification_criteria": "If residual entropy loss at fixed lsd_f and fixed ASA/AV strata shows no monotone association with the Dif/Df contrast, or shows the opposite (negative) sign to the pre-declared direction — i.e., entropy loss DECREASES with Dif/Df, as the reported larger-cavity/smaller-loss trend (E02, E09) would predict at fixed bottleneck — the window-to-cavity contrast mechanism as declared is falsified. A competing mechanism would attribute the effect to absolute included-sphere/cavity size (Dif) or to probe-accessible volume (AV/ASA) rather than to the contrast ratio; the essentially zero training precheck correlation means neither sign is currently supported.",
    "novelty_status": "uncertain",
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
      "proxy_assumptions": "Dif/Df from fixed-probe sphere calculations proxies the window-to-cavity confinement gradient experienced by real adsorbates; the mapping from hard-sphere path geometry to molecule-specific entropy loss is approximate and transfer-limited, especially for molecules comparable to the bottleneck size.",
      "physical_interpretation": "The ratio q_lsd_p/q_lsd_f is dimensionless and equals (lsd_p/lsd_f) * (lsd_f_ref/lsd_p_ref); it is a normalization-rescaled contrast, not a physical equality threshold at value 1. Only the product's ordering across rows is interpreted.",
      "boundary_behavior": "Both lsd_f (min 0.85684 A) and lsd_p (min 3.3452 A) are strictly positive across the training domain with no zero rows, so the quotient and the 0.5 power are finite for every training row; the fixed reference medians (5.16326 A and 6.38663 A) are constants of normalization, not fitted parameters.",
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
        "record_id": "chunk:bd75db1400cf2ce6171ef0f6",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
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
        "record_id": "chunk:1487a816fb99c8a313aa68d6",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b86d2d3284fbbe6696210c35",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f778ee929c947fcc9e316c34",
        "paper_id": "pmc:pmc12559319",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:18391cdbbe5e3ebe0bcf4b09",
        "paper_id": "doi:10.1038/nmat1784",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5aff3d9da9c035dec7cb74e7",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6548d8cfcf6b0a54557fd663",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7bec0989f12cc18693a97a3f",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:98e1a32b2368edb9fba035bb",
        "paper_id": "doi:10.1021/ja1073992",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c97221094e85a6a9a0b89dc9",
        "paper_id": "pmc:pmc12272692",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd1acc7b04d64296bb68e884",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:147fa339122edc3ff44ba658",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, the adsorbed-phase/gas entropy ratio s_ads/s_gas decreases with adsorbate translational confinement: it increases with the framework free-path bottleneck (lsd_f, Df) and decreases with adsorbate mass and van der Waals volume. Equivalently, the dimensionless entropy loss -ln(s_ads/s_gas) is monotonically decreasing in q_lsd_f and monotonically increasing in MW and Vol. (q_lsd_f ** 0.5) * (MW_ref / MW ** 1.0) ** 0.25 * (Vol_ref / Vol ** 1.0) ** 0.125 At infinite dilution, s_ads/s_gas decreases with the adsorbate's rotational state suppression in the confined phase, which scales with heavy-atom principal moments of inertia in a rotor-class-dependent way: single-site molecules (methane-like, PMI1=PMI2=PMI3=0 in the heavy-atom representation) are assigned a constant descriptor (no rotational entropy-loss gradient), near-linear molecules depend on the intermediate/heavy-axis moment PMI2, and nonlinear molecules depend on the geometric-mean-like combination of PMI2 and PMI3. Pre-declared association: entropy loss increases with the descriptor value within the linear and nonlinear branches. rotor_case(1.0, (q_PMI2 ** 0.25), ((q_PMI2 * q_PMI3) ** 0.125)) At infinite dilution, the ratio between the largest included sphere along the free-sphere path (lsd_p, Dif) and the passing bottleneck sphere (lsd_f, Df) encodes a pore connectivity contrast: frameworks whose local cavities (Dif) are large relative to their windows (Df) impose a stronger window-to-cavity entropy gradient on the adsorbate. Pre-declared association: entropy loss -ln(s_ads/s_gas) increases with the descriptor (Dif/Df contrast); equivalently s_ads/s_gas decreases with increasing Dif/Df at fixed accessibility. (q_lsd_p / q_lsd_f) ** 0.5",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:e9ae89d415e72e1faf77faf0",
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
