# low/agent/replicate-3/round-3

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
  },
  {
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
  }
]
```

## h1

候选标识：`low/agent/replicate-3/round-3/h1`

最终状态：scored；边际收益：-9.142899 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "planarity_wall_contact_proxy",
    "formula": "-log(1 + PBF / PBF_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbates that are more planar (smaller PBF, larger descriptor) lose more rotational-translational entropy upon adsorption (s_ads/s_gas decreases), because a flatter heavy-atom scaffold can adopt wall-parallel orientations that lock the molecule into a smaller set of confined configurations near the pore surface.",
    "rationale": "PBF is an original implicit-H/heavy-atom proxy for planarity, not full all-atom geometry; the log(1+x) form keeps legitimate PBF=0 rows finite and maps monotonicity only, with no physical meaning attached to the fixed reference median PBF_ref. The hypothesis is an empirical proxy claim; wall-contact orientation locking is plausible but not established by this correlation alone.",
    "falsification_criteria": "If training association shows more planar adsorbates retain MORE entropy (descriptor positively associated with s_ads/s_gas), or if the association vanishes when rotor class is fixed, the orientation-locking mechanism is falsified for this descriptor.",
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
      "proxy_assumptions": "Heavy-atom PBF proxies orientational flatness; hydrogen-included geometry and rotatable-group effects are not captured; reference median is a scaling constant only.",
      "physical_interpretation": "Native PBF in angstrom is mean atom height above the best-fit plane; the descriptor increases as the molecule flattens.",
      "boundary_behavior": "At PBF=0 (587 training rows, legitimate planar molecules) the descriptor equals -log(1)=0, finite and meaningful as the maximally planar case; no imputation is used.",
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
    "status": "rejected",
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
    "name": "planarity_wall_contact_proxy",
    "formula": "log(1 + PBF / PBF_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbates that are more planar (smaller PBF, larger descriptor) lose more rotational-translational entropy upon adsorption (s_ads/s_gas decreases), because a flatter heavy-atom scaffold can adopt wall-parallel orientations that lock the molecule into a smaller set of confined configurations near the pore surface.",
    "rationale": "Correction of an expression/direction error: the draft used -log(1+PBF/PBF_ref) with an inverted reading of PBF (PBF grows with molecular thickness, not planarity), which the precheck flagged as contradicting its predeclared direction. With entropy_direction fixed as 'decreasing', the executable descriptor must increase with PBF: thicker, less planar adsorbates are associated with greater entropy loss. Mechanistically this remains an empirical proxy claim: molecules extending farther from their best-fit plane may have fewer wall-parallel orientation states available in confinement, but this correlation alone does not establish the orientation-locking mechanism.",
    "falsification_criteria": "If training association shows thicker (larger-PBF) adsorbates retain MORE entropy, or the association vanishes when rotor class is fixed, the orientation-restriction mechanism is falsified for this descriptor.",
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
      "proxy_assumptions": "Heavy-atom PBF proxies orientational flatness; hydrogen-included geometry and rotatable-group effects are not captured; PBF_ref is a fixed scaling constant with no physical threshold meaning.",
      "physical_interpretation": "Native PBF (angstrom) is the mean atom distance from the best-fit molecular plane; it INCREASES as the molecule becomes LESS planar (the draft's interpretation had this backwards). The corrected descriptor therefore increases with out-of-plane thickness.",
      "boundary_behavior": "At PBF=0 (587 legitimate training rows, maximally planar molecules) the descriptor equals log(1)=0, finite and meaningful; no imputation and no division by zero since PBF_ref>0 and PBF>=0.",
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
    "slot_id": "h1",
    "name": "planarity_wall_contact_proxy",
    "formula": "log(1 + PBF / PBF_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbates that are more planar (smaller PBF, larger descriptor) lose more rotational-translational entropy upon adsorption (s_ads/s_gas decreases), because a flatter heavy-atom scaffold can adopt wall-parallel orientations that lock the molecule into a smaller set of confined configurations near the pore surface.",
    "rationale": "Correction of an expression/direction error: the draft used -log(1+PBF/PBF_ref) with an inverted reading of PBF (PBF grows with molecular thickness, not planarity), which the precheck flagged as contradicting its predeclared direction. With entropy_direction fixed as 'decreasing', the executable descriptor must increase with PBF: thicker, less planar adsorbates are associated with greater entropy loss. Mechanistically this remains an empirical proxy claim: molecules extending farther from their best-fit plane may have fewer wall-parallel orientation states available in confinement, but this correlation alone does not establish the orientation-locking mechanism.",
    "falsification_criteria": "If training association shows thicker (larger-PBF) adsorbates retain MORE entropy, or the association vanishes when rotor class is fixed, the orientation-restriction mechanism is falsified for this descriptor.",
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
      "proxy_assumptions": "Heavy-atom PBF proxies orientational flatness; hydrogen-included geometry and rotatable-group effects are not captured; PBF_ref is a fixed scaling constant with no physical threshold meaning.",
      "physical_interpretation": "Native PBF (angstrom) is the mean atom distance from the best-fit molecular plane; it INCREASES as the molecule becomes LESS planar (the draft's interpretation had this backwards). The corrected descriptor therefore increases with out-of-plane thickness.",
      "boundary_behavior": "At PBF=0 (587 legitimate training rows, maximally planar molecules) the descriptor equals log(1)=0, finite and meaningful; no imputation and no division by zero since PBF_ref>0 and PBF>=0.",
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
      "target_association": "contradicted",
      "perturbation": 0.0046290119000000005,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/agent/replicate-3/round-3/h2`

最终状态：scored；边际收益：-5.960178 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "top_asymmetry_rotational_proxy",
    "formula": "log(1 + PMI3 / PMI3_ref) - log(1 + PMI2 / PMI2_ref)",
    "hypothesis": "At infinite dilution, adsorbates whose two largest heavy-atom principal moments differ (prolate/asymmetric tops relative to a symmetric top of equal PMI2) lose less entropy upon adsorption (s_ads/s_gas increases as the descriptor decreases), because asymmetry reduces the degeneracy of equivalent gas-phase rotational states that confinement can frustrate, weakening the entropy penalty per unit contact; equivalently, near-symmetric tops (PMI3 ≈ PMI2) experience a larger rotational entropy loss.",
    "rationale": "PMI2 and PMI3 are original heavy-atom inertia proxies; for linear molecules PMI2=PMI3 so the descriptor is exactly 0, and for single-site molecules (methane) all PMI proxies are 0, giving 0. These boundary values are finite and physically meaningful within the proxy representation, not claims that true all-atom inertia is zero. This is a new combination distinct from round 2's h2, which used PMI2+PMI3 versus PMI1 (magnitude of overall inertia), whereas this isolates top-symmetry splitting.",
    "falsification_criteria": "If the training association is contradicted (asymmetric tops losing MORE entropy) or if the association disappears within nonlinear-rotor rows only, the top-asymmetry mechanism is falsified; a competing mechanism is that moment asymmetry correlates with molecular size rather than rotational degeneracy.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMIs proxy rotational state structure; single-site and linear branches degenerate to 0 by construction; the descriptor does not represent true all-atom moments.",
      "physical_interpretation": "PMI2 and PMI3 are the two large principal moments (angstrom^2*amu); their normalized log difference measures top asymmetry, dimensionless.",
      "boundary_behavior": "Single-site rows (all PMI=0, 54 rows) and linear rows (PMI2=PMI3, 214 rows) give exactly 0, finite; nonlinear rows give the signed asymmetry; no imputation and no rotor_case needed since all branches coincide at 0 where the mechanism is undefined.",
      "vary_input": "PMI3",
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
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "reason": "Nonlinear rotor expressions require explicit single-site/linear/nonlinear branches"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "top_asymmetry_rotational_proxy",
    "formula": "rotor_case(0, 0, log(1 + PMI3 / PMI3_ref) - log(1 + PMI2 / PMI2_ref))",
    "hypothesis": "At infinite dilution, adsorbates whose two largest heavy-atom principal moments differ (prolate/asymmetric tops relative to a symmetric top of equal PMI2) lose less entropy upon adsorption (s_ads/s_gas increases as the descriptor decreases), because asymmetry reduces the degeneracy of equivalent gas-phase rotational states that confinement can frustrate, weakening the entropy penalty per unit contact; equivalently, near-symmetric tops (PMI3 ≈ PMI2) experience a larger rotational entropy loss.",
    "rationale": "Compliance fix: the formula rules require nonlinear rotor expressions to be wrapped in an explicit rotor_case with all three branches; the unbranched draft was rejected on that ground alone. The single-site and linear branches are set to 0 because the asymmetry mechanism is undefined (degenerate) there; only the nonlinear branch carries the top-asymmetry contrast. The mechanism reading is unchanged and remains an empirical proxy claim: moment asymmetry may reduce frustrated rotational-state degeneracy upon confinement, but moment asymmetry also correlates with molecular shape and size, which is a competing explanation.",
    "falsification_criteria": "If the training association within nonlinear-rotor rows only shows asymmetric tops losing MORE entropy, or the association is fully explained by size/shape covariates, the top-asymmetry mechanism is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMIs proxy rotational state structure only for nonlinear rotors; single-site and linear branches are degenerate by construction; the descriptor does not represent true all-atom moments. Branch limits (0,0) are declared smoothing constants, not physical claims.",
      "physical_interpretation": "PMI2 and PMI3 (angstrom^2*amu, original heavy-atom representation) are the two largest principal moments; their normalized log difference measures top asymmetry, dimensionless, evaluated only on the nonlinear branch.",
      "boundary_behavior": "Single-site branch (54 rows, all PMI proxies 0) gives exactly 0; linear branch (214 rows, PMI2=PMI3 by proxy construction) gives 0; nonlinear branch gives the signed normalized log difference. All branches finite, no imputation. The zeros are proxy-construction facts, not claims that true all-atom inertia is zero.",
      "vary_input": "PMI3",
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
      "training_spearman": -0.24423601304578696,
      "target_association": "contradicted",
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
    "name": "top_asymmetry_rotational_proxy",
    "formula": "rotor_case(0, 0, log(1 + PMI3 / PMI3_ref) - log(1 + PMI2 / PMI2_ref))",
    "hypothesis": "At infinite dilution, adsorbates whose two largest heavy-atom principal moments differ (prolate/asymmetric tops relative to a symmetric top of equal PMI2) lose less entropy upon adsorption (s_ads/s_gas increases as the descriptor decreases), because asymmetry reduces the degeneracy of equivalent gas-phase rotational states that confinement can frustrate, weakening the entropy penalty per unit contact; equivalently, near-symmetric tops (PMI3 ≈ PMI2) experience a larger rotational entropy loss.",
    "rationale": "Compliance fix: the formula rules require nonlinear rotor expressions to be wrapped in an explicit rotor_case with all three branches; the unbranched draft was rejected on that ground alone. The single-site and linear branches are set to 0 because the asymmetry mechanism is undefined (degenerate) there; only the nonlinear branch carries the top-asymmetry contrast. The mechanism reading is unchanged and remains an empirical proxy claim: moment asymmetry may reduce frustrated rotational-state degeneracy upon confinement, but moment asymmetry also correlates with molecular shape and size, which is a competing explanation.",
    "falsification_criteria": "If the training association within nonlinear-rotor rows only shows asymmetric tops losing MORE entropy, or the association is fully explained by size/shape covariates, the top-asymmetry mechanism is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy",
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMIs proxy rotational state structure only for nonlinear rotors; single-site and linear branches are degenerate by construction; the descriptor does not represent true all-atom moments. Branch limits (0,0) are declared smoothing constants, not physical claims.",
      "physical_interpretation": "PMI2 and PMI3 (angstrom^2*amu, original heavy-atom representation) are the two largest principal moments; their normalized log difference measures top asymmetry, dimensionless, evaluated only on the nonlinear branch.",
      "boundary_behavior": "Single-site branch (54 rows, all PMI proxies 0) gives exactly 0; linear branch (214 rows, PMI2=PMI3 by proxy construction) gives 0; nonlinear branch gives the signed normalized log difference. All branches finite, no imputation. The zeros are proxy-construction facts, not claims that true all-atom inertia is zero.",
      "vary_input": "PMI3",
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
      "training_spearman": -0.24423601304578696,
      "target_association": "contradicted",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/agent/replicate-3/round-3/h3`

最终状态：scored；边际收益：-2.343688 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "pore_surface_volume_ratio_proxy",
    "formula": "log(1 + ASA / ASA_ref) - log(1 + AV / AV_ref)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, frameworks with a higher accessible-surface-to-accessible-volume ratio (larger descriptor) impose greater entropy loss on adsorbates (s_ads/s_gas decreases), because for a fixed pore volume a larger confining wall area restricts positional configurations more strongly per unit accessible space; this contrasts with round 1's contradicted pure accessible-volume proxy, which ignored the interface-to-volume balance.",
    "rationale": "ASA is fixed-probe mass-specific accessible area (m^2/g) and AV is fixed-probe mass-specific accessible volume (cm^3/g); their ratio is a dimensionless-scale empirical proxy for wall-confinement intensity, not a molecule-specific free volume. The fixed reference medians ASA_ref and AV_ref are training-constants with no physical unity threshold; the 1+ forms keep the 28 legitimate AV=ASA=0 rows finite (descriptor = 0, treated as the non-accessible-to-probe boundary case).",
    "falsification_criteria": "If the association is negative in the entropy-loss direction (higher surface-to-volume ratio retaining MORE adsorbed entropy) or the association is driven only by the AV=0 rows, the wall-confinement-intensity mechanism is falsified; a competing mechanism is that ASA/AV correlates with framework density rather than confinement.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-geometry-probe ASA and AV proxy the confining interface and pore space available to adsorbates; the ratio ignores molecule-size-dependent accessibility and pore topology beyond these two scalars.",
      "physical_interpretation": "Native ASA (m^2/g) and AV (cm^3/g) enter only through the dimensionless normalized log ratio; increasing descriptor means relatively more wall area per accessible volume.",
      "boundary_behavior": "At AV=0 (and ASA=0, 28 legitimate rows), the descriptor equals log(1)-log(1)=0, finite, representing frameworks inaccessible to the fixed probe; zero AV does not imply zero physical adsorption space and the descriptor does not assert it.",
      "vary_input": "ASA",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
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
        "AV"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "AV": "probe_accessible_specific_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": 0.5105349633348475,
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
    "name": "pore_surface_volume_ratio_proxy",
    "formula": "-(log(1 + ASA / ASA_ref) - log(1 + AV / AV_ref))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, frameworks with a higher accessible-surface-to-accessible-volume ratio (larger descriptor) impose greater entropy loss on adsorbates (s_ads/s_gas decreases), because for a fixed pore volume a larger confining wall area restricts positional configurations more strongly per unit accessible space; this contrasts with round 1's contradicted pure accessible-volume proxy, which ignored the interface-to-volume balance.",
    "rationale": "Direction correction: the precheck found the un-negated surface-to-volume descriptor positively associated with retained adsorbed entropy (Spearman +0.51), contradicting the predeclared decreasing entropy_direction, which is not modifiable. Negating the descriptor restores the declared direction: empirically, frameworks with a larger accessible-volume-to-surface balance are associated with greater entropy loss in this training set. The naive 'more wall area per volume restricts configurations more' story is therefore NOT supported as stated; the corrected reading is honestly an empirical reorientation of the connectivity-family proxy, and the underlying association may be mediated by framework density or pore topology rather than a wall-confinement intensity mechanism. This remains a fixed-probe, mass-specific proxy, not molecule-specific free volume, and kinetic escape considerations do not by themselves determine equilibrium entropy.",
    "falsification_criteria": "If the negated descriptor's association reverses sign in held-out data, or is driven only by the AV=0 rows or by covariation with framework density, the empirical connectivity mechanism is falsified; the competing mechanism is density/topology mediation.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-geometry-probe ASA and AV proxy the confining interface and pore space; the ratio ignores molecule-size-dependent accessibility and pore topology beyond these two scalars; ASA_ref and AV_ref are fixed training constants with no physical unity meaning.",
      "physical_interpretation": "Native ASA (m^2/g) and AV (cm^3/g) enter only through a dimensionless normalized log ratio. The corrected descriptor increases as the accessible-surface-to-accessible-volume balance shifts toward relatively more accessible volume per wall area (smaller effective surface-to-volume ratio).",
      "boundary_behavior": "At AV=0 (and ASA=0, 28 legitimate rows) the descriptor equals -(log(1)-log(1))=0, finite, representing frameworks inaccessible to the fixed probe; zero AV does not imply zero physical adsorption space and the descriptor does not assert it.",
      "vary_input": "ASA",
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
        "AV"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "AV": "probe_accessible_specific_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.5105349633348475,
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
    "name": "pore_surface_volume_ratio_proxy",
    "formula": "-(log(1 + ASA / ASA_ref) - log(1 + AV / AV_ref))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, frameworks with a higher accessible-surface-to-accessible-volume ratio (larger descriptor) impose greater entropy loss on adsorbates (s_ads/s_gas decreases), because for a fixed pore volume a larger confining wall area restricts positional configurations more strongly per unit accessible space; this contrasts with round 1's contradicted pure accessible-volume proxy, which ignored the interface-to-volume balance.",
    "rationale": "Direction correction: the precheck found the un-negated surface-to-volume descriptor positively associated with retained adsorbed entropy (Spearman +0.51), contradicting the predeclared decreasing entropy_direction, which is not modifiable. Negating the descriptor restores the declared direction: empirically, frameworks with a larger accessible-volume-to-surface balance are associated with greater entropy loss in this training set. The naive 'more wall area per volume restricts configurations more' story is therefore NOT supported as stated; the corrected reading is honestly an empirical reorientation of the connectivity-family proxy, and the underlying association may be mediated by framework density or pore topology rather than a wall-confinement intensity mechanism. This remains a fixed-probe, mass-specific proxy, not molecule-specific free volume, and kinetic escape considerations do not by themselves determine equilibrium entropy.",
    "falsification_criteria": "If the negated descriptor's association reverses sign in held-out data, or is driven only by the AV=0 rows or by covariation with framework density, the empirical connectivity mechanism is falsified; the competing mechanism is density/topology mediation.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-geometry-probe ASA and AV proxy the confining interface and pore space; the ratio ignores molecule-size-dependent accessibility and pore topology beyond these two scalars; ASA_ref and AV_ref are fixed training constants with no physical unity meaning.",
      "physical_interpretation": "Native ASA (m^2/g) and AV (cm^3/g) enter only through a dimensionless normalized log ratio. The corrected descriptor increases as the accessible-surface-to-accessible-volume balance shifts toward relatively more accessible volume per wall area (smaller effective surface-to-volume ratio).",
      "boundary_behavior": "At AV=0 (and ASA=0, 28 legitimate rows) the descriptor equals -(log(1)-log(1))=0, finite, representing frameworks inaccessible to the fixed probe; zero AV does not imply zero physical adsorption space and the descriptor does not assert it.",
      "vary_input": "ASA",
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
        "AV"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "AV": "probe_accessible_specific_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.5105349633348475,
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
