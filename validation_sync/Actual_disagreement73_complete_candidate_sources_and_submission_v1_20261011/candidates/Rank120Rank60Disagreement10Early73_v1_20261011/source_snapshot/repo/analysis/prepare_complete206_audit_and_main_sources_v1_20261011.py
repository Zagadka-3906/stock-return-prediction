from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
s=(A/'audit_prospective205_v2_runtime_imports_v2_20261011.py').read_text(encoding='utf8').replace('prepare_Rank60TwoSeedProtected205_complete39_pipeline_v2_20261011','prepare_StockRank60Window504Direct206_complete35_pipeline_v1_20261011').replace('actual205_v2','actual206_v1')
p=A/'audit_prospective206_v1_runtime_imports_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
t=(A/'prepare_new_complete202_205_sources_main_v1_20261011.py').read_text(encoding='utf8')
lines=t.splitlines();lines=["mods=['prepare_StockRank60Window504Direct206_complete35_pipeline_v1_20261011']" if line.startswith('mods=') else line for line in lines]
lines=["paths.extend(A/n for n in ['actual206_v1_runtime_imports_source_pins_admission_v2_20261011.json','rank60window504_parent183_future_sources_admission_v2_20261011.json','stock_rank60window504_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json','rank60window504_complete206_factory_sources_admission_v1_20261011.json','actual_observer127_complete205_refresh_admission_v2_20261011.json'])" if line.startswith('paths.extend(A/n') else line for line in lines]
t='\n'.join(lines)+'\n';t=t.replace('complete202_205','complete206').replace('202至205轮','206轮504日训练窗口').replace('prospective202_to205','prospective206_window504')
q=A/'prepare_new_complete206_sources_main_v1_20261011.py';ast.parse(t);assert not q.exists();q.write_text(t,encoding='utf8')
print({'audit':p.name,'publication_preparation':q.name},flush=True)
