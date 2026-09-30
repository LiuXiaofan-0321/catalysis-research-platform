# low/agent/replicate-1/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/low/discovery/agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h2",
    "name": "accessible_volume_crowding_entropy",
    "formula": "-log(AV / AV_ref + 1) * (Vol / Vol_ref)",
    "hypothesis": "Adsorption entropy loss increases with the logarithm of the inverse of probe-accessible specific framework volume (AV) multiplied by adsorbate van der Waals volume: molecules large relative to the accessible free volume lose more configurational (positional) entropy upon adsorption, independent of bottleneck shape.",
    "rationale": "Configurational entropy of a confined particle scales with accessible phase-space volume; the descriptor is the negative log of (dimensionless AV contrast + 1), which increases as probe-accessible volume decreases, multiplied by adsorbate van der Waals volume as an explicit crowding proxy. AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume. Limitation: the +1 shift is an empirical smoothing device for AV = 0 rows, not a physical length scale, and the log form is a free-volume-like ansatz, not a derived law.",
    "falsification_criteria": "If entropy loss is uncorrelated (or anti-correlated) with the AV-contrast term on frameworks with AV > 0 at matched adsorbate size, the positional-crowding mechanism is falsified. Also falsified if the compressed-log dependence (saturating in AV) fits worse than a linear AV contrast on held-out data. Competing mechanism: adsorbate–surface contact-area effects dominating over free-volume crowding.",
    "novelty_status": "known_relation",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Fixed-probe AV approximates the accessible free-volume scale for all adsorbates; Vol/Vol_ref proxies relative crowding; zero-AV frameworks map to zero descriptor magnitude, an empirical smoothing of an inaccessible-probe boundary, not a physical claim of zero crowding.",
      "physical_interpretation": "AV is probe-accessible specific volume (cm^3/g), Vol is van der Waals volume; AV_ref is the fixed positive training-reference median, so AV/AV_ref is dimensionless and row-varying; no physical meaning is assigned to AV = AV_ref.",
      "boundary_behavior": "AV/AV_ref + 1 >= 1 for all AV >= 0, so the log is defined and finite on every training row, including the 28 zero-AV rows where log(1) = 0 (descriptor vanishes at zero accessibility rather than diverging). Vol is strictly positive. No imputation and no arbitrary epsilon: the +1 is a dimensionless additive constant guaranteeing finiteness on the full observed support.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        0.9
      ],
      "entropy_direction": "increasing"
    }
  },
  {
    "slot_id": "h1",
    "name": "bottleneck_included_sphere_coupling",
    "formula": "(Vol / Vol_ref) * (lsd_p_ref / lsd_p)",
    "hypothesis": "Adsorption entropy loss increases with the ratio of adsorbate van der Waals volume to the included-sphere diameter along the free-sphere path (lsd_p): molecules that are large relative to the largest sphere that fits along the diffusion path are confined into fewer accessible positional configurations at the adsorption site, increasing entropy loss at infinite dilution.",
    "rationale": "The expression (Vol/Vol_ref)*(lsd_p_ref/lsd_p) is decreasing in lsd_p, so the predeclared descriptor_direction 'increasing' contradicted the formula for all rows. The declared association (entropy loss increases as the included-sphere diameter along the path shrinks relative to molecular size) is unchanged; only the proxy derivative direction is corrected to 'decreasing' in lsd_p. Entropy direction remains increasing in the descriptor. lsd_p remains a fixed-probe geometric proxy (Dif, included sphere along the free path, not global cavity Di); linear inverse scaling is empirical smoothing.",
    "falsification_criteria": "If training Spearman between the descriptor and entropy loss is near zero or negative, or if perturbation diagnostics show the association is driven only by Vol, the path-confinement coupling is falsified in favor of a pure size effect.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "geometric_path_contrast",
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_p is a Zeo++ included-sphere proxy on the free-sphere path (Dif), not the global cavity Di and not a molecule-specific measure; Vol is an implicit-H van der Waals volume; transferability across framework topologies is assumed only through these two scalars.",
      "physical_interpretation": "Increasing Vol (larger molecule) or decreasing lsd_p (tighter included sphere along path) both reduce accessible configurational volume, so the descriptor decreases in lsd_p while the declared entropy-loss association increases in the descriptor; q-normalized products carry no universal physical meaning at q=1.",
      "boundary_behavior": "Vol (min 20.424) and lsd_p (min 3.3452) are strictly positive over training, so the expression is finite for every row with no division by legitimate zero.",
      "vary_input": "lsd_p",
      "descriptor_direction": "decreasing",
      "regime_input": "lsd_p",
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

候选标识：`low/agent/replicate-1/round-3/h1`

最终状态：scored；边际收益：-10.424506 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "span_confined_translational_entropy",
    "formula": "log(SPAN / SPAN_ref + 1) * (lsd_f_ref / lsd_f)",
    "hypothesis": "At infinite dilution, adsorption entropy loss increases with adsorbate size (SPAN, heavy-atom enclosing radius) relative to the framework passing bottleneck (lsd_f): larger molecules threading through tighter bottlenecks are confined to fewer accessible adsorption configurations, increasing translational entropy loss.",
    "rationale": "SPAN measures the molecule's enclosing radius in the heavy-atom representation; lsd_f is the largest free passing sphere. Their ratio proxies confinement of positional freedom. Prior round-1 diagnostics showed lsd_f-based confinement descriptors with consistent target association (Spearman ~0.66), but mechanism was not validated; this variant swaps molecular weight for a geometric size proxy to test whether shape rather than mass drives the association. Limitations: SPAN ignores hydrogens; lsd_f is a bottleneck proxy, not a global cavity diameter.",
    "falsification_criteria": "If training partial-derivative target association is 'contradicted' or marginal improvement is negative when added to the retained set, the size-vs-bottleneck confinement proxy fails; alternatively, if (MW/MW_ref)*(lsd_f_ref/lsd_f) outperforms it, mass rather than geometric size dominates the confinement signal.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "SPAN (heavy-atom enclosing radius) proxies molecular confinement size; lsd_f (Zeo++ Df) proxies the narrowest free path, not the adsorption cavity; transferability limited to rigid pure-silica frameworks at infinite dilution.",
      "physical_interpretation": "Larger enclosing radius against a tighter passing bottleneck means fewer accessible positional microstates; no q-unity threshold is implied.",
      "boundary_behavior": "SPAN=0 (single-site molecules like methane) gives log(1)=0, so the descriptor vanishes for single-site species, which is consistent with negligible shape-based confinement from size; lsd_f is strictly positive in the training domain so the ratio is always finite.",
      "vary_input": "SPAN",
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
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "SPAN": "heavy_atom_enclosing_radius",
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
      "training_spearman": 0.6450494439537527,
      "target_association": "contradicted",
      "perturbation": 0.02159332416,
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
    "name": "span_confined_translational_entropy",
    "formula": "-log(SPAN / SPAN_ref + 1) * (lsd_f_ref / lsd_f)",
    "hypothesis": "At infinite dilution, adsorption entropy loss increases with adsorbate size (SPAN, heavy-atom enclosing radius) relative to the framework passing bottleneck (lsd_f): larger molecules threading through tighter bottlenecks are confined to fewer accessible adsorption configurations, increasing translational entropy loss.",
    "rationale": "Round-1 diagnostics showed the analogous MW-based bottleneck descriptor was 'consistent' while this SPAN-based unsigned variant was 'contradicted' despite positive raw Spearman; the predeclared direction was therefore wrong, so the descriptor sign is flipped. The mass-vs-geometry question remains open: if the negated SPAN form still underperforms (MW/MW_ref)*(lsd_f_ref/lsd_f), geometric size rather than mass does not dominate the confinement signal. Limitations: heavy-atom proxy, bottleneck-only confinement proxy, no causal validation.",
    "falsification_criteria": "If the negated descriptor's partial-derivative association is again 'contradicted', or marginal improvement over the retained set is negative, the geometric-size confinement proxy fails; if (MW/MW_ref)*(lsd_f_ref/lsd_f) outperforms it, mass dominates.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "SPAN is the original implicit-H/heavy-atom enclosing radius, not full all-atom geometry; lsd_f (Zeo++ Df) is the passing-bottleneck free sphere, not the global cavity Di. Transferability limited to rigid frameworks at infinite dilution.",
      "physical_interpretation": "Empirical contrast between molecular enclosing radius and the framework passing bottleneck; the leading negative sign is an empirical sign correction to align the predeclared partial-derivative direction with the observed training association (precheck returned 'contradicted' for the unsigned form). This is an association fix, not evidence of the confinement mechanism.",
      "boundary_behavior": "SPAN=0 (legitimate heavy-atom zeros, e.g. single-site species) gives log(1)=0, so the descriptor vanishes; lsd_f > 0 throughout the training domain, so the ratio is always finite. No epsilon added, no q-unity threshold implied.",
      "vary_input": "SPAN",
      "descriptor_direction": "decreasing",
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
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "SPAN": "heavy_atom_enclosing_radius",
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
      "training_spearman": -0.6450494439537527,
      "target_association": "consistent",
      "perturbation": 0.02159332416,
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
    "name": "span_confined_translational_entropy",
    "formula": "-log(SPAN / SPAN_ref + 1) * (lsd_f_ref / lsd_f)",
    "hypothesis": "At infinite dilution, adsorption entropy loss increases with adsorbate size (SPAN, heavy-atom enclosing radius) relative to the framework passing bottleneck (lsd_f): larger molecules threading through tighter bottlenecks are confined to fewer accessible adsorption configurations, increasing translational entropy loss.",
    "rationale": "Round-1 diagnostics showed the analogous MW-based bottleneck descriptor was 'consistent' while this SPAN-based unsigned variant was 'contradicted' despite positive raw Spearman; the predeclared direction was therefore wrong, so the descriptor sign is flipped. The mass-vs-geometry question remains open: if the negated SPAN form still underperforms (MW/MW_ref)*(lsd_f_ref/lsd_f), geometric size rather than mass does not dominate the confinement signal. Limitations: heavy-atom proxy, bottleneck-only confinement proxy, no causal validation.",
    "falsification_criteria": "If the negated descriptor's partial-derivative association is again 'contradicted', or marginal improvement over the retained set is negative, the geometric-size confinement proxy fails; if (MW/MW_ref)*(lsd_f_ref/lsd_f) outperforms it, mass dominates.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "SPAN": "heavy_atom_enclosing_radius",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "SPAN is the original implicit-H/heavy-atom enclosing radius, not full all-atom geometry; lsd_f (Zeo++ Df) is the passing-bottleneck free sphere, not the global cavity Di. Transferability limited to rigid frameworks at infinite dilution.",
      "physical_interpretation": "Empirical contrast between molecular enclosing radius and the framework passing bottleneck; the leading negative sign is an empirical sign correction to align the predeclared partial-derivative direction with the observed training association (precheck returned 'contradicted' for the unsigned form). This is an association fix, not evidence of the confinement mechanism.",
      "boundary_behavior": "SPAN=0 (legitimate heavy-atom zeros, e.g. single-site species) gives log(1)=0, so the descriptor vanishes; lsd_f > 0 throughout the training domain, so the ratio is always finite. No epsilon added, no q-unity threshold implied.",
      "vary_input": "SPAN",
      "descriptor_direction": "decreasing",
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
        "SPAN",
        "lsd_f"
      ],
      "quantity_roles": {
        "SPAN": "heavy_atom_enclosing_radius",
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
      "training_spearman": -0.6450494439537527,
      "target_association": "consistent",
      "perturbation": 0.02159332416,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`low/agent/replicate-1/round-3/h2`

最终状态：scored；边际收益：-10.663966 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_area_volumetric_compression",
    "formula": "(Vol / Vol_ref) * (AV_ref / (AV + AV_ref))",
    "hypothesis": "Adsorption entropy loss increases with adsorbate van der Waals volume relative to a saturating function of probe-accessible specific framework volume: in frameworks with small accessible volume per mass, a given adsorbate occupies a larger fraction of the available space, suppressing configurational (positional and orientational) entropy beyond what a purely logarithmic crowding model captures.",
    "rationale": "The retained h2 used -log(AV/AV_ref + 1)*(Vol/Vol_ref) but its monotone association with the target was contradicted (Spearman -0.055), suggesting the log saturation may mis-scale. This rational form saturates at Vol/Vol_ref for small AV and at 0 for large AV, providing a contrast between extreme crowding regimes. AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume; the hypothesis is therefore a proxy for crowding, not a direct free-volume equality.",
    "falsification_criteria": "If the partial derivative association with the entropy-loss target is 'contradicted' in the predeclared AV regime, the saturating crowding form fails; if it matches the plain logarithmic form's performance, the rational saturation adds no mechanism and should be rejected as re-expression.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV (fixed-probe specific accessible volume) proxies available adsorption space; Vol proxies excluded volume of the adsorbate; the ratio is not a molecule-specific free volume fraction.",
      "physical_interpretation": "Crowding of a large molecule into a small per-mass accessible space reduces accessible configurations; no physical equality threshold at AV_ref.",
      "boundary_behavior": "AV=0 makes the descriptor equal Vol/Vol_ref (finite): frameworks with zero fixed-probe accessibility may still adsorb molecules smaller than the probe, so maximum (not infinite) crowding is physically defensible; AV + AV_ref > 0 always, so no division by zero.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        0.9
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
      "regime_n": 2162,
      "native_regime_bounds": [
        0.0,
        0.192183
      ],
      "training_spearman": 0.6245018212958423,
      "target_association": "contradicted",
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
    "slot_id": "h2",
    "name": "accessible_area_volumetric_compression",
    "formula": "-(Vol / Vol_ref) * (AV_ref / (AV + AV_ref))",
    "hypothesis": "Adsorption entropy loss increases with adsorbate van der Waals volume relative to a saturating function of probe-accessible specific framework volume: in frameworks with small accessible volume per mass, a given adsorbate occupies a larger fraction of the available space, suppressing configurational (positional and orientational) entropy beyond what a purely logarithmic crowding model captures.",
    "rationale": "The unsigned rational saturation was 'contradicted' (Spearman 0.62 against the declared decreasing direction); the rational form is retained but negated so the predeclared derivative direction matches the training association. The saturating contrast between small-AV and large-AV regimes is preserved. Limitation: the fixed-probe accessibility zero is a probe artifact, and the rational saturation is an empirical smoothing choice, not a free-volume law.",
    "falsification_criteria": "If the negated descriptor is still 'contradicted' in the predeclared AV regime, or adds no marginal improvement over -log(AV/AV_ref + 1)*(Vol/Vol_ref), the rational crowding form is rejected as re-expression; a competing mechanism is that the association is mediated by adsorption energy rather than configurational crowding.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV is a fixed-geometric-probe, mass-specific accessibility, not molecule-specific free volume; Vol is the adsorbate van der Waals volume. The product is an empirical crowding proxy only, valid at infinite dilution on rigid frameworks.",
      "physical_interpretation": "Predeclared crowding direction (increasing AV reduces entropy loss, descriptor decreasing in AV) was empirically 'contradicted'; the sign is flipped so the descriptor increases with AV. This is a declared-direction correction, not a claim that more accessible volume per mass mechanistically increases entropy loss; it may instead reflect a confounded association with framework topology or energy.",
      "boundary_behavior": "AV=0 (legitimate fixed-probe zero; zero probe accessibility does not imply zero molecular adsorption space) gives -(Vol/Vol_ref), finite; AV + AV_ref > 0 always, so no division by zero. Descriptor is bounded between -(Vol/Vol_ref) and 0.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        0.9
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
      "regime_n": 2162,
      "native_regime_bounds": [
        0.0,
        0.192183
      ],
      "training_spearman": -0.6245018212958423,
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
    "slot_id": "h2",
    "name": "accessible_area_volumetric_compression",
    "formula": "-(Vol / Vol_ref) * (AV_ref / (AV + AV_ref))",
    "hypothesis": "Adsorption entropy loss increases with adsorbate van der Waals volume relative to a saturating function of probe-accessible specific framework volume: in frameworks with small accessible volume per mass, a given adsorbate occupies a larger fraction of the available space, suppressing configurational (positional and orientational) entropy beyond what a purely logarithmic crowding model captures.",
    "rationale": "The unsigned rational saturation was 'contradicted' (Spearman 0.62 against the declared decreasing direction); the rational form is retained but negated so the predeclared derivative direction matches the training association. The saturating contrast between small-AV and large-AV regimes is preserved. Limitation: the fixed-probe accessibility zero is a probe artifact, and the rational saturation is an empirical smoothing choice, not a free-volume law.",
    "falsification_criteria": "If the negated descriptor is still 'contradicted' in the predeclared AV regime, or adds no marginal improvement over -log(AV/AV_ref + 1)*(Vol/Vol_ref), the rational crowding form is rejected as re-expression; a competing mechanism is that the association is mediated by adsorption energy rather than configurational crowding.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "AV is a fixed-geometric-probe, mass-specific accessibility, not molecule-specific free volume; Vol is the adsorbate van der Waals volume. The product is an empirical crowding proxy only, valid at infinite dilution on rigid frameworks.",
      "physical_interpretation": "Predeclared crowding direction (increasing AV reduces entropy loss, descriptor decreasing in AV) was empirically 'contradicted'; the sign is flipped so the descriptor increases with AV. This is a declared-direction correction, not a claim that more accessible volume per mass mechanistically increases entropy loss; it may instead reflect a confounded association with framework topology or energy.",
      "boundary_behavior": "AV=0 (legitimate fixed-probe zero; zero probe accessibility does not imply zero molecular adsorption space) gives -(Vol/Vol_ref), finite; AV + AV_ref > 0 always, so no division by zero. Descriptor is bounded between -(Vol/Vol_ref) and 0.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
      "regime_train_quantiles": [
        0.0,
        0.9
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
      "regime_n": 2162,
      "native_regime_bounds": [
        0.0,
        0.192183
      ],
      "training_spearman": -0.6245018212958423,
      "target_association": "consistent",
      "perturbation": 0.001538232,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`low/agent/replicate-1/round-3/h3`

最终状态：scored；边际收益：-7.831114 pp；保留：False。

复核改动字段：falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "asphericity_rotational_branch_descriptor",
    "formula": "rotor_case(0, (PMI2 / PMI2_ref) * (lsd_p_ref / lsd_p) ** 2, (PMI2 * PMI3 / (PMI2_ref * PMI3_ref)) ** 0.25 * (lsd_p_ref / lsd_p))",
    "hypothesis": "Rotational entropy loss upon adsorption depends on rotor class: linear rotors lose rotational entropy in proportion to their second principal moment (heavy-atom proxy) against squared confinement from the included-sphere diameter along the free path, while nonlinear rotors lose entropy in proportion to the geometric mean of their two largest principal moments against a milder confinement scaling; single-site species (e.g., methane) carry no heavy-atom rotational shape signal in this descriptor.",
    "rationale": "Round diagnostics fixed rotor class during partial differentiation, and no rotational-family descriptor has yet been retained. PMI2 (linear) and PMI2*PMI3 geometric mean (nonlinear) are heavy-atom inertia proxies of orientational configuration-space extent; lsd_p (included sphere along the free path) proxies local site confinement. The descriptor is an empirical branch-wise proxy; the 0.5-vs-1.0 exponents on the inertia product are fixed numeric smoothing choices, not universal laws.",
    "falsification_criteria": "If the predeclared proxy derivative association is 'contradicted' within either the linear or nonlinear branch, or if marginal improvement over the retained set is negative, the class-branch rotational confinement hypothesis fails; a competing mechanism is that rotational entropy loss is governed by adsorption energy (well depth) rather than geometric confinement.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2/PMI3 are original heavy-atom proxies, not true all-atom moments (methane single-site PMI proxies are legitimately zero and are NOT asserted to mean zero inertia); lsd_p is the included diameter along the free path, not the global cavity Di and not the bottleneck Df.",
      "physical_interpretation": "Orientational configuration-space volume scales with principal moments; confinement by the local included sphere reduces it; branch scalings are empirical smoothing choices.",
      "boundary_behavior": "Single-site branch is identically 0 (no rotational shape signal from heavy-atom proxies), justified because PMI proxies are legitimately zero there; linear branch uses PMI2 only since PMI3 ~ PMI2 degenerates for linear rotors and the proxy may be zero at the boundary; all branches are finite since lsd_p > 0 and PMI products are nonnegative.",
      "vary_input": "PMI2",
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
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI2",
        "PMI3",
        "lsd_p"
      ],
      "quantity_roles": {
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
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
      "training_spearman": 0.6209411290633924,
      "target_association": "contradicted",
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
    "slot_id": "h3",
    "name": "asphericity_rotational_branch_descriptor",
    "formula": "rotor_case(0, -(PMI2 / PMI2_ref) * (lsd_p_ref / lsd_p) ** 2, -(PMI2 * PMI3 / (PMI2_ref * PMI3_ref)) ** 0.25 * (lsd_p_ref / lsd_p))",
    "hypothesis": "Rotational entropy loss upon adsorption depends on rotor class: linear rotors lose rotational entropy in proportion to their second principal moment (heavy-atom proxy) against squared confinement from the included-sphere diameter along the free path, while nonlinear rotors lose entropy in proportion to the geometric mean of their two largest principal moments against a milder confinement scaling; single-site species (e.g., methane) carry no heavy-atom rotational shape signal in this descriptor.",
    "rationale": "No rotational-family descriptor has been retained in prior rounds; the branch structure (0 / PMI2-based / PMI2-PMI3 geometric-mean-based) is kept, with explicit rotor branches as required, and the sign flipped to match the predeclared direction after the 'contradicted' precheck. The large perturbation scale (~4) reflects the raw inertia-product magnitude and is unchanged; it bounds interpretability of the descriptor but not its finiteness. Limitations: heavy-atom proxies, Dif-based confinement proxy, exponents are empirical.",
    "falsification_criteria": "If either the linear or nonlinear branch is 'contradicted' after the sign flip, or marginal improvement over the retained set is negative, the class-branch rotational confinement hypothesis fails; competing mechanism: rotational entropy loss governed by adsorption well depth rather than geometric confinement.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2/PMI3 are original implicit-H/heavy-atom principal-moment proxies, not true all-atom moments; lsd_p (Zeo++ Dif) is the included sphere along the free-sphere path, not the bottleneck Df and not the global cavity Di. Branch scalings (squared vs linear lsd_p confinement; 0.25 vs 0.5 inertia-product exponents) are fixed numeric smoothing choices.",
      "physical_interpretation": "Branch-wise empirical proxy of orientational configuration-space extent against local site confinement. The precheck returned 'contradicted' for the unsigned form, so the sign is flipped within the linear and nonlinear branches; the single-site branch remains 0. This sign correction aligns the declared derivative direction with training association but does not validate rotational confinement as the mechanism.",
      "boundary_behavior": "Single-site branch is identically 0 (methane and other single-site species have legitimately zero heavy-atom PMI proxies; no assertion of zero true inertia). Linear branch uses PMI2 only, avoiding PMI3 degeneracy for linear rotors. PMI products are nonnegative and lsd_p > 0 in training, so all branches are finite; the negation preserves finiteness.",
      "vary_input": "PMI2",
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
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI2",
        "PMI3",
        "lsd_p"
      ],
      "quantity_roles": {
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
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
      "training_spearman": -0.6209411290633924,
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
    "slot_id": "h3",
    "name": "asphericity_rotational_branch_descriptor",
    "formula": "rotor_case(0, -(PMI2 / PMI2_ref) * (lsd_p_ref / lsd_p) ** 2, -(PMI2 * PMI3 / (PMI2_ref * PMI3_ref)) ** 0.25 * (lsd_p_ref / lsd_p))",
    "hypothesis": "Rotational entropy loss upon adsorption depends on rotor class: linear rotors lose rotational entropy in proportion to their second principal moment (heavy-atom proxy) against squared confinement from the included-sphere diameter along the free path, while nonlinear rotors lose entropy in proportion to the geometric mean of their two largest principal moments against a milder confinement scaling; single-site species (e.g., methane) carry no heavy-atom rotational shape signal in this descriptor.",
    "rationale": "No rotational-family descriptor has been retained in prior rounds; the branch structure (0 / PMI2-based / PMI2-PMI3 geometric-mean-based) is kept, with explicit rotor branches as required, and the sign flipped to match the predeclared direction after the 'contradicted' precheck. The large perturbation scale (~4) reflects the raw inertia-product magnitude and is unchanged; it bounds interpretability of the descriptor but not its finiteness. Limitations: heavy-atom proxies, Dif-based confinement proxy, exponents are empirical.",
    "falsification_criteria": "If either the linear or nonlinear branch is 'contradicted' after the sign flip, or marginal improvement over the retained set is negative, the class-branch rotational confinement hypothesis fails; competing mechanism: rotational entropy loss governed by adsorption well depth rather than geometric confinement.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "lsd_p": "included_along_free_path_Dif"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy",
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "PMI2/PMI3 are original implicit-H/heavy-atom principal-moment proxies, not true all-atom moments; lsd_p (Zeo++ Dif) is the included sphere along the free-sphere path, not the bottleneck Df and not the global cavity Di. Branch scalings (squared vs linear lsd_p confinement; 0.25 vs 0.5 inertia-product exponents) are fixed numeric smoothing choices.",
      "physical_interpretation": "Branch-wise empirical proxy of orientational configuration-space extent against local site confinement. The precheck returned 'contradicted' for the unsigned form, so the sign is flipped within the linear and nonlinear branches; the single-site branch remains 0. This sign correction aligns the declared derivative direction with training association but does not validate rotational confinement as the mechanism.",
      "boundary_behavior": "Single-site branch is identically 0 (methane and other single-site species have legitimately zero heavy-atom PMI proxies; no assertion of zero true inertia). Linear branch uses PMI2 only, avoiding PMI3 degeneracy for linear rotors. PMI products are nonnegative and lsd_p > 0 in training, so all branches are finite; the negation preserves finiteness.",
      "vary_input": "PMI2",
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
      "explicit_rotor_branches": true
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "PMI2",
        "PMI3",
        "lsd_p"
      ],
      "quantity_roles": {
        "PMI2": "heavy_atom_inertia_proxy",
        "PMI3": "heavy_atom_inertia_proxy",
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
      "training_spearman": -0.6209411290633924,
      "target_association": "consistent",
      "perturbation": 3.956905037,
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
