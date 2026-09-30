# low/rag_agent/replicate-3/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h2",
    "name": "accessible_volume_entropy_reservoir",
    "formula": "((Vol / Vol_ref) ** 0.5) * (1 + AV_ref / maximum(AV, AV_ref))",
    "hypothesis": "Entropy loss at infinite dilution decreases with the probe-accessible specific volume (AV) of the framework and increases with adsorbate van der Waals volume (Vol): frameworks offering more accessible space preserve more adsorbed-phase configurational/vibrational freedom, while bulky molecules lose more entropy upon docking.",
    "rationale": "The training-only precheck contradicted the original increasing descriptor (Spearman -0.63): empirically, higher probe-accessible volume associates with LOWER entropy loss, consistent with E02 (smaller cavities lose more rotational entropy) and E04 (larger-pore FAU shows smaller fractional entropy loss than MFI). The descriptor was inverted so the descriptor-decreasing-in-AV form carries the declared increasing entropy-loss direction. Mechanism remains configurational freedom, not kinetic escape; association is not causation.",
    "falsification_criteria": "If, within fixed-Vol bins, entropy loss no longer decreases with the inverted AV descriptor, or if lsd_f/lsd_p cavity-size descriptors explain more variance than probe accessibility, the accessible-volume-reservoir mechanism is falsified in favor of a cavity-diameter mechanism.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E02",
      "E04",
      "E09"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe AV is assumed monotone with molecule-accessible space for the adsorbates studied; this fails for molecules near or larger than the probe. AV is mass-specific accessibility, not molecule-specific free volume; the mapping to configurational freedom is a declared proxy limitation. No source coefficient becomes a universal constant (C4, C7).",
      "physical_interpretation": "AV/AV_ref is a dimensionless row-varying accessibility ratio; Vol/Vol_ref is a dimensionless row-varying steric-demand ratio. Neither ratio unity carries a physical threshold meaning. The descriptor decreases with AV and increases with Vol, matching the predeclared entropy-loss direction.",
      "boundary_behavior": "Finite on the full training domain. At AV = 0 (28 training rows, zero accessibility for the fixed geometric probe), maximum(AV, AV_ref) = AV_ref > 0, so the descriptor equals 2*(Vol/Vol_ref)**0.5; for large AV it decreases toward (Vol/Vol_ref)**0.5. The maximum() clamp is an empirical smoothing choice to avoid division by the legitimate physical zero AV = 0 (zero fixed-probe accessibility does not imply zero molecular adsorption space); it is not a physical threshold or imputed value. The descriptor remains decreasing in AV and increasing in Vol, consistent with the stored hypothesis and entropy_direction.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "Vol",
      "regime_train_quantiles": [
        0.1,
        0.9
      ],
      "entropy_direction": "increasing"
    }
  },
  {
    "slot_id": "h1",
    "name": "surface_area_anchor_entropy_quench",
    "formula": "1 / (log(1 + q_LabuteASA) * sqrt(1 + SPAN / SPAN_ref))",
    "hypothesis": "At infinite dilution, adsorbed-phase entropy loss increases with the adsorbate's contact-capable surface area (LabuteASA) and overall extension (SPAN): larger, more extended molecules can make more simultaneous surface contacts with the framework wall, suppressing more translational and librational freedom upon docking.",
    "rationale": "Round-2 precheck contradicted the original increasing-in-area orientation (Spearman +0.219 against the predeclared direction). The formula is inverted so larger LabuteASA/SPAN lowers the descriptor, preserving the stored entropy_direction. The inverse is a numerical re-expression; the association sign itself remains empirically uncertain and mechanism causality is unvalidated.",
    "falsification_criteria": "If within fixed MW and rotor-class strata the partial association of this descriptor with entropy loss reverses sign again, or if planar molecules (PBF near 0) show the opposite behavior, the re-oriented contact-area mechanism is falsified in favor of a volume-dominated mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "SPAN": "heavy_atom_enclosing_radius"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA and SPAN from the implicit-H/heavy-atom representation stand in for contact-capable area and extension; hydrogen contributions ignored; transfer limited to rigid pure-silica frameworks at infinite dilution.",
      "physical_interpretation": "Larger contact-capable surface area and extension empirically associate with LESS retained adsorbed-phase entropy, so the descriptor is defined to decrease as these grow; the training precheck contradicted the original positive orientation, so the inverse form is used. This is an empirical re-orientation, not validated causality; no physical meaning at q=1.",
      "boundary_behavior": "LabuteASA is strictly positive in training (min 7.45) so log(1+q) > 1; SPAN=0 (single-site/linear proxies) gives sqrt(1+0)=1; the descriptor is finite everywhere and decays smoothly as either factor grows.",
      "vary_input": "LabuteASA",
      "descriptor_direction": "decreasing",
      "regime_input": "MW",
      "regime_train_quantiles": [
        0.25,
        0.75
      ],
      "entropy_direction": "decreasing"
    }
  }
]
```

## h1

候选标识：`low/rag_agent/replicate-3/round-3/h1`

最终状态：scored；边际收益：-14.961228 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "framework_density_confinement_quench",
    "formula": "(density / density_ref) * (1 + (Vol / Vol_ref) ** 0.5)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase entropy loss increases with framework density (framework atom packing per volume) and with adsorbate van der Waals volume: denser frameworks confine the guest in tighter environments, and bulkier guests experience a larger entropy reduction upon docking in that confined environment.",
    "rationale": "Framework density is the native inverse-porosity proxy on the published scale; multiplication with an adsorbate volume term encodes a guest-framework confinement coupling rather than either factor alone. Limitations: density is a proxy with unresolved physical unit; Vol is a heavy-atom-derived van der Waals volume; the empirical coupling exponent is a smoothing choice, not a physical law.",
    "falsification_criteria": "If training Spearman between the descriptor and entropy loss within the Vol median regime band is near zero or opposite in sign to the predeclared direction, the confinement-coupling hypothesis is falsified for this domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "density": "native_framework_density_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "density stands in for framework confinement; Vol stands in for adsorbate size; neither resolves molecular or framework detail beyond these proxies.",
      "physical_interpretation": "Native meanings only: heavier framework packing and larger guest volume; all q-normalized quantities are dimensionless row-varying inputs with no physical unity threshold.",
      "boundary_behavior": "All native inputs are strictly positive in the training domain (density min 0.759654, Vol min 20.424), so the expression is finite for every training row; no zero handling is required.",
      "vary_input": "density",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "density"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1548,
      "native_regime_bounds": [
        52.632,
        108.112
      ],
      "training_spearman": 0.5617439607733851,
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
    "slot_id": "h1",
    "name": "framework_density_confinement_quench",
    "formula": "(density / density_ref) * (1 + (Vol / Vol_ref) ** 0.5)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase entropy loss increases with framework density (framework atom packing per volume) and with adsorbate van der Waals volume: denser frameworks confine the guest in tighter environments, and bulkier guests experience a larger entropy reduction upon docking in that confined environment.",
    "rationale": "Framework density is the native inverse-porosity proxy on the published scale; multiplication with an adsorbate volume term encodes a guest-framework confinement coupling rather than either factor alone. Limitations: density is a proxy with unresolved physical unit; Vol is a heavy-atom-derived van der Waals volume; the empirical coupling exponent is a smoothing choice, not a physical law.",
    "falsification_criteria": "If training Spearman between the descriptor and entropy loss within the Vol median regime band is near zero or opposite in sign to the predeclared direction, the confinement-coupling hypothesis is falsified for this domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "density": "native_framework_density_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "density stands in for framework confinement; Vol stands in for adsorbate size; neither resolves molecular or framework detail beyond these proxies.",
      "physical_interpretation": "Native meanings only: heavier framework packing and larger guest volume; all q-normalized quantities are dimensionless row-varying inputs with no physical unity threshold.",
      "boundary_behavior": "All native inputs are strictly positive in the training domain (density min 0.759654, Vol min 20.424), so the expression is finite for every training row; no zero handling is required.",
      "vary_input": "density",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "density"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1548,
      "native_regime_bounds": [
        52.632,
        108.112
      ],
      "training_spearman": 0.5617439607733851,
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
    "slot_id": "h1",
    "name": "framework_density_confinement_quench",
    "formula": "(density / density_ref) * (1 + (Vol / Vol_ref) ** 0.5)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed-phase entropy loss increases with framework density (framework atom packing per volume) and with adsorbate van der Waals volume: denser frameworks confine the guest in tighter environments, and bulkier guests experience a larger entropy reduction upon docking in that confined environment.",
    "rationale": "Framework density is the native inverse-porosity proxy on the published scale; multiplication with an adsorbate volume term encodes a guest-framework confinement coupling rather than either factor alone. Limitations: density is a proxy with unresolved physical unit; Vol is a heavy-atom-derived van der Waals volume; the empirical coupling exponent is a smoothing choice, not a physical law.",
    "falsification_criteria": "If training Spearman between the descriptor and entropy loss within the Vol median regime band is near zero or opposite in sign to the predeclared direction, the confinement-coupling hypothesis is falsified for this domain.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "density": "native_framework_density_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "density stands in for framework confinement; Vol stands in for adsorbate size; neither resolves molecular or framework detail beyond these proxies.",
      "physical_interpretation": "Native meanings only: heavier framework packing and larger guest volume; all q-normalized quantities are dimensionless row-varying inputs with no physical unity threshold.",
      "boundary_behavior": "All native inputs are strictly positive in the training domain (density min 0.759654, Vol min 20.424), so the expression is finite for every training row; no zero handling is required.",
      "vary_input": "density",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "density"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1548,
      "native_regime_bounds": [
        52.632,
        108.112
      ],
      "training_spearman": 0.5617439607733851,
      "target_association": "consistent",
      "perturbation": 0.005792599999999999,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/rag_agent/replicate-3/round-3/h2`

最终状态：scored；边际收益：-9.352936 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "size_free_path_retention",
    "formula": "log(1 + MW / MW_ref) * (lsd_p / lsd_p_ref)",
    "hypothesis": "At infinite dilution, adsorbed-phase entropy loss increases with adsorbate molecular weight (translational quasi-classical entropy scale) and decreases with the largest included free-sphere diameter along the free-sphere path (lsd_p): wider channel interiors preserve more adsorbed-phase translational freedom. The descriptor is constructed so that higher descriptor values correspond to lower entropy loss, i.e. the product encodes size against available interior space.",
    "rationale": "MW sets the guest translational entropy scale; lsd_p (Dif) is a probe of interior space along the diffusion path, distinct from the bottleneck Df. The descriptor is a size-to-space contrast. Limitations: lsd_p is a geometric hard-sphere probe, not the true molecule-specific free volume; MW is not itself an entropy quantity. The log term is an empirical smoothing of the dimensionless MW ratio.",
    "falsification_criteria": "If the descriptor's association with entropy loss within the MW quantile band [0.25, 0.9] is not consistent with the predeclared direction, the space-retention mechanism is falsified; also falsified if the retained AV-based reservoir already explains all framework-side variance.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "MW proxies the classical translational entropy scale; lsd_p (Dif) proxies interior channel space along the path; both are geometric/statistical proxies, not direct entropy observables.",
      "physical_interpretation": "Native meanings: molecular weight and Zeo++ Dif only; Dif is not the bottleneck Df and not the global cavity Di; no q-unity threshold is physical.",
      "boundary_behavior": "MW min 16.0313 and lsd_p min 3.3452 are strictly positive in training, so MW/MW_ref > 0, log(1+x) > 0, and the product is finite for all rows.",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
      "regime_input": "MW",
      "regime_train_quantiles": [
        0.25,
        0.9
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
    "grounding": {
      "status": "passed",
      "used_variables": [
        "MW",
        "lsd_p"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 1548,
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
    "slot_id": "h2",
    "name": "size_free_path_retention",
    "formula": "log(1 + MW / MW_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "At infinite dilution, adsorbed-phase entropy loss increases with adsorbate molecular weight (translational quasi-classical entropy scale) and decreases with the largest included free-sphere diameter along the free-sphere path (lsd_p): wider channel interiors preserve more adsorbed-phase translational freedom. The descriptor is constructed so that higher descriptor values correspond to lower entropy loss, i.e. the product encodes size against available interior space.",
    "rationale": "Corrected the space-contrast sign: larger included-along-path diameter (lsd_p) should preserve translational freedom and reduce entropy loss, so the descriptor must decrease with lsd_p. The previous draft multiplied by lsd_p/lsd_p_ref, contradicting the predeclared direction and failing the precheck. The log term on the MW ratio remains an empirical smoothing choice.",
    "falsification_criteria": "If the descriptor's association with entropy loss within the MW quantile band [0.25, 0.9] is not consistent with the predeclared decreasing-in-lsd_p direction, the space-retention mechanism is falsified; also falsified if the retained AV-based reservoir already explains all framework-side variance.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E04"
    ],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "MW proxies the classical translational entropy scale; lsd_p (Dif) proxies interior channel space along the free-sphere path, not the bottleneck Df and not the global cavity Di; both are geometric/statistical proxies, not direct entropy observables.",
      "physical_interpretation": "Native meanings only: molecular weight and Zeo++ Dif. The ratio lsd_p_ref/lsd_p is a dimensionless row-varying input; unity carries no physical threshold meaning.",
      "boundary_behavior": "MW min 16.0313 and lsd_p min 3.3452 are strictly positive in training, so MW/MW_ref > 0, log(1+x) > 0, and lsd_p_ref/lsd_p is finite and positive for every row.",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
      "regime_input": "MW",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "MW",
        "lsd_p"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1548,
      "native_regime_bounds": [
        56.06260026,
        120.0939004
      ],
      "training_spearman": 0.7395796635334853,
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
    "slot_id": "h2",
    "name": "size_free_path_retention",
    "formula": "log(1 + MW / MW_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "At infinite dilution, adsorbed-phase entropy loss increases with adsorbate molecular weight (translational quasi-classical entropy scale) and decreases with the largest included free-sphere diameter along the free-sphere path (lsd_p): wider channel interiors preserve more adsorbed-phase translational freedom. The descriptor is constructed so that higher descriptor values correspond to lower entropy loss, i.e. the product encodes size against available interior space.",
    "rationale": "Corrected the space-contrast sign: larger included-along-path diameter (lsd_p) should preserve translational freedom and reduce entropy loss, so the descriptor must decrease with lsd_p. The previous draft multiplied by lsd_p/lsd_p_ref, contradicting the predeclared direction and failing the precheck. The log term on the MW ratio remains an empirical smoothing choice.",
    "falsification_criteria": "If the descriptor's association with entropy loss within the MW quantile band [0.25, 0.9] is not consistent with the predeclared decreasing-in-lsd_p direction, the space-retention mechanism is falsified; also falsified if the retained AV-based reservoir already explains all framework-side variance.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E04"
    ],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "MW proxies the classical translational entropy scale; lsd_p (Dif) proxies interior channel space along the free-sphere path, not the bottleneck Df and not the global cavity Di; both are geometric/statistical proxies, not direct entropy observables.",
      "physical_interpretation": "Native meanings only: molecular weight and Zeo++ Dif. The ratio lsd_p_ref/lsd_p is a dimensionless row-varying input; unity carries no physical threshold meaning.",
      "boundary_behavior": "MW min 16.0313 and lsd_p min 3.3452 are strictly positive in training, so MW/MW_ref > 0, log(1+x) > 0, and lsd_p_ref/lsd_p is finite and positive for every row.",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
      "regime_input": "MW",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "MW",
        "lsd_p"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1548,
      "native_regime_bounds": [
        56.06260026,
        120.0939004
      ],
      "training_spearman": 0.7395796635334853,
      "target_association": "consistent",
      "perturbation": 0.0452717,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/rag_agent/replicate-3/round-3/h3`

最终状态：scored；边际收益：-5.630678 pp；保留：False。

复核改动字段：evidence_ids, formula, rationale, scientific_test.boundary_behavior

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "bottleneck_included_contrast_shape_gate",
    "formula": "sqrt(1 + GeDi / GeDi_ref) * (1 + lsd_f_ref / lsd_f) * (lsd_p / lsd_p_ref)",
    "hypothesis": "At infinite dilution, adsorbed-phase entropy loss is governed by a geometric contrast between guest extension and framework connectivity: more extended adsorbates (larger GeDi, heavy-atom max pair distance) lose more configurational freedom, and tighter passing bottlenecks (smaller lsd_f relative to its reference) further quench adsorbed-phase motion, while larger included interior spheres (larger lsd_p) partially restore freedom. The descriptor is constructed so increasing values correspond to increasing entropy loss.",
    "rationale": "Combines a shape factor (GeDi), a connectivity bottleneck factor (1 + Df_ref/Df), and an interior-space factor (Dif/Dif_ref) into a single geometric-path contrast. Limitations: GeDi is a heavy-atom-representation proxy (legitimate zeros exist, hence the 1+ form keeps the expression finite without imputation or invented physics); lsd_f is the passing bottleneck, not a cavity diameter; the exponents 0.5 on the shape factor and the additive-1 forms are empirical smoothings.",
    "falsification_criteria": "If training Spearman within the lsd_p quantile band [0.25, 0.9] is opposite in sign to the predeclared descriptor_direction, or if the descriptor adds no marginal improvement over the retained h1/h2 set, the geometric-path-contrast mechanism is falsified as a distinct contributor.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "GeDi proxies adsorbate extension on the original heavy-atom representation; Df proxies connectivity restriction; Dif proxies interior space. None resolves all-atom geometry or true kinetic barriers governing equilibrium entropy.",
      "physical_interpretation": "Native geometric meanings only: maximum heavy-atom pair distance, Zeo++ Df, Zeo++ Dif. Ratios to fixed positive references are dimensionless row-varying inputs with no physical unity meaning.",
      "boundary_behavior": "GeDi has legitimate training zeros (n=54), so the factor sqrt(1 + GeDi/GeDi_ref) stays finite and positive (value 1) at GeDi = 0 without imputation; lsd_f and lsd_p are strictly positive in training, so their reciprocal/ratio terms are finite for every row.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.25,
        0.9
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
    "grounding": {
      "status": "passed",
      "used_variables": [
        "GeDi",
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_f": "bottleneck_free_sphere_Df",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 1536,
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
    "slot_id": "h3",
    "name": "bottleneck_included_contrast_shape_gate",
    "formula": "sqrt(1 + GeDi / GeDi_ref) * (1 + lsd_f / lsd_f_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "At infinite dilution, adsorbed-phase entropy loss is governed by a geometric contrast between guest extension and framework connectivity: more extended adsorbates (larger GeDi, heavy-atom max pair distance) lose more configurational freedom, and tighter passing bottlenecks (smaller lsd_f relative to its reference) further quench adsorbed-phase motion, while larger included interior spheres (larger lsd_p) partially restore freedom. The descriptor is constructed so increasing values correspond to increasing entropy loss.",
    "rationale": "Sign corrections to match the predeclared direction and prior round-2 diagnostics: the bottleneck factor is now (1 + lsd_f/lsd_f_ref), increasing with wider passing bottlenecks, and the interior-space factor is inverted to lsd_p_ref/lsd_p so that larger included spheres along the path reduce the descriptor. This mirrors the round-2 'included_to_bottleneck_freedom_contrast' form (positive training Spearman 0.213, consistent) while adding the guest-shape factor. The 1+ forms and exponent 0.5 remain empirical smoothings, not physical laws.",
    "falsification_criteria": "If training Spearman within the lsd_p quantile band [0.25, 0.9] is opposite in sign to the predeclared descriptor_direction, or if the descriptor adds no marginal improvement over the retained h1/h2 set, the geometric-path-contrast mechanism is falsified as a distinct contributor.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E02"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "GeDi proxies adsorbate extension on the original heavy-atom representation; Df proxies connectivity restriction; Dif proxies interior space. None resolves all-atom geometry or true kinetic barriers governing equilibrium entropy.",
      "physical_interpretation": "Native geometric meanings only: maximum heavy-atom pair distance, Zeo++ Df, Zeo++ Dif. Ratios to fixed positive references are dimensionless row-varying inputs with no physical unity meaning.",
      "boundary_behavior": "GeDi has legitimate training zeros (n=54), so sqrt(1 + GeDi/GeDi_ref) stays finite and positive (value 1) at GeDi = 0 without imputation; lsd_f and lsd_p are strictly positive in training, so all ratio terms are finite for every row.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_f": "bottleneck_free_sphere_Df",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1536,
      "native_regime_bounds": [
        5.82527,
        9.54223
      ],
      "training_spearman": 0.4768385524065452,
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
    "slot_id": "h3",
    "name": "bottleneck_included_contrast_shape_gate",
    "formula": "sqrt(1 + GeDi / GeDi_ref) * (1 + lsd_f / lsd_f_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "At infinite dilution, adsorbed-phase entropy loss is governed by a geometric contrast between guest extension and framework connectivity: more extended adsorbates (larger GeDi, heavy-atom max pair distance) lose more configurational freedom, and tighter passing bottlenecks (smaller lsd_f relative to its reference) further quench adsorbed-phase motion, while larger included interior spheres (larger lsd_p) partially restore freedom. The descriptor is constructed so increasing values correspond to increasing entropy loss.",
    "rationale": "Sign corrections to match the predeclared direction and prior round-2 diagnostics: the bottleneck factor is now (1 + lsd_f/lsd_f_ref), increasing with wider passing bottlenecks, and the interior-space factor is inverted to lsd_p_ref/lsd_p so that larger included spheres along the path reduce the descriptor. This mirrors the round-2 'included_to_bottleneck_freedom_contrast' form (positive training Spearman 0.213, consistent) while adding the guest-shape factor. The 1+ forms and exponent 0.5 remain empirical smoothings, not physical laws.",
    "falsification_criteria": "If training Spearman within the lsd_p quantile band [0.25, 0.9] is opposite in sign to the predeclared descriptor_direction, or if the descriptor adds no marginal improvement over the retained h1/h2 set, the geometric-path-contrast mechanism is falsified as a distinct contributor.",
    "novelty_status": "uncertain",
    "evidence_ids": [
      "E01",
      "E02"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "GeDi proxies adsorbate extension on the original heavy-atom representation; Df proxies connectivity restriction; Dif proxies interior space. None resolves all-atom geometry or true kinetic barriers governing equilibrium entropy.",
      "physical_interpretation": "Native geometric meanings only: maximum heavy-atom pair distance, Zeo++ Df, Zeo++ Dif. Ratios to fixed positive references are dimensionless row-varying inputs with no physical unity meaning.",
      "boundary_behavior": "GeDi has legitimate training zeros (n=54), so sqrt(1 + GeDi/GeDi_ref) stays finite and positive (value 1) at GeDi = 0 without imputation; lsd_f and lsd_p are strictly positive in training, so all ratio terms are finite for every row.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.25,
        0.9
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
        "lsd_f",
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_f": "bottleneck_free_sphere_Df",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1536,
      "native_regime_bounds": [
        5.82527,
        9.54223
      ],
      "training_spearman": 0.4768385524065452,
      "target_association": "consistent",
      "perturbation": 0.029412300000000006,
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
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd75db1400cf2ce6171ef0f6",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5aff3d9da9c035dec7cb74e7",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d551cda661adcb5ac3f29200",
        "paper_id": "doi:10.1038/s41586-021-03429-y",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ecf3b350af8d5c09a9a10048",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:02756f5540571e85d7747cdc",
        "paper_id": "doi:10.1021/acs.jctc.0c01022",
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
        "record_id": "chunk:3f393dae0a18a5310296642a",
        "paper_id": "doi:10.1039/d3cs00404j",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3f5768387a8e2dd4104cc2f6",
        "paper_id": "doi:10.1039/c3cc40731d",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5179e468ef50b2674a95d1b9",
        "paper_id": "doi:10.1063/1.4706520",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:57ee5f72df780c7e9698cbc9",
        "paper_id": "doi:10.1021/ja0481474",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:5d62cd81d1c76b19dcdcfff9",
        "paper_id": "doi:10.1021/acs.langmuir.2c00923",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cc904c61f240366bfe7825e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9149465393580d1d53d84d0f",
        "paper_id": "doi:10.1002/cphc.202400347",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9a3907e626bcdef0bc5bb0cb",
        "paper_id": "doi:10.1002/chem.201705627",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, adsorbed-phase entropy loss increases with framework density (framework atom packing per volume) and with adsorbate van der Waals volume: denser frameworks confine the guest in tighter environments, and bulkier guests experience a larger entropy reduction upon docking in that confined environment. (density / density_ref) * (1 + (Vol / Vol_ref) ** 0.5) At infinite dilution, adsorbed-phase entropy loss increases with adsorbate molecular weight (translational quasi-classical entropy scale) and decreases with the largest included free-sphere diameter along the free-sphere path (lsd_p): wider channel interiors preserve more adsorbed-phase translational freedom. The descriptor is constructed so that higher descriptor values correspond to lower entropy loss, i.e. the product encodes size against available interior space. log(1 + MW / MW_ref) * (lsd_p / lsd_p_ref) At infinite dilution, adsorbed-phase entropy loss is governed by a geometric contrast between guest extension and framework connectivity: more extended adsorbates (larger GeDi, heavy-atom max pair distance) lose more configurational freedom, and tighter passing bottlenecks (smaller lsd_f relative to its reference) further quench adsorbed-phase motion, while larger included interior spheres (larger lsd_p) partially restore freedom. The descriptor is constructed so increasing values correspond to increasing entropy loss. sqrt(1 + GeDi / GeDi_ref) * (1 + lsd_f_ref / lsd_f) * (lsd_p / lsd_p_ref)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:8ffcc4698d37d4f5569d53f5",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:0d886a705a91409f8e891c53",
      "chunk:11077178fd4d765fcf20a5a1"
    ],
    "items": 10,
    "lexical_tokens": 4564,
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
