"""Verify exact archived run bytes using stdlib only."""
from pathlib import Path
import hashlib
import json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'ARTIFACTS.json').read_text(encoding='utf-8'))
for row in manifest['files']:
    p=(root/row['path']).resolve()
    assert p.is_relative_to(root.resolve()), row['path']
    assert p.is_file() and p.stat().st_size==row['bytes'], row['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'], row['path']
expected={r['path'] for r in manifest['files']}|{'ARTIFACTS.json'}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual==expected, 'Extra or missing files: '+str(actual^expected)
print(json.dumps({'verified_files':len(manifest['files']),'original_run_files':len(manifest['original_run_files']),'bytes':sum(x['bytes'] for x in manifest['files'])}))
