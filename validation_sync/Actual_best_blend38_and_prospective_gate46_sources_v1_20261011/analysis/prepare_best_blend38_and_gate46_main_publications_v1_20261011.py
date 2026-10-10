from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
source=A/'publish_actual_rank120_rank60_protected37_completed_main_v1_20261011.py'
s=source.read_text(encoding='utf8').replace('Actual_rank120_rank60_protected37_completed_TRAIN_records','Actual_rank120_rank60_best_blend_fraction38_completed_TRAIN_records')
lines=s.splitlines();lines=["    pairs=[('actual_rank120_rank60_after183_best_blend_fraction38_screen_v1_20261011','StockRank120Rank60_after183_best_blend_fraction38_screen_v1_20261011',38)]" if line.strip().startswith('pairs=') else line for line in lines]
s='\n'.join(lines)+'\n';s=s.replace("'actual_completed_official_records':37","'actual_completed_official_records':38").replace('完成37项TRAIN验证：rank120_rank60_protected37','完成38项TRAIN验证：60与120日最佳组合的保护比例权重').replace("        for row in proof['records']:","        paths.extend(output.glob('blend*_controls.json'))\n        for row in proof['records']:")
p=A/'publish_actual_rank120_rank60_best_blend_fraction38_completed_main_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
r=start_service('actual_rank120_rank60_best_blend_fraction38_completed_main_v1_20261011',p.name,[],{str(p):sha(p),str(Path(__file__)):sha(__file__)})
routeproof=A/'actual_fraction38_gate_only_routes46_admission_v1_20261011.json';proof=read(routeproof)
paths=[Path(x) for x in proof['input_sha256'] if Path(x).suffix in ('.py','.json','.md')]
paths += [Path(__file__),routeproof,A/'verify_completed_fraction38_namespace_bridge_v1_20261011.py',A/'prepare_rank120_rank60_best_blend_fraction38_v1_20261011.py',A/'run_rank120_rank60_after183_best_blend_fraction38_screen_v1_20261011.py',A/'rank120_rank60_best_blend_fraction38_predeclared_sources_admission_v1_20261011.json',A/'resume_fraction38_gate_only_route46_preparation_v2_20261011.py',p]
t=(A/'publish_actual_rank60_seed10_own6_and_two_seed37_predeclared_sources_main_v1_20261011.py').read_text(encoding='utf8')
lines=t.splitlines();lines=[('    paths=[Path(p) for p in '+repr([str(x) for x in dict.fromkeys(paths)])+']') if line.strip().startswith('paths=') else line for line in lines]
t='\n'.join(lines)+'\n';t=t.replace('Actual_rank60_seed10_own6_and_two_seed37_predeclared_sources','Actual_best_blend38_and_prospective_gate46_sources')
t=t.replace('predeclared_seed10_mature60day_own6_full5_native42_direct33_and_two_seed37_original_seed9_models_not_reused_for_training','predeclared_best_blend38_more_fractions_and_weights_actual_idle_future_gate_only_recovery46_scientific_workers_preserved')
t=t.replace('预声明60日第二种子六年度训练与33项直接方案、37项双种子组合；未完成模型不计入核验','预声明最佳60与120日组合的38项保护比例权重；仅修复前瞻队列门控；保留原始分数和失败证据')
q=A/'publish_actual_best_blend38_and_prospective_gate46_sources_main_v1_20261011.py';ast.parse(t);assert not q.exists();q.write_text(t,encoding='utf8')
sr=start_service('actual_best_blend38_and_prospective_gate46_sources_main_v1_20261011',q.name,[],{str(q):sha(q),str(Path(__file__)):sha(__file__)})
create(A/'actual_best_blend38_and_gate46_main_publications_activation_v1_20261011.json',{'completed38_publication':r,'predeclared_source_publication':sr,'no_pending_round_declared_completed':True})
print({'main_only_publishers':2},flush=True)
