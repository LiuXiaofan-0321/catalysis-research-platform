# high/agent/replicate-1/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h1",
    "name": "volume_accessibility_confinement_loss",
    "formula": "log10(1 + q_Vol / (1 + q_AV))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with adsorbate van der Waals volume and decreases with the fixed-probe accessible specific volume of the framework: bulky adsorbates in frameworks with small probe-accessible volume lose the largest fraction of translational/configurational entropy.",
    "rationale": "Translational entropy loss upon confinement is expected to scale with how much molecular volume must be accommodated in a restricted pore space. AV is a fixed-probe, mass-specific accessibility proxy, not a molecule-specific free volume, so the ratio q_Vol/(1+q_AV) is an empirical confinement index: it grows with adsorbate size and shrinks as the framework offers more probe-accessible volume. The log10(1+.) form is a monotone empirical smoothing that keeps the descriptor finite and bounded for all training rows; its scale has no universal physical meaning.",
    "falsification_criteria": "If entropy loss (MAE-scored as s_ads/s_gas deviation) shows no monotone association with this descriptor across the training domain, or if frameworks with equal AV but different connectivity (e.g., different lsd_f at matched AV) systematically invert the predicted ordering, the volume-accessibility confinement mechanism is falsified for this dataset and a connectivity- or shape-dominated mechanism should be tested instead.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "AV is a fixed-geometric-probe accessibility proxy; zero AV for the fixed probe does not imply zero molecular adsorption space, so AV enters only through the finite, monotone factor 1/(1+q_AV). Vol is an all-atom van der Waals volume proxy. Neither proxy captures framework chemistry beyond geometry.",
      "physical_interpretation": "q_Vol normalizes adsorbate size by the fixed training-reference median Vol_ref; q_AV normalizes fixed-probe accessibility by AV_ref. Both are dimensionless row-varying inputs. No unity threshold in q carries physical meaning; the descriptor is an empirical monotone index.",
      "boundary_behavior": "At AV=0 (28 training rows), q_AV=0 and the descriptor reduces to log10(1+q_Vol), finite and positive; this is justified because zero fixed-probe accessibility is a probe limitation, not proof of zero adsorption entropy loss. q_Vol is bounded away from zero in training (Vol min 20.424), so the descriptor is finite everywhere.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  {
    "slot_id": "h2",
    "name": "planarity_orientational_constraint_loss",
    "formula": "log10(1 + q_PBF * q_Vol / (1 + q_ASA))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with the out-of-plane deviation of the adsorbate (PBF) and with adsorbate volume, and decreases with the probe-accessible specific surface area of the framework: non-planar, bulky adsorbates in frameworks with small accessible surface have fewer energetically compatible orientations and contact configurations near the pore walls, losing more rotational/configurational entropy.",
    "rationale": "PBF measures the mean atom distance from the best-fit molecular plane in the original implicit-H/heavy-atom representation, so it separates planar from three-dimensional adsorbates; this is a shape-family mechanism complementary to the retained volume/accessibility (translation-like) descriptor. Framework ASA enters as an inverse openness proxy: frameworks with more probe-accessible surface per mass offer more wall-adjacent configurations, reducing the orientational constraint. Limitations: PBF is a heavy-atom representation quantity with legitimate zeros and is not all-atom geometry; ASA is a fixed-probe quantity whose zero does not imply zero adsorption space; the multiplicative form is an empirical smoothing choice, not a derived law.",
    "falsification_criteria": "If entropy loss at fixed volume and framework is independent of PBF (planar and non-planar adsorbates equivalent), or if it decreases with PBF, the orientational-constraint hypothesis is falsified. If replacing the product q_PBF*q_Vol by q_PBF alone or by q_Vol alone yields equal or better association, the joint size-planarity interaction is not supported.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "Vol": "molecular_vdw_volume",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF proxies orientational anisotropy of the adsorbate in the implicit-H/heavy-atom representation (not true all-atom shape); Vol proxies adsorbate size; ASA is a fixed-probe accessibility proxy, not a molecule-specific surface. The descriptor does not encode energetics or framework flexibility.",
      "physical_interpretation": "PBF is the mean atom distance from the best-fit plane in angstrom; Vol is van der Waals volume in angstrom^3; ASA is probe-accessible specific area in m^2/g. All q-terms are row-varying ratios to fixed positive training-reference medians; (1 + q_ASA) is a dimensionless guard because ASA has legitimate zeros (28 rows), and no q-unity threshold is asserted. The declared regime is expressed as training-quantile fractions [0.0, 1.0], i.e. the full native PBF range [0.0, 0.656249528] angstrom, covering 100 percent of the 2361 training rows.",
      "boundary_behavior": "At PBF = 0 (planar adsorbates, 587 training rows) the descriptor is exactly log10(1) = 0, finite and interpretable as no planarity-based constraint; at ASA = 0 the denominator is 1, so the descriptor stays finite; Vol > 0 everywhere. No division by a legitimate zero occurs and no imputation is used.",
      "vary_input": "PBF",
      "descriptor_direction": "increasing",
      "regime_input": "PBF",
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

候选标识：`high/agent/replicate-1/round-3/h1`

最终状态：scored；边际收益：-3.750821 pp；保留：False。

复核改动字段：scientific_test.boundary_behavior

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "rotational_confined_inertia_loss",
    "formula": "rotor_case(0, log10(1 + q_PMI2 / q_lsd_f), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3) / (3 * q_lsd_f)))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the rotational contribution to adsorption entropy loss relative to the gas phase increases with the heavy-atom principal moment-of-inertia proxies of the adsorbate and with the degree of framework confinement as proxied by the inverse of the Zeo++ free-path bottleneck diameter (lsd_f): adsorbates with larger rotational inertia adsorbed in frameworks with narrower passing bottlenecks have fewer energetically compatible rotational states and lose more rotational entropy. The rotor_case branches encode that single-site species contribute no rotational-inertia term under this proxy scheme, linear species are governed by their single perpendicular moment proxy (PMI2), and nonlinear species by the mean of all three moment proxies.",
    "rationale": "Rotational entropy loss is a distinct mechanism family from the two retained volume/planarity descriptors. The numerator is a rotor-class-specific inertia aggregate; the denominator q_lsd_f is strictly positive over the whole training domain (native lsd_f min 0.85684 angstrom), so every row yields a finite value with no imputation. Limitations: PMI proxies come from the original implicit-H/heavy-atom representation, not true all-atom inertia; the single-site branch outputs the constant 0 as a modeling choice, which must not be read as a claim that true all-atom inertia or rotational entropy is zero. q-normalization uses fixed positive training-reference medians; no physical unity threshold is implied by q values.",
    "falsification_criteria": "If the predeclared positive association between this descriptor and entropy loss is contradicted in training diagnostics (negative Spearman sign, or target_association 'contradicted'), or if the marginal improvement over the retained volume-accessibility and planarity descriptors is negative after controlling for redundancy with q_Vol-driven features, the rotational-confinement coupling hypothesis loses support for this dataset and should be revised or dropped. A competing mechanism is that rotational loss is set by local wall curvature rather than the global free-path bottleneck, which would predict no association once lsd_p or ASA are conditioned on.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies are treated as orderings for rotational inertia; rotor_case single-site branch is fixed at 0 by construction (rotor_class counts: 54 single-site, 214 linear, 2093 nonlinear). The nonlinear_rotor_expression is the explicit rotor_case branch log10(1 + (q_PMI1 + q_PMI2 + q_PMI3)/(3*q_lsd_f)) for nonlinear species; the linear branch log10(1 + q_PMI2/q_lsd_f) uses only the perpendicular moment proxy because a linear rotor's rotational partition function depends on one degenerate perpendicular moment; the single_site branch is 0. lsd_f is the passing-bottleneck free sphere Df, not the global cavity diameter Di, and not Dif.",
      "physical_interpretation": "All quantities enter via dimensionless q_X = X/X_ref ratios with fixed positive training-reference medians; log10 arguments are dimensionless. The predeclared proxy derivative is: holding rotor class and the other inputs fixed, d(descriptor)/d(PMI2) > 0 and d(descriptor)/d(lsd_f) < 0. The target is entropy loss = -(S_ads - S_gas)/R, so descriptor_direction 'increasing' with entropy_direction 'increasing' means larger inertia in tighter frameworks predicts larger entropy loss (smaller s_ads/s_gas). Correlations and partial derivatives do not establish causality.",
      "boundary_behavior": "At legitimate q_PMI = 0 rows (e.g., linear degenerate moments in the heavy-atom proxy), the numerator is 0 and log10(1+0) = 0, finite. The single-site branch is constant 0, matching the absence of a heavy-atom inertia proxy for methane-like species. q_lsd_f is strictly positive (native min 0.85684), so no division by zero occurs anywhere. For extreme inertia or narrow bottlenecks the descriptor grows only logarithmically, an empirical smoothing choice with no universal physical meaning attached to the fixed reference constants.",
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
        "PMI1",
        "PMI2",
        "PMI3",
        "lsd_f"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.5010126565750941,
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
    "slot_id": "h1",
    "name": "rotational_confined_inertia_loss",
    "formula": "rotor_case(0, log10(1 + q_PMI2 / q_lsd_f), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3) / (3 * q_lsd_f)))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the rotational contribution to adsorption entropy loss relative to the gas phase increases with the heavy-atom principal moment-of-inertia proxies of the adsorbate and with the degree of framework confinement as proxied by the inverse of the Zeo++ free-path bottleneck diameter (lsd_f): adsorbates with larger rotational inertia adsorbed in frameworks with narrower passing bottlenecks have fewer energetically compatible rotational states and lose more rotational entropy. The rotor_case branches encode that single-site species contribute no rotational-inertia term under this proxy scheme, linear species are governed by their single perpendicular moment proxy (PMI2), and nonlinear species by the mean of all three moment proxies.",
    "rationale": "Rotational entropy loss is a distinct mechanism family from the two retained volume/planarity descriptors. The numerator is a rotor-class-specific inertia aggregate; the denominator q_lsd_f is strictly positive over the whole training domain (native lsd_f min 0.85684 angstrom), so every row yields a finite value with no imputation. Limitations: PMI proxies come from the original implicit-H/heavy-atom representation, not true all-atom inertia; the single-site branch outputs the constant 0 as a modeling choice, which must not be read as a claim that true all-atom inertia or rotational entropy is zero. q-normalization uses fixed positive training-reference medians; no physical unity threshold is implied by q values.",
    "falsification_criteria": "If the predeclared positive association between this descriptor and entropy loss is contradicted in training diagnostics (negative Spearman sign, or target_association 'contradicted'), or if the marginal improvement over the retained volume-accessibility and planarity descriptors is negative after controlling for redundancy with q_Vol-driven features, the rotational-confinement coupling hypothesis loses support for this dataset and should be revised or dropped. A competing mechanism is that rotational loss is set by local wall curvature rather than the global free-path bottleneck, which would predict no association once lsd_p or ASA are conditioned on.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies are treated as orderings for rotational inertia; rotor_case single-site branch is fixed at 0 by construction (rotor_class counts: 54 single-site, 214 linear, 2093 nonlinear). The nonlinear_rotor_expression is the explicit rotor_case branch log10(1 + (q_PMI1 + q_PMI2 + q_PMI3)/(3*q_lsd_f)) for nonlinear species; the linear branch log10(1 + q_PMI2/q_lsd_f) uses only the perpendicular moment proxy because a linear rotor's rotational partition function depends on one degenerate perpendicular moment; the single_site branch is 0. lsd_f is the passing-bottleneck free sphere Df, not the global cavity diameter Di, and not Dif.",
      "physical_interpretation": "All quantities enter via dimensionless q_X = X/X_ref ratios with fixed positive training-reference medians; log10 arguments are dimensionless. The predeclared proxy derivative is: holding rotor class and the other inputs fixed, d(descriptor)/d(PMI2) > 0 and d(descriptor)/d(lsd_f) < 0. The target is entropy loss = -(S_ads - S_gas)/R, so descriptor_direction 'increasing' with entropy_direction 'increasing' means larger inertia in tighter frameworks predicts larger entropy loss (smaller s_ads/s_gas). Correlations and partial derivatives do not establish causality.",
      "boundary_behavior": "Zeros of the PMI proxies are legitimate and structurally interpretable: PMI1, PMI2 and PMI3 all vanish on the 54 single-site rows, and PMI1 (the axial moment about the molecular long axis) additionally vanishes on linear rows (PMI1 near_zero_n = 268 = 54 single-site + 214 linear), consistent with any strictly linear heavy-atom layout having zero moment about its own axis. Where a numerator is 0, log10(1+0) = 0 is finite; this includes the constant single_site branch. The linear branch deliberately uses PMI2, which is strictly positive on all linear rows (the 54 PMI2 zeros are exactly the single-site rows), so no zero numerator arises in that branch. q_lsd_f is strictly positive (native lsd_f min 0.85684 angstrom), so no division by zero occurs anywhere. Logarithmic growth at extreme inertia or narrow bottlenecks is an empirical smoothing choice; the fixed training-reference medians carry no universal physical threshold meaning.",
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
        "PMI1",
        "PMI2",
        "PMI3",
        "lsd_f"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.5010126565750941,
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
    "slot_id": "h1",
    "name": "rotational_confined_inertia_loss",
    "formula": "rotor_case(0, log10(1 + q_PMI2 / q_lsd_f), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3) / (3 * q_lsd_f)))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the rotational contribution to adsorption entropy loss relative to the gas phase increases with the heavy-atom principal moment-of-inertia proxies of the adsorbate and with the degree of framework confinement as proxied by the inverse of the Zeo++ free-path bottleneck diameter (lsd_f): adsorbates with larger rotational inertia adsorbed in frameworks with narrower passing bottlenecks have fewer energetically compatible rotational states and lose more rotational entropy. The rotor_case branches encode that single-site species contribute no rotational-inertia term under this proxy scheme, linear species are governed by their single perpendicular moment proxy (PMI2), and nonlinear species by the mean of all three moment proxies.",
    "rationale": "Rotational entropy loss is a distinct mechanism family from the two retained volume/planarity descriptors. The numerator is a rotor-class-specific inertia aggregate; the denominator q_lsd_f is strictly positive over the whole training domain (native lsd_f min 0.85684 angstrom), so every row yields a finite value with no imputation. Limitations: PMI proxies come from the original implicit-H/heavy-atom representation, not true all-atom inertia; the single-site branch outputs the constant 0 as a modeling choice, which must not be read as a claim that true all-atom inertia or rotational entropy is zero. q-normalization uses fixed positive training-reference medians; no physical unity threshold is implied by q values.",
    "falsification_criteria": "If the predeclared positive association between this descriptor and entropy loss is contradicted in training diagnostics (negative Spearman sign, or target_association 'contradicted'), or if the marginal improvement over the retained volume-accessibility and planarity descriptors is negative after controlling for redundancy with q_Vol-driven features, the rotational-confinement coupling hypothesis loses support for this dataset and should be revised or dropped. A competing mechanism is that rotational loss is set by local wall curvature rather than the global free-path bottleneck, which would predict no association once lsd_p or ASA are conditioned on.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI1": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies are treated as orderings for rotational inertia; rotor_case single-site branch is fixed at 0 by construction (rotor_class counts: 54 single-site, 214 linear, 2093 nonlinear). The nonlinear_rotor_expression is the explicit rotor_case branch log10(1 + (q_PMI1 + q_PMI2 + q_PMI3)/(3*q_lsd_f)) for nonlinear species; the linear branch log10(1 + q_PMI2/q_lsd_f) uses only the perpendicular moment proxy because a linear rotor's rotational partition function depends on one degenerate perpendicular moment; the single_site branch is 0. lsd_f is the passing-bottleneck free sphere Df, not the global cavity diameter Di, and not Dif.",
      "physical_interpretation": "All quantities enter via dimensionless q_X = X/X_ref ratios with fixed positive training-reference medians; log10 arguments are dimensionless. The predeclared proxy derivative is: holding rotor class and the other inputs fixed, d(descriptor)/d(PMI2) > 0 and d(descriptor)/d(lsd_f) < 0. The target is entropy loss = -(S_ads - S_gas)/R, so descriptor_direction 'increasing' with entropy_direction 'increasing' means larger inertia in tighter frameworks predicts larger entropy loss (smaller s_ads/s_gas). Correlations and partial derivatives do not establish causality.",
      "boundary_behavior": "Zeros of the PMI proxies are legitimate and structurally interpretable: PMI1, PMI2 and PMI3 all vanish on the 54 single-site rows, and PMI1 (the axial moment about the molecular long axis) additionally vanishes on linear rows (PMI1 near_zero_n = 268 = 54 single-site + 214 linear), consistent with any strictly linear heavy-atom layout having zero moment about its own axis. Where a numerator is 0, log10(1+0) = 0 is finite; this includes the constant single_site branch. The linear branch deliberately uses PMI2, which is strictly positive on all linear rows (the 54 PMI2 zeros are exactly the single-site rows), so no zero numerator arises in that branch. q_lsd_f is strictly positive (native lsd_f min 0.85684 angstrom), so no division by zero occurs anywhere. Logarithmic growth at extreme inertia or narrow bottlenecks is an empirical smoothing choice; the fixed training-reference medians carry no universal physical threshold meaning.",
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
        "PMI1",
        "PMI2",
        "PMI3",
        "lsd_f"
      ],
      "quantity_roles": {
        "PMI1": "heavy_atom_inertia_proxy",
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2299.281763
      ],
      "training_spearman": 0.5010126565750941,
      "target_association": "consistent",
      "perturbation": 3.956905037,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/agent/replicate-1/round-3/h2`

最终状态：scored；边际收益：-2.839934 pp；保留：False。

复核改动字段：rationale, scientific_test.boundary_behavior

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "elongation_slenderness_loss",
    "formula": "log10(1 + q_GeDi**3 / (1 + q_Vol))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with molecular slenderness, proxied by the largest heavy-atom pair distance (GeDi) scaled against the van der Waals volume (Vol): elongated molecules present a larger anisotropic contact footprint per unit volume, fit fewer pore-wall-compatible orientations, and therefore lose more rotational/configurational entropy than compact molecules of equal volume.",
    "rationale": "This isolates molecular shape from molecular size: q_Vol alone is already carried by the retained volume-accessibility descriptor, so the proposed term conditions on volume and rises only when the heavy-atom pair distance is large relative to volume (slender/elongated geometry). Both GeDi and Vol are strictly positive-or-zero heavy-atom/vdW proxies from the original implicit-H representation; the (1 + q_Vol) offset keeps the denominator away from the legitimate zero rows of GeDi without imputing physics. Limitations: GeDi is a two-atom extreme statistic and can be sensitive to a single protruding heavy atom; q constants are dataset-fixed reference medians with no universal meaning; the cubic power is an empirical smoothing choice, not a derived law.",
    "falsification_criteria": "The hypothesis is falsified if the training association between this descriptor and entropy loss is negative or statistically inconsistent with the predeclared increasing direction (target_association 'contradicted'), or if the marginal improvement over the retained descriptors is non-positive, indicating slenderness carries no information beyond volume and planarity. A competing mechanism predicts the opposite sign: slender molecules may thread straight channels with less orientational frustration, which would yield a decreasing association.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi (largest heavy-atom pair distance) and Vol (vdW volume) are geometry proxies from the original implicit-H/heavy-atom representation; legitimate zeros exist for GeDi (54 single-site rows) and are handled by the additive denominator offset, which is an empirical smoothing device, not a physical epsilon in a law. The descriptor does not distinguish shape anisotropy within the all-atom hydrogen envelope.",
      "physical_interpretation": "q_GeDi and q_Vol are dimensionless ratios to fixed positive training-reference medians; the log10 argument is dimensionless. Predeclared proxy derivatives: d(descriptor)/d(GeDi) > 0 at fixed Vol, d(descriptor)/d(Vol) < 0 at fixed GeDi. Since the scored target is entropy loss = -(S_ads - S_gas)/R, descriptor_direction 'increasing' pairs with entropy_direction 'increasing': slender molecules are predicted to lose more entropy (lower s_ads/s_gas). Association tests do not validate causality.",
      "boundary_behavior": "At GeDi = 0 (the 54 single-site rows where the heavy-atom pair distance legitimately vanishes), the descriptor equals log10(1+0) = 0, finite and interpretable as no slenderness signal from this proxy. For compact molecules (GeDi small relative to Vol) the descriptor approaches 0. Growth with slenderness is logarithmically damped by construction; the fixed q constants carry no universal physical threshold meaning.",
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
        "Vol"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.3927418471103523,
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
    "name": "elongation_slenderness_loss",
    "formula": "log10(1 + q_GeDi**3 / (1 + q_Vol))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with molecular slenderness, proxied by the largest heavy-atom pair distance (GeDi) scaled against the van der Waals volume (Vol): elongated molecules present a larger anisotropic contact footprint per unit volume, fit fewer pore-wall-compatible orientations, and therefore lose more rotational/configurational entropy than compact molecules of equal volume.",
    "rationale": "This isolates molecular shape from molecular size: q_Vol alone is already carried by the retained volume-accessibility descriptor, so the proposed term conditions on volume and rises only when the heavy-atom pair distance is large relative to volume (slender/elongated geometry). Domain note corrected: Vol is strictly positive over training (min 20.424 angstrom^3), so the denominator 1 + q_Vol is bounded away from zero regardless of any offset; the (1 + q_Vol) term is an empirical smoothing device for the denominator, not a guard against the GeDi zeros. The legitimate GeDi zeros (54 single-site rows) enter the numerator and are handled by log10(1+0) = 0, with no imputation. Limitations: GeDi is a two-atom extreme statistic and can be sensitive to a single protruding heavy atom; the descriptor does not resolve shape anisotropy within the all-atom hydrogen envelope; q constants are dataset-fixed reference medians with no universal meaning; the cubic power is an empirical smoothing choice, not a derived law.",
    "falsification_criteria": "The hypothesis is falsified if the training association between this descriptor and entropy loss is negative or statistically inconsistent with the predeclared increasing direction (target_association 'contradicted'), or if the marginal improvement over the retained descriptors is non-positive, indicating slenderness carries no information beyond volume and planarity. A competing mechanism predicts the opposite sign: slender molecules may thread straight channels with less orientational frustration, which would yield a decreasing association.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi (largest heavy-atom pair distance) and Vol (vdW volume) are geometry proxies from the original implicit-H/heavy-atom representation; legitimate zeros exist for GeDi (54 single-site rows) and are handled by the additive denominator offset, which is an empirical smoothing device, not a physical epsilon in a law. The descriptor does not distinguish shape anisotropy within the all-atom hydrogen envelope.",
      "physical_interpretation": "q_GeDi and q_Vol are dimensionless ratios to fixed positive training-reference medians; the log10 argument is dimensionless. Predeclared proxy derivatives: d(descriptor)/d(GeDi) > 0 at fixed Vol, d(descriptor)/d(Vol) < 0 at fixed GeDi. Since the scored target is entropy loss = -(S_ads - S_gas)/R, descriptor_direction 'increasing' pairs with entropy_direction 'increasing': slender molecules are predicted to lose more entropy (lower s_ads/s_gas). Association tests do not validate causality.",
      "boundary_behavior": "At the 54 single-site rows GeDi legitimately equals 0 (a single heavy atom has no two-atom pair distance); the numerator is then 0 and the descriptor is log10(1+0) = 0, finite and interpretable as no slenderness signal from this proxy. The denominator satisfies 1 + q_Vol > 1 for every row because Vol is strictly positive (min 20.424 angstrom^3); the additive offset is an empirical smoothing choice, not a physical epsilon in a law. For compact molecules (GeDi small relative to Vol) the descriptor approaches 0. Growth with slenderness is logarithmically damped by construction; the fixed q constants carry no universal threshold meaning.",
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
        "Vol"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.3927418471103523,
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
    "name": "elongation_slenderness_loss",
    "formula": "log10(1 + q_GeDi**3 / (1 + q_Vol))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with molecular slenderness, proxied by the largest heavy-atom pair distance (GeDi) scaled against the van der Waals volume (Vol): elongated molecules present a larger anisotropic contact footprint per unit volume, fit fewer pore-wall-compatible orientations, and therefore lose more rotational/configurational entropy than compact molecules of equal volume.",
    "rationale": "This isolates molecular shape from molecular size: q_Vol alone is already carried by the retained volume-accessibility descriptor, so the proposed term conditions on volume and rises only when the heavy-atom pair distance is large relative to volume (slender/elongated geometry). Domain note corrected: Vol is strictly positive over training (min 20.424 angstrom^3), so the denominator 1 + q_Vol is bounded away from zero regardless of any offset; the (1 + q_Vol) term is an empirical smoothing device for the denominator, not a guard against the GeDi zeros. The legitimate GeDi zeros (54 single-site rows) enter the numerator and are handled by log10(1+0) = 0, with no imputation. Limitations: GeDi is a two-atom extreme statistic and can be sensitive to a single protruding heavy atom; the descriptor does not resolve shape anisotropy within the all-atom hydrogen envelope; q constants are dataset-fixed reference medians with no universal meaning; the cubic power is an empirical smoothing choice, not a derived law.",
    "falsification_criteria": "The hypothesis is falsified if the training association between this descriptor and entropy loss is negative or statistically inconsistent with the predeclared increasing direction (target_association 'contradicted'), or if the marginal improvement over the retained descriptors is non-positive, indicating slenderness carries no information beyond volume and planarity. A competing mechanism predicts the opposite sign: slender molecules may thread straight channels with less orientational frustration, which would yield a decreasing association.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "GeDi (largest heavy-atom pair distance) and Vol (vdW volume) are geometry proxies from the original implicit-H/heavy-atom representation; legitimate zeros exist for GeDi (54 single-site rows) and are handled by the additive denominator offset, which is an empirical smoothing device, not a physical epsilon in a law. The descriptor does not distinguish shape anisotropy within the all-atom hydrogen envelope.",
      "physical_interpretation": "q_GeDi and q_Vol are dimensionless ratios to fixed positive training-reference medians; the log10 argument is dimensionless. Predeclared proxy derivatives: d(descriptor)/d(GeDi) > 0 at fixed Vol, d(descriptor)/d(Vol) < 0 at fixed GeDi. Since the scored target is entropy loss = -(S_ads - S_gas)/R, descriptor_direction 'increasing' pairs with entropy_direction 'increasing': slender molecules are predicted to lose more entropy (lower s_ads/s_gas). Association tests do not validate causality.",
      "boundary_behavior": "At the 54 single-site rows GeDi legitimately equals 0 (a single heavy atom has no two-atom pair distance); the numerator is then 0 and the descriptor is log10(1+0) = 0, finite and interpretable as no slenderness signal from this proxy. The denominator satisfies 1 + q_Vol > 1 for every row because Vol is strictly positive (min 20.424 angstrom^3); the additive offset is an empirical smoothing choice, not a physical epsilon in a law. For compact molecules (GeDi small relative to Vol) the descriptor approaches 0. Growth with slenderness is logarithmically damped by construction; the fixed q constants carry no universal threshold meaning.",
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
        "Vol"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.3927418471103523,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/agent/replicate-1/round-3/h3`

最终状态：scored；边际收益：-4.156776 pp；保留：False。

复核改动字段：physical_claims, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "framework_density_confinement_loss",
    "formula": "log10(1 + q_Vol * q_density / q_lsd_p)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with the product of adsorbate van der Waals volume and framework density, and decreases with the largest included sphere along the free-sphere path (lsd_p): bulky adsorbates in crystallographically dense frameworks (little void per framework atom) with small included free-path spheres experience the tightest confinement and lose the largest fraction of translational entropy.",
    "rationale": "This combines two framework-side descriptors (native-scale density proxy and Dif) not directly present in the retained set with the adsorbate volume. The declared increasing direction of the size/headroom ratio with entropy loss is pre-registered in light of the round-2 diagnostic in which the analogous q_Vol/q_lsd_p headroom descriptor showed a positive Spearman association with entropy loss but a 'contradicted' label under a decreasing declaration; this candidate therefore declares the association with entropy loss directly. Limitations: density enters on its published numerical scale with unresolved physical units, so it is used only as a monotone framework-density proxy; lsd_p (Dif) is the included sphere along the free path, neither the bottleneck Df nor necessarily the global cavity Di; q constants are fixed training-reference medians with no universal physical meaning.",
    "falsification_criteria": "The hypothesis is falsified if the training Spearman association between this descriptor and entropy loss is negative (target_association 'contradicted'), or if the marginal improvement over the retained volume-accessibility and planarity descriptors is non-positive after accounting for redundancy with q_Vol and q_AV. A competing mechanism holds that equilibrium entropy loss at infinite dilution is governed by accessible free volume (AV) rather than by framework density or path-included sphere geometry, which would leave this descriptor without residual explanatory power.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "density": "native_framework_density_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "density is a monotone proxy on an unresolved published numerical scale and supports only ordinal claims; lsd_p is the Zeo++ Dif included sphere along the free-sphere path, explicitly not the bottleneck Df and not the global cavity diameter; AV (fixed-probe accessibility) is deliberately not used here. The product form is an empirical coupling assumption between adsorbate size and framework packing, not a derived physical law.",
      "physical_interpretation": "q_Vol, q_density and q_lsd_p are dimensionless ratios to fixed positive training-reference medians; all three native inputs are strictly positive across the training domain, so log10 arguments are dimensionless and finite. Predeclared proxy derivatives: d(descriptor)/d(Vol) > 0, d(descriptor)/d(density) > 0, d(descriptor)/d(lsd_p) < 0. Because the scored target is entropy loss = -(S_ads - S_gas)/R, descriptor_direction 'increasing' pairs with entropy_direction 'increasing': denser frameworks with smaller included free-path spheres adsorbing larger molecules are predicted to show larger entropy loss (smaller s_ads/s_gas). Numerical tests do not establish causality.",
      "boundary_behavior": "Every training row has strictly positive Vol (min 20.424 angstrom^3), density (min 0.759654) and lsd_p (min 3.3452 angstrom), so q_lsd_p > 0 and no division by zero occurs; the descriptor is finite for all rows without imputation. As lsd_p grows, the descriptor decays toward log10(1 + small) ~ 0, i.e., an unconfined limit with vanishing predicted confinement loss. The logarithm and the fixed reference medians are empirical smoothings with no claimed universal threshold meaning.",
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
        "Vol",
        "density",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "density": "native_framework_density_proxy",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": 0.704694379388966,
      "target_association": "consistent",
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
    "name": "framework_density_confinement_loss",
    "formula": "log10(1 + q_Vol * q_density / q_lsd_p)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with the product of adsorbate van der Waals volume and framework density, and decreases with the largest included sphere along the free-sphere path (lsd_p): bulky adsorbates in crystallographically dense frameworks (little void per framework atom) with small included free-path spheres experience the tightest confinement and lose the largest fraction of translational entropy.",
    "rationale": "This combines two framework-side descriptors (native-scale density proxy and Dif) not directly present in the retained set with the adsorbate volume. The declared increasing direction of the size/headroom ratio with entropy loss is pre-registered in light of the round-2 diagnostic in which the analogous q_Vol/q_lsd_p headroom descriptor showed a positive Spearman association with entropy loss but a 'contradicted' label under a decreasing declaration; this candidate therefore declares the association with entropy loss directly. Limitations: density enters on its published numerical scale with unresolved physical units, so it is used only as a monotone framework-density proxy; lsd_p (Dif) is the included sphere along the free path, neither the bottleneck Df nor necessarily the global cavity Di; q constants are fixed training-reference medians with no universal physical meaning.",
    "falsification_criteria": "The hypothesis is falsified if the training Spearman association between this descriptor and entropy loss is negative (target_association 'contradicted'), or if the marginal improvement over the retained volume-accessibility and planarity descriptors is non-positive after accounting for redundancy with q_Vol and q_AV. A competing mechanism holds that equilibrium entropy loss at infinite dilution is governed by accessible free volume (AV) rather than by framework density or path-included sphere geometry, which would leave this descriptor without residual explanatory power.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "density": "native_framework_density_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "density is a monotone proxy on an unresolved published numerical scale and supports only ordinal claims; lsd_p is the Zeo++ Dif included sphere along the free-sphere path, explicitly not the bottleneck Df and not the global cavity diameter Di; Vol is the adsorbate's molecular van der Waals volume, NOT a probe-accessible volume — AV (fixed-probe accessibility) is deliberately not used here, so no probe_volume_proxy claim is made. The descriptor contrasts adsorbate molecular size against path-included geometric headroom (geometric_path_contrast), and the product form is an empirical coupling assumption between adsorbate size and framework packing, not a derived physical law.",
      "physical_interpretation": "q_Vol, q_density and q_lsd_p are dimensionless ratios to fixed positive training-reference medians; all three native inputs are strictly positive across the training domain, so log10 arguments are dimensionless and finite. Predeclared proxy derivatives: d(descriptor)/d(Vol) > 0, d(descriptor)/d(density) > 0, d(descriptor)/d(lsd_p) < 0. Because the scored target is entropy loss = -(S_ads - S_gas)/R, descriptor_direction 'increasing' pairs with entropy_direction 'increasing': denser frameworks with smaller included free-path spheres adsorbing larger molecules are predicted to show larger entropy loss (smaller s_ads/s_gas). Numerical tests do not establish causality.",
      "boundary_behavior": "Every training row has strictly positive Vol (min 20.424 angstrom^3), density (min 0.759654) and lsd_p (min 3.3452 angstrom), so q_lsd_p > 0 and no division by zero occurs; the descriptor is finite for all rows without imputation. As lsd_p grows, the descriptor decays toward log10(1 + small) ~ 0, i.e., an unconfined limit with vanishing predicted confinement loss. The logarithm and the fixed reference medians are empirical smoothings with no claimed universal threshold meaning.",
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
        "Vol",
        "density",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "density": "native_framework_density_proxy",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": 0.704694379388966,
      "target_association": "consistent",
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
    "name": "framework_density_confinement_loss",
    "formula": "log10(1 + q_Vol * q_density / q_lsd_p)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with the product of adsorbate van der Waals volume and framework density, and decreases with the largest included sphere along the free-sphere path (lsd_p): bulky adsorbates in crystallographically dense frameworks (little void per framework atom) with small included free-path spheres experience the tightest confinement and lose the largest fraction of translational entropy.",
    "rationale": "This combines two framework-side descriptors (native-scale density proxy and Dif) not directly present in the retained set with the adsorbate volume. The declared increasing direction of the size/headroom ratio with entropy loss is pre-registered in light of the round-2 diagnostic in which the analogous q_Vol/q_lsd_p headroom descriptor showed a positive Spearman association with entropy loss but a 'contradicted' label under a decreasing declaration; this candidate therefore declares the association with entropy loss directly. Limitations: density enters on its published numerical scale with unresolved physical units, so it is used only as a monotone framework-density proxy; lsd_p (Dif) is the included sphere along the free path, neither the bottleneck Df nor necessarily the global cavity Di; q constants are fixed training-reference medians with no universal physical meaning.",
    "falsification_criteria": "The hypothesis is falsified if the training Spearman association between this descriptor and entropy loss is negative (target_association 'contradicted'), or if the marginal improvement over the retained volume-accessibility and planarity descriptors is non-positive after accounting for redundancy with q_Vol and q_AV. A competing mechanism holds that equilibrium entropy loss at infinite dilution is governed by accessible free volume (AV) rather than by framework density or path-included sphere geometry, which would leave this descriptor without residual explanatory power.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "density": "native_framework_density_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "density is a monotone proxy on an unresolved published numerical scale and supports only ordinal claims; lsd_p is the Zeo++ Dif included sphere along the free-sphere path, explicitly not the bottleneck Df and not the global cavity diameter Di; Vol is the adsorbate's molecular van der Waals volume, NOT a probe-accessible volume — AV (fixed-probe accessibility) is deliberately not used here, so no probe_volume_proxy claim is made. The descriptor contrasts adsorbate molecular size against path-included geometric headroom (geometric_path_contrast), and the product form is an empirical coupling assumption between adsorbate size and framework packing, not a derived physical law.",
      "physical_interpretation": "q_Vol, q_density and q_lsd_p are dimensionless ratios to fixed positive training-reference medians; all three native inputs are strictly positive across the training domain, so log10 arguments are dimensionless and finite. Predeclared proxy derivatives: d(descriptor)/d(Vol) > 0, d(descriptor)/d(density) > 0, d(descriptor)/d(lsd_p) < 0. Because the scored target is entropy loss = -(S_ads - S_gas)/R, descriptor_direction 'increasing' pairs with entropy_direction 'increasing': denser frameworks with smaller included free-path spheres adsorbing larger molecules are predicted to show larger entropy loss (smaller s_ads/s_gas). Numerical tests do not establish causality.",
      "boundary_behavior": "Every training row has strictly positive Vol (min 20.424 angstrom^3), density (min 0.759654) and lsd_p (min 3.3452 angstrom), so q_lsd_p > 0 and no division by zero occurs; the descriptor is finite for all rows without imputation. As lsd_p grows, the descriptor decays toward log10(1 + small) ~ 0, i.e., an unconfined limit with vanishing predicted confinement loss. The logarithm and the fixed reference medians are empirical smoothings with no claimed universal threshold meaning.",
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
        "Vol",
        "density",
        "lsd_p"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "density": "native_framework_density_proxy",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.759654,
        2.11908
      ],
      "training_spearman": 0.704694379388966,
      "target_association": "consistent",
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
    "mode": "no_retrieval",
    "items": 0,
    "lexical_tokens": 0
  },
  "cited_items": [],
  "mechanism_cards": []
}
```
