from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
p=A/'prepare_rank120medium2048_own6_direct33_v1_20261011.py';s=p.read_text(encoding='utf8')
s=s.replace(' return s\n'," return s.replace('run_publish_rank120_after183','run_publish_rank120medium_after183').replace('Rank120_after183_actual33','Rank120Medium_after183_actual33')\n")
old="ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8',newline='\\n');outputs.append(q)"
new="ast.parse(s)\n  if q.exists():assert q.read_text(encoding='utf8')==s,q\n  else:q.write_text(s,encoding='utf8',newline='\\n')\n  outputs.append(q)"
assert s.count(old)==1;s=s.replace(old,new)
q=A/'prepare_rank120medium2048_own6_direct33_v2_20261011.py';ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8',newline='\n')
import runpy
runpy.run_path(str(q),run_name='__main__')
