from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();old=A/'run_stock_rank20class10_embedding_after175_fast17_screen_v1_20261011.py';new=A/'run_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011.py';assert not new.exists()
 s=old.read_text(encoding='utf8').replace('after175','after183').replace('anchor175','anchor183').replace('parent175','parent183').replace('parent_round\':175','parent_round\':183').replace('r175','r183').replace('round175','round183')
 s=s.replace("closed('StockTop10Embedding175_selected_candidate_sealing_recovery_v2_20261010')","closed('recovery15_StockRank20Embedding183_selected_candidate_sealing_v1_20261010')")
 s=s.replace("release['scored_records']==47","release['scored_records']==85")
 needle="    closed('actual_stock_rank20class10_embedding_six_state_native42_v1_20261011')"
 assert needle in s;s=s.replace(needle,"    closed('actual_stock_rank20class10_embedding_after175_large_allocation29_screen_v1_20261011')\n"+needle)
 assert "optimization_20261003_r175" not in s and "round175_receipt" not in s
 compile(s,str(new),'exec');new.write_text(s,encoding='utf8',newline='\n')
 rows=__import__(new.stem).cases();assert len(rows)==17
 proof=A/'stock_rank20class10_latest_qualified183_predeclared17_sources_v1_20261011.json';paths=[Path(__file__),old,new,A/'optimization_20261003_r183/calibrated_csv_official.json',A/'github_validation_sync_main_20261005/round183_receipt.json',A/'stock_rank20class10_BCE_own6_sources_admission_v1_20261011.json'];create(proof,{'status':'compiled17_against_latest_fully_qualified183_and_causal_BCE_own_bank_before_scores','input_sha256':{str(p):sha(p) for p in paths},'parent_round':183,'cases':rows,'new_fits':0,'new_scores':0,'future_X_read':False,'test_labels_read':False})
 assert allowed();r=start_service('actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011',new.name,[],{str(new):sha(new),str(proof):sha(proof)});create(A/'actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_activation_v1_20261011.json',r)
 print({'latest183_top10_BCE17_queued_after_actual46','no_new_model_fit'},flush=True)
if __name__=='__main__':main()
