from pathlib import Path
import json,hashlib
p=Path(__file__).parent
for d in p.glob('*.parts.json'):
 m=json.loads(d.read_text(encoding='utf8'));target=p/m['original_filename'];assert not target.exists()
 h=hashlib.sha256();size=0
 with target.open('xb') as f:
  for item in m['parts']:
   b=(p/item['path']).read_bytes();assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
   f.write(b);h.update(b);size+=len(b)
 assert size==m['compressed_bytes'] and h.hexdigest()==m['compressed_sha256']
 print(target)
