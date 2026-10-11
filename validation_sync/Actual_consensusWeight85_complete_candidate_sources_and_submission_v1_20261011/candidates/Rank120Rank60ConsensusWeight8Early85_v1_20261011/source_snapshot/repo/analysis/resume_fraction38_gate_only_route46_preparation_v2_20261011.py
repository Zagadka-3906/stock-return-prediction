from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
source=A/'prepare_fraction38_gate_only_prospective_routes46_v1_20261011.py';s=source.read_text(encoding='utf8')
s=s.replace("ast.parse(s);assert not route.exists();route.write_text(s,encoding='utf8');paths.append(route)","ast.parse(s)\nif route.exists():assert route.read_text(encoding='utf8')==s\nelse:route.write_text(s,encoding='utf8')\npaths.append(route)")
s=s.replace(" assert not p.exists();ast.parse(t);p.write_text(t,encoding='utf8');wrappers[driver]=p.name;paths.append(p)"," ast.parse(t)\n if p.exists():assert p.read_text(encoding='utf8')==t\n else:p.write_text(t,encoding='utf8')\n wrappers[driver]=p.name;paths.append(p)")
s=s.replace(" else:\n  assert owned(row),name", " elif (folder/'administrative_prospective_gate_only_supersession46.json').exists():\n  assert not owned(row),name\n  item=read(folder/'administrative_prospective_gate_only_supersession46.json');assert item['identity']==row\n  retired.append(item)\n else:\n  assert owned(row),name")
s=s.replace("assert 'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:' in spy and driver in spy", "assert 'closed (' in spy and 'MainThread' in spy and '(idle)' in spy and driver in spy")
p=A/'prepare_fraction38_gate_only_prospective_routes46_v2_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');print(p,flush=True)
