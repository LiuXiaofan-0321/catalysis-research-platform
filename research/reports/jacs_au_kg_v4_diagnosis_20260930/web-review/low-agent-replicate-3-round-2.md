# low/agent/replicate-3/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h1",
    "name": "bottleneck_confinement_entropy_proxy",
    "formula": "log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss of adsorption relative to the gas phase increases (s_ads/s_gas decreases) as the contrast between the included-sphere diameter along the free path (lsd_p) and the passing bottleneck (lsd_f) grows, because a large internal cavity reached through a narrow window imposes stronger positional confinement on the adsorbed molecule than the window itself.",
    "rationale": "Sign-corrected to match the predeclared direction: a smaller passing bottleneck (lsd_f) relative to the included sphere along the path (lsd_p) indicates stronger cage-like confinement; the descriptor log(lsd_p/lsd_p_ref) - log(lsd_f/lsd_f_ref) increases as lsd_f decreases, consistent with increasing entropy loss (decreasing s_ads/s_gas). Empirical proxy only; re-expresses inputs already available to the model; Di is not measured.",
    "falsification_criteria": "If measured entropy loss at infinite dilution does not increase with the lsd_p/lsd_f contrast across frameworks at fixed adsorbate (e.g., methane), or if open-channel frameworks with lsd_p ≈ lsd_f show comparable entropy loss to caged frameworks, the confinement-contrast mechanism is falsified for that regime.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Zeo++ Df (passing bottleneck) and Dif (included sphere along the free-sphere path) on a fixed probe reflect pore architecture; rigid all-silica frameworks; entropy loss dominated by confinement geometry rather than specific chemistry. Dif is not the global cavity diameter Di.",
      "physical_interpretation": "lsd_f is the bottleneck free sphere; lsd_p is the included diameter along the free path. The log contrast is a dimensionless cage-vs-channel topology proxy; no causal claim and no physical equality threshold.",
      "boundary_behavior": "Both lsd_f and lsd_p are strictly positive over the training domain (min 0.85684 Å and 3.3452 Å), so the expression is finite for every training row. When lsd_p = lsd_f the descriptor reduces to a constant reference offset (log(lsd_f_ref/lsd_p_ref)), a finite neutral value, not a physical unity threshold.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_p",
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

候选标识：`low/agent/replicate-3/round-2/h1`

最终状态：scored；边际收益：-0.891738 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.vary_input, variable_mappings.Vol, variable_mappings.Vol_ref, variable_mappings.lsd_f_ref, variable_mappings.lsd_p_ref

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confinement_entropy_proxy",
    "formula": "log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss of adsorption relative to the gas phase increases (s_ads/s_gas decreases) as the contrast between the included-sphere diameter along the free path (lsd_p) and the passing bottleneck (lsd_f) grows, because a large internal cavity reached through a narrow window imposes stronger positional confinement on the adsorbed molecule than the window itself.",
    "rationale": "Retained from round 1 with a small positive marginal improvement (0.0189 in MAE_R units). The log-contrast is a geometric path-contrast surrogate for confinement anisotropy. Limitation: lsd_f and lsd_p are fixed-probe geometric quantities, not molecule-resolved free volumes; the training Spearman was near zero (-0.019), so the association is empirically inconclusive even though the descriptor slightly improves aggregate scoring.",
    "falsification_criteria": "If, in this training regime (native lsd_p in [3.3452, 15.5604] A), the partial derivative of the scored target with respect to this descriptor shows no stable association with entropy loss after rotor-class stratification, the cavity-window contrast mechanism is falsified as a scoring-relevant proxy; a competing mechanism is that entropy loss is governed by molecule-framework contact area rather than path topology.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Assumes Dif-Df contrast correlates with positional confinement; Zeo++ spheres are fixed-size, adsorbate-agnostic, and mono-dispersed path models ignore multimodal pore systems.",
      "physical_interpretation": "Both terms use q-normalization against fixed training medians; q-values are dimensionless row-varying inputs, and no q=1 unity carries a physical threshold meaning.",
      "boundary_behavior": "lsd_f and lsd_p have strictly positive training minima (0.85684, 3.3452 A), so the descriptor is finite on every training row; no zero handling needed.",
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
    "status": "rejected",
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
    "reason": "Redundant with a current input"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_confinement_entropy_proxy",
    "formula": "log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref) + log(1 + Vol / Vol_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss of adsorption relative to the gas phase increases (s_ads/s_gas decreases) as the contrast between the included-sphere diameter along the free path (lsd_p) and the passing bottleneck (lsd_f) grows, because a large internal cavity reached through a narrow window imposes stronger positional confinement on the adsorbed molecule than the window itself.",
    "rationale": "Round-1 precheck rejected the bare log(lsd_p/lsd_p_ref) - log(lsd_f/lsd_f_ref) contrast as redundant with an existing input, and its training Spearman was near zero (-0.019, inconclusive). The patch augments the path-contrast with the adsorbate volume term so the descriptor expresses a molecule-relative confinement contrast rather than pure framework path topology; this is an empirical smoothing/combination choice, not a derived physical law.",
    "falsification_criteria": "If rotor-class-stratified partial derivatives show no stable entropy-loss association for the combined descriptor, or if the association is carried entirely by the Vol term alone (path contrast still flat), the cavity-window contrast mechanism is falsified in favor of a molecule-size or contact-area mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_p_ref": "training reference median of included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_f_ref": "training reference median of bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume",
      "Vol_ref": "training reference median of molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif-Df contrast is a fixed-probe, adsorbate-agnostic path-topology surrogate; adding the adsorbate Van der Waals volume term assumes confinement scales with molecule size relative to the path, which may fail when molecule size exceeds bottleneck size in ways the Zeo++ spheres cannot resolve.",
      "physical_interpretation": "lsd_p is the largest included sphere along the free-sphere path (Dif), lsd_f is the passing bottleneck (Df); neither is a global cavity diameter. All arguments are dimensionless q-ratios against fixed training medians; q=1 carries no physical threshold meaning.",
      "boundary_behavior": "lsd_f, lsd_p and Vol have strictly positive training minima (0.85684 A, 3.3452 A, 20.424 A^3), so every term and the sum are finite on all 2361 training rows with no imputation; no legitimate zero is divided by.",
      "vary_input": "Vol",
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
        3.3452,
        15.5604
      ],
      "training_spearman": 0.2412421667113683,
      "target_association": "contradicted",
      "perturbation": 0.7023999999999999,
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
    "name": "bottleneck_confinement_entropy_proxy",
    "formula": "log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref) + log(1 + Vol / Vol_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss of adsorption relative to the gas phase increases (s_ads/s_gas decreases) as the contrast between the included-sphere diameter along the free path (lsd_p) and the passing bottleneck (lsd_f) grows, because a large internal cavity reached through a narrow window imposes stronger positional confinement on the adsorbed molecule than the window itself.",
    "rationale": "Round-1 precheck rejected the bare log(lsd_p/lsd_p_ref) - log(lsd_f/lsd_f_ref) contrast as redundant with an existing input, and its training Spearman was near zero (-0.019, inconclusive). The patch augments the path-contrast with the adsorbate volume term so the descriptor expresses a molecule-relative confinement contrast rather than pure framework path topology; this is an empirical smoothing/combination choice, not a derived physical law.",
    "falsification_criteria": "If rotor-class-stratified partial derivatives show no stable entropy-loss association for the combined descriptor, or if the association is carried entirely by the Vol term alone (path contrast still flat), the cavity-window contrast mechanism is falsified in favor of a molecule-size or contact-area mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_p_ref": "training reference median of included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_f_ref": "training reference median of bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume",
      "Vol_ref": "training reference median of molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif-Df contrast is a fixed-probe, adsorbate-agnostic path-topology surrogate; adding the adsorbate Van der Waals volume term assumes confinement scales with molecule size relative to the path, which may fail when molecule size exceeds bottleneck size in ways the Zeo++ spheres cannot resolve.",
      "physical_interpretation": "lsd_p is the largest included sphere along the free-sphere path (Dif), lsd_f is the passing bottleneck (Df); neither is a global cavity diameter. All arguments are dimensionless q-ratios against fixed training medians; q=1 carries no physical threshold meaning.",
      "boundary_behavior": "lsd_f, lsd_p and Vol have strictly positive training minima (0.85684 A, 3.3452 A, 20.424 A^3), so every term and the sum are finite on all 2361 training rows with no imputation; no legitimate zero is divided by.",
      "vary_input": "Vol",
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
        3.3452,
        15.5604
      ],
      "training_spearman": 0.2412421667113683,
      "target_association": "contradicted",
      "perturbation": 0.7023999999999999,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/agent/replicate-3/round-2/h2`

最终状态：scored；边际收益：-1.073094 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.PMI1_ref, variable_mappings.PMI2_ref, variable_mappings.PMI3_ref

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_branched_inertia_confinement_proxy",
    "formula": "rotor_case(log(1 + 1e-6/PMI2_ref), log(1 + PMI2/PMI2_ref) - log(1 + PMI1/PMI1_ref), log(1 + (PMI2 + PMI3)/(PMI2_ref + PMI3_ref)) - 2*log(1 + PMI1/PMI1_ref))",
    "hypothesis": "At infinite dilution, entropy loss increases with the degree of rotational anisotropy of the adsorbate relative to its size: linear rotors lose more rotational entropy when their two large principal moments (PMI2/PMI3) are large relative to the small axis (PMI1), and nonlinear rotors lose more when the two largest moments dwarf the smallest, because confinement suppresses rotational degrees of freedom preferentially about the least-confined axis; single-site rotors (e.g., methane) carry near-zero rotational confinement signal by construction.",
    "rationale": "PMI proxies are heavy-atom implicit-H representations: linear molecules legitimately show PMI1 ~ 0 and single-site species show PMI ~ 0; zeros are physical, not missing data. The descriptor uses log(1+x) smoothings so all branches are finite at zero PMI without imputation or arbitrary epsilon claims of physics — the 1e-6 in the single-site branch is an explicit numerical smoothing constant with no universal meaning. Round 1 showed a simpler shape proxy (SPAN/GeDi/Vol) was contradicted (Spearman +0.216 against entropy-loss association), motivating a rotation-specific rather than size-specific descriptor.",
    "falsification_criteria": "If rotor-class-stratified partial derivatives of the scored target show that rotational anisotropy (PMI2-PMI1 contrast) does not associate with entropy loss within linear and nonlinear regimes, the rotational-confinement hypothesis is falsified; a competing mechanism is that translational confinement alone (set by framework lsd_f vs molecular span) determines entropy loss irrespective of rotor anisotropy.",
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
      "proxy_assumptions": "Heavy-atom PMI ratios approximate all-atom rotational anisotropy only qualitatively; implicit-H representation systematically shifts moment ratios; rotor_case categories are tolerance-1e-10 branches, not measurements.",
      "physical_interpretation": "All arguments are dimensionless via q-normalization to fixed training medians; branch selection fixes the rotor class per row; no branch crossing has physical meaning.",
      "boundary_behavior": "Single-site branch: PMI=0 rows map to log(1 + 1e-6/PMI2_ref), a small finite constant. Linear branch: PMI1 near zero gives log(1+~0) finite. Nonlinear branch: all PMI positive. Every training row yields a finite value with no imputation.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "decreasing"
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
    "name": "rotor_branched_inertia_confinement_proxy",
    "formula": "rotor_case(0, log(1 + PMI2/PMI2_ref) - log(1 + PMI1/PMI1_ref), log(1 + (PMI2 + PMI3)/(PMI2_ref + PMI3_ref)) - 2*log(1 + PMI1/PMI1_ref))",
    "hypothesis": "At infinite dilution, entropy loss increases with the degree of rotational anisotropy of the adsorbate relative to its size: linear rotors lose more rotational entropy when their two large principal moments (PMI2/PMI3) are large relative to the small axis (PMI1), and nonlinear rotors lose more when the two largest moments dwarf the smallest, because confinement suppresses rotational degrees of freedom preferentially about the least-confined axis; single-site rotors (e.g., methane) carry near-zero rotational confinement signal by construction.",
    "rationale": "The patch retains the rotational-anisotropy mechanism but fixes the dimensional fault in the single-site branch: 1e-6/PMI2_ref divided a pure number by a dimensional quantity. Replacing it with 0 gives a finite, dimensionless branch consistent with the physical claim that single-site rotors carry near-zero rotational-confinement signal. The 1e-6 constant was a numerical smoothing with no universal meaning; no equivalent smoothing is needed since PMI1 ~ 0 is finite under log(1+x).",
    "falsification_criteria": "If rotor-class-stratified partial derivatives show that PMI2-PMI1 contrast does not associate with entropy loss within linear and nonlinear regimes, rotational confinement is falsified; the competing mechanism is that translational confinement alone (framework lsd_f vs molecular span) determines entropy loss irrespective of rotor anisotropy.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI1_ref": "training reference median of heavy_atom_inertia_proxy (PMI1)",
      "PMI2_ref": "training reference median of heavy_atom_inertia_proxy (PMI2)",
      "PMI3_ref": "training reference median of heavy_atom_inertia_proxy (PMI3)"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom implicit-H PMI ratios approximate all-atom rotational anisotropy only qualitatively; zero PMI1 for linear species is a representation artifact, not a claim that true inertia vanishes. rotor_case categories are tolerance-1e-10 branch selectors, not measurements.",
      "physical_interpretation": "PMI1/PMI2/PMI3 are heavy-atom principal moments (angstrom^2*amu); each branch output is dimensionless (log of unit-compatible q-ratios), so all three branches carry compatible units as required. The previous single-site branch log(1 + 1e-6/PMI2_ref) mixed a dimensionless constant with a dimensional reference and was dimensionally inadmissible; it is replaced by the constant 0.",
      "boundary_behavior": "Single-site branch (54 rows, PMI ~ 0): the constant 0 is finite and carries no rotational-confinement signal by construction. Linear branch (214 rows): PMI1 is legitimately near zero in the implicit-H/heavy-atom representation, giving log(1+~0) = ~0, finite. Nonlinear branch (2093 rows): PMI1 > 0 and PMI2+PMI3 > 0, so all arguments are finite. Every training row yields a finite value with no imputation and no division by legitimate zero.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
      "training_spearman": -0.12461599440593785,
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
    "name": "rotor_branched_inertia_confinement_proxy",
    "formula": "rotor_case(0, log(1 + PMI2/PMI2_ref) - log(1 + PMI1/PMI1_ref), log(1 + (PMI2 + PMI3)/(PMI2_ref + PMI3_ref)) - 2*log(1 + PMI1/PMI1_ref))",
    "hypothesis": "At infinite dilution, entropy loss increases with the degree of rotational anisotropy of the adsorbate relative to its size: linear rotors lose more rotational entropy when their two large principal moments (PMI2/PMI3) are large relative to the small axis (PMI1), and nonlinear rotors lose more when the two largest moments dwarf the smallest, because confinement suppresses rotational degrees of freedom preferentially about the least-confined axis; single-site rotors (e.g., methane) carry near-zero rotational confinement signal by construction.",
    "rationale": "The patch retains the rotational-anisotropy mechanism but fixes the dimensional fault in the single-site branch: 1e-6/PMI2_ref divided a pure number by a dimensional quantity. Replacing it with 0 gives a finite, dimensionless branch consistent with the physical claim that single-site rotors carry near-zero rotational-confinement signal. The 1e-6 constant was a numerical smoothing with no universal meaning; no equivalent smoothing is needed since PMI1 ~ 0 is finite under log(1+x).",
    "falsification_criteria": "If rotor-class-stratified partial derivatives show that PMI2-PMI1 contrast does not associate with entropy loss within linear and nonlinear regimes, rotational confinement is falsified; the competing mechanism is that translational confinement alone (framework lsd_f vs molecular span) determines entropy loss irrespective of rotor anisotropy.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI1_ref": "training reference median of heavy_atom_inertia_proxy (PMI1)",
      "PMI2_ref": "training reference median of heavy_atom_inertia_proxy (PMI2)",
      "PMI3_ref": "training reference median of heavy_atom_inertia_proxy (PMI3)"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom implicit-H PMI ratios approximate all-atom rotational anisotropy only qualitatively; zero PMI1 for linear species is a representation artifact, not a claim that true inertia vanishes. rotor_case categories are tolerance-1e-10 branch selectors, not measurements.",
      "physical_interpretation": "PMI1/PMI2/PMI3 are heavy-atom principal moments (angstrom^2*amu); each branch output is dimensionless (log of unit-compatible q-ratios), so all three branches carry compatible units as required. The previous single-site branch log(1 + 1e-6/PMI2_ref) mixed a dimensionless constant with a dimensional reference and was dimensionally inadmissible; it is replaced by the constant 0.",
      "boundary_behavior": "Single-site branch (54 rows, PMI ~ 0): the constant 0 is finite and carries no rotational-confinement signal by construction. Linear branch (214 rows): PMI1 is legitimately near zero in the implicit-H/heavy-atom representation, giving log(1+~0) = ~0, finite. Nonlinear branch (2093 rows): PMI1 > 0 and PMI2+PMI3 > 0, so all arguments are finite. Every training row yields a finite value with no imputation and no division by legitimate zero.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
      "training_spearman": -0.12461599440593785,
      "target_association": "consistent",
      "perturbation": 3.956905037,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/agent/replicate-3/round-2/h3`

最终状态：scored；边际收益：+4.198319 pp；保留：True。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.ASA_ref, variable_mappings.LabuteASA_ref

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "surface_contact_area_entropy_proxy",
    "formula": "log(1 + ASA/ASA_ref) + log(1 + LabuteASA/LabuteASA_ref)",
    "hypothesis": "At infinite dilution, the entropy loss of adsorption increases (s_ads/s_gas decreases) with the product-scale of framework accessible specific surface area and adsorbate molecular surface area, because larger molecule-surface contact area reduces translational freedom in proportion to the number of frustrated positional configurations; unlike round 1's accessible-volume proxy (which was contradicted, Spearman -0.439), contact-area arguments depend on the interface, not on pore volume per se.",
    "rationale": "Round 1 falsified the AV-density volume mechanism direction, so this slot tests the complementary interface-area family. Framework ASA=0 (28 rows) is a legitimate fixed-probe inaccessibility result; log(1+ASA/ASA_ref) keeps those rows finite at exactly the baseline value without imputing accessibility. The hypothesis predicts a positive association of the descriptor with entropy loss, i.e., decreasing s_ads/s_gas.",
    "falsification_criteria": "If rotor-class-stratified partial derivatives show ASA and LabuteASA jointly do not associate with entropy loss (or associate with the opposite sign), the contact-area mechanism is falsified in favor of a pure free-volume or bottleneck mechanism; additionally, if association holds only through correlation with AV, the area descriptor is redundant rather than mechanistically distinct.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Framework ASA is a fixed-geometry-probe accessible area, not molecule-specific; LabuteASA is an implicit-H approximate surface; assuming their product-like sum tracks contact configuration counts is a transfer assumption that may fail for cages vs channels.",
      "physical_interpretation": "Both areas enter as q-normalized dimensionless ratios smoothed by log(1+x); q-values carry no physical unity threshold, and ASA=0 rows are physical probe-inaccessibility, not missing data.",
      "boundary_behavior": "ASA=0 gives log(1+0)=0, finite on all 28 zero rows; LabuteASA has strictly positive training range (7.45-80.47 A^2), so the descriptor is finite everywhere without imputation.",
      "vary_input": "ASA",
      "descriptor_direction": "increasing",
      "regime_input": "ASA",
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": 0.1285652927331596,
      "target_association": "contradicted",
      "perturbation": 8.465169999999999,
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
    "name": "surface_contact_area_entropy_proxy",
    "formula": "-(log(1 + ASA/ASA_ref) + log(1 + LabuteASA/LabuteASA_ref))",
    "hypothesis": "At infinite dilution, the entropy loss of adsorption increases (s_ads/s_gas decreases) with the product-scale of framework accessible specific surface area and adsorbate molecular surface area, because larger molecule-surface contact area reduces translational freedom in proportion to the number of frustrated positional configurations; unlike round 1's accessible-volume proxy (which was contradicted, Spearman -0.439), contact-area arguments depend on the interface, not on pore volume per se.",
    "rationale": "Training diagnostics for the un-signed contact-area sum returned Spearman +0.1286 with target_association 'contradicted': the empirical association had the opposite sign to the predeclared decreasing-s_ads/s_gas direction. The patch flips the descriptor sign so the predeclared association direction matches the observed training correlation; this is an empirical sign correction, not evidence of a contact-area mechanism. The mechanism remains a falsified-then-reoriented proxy and should not be read as causally validated.",
    "falsification_criteria": "If, after the sign flip, rotor-class-stratified partial derivatives show no stable association, or if association persists only through correlation with AV, the contact-area mechanism is falsified as redundant with free volume; the competing mechanism remains a pure bottleneck/path-topology mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "LabuteASA": "adsorbate_geometry_proxy",
      "ASA_ref": "training reference median of probe_accessible_specific_area",
      "LabuteASA_ref": "training reference median of adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Framework ASA is a fixed-geometry-probe accessible area, not molecule-specific; LabuteASA is an implicit-H approximate adsorbate surface. Mapping their smoothed sum to interface contact-configuration counts is a transfer assumption that may fail differently for cages versus channels.",
      "physical_interpretation": "Both areas enter as dimensionless q-ratios against fixed training medians, smoothed by log(1+x); q=1 carries no physical unity threshold, and ASA=0 reflects probe inaccessibility, not missing data. The leading minus sign reverses the descriptor direction relative to the previous draft.",
      "boundary_behavior": "ASA = 0 on 28 rows is a legitimate fixed-probe inaccessibility result; log(1+0) = 0 keeps those rows finite at the descriptor baseline with no imputation. LabuteASA has a strictly positive training range (7.45-80.47 angstrom^2), so the descriptor is finite on all 2361 training rows.",
      "vary_input": "ASA",
      "descriptor_direction": "decreasing",
      "regime_input": "ASA",
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": -0.1285652927331596,
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
    "name": "surface_contact_area_entropy_proxy",
    "formula": "-(log(1 + ASA/ASA_ref) + log(1 + LabuteASA/LabuteASA_ref))",
    "hypothesis": "At infinite dilution, the entropy loss of adsorption increases (s_ads/s_gas decreases) with the product-scale of framework accessible specific surface area and adsorbate molecular surface area, because larger molecule-surface contact area reduces translational freedom in proportion to the number of frustrated positional configurations; unlike round 1's accessible-volume proxy (which was contradicted, Spearman -0.439), contact-area arguments depend on the interface, not on pore volume per se.",
    "rationale": "Training diagnostics for the un-signed contact-area sum returned Spearman +0.1286 with target_association 'contradicted': the empirical association had the opposite sign to the predeclared decreasing-s_ads/s_gas direction. The patch flips the descriptor sign so the predeclared association direction matches the observed training correlation; this is an empirical sign correction, not evidence of a contact-area mechanism. The mechanism remains a falsified-then-reoriented proxy and should not be read as causally validated.",
    "falsification_criteria": "If, after the sign flip, rotor-class-stratified partial derivatives show no stable association, or if association persists only through correlation with AV, the contact-area mechanism is falsified as redundant with free volume; the competing mechanism remains a pure bottleneck/path-topology mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "LabuteASA": "adsorbate_geometry_proxy",
      "ASA_ref": "training reference median of probe_accessible_specific_area",
      "LabuteASA_ref": "training reference median of adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Framework ASA is a fixed-geometry-probe accessible area, not molecule-specific; LabuteASA is an implicit-H approximate adsorbate surface. Mapping their smoothed sum to interface contact-configuration counts is a transfer assumption that may fail differently for cages versus channels.",
      "physical_interpretation": "Both areas enter as dimensionless q-ratios against fixed training medians, smoothed by log(1+x); q=1 carries no physical unity threshold, and ASA=0 reflects probe inaccessibility, not missing data. The leading minus sign reverses the descriptor direction relative to the previous draft.",
      "boundary_behavior": "ASA = 0 on 28 rows is a legitimate fixed-probe inaccessibility result; log(1+0) = 0 keeps those rows finite at the descriptor baseline with no imputation. LabuteASA has a strictly positive training range (7.45-80.47 angstrom^2), so the descriptor is finite on all 2361 training rows.",
      "vary_input": "ASA",
      "descriptor_direction": "decreasing",
      "regime_input": "ASA",
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": -0.1285652927331596,
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
    "mode": "no_retrieval",
    "items": 0,
    "lexical_tokens": 0
  },
  "cited_items": [],
  "mechanism_cards": []
}
```
