from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from run_protected167_complete_family_v1_20261010 import junction
assert allowed()
names=['normalize_rank120_rank60_protected37_early_v1_20261011.py','qualify_rank120_rank60_protected37_early_selected_native14_v2_20261011.py','prepare_Rank120Rank60ProtectedEarly_selected_candidate_v2_20261011.py','run_Rank120Rank60ProtectedEarly_selected_candidate_feature_cache_v2_20261011.py','seal_Rank120Rank60ProtectedEarly_selected_candidate_v2_20261011.py','rank120_rank60_protected_early_storage_v1_20261011.py']
def changed(s):
 s=s.replace('rank120_rank60_protected37_early','rank120_rank60_best_blend_fraction38_early').replace('Rank120Rank60ProtectedEarly','Rank120Rank60BestBlend38Early').replace('rank120_rank60_protected_early_storage','rank120_rank60_best_blend_fraction38_early_storage').replace('60与120日37项提前完整候选','60与120日最佳组合38项提前完整候选')
 s=s.replace('pilot37.json','pilot38.json').replace('normalized37_actual','normalized38_actual').replace('actual37_capsules','actual38_capsules').replace('selected_by_all37','selected_by_all38').replace('actual_all37_official_controls','actual_all38_official_controls')
 s=s.replace("len(pilot['records'])==37","len(pilot['records'])==38").replace("proof['new_quality_score_records']==37","proof['new_quality_score_records']==38").replace('(36,108)','(37,111)').replace("'expected_scored_records':37","'expected_scored_records':38").replace('expected_scored_records=37','expected_scored_records=38').replace("'scored_records':37","'scored_records':38").replace("'actual_nonidentity_full_controls':36","'actual_nonidentity_full_controls':37").replace("'actual_nonidentity_prefix_controls':108","'actual_nonidentity_prefix_controls':111")
 return s
outputs=[]
for name in names:
 p=A/name;s=changed(p.read_text(encoding='utf8'))
 if name.startswith('normalize_'):
  s=s.replace('actual_rank120_rank60_after183_protected37_screen_v2_20261011','actual_rank120_rank60_after183_best_blend_fraction38_screen_v1_20261011').replace('StockRank120Rank60_after183_protected37_screen_v1_20261011','StockRank120Rank60_after183_best_blend_fraction38_screen_v1_20261011')
 if name.startswith('qualify_'):
  s=s.replace("    closed('actual_stock_rank60seed10_embedding_small512_bank6_v1_20261011')","    closed('Rank120Rank60ProtectedEarly_selected_candidate_sealing_v1_20261011')")
 q=A/changed(name);ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8');outputs.append(q)
protocol=A/'rank120_rank60_best_blend_fraction38_early_sources_admission_v2_20261011.json'
create(protocol,{'status':'predeclared_all38_best_selection_after_completed_official_TRAIN_only_scores_before_new_candidate_future_full_native_independent_and_cold80_required','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in names],*outputs,A/'rank120_rank60_best_blend_fraction38_predeclared_sources_admission_v1_20261011.json']},'expected_official_records':38,'full_independent_controls':37,'prefix_controls':111,'actual_physical_models_if_new':37,'new_fits_or_scores':0,'actual_future_X_read':False,'test_labels_read':False})
import importlib
storage=importlib.import_module(changed(Path(names[-1]).stem))
for logical,physical in storage.OUTPUTS.items():
 assert not logical.exists() and not physical.exists();physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical)
jobs=[('actual_rank120_rank60_best_blend_fraction38_early_normalization_v1_20261011',outputs[0].name),('actual_rank120_rank60_best_blend_fraction38_early_selected_native14_v1_20261011',outputs[1].name),('Rank120Rank60BestBlend38Early_selected_candidate_preparation_v1_20261011',outputs[3].name),('Rank120Rank60BestBlend38Early_selected_candidate_sealing_v1_20261011',outputs[4].name)]
for name,driver in jobs:
 assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(protocol):sha(protocol)});create(A/(name+'_activation.json'),r)
print({'new_candidate_helpers':len(jobs),'physical_models_if_selected':37,'new_fits':0,'actual_future_inference_not_yet_claimed':True},flush=True)
