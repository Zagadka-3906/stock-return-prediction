from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
names=['stock_rank60seed10_embedding_after_complete_qualified_parent_native_stage_v2_20261011.py','predict_stock_rank60seed10_embedding_complete_qualified_parent_scheme_v2_20261011.py','verify_stock_rank60seed10_actual_twelve_parent183_callbacks_CPU_v2_20261011.py']
outputs=[]
for name in names:
 p=A/name;t=p.read_text(encoding='utf8').replace('stock_rank60seed10','stock_rank60window504').replace('recent252','recent504')
 t=t.replace("meta['training_calendar_window']==252 and meta['days']<=252","meta['training_calendar_window']==504 and meta['days']<=504")
 target=A/name.replace('stock_rank60seed10','stock_rank60window504');ast.parse(t);assert not target.exists();target.write_text(t,encoding='utf8');outputs.append(target)
create(A/'rank60window504_parent183_future_sources_admission_v2_20261011.json',{'status':'prospective_window504_own_cfg_native_source_and_parent183_callbacks_before_future','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in names],*outputs]},'actual_future_X_read':False,'new_fits_or_scores':0})
print({'new_sources':len(outputs)},flush=True)
