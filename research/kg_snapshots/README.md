# Frozen Knowledge Snapshots

Knowledge snapshots in this directory are immutable scientific inputs.

Rules:

1. A frozen snapshot directory must never be overwritten.
2. Corrections create a new snapshot ID and version.
3. Every snapshot contains an exact paper list, source hashes, graph artifacts,
   ontology version, extraction metadata, generation commit, and content hash.
4. Experiment runs must reference the exact snapshot ID and content hash.
5. A later, larger corpus does not replace an earlier scaling point.

## Registered Snapshots

| Snapshot | Domain | Papers | Nodes | Edges | Role |
| --- | --- | ---: | ---: | ---: | --- |
| `K247-photocatalysis-v1` | Photocatalysis | 247 | 10,503 | 23,423 | First frozen absolute-size knowledge point |
| `K20-thermal-catalysis-v1` | Thermal catalysis | 102 | 4,576 | 10,321 | 20% nested prefix |
| `K40-thermal-catalysis-v1` | Thermal catalysis | 205 | 8,842 | 21,540 | 40% nested prefix |
| `K60-thermal-catalysis-v1` | Thermal catalysis | 307 | 12,656 | 31,931 | 60% nested prefix |
| `K80-thermal-catalysis-v1` | Thermal catalysis | 410 | 16,319 | 42,008 | 80% nested prefix |
| `K100-thermal-catalysis-v1` | Thermal catalysis | 512 | 19,949 | 52,208 | 100% nested prefix |

Verify from the repository root:

```bash
npm run research:verify:k247
npm run research:verify:thermal-corpus
npm run research:verify:thermal-nested
```

The thermal family is anchored by
`research/corpora/thermal-catalysis-stage1-v1` and the frozen selection order in
`research/manifests/kg/thermal-catalysis-nested-v1.order.jsonl`. Coverage is
`not_measured` until an eligible public predictive dataset is frozen.
