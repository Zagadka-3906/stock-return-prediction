"""Prepare isolated, source-pinned full inference only after an actual TRAIN S gain."""
from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def main():
 assert allowed()
 originals=['normalize_rank120_rank60_best_blend_fraction38_early_v1_20261011.py','qualify_rank120_rank60_best_blend_fraction38_early_selected_native14_v2_20261011.py','prepare_Rank120Rank60BestBlend38Early_selected_candidate_v2_20261011.py','run_Rank120Rank60BestBlend38Early_selected_candidate_feature_cache_v2_20261011.py','seal_Rank120Rank60BestBlend38Early_selected_candidate_v2_20261011.py','rank120_rank60_best_blend_fraction38_early_storage_v1_20261011.py','rank120_rank60_protected_after_qualified183_native_stage_v1_20261011.py','predict_rank120_rank60_protected_complete_qualified183_scheme_v1_20261011.py']
 def rename(s):
  for before,after in [('rank120_rank60_best_blend_fraction38_early','rank120_rank60_disagreement10_early73'),('Rank120Rank60BestBlend38Early','Rank120Rank60Disagreement10Early73'),('60与120日最佳组合38项提前完整候选','60与120日分歧10项完整候选73'),('rank120_rank60_protected_after_qualified183_native_stage_v1','rank120_rank60_disagreement_after_qualified183_native_stage73_v1'),('predict_rank120_rank60_protected_complete_qualified183_scheme_v1','predict_rank120_rank60_disagreement_complete_qualified183_scheme73_v1'),('rank120_rank60_protected_after_complete_qualified_parent_v1','rank120_rank60_disagreement_after_complete_qualified_parent73_v1'),('stock_rank120_rank60_protected_label_horizon_ID16_cross120_recent252_e64','stock_rank120_rank60_disagreement_label_horizon_ID16_cross120_recent252_e64'),('rank120_rank60_protected_raw_average','rank120_rank60_disagreement_raw_fusion'),('rank120_weight','disagreement_penalty'),('rank20_two_seed_raw_signal_v1_20261010','rank120_rank60_disagreement_raw_signal_v1_20261011'),('pilot38.json','pilot10.json'),('normalized38_actual','normalized10_actual'),('actual38_capsules','actual10_capsules'),('selected_by_all38','selected_by_all10'),('actual_all38_official_controls','actual_all10_official_controls')]:s=s.replace(before,after)
  for before,after in [("len(pilot['records'])==38","len(pilot['records'])==10"),("len(proof['records'])==proof['new_quality_score_records']==38","len(proof['records'])==proof['new_quality_score_records']==10"),('(37,111)','(9,27)'),("'expected_scored_records':38","'expected_scored_records':10"),('expected_scored_records=38','expected_scored_records=10'),("'scored_records':38","'scored_records':10"),("'actual_nonidentity_full_controls':37","'actual_nonidentity_full_controls':9"),("'actual_nonidentity_prefix_controls':111","'actual_nonidentity_prefix_controls':27"),('passed_normalized38_actual','passed_normalized10_actual'),('in (.125,.5,.875)','in (-.5,-.25,0.,.25,.5)')]:s=s.replace(before,after)
  return s
 outputs=[]
 for name in originals:
  s=rename((A/name).read_text(encoding='utf8'))
  if name.startswith('normalize_'):
   s=s.replace('actual_rank120_rank60_after183_best_blend_fraction38_screen_v1_20261011','actual_completed_disagreement10_pointer_namespace_bridge72_v1_20261011').replace('StockRank120Rank60_after183_best_blend_fraction38_screen_v1_20261011','StockRank120Rank60_after183_disagreement10_screen_v1_20261011')
  if name.startswith('qualify_'):
   # This remains a parent callback prerequisite; the new stage itself is executed fourteen times below.
   needle="A/'rank120_rank60_disagreement10_early73_sources_admission_v2_20261011.json',"
   assert needle in s
   s=s.replace(needle,needle+"A/'rank120_rank60_disagreement_actual_CPU_controls_v1_20261011.json',")
  if name.startswith('prepare_'):
   s=s.replace('by independently matured Rank60/Rank120 raw average and protected-tail permutation','by independently matured Rank60/Rank120 mean with a pointwise disagreement penalty and protected-tail permutation')
  q=A/rename(name);ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8');outputs.append(q)
 protocol=A/'rank120_rank60_disagreement10_early73_sources_admission_v2_20261011.json'
 create(protocol,{'status':'predeclared_conditional_S_gain_only_complete37_native14_cold14_prefit7_full_independent_reload_CSV_cold80_required_before_delivery','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in originals],*outputs,A/'rank120_rank60_disagreement10_predeclared_sources_admission_v1_20261011.json',A/'rank120_rank60_disagreement_actual_CPU_controls_v1_20261011.json']},'expected_official_records':10,'full_independent_controls':9,'prefix_controls':27,'new_training_fits':0,'future_X_read':False,'test_labels_read':False})
 launcher=A/'launch_disagreement10_conditional_full_pipeline73_v1_20261011.py'
 text='''from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('actual_rank120_rank60_disagreement10_S_only_gain_decision_v2_20261011')
 decision=read(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json')
 if not decision['adopt']:
  create(A/'actual_disagreement10_conditional_full_pipeline73_no_gain_v1_20261011.json',{'status':'passed_actual_S_no_gain_no_Test_inference_required','decision_sha256':sha(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json'),'future_X_read':False});return
 assert allowed()
 protocol=A/'rank120_rank60_disagreement10_early73_sources_admission_v2_20261011.json'
 for p,d in read(protocol)['input_sha256'].items():assert sha(p)==d,p
 storage=importlib.import_module('rank120_rank60_disagreement10_early73_storage_v1_20261011')
 from run_protected167_complete_family_v1_20261010 import junction
 for logical,physical in storage.OUTPUTS.items():
  assert not logical.exists() and not physical.exists();physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical)
 jobs=[('actual_rank120_rank60_disagreement10_early73_normalization_v1_20261011','normalize_rank120_rank60_disagreement10_early73_v1_20261011.py'),('actual_rank120_rank60_disagreement10_early73_selected_native14_v1_20261011','qualify_rank120_rank60_disagreement10_early73_selected_native14_v2_20261011.py'),('Rank120Rank60Disagreement10Early73_selected_candidate_preparation_v1_20261011','run_Rank120Rank60Disagreement10Early73_selected_candidate_feature_cache_v2_20261011.py'),('Rank120Rank60Disagreement10Early73_selected_candidate_sealing_v1_20261011','seal_Rank120Rank60Disagreement10Early73_selected_candidate_v2_20261011.py')]
 for name,driver in jobs:
  assert allowed();p=A/driver;result=start_service(name,driver,[],{str(p):sha(p),str(protocol):sha(protocol)});create(A/(name+'_activation.json'),result);closed(name)
 create(A/'actual_disagreement10_conditional_full_pipeline73_sealed_v1_20261011.json',{'status':'passed_complete_candidate_sealed_main_publication_and_delivery_still_required','decision_sha256':sha(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json'),'sealed_ready_sha256':sha(A/'Rank120Rank60Disagreement10Early73_selected_release_v1_20261011/selected_candidate_ready_for_registration.json'),'official_TRAIN_internal_score':decision['best']['connected_final_score'],'test_labels_read':False})
if __name__=='__main__':main()
'''
 ast.parse(text);assert not launcher.exists();launcher.write_text(text,encoding='utf8')
 create(A/'actual_disagreement10_conditional_full_pipeline73_source_preparation_v1_20261011.json',{'status':'passed_AST_and_isolated_namespaces_only_native_execution_not_yet_claimed','input_sha256':{str(p):sha(p) for p in [Path(__file__),launcher,protocol,*outputs]},'original_files_unchanged':all(sha(A/n)==read(protocol)['input_sha256'][str(A/n)] for n in originals),'new_Test_inference':False})
 assert allowed();r=start_service('actual_disagreement10_conditional_full_pipeline73_v1_20261011',launcher.name,[],{str(launcher):sha(launcher),str(protocol):sha(protocol)});create(A/'actual_disagreement10_conditional_full_pipeline73_activation_v1_20261011.json',r)
 print({'prepared_isolated_helpers':len(outputs),'conditional_adoption_only':True,'actual_full_candidate_not_yet_claimed':True},flush=True)
if __name__=='__main__':main()
