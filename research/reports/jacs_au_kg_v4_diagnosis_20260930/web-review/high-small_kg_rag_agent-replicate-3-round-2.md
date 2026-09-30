# high/small_kg_rag_agent/replicate-3/round-2

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
  }
]
```

## h1

候选标识：`high/small_kg_rag_agent/replicate-3/round-2/h1`

最终状态：scored；边际收益：-0.006963 pp；保留：False。

复核改动字段：

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h1",
    "name": "size_density_confinement",
    "formula": "log(q_Vol) * q_density",
    "hypothesis": "Falsifiable hypothesis (translation family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases with the adsorbate van der Waals volume, and the increase is steeper for frameworks of higher native density (a proxy for lower void fraction per framework mass). The joint size-density product therefore predicts the entropy-loss magnitude, not the s_ads/s_gas ratio directly.",
    "rationale": "Larger confined molecules lose more translational/configurational freedom relative to the gas; a denser framework offers less free space per unit mass, plausibly amplifying confinement for a molecule of given size. The product form predeclares a positive coupling of size and framework density. Limitations: density is on an unresolved native numerical scale; q_Vol and q_density are dimensionless row-varying ratios to fixed positive training-reference medians, and the fixed reference constants carry no universal physical meaning. The descriptor re-expresses inputs already available to the nonlinear ANN, so any association is empirical, not a validated causal mechanism.",
    "falsification_criteria": "If the partial association between log(q_Vol)*q_density and the entropy loss (with rotor class fixed) is negative or non-monotonic within the native domains (Vol 20.424-161.144, density 0.759654-2.11908), the size-density coupling hypothesis is contradicted; a competing mechanism is that framework topology (window/cage connectivity, not captured by density alone) dominates and decouples the density effect from confinement.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Vol proxies molecular excluded volume for translation; native-scale density proxies framework void fraction. Both are geometric proxies; no energetic (adsorbate-framework interaction) information is included, and transfer to chemically heterogeneous adsorbates is not assumed.",
      "physical_interpretation": "q_Vol = Vol/Vol_ref and q_density = density/density_ref are dimensionless row-varying ratios to fixed positive training medians; the descriptor is a dimensionless empirical product. No q-unity threshold is asserted as a physical transition.",
      "boundary_behavior": "Vol and density are strictly positive on the training domain (min 20.424 and 0.759654), so log(q_Vol) is finite for every row; no zero-division or imputation is needed.",
      "vary_input": "Vol",
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
        "Vol",
        "density"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        20.424,
        161.144
      ],
      "training_spearman": 0.3978290767288544,
      "target_association": "consistent",
      "perturbation": 0.7023999999999999,
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
    "name": "size_density_confinement",
    "formula": "log(q_Vol) * q_density",
    "hypothesis": "Falsifiable hypothesis (translation family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases with the adsorbate van der Waals volume, and the increase is steeper for frameworks of higher native density (a proxy for lower void fraction per framework mass). The joint size-density product therefore predicts the entropy-loss magnitude, not the s_ads/s_gas ratio directly.",
    "rationale": "Larger confined molecules lose more translational/configurational freedom relative to the gas; a denser framework offers less free space per unit mass, plausibly amplifying confinement for a molecule of given size. The product form predeclares a positive coupling of size and framework density. Limitations: density is on an unresolved native numerical scale; q_Vol and q_density are dimensionless row-varying ratios to fixed positive training-reference medians, and the fixed reference constants carry no universal physical meaning. The descriptor re-expresses inputs already available to the nonlinear ANN, so any association is empirical, not a validated causal mechanism.",
    "falsification_criteria": "If the partial association between log(q_Vol)*q_density and the entropy loss (with rotor class fixed) is negative or non-monotonic within the native domains (Vol 20.424-161.144, density 0.759654-2.11908), the size-density coupling hypothesis is contradicted; a competing mechanism is that framework topology (window/cage connectivity, not captured by density alone) dominates and decouples the density effect from confinement.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Vol proxies molecular excluded volume for translation; native-scale density proxies framework void fraction. Both are geometric proxies; no energetic (adsorbate-framework interaction) information is included, and transfer to chemically heterogeneous adsorbates is not assumed.",
      "physical_interpretation": "q_Vol = Vol/Vol_ref and q_density = density/density_ref are dimensionless row-varying ratios to fixed positive training medians; the descriptor is a dimensionless empirical product. No q-unity threshold is asserted as a physical transition.",
      "boundary_behavior": "Vol and density are strictly positive on the training domain (min 20.424 and 0.759654), so log(q_Vol) is finite for every row; no zero-division or imputation is needed.",
      "vary_input": "Vol",
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
        "Vol",
        "density"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        20.424,
        161.144
      ],
      "training_spearman": 0.3978290767288544,
      "target_association": "consistent",
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
    "name": "size_density_confinement",
    "formula": "log(q_Vol) * q_density",
    "hypothesis": "Falsifiable hypothesis (translation family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases with the adsorbate van der Waals volume, and the increase is steeper for frameworks of higher native density (a proxy for lower void fraction per framework mass). The joint size-density product therefore predicts the entropy-loss magnitude, not the s_ads/s_gas ratio directly.",
    "rationale": "Larger confined molecules lose more translational/configurational freedom relative to the gas; a denser framework offers less free space per unit mass, plausibly amplifying confinement for a molecule of given size. The product form predeclares a positive coupling of size and framework density. Limitations: density is on an unresolved native numerical scale; q_Vol and q_density are dimensionless row-varying ratios to fixed positive training-reference medians, and the fixed reference constants carry no universal physical meaning. The descriptor re-expresses inputs already available to the nonlinear ANN, so any association is empirical, not a validated causal mechanism.",
    "falsification_criteria": "If the partial association between log(q_Vol)*q_density and the entropy loss (with rotor class fixed) is negative or non-monotonic within the native domains (Vol 20.424-161.144, density 0.759654-2.11908), the size-density coupling hypothesis is contradicted; a competing mechanism is that framework topology (window/cage connectivity, not captured by density alone) dominates and decouples the density effect from confinement.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "Vol": "molecular_vdw_volume",
      "density": "native_framework_density_proxy"
    },
    "physical_claims": [
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "coupling",
      "proxy_assumptions": "Vol proxies molecular excluded volume for translation; native-scale density proxies framework void fraction. Both are geometric proxies; no energetic (adsorbate-framework interaction) information is included, and transfer to chemically heterogeneous adsorbates is not assumed.",
      "physical_interpretation": "q_Vol = Vol/Vol_ref and q_density = density/density_ref are dimensionless row-varying ratios to fixed positive training medians; the descriptor is a dimensionless empirical product. No q-unity threshold is asserted as a physical transition.",
      "boundary_behavior": "Vol and density are strictly positive on the training domain (min 20.424 and 0.759654), so log(q_Vol) is finite for every row; no zero-division or imputation is needed.",
      "vary_input": "Vol",
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
        "Vol",
        "density"
      ],
      "quantity_roles": {
        "Vol": "molecular_vdw_volume",
        "density": "native_framework_density_proxy"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        20.424,
        161.144
      ],
      "training_spearman": 0.3978290767288544,
      "target_association": "consistent",
      "perturbation": 0.7023999999999999,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h2

候选标识：`high/small_kg_rag_agent/replicate-3/round-2/h2`

最终状态：scored；边际收益：+0.414020 pp；保留：False。

复核改动字段：evidence_ids, falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.GeDi

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_inertia_caging_branches",
    "formula": "rotor_case(0.0, q_PMI2, sqrt(q_PMI2 * q_PMI3))",
    "hypothesis": "Falsifiable hypothesis (rotation family, nonlinear_rotor_expression with explicit rotor_case branches): at infinite dilution, the adsorption entropy loss (in units of R) increases with the effective heavy-atom rotational inertia proxy, taken as q_PMI2 for linear adsorbates (PMI1 proxy is zero by the implicit-H/heavy-atom representation) and sqrt(q_PMI2*q_PMI3) for nonlinear adsorbates; single-site molecules (e.g., methane in the heavy-atom representation) receive the constant zero branch. The claim concerns association with entropy loss, not the s_ads/s_gas ratio.",
    "rationale": "Confinement restricts rotational freedom most for adsorbates with large heavy-atom inertias, so a larger effective inertia proxy should associate with larger entropy loss. The geometric mean of the two non-zero principal-moment proxies is used for nonlinear molecules to avoid favoring one axis. Limitations: PMI values are original implicit-H/heavy-atom proxies, not true all-atom inertias; legitimate zeros for single-site molecules must not be read as physical zero inertia, hence the explicit zero branch. The prior round's logarithmic variant scored inconsistently, so the monotonic direction is explicitly falsifiable rather than assumed.",
    "falsification_criteria": "If, with rotor class fixed, the partial association of the branch-selected inertia proxy with entropy loss is negative or insignificant within native PMI2 ranges (linear and nonlinear branches, PMI2 up to 2299.281763), the rotational caging hypothesis is contradicted; a competing mechanism is that shape anisotropy (SPAN/GeDi contrast) rather than inertia magnitude governs rotational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy"
    },
    "physical_claims": [
      "nonlinear_rotor_expression"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments proxy rotational degrees of freedom that confinement suppresses; rotor_case classification is by the native PMI proxy categories with tolerance 1e-10. Transfer limitations: hydrogens are implicit, so all-atom rotational entropy is not represented; single-site molecules are given a zero contribution by construction, not by physics.",
      "physical_interpretation": "q_PMI2 and q_PMI3 are dimensionless row-varying ratios to fixed positive training-reference medians; all three rotor_case branches return dimensionless values. No unity threshold of any q-ratio is interpreted as a physical boundary.",
      "boundary_behavior": "Single-site rows (54 in training) take the constant 0.0 branch, so their legitimate PMI zeros never enter a log or denominator. Linear rows have positive PMI2 proxies; nonlinear rows have non-negative PMI2*q_PMI3 products whose square root is finite (zeros occur only in the single-site class). Every training row yields a finite value without imputation.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
    "reason": "Redundant with a current input"
  }
}
```

### 复核稿

```json
{
  "candidate": {
    "slot_id": "h2",
    "name": "rotor_inertia_caging_branches",
    "formula": "rotor_case(0.0, sqrt(q_PMI2 * q_PMI3) / q_GeDi**2, sqrt(q_PMI2 * q_PMI3) / q_GeDi**2)",
    "hypothesis": "Falsifiable hypothesis (rotation family, nonlinear_rotor_expression with explicit rotor_case branches): at infinite dilution, the adsorption entropy loss (in units of R) increases with the effective heavy-atom rotational inertia proxy, taken as q_PMI2 for linear adsorbates (PMI1 proxy is zero by the implicit-H/heavy-atom representation) and sqrt(q_PMI2*q_PMI3) for nonlinear adsorbates; single-site molecules (e.g., methane in the heavy-atom representation) receive the constant zero branch. The claim concerns association with entropy loss, not the s_ads/s_gas ratio.",
    "rationale": "Correction of the rejected draft: its linear branch q_PMI2 was exactly proportional to an existing ANN input, triggering the redundancy rejection. The corrected descriptor multiplies the two nonzero heavy-atom principal-moment proxies and divides by the squared largest heavy-atom pair distance, so no branch is proportional to a single native input. Physical motivation (qualified): confinement suppresses rotational freedom more for adsorbates with larger effective inertia relative to their size (E01, E03, E06); prior evidence also warns that heavy-atom (implicit-H) moments differ from experimental all-atom moments, so only an association claim is made (E10). The prior round's logarithmic inertia variant scored negatively, so the monotone direction is declared falsifiable rather than assumed. The mechanism remains an empirical proxy already re-expressing ANN inputs.",
    "falsification_criteria": "If, with rotor class fixed, the partial association of sqrt(q_PMI2*q_PMI3)/q_GeDi**2 with entropy loss is negative or null within the native PMI2 training domain (0 to 2299.281763, evaluated separately in linear and nonlinear classes), the rotational caging hypothesis is contradicted; a competing mechanism is that shape anisotropy (SPAN/GeDi contrast) or framework geometry (cavity/bottleneck sizes) rather than inertia magnitude governs rotational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E03",
      "E06",
      "E10"
    ],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments proxy rotational degrees of freedom that confinement suppresses (E01, E03); the normalization by the largest heavy-atom pair distance squared turns the inertia product into a dimensionless compactness-weighted inertia proxy, qualitatively echoing the reported comparison of molecular radius of gyration to available cage space (E06). Transfer limitations: hydrogens are implicit, so all-atom rotational entropy and symmetry numbers are not represented (E10); single-site molecules receive zero by construction, not by physics; the fixed q-reference constants carry no universal meaning.",
      "physical_interpretation": "q_PMI2, q_PMI3 and q_GeDi are dimensionless row-varying ratios to fixed positive training-reference medians; sqrt(q_PMI2*q_PMI3)/q_GeDi**2 is a dimensionless empirical descriptor. No q-unity threshold is asserted as a physical transition. In native units sqrt(PMI2*PMI3) has units angstrom^2*amu, so the descriptor is an inertia-per-squared-size proxy, not a physical mass or entropy.",
      "boundary_behavior": "Single-site rows (54 in training) take the constant 0.0 branch, so their legitimate PMI/geometry zeros never enter a denominator. The native zero counts for PMI2, PMI3 and GeDi each equal 54, matching the single-site rotor count, so on training data every linear and nonlinear row has strictly positive PMI2, PMI3 and GeDi and the branch expression is finite; this finiteness is an empirical count-based argument for the training set, not a theorem for unseen rows. No logs, no epsilon, no imputation.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
        "GeDi",
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.28959500108064234,
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
    "slot_id": "h2",
    "name": "rotor_inertia_caging_branches",
    "formula": "rotor_case(0.0, sqrt(q_PMI2 * q_PMI3) / q_GeDi**2, sqrt(q_PMI2 * q_PMI3) / q_GeDi**2)",
    "hypothesis": "Falsifiable hypothesis (rotation family, nonlinear_rotor_expression with explicit rotor_case branches): at infinite dilution, the adsorption entropy loss (in units of R) increases with the effective heavy-atom rotational inertia proxy, taken as q_PMI2 for linear adsorbates (PMI1 proxy is zero by the implicit-H/heavy-atom representation) and sqrt(q_PMI2*q_PMI3) for nonlinear adsorbates; single-site molecules (e.g., methane in the heavy-atom representation) receive the constant zero branch. The claim concerns association with entropy loss, not the s_ads/s_gas ratio.",
    "rationale": "Correction of the rejected draft: its linear branch q_PMI2 was exactly proportional to an existing ANN input, triggering the redundancy rejection. The corrected descriptor multiplies the two nonzero heavy-atom principal-moment proxies and divides by the squared largest heavy-atom pair distance, so no branch is proportional to a single native input. Physical motivation (qualified): confinement suppresses rotational freedom more for adsorbates with larger effective inertia relative to their size (E01, E03, E06); prior evidence also warns that heavy-atom (implicit-H) moments differ from experimental all-atom moments, so only an association claim is made (E10). The prior round's logarithmic inertia variant scored negatively, so the monotone direction is declared falsifiable rather than assumed. The mechanism remains an empirical proxy already re-expressing ANN inputs.",
    "falsification_criteria": "If, with rotor class fixed, the partial association of sqrt(q_PMI2*q_PMI3)/q_GeDi**2 with entropy loss is negative or null within the native PMI2 training domain (0 to 2299.281763, evaluated separately in linear and nonlinear classes), the rotational caging hypothesis is contradicted; a competing mechanism is that shape anisotropy (SPAN/GeDi contrast) or framework geometry (cavity/bottleneck sizes) rather than inertia magnitude governs rotational entropy loss.",
    "novelty_status": "new_combination",
    "evidence_ids": [
      "E01",
      "E03",
      "E06",
      "E10"
    ],
    "variable_mappings": {
      "PMI2": "heavy_atom_inertia_proxy",
      "PMI3": "heavy_atom_inertia_proxy",
      "GeDi": "heavy_atom_pair_distance"
    },
    "physical_claims": [
      "nonlinear_rotor_expression",
      "empirical_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "rotation",
      "proxy_assumptions": "Heavy-atom principal moments proxy rotational degrees of freedom that confinement suppresses (E01, E03); the normalization by the largest heavy-atom pair distance squared turns the inertia product into a dimensionless compactness-weighted inertia proxy, qualitatively echoing the reported comparison of molecular radius of gyration to available cage space (E06). Transfer limitations: hydrogens are implicit, so all-atom rotational entropy and symmetry numbers are not represented (E10); single-site molecules receive zero by construction, not by physics; the fixed q-reference constants carry no universal meaning.",
      "physical_interpretation": "q_PMI2, q_PMI3 and q_GeDi are dimensionless row-varying ratios to fixed positive training-reference medians; sqrt(q_PMI2*q_PMI3)/q_GeDi**2 is a dimensionless empirical descriptor. No q-unity threshold is asserted as a physical transition. In native units sqrt(PMI2*PMI3) has units angstrom^2*amu, so the descriptor is an inertia-per-squared-size proxy, not a physical mass or entropy.",
      "boundary_behavior": "Single-site rows (54 in training) take the constant 0.0 branch, so their legitimate PMI/geometry zeros never enter a denominator. The native zero counts for PMI2, PMI3 and GeDi each equal 54, matching the single-site rotor count, so on training data every linear and nonlinear row has strictly positive PMI2, PMI3 and GeDi and the branch expression is finite; this finiteness is an empirical count-based argument for the training set, not a theorem for unseen rows. No logs, no epsilon, no imputation.",
      "vary_input": "PMI2",
      "descriptor_direction": "increasing",
      "regime_input": "PMI2",
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
        "GeDi",
        "PMI2",
        "PMI3"
      ],
      "quantity_roles": {
        "GeDi": "heavy_atom_pair_distance",
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
      "training_spearman": 0.28959500108064234,
      "target_association": "consistent",
      "perturbation": 3.956905037,
      "mechanism_validated": false,
      "rotor_class_fixed_during_partial_derivative": true
    }
  }
}
```

## h3

候选标识：`high/small_kg_rag_agent/replicate-3/round-2/h3`

最终状态：scored；边际收益：+3.132006 pp；保留：True。

复核改动字段：evidence_ids, falsification_criteria, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

训练前修复改动字段：

### 盲初稿

```json
{
  "candidate": {
    "slot_id": "h3",
    "name": "accessible_volume_confinement",
    "formula": "exp(-q_AV)",
    "hypothesis": "Falsifiable hypothesis (connectivity family, probe-volume proxy): at infinite dilution, the adsorption entropy loss (in units of R) increases as the fixed-probe accessible specific volume AV of the framework decreases; equivalently, the descriptor exp(-q_AV) associates positively with entropy loss at fixed adsorbate geometry. This tests whether global probe-accessible void space, rather than the local bottleneck Df alone, sets the configurational entropy penalty.",
    "rationale": "A framework with less accessible volume per mass restricts where a molecule can sit, reducing configurational freedom relative to the gas. The negative exponential is a smooth, finite monotone re-expression chosen so the descriptor increases as AV decreases. Limitations: AV is a fixed-geometric-probe, mass-specific accessibility, not molecule-specific free volume; zero AV means the fixed probe finds no accessible space and does not imply zero adsorption space for a given molecule; the unitless q_AV ratio to a fixed positive training median carries no universal physical meaning. The mechanism remains a correlational proxy and the ANN already receives AV as an input.",
    "falsification_criteria": "If, with adsorbate geometry proxies held fixed, exp(-q_AV) shows a negative or null partial association with entropy loss within the native AV domain (0 to 0.661336), the accessible-volume confinement hypothesis is contradicted; a competing mechanism is that pore connectivity and bottleneck diameter (Df/Dif contrast) dominate the entropy loss while total accessible volume is redundant.",
    "novelty_status": "new_combination",
    "evidence_ids": [],
    "variable_mappings": {
      "AV": "probe_accessible_specific_volume"
    },
    "physical_claims": [
      "probe_volume_proxy"
    ],
    "scientific_test": {
      "mechanism_family": "connectivity",
      "proxy_assumptions": "Fixed-probe accessible specific volume proxies the configurational space available to adsorbates generally; this fails for molecules smaller or larger than the probe and for frameworks whose accessible volume is fragmented. The descriptor assumes a monotone, smooth mapping from AV to entropy loss without threshold behavior.",
      "physical_interpretation": "q_AV = AV/AV_ref is a dimensionless row-varying ratio to the fixed positive training-reference median 0.0759781; exp(-q_AV) is dimensionless. Zero AV rows are legitimate fixed-probe inaccessibility, not zero physical adsorption space, and map to descriptor value exp(0)=1.",
      "boundary_behavior": "AV is non-negative on the training domain (zero_n = 28); the negative exponential is defined and finite for all AV >= 0, so legitimate zeros produce the finite value 1 rather than a singularity, and no imputation or epsilon is used.",
      "vary_input": "AV",
      "descriptor_direction": "increasing",
      "regime_input": "AV",
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
      "output_dimensions": {},
      "limitation": "Unit algebra does not verify the mechanism or numerical unit conversion."
    },
    "grounding": {
      "status": "passed",
      "used_variables": [
        "AV"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "direction_failure": {
      "opposite_n": 2361,
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
        "AV"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": 0.4572606532712195,
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
        "AV"
      ],
      "quantity_roles": {
        "AV": "probe_accessible_specific_volume"
      },
      "interpretation": "Executable definition checks; not a proof of all natural-language claims or causality."
    },
    "scientific_check": {
      "regime_n": 2361,
      "native_regime_bounds": [
        0.0,
        0.661336
      ],
      "training_spearman": 0.4572606532712195,
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
        "record_id": "chunk:65fe4c2190f39891e61b4b94",
        "paper_id": "doi:10.1039/d5cs00220f",
        "reason": "source identity/application not reviewed"
      },
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
        "record_id": "chunk:9805f0a944c903cd7580bbcb",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9a3907e626bcdef0bc5bb0cb",
        "paper_id": "doi:10.1002/chem.201705627",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9cdf07cef931a6556f3e0bc9",
        "paper_id": "doi:10.1021/jp0629543",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e4fac391d22a51182458ec9f",
        "paper_id": "doi:10.1021/jp910543r",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:323d66ad417d981217705b45",
        "paper_id": "doi:10.1021/ja015797o",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:560d540c09c85dfa3faa0e8c",
        "paper_id": "doi:10.1021/acs.jpcb.1c02929",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:9fb9ebfc097582b062cf2eb3",
        "paper_id": "doi:10.1039/c3cp55039g",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:a716c0f2d08195e0bc57308d",
        "paper_id": "doi:10.1021/ja105950z",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:abec6882ca4afbb20396aaee",
        "paper_id": "doi:10.1002/cphc.201402189",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:bd25ae12ad46fcd087e05e23",
        "paper_id": "pmc:pmc12747119",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:dfd4ea8f147a6b4f80683826",
        "paper_id": "doi:10.1021/jacs.5c14291",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:e1b683dc5917739326965133",
        "paper_id": "doi:10.1021/acs.chemrev.2c00896",
        "reason": "source identity/application not reviewed"
      },
      {
        "record_id": "chunk:f0a5a652a4377235ec566770",
        "paper_id": "doi:10.1007/s00894-008-0417-6",
        "reason": "source identity/application not reviewed"
      }
    ],
    "identity_boundary": "Reviewed source papers; new passages retain full conditions and conditional transfer status.",
    "mode": "live_full_index_reviewed_identity_search",
    "query": "adsorption entropy confinement Falsifiable hypothesis (translation family): at infinite dilution in rigid pure-silica zeolites, the adsorption entropy loss (in units of R) increases with the adsorbate van der Waals volume, and the increase is steeper for frameworks of higher native density (a proxy for lower void fraction per framework mass). The joint size-density product therefore predicts the entropy-loss magnitude, not the s_ads/s_gas ratio directly. log(q_Vol) * q_density Falsifiable hypothesis (rotation family, nonlinear_rotor_expression with explicit rotor_case branches): at infinite dilution, the adsorption entropy loss (in units of R) increases with the effective heavy-atom rotational inertia proxy, taken as q_PMI2 for linear adsorbates (PMI1 proxy is zero by the implicit-H/heavy-atom representation) and sqrt(q_PMI2*q_PMI3) for nonlinear adsorbates; single-site molecules (e.g., methane in the heavy-atom representation) receive the constant zero branch. The claim concerns association with entropy loss, not the s_ads/s_gas ratio. rotor_case(0.0, q_PMI2, sqrt(q_PMI2 * q_PMI3)) Falsifiable hypothesis (connectivity family, probe-volume proxy): at infinite dilution, the adsorption entropy loss (in units of R) increases as the fixed-probe accessible specific volume AV of the framework decreases; equivalently, the descriptor exp(-q_AV) associates positively with entropy loss at fixed adsorbate geometry. This tests whether global probe-accessible void space, rather than the local bottleneck Df alone, sets the configurational entropy penalty. exp(-q_AV)   ",
    "selected_records": [
      "kg:node:kg-node-f9e5d077b614791a33620d468e9a47cc:1",
      "kg:node:kg-node-881f6860485ff9825beb6894323a720b:0",
      "kg:edge:kg-edge-1cae791bdbd219d2107e377717821edc:15",
      "kg:node:kg-node-587bd87b40facdd05193874e66354ebc:0",
      "chunk:878e3cf9557831b0616715f9",
      "chunk:51aa804bfe1967d7ebb1d76f",
      "chunk:d52b47528dc9757d7e603c4f",
      "chunk:e9ae89d415e72e1faf77faf0",
      "chunk:0add805569d6cec323bb89b1",
      "chunk:4e0a09f3bacb310a3d0b505c"
    ],
    "items": 10,
    "lexical_tokens": 4651,
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
      "id": "E08"
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
      "id": "E10"
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
