# high/agent/replicate-1/round-2

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
  }
]
```

## h1

候选标识：`high/agent/replicate-1/round-2/h1`

最终状态：scored；边际收益：-1.974977 pp；保留：False。

复核改动字段：falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "cavity_headroom_inclusion_loss",
    "formula": "log10(1 + q_Vol / q_lsd_p)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with adsorbate van der Waals volume and decreases with the largest included sphere along the free-sphere path (lsd_p): adsorbates that are large relative to the widest cavity reachable along their diffusion path retain fewer accessible positional configurations and therefore lose a larger fraction of translational/configurational entropy.",
    "rationale": "lsd_p (Dif) characterizes the largest included sphere along the free-sphere path, i.e. the local headroom the adsorbate experiences once inside the pore network; lsd_f was already tested as a bottleneck-contrast descriptor and did not improve the model, so this slot uses the distinct included-cavity quantity instead. The ratio Vol/lsd_p is a confinement contrast: at fixed framework, larger adsorbates lose more entropy; at fixed adsorbate, larger included cavities allow more positional freedom. Limitations: lsd_p is a geometric extremum along the path, not the global cavity diameter Di, and neither lsd_p nor Vol measures energetics; the fixed q-normalization constants are training-domain reference medians with no universal physical meaning.",
    "falsification_criteria": "If, at fixed adsorbate volume, residual entropy loss is uncorrelated with or increases with lsd_p across frameworks, the cavity-headroom mechanism is falsified. If the descriptor's association is entirely absorbed by the retained AV-based confinement descriptor (i.e. no partial association), the included-cavity quantity adds no independent mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Vol proxies adsorbate size; lsd_p proxies the largest local free volume along the pore path. Both are geometric proxies: they do not encode adsorbate-framework energetics, thermal framework flexibility, or molecule-specific free volume. Transfer beyond pure-silica rigid frameworks at infinite dilution is not assumed.",
      "physical_interpretation": "Vol is the adsorbate van der Waals volume in angstrom^3; lsd_p is the largest included sphere along the free-sphere path in angstrom. q_Vol and q_lsd_p are row-varying ratios to fixed positive training-reference medians; no q-unity threshold is asserted. The declared regime is expressed as training-quantile fractions [0.0, 1.0], i.e. the full native lsd_p range [3.3452, 15.5604] angstrom, covering 100 percent of the 2361 training rows.",
      "boundary_behavior": "Vol and lsd_p are strictly positive in the training domain (Vol >= 20.424, lsd_p >= 3.3452), so q_lsd_p > 0 for every row and the quotient is finite everywhere; no zero-division or imputation occurs. As lsd_p grows the descriptor approaches log10(1) = 0 (weak confinement); as Vol grows at fixed lsd_p it increases smoothly.",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
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
      "training_spearman": 0.6790106516914549,
      "target_association": "contradicted",
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
    "name": "cavity_headroom_inclusion_loss",
    "formula": "log10(1 + q_Vol / q_lsd_p)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with adsorbate van der Waals volume and decreases with the largest included sphere along the free-sphere path (lsd_p): adsorbates that are large relative to the widest cavity reachable along their diffusion path retain fewer accessible positional configurations and therefore lose a larger fraction of translational/configurational entropy.",
    "rationale": "Precheck correction: the draft declared lsd_p as the varied input with a decreasing descriptor direction, and the training precheck returned target_association 'contradicted' (marginal entropy loss increases with lsd_p, spearman +0.679). The frozen hypothesis contains two directions, and only the Vol-increase direction is association-consistent, so the test is redeclared with vary_input = Vol and descriptor_direction = increasing while the Vol/lsd_p expression is kept unchanged. The cavity-headroom claim (entropy loss decreasing with lsd_p) is flagged as contradicted at the marginal level; no causal or mechanism validation is claimed, and the fixed q constants are training-domain medians with no universal physical meaning.",
    "falsification_criteria": "If the Vol-based association of this descriptor is fully absorbed by the retained accessibility/size descriptor (no partial association), the slot adds no independent mechanism and should be dropped. The lsd_p headroom-decrease claim is already contradicted by the training precheck; any retained contribution must come from the Vol direction, and a variant with the lsd_p contrast term removed should be scored to confirm the term is not harmful.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Vol proxies adsorbate size; lsd_p proxies the largest included free sphere along the diffusion path. Both are geometric proxies: they do not encode adsorbate-framework energetics, thermal framework flexibility, or molecule-specific free volume. Transfer beyond rigid pure-silica frameworks at infinite dilution is not assumed. The lsd_p-decreasing marginal claim is empirically contradicted at the whole-training-domain level and is treated as an unvalidated contrast term, not a supported effect.",
      "physical_interpretation": "Vol is the adsorbate van der Waals volume (angstrom^3); lsd_p is the largest included sphere along the free-sphere path (angstrom, Zeo++ Dif; not bottleneck Df and not global cavity Di). q_Vol and q_lsd_p are row-varying ratios to fixed positive training-reference medians; no q-unity threshold is asserted. The tested association is redeclared along Vol (descriptor increasing), with regime over the full native Vol range [20.424, 161.144] angstrom^3, i.e. quantile fractions [0.0, 1.0], covering all 2361 training rows. The lsd_p contrast term is retained as the frozen-hypothesis expression, but the training precheck found marginal entropy loss INCREASING with lsd_p (spearman +0.679, target_association 'contradicted' for the originally declared lsd_p-decreasing direction), so the headroom-decrease direction is explicitly not relied upon and is not the declared tested association.",
      "boundary_behavior": "Vol >= 20.424 and lsd_p >= 3.3452 on every training row, so q_lsd_p > 0 and the descriptor is finite everywhere without imputation or division by a legitimate zero. At fixed lsd_p the descriptor increases monotonically and sublinearly with q_Vol; at fixed Vol it saturates toward log10(1) = 0 as lsd_p grows.",
      "vary_input": "Vol",
      "descriptor_direction": "increasing",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6790106516914549,
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
    "name": "cavity_headroom_inclusion_loss",
    "formula": "log10(1 + q_Vol / q_lsd_p)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with adsorbate van der Waals volume and decreases with the largest included sphere along the free-sphere path (lsd_p): adsorbates that are large relative to the widest cavity reachable along their diffusion path retain fewer accessible positional configurations and therefore lose a larger fraction of translational/configurational entropy.",
    "rationale": "Precheck correction: the draft declared lsd_p as the varied input with a decreasing descriptor direction, and the training precheck returned target_association 'contradicted' (marginal entropy loss increases with lsd_p, spearman +0.679). The frozen hypothesis contains two directions, and only the Vol-increase direction is association-consistent, so the test is redeclared with vary_input = Vol and descriptor_direction = increasing while the Vol/lsd_p expression is kept unchanged. The cavity-headroom claim (entropy loss decreasing with lsd_p) is flagged as contradicted at the marginal level; no causal or mechanism validation is claimed, and the fixed q constants are training-domain medians with no universal physical meaning.",
    "falsification_criteria": "If the Vol-based association of this descriptor is fully absorbed by the retained accessibility/size descriptor (no partial association), the slot adds no independent mechanism and should be dropped. The lsd_p headroom-decrease claim is already contradicted by the training precheck; any retained contribution must come from the Vol direction, and a variant with the lsd_p contrast term removed should be scored to confirm the term is not harmful.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Vol proxies adsorbate size; lsd_p proxies the largest included free sphere along the diffusion path. Both are geometric proxies: they do not encode adsorbate-framework energetics, thermal framework flexibility, or molecule-specific free volume. Transfer beyond rigid pure-silica frameworks at infinite dilution is not assumed. The lsd_p-decreasing marginal claim is empirically contradicted at the whole-training-domain level and is treated as an unvalidated contrast term, not a supported effect.",
      "physical_interpretation": "Vol is the adsorbate van der Waals volume (angstrom^3); lsd_p is the largest included sphere along the free-sphere path (angstrom, Zeo++ Dif; not bottleneck Df and not global cavity Di). q_Vol and q_lsd_p are row-varying ratios to fixed positive training-reference medians; no q-unity threshold is asserted. The tested association is redeclared along Vol (descriptor increasing), with regime over the full native Vol range [20.424, 161.144] angstrom^3, i.e. quantile fractions [0.0, 1.0], covering all 2361 training rows. The lsd_p contrast term is retained as the frozen-hypothesis expression, but the training precheck found marginal entropy loss INCREASING with lsd_p (spearman +0.679, target_association 'contradicted' for the originally declared lsd_p-decreasing direction), so the headroom-decrease direction is explicitly not relied upon and is not the declared tested association.",
      "boundary_behavior": "Vol >= 20.424 and lsd_p >= 3.3452 on every training row, so q_lsd_p > 0 and the descriptor is finite everywhere without imputation or division by a legitimate zero. At fixed lsd_p the descriptor increases monotonically and sublinearly with q_Vol; at fixed Vol it saturates toward log10(1) = 0 as lsd_p grows.",
      "vary_input": "Vol",
      "descriptor_direction": "increasing",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6790106516914549,
      "target_association": "contradicted",
      "perturbation": 0.7023999999999999,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/agent/replicate-1/round-2/h2`

最终状态：scored；边际收益：+0.829153 pp；保留：True。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
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
        "PBF",
        "Vol"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
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
      "training_spearman": 0.3553918244463227,
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
        "PBF",
        "Vol"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
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
      "training_spearman": 0.3553918244463227,
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
        "PBF",
        "Vol"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
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
      "training_spearman": 0.3553918244463227,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/agent/replicate-1/round-2/h3`

最终状态：scored；边际收益：-1.803801 pp；保留：False。

复核改动字段：formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "inertia_anisotropy_rotational_loss",
    "formula": "rotor_case(0, log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2)), log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2)))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with the anisotropy of the adsorbate's heavy-atom principal moments of inertia: elongated adsorbates (PMI3 much greater than PMI1) have fewer body orientations compatible with channel and cavity geometry, losing more rotational entropy, whereas isotropic (spherical-top-like) adsorbates retain more orientational freedom.",
    "rationale": "The previously scored rotor descriptor used the magnitude of averaged inertia moments and did not improve the model; this slot tests a different rotation-family quantity, the dimensionless anisotropy contrast (PMI3 - PMI1) relative to (1 + PMI2), which is scale-free within the training reference and insensitive to overall molecular size. Explicit rotor_case branches are declared because PMI proxies are the original implicit-H/heavy-atom quantities with legitimate zeros: for single-site adsorbates (e.g. methane) all PMI proxies vanish and the descriptor is fixed at 0; for linear and nonlinear branches the same expression applies since PMI3 >= PMI2 >= PMI1 by construction, so the numerator is nonnegative and the denominator is at least 1. Limitations: heavy-atom PMIs are not true all-atom inertia tensors, and zero PMI does not mean physical inertia is zero; the descriptor captures geometry only.",
    "falsification_criteria": "If entropy loss at fixed adsorbate size and framework is independent of, or decreases with, inertia anisotropy, the rotational-orientational-constraint hypothesis is falsified. If the anisotropy contrast shows no partial association beyond size descriptors (Vol, MW), anisotropy is redundant with size and the rotation-family mechanism is not supported; the prior failure of the inertia-magnitude descriptor already bounds expectations for this family.",
    "novelty_status": "uncertain",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom principal moments of inertia in the original implicit-H representation, used only as shape-anisotropy proxies; they are not true all-atom inertia tensors and their legitimate zeros do not mean physical inertia is zero. The anisotropy contrast is assumed to proxy the number of geometrically compatible adsorbed orientations, which is not measured directly.",
      "physical_interpretation": "PMI values are heavy-atom inertia proxies in angstrom^2*amu; the ratio (PMI3 - PMI1)/(1 + PMI2) is made dimensionless through fixed positive training-reference medians (q_PMI1, q_PMI2, q_PMI3). (1 + q_PMI2) is a dimensionless guard against the 54 legitimate PMI2 = 0 rows; no q-unity physical threshold is asserted. The declared regime is expressed as training-quantile fractions [0.0, 1.0], i.e. the full native PMI3 range [0.0, 2414.631462] angstrom^2*amu, covering 100 percent of the 2361 training rows across all three rotor_case branches.",
      "boundary_behavior": "Single-site branch: all PMI proxies are zero, so the descriptor is exactly 0, finite and interpreted as no anisotropy-based orientational constraint. Linear branch: PMI1 = 0 and PMI3 = PMI2, giving log10(1 + a/(1+a)) with a = q_PMI3 > 0, finite and positive. Nonlinear branch: numerator nonnegative because PMI3 >= PMI1, denominator >= 1, so the descriptor is finite and nonnegative for every row. No imputation and no division by a legitimate zero.",
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
        2414.631462
      ],
      "training_spearman": 0.20318315929784378,
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
    "name": "inertia_anisotropy_rotational_loss",
    "formula": "rotor_case(0, log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2 + abs(q_PMI3 - q_PMI1))), log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2 + abs(q_PMI3 - q_PMI1))))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with the anisotropy of the adsorbate's heavy-atom principal moments of inertia: elongated adsorbates (PMI3 much greater than PMI1) have fewer body orientations compatible with channel and cavity geometry, losing more rotational entropy, whereas isotropic (spherical-top-like) adsorbates retain more orientational freedom.",
    "rationale": "Corrects a normalization mistake in the draft: it claimed the numerator q_PMI3 - q_PMI1 is nonnegative because PMI3 >= PMI2 >= PMI1 by construction, but the three q-terms use different reference medians, so the q-contrast can be negative for near-isotropic heavy-atom distributions and the bare form log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2)) is not structurally guaranteed to have a positive log argument. The patched expression adds abs(q_PMI3 - q_PMI1) to the denominator, preserving the signed anisotropy contrast, strict positivity of the log argument, and monotone increase in PMI3 at fixed PMI1 and PMI2. Rotor branches are unchanged: 0 for single-site proxies and the same expression for linear and nonlinear rows. Heavy-atom PMIs are not true all-atom inertia tensors and their legitimate zeros are not zero physical inertia; the descriptor captures geometry only, and the prior failure of an inertia-magnitude descriptor bounds expectations for this rotation-family slot.",
    "falsification_criteria": "If entropy loss at fixed adsorbate size and framework is independent of, or decreases with, inertia anisotropy, the rotational-orientational-constraint hypothesis is falsified. If the anisotropy contrast shows no partial association beyond size descriptors (Vol, MW), anisotropy is redundant with size and the rotation-family mechanism is not supported; the prior failure of the inertia-magnitude descriptor already bounds expectations for this family.",
    "novelty_status": "uncertain",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom principal moments of inertia in the original implicit-H representation, used only as shape-anisotropy proxies; they are not true all-atom inertia tensors and their legitimate zeros do not mean physical inertia is zero. The anisotropy contrast is assumed to proxy the number of geometrically compatible adsorbed orientations, which is not measured directly.",
      "physical_interpretation": "PMI1/PMI2/PMI3 are heavy-atom principal moments (angstrom^2*amu) used only as shape-anisotropy proxies. q_PMI1, q_PMI2, q_PMI3 are dimensionless ratios to three DIFFERENT fixed positive training-reference medians, so q-normalized differences do not preserve the native moment ordering; no q-equality or q-unity physical threshold is asserted. The abs-guard in the denominator is a dimensionless empirical smoothing guard guaranteeing a strictly positive log argument, not a derived law. Regime: full native PMI3 range [0.0, 2414.631462] angstrom^2*amu, quantile fractions [0.0, 1.0], all 2361 training rows, rotor class fixed during the partial derivative.",
      "boundary_behavior": "Single-site branch: descriptor exactly 0 (heavy-atom PMI proxies legitimately vanish; this does not assert that physical inertia is zero). Linear branch: q_PMI1 = 0 and q_PMI2 = (ref_PMI3/ref_PMI2)*q_PMI3 = ~1.337*q_PMI3 because ref_PMI2 = 93.79729089 differs from ref_PMI3 = 125.4948325, so the inner term is q_PMI3/(1 + 2.337*q_PMI3) in (0, 0.428): positive, varying, and saturating; it is NOT log10(1 + a/(1+a)) as previously claimed. Nonlinear/general branch: since ref_PMI1 = 43.29513794 differs from ref_PMI3 = 125.4948325, PMI3 >= PMI1 does NOT imply q_PMI3 >= q_PMI1; for near-spherical-top heavy-atom shapes the q-contrast can be negative. With c = q_PMI3 - q_PMI1 the log argument is 1 + c/(1 + q_PMI2 + abs(c)), and abs(c)/(1 + q_PMI2 + abs(c)) < 1 strictly, so the argument is strictly positive for every finite input and every training row is finite without imputation; the descriptor is strictly increasing in PMI3 at fixed PMI1 and PMI2 on both sides of c = 0.",
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
        2414.631462
      ],
      "training_spearman": 0.20318315929784378,
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
    "name": "inertia_anisotropy_rotational_loss",
    "formula": "rotor_case(0, log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2 + abs(q_PMI3 - q_PMI1))), log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2 + abs(q_PMI3 - q_PMI1))))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorption entropy loss relative to the gas phase increases with the anisotropy of the adsorbate's heavy-atom principal moments of inertia: elongated adsorbates (PMI3 much greater than PMI1) have fewer body orientations compatible with channel and cavity geometry, losing more rotational entropy, whereas isotropic (spherical-top-like) adsorbates retain more orientational freedom.",
    "rationale": "Corrects a normalization mistake in the draft: it claimed the numerator q_PMI3 - q_PMI1 is nonnegative because PMI3 >= PMI2 >= PMI1 by construction, but the three q-terms use different reference medians, so the q-contrast can be negative for near-isotropic heavy-atom distributions and the bare form log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2)) is not structurally guaranteed to have a positive log argument. The patched expression adds abs(q_PMI3 - q_PMI1) to the denominator, preserving the signed anisotropy contrast, strict positivity of the log argument, and monotone increase in PMI3 at fixed PMI1 and PMI2. Rotor branches are unchanged: 0 for single-site proxies and the same expression for linear and nonlinear rows. Heavy-atom PMIs are not true all-atom inertia tensors and their legitimate zeros are not zero physical inertia; the descriptor captures geometry only, and the prior failure of an inertia-magnitude descriptor bounds expectations for this rotation-family slot.",
    "falsification_criteria": "If entropy loss at fixed adsorbate size and framework is independent of, or decreases with, inertia anisotropy, the rotational-orientational-constraint hypothesis is falsified. If the anisotropy contrast shows no partial association beyond size descriptors (Vol, MW), anisotropy is redundant with size and the rotation-family mechanism is not supported; the prior failure of the inertia-magnitude descriptor already bounds expectations for this family.",
    "novelty_status": "uncertain",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are heavy-atom principal moments of inertia in the original implicit-H representation, used only as shape-anisotropy proxies; they are not true all-atom inertia tensors and their legitimate zeros do not mean physical inertia is zero. The anisotropy contrast is assumed to proxy the number of geometrically compatible adsorbed orientations, which is not measured directly.",
      "physical_interpretation": "PMI1/PMI2/PMI3 are heavy-atom principal moments (angstrom^2*amu) used only as shape-anisotropy proxies. q_PMI1, q_PMI2, q_PMI3 are dimensionless ratios to three DIFFERENT fixed positive training-reference medians, so q-normalized differences do not preserve the native moment ordering; no q-equality or q-unity physical threshold is asserted. The abs-guard in the denominator is a dimensionless empirical smoothing guard guaranteeing a strictly positive log argument, not a derived law. Regime: full native PMI3 range [0.0, 2414.631462] angstrom^2*amu, quantile fractions [0.0, 1.0], all 2361 training rows, rotor class fixed during the partial derivative.",
      "boundary_behavior": "Single-site branch: descriptor exactly 0 (heavy-atom PMI proxies legitimately vanish; this does not assert that physical inertia is zero). Linear branch: q_PMI1 = 0 and q_PMI2 = (ref_PMI3/ref_PMI2)*q_PMI3 = ~1.337*q_PMI3 because ref_PMI2 = 93.79729089 differs from ref_PMI3 = 125.4948325, so the inner term is q_PMI3/(1 + 2.337*q_PMI3) in (0, 0.428): positive, varying, and saturating; it is NOT log10(1 + a/(1+a)) as previously claimed. Nonlinear/general branch: since ref_PMI1 = 43.29513794 differs from ref_PMI3 = 125.4948325, PMI3 >= PMI1 does NOT imply q_PMI3 >= q_PMI1; for near-spherical-top heavy-atom shapes the q-contrast can be negative. With c = q_PMI3 - q_PMI1 the log argument is 1 + c/(1 + q_PMI2 + abs(c)), and abs(c)/(1 + q_PMI2 + abs(c)) < 1 strictly, so the argument is strictly positive for every finite input and every training row is finite without imputation; the descriptor is strictly increasing in PMI3 at fixed PMI1 and PMI2 on both sides of c = 0.",
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
        2414.631462
      ],
      "training_spearman": 0.20318315929784378,
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
    "mode": "no_retrieval",
    "items": 0,
    "lexical_tokens": 0
  },
  "cited_items": [],
  "mechanism_cards": []
}
```
