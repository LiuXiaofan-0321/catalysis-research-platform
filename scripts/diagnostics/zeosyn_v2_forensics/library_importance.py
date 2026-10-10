"""Does the RandomForest use the kg_* columns at all when they are force-fed (library-only diagnostic)?"""
import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..', '..'))
import sys, json
ROOT = _REPO
sys.path[:0] = [ROOT + '/src', ROOT + '/scripts', ROOT + '/literature_pipeline/src']
import numpy as np
import run_zeosyn_v2 as rz
from catalysis_research.benchmarks import zeosyn as z
from catalysis_research.knowledge.kg_features import FEATURE_NAMES
from catalysis_research.discovery import zeosyn_v2_eval as ev
from sklearn.ensemble import RandomForestClassifier
split = rz.load_split(ROOT + '/results/zeosyn_v2_dev_1')
tr, te, y = split['train'], split['eval'], split['y']
names = list(z.D0) + list(FEATURE_NAMES)
for table in ('kg', 'kg_shuffled'):
    x = ev.library_matrix(split, table)
    rf = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=3, n_jobs=2).fit(x[tr], y[tr])
    acc = (rf.predict(x[te]) == y[te]).mean()
    imp = rf.feature_importances_
    order = np.argsort(-imp)
    print(f'=== D0 + {table} (seed 3): eval accuracy {acc:.4f} | total importance of kg_* columns {imp[43:].sum():.3f} vs D0 {imp[:43].sum():.3f} ===')
    print('top 15 features:', [(names[i], round(float(imp[i]), 4)) for i in order[:15]])
    print('kg_* ranks:', sorted(((int(np.where(order == i)[0][0]) + 1, names[i], round(float(imp[i]), 4)) for i in range(43, len(names))))[:12])
