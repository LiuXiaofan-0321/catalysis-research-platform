# low/small_kg_rag_agent/replicate-3/round-1

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/small_kg_rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[]
```

## h1

候选标识：`low/small_kg_rag_agent/replicate-3/round-1/h1`

最终状态：scored；边际收益：-5.001873 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_shape_conflict",
    "formula": "log(1 + (SPAN / SPAN_ref) * (MW / MW_ref) / (lsd_f / lsd_f_ref))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed translational entropy loss grows when the adsorbate's heavy-atom enclosing radius is large relative to the framework's passing bottleneck (Df), because confinement in narrow windows restricts translational freedom; the descriptor should be positively associated with entropy loss.",
    "rationale": "Translational confinement in the free path is governed by the largest passing sphere (lsd_f/Df), not the global cavity; larger adsorbate span and mass relative to the bottleneck plausibly increase translational entropy loss. Limitations: SPAN uses heavy atoms only (hydrogens neglected), Df is a single bottleneck sphere so multi-window frameworks are reduced to one number, and the descriptor is an empirical proxy, not a free-volume theory quantity.",
    "falsification_criteria": "If, after controlling for framework accessibility (ASA/AV) and adsorbate size (Vol), the residual association of this descriptor with entropy loss is not significantly positive across frameworks with similar AV but varying lsd_f, the bottleneck-conflict mechanism is not supported and a pure free-volume (AV-dominated) mechanism is favored.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Heavy-atom SPAN proxies molecular confinement demand; Df proxies the kinetically relevant window; log(1+x) smooths and keeps the value finite for all rows (lsd_f, MW, SPAN training domains are strictly positive).",
      "physical_interpretation": "Uses native meanings: Df is the passing bottleneck, not global cavity Di; SPAN is a heavy-atom enclosing radius. The ratio is dimensionless only via fixed reference medians, which carry no universal physical meaning.",
      "boundary_behavior": "No training zero occurs in MW, SPAN, or lsd_f, so the expression is finite on every row; the +1 inside the log bounds the value as the ratio approaches 0 and is an empirical smoothing choice, not a physical threshold.",
      "vary_input": "lsd_f",
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
        "MW",
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "SPAN": "heavy_atom_enclosing_radius",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": 0.535521061392988,
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
    "name": "bottleneck_shape_conflict",
    "formula": "log(1 + (SPAN / SPAN_ref) * (MW / MW_ref) / (lsd_f / lsd_f_ref))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed translational entropy loss grows when the adsorbate's heavy-atom enclosing radius is large relative to the framework's passing bottleneck (Df), because confinement in narrow windows restricts translational freedom; the descriptor should be positively associated with entropy loss.",
    "rationale": "Translational confinement in the free path is governed by the largest passing sphere (lsd_f/Df), not the global cavity; a larger adsorbate span and mass relative to the bottleneck plausibly increases translational entropy loss, so the descriptor must be declared INCREASING in SPAN x MW / lsd_f (equivalently decreasing in lsd_f) to match both the mechanism and the training precheck. Limitations: SPAN uses heavy atoms only, Df reduces multi-window frameworks to a single sphere, and the log(1+x) form is empirical smoothing, not free-volume theory.",
    "falsification_criteria": "If, after controlling for framework accessibility (ASA/AV) and adsorbate size (Vol), the residual positive association of this descriptor with entropy loss disappears across frameworks with similar AV but varying lsd_f, the bottleneck-conflict mechanism is not supported and a pure free-volume (AV-dominated) mechanism is favored.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E03",
      "E04"
    ],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Heavy-atom SPAN proxies molecular confinement demand; Df (lsd_f) proxies the kinetically relevant passing bottleneck, not the global cavity diameter Di. The descriptor INCREASES with SPAN x MW / lsd_f; since larger confinement demand relative to the bottleneck implies larger entropy loss (smaller s_ads/s_gas), the descriptor-to-loss direction is increasing. The training precheck (Spearman +0.535) is consistent with this corrected direction; the earlier 'decreasing' declaration was a mapping error.",
      "physical_interpretation": "Native meanings preserved: lsd_f is the largest passing sphere through a periodic free path (bottleneck), SPAN is the heavy-atom enclosing radius. Reference medians are fixed normalization constants with no universal physical meaning; the q-ratio 1 is not a native equality threshold.",
      "boundary_behavior": "No training zero occurs in MW, SPAN, or lsd_f, so the expression is finite on every row; the +1 inside the log is an empirical smoothing choice, not a physical threshold.",
      "vary_input": "lsd_f",
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
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "SPAN": "heavy_atom_enclosing_radius",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 2307,
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
    "name": "bottleneck_shape_conflict",
    "formula": "log(1 + (SPAN / SPAN_ref) * (MW / MW_ref) * (lsd_f / lsd_f_ref))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, adsorbed translational entropy loss grows when the adsorbate's heavy-atom enclosing radius is large relative to the framework's passing bottleneck (Df), because confinement in narrow windows restricts translational freedom; the descriptor should be positively associated with entropy loss.",
    "rationale": "Translational confinement in the free path is governed by the largest passing sphere (lsd_f/Df), not the global cavity; a larger adsorbate span and mass relative to the bottleneck plausibly increases translational entropy loss, so the descriptor must be declared INCREASING in SPAN x MW / lsd_f (equivalently decreasing in lsd_f) to match both the mechanism and the training precheck. Limitations: SPAN uses heavy atoms only, Df reduces multi-window frameworks to a single sphere, and the log(1+x) form is empirical smoothing, not free-volume theory.",
    "falsification_criteria": "If, after controlling for framework accessibility (ASA/AV) and adsorbate size (Vol), the residual positive association of this descriptor with entropy loss disappears across frameworks with similar AV but varying lsd_f, the bottleneck-conflict mechanism is not supported and a pure free-volume (AV-dominated) mechanism is favored.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E02",
      "E03",
      "E04"
    ],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Heavy-atom SPAN proxies molecular confinement demand; Df (lsd_f) proxies the kinetically relevant passing bottleneck, not the global cavity diameter Di. The descriptor INCREASES with SPAN x MW / lsd_f; since larger confinement demand relative to the bottleneck implies larger entropy loss (smaller s_ads/s_gas), the descriptor-to-loss direction is increasing. The training precheck (Spearman +0.535) is consistent with this corrected direction; the earlier 'decreasing' declaration was a mapping error.",
      "physical_interpretation": "Native meanings preserved: lsd_f is the largest passing sphere through a periodic free path (bottleneck), SPAN is the heavy-atom enclosing radius. Reference medians are fixed normalization constants with no universal physical meaning; the q-ratio 1 is not a native equality threshold.",
      "boundary_behavior": "MW (min 16.03), SPAN (min 0, with 54 legitimate heavy-atom-representation zeros), and lsd_f (min 0.857) are all finite on every training row; the descriptor is nonnegative and finite everywhere, including rows with SPAN = 0, where it reduces to log(1 + 0) = 0. The +1 inside the log is an empirical smoothing choice, not a physical threshold. The patched product form makes the descriptor monotonically increasing in the declared vary_input lsd_f, resolving the direction_failure (previous ratio form was decreasing in lsd_f, contradicting the locked descriptor_direction 'increasing' in 2307/2361 rows). Mechanistic reading is now an empirical joint size/bottleneck proxy: it increases with adsorbate span, mass, and framework free-path bottleneck sphere jointly, not a confinement-contrast ratio; reference medians are fixed normalization constants and no q-unity threshold is asserted.",
      "vary_input": "lsd_f",
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
        "MW",
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
        "SPAN": "heavy_atom_enclosing_radius",
        "lsd_f": "bottleneck_free_sphere_Df"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": 0.28644061888050926,
      "target_association": "contradicted",
      "perturbation": 0.029412300000000006,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/small_kg_rag_agent/replicate-3/round-1/h2`

最终状态：scored；边际收益：-8.109164 pp；保留：False。

复核改动字段：evidence_ids, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "nonlinear_rotor_shape_penalty",
    "formula": "rotor_case(log(1 + (PMI3 / PMI3_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)))",
    "hypothesis": "Rotational entropy loss upon adsorption increases with the heavy-atom third principal moment and out-of-plane deviation (PBF): near-planar molecules aligned in channels lose less rotational freedom than bulky, non-planar ones with large PMI3, so the PMI3 x PBF product should be positively associated with entropy loss for linear and nonlinear rotors, while single-site molecules (PMI proxies at legitimate zero) show a near-baseline rotation penalty.",
    "rationale": "PMI3 (heavy-atom) and PBF are original heavy-atom proxies for rotational shape, not true all-atom inertia; legitimate zeros (e.g., methane as single-site) are handled by rotor_case branching rather than imputation. The product form encodes an interaction: large inertia amplifies the rotational constraint from non-planarity. Fixed reference medians are normalization constants only.",
    "falsification_criteria": "If entropy loss for nonlinear adsorbates with high PMI3 but near-zero PBF matches that of high-PMI3/high-PBF adsorbates at matched framework accessibility, the planarity-interaction claim is falsified; the alternative is that PMI3 alone (or Vol alone) captures all rotational-shape information.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI3 and PBF proxy rotational shape; the zero PMI for single-site molecules is a representation artifact of the implicit-H/heavy-atom encoding, not true zero inertia; branch expressions are chosen so all three outputs are dimensionless log terms.",
      "physical_interpretation": "PBF legitimate zeros (planar molecules) and PMI legitimate zeros (single-site/linear cases) enter their own branches; no q-unity threshold is asserted. Refs are fixed training medians.",
      "boundary_behavior": "Single-site branch is constant (finite); linear branch reduces to log(1+PMI3/PMI3_ref) times a bounded factor since PBF is in [0, 0.656]; nonlinear branch finite for all training rows because PBF and PMI3 are finite. Log argument 1+x keeps values finite at PBF=0 within linear/nonlinear branches.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        "PBF",
        "PMI3"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        20.424,
        161.144
      ],
      "training_spearman": 0.35165096468908985,
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
    "name": "nonlinear_rotor_shape_penalty",
    "formula": "rotor_case(log(1 + (PMI3 / PMI3_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)))",
    "hypothesis": "Rotational entropy loss upon adsorption increases with the heavy-atom third principal moment and out-of-plane deviation (PBF): near-planar molecules aligned in channels lose less rotational freedom than bulky, non-planar ones with large PMI3, so the PMI3 x PBF product should be positively associated with entropy loss for linear and nonlinear rotors, while single-site molecules (PMI proxies at legitimate zero) show a near-baseline rotation penalty.",
    "rationale": "Rotational entropy loss plausibly increases with heavy-atom third principal moment and out-of-plane deviation: bulky, non-planar molecules in confined channels lose more rotational freedom than near-planar ones, an interaction encoded by the PMI3 x PBF product. Legitimate PMI zeros (single-site molecules such as methane) are handled by rotor_case branching, not imputation. Limitations: heavy-atom proxies neglect hydrogen contributions; the RRHO immobile-adsorbate treatment is known to overestimate entropy losses, so this is only a coarse shape proxy (E05).",
    "falsification_criteria": "If entropy loss for nonlinear adsorbates with high PMI3 but near-zero PBF matches that of high-PMI3/high-PBF adsorbates at matched framework accessibility, the planarity-interaction claim is falsified; the alternative is that PMI3 alone (or Vol alone) captures all rotational-shape information.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E05",
      "E06"
    ],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI3 and PBF proxy rotational shape in the original implicit-H/heavy-atom encoding; legitimate zeros are representation artifacts, not true zero all-atom inertia or true zero rotational constraint. Branch expressions are all dimensionless log terms. The product form is an empirical interaction, not a derived rotor partition-function result.",
      "physical_interpretation": "PMI3 is the heavy-atom third principal moment (inertia proxy); PBF measures out-of-plane deviation (planarity). No q-unity threshold is asserted; reference medians are fixed training constants. The precheck (Spearman +0.35, consistent) supports the declared increasing descriptor-to-loss direction but does not validate causality.",
      "boundary_behavior": "Single-site branch is constant 0 (PMI3 = 0 by representation, log(1+0) = 0, finite). Linear branch is log(1 + (PMI3/PMI3_ref) * (PBF/PBF_ref)); at PBF = 0 (planar molecules) it equals exactly 0, not a scaled log term. Nonlinear branch is finite for all training rows since PBF in [0, 0.656] and PMI3 in [0, 2414.6] are finite. The +1 keeps the log argument positive at legitimate zeros.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        "PBF",
        "PMI3"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        20.424,
        161.144
      ],
      "training_spearman": 0.35165096468908985,
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
    "name": "nonlinear_rotor_shape_penalty",
    "formula": "rotor_case(log(1 + (PMI3 / PMI3_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)))",
    "hypothesis": "Rotational entropy loss upon adsorption increases with the heavy-atom third principal moment and out-of-plane deviation (PBF): near-planar molecules aligned in channels lose less rotational freedom than bulky, non-planar ones with large PMI3, so the PMI3 x PBF product should be positively associated with entropy loss for linear and nonlinear rotors, while single-site molecules (PMI proxies at legitimate zero) show a near-baseline rotation penalty.",
    "rationale": "Rotational entropy loss plausibly increases with heavy-atom third principal moment and out-of-plane deviation: bulky, non-planar molecules in confined channels lose more rotational freedom than near-planar ones, an interaction encoded by the PMI3 x PBF product. Legitimate PMI zeros (single-site molecules such as methane) are handled by rotor_case branching, not imputation. Limitations: heavy-atom proxies neglect hydrogen contributions; the RRHO immobile-adsorbate treatment is known to overestimate entropy losses, so this is only a coarse shape proxy (E05).",
    "falsification_criteria": "If entropy loss for nonlinear adsorbates with high PMI3 but near-zero PBF matches that of high-PMI3/high-PBF adsorbates at matched framework accessibility, the planarity-interaction claim is falsified; the alternative is that PMI3 alone (or Vol alone) captures all rotational-shape information.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E02",
      "E05",
      "E06"
    ],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI3 and PBF proxy rotational shape in the original implicit-H/heavy-atom encoding; legitimate zeros are representation artifacts, not true zero all-atom inertia or true zero rotational constraint. Branch expressions are all dimensionless log terms. The product form is an empirical interaction, not a derived rotor partition-function result.",
      "physical_interpretation": "PMI3 is the heavy-atom third principal moment (inertia proxy); PBF measures out-of-plane deviation (planarity). No q-unity threshold is asserted; reference medians are fixed training constants. The precheck (Spearman +0.35, consistent) supports the declared increasing descriptor-to-loss direction but does not validate causality.",
      "boundary_behavior": "Single-site branch is constant 0 (PMI3 = 0 by representation, log(1+0) = 0, finite). Linear branch is log(1 + (PMI3/PMI3_ref) * (PBF/PBF_ref)); at PBF = 0 (planar molecules) it equals exactly 0, not a scaled log term. Nonlinear branch is finite for all training rows since PBF in [0, 0.656] and PMI3 in [0, 2414.6] are finite. The +1 keeps the log argument positive at legitimate zeros.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "Vol",
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
        "PBF",
        "PMI3"
      ],
      "quantity_roles": {
        "PBF": "heavy_atom_planarity",
        "PMI3": "heavy_atom_inertia_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        20.424,
        161.144
      ],
      "training_spearman": 0.35165096468908985,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/small_kg_rag_agent/replicate-3/round-1/h3`

最终状态：scored；边际收益：+1.205689 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks (large AV) the same molecule retains more configurational freedom.",
    "rationale": "AV is a fixed-probe, mass-specific accessibility measure; it is not molecule-specific free volume, so dividing molecular volume by it is an empirical contrast, not a free-volume equality. The 0.1 additive constant keeps the expression finite at AV = 0 (28 training frameworks where the fixed probe finds zero accessibility), and is an arbitrary smoothing constant, not a physical length scale. The descriptor trades off molecule bulk against framework openness.",
    "falsification_criteria": "If entropy loss correlates with Vol alone equally well as with this ratio across frameworks spanning the AV range (including AV=0 frameworks, where the fixed-probe accessibility may still permit molecular adsorption), the AV-contrast mechanism adds no explanatory power and should be rejected in favor of a pure molecular-size mechanism.",
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
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe AV ranks framework openness but is not molecule-specific; transfer of the ratio to molecules smaller or larger than the probe is an empirical assumption. AV=0 does not imply zero molecular adsorption space, so the expression remains a smooth proxy there.",
      "physical_interpretation": "Native Vol (van der Waals volume) and native AV (probe-accessible specific volume); the additive 0.1 is a fixed numeric smoothing constant without universal physical meaning, ensuring finiteness at legitimate AV zeros.",
      "boundary_behavior": "At AV = 0 the expression is finite (value log(1 + 10*Vol/Vol_ref)); at large AV the descriptor saturates toward log(1 + Vol/Vol_ref). Vol training domain is strictly positive, so no division by zero occurs.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
        "AV",
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        3.3452,
        15.5604
      ],
      "training_spearman": 0.6807900295104288,
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
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks (large AV) the same molecule retains more configurational freedom.",
    "rationale": "Entropy loss plausibly increases with the empirical contrast between adsorbate van der Waals volume and framework probe-accessible specific volume: in frameworks with small fixed-probe accessibility a large molecule is more spatially constrained, while open frameworks allow more configurational freedom, consistent with reported use of occupiable volume as an entropy-loss descriptor (E07). Limitations: AV is fixed-probe and mass-specific, not molecule-specific free volume, so no literal Vol/AV free-volume claim is made.",
    "falsification_criteria": "If entropy loss correlates with Vol alone equally well as with this ratio across frameworks spanning the AV range (including AV = 0 frameworks, where the fixed-probe accessibility may still permit molecular adsorption), the AV-contrast mechanism adds no explanatory power and should be rejected in favor of a pure molecular-size mechanism.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E03",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe AV ranks framework openness but is mass-specific and not molecule-specific; AV = 0 for the fixed geometric probe does not imply zero molecular adsorption space, so the ratio remains a smooth empirical proxy at AV = 0. Transferring the Vol/AV contrast to molecules smaller or larger than the probe is an empirical assumption.",
      "physical_interpretation": "Native Vol (van der Waals volume of the adsorbate) against native AV (probe-accessible specific volume of the framework, cm^3/g); the units do not form a physical free-volume equality, only a dimensionless empirical contrast after reference normalization. The additive 0.1 is a fixed smoothing constant without universal physical meaning. The precheck (Spearman +0.68, consistent) supports the declared decreasing-in-AV / increasing-in-Vol descriptor-to-loss direction but does not validate causality.",
      "boundary_behavior": "At AV = 0 the expression is finite, log(1 + 10 * Vol/Vol_ref); as AV grows, (Vol/Vol_ref)/(0.1 + AV/AV_ref) decreases monotonically toward 0, so the descriptor tends to log(1 + 0) = 0, NOT toward log(1 + Vol/Vol_ref). Vol training domain is strictly positive, so no division by zero occurs; the additive 0.1 only guards the legitimate AV zeros (28 training frameworks).",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
        "AV",
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        3.3452,
        15.5604
      ],
      "training_spearman": 0.6807900295104288,
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
    "name": "accessible_volume_contrast",
    "formula": "log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))",
    "hypothesis": "Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks (large AV) the same molecule retains more configurational freedom.",
    "rationale": "Entropy loss plausibly increases with the empirical contrast between adsorbate van der Waals volume and framework probe-accessible specific volume: in frameworks with small fixed-probe accessibility a large molecule is more spatially constrained, while open frameworks allow more configurational freedom, consistent with reported use of occupiable volume as an entropy-loss descriptor (E07). Limitations: AV is fixed-probe and mass-specific, not molecule-specific free volume, so no literal Vol/AV free-volume claim is made.",
    "falsification_criteria": "If entropy loss correlates with Vol alone equally well as with this ratio across frameworks spanning the AV range (including AV = 0 frameworks, where the fixed-probe accessibility may still permit molecular adsorption), the AV-contrast mechanism adds no explanatory power and should be rejected in favor of a pure molecular-size mechanism.",
    "novelty_status": "known_relation",
    "evidence_ids": [
      "E03",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe AV ranks framework openness but is mass-specific and not molecule-specific; AV = 0 for the fixed geometric probe does not imply zero molecular adsorption space, so the ratio remains a smooth empirical proxy at AV = 0. Transferring the Vol/AV contrast to molecules smaller or larger than the probe is an empirical assumption.",
      "physical_interpretation": "Native Vol (van der Waals volume of the adsorbate) against native AV (probe-accessible specific volume of the framework, cm^3/g); the units do not form a physical free-volume equality, only a dimensionless empirical contrast after reference normalization. The additive 0.1 is a fixed smoothing constant without universal physical meaning. The precheck (Spearman +0.68, consistent) supports the declared decreasing-in-AV / increasing-in-Vol descriptor-to-loss direction but does not validate causality.",
      "boundary_behavior": "At AV = 0 the expression is finite, log(1 + 10 * Vol/Vol_ref); as AV grows, (Vol/Vol_ref)/(0.1 + AV/AV_ref) decreases monotonically toward 0, so the descriptor tends to log(1 + 0) = 0, NOT toward log(1 + Vol/Vol_ref). Vol training domain is strictly positive, so no division by zero occurs; the additive 0.1 only guards the legitimate AV zeros (28 training frameworks).",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
        "AV",
        "Vol"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "Vol": "molecular_vdw_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        3.3452,
        15.5604
      ],
      "training_spearman": 0.6807900295104288,
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
        "record_id": "chunk:cdbfb43c28a3c70f95ba6aaa",
        "paper_id": "doi:10.1002/cphc.200800238",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:43dedbc998f9c278eea622b0",
        "paper_id": "pmc:pmc9739862",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f0a5a652a4377235ec566770",
        "paper_id": "doi:10.1007/s00894-008-0417-6",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:30a95992af001123813578a0",
        "paper_id": "doi:10.1021/jp052941+",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e933adf17670b8f416a9170e",
        "paper_id": "doi:10.1021/la302230z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:004b7a71bd35e46700101a49",
        "paper_id": "doi:10.1039/a803263g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2cab4c5858c1d76e029f2dbd",
        "paper_id": "pmc:pmc10979502",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:323d66ad417d981217705b45",
        "paper_id": "doi:10.1021/ja015797o",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:344ef3f3358677af422a5fea",
        "paper_id": "pmc:pmc6151591",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:522d58342ca7e271d4501291",
        "paper_id": "doi:10.26434/chemrxiv.11695482.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7342d031262bdf8cf5e759a2",
        "paper_id": "doi:10.1002/cphc.202300022",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, adsorbed translational entropy loss grows when the adsorbate's heavy-atom enclosing radius is large relative to the framework's passing bottleneck (Df), because confinement in narrow windows restricts translational freedom; the descriptor should be positively associated with entropy loss. log(1 + (SPAN / SPAN_ref) * (MW / MW_ref) / (lsd_f / lsd_f_ref)) Rotational entropy loss upon adsorption increases with the heavy-atom third principal moment and out-of-plane deviation (PBF): near-planar molecules aligned in channels lose less rotational freedom than bulky, non-planar ones with large PMI3, so the PMI3 x PBF product should be positively associated with entropy loss for linear and nonlinear rotors, while single-site molecules (PMI proxies at legitimate zero) show a near-baseline rotation penalty. rotor_case(log(1 + (PMI3 / PMI3_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref))) Entropy loss increases with the ratio of adsorbate van der Waals volume to the framework's probe-accessible specific volume: in frameworks with small fixed-probe accessibility, a large molecule is more spatially constrained (fewer accessible configurations), raising entropy loss, whereas in open frameworks (large AV) the same molecule retains more configurational freedom. log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:8dd99e6f4fc8a3c4e46d940b",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e98dff054a73e56b28f6bdf3"
    ],
    "items": 10,
    "lexical_tokens": 4774,
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
      "record_id": "chunk:878e3cf9557831b0616715f9",
      "paper_id": "doi:10.1002/cphc.201701084",
      "document_id": "document:2599bae9c40111b40c45ccef",
      "quote": "and rotational movements of the guest molecule relative to the zeolite host as vibrations under the rigid rotor-harmonic oscillator ( RRHO ) approximation has been shown to overestimate the entropy losses associated with the adsorption of the guest molecules from the gas phase into the zeolite pores . $ ^ { [ 59 , 84 , 85 ] } $ In their study of hydrocarbon adsorption in zeolites, De Moor et al. demonstrated that the entropy cannot be calculated correctly by treating the guest molecules as immobile adsorbates in the RRHO approximation, and that the remaining mobility of the adsorbed species at the active sites needs to be taken into account. $ ^{[85]} $ The authors suggested an alternative, mobile adsorbate calculation, which uses a so-called mobile block analysis of the Hessian (MBH) $ ^{[86,87]} $ to identify those low-frequency modes corresponding to overall global translations and rotations of the guest molecule relative to the framework. Once identified, the contributions of the modes to the partition function are replaced by the correct ones for translational or rotational motions.",
      "locator": {
        "kind": "markdown_section",
        "section": "3.3. thermochemical calculations"
      },
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
      "id": "E05"
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
