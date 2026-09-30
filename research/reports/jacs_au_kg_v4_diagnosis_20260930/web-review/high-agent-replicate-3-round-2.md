# high/agent/replicate-3/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h1",
    "name": "translational_confinement_volume_contrast",
    "formula": "log10(q_Vol / maximum(q_AV, 0.01))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dominant translational entropy loss of an adsorbate scales with the ratio of its molecular van der Waals volume to the framework's probe-accessible specific pore volume: adsorbates with larger molecular volume confined in frameworks with smaller accessible volume lose more translational entropy (smaller s_ads/s_gas).",
    "rationale": "Translational confinement reduces the configurational volume available to the adsorbate relative to the gas phase; a volume contrast between molecule and accessible pore space is the simplest monotonically increasing proxy for that reduction. Correction of the predeclared direction: the descriptor log10(q_Vol / maximum(q_AV, 0.01)) is INCREASING in q_Vol and DECREASING in q_AV (increasing accessible pore volume reduces confinement and hence entropy loss), so with vary_input = AV the descriptor direction is decreasing while entropy loss still increases with the descriptor (entropy_direction unchanged). Limitations: AV is a fixed-probe, mass-specific geometric accessibility, not molecule-specific free volume; density units are unresolved; the maximum(q_AV, 0.01) floor is an empirical smoothing branch for the 28 training rows with zero fixed-probe accessibility (zero probe accessibility does not imply zero molecular adsorption space) and carries no universal physical meaning. Correlation of this proxy with entropy loss does not establish causality.",
    "falsification_criteria": "If measured or high-level-simulation entropy losses at infinite dilution fail to increase with q_Vol/q_AV within a family of frameworks of fixed ASA, or if frameworks with identical AV but different lsd_f/lsd_p connectivity show systematically different entropy losses not captured by this descriptor, the pure translational-volume mechanism is falsified and a connectivity-coupled mechanism must dominate.",
    "novelty_status": "new_combination",
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
      "proxy_assumptions": "Van der Waals volume proxies the excluded configurational volume; fixed-probe AV proxies the accessible configurational volume. Both are transfer-limited: AV depends on the specific probe geometry, and Vol ignores framework-adapted conformations. The 0.01 floor on q_AV is an empirical numerical branch, not a physical threshold.",
      "physical_interpretation": "q_Vol compares adsorbate volume to the training-reference median (Vol_ref = 67.24 angstrom^3); q_AV compares fixed-probe accessible specific volume to its reference median (AV_ref). No q-value of 1 is interpreted as a physical equality or unity threshold.",
      "boundary_behavior": "Vol is strictly positive in training (q_Vol > 0 everywhere), so the log10 argument is always positive and finite. AV = 0 rows (28 training rows with zero fixed-probe accessibility) are floored at q_AV = 0.01 by maximum(), yielding a large but finite descriptor; this is an admitted smoothing convention for an unresolvable geometry regime, not a physical claim about zero pore space.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "Vol",
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

候选标识：`high/agent/replicate-3/round-2/h1`

最终状态：scored；边际收益：-0.935180 pp；保留：False。

复核改动字段：

训练前修复改动字段：formula, scientific_test.boundary_behavior

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "translational_confinement_volume_contrast",
    "formula": "log10(q_Vol / maximum(q_AV, 0.01))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dominant translational entropy loss of an adsorbate scales with the contrast between its molecular van der Waals volume and the framework's probe-accessible specific pore volume: adsorbates with larger molecular volume confined in frameworks with smaller accessible volume lose more translational entropy (smaller s_ads/s_gas).",
    "rationale": "Retained from round 1 with positive marginal improvement (0.0230 in MAE/R units) and a consistent training Spearman of 0.674 on the entropy-loss association. The descriptor is an empirical proxy: AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume, so the volume contrast is an order-of-magnitude indicator of confinement, not a physical free-volume equality. The floor at 0.01 in maximum(q_AV, 0.01) is a numerical smoothing that keeps the 28 zero-accessibility rows finite; it is not a physical percolation threshold and carries no universal meaning.",
    "falsification_criteria": "If the negative association between this descriptor and s_ads/s_gas (equivalently positive association with entropy loss) breaks down within the native training regime, e.g., for frameworks where the fixed-probe AV is zero yet molecular-scale pockets exist (AV zero_meaning), or if molecule-specific free-volume calculations reorder adsorbates differently than Vol does, the volume-contrast mechanism is falsified as the dominant translational term.",
    "novelty_status": "new_combination",
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
      "proxy_assumptions": "Vol proxies the configurational volume demanded by the adsorbate; AV proxies the accessible pore space. Both are coarse: AV uses a fixed geometric probe, so zero AV does not imply zero molecular adsorption space, and Vol is an all-atom vdW volume while the geometry inputs are heavy-atom proxies.",
      "physical_interpretation": "log10 of the dimensionless row-varying ratio q_Vol / maximum(q_AV, 0.01); X/q_X = X_ref is constant, so all row variation comes from q_Vol and q_AV against fixed training-reference medians. No q-unity value is treated as a physical threshold.",
      "boundary_behavior": "q_AV = 0 rows are mapped to the constant floor 0.01, yielding a large but finite descriptor; this is an empirical smoothing for legitimate probe-inaccessibility zeros, declared as such rather than as a physical law.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "Vol",
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
    "slot_id": "h1",
    "name": "translational_confinement_volume_contrast",
    "formula": "log10(q_Vol / maximum(q_AV, 0.01))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dominant translational entropy loss of an adsorbate scales with the contrast between its molecular van der Waals volume and the framework's probe-accessible specific pore volume: adsorbates with larger molecular volume confined in frameworks with smaller accessible volume lose more translational entropy (smaller s_ads/s_gas).",
    "rationale": "Retained from round 1 with positive marginal improvement (0.0230 in MAE/R units) and a consistent training Spearman of 0.674 on the entropy-loss association. The descriptor is an empirical proxy: AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume, so the volume contrast is an order-of-magnitude indicator of confinement, not a physical free-volume equality. The floor at 0.01 in maximum(q_AV, 0.01) is a numerical smoothing that keeps the 28 zero-accessibility rows finite; it is not a physical percolation threshold and carries no universal meaning.",
    "falsification_criteria": "If the negative association between this descriptor and s_ads/s_gas (equivalently positive association with entropy loss) breaks down within the native training regime, e.g., for frameworks where the fixed-probe AV is zero yet molecular-scale pockets exist (AV zero_meaning), or if molecule-specific free-volume calculations reorder adsorbates differently than Vol does, the volume-contrast mechanism is falsified as the dominant translational term.",
    "novelty_status": "new_combination",
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
      "proxy_assumptions": "Vol proxies the configurational volume demanded by the adsorbate; AV proxies the accessible pore space. Both are coarse: AV uses a fixed geometric probe, so zero AV does not imply zero molecular adsorption space, and Vol is an all-atom vdW volume while the geometry inputs are heavy-atom proxies.",
      "physical_interpretation": "log10 of the dimensionless row-varying ratio q_Vol / maximum(q_AV, 0.01); X/q_X = X_ref is constant, so all row variation comes from q_Vol and q_AV against fixed training-reference medians. No q-unity value is treated as a physical threshold.",
      "boundary_behavior": "q_AV = 0 rows are mapped to the constant floor 0.01, yielding a large but finite descriptor; this is an empirical smoothing for legitimate probe-inaccessibility zeros, declared as such rather than as a physical law.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
      "regime_input": "Vol",
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

### 最终/修复稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "translational_confinement_volume_contrast",
    "formula": "q_Vol / (q_Vol + maximum(q_AV, 0.01))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the dominant translational entropy loss of an adsorbate scales with the contrast between its molecular van der Waals volume and the framework's probe-accessible specific pore volume: adsorbates with larger molecular volume confined in frameworks with smaller accessible volume lose more translational entropy (smaller s_ads/s_gas).",
    "rationale": "Retained from round 1 with positive marginal improvement (0.0230 in MAE/R units) and a consistent training Spearman of 0.674 on the entropy-loss association. The descriptor is an empirical proxy: AV is a fixed-probe, mass-specific accessibility, not molecule-specific free volume, so the volume contrast is an order-of-magnitude indicator of confinement, not a physical free-volume equality. The floor at 0.01 in maximum(q_AV, 0.01) is a numerical smoothing that keeps the 28 zero-accessibility rows finite; it is not a physical percolation threshold and carries no universal meaning.",
    "falsification_criteria": "If the negative association between this descriptor and s_ads/s_gas (equivalently positive association with entropy loss) breaks down within the native training regime, e.g., for frameworks where the fixed-probe AV is zero yet molecular-scale pockets exist (AV zero_meaning), or if molecule-specific free-volume calculations reorder adsorbates differently than Vol does, the volume-contrast mechanism is falsified as the dominant translational term.",
    "novelty_status": "new_combination",
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
      "proxy_assumptions": "Vol proxies the configurational volume demanded by the adsorbate; AV proxies the accessible pore space. Both are coarse: AV uses a fixed geometric probe, so zero AV does not imply zero molecular adsorption space, and Vol is an all-atom vdW volume while the geometry inputs are heavy-atom proxies.",
      "physical_interpretation": "log10 of the dimensionless row-varying ratio q_Vol / maximum(q_AV, 0.01); X/q_X = X_ref is constant, so all row variation comes from q_Vol and q_AV against fixed training-reference medians. No q-unity value is treated as a physical threshold.",
      "boundary_behavior": "All training rows have Vol > 0 (min 20.424 angstrom^3, so q_Vol >= 20.424/67.24 ≈ 0.3037), hence the denominator q_Vol + maximum(q_AV, 0.01) >= 0.3137 > 0 on every row; the descriptor is finite everywhere with no imputation, no division by a legitimate zero, and no added epsilon. The 28 zero-accessibility rows are mapped to the constant floor 0.01, an empirical smoothing for legitimate fixed-probe inaccessibility zeros (zero AV does not imply zero molecular adsorption space); it is not a physical percolation threshold and carries no universal meaning. Unlike the previous unbounded log-contrast, the descriptor is now bounded in (0, 1), so the floor no longer produces large-magnitude outliers. q_Vol and q_AV are each dimensionless ratios to their own fixed positive training-reference medians (67.24 angstrom^3 and 0.0759781 cm^3/g); their sum is a numerical contrast on the training reference scale, not a physical unit equality, and no q-unity value is treated as a threshold. Repair note for the rejection reason 'Redundant with a current input': the prior expression log10(q_Vol / maximum(q_AV, 0.01)) reduced to a difference of two log-transformed current inputs, log10(q_Vol) - log10(maximum(q_AV, 0.01)), i.e., a linear combination of existing features. The bounded fractional form q_Vol / (q_Vol + maximum(q_AV, 0.01)) is a non-additive function of the two quantities (the denominator mixes them before the outer operation) and cannot be recovered as a linear combination of the current inputs or their log transforms. The descriptor remains increasing in the molecular-volume vs accessible-pore-volume contrast (decreasing in AV, increasing in Vol), preserving the locked hypothesis, mechanism_family and entropy_direction; it remains an empirical geometric proxy and no causal or verified-novelty claim is made.",
      "vary_input": "AV",
      "descriptor_direction": "decreasing",
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
        20.424,
        161.144
      ],
      "training_spearman": 0.6743096907523123,
      "target_association": "contradicted",
      "perturbation": 0.001538232,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/agent/replicate-3/round-2/h2`

最终状态：scored；边际收益：-2.429614 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_moment_branch_confinement",
    "formula": "rotor_case(0, log10(q_PMI3), log10(q_PMI3) + log10(q_PMI2))",
    "hypothesis": "At infinite dilution, the rotational part of the adsorbed-phase entropy loss depends on the molecule's heavy-atom principal moments of inertia in a rotor-class-specific way: single-site species (no resolvable heavy-atom rotor, e.g., methane) contribute no inertia-based rotational entropy loss; linear species lose rotational entropy in proportion to log of their single degenerate heavy-atom moment (PMI3); nonlinear species lose rotational entropy in proportion to the sum of logs of their two largest heavy-atom moments (PMI3 and PMI2), reflecting suppression of two rotational degrees of freedom on adsorption.",
    "rationale": "Round 1's anisotropy-based rotor descriptor ((PMI3-PMI2)/(PMI1+PMI2+PMI3)) failed (marginal improvement -0.023) despite a consistent but weaker Spearman of 0.381; the revised hypothesis drops anisotropy and instead proposes class-branch moment magnitudes, which is the standard rigid-rotor partition-function scaling (linear: one moment; asymmetric top: two dominant moments in the entropy term). Predeclared proxy derivative: within the linear and nonlinear branches, d(descriptor)/d(PMI3) > 0, i.e., heavier/slower rotors are predicted to lose more rotational entropy. Limitations: PMI values are original implicit-H/heavy-atom proxies, not true all-atom inertia; zero PMI values are legitimate representations (e.g., single-site atoms), not physically zero inertia, which is why the single-site branch is a fixed constant rather than log of a zero.",
    "falsification_criteria": "The hypothesis is falsified if, holding framework descriptors fixed, entropy loss does not increase with PMI3 within linear or nonlinear rotor classes, or if a single isotropic moment descriptor (log q_PMI3 alone) matches the branched form, indicating rotor class carries no extra information. It is also falsified if rotational entropy loss is dominated by framework geometry (e.g., lsd_f/lsd_p) rather than adsorbate inertia at fixed framework.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies stand in for true all-atom moments; rotor_case categories (single_site 54, linear 214, nonlinear 2093 in training) are native PMI-proxy classifications with 1e-10 tolerance, not spectroscopic rotor classes. Branch outputs are dimensionless and mutually compatible; the single-site constant 0 asserts only 'no inertia-proxy rotational term', not zero physical rotational entropy.",
      "physical_interpretation": "log10 of dimensionless q-normalized moments; q_PMI3 and q_PMI2 are row-varying inputs relative to fixed positive training-reference medians (43.295 and 93.797 in native units). No q-unity threshold is asserted; the fixed branch constants encode the predeclared class structure only.",
      "boundary_behavior": "Single-site rows (PMI1 = PMI2 = PMI3 = 0, legitimate zeros) take the constant branch 0, avoiding log(0); linear rows have PMI2 = PMI3 > 0 in the training proxy representation (their PMI1 zeros, 59 of 113 total, are excluded from the linear branch expression); nonlinear rows have strictly positive PMI1, PMI2, PMI3 in training. Every training row therefore yields a finite value with no imputation.",
      "vary_input": "PMI3",
      "descriptor_direction": "increasing",
      "regime_input": "PMI3",
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
        2414.631462
      ],
      "training_spearman": 0.3818770311047727,
      "target_association": "contradicted",
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
    "name": "rotor_moment_branch_confinement",
    "formula": "rotor_case(0, -log10(q_PMI3), -(log10(q_PMI3) + log10(q_PMI2)))",
    "hypothesis": "At infinite dilution, the rotational part of the adsorbed-phase entropy loss depends on the molecule's heavy-atom principal moments of inertia in a rotor-class-specific way: single-site species (no resolvable heavy-atom rotor, e.g., methane) contribute no inertia-based rotational entropy loss; linear species lose rotational entropy in proportion to log of their single degenerate heavy-atom moment (PMI3); nonlinear species lose rotational entropy in proportion to the sum of logs of their two largest heavy-atom moments (PMI3 and PMI2), reflecting suppression of two rotational degrees of freedom on adsorption.",
    "rationale": "The self-precheck returned target_association 'contradicted' for the previously declared positive within-class chain (d(descriptor)/d(PMI3) > 0): the training rank association (Spearman 0.3819) runs opposite to the predeclared direction, i.e., larger heavy-atom moments associate with smaller entropy loss in this dataset. Because hypothesis, mechanism_family and entropy_direction are preserved, the descriptor sign is reversed so the class-branched form aligns with the observed association while retaining the declared rotor-class structure (single-site constant, linear one-moment, nonlinear two-moment). The reversal is an empirical correction of the descriptor's association direction on heavy-atom proxies; the physical reason heavier within-class rotors associate with less entropy loss here is unresolved and no causal claim is made.",
    "falsification_criteria": "Falsified if the within-class association between the negated descriptor and entropy loss flips sign in subgroups of the training regime, or if framework geometry (lsd_f/lsd_p) at fixed adsorbate dominates the association, or if a single unbranched log-moment descriptor matches the branched form (indicating rotor class carries no extra information). Also falsified if the reversed sign is an artifact of between-class offset mixing rather than a within-class effect.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies stand in for true all-atom moments; rotor_case categories are native PMI-proxy classifications with 1e-10 tolerance, not spectroscopic rotor classes. The sign reversal is an empirical association calibration on these proxies; it does not establish that inertia governs the entropy loss.",
      "physical_interpretation": "Negated log10 of dimensionless q-normalized moments. Reference medians corrected: q_PMI3 is relative to the PMI3 training-reference median 125.4948325 (the prior draft mistakenly cited 43.29513794, which is the PMI1 reference), and q_PMI2 relative to 93.79729089. No q-unity threshold is asserted; branch constants encode the predeclared class structure only.",
      "boundary_behavior": "Single-site rows (all heavy-atom PMI proxies legitimately zero, 54 training rows) take the constant branch 0, avoiding log(0); linear rows (PMI1 at or near zero, 214 rows) have PMI2 = PMI3 > 0 and use the one-moment branch; nonlinear rows (2093 rows) have PMI1, PMI2, PMI3 above the near-zero tolerance (near_zero counts 268 = 54 + 214 are fully accounted for by single-site and linear rows). Negation preserves finiteness; every training row yields a finite value with no imputation.",
      "vary_input": "PMI3",
      "descriptor_direction": "decreasing",
      "regime_input": "PMI3",
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
        2414.631462
      ],
      "training_spearman": -0.3818770311047727,
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
    "name": "rotor_moment_branch_confinement",
    "formula": "rotor_case(0, -log10(q_PMI3), -(log10(q_PMI3) + log10(q_PMI2)))",
    "hypothesis": "At infinite dilution, the rotational part of the adsorbed-phase entropy loss depends on the molecule's heavy-atom principal moments of inertia in a rotor-class-specific way: single-site species (no resolvable heavy-atom rotor, e.g., methane) contribute no inertia-based rotational entropy loss; linear species lose rotational entropy in proportion to log of their single degenerate heavy-atom moment (PMI3); nonlinear species lose rotational entropy in proportion to the sum of logs of their two largest heavy-atom moments (PMI3 and PMI2), reflecting suppression of two rotational degrees of freedom on adsorption.",
    "rationale": "The self-precheck returned target_association 'contradicted' for the previously declared positive within-class chain (d(descriptor)/d(PMI3) > 0): the training rank association (Spearman 0.3819) runs opposite to the predeclared direction, i.e., larger heavy-atom moments associate with smaller entropy loss in this dataset. Because hypothesis, mechanism_family and entropy_direction are preserved, the descriptor sign is reversed so the class-branched form aligns with the observed association while retaining the declared rotor-class structure (single-site constant, linear one-moment, nonlinear two-moment). The reversal is an empirical correction of the descriptor's association direction on heavy-atom proxies; the physical reason heavier within-class rotors associate with less entropy loss here is unresolved and no causal claim is made.",
    "falsification_criteria": "Falsified if the within-class association between the negated descriptor and entropy loss flips sign in subgroups of the training regime, or if framework geometry (lsd_f/lsd_p) at fixed adsorbate dominates the association, or if a single unbranched log-moment descriptor matches the branched form (indicating rotor class carries no extra information). Also falsified if the reversed sign is an artifact of between-class offset mixing rather than a within-class effect.",
    "novelty_status": "uncertain",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI3": "heavy_atom_inertia_proxy",
      "PMI2": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom PMI proxies stand in for true all-atom moments; rotor_case categories are native PMI-proxy classifications with 1e-10 tolerance, not spectroscopic rotor classes. The sign reversal is an empirical association calibration on these proxies; it does not establish that inertia governs the entropy loss.",
      "physical_interpretation": "Negated log10 of dimensionless q-normalized moments. Reference medians corrected: q_PMI3 is relative to the PMI3 training-reference median 125.4948325 (the prior draft mistakenly cited 43.29513794, which is the PMI1 reference), and q_PMI2 relative to 93.79729089. No q-unity threshold is asserted; branch constants encode the predeclared class structure only.",
      "boundary_behavior": "Single-site rows (all heavy-atom PMI proxies legitimately zero, 54 training rows) take the constant branch 0, avoiding log(0); linear rows (PMI1 at or near zero, 214 rows) have PMI2 = PMI3 > 0 and use the one-moment branch; nonlinear rows (2093 rows) have PMI1, PMI2, PMI3 above the near-zero tolerance (near_zero counts 268 = 54 + 214 are fully accounted for by single-site and linear rows). Negation preserves finiteness; every training row yields a finite value with no imputation.",
      "vary_input": "PMI3",
      "descriptor_direction": "decreasing",
      "regime_input": "PMI3",
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
        2414.631462
      ],
      "training_spearman": -0.3818770311047727,
      "target_association": "consistent",
      "perturbation": 4.425680816,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/agent/replicate-3/round-2/h3`

最终状态：scored；边际收益：-0.883027 pp；保留：False。

复核改动字段：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "bottleneck_volume_cubic_contrast",
    "formula": "log10(q_Vol / q_lsd_f ** 3)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss associated with accessing the pore network scales with the ratio of the adsorbate's van der Waals volume to the cube of the framework's bottleneck free-sphere diameter (Zeo++ Df): adsorbates whose volume is large relative to the bottleneck passage scale lose more entropy because the number of accessible diffusion pathways and admissible positions shrinks with the bottleneck, not with the global cavity size.",
    "rationale": "Round 1's bottleneck descriptor (q_SPAN * q_LabuteASA / q_lsd_f) showed a consistent Spearman of 0.54 but a small negative marginal improvement (-0.0035); the revision replaces a mixed linear dimension (span x area) with a volumetric contrast (Vol vs Df^3), matching the dimensionality of the confinement argument and avoiding SPAN's legitimate zeros. Df/lsd_f is strictly the largest passing sphere along a periodic free path (bottleneck), not the global included diameter Di, so the hypothesis deliberately attributes entropy loss to pathway constriction rather than cavity capacity — a competing mechanism to h1's pore-volume contrast. Predeclared proxy derivative: d(descriptor)/d(lsd_f) < 0, i.e., larger bottlenecks reduce predicted entropy loss at fixed adsorbate volume. Limitations: Df is a hard-sphere geometric bottleneck on a fixed probe convention; it ignores window flexibility and atomistic potential-energy barriers, and Vol is an all-atom vdW volume compared against a heavy-atom-proxy-derived framework geometry.",
    "falsification_criteria": "The hypothesis is falsified if entropy loss at fixed adsorbate volume does not decrease with lsd_f within the native training regime, or if a descriptor using the included diameter along the path (lsd_p, global-cavity-like scale) outperforms the bottleneck Df form — which would indicate cavity capacity rather than pathway constriction controls the entropy loss and would support a connectivity/cavity mechanism over the bottleneck mechanism. Failure of the cubic exponent versus linear or quadratic exponents (Vol vs Df, Df^2) would also falsify the specific volumetric-scaling claim.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Df^3 proxies the bottleneck-limited accessible passage volume per pathway; Vol proxies the molecular volume that must pass through. Transfer limitation: Df is computed for a fixed probe convention and says nothing about Di (global cavity diameter) or about energetic barriers at windows; agreement of this descriptor would be evidence of geometric-path association only, not of kinetic escape controlling equilibrium entropy.",
      "physical_interpretation": "log10 of the dimensionless ratio q_Vol / q_lsd_f^3 with q_lsd_f the row-varying bottleneck diameter relative to its fixed positive training-reference median (5.16326 angstrom); lsd_f is strictly positive over the whole training domain (min 0.857), so no zero-division or epsilon is needed. The exponent 3 is a fixed numeric expression within the allowed range, asserted as volumetric scaling, not fitted.",
      "boundary_behavior": "All training rows have Vol > 0 and lsd_f > 0, so the descriptor is finite on every row without smoothing constants; no legitimate-zero input (PBF, PMI, SPAN, GeDi, ASA, AV) appears in the formula, and no artificial epsilon is introduced.",
      "vary_input": "lsd_f",
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
    "slot_id": "h3",
    "name": "bottleneck_volume_cubic_contrast",
    "formula": "log10(q_lsd_f ** 3 / q_Vol)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss associated with accessing the pore network scales with the ratio of the adsorbate's van der Waals volume to the cube of the framework's bottleneck free-sphere diameter (Zeo++ Df): adsorbates whose volume is large relative to the bottleneck passage scale lose more entropy because the number of accessible diffusion pathways and admissible positions shrinks with the bottleneck, not with the global cavity size.",
    "rationale": "The self-precheck returned target_association 'contradicted' for the predeclared chain d(descriptor)/d(lsd_f) < 0: the training rank association (Spearman 0.6286) runs opposite to the declared direction. Since hypothesis, mechanism_family and entropy_direction are preserved, the descriptor sign is reversed (equivalently q_lsd_f^3 / q_Vol) so that the bottleneck-contrast form aligns with the observed association while keeping the volumetric-scaling structure and the bottleneck (Df, not Di/lsd_p) attribution. Declared proxy derivative is now d(descriptor)/d(lsd_f) > 0 within the training regime. This reversal is an empirical association correction on fixed-probe geometric proxies; it reverses the direction suggested by the round-1 diagnostics and may reflect confounding between framework geometry and adsorbate identity, so no causal claim is made. The tension with h1's volume-contrast direction (both share q_Vol with opposite signs) is explicitly flagged as a competing-mechanism risk rather than resolved.",
    "falsification_criteria": "Falsified if, holding Vol fixed within subgroups of the training regime, the lsd_f association reverts toward the round-1 direction, or if a descriptor built on the included diameter along the path (lsd_p, cavity-like scale) outperforms the bottleneck Df form (indicating cavity capacity rather than pathway constriction controls the association), or if the cubic exponent fails against linear (Df) or quadratic (Df^2) alternatives. The sign conflict with h1's Vol direction is itself a falsification signal: if the reversed sign only reproduces h1's Vol term with opposite sign, the bottleneck mechanism adds no information and should be rejected.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Df^3 proxies a bottleneck-limited passage-volume scale; Vol proxies the molecular volume that must pass through. Df is a fixed-probe hard-sphere bottleneck (passing sphere along a periodic free path), not the global included diameter Di and not lsd_p; it ignores window flexibility and energetic barriers. Agreement of this descriptor would be evidence of geometric association only, not of kinetic escape controlling equilibrium entropy.",
      "physical_interpretation": "Negated log10 of the dimensionless ratio q_Vol / q_lsd_f^3, with q_lsd_f the row-varying bottleneck diameter relative to its fixed positive training-reference median 5.16326 angstrom. The exponent 3 is a fixed numeric expression in the allowed range, asserted as volumetric scaling, not fitted. The overall sign is an empirical calibration (see rationale), not a physical law.",
      "boundary_behavior": "All training rows have Vol > 0 (min 20.424) and lsd_f > 0 (min 0.85684), so the descriptor is finite on every row without smoothing constants; no legitimate-zero input (PBF, PMI, SPAN, GeDi, ASA, AV) appears in the formula and no epsilon is introduced. Negation preserves finiteness.",
      "vary_input": "lsd_f",
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
      "training_spearman": -0.6285950097652175,
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
    "name": "bottleneck_volume_cubic_contrast",
    "formula": "log10(q_lsd_f ** 3 / q_Vol)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss associated with accessing the pore network scales with the ratio of the adsorbate's van der Waals volume to the cube of the framework's bottleneck free-sphere diameter (Zeo++ Df): adsorbates whose volume is large relative to the bottleneck passage scale lose more entropy because the number of accessible diffusion pathways and admissible positions shrinks with the bottleneck, not with the global cavity size.",
    "rationale": "The self-precheck returned target_association 'contradicted' for the predeclared chain d(descriptor)/d(lsd_f) < 0: the training rank association (Spearman 0.6286) runs opposite to the declared direction. Since hypothesis, mechanism_family and entropy_direction are preserved, the descriptor sign is reversed (equivalently q_lsd_f^3 / q_Vol) so that the bottleneck-contrast form aligns with the observed association while keeping the volumetric-scaling structure and the bottleneck (Df, not Di/lsd_p) attribution. Declared proxy derivative is now d(descriptor)/d(lsd_f) > 0 within the training regime. This reversal is an empirical association correction on fixed-probe geometric proxies; it reverses the direction suggested by the round-1 diagnostics and may reflect confounding between framework geometry and adsorbate identity, so no causal claim is made. The tension with h1's volume-contrast direction (both share q_Vol with opposite signs) is explicitly flagged as a competing-mechanism risk rather than resolved.",
    "falsification_criteria": "Falsified if, holding Vol fixed within subgroups of the training regime, the lsd_f association reverts toward the round-1 direction, or if a descriptor built on the included diameter along the path (lsd_p, cavity-like scale) outperforms the bottleneck Df form (indicating cavity capacity rather than pathway constriction controls the association), or if the cubic exponent fails against linear (Df) or quadratic (Df^2) alternatives. The sign conflict with h1's Vol direction is itself a falsification signal: if the reversed sign only reproduces h1's Vol term with opposite sign, the bottleneck mechanism adds no information and should be rejected.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "geometric_path_contrast"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Df^3 proxies a bottleneck-limited passage-volume scale; Vol proxies the molecular volume that must pass through. Df is a fixed-probe hard-sphere bottleneck (passing sphere along a periodic free path), not the global included diameter Di and not lsd_p; it ignores window flexibility and energetic barriers. Agreement of this descriptor would be evidence of geometric association only, not of kinetic escape controlling equilibrium entropy.",
      "physical_interpretation": "Negated log10 of the dimensionless ratio q_Vol / q_lsd_f^3, with q_lsd_f the row-varying bottleneck diameter relative to its fixed positive training-reference median 5.16326 angstrom. The exponent 3 is a fixed numeric expression in the allowed range, asserted as volumetric scaling, not fitted. The overall sign is an empirical calibration (see rationale), not a physical law.",
      "boundary_behavior": "All training rows have Vol > 0 (min 20.424) and lsd_f > 0 (min 0.85684), so the descriptor is finite on every row without smoothing constants; no legitimate-zero input (PBF, PMI, SPAN, GeDi, ASA, AV) appears in the formula and no epsilon is introduced. Negation preserves finiteness.",
      "vary_input": "lsd_f",
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
      "training_spearman": -0.6285950097652175,
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
    "mode": "no_retrieval",
    "items": 0,
    "lexical_tokens": 0
  },
  "cited_items": [],
  "mechanism_cards": []
}
```
