# high/rag_agent/replicate-2/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/rag_agent-replicate-2.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h1",
    "name": "bottleneck_volume_confinement",
    "formula": "log((q_Vol**(0.3333333333)) / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because tighter passage relative to molecular size reduces the accessible translational configuration space.",
    "rationale": "Translational confinement at infinite dilution is governed by the free volume actually reachable by a molecule of a given size; lsd_f (Zeo++ Df) is the largest free sphere that can pass through the periodic path, so a molecule whose cubic volume scale approaches the bottleneck experiences strong translational restriction. Literature reports that entropic loss correlates with gas-phase translational/rotational entropies and with framework occupiable volume (E07) and that tighter frameworks show larger entropy-loss fractions for linear alkanes (E04), consistent in direction with this descriptor. The descriptor is a dimensionless re-expression of two native inputs already present in the nonlinear ANN baseline; it adds interpretability, not new information. Limitations: Df is a geometric bottleneck proxy, not a global cavity diameter, and vdW volume is not the kinetic diameter seen by the framework; training association (Spearman ~0.63) is consistent but does not validate causality.",
    "falsification_criteria": "If entropy loss computed from published D0 values shows no monotone positive association with (Vol)^(1/3)/Df across the training domain, or if frameworks with equal Df but different pore connectivity (e.g., 1D channels vs 3D cages) show systematically different entropy loss at the same descriptor value, the confinement-ratio mechanism is falsified in favor of a connectivity or multi-site mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E07"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "(Vol)^(1/3) is a length-scale proxy for the molecule and lsd_f (Df) is the passing-bottleneck proxy only; neither is the true kinetic dimension nor the global cavity diameter Di, and Di is not available in D0. Cited comparisons (E02, E04) use average cavity/pore size, a different geometric quantity from Df; the transfer to a Df-based descriptor is a hypothesis. Source temperature, loading and framework chemistry are not fully resolved, and no source percentage or coefficient becomes a universal constant. Both proxies are transferable only within this rigid pure-silica, infinite-dilution regime.",
      "physical_interpretation": "Vol is the native vdW volume; lsd_f is the native passing free sphere (bottleneck), not the included-along-path Dif (lsd_p) and not a cavity diameter. q_Vol and q_lsd_f are dimensionless row-varying ratios to fixed positive training-reference medians; no q-unity threshold and no X/q_X construction is used.",
      "boundary_behavior": "Vol (min 20.424) and lsd_f (min 0.85684) are strictly positive over the full training domain, so log((q_Vol**(1/3))/q_lsd_f) is finite for every row with no imputation or epsilon; the monotone claim is declared only over the observed training range, and the fixed reference constants Vol_ref^(1/3)/lsd_f_ref carry no universal physical meaning (they rescale the physical ratio Vol**(1/3)/Df by a constant).",
      "vary_input": "Vol",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
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

候选标识：`high/rag_agent/replicate-2/round-2/h1`

最终状态：scored；边际收益：+0.513107 pp；保留：False。

复核改动字段：

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_volume_confinement",
    "formula": "log((q_Vol**(0.3333333333)) / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because tighter passage relative to molecular size reduces the accessible translational configuration space. Equivalently, s_ads/s_gas decreases as this descriptor increases.",
    "rationale": "Retained from round 1 with a positive marginal improvement (training Spearman ~0.63 against the entropy-loss target). The descriptor contrasts a heavy-atom-representation size proxy (Vol) with the Zeo++ Df bottleneck (lsd_f), both positive over the full training domain, so every row yields a finite value. Limitation: Vol is an all-atom vdW volume while lsd_f derives from a fixed geometric sphere analysis; the ratio is an empirical confinement proxy, not a rigorous free-volume identity. Global cavity Di is not represented by lsd_f.",
    "falsification_criteria": "If, within fixed lsd_f strata, entropy loss is flat or decreasing in Vol (or if frameworks with equal Vol/lsd_f ratios but different lsd_p show systematically different entropy losses dominating the trend), the bottleneck-confinement mechanism is falsified in favor of a cage-localization or wall-interaction mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol^(1/3) is a monotone size proxy; lsd_f is a bottleneck, not a cavity-diameter, proxy. q-normalization by fixed training-reference medians carries no physical unity threshold; predictions are association-level only.",
      "physical_interpretation": "Native meanings: molecular vdW volume (angstrom^3) and largest passing free sphere (angstrom). Increasing descriptor means larger molecule relative to passage; entropy loss (-delta_s/R) increases and s_ads/s_gas correspondingly decreases. No claim that q_Vol^(1/3) = q_lsd_f is a physical equality boundary.",
      "boundary_behavior": "Both Vol (min 20.424) and lsd_f (min 0.85684) are strictly positive across all 2361 training rows, so the descriptor is finite everywhere with no zero-division or log-of-nonnegative issues; no epsilon or imputation is used.",
      "vary_input": "Vol",
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
    "reason": "Redundant with a current input"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_volume_confinement",
    "formula": "log((q_Vol**(0.3333333333)) / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because tighter passage relative to molecular size reduces the accessible translational configuration space. Equivalently, s_ads/s_gas decreases as this descriptor increases.",
    "rationale": "Retained from round 1 with a positive marginal improvement (training Spearman ~0.63 against the entropy-loss target). The descriptor contrasts a heavy-atom-representation size proxy (Vol) with the Zeo++ Df bottleneck (lsd_f), both positive over the full training domain, so every row yields a finite value. Limitation: Vol is an all-atom vdW volume while lsd_f derives from a fixed geometric sphere analysis; the ratio is an empirical confinement proxy, not a rigorous free-volume identity. Global cavity Di is not represented by lsd_f.",
    "falsification_criteria": "If, within fixed lsd_f strata, entropy loss is flat or decreasing in Vol (or if frameworks with equal Vol/lsd_f ratios but different lsd_p show systematically different entropy losses dominating the trend), the bottleneck-confinement mechanism is falsified in favor of a cage-localization or wall-interaction mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol^(1/3) is a monotone size proxy; lsd_f is a bottleneck, not a cavity-diameter, proxy. q-normalization by fixed training-reference medians carries no physical unity threshold; predictions are association-level only.",
      "physical_interpretation": "Native meanings: molecular vdW volume (angstrom^3) and largest passing free sphere (angstrom). Increasing descriptor means larger molecule relative to passage; entropy loss (-delta_s/R) increases and s_ads/s_gas correspondingly decreases. No claim that q_Vol^(1/3) = q_lsd_f is a physical equality boundary.",
      "boundary_behavior": "Both Vol (min 20.424) and lsd_f (min 0.85684) are strictly positive across all 2361 training rows, so the descriptor is finite everywhere with no zero-division or log-of-nonnegative issues; no epsilon or imputation is used.",
      "vary_input": "Vol",
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
    "reason": "Redundant with a current input"
  }
}
```

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_volume_confinement",
    "formula": "(Vol**(0.3333333333))/lsd_f",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because tighter passage relative to molecular size reduces the accessible translational configuration space. Equivalently, s_ads/s_gas decreases as this descriptor increases.",
    "rationale": "Retained from round 1 with a positive marginal improvement (training Spearman ~0.63 against the entropy-loss target). The descriptor contrasts a heavy-atom-representation size proxy (Vol) with the Zeo++ Df bottleneck (lsd_f), both positive over the full training domain, so every row yields a finite value. Limitation: Vol is an all-atom vdW volume while lsd_f derives from a fixed geometric sphere analysis; the ratio is an empirical confinement proxy, not a rigorous free-volume identity. Global cavity Di is not represented by lsd_f.",
    "falsification_criteria": "If, within fixed lsd_f strata, entropy loss is flat or decreasing in Vol (or if frameworks with equal Vol/lsd_f ratios but different lsd_p show systematically different entropy losses dominating the trend), the bottleneck-confinement mechanism is falsified in favor of a cage-localization or wall-interaction mechanism.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Vol^(1/3) is a monotone size proxy; lsd_f is a bottleneck, not a cavity-diameter, proxy. q-normalization by fixed training-reference medians carries no physical unity threshold; predictions are association-level only.",
      "physical_interpretation": "Native meanings: molecular vdW volume (angstrom^3) and largest passing free sphere (angstrom). Increasing descriptor means larger molecule relative to passage; entropy loss (-delta_s/R) increases and s_ads/s_gas correspondingly decreases. No claim that q_Vol^(1/3) = q_lsd_f is a physical equality boundary.",
      "boundary_behavior": "Vol is strictly positive on all 2361 training rows (min 20.424 angstrom^3, zero_n = 0) and lsd_f is strictly positive on all rows (min 0.85684 angstrom), so Vol**(1/3)/lsd_f is finite and strictly positive on every training row. Units are compatible: Vol**(1/3) carries angstrom (from angstrom^3), lsd_f carries angstrom, so the ratio is dimensionless with no unit-incompatible operations. The rejection reason 'redundant with a current input' is repaired by removing the outer log: the previous expression log(q_Vol**(1/3)/q_lsd_f) was a fixed linear combination of log(Vol) and log(lsd_f), hence redundant with log-linear representations of the current inputs; the direct ratio is a genuinely nonlinear size-to-bottleneck confinement contrast that is not decomposable into per-input log terms. No division by a legitimate zero, no log of a nonpositive argument, no epsilon and no imputation; every training row yields a finite value. The descriptor remains an empirical confinement proxy (Vol is an all-atom vdW volume while lsd_f derives from a fixed geometric sphere analysis and is a bottleneck, not a global cavity diameter), and q-normalization constants are absorbed as a fixed scale with no physical unity threshold.",
      "vary_input": "Vol",
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
      "output_dimensions": {
        "length": "-1/10000000000"
      },
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
      "training_spearman": 0.6285950097652175,
      "target_association": "contradicted",
      "perturbation": 0.7023999999999999,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/rag_agent/replicate-2/round-2/h2`

最终状态：scored；边际收益：+4.897936 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "cage_window_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, a cavity-scale proxy) and the bottleneck diameter (lsd_f), because cage-like frameworks with large interior free volume behind narrow windows localize the adsorbate in discrete cavities and reduce accessible translational configurations relative to quasi-continuous channels; equivalently s_ads/s_gas decreases with the contrast.",
    "rationale": "Uses two framework path descriptors that are jointly available and co-measured by the same sphere analysis, isolating topology (cage vs channel) rather than absolute size. By construction the included sphere along the free path is at least the passing free sphere, so lsd_p/lsd_f >= 1 per row and the logarithm is finite for all rows. Limitations: lsd_p is neither the global cavity diameter Di nor a direct measure of cage volume; both descriptors derive from a fixed geometric probe and carry no energetic information.",
    "falsification_criteria": "If entropy loss instead decreases with lsd_p/lsd_f (e.g., if smooth wide channels restrict configurations more than cages) or if the association vanishes once lsd_f (h1's confinement term) is held fixed, the cage-localization hypothesis is falsified and confinement should be attributed to window size alone.",
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
      "proxy_assumptions": "lsd_p is used only as a path-local included-diameter proxy, explicitly not as global Di; lsd_f is used only as a bottleneck proxy. The ratio contrast is an empirical topology proxy; no claim that the q-normalized ratio equals 1 at any physical transition.",
      "physical_interpretation": "Native meanings: Dif (angstrom) along the free-sphere path versus Df (angstrom) bottleneck. Increasing descriptor means stronger cage-over-window contrast; entropy loss (-delta_s/R) is hypothesized to increase, hence s_ads/s_gas decreases. Association-level claim only; correlation does not establish causality.",
      "boundary_behavior": "Both lsd_p (min 3.3452) and lsd_f (min 0.85684) are strictly positive in training, and lsd_p >= lsd_f row-wise, so the descriptor is finite and nonnegative for all 2361 rows; a contrast near 0 (channel-like framework) maps to descriptor near 0 without singularity.",
      "vary_input": "lsd_p",
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
        0.85684,
        7.68726
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
    "slot_id": "h2",
    "name": "cage_window_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, a cavity-scale proxy) and the bottleneck diameter (lsd_f), because cage-like frameworks with large interior free volume behind narrow windows localize the adsorbate in discrete cavities and reduce accessible translational configurations relative to quasi-continuous channels; equivalently s_ads/s_gas decreases with the contrast.",
    "rationale": "Uses two framework path descriptors from the same Zeo++ sphere analysis to isolate a topology contrast (included-along-path scale versus passing bottleneck) rather than absolute pore size. Correction to the round-1 rationale: the round-2 training-only precheck returns Spearman ~ -0.02 and target_association 'inconclusive', so no strong topology signal is claimed; the slot is retained as a falsifiable connectivity probe, not a validated mechanism. lsd_p is neither the global cavity diameter Di nor a cage-volume measure, and both descriptors derive from a fixed geometric probe with no energetic content.",
    "falsification_criteria": "The training precheck already shows an inconclusive association (Spearman ~ -0.02); if this persists, or if entropy loss decreases with lsd_p/lsd_f within lsd_f strata, or the contrast carries no signal once lsd_f (h1's confinement term) is held fixed, the cage-localization reading is falsified and confinement should be attributed to window size alone.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
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
      "proxy_assumptions": "lsd_p is used only as a path-local included-diameter proxy, explicitly not as global Di; lsd_f is used only as a bottleneck proxy. The contrast is an empirical topology proxy; q-normalization constants cancel in the ratio and carry no physical threshold at 1. Honest limitation: the training association is inconclusive (Spearman ~ -0.02), so this descriptor currently carries no demonstrated entropy-loss signal and may contribute noise; it is kept only as a predeclared test of the cage-versus-channel contrast.",
      "physical_interpretation": "Native meanings: Dif (angstrom), the largest included sphere along the free-sphere path, versus Df (angstrom), the passing bottleneck. The predeclared association direction is unchanged: if the contrast were operative, larger contrast (cage-like localization behind narrow windows) would increase entropy loss (-delta_s/R) and decrease s_ads/s_gas. This is an association-level hypothesis; the training precheck neither validates mechanism nor causality and is currently inconclusive.",
      "boundary_behavior": "Both lsd_p (min 3.3452 angstrom) and lsd_f (min 0.85684 angstrom) are strictly positive across all 2361 training rows and lsd_p >= lsd_f row-wise by construction, so the descriptor is finite and nonnegative everywhere; a channel-like contrast near 0 maps to a descriptor near the constant offset log(lsd_f_ref/lsd_p_ref) without singularity. No epsilon, no imputation.",
      "vary_input": "lsd_p",
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
        0.85684,
        7.68726
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
    "slot_id": "h2",
    "name": "cage_window_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, a cavity-scale proxy) and the bottleneck diameter (lsd_f), because cage-like frameworks with large interior free volume behind narrow windows localize the adsorbate in discrete cavities and reduce accessible translational configurations relative to quasi-continuous channels; equivalently s_ads/s_gas decreases with the contrast.",
    "rationale": "Uses two framework path descriptors from the same Zeo++ sphere analysis to isolate a topology contrast (included-along-path scale versus passing bottleneck) rather than absolute pore size. Correction to the round-1 rationale: the round-2 training-only precheck returns Spearman ~ -0.02 and target_association 'inconclusive', so no strong topology signal is claimed; the slot is retained as a falsifiable connectivity probe, not a validated mechanism. lsd_p is neither the global cavity diameter Di nor a cage-volume measure, and both descriptors derive from a fixed geometric probe with no energetic content.",
    "falsification_criteria": "The training precheck already shows an inconclusive association (Spearman ~ -0.02); if this persists, or if entropy loss decreases with lsd_p/lsd_f within lsd_f strata, or the contrast carries no signal once lsd_f (h1's confinement term) is held fixed, the cage-localization reading is falsified and confinement should be attributed to window size alone.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
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
      "proxy_assumptions": "lsd_p is used only as a path-local included-diameter proxy, explicitly not as global Di; lsd_f is used only as a bottleneck proxy. The contrast is an empirical topology proxy; q-normalization constants cancel in the ratio and carry no physical threshold at 1. Honest limitation: the training association is inconclusive (Spearman ~ -0.02), so this descriptor currently carries no demonstrated entropy-loss signal and may contribute noise; it is kept only as a predeclared test of the cage-versus-channel contrast.",
      "physical_interpretation": "Native meanings: Dif (angstrom), the largest included sphere along the free-sphere path, versus Df (angstrom), the passing bottleneck. The predeclared association direction is unchanged: if the contrast were operative, larger contrast (cage-like localization behind narrow windows) would increase entropy loss (-delta_s/R) and decrease s_ads/s_gas. This is an association-level hypothesis; the training precheck neither validates mechanism nor causality and is currently inconclusive.",
      "boundary_behavior": "Both lsd_p (min 3.3452 angstrom) and lsd_f (min 0.85684 angstrom) are strictly positive across all 2361 training rows and lsd_p >= lsd_f row-wise by construction, so the descriptor is finite and nonnegative everywhere; a channel-like contrast near 0 maps to a descriptor near the constant offset log(lsd_f_ref/lsd_p_ref) without singularity. No epsilon, no imputation.",
      "vary_input": "lsd_p",
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
        0.85684,
        7.68726
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

## h3

候选标识：`high/rag_agent/replicate-2/round-2/h3`

最终状态：scored；边际收益：-0.374322 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.Vol

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "planarity_orientation_restriction",
    "formula": "log(1.0 + q_PBF)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the adsorbate's out-of-plane thickness (PBF), because molecules deviating from planarity possess orientation-dependent minimal cross-sections that restrict the rotational and passage configurations compatible with pore windows and walls; equivalently s_ads/s_gas decreases with PBF at comparable size.",
    "rationale": "Tests a shape-family mechanism complementary to h1 (size) and h2 (topology): molecular flatness versus thickness. PBF is a heavy-atom, implicit-H proxy with legitimate exact zeros for planar molecules (587 training rows); log(1 + q_PBF) maps zero to exactly 0 without any epsilon or imputation, keeping every row finite. The derivative d/dPBF log(1 + PBF/PBF_ref) = 1/(PBF_ref + PBF) > 0 is predeclared positive. Limitations: PBF does not capture all-atom geometry, hydrogen positions, or conformational flexibility; the +1 offset is an empirical smoothing choice ensuring finiteness at legitimate zeros and carries no universal physical meaning.",
    "falsification_criteria": "If entropy loss decreases with PBF (i.e., planar adsorbates lose more entropy because they must adopt face-on wall-parallel orientations, losing out-of-plane rotation) or if the association vanishes after conditioning on Vol, the thickness-restriction hypothesis is falsified in favor of a flat-alignment penalty mechanism.",
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
      "proxy_assumptions": "PBF (angstrom) is a heavy-atom planarity proxy from the original implicit-H representation, not full all-atom molecular geometry; legitimate zeros denote planar heavy-atom skeletons, not absent molecules. The log(1+x) form is an empirical monotone smoothing; q_PBF = 1 has no physical significance.",
      "physical_interpretation": "Native meaning: mean atom distance from the best-fit molecular plane (angstrom). Increasing PBF means a more three-dimensional (thicker) molecule; the predeclared association is that entropy loss (-delta_s/R) increases, so s_ads/s_gas decreases. This is a hypothesis about association direction, not a validated causal statement.",
      "boundary_behavior": "At PBF = 0 (587 training rows with legitimate planar zeros) the descriptor equals exactly log(1) = 0, finite and smooth; for the maximum PBF of 0.65625 the descriptor remains small and finite. No division, no epsilon, no imputation is involved.",
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

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "planarity_orientation_restriction",
    "formula": "log(1.0 + q_PBF/(q_Vol**(0.3333333333)))",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the adsorbate's out-of-plane thickness (PBF), because molecules deviating from planarity possess orientation-dependent minimal cross-sections that restrict the rotational and passage configurations compatible with pore windows and walls; equivalently s_ads/s_gas decreases with PBF at comparable size.",
    "rationale": "Mapping correction: the stored hypothesis concerns orientation restriction from out-of-plane thickness 'at comparable size', but the previous formula used absolute PBF, which confounds molecular shape with molecular size (larger molecules are both thicker and, via h1's size channel, differently entropically penalized). The corrected descriptor normalizes thickness by the cube root of the vdW volume, a strictly positive size scale, yielding a dimensionless aspect-shape proxy that is finite at all legitimate PBF zeros (including single-site molecules, where it equals 0). The predeclared derivative d/dPBF log(1 + PBF/(PBF_ref * Vol_ref^(1/3) * q_Vol^(1/3))) is positive. Limitations: both inputs are empirical heavy-atom/implicit-H proxies; the log(1+x) offset is smoothing, not physics; and the raw absolute-PBF association was contradicted in the round-2 precheck, so this corrected form is an untested hypothesis, not a validated mechanism.",
    "falsification_criteria": "If entropy loss decreases with the size-conditioned thickness ratio, or if planar adsorbates lose more entropy than comparably sized thick ones after conditioning on Vol (face-on wall-parallel orientation penalty removing out-of-plane rotation), the thickness-restriction reading is falsified in favor of the flat-alignment mechanism; a null result after Vol conditioning would also falsify the shape channel.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E07"
    ],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF (angstrom) is a heavy-atom, implicit-H planarity proxy from the original representation, not full all-atom geometry; legitimate zeros denote planar heavy-atom skeletons, not absent molecules. Vol**(1/3) is an empirical molecular size scale. The ratio operationalizes the hypothesis clause 'at comparable size': it measures out-of-plane thickness relative to molecular size instead of absolute thickness, which confounded shape with size in the raw descriptor. log(1+x) is an empirical monotone smoothing for the legitimate zeros; no ratio value has universal physical meaning. Honest limitation: the round-2 precheck flagged the raw absolute-PBF descriptor's training association as contradicted; the size-conditioned form is a corrected operationalization whose association must be re-tested and is not validated.",
      "physical_interpretation": "Native meanings: mean heavy-atom distance from the best-fit molecular plane (angstrom) and van der Waals volume (angstrom^3). Increasing thickness at comparable molecular size means a more three-dimensional molecule; the predeclared association remains that entropy loss (-delta_s/R) increases, so s_ads/s_gas decreases. Association-level hypothesis only; no causality claim, and the competing flat-alignment mechanism remains live.",
      "boundary_behavior": "q_PBF >= 0 with legitimate exact zeros (587 training rows, including the 54 single-site rows), and q_Vol**(1/3) > 0 on every row (Vol min 20.424 angstrom^3, zero_n = 0), so the ratio is finite and nonnegative everywhere; at PBF = 0 the descriptor is exactly log(1) = 0. No division by a legitimate zero, no epsilon, no imputation; every training row yields a finite value.",
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
        "PBF",
        "Vol"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.2767107320017334,
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
    "slot_id": "h3",
    "name": "planarity_orientation_restriction",
    "formula": "log(1.0 + q_PBF/(q_Vol**(0.3333333333)))",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the adsorbate's out-of-plane thickness (PBF), because molecules deviating from planarity possess orientation-dependent minimal cross-sections that restrict the rotational and passage configurations compatible with pore windows and walls; equivalently s_ads/s_gas decreases with PBF at comparable size.",
    "rationale": "Mapping correction: the stored hypothesis concerns orientation restriction from out-of-plane thickness 'at comparable size', but the previous formula used absolute PBF, which confounds molecular shape with molecular size (larger molecules are both thicker and, via h1's size channel, differently entropically penalized). The corrected descriptor normalizes thickness by the cube root of the vdW volume, a strictly positive size scale, yielding a dimensionless aspect-shape proxy that is finite at all legitimate PBF zeros (including single-site molecules, where it equals 0). The predeclared derivative d/dPBF log(1 + PBF/(PBF_ref * Vol_ref^(1/3) * q_Vol^(1/3))) is positive. Limitations: both inputs are empirical heavy-atom/implicit-H proxies; the log(1+x) offset is smoothing, not physics; and the raw absolute-PBF association was contradicted in the round-2 precheck, so this corrected form is an untested hypothesis, not a validated mechanism.",
    "falsification_criteria": "If entropy loss decreases with the size-conditioned thickness ratio, or if planar adsorbates lose more entropy than comparably sized thick ones after conditioning on Vol (face-on wall-parallel orientation penalty removing out-of-plane rotation), the thickness-restriction reading is falsified in favor of the flat-alignment mechanism; a null result after Vol conditioning would also falsify the shape channel.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E07"
    ],
    "variable_mappings": {
      "PBF": "heavy_atom_planarity",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF (angstrom) is a heavy-atom, implicit-H planarity proxy from the original representation, not full all-atom geometry; legitimate zeros denote planar heavy-atom skeletons, not absent molecules. Vol**(1/3) is an empirical molecular size scale. The ratio operationalizes the hypothesis clause 'at comparable size': it measures out-of-plane thickness relative to molecular size instead of absolute thickness, which confounded shape with size in the raw descriptor. log(1+x) is an empirical monotone smoothing for the legitimate zeros; no ratio value has universal physical meaning. Honest limitation: the round-2 precheck flagged the raw absolute-PBF descriptor's training association as contradicted; the size-conditioned form is a corrected operationalization whose association must be re-tested and is not validated.",
      "physical_interpretation": "Native meanings: mean heavy-atom distance from the best-fit molecular plane (angstrom) and van der Waals volume (angstrom^3). Increasing thickness at comparable molecular size means a more three-dimensional molecule; the predeclared association remains that entropy loss (-delta_s/R) increases, so s_ads/s_gas decreases. Association-level hypothesis only; no causality claim, and the competing flat-alignment mechanism remains live.",
      "boundary_behavior": "q_PBF >= 0 with legitimate exact zeros (587 training rows, including the 54 single-site rows), and q_Vol**(1/3) > 0 on every row (Vol min 20.424 angstrom^3, zero_n = 0), so the ratio is finite and nonnegative everywhere; at PBF = 0 the descriptor is exactly log(1) = 0. No division by a legitimate zero, no epsilon, no imputation; every training row yields a finite value.",
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
        "PBF",
        "Vol"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.2767107320017334,
      "target_association": "contradicted",
      "perturbation": 0.0046290119000000005,
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
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b86d2d3284fbbe6696210c35",
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
        "record_id": "chunk:9a3907e626bcdef0bc5bb0cb",
        "paper_id": "doi:10.1002/chem.201705627",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a716c0f2d08195e0bc57308d",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd75db1400cf2ce6171ef0f6",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d551cda661adcb5ac3f29200",
        "paper_id": "doi:10.1038/s41586-021-03429-y",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ab78d7d59314be481dfe59a6",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6918f943bdf0f8fa691559fc",
        "paper_id": "doi:10.1038/nature04097",
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
        "record_id": "chunk:ae627ac039efcb7fe83c7653",
        "paper_id": "pmc:pmc11228971",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1487a816fb99c8a313aa68d6",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:3f5768387a8e2dd4104cc2f6",
        "paper_id": "doi:10.1039/c3cc40731d",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:45c6c30e39c58cf298acb495",
        "paper_id": "pmc:pmc8113345",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because tighter passage relative to molecular size reduces the accessible translational configuration space. Equivalently, s_ads/s_gas decreases as this descriptor increases. log((q_Vol**(0.3333333333)) / q_lsd_f) For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, a cavity-scale proxy) and the bottleneck diameter (lsd_f), because cage-like frameworks with large interior free volume behind narrow windows localize the adsorbate in discrete cavities and reduce accessible translational configurations relative to quasi-continuous channels; equivalently s_ads/s_gas decreases with the contrast. log(q_lsd_p / q_lsd_f) For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the adsorbate's out-of-plane thickness (PBF), because molecules deviating from planarity possess orientation-dependent minimal cross-sections that restrict the rotational and passage configurations compatible with pore windows and walls; equivalently s_ads/s_gas decreases with PBF at comparable size. log(1.0 + q_PBF)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:8dd99e6f4fc8a3c4e46d940b",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:ae6e434cc894357276cba23f"
    ],
    "items": 10,
    "lexical_tokens": 4643,
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
      "record_id": "chunk:8dd99e6f4fc8a3c4e46d940b",
      "paper_id": "doi:10.1021/acs.jpcc.0c02671",
      "document_id": "document:679638c993b24ed3004656c6",
      "quote": "infty } $ with $ s _ { gas } ^ { 0 } $ is , of course , a highly simplified model of the adsorbed-phase entropy and includes minimal physical insight or intuition . As shown in the next section , one can introduce physically intuitive arguments into more complicated models of entropy than that presented above . 4.3. Empirical Model of Entropy Based on Adsorbent Identity. While the linear entropy scaling in Figures 1 and 3 is quite successful for the TraPPE-based adsorption systems, it is ultimately an oversimplified correlation. We seek a physics-based structure—topology—entropy relationship that is generic and applicable across molecule classes and zeolites. As a first step to this end, motivated by the arguments in refs 13 and 27, we considered a simple linear model wherein each contributor to the entropy is affected differently. However, it has been argued that the translational contribution to the adsorbate entropy (for alkanes) is relatively uniform across frameworks, with the emphasis being on the disparate rotational contributions. $ ^{13,58} $ For example, Denayer et al. have demonstrated that the driving force behind the zeolitic separation of alkane/isoalkane mixtures is exclusively the difference in rotational loss, represented by a ratio between the molecule's radius of gyration with the cavity's largest inscribed van der Waals radius. $ ^{58} $ Therefore, we consider a model where $ s_{ads}^{\\infty} $ is composed of (1) two-third translational entropy (equivalent to the loss of one-third of the gas-phase translational entropy) and (2) a fraction of the gas-phase rotational entropy. As mentioned previously, the vibrational entropy is assumed to be unaffected by adsorption or confinement. We propose the simplest model consistent with the proposition that the adsorbed-phase entropy is composed of the translational and rotational entropies and all of the vibrational entropy of the gas state. Mathematically, this may be stated as $$ s_{\\mathrm{a d s}}^{\\quad\\infty}=\\alpha s_{\\mathrm{t r a n s}}^{0}+\\beta s_{\\mathrm{r o t}}^{0}+s_{\\mathrm{v i b}}^{0} $$ $$ where\\quad\\alpha=2/3\\quad and\\quad0<\\beta<1 $$",
      "locator": {
        "section": "4. results and discussion",
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
