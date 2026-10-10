from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A),str(A/'connected_validation')]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
import prepare_Rank60TwoSeedProtected205_complete39_pipeline_v2_20261011 as factory
proof=A/factory.PROOF
for p,d in read(proof)['input_sha256'].items():assert sha(p)==d,p
rows=[]
for p in factory.source_paths():
 if p.suffix!='.py':continue
 for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
  if not isinstance(node,ast.ImportFrom) or not node.module or node.level:continue
  local=A/(node.module+'.py')
  if not local.exists():continue
  module=importlib.import_module(node.module)
  for name in node.names:
   if name.name!='*':assert hasattr(module,name.name),(p,node.module,name.name)
  rows.append({'source':str(p),'module':node.module,'names':[n.name for n in node.names]})
create(A/'actual205_v2_runtime_imports_source_pins_admission_v1_20261011.json',{'status':'passed_all_actual205_v2_local_runtime_from_imports_resolve_and_all_source_pins_unchanged','input_sha256':{str(proof):sha(proof),str(Path(__file__)):sha(__file__)},'actual_import_checks':rows,'new_fits_or_scores':0,'future_X_read':False})
print({'runtime_local_from_imports':len(rows)},flush=True)
