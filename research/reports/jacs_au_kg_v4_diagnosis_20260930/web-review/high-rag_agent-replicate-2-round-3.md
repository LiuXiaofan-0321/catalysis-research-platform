# high/rag_agent/replicate-2/round-3

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
  },
  {
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
  }
]
```

## h1

候选标识：`high/rag_agent/replicate-2/round-3/h1`

最终状态：scored；边际收益：-2.939167 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "bottleneck_volume_confinement",
    "formula": "log((q_Vol**(0.3333333333)) / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because a tighter passage relative to molecular size reduces the accessible translational configuration space of the confined molecule.",
    "rationale": "Volume and bottleneck diameter are native geometric scales; the q-normalization only fixes dimensionless row-varying inputs against fixed training-reference medians (q_Vol = Vol/Vol_ref, q_lsd_f = lsd_f/lsd_f_ref), so no q-unity physical threshold is asserted. The cubic root converts volume to a length scale compatible with lsd_f for the log argument. This descriptor was retained in rounds 1-2 with a consistent positive training association with entropy loss (Spearman ~0.63), but the round-2 native-scale variant scored as contradicted, so the monotonic claim remains an empirical proxy relation, not a validated mechanism; numerical correlations do not establish causality.",
    "falsification_criteria": "If, within fixed framework bottleneck (lsd_f fixed), larger-Vol adsorbates systematically show lower entropy loss than smaller ones in held-out pure-silica frameworks, or if the association flips sign when lsd_f is varied at fixed Vol, the confinement-by-bottleneck hypothesis is falsified for this regime.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Van der Waals volume cubed-root is a spherical-equivalent molecular length; Zeo++ Df (lsd_f) is a hard-sphere passing bottleneck along a periodic free path, not the global cavity diameter Di, and not a molecule-specific window. The proxy ignores framework flexibility, adsorbate-framework energetic heterogeneity, and all-atom shape.",
      "physical_interpretation": "Native meaning: ratio of molecular size scale to the largest free passing sphere; larger ratio means tighter confinement at the narrowest passage. q_X are dimensionless row-varying ratios to fixed positive training medians; X_ref itself is constant for positive X and never used as a denominator.",
      "boundary_behavior": "Vol and lsd_f have zero training zeros and strictly positive native ranges (Vol: 20.424-161.144; lsd_f: 0.85684-7.68726), so log arguments are strictly positive and finite on every training row; no epsilon is added and no imputation is used.",
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
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because a tighter passage relative to molecular size reduces the accessible translational configuration space of the confined molecule.",
    "rationale": "Volume and bottleneck diameter are native geometric scales; q_Vol and q_lsd_f are dimensionless row-varying ratios to fixed positive training-reference medians, so no q-unity physical threshold is asserted. The 1/3 exponent converts van der Waals volume to a length scale compatible with lsd_f inside the dimensionless log argument. Round-1 scored this q-log form as retained with a positive training association (Spearman ~0.63), while the round-2 native-scale variant (Vol**(1/3)/lsd_f) was scored contradicted and not retained; therefore only the q-log form is kept. Source E04 reports larger fractional gas-phase entropy loss for linear alkanes in medium-pore MFI than in larger-pore FAU, motivating a smaller-pore/larger-loss association, but E02/E04 refer to cavity-scale diameters, not the Zeo++ passing bottleneck Df, and source-specific percentages must not become universal constants; the mapping to lsd_f is a proxy transfer and the monotone claim remains an empirical proxy relation, not a validated mechanism. The training-only precheck flagged this descriptor as redundant with a current input, further limiting any claim of independent mechanistic content. Numerical correlations do not establish causality.",
    "falsification_criteria": "If, within fixed framework bottleneck (lsd_f fixed), larger-Vol adsorbates systematically show lower entropy loss than smaller ones in held-out pure-silica frameworks, or if the association flips sign when lsd_f is varied at fixed Vol, the confinement-by-bottleneck hypothesis is falsified for this regime.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Van der Waals volume cubed-root is a spherical-equivalent molecular length; Zeo++ Df (lsd_f) is a hard-sphere passing bottleneck along a periodic free path, not the global cavity diameter Di, and not a molecule-specific window. The proxy ignores framework flexibility, adsorbate-framework energetic heterogeneity, and all-atom shape.",
      "physical_interpretation": "Native meaning: ratio of molecular size scale to the largest free passing sphere; larger ratio means tighter confinement at the narrowest passage. q_X are dimensionless row-varying ratios to fixed positive training medians; X_ref itself is constant for positive X and never used as a denominator.",
      "boundary_behavior": "Vol and lsd_f have zero training zeros and strictly positive native ranges (Vol: 20.424-161.144; lsd_f: 0.85684-7.68726), so log arguments are strictly positive and finite on every training row; no epsilon is added and no imputation is used.",
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
    "formula": "(q_Vol**(0.3333333333)) / q_lsd_f",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because a tighter passage relative to molecular size reduces the accessible translational configuration space of the confined molecule.",
    "rationale": "Volume and bottleneck diameter are native geometric scales; q_Vol and q_lsd_f are dimensionless row-varying ratios to fixed positive training-reference medians, so no q-unity physical threshold is asserted. The 1/3 exponent converts van der Waals volume to a length scale compatible with lsd_f inside the dimensionless log argument. Round-1 scored this q-log form as retained with a positive training association (Spearman ~0.63), while the round-2 native-scale variant (Vol**(1/3)/lsd_f) was scored contradicted and not retained; therefore only the q-log form is kept. Source E04 reports larger fractional gas-phase entropy loss for linear alkanes in medium-pore MFI than in larger-pore FAU, motivating a smaller-pore/larger-loss association, but E02/E04 refer to cavity-scale diameters, not the Zeo++ passing bottleneck Df, and source-specific percentages must not become universal constants; the mapping to lsd_f is a proxy transfer and the monotone claim remains an empirical proxy relation, not a validated mechanism. The training-only precheck flagged this descriptor as redundant with a current input, further limiting any claim of independent mechanistic content. Numerical correlations do not establish causality.",
    "falsification_criteria": "If, within fixed framework bottleneck (lsd_f fixed), larger-Vol adsorbates systematically show lower entropy loss than smaller ones in held-out pure-silica frameworks, or if the association flips sign when lsd_f is varied at fixed Vol, the confinement-by-bottleneck hypothesis is falsified for this regime.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Van der Waals volume cubed-root is a spherical-equivalent molecular length; Zeo++ Df (lsd_f) is a hard-sphere passing bottleneck along a periodic free path, not the global cavity diameter Di, and not a molecule-specific window. The proxy ignores framework flexibility, adsorbate-framework energetic heterogeneity, and all-atom shape.",
      "physical_interpretation": "Native meaning: ratio of molecular size scale to the largest free passing sphere; larger ratio means tighter confinement at the narrowest passage. q_X are dimensionless row-varying ratios to fixed positive training medians; X_ref itself is constant for positive X and never used as a denominator.",
      "boundary_behavior": "Vol and lsd_f have zero training zeros and strictly positive native ranges (Vol: 20.424-161.144; lsd_f: 0.85684-7.68726), so the ratio is strictly positive and finite on every training row without epsilon or imputation. The fixed exponent 1/3 converts the van der Waals volume to a spherical-equivalent length scale compatible with lsd_f, and the ratio is dimensionless, taking values below or above 1 with no q-unity physical threshold asserted. Replacing the previous log-of-ratio with the raw ratio removes the exact log-linear decomposition into existing inputs ((1/3)*log(q_Vol) - log(q_lsd_f)) that caused the redundancy rejection; the confinement proxy claim itself is unchanged and remains an empirical relation, not a validated mechanism.",
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

候选标识：`high/rag_agent/replicate-2/round-3/h2`

最终状态：scored；边际收益：-4.698935 pp；保留：False。

复核改动字段：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "cage_window_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, a cavity-scale proxy) and the bottleneck diameter (lsd_f), because cage-like frameworks with large interior free space behind narrow windows localize the adsorbate in discrete cavities and reduce accessible translational configurations relative to quasi-continuous channels; equivalently s_ads/s_gas decreases as the contrast grows.",
    "rationale": "lsd_p (Zeo++ Dif) is the largest included sphere along the free-sphere path and is explicitly NOT the bottleneck Df and NOT necessarily the global cavity Di; lsd_f is the passing bottleneck. Their contrast is a connectivity/topology proxy distinguishing cage-window from channel-like diffusion paths. Round-2 scoring retained this slot with the largest positive marginal improvement (+0.028 R in MAE), but its raw marginal training association with entropy loss was inconclusive (Spearman ~ -0.02), so its value likely arises through interactions in the nonlinear ANN rather than a monotone first-order effect; the hypothesis is stated as falsifiable and is not claimed as causally validated.",
    "falsification_criteria": "If frameworks with large lsd_p/lsd_f contrast (cage-like) show equal or lower entropy loss than channel-like frameworks of matched lsd_f and matched adsorbate, or if the entropy-loss association with the contrast is flat after conditioning on accessible volume proxies, the cage-localization hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif/Df contrast is a hard-sphere geometric surrogate for cage-versus-channel topology; it cannot distinguish connected cages from isolated ones, ignores window shapes and non-spherical pore cross-sections, and says nothing about energetic heterogeneity. Equilibrium entropy depends on the accessible configuration space, not on kinetic escape rates.",
      "physical_interpretation": "Native meaning: ratio of included-along-path sphere diameter to passing-bottleneck diameter; a large ratio indicates roomy interior space reachable through tight windows. q_lsd_p and q_lsd_f are dimensionless row-varying ratios to fixed positive training medians; no q-unity physical threshold is implied.",
      "boundary_behavior": "lsd_p (3.3452-15.5604) and lsd_f (0.85684-7.68726) are strictly positive over the full training domain, so the log argument is finite on every row; lsd_p >= lsd_f makes the ratio >= 1, so the descriptor is nonnegative without any added epsilon.",
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
    "slot_id": "h2",
    "name": "cage_window_contrast",
    "formula": "log(q_lsd_p / q_lsd_f)",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, a cavity-scale proxy) and the bottleneck diameter (lsd_f), because cage-like frameworks with large interior free space behind narrow windows localize the adsorbate in discrete cavities and reduce accessible translational configurations relative to quasi-continuous channels; equivalently s_ads/s_gas decreases as the contrast grows.",
    "rationale": "lsd_p (Zeo++ Dif) is the largest included sphere along the free-sphere path and is explicitly NOT the bottleneck Df and NOT necessarily the global cavity Di; lsd_f is the passing bottleneck. Their contrast is a connectivity/topology proxy distinguishing cage-window from channel-like diffusion paths. Round-2 scoring retained this slot with the largest positive marginal improvement (+0.028 R in MAE), but its raw marginal training association with entropy loss was inconclusive (Spearman ~ -0.02), so its value likely arises through interactions in the nonlinear model rather than a monotone first-order effect; the training-only precheck additionally flags the descriptor as redundant with a current input. Source E06 (MCM-22 supercage adsorption) supports the qualitative idea that rotational freedom inside cages can affect adsorption equilibrium, but that source is molecule- and framework-specific (450-850 K discussions) and transfers only conditionally; the hypothesis is stated as falsifiable and is not claimed as causally validated.",
    "falsification_criteria": "If frameworks with large lsd_p/lsd_f contrast (cage-like) show equal or lower entropy loss than channel-like frameworks of matched lsd_f and matched adsorbate, or if the entropy-loss association with the contrast is flat after conditioning on accessible volume proxies, the cage-localization hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif/lsd_p is the largest sphere included ALONG the free-sphere path and Df/lsd_f is the passing bottleneck; neither is necessarily the global cavity diameter Di, and their contrast is a hard-sphere geometric surrogate for cage-versus-channel topology. It cannot distinguish connected cages from isolated ones, ignores window shapes and non-spherical pore cross-sections, and says nothing about energetic heterogeneity. Equilibrium entropy depends on the accessible configuration space, not on kinetic escape rates. Source E06 discusses cage-confined molecules in MCM-22 supercages where rotational freedom may substantially affect equilibrium; transfer to all pure-silica frameworks at infinite dilution remains a hypothesis, and lsd_p/lsd_f are not the supercage radii discussed there.",
      "physical_interpretation": "Native meaning: ratio of the largest included-along-path sphere diameter to the passing-bottleneck diameter; a large ratio suggests roomy interior space reachable through tighter passages. q_lsd_p and q_lsd_f are dimensionless row-varying ratios to fixed positive training medians; no q-unity physical threshold is implied.",
      "boundary_behavior": "lsd_p (3.3452-15.5604) and lsd_f (0.85684-7.68726) are strictly positive over the full training domain, so the log argument is finite on every training row without epsilon or imputation. The earlier claim that lsd_p >= lsd_f is incorrect as a domain statement: the training ranges overlap and cross (lsd_p min 3.3452 < lsd_f max 7.68726), so the ratio can be below 1 and the descriptor can be negative; no nonnegativity is asserted or needed. The ratio is dimensionless, so the log argument is dimensionless.",
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

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "cage_window_contrast",
    "formula": "q_lsd_p / q_lsd_f",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, a cavity-scale proxy) and the bottleneck diameter (lsd_f), because cage-like frameworks with large interior free space behind narrow windows localize the adsorbate in discrete cavities and reduce accessible translational configurations relative to quasi-continuous channels; equivalently s_ads/s_gas decreases as the contrast grows.",
    "rationale": "lsd_p (Zeo++ Dif) is the largest included sphere along the free-sphere path and is explicitly NOT the bottleneck Df and NOT necessarily the global cavity Di; lsd_f is the passing bottleneck. Their contrast is a connectivity/topology proxy distinguishing cage-window from channel-like diffusion paths. Round-2 scoring retained this slot with the largest positive marginal improvement (+0.028 R in MAE), but its raw marginal training association with entropy loss was inconclusive (Spearman ~ -0.02), so its value likely arises through interactions in the nonlinear model rather than a monotone first-order effect; the training-only precheck additionally flags the descriptor as redundant with a current input. Source E06 (MCM-22 supercage adsorption) supports the qualitative idea that rotational freedom inside cages can affect adsorption equilibrium, but that source is molecule- and framework-specific (450-850 K discussions) and transfers only conditionally; the hypothesis is stated as falsifiable and is not claimed as causally validated.",
    "falsification_criteria": "If frameworks with large lsd_p/lsd_f contrast (cage-like) show equal or lower entropy loss than channel-like frameworks of matched lsd_f and matched adsorbate, or if the entropy-loss association with the contrast is flat after conditioning on accessible volume proxies, the cage-localization hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif/lsd_p is the largest sphere included ALONG the free-sphere path and Df/lsd_f is the passing bottleneck; neither is necessarily the global cavity diameter Di, and their contrast is a hard-sphere geometric surrogate for cage-versus-channel topology. It cannot distinguish connected cages from isolated ones, ignores window shapes and non-spherical pore cross-sections, and says nothing about energetic heterogeneity. Equilibrium entropy depends on the accessible configuration space, not on kinetic escape rates. Source E06 discusses cage-confined molecules in MCM-22 supercages where rotational freedom may substantially affect equilibrium; transfer to all pure-silica frameworks at infinite dilution remains a hypothesis, and lsd_p/lsd_f are not the supercage radii discussed there.",
      "physical_interpretation": "Native meaning: ratio of the largest included-along-path sphere diameter to the passing-bottleneck diameter; a large ratio suggests roomy interior space reachable through tighter passages. q_lsd_p and q_lsd_f are dimensionless row-varying ratios to fixed positive training medians; no q-unity physical threshold is implied.",
      "boundary_behavior": "lsd_p (3.3452-15.5604) and lsd_f (0.85684-7.68726) are strictly positive over the full training domain, so the ratio is finite on every training row without epsilon or imputation. The training ranges overlap and cross (lsd_p min 3.3452 < lsd_f max 7.68726), so the ratio can be below or above 1; only strict positivity is asserted, not lsd_p >= lsd_f. The ratio is dimensionless. Replacing the previous log-of-ratio with the raw ratio removes the exact log-linear decomposition into existing inputs (log(q_lsd_p) - log(q_lsd_f)) that caused the redundancy rejection; the cage-window connectivity-contrast claim itself is unchanged and remains an empirical proxy relation, not a validated mechanism.",
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

候选标识：`high/rag_agent/replicate-2/round-3/h3`

最终状态：scored；边际收益：-2.270553 pp；保留：False。

复核改动字段：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "elongation_window_orientation_penalty",
    "formula": "rotor_case(0.0, log(q_GeDi / q_lsd_f), log(q_GeDi / q_lsd_f))",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, among molecules with anisotropic heavy-atom geometry (linear and nonlinear rotor classes), the adsorption entropy loss (-delta_s/R) increases with the ratio of the molecule's largest interatomic distance (GeDi) to the framework bottleneck diameter (lsd_f), because elongated molecules must adopt a restricted subset of orientations to pass through and reside behind narrow windows, reducing rotational-translational configuration space; single-site molecules (GeDi = 0 in the heavy-atom representation) carry no elongation penalty by definition and take the constant single-site branch.",
    "rationale": "GeDi is the largest distance between two molecular atoms in the original implicit-H/heavy-atom representation; it is a legitimate zero exactly for the 54 single-site training rows, so the rotor_case branching (single_site = 0.0, linear and nonlinear = log(q_GeDi/q_lsd_f), all branches dimensionless and unit-compatible) keeps every training row finite without imputation or epsilon. The predeclared proxy derivative is d(descriptor)/d(GeDi) > 0 within the linear and nonlinear branches, and the predeclared target-association direction is entropy loss increasing with the descriptor. This differs from the rejected round-1 inertia and asphericity slots by coupling molecular elongation directly to the bottleneck scale rather than to surface area or inertia alone; its novelty is a new combination and it is not claimed as causally validated.",
    "falsification_criteria": "If, at fixed Vol^(1/3)/lsd_f, elongated adsorbates (high GeDi/Vol^(1/3)) show no systematically higher entropy loss than compact ones in narrow-bottleneck frameworks, or if the association reverses sign in wide-pore frameworks where orientation at windows should not matter, the window-orientation-penalty hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "GeDi in the heavy-atom representation is a maximum-extent proxy, not true all-atom geometry; hydrogen positions and all-atom inertia are not captured, and zero GeDi for single-site molecules reflects the representation, not a physical absence of the molecule. Explicit rotor_case branches: single_site -> 0.0 (dimensionless constant, no anisotropic axis defined), linear -> log(q_GeDi/q_lsd_f), nonlinear -> log(q_GeDi/q_lsd_f). The linear and nonlinear branches share the same expression empirically because the training split does not justify distinct functional forms, not because the physics is identical.",
      "physical_interpretation": "Native meaning: ratio of the molecule's largest heavy-atom separation to the largest free passing sphere; a large ratio indicates a molecule whose longest axis exceeds the bottleneck scale, forcing orientation selection at windows. q_GeDi and q_lsd_f are dimensionless row-varying ratios to fixed positive training medians; no q-unity physical threshold is implied.",
      "boundary_behavior": "At the single-site boundary (GeDi = 0, 54 training rows), the constant branch 0.0 is used, avoiding log(0); lsd_f is strictly positive (0.85684-7.68726), so the linear and nonlinear branch log arguments are strictly positive and finite on every training row; the rotor class is fixed during the partial derivative and the branch selection tolerance is 1e-10 on normalized PMI proxies.",
      "vary_input": "GeDi",
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
      "explicit_rotor_branches": true
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
      "training_spearman": 0.5911725091793586,
      "target_association": "contradicted",
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
    "slot_id": "h3",
    "name": "elongation_window_orientation_penalty",
    "formula": "rotor_case(0.0, log(q_GeDi / q_lsd_f), log(q_GeDi / q_lsd_f))",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, among molecules with anisotropic heavy-atom geometry (linear and nonlinear rotor classes), the adsorption entropy loss (-delta_s/R) increases with the ratio of the molecule's largest interatomic distance (GeDi) to the framework bottleneck diameter (lsd_f), because elongated molecules must adopt a restricted subset of orientations to pass through and reside behind narrow windows, reducing rotational-translational configuration space; single-site molecules (GeDi = 0 in the heavy-atom representation) carry no elongation penalty by definition and take the constant single-site branch.",
    "rationale": "GeDi is the largest distance between two molecular atoms in the original implicit-H/heavy-atom representation; it is a legitimate zero exactly for the 54 single-site training rows, matching the rotor classification, so the rotor_case branching (single_site = 0.0, linear and nonlinear = log(q_GeDi/q_lsd_f), all branches dimensionless and unit-compatible) keeps every training row finite without imputation or epsilon. The predeclared proxy derivative is d(descriptor)/d(GeDi) > 0 within the linear and nonlinear branches. Honest qualification: the training-only precheck reports the predeclared target association as contradicted (Spearman ~0.59 on the full regime, perturbation ~0.039) despite the positive rank correlation, so the monotone first-order claim is empirically unsupported in training and any retained value may arise through interactions in the nonlinear model; this differs from the rejected round-1 inertia and asphericity slots by coupling molecular elongation directly to the bottleneck scale, but it is a new combination only and is not claimed as causally validated. Sources E01/E03 support rotational contributions to entropy loss in confined zeolite environments conditionally and do not supply fitted coefficients.",
    "falsification_criteria": "If, at fixed Vol^(1/3)/lsd_f, elongated adsorbates (high GeDi/Vol^(1/3)) show no systematically higher entropy loss than compact ones in narrow-bottleneck frameworks, or if the association reverses sign in wide-pore frameworks where orientation at windows should not matter, the window-orientation-penalty hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E03"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "GeDi in the original implicit-H/heavy-atom representation is a maximum heavy-atom pair distance proxy, not true all-atom geometry; hydrogen positions and all-atom inertia are not captured, and zero GeDi for single-site molecules reflects the representation, not a physical absence of the molecule. Explicit rotor_case branches: single_site -> 0.0 (dimensionless constant, no anisotropic heavy-atom axis defined), linear -> log(q_GeDi/q_lsd_f), nonlinear -> log(q_GeDi/q_lsd_f). The linear and nonlinear branches share the same expression empirically because the training split does not justify distinct functional forms, not because the physics is identical. Sources E01 and E03 report that rotational degrees of freedom contribute to adsorption entropy loss in zeolites (e.g., larger rotational loss in MFI than FAU), but those sources concern cavity-scale confinement of alkanes, not bottleneck-relative elongation, and transfer remains a hypothesis.",
      "physical_interpretation": "Native meaning: ratio of the molecule's largest heavy-atom separation to the largest free passing sphere; a large ratio indicates a molecule whose longest heavy-atom axis exceeds the bottleneck scale, plausibly forcing orientation selection at windows. q_GeDi and q_lsd_f are dimensionless row-varying ratios to fixed positive training medians; no q-unity physical threshold is implied.",
      "boundary_behavior": "At the single-site boundary (GeDi = 0, exactly the 54 single-site training rows under the heavy-atom representation), the constant branch 0.0 is used, avoiding log(0) without epsilon or imputation; zero GeDi is a representation fact, not zero molecular size. lsd_f is strictly positive (0.85684-7.68726), so the linear and nonlinear branch log arguments are strictly positive and finite on every training row. The ratio is dimensionless and can be below or above 1. The rotor class is fixed during the partial derivative and branch selection uses the 1e-10 tolerance on normalized PMI proxies.",
      "vary_input": "GeDi",
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
      "explicit_rotor_branches": true
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
      "training_spearman": 0.5911725091793586,
      "target_association": "contradicted",
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
    "slot_id": "h3",
    "name": "elongation_window_orientation_penalty",
    "formula": "rotor_case(0.0, log(q_GeDi / q_lsd_f), log(q_GeDi / q_lsd_f))",
    "hypothesis": "For pure-silica rigid zeolites at infinite dilution, among molecules with anisotropic heavy-atom geometry (linear and nonlinear rotor classes), the adsorption entropy loss (-delta_s/R) increases with the ratio of the molecule's largest interatomic distance (GeDi) to the framework bottleneck diameter (lsd_f), because elongated molecules must adopt a restricted subset of orientations to pass through and reside behind narrow windows, reducing rotational-translational configuration space; single-site molecules (GeDi = 0 in the heavy-atom representation) carry no elongation penalty by definition and take the constant single-site branch.",
    "rationale": "GeDi is the largest distance between two molecular atoms in the original implicit-H/heavy-atom representation; it is a legitimate zero exactly for the 54 single-site training rows, matching the rotor classification, so the rotor_case branching (single_site = 0.0, linear and nonlinear = log(q_GeDi/q_lsd_f), all branches dimensionless and unit-compatible) keeps every training row finite without imputation or epsilon. The predeclared proxy derivative is d(descriptor)/d(GeDi) > 0 within the linear and nonlinear branches. Honest qualification: the training-only precheck reports the predeclared target association as contradicted (Spearman ~0.59 on the full regime, perturbation ~0.039) despite the positive rank correlation, so the monotone first-order claim is empirically unsupported in training and any retained value may arise through interactions in the nonlinear model; this differs from the rejected round-1 inertia and asphericity slots by coupling molecular elongation directly to the bottleneck scale, but it is a new combination only and is not claimed as causally validated. Sources E01/E03 support rotational contributions to entropy loss in confined zeolite environments conditionally and do not supply fitted coefficients.",
    "falsification_criteria": "If, at fixed Vol^(1/3)/lsd_f, elongated adsorbates (high GeDi/Vol^(1/3)) show no systematically higher entropy loss than compact ones in narrow-bottleneck frameworks, or if the association reverses sign in wide-pore frameworks where orientation at windows should not matter, the window-orientation-penalty hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E03"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "GeDi in the original implicit-H/heavy-atom representation is a maximum heavy-atom pair distance proxy, not true all-atom geometry; hydrogen positions and all-atom inertia are not captured, and zero GeDi for single-site molecules reflects the representation, not a physical absence of the molecule. Explicit rotor_case branches: single_site -> 0.0 (dimensionless constant, no anisotropic heavy-atom axis defined), linear -> log(q_GeDi/q_lsd_f), nonlinear -> log(q_GeDi/q_lsd_f). The linear and nonlinear branches share the same expression empirically because the training split does not justify distinct functional forms, not because the physics is identical. Sources E01 and E03 report that rotational degrees of freedom contribute to adsorption entropy loss in zeolites (e.g., larger rotational loss in MFI than FAU), but those sources concern cavity-scale confinement of alkanes, not bottleneck-relative elongation, and transfer remains a hypothesis.",
      "physical_interpretation": "Native meaning: ratio of the molecule's largest heavy-atom separation to the largest free passing sphere; a large ratio indicates a molecule whose longest heavy-atom axis exceeds the bottleneck scale, plausibly forcing orientation selection at windows. q_GeDi and q_lsd_f are dimensionless row-varying ratios to fixed positive training medians; no q-unity physical threshold is implied.",
      "boundary_behavior": "At the single-site boundary (GeDi = 0, exactly the 54 single-site training rows under the heavy-atom representation), the constant branch 0.0 is used, avoiding log(0) without epsilon or imputation; zero GeDi is a representation fact, not zero molecular size. lsd_f is strictly positive (0.85684-7.68726), so the linear and nonlinear branch log arguments are strictly positive and finite on every training row. The ratio is dimensionless and can be below or above 1. The rotor class is fixed during the partial derivative and branch selection uses the 1e-10 tolerance on normalized PMI proxies.",
      "vary_input": "GeDi",
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
      "explicit_rotor_branches": true
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
      "training_spearman": 0.5911725091793586,
      "target_association": "contradicted",
      "perturbation": 0.03867262081,
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
        "record_id": "chunk:d551cda661adcb5ac3f29200",
        "paper_id": "doi:10.1038/s41586-021-03429-y",
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
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a716c0f2d08195e0bc57308d",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6cc904c61f240366bfe7825e",
        "paper_id": "doi:10.1039/c8cp01615a",
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
        "record_id": "chunk:1ce2e04d7643ce73d701feab",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
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
        "record_id": "chunk:739732ec5f189e86e2a38fdd",
        "paper_id": "doi:10.26434/chemrxiv.13288805.v1",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9a3907e626bcdef0bc5bb0cb",
        "paper_id": "doi:10.1002/chem.201705627",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd6fadcf0e5f2fd99bb3f46e",
        "paper_id": "doi:10.1021/acsami.5c17486",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ecf3b350af8d5c09a9a10048",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:0b24581feff306a74a633d6f",
        "paper_id": "doi:10.1038/s41586-021-03429-y",
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
    "query": "adsorption entropy confinement For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases monotonically with the ratio of the adsorbate's cubic-root van der Waals volume to the framework's free-passage bottleneck diameter, because a tighter passage relative to molecular size reduces the accessible translational configuration space of the confined molecule. log((q_Vol**(0.3333333333)) / q_lsd_f) For pure-silica rigid zeolites at infinite dilution, the adsorption entropy loss (-delta_s/R) increases with the contrast between the largest included sphere along the free-sphere path (lsd_p, a cavity-scale proxy) and the bottleneck diameter (lsd_f), because cage-like frameworks with large interior free space behind narrow windows localize the adsorbate in discrete cavities and reduce accessible translational configurations relative to quasi-continuous channels; equivalently s_ads/s_gas decreases as the contrast grows. log(q_lsd_p / q_lsd_f) For pure-silica rigid zeolites at infinite dilution, among molecules with anisotropic heavy-atom geometry (linear and nonlinear rotor classes), the adsorption entropy loss (-delta_s/R) increases with the ratio of the molecule's largest interatomic distance (GeDi) to the framework bottleneck diameter (lsd_f), because elongated molecules must adopt a restricted subset of orientations to pass through and reside behind narrow windows, reducing rotational-translational configuration space; single-site molecules (GeDi = 0 in the heavy-atom representation) carry no elongation penalty by definition and take the constant single-site branch. rotor_case(0.0, log(q_GeDi / q_lsd_f), log(q_GeDi / q_lsd_f))   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:8dd99e6f4fc8a3c4e46d940b",
      "chunk:ae6e434cc894357276cba23f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:d52b47528dc9757d7e603c4f"
    ],
    "items": 10,
    "lexical_tokens": 4627,
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
