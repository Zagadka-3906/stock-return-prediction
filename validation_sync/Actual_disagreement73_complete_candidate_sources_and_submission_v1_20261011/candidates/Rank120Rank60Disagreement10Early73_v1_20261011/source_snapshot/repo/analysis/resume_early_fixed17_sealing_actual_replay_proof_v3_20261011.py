"""Resume only sealing after actual full inference; retain original wrong-name failure."""
from pathlib import Path
import sys,ast,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
 assert allowed()
 old=A/'service_owned_workflows_20261006/actual_StockRank60Fixed17Early2_selected_candidate_sealing_v2_20261011'
 assert read(old/'service_execution.json')['status']=='failed' and not owned(read(old/'native_launch.json'))
 release=A/'StockRank60Fixed17Early2_selected_release_v2_20261011'
 ready=read(release/'inference_ready.json');candidate=Path(ready['source_candidate'])
 assert ready['new_inference_claimed'] and ready['actual_saved_native_models']==36
 actual=candidate/'stock_rank60_embedding_complete_parent_native_replay_verification.json'
 proof=read(actual)
 assert proof['status']=='passed_actual_complete_qualified_parent_stock_rank60_embedding_two_full_native_independent_replays_and_cold80'
 assert proof['actual_saved_model_count']==36
 assert not (candidate/'manifest.json').exists() and not (candidate/'source_package_verification.json').exists()
 source=A/'seal_StockRank60Fixed17Early2_selected_candidate_v2_20261011.py'
 text=source.read_text(encoding='utf8')
 changes={'stock_rank60_direct_embedding_complete_parent_native_replay_verification.json':'stock_rank60_embedding_complete_parent_native_replay_verification.json',
 'passed_actual_complete_qualified_parent_stock_rank60_direct_embedding_two_full_native_independent_replays_and_cold80':'passed_actual_complete_qualified_parent_stock_rank60_embedding_two_full_native_independent_replays_and_cold80'}
 for before,after in changes.items():assert text.count(before)==1;text=text.replace(before,after)
 # Include this post-inference sealing repair as evidence rather than changing the pre-inference snapshot.
 needle="    create(candidate/'source_package_verification.json'"
 assert text.count(needle)==1
 insert="""    repair=A/'early_fixed17_actual_replay_filename_sealing_recovery_v3_20261011.json'
    for extra in [Path(__file__),repair]:
        target=candidate/'evidence/post_inference_sealing_repair'/extra.name
        target.parent.mkdir(parents=True,exist_ok=True);os.link(extra,target);assert sha(extra)==sha(target)
"""
 text=text.replace(needle,insert+needle)
 driver=A/'seal_StockRank60Fixed17Early2_selected_candidate_v3_20261011.py';ast.parse(text);assert not driver.exists();driver.write_text(text,encoding='utf8')
 repair=A/'early_fixed17_actual_replay_filename_sealing_recovery_v3_20261011.json'
 pins={str(p):sha(p) for p in [Path(__file__),source,driver,actual,old/'service_execution.json',release/'inference_ready.json']}
 create(repair,{'status':'actual_full36_native_independent_cold80_replay_proof_name_and_status_checked_before_sealing_only_resume',
  'input_sha256':pins,'old_failed_sealer_preserved':True,'all_original_full_checks_retained':True,
  'pre_inference_sources_and_models_and_predictions_not_changed':True,'new_fits':0,'new_scores':0,'new_inference':0,'test_labels_read':False})
 from start_fast_completed_owned_service_v1_20261011 import start_service
 assert allowed()
 print(start_service('actual_StockRank60Fixed17Early2_selected_candidate_sealing_v3_20261011',driver.name,[],{**pins,str(repair):sha(repair)}),flush=True)
 pubsource=A/'publish_early_fixed60_complete_candidate_and_own_aliases_main_v1_20261011.py'
 pub=pubsource.read_text(encoding='utf8').replace('actual_StockRank60Fixed17Early2_selected_candidate_sealing_v2_20261011','actual_StockRank60Fixed17Early2_selected_candidate_sealing_v3_20261011')
 pub=pub.replace("label='Early_fixed60_full_candidate_and_actual_own_aliases'","label='Early_fixed60_full_candidate_and_actual_own_aliases_v2'")
 pub=pub.replace('publish_frozen_early_fixed60_complete_candidate_and_own_aliases_main_v1_20261011.py','publish_frozen_early_fixed60_complete_candidate_and_own_aliases_main_v2_20261011.py')
 pub=pub.replace("A/'seal_StockRank60Fixed17Early2_selected_candidate_v2_20261011.py'","A/'seal_StockRank60Fixed17Early2_selected_candidate_v3_20261011.py'")
 pubdriver=A/'publish_early_fixed60_complete_candidate_and_own_aliases_main_v2_20261011.py';ast.parse(pub);assert not pubdriver.exists();pubdriver.write_text(pub,encoding='utf8')
 assert allowed();print(start_service('actual_early_fixed60_complete_candidate_and_own_aliases_main_v2_20261011',pubdriver.name,[],{str(pubdriver):sha(pubdriver),str(repair):sha(repair)}),flush=True)

if __name__=='__main__':main()
