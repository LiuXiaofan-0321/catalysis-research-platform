# high/rag_agent/replicate-3/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h2",
    "name": "bottleneck_confinement_inverse",
    "formula": "1 / q_lsd_f**2",
    "hypothesis": "Frameworks with smaller passing free-sphere bottlenecks (smaller lsd_f, the Zeo++ Df largest sphere through a periodic free path) impose stronger geometric confinement gradients at adsorption sites, producing larger adsorbed-phase entropy loss at infinite dilution; the entropy loss is inversely associated with the bottleneck diameter squared.",
    "rationale": "Df/lsd_f is strictly positive in training (min 0.85684), so 1/q_lsd_f**2 is finite for every row with no imputation. The exponent 2 lies within the allowed fixed-numeric range. This descriptor deliberately uses the bottleneck, not the included-along-path diameter lsd_p and not a global cavity Di, because Df is the quantity in D0 that gates access to adsorption space. The association is hypothesized, not established; a known qualitative confinement relation is re-expressed here in normalized proxy form, and the D0 inputs already present in the nonlinear ANN may re-express part of this signal.",
    "falsification_criteria": "If, holding AV and adsorbate shape fixed, entropy loss shows no inverse association with lsd_f, or if the association is dominated by lsd_p (included diameter along the free path) rather than lsd_f, the bottleneck-gradient mechanism is falsified and an alternative included-cavity mechanism should be tested instead.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Zeo++ Df computed with a fixed probe geometry proxies the geometric confinement gradient felt by diverse adsorbates; the transfer from a hard-sphere path measure to molecule-specific entropy loss is approximate and unresolved for flexible or off-path adsorption sites.",
      "physical_interpretation": "lsd_f is the largest sphere able to pass through a periodic free path (bottleneck), not the global included cavity diameter; q_lsd_f = lsd_f/5.16326 is a dimensionless row-varying input with no physical unity threshold.",
      "boundary_behavior": "lsd_f is strictly positive on the training domain (0.85684 to 7.68726), so 1/q_lsd_f**2 is finite and well-defined everywhere; the descriptor grows steeply as the bottleneck approaches its lower domain bound, which is an extrapolation regime flagged for honest uncertainty.",
      "vary_input": "lsd_f",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_f",
      "regime_train_quantiles": [
        0.0,
        1.0
      ],
      "entropy_direction": "increasing"
    }
  },
  {
    "slot_id": "h1",
    "name": "path_contrast_localization",
    "formula": "q_Vol * (lsd_p / lsd_f)**2",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases when the largest included sphere along the free-sphere path (lsd_p, Zeo++ Dif) is large relative to the passing bottleneck (lsd_f, Zeo++ Df). A large included-region-to-bottleneck contrast indicates adsorbates localizing in spacious cavities behind narrow windows, which plausibly increases the site-localization entropy penalty; entropy loss is monotonically associated with (lsd_p/lsd_f)**2.",
    "rationale": "Keeps the preserved cavity-behind-narrow-window localization story but corrects the expression: the round-2 precheck found the bare contrast (lsd_p/lsd_f)**2 essentially unassociated with entropy loss (Spearman -0.019, inconclusive), violating its own predeclared falsification condition. The contrast is therefore weighted by q_Vol, since a localization entropy penalty should scale with how much molecular volume must be accommodated inside the cavity; this is consistent with reported reasoning that rotational freedom depends on molecular size relative to available cage space (E06, E07). Limitations: hard-sphere geometric extremes, an empirical combination blind to surface chemistry, window multiplicity and molecular flexibility; mechanism_validated remains false and the association is statistical, not derived.",
    "falsification_criteria": "Predeclared proxy derivative: d(entropy loss)/d(q_Vol * (lsd_p/lsd_f)**2) > 0 within rotor-class-stratified training data. Falsified if the size-weighted contrast shows no residual association after conditioning on q_Vol and lsd_f (i.e., it adds nothing beyond molecular size and bottleneck confinement), if the sign flips, or if high-contrast frameworks with small adsorbates show entropy losses statistically indistinguishable from low-contrast frameworks at matched q_Vol and lsd_f.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E06",
      "E07"
    ],
    "variable_mappings": {
      "lsd_p": "included_along_free_path_Dif",
      "lsd_f": "bottleneck_free_sphere_Df",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Dif (largest included sphere along the free-sphere path) and Df (largest passing bottleneck sphere) are hard-sphere geometric extremes on representative paths, not the global cavity diameter Di, and transfer imperfectly to real adsorbates with finite size and soft potentials; Vol ignores shape anisotropy. The unweighted contrast (lsd_p/lsd_f)**2 showed an inconclusive global training association (Spearman -0.019), so the size weighting is a predeclared expression correction, not a validated mechanism.",
      "physical_interpretation": "lsd_f is the largest sphere that can pass through a periodic free path (window bottleneck); lsd_p is the largest included sphere along that path (cavity scale on the path); Vol is the adsorbate van der Waals volume. q_Vol = Vol / Vol_ref is a dimensionless row-varying input relative to the fixed positive reference median 67.24 A^3; the full descriptor is dimensionless and no physical threshold is asserted at descriptor value 1.",
      "boundary_behavior": "lsd_p (min 3.3452 A), lsd_f (min 0.85684 A) and Vol (min 20.424 A^3) are strictly positive across all 2361 training rows with strictly positive reference medians, so q_Vol and the squared contrast ratio are finite for every row without imputation; the descriptor grows only outside the native domain, which the regime bounds exclude. No zero branch or rotor_case is invoked.",
      "vary_input": "lsd_p",
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

候选标识：`high/rag_agent/replicate-3/round-3/h1`

最终状态：scored；边际收益：-4.291630 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "thickness_orientation_penalty",
    "formula": "q_Vol * PBF**2",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the product of adsorbate van der Waals volume and squared out-of-plane thickness (PBF, mean heavy-atom distance from the best-fit plane). At fixed volume, thicker (less planar) molecules fit fewer stable orientations against channel walls and within cavity sites, so the orientational/configurational entropy penalty at the adsorption site grows with q_Vol * PBF**2; entropy loss is monotonically associated with this descriptor.",
    "rationale": "PBF is an original implicit-H/heavy-atom planarity proxy, not full all-atom geometry; its zeros are legitimate (planar heavy-atom skeletons) and the product form keeps the descriptor finite there. The volume factor encodes that at equal thickness a larger molecule excludes more site configurations. Mechanistic limit: the proxy cannot distinguish orientation locking parallel to walls from true rotational freezing, and it carries no all-atom inertia information.",
    "falsification_criteria": "If training association shows entropy loss decreasing with PBF at fixed volume (i.e., planar molecules lock flat against walls with a single dominant orientation and lose more entropy than thick molecules), the thickness-orientation mechanism is falsified. Also falsified if association vanishes within fixed rotor_class strata.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF is a heavy-atom planarity proxy from the original representation; it is not all-atom thickness and legitimate zeros mean planar heavy-atom skeletons, not absent molecules. Vol is a van der Waals volume proxy. Transfer limit: neither captures chemistry-specific wall interactions.",
      "physical_interpretation": "Native PBF in angstrom and Vol in angstrom^3; q_Vol is dimensionless. Increasing descriptor means larger, thicker molecules. Predeclared partial-derivative direction: increasing q_Vol * PBF**2 is associated with increasing entropy loss and correspondingly decreasing s_ads/s_gas. No q-unity value is claimed as a physical threshold.",
      "boundary_behavior": "At PBF = 0 (587 legitimate planar rows) the descriptor is exactly 0, finite, interpreted as minimal thickness penalty for that proxy; no imputation and no epsilon added. All training rows finite over native PBF in [0, 0.656249528] and Vol in [20.424, 161.144].",
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
      "output_dimensions": {
        "length": "2"
      },
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
      "training_spearman": 0.3090560731837001,
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
    "slot_id": "h1",
    "name": "thickness_orientation_penalty",
    "formula": "q_Vol * PBF**2",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the product of adsorbate van der Waals volume and squared out-of-plane thickness (PBF, mean heavy-atom distance from the best-fit plane). At fixed volume, thicker (less planar) molecules fit fewer stable orientations against channel walls and within cavity sites, so the orientational/configurational entropy penalty at the adsorption site grows with q_Vol * PBF**2; entropy loss is monotonically associated with this descriptor.",
    "rationale": "PBF is an original implicit-H/heavy-atom planarity proxy, not full all-atom geometry; its zeros are legitimate (planar heavy-atom skeletons) and the product form keeps the descriptor finite there. The volume factor encodes that at equal thickness a larger molecule excludes more site configurations. Mechanistic limit: the proxy cannot distinguish orientation locking parallel to walls from true rotational freezing, and it carries no all-atom inertia information.",
    "falsification_criteria": "If training association shows entropy loss decreasing with PBF at fixed volume (i.e., planar molecules lock flat against walls with a single dominant orientation and lose more entropy than thick molecules), the thickness-orientation mechanism is falsified. Also falsified if association vanishes within fixed rotor_class strata.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF is a heavy-atom planarity proxy from the original representation; it is not all-atom thickness and legitimate zeros mean planar heavy-atom skeletons, not absent molecules. Vol is a van der Waals volume proxy. Transfer limit: neither captures chemistry-specific wall interactions.",
      "physical_interpretation": "Native PBF in angstrom and Vol in angstrom^3; q_Vol is dimensionless. Increasing descriptor means larger, thicker molecules. Predeclared partial-derivative direction: increasing q_Vol * PBF**2 is associated with increasing entropy loss and correspondingly decreasing s_ads/s_gas. No q-unity value is claimed as a physical threshold.",
      "boundary_behavior": "At PBF = 0 (587 legitimate planar rows) the descriptor is exactly 0, finite, interpreted as minimal thickness penalty for that proxy; no imputation and no epsilon added. All training rows finite over native PBF in [0, 0.656249528] and Vol in [20.424, 161.144].",
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
      "output_dimensions": {
        "length": "2"
      },
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
      "training_spearman": 0.3090560731837001,
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
    "slot_id": "h1",
    "name": "thickness_orientation_penalty",
    "formula": "q_Vol * PBF**2",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the product of adsorbate van der Waals volume and squared out-of-plane thickness (PBF, mean heavy-atom distance from the best-fit plane). At fixed volume, thicker (less planar) molecules fit fewer stable orientations against channel walls and within cavity sites, so the orientational/configurational entropy penalty at the adsorption site grows with q_Vol * PBF**2; entropy loss is monotonically associated with this descriptor.",
    "rationale": "PBF is an original implicit-H/heavy-atom planarity proxy, not full all-atom geometry; its zeros are legitimate (planar heavy-atom skeletons) and the product form keeps the descriptor finite there. The volume factor encodes that at equal thickness a larger molecule excludes more site configurations. Mechanistic limit: the proxy cannot distinguish orientation locking parallel to walls from true rotational freezing, and it carries no all-atom inertia information.",
    "falsification_criteria": "If training association shows entropy loss decreasing with PBF at fixed volume (i.e., planar molecules lock flat against walls with a single dominant orientation and lose more entropy than thick molecules), the thickness-orientation mechanism is falsified. Also falsified if association vanishes within fixed rotor_class strata.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "PBF": "heavy_atom_planarity"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "PBF is a heavy-atom planarity proxy from the original representation; it is not all-atom thickness and legitimate zeros mean planar heavy-atom skeletons, not absent molecules. Vol is a van der Waals volume proxy. Transfer limit: neither captures chemistry-specific wall interactions.",
      "physical_interpretation": "Native PBF in angstrom and Vol in angstrom^3; q_Vol is dimensionless. Increasing descriptor means larger, thicker molecules. Predeclared partial-derivative direction: increasing q_Vol * PBF**2 is associated with increasing entropy loss and correspondingly decreasing s_ads/s_gas. No q-unity value is claimed as a physical threshold.",
      "boundary_behavior": "At PBF = 0 (587 legitimate planar rows) the descriptor is exactly 0, finite, interpreted as minimal thickness penalty for that proxy; no imputation and no epsilon added. All training rows finite over native PBF in [0, 0.656249528] and Vol in [20.424, 161.144].",
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
      "output_dimensions": {
        "length": "2"
      },
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
      "training_spearman": 0.3090560731837001,
      "target_association": "consistent",
      "perturbation": 0.0046290119000000005,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/rag_agent/replicate-3/round-3/h2`

最终状态：scored；边际收益：-2.281891 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "corridor_steering_mismatch",
    "formula": "q_GeDi / lsd_p",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the ratio of the adsorbate's longest heavy-atom extension (GeDi, largest interatomic distance) to the largest included sphere along the free-sphere path (lsd_p, Zeo++ Dif). When molecular extension approaches the corridor's included diameter, translational passage requires alignment and steering through the pore network, reducing the accessible configuration space sampled at adsorption sites; entropy loss is monotonically associated with q_GeDi / lsd_p.",
    "rationale": "This is a cross term between an adsorbate shape proxy and a framework path descriptor: lsd_p (Dif) is explicitly the included diameter along the free path, not the bottleneck Df and not a global cavity diameter Di. The mechanism is corridor steering, distinct from bottleneck confinement (retained h2) and from cavity localization (retained h1). Limit: GeDi is a heavy-atom proxy ignoring hydrogen extent, and lsd_p is a single geometric summary that ignores path tortuosity and site multiplicity.",
    "falsification_criteria": "If entropy loss instead correlates primarily with the passing bottleneck lsd_f (Df) rather than the included-path diameter lsd_p at fixed molecule size, or if the association inverts (steering through wide corridors adding rather than removing configurations), the hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "GeDi is the original heavy-atom representation pair distance; legitimate zeros (54 rows) mean a single heavy-atom site, not zero true molecular extent. lsd_p is Dif along the free-sphere path, not Df and not global Di. Transfer limit: steering in real diffusion is kinetic; only the equilibrium configuration-space reduction is claimed here.",
      "physical_interpretation": "q_GeDi is dimensionless, lsd_p is in angstrom, so the descriptor scales as 1/angstrom on native units; only its monotonic association is claimed. Predeclared partial-derivative direction: increasing q_GeDi / lsd_p is associated with increasing entropy loss and decreasing s_ads/s_gas. No q-unity ratio is a physical equality threshold.",
      "boundary_behavior": "At GeDi = 0 the descriptor is exactly 0, finite, interpreted as no elongation-steering proxy; lsd_p has training minimum 3.3452 angstrom so the divisor never vanishes. All 2361 rows finite over GeDi in [0, 10.97181443] and lsd_p in [3.3452, 15.5604].",
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
    "status": "rejected",
    "dimensions": {
      "status": "passed",
      "output_dimensions": {
        "length": "-1"
      },
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "GeDi",
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_p": "included_along_free_path_Dif"
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

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "corridor_steering_mismatch",
    "formula": "q_GeDi / q_lsd_p",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the ratio of the adsorbate's longest heavy-atom extension (GeDi, largest interatomic distance) to the largest included sphere along the free-sphere path (lsd_p, Zeo++ Dif). When molecular extension approaches the corridor's included diameter, translational passage requires alignment and steering through the pore network, reducing the accessible configuration space sampled at adsorption sites; entropy loss is monotonically associated with q_GeDi / lsd_p.",
    "rationale": "Corrected cross term between an adsorbate shape proxy and a framework path descriptor: lsd_p (Dif) is the included diameter along the free-sphere path, not the bottleneck Df and not a global cavity diameter Di, so it is used only as a corridor-accommodation proxy with q-normalization making the descriptor dimensionless. The mechanism is corridor steering: when the molecular extension approaches the corridor's included diameter, translational passage requires alignment through the pore network, reducing the configuration space sampled at adsorption sites. The formula's monotonicity is now declared consistently: the descriptor increases in GeDi and decreases in lsd_p, and the predeclared varying input is GeDi. Limit: the empirical association of this descriptor with entropy loss remains a hypothesis to be tested; the previous draft's direction declaration, not the mechanism, was the identified error.",
    "falsification_criteria": "If training association shows entropy loss decreasing with q_GeDi/q_lsd_p (e.g., elongated molecules retaining translational freedom along channels dominate the association), the corridor-steering mechanism is falsified. Also falsified if the association is governed primarily by the passing bottleneck lsd_f (Df) rather than the included-path diameter lsd_p at fixed molecular extension, or if the association vanishes within fixed rotor_class strata.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "GeDi is the original implicit-H/heavy-atom largest interatomic distance; legitimate zeros mean a single-heavy-atom site, not zero true molecular extent. lsd_p is Zeo++ Dif, the largest included sphere along the free-sphere path; it is neither the bottleneck Df (lsd_f) nor a global cavity diameter Di, so it is only a corridor-accommodation proxy. Transfer limit: steering in real diffusion is kinetic; only an equilibrium configuration-space reduction is claimed, and neither proxy captures chemistry-specific wall interactions or path tortuosity/site multiplicity.",
      "physical_interpretation": "q_GeDi and q_lsd_p are both dimensionless row-varying inputs relative to fixed training-reference medians (GeDi_ref = 3.302656784, lsd_p_ref = 6.38663); the descriptor is dimensionless. Correction versus the previous draft: the descriptor q_GeDi/q_lsd_p INCREASES with GeDi (the molecular extension), not with lsd_p; the prior declaration of vary_input = lsd_p with descriptor_direction = increasing contradicted the formula's monotonicity, since the descriptor decreases in lsd_p. Predeclared partial-derivative direction: increasing q_GeDi / q_lsd_p (larger molecular extension relative to the corridor included diameter, e.g., by varying GeDi at fixed framework) is associated with increasing entropy loss and decreasing s_ads/s_gas. No q-unity ratio is claimed as a physical equality threshold; the fixed reference constants carry no universal physical meaning.",
      "boundary_behavior": "At GeDi = 0 (54 legitimate single-heavy-atom rows) the descriptor is exactly 0, finite, interpreted as no elongation-steering proxy; no imputation and no epsilon added. q_lsd_p is strictly positive on training data because lsd_p has minimum 3.3452 angstrom (lsd_p_ref = 6.38663), so the divisor never vanishes. All 2361 rows finite over GeDi in [0, 10.97181443] and lsd_p in [3.3452, 15.5604].",
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
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.6546880504725221,
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
    "name": "corridor_steering_mismatch",
    "formula": "q_GeDi / q_lsd_p",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the ratio of the adsorbate's longest heavy-atom extension (GeDi, largest interatomic distance) to the largest included sphere along the free-sphere path (lsd_p, Zeo++ Dif). When molecular extension approaches the corridor's included diameter, translational passage requires alignment and steering through the pore network, reducing the accessible configuration space sampled at adsorption sites; entropy loss is monotonically associated with q_GeDi / lsd_p.",
    "rationale": "Corrected cross term between an adsorbate shape proxy and a framework path descriptor: lsd_p (Dif) is the included diameter along the free-sphere path, not the bottleneck Df and not a global cavity diameter Di, so it is used only as a corridor-accommodation proxy with q-normalization making the descriptor dimensionless. The mechanism is corridor steering: when the molecular extension approaches the corridor's included diameter, translational passage requires alignment through the pore network, reducing the configuration space sampled at adsorption sites. The formula's monotonicity is now declared consistently: the descriptor increases in GeDi and decreases in lsd_p, and the predeclared varying input is GeDi. Limit: the empirical association of this descriptor with entropy loss remains a hypothesis to be tested; the previous draft's direction declaration, not the mechanism, was the identified error.",
    "falsification_criteria": "If training association shows entropy loss decreasing with q_GeDi/q_lsd_p (e.g., elongated molecules retaining translational freedom along channels dominate the association), the corridor-steering mechanism is falsified. Also falsified if the association is governed primarily by the passing bottleneck lsd_f (Df) rather than the included-path diameter lsd_p at fixed molecular extension, or if the association vanishes within fixed rotor_class strata.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03"
    ],
    "variable_mappings": {
      "GeDi": "heavy_atom_pair_distance",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "GeDi is the original implicit-H/heavy-atom largest interatomic distance; legitimate zeros mean a single-heavy-atom site, not zero true molecular extent. lsd_p is Zeo++ Dif, the largest included sphere along the free-sphere path; it is neither the bottleneck Df (lsd_f) nor a global cavity diameter Di, so it is only a corridor-accommodation proxy. Transfer limit: steering in real diffusion is kinetic; only an equilibrium configuration-space reduction is claimed, and neither proxy captures chemistry-specific wall interactions or path tortuosity/site multiplicity.",
      "physical_interpretation": "q_GeDi and q_lsd_p are both dimensionless row-varying inputs relative to fixed training-reference medians (GeDi_ref = 3.302656784, lsd_p_ref = 6.38663); the descriptor is dimensionless. Correction versus the previous draft: the descriptor q_GeDi/q_lsd_p INCREASES with GeDi (the molecular extension), not with lsd_p; the prior declaration of vary_input = lsd_p with descriptor_direction = increasing contradicted the formula's monotonicity, since the descriptor decreases in lsd_p. Predeclared partial-derivative direction: increasing q_GeDi / q_lsd_p (larger molecular extension relative to the corridor included diameter, e.g., by varying GeDi at fixed framework) is associated with increasing entropy loss and decreasing s_ads/s_gas. No q-unity ratio is claimed as a physical equality threshold; the fixed reference constants carry no universal physical meaning.",
      "boundary_behavior": "At GeDi = 0 (54 legitimate single-heavy-atom rows) the descriptor is exactly 0, finite, interpreted as no elongation-steering proxy; no imputation and no epsilon added. q_lsd_p is strictly positive on training data because lsd_p has minimum 3.3452 angstrom (lsd_p_ref = 6.38663), so the divisor never vanishes. All 2361 rows finite over GeDi in [0, 10.97181443] and lsd_p in [3.3452, 15.5604].",
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
        "lsd_p"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
        "lsd_p": "included_along_free_path_Dif"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        10.97181443
      ],
      "training_spearman": 0.6546880504725221,
      "target_association": "consistent",
      "perturbation": 0.03867262081,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/rag_agent/replicate-3/round-3/h3`

最终状态：scored；边际收益：+1.627473 pp；保留：True。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "heavy_inertia_extent_penalty",
    "formula": "sqrt(q_PMI3)",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the square root of the normalized third principal moment of inertia of the adsorbate's heavy-atom skeleton (PMI3). A larger largest heavy-atom moment proxies a more extended mass distribution, which experiences more orientational constraints inside cavities and channels, freezing out more rotational/configuration coordinates; entropy loss is monotonically associated with sqrt(q_PMI3).",
    "rationale": "PMI3 is an original implicit-H/heavy-atom inertia proxy, not true all-atom inertia; monatomic or single-heavy-atom rows legitimately have PMI3 = 0, which must not be read as zero physical rotational inertia (e.g., methane remains a symmetric rotor). The square root compresses the wide native range [0, 2414.63] and keeps the descriptor finite at zero. Mechanistic limit: the proxy cannot separate rotational entropy loss from translational size effects, which are already represented by volume- and bottleneck-based descriptors; it is intended as an independent shape/inertia axis.",
    "falsification_criteria": "If, within fixed rotor_class strata (single_site / linear / nonlinear), entropy loss shows no monotone association with PMI3 — i.e., rotational loss is governed by rotor symmetry and degeneracy rather than moment magnitude — the hypothesis is falsified. It is also weakened if sqrt(q_PMI3) adds no association beyond q_Vol (pure size restatement).",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI3 is a heavy-atom principal-moment proxy from the original representation; legitimate zeros are heavy-atom-degenerate cases, not zero all-atom inertia. Transfer limit: the proxy ignores hydrogen mass distribution and adsorbate symmetry number, both of which affect true rotational entropy loss.",
      "physical_interpretation": "PMI3 is native in angstrom^2*amu; q_PMI3 is dimensionless so the square root is dimensionless. Predeclared partial-derivative direction: increasing sqrt(q_PMI3) is associated with increasing entropy loss and decreasing s_ads/s_gas. No q-unity value is a physical threshold.",
      "boundary_behavior": "At PMI3 = 0 (54 legitimate rows, single-heavy-atom proxies) the descriptor is exactly 0, finite, interpreted as the minimal extent proxy, not zero physical inertia; no imputation and no epsilon added. All 2361 rows finite over PMI3 in [0, 2414.631462].",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI3"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.4086623414827737,
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
    "name": "heavy_inertia_extent_penalty",
    "formula": "sqrt(q_PMI3)",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the square root of the normalized third principal moment of inertia of the adsorbate's heavy-atom skeleton (PMI3). A larger largest heavy-atom moment proxies a more extended mass distribution, which experiences more orientational constraints inside cavities and channels, freezing out more rotational/configuration coordinates; entropy loss is monotonically associated with sqrt(q_PMI3).",
    "rationale": "PMI3 is an original implicit-H/heavy-atom inertia proxy, not true all-atom inertia; monatomic or single-heavy-atom rows legitimately have PMI3 = 0, which must not be read as zero physical rotational inertia (e.g., methane remains a symmetric rotor). The square root compresses the wide native range [0, 2414.63] and keeps the descriptor finite at zero. Mechanistic limit: the proxy cannot separate rotational entropy loss from translational size effects, which are already represented by volume- and bottleneck-based descriptors; it is intended as an independent shape/inertia axis.",
    "falsification_criteria": "If, within fixed rotor_class strata (single_site / linear / nonlinear), entropy loss shows no monotone association with PMI3 — i.e., rotational loss is governed by rotor symmetry and degeneracy rather than moment magnitude — the hypothesis is falsified. It is also weakened if sqrt(q_PMI3) adds no association beyond q_Vol (pure size restatement).",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI3 is a heavy-atom principal-moment proxy from the original representation; legitimate zeros are heavy-atom-degenerate cases, not zero all-atom inertia. Transfer limit: the proxy ignores hydrogen mass distribution and adsorbate symmetry number, both of which affect true rotational entropy loss.",
      "physical_interpretation": "PMI3 is native in angstrom^2*amu; q_PMI3 is dimensionless so the square root is dimensionless. Predeclared partial-derivative direction: increasing sqrt(q_PMI3) is associated with increasing entropy loss and decreasing s_ads/s_gas. No q-unity value is a physical threshold.",
      "boundary_behavior": "At PMI3 = 0 (54 legitimate rows, single-heavy-atom proxies) the descriptor is exactly 0, finite, interpreted as the minimal extent proxy, not zero physical inertia; no imputation and no epsilon added. All 2361 rows finite over PMI3 in [0, 2414.631462].",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI3"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.4086623414827737,
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
    "name": "heavy_inertia_extent_penalty",
    "formula": "sqrt(q_PMI3)",
    "hypothesis": "For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the square root of the normalized third principal moment of inertia of the adsorbate's heavy-atom skeleton (PMI3). A larger largest heavy-atom moment proxies a more extended mass distribution, which experiences more orientational constraints inside cavities and channels, freezing out more rotational/configuration coordinates; entropy loss is monotonically associated with sqrt(q_PMI3).",
    "rationale": "PMI3 is an original implicit-H/heavy-atom inertia proxy, not true all-atom inertia; monatomic or single-heavy-atom rows legitimately have PMI3 = 0, which must not be read as zero physical rotational inertia (e.g., methane remains a symmetric rotor). The square root compresses the wide native range [0, 2414.63] and keeps the descriptor finite at zero. Mechanistic limit: the proxy cannot separate rotational entropy loss from translational size effects, which are already represented by volume- and bottleneck-based descriptors; it is intended as an independent shape/inertia axis.",
    "falsification_criteria": "If, within fixed rotor_class strata (single_site / linear / nonlinear), entropy loss shows no monotone association with PMI3 — i.e., rotational loss is governed by rotor symmetry and degeneracy rather than moment magnitude — the hypothesis is falsified. It is also weakened if sqrt(q_PMI3) adds no association beyond q_Vol (pure size restatement).",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI3 is a heavy-atom principal-moment proxy from the original representation; legitimate zeros are heavy-atom-degenerate cases, not zero all-atom inertia. Transfer limit: the proxy ignores hydrogen mass distribution and adsorbate symmetry number, both of which affect true rotational entropy loss.",
      "physical_interpretation": "PMI3 is native in angstrom^2*amu; q_PMI3 is dimensionless so the square root is dimensionless. Predeclared partial-derivative direction: increasing sqrt(q_PMI3) is associated with increasing entropy loss and decreasing s_ads/s_gas. No q-unity value is a physical threshold.",
      "boundary_behavior": "At PMI3 = 0 (54 legitimate rows, single-heavy-atom proxies) the descriptor is exactly 0, finite, interpreted as the minimal extent proxy, not zero physical inertia; no imputation and no epsilon added. All 2361 rows finite over PMI3 in [0, 2414.631462].",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI3"
      ],
      "quantity_roles": {
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
      "training_spearman": 0.4086623414827737,
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
    "full_index_rows_in_task_scope": 6004,
    "pending_source_review": [
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9a3907e626bcdef0bc5bb0cb",
        "paper_id": "doi:10.1002/chem.201705627",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:b86d2d3284fbbe6696210c35",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd75db1400cf2ce6171ef0f6",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:022ab9eebdc42323bbc9006a",
        "paper_id": "doi:10.1039/d5tb00256g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:45c6c30e39c58cf298acb495",
        "paper_id": "pmc:pmc8113345",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:56e76b113baba858d09e9a1f",
        "paper_id": "doi:10.1063/1.4706520",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:6e3b310eb7c21b4c7481c2e9",
        "paper_id": "doi:10.1039/d0cp03871g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c3607df07f87ae637dfc8075",
        "paper_id": "doi:10.1021/la104245c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:46f247733ebb113afc9a8a26",
        "paper_id": "doi:10.1021/jp050434m",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:4a04fd9ec370a22894c63812",
        "paper_id": "doi:10.1021/acs.langmuir.2c01491",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:7bec0989f12cc18693a97a3f",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:c515aa77b0e6afe8275e4595",
        "paper_id": "doi:10.1039/d5cs00613a",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d7f5dcb78a7807132114232c",
        "paper_id": "doi:10.1021/jp808588n",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e1b683dc5917739326965133",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f778ee929c947fcc9e316c34",
        "paper_id": "pmc:pmc12559319",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:06a26a29dca2516a90c93ace",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:08b9bc71084bd99725ff4b87",
        "paper_id": "pmc:pmc10476167",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:166106b9d0f41731d2d72c4f",
        "paper_id": "doi:10.1039/c8cp01615a",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the product of adsorbate van der Waals volume and squared out-of-plane thickness (PBF, mean heavy-atom distance from the best-fit plane). At fixed volume, thicker (less planar) molecules fit fewer stable orientations against channel walls and within cavity sites, so the orientational/configurational entropy penalty at the adsorption site grows with q_Vol * PBF**2; entropy loss is monotonically associated with this descriptor. q_Vol * PBF**2 For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the ratio of the adsorbate's longest heavy-atom extension (GeDi, largest interatomic distance) to the largest included sphere along the free-sphere path (lsd_p, Zeo++ Dif). When molecular extension approaches the corridor's included diameter, translational passage requires alignment and steering through the pore network, reducing the accessible configuration space sampled at adsorption sites; entropy loss is monotonically associated with q_GeDi / lsd_p. q_GeDi / lsd_p For rigid pure-silica frameworks at infinite dilution, adsorbed-phase entropy loss increases with the square root of the normalized third principal moment of inertia of the adsorbate's heavy-atom skeleton (PMI3). A larger largest heavy-atom moment proxies a more extended mass distribution, which experiences more orientational constraints inside cavities and channels, freezing out more rotational/configuration coordinates; entropy loss is monotonically associated with sqrt(q_PMI3). sqrt(q_PMI3)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:e98dff054a73e56b28f6bdf3",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:01d0cb8bf43d75bbc448e004"
    ],
    "items": 10,
    "lexical_tokens": 4756,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [
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
