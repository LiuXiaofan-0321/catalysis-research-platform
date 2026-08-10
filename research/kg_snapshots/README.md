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

| Snapshot | Domain | Papers | Role |
| --- | --- | ---: | --- |
| `K247-photocatalysis-v1` | Photocatalysis | 247 | First frozen absolute-size knowledge point |

Verify from the repository root:

```bash
npm run research:verify:k247
```
