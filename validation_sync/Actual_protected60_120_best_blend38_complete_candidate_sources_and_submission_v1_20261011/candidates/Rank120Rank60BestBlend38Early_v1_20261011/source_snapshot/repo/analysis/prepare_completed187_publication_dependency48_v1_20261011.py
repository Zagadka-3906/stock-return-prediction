from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
old=A/'route_actual_nested_dispatch_and_complete_aliases45_v1_20261011.py';s=old.read_text(encoding='utf8').replace("PROOF=A/'actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json'","PROOF=A/'actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json'")
s=s.replace("'actual_nested_dispatch_and_complete_aliases44_admission_v1_20261011.json']","'actual_nested_dispatch_and_complete_aliases44_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json','actual_fraction38_gate_only_routes46_admission_v1_20261011.json']")
p=A/'route_actual_nested_dispatch_and_complete_aliases48_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
old=A/'start_actual_nested_dispatch_and_complete_aliases45_v1_20261011.py';t=old.read_text(encoding='utf8').replace('recovery45_','recovery48_').replace('nested_dispatch45','nested_dispatch48').replace('aliases45','aliases48').replace('actual187_registered_QA_main_resume45_v1_20261011','actual187_completed_QA_publication_only_resume47_v1_20261011')
t=t.replace(" for n in names:\n  if re.match", " extra45=read(A/'actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json')\n for k,v in extra45['service_alias_updates'].items():names.update([k,v])\n aliases['actual187_registered_QA_main_resume45_v1_20261011']='actual187_completed_QA_publication_only_resume47_v1_20261011'\n for n in names:\n  if re.match",1)
t=t.replace(" paths=[Path(__file__),", " paths=[A/'actual187_publication_only_resume47_sources_admission_v1_20261011.json',A/'actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json',Path(__file__),",1)
q=A/'start_actual_nested_dispatch_and_complete_aliases48_v1_20261011.py';ast.parse(t);assert not q.exists();q.write_text(t,encoding='utf8')
print(q,flush=True)
