from pathlib import Path
import sys,runpy,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def dispatch(name,driver,protocol):
 assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p),str(protocol):sha(protocol)});create(A/(name+'_activation.json'),r);closed(name)
def main():
 assert allowed();closed('actual_rank120_rank60_after183_consensusFraction8_screen88_v1_20261011');closed('actual_consensusWeight8_results_selection_main85_v1_20261011')
 folder=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_consensusFraction8_screen88_v1_20261011');proof=read(folder/'verification.json')
 assert proof['new_quality_score_records']==len(proof['records'])==8 and (proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls'])==(7,21)
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 for row in proof['records']:
  cap=Path(row['official_score_cache']['official_metrics_source']);assert sha(cap)==row['official_metric_capsule_sha256'] and read(cap)['metrics']==row['metrics']
  controls=folder/f"case{row['case']:03d}_controls.json";assert sha(controls)==row['control_sha256']
 references=[A/'alternate_verified_best_blend38_submission_delivery_v1_20261011.json',A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json'];reference_data=[read(p) for p in references]
 incumbent=max(reference_data[0]['official_TRAIN_internal_score'],reference_data[1]['best']['connected_final_score'])
 prior=A/'rank120_rank60_consensusWeight8_gain_decision85_v1_20261011.json';incumbent=max(incumbent,read(prior)['best']['connected_final_score']);references.append(prior)
 best=min(proof['records'],key=lambda r:(-r['connected_final_score'],abs(r['configuration'].get('disagreement_penalty') or 0),r['configuration']['weight'],r['case']));adopt=best['connected_final_score']>incumbent
 decision=A/'rank120_rank60_consensusFraction8_gain_decision89_v1_20261011.json';create(decision,{'status':'actual8_TRAIN_S_only_selection_vs_highest_complete38_and_actual10_protected_records','adopt':adopt,'best':best,'incumbent_S':incumbent,'input_sha256':{str(p):sha(p) for p in [folder/'verification.json',*references]},'test_labels_read':False})
 # Export every actual score and scientific source; scientific and full-board qualification remain separate.
 original=A/'run_publish_completed_rank120_rank60_disagreement10_main_v1_20261011.py';s=original.read_text(encoding='utf8')
 for before,after in [('actual_completed_disagreement10_pointer_namespace_bridge72_v1_20261011','actual_rank120_rank60_after183_consensusFraction8_screen88_v1_20261011'),('StockRank120Rank60_after183_disagreement10_screen_v1_20261011','StockRank120Rank60_after183_consensusFraction8_screen88_v1_20261011'),('rank120_rank60_disagreement10_predeclared_sources_admission_v1','rank120_rank60_consensusFraction8_predeclared_sources88_v1'),("len(proof['records'])==10","len(proof['records'])==8"),("proof['actual_nonidentity_full_controls']==9","proof['actual_nonidentity_full_controls']==7"),("proof['actual_nonidentity_prefix_controls']==27","proof['actual_nonidentity_prefix_controls']==21"),('Rank120Rank60Disagreement_after183_actual10','Rank120Rank60ConsensusFraction_after183_actual8_89'),('actual10_disagreement','actual8_disagreement_CDF'),("'actual_nonidentity_full_Pandas_controls':9","'actual_nonidentity_full_Pandas_controls':7"),("'actual_prefix_controls':27","'actual_prefix_controls':21")]:s=s.replace(before,after)
 pubdriver=A/'run_publish_actual_completed_consensusFraction8_all_records89_v1_20261011.py';assert not pubdriver.exists();compile(s,str(pubdriver),'exec');pubdriver.write_text(s,encoding='utf8')
 protocol=A/'rank120_rank60_consensusFraction8_early89_sources_admission_v2_20261011.json'
 if adopt:
  assert best['configuration']['kind']=='valid_pool_protection_v1'
  for p,d in read(protocol)['input_sha256'].items():assert sha(p)==d,p
  storage=importlib.import_module('rank120_rank60_consensusFraction8_early89_storage_v1_20261011')
  from run_protected167_complete_family_v1_20261010 import junction
  for logical,physical in storage.OUTPUTS.items():
   assert not logical.exists() and not physical.exists();physical.mkdir(parents=True);logical.parent.mkdir(parents=True,exist_ok=True);junction(logical,physical)
  for name,driver in [('actual_rank120_rank60_consensusFraction8_early89_normalization_v1_20261011','normalize_rank120_rank60_consensusFraction8_early89_v1_20261011.py'),('actual_rank120_rank60_consensusFraction8_early89_selected_native14_v1_20261011','qualify_rank120_rank60_consensusFraction8_early89_selected_native14_v2_20261011.py'),('Rank120Rank60ConsensusFraction8Early89_selected_candidate_preparation_v1_20261011','run_Rank120Rank60ConsensusFraction8Early89_selected_candidate_feature_cache_v2_20261011.py'),('Rank120Rank60ConsensusFraction8Early89_selected_candidate_sealing_v1_20261011','seal_Rank120Rank60ConsensusFraction8Early89_selected_candidate_v2_20261011.py'),('actual_consensusFraction89_complete_candidate_main_v1_20261011','publish_actual_consensusFraction89_complete_candidate_main_v1_20261011.py'),('actual_verified_consensusFraction89_alternate_submission_delivery_v1_20261011','prepare_verified_consensusFraction89_alternate_submission_delivery_v1_20261011.py')]:dispatch(name,driver,protocol)
  actual=read(A/'alternate_verified_consensusFraction89_submission_delivery_v1_20261011.json');assert actual['all_full_native_independent_reload_csv_and_cold80_checks_passed'] and actual['official_TRAIN_internal_score']==best['connected_final_score']
  create(A/'rank120_rank60_consensusFraction8_selected_full_candidate_complete89_v1_20261011.json',actual)
 assert allowed();runpy.run_path(str(pubdriver),run_name='__main__')
 create(A/'actual_consensusFraction8_all8_scores_main_and_conditional_delivery89_complete_v1_20261011.json',{'status':'passed_all8_actual_scientific_controls_and_main_publication_conditional_full_candidate_complete_only_if_S_gain','adopt':adopt,'best_S':best['connected_final_score'],'decision_sha256':sha(decision),'incumbent_S':incumbent,'test_labels_read':False})
if __name__=='__main__':main()
