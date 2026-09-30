# V4 全部 162 槽的初稿、复核与最终评分

只引用原始最终评分；初稿/复核稿未训练，不能将最终增益解释为复核因果收益。边际增益单位为相对 D0 的百分点。

## high/agent/replicate-1/round-1

该轮最佳保留增益：3.0468 pp；保留 `log10(1 + q_Vol / (1 + q_AV))`。

### h1 (translation)

- 初稿 `log10(1 + q_Vol / (1 + q_AV))`：passed；
- 复核 `log10(1 + q_Vol / (1 + q_AV))`：passed；
- 最终 `log10(1 + q_Vol / (1 + q_AV))`：scored；边际 +3.0468 pp；保留=True
- 复核字段变化：无

### h2 (rotation)

- 初稿 `rotor_case(0, log10(1 + q_PMI1), log10(1 + (q_PMI2 + q_PMI3)/2))`：passed；
- 复核 `rotor_case(0, log10(1 + (q_PMI2 + q_PMI3)/2), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3)/3))`：passed；
- 最终 `rotor_case(0, log10(1 + (q_PMI2 + q_PMI3)/2), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3)/3))`：scored；边际 -4.4959 pp；保留=False
- 复核字段变化：formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation

### h3 (connectivity)

- 初稿 `log10(1 + q_GeDi / q_lsd_f)`：passed；
- 复核 `log10(1 + q_GeDi / q_lsd_f)`：passed；
- 最终 `log10(1 + q_GeDi / q_lsd_f)`：scored；边际 -1.5408 pp；保留=False
- 复核字段变化：无

## high/agent/replicate-1/round-2

该轮最佳保留增益：0.8292 pp；保留 `log10(1 + q_PBF * q_Vol / (1 + q_ASA))`。

### h1 (connectivity)

- 初稿 `log10(1 + q_Vol / q_lsd_p)`：passed；
- 复核 `log10(1 + q_Vol / q_lsd_p)`：passed；
- 最终 `log10(1 + q_Vol / q_lsd_p)`：scored；边际 -1.9750 pp；保留=False
- 复核字段变化：falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

### h2 (shape)

- 初稿 `log10(1 + q_PBF * q_Vol / (1 + q_ASA))`：passed；
- 复核 `log10(1 + q_PBF * q_Vol / (1 + q_ASA))`：passed；
- 最终 `log10(1 + q_PBF * q_Vol / (1 + q_ASA))`：scored；边际 +0.8292 pp；保留=True
- 复核字段变化：无

### h3 (rotation)

- 初稿 `rotor_case(0, log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2)), log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2)))`：passed；
- 复核 `rotor_case(0, log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2 + abs(q_PMI3 - q_PMI1))), log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2 + abs(q_PMI3 - q_PMI1))))`：passed；
- 最终 `rotor_case(0, log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2 + abs(q_PMI3 - q_PMI1))), log10(1 + (q_PMI3 - q_PMI1)/(1 + q_PMI2 + abs(q_PMI3 - q_PMI1))))`：scored；边际 -1.8038 pp；保留=False
- 复核字段变化：formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation

## high/agent/replicate-1/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (rotation)

- 初稿 `rotor_case(0, log10(1 + q_PMI2 / q_lsd_f), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3) / (3 * q_lsd_f)))`：passed；
- 复核 `rotor_case(0, log10(1 + q_PMI2 / q_lsd_f), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3) / (3 * q_lsd_f)))`：passed；
- 最终 `rotor_case(0, log10(1 + q_PMI2 / q_lsd_f), log10(1 + (q_PMI1 + q_PMI2 + q_PMI3) / (3 * q_lsd_f)))`：scored；边际 -3.7508 pp；保留=False
- 复核字段变化：scientific_test.boundary_behavior

### h2 (shape)

- 初稿 `log10(1 + q_GeDi**3 / (1 + q_Vol))`：passed；
- 复核 `log10(1 + q_GeDi**3 / (1 + q_Vol))`：passed；
- 最终 `log10(1 + q_GeDi**3 / (1 + q_Vol))`：scored；边际 -2.8399 pp；保留=False
- 复核字段变化：rationale, scientific_test.boundary_behavior

### h3 (coupling)

- 初稿 `log10(1 + q_Vol * q_density / q_lsd_p)`：passed；
- 复核 `log10(1 + q_Vol * q_density / q_lsd_p)`：passed；
- 最终 `log10(1 + q_Vol * q_density / q_lsd_p)`：scored；边际 -4.1568 pp；保留=False
- 复核字段变化：physical_claims, scientific_test.proxy_assumptions

## high/agent/replicate-2/round-1

该轮最佳保留增益：4.1237 pp；保留 `log(1 + q_PMI3) - log(1 + q_PMI1)`。

### h1 (connectivity)

- 初稿 `log(1 + q_AV) + 0.5 * log(1 + q_lsd_f)`：passed；
- 复核 `log(1 + q_AV) + 0.5 * log(1 + q_lsd_f)`：passed；
- 最终 `log(1 + q_AV) + 0.5 * log(1 + q_lsd_f)`：scored；边际 +2.7386 pp；保留=False
- 复核字段变化：无

### h2 (rotation)

- 初稿 `log(1 + q_PMI3) - log(1 + q_PMI1)`：passed；
- 复核 `log(1 + q_PMI3) - log(1 + q_PMI1)`：passed；
- 最终 `log(1 + q_PMI3) - log(1 + q_PMI1)`：scored；边际 +4.1237 pp；保留=True
- 复核字段变化：无

### h3 (coupling)

- 初稿 `log(1 + q_Vol) - log(1 + q_lsd_f)`：passed；
- 复核 `log(1 + q_Vol) - log(1 + q_lsd_f)`：passed；
- 最终 `log(1 + q_Vol) - log(1 + q_lsd_f)`：scored；边际 +0.7890 pp；保留=False
- 复核字段变化：falsification_criteria, physical_claims, rationale, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## high/agent/replicate-2/round-2

该轮最佳保留增益：3.8739 pp；保留 `log(q_lsd_p) - log(q_lsd_f)`。

### h1 (connectivity)

- 初稿 `log(1 + q_lsd_p) - log(1 + q_lsd_f)`：passed；
- 复核 `log(q_lsd_p) - log(q_lsd_f)`：passed；
- 最终 `log(q_lsd_p) - log(q_lsd_f)`：scored；边际 +3.8739 pp；保留=True
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `log(1 + q_PMI3) - log(1 + q_PMI1)`：rejected；Redundant with a current input
- 复核 `log(1 + q_PMI3) - log(1 + q_PMI1)`：rejected；Redundant with a current input
- 最终 `((q_PMI1 - q_PMI2)**2 + (q_PMI2 - q_PMI3)**2 + (q_PMI3 - q_PMI1)**2) / (1 + (q_PMI1 + q_PMI2 + q_PMI3)**2 + (q_PMI1 - q_PMI2)**2 + (q_PMI2 - q_PMI3)**2 + (q_PMI3 - q_PMI1)**2)`：rejected；边际 未评分 pp；保留=False
- 复核字段变化：无

### h3 (coupling)

- 初稿 `log(1 + q_Vol) - log(1 + q_lsd_p)`：passed；
- 复核 `log(1 + q_Vol) - log(1 + q_lsd_p)`：passed；
- 最终 `log(1 + q_Vol) - log(1 + q_lsd_p)`：scored；边际 -2.1054 pp；保留=False
- 复核字段变化：无

## high/agent/replicate-2/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (translation)

- 初稿 `log(1 + q_Vol) - log(1 + q_AV)`：passed；
- 复核 `log(1 + q_Vol) - log(1 + q_AV)`：passed；
- 最终 `log(1 + q_Vol) - log(1 + q_AV)`：scored；边际 -5.0030 pp；保留=False
- 复核字段变化：无

### h2 (rotation)

- 初稿 `rotor_case(0, log(1 + q_PMI1 + q_PMI2 + q_PMI3), log(1 + q_PMI1 + q_PMI2 + q_PMI3))`：passed；
- 复核 `rotor_case(0, log(1 + q_PMI1 + q_PMI2 + q_PMI3), log(1 + q_PMI1 + q_PMI2 + q_PMI3))`：passed；
- 最终 `rotor_case(0, log(1 + q_PMI1 + q_PMI2 + q_PMI3), log(1 + q_PMI1 + q_PMI2 + q_PMI3))`：scored；边际 -1.7512 pp；保留=False
- 复核字段变化：无

### h3 (coupling)

- 初稿 `log(1 + q_LabuteASA) - log(1 + q_ASA)`：passed；
- 复核 `log(1 + q_LabuteASA) - log(1 + q_ASA)`：passed；
- 最终 `log(1 + q_LabuteASA) - log(1 + q_ASA)`：scored；边际 -8.4052 pp；保留=False
- 复核字段变化：无

## high/agent/replicate-3/round-1

该轮最佳保留增益：4.0000 pp；保留 `log10(q_Vol / maximum(q_AV, 0.01))`。

### h1 (translation)

- 初稿 `log10(q_Vol / maximum(q_AV, 0.01))`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `log10(q_Vol / maximum(q_AV, 0.01))`：passed；
- 最终 `log10(q_Vol / maximum(q_AV, 0.01))`：scored；边际 +4.0000 pp；保留=True
- 复核字段变化：rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction

### h2 (rotation)

- 初稿 `rotor_case(0, log10(q_PMI3), log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3))`：passed；
- 复核 `rotor_case(0, log10(q_PMI3), log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3))`：passed；
- 最终 `rotor_case(0, log10(q_PMI3), log10(q_PMI3) + (PMI3 - PMI2) / (PMI1 + PMI2 + PMI3))`：scored；边际 -3.9490 pp；保留=False
- 复核字段变化：无

### h3 (connectivity)

- 初稿 `(q_SPAN * q_LabuteASA) / q_lsd_f ** 1`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `(q_SPAN * q_LabuteASA) / q_lsd_f ** 1`：passed；
- 最终 `(q_SPAN * q_LabuteASA) / q_lsd_f ** 1`：scored；边际 -0.6131 pp；保留=False
- 复核字段变化：rationale, scientific_test.descriptor_direction

## high/agent/replicate-3/round-2

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (translation)

- 初稿 `log10(q_Vol / maximum(q_AV, 0.01))`：rejected；Redundant with a current input
- 复核 `log10(q_Vol / maximum(q_AV, 0.01))`：rejected；Redundant with a current input
- 最终 `q_Vol / (q_Vol + maximum(q_AV, 0.01))`：scored；边际 -0.9352 pp；保留=False
- 复核字段变化：无

### h2 (rotation)

- 初稿 `rotor_case(0, log10(q_PMI3), log10(q_PMI3) + log10(q_PMI2))`：passed；
- 复核 `rotor_case(0, -log10(q_PMI3), -(log10(q_PMI3) + log10(q_PMI2)))`：passed；
- 最终 `rotor_case(0, -log10(q_PMI3), -(log10(q_PMI3) + log10(q_PMI2)))`：scored；边际 -2.4296 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (connectivity)

- 初稿 `log10(q_Vol / q_lsd_f ** 3)`：passed；
- 复核 `log10(q_lsd_f ** 3 / q_Vol)`：passed；
- 最终 `log10(q_lsd_f ** 3 / q_Vol)`：scored；边际 -0.8830 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## high/agent/replicate-3/round-3

该轮最佳保留增益：5.0792 pp；保留 `log10(q_lsd_p / q_lsd_f)`。

### h1 (translation)

- 初稿 `log10(q_MW)`：passed；
- 复核 `log10(q_MW)`：passed；
- 最终 `log10(q_MW)`：scored；边际 -0.3991 pp；保留=False
- 复核字段变化：无

### h2 (coupling)

- 初稿 `log10(q_LabuteASA / maximum(q_ASA, 0.01))`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `log10(q_LabuteASA / maximum(q_ASA, 0.01))`：passed；
- 最终 `log10(q_LabuteASA / maximum(q_ASA, 0.01))`：scored；边际 -0.0298 pp；保留=False
- 复核字段变化：scientific_test.descriptor_direction

### h3 (connectivity)

- 初稿 `log10(q_lsd_p / q_lsd_f)`：passed；
- 复核 `log10(q_lsd_p / q_lsd_f)`：passed；
- 最终 `log10(q_lsd_p / q_lsd_f)`：scored；边际 +5.0792 pp；保留=True
- 复核字段变化：无

## high/rag_agent/replicate-1/round-1

该轮最佳保留增益：3.9893 pp；保留 `(q_lsd_f ** 0.5) * (MW_ref / MW ** 1.0) ** 0.25 * (Vol_ref / Vol ** 1.0) ** 0.125`。

### h1 (translation)

- 初稿 `(q_lsd_f ** 0.5) * (MW_ref / MW ** 1.0) ** 0.25 * (Vol_ref / Vol ** 1.0) ** 0.125`：passed；
- 复核 `(q_lsd_f ** 0.5) * (MW_ref / MW ** 1.0) ** 0.25 * (Vol_ref / Vol ** 1.0) ** 0.125`：passed；
- 最终 `(q_lsd_f ** 0.5) * (MW_ref / MW ** 1.0) ** 0.25 * (Vol_ref / Vol ** 1.0) ** 0.125`：scored；边际 +3.9893 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria

### h2 (rotation)

- 初稿 `rotor_case(1.0, (q_PMI2 ** 0.25), ((q_PMI2 * q_PMI3) ** 0.125))`：passed；
- 复核 `rotor_case(1.0, (q_PMI2 ** 0.25), ((q_PMI2 * q_PMI3) ** 0.125))`：passed；
- 最终 `rotor_case(1.0, (q_PMI2 ** 0.25), ((q_PMI2 * q_PMI3) ** 0.125))`：scored；边际 -0.5617 pp；保留=False
- 复核字段变化：evidence_ids, rationale

### h3 (connectivity)

- 初稿 `(q_lsd_p / q_lsd_f) ** 0.5`：passed；
- 复核 `(q_lsd_p / q_lsd_f) ** 0.5`：passed；
- 最终 `(q_lsd_p / q_lsd_f) ** 0.5`：scored；边际 +2.6129 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, rationale

## high/rag_agent/replicate-1/round-2

该轮最佳保留增益：3.1178 pp；保留 `(q_AV ** 0.25) * (q_density ** (-0.125))`。

### h1 (rotation)

- 初稿 `rotor_case(1.0, (q_PMI1 * q_PMI2) ** 0.25, (q_PMI1 * q_PMI2 * q_PMI3) ** 0.33333333)`：passed；
- 复核 `rotor_case(1.0, exp(-((q_PMI1 * q_PMI2) ** 0.5)), exp(-((q_PMI1 * q_PMI2 * q_PMI3) ** 0.33333333)))`：passed；
- 最终 `rotor_case(1.0, exp(-((q_PMI1 * q_PMI2) ** 0.5)), exp(-((q_PMI1 * q_PMI2 * q_PMI3) ** 0.33333333)))`：scored；边际 -0.6981 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

### h2 (connectivity)

- 初稿 `(q_AV ** 0.25) * (q_density ** (-0.125))`：passed；
- 复核 `(q_AV ** 0.25) * (q_density ** (-0.125))`：passed；
- 最终 `(q_AV ** 0.25) * (q_density ** (-0.125))`：scored；边际 +3.1178 pp；保留=True
- 复核字段变化：无

### h3 (coupling)

- 初稿 `(q_ASA ** 0.25) * (q_LabuteASA ** (-0.25))`：passed；
- 复核 `(q_ASA ** 0.25) * (q_LabuteASA ** (-0.25))`：passed；
- 最终 `(q_ASA ** 0.25) * (q_LabuteASA ** (-0.25))`：scored；边际 -3.0901 pp；保留=False
- 复核字段变化：无

## high/rag_agent/replicate-1/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (coupling)

- 初稿 `(q_GeDi ** 0.25) * (q_lsd_f ** (-0.25))`：passed；
- 复核 `(q_GeDi ** 0.25) * (q_lsd_f ** (-0.25))`：passed；
- 最终 `(q_GeDi ** 0.25) * (q_lsd_f ** (-0.25))`：scored；边际 -6.2111 pp；保留=False
- 复核字段变化：无

### h2 (shape)

- 初稿 `q_PBF ** 0.25`：passed；
- 复核 `q_PBF ** 0.25`：passed；
- 最终 `q_PBF ** 0.25`：scored；边际 -6.6297 pp；保留=False
- 复核字段变化：无

### h3 (connectivity)

- 初稿 `q_lsd_p ** 0.25`：passed；
- 复核 `q_lsd_p ** 0.25`：passed；
- 最终 `q_lsd_p ** 0.25`：scored；边际 -5.1158 pp；保留=False
- 复核字段变化：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation

## high/rag_agent/replicate-2/round-1

该轮最佳保留增益：1.2620 pp；保留 `log((q_Vol**(0.3333333333)) / q_lsd_f)`。

### h1 (translation)

- 初稿 `log((q_Vol**(0.3333333333)) / q_lsd_f)`：passed；
- 复核 `log((q_Vol**(0.3333333333)) / q_lsd_f)`：passed；
- 最终 `log((q_Vol**(0.3333333333)) / q_lsd_f)`：scored；边际 +1.2620 pp；保留=True
- 复核字段变化：evidence_ids, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `rotor_case(0.0, log(q_PMI3), log(q_PMI3))`：passed；
- 复核 `rotor_case(0.0, log(q_PMI3), log(q_PMI3))`：passed；
- 最终 `rotor_case(0.0, log(q_PMI3), log(q_PMI3))`：scored；边际 -2.6444 pp；保留=False
- 复核字段变化：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (shape)

- 初稿 `log(q_LabuteASA / (q_Vol**(0.6666666667)))`：passed；
- 复核 `log(q_LabuteASA / (q_Vol**(0.6666666667)))`：passed；
- 最终 `log(q_LabuteASA / (q_Vol**(0.6666666667)))`：scored；边际 -3.2791 pp；保留=False
- 复核字段变化：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## high/rag_agent/replicate-2/round-2

该轮最佳保留增益：4.8979 pp；保留 `log(q_lsd_p / q_lsd_f)`。

### h1 (translation)

- 初稿 `log((q_Vol**(0.3333333333)) / q_lsd_f)`：rejected；Redundant with a current input
- 复核 `log((q_Vol**(0.3333333333)) / q_lsd_f)`：rejected；Redundant with a current input
- 最终 `(Vol**(0.3333333333))/lsd_f`：scored；边际 +0.5131 pp；保留=False
- 复核字段变化：无

### h2 (connectivity)

- 初稿 `log(q_lsd_p / q_lsd_f)`：passed；
- 复核 `log(q_lsd_p / q_lsd_f)`：passed；
- 最终 `log(q_lsd_p / q_lsd_f)`：scored；边际 +4.8979 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (shape)

- 初稿 `log(1.0 + q_PBF)`：passed；
- 复核 `log(1.0 + q_PBF/(q_Vol**(0.3333333333)))`：passed；
- 最终 `log(1.0 + q_PBF/(q_Vol**(0.3333333333)))`：scored；边际 -0.3743 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.Vol

## high/rag_agent/replicate-2/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (translation)

- 初稿 `log((q_Vol**(0.3333333333)) / q_lsd_f)`：rejected；Redundant with a current input
- 复核 `log((q_Vol**(0.3333333333)) / q_lsd_f)`：rejected；Redundant with a current input
- 最终 `(q_Vol**(0.3333333333)) / q_lsd_f`：scored；边际 -2.9392 pp；保留=False
- 复核字段变化：evidence_ids, rationale

### h2 (connectivity)

- 初稿 `log(q_lsd_p / q_lsd_f)`：rejected；Redundant with a current input
- 复核 `log(q_lsd_p / q_lsd_f)`：rejected；Redundant with a current input
- 最终 `q_lsd_p / q_lsd_f`：scored；边际 -4.6989 pp；保留=False
- 复核字段变化：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (coupling)

- 初稿 `rotor_case(0.0, log(q_GeDi / q_lsd_f), log(q_GeDi / q_lsd_f))`：passed；
- 复核 `rotor_case(0.0, log(q_GeDi / q_lsd_f), log(q_GeDi / q_lsd_f))`：passed；
- 最终 `rotor_case(0.0, log(q_GeDi / q_lsd_f), log(q_GeDi / q_lsd_f))`：scored；边际 -2.2706 pp；保留=False
- 复核字段变化：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## high/rag_agent/replicate-3/round-1

该轮最佳保留增益：3.8796 pp；保留 `1 / q_lsd_f**2`。

### h1 (shape)

- 初稿 `log(1 + q_GeDi)`：rejected；Wrong physical variable mapping: GeDi requires heavy_atom_pair_distance
- 复核 `log(1 + q_GeDi)`：passed；
- 最终 `log(1 + q_GeDi)`：scored；边际 -2.8876 pp；保留=False
- 复核字段变化：variable_mappings.GeDi, variable_mappings.q_GeDi

### h2 (connectivity)

- 初稿 `1 / q_lsd_f**2`：rejected；Wrong physical variable mapping: lsd_f requires bottleneck_free_sphere_Df
- 复核 `1 / q_lsd_f**2`：passed；
- 最终 `1 / q_lsd_f**2`：scored；边际 +3.8796 pp；保留=True
- 复核字段变化：variable_mappings.lsd_f, variable_mappings.q_lsd_f

### h3 (translation)

- 初稿 `q_Vol / (q_AV + 1)`：rejected；Wrong physical variable mapping: Vol requires molecular_vdw_volume
- 复核 `q_Vol / (q_AV + 1)`：passed；
- 最终 `q_Vol / (q_AV + 1)`：scored；边际 +0.1555 pp；保留=False
- 复核字段变化：variable_mappings.AV, variable_mappings.Vol, variable_mappings.q_AV, variable_mappings.q_Vol

## high/rag_agent/replicate-3/round-2

该轮最佳保留增益：0.4991 pp；保留 `q_Vol * (lsd_p / lsd_f)**2`。

### h1 (connectivity)

- 初稿 `(lsd_p / lsd_f)**2`：passed；
- 复核 `q_Vol * (lsd_p / lsd_f)**2`：passed；
- 最终 `q_Vol * (lsd_p / lsd_f)**2`：scored；边际 +0.4991 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.Vol

### h2 (translation)

- 初稿 `1 / q_lsd_f**2`：rejected；Redundant with a current input
- 复核 `1 / (1 + q_AV)`：passed；
- 最终 `1 / (1 + q_AV)`：scored；边际 -2.1950 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.AV, variable_mappings.lsd_f

### h3 (coupling)

- 初稿 `q_Vol * q_density`：passed；
- 复核 `q_Vol * q_density`：passed；
- 最终 `q_Vol * q_density`：scored；边际 -1.4102 pp；保留=False
- 复核字段变化：无

## high/rag_agent/replicate-3/round-3

该轮最佳保留增益：1.6275 pp；保留 `sqrt(q_PMI3)`。

### h1 (shape)

- 初稿 `q_Vol * PBF**2`：passed；
- 复核 `q_Vol * PBF**2`：passed；
- 最终 `q_Vol * PBF**2`：scored；边际 -4.2916 pp；保留=False
- 复核字段变化：无

### h2 (translation)

- 初稿 `q_GeDi / lsd_p`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `q_GeDi / q_lsd_p`：passed；
- 最终 `q_GeDi / q_lsd_p`：scored；边际 -2.2819 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

### h3 (rotation)

- 初稿 `sqrt(q_PMI3)`：passed；
- 复核 `sqrt(q_PMI3)`：passed；
- 最终 `sqrt(q_PMI3)`：scored；边际 +1.6275 pp；保留=True
- 复核字段变化：无

## high/small_kg_rag_agent/replicate-1/round-1

该轮最佳保留增益：3.2784 pp；保留 `log(lsd_p / lsd_f)`。

### h1 (connectivity)

- 初稿 `log(lsd_p / lsd_f)`：passed；
- 复核 `log(lsd_p / lsd_f)`：passed；
- 最终 `log(lsd_p / lsd_f)`：scored；边际 +3.2784 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, rationale, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (translation)

- 初稿 `exp(-(AV / AV_ref))`：passed；
- 复核 `exp(-(AV / AV_ref))`：passed；
- 最终 `exp(-(AV / AV_ref))`：scored；边际 +0.2201 pp；保留=False
- 复核字段变化：evidence_ids, rationale

### h3 (rotation)

- 初稿 `rotor_case(1, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 / PMI1_ref) * (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref)))`：passed；
- 复核 `rotor_case(1, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 / PMI1_ref) * (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref)))`：passed；
- 最终 `rotor_case(1, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 / PMI1_ref) * (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref)))`：scored；边际 -2.2146 pp；保留=False
- 复核字段变化：evidence_ids, rationale

## high/small_kg_rag_agent/replicate-1/round-2

该轮最佳保留增益：4.2472 pp；保留 `log(1 + LabuteASA / LabuteASA_ref) - log(1 + ASA / ASA_ref)`。

### h1 (connectivity)

- 初稿 `log(lsd_p / lsd_f)`：rejected；Redundant with a current input
- 复核 `log(lsd_p / lsd_f)`：rejected；Redundant with a current input
- 最终 `log(1 + (lsd_p - lsd_f) / lsd_f_ref)`：scored；边际 -2.4499 pp；保留=False
- 复核字段变化：evidence_ids, rationale

### h2 (shape)

- 初稿 `log(1 + LabuteASA / LabuteASA_ref) - log(1 + ASA / ASA_ref)`：passed；
- 复核 `log(1 + LabuteASA / LabuteASA_ref) - log(1 + ASA / ASA_ref)`：passed；
- 最终 `log(1 + LabuteASA / LabuteASA_ref) - log(1 + ASA / ASA_ref)`：scored；边际 +4.2472 pp；保留=True
- 复核字段变化：无

### h3 (rotation)

- 初稿 `rotor_case(0.0, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 + PMI2 + PMI3) / (PMI1_ref + PMI2_ref + PMI3_ref)))`：passed；
- 复核 `rotor_case(0.0, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 + PMI2 + PMI3) / (PMI1_ref + PMI2_ref + PMI3_ref)))`：passed；
- 最终 `rotor_case(0.0, log(1 + PMI2 / PMI2_ref), log(1 + (PMI1 + PMI2 + PMI3) / (PMI1_ref + PMI2_ref + PMI3_ref)))`：scored；边际 -1.6209 pp；保留=False
- 复核字段变化：evidence_ids, rationale

## high/small_kg_rag_agent/replicate-1/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (translation)

- 初稿 `log(1 + Vol / Vol_ref) - log(1 + AV / AV_ref)`：passed；
- 复核 `log(1 + Vol / Vol_ref) - log(1 + AV / AV_ref)`：passed；
- 最终 `log(1 + Vol / Vol_ref) - log(1 + AV / AV_ref)`：scored；边际 -5.0834 pp；保留=False
- 复核字段变化：无

### h2 (shape)

- 初稿 `log(1 + GeDi / GeDi_ref) - log(1 + lsd_p / lsd_p_ref)`：passed；
- 复核 `log(1 + GeDi / GeDi_ref) - log(1 + lsd_p / lsd_p_ref)`：passed；
- 最终 `log(1 + GeDi / GeDi_ref) - log(1 + lsd_p / lsd_p_ref)`：scored；边际 -7.5253 pp；保留=False
- 复核字段变化：evidence_ids, rationale

### h3 (coupling)

- 初稿 `(PBF / PBF_ref) * log(1 + SPAN / SPAN_ref)`：passed；
- 复核 `(PBF / PBF_ref) * log(1 + SPAN / SPAN_ref)`：passed；
- 最终 `(PBF / PBF_ref) * log(1 + SPAN / SPAN_ref)`：scored；边际 -10.2559 pp；保留=False
- 复核字段变化：scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## high/small_kg_rag_agent/replicate-2/round-1

该轮最佳保留增益：3.2784 pp；保留 `log(q_lsd_p / q_lsd_f)`。

### h1 (translation)

- 初稿 `log(q_Vol) - 2.0 * log(q_lsd_f)`：passed；
- 复核 `2.0 * log(q_lsd_f) - log(q_Vol)`：passed；
- 最终 `2.0 * log(q_lsd_f) - log(q_Vol)`：scored；边际 +0.0498 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `q_PMI3 * q_Vol`：passed；
- 复核 `q_PMI3 * q_Vol`：passed；
- 最终 `q_PMI3 * q_Vol`：scored；边际 +1.2215 pp；保留=False
- 复核字段变化：无

### h3 (connectivity)

- 初稿 `log(q_lsd_p / q_lsd_f)`：passed；
- 复核 `log(q_lsd_p / q_lsd_f)`：passed；
- 最终 `log(q_lsd_p / q_lsd_f)`：scored；边际 +3.2784 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## high/small_kg_rag_agent/replicate-2/round-2

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (translation)

- 初稿 `q_AV / q_Vol`：passed；
- 复核 `q_AV / q_Vol`：passed；
- 最终 `q_AV / q_Vol`：scored；边际 -1.0934 pp；保留=False
- 复核字段变化：evidence_ids

### h2 (rotation)

- 初稿 `rotor_case(1.0, log(1.0 + q_PMI2), log(1.0 + q_PMI3))`：passed；
- 复核 `rotor_case(1.0, log(1.0 + q_PMI2), log(1.0 + q_PMI3))`：passed；
- 最终 `rotor_case(1.0, log(1.0 + q_PMI2), log(1.0 + q_PMI3))`：scored；边际 -4.7354 pp；保留=False
- 复核字段变化：evidence_ids

### h3 (connectivity)

- 初稿 `log(q_lsd_p / q_lsd_f)`：rejected；Redundant with a current input
- 复核 `q_GeDi / q_lsd_p`：passed；
- 最终 `q_GeDi / q_lsd_p`：scored；边际 -0.0432 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.GeDi, variable_mappings.lsd_f

## high/small_kg_rag_agent/replicate-2/round-3

该轮最佳保留增益：4.1902 pp；保留 `log(1.0 + q_PMI3) - log(1.0 + q_PMI1)`。

### h1 (translation)

- 初稿 `q_GeDi / q_lsd_f`：passed；
- 复核 `q_GeDi / q_lsd_f`：passed；
- 最终 `q_GeDi / q_lsd_f`：scored；边际 -1.7316 pp；保留=False
- 复核字段变化：evidence_ids

### h2 (rotation)

- 初稿 `log(1.0 + q_PMI3) - log(1.0 + q_PMI1)`：passed；
- 复核 `log(1.0 + q_PMI3) - log(1.0 + q_PMI1)`：passed；
- 最终 `log(1.0 + q_PMI3) - log(1.0 + q_PMI1)`：scored；边际 +4.1902 pp；保留=True
- 复核字段变化：evidence_ids, scientific_test.boundary_behavior

### h3 (connectivity)

- 初稿 `log(q_lsd_p / q_lsd_f)`：rejected；Redundant with a current input
- 复核 `q_Vol / (q_lsd_p ** 3)`：passed；
- 最终 `q_Vol / (q_lsd_p ** 3)`：scored；边际 +2.0511 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.Vol, variable_mappings.lsd_f

## high/small_kg_rag_agent/replicate-3/round-1

该轮最佳保留增益：3.3509 pp；保留 `log(q_Vol / q_lsd_f**2)`。

### h1 (translation)

- 初稿 `log((q_MW * q_Vol) / q_lsd_f**2)`：passed；
- 复核 `log(q_lsd_f**2 / q_Vol)`：rejected；Formula contradicts its predeclared proxy direction
- 最终 `log(q_Vol / q_lsd_f**2)`：scored；边际 +3.3509 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.MW

### h2 (rotation)

- 初稿 `rotor_case(0.0, log(q_PMI2 * q_PMI3), log(q_PMI2 * q_PMI3) + abs(log(q_PMI3 / q_PMI2)))`：passed；
- 复核 `rotor_case(0.0, log(q_PMI2 * q_PMI3), log(q_PMI2 * q_PMI3) + abs(log(q_PMI3 / q_PMI2)))`：passed；
- 最终 `rotor_case(0.0, log(q_PMI2 * q_PMI3), log(q_PMI2 * q_PMI3) + abs(log(q_PMI3 / q_PMI2)))`：scored；边际 -2.7279 pp；保留=False
- 复核字段变化：无

### h3 (connectivity)

- 初稿 `q_lsd_p / q_lsd_f`：passed；
- 复核 `q_lsd_p / q_lsd_f`：passed；
- 最终 `q_lsd_p / q_lsd_f`：scored；边际 +0.7778 pp；保留=False
- 复核字段变化：falsification_criteria, rationale

## high/small_kg_rag_agent/replicate-3/round-2

该轮最佳保留增益：3.1320 pp；保留 `exp(-q_AV)`。

### h1 (coupling)

- 初稿 `log(q_Vol) * q_density`：passed；
- 复核 `log(q_Vol) * q_density`：passed；
- 最终 `log(q_Vol) * q_density`：scored；边际 -0.0070 pp；保留=False
- 复核字段变化：无

### h2 (rotation)

- 初稿 `rotor_case(0.0, q_PMI2, sqrt(q_PMI2 * q_PMI3))`：rejected；Redundant with a current input
- 复核 `rotor_case(0.0, sqrt(q_PMI2 * q_PMI3) / q_GeDi**2, sqrt(q_PMI2 * q_PMI3) / q_GeDi**2)`：passed；
- 最终 `rotor_case(0.0, sqrt(q_PMI2 * q_PMI3) / q_GeDi**2, sqrt(q_PMI2 * q_PMI3) / q_GeDi**2)`：scored；边际 +0.4140 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.GeDi

### h3 (connectivity)

- 初稿 `exp(-q_AV)`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `exp(-q_AV)`：passed；
- 最终 `exp(-q_AV)`：scored；边际 +3.1320 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## high/small_kg_rag_agent/replicate-3/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (shape)

- 初稿 `log(q_LabuteASA / q_Vol**(2/3))`：passed；
- 复核 `log(q_LabuteASA / q_Vol**(2/3))`：passed；
- 最终 `log(q_LabuteASA / q_Vol**(2/3))`：scored；边际 -7.1537 pp；保留=False
- 复核字段变化：无

### h2 (translation)

- 初稿 `q_MW * exp(-q_lsd_f)`：passed；
- 复核 `q_MW * exp(-q_lsd_f)`：passed；
- 最终 `q_MW * exp(-q_lsd_f)`：scored；边际 -6.5129 pp；保留=False
- 复核字段变化：无

### h3 (rotation)

- 初稿 `rotor_case(0.0, sqrt(q_PMI2 * q_PMI3), (q_PMI1 * q_PMI2 * q_PMI3)**(1/3))`：passed；
- 复核 `rotor_case(0.0, sqrt(q_PMI2 * q_PMI3), (q_PMI1 * q_PMI2 * q_PMI3)**(1/3))`：passed；
- 最终 `rotor_case(0.0, sqrt(q_PMI2 * q_PMI3), (q_PMI1 * q_PMI2 * q_PMI3)**(1/3))`：scored；边际 -9.9503 pp；保留=False
- 复核字段变化：evidence_ids, rationale

## low/agent/replicate-1/round-1

该轮最佳保留增益：2.9866 pp；保留 `-log(AV / AV_ref + 1) * (Vol / Vol_ref)`。

### h1 (translation)

- 初稿 `(MW / MW_ref) * (lsd_f_ref / lsd_f) ** 2`：passed；
- 复核 `(MW / MW_ref) * (lsd_f_ref / lsd_f) ** 2`：passed；
- 最终 `(MW / MW_ref) * (lsd_f_ref / lsd_f) ** 2`：scored；边际 -0.2024 pp；保留=False
- 复核字段变化：无

### h2 (translation)

- 初稿 `log(AV_ref / AV) * (Vol / Vol_ref)`：rejected；Formula undefined on observed training support; use a justified finite proxy or explicit rotor branches
- 复核 `-log(AV / AV_ref + 1) * (Vol / Vol_ref)`：passed；
- 最终 `-log(AV / AV_ref + 1) * (Vol / Vol_ref)`：scored；边际 +2.9866 pp；保留=True
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (rotation)

- 初稿 `rotor_case(PBF / PBF_ref, (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref) ** 0.5, log(SPAN / SPAN_ref + 1) * (LabuteASA / LabuteASA_ref))`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `rotor_case(PBF / PBF_ref, (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref) ** 0.5, log(SPAN / SPAN_ref + 1) * (LabuteASA / LabuteASA_ref))`：passed；
- 最终 `rotor_case(PBF / PBF_ref, (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref) ** 0.5, log(SPAN / SPAN_ref + 1) * (LabuteASA / LabuteASA_ref))`：scored；边际 -2.9629 pp；保留=False
- 复核字段变化：rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.regime_input, scientific_test.vary_input

## low/agent/replicate-1/round-2

该轮最佳保留增益：2.9573 pp；保留 `(Vol / Vol_ref) * (lsd_p_ref / lsd_p)`。

### h1 (translation)

- 初稿 `(Vol / Vol_ref) * (lsd_p_ref / lsd_p)`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `(Vol / Vol_ref) * (lsd_p_ref / lsd_p)`：passed；
- 最终 `(Vol / Vol_ref) * (lsd_p_ref / lsd_p)`：scored；边际 +2.9573 pp；保留=True
- 复核字段变化：falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (connectivity)

- 初稿 `log(LabuteASA / LabuteASA_ref + 1) * (density / density_ref) ** 2`：passed；
- 复核 `log(LabuteASA / LabuteASA_ref + 1) * (density / density_ref) ** 2`：passed；
- 最终 `log(LabuteASA / LabuteASA_ref + 1) * (density / density_ref) ** 2`：scored；边际 +0.7216 pp；保留=False
- 复核字段变化：无

### h3 (rotation)

- 初稿 `rotor_case(SPAN / SPAN_ref, (PMI2 / PMI2_ref) * (PMI3 / PMI3_ref) ** -0.5, (PMI3 / PMI3_ref) ** 0.5 * (GeDi / GeDi_ref))`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `rotor_case(SPAN / SPAN_ref, (PMI2 / PMI2_ref) ** -0.5 * (PMI3 / PMI3_ref) ** 0.5, (PMI3 / PMI3_ref) ** 0.5 * (GeDi / GeDi_ref))`：passed；
- 最终 `rotor_case(SPAN / SPAN_ref, (PMI2 / PMI2_ref) ** -0.5 * (PMI3 / PMI3_ref) ** 0.5, (PMI3 / PMI3_ref) ** 0.5 * (GeDi / GeDi_ref))`：scored；边际 -0.1910 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/agent/replicate-1/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (translation)

- 初稿 `log(SPAN / SPAN_ref + 1) * (lsd_f_ref / lsd_f)`：passed；
- 复核 `-log(SPAN / SPAN_ref + 1) * (lsd_f_ref / lsd_f)`：passed；
- 最终 `-log(SPAN / SPAN_ref + 1) * (lsd_f_ref / lsd_f)`：scored；边际 -10.4245 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (shape)

- 初稿 `(Vol / Vol_ref) * (AV_ref / (AV + AV_ref))`：passed；
- 复核 `-(Vol / Vol_ref) * (AV_ref / (AV + AV_ref))`：passed；
- 最终 `-(Vol / Vol_ref) * (AV_ref / (AV + AV_ref))`：scored；边际 -10.6640 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (rotation)

- 初稿 `rotor_case(0, (PMI2 / PMI2_ref) * (lsd_p_ref / lsd_p) ** 2, (PMI2 * PMI3 / (PMI2_ref * PMI3_ref)) ** 0.25 * (lsd_p_ref / lsd_p))`：passed；
- 复核 `rotor_case(0, -(PMI2 / PMI2_ref) * (lsd_p_ref / lsd_p) ** 2, -(PMI2 * PMI3 / (PMI2_ref * PMI3_ref)) ** 0.25 * (lsd_p_ref / lsd_p))`：passed；
- 最终 `rotor_case(0, -(PMI2 / PMI2_ref) * (lsd_p_ref / lsd_p) ** 2, -(PMI2 * PMI3 / (PMI2_ref * PMI3_ref)) ** 0.25 * (lsd_p_ref / lsd_p))`：scored；边际 -7.8311 pp；保留=False
- 复核字段变化：falsification_criteria, formula, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/agent/replicate-2/round-1

该轮最佳保留增益：2.8962 pp；保留 `q_AV / (q_LabuteASA ** 0.5)`。

### h1 (translation)

- 初稿 `q_Vol * exp(-(q_lsd_f))`：passed；
- 复核 `q_Vol * exp(-(q_lsd_f))`：passed；
- 最终 `q_Vol * exp(-(q_lsd_f))`：scored；边际 +1.8376 pp；保留=False
- 复核字段变化：无

### h2 (rotation)

- 初稿 `rotor_case(0, log1p_stub_rejected, log((q_PMI3 * q_PMI2 + 1) ) / (q_PMI2 + 1))`：rejected；Unsupported formula symbol or syntax
- 复核 `rotor_case(0, 1, log(q_PMI2 * q_PMI3 + 1) / (q_PMI2 + 1))`：passed；
- 最终 `rotor_case(0, 1, log(q_PMI2 * q_PMI3 + 1) / (q_PMI2 + 1))`：scored；边际 -6.7498 pp；保留=False
- 复核字段变化：formula, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (coupling)

- 初稿 `q_AV / (q_LabuteASA ** 0.5)`：passed；
- 复核 `q_AV / (q_LabuteASA ** 0.5)`：passed；
- 最终 `q_AV / (q_LabuteASA ** 0.5)`：scored；边际 +2.8962 pp；保留=True
- 复核字段变化：无

## low/agent/replicate-2/round-2

该轮最佳保留增益：2.8214 pp；保留 `q_LabuteASA * exp(-q_ASA)`。

### h1 (translation)

- 初稿 `q_lsd_f / (q_Vol ** (1/3))`：passed；
- 复核 `(q_Vol ** (1/3)) / q_lsd_f`：passed；
- 最终 `(q_Vol ** (1/3)) / q_lsd_f`：scored；边际 +0.4860 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `q_PBF * q_LabuteASA`：passed；
- 复核 `exp(-(q_PBF * q_LabuteASA))`：passed；
- 最终 `exp(-(q_PBF * q_LabuteASA))`：scored；边际 -0.5362 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (connectivity)

- 初稿 `q_ASA / q_LabuteASA`：passed；
- 复核 `q_LabuteASA * exp(-q_ASA)`：passed；
- 最终 `q_LabuteASA * exp(-q_ASA)`：scored；边际 +2.8214 pp；保留=True
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/agent/replicate-2/round-3

该轮最佳保留增益：0.7851 pp；保留 `rotor_case(0, log(q_PMI2 + 1) / q_LabuteASA, log(q_PMI2 + 1) / q_LabuteASA)`。

### h1 (connectivity)

- 初稿 `(q_Vol ** (1/3)) / q_lsd_p`：passed；
- 复核 `q_lsd_p / (q_Vol ** (1/3))`：passed；
- 最终 `q_lsd_p / (q_Vol ** (1/3))`：scored；边际 -4.7083 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `log(q_PMI2 + 1) / q_LabuteASA`：rejected；Nonlinear rotor expressions require explicit single-site/linear/nonlinear branches
- 复核 `rotor_case(0, log(q_PMI2 + 1) / q_LabuteASA, log(q_PMI2 + 1) / q_LabuteASA)`：passed；
- 最终 `rotor_case(0, log(q_PMI2 + 1) / q_LabuteASA, log(q_PMI2 + 1) / q_LabuteASA)`：scored；边际 +0.7851 pp；保留=True
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (coupling)

- 初稿 `(q_ASA * q_density) / q_LabuteASA`：passed；
- 复核 `q_LabuteASA / (q_ASA * q_density + 1)`：passed；
- 最终 `q_LabuteASA / (q_ASA * q_density + 1)`：scored；边际 -5.5048 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/agent/replicate-3/round-1

该轮最佳保留增益：3.2784 pp；保留 `log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref)`。

### h1 (connectivity)

- 初稿 `log(lsd_f / lsd_f_ref) - log(lsd_p / lsd_p_ref)`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref)`：passed；
- 最终 `log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref)`：scored；边际 +3.2784 pp；保留=True
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (shape)

- 初稿 `log(SPAN / SPAN_ref) + log(GeDi / GeDi_ref) - log(Vol / Vol_ref)`：rejected；Formula undefined on observed training support; use a justified finite proxy or explicit rotor branches
- 复核 `log(1 + SPAN / SPAN_ref) + log(1 + GeDi / GeDi_ref) - log(Vol / Vol_ref)`：passed；
- 最终 `log(1 + SPAN / SPAN_ref) + log(1 + GeDi / GeDi_ref) - log(Vol / Vol_ref)`：scored；边际 +1.0383 pp；保留=False
- 复核字段变化：formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (translation)

- 初稿 `log((AV / AV_ref) / (density / density_ref))`：rejected；Formula undefined on observed training support; use a justified finite proxy or explicit rotor branches
- 复核 `log(1 + AV / AV_ref) - log(density / density_ref)`：passed；
- 最终 `log(1 + AV / AV_ref) - log(density / density_ref)`：scored；边际 +2.4840 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/agent/replicate-3/round-2

该轮最佳保留增益：4.1983 pp；保留 `-(log(1 + ASA/ASA_ref) + log(1 + LabuteASA/LabuteASA_ref))`。

### h1 (connectivity)

- 初稿 `log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref)`：rejected；Redundant with a current input
- 复核 `log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref) + log(1 + Vol / Vol_ref)`：passed；
- 最终 `log(lsd_p / lsd_p_ref) - log(lsd_f / lsd_f_ref) + log(1 + Vol / Vol_ref)`：scored；边际 -0.8917 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.vary_input, variable_mappings.Vol, variable_mappings.Vol_ref, variable_mappings.lsd_f_ref, variable_mappings.lsd_p_ref

### h2 (rotation)

- 初稿 `rotor_case(log(1 + 1e-6/PMI2_ref), log(1 + PMI2/PMI2_ref) - log(1 + PMI1/PMI1_ref), log(1 + (PMI2 + PMI3)/(PMI2_ref + PMI3_ref)) - 2*log(1 + PMI1/PMI1_ref))`：rejected；Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references
- 复核 `rotor_case(0, log(1 + PMI2/PMI2_ref) - log(1 + PMI1/PMI1_ref), log(1 + (PMI2 + PMI3)/(PMI2_ref + PMI3_ref)) - 2*log(1 + PMI1/PMI1_ref))`：passed；
- 最终 `rotor_case(0, log(1 + PMI2/PMI2_ref) - log(1 + PMI1/PMI1_ref), log(1 + (PMI2 + PMI3)/(PMI2_ref + PMI3_ref)) - 2*log(1 + PMI1/PMI1_ref))`：scored；边际 -1.0731 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.PMI1_ref, variable_mappings.PMI2_ref, variable_mappings.PMI3_ref

### h3 (coupling)

- 初稿 `log(1 + ASA/ASA_ref) + log(1 + LabuteASA/LabuteASA_ref)`：passed；
- 复核 `-(log(1 + ASA/ASA_ref) + log(1 + LabuteASA/LabuteASA_ref))`：passed；
- 最终 `-(log(1 + ASA/ASA_ref) + log(1 + LabuteASA/LabuteASA_ref))`：scored；边际 +4.1983 pp；保留=True
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.ASA_ref, variable_mappings.LabuteASA_ref

## low/agent/replicate-3/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (shape)

- 初稿 `-log(1 + PBF / PBF_ref)`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `log(1 + PBF / PBF_ref)`：passed；
- 最终 `log(1 + PBF / PBF_ref)`：scored；边际 -9.1429 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `log(1 + PMI3 / PMI3_ref) - log(1 + PMI2 / PMI2_ref)`：rejected；Nonlinear rotor expressions require explicit single-site/linear/nonlinear branches
- 复核 `rotor_case(0, 0, log(1 + PMI3 / PMI3_ref) - log(1 + PMI2 / PMI2_ref))`：passed；
- 最终 `rotor_case(0, 0, log(1 + PMI3 / PMI3_ref) - log(1 + PMI2 / PMI2_ref))`：scored；边际 -5.9602 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (connectivity)

- 初稿 `log(1 + ASA / ASA_ref) - log(1 + AV / AV_ref)`：passed；
- 复核 `-(log(1 + ASA / ASA_ref) - log(1 + AV / AV_ref))`：passed；
- 最终 `-(log(1 + ASA / ASA_ref) - log(1 + AV / AV_ref))`：scored；边际 -2.3437 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/rag_agent/replicate-1/round-1

该轮最佳保留增益：5.6485 pp；保留 `q_AV / q_Vol`。

### h1 (translation)

- 初稿 `log( (lsd_f / 5.16326) * (lsd_p / 6.38663) )`：rejected；log requires a dimensionless argument; divide by a matching reference
- 复核 `log( (lsd_f / 5.16326) * (lsd_p / 6.38663) )`：rejected；log requires a dimensionless argument; divide by a matching reference
- 最终 `log(q_lsd_f * q_lsd_p)`：rejected；边际 未评分 pp；保留=False
- 复核字段变化：evidence_ids, rationale

### h2 (rotation)

- 初稿 `rotor_case( log(1 + (PMI1 / 43.29513794)**0.5), log(1 + (PMI2 / 93.79729089)**0.5), log(1 + (PMI3 / 125.4948325)**0.5) )`：rejected；Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references
- 复核 `rotor_case( log(1 + (PMI1 / 43.29513794)**0.5), log(1 + (PMI2 / 93.79729089)**0.5), log(1 + (PMI3 / 125.4948325)**0.5) )`：rejected；Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references
- 最终 `rotor_case( q_PMI1**0.5, q_PMI2**0.5, q_PMI3**0.5 )`：scored；边际 -2.6817 pp；保留=False
- 复核字段变化：evidence_ids, rationale

### h3 (shape)

- 初稿 `log(1 + (AV / 0.0759781)) - log(1 + (Vol / 67.24))`：rejected；Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references
- 复核 `log(1 + (AV / 0.0759781)) - log(1 + (Vol / 67.24))`：rejected；Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references
- 最终 `q_AV / q_Vol`：scored；边际 +5.6485 pp；保留=True
- 复核字段变化：evidence_ids, rationale

## low/rag_agent/replicate-1/round-2

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (translation)

- 初稿 `log(q_Vol) - log(q_lsd_f)`：passed；
- 复核 `log(q_lsd_f) - log(q_Vol)`：passed；
- 最终 `log(q_lsd_f) - log(q_Vol)`：scored；边际 -2.0222 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

### h2 (rotation)

- 初稿 `rotor_case( q_SPAN, q_SPAN, q_SPAN * q_PBF )`：passed；
- 复核 `rotor_case( q_SPAN, q_SPAN, q_SPAN * (1 - q_PBF) )`：passed；
- 最终 `rotor_case( q_SPAN, q_SPAN, q_SPAN * (1 - q_PBF) )`：scored；边际 -3.7404 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (connectivity)

- 初稿 `q_AV * q_lsd_p`：passed；
- 复核 `q_AV * q_lsd_p`：passed；
- 最终 `q_AV * q_lsd_p`：scored；边际 -2.4394 pp；保留=False
- 复核字段变化：无

## low/rag_agent/replicate-1/round-3

该轮最佳保留增益：0.1507 pp；保留 `q_LabuteASA / q_Vol`。

### h1 (translation)

- 初稿 `log(q_lsd_f) - log(q_SPAN + 0.1)`：passed；
- 复核 `log(q_lsd_f) - log(q_SPAN + 0.1)`：passed；
- 最终 `log(q_lsd_f) - log(q_SPAN + 0.1)`：scored；边际 -4.2839 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `q_LabuteASA / q_Vol`：passed；
- 复核 `q_LabuteASA / q_Vol`：passed；
- 最终 `q_LabuteASA / q_Vol`：scored；边际 +0.1507 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (shape)

- 初稿 `rotor_case( q_PBF, q_SPAN, q_PBF * q_SPAN )`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `rotor_case( q_SPAN, q_SPAN, q_PBF * q_SPAN )`：passed；
- 最终 `rotor_case( q_SPAN, q_SPAN, q_PBF * q_SPAN )`：scored；边际 -3.3540 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/rag_agent/replicate-2/round-1

该轮最佳保留增益：4.8844 pp；保留 `q_PBF * sqrt(q_SPAN * q_GeDi) / maximum(q_ASA, 0.01)`。

### h1 (translation)

- 初稿 `log(q_lsd_f * q_Vol / q_MW)`：rejected；Wrong physical variable mapping: Vol requires molecular_vdw_volume
- 复核 `log(q_lsd_f * q_AV / q_MW)`：rejected；Formula undefined on observed training support; use a justified finite proxy or explicit rotor branches
- 最终 `log(q_lsd_f / q_MW) + q_AV`：scored；边际 +0.4952 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `rotor_case(log(q_MW), log(q_MW) - 0.2 * q_PMI2 / q_PMI3, log(q_MW) - 0.2 * q_PMI2 / q_PMI3)`：passed；
- 复核 `rotor_case(log(q_MW), log(q_MW), log(q_MW) - 0.2 * q_PMI2 / q_PMI3)`：passed；
- 最终 `rotor_case(log(q_MW), log(q_MW), log(q_MW) - 0.2 * q_PMI2 / q_PMI3)`：scored；边际 -6.7728 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (shape)

- 初稿 `q_PBF * sqrt(q_SPAN * q_GeDi) / q_ASA`：rejected；Formula undefined on observed training support; use a justified finite proxy or explicit rotor branches
- 复核 `q_PBF * sqrt(q_SPAN * q_GeDi) / maximum(q_ASA, 0.01)`：passed；
- 最终 `q_PBF * sqrt(q_SPAN * q_GeDi) / maximum(q_ASA, 0.01)`：scored；边际 +4.8844 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/rag_agent/replicate-2/round-2

该轮最佳保留增益：2.1358 pp；保留 `q_Vol * q_LabuteASA * q_AV`。

### h1 (translation)

- 初稿 `log(q_MW) * q_lsd_f / maximum(q_lsd_p, 0.5)`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `log(q_lsd_f / q_MW) + q_AV`：passed；
- 最终 `log(q_lsd_f / q_MW) + q_AV`：scored；边际 +0.6217 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.AV, variable_mappings.lsd_p

### h2 (rotation)

- 初稿 `rotor_case(log(q_Vol), log(q_Vol) - 0.1 * q_PMI1 / q_PMI3, log(q_Vol) - 0.1 * q_PMI1 / q_PMI3)`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `rotor_case(log(q_Vol), log(q_Vol) + 0.1 * q_PMI1 / q_PMI3, log(q_Vol) + 0.1 * q_PMI1 / q_PMI3)`：passed；
- 最终 `rotor_case(log(q_Vol), log(q_Vol) + 0.1 * q_PMI1 / q_PMI3, log(q_Vol) + 0.1 * q_PMI1 / q_PMI3)`：scored；边际 -5.0349 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (coupling)

- 初稿 `q_Vol * q_LabuteASA / maximum(q_AV, 0.05)`：passed；
- 复核 `q_Vol * q_LabuteASA * q_AV`：passed；
- 最终 `q_Vol * q_LabuteASA * q_AV`：scored；边际 +2.1358 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/rag_agent/replicate-2/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (translation)

- 初稿 `q_Vol / q_lsd_f`：passed；
- 复核 `q_Vol / q_lsd_f`：passed；
- 最终 `q_Vol / q_lsd_f`：scored；边际 -5.4276 pp；保留=False
- 复核字段变化：无

### h2 (rotation)

- 初稿 `rotor_case(q_LabuteASA / q_lsd_p, q_LabuteASA / q_lsd_p, q_LabuteASA / q_lsd_p)`：passed；
- 复核 `q_LabuteASA / q_lsd_p`：passed；
- 最终 `q_LabuteASA / q_lsd_p`：scored；边际 -4.2393 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (shape)

- 初稿 `q_PBF * q_GeDi / (q_ASA + 0.5)`：passed；
- 复核 `q_PBF * q_GeDi / (q_ASA + 0.5)`：passed；
- 最终 `q_PBF * q_GeDi / (q_ASA + 0.5)`：scored；边际 -4.7798 pp；保留=False
- 复核字段变化：无

## low/rag_agent/replicate-3/round-1

该轮最佳保留增益：1.2112 pp；保留 `((Vol / Vol_ref) ** 0.5) * (1 + AV_ref / maximum(AV, AV_ref))`。

### h1 (translation)

- 初稿 `log(1 + q_lsd_f) * (MW / MW_ref) ** 0.5`：passed；
- 复核 `log(1 + q_lsd_f) * (MW / MW_ref) ** 0.5`：passed；
- 最终 `log(1 + q_lsd_f) * (MW / MW_ref) ** 0.5`：scored；边际 -3.0575 pp；保留=False
- 复核字段变化：无

### h2 (connectivity)

- 初稿 `log(1 + AV/AV_ref) / (Vol / Vol_ref) ** 0.5`：passed；
- 复核 `((Vol / Vol_ref) ** 0.5) / log(1 + AV / AV_ref)`：rejected；Formula undefined on observed training support; use a justified finite proxy or explicit rotor branches
- 最终 `((Vol / Vol_ref) ** 0.5) * (1 + AV_ref / maximum(AV, AV_ref))`：scored；边际 +1.2112 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, formula, novelty_status, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (rotation)

- 初稿 `rotor_case(log(1 + q_SPAN), log(1 + (SPAN/SPAN_ref) * (PBF/PBF_ref + 1)), log(1 + (SPAN/SPAN_ref) ** 2 * (PMI3/PMI3_ref) ** 0.25))`：passed；
- 复核 `rotor_case(log(1 + q_SPAN), log(1 + (SPAN/SPAN_ref) * (PBF/PBF_ref + 1)), log(1 + (SPAN/SPAN_ref) ** 2 * (PMI3/PMI3_ref) ** 0.25))`：passed；
- 最终 `rotor_case(log(1 + q_SPAN), log(1 + (SPAN/SPAN_ref) * (PBF/PBF_ref + 1)), log(1 + (SPAN/SPAN_ref) ** 2 * (PMI3/PMI3_ref) ** 0.25))`：scored；边际 -2.6590 pp；保留=False
- 复核字段变化：无

## low/rag_agent/replicate-3/round-2

该轮最佳保留增益：6.5900 pp；保留 `1 / (log(1 + q_LabuteASA) * sqrt(1 + SPAN / SPAN_ref))`。

### h1 (shape)

- 初稿 `log(1 + q_LabuteASA) * sqrt(1 + SPAN / SPAN_ref)`：passed；
- 复核 `1 / (log(1 + q_LabuteASA) * sqrt(1 + SPAN / SPAN_ref))`：passed；
- 最终 `1 / (log(1 + q_LabuteASA) * sqrt(1 + SPAN / SPAN_ref))`：scored；边际 +6.5900 pp；保留=True
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (translation)

- 初稿 `((Vol / Vol_ref) ** 0.5) * (1 + AV_ref / maximum(AV, AV_ref))`：rejected；Redundant with a current input
- 复核 `((Vol / Vol_ref) ** 0.5) * (1 + ASA_ref / maximum(ASA, ASA_ref))`：passed；
- 最终 `((Vol / Vol_ref) ** 0.5) * (1 + ASA_ref / maximum(ASA, ASA_ref))`：scored；边际 +0.2341 pp；保留=False
- 复核字段变化：falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.vary_input, variable_mappings.ASA, variable_mappings.AV

### h3 (connectivity)

- 初稿 `(lsd_p / lsd_p_ref) / (1 + lsd_f / lsd_f_ref)`：passed；
- 复核 `(1 + lsd_f / lsd_f_ref) * (lsd_p_ref / lsd_p)`：passed；
- 最终 `(1 + lsd_f / lsd_f_ref) * (lsd_p_ref / lsd_p)`：scored；边际 +5.0358 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input

## low/rag_agent/replicate-3/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (coupling)

- 初稿 `(density / density_ref) * (1 + (Vol / Vol_ref) ** 0.5)`：passed；
- 复核 `(density / density_ref) * (1 + (Vol / Vol_ref) ** 0.5)`：passed；
- 最终 `(density / density_ref) * (1 + (Vol / Vol_ref) ** 0.5)`：scored；边际 -14.9612 pp；保留=False
- 复核字段变化：无

### h2 (translation)

- 初稿 `log(1 + MW / MW_ref) * (lsd_p / lsd_p_ref)`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `log(1 + MW / MW_ref) * (lsd_p_ref / lsd_p)`：passed；
- 最终 `log(1 + MW / MW_ref) * (lsd_p_ref / lsd_p)`：scored；边际 -9.3529 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (connectivity)

- 初稿 `sqrt(1 + GeDi / GeDi_ref) * (1 + lsd_f_ref / lsd_f) * (lsd_p / lsd_p_ref)`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `sqrt(1 + GeDi / GeDi_ref) * (1 + lsd_f / lsd_f_ref) * (lsd_p_ref / lsd_p)`：passed；
- 最终 `sqrt(1 + GeDi / GeDi_ref) * (1 + lsd_f / lsd_f_ref) * (lsd_p_ref / lsd_p)`：scored；边际 -5.6307 pp；保留=False
- 复核字段变化：evidence_ids, formula, rationale, scientific_test.boundary_behavior

## low/small_kg_rag_agent/replicate-1/round-1

该轮最佳保留增益：2.8960 pp；保留 `(AV/AV_ref) * ((LabuteASA/LabuteASA_ref) / (GeDi/GeDi_ref + 0.5))`。

### h1 (translation)

- 初稿 `log(1 + (Vol/Vol_ref) * (lsd_f/lsd_f_ref)**-2) - (lsd_f/lsd_f_ref)`：passed；
- 复核 `log(1 + (Vol/Vol_ref) * (lsd_f/lsd_f_ref)**-2) - (lsd_f/lsd_f_ref)`：passed；
- 最终 `log(1 + (Vol/Vol_ref) * (lsd_f/lsd_f_ref)**-2) - (lsd_f/lsd_f_ref)`：scored；边际 +0.6576 pp；保留=False
- 复核字段变化：evidence_ids, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `rotor_case(log(1 + 1e-8), log(1 + (PMI2/PMI2_ref)**0.5 / (SPAN/SPAN_ref + 1.0)), log(1 + (PMI3/PMI3_ref)**0.5 / (SPAN/SPAN_ref + 1.0)))`：passed；
- 复核 `rotor_case(log(1 + 1e-8), log(1 + (PMI2/PMI2_ref)**0.5 / (SPAN/SPAN_ref + 1.0)), log(1 + (PMI3/PMI3_ref)**0.5 / (SPAN/SPAN_ref + 1.0)))`：passed；
- 最终 `rotor_case(log(1 + 1e-8), log(1 + (PMI2/PMI2_ref)**0.5 / (SPAN/SPAN_ref + 1.0)), log(1 + (PMI3/PMI3_ref)**0.5 / (SPAN/SPAN_ref + 1.0)))`：scored；边际 -2.9185 pp；保留=False
- 复核字段变化：无

### h3 (shape)

- 初稿 `(AV/AV_ref) * ((LabuteASA/LabuteASA_ref) / (GeDi/GeDi_ref + 0.5))`：passed；
- 复核 `(AV/AV_ref) * ((LabuteASA/LabuteASA_ref) / (GeDi/GeDi_ref + 0.5))`：passed；
- 最终 `(AV/AV_ref) * ((LabuteASA/LabuteASA_ref) / (GeDi/GeDi_ref + 0.5))`：scored；边际 +2.8960 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/small_kg_rag_agent/replicate-1/round-2

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (connectivity)

- 初稿 `log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)`：passed；
- 复核 `log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)`：passed；
- 最终 `log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)`：scored；边际 -0.0243 pp；保留=False
- 复核字段变化：无

### h2 (rotation)

- 初稿 `rotor_case(0.0, log(1 + (PMI2/maximum(PMI1, 1.0)))**0.5, log(1 + (PMI2/maximum(PMI1, 1.0)))**0.5 + log(1 + (PMI3/maximum(PMI2, 1.0)))**0.5)`：rejected；Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references
- 复核 `rotor_case(0.0, (q_PMI2/maximum(q_PMI1, 0.001))**0.5, (q_PMI2/maximum(q_PMI1, 0.001))**0.5 + (q_PMI3/maximum(q_PMI2, 0.001))**0.5)`：passed；
- 最终 `rotor_case(0.0, (q_PMI2/maximum(q_PMI1, 0.001))**0.5, (q_PMI2/maximum(q_PMI1, 0.001))**0.5 + (q_PMI3/maximum(q_PMI2, 0.001))**0.5)`：scored；边际 -0.3559 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (shape)

- 初稿 `(ASA/ASA_ref) / (MW/MW_ref)`：rejected；Wrong physical variable mapping: MW requires adsorbate_geometry_proxy
- 复核 `(ASA/ASA_ref) / (MW/MW_ref)`：passed；
- 最终 `(ASA/ASA_ref) / (MW/MW_ref)`：scored；边际 -0.9123 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.MW

## low/small_kg_rag_agent/replicate-1/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (connectivity)

- 初稿 `(lsd_p/lsd_p_ref) - (lsd_f/lsd_f_ref)`：passed；
- 复核 `log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)`：passed；
- 最终 `log(1 + (lsd_p/lsd_p_ref) * (lsd_f/lsd_f_ref) * (Vol/Vol_ref)**-0.5)`：scored；边际 -0.0243 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.Vol

### h2 (shape)

- 初稿 `log(1 + (Vol/Vol_ref) * (PBF/PBF_ref + 0.1))`：passed；
- 复核 `log(1 + (Vol/Vol_ref) * (PBF/PBF_ref + 0.1))`：passed；
- 最终 `log(1 + (Vol/Vol_ref) * (PBF/PBF_ref + 0.1))`：scored；边际 -2.3431 pp；保留=False
- 复核字段变化：无

### h3 (rotation)

- 初稿 `rotor_case(log(1 + q_PMI1), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5))`：passed；
- 复核 `rotor_case(0.0, log(1 + (PMI2/PMI2_ref)**0.5), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5))`：passed；
- 最终 `rotor_case(0.0, log(1 + (PMI2/PMI2_ref)**0.5), log(1 + (q_PMI2/maximum(q_PMI1, 1e-10))**0.5))`：scored；边际 -3.3435 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/small_kg_rag_agent/replicate-2/round-1

该轮最佳保留增益：1.4205 pp；保留 `log((LabuteASA/LabuteASA_ref) / (AV/AV_ref + 1))`。

### h1 (coupling)

- 初稿 `log((Vol/Vol_ref) ** 2 * (lsd_f/lsd_f_ref))`：rejected；Formula contradicts its predeclared proxy direction
- 复核 `log((Vol/Vol_ref) ** 2 / (lsd_f/lsd_f_ref))`：passed；
- 最终 `log((Vol/Vol_ref) ** 2 / (lsd_f/lsd_f_ref))`：scored；边际 -3.6895 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `rotor_case(log1p_style_placeholder_removed, log1p_style_placeholder_removed, log((PBF/PBF_ref) ** 2 + 1))`：rejected；Unsupported formula symbol or syntax
- 复核 `rotor_case(0, log((PBF/PBF_ref) ** 2 + 1), log((PBF/PBF_ref) ** 2 + 1))`：passed；
- 最终 `rotor_case(0, log((PBF/PBF_ref) ** 2 + 1), log((PBF/PBF_ref) ** 2 + 1))`：scored；边际 -4.7143 pp；保留=False
- 复核字段变化：evidence_ids, formula, rationale, scientific_test.boundary_behavior, scientific_test.proxy_assumptions

### h3 (coupling)

- 初稿 `log((LabuteASA/LabuteASA_ref) / (AV/AV_ref + 1))`：passed；
- 复核 `log((LabuteASA/LabuteASA_ref) / (AV/AV_ref + 1))`：passed；
- 最终 `log((LabuteASA/LabuteASA_ref) / (AV/AV_ref + 1))`：scored；边际 +1.4205 pp；保留=True
- 复核字段变化：evidence_ids

## low/small_kg_rag_agent/replicate-2/round-2

该轮最佳保留增益：0.2994 pp；保留 `log(1 + (Vol/Vol_ref) * (lsd_p/lsd_p_ref) ** -2)`。

### h1 (translation)

- 初稿 `log(1 + (Vol/Vol_ref) * (lsd_p/lsd_p_ref) ** -2)`：passed；
- 复核 `log(1 + (Vol/Vol_ref) * (lsd_p/lsd_p_ref) ** -2)`：passed；
- 最终 `log(1 + (Vol/Vol_ref) * (lsd_p/lsd_p_ref) ** -2)`：scored；边际 +0.2994 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (shape)

- 初稿 `log(1 + (GeDi/GeDi_ref) * (LabuteASA/LabuteASA_ref) / (1 + (PBF/PBF_ref)))`：passed；
- 复核 `log(1 + (GeDi/GeDi_ref) * (LabuteASA/LabuteASA_ref) / (1 + (PBF/PBF_ref)))`：passed；
- 最终 `log(1 + (GeDi/GeDi_ref) * (LabuteASA/LabuteASA_ref) / (1 + (PBF/PBF_ref)))`：scored；边际 -0.1322 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (rotation)

- 初稿 `rotor_case(log(1 + (LabuteASA/LabuteASA_ref)), log(1 + (PMI2/PMI2_ref) * (LabuteASA/LabuteASA_ref) ** -1), log(1 + (PMI3/PMI3_ref) * (LabuteASA/LabuteASA_ref) ** -1))`：passed；
- 复核 `rotor_case(log(1 + (LabuteASA/LabuteASA_ref)), log(1 + (PMI2/PMI2_ref) * (LabuteASA/LabuteASA_ref) ** -1), log(1 + (PMI3/PMI3_ref) * (LabuteASA/LabuteASA_ref) ** -1))`：passed；
- 最终 `rotor_case(log(1 + (LabuteASA/LabuteASA_ref)), log(1 + (PMI2/PMI2_ref) * (LabuteASA/LabuteASA_ref) ** -1), log(1 + (PMI3/PMI3_ref) * (LabuteASA/LabuteASA_ref) ** -1))`：scored；边际 -2.5034 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/small_kg_rag_agent/replicate-2/round-3

该轮最佳保留增益：0.9612 pp；保留 `log(1 + (ASA/ASA_ref) * (density/density_ref) ** 1)`。

### h1 (coupling)

- 初稿 `log(1 + (LabuteASA/LabuteASA_ref) * (lsd_f/lsd_f_ref) ** -1)`：passed；
- 复核 `log(1 + (LabuteASA/LabuteASA_ref) * (lsd_f/lsd_f_ref) ** -1)`：passed；
- 最终 `log(1 + (LabuteASA/LabuteASA_ref) * (lsd_f/lsd_f_ref) ** -1)`：scored；边际 -1.5272 pp；保留=False
- 复核字段变化：evidence_ids, rationale

### h2 (rotation)

- 初稿 `log(1 + (Vol/Vol_ref) * (PBF/PBF_ref) ** 2)`：passed；
- 复核 `log(1 + (Vol/Vol_ref) * (PBF/PBF_ref) ** 2)`：passed；
- 最终 `log(1 + (Vol/Vol_ref) * (PBF/PBF_ref) ** 2)`：scored；边际 -1.3090 pp；保留=False
- 复核字段变化：evidence_ids, rationale

### h3 (connectivity)

- 初稿 `log(1 + (ASA/ASA_ref) * (density/density_ref) ** -1)`：passed；
- 复核 `log(1 + (ASA/ASA_ref) * (density/density_ref) ** 1)`：passed；
- 最终 `log(1 + (ASA/ASA_ref) * (density/density_ref) ** 1)`：scored；边际 +0.9612 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/small_kg_rag_agent/replicate-3/round-1

该轮最佳保留增益：1.2057 pp；保留 `log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))`。

### h1 (translation)

- 初稿 `log(1 + (SPAN / SPAN_ref) * (MW / MW_ref) / (lsd_f / lsd_f_ref))`：passed；
- 复核 `log(1 + (SPAN / SPAN_ref) * (MW / MW_ref) / (lsd_f / lsd_f_ref))`：rejected；Formula contradicts its predeclared proxy direction
- 最终 `log(1 + (SPAN / SPAN_ref) * (MW / MW_ref) * (lsd_f / lsd_f_ref))`：scored；边际 -5.0019 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.descriptor_direction, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `rotor_case(log(1 + (PMI3 / PMI3_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)))`：passed；
- 复核 `rotor_case(log(1 + (PMI3 / PMI3_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)))`：passed；
- 最终 `rotor_case(log(1 + (PMI3 / PMI3_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)), log(1 + (PMI3 / PMI3_ref) * (PBF / PBF_ref)))`：scored；边际 -8.1092 pp；保留=False
- 复核字段变化：evidence_ids, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h3 (connectivity)

- 初稿 `log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))`：passed；
- 复核 `log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))`：passed；
- 最终 `log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))`：scored；边际 +1.2057 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

## low/small_kg_rag_agent/replicate-3/round-2

该轮最佳保留增益：6.1025 pp；保留 `log(1 + (Vol / Vol_ref) / (0.1 + lsd_p / lsd_p_ref))`。

### h1 (translation)

- 初稿 `log(1 + (SPAN / SPAN_ref) * exp(-(lsd_f / lsd_f_ref)))`：passed；
- 复核 `log(1 + (SPAN / SPAN_ref) * (lsd_f_ref / lsd_f))`：passed；
- 最终 `log(1 + (SPAN / SPAN_ref) * (lsd_f_ref / lsd_f))`：scored；边际 +2.2166 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions

### h2 (rotation)

- 初稿 `rotor_case(log(1 + PBF / PBF_ref), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref) / (0.1 + LabuteASA / LabuteASA_ref)), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref) / (0.1 + LabuteASA / LabuteASA_ref)))`：passed；
- 复核 `rotor_case(log(1 + PBF / PBF_ref), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref)), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref)))`：passed；
- 最终 `rotor_case(log(1 + PBF / PBF_ref), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref)), log(1 + (PBF / PBF_ref) * (PMI3 / PMI3_ref)))`：scored；边际 +3.0420 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, variable_mappings.LabuteASA

### h3 (coupling)

- 初稿 `log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))`：rejected；Redundant with a current input
- 复核 `log(1 + (Vol / Vol_ref) / (0.1 + lsd_p / lsd_p_ref))`：passed；
- 最终 `log(1 + (Vol / Vol_ref) / (0.1 + lsd_p / lsd_p_ref))`：scored；边际 +6.1025 pp；保留=True
- 复核字段变化：evidence_ids, falsification_criteria, formula, novelty_status, physical_claims, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, scientific_test.vary_input, variable_mappings.AV, variable_mappings.lsd_p

## low/small_kg_rag_agent/replicate-3/round-3

该轮最佳保留增益：0.0000 pp；保留 `None`。

### h1 (coupling)

- 初稿 `log(1 + (LabuteASA / LabuteASA_ref) * (AV_ref / (0.1 + AV)))`：rejected；Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references
- 复核 `log(1 + (LabuteASA / LabuteASA_ref) * (AV_ref / (0.1 + AV)))`：rejected；Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references
- 最终 `log(1 + (LabuteASA / LabuteASA_ref) / (0.1 + AV / AV_ref))`：scored；边际 -4.7657 pp；保留=False
- 复核字段变化：无

### h2 (rotation)

- 初稿 `rotor_case(log(1 + (PMI1 / PMI1_ref)), log(1 + (PMI2 / PMI2_ref)), log(1 + (PMI2 / PMI2_ref)))`：passed；
- 复核 `rotor_case(log(1 + (PMI1 / PMI1_ref)), log(1 + (PMI2 / PMI2_ref)), log(1 + (PMI2 / PMI2_ref)))`：passed；
- 最终 `rotor_case(log(1 + (PMI1 / PMI1_ref)), log(1 + (PMI2 / PMI2_ref)), log(1 + (PMI2 / PMI2_ref)))`：scored；边际 -7.5178 pp；保留=False
- 复核字段变化：无

### h3 (translation)

- 初稿 `log(1 + (Vol / Vol_ref) / (0.1 + AV / AV_ref))`：rejected；Redundant with a current input
- 复核 `log(1 + (Vol / Vol_ref) / (0.1 + ASA / ASA_ref))`：passed；
- 最终 `log(1 + (Vol / Vol_ref) / (0.1 + ASA / ASA_ref))`：scored；边际 -5.8489 pp；保留=False
- 复核字段变化：evidence_ids, falsification_criteria, formula, novelty_status, rationale, scientific_test.boundary_behavior, scientific_test.physical_interpretation, scientific_test.proxy_assumptions, scientific_test.regime_input, variable_mappings.ASA, variable_mappings.AV
