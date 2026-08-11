# Public Predictive Datasets

This directory is reserved for public, AI-ready predictive datasets. The
existing literature ZIP archives are not predictive datasets and must not be
registered here without a separately reviewed dataset construction protocol.

## Firewall

- Only configs with `data_classification: public` are accepted.
- `contains_private_data` must be explicitly `false`.
- Registration configs must be committed under `research/configs/datasets/`.
- Raw public files must be staged under `research/datasets/raw/`.
- Raw files are ignored by Git and frozen through SHA256 in the dataset
  manifest.
- No private path discovery or scanning is performed.

## Freeze Workflow

1. Review the source, license, target, inputs, duplicate policy, and OOD
   rationale.
2. Commit the registration config.
3. Register the dataset from a clean Git worktree.
4. Review and commit the generated dataset manifest.
5. Generate IID and OOD split manifests from a clean Git worktree.
6. Run structural leakage audits.
7. Commit the split manifests only after review.

```bash
python research/scripts/research.py dataset register \
  --config research/configs/datasets/<dataset>.json

python research/scripts/research.py dataset split \
  --dataset <dataset-id> \
  --strategy iid

python research/scripts/research.py dataset split \
  --dataset <dataset-id> \
  --strategy ood

python research/scripts/research.py dataset leakage-audit \
  --dataset <dataset-id> \
  --split research/manifests/splits/<split-id>.json
```

The structural audit cannot establish that a scientifically plausible input is
free of semantic target leakage. Dataset review must separately assess target
proxies, benchmark contamination, publication overlap, and whether the OOD
definition was chosen without model outcome feedback.
