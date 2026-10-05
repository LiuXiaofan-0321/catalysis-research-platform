# V5 全部30轨迹与90槽

主结果使用每条最终实际组合的五seed平均；此清单不选择最好公式或省略失败。

## agent

| 重复 | 最终降幅/% | 追加数 | 最终公式 |
| --- | ---: | ---: | --- |
| 1 | 1.890413 | 2 | `(Vol/Vol_ref) * (lsd_p_ref/lsd_p)**3`<br>`(PMI3/(MW * lsd_p**2))` |
| 2 | 0.801322 | 1 | `GeDi/(GeDi + lsd_f)` |
| 3 | 1.431186 | 3 | `GeDi/lsd_f`<br>`Vol/(LabuteASA*lsd_f)`<br>`GeDi/lsd_p` |
| 4 | 2.200377 | 2 | `log(1 + (q_GeDi / q_lsd_f)**2)`<br>`(Vol/Vol_ref) / ((Vol/Vol_ref) + (AV/AV_ref) + 0.02)` |
| 5 | 1.857812 | 3 | `SPAN / lsd_f`<br>`lsd_p / lsd_f`<br>`Vol / (AV + AV_ref)` |
| 6 | 0.416722 | 2 | `lsd_f / (Vol ** (1.0 / 3.0))`<br>`lsd_p / sqrt(LabuteASA)` |
| 7 | -0.740552 | 2 | `(q_GeDi) / (q_lsd_f)`<br>`(q_LabuteASA) / (q_lsd_p**2)` |
| 8 | 1.769402 | 2 | `(Vol ** 0.3333333333) / lsd_f`<br>`SPAN / lsd_p` |
| 9 | -0.949395 | 3 | `GeDi / (GeDi + lsd_f)`<br>`q_PBF * (GeDi / lsd_f)`<br>`SPAN / lsd_p` |
| 10 | -0.916872 | 1 | `exp(-(q_GeDi / q_lsd_f))` |

| 重复/轮 | 状态 | 首次公式 | 最终公式 | 接口或执行问题 |
| --- | --- | --- | --- | --- |
| 1/1 | technical_failure_not_appended | `(GeDi/GeDi_ref)/(lsd_f/lsd_f_ref)` | `(GeDi/GeDi_ref)/(lsd_f/lsd_f_ref)` | Wrong physical variable mapping: lsd_f requires bottleneck_free_sphere_Df |
| 1/2 | appended | `(Vol/Vol_ref) * (lsd_p_ref/lsd_p)**3` | `(Vol/Vol_ref) * (lsd_p_ref/lsd_p)**3` | 结构/数值通过，机制仍未验证 |
| 1/3 | appended | `(PMI3/(MW * lsd_p**2))` | `(PMI3/(MW * lsd_p**2))` | Incorrect structured limit: PMI3 |
| 2/1 | technical_failure_not_appended | `Vol/(lsd_f**3)` | `Vol/(lsd_f**3)` | Wrong physical variable mapping: lsd_f requires bottleneck_free_sphere_Df |
| 2/2 | proposal_failure | `GeDi/lsd_p` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 2/3 | appended | `GeDi/(GeDi + lsd_f)` | `GeDi/(GeDi + lsd_f)` | 结构/数值通过，机制仍未验证 |
| 3/1 | appended | `GeDi/lsd_f` | `GeDi/lsd_f` | 结构/数值通过，机制仍未验证 |
| 3/2 | appended | `Vol/(LabuteASA*lsd_f)` | `Vol/(LabuteASA*lsd_f)` | 结构/数值通过，机制仍未验证 |
| 3/3 | appended | `GeDi/lsd_p` | `GeDi/lsd_p` | 结构/数值通过，机制仍未验证 |
| 4/1 | appended | `log(1 + (q_GeDi / q_lsd_f)**2)` | `log(1 + (q_GeDi / q_lsd_f)**2)` | 结构/数值通过，机制仍未验证 |
| 4/2 | appended | `(Vol/Vol_ref) / ((Vol/Vol_ref) + (AV/AV_ref) + 0.02)` | `(Vol/Vol_ref) / ((Vol/Vol_ref) + (AV/AV_ref) + 0.02)` | 结构/数值通过，机制仍未验证 |
| 4/3 | technical_failure_not_appended | `(SPAN**2) / (SPAN**2 + lsd_p**2 + 0.04)` | `(SPAN**2) / (SPAN**2 + lsd_p**2 + 0.04)` | Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references |
| 5/1 | appended | `SPAN / lsd_f` | `SPAN / lsd_f` | 结构/数值通过，机制仍未验证 |
| 5/2 | appended | `lsd_p / lsd_f` | `lsd_p / lsd_f` | 结构/数值通过，机制仍未验证 |
| 5/3 | appended | `Vol / (AV + AV_ref)` | `Vol / (AV + AV_ref)` | 结构/数值通过，机制仍未验证 |
| 6/1 | proposal_failure | `q_GeDi / q_lsd_f` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 6/2 | appended | `lsd_f / (Vol ** (1.0 / 3.0))` | `lsd_f / (Vol ** (1.0 / 3.0))` | 结构/数值通过，机制仍未验证 |
| 6/3 | appended | `lsd_p / sqrt(LabuteASA)` | `lsd_p / sqrt(LabuteASA)` | 结构/数值通过，机制仍未验证 |
| 7/1 | appended | `(q_GeDi) / (q_lsd_f)` | `(q_GeDi) / (q_lsd_f)` | 结构/数值通过，机制仍未验证 |
| 7/2 | appended | `(q_LabuteASA) / (q_lsd_p**2)` | `(q_LabuteASA) / (q_lsd_p**2)` | 结构/数值通过，机制仍未验证 |
| 7/3 | proposal_failure | `(q_Vol) / (q_lsd_f**3)` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 8/1 | appended | `(Vol ** 0.3333333333) / lsd_f` | `(Vol ** 0.3333333333) / lsd_f` | 结构/数值通过，机制仍未验证 |
| 8/2 | appended | `SPAN / lsd_p` | `SPAN / lsd_p` | 结构/数值通过，机制仍未验证 |
| 8/3 | proposal_failure | `(ASA / maximum(AV, 1e-6)) * (Vol ** 0.3333333333)` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 9/1 | appended | `GeDi / (GeDi + lsd_f)` | `GeDi / (GeDi + lsd_f)` | 结构/数值通过，机制仍未验证 |
| 9/2 | appended | `q_PBF * (GeDi / lsd_f)` | `q_PBF * (GeDi / lsd_f)` | 结构/数值通过，机制仍未验证 |
| 9/3 | appended | `SPAN / lsd_p` | `SPAN / lsd_p` | 结构/数值通过，机制仍未验证 |
| 10/1 | appended | `exp(-(q_GeDi / q_lsd_f))` | `exp(-(q_GeDi / q_lsd_f))` | 结构/数值通过，机制仍未验证 |
| 10/2 | technical_failure_not_appended | `q_SPAN / q_lsd_p` | `q_SPAN / q_lsd_p` | Wrong physical variable mapping: lsd_p requires included_along_free_path_Dif |
| 10/3 | technical_failure_not_appended | `q_Vol / (q_AV + AV_ref)` | `q_Vol / (q_AV + AV_ref)` | Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references |

## rag_agent

| 重复 | 最终降幅/% | 追加数 | 最终公式 |
| --- | ---: | ---: | --- |
| 1 | 1.311010 | 3 | `lsd_p / (lsd_p + GeDi)`<br>`lsd_f / (lsd_f + SPAN)`<br>`lsd_f / (lsd_f + lsd_p)` |
| 2 | 0.610742 | 3 | `GeDi / lsd_p`<br>`(SPAN / lsd_f) ** 2`<br>`Vol / (lsd_p ** 3)` |
| 3 | 1.345662 | 3 | `log(1 + GeDi/lsd_p)`<br>`log(1 + SPAN/lsd_f)`<br>`log(1 + Vol/lsd_p**3)` |
| 4 | 0.000000 | 0 | D0（无成功追加） |
| 5 | -1.214299 | 1 | `(GeDi / lsd_f) ** 2` |
| 6 | -0.807314 | 1 | `q_PBF / q_lsd_f` |
| 7 | 1.448710 | 1 | `exp(-q_SPAN/q_lsd_p)` |
| 8 | 0.307227 | 1 | `GeDi/lsd_f` |
| 9 | 0.481065 | 3 | `log(1 + GeDi/lsd_p)`<br>`log(1 + Vol / (lsd_f**3))`<br>`log(1 + LabuteASA / (lsd_p ** 2))` |
| 10 | 0.801322 | 1 | `lsd_f / (lsd_f + GeDi)` |

| 重复/轮 | 状态 | 首次公式 | 最终公式 | 接口或执行问题 |
| --- | --- | --- | --- | --- |
| 1/1 | appended | `lsd_p / (lsd_p + GeDi)` | `lsd_p / (lsd_p + GeDi)` | 结构/数值通过，机制仍未验证 |
| 1/2 | appended | `lsd_f / (lsd_f + SPAN)` | `lsd_f / (lsd_f + SPAN)` | 结构/数值通过，机制仍未验证 |
| 1/3 | appended | `lsd_f / (lsd_f + lsd_p)` | `lsd_f / (lsd_f + lsd_p)` | 结构/数值通过，机制仍未验证 |
| 2/1 | appended | `GeDi / lsd_p` | `GeDi / lsd_p` | Incorrect structured limit: GeDi |
| 2/2 | appended | `(SPAN / lsd_f) ** 2` | `(SPAN / lsd_f) ** 2` | 结构/数值通过，机制仍未验证 |
| 2/3 | appended | `Vol / (lsd_p ** 3)` | `Vol / (lsd_p ** 3)` | 结构/数值通过，机制仍未验证 |
| 3/1 | appended | `log(1 + GeDi/lsd_p)` | `log(1 + GeDi/lsd_p)` | 结构/数值通过，机制仍未验证 |
| 3/2 | appended | `log(1 + SPAN/lsd_f)` | `log(1 + SPAN/lsd_f)` | 结构/数值通过，机制仍未验证 |
| 3/3 | appended | `log(1 + Vol/lsd_p**3)` | `log(1 + Vol/lsd_p**3)` | Incorrect structured limit: Vol |
| 4/1 | technical_failure_not_appended | `GeDi / lsd_p` | `GeDi / lsd_p` | Wrong physical variable mapping: GeDi requires heavy_atom_pair_distance |
| 4/2 | technical_failure_not_appended | `LabuteASA / (Vol ** (2.0 / 3.0))` | `LabuteASA / (Vol ** (2.0 / 3.0))` | Wrong physical variable mapping: Vol requires molecular_vdw_volume |
| 4/3 | proposal_failure | `Vol / (lsd_p ** 3.0)` | `—` | Structural recovery exhausted: Missing candidate text: proxy_assumptions |
| 5/1 | proposal_failure | `log(1 + GeDi / lsd_f)` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 5/2 | appended | `(GeDi / lsd_f) ** 2` | `(GeDi / lsd_f) ** 2` | 结构/数值通过，机制仍未验证 |
| 5/3 | proposal_failure | `Vol / (lsd_p ** 3)` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 6/1 | technical_failure_not_appended | `(q_Vol ** (1.0 / 3.0)) / q_lsd_p` | `(q_Vol ** (1.0 / 3.0)) / q_lsd_p` | Wrong physical variable mapping: lsd_p requires included_along_free_path_Dif |
| 6/2 | technical_failure_not_appended | `q_SPAN / q_lsd_f` | `q_SPAN / q_lsd_f` | Wrong physical variable mapping: lsd_f requires bottleneck_free_sphere_Df |
| 6/3 | appended | `q_PBF / q_lsd_f` | `q_PBF / q_lsd_f` | 结构/数值通过，机制仍未验证 |
| 7/1 | appended | `exp(-q_SPAN/q_lsd_p)` | `exp(-q_SPAN/q_lsd_p)` | 结构/数值通过，机制仍未验证 |
| 7/2 | proposal_failure | `exp(-((q_GeDi/q_lsd_f)**2))` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 7/3 | proposal_failure | `exp(-(q_GeDi/q_lsd_f))` | `—` | Structural recovery exhausted: Missing candidate text: proxy_assumptions |
| 8/1 | appended | `GeDi/lsd_f` | `GeDi/lsd_f` | 结构/数值通过，机制仍未验证 |
| 8/2 | proposal_failure | `sqrt((PMI1 + PMI2 + PMI3)/MW) / lsd_p` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 8/3 | proposal_failure | `GeDi * SPAN / lsd_p**2` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 9/1 | appended | `log(1 + GeDi/lsd_p)` | `log(1 + GeDi/lsd_p)` | 结构/数值通过，机制仍未验证 |
| 9/2 | appended | `log(1 + Vol / (lsd_f**3))` | `log(1 + Vol / (lsd_f**3))` | 结构/数值通过，机制仍未验证 |
| 9/3 | appended | `log(1 + LabuteASA / (lsd_p ** 2))` | `log(1 + LabuteASA / (lsd_p ** 2))` | 结构/数值通过，机制仍未验证 |
| 10/1 | proposal_failure | `(q_GeDi) / (q_lsd_p)` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 10/2 | appended | `lsd_f / (lsd_f + GeDi)` | `lsd_f / (lsd_f + GeDi)` | 结构/数值通过，机制仍未验证 |
| 10/3 | proposal_failure | `lsd_f / (lsd_f + lsd_p)` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |

## small_kg_rag_agent

| 重复 | 最终降幅/% | 追加数 | 最终公式 |
| --- | ---: | ---: | --- |
| 1 | 0.419304 | 3 | `exp(-GeDi / lsd_p)`<br>`exp(-((q_SPAN * SPAN_ref) / (q_lsd_f * lsd_f_ref)) ** 2)`<br>`exp(-Vol / (lsd_p ** 3))` |
| 2 | 0.000000 | 0 | D0（无成功追加） |
| 3 | 1.603033 | 2 | `(q_Vol ** (1.0/3.0)) / q_lsd_p`<br>`q_GeDi / q_lsd_f` |
| 4 | -2.107655 | 2 | `GeDi / lsd_f`<br>`SPAN / lsd_p` |
| 5 | 0.307227 | 1 | `q_GeDi / q_lsd_f` |
| 6 | 0.307227 | 1 | `GeDi/lsd_f` |
| 7 | 1.946454 | 2 | `(Vol ** 0.3333333333) / lsd_p`<br>`GeDi / lsd_f` |
| 8 | 2.366264 | 1 | `(q_Vol ** (1.0/3.0)) / q_lsd_f` |
| 9 | 2.902813 | 1 | `(q_SPAN) / (q_SPAN + q_lsd_p)` |
| 10 | 1.520017 | 3 | `GeDi / lsd_f`<br>`(Vol ** (1.0/3.0)) / lsd_p`<br>`LabuteASA / (lsd_p ** 2)` |

| 重复/轮 | 状态 | 首次公式 | 最终公式 | 接口或执行问题 |
| --- | --- | --- | --- | --- |
| 1/1 | appended | `exp(-GeDi / lsd_p)` | `exp(-GeDi / lsd_p)` | 结构/数值通过，机制仍未验证 |
| 1/2 | appended | `exp(-((q_SPAN * SPAN_ref) / (q_lsd_f * lsd_f_ref)) ** 2)` | `exp(-((q_SPAN * SPAN_ref) / (q_lsd_f * lsd_f_ref)) ** 2)` | 结构/数值通过，机制仍未验证 |
| 1/3 | appended | `exp(-Vol / (lsd_p ** 3))` | `exp(-Vol / (lsd_p ** 3))` | 结构/数值通过，机制仍未验证 |
| 2/1 | proposal_failure | `GeDi / (GeDi + lsd_f)` | `—` | Structural recovery exhausted: Missing candidate text: proxy_assumptions |
| 2/2 | proposal_failure | `q_GeDi / q_lsd_f` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 2/3 | technical_failure_not_appended | `q_GeDi / (q_GeDi + q_lsd_p)` | `q_GeDi / (q_GeDi + q_lsd_p)` | Wrong physical variable mapping: GeDi requires heavy_atom_pair_distance |
| 3/1 | appended | `(q_Vol ** (1.0/3.0)) / q_lsd_p` | `(q_Vol ** (1.0/3.0)) / q_lsd_p` | 结构/数值通过，机制仍未验证 |
| 3/2 | appended | `q_GeDi / q_lsd_f` | `q_GeDi / q_lsd_f` | 结构/数值通过，机制仍未验证 |
| 3/3 | proposal_failure | `q_PBF / q_lsd_p` | `—` | Structural recovery exhausted: Missing candidate text: proxy_assumptions |
| 4/1 | proposal_failure | `(GeDi * lsd_p_ref) / (lsd_p * GeDi_ref)` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 4/2 | appended | `GeDi / lsd_f` | `GeDi / lsd_f` | 结构/数值通过，机制仍未验证 |
| 4/3 | appended | `SPAN / lsd_p` | `SPAN / lsd_p` | 结构/数值通过，机制仍未验证 |
| 5/1 | appended | `q_GeDi / q_lsd_f` | `q_GeDi / q_lsd_f` | 结构/数值通过，机制仍未验证 |
| 5/2 | proposal_failure | `q_SPAN / q_lsd_p` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 5/3 | proposal_failure | `q_SPAN / q_lsd_p` | `—` | Structural recovery exhausted: Missing candidate text: proxy_assumptions |
| 6/1 | proposal_failure | `q_SPAN / q_lsd_p` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 6/2 | appended | `GeDi/lsd_f` | `GeDi/lsd_f` | 结构/数值通过，机制仍未验证 |
| 6/3 | technical_failure_not_appended | `maximum(q_PMI2, q_PMI3)/q_MW` | `maximum(q_PMI2, q_PMI3)/q_MW` | Conditional prediction must hold other used inputs fixed |
| 7/1 | appended | `(Vol ** 0.3333333333) / lsd_p` | `(Vol ** 0.3333333333) / lsd_p` | 结构/数值通过，机制仍未验证 |
| 7/2 | appended | `GeDi / lsd_f` | `GeDi / lsd_f` | Incorrect structured limit: GeDi |
| 7/3 | proposal_failure | `SPAN / lsd_p` | `—` | Scientific repair contract exhausted: Format recovery changed an already recorded scientific claim |
| 8/1 | proposal_failure | `GeDi / lsd_p` | `—` | Structural recovery exhausted: Missing candidate text: proxy_assumptions |
| 8/2 | appended | `(q_Vol ** (1.0/3.0)) / q_lsd_f` | `(q_Vol ** (1.0/3.0)) / q_lsd_f` | 结构/数值通过，机制仍未验证 |
| 8/3 | technical_failure_not_appended | `(PMI3 - PMI1) / (PMI3 + PMI1 + 1.0)` | `(PMI3 - PMI1) / (PMI3 + PMI1 + 1.0)` | Incompatible dimensions in addition, subtraction, minimum or maximum; use matching units or training references |
| 9/1 | appended | `(q_SPAN) / (q_SPAN + q_lsd_p)` | `(q_SPAN) / (q_SPAN + q_lsd_p)` | 结构/数值通过，机制仍未验证 |
| 9/2 | technical_failure_not_appended | `(q_GeDi) / (q_GeDi + q_lsd_f)` | `(q_GeDi) / (q_GeDi + q_lsd_f)` | Wrong physical variable mapping: lsd_f requires bottleneck_free_sphere_Df |
| 9/3 | proposal_failure | `(q_LabuteASA) / (q_LabuteASA + q_ASA)` | `—` | Structural recovery exhausted: Missing candidate text: proxy_assumptions |
| 10/1 | appended | `GeDi / lsd_f` | `GeDi / lsd_f` | 结构/数值通过，机制仍未验证 |
| 10/2 | appended | `(Vol ** (1.0/3.0)) / lsd_p` | `(Vol ** (1.0/3.0)) / lsd_p` | 结构/数值通过，机制仍未验证 |
| 10/3 | appended | `LabuteASA / (lsd_p ** 2)` | `LabuteASA / (lsd_p ** 2)` | 结构/数值通过，机制仍未验证 |
