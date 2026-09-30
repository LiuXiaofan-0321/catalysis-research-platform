# high/small_kg_rag_agent/replicate-3/round-3

[原始轨迹JSON](../../jacs_au_kg_v4_20260930/complete-server-results/high/discovery/small_kg_rag_agent-replicate-3.json)

训练/评分reference是D0加下列历史保留组合。三个最终槽分别评分，只有最多一个改善者保留。

```json
[
  {
    "slot_id": "h1",
    "name": "size_vs_bottleneck_confinement",
    "formula": "log(q_Vol / q_lsd_f**2)",
    "hypothesis": "Falsifiable hypothesis (translation family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases monotonically with the adsorbate size (molecular weight and vdW volume, joint size proxy) normalized by the framework passing-bottleneck diameter Df; i.e., tighter windows relative to molecular size reduce translational/configurational freedom of the confined molecule relative to the gas.",
    "rationale": "Direction/expression correction of the translation-family draft. The original descriptor log((q_MW*q_Vol)/q_lsd_f**2) was confinement-signed and its training-only precheck contradicted the stored entropy_direction (Spearman +0.61, target_association 'contradicted'). Since hypothesis, mechanism_family (translation) and entropy_direction (decreasing) are fixed, the descriptor is inverted to a freedom proxy log(q_lsd_f**2/q_Vol) and simplified: MW is dropped because mass conflates mass with size (double-counting with Vol) and lacks graph support for this mechanism. Mechanism unchanged: tighter windows relative to molecular size restrict translational/configurational freedom, raising entropy loss = -ln(s_ads/s_gas); equivalently, larger passing bottleneck relative to molecular vdW volume lowers entropy loss. Df is a hard-sphere geometric bottleneck proxy, not the cavity diameter Di and not an energetic quantity; the descriptor is a pre-registered association claim only, exponents (1,2) are fixed numerical choices, not fitted universal constants.",
    "falsification_criteria": "Refutation boundary: if, within fixed lsd_f quantile bands (e.g., 0-0.25, 0.25-0.75, 0.75-1.0 of the training domain), the residual association between log(q_lsd_f**2/q_Vol) and entropy loss/R is not negative (i.e., entropy loss does not decrease as the freedom proxy grows), or the sign flips across lsd_f regimes, the translational-confinement hypothesis as parameterized here is falsified. Competing mechanism: entropy loss dominated by framework energy-site heterogeneity or adsorbate-framework interaction stiffness (enthalpic/rotational origin), in which case a translation-only freedom descriptor should show no stable association. Numerical correlation alone would not validate the mechanism; the precheck statistic of the prior confinement-signed form (+0.61) is descriptive evidence of association, not causal confirmation.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E04",
      "E10"
    ],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "Assumes (i) vdW volume ranks the effective molecular cross-section relevant to a hard-sphere passing bottleneck; (ii) Df (largest passing free sphere) is an adequate bottleneck proxy for translational access; (iii) heavy-atom-derived adsorbate descriptors transfer to real adsorbates. All are approximations: Vol is a static geometric size proxy, Df ignores thermal framework flexibility and site-specific adsorption geometry, and the descriptor says nothing about loading dependence. MW was removed: mass is not itself a geometry proxy, it double-counted size alongside Vol, and no mechanism edge in the source graph supports MW for the translation family (graph edges support Vol and lsd_f/lsd_p).",
      "physical_interpretation": "Native meanings: lsd_f (Df) is the largest sphere that can pass through a periodic free path (bottleneck), NOT the global cavity diameter Di; Vol is the adsorbate vdW volume. q_lsd_f and q_Vol are row-varying ratios to fixed positive training-reference medians (5.16326 angstrom, 67.24 angstrom^3); X/q_X = X_ref is constant for positive X and never used; a q-ratio of 1 is a numerical reference point, not a physical equality threshold. The descriptor log(q_lsd_f**2/q_Vol) is a dimensionless 'translational freedom' proxy: it increases when the passing bottleneck is large relative to molecular volume. Direction correction: the previously stored descriptor was confinement-signed and its training-only precheck returned target_association 'contradicted' (Spearman +0.61 with entropy loss/R) relative to the stored entropy_direction 'decreasing'. With mechanism_family and entropy_direction fixed, the descriptor is inverted so that increasing vary_input (lsd_f) increases the descriptor and is hypothesized to decrease entropy loss per R (more configurational freedom, less entropy loss). This inversion is a descriptor-sign correction, not a validation: the precheck statistic is descriptive only and does not establish causality.",
      "boundary_behavior": "Vol (min 20.424 angstrom^3) and lsd_f (min 0.85684 angstrom) are strictly positive on the training domain, so q_Vol > 0 and q_lsd_f > 0 on every training row; the log argument q_Vol / q_lsd_f**2 is strictly positive and the descriptor is finite on all 2361 training rows with no division by zero, no imputation, and no added epsilon. The patched descriptor now decreases monotonically and smoothly as vary_input lsd_f increases (matching the locked descriptor_direction 'decreasing': d(descriptor)/d(lsd_f) < 0) and increases monotonically with Vol; with the locked entropy_direction 'decreasing' (d(entropy loss)/d(lsd_f) < 0), the descriptor acts as a confinement-signed size-vs-bottleneck proxy: larger molecular vdW volume relative to the passing-bottleneck squared corresponds to greater entropy loss, equivalently a larger passing bottleneck relative to molecular size lowers entropy loss. No singularities exist inside the training domain; behavior outside the training quantile range is extrapolation and is not claimed physical. The exponent 2 on the bottleneck and 1 on volume remain fixed numerical choices, not fitted universal constants; lsd_f (Df) is a hard-sphere bottleneck proxy, not the global cavity diameter Di and not an energetic quantity. This patch corrects only the expression sign convention to resolve the predeclared direction contradiction (opposite_n = 2361); any empirical association remains descriptive and does not establish causality.",
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
  {
    "slot_id": "h3",
    "name": "accessible_volume_confinement",
    "formula": "exp(-q_AV)",
    "hypothesis": "Falsifiable hypothesis (connectivity family, probe-volume proxy): at infinite dilution, the adsorption entropy loss (in units of R) increases as the fixed-probe accessible specific volume AV of the framework decreases; equivalently, the descriptor exp(-q_AV) associates positively with entropy loss at fixed adsorbate geometry. This tests whether global probe-accessible void space, rather than the local bottleneck Df alone, sets the configurational entropy penalty.",
    "rationale": "Direction-declaration correction of a rejected draft: the formula exp(-q_AV) is retained (the stored hypothesis and entropy_direction are immutable and consistent with it), but descriptor_direction is corrected to decreasing with respect to AV, resolving the precheck's direction contradiction. Substantive claim unchanged: at fixed adsorbate geometry, less fixed-probe accessible volume per framework mass should associate with larger entropy loss (E03, E08). Limitations: AV is a fixed-probe, mass-specific accessibility rather than molecule-specific free volume; the mechanism is a correlational proxy and the ANN already receives AV as an input.",
    "falsification_criteria": "If, with adsorbate geometry proxies held fixed, exp(-q_AV) shows a negative or null partial association with entropy loss within the native AV domain (0 to 0.661336) — i.e., entropy loss does not increase as AV decreases — the accessible-volume confinement hypothesis is contradicted; a competing mechanism is that pore connectivity and bottleneck diameter (the Df/Dif contrast) dominate the entropy loss while total accessible volume is redundant.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E03",
      "E08"
    ],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe accessible specific volume proxies the configurational space available to adsorbates generally; this fails for molecules smaller or larger than the fixed geometric probe and for frameworks whose accessible volume is fragmented (connectivity is not resolved by AV). The descriptor assumes a smooth monotone mapping from AV to entropy loss without threshold behavior; zero AV means fixed-probe inaccessibility, not zero physical adsorption space (E08 reports occupiable zeolite volume as an empirical entropy-loss descriptor, without establishing molecule-specific free volume).",
      "physical_interpretation": "q_AV = AV/0.0759781 is a dimensionless row-varying ratio to the fixed positive training-reference median; exp(-q_AV) is dimensionless. AV is a mass-specific, fixed-probe accessibility, not molecule-specific free volume, so no literal AV/Vol free-volume equality is claimed and no q-unity threshold is interpreted physically. Direction correction: the descriptor exp(-q_AV) DECREASES as AV increases; combined with the stored entropy_direction (increasing with the descriptor), this encodes the hypothesis that entropy loss increases as accessible volume decreases. The prior draft erroneously declared descriptor_direction increasing, which contradicted the formula.",
      "boundary_behavior": "AV is non-negative on the training domain (zero_n = 28); exp(-q_AV) is defined and finite for all AV >= 0, so legitimate fixed-probe zeros map to the finite value exp(0)=1 with no singularity, no epsilon and no imputation. At the domain maximum AV = 0.661336 the descriptor is exp(-0.661336/0.0759781), a small strictly positive number.",
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

候选标识：`high/small_kg_rag_agent/replicate-3/round-3/h1`

最终状态：scored；边际收益：-7.153690 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "shape_compactness_confinement",
    "formula": "log(q_LabuteASA / q_Vol**(2/3))",
    "hypothesis": "Falsifiable hypothesis (shape family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases with the dimensionless adsorbate compactness ratio LabuteASA / Vol**(2/3); i.e., at fixed vdW volume, molecules with larger accessible surface area (less compact, more extended) lose more translational and configurational entropy upon confinement.",
    "rationale": "The ratio of molecular surface area to the two-thirds power of vdW volume is a purely geometric shape factor: compact near-spherical molecules approach a lower bound, while elongated or branched molecules take larger values. More extended molecules have fewer accessible positions and orientations inside framework cavities, so their entropy loss relative to the gas should be larger. This is an empirical proxy re-expression of geometry inputs already present in the ANN; no causal claim is made.",
    "falsification_criteria": "If the training Spearman association between this descriptor and entropy loss is negative or inconclusive after conditioning on the currently retained descriptors, or if the marginal improvement is non-positive, the shape-compactness confinement hypothesis is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA and Vol are implicit-H/heavy-atom geometry proxies; their ratio is dimensionless and strictly positive over the whole training domain. The exponent 2/3 is a fixed geometric scaling reference, not a fitted parameter.",
      "physical_interpretation": "q_LabuteASA and q_Vol are ratios to fixed positive training-reference medians; the descriptor is a dimensionless shape factor with no physical q-unity threshold.",
      "boundary_behavior": "Both LabuteASA and Vol are strictly positive in the training domain (zero_n = 0), so the log-ratio is finite for every row; no zero or negative arguments occur.",
      "vary_input": "LabuteASA",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "LabuteASA",
        "Vol"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.381525237901583,
      "target_association": "consistent",
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
    "name": "shape_compactness_confinement",
    "formula": "log(q_LabuteASA / q_Vol**(2/3))",
    "hypothesis": "Falsifiable hypothesis (shape family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases with the dimensionless adsorbate compactness ratio LabuteASA / Vol**(2/3); i.e., at fixed vdW volume, molecules with larger accessible surface area (less compact, more extended) lose more translational and configurational entropy upon confinement.",
    "rationale": "The ratio of molecular surface area to the two-thirds power of vdW volume is a purely geometric shape factor: compact near-spherical molecules approach a lower bound, while elongated or branched molecules take larger values. More extended molecules have fewer accessible positions and orientations inside framework cavities, so their entropy loss relative to the gas should be larger. This is an empirical proxy re-expression of geometry inputs already present in the ANN; no causal claim is made.",
    "falsification_criteria": "If the training Spearman association between this descriptor and entropy loss is negative or inconclusive after conditioning on the currently retained descriptors, or if the marginal improvement is non-positive, the shape-compactness confinement hypothesis is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA and Vol are implicit-H/heavy-atom geometry proxies; their ratio is dimensionless and strictly positive over the whole training domain. The exponent 2/3 is a fixed geometric scaling reference, not a fitted parameter.",
      "physical_interpretation": "q_LabuteASA and q_Vol are ratios to fixed positive training-reference medians; the descriptor is a dimensionless shape factor with no physical q-unity threshold.",
      "boundary_behavior": "Both LabuteASA and Vol are strictly positive in the training domain (zero_n = 0), so the log-ratio is finite for every row; no zero or negative arguments occur.",
      "vary_input": "LabuteASA",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "LabuteASA",
        "Vol"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.381525237901583,
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
    "name": "shape_compactness_confinement",
    "formula": "log(q_LabuteASA / q_Vol**(2/3))",
    "hypothesis": "Falsifiable hypothesis (shape family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases with the dimensionless adsorbate compactness ratio LabuteASA / Vol**(2/3); i.e., at fixed vdW volume, molecules with larger accessible surface area (less compact, more extended) lose more translational and configurational entropy upon confinement.",
    "rationale": "The ratio of molecular surface area to the two-thirds power of vdW volume is a purely geometric shape factor: compact near-spherical molecules approach a lower bound, while elongated or branched molecules take larger values. More extended molecules have fewer accessible positions and orientations inside framework cavities, so their entropy loss relative to the gas should be larger. This is an empirical proxy re-expression of geometry inputs already present in the ANN; no causal claim is made.",
    "falsification_criteria": "If the training Spearman association between this descriptor and entropy loss is negative or inconclusive after conditioning on the currently retained descriptors, or if the marginal improvement is non-positive, the shape-compactness confinement hypothesis is falsified for this dataset.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "LabuteASA": "adsorbate_geometry_proxy",
      "Vol": "molecular_vdw_volume"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "shape",
      "proxy_assumptions": "LabuteASA and Vol are implicit-H/heavy-atom geometry proxies; their ratio is dimensionless and strictly positive over the whole training domain. The exponent 2/3 is a fixed geometric scaling reference, not a fitted parameter.",
      "physical_interpretation": "q_LabuteASA and q_Vol are ratios to fixed positive training-reference medians; the descriptor is a dimensionless shape factor with no physical q-unity threshold.",
      "boundary_behavior": "Both LabuteASA and Vol are strictly positive in the training domain (zero_n = 0), so the log-ratio is finite for every row; no zero or negative arguments occur.",
      "vary_input": "LabuteASA",
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
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "LabuteASA",
        "Vol"
      ],
      "quantity_roles": {
        "LabuteASA": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.381525237901583,
      "target_association": "consistent",
      "perturbation": 0.3451394019,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/small_kg_rag_agent/replicate-3/round-3/h2`

最终状态：scored；边际收益：-6.512927 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "mass_bottleneck_confinement",
    "formula": "q_MW * exp(-q_lsd_f)",
    "hypothesis": "Falsifiable hypothesis (translation family, mass-resolved): at infinite dilution, the adsorption entropy loss (in units of R) increases with the product of adsorbate molecular weight and an exponential bottleneck-confinement factor; specifically, q_MW * exp(-q_lsd_f) associates positively with entropy loss because heavier adsorbates carry more gas-phase translational entropy and tighter passing bottlenecks (smaller Df) suppress accessible confined translational states.",
    "rationale": "This couples a strictly positive adsorbate mass proxy with a monotonically decreasing empirical kernel of the framework passing-bottleneck diameter. The exponential weighting is a smooth alternative to the power-law form already retained; it emphasises confinement differences at small Df without introducing any physical threshold. Because MW and lsd_f are strictly positive in the training domain, the descriptor is finite everywhere.",
    "falsification_criteria": "If the descriptor shows negative or inconclusive association with entropy loss after accounting for the retained descriptors, or if the marginal improvement is non-positive, the mass-bottleneck coupling hypothesis is falsified in favour of a size-only or bottleneck-only description.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "MW is a mass/size proxy for the adsorbate; lsd_f is the Zeo++ passing bottleneck Df, not a global cavity diameter. exp(-q_lsd_f) is a monotone empirical weighting, not a Boltzmann factor.",
      "physical_interpretation": "q_MW and q_lsd_f are dimensionless ratios to fixed positive training-reference medians; the product has no physical q-unity threshold.",
      "boundary_behavior": "MW and lsd_f are strictly positive in the training domain (zero_n = 0), so q_MW is positive, exp(-q_lsd_f) is finite and positive, and the product is finite for every row.",
      "vary_input": "MW",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.588951145740889,
      "target_association": "consistent",
      "perturbation": 0.790673513,
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
    "name": "mass_bottleneck_confinement",
    "formula": "q_MW * exp(-q_lsd_f)",
    "hypothesis": "Falsifiable hypothesis (translation family, mass-resolved): at infinite dilution, the adsorption entropy loss (in units of R) increases with the product of adsorbate molecular weight and an exponential bottleneck-confinement factor; specifically, q_MW * exp(-q_lsd_f) associates positively with entropy loss because heavier adsorbates carry more gas-phase translational entropy and tighter passing bottlenecks (smaller Df) suppress accessible confined translational states.",
    "rationale": "This couples a strictly positive adsorbate mass proxy with a monotonically decreasing empirical kernel of the framework passing-bottleneck diameter. The exponential weighting is a smooth alternative to the power-law form already retained; it emphasises confinement differences at small Df without introducing any physical threshold. Because MW and lsd_f are strictly positive in the training domain, the descriptor is finite everywhere.",
    "falsification_criteria": "If the descriptor shows negative or inconclusive association with entropy loss after accounting for the retained descriptors, or if the marginal improvement is non-positive, the mass-bottleneck coupling hypothesis is falsified in favour of a size-only or bottleneck-only description.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "MW is a mass/size proxy for the adsorbate; lsd_f is the Zeo++ passing bottleneck Df, not a global cavity diameter. exp(-q_lsd_f) is a monotone empirical weighting, not a Boltzmann factor.",
      "physical_interpretation": "q_MW and q_lsd_f are dimensionless ratios to fixed positive training-reference medians; the product has no physical q-unity threshold.",
      "boundary_behavior": "MW and lsd_f are strictly positive in the training domain (zero_n = 0), so q_MW is positive, exp(-q_lsd_f) is finite and positive, and the product is finite for every row.",
      "vary_input": "MW",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.588951145740889,
      "target_association": "consistent",
      "perturbation": 0.790673513,
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
    "name": "mass_bottleneck_confinement",
    "formula": "q_MW * exp(-q_lsd_f)",
    "hypothesis": "Falsifiable hypothesis (translation family, mass-resolved): at infinite dilution, the adsorption entropy loss (in units of R) increases with the product of adsorbate molecular weight and an exponential bottleneck-confinement factor; specifically, q_MW * exp(-q_lsd_f) associates positively with entropy loss because heavier adsorbates carry more gas-phase translational entropy and tighter passing bottlenecks (smaller Df) suppress accessible confined translational states.",
    "rationale": "This couples a strictly positive adsorbate mass proxy with a monotonically decreasing empirical kernel of the framework passing-bottleneck diameter. The exponential weighting is a smooth alternative to the power-law form already retained; it emphasises confinement differences at small Df without introducing any physical threshold. Because MW and lsd_f are strictly positive in the training domain, the descriptor is finite everywhere.",
    "falsification_criteria": "If the descriptor shows negative or inconclusive association with entropy loss after accounting for the retained descriptors, or if the marginal improvement is non-positive, the mass-bottleneck coupling hypothesis is falsified in favour of a size-only or bottleneck-only description.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "MW": "adsorbate_geometry_proxy",
      "lsd_f": "bottleneck_free_sphere_Df"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "translation",
      "proxy_assumptions": "MW is a mass/size proxy for the adsorbate; lsd_f is the Zeo++ passing bottleneck Df, not a global cavity diameter. exp(-q_lsd_f) is a monotone empirical weighting, not a Boltzmann factor.",
      "physical_interpretation": "q_MW and q_lsd_f are dimensionless ratios to fixed positive training-reference medians; the product has no physical q-unity threshold.",
      "boundary_behavior": "MW and lsd_f are strictly positive in the training domain (zero_n = 0), so q_MW is positive, exp(-q_lsd_f) is finite and positive, and the product is finite for every row.",
      "vary_input": "MW",
      "descriptor_direction": "increasing",
      "regime_input": "lsd_f",
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
        "MW",
        "lsd_f"
      ],
      "quantity_roles": {
        "MW": "adsorbate_geometry_proxy",
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
      "training_spearman": 0.588951145740889,
      "target_association": "consistent",
      "perturbation": 0.790673513,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/small_kg_rag_agent/replicate-3/round-3/h3`

最终状态：scored；边际收益：-9.950330 pp；保留：False。

复核改动字段：evidence_ids, rationale

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "rotor_inertia_magnitude",
    "formula": "rotor_case(0.0, sqrt(q_PMI2 * q_PMI3), (q_PMI1 * q_PMI2 * q_PMI3)**(1/3))",
    "hypothesis": "Falsifiable hypothesis (rotation family, rotor-branched): at infinite dilution, the adsorption entropy loss (in units of R) increases with the magnitude of the heavy-atom principal moments of inertia; linear species are scored by the geometric mean of their two transverse moments sqrt(q_PMI2*q_PMI3), nonlinear species by the geometric mean of all three moments (q_PMI1*q_PMI2*q_PMI3)**(1/3), and single-site species carry no heavy-atom rotational inertia proxy and take the zero branch. Larger rotational inertia implies more gas-phase rotational entropy that can be lost upon confinement.",
    "rationale": "The rotor_case branches respect the physical structure of the heavy-atom inertia proxy: single-site molecules (e.g. methane in the implicit-H representation) have zero moments, linear molecules have PMI1 = 0 and equal transverse moments, and nonlinear molecules have three strictly positive moments. Using the geometric mean of the relevant non-zero moments yields a strictly positive, dimensionless inertia magnitude for linear and nonlinear classes. This is an empirical proxy combination, not a rotational partition-function model.",
    "falsification_criteria": "If the rotor-branched descriptor shows negative or inconclusive association with entropy loss within the linear and nonlinear subpopulations, or if the marginal improvement is non-positive, the rotational inertia-magnitude hypothesis is falsified; a competing mechanism would attribute the entropy loss to framework confinement rather than adsorbate inertia.",
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
      "proxy_assumptions": "PMI1, PMI2 and PMI3 are original implicit-H/heavy-atom inertia proxies, not true all-atom moments; single-site species have legitimate zeros and take the explicit rotor_case branch 0.0. Linear branch: sqrt(q_PMI2*q_PMI3). Nonlinear branch: (q_PMI1*q_PMI2*q_PMI3)**(1/3).",
      "physical_interpretation": "q_PMI1, q_PMI2 and q_PMI3 are dimensionless ratios to fixed positive training-reference medians; the descriptor is an inertia magnitude with no physical q-unity threshold.",
      "boundary_behavior": "For single-site rows the descriptor is exactly 0.0. For linear rows PMI2 and PMI3 are strictly positive, so sqrt(q_PMI2*q_PMI3) is finite. For nonlinear rows PMI1, PMI2 and PMI3 are strictly positive (all 268 PMI1 near-zero rows are single-site or linear), so the cube-root expression is finite. Every training row yields a finite value.",
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
      "training_spearman": 0.39465906035514964,
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
    "name": "rotor_inertia_magnitude",
    "formula": "rotor_case(0.0, sqrt(q_PMI2 * q_PMI3), (q_PMI1 * q_PMI2 * q_PMI3)**(1/3))",
    "hypothesis": "Falsifiable hypothesis (rotation family, rotor-branched): at infinite dilution, the adsorption entropy loss (in units of R) increases with the magnitude of the heavy-atom principal moments of inertia; linear species are scored by the geometric mean of their two transverse moments sqrt(q_PMI2*q_PMI3), nonlinear species by the geometric mean of all three moments (q_PMI1*q_PMI2*q_PMI3)**(1/3), and single-site species carry no heavy-atom rotational inertia proxy and take the zero branch. Larger rotational inertia implies more gas-phase rotational entropy that can be lost upon confinement.",
    "rationale": "The rotor-branched inertia-magnitude descriptor is retained unchanged: expression, rotor_case branches, variable mappings and domain behavior all check out (single-site branch 0.0 for the 54 single-site rows; linear branch sqrt(q_PMI2*q_PMI3) finite since PMI2 zero_n = 54 matches the single-site count; nonlinear branch (q_PMI1*q_PMI2*q_PMI3)**(1/3) finite since the 268 PMI1 near-zero rows equal 54 single-site + 214 linear, leaving all nonlinear rows strictly positive). Evidence item E07 is added as conditional support for the proxy framing: it explicitly notes that implicit-H (pseudo-atom) representations change the principal moments of inertia entering the rotational entropy expression, which is exactly the heavy-atom-proxy limitation the hypothesis already declares. No causal or novelty claim is made; the training association (Spearman 0.395, consistent) is an empirical regularity, not a validated mechanism.",
    "falsification_criteria": "If the rotor-branched descriptor shows negative or inconclusive association with entropy loss within the linear and nonlinear subpopulations, or if the marginal improvement is non-positive, the rotational inertia-magnitude hypothesis is falsified; a competing mechanism would attribute the entropy loss to framework confinement rather than adsorbate inertia.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E07"
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
      "proxy_assumptions": "PMI1, PMI2 and PMI3 are original implicit-H/heavy-atom inertia proxies, not true all-atom moments; single-site species have legitimate zeros and take the explicit rotor_case branch 0.0. Linear branch: sqrt(q_PMI2*q_PMI3). Nonlinear branch: (q_PMI1*q_PMI2*q_PMI3)**(1/3).",
      "physical_interpretation": "q_PMI1, q_PMI2 and q_PMI3 are dimensionless ratios to fixed positive training-reference medians; the descriptor is an inertia magnitude with no physical q-unity threshold.",
      "boundary_behavior": "For single-site rows the descriptor is exactly 0.0. For linear rows PMI2 and PMI3 are strictly positive, so sqrt(q_PMI2*q_PMI3) is finite. For nonlinear rows PMI1, PMI2 and PMI3 are strictly positive (all 268 PMI1 near-zero rows are single-site or linear), so the cube-root expression is finite. Every training row yields a finite value.",
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
      "training_spearman": 0.39465906035514964,
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
    "name": "rotor_inertia_magnitude",
    "formula": "rotor_case(0.0, sqrt(q_PMI2 * q_PMI3), (q_PMI1 * q_PMI2 * q_PMI3)**(1/3))",
    "hypothesis": "Falsifiable hypothesis (rotation family, rotor-branched): at infinite dilution, the adsorption entropy loss (in units of R) increases with the magnitude of the heavy-atom principal moments of inertia; linear species are scored by the geometric mean of their two transverse moments sqrt(q_PMI2*q_PMI3), nonlinear species by the geometric mean of all three moments (q_PMI1*q_PMI2*q_PMI3)**(1/3), and single-site species carry no heavy-atom rotational inertia proxy and take the zero branch. Larger rotational inertia implies more gas-phase rotational entropy that can be lost upon confinement.",
    "rationale": "The rotor-branched inertia-magnitude descriptor is retained unchanged: expression, rotor_case branches, variable mappings and domain behavior all check out (single-site branch 0.0 for the 54 single-site rows; linear branch sqrt(q_PMI2*q_PMI3) finite since PMI2 zero_n = 54 matches the single-site count; nonlinear branch (q_PMI1*q_PMI2*q_PMI3)**(1/3) finite since the 268 PMI1 near-zero rows equal 54 single-site + 214 linear, leaving all nonlinear rows strictly positive). Evidence item E07 is added as conditional support for the proxy framing: it explicitly notes that implicit-H (pseudo-atom) representations change the principal moments of inertia entering the rotational entropy expression, which is exactly the heavy-atom-proxy limitation the hypothesis already declares. No causal or novelty claim is made; the training association (Spearman 0.395, consistent) is an empirical regularity, not a validated mechanism.",
    "falsification_criteria": "If the rotor-branched descriptor shows negative or inconclusive association with entropy loss within the linear and nonlinear subpopulations, or if the marginal improvement is non-positive, the rotational inertia-magnitude hypothesis is falsified; a competing mechanism would attribute the entropy loss to framework confinement rather than adsorbate inertia.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E07"
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
      "proxy_assumptions": "PMI1, PMI2 and PMI3 are original implicit-H/heavy-atom inertia proxies, not true all-atom moments; single-site species have legitimate zeros and take the explicit rotor_case branch 0.0. Linear branch: sqrt(q_PMI2*q_PMI3). Nonlinear branch: (q_PMI1*q_PMI2*q_PMI3)**(1/3).",
      "physical_interpretation": "q_PMI1, q_PMI2 and q_PMI3 are dimensionless ratios to fixed positive training-reference medians; the descriptor is an inertia magnitude with no physical q-unity threshold.",
      "boundary_behavior": "For single-site rows the descriptor is exactly 0.0. For linear rows PMI2 and PMI3 are strictly positive, so sqrt(q_PMI2*q_PMI3) is finite. For nonlinear rows PMI1, PMI2 and PMI3 are strictly positive (all 268 PMI1 near-zero rows are single-site or linear), so the cube-root expression is finite. Every training row yields a finite value.",
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
      "training_spearman": 0.39465906035514964,
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
        "record_id": "chunk:d65d8d58704815da0b0ad4b7",
        "paper_id": "doi:10.1063/1.4750979",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:8dc09a802942ff3d455ea3a8",
        "paper_id": "doi:10.26434/chemrxiv.9725948.v2",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:194f3dc043b8b419400650a3",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:d3a799358d58da57167e96f1",
        "paper_id": "doi:10.1021/acs.langmuir.3c03931",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:284bd753c3b7265971a69c86",
        "paper_id": "pmc:pmc7690318",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:2a36986d9ba7dbe05f02c0d2",
        "paper_id": "doi:10.1021/acs.langmuir.5b03015",
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
        "record_id": "chunk:472c89f72d857bbcf16ff16e",
        "paper_id": "doi:10.1002/asia.202400973",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:4ee093d81da6b5c01358e0ca",
        "paper_id": "doi:10.1021/acs.jctc.5c01100",
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
        "record_id": "chunk:899f3c42d1c6c876da906571",
        "paper_id": "pmc:pmc9888634",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:ab32bc39777676fd9cacd2f5",
        "paper_id": "pmc:pmc5805402",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:af5184fc2573625a8c063e9f",
        "paper_id": "doi:10.1039/b819435c",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement Falsifiable hypothesis (shape family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases with the dimensionless adsorbate compactness ratio LabuteASA / Vol**(2/3); i.e., at fixed vdW volume, molecules with larger accessible surface area (less compact, more extended) lose more translational and configurational entropy upon confinement. log(q_LabuteASA / q_Vol**(2/3)) Falsifiable hypothesis (translation family, mass-resolved): at infinite dilution, the adsorption entropy loss (in units of R) increases with the product of adsorbate molecular weight and an exponential bottleneck-confinement factor; specifically, q_MW * exp(-q_lsd_f) associates positively with entropy loss because heavier adsorbates carry more gas-phase translational entropy and tighter passing bottlenecks (smaller Df) suppress accessible confined translational states. q_MW * exp(-q_lsd_f) Falsifiable hypothesis (rotation family, rotor-branched): at infinite dilution, the adsorption entropy loss (in units of R) increases with the magnitude of the heavy-atom principal moments of inertia; linear species are scored by the geometric mean of their two transverse moments sqrt(q_PMI2*q_PMI3), nonlinear species by the geometric mean of all three moments (q_PMI1*q_PMI2*q_PMI3)**(1/3), and single-site species carry no heavy-atom rotational inertia proxy and take the zero branch. Larger rotational inertia implies more gas-phase rotational entropy that can be lost upon confinement. rotor_case(0.0, sqrt(q_PMI2 * q_PMI3), (q_PMI1 * q_PMI2 * q_PMI3)**(1/3))   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:4e0a09f3bacb310a3d0b505c",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:01d0cb8bf43d75bbc448e004",
      "chunk:e98dff054a73e56b28f6bdf3"
    ],
    "items": 10,
    "lexical_tokens": 4796,
    "unique_source_papers": 4,
    "mechanism_cards": 6,
    "all_source_paragraphs_complete": true,
    "quotes_serialized_once": true
  },
  "cited_items": [
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
