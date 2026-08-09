# 结构化催化语料

本目录只包含逐篇结构化抽取结果，不包含论文 PDF。

| 数据包 | 纳入规则 | 文献数 |
| --- | --- | ---: |
| `photocatalysis-stage1.zip` | `photocatalysis` 与 `both`，跨两个处理批次按 DOI/SHA 去重 | 247 |
| `thermal-catalysis-stage1.zip` | `thermal_catalysis` | 512 |

每个压缩包包含：

- `json/*.json`：逐篇结构化抽取结果；
- `dataset-manifest.json`：语料数量、类型分布和文档指纹。

图谱导入只生成有来源记录的单向证据边，不自动生成因果边或跨论文关系。`needs_review`、`unverified` 和视觉复核标记会保留。

这些数据用于科研检索和候选假设生成，不替代原始论文核验。使用者应自行确认论文许可、引用规范和数据使用边界。
