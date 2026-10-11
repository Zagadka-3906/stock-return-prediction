"""Combine a genuinely new flag-only stage with the actual strongest fully inferred37-model scheme."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def main():
 assert allowed()
 delivery=A/'alternate_verified_best_blend38_submission_delivery_v1_20261011.json';parent=read(delivery)
 assert parent['all_full_native_independent_reload_csv_and_cold80_checks_passed'] and parent['models']==37 and not parent['test_labels_read']
 candidate=Path(parent['source_candidate']);assert sha(candidate/'manifest.json')==parent['source_candidate_manifest_sha256']
 release=A/'Rank120Rank60BestBlend38Early_selected_release_v1_20261011';ready=read(release/'selected_candidate_ready_for_registration.json')
 assert ready['sealed_candidate_complete'] and ready['new_inference_claimed'] and ready['actual_saved_native_models']==37
 assert read(Path(parent['main_receipt']))['status']=='pushed_and_remote_head_verified'
 old=A/'run_rank60_flag17_after183_direct17_v1_20261011.py';s=old.read_text(encoding='utf8')
 s=s.replace('StockRank60FlagOnly_after183_direct17_screen','StockRank60FlagOnly_after_verified_best38_direct17_screen')
 s=s.replace("closed('actual_rank60medium2048_gain_selected_full_candidate_queue_v1_20261011')","closed('actual_stock_rank60_flag17_after183_direct17_v1_20261011')")
 s=s.replace("A/'optimization_20261003_r183/selected_validation.npy'","A/'Rank120Rank60BestBlend38Early_selected_release_v1_20261011/selected_validation.npy'")
 s=s.replace("A/'optimization_20261003_r183/calibrated_csv_official.json'","A/'Rank120Rank60BestBlend38Early_selected_release_v1_20261011/calibrated_csv_official.json'")
 s=s.replace('anchor183','anchor_verified_best38')
 needle="    paths.extend([Path(panel_cache.__file__),A/'immutable_prepared_rank_panel_cache_actual_full_TRAIN_benchmark_v1_20261010.json'])";assert s.count(needle)==1
 s=s.replace(needle,needle+"\n    paths.extend([A/'flag17_after_verified_best38_raw_sources_admission_v1_20261011.json',A/'alternate_verified_best_blend38_submission_delivery_v1_20261011.json',A/'Rank120Rank60BestBlend38Early_selected_release_v1_20261011/selected_candidate_ready_for_registration.json'])")
 q=A/'run_flag17_after_verified_best38_direct17_v1_20261011.py';ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8',newline='\n')
 paths=[Path(__file__),old,q,delivery,release/'selected_candidate_ready_for_registration.json',release/'selected_validation.npy',release/'calibrated_csv_official.json',candidate/'manifest.json',Path(parent['main_receipt'])]
 proof=A/'flag17_after_verified_best38_raw_sources_admission_v1_20261011.json';create(proof,{'status':'predeclared_actual_complete37_model_best38_parent_plus_flag_only17_TRAIN_validation_before_new_scores','input_sha256':{str(p):sha(p) for p in paths},'actual_parent_score':parent['official_TRAIN_internal_score'],'actual_parent_unique_models':37,'actual_parent_source_candidate':str(candidate),'parent_full_connected_board_pending':True,'actual_parent_all_native_independent_reload_cold80_main_complete':True,'new_fits':0,'new_scores':0,'expected_official_records':17,'expected_full_controls':16,'expected_prefix_controls':48,'submission_candidate_qualification_pending':True,'test_labels_read':False})
 # The original flag17 direct branch retains its own scores; this new composition waits for it.
 assert allowed();i=start_service('actual_flag17_after_verified_best38_direct17_v1_20261011',q.name,[],{str(q):sha(q),str(proof):sha(proof)});create(A/'actual_flag17_after_verified_best38_direct17_activation_v1_20261011.json',i)
 rawpub=A/'run_publish_rank60_flag17_after183_completed17_main_v1_20261011.py';text=rawpub.read_text(encoding='utf8')
 text=text.replace('actual_stock_rank60_flag17_after183_direct17','actual_flag17_after_verified_best38_direct17').replace('StockRank60FlagOnly_after183_direct17_screen','StockRank60FlagOnly_after_verified_best38_direct17_screen').replace('rank60_flag17_raw_sources_predeclared','flag17_after_verified_best38_raw_sources_admission').replace('Rank60FlagOnly_after183_actual17','FlagOnly_after_verified_best38_actual17')
 r=A/'run_publish_flag17_after_verified_best38_completed17_main_v1_20261011.py';ast.parse(text);assert not r.exists();r.write_text(text,encoding='utf8',newline='\n')
 assert allowed();i=start_service('actual_flag17_after_verified_best38_completed17_main_v1_20261011',r.name,[],{str(r):sha(r),str(proof):sha(proof)});create(A/'actual_flag17_after_verified_best38_completed17_main_activation_v1_20261011.json',i)
 print('Best38 full37 parent plus flag17 composition frozen; full16 and prefix48 official scoring queued; no new fit',flush=True)

if __name__=='__main__':main()
