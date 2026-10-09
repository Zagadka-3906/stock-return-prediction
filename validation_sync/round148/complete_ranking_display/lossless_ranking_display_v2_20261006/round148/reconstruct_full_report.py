from pathlib import Path
import json,hashlib
p=Path(__file__).parent
m=json.loads((p/'full_report_reconstructed_for_publication.json.gz.parts.json').read_text(encoding='utf8'))
out=p/m['original_filename']
assert not out.exists()
h=hashlib.sha256();size=0
with out.open('xb') as f:
 for item in m['parts']:
  data=(p/item['path']).read_bytes()
  assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
  f.write(data);h.update(data);size+=len(data)
assert size==m['compressed_bytes'] and h.hexdigest()==m['compressed_sha256']
print(out)
