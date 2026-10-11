"""Queue a full score-instance catalog after actual formal191 and both new raw screens complete."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
original=A/'build_complete190_plus_completed_raw_TRAIN_score_catalog_v2_20261011.py'
s=original.read_text(encoding='utf8').replace("closed('recovery65_actual_flag17_after_verified_best38_direct17_v1_20261011')","closed('actual191_original_QA102_main_delivery_completion_bridge71_v1_20261011');closed('actual_rank120_rank60_after183_disagreement_CDF8_screen75_v1_20261011')")
s=s.replace('complete190','complete191').replace('formal190','formal191').replace('>190:continue','>191:continue').replace('17726','17753').replace('verified190','verified191').replace('第190轮','第191轮').replace('完整190轮','完整191轮').replace('榜_v2_20261011','榜_v3_20261011').replace('location_v2_20261011','location_v3_20261011')
needle=" best=read(A/'alternate_verified_best_blend38_submission_delivery_v1_20261011.json')";assert s.count(needle)==1
s=s.replace(needle,""" candidates=[]
 for pointer in sorted(A.glob('alternate_verified_*submission_delivery_v1_20261011.json')):
  value=read(pointer)
  if value.get('all_full_native_independent_reload_csv_and_cold80_checks_passed') and value.get('actual_main_commit') and Path(value['output']).is_dir():candidates.append((value['official_TRAIN_internal_score'],str(pointer),value))
 assert candidates;_,best_path,best=max(candidates,key=lambda r:(r[0],r[1]));sources[best_path]=sha(best_path)
""")
builder=A/'build_complete191_plus_completed_raw_TRAIN_score_catalog_v3_20261011.py';ast.parse(s);assert not builder.exists();builder.write_text(s,encoding='utf8')
oldpub=A/'publish_actual_complete190_and_raw_TRAIN_score_catalog_v2_main_v1_20261011.py';s=oldpub.read_text(encoding='utf8').replace('complete190','complete191').replace('original190','original191').replace('catalog_v2','catalog_v3').replace('location_v2','location_v3').replace('第190轮','第191轮')
publisher=A/'publish_actual_complete191_and_raw_TRAIN_score_catalog_v3_main_v1_20261011.py';ast.parse(s);assert not publisher.exists();publisher.write_text(s,encoding='utf8')
proof=A/'actual_complete191_and_disagreement_completed_catalog_v3_sources_admission_v1_20261011.json';create(proof,{'status':'frozen_exact_original17753_formal191_after_actual_QA102_main_plus_completed_evidence_raw_records_only_no_partial_scoring_or_candidate_qualification_assumption','input_sha256':{str(p):sha(p) for p in [Path(__file__),original,oldpub,builder,publisher]},'expected_formal_records':17753,'new_scientific_scores_by_catalog':0,'candidate_qualification_separate':True})
for name,p in [('actual_complete191_plus_completed_raw_TRAIN_score_catalog_v3_20261011',builder),('actual_complete191_and_raw_TRAIN_score_catalog_v3_main_v1_20261011',publisher)]:
 assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
print({'exact17753_formal191_and_completed_raw_catalog_queued':True,'partial_scores_and_new_candidate_qualification_not_claimed':True},flush=True)
