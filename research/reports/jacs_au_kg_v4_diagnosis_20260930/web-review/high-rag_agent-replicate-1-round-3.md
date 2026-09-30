# high/rag_agent/replicate-1/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/rag_agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
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
  {
    "slot_id": "h2",
    "name": "accessible_volume_density_contrast_descriptor",
    "formula": "(q_AV ** 0.25) * (q_density ** (-0.125))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the probe-accessible specific volume (AV) and increases with the framework density on its native numerical scale: the descriptor D = q_AV**0.25 * q_density**(-0.125) is negatively associated with entropy loss, because roomier, less dense frameworks impose weaker translational confinement on a single adsorbed molecule.",
    "rationale": "AV (fixed-probe, mass-specific) and framework density jointly index pore space per framework mass from opposite sides; their contrast is a connectivity/pore-space mechanism distinct from the bottleneck-size mechanism of the retained h1 and from adsorbate-only size terms. Limitations: AV is a fixed geometric-probe quantity, so AV=0 does not imply zero molecular adsorption space; the density unit is unresolved on its native scale; both terms are strongly mutually correlated so the formula re-expresses already-available D0 inputs, and the exponents are empirical smoothings without universal meaning.",
    "falsification_criteria": "If, holding lsd_f fixed, the partial association of the descriptor with entropy loss is inconclusive or positive (i.e., roomier frameworks show equal or larger entropy loss), or if the association is entirely absorbed by lsd_f (no residual connectivity effect), the pore-space hypothesis is falsified for this descriptor.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV is a fixed-probe, mass-specific accessibility proxy, not molecule-specific free volume; density is a native-scale framework density proxy with unresolved unit; the product assumes these two proxies jointly rank translational confinement at infinite dilution.",
      "physical_interpretation": "Only native AV and native-scale density meanings are claimed, entering as dimensionless q-ratios; no q-unity threshold is asserted; the negative density exponent reflects the native scale's inverse ranking of pore space, not a physical law.",
      "boundary_behavior": "For the 28 training rows with AV=0, q_AV**0.25 = 0 gives D=0, a finite lower bound representing maximal confinement under the fixed-probe proxy; this is explicitly a proxy bound, since zero fixed-probe accessibility does not imply zero molecular adsorption space. density is strictly positive in training, so the negative exponent never divides by zero.",
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

候选标识：`high/rag_agent/replicate-1/round-3/h1`

最终状态：scored；边际收益：-6.211148 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "molecule_bottleneck_fit_descriptor",
    "formula": "(q_GeDi ** 0.25) * (q_lsd_f ** (-0.25))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dimensionless entropy loss -ln(s_ads/s_gas) increases with the geometric mismatch between adsorbate extension and framework bottleneck: molecules whose largest heavy-atom pair distance (GeDi) is large relative to the free-path bottleneck (lsd_f, Df) experience a tighter fit, which suppresses translational and orientational sampling. The descriptor D = q_GeDi**0.25 * q_lsd_f**(-0.25) is therefore positively associated with entropy loss; equivalently s_ads/s_gas decreases as D increases.",
    "rationale": "Df is the largest sphere that can pass through the periodic free path, so a large adsorbate span relative to Df forces the molecule into a narrow corridor of admissible positions and orientations at a single adsorption site, reducing configurational entropy. This is an association claim about a heavy-atom geometric proxy, not a causal or all-atom statement. Limitations: GeDi is computed in the original implicit-H/heavy-atom representation, so it understates the extension of hydrogen-rich molecules; lsd_f is a bottleneck measure, not the global cavity diameter Di.",
    "falsification_criteria": "If, holding MW and Vol fixed within the training set, the partial rank association between D and entropy loss is indistinguishable from zero, the size-fit coupling mechanism is falsified; the competing mechanism is that confinement is governed by volume (Vol) rather than by the extension-to-bottleneck ratio.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "GeDi is a heavy-atom enclosing pair-distance proxy with legitimate zeros for single-site molecules (54 training rows); lsd_f is a passing-bottleneck proxy, not Di. Neither equals true all-atom geometry or a physical equality threshold; q-normalized values carry no universal physical meaning.",
      "physical_interpretation": "Native meanings: GeDi in angstrom is the largest heavy-atom pair distance; lsd_f in angstrom is the free-path bottleneck diameter. D is a dimensionless ratio of q-normalized proxies used only for monotone association with entropy loss.",
      "boundary_behavior": "For single-site molecules (GeDi = 0, a legitimate heavy-atom-representation zero, e.g. methane), D = 0, encoding no heavy-atom elongation penalty and hence minimal fit-based confinement; this is finite because only a nonnegative exponent is applied to q_GeDi. q_lsd_f is strictly positive on the training domain (0.85684-7.68726 angstrom), so its negative exponent never divides by zero.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
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
        "GeDi",
        "lsd_f"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.608006859917338,
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
    "slot_id": "h1",
    "name": "molecule_bottleneck_fit_descriptor",
    "formula": "(q_GeDi ** 0.25) * (q_lsd_f ** (-0.25))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dimensionless entropy loss -ln(s_ads/s_gas) increases with the geometric mismatch between adsorbate extension and framework bottleneck: molecules whose largest heavy-atom pair distance (GeDi) is large relative to the free-path bottleneck (lsd_f, Df) experience a tighter fit, which suppresses translational and orientational sampling. The descriptor D = q_GeDi**0.25 * q_lsd_f**(-0.25) is therefore positively associated with entropy loss; equivalently s_ads/s_gas decreases as D increases.",
    "rationale": "Df is the largest sphere that can pass through the periodic free path, so a large adsorbate span relative to Df forces the molecule into a narrow corridor of admissible positions and orientations at a single adsorption site, reducing configurational entropy. This is an association claim about a heavy-atom geometric proxy, not a causal or all-atom statement. Limitations: GeDi is computed in the original implicit-H/heavy-atom representation, so it understates the extension of hydrogen-rich molecules; lsd_f is a bottleneck measure, not the global cavity diameter Di.",
    "falsification_criteria": "If, holding MW and Vol fixed within the training set, the partial rank association between D and entropy loss is indistinguishable from zero, the size-fit coupling mechanism is falsified; the competing mechanism is that confinement is governed by volume (Vol) rather than by the extension-to-bottleneck ratio.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "GeDi is a heavy-atom enclosing pair-distance proxy with legitimate zeros for single-site molecules (54 training rows); lsd_f is a passing-bottleneck proxy, not Di. Neither equals true all-atom geometry or a physical equality threshold; q-normalized values carry no universal physical meaning.",
      "physical_interpretation": "Native meanings: GeDi in angstrom is the largest heavy-atom pair distance; lsd_f in angstrom is the free-path bottleneck diameter. D is a dimensionless ratio of q-normalized proxies used only for monotone association with entropy loss.",
      "boundary_behavior": "For single-site molecules (GeDi = 0, a legitimate heavy-atom-representation zero, e.g. methane), D = 0, encoding no heavy-atom elongation penalty and hence minimal fit-based confinement; this is finite because only a nonnegative exponent is applied to q_GeDi. q_lsd_f is strictly positive on the training domain (0.85684-7.68726 angstrom), so its negative exponent never divides by zero.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
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
        "GeDi",
        "lsd_f"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.608006859917338,
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
    "slot_id": "h1",
    "name": "molecule_bottleneck_fit_descriptor",
    "formula": "(q_GeDi ** 0.25) * (q_lsd_f ** (-0.25))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dimensionless entropy loss -ln(s_ads/s_gas) increases with the geometric mismatch between adsorbate extension and framework bottleneck: molecules whose largest heavy-atom pair distance (GeDi) is large relative to the free-path bottleneck (lsd_f, Df) experience a tighter fit, which suppresses translational and orientational sampling. The descriptor D = q_GeDi**0.25 * q_lsd_f**(-0.25) is therefore positively associated with entropy loss; equivalently s_ads/s_gas decreases as D increases.",
    "rationale": "Df is the largest sphere that can pass through the periodic free path, so a large adsorbate span relative to Df forces the molecule into a narrow corridor of admissible positions and orientations at a single adsorption site, reducing configurational entropy. This is an association claim about a heavy-atom geometric proxy, not a causal or all-atom statement. Limitations: GeDi is computed in the original implicit-H/heavy-atom representation, so it understates the extension of hydrogen-rich molecules; lsd_f is a bottleneck measure, not the global cavity diameter Di.",
    "falsification_criteria": "If, holding MW and Vol fixed within the training set, the partial rank association between D and entropy loss is indistinguishable from zero, the size-fit coupling mechanism is falsified; the competing mechanism is that confinement is governed by volume (Vol) rather than by the extension-to-bottleneck ratio.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "GeDi is a heavy-atom enclosing pair-distance proxy with legitimate zeros for single-site molecules (54 training rows); lsd_f is a passing-bottleneck proxy, not Di. Neither equals true all-atom geometry or a physical equality threshold; q-normalized values carry no universal physical meaning.",
      "physical_interpretation": "Native meanings: GeDi in angstrom is the largest heavy-atom pair distance; lsd_f in angstrom is the free-path bottleneck diameter. D is a dimensionless ratio of q-normalized proxies used only for monotone association with entropy loss.",
      "boundary_behavior": "For single-site molecules (GeDi = 0, a legitimate heavy-atom-representation zero, e.g. methane), D = 0, encoding no heavy-atom elongation penalty and hence minimal fit-based confinement; this is finite because only a nonnegative exponent is applied to q_GeDi. q_lsd_f is strictly positive on the training domain (0.85684-7.68726 angstrom), so its negative exponent never divides by zero.",
      "vary_input": "GeDi",
      "descriptor_direction": "increasing",
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
        "GeDi",
        "lsd_f"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.608006859917338,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/rag_agent/replicate-1/round-3/h2`

最终状态：scored；边际收益：-6.629657 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "planarity_orientation_descriptor",
    "formula": "q_PBF ** 0.25",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) increases with adsorbate non-planarity measured by PBF (mean heavy-atom distance from the best-fit plane). Planar molecules (PBF at or near 0, including linear rotors) can adsorb in wall-parallel flat configurations that retain some rotational freedom, whereas non-planar molecules lose orientational freedom more completely upon confinement. The descriptor D = q_PBF**0.25 is therefore positively associated with entropy loss.",
    "rationale": "PBF separates the heavy-atom shape classes that mass and volume do not: at fixed Vol, a planar molecule has admissible low-energy orientations that a three-dimensionally extended molecule lacks, so the residual adsorbed-phase rotational/configurational entropy differs. This is an empirical proxy association, not a statement that all-atom out-of-plane displacement is zero; the representation is the original implicit-H/heavy-atom one, and the 587 training rows with PBF = 0 include linear rotors and planar molecules for which the value is physically legitimate.",
    "falsification_criteria": "If, at fixed rotor class, inertia scale, and Vol, planar (PBF ~ 0) and non-planar adsorbates show equal entropy loss, the planarity-orientation mechanism is falsified. Competing mechanism: entropy loss is set by translational confinement (bottleneck and volume) with shape playing no independent role; a second competing prediction is the opposite sign, i.e. flat-lying planar adsorbates lose more orientational entropy because the wall pins the plane, which would make D negatively associated with entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF is an implicit-H/heavy-atom planarity proxy; zero is a legitimate physical value (planar or linear heavy-atom skeleton), not missing data, and no imputation is applied. It does not measure all-atom out-of-plane hydrogen displacement.",
      "physical_interpretation": "Native meaning: PBF in angstrom is the mean heavy-atom distance from the best-fit molecular plane. q_PBF is a dimensionless ratio to the fixed training-reference median (0.230844767 angstrom), used only for monotone association; q-unity carries no physical threshold meaning.",
      "boundary_behavior": "At PBF = 0 the descriptor is exactly 0 and finite; the 0.25 power is monotone and compresses the upper tail (max 0.656249528 angstrom) without introducing singularities. No division by a legitimate zero occurs anywhere in the expression.",
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

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "planarity_orientation_descriptor",
    "formula": "q_PBF ** 0.25",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) increases with adsorbate non-planarity measured by PBF (mean heavy-atom distance from the best-fit plane). Planar molecules (PBF at or near 0, including linear rotors) can adsorb in wall-parallel flat configurations that retain some rotational freedom, whereas non-planar molecules lose orientational freedom more completely upon confinement. The descriptor D = q_PBF**0.25 is therefore positively associated with entropy loss.",
    "rationale": "PBF separates the heavy-atom shape classes that mass and volume do not: at fixed Vol, a planar molecule has admissible low-energy orientations that a three-dimensionally extended molecule lacks, so the residual adsorbed-phase rotational/configurational entropy differs. This is an empirical proxy association, not a statement that all-atom out-of-plane displacement is zero; the representation is the original implicit-H/heavy-atom one, and the 587 training rows with PBF = 0 include linear rotors and planar molecules for which the value is physically legitimate.",
    "falsification_criteria": "If, at fixed rotor class, inertia scale, and Vol, planar (PBF ~ 0) and non-planar adsorbates show equal entropy loss, the planarity-orientation mechanism is falsified. Competing mechanism: entropy loss is set by translational confinement (bottleneck and volume) with shape playing no independent role; a second competing prediction is the opposite sign, i.e. flat-lying planar adsorbates lose more orientational entropy because the wall pins the plane, which would make D negatively associated with entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF is an implicit-H/heavy-atom planarity proxy; zero is a legitimate physical value (planar or linear heavy-atom skeleton), not missing data, and no imputation is applied. It does not measure all-atom out-of-plane hydrogen displacement.",
      "physical_interpretation": "Native meaning: PBF in angstrom is the mean heavy-atom distance from the best-fit molecular plane. q_PBF is a dimensionless ratio to the fixed training-reference median (0.230844767 angstrom), used only for monotone association; q-unity carries no physical threshold meaning.",
      "boundary_behavior": "At PBF = 0 the descriptor is exactly 0 and finite; the 0.25 power is monotone and compresses the upper tail (max 0.656249528 angstrom) without introducing singularities. No division by a legitimate zero occurs anywhere in the expression.",
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
    "name": "planarity_orientation_descriptor",
    "formula": "q_PBF ** 0.25",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) increases with adsorbate non-planarity measured by PBF (mean heavy-atom distance from the best-fit plane). Planar molecules (PBF at or near 0, including linear rotors) can adsorb in wall-parallel flat configurations that retain some rotational freedom, whereas non-planar molecules lose orientational freedom more completely upon confinement. The descriptor D = q_PBF**0.25 is therefore positively associated with entropy loss.",
    "rationale": "PBF separates the heavy-atom shape classes that mass and volume do not: at fixed Vol, a planar molecule has admissible low-energy orientations that a three-dimensionally extended molecule lacks, so the residual adsorbed-phase rotational/configurational entropy differs. This is an empirical proxy association, not a statement that all-atom out-of-plane displacement is zero; the representation is the original implicit-H/heavy-atom one, and the 587 training rows with PBF = 0 include linear rotors and planar molecules for which the value is physically legitimate.",
    "falsification_criteria": "If, at fixed rotor class, inertia scale, and Vol, planar (PBF ~ 0) and non-planar adsorbates show equal entropy loss, the planarity-orientation mechanism is falsified. Competing mechanism: entropy loss is set by translational confinement (bottleneck and volume) with shape playing no independent role; a second competing prediction is the opposite sign, i.e. flat-lying planar adsorbates lose more orientational entropy because the wall pins the plane, which would make D negatively associated with entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF is an implicit-H/heavy-atom planarity proxy; zero is a legitimate physical value (planar or linear heavy-atom skeleton), not missing data, and no imputation is applied. It does not measure all-atom out-of-plane hydrogen displacement.",
      "physical_interpretation": "Native meaning: PBF in angstrom is the mean heavy-atom distance from the best-fit molecular plane. q_PBF is a dimensionless ratio to the fixed training-reference median (0.230844767 angstrom), used only for monotone association; q-unity carries no physical threshold meaning.",
      "boundary_behavior": "At PBF = 0 the descriptor is exactly 0 and finite; the 0.25 power is monotone and compresses the upper tail (max 0.656249528 angstrom) without introducing singularities. No division by a legitimate zero occurs anywhere in the expression.",
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

候选标识：`high/rag_agent/replicate-1/round-3/h3`

最终状态：scored；边际收益：-5.115790 pp；保留：False。

复核改动字段：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "included_path_cavity_descriptor",
    "formula": "q_lsd_p ** 0.25",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the largest included sphere along the free-sphere path (lsd_p, Dif): a larger included sphere along the corridor means more local free volume around the adsorption site, weaker positional and orientational constraint on a single molecule, and hence smaller entropy loss. The descriptor D = q_lsd_p**0.25 is therefore negatively associated with entropy loss.",
    "rationale": "lsd_p carries information complementary to the bottleneck lsd_f: two frameworks with similar bottlenecks can differ in the local free space along the path where the molecule actually resides, and it is this local free space that sets the configurational volume accessible at the adsorption minimum. This extends the retained bottleneck descriptor to the included-diameter mechanism family. Limitations: lsd_p is a hard-sphere geometric probe quantity along a free path, not a molecule-specific free volume and not the global cavity diameter Di; the round-1 lsd_p/lsd_f contrast was inconclusive, so the present hypothesis asserts an independent monotone role for lsd_p rather than for its ratio to lsd_f.",
    "falsification_criteria": "If the rank association between q_lsd_p**0.25 and entropy loss vanishes after controlling for q_lsd_f (i.e. lsd_p adds no information beyond the bottleneck), the included-cavity mechanism is falsified and confinement is bottleneck-dominated. A second falsifier is a sign reversal, which would indicate that large included cavities coincide with dense, strongly binding frameworks in this training domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "lsd_p (Zeo++ Dif) is the largest included sphere along the free-sphere path; it is neither the bottleneck Df nor necessarily the global maximum cavity Di, and it is a fixed-probe geometric quantity, not molecule-specific free volume. Kinetic passability does not by itself determine equilibrium entropy; the claim is a statistical association.",
      "physical_interpretation": "Native meaning: lsd_p in angstrom measures the local included free-sphere radius along the periodic free path. q_lsd_p is a dimensionless ratio to the fixed training-reference median (6.38663 angstrom); the 0.25 power is a monotone empirical smoothing with no universal physical meaning at q = 1.",
      "boundary_behavior": "lsd_p is strictly positive on the training domain (3.3452-15.5604 angstrom, zero_n = 0), so the negative-free expression is finite for every training row; no legitimate zero is divided by and no epsilon is introduced.",
      "vary_input": "lsd_p",
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
        "lsd_p"
      ],
      "quantity_roles": {
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
      "training_spearman": -0.5083341656890338,
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
    "slot_id": "h3",
    "name": "included_path_cavity_descriptor",
    "formula": "q_lsd_p ** 0.25",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the largest included sphere along the free-sphere path (lsd_p, Dif): a larger included sphere along the corridor means more local free volume around the adsorption site, weaker positional and orientational constraint on a single molecule, and hence smaller entropy loss. The descriptor D = q_lsd_p**0.25 is therefore negatively associated with entropy loss.",
    "rationale": "lsd_p carries information complementary to the bottleneck lsd_f: two frameworks with similar bottlenecks can differ in the local free space along the path where the molecule resides. Correction: lsd_p (Dif) and lsd_f (Df) are both reported as sphere diameters in angstrom, so the descriptor is a consistent diameter-scale quantity; the draft's 'radius' wording was a unit-scale mislabel, not a formula change. Limitations: lsd_p is a hard-sphere geometric probe quantity along a free path, not a molecule-specific free volume and not the global cavity diameter Di; the round-1 lsd_p/lsd_f ratio was inconclusive, so this hypothesis asserts an independent monotone role for lsd_p rather than for its ratio to lsd_f. Literature reports that larger-pore frameworks show smaller fractional entropy loss for alkanes (E02, E04), but cavity-diameter comparisons do not map one-to-one onto Dif, so the transfer remains a conditional association claim, not a validated causal law.",
    "falsification_criteria": "If the rank association between q_lsd_p**0.25 and entropy loss vanishes after controlling for q_lsd_f (i.e. lsd_p adds no information beyond the bottleneck), the included-cavity mechanism is falsified and confinement is bottleneck-dominated. A second falsifier is a sign reversal, which would indicate that large included cavities coincide with dense, strongly binding frameworks in this training domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "lsd_p (Zeo++ Dif) is the largest included sphere along the free-sphere path; it is neither the bottleneck Df nor necessarily the global maximum cavity Di, and it is a fixed-probe geometric quantity, not molecule-specific free volume. Kinetic passability does not by itself determine equilibrium entropy; the claim is a statistical association.",
      "physical_interpretation": "Native meaning: lsd_p in angstrom is the Zeo++ Dif quantity, reported on the same diameter scale as lsd_f (Df); the draft's 'included free-sphere radius' wording is corrected to 'included free-sphere diameter along the free-sphere path'. It is neither the bottleneck Df nor necessarily the global maximum cavity Di, and it is a fixed-probe geometric quantity, not molecule-specific free volume. q_lsd_p is a dimensionless ratio to the fixed training-reference median (6.38663 angstrom); the 0.25 power is a monotone empirical smoothing with no universal physical meaning at q = 1.",
      "boundary_behavior": "lsd_p is strictly positive on the training domain (native range 3.3452-15.5604 angstrom, zero_n = 0), so q_lsd_p > 0 for every training row. The expression q_lsd_p**0.25 uses only a positive fixed exponent, so it is finite everywhere on the training domain; no legitimate zero is divided by, no negative exponent is applied, and no epsilon is introduced.",
      "vary_input": "lsd_p",
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
        "lsd_p"
      ],
      "quantity_roles": {
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
      "training_spearman": -0.5083341656890338,
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
    "slot_id": "h3",
    "name": "included_path_cavity_descriptor",
    "formula": "q_lsd_p ** 0.25",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the largest included sphere along the free-sphere path (lsd_p, Dif): a larger included sphere along the corridor means more local free volume around the adsorption site, weaker positional and orientational constraint on a single molecule, and hence smaller entropy loss. The descriptor D = q_lsd_p**0.25 is therefore negatively associated with entropy loss.",
    "rationale": "lsd_p carries information complementary to the bottleneck lsd_f: two frameworks with similar bottlenecks can differ in the local free space along the path where the molecule resides. Correction: lsd_p (Dif) and lsd_f (Df) are both reported as sphere diameters in angstrom, so the descriptor is a consistent diameter-scale quantity; the draft's 'radius' wording was a unit-scale mislabel, not a formula change. Limitations: lsd_p is a hard-sphere geometric probe quantity along a free path, not a molecule-specific free volume and not the global cavity diameter Di; the round-1 lsd_p/lsd_f ratio was inconclusive, so this hypothesis asserts an independent monotone role for lsd_p rather than for its ratio to lsd_f. Literature reports that larger-pore frameworks show smaller fractional entropy loss for alkanes (E02, E04), but cavity-diameter comparisons do not map one-to-one onto Dif, so the transfer remains a conditional association claim, not a validated causal law.",
    "falsification_criteria": "If the rank association between q_lsd_p**0.25 and entropy loss vanishes after controlling for q_lsd_f (i.e. lsd_p adds no information beyond the bottleneck), the included-cavity mechanism is falsified and confinement is bottleneck-dominated. A second falsifier is a sign reversal, which would indicate that large included cavities coincide with dense, strongly binding frameworks in this training domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E04"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "lsd_p (Zeo++ Dif) is the largest included sphere along the free-sphere path; it is neither the bottleneck Df nor necessarily the global maximum cavity Di, and it is a fixed-probe geometric quantity, not molecule-specific free volume. Kinetic passability does not by itself determine equilibrium entropy; the claim is a statistical association.",
      "physical_interpretation": "Native meaning: lsd_p in angstrom is the Zeo++ Dif quantity, reported on the same diameter scale as lsd_f (Df); the draft's 'included free-sphere radius' wording is corrected to 'included free-sphere diameter along the free-sphere path'. It is neither the bottleneck Df nor necessarily the global maximum cavity Di, and it is a fixed-probe geometric quantity, not molecule-specific free volume. q_lsd_p is a dimensionless ratio to the fixed training-reference median (6.38663 angstrom); the 0.25 power is a monotone empirical smoothing with no universal physical meaning at q = 1.",
      "boundary_behavior": "lsd_p is strictly positive on the training domain (native range 3.3452-15.5604 angstrom, zero_n = 0), so q_lsd_p > 0 for every training row. The expression q_lsd_p**0.25 uses only a positive fixed exponent, so it is finite everywhere on the training domain; no legitimate zero is divided by, no negative exponent is applied, and no epsilon is introduced.",
      "vary_input": "lsd_p",
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
        "lsd_p"
      ],
      "quantity_roles": {
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
      "training_spearman": -0.5083341656890338,
      "target_association": "consistent",
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
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7342d031262bdf8cf5e759a2",
        "paper_id": "doi:10.1002/cphc.202300022",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:04264c83a4c746d4f901d812",
        "paper_id": "doi:10.1002/1521-3765_20010618_7_12_2521_aid-chem25210_3.0.co_2-n",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6c42e60d15e1bcc680c86db1",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:06a26a29dca2516a90c93ace",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:8b8a3218b92a9531ca89664e",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9805f0a944c903cd7580bbcb",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f79a9410c331a9d45a514d92",
        "paper_id": "doi:10.1039/d3cp02523c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f8666b352fe022c89c66a90b",
        "paper_id": "doi:10.1002/chem.201402665",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:00992287f63e5424d7a6b927",
        "paper_id": "doi:10.26434/chemrxiv.7538720.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:10c3cccf5a27daa756fbb656",
        "paper_id": "doi:10.1039/c003977b",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2b5bdff1874c6347d6ce0eaf",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:344ef3f3358677af422a5fea",
        "paper_id": "pmc:pmc6151591",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3dd1e3b89a0f8f43f056aaa3",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, the dimensionless entropy loss -ln(s_ads/s_gas) increases with the geometric mismatch between adsorbate extension and framework bottleneck: molecules whose largest heavy-atom pair distance (GeDi) is large relative to the free-path bottleneck (lsd_f, Df) experience a tighter fit, which suppresses translational and orientational sampling. The descriptor D = q_GeDi**0.25 * q_lsd_f**(-0.25) is therefore positively associated with entropy loss; equivalently s_ads/s_gas decreases as D increases. (q_GeDi ** 0.25) * (q_lsd_f ** (-0.25)) At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) increases with adsorbate non-planarity measured by PBF (mean heavy-atom distance from the best-fit plane). Planar molecules (PBF at or near 0, including linear rotors) can adsorb in wall-parallel flat configurations that retain some rotational freedom, whereas non-planar molecules lose orientational freedom more completely upon confinement. The descriptor D = q_PBF**0.25 is therefore positively associated with entropy loss. q_PBF ** 0.25 At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the largest included sphere along the free-sphere path (lsd_p, Dif): a larger included sphere along the corridor means more local free volume around the adsorption site, weaker positional and orientational constraint on a single molecule, and hence smaller entropy loss. The descriptor D = q_lsd_p**0.25 is therefore negatively associated with entropy loss. q_lsd_p ** 0.25   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:0d886a705a91409f8e891c53"
    ],
    "items": 10,
    "lexical_tokens": 4533,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [
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
