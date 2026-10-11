from pathlib import Path
import hashlib
A=Path(__file__).resolve().parent
source=A/'reconcile_exact135_144_connected_API_publication_v1_20261008.py';text=source.read_text(encoding='utf8')
old="    candidates=[(prefix+raw['message']+end).encode('utf8') for end in ('','\\n')]\n    matched=[v for v in candidates if hashlib.sha1(b'commit '+str(len(v)).encode()+b'\\0'+v).hexdigest()==commit];assert len(matched)==1"
new="    verified=(E/'actual_verified_raw_commit.bin').read_bytes()\n    assert hashlib.sha1(b'commit '+str(len(verified)).encode()+b'\\0'+verified).hexdigest()==commit\n    assert verified.decode('utf8').split('\\n\\n',1)[1]==raw['message']\n    assert verified.startswith(('tree '+raw['tree']['sha']+'\\nparent '+b['parent_commit']+'\\n').encode())\n    matched=[verified]"
assert old in text;text=text.replace(old,new).replace('exact135_144_connected_API_reconciliation_v1_20261008.json','exact135_144_connected_API_reconciliation_v2_20261008.json')
target=A/'reconcile_exact135_144_connected_API_publication_v2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
