from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
names=['publish_actual_protected60_120_37_complete_candidate_main_v1_20261011.py','prepare_verified_early37_alternate_submission_delivery_v1_20261011.py']
outputs=[]
for name in names:
 s=(A/name).read_text(encoding='utf8').replace('Rank120Rank60ProtectedEarly','Rank120Rank60BestBlend38Early').replace('protected60_120_37_complete_candidate','protected60_120_best_blend38_complete_candidate').replace('protected60_120_37_complete_candidate','protected60_120_best_blend38_complete_candidate').replace('Actual_protected60_120_37_complete_candidate','Actual_protected60_120_best_blend38_complete_candidate')
 s=s.replace('rank120_rank60_protected37_early_normalized','rank120_rank60_best_blend_fraction38_early_normalized').replace('pilot37.json','pilot38.json').replace('alternate_verified_early37','alternate_verified_best_blend38').replace('已核验候选_60与120日组合37项','已核验候选_60与120日最佳组合38项')
 s=s.replace("pilot['expected_scored_records']==len(pilot['records'])==37","pilot['expected_scored_records']==len(pilot['records'])==38").replace('(36,108)','(37,111)').replace('37项TRAIN官方评分','38项TRAIN官方评分').replace('actual37_record_selected','actual38_record_selected')
 s=s.replace('from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold','from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold')
 target=name.replace('protected60_120_37_complete_candidate','protected60_120_best_blend38_complete_candidate').replace('verified_early37_alternate','verified_best_blend38_alternate')
 p=A/target;ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');outputs.append(p)
proof=A/'best_blend38_candidate_main_and_alternate_delivery_sources_v1_20261011.json'
create(proof,{'status':'prospective_all38_selected37_physical_model_full_native_candidate_main_and_alternate_csv_require_actual_completed_sealing_and_main_first_full_board_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in names],*outputs]},'new_fits_or_scores':0,'pending_candidate_not_declared_completed':True})
jobs=[('actual_protected60_120_best_blend38_complete_candidate_main_v1_20261011',outputs[0]),('actual_verified_best_blend38_alternate_submission_delivery_v1_20261011',outputs[1])]
for name,p in jobs:
 assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
print({'conditional_candidate_main_and_delivery_helpers':2,'complete_validation_required':True},flush=True)
