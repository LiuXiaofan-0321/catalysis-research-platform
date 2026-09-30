# high/small_kg_rag_agent/replicate-3/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/small_kg_rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`high/small_kg_rag_agent/replicate-3/round-1/h1`

最终状态：scored；边际收益：+3.350877 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.MW

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "size_vs_bottleneck_confinement",
    "formula": "log((q_MW * q_Vol) / q_lsd_f**2)",
    "hypothesis": "Falsifiable hypothesis (translation family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases monotonically with the adsorbate size (molecular weight and vdW volume, joint size proxy) normalized by the framework passing-bottleneck diameter Df; i.e., tighter windows relative to molecular size reduce translational/configurational freedom of the confined molecule relative to the gas.",
    "rationale": "Mechanism: translational confinement. A molecule whose size approaches the largest passing free sphere (Zeo++ Df, native lsd_f) samples fewer accessible configurations in the pore network than in the gas, increasing entropy loss = -ln(s_ads/s_gas). The descriptor is a pre-registered association claim only; it does not establish causality and Df is a hard-sphere geometric bottleneck proxy, not the global cavity diameter Di and not an energetic quantity. Normalization honesty: q_MW, q_Vol, q_lsd_f are row-varying ratios X/X_ref with fixed positive training-reference medians (X_ref = 74.07316494 g/mol, 67.24 angstrom^3, 5.16326 angstrom); X/q_X = X_ref is constant and never used. Limitations: MW and Vol are correlated size proxies, so their product double-counts size; the descriptor is empirical, and exponents (1, 1, 2) are fixed numerical choices, not fitted constants with universal meaning.",
    "falsification_criteria": "Refutation boundary: if, within fixed lsd_f quantile bands (e.g., 0-0.25, 0.25-0.75, 0.75-1.0 of the training domain), the residual association between this descriptor and entropy loss/R is not positive, or the sign of the association flips across lsd_f regimes, the translational-confinement hypothesis is falsified. Competing mechanism: entropy loss dominated by framework energy-site heterogeneity or adsorbate-framework interaction stiffness (enthalpic/rotational origin), in which case a translation-only descriptor should show no stable association. Numerical correlation alone would not validate the mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Assumes (i) MW and Vol jointly rank effective molecular cross-section relevant to a hard-sphere bottleneck; (ii) Df (largest passing free sphere) is an adequate bottleneck proxy for translational access; (iii) heavy-atom geometry descriptors transfer to real adsorbates including hydrogens. All three are approximations: MW/Vol conflate mass and size, Df ignores thermal framework flexibility and specific adsorption-site geometry, and the descriptor says nothing about entropy loss direction at fixed structure under loading.",
      "physical_interpretation": "Native meanings: MW and Vol are adsorbate size; lsd_f is the bottleneck free-sphere diameter along a periodic free path, not the included cavity diameter. The log argument (q_MW*q_Vol)/q_lsd_f**2 is dimensionless and strictly positive on the training domain. No q-unity threshold (descriptor value 0) is claimed to be a physical equality condition; it is merely the reference-median point. entropy_direction here refers to entropy loss per R: increasing vary_input (lsd_f) decreases the descriptor and is hypothesized to decrease entropy loss.",
      "boundary_behavior": "MW, Vol, and lsd_f have strictly positive training minima (16.0313, 20.424, 0.85684), so every training row yields a finite value with no zero division and no imputation. As lsd_f grows toward its domain maximum, the descriptor decreases smoothly (log) without singularity; as MW/Vol grow, it increases smoothly. Behavior outside the training domain is an extrapolation and is not claimed physical.",
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
      "training_spearman": 0.6149071995727097,
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
    "name": "size_vs_bottleneck_confinement",
    "formula": "log(q_lsd_f**2 / q_Vol)",
    "hypothesis": "Falsifiable hypothesis (translation family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases monotonically with the adsorbate size (molecular weight and vdW volume, joint size proxy) normalized by the framework passing-bottleneck diameter Df; i.e., tighter windows relative to molecular size reduce translational/configurational freedom of the confined molecule relative to the gas.",
    "rationale": "Direction/expression correction of the translation-family draft. The original descriptor log((q_MW*q_Vol)/q_lsd_f**2) was confinement-signed and its training-only precheck contradicted the stored entropy_direction (Spearman +0.61, target_association 'contradicted'). Since hypothesis, mechanism_family (translation) and entropy_direction (decreasing) are fixed, the descriptor is inverted to a freedom proxy log(q_lsd_f**2/q_Vol) and simplified: MW is dropped because mass conflates mass with size (double-counting with Vol) and lacks graph support for this mechanism. Mechanism unchanged: tighter windows relative to molecular size restrict translational/configurational freedom, raising entropy loss = -ln(s_ads/s_gas); equivalently, larger passing bottleneck relative to molecular vdW volume lowers entropy loss. Df is a hard-sphere geometric bottleneck proxy, not the cavity diameter Di and not an energetic quantity; the descriptor is a pre-registered association claim only, exponents (1,2) are fixed numerical choices, not fitted universal constants.",
    "falsification_criteria": "Refutation boundary: if, within fixed lsd_f quantile bands (e.g., 0-0.25, 0.25-0.75, 0.75-1.0 of the training domain), the residual association between log(q_lsd_f**2/q_Vol) and entropy loss/R is not negative (i.e., entropy loss does not decrease as the freedom proxy grows), or the sign flips across lsd_f regimes, the translational-confinement hypothesis as parameterized here is falsified. Competing mechanism: entropy loss dominated by framework energy-site heterogeneity or adsorbate-framework interaction stiffness (enthalpic/rotational origin), in which case a translation-only freedom descriptor should show no stable association. Numerical correlation alone would not validate the mechanism; the precheck statistic of the prior confinement-signed form (+0.61) is descriptive evidence of association, not causal confirmation.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E10"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Assumes (i) vdW volume ranks the effective molecular cross-section relevant to a hard-sphere passing bottleneck; (ii) Df (largest passing free sphere) is an adequate bottleneck proxy for translational access; (iii) heavy-atom-derived adsorbate descriptors transfer to real adsorbates. All are approximations: Vol is a static geometric size proxy, Df ignores thermal framework flexibility and site-specific adsorption geometry, and the descriptor says nothing about loading dependence. MW was removed: mass is not itself a geometry proxy, it double-counted size alongside Vol, and no mechanism edge in the source graph supports MW for the translation family (graph edges support Vol and lsd_f/lsd_p).",
      "physical_interpretation": "Native meanings: lsd_f (Df) is the largest sphere that can pass through a periodic free path (bottleneck), NOT the global cavity diameter Di; Vol is the adsorbate vdW volume. q_lsd_f and q_Vol are row-varying ratios to fixed positive training-reference medians (5.16326 angstrom, 67.24 angstrom^3); X/q_X = X_ref is constant for positive X and never used; a q-ratio of 1 is a numerical reference point, not a physical equality threshold. The descriptor log(q_lsd_f**2/q_Vol) is a dimensionless 'translational freedom' proxy: it increases when the passing bottleneck is large relative to molecular volume. Direction correction: the previously stored descriptor was confinement-signed and its training-only precheck returned target_association 'contradicted' (Spearman +0.61 with entropy loss/R) relative to the stored entropy_direction 'decreasing'. With mechanism_family and entropy_direction fixed, the descriptor is inverted so that increasing vary_input (lsd_f) increases the descriptor and is hypothesized to decrease entropy loss per R (more configurational freedom, less entropy loss). This inversion is a descriptor-sign correction, not a validation: the precheck statistic is descriptive only and does not establish causality.",
      "boundary_behavior": "Vol (min 20.424 angstrom^3) and lsd_f (min 0.85684 angstrom) are strictly positive on the training domain, so log(q_lsd_f**2/q_Vol) is finite on every training row with no zero division and no imputation. The descriptor increases smoothly with lsd_f and decreases smoothly with Vol (log form, no singularities inside the domain). Behavior outside the training domain is extrapolation and is not claimed physical.",
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

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "size_vs_bottleneck_confinement",
    "formula": "log(q_Vol / q_lsd_f**2)",
    "hypothesis": "Falsifiable hypothesis (translation family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases monotonically with the adsorbate size (molecular weight and vdW volume, joint size proxy) normalized by the framework passing-bottleneck diameter Df; i.e., tighter windows relative to molecular size reduce translational/configurational freedom of the confined molecule relative to the gas.",
    "rationale": "Direction/expression correction of the translation-family draft. The original descriptor log((q_MW*q_Vol)/q_lsd_f**2) was confinement-signed and its training-only precheck contradicted the stored entropy_direction (Spearman +0.61, target_association 'contradicted'). Since hypothesis, mechanism_family (translation) and entropy_direction (decreasing) are fixed, the descriptor is inverted to a freedom proxy log(q_lsd_f**2/q_Vol) and simplified: MW is dropped because mass conflates mass with size (double-counting with Vol) and lacks graph support for this mechanism. Mechanism unchanged: tighter windows relative to molecular size restrict translational/configurational freedom, raising entropy loss = -ln(s_ads/s_gas); equivalently, larger passing bottleneck relative to molecular vdW volume lowers entropy loss. Df is a hard-sphere geometric bottleneck proxy, not the cavity diameter Di and not an energetic quantity; the descriptor is a pre-registered association claim only, exponents (1,2) are fixed numerical choices, not fitted universal constants.",
    "falsification_criteria": "Refutation boundary: if, within fixed lsd_f quantile bands (e.g., 0-0.25, 0.25-0.75, 0.75-1.0 of the training domain), the residual association between log(q_lsd_f**2/q_Vol) and entropy loss/R is not negative (i.e., entropy loss does not decrease as the freedom proxy grows), or the sign flips across lsd_f regimes, the translational-confinement hypothesis as parameterized here is falsified. Competing mechanism: entropy loss dominated by framework energy-site heterogeneity or adsorbate-framework interaction stiffness (enthalpic/rotational origin), in which case a translation-only freedom descriptor should show no stable association. Numerical correlation alone would not validate the mechanism; the precheck statistic of the prior confinement-signed form (+0.61) is descriptive evidence of association, not causal confirmation.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E10"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Assumes (i) vdW volume ranks the effective molecular cross-section relevant to a hard-sphere passing bottleneck; (ii) Df (largest passing free sphere) is an adequate bottleneck proxy for translational access; (iii) heavy-atom-derived adsorbate descriptors transfer to real adsorbates. All are approximations: Vol is a static geometric size proxy, Df ignores thermal framework flexibility and site-specific adsorption geometry, and the descriptor says nothing about loading dependence. MW was removed: mass is not itself a geometry proxy, it double-counted size alongside Vol, and no mechanism edge in the source graph supports MW for the translation family (graph edges support Vol and lsd_f/lsd_p).",
      "physical_interpretation": "Native meanings: lsd_f (Df) is the largest sphere that can pass through a periodic free path (bottleneck), NOT the global cavity diameter Di; Vol is the adsorbate vdW volume. q_lsd_f and q_Vol are row-varying ratios to fixed positive training-reference medians (5.16326 angstrom, 67.24 angstrom^3); X/q_X = X_ref is constant for positive X and never used; a q-ratio of 1 is a numerical reference point, not a physical equality threshold. The descriptor log(q_lsd_f**2/q_Vol) is a dimensionless 'translational freedom' proxy: it increases when the passing bottleneck is large relative to molecular volume. Direction correction: the previously stored descriptor was confinement-signed and its training-only precheck returned target_association 'contradicted' (Spearman +0.61 with entropy loss/R) relative to the stored entropy_direction 'decreasing'. With mechanism_family and entropy_direction fixed, the descriptor is inverted so that increasing vary_input (lsd_f) increases the descriptor and is hypothesized to decrease entropy loss per R (more configurational freedom, less entropy loss). This inversion is a descriptor-sign correction, not a validation: the precheck statistic is descriptive only and does not establish causality.",
      "boundary_behavior": "Vol (min 20.424 angstrom^3) and lsd_f (min 0.85684 angstrom) are strictly positive on the training domain, so q_Vol > 0 and q_lsd_f > 0 on every training row; the log argument q_Vol / q_lsd_f**2 is strictly positive and the descriptor is finite on all 2361 training rows with no division by zero, no imputation, and no added epsilon. The patched descriptor now decreases monotonically and smoothly as vary_input lsd_f increases (matching the locked descriptor_direction 'decreasing': d(descriptor)/d(lsd_f) < 0) and increases monotonically with Vol; with the locked entropy_direction 'decreasing' (d(entropy loss)/d(lsd_f) < 0), the descriptor acts as a confinement-signed size-vs-bottleneck proxy: larger molecular vdW volume relative to the passing-bottleneck squared corresponds to greater entropy loss, equivalently a larger passing bottleneck relative to molecular size lowers entropy loss. No singularities exist inside the training domain; behavior outside the training quantile range is extrapolation and is not claimed physical. The exponent 2 on the bottleneck and 1 on volume remain fixed numerical choices, not fitted universal constants; lsd_f (Df) is a hard-sphere bottleneck proxy, not the global cavity diameter Di and not an energetic quantity. This patch corrects only the expression sign convention to resolve the predeclared direction contradiction (opposite_n = 2361); any empirical association remains descriptive and does not establish causality.",
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
      "training_spearman": 0.6703897107878907,
      "target_association": "contradicted",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/small_kg_rag_agent/replicate-3/round-1/h2`

最终状态：scored；边际收益：-2.727854 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_inertia_confinement_branches",
    "formula": "rotor_case(0.0, log(q_PMI2 * q_PMI3), log(q_PMI2 * q_PMI3) + abs(log(q_PMI3 / q_PMI2)))",
    "hypothesis": "Falsifiable hypothesis (rotation family): at infinite dilution, adsorption entropy loss from hindered rotation grows with the magnitude of the adsorbate's two largest heavy-atom principal moments of inertia (PMI2, PMI3) and, for nonlinear rotors, additionally with inertia asymmetry |log(I3/I2)|; single-site rotors (e.g., methane, treated as a point site in the heavy-atom representation) are hypothesized to have negligible rotational-confinement entropy loss relative to extended rotors, so their branch contributes no rotational penalty.",
    "rationale": "Mechanism: hindered rotation. In cage/window geometries, rotational orientational freedom is partially frozen out; larger and more anisotropic rotors are hypothesized to lose more rotational entropy upon confinement. The rotor_case construct supplies explicit branches: single_site branch = constant 0.0 (no rotational proxy asserted; methane is single-site and true all-atom inertia is NOT claimed to be zero); linear branch = log(q_PMI2*q_PMI3) only, avoiding PMI1 which is a legitimate heavy-atom zero for linear molecules; nonlinear branch adds abs(log(q_PMI3/q_PMI2)) as an anisotropy term, using only PMI2/PMI3 which are strictly positive for nonlinear rows in the training domain. Limitations: PMI values are original implicit-H/heavy-atom proxies, not all-atom inertias; the mapping from heavy-atom inertia to true rotational entropy loss is an empirical proxy assumption; the branch forms and fixed exponents (1, 1) are numerical choices, not fitted physical constants, and branch behavior is smoothed/limited by the category labels rather than by a continuous physical variable.",
    "falsification_criteria": "Refutation boundary: (i) if the nonlinear branch shows no positive association between the anisotropy term abs(log(q_PMI3/q_PMI2)) and entropy loss/R at matched log(q_PMI2*q_PMI3), the hindered-rotor anisotropy mechanism is falsified; (ii) if linear-rotor rows show systematically larger entropy loss than nonlinear rows at equal branch descriptor values, the branch structure (not just the proxy) is falsified; (iii) if single-site rows (e.g., methane-like) show entropy-loss residuals indistinguishable from extended rotors at matched translational confinement (h1 descriptor), the assumed negligible rotational penalty for point-like sites is falsified. Competing mechanism: entropy loss governed by translational/accessibility geometry alone (h1/h3), with rotational proxies acting only as hidden size surrogates.",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom (implicit-H) principal moments; legitimate exact zeros exist (PMI1 zero for 113 rows incl. linear/point-like, PMI2/PMI3 zero for 54 single-site rows). The rotor_case branches (single_site: constant 0.0; linear: log(q_PMI2*q_PMI3); nonlinear: log(q_PMI2*q_PMI3)+abs(log(q_PMI3/q_PMI2))) are an empirical branch-limit device with normalized tolerance 1e-10, not a physical discontinuity. Assumes heavy-atom inertia ranks hindered-rotor entropy loss; this does not transfer to all-atom rotor thermodynamics and ignores framework-site anisotropy.",
      "physical_interpretation": "Native meanings: PMI2, PMI3 are the two largest heavy-atom principal moments of inertia (angstrom^2*amu). q_PMI2 and q_PMI3 are row-varying ratios to fixed reference medians (93.79729089, 125.4948325 angstrom^2*amu); X/q_X = X_ref is constant and never used. Log arguments are strictly positive within their branches, so the descriptor is dimensionless. The single-site branch value 0.0 is a branch offset, not a physical claim of zero all-atom inertia or zero entropy loss. entropy_direction: increasing vary_input (PMI2) increases the descriptor and is hypothesized to increase entropy loss per R.",
      "boundary_behavior": "Finite on every training row by branch construction: the single_site branch is the constant 0.0; the linear branch uses only PMI2/PMI3 (positive for linear rows; PMI1 legitimate zeros are never divided by or logged); the nonlinear branch uses only PMI2/PMI3 (zero only among single-site rows, excluded from that branch). At the PMI1 -> 0 boundary (linear-like limit) the descriptor tends smoothly to the linear branch value because PMI1 never enters; at PMI2 -> 0 (single-site limit) the nonlinear expression is undefined, which is exactly why the branch excludes it — this is an honest empirical branch limit, not a physical law.",
      "vary_input": "PMI2",
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
        2299.281763
      ],
      "training_spearman": 0.38139847647818115,
      "target_association": "consistent",
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
    "slot_id": "h2",
    "name": "rotor_inertia_confinement_branches",
    "formula": "rotor_case(0.0, log(q_PMI2 * q_PMI3), log(q_PMI2 * q_PMI3) + abs(log(q_PMI3 / q_PMI2)))",
    "hypothesis": "Falsifiable hypothesis (rotation family): at infinite dilution, adsorption entropy loss from hindered rotation grows with the magnitude of the adsorbate's two largest heavy-atom principal moments of inertia (PMI2, PMI3) and, for nonlinear rotors, additionally with inertia asymmetry |log(I3/I2)|; single-site rotors (e.g., methane, treated as a point site in the heavy-atom representation) are hypothesized to have negligible rotational-confinement entropy loss relative to extended rotors, so their branch contributes no rotational penalty.",
    "rationale": "Mechanism: hindered rotation. In cage/window geometries, rotational orientational freedom is partially frozen out; larger and more anisotropic rotors are hypothesized to lose more rotational entropy upon confinement. The rotor_case construct supplies explicit branches: single_site branch = constant 0.0 (no rotational proxy asserted; methane is single-site and true all-atom inertia is NOT claimed to be zero); linear branch = log(q_PMI2*q_PMI3) only, avoiding PMI1 which is a legitimate heavy-atom zero for linear molecules; nonlinear branch adds abs(log(q_PMI3/q_PMI2)) as an anisotropy term, using only PMI2/PMI3 which are strictly positive for nonlinear rows in the training domain. Limitations: PMI values are original implicit-H/heavy-atom proxies, not all-atom inertias; the mapping from heavy-atom inertia to true rotational entropy loss is an empirical proxy assumption; the branch forms and fixed exponents (1, 1) are numerical choices, not fitted physical constants, and branch behavior is smoothed/limited by the category labels rather than by a continuous physical variable.",
    "falsification_criteria": "Refutation boundary: (i) if the nonlinear branch shows no positive association between the anisotropy term abs(log(q_PMI3/q_PMI2)) and entropy loss/R at matched log(q_PMI2*q_PMI3), the hindered-rotor anisotropy mechanism is falsified; (ii) if linear-rotor rows show systematically larger entropy loss than nonlinear rows at equal branch descriptor values, the branch structure (not just the proxy) is falsified; (iii) if single-site rows (e.g., methane-like) show entropy-loss residuals indistinguishable from extended rotors at matched translational confinement (h1 descriptor), the assumed negligible rotational penalty for point-like sites is falsified. Competing mechanism: entropy loss governed by translational/accessibility geometry alone (h1/h3), with rotational proxies acting only as hidden size surrogates.",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom (implicit-H) principal moments; legitimate exact zeros exist (PMI1 zero for 113 rows incl. linear/point-like, PMI2/PMI3 zero for 54 single-site rows). The rotor_case branches (single_site: constant 0.0; linear: log(q_PMI2*q_PMI3); nonlinear: log(q_PMI2*q_PMI3)+abs(log(q_PMI3/q_PMI2))) are an empirical branch-limit device with normalized tolerance 1e-10, not a physical discontinuity. Assumes heavy-atom inertia ranks hindered-rotor entropy loss; this does not transfer to all-atom rotor thermodynamics and ignores framework-site anisotropy.",
      "physical_interpretation": "Native meanings: PMI2, PMI3 are the two largest heavy-atom principal moments of inertia (angstrom^2*amu). q_PMI2 and q_PMI3 are row-varying ratios to fixed reference medians (93.79729089, 125.4948325 angstrom^2*amu); X/q_X = X_ref is constant and never used. Log arguments are strictly positive within their branches, so the descriptor is dimensionless. The single-site branch value 0.0 is a branch offset, not a physical claim of zero all-atom inertia or zero entropy loss. entropy_direction: increasing vary_input (PMI2) increases the descriptor and is hypothesized to increase entropy loss per R.",
      "boundary_behavior": "Finite on every training row by branch construction: the single_site branch is the constant 0.0; the linear branch uses only PMI2/PMI3 (positive for linear rows; PMI1 legitimate zeros are never divided by or logged); the nonlinear branch uses only PMI2/PMI3 (zero only among single-site rows, excluded from that branch). At the PMI1 -> 0 boundary (linear-like limit) the descriptor tends smoothly to the linear branch value because PMI1 never enters; at PMI2 -> 0 (single-site limit) the nonlinear expression is undefined, which is exactly why the branch excludes it — this is an honest empirical branch limit, not a physical law.",
      "vary_input": "PMI2",
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
        2299.281763
      ],
      "training_spearman": 0.38139847647818115,
      "target_association": "consistent",
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
    "slot_id": "h2",
    "name": "rotor_inertia_confinement_branches",
    "formula": "rotor_case(0.0, log(q_PMI2 * q_PMI3), log(q_PMI2 * q_PMI3) + abs(log(q_PMI3 / q_PMI2)))",
    "hypothesis": "Falsifiable hypothesis (rotation family): at infinite dilution, adsorption entropy loss from hindered rotation grows with the magnitude of the adsorbate's two largest heavy-atom principal moments of inertia (PMI2, PMI3) and, for nonlinear rotors, additionally with inertia asymmetry |log(I3/I2)|; single-site rotors (e.g., methane, treated as a point site in the heavy-atom representation) are hypothesized to have negligible rotational-confinement entropy loss relative to extended rotors, so their branch contributes no rotational penalty.",
    "rationale": "Mechanism: hindered rotation. In cage/window geometries, rotational orientational freedom is partially frozen out; larger and more anisotropic rotors are hypothesized to lose more rotational entropy upon confinement. The rotor_case construct supplies explicit branches: single_site branch = constant 0.0 (no rotational proxy asserted; methane is single-site and true all-atom inertia is NOT claimed to be zero); linear branch = log(q_PMI2*q_PMI3) only, avoiding PMI1 which is a legitimate heavy-atom zero for linear molecules; nonlinear branch adds abs(log(q_PMI3/q_PMI2)) as an anisotropy term, using only PMI2/PMI3 which are strictly positive for nonlinear rows in the training domain. Limitations: PMI values are original implicit-H/heavy-atom proxies, not all-atom inertias; the mapping from heavy-atom inertia to true rotational entropy loss is an empirical proxy assumption; the branch forms and fixed exponents (1, 1) are numerical choices, not fitted physical constants, and branch behavior is smoothed/limited by the category labels rather than by a continuous physical variable.",
    "falsification_criteria": "Refutation boundary: (i) if the nonlinear branch shows no positive association between the anisotropy term abs(log(q_PMI3/q_PMI2)) and entropy loss/R at matched log(q_PMI2*q_PMI3), the hindered-rotor anisotropy mechanism is falsified; (ii) if linear-rotor rows show systematically larger entropy loss than nonlinear rows at equal branch descriptor values, the branch structure (not just the proxy) is falsified; (iii) if single-site rows (e.g., methane-like) show entropy-loss residuals indistinguishable from extended rotors at matched translational confinement (h1 descriptor), the assumed negligible rotational penalty for point-like sites is falsified. Competing mechanism: entropy loss governed by translational/accessibility geometry alone (h1/h3), with rotational proxies acting only as hidden size surrogates.",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom (implicit-H) principal moments; legitimate exact zeros exist (PMI1 zero for 113 rows incl. linear/point-like, PMI2/PMI3 zero for 54 single-site rows). The rotor_case branches (single_site: constant 0.0; linear: log(q_PMI2*q_PMI3); nonlinear: log(q_PMI2*q_PMI3)+abs(log(q_PMI3/q_PMI2))) are an empirical branch-limit device with normalized tolerance 1e-10, not a physical discontinuity. Assumes heavy-atom inertia ranks hindered-rotor entropy loss; this does not transfer to all-atom rotor thermodynamics and ignores framework-site anisotropy.",
      "physical_interpretation": "Native meanings: PMI2, PMI3 are the two largest heavy-atom principal moments of inertia (angstrom^2*amu). q_PMI2 and q_PMI3 are row-varying ratios to fixed reference medians (93.79729089, 125.4948325 angstrom^2*amu); X/q_X = X_ref is constant and never used. Log arguments are strictly positive within their branches, so the descriptor is dimensionless. The single-site branch value 0.0 is a branch offset, not a physical claim of zero all-atom inertia or zero entropy loss. entropy_direction: increasing vary_input (PMI2) increases the descriptor and is hypothesized to increase entropy loss per R.",
      "boundary_behavior": "Finite on every training row by branch construction: the single_site branch is the constant 0.0; the linear branch uses only PMI2/PMI3 (positive for linear rows; PMI1 legitimate zeros are never divided by or logged); the nonlinear branch uses only PMI2/PMI3 (zero only among single-site rows, excluded from that branch). At the PMI1 -> 0 boundary (linear-like limit) the descriptor tends smoothly to the linear branch value because PMI1 never enters; at PMI2 -> 0 (single-site limit) the nonlinear expression is undefined, which is exactly why the branch excludes it — this is an honest empirical branch limit, not a physical law.",
      "vary_input": "PMI2",
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
        2299.281763
      ],
      "training_spearman": 0.38139847647818115,
      "target_association": "consistent",
      "perturbation": 3.956905037,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/small_kg_rag_agent/replicate-3/round-1/h3`

最终状态：scored；边际收益：+0.777770 pp；保留：False。

复核改动字段：falsification_criteria, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "cage_window_contrast_caging",
    "formula": "q_lsd_p / q_lsd_f",
    "hypothesis": "Falsifiable hypothesis (connectivity family): at infinite dilution, adsorption entropy loss increases with the contrast between the largest included sphere along the free-sphere path (Dif, native lsd_p) and the passing bottleneck (Df, native lsd_f); frameworks with cage-like cavities much larger than their connecting windows ('cage-trap' topology) restrict the adsorbed molecule to a smaller effective configuration space relative to the gas than frameworks with gradually varying pore diameters, at fixed accessible volume.",
    "rationale": "Mechanism: connectivity/caging. A high Dif/Df contrast indicates large local cavities connected through narrow windows; the hypothesis is that such topology confines the molecule's accessible positional/orientational configurations (caging), raising entropy loss = -ln(s_ads/s_gas) even when total accessible volume is comparable. Limitations: lsd_p (Dif) is the largest included sphere ALONG the free-sphere path, not necessarily the global cavity diameter Di, and lsd_f is the bottleneck Df; both are hard-sphere geometric proxies on a fixed numerical scale and ignore thermal effects, site-specific adsorption positions, and multi-window cage topologies that hard-sphere path analysis may miss. The ratio is a pure shape/contrast proxy and carries no enthalpic information. No claim is made that kinetic window-passing rates determine the equilibrium entropy; escape kinetics and equilibrium configurational entropy are distinct quantities.",
    "falsification_criteria": "Refutation boundary: if, within fixed AV (probe accessible volume) quantile bands, the association between q_lsd_p/q_lsd_f and entropy loss/R is not positive, or is dominated by lsd_p alone with lsd_f contributing no independent effect at matched accessible volume, the caging-contrast hypothesis is falsified. Competing mechanism: entropy loss controlled primarily by total accessible free volume (AV) or surface area (ASA) rather than by window-to-cavity contrast; if an AV-only descriptor outperforms the contrast at matched regimes, connectivity caging is not the operative mechanism. Correlation with the descriptor does not validate the caging mechanism causally.",
    "novelty_status": "new_combination",
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
      "proxy_assumptions": "Assumes (i) the Dif/Df contrast ranks cage-trap topology relevant to configurational confinement at infinite dilution; (ii) hard-sphere path geometry (Zeo++ Df, Dif) transfers to finite-temperature, finite-size real adsorbates; (iii) contrast effects are separable from absolute pore size and accessible volume effects (AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume, so AV is deliberately excluded from the formula). These assumptions are approximations; Dif along a single free path may miss multiple windows or side pockets.",
      "physical_interpretation": "Native meanings: lsd_f (Df) is the largest sphere that can pass through a periodic free path (bottleneck); lsd_p (Dif) is the largest included sphere along that path — neither is the global cavity diameter Di and neither enters D0 directly here. q_lsd_p and q_lsd_f are row-varying ratios to fixed reference medians (6.38663 and 5.16326 angstrom); X/q_X = X_ref is constant and never used. The ratio is dimensionless and positive on the training domain. The reference point q_lsd_p/q_lsd_f = 1 is a numerical reference, not a physical cage/window equality threshold. entropy_direction: increasing vary_input (lsd_p) increases the descriptor and is hypothesized to increase entropy loss per R.",
      "boundary_behavior": "Both lsd_f (min 0.85684 angstrom) and lsd_p (min 3.3452 angstrom) are strictly positive on the training domain, so every training row yields a finite value with no zero division and no imputation. As lsd_f -> large at fixed lsd_p, the descriptor decreases smoothly toward small positive values; as lsd_p grows toward its domain maximum (15.5604), the descriptor grows smoothly. Behavior outside the training quantile range [0.0, 1.0] is extrapolation and not claimed physical.",
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
    "name": "cage_window_contrast_caging",
    "formula": "q_lsd_p / q_lsd_f",
    "hypothesis": "Falsifiable hypothesis (connectivity family): at infinite dilution, adsorption entropy loss increases with the contrast between the largest included sphere along the free-sphere path (Dif, native lsd_p) and the passing bottleneck (Df, native lsd_f); frameworks with cage-like cavities much larger than their connecting windows ('cage-trap' topology) restrict the adsorbed molecule to a smaller effective configuration space relative to the gas than frameworks with gradually varying pore diameters, at fixed accessible volume.",
    "rationale": "Mechanism: connectivity/caging. A high Dif/Df contrast indicates large local cavities connected through narrow windows; the pre-registered hypothesis is that such topology confines accessible positional/orientational configurations, raising entropy loss = -ln(s_ads/s_gas) even at comparable accessible volume. Audit note (training-only precheck, retained as the pre-registered baseline): Spearman between q_lsd_p/q_lsd_f and entropy loss/R was approximately -0.019 (target_association 'inconclusive'), i.e., no detectable monotone training association in the declared direction; the descriptor is adsorbate-independent pure framework contrast, so it can only express framework-to-framework variation. Limitations: lsd_p (Dif) is the largest included sphere ALONG the free-sphere path, not necessarily the global cavity diameter Di, and lsd_f is the bottleneck Df; both are hard-sphere geometric proxies ignoring thermal effects, site-specific adsorption positions, and multi-window topologies. The ratio carries no enthalpic information. No claim is made that kinetic window-passing rates determine equilibrium entropy; escape kinetics and equilibrium configurational entropy are distinct quantities.",
    "falsification_criteria": "Pre-registered refutation boundary, now including the observed training-only precheck: the contrast descriptor already shows no monotone association with entropy loss/R in training data (Spearman ~ -0.019, 'inconclusive'); the hypothesis is falsified if, within fixed AV quantile bands, this non-association persists as a genuine null (or a stable negative association emerges) rather than a positive association, or if the descriptor is dominated by lsd_p alone with lsd_f contributing no independent effect at matched accessible volume. Competing mechanism: entropy loss controlled primarily by total accessible free volume or surface area, or by cavity size itself (smaller cavities losing more entropy per the FER/FAU comparison), rather than by window-to-cavity contrast; if an AV-only or cavity-size descriptor outperforms the contrast at matched regimes, connectivity caging is not the operative mechanism. Correlation with the descriptor would not validate the caging mechanism causally.",
    "novelty_status": "new_combination",
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
      "proxy_assumptions": "Assumes (i) the Dif/Df contrast ranks cage-trap topology relevant to configurational confinement at infinite dilution; (ii) hard-sphere path geometry (Zeo++ Df, Dif) transfers to finite-temperature, finite-size real adsorbates; (iii) contrast effects are separable from absolute pore size and accessible volume effects (AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume, so AV is deliberately excluded from the formula). These assumptions are approximations; Dif along a single free path may miss multiple windows or side pockets.",
      "physical_interpretation": "Native meanings: lsd_f (Df) is the largest sphere that can pass through a periodic free path (bottleneck); lsd_p (Dif) is the largest included sphere along that path — neither is the global cavity diameter Di and neither enters D0 directly here. q_lsd_p and q_lsd_f are row-varying ratios to fixed reference medians (6.38663 and 5.16326 angstrom); X/q_X = X_ref is constant and never used. The ratio is dimensionless and positive on the training domain. The reference point q_lsd_p/q_lsd_f = 1 is a numerical reference, not a physical cage/window equality threshold. entropy_direction: increasing vary_input (lsd_p) increases the descriptor and is hypothesized to increase entropy loss per R.",
      "boundary_behavior": "Both lsd_f (min 0.85684 angstrom) and lsd_p (min 3.3452 angstrom) are strictly positive on the training domain, so every training row yields a finite value with no zero division and no imputation. As lsd_f -> large at fixed lsd_p, the descriptor decreases smoothly toward small positive values; as lsd_p grows toward its domain maximum (15.5604), the descriptor grows smoothly. Behavior outside the training quantile range [0.0, 1.0] is extrapolation and not claimed physical.",
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
    "name": "cage_window_contrast_caging",
    "formula": "q_lsd_p / q_lsd_f",
    "hypothesis": "Falsifiable hypothesis (connectivity family): at infinite dilution, adsorption entropy loss increases with the contrast between the largest included sphere along the free-sphere path (Dif, native lsd_p) and the passing bottleneck (Df, native lsd_f); frameworks with cage-like cavities much larger than their connecting windows ('cage-trap' topology) restrict the adsorbed molecule to a smaller effective configuration space relative to the gas than frameworks with gradually varying pore diameters, at fixed accessible volume.",
    "rationale": "Mechanism: connectivity/caging. A high Dif/Df contrast indicates large local cavities connected through narrow windows; the pre-registered hypothesis is that such topology confines accessible positional/orientational configurations, raising entropy loss = -ln(s_ads/s_gas) even at comparable accessible volume. Audit note (training-only precheck, retained as the pre-registered baseline): Spearman between q_lsd_p/q_lsd_f and entropy loss/R was approximately -0.019 (target_association 'inconclusive'), i.e., no detectable monotone training association in the declared direction; the descriptor is adsorbate-independent pure framework contrast, so it can only express framework-to-framework variation. Limitations: lsd_p (Dif) is the largest included sphere ALONG the free-sphere path, not necessarily the global cavity diameter Di, and lsd_f is the bottleneck Df; both are hard-sphere geometric proxies ignoring thermal effects, site-specific adsorption positions, and multi-window topologies. The ratio carries no enthalpic information. No claim is made that kinetic window-passing rates determine equilibrium entropy; escape kinetics and equilibrium configurational entropy are distinct quantities.",
    "falsification_criteria": "Pre-registered refutation boundary, now including the observed training-only precheck: the contrast descriptor already shows no monotone association with entropy loss/R in training data (Spearman ~ -0.019, 'inconclusive'); the hypothesis is falsified if, within fixed AV quantile bands, this non-association persists as a genuine null (or a stable negative association emerges) rather than a positive association, or if the descriptor is dominated by lsd_p alone with lsd_f contributing no independent effect at matched accessible volume. Competing mechanism: entropy loss controlled primarily by total accessible free volume or surface area, or by cavity size itself (smaller cavities losing more entropy per the FER/FAU comparison), rather than by window-to-cavity contrast; if an AV-only or cavity-size descriptor outperforms the contrast at matched regimes, connectivity caging is not the operative mechanism. Correlation with the descriptor would not validate the caging mechanism causally.",
    "novelty_status": "new_combination",
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
      "proxy_assumptions": "Assumes (i) the Dif/Df contrast ranks cage-trap topology relevant to configurational confinement at infinite dilution; (ii) hard-sphere path geometry (Zeo++ Df, Dif) transfers to finite-temperature, finite-size real adsorbates; (iii) contrast effects are separable from absolute pore size and accessible volume effects (AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume, so AV is deliberately excluded from the formula). These assumptions are approximations; Dif along a single free path may miss multiple windows or side pockets.",
      "physical_interpretation": "Native meanings: lsd_f (Df) is the largest sphere that can pass through a periodic free path (bottleneck); lsd_p (Dif) is the largest included sphere along that path — neither is the global cavity diameter Di and neither enters D0 directly here. q_lsd_p and q_lsd_f are row-varying ratios to fixed reference medians (6.38663 and 5.16326 angstrom); X/q_X = X_ref is constant and never used. The ratio is dimensionless and positive on the training domain. The reference point q_lsd_p/q_lsd_f = 1 is a numerical reference, not a physical cage/window equality threshold. entropy_direction: increasing vary_input (lsd_p) increases the descriptor and is hypothesized to increase entropy loss per R.",
      "boundary_behavior": "Both lsd_f (min 0.85684 angstrom) and lsd_p (min 3.3452 angstrom) are strictly positive on the training domain, so every training row yields a finite value with no zero division and no imputation. As lsd_f -> large at fixed lsd_p, the descriptor decreases smoothly toward small positive values; as lsd_p grows toward its domain maximum (15.5604), the descriptor grows smoothly. Behavior outside the training quantile range [0.0, 1.0] is extrapolation and not claimed physical.",
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
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
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
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6ca1143916b8e66b0a19e889",
        "paper_id": "pmc:pmc8879942",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd75db1400cf2ce6171ef0f6",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d270ec3d6183be4a3de52cd8",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ecf3b350af8d5c09a9a10048",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1feac0dfc9ab0dc8a9a0c9eb",
        "paper_id": "doi:10.1063/1.4706520",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2a36986d9ba7dbe05f02c0d2",
        "paper_id": "doi:10.1021/acs.langmuir.5b03015",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:37dd34c64af45105c20d0042",
        "paper_id": "doi:10.1063/1.1697382",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6dfd4c9dd250f5414a82938f",
        "paper_id": "doi:10.1021/acs.jctc.7b00716",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:72dfcce988c17185f87c465c",
        "paper_id": "doi:10.1021/jp1096663",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9a3907e626bcdef0bc5bb0cb",
        "paper_id": "doi:10.1002/chem.201705627",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd4794ce62afc7c5c5d7b896",
        "paper_id": "doi:10.1021/acs.jpclett.2c03302",
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
        "record_id": "chunk:ec1e8193a4e127c7e5a5ba8d",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement Falsifiable hypothesis (translation family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases monotonically with the adsorbate size (molecular weight and vdW volume, joint size proxy) normalized by the framework passing-bottleneck diameter Df; i.e., tighter windows relative to molecular size reduce translational/configurational freedom of the confined molecule relative to the gas. log((q_MW * q_Vol) / q_lsd_f**2) Falsifiable hypothesis (rotation family): at infinite dilution, adsorption entropy loss from hindered rotation grows with the magnitude of the adsorbate's two largest heavy-atom principal moments of inertia (PMI2, PMI3) and, for nonlinear rotors, additionally with inertia asymmetry |log(I3/I2)|; single-site rotors (e.g., methane, treated as a point site in the heavy-atom representation) are hypothesized to have negligible rotational-confinement entropy loss relative to extended rotors, so their branch contributes no rotational penalty. rotor_case(0.0, log(q_PMI2 * q_PMI3), log(q_PMI2 * q_PMI3) + abs(log(q_PMI3 / q_PMI2))) Falsifiable hypothesis (connectivity family): at infinite dilution, adsorption entropy loss increases with the contrast between the largest included sphere along the free-sphere path (Dif, native lsd_p) and the passing bottleneck (Df, native lsd_f); frameworks with cage-like cavities much larger than their connecting windows ('cage-trap' topology) restrict the adsorbed molecule to a smaller effective configuration space relative to the gas than frameworks with gradually varying pore diameters, at fixed accessible volume. q_lsd_p / q_lsd_f",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e9ae89d415e72e1faf77faf0"
    ],
    "items": 10,
    "lexical_tokens": 4644,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [
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
      "id": "E10"
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
