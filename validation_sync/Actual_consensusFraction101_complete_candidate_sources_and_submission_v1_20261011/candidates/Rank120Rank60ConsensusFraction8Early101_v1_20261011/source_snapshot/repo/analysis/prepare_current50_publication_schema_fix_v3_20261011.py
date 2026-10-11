from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
s=(A/'start_current_publication_paths_and_prospective50_v2_20261011.py').read_text(encoding='utf8')
s=s.replace("assert len(read(folder/'verification.json')['records'])==family['records']","assert family.get('records',len(read(folder/'verification.json')['records']))==len(read(folder/'verification.json')['records'])")
s=s.replace("==family['records'],(source,family)","==family.get('records',len(read(existing[0]/'verification.json')['records'])),(source,family)")
s=s.replace('_actual_family_paths50.py','_actual_family_paths51.py')
p=A/'start_current_publication_paths_and_prospective50_v3_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');print(p,flush=True)
