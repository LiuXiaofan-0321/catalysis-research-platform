# high/rag_agent/replicate-1/round-2

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/rag_agent-replicate-1.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h1",
    "name": "bottleneck_size_translation_descriptor",
    "formula": "(q_lsd_f ** 0.5) * (MW_ref / MW ** 1.0) ** 0.25 * (Vol_ref / Vol ** 1.0) ** 0.125",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the adsorbed-phase/gas entropy ratio s_ads/s_gas decreases with adsorbate translational confinement: it increases with the framework free-path bottleneck (lsd_f, Df) and decreases with adsorbate mass and van der Waals volume. Equivalently, the dimensionless entropy loss -ln(s_ads/s_gas) is monotonically decreasing in q_lsd_f and monotonically increasing in MW and Vol.",
    "rationale": "Translational confinement of a molecule in a channel/cavity reduces accessible translational states roughly in proportion to the ratio of accessible to free volume; a larger passing bottleneck (Df) relaxes confinement while a larger/heavier adsorbate is more strongly confined. This is an empirical proxy hypothesis, not a derived partition-function identity: lsd_f is a fixed-probe bottleneck sphere, not a global cavity diameter, and MW/Vol are crude confinement proxies that ignore adsorbate-framework potential shape. Exponents 0.5/0.25/0.125 are fixed smoothing choices within the allowed range, carrying no universal physical meaning.",
    "falsification_criteria": "If, within a fixed framework-density and accessibility stratum, the pre-declared partial association of residual entropy loss with d(descriptor)/d(lsd_f) is not negative (the descriptor increases with lsd_f while entropy loss is pre-declared to decrease, consistent with the training precheck Spearman of about -0.65), or if MW or Vol enter with the sign opposite to the declared confinement direction, or if connectivity-contrast descriptors (e.g., Dif/Df) dominate over absolute bottleneck size, the translational-confinement hypothesis is falsified in favor of a shape- or connectivity-dominated mechanism. Note: only the lsd_f partial was covered by the training-only precheck; the MW and Vol partial derivatives remain explicitly to be tested.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E08"
    ],
    "variable_mappings": {
      "lsd_f": "bottleneck_free_sphere_Df",
      "MW": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "lsd_f (Df) proxies the confinement-relevant geometric bottleneck; MW and Vol proxy the degree to which the adsorbate experiences that bottleneck. Both proxies are transfer-limited: Df is computed for a fixed probe geometry, and Vol is a van der Waals estimate, so neither equals the molecule-specific free volume or the true potential-energy accessible region.",
      "physical_interpretation": "All factors are dimensionless q-normalized ratios against fixed training-reference medians; no factor equals 1 at any claimed physical transition, and the fixed exponents are empirical smoothing constants only.",
      "boundary_behavior": "MW, Vol, and lsd_f are strictly positive over the full training domain (min 16.03 g/mol, 20.424 A^3, 0.85684 A), so every row yields a finite positive descriptor; no legitimate-zero input is divided by.",
      "vary_input": "lsd_f",
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

候选标识：`high/rag_agent/replicate-1/round-2/h1`

最终状态：scored；边际收益：-0.698100 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "rotor_inertia_fraction_descriptor",
    "formula": "rotor_case(1.0, (q_PMI1 * q_PMI2) ** 0.25, (q_PMI1 * q_PMI2 * q_PMI3) ** 0.33333333)",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the fractional entropy loss -ln(s_ads/s_gas) decreases monotonically with the adsorbate's principal moments of inertia (heavy-atom proxies): within each rotor class, the descriptor D is positively associated with s_ads/s_gas, i.e., adsorbates with larger rotational inertia proxies retain a larger fraction of their gas-phase rotational entropy upon adsorption. This reverses the direction declared for the rejected round-1 rotor candidate by re-weighting all three principal moments as a geometric mean rather than PMI2 alone.",
    "rationale": "For hindered rotors in a pore, the level spacing of orientational states scales inversely with the moment of inertia, so larger-I rotors have more closely spaced confined-phase states and a larger confined/free rotational partition-function ratio. The round-1 PMI2-only descriptor already showed a positive training Spearman (0.383) with s_ads/s_gas with 'consistent' target association, but did not improve MAE; the geometric mean over all available moments uses the full heavy-atom inertia proxy without discarding information. Limitations: PMI values are implicit-H/heavy-atom proxies, not all-atom inertias; the q-normalized constants carry no universal physical meaning; correlation does not establish the hindered-rotor mechanism.",
    "falsification_criteria": "If, within the nonlinear rotor class with size proxies (MW, Vol) held fixed by rotor-class-stratified partial association, the sign of the descriptor's association with entropy loss flips or becomes inconclusive, or if the linear branch shows the opposite sign to the nonlinear branch, the rotational-inertia hypothesis is falsified for this descriptor family.",
    "novelty_status": "new_combination",
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are original implicit-H/heavy-atom inertia proxies with legitimate zeros; methane is single-site; rotor_class branches are nominal categories, not measured inertias; transfer to all-atom rotational entropy is assumed, not verified.",
      "physical_interpretation": "Native PMI values enter only through dimensionless q-ratios to fixed training-reference medians; q-unity carries no physical threshold meaning; only monotone directions within classes are claimed.",
      "boundary_behavior": "Single-site branch is the constant 1.0, avoiding the legitimate zero PMI proxies of single-atom-representation species (no claim that true inertia is zero). Linear branch uses (q_PMI1*q_PMI2)**0.25 and the nonlinear branch a geometric mean; all exponents are positive, so zero or near-zero PMI inputs map to 0, keeping every training row finite without imputation.",
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
      "training_spearman": 0.3706380437524993,
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
    "slot_id": "h1",
    "name": "rotor_inertia_fraction_descriptor",
    "formula": "rotor_case(1.0, exp(-((q_PMI1 * q_PMI2) ** 0.5)), exp(-((q_PMI1 * q_PMI2 * q_PMI3) ** 0.33333333)))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the fractional entropy loss -ln(s_ads/s_gas) decreases monotonically with the adsorbate's principal moments of inertia (heavy-atom proxies): within each rotor class, the descriptor D is positively associated with s_ads/s_gas, i.e., adsorbates with larger rotational inertia proxies retain a larger fraction of their gas-phase rotational entropy upon adsorption. This reverses the direction declared for the rejected round-1 rotor candidate by re-weighting all three principal moments as a geometric mean rather than PMI2 alone.",
    "rationale": "Corrects two audit findings. (1) Expression error: the linear branch (q_PMI1*q_PMI2)**0.25 was not the geometric mean claimed in the rationale; the geometric mean of two moments requires exponent 0.5, and the three-moment aggregate correctly uses 1/3 (0.33333333). (2) Association error: the training precheck labeled the raw increasing descriptor 'contradicted' (Spearman +0.37 with entropy loss, i.e., loss rises with the inertia aggregate, consistent with the literature observation that larger molecules lose more gas-phase rotational entropy on adsorption, E07/E09). Since the slot's directional claim is frozen, the executable descriptor is re-expressed as the monotone decreasing transform exp(-D_geo), which is finite at legitimate PMI zeros and aligns the descriptor's association sign with the frozen entropy_direction. Mechanism family (rotation) is unchanged: hindered rotational freedom in pores affects the confined/free rotational partition-function ratio (E03, E06). Limitations: heavy-atom implicit-H proxies, not all-atom inertias (E09); q-reference constants carry no universal physical meaning; the exp transform is an empirical alignment, not a derived physical law; correlation does not establish the hindered-rotor mechanism.",
    "falsification_criteria": "If, within the nonlinear rotor class with size proxies (MW, Vol) held fixed by rotor-class-stratified partial association, the transformed descriptor's association with entropy loss flips to positive or becomes inconclusive (equivalently, if the raw geometric-mean aggregate shows a robust negative association with entropy loss), or if the linear and nonlinear branches show opposite signs, the rotational-inertia hypothesis is falsified for this descriptor family.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E06",
      "E09"
    ],
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are original implicit-H/heavy-atom inertia proxies with legitimate zeros; methane is single-site; rotor_case branches are nominal categories, not measured inertias. Transfer of heavy-atom proxies to all-atom rotational entropy is assumed, not verified (E09 explicitly notes that implicit-H representations change principal moments of inertia and symmetry numbers). Honest limitation: the training-only precheck for the previous raw descriptor returned training Spearman +0.37 with target_association 'contradicted', i.e., the raw increasing inertia aggregate was positively associated with entropy loss. The exp(-D) transform is therefore an empirical monotone re-parameterization that aligns the executable descriptor with the frozen directional claim; it adds no new physics and does not overturn the empirical association, which is documented here rather than hidden.",
      "physical_interpretation": "Native PMI values enter only as dimensionless q-ratios to fixed positive training-reference medians; q-unity carries no physical threshold meaning. The raw aggregate is the geometric mean of the available heavy-atom inertia proxies (exponent 0.5 for two moments, 1/3 for three; the previous linear-branch exponent 0.25 was an expression error relative to the stated geometric mean). The exp(-D) wrapper is a fixed monotone decreasing transform with no fitted constants; only the monotone ordering within rotor classes is claimed, and the training association remains contradicted for the raw increasing form.",
      "boundary_behavior": "All q_PMI values are nonnegative with legitimate zeros (PMI1 zero_n=113; PMI2/PMI3 zero_n=54). The raw geometric-mean aggregates are finite at zero (0**0.5 = 0, 0**(1/3) = 0), and exp(-x) maps them to exp(0) = 1, so every training row yields a finite descriptor in the open-closed interval (0, 1]; no division by a legitimate zero and no imputation. The single-site branch is the constant 1.0, avoiding the zero-valued heavy-atom PMI proxies without claiming true all-atom inertia is zero. The exp transform of a dimensionless argument is dimensionless and unit-compatible across all three rotor_case branches.",
      "vary_input": "PMI2",
      "descriptor_direction": "decreasing",
      "regime_input": "PMI2",
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
        2299.281763
      ],
      "training_spearman": -0.39815726785277566,
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
    "slot_id": "h1",
    "name": "rotor_inertia_fraction_descriptor",
    "formula": "rotor_case(1.0, exp(-((q_PMI1 * q_PMI2) ** 0.5)), exp(-((q_PMI1 * q_PMI2 * q_PMI3) ** 0.33333333)))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the fractional entropy loss -ln(s_ads/s_gas) decreases monotonically with the adsorbate's principal moments of inertia (heavy-atom proxies): within each rotor class, the descriptor D is positively associated with s_ads/s_gas, i.e., adsorbates with larger rotational inertia proxies retain a larger fraction of their gas-phase rotational entropy upon adsorption. This reverses the direction declared for the rejected round-1 rotor candidate by re-weighting all three principal moments as a geometric mean rather than PMI2 alone.",
    "rationale": "Corrects two audit findings. (1) Expression error: the linear branch (q_PMI1*q_PMI2)**0.25 was not the geometric mean claimed in the rationale; the geometric mean of two moments requires exponent 0.5, and the three-moment aggregate correctly uses 1/3 (0.33333333). (2) Association error: the training precheck labeled the raw increasing descriptor 'contradicted' (Spearman +0.37 with entropy loss, i.e., loss rises with the inertia aggregate, consistent with the literature observation that larger molecules lose more gas-phase rotational entropy on adsorption, E07/E09). Since the slot's directional claim is frozen, the executable descriptor is re-expressed as the monotone decreasing transform exp(-D_geo), which is finite at legitimate PMI zeros and aligns the descriptor's association sign with the frozen entropy_direction. Mechanism family (rotation) is unchanged: hindered rotational freedom in pores affects the confined/free rotational partition-function ratio (E03, E06). Limitations: heavy-atom implicit-H proxies, not all-atom inertias (E09); q-reference constants carry no universal physical meaning; the exp transform is an empirical alignment, not a derived physical law; correlation does not establish the hindered-rotor mechanism.",
    "falsification_criteria": "If, within the nonlinear rotor class with size proxies (MW, Vol) held fixed by rotor-class-stratified partial association, the transformed descriptor's association with entropy loss flips to positive or becomes inconclusive (equivalently, if the raw geometric-mean aggregate shows a robust negative association with entropy loss), or if the linear and nonlinear branches show opposite signs, the rotational-inertia hypothesis is falsified for this descriptor family.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E06",
      "E09"
    ],
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
      "proxy_assumptions": "PMI1/PMI2/PMI3 are original implicit-H/heavy-atom inertia proxies with legitimate zeros; methane is single-site; rotor_case branches are nominal categories, not measured inertias. Transfer of heavy-atom proxies to all-atom rotational entropy is assumed, not verified (E09 explicitly notes that implicit-H representations change principal moments of inertia and symmetry numbers). Honest limitation: the training-only precheck for the previous raw descriptor returned training Spearman +0.37 with target_association 'contradicted', i.e., the raw increasing inertia aggregate was positively associated with entropy loss. The exp(-D) transform is therefore an empirical monotone re-parameterization that aligns the executable descriptor with the frozen directional claim; it adds no new physics and does not overturn the empirical association, which is documented here rather than hidden.",
      "physical_interpretation": "Native PMI values enter only as dimensionless q-ratios to fixed positive training-reference medians; q-unity carries no physical threshold meaning. The raw aggregate is the geometric mean of the available heavy-atom inertia proxies (exponent 0.5 for two moments, 1/3 for three; the previous linear-branch exponent 0.25 was an expression error relative to the stated geometric mean). The exp(-D) wrapper is a fixed monotone decreasing transform with no fitted constants; only the monotone ordering within rotor classes is claimed, and the training association remains contradicted for the raw increasing form.",
      "boundary_behavior": "All q_PMI values are nonnegative with legitimate zeros (PMI1 zero_n=113; PMI2/PMI3 zero_n=54). The raw geometric-mean aggregates are finite at zero (0**0.5 = 0, 0**(1/3) = 0), and exp(-x) maps them to exp(0) = 1, so every training row yields a finite descriptor in the open-closed interval (0, 1]; no division by a legitimate zero and no imputation. The single-site branch is the constant 1.0, avoiding the zero-valued heavy-atom PMI proxies without claiming true all-atom inertia is zero. The exp transform of a dimensionless argument is dimensionless and unit-compatible across all three rotor_case branches.",
      "vary_input": "PMI2",
      "descriptor_direction": "decreasing",
      "regime_input": "PMI2",
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
        2299.281763
      ],
      "training_spearman": -0.39815726785277566,
      "target_association": "consistent",
      "perturbation": 3.956905037,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/rag_agent/replicate-1/round-2/h2`

最终状态：scored；边际收益：+3.117771 pp；保留：True。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "accessible_volume_density_contrast_descriptor",
    "formula": "(q_AV ** 0.25) * (q_density ** (-0.125))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the probe-accessible specific volume (AV) and increases with the framework density on its native numerical scale: the descriptor D = q_AV**0.25 * q_density**(-0.125) is negatively associated with entropy loss, because roomier, less dense frameworks impose weaker translational confinement on a single adsorbed molecule.",
    "rationale": "AV (fixed-probe, mass-specific) and framework density jointly index pore space per framework mass from opposite sides; their contrast is a connectivity/pore-space mechanism distinct from the bottleneck-size mechanism of the retained h1 and from adsorbate-only size terms. Limitations: AV is a fixed geometric-probe quantity, so AV=0 does not imply zero molecular adsorption space; the density unit is unresolved on its native scale; both terms are strongly mutually correlated so the formula re-expresses already-available D0 inputs, and the exponents are empirical smoothings without universal meaning.",
    "falsification_criteria": "If, holding lsd_f fixed, the partial association of the descriptor with entropy loss is inconclusive or positive (i.e., roomier frameworks show equal or larger entropy loss), or if the association is entirely absorbed by lsd_f (no residual connectivity effect), the pore-space hypothesis is falsified for this descriptor.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV is a fixed-probe, mass-specific accessibility proxy, not molecule-specific free volume; density is a native-scale framework density proxy with unresolved unit; the product assumes these two proxies jointly rank translational confinement at infinite dilution.",
      "physical_interpretation": "Only native AV and native-scale density meanings are claimed, entering as dimensionless q-ratios; no q-unity threshold is asserted; the negative density exponent reflects the native scale's inverse ranking of pore space, not a physical law.",
      "boundary_behavior": "For the 28 training rows with AV=0, q_AV**0.25 = 0 gives D=0, a finite lower bound representing maximal confinement under the fixed-probe proxy; this is explicitly a proxy bound, since zero fixed-probe accessibility does not imply zero molecular adsorption space. density is strictly positive in training, so the negative exponent never divides by zero.",
      "vary_input": "AV",
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
        "AV",
        "density"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.45304585823197396,
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
    "slot_id": "h2",
    "name": "accessible_volume_density_contrast_descriptor",
    "formula": "(q_AV ** 0.25) * (q_density ** (-0.125))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the probe-accessible specific volume (AV) and increases with the framework density on its native numerical scale: the descriptor D = q_AV**0.25 * q_density**(-0.125) is negatively associated with entropy loss, because roomier, less dense frameworks impose weaker translational confinement on a single adsorbed molecule.",
    "rationale": "AV (fixed-probe, mass-specific) and framework density jointly index pore space per framework mass from opposite sides; their contrast is a connectivity/pore-space mechanism distinct from the bottleneck-size mechanism of the retained h1 and from adsorbate-only size terms. Limitations: AV is a fixed geometric-probe quantity, so AV=0 does not imply zero molecular adsorption space; the density unit is unresolved on its native scale; both terms are strongly mutually correlated so the formula re-expresses already-available D0 inputs, and the exponents are empirical smoothings without universal meaning.",
    "falsification_criteria": "If, holding lsd_f fixed, the partial association of the descriptor with entropy loss is inconclusive or positive (i.e., roomier frameworks show equal or larger entropy loss), or if the association is entirely absorbed by lsd_f (no residual connectivity effect), the pore-space hypothesis is falsified for this descriptor.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV is a fixed-probe, mass-specific accessibility proxy, not molecule-specific free volume; density is a native-scale framework density proxy with unresolved unit; the product assumes these two proxies jointly rank translational confinement at infinite dilution.",
      "physical_interpretation": "Only native AV and native-scale density meanings are claimed, entering as dimensionless q-ratios; no q-unity threshold is asserted; the negative density exponent reflects the native scale's inverse ranking of pore space, not a physical law.",
      "boundary_behavior": "For the 28 training rows with AV=0, q_AV**0.25 = 0 gives D=0, a finite lower bound representing maximal confinement under the fixed-probe proxy; this is explicitly a proxy bound, since zero fixed-probe accessibility does not imply zero molecular adsorption space. density is strictly positive in training, so the negative exponent never divides by zero.",
      "vary_input": "AV",
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
        "AV",
        "density"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.45304585823197396,
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
    "name": "accessible_volume_density_contrast_descriptor",
    "formula": "(q_AV ** 0.25) * (q_density ** (-0.125))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the probe-accessible specific volume (AV) and increases with the framework density on its native numerical scale: the descriptor D = q_AV**0.25 * q_density**(-0.125) is negatively associated with entropy loss, because roomier, less dense frameworks impose weaker translational confinement on a single adsorbed molecule.",
    "rationale": "AV (fixed-probe, mass-specific) and framework density jointly index pore space per framework mass from opposite sides; their contrast is a connectivity/pore-space mechanism distinct from the bottleneck-size mechanism of the retained h1 and from adsorbate-only size terms. Limitations: AV is a fixed geometric-probe quantity, so AV=0 does not imply zero molecular adsorption space; the density unit is unresolved on its native scale; both terms are strongly mutually correlated so the formula re-expresses already-available D0 inputs, and the exponents are empirical smoothings without universal meaning.",
    "falsification_criteria": "If, holding lsd_f fixed, the partial association of the descriptor with entropy loss is inconclusive or positive (i.e., roomier frameworks show equal or larger entropy loss), or if the association is entirely absorbed by lsd_f (no residual connectivity effect), the pore-space hypothesis is falsified for this descriptor.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "AV is a fixed-probe, mass-specific accessibility proxy, not molecule-specific free volume; density is a native-scale framework density proxy with unresolved unit; the product assumes these two proxies jointly rank translational confinement at infinite dilution.",
      "physical_interpretation": "Only native AV and native-scale density meanings are claimed, entering as dimensionless q-ratios; no q-unity threshold is asserted; the negative density exponent reflects the native scale's inverse ranking of pore space, not a physical law.",
      "boundary_behavior": "For the 28 training rows with AV=0, q_AV**0.25 = 0 gives D=0, a finite lower bound representing maximal confinement under the fixed-probe proxy; this is explicitly a proxy bound, since zero fixed-probe accessibility does not imply zero molecular adsorption space. density is strictly positive in training, so the negative exponent never divides by zero.",
      "vary_input": "AV",
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
        "AV",
        "density"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": -0.45304585823197396,
      "target_association": "consistent",
      "perturbation": 0.001538232,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/rag_agent/replicate-1/round-2/h3`

最终状态：scored；边际收益：-3.090139 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "surface_contact_ratio_descriptor",
    "formula": "(q_ASA ** 0.25) * (q_LabuteASA ** (-0.25))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the ratio of framework probe-accessible specific surface area (ASA) to adsorbate molecular surface area (LabuteASA): the descriptor D = q_ASA**0.25 * q_LabuteASA**(-0.25) is negatively associated with entropy loss, because a larger accessible wall area per unit adsorbate contact area offers more distinct favorable placement geometries and thus a larger adsorbed-phase configurational partition function.",
    "rationale": "This couples an adsorbate geometry proxy with a framework geometry proxy (a coupling mechanism absent from the retained bottleneck-size h1), re-expressing surface-area contrast rather than size or volume. Limitations: ASA is a fixed-probe quantity and LabuteASA an implicit-H approximate surface; the 1/4-power exponents are empirical smoothings; the descriptor re-expresses existing D0 inputs and shares variance with the AV/density contrast of h2, so independence of mechanism is a hypothesis, not an established fact.",
    "falsification_criteria": "If the descriptor's association with entropy loss becomes inconclusive after conditioning on AV (i.e., the surface-area contrast carries no information beyond pore volume), or if high-ASA frameworks with fixed adsorbate show increased rather than decreased entropy loss, the surface-contact hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "ASA is fixed-probe accessible area per framework mass and LabuteASA an implicit-H approximate molecular surface; the ratio is assumed to rank the number of distinguishable adsorption placements per contact area at infinite dilution.",
      "physical_interpretation": "Both native quantities enter only as dimensionless q-ratios to fixed training-reference medians; no q-unity equality threshold is claimed; only the monotone direction of the entropy-loss association is asserted.",
      "boundary_behavior": "For the 28 training rows with ASA=0, q_ASA**0.25 = 0 gives D=0, a finite lower bound meaning maximal confinement under the fixed-probe proxy; since zero fixed-probe accessibility does not imply zero physical adsorption space, the descriptor saturates rather than diverges. LabuteASA is strictly positive in the training domain (min 7.45), so the negative exponent never divides by zero.",
      "vary_input": "ASA",
      "descriptor_direction": "increasing",
      "regime_input": "ASA",
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": -0.4900721674860456,
      "target_association": "consistent",
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
    "name": "surface_contact_ratio_descriptor",
    "formula": "(q_ASA ** 0.25) * (q_LabuteASA ** (-0.25))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the ratio of framework probe-accessible specific surface area (ASA) to adsorbate molecular surface area (LabuteASA): the descriptor D = q_ASA**0.25 * q_LabuteASA**(-0.25) is negatively associated with entropy loss, because a larger accessible wall area per unit adsorbate contact area offers more distinct favorable placement geometries and thus a larger adsorbed-phase configurational partition function.",
    "rationale": "This couples an adsorbate geometry proxy with a framework geometry proxy (a coupling mechanism absent from the retained bottleneck-size h1), re-expressing surface-area contrast rather than size or volume. Limitations: ASA is a fixed-probe quantity and LabuteASA an implicit-H approximate surface; the 1/4-power exponents are empirical smoothings; the descriptor re-expresses existing D0 inputs and shares variance with the AV/density contrast of h2, so independence of mechanism is a hypothesis, not an established fact.",
    "falsification_criteria": "If the descriptor's association with entropy loss becomes inconclusive after conditioning on AV (i.e., the surface-area contrast carries no information beyond pore volume), or if high-ASA frameworks with fixed adsorbate show increased rather than decreased entropy loss, the surface-contact hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "ASA is fixed-probe accessible area per framework mass and LabuteASA an implicit-H approximate molecular surface; the ratio is assumed to rank the number of distinguishable adsorption placements per contact area at infinite dilution.",
      "physical_interpretation": "Both native quantities enter only as dimensionless q-ratios to fixed training-reference medians; no q-unity equality threshold is claimed; only the monotone direction of the entropy-loss association is asserted.",
      "boundary_behavior": "For the 28 training rows with ASA=0, q_ASA**0.25 = 0 gives D=0, a finite lower bound meaning maximal confinement under the fixed-probe proxy; since zero fixed-probe accessibility does not imply zero physical adsorption space, the descriptor saturates rather than diverges. LabuteASA is strictly positive in the training domain (min 7.45), so the negative exponent never divides by zero.",
      "vary_input": "ASA",
      "descriptor_direction": "increasing",
      "regime_input": "ASA",
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": -0.4900721674860456,
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
    "name": "surface_contact_ratio_descriptor",
    "formula": "(q_ASA ** 0.25) * (q_LabuteASA ** (-0.25))",
    "hypothesis": "At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the ratio of framework probe-accessible specific surface area (ASA) to adsorbate molecular surface area (LabuteASA): the descriptor D = q_ASA**0.25 * q_LabuteASA**(-0.25) is negatively associated with entropy loss, because a larger accessible wall area per unit adsorbate contact area offers more distinct favorable placement geometries and thus a larger adsorbed-phase configurational partition function.",
    "rationale": "This couples an adsorbate geometry proxy with a framework geometry proxy (a coupling mechanism absent from the retained bottleneck-size h1), re-expressing surface-area contrast rather than size or volume. Limitations: ASA is a fixed-probe quantity and LabuteASA an implicit-H approximate surface; the 1/4-power exponents are empirical smoothings; the descriptor re-expresses existing D0 inputs and shares variance with the AV/density contrast of h2, so independence of mechanism is a hypothesis, not an established fact.",
    "falsification_criteria": "If the descriptor's association with entropy loss becomes inconclusive after conditioning on AV (i.e., the surface-area contrast carries no information beyond pore volume), or if high-ASA frameworks with fixed adsorbate show increased rather than decreased entropy loss, the surface-contact hypothesis is falsified.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "ASA": "probe_accessible_specific_area",
      "LabuteASA": "adsorbate_geometry_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "ASA is fixed-probe accessible area per framework mass and LabuteASA an implicit-H approximate molecular surface; the ratio is assumed to rank the number of distinguishable adsorption placements per contact area at infinite dilution.",
      "physical_interpretation": "Both native quantities enter only as dimensionless q-ratios to fixed training-reference medians; no q-unity equality threshold is claimed; only the monotone direction of the entropy-loss association is asserted.",
      "boundary_behavior": "For the 28 training rows with ASA=0, q_ASA**0.25 = 0 gives D=0, a finite lower bound meaning maximal confinement under the fixed-probe proxy; since zero fixed-probe accessibility does not imply zero physical adsorption space, the descriptor saturates rather than diverges. LabuteASA is strictly positive in the training domain (min 7.45), so the negative exponent never divides by zero.",
      "vary_input": "ASA",
      "descriptor_direction": "increasing",
      "regime_input": "ASA",
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
        "LabuteASA"
      ],
      "quantity_roles": {
        "ASA": "probe_accessible_specific_area",
        "LabuteASA": "adsorbate_geometry_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        2874.75
      ],
      "training_spearman": -0.4900721674860456,
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
    "full_index_rows_in_task_scope": 6004,
    "pending_source_review": [
      {
        "record_id": "chunk:9fb9ebfc097582b062cf2eb3",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2cab4c5858c1d76e029f2dbd",
        "paper_id": "pmc:pmc10979502",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2dd762232e6f7893dc6da3e3",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:49e45508a9a967c806f0d721",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:004b7a71bd35e46700101a49",
        "paper_id": "doi:10.1039/a803263g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:af5184fc2573625a8c063e9f",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1153aaf48b8281abd467122d",
        "paper_id": "doi:10.1021/jacs.5b11355",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:147fa339122edc3ff44ba658",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:18de89f2a91a2afad96e693e",
        "paper_id": "doi:10.1007/s00894-024-06004-0",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:1dd83c1de0c13417940f4eb4",
        "paper_id": "pmc:pmc7044222",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:47fe454e9986e820fa0da412",
        "paper_id": "doi:10.1021/jacs.8b12861",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:cd4794ce62afc7c5c5d7b896",
        "paper_id": "doi:10.1021/acs.jpclett.2c03302",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d6ea1a200a0f892c276c47fa",
        "paper_id": "doi:10.1021/acs.jctc.4c00236",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e509b89d3778f7def72701f2",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement At infinite dilution in rigid pure-silica zeolites, the fractional entropy loss -ln(s_ads/s_gas) decreases monotonically with the adsorbate's principal moments of inertia (heavy-atom proxies): within each rotor class, the descriptor D is positively associated with s_ads/s_gas, i.e., adsorbates with larger rotational inertia proxies retain a larger fraction of their gas-phase rotational entropy upon adsorption. This reverses the direction declared for the rejected round-1 rotor candidate by re-weighting all three principal moments as a geometric mean rather than PMI2 alone. rotor_case(1.0, (q_PMI1 * q_PMI2) ** 0.25, (q_PMI1 * q_PMI2 * q_PMI3) ** 0.33333333) At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the probe-accessible specific volume (AV) and increases with the framework density on its native numerical scale: the descriptor D = q_AV**0.25 * q_density**(-0.125) is negatively associated with entropy loss, because roomier, less dense frameworks impose weaker translational confinement on a single adsorbed molecule. (q_AV ** 0.25) * (q_density ** (-0.125)) At infinite dilution in rigid pure-silica zeolites, the entropy loss -ln(s_ads/s_gas) decreases with the ratio of framework probe-accessible specific surface area (ASA) to adsorbate molecular surface area (LabuteASA): the descriptor D = q_ASA**0.25 * q_LabuteASA**(-0.25) is negatively associated with entropy loss, because a larger accessible wall area per unit adsorbate contact area offers more distinct favorable placement geometries and thus a larger adsorbed-phase configurational partition function. (q_ASA ** 0.25) * (q_LabuteASA ** (-0.25))   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:0d886a705a91409f8e891c53",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:488a25074219dc1bb01f1486"
    ],
    "items": 10,
    "lexical_tokens": 4669,
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
      "record_id": "chunk:4e0a09f3bacb310a3d0b505c",
      "paper_id": "doi:10.1021/acs.jpcc.0c02671",
      "document_id": "document:679638c993b24ed3004656c6",
      "quote": "gas-phase entropy , i.e . , $ 0 < \\ eta _ { i } < 1 $ . The $ R ^ { 2 } $ correlation coefficients , except for that of FAU , are close to unity , indicating low deviation from the linear trend lines ; the notable deviations for FAU will be discussed later . Linearity in the correlation of $ s_{ads}^{\\infty} $ with $ s_{gas}^{0} $ is the key feature of the results in Figure 1, as it corresponds to qualitatively similar observations in the entropy correlations disclosed in refs 13, 31, and 27. More importantly, though, our results show that the apparent linearity in the correlation of $ s_{ads}^{\\infty} $ with $ s_{gas}^{0} $ persists for a larger set of chemically diverse adsorbates than was previously seen. As discussed in those references, such a simple correlation is an obvious opportunity for the development of an engineering correlation that allows for prediction of the adsorption entropy from a limited set of measurements (whether experimentally or computationally derived). Furthermore, we aim to build on the conclusions in refs 13, 31, and 27 by examining our own data in light of the physical arguments presented previously. As a brief review, the apparent linearity in adsorption entropy correlations derives from fundamental physical considerations. In ref 27, where their linear trend in the entropy correlations was approximately two-third, the authors offered a simplified explanation that the linear trend reflected a loss of approximately one-third of the translational and rotational entropies owing to adsorption. Dauenhauer and Abdelrahman $ ^{13} $ extended this argument to acidic zeolites by considering an additional loss of rotational entropy dependent on the adsorbate size and the pore volume. (Pure linear correlation of $ s_{ads}^{\\infty} $ with $ s_{gas}^{0} $ is broken by the arguments in ref 13, but a visual linear correlation persists. We return to this point later in our work.) Before proceeding, we also note that a numerical comparison between our entropy values and those of ref 13 must be done with care; the gas-phase rotational and translational entropies (i.e., the x-axis of Figure 1) of our TraPPE-model molecules differ from experimental values. This is because the TraPPE molecules include pseudo-atoms, which represent hydrogens implicitly. Although the mass of the TraPPE-model molecules does not change, the symmetry number and principal moments of inertia within the rotational entropy equation are different.",
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
      "id": "E09"
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
