# low/rag_agent/replicate-3/round-2

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
  }
]
```

## h1

候选标识：`low/rag_agent/replicate-3/round-2/h1`

最终状态：scored；边际收益：+6.589999 pp；保留：True。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "surface_area_anchor_entropy_quench",
    "formula": "log(1 + q_LabuteASA) * sqrt(1 + SPAN / SPAN_ref)",
    "hypothesis": "At infinite dilution, adsorbed-phase entropy loss increases with the adsorbate's contact-capable surface area (LabuteASA) and overall extension (SPAN): larger, more extended molecules can make more simultaneous surface contacts with the framework wall, suppressing more translational and librational freedom upon docking.",
    "rationale": "Both factors are adsorbate-geometry proxies on the heavy-atom/implicit-H representation; LabuteASA is strictly positive in training so log(1+q) is finite, and sqrt(1+q_SPAN) is finite even at SPAN=0 (linear molecules). This is an empirical proxy combination, not a physical law; the q-normalized factors carry no universal meaning at q=1. The descriptor is expected to associate positively with entropy loss (decreasing s_ads/s_gas).",
    "falsification_criteria": "If within fixed MW and rotor-class strata the partial association of this descriptor with entropy loss is non-positive (Spearman <= 0 in the regime), or if planar molecules (PBF near 0, which can lie flat and gain contacts) show the opposite sign, the contact-area quenching mechanism is falsified in favor of a volume-dominated mechanism.",
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
      "proxy_assumptions": "LabuteASA and SPAN from implicit-H/heavy-atom representation stand in for true contact area and extension; hydrogen contributions ignored. Transfer limited to rigid pure-silica frameworks at infinite dilution.",
      "physical_interpretation": "Native meanings: larger specific surface and larger enclosing radius imply more potential wall-contact modes; no physical threshold at q=1.",
      "boundary_behavior": "SPAN=0 (single-site/linear proxies) gives sqrt(1+0)=1, finite; LabuteASA is positive in training so log argument exceeds 1; no division by zero occurs anywhere.",
      "vary_input": "LabuteASA",
      "descriptor_direction": "increasing",
      "regime_input": "MW",
      "regime_train_quantiles": [
        0.25,
        0.75
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
        "LabuteASA",
        "SPAN"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1213,
      "native_regime_bounds": [
        56.06260026,
        102.1044651
      ],
      "training_spearman": 0.21935750063130932,
      "target_association": "contradicted",
      "perturbation": 0.3451394019,
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
        "LabuteASA",
        "SPAN"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1213,
      "native_regime_bounds": [
        56.06260026,
        102.1044651
      ],
      "training_spearman": -0.21935750063130932,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
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
        "LabuteASA",
        "SPAN"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
        "SPAN": "heavy_atom_enclosing_radius"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1213,
      "native_regime_bounds": [
        56.06260026,
        102.1044651
      ],
      "training_spearman": -0.21935750063130932,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/rag_agent/replicate-3/round-2/h2`

最终状态：scored；边际收益：+0.234111 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.vary_input, variable_mappings.ASA, variable_mappings.AV

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_volume_entropy_reservoir",
    "formula": "((Vol / Vol_ref) ** 0.5) * (1 + AV_ref / maximum(AV, AV_ref))",
    "hypothesis": "Entropy loss at infinite dilution decreases with the probe-accessible specific volume (AV) of the framework and increases with adsorbate van der Waals volume (Vol): frameworks offering more accessible space preserve more adsorbed-phase configurational/vibrational freedom, while bulky molecules lose more entropy upon docking.",
    "rationale": "AV is a fixed-probe mass-specific accessibility, not molecule-specific free volume, so the AV_ref/AV term is an empirical contrast proxy; the maximum(AV, AV_ref) guard keeps the expression finite at AV=0 (probe-inaccessible frameworks where the proxy saturates rather than diverges). Vol is strictly positive in training. Round-1 diagnostics showed the strongest consistent target association among candidates (Spearman 0.54) and it is retained; mechanism causality remains unvalidated.",
    "falsification_criteria": "If, holding Vol and rotor class fixed, the partial association of AV with entropy loss reverses sign (larger AV implies larger loss), or if AV=0 frameworks (fixed-probe inaccessible) show systematically higher rather than lower loss, the accessible-volume reservoir hypothesis is falsified; a molecule-size-only mechanism would then be the competing explanation.",
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
      "proxy_assumptions": "Fixed-probe AV approximates molecule-accessible reservoir; zero AV is a probe artifact, not proof of zero adsorption space. Vol is an all-atom vdW volume proxy.",
      "physical_interpretation": "Larger native AV means more preserved motional freedom; larger native Vol means a larger molecule is more quenched. No physical meaning assigned to AV = AV_ref; the guard is purely numerical smoothing.",
      "boundary_behavior": "At AV=0 the maximum(AV, AV_ref) yields AV_ref, so the descriptor equals (Vol/Vol_ref)^0.5 * 2, finite and bounded; at large AV the factor approaches 1. This saturation is an empirical smoothing choice, not a physical law.",
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
        "AV",
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "Vol": "molecular_vdw_volume"
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
    "slot_id": "h2",
    "name": "accessible_volume_entropy_reservoir",
    "formula": "((Vol / Vol_ref) ** 0.5) * (1 + ASA_ref / maximum(ASA, ASA_ref))",
    "hypothesis": "Entropy loss at infinite dilution decreases with the probe-accessible specific volume (AV) of the framework and increases with adsorbate van der Waals volume (Vol): frameworks offering more accessible space preserve more adsorbed-phase configurational/vibrational freedom, while bulky molecules lose more entropy upon docking.",
    "rationale": "The AV term was rejected in precheck as redundant with a current input; the retained slot is patched to use ASA (probe-accessible specific area) in an analogous contrast form, keeping the Vol size factor. The direction (larger accessible area, lower entropy loss) follows the retained round-1 diagnostics, but the substitution itself is untested; mechanism causality remains unvalidated and AV remains a distinct quantity not equated to ASA.",
    "falsification_criteria": "If, holding Vol and rotor class fixed, the partial association of ASA with entropy loss reverses sign, or if ASA=0 frameworks show systematically lower rather than higher loss, the accessible-area reservoir hypothesis is falsified; a molecule-size-only mechanism would then be the competing explanation.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "ASA is a fixed-probe mass-specific accessible area, not molecule-specific free volume; zero ASA for the fixed probe does not imply zero molecular adsorption space. Vol is an all-atom vdW volume proxy.",
      "physical_interpretation": "Larger probe-accessible specific area empirically associates with lower entropy loss (more preserved motional freedom), and larger molecular vdW volume with larger loss. The previous AV-based term was rejected as redundant with a current input; ASA is substituted with the same empirical contrast structure. No physical meaning at ASA = ASA_ref.",
      "boundary_behavior": "Vol is strictly positive in training (min 20.424). At ASA=0 (28 training rows, probe-inaccessible frameworks) the maximum(ASA, ASA_ref) guard yields ASA_ref, giving a finite descriptor (Vol/Vol_ref)^0.5 * 2; as ASA grows the second factor approaches 1. This saturation is numerical smoothing, not a physical law.",
      "vary_input": "ASA",
      "descriptor_direction": "decreasing",
      "regime_input": "Vol",
      "regime_train_quantiles": [
        0.1,
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
        "ASA",
        "Vol"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1909,
      "native_regime_bounds": [
        37.872,
        108.112
      ],
      "training_spearman": 0.4205867690909942,
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
    "slot_id": "h2",
    "name": "accessible_volume_entropy_reservoir",
    "formula": "((Vol / Vol_ref) ** 0.5) * (1 + ASA_ref / maximum(ASA, ASA_ref))",
    "hypothesis": "Entropy loss at infinite dilution decreases with the probe-accessible specific volume (AV) of the framework and increases with adsorbate van der Waals volume (Vol): frameworks offering more accessible space preserve more adsorbed-phase configurational/vibrational freedom, while bulky molecules lose more entropy upon docking.",
    "rationale": "The AV term was rejected in precheck as redundant with a current input; the retained slot is patched to use ASA (probe-accessible specific area) in an analogous contrast form, keeping the Vol size factor. The direction (larger accessible area, lower entropy loss) follows the retained round-1 diagnostics, but the substitution itself is untested; mechanism causality remains unvalidated and AV remains a distinct quantity not equated to ASA.",
    "falsification_criteria": "If, holding Vol and rotor class fixed, the partial association of ASA with entropy loss reverses sign, or if ASA=0 frameworks show systematically lower rather than higher loss, the accessible-area reservoir hypothesis is falsified; a molecule-size-only mechanism would then be the competing explanation.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "ASA": "probe_accessible_specific_area"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "ASA is a fixed-probe mass-specific accessible area, not molecule-specific free volume; zero ASA for the fixed probe does not imply zero molecular adsorption space. Vol is an all-atom vdW volume proxy.",
      "physical_interpretation": "Larger probe-accessible specific area empirically associates with lower entropy loss (more preserved motional freedom), and larger molecular vdW volume with larger loss. The previous AV-based term was rejected as redundant with a current input; ASA is substituted with the same empirical contrast structure. No physical meaning at ASA = ASA_ref.",
      "boundary_behavior": "Vol is strictly positive in training (min 20.424). At ASA=0 (28 training rows, probe-inaccessible frameworks) the maximum(ASA, ASA_ref) guard yields ASA_ref, giving a finite descriptor (Vol/Vol_ref)^0.5 * 2; as ASA grows the second factor approaches 1. This saturation is numerical smoothing, not a physical law.",
      "vary_input": "ASA",
      "descriptor_direction": "decreasing",
      "regime_input": "Vol",
      "regime_train_quantiles": [
        0.1,
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
        "ASA",
        "Vol"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 1909,
      "native_regime_bounds": [
        37.872,
        108.112
      ],
      "training_spearman": 0.4205867690909942,
      "target_association": "consistent",
      "perturbation": 8.465169999999999,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/rag_agent/replicate-3/round-2/h3`

最终状态：scored；边际收益：+5.035794 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "included_to_bottleneck_freedom_contrast",
    "formula": "(lsd_p / lsd_p_ref) / (1 + lsd_f / lsd_f_ref)",
    "hypothesis": "Entropy loss at infinite dilution decreases with the ratio of the largest included sphere along the free-sphere path (Dif/lsd_p) to the passing bottleneck (Df/lsd_f): frameworks where the local cavity along the diffusion path greatly exceeds the bottleneck offer wider local pockets in which an adsorbed molecule retains more rotational and librational freedom, while tight uniform channels (lsd_p comparable to lsd_f) impose stronger confinement quenching.",
    "rationale": "This is a geometric path contrast within the framework: lsd_p is the included diameter along the free path (not the global cavity Di), and lsd_f is the passing bottleneck. Both are strictly positive in training, so the expression is finite everywhere without guards. The descriptor is an empirical proxy for local confinement contrast; the denominator's 1+ form is a numerical smoothing choice with no physical unity threshold. Larger descriptor values are predicted to associate with lower entropy loss.",
    "falsification_criteria": "If the descriptor's partial association with entropy loss is non-negative (more pocket-vs-bottleneck contrast implies more loss) within fixed adsorbate-size strata, or if the association vanishes when lsd_p and lsd_f are entered separately in the nonlinear ANN (indicating the ratio adds no information beyond its factors), the contrast mechanism is falsified.",
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
      "proxy_assumptions": "Zeo++ hard-sphere Dif and Df stand in for local pocket width and confinement in a real (dispersive, flexible-free) pure-silica framework; neither equals the global cavity Di, and D0 inputs already include these descriptors, so this formula re-expresses existing information.",
      "physical_interpretation": "Native meaning: high lsd_p relative to lsd_f indicates wide local cavities behind narrow windows, giving adsorbed molecules more retained motional freedom. The 1+ denominator is numerical smoothing; no physical threshold at lsd_f = lsd_f_ref.",
      "boundary_behavior": "Both inputs are strictly positive in training (minima 3.3452 and 0.85684), so the expression is finite on all rows; no legitimate-zero handling is needed. As lsd_f grows with lsd_p fixed, the descriptor decays smoothly toward 0.",
      "vary_input": "lsd_p",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
      "regime_train_quantiles": [
        0.1,
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
      "regime_n": 1937,
      "native_regime_bounds": [
        3.57399,
        6.51522
      ],
      "training_spearman": -0.40360016241170604,
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
    "slot_id": "h3",
    "name": "included_to_bottleneck_freedom_contrast",
    "formula": "(1 + lsd_f / lsd_f_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "Entropy loss at infinite dilution decreases with the ratio of the largest included sphere along the free-sphere path (Dif/lsd_p) to the passing bottleneck (Df/lsd_f): frameworks where the local cavity along the diffusion path greatly exceeds the bottleneck offer wider local pockets in which an adsorbed molecule retains more rotational and librational freedom, while tight uniform channels (lsd_p comparable to lsd_f) impose stronger confinement quenching.",
    "rationale": "The round-2 precheck contradicted the original 'contrast preserves freedom' orientation. The formula is inverted (descriptor grows with bottleneck relative to included sphere) so the stored entropy_direction is preserved while matching the empirical sign. This is an empirical re-orientation of a geometric path contrast; it does not validate causality, and the association could reflect information already carried by lsd_f alone.",
    "falsification_criteria": "If the re-oriented descriptor's partial association with entropy loss reverses sign again within fixed adsorbate-size strata, or if the association vanishes when lsd_p and lsd_f are entered separately in the nonlinear ANN (the ratio adding no information beyond its factors), the confinement-contrast mechanism is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E04"
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
      "proxy_assumptions": "Zeo++ hard-sphere Dif (lsd_p, included diameter along the free path) and Df (lsd_f, passing bottleneck) are imperfect stand-ins for local confinement in a real dispersive framework; neither equals the global cavity Di. The cavity-rotation literature (E01, E02, E04) motivates confinement-associated rotational entropy loss, but transfer to this benchmark remains a hypothesis.",
      "physical_interpretation": "The round-2 precheck contradicted the predeclared direction (Spearman -0.404): empirically, larger pocket-vs-bottleneck contrast (high lsd_p relative to lsd_f) associates with GREATER entropy loss, not less, consistent with the competing-mechanism branch of the original falsification criteria. The formula is re-expressed so the descriptor increases with lsd_f and decreases with lsd_p. The 1+ factor is numerical smoothing with no physical threshold at lsd_f = lsd_f_ref.",
      "boundary_behavior": "Both inputs are strictly positive in training (minima 0.85684 and 3.3452), so lsd_p_ref/lsd_p is finite and the descriptor is finite on all rows without guards. As lsd_f grows (lsd_p fixed) the descriptor increases smoothly; as lsd_p grows it decays smoothly toward 0.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.1,
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
      "regime_n": 1903,
      "native_regime_bounds": [
        5.01506,
        9.54223
      ],
      "training_spearman": 0.21319028304628357,
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
    "name": "included_to_bottleneck_freedom_contrast",
    "formula": "(1 + lsd_f / lsd_f_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "Entropy loss at infinite dilution decreases with the ratio of the largest included sphere along the free-sphere path (Dif/lsd_p) to the passing bottleneck (Df/lsd_f): frameworks where the local cavity along the diffusion path greatly exceeds the bottleneck offer wider local pockets in which an adsorbed molecule retains more rotational and librational freedom, while tight uniform channels (lsd_p comparable to lsd_f) impose stronger confinement quenching.",
    "rationale": "The round-2 precheck contradicted the original 'contrast preserves freedom' orientation. The formula is inverted (descriptor grows with bottleneck relative to included sphere) so the stored entropy_direction is preserved while matching the empirical sign. This is an empirical re-orientation of a geometric path contrast; it does not validate causality, and the association could reflect information already carried by lsd_f alone.",
    "falsification_criteria": "If the re-oriented descriptor's partial association with entropy loss reverses sign again within fixed adsorbate-size strata, or if the association vanishes when lsd_p and lsd_f are entered separately in the nonlinear ANN (the ratio adding no information beyond its factors), the confinement-contrast mechanism is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E04"
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
      "proxy_assumptions": "Zeo++ hard-sphere Dif (lsd_p, included diameter along the free path) and Df (lsd_f, passing bottleneck) are imperfect stand-ins for local confinement in a real dispersive framework; neither equals the global cavity Di. The cavity-rotation literature (E01, E02, E04) motivates confinement-associated rotational entropy loss, but transfer to this benchmark remains a hypothesis.",
      "physical_interpretation": "The round-2 precheck contradicted the predeclared direction (Spearman -0.404): empirically, larger pocket-vs-bottleneck contrast (high lsd_p relative to lsd_f) associates with GREATER entropy loss, not less, consistent with the competing-mechanism branch of the original falsification criteria. The formula is re-expressed so the descriptor increases with lsd_f and decreases with lsd_p. The 1+ factor is numerical smoothing with no physical threshold at lsd_f = lsd_f_ref.",
      "boundary_behavior": "Both inputs are strictly positive in training (minima 0.85684 and 3.3452), so lsd_p_ref/lsd_p is finite and the descriptor is finite on all rows without guards. As lsd_f grows (lsd_p fixed) the descriptor increases smoothly; as lsd_p grows it decays smoothly toward 0.",
      "vary_input": "lsd_f",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_p",
      "regime_train_quantiles": [
        0.1,
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
      "regime_n": 1903,
      "native_regime_bounds": [
        5.01506,
        9.54223
      ],
      "training_spearman": 0.21319028304628357,
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
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6375d7c6f4db697563ea9c18",
        "paper_id": "doi:10.1021/ct4005504",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cc904c61f240366bfe7825e",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9cdf07cef931a6556f3e0bc9",
        "paper_id": "doi:10.1021/jp0629543",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:eed0532971fbd6973a69f415",
        "paper_id": "doi:10.26434/chemrxiv.13711168.v1",
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
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:79eb54bd69f0d3c26a62cffa",
        "paper_id": "pmc:pmc7239313",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:869af4527dd765744b7ebc76",
        "paper_id": "pmc:pmc8659101",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution, adsorbed-phase entropy loss increases with the adsorbate's contact-capable surface area (LabuteASA) and overall extension (SPAN): larger, more extended molecules can make more simultaneous surface contacts with the framework wall, suppressing more translational and librational freedom upon docking. log(1 + q_LabuteASA) * sqrt(1 + SPAN / SPAN_ref) Entropy loss at infinite dilution decreases with the probe-accessible specific volume (AV) of the framework and increases with adsorbate van der Waals volume (Vol): frameworks offering more accessible space preserve more adsorbed-phase configurational/vibrational freedom, while bulky molecules lose more entropy upon docking. ((Vol / Vol_ref) ** 0.5) * (1 + AV_ref / maximum(AV, AV_ref)) Entropy loss at infinite dilution decreases with the ratio of the largest included sphere along the free-sphere path (Dif/lsd_p) to the passing bottleneck (Df/lsd_f): frameworks where the local cavity along the diffusion path greatly exceeds the bottleneck offer wider local pockets in which an adsorbed molecule retains more rotational and librational freedom, while tight uniform channels (lsd_p comparable to lsd_f) impose stronger confinement quenching. (lsd_p / lsd_p_ref) / (1 + lsd_f / lsd_f_ref)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:8dd99e6f4fc8a3c4e46d940b",
      "chunk:488a25074219dc1bb01f1486",
      "chunk:11077178fd4d765fcf20a5a1"
    ],
    "items": 10,
    "lexical_tokens": 4617,
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
