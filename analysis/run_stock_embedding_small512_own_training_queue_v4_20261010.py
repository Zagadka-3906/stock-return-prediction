"""Serial new GPU recipe after the actual172 candidate has completed both replays."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from scheduled_user_pause_20261007 import write
OUT=A/'stock_embedding_small512_own_training_queue_v1_20261010'
def main():
    assert allowed();OUT.mkdir(exist_ok=False)
    predecessor='Frontier133172_selected_candidate_sealing_v1_20261010'
    write(OUT/'state.json',{'status':'waiting_actual172_candidate_sealing_no_GPU_overlap','actual_service':predecessor,'new_quality_scores':0})
    closed('actual_frontier133_2020_TRAIN_native42_controls_v1_20261010')
    closed('actual_cross120_recent252_return_own_controls_and_training_queue_v2_20261010')
    assert not (A/'service_owned_workflows_20261006/Frontier233171_selected_candidate_preparation_v1_20261010/native_launch.json').exists()
    assert not Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists()
    if not allowed():return
    for proof in ('stock_embedding_small512_sources_admission_v1_20261010.json','stock_embedding_actual_full5_routes_admission_v2_20261010.json'):
        for p,d in read(A/proof)['input_sha256'].items():assert sha(p)==d,p
    for p,d in read(A/'stock_embedding_E_cache_safe_runtime_admission_v3_20261010.json')['input_sha256'].items():assert sha(p)==d,p
    fixture=Path(read(A/'actual_stock_embedding_mature_fixture_location_v1_20261010.json')['output'])
    assert read(fixture/'verification.json')['status'].startswith('passed')
    tasks=[('actual_stock_embedding_small512_restart_v1_20261010','verify_stock_embedding_small512_restart_v3_20261010.py'),('StockEmbeddingSmall512_independent_small_CPU_v1_20261009','verify_stock_embedding_small512_small_CPU_v3_20261010.py'),('actual_stock_embedding_small512_bank6_v1_20261010','train_stock_embedding_small512_BF16_bank6_v3_20261010.py'),('StockEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','verify_stock_embedding_small512_full5_independent_v3_20261010.py')]
    for name,driver in tasks:
        if not allowed():return
        if name=='actual_stock_embedding_small512_bank6_v1_20261010':
            write(OUT/'state.json',{'status':'restart_and_independent_CPU_admission_complete_waiting_actual172_seal_before_six_fits','actual_service':predecessor,'new_quality_scores':0})
            closed(predecessor)
            if not allowed():return
        pins={str(p):sha(p) for p in [A/driver,A/'stock_embedding_small512_BF16_native_v1_20261010.py',A/'stock_identity_embedding_network_v1_20261010.py',A/'stock_embedding_saved_tensor_decoder_v1_20261010.py']}
        row=start_service(name,driver,[],pins);create(OUT/(name+'_launch.json'),row)
        write(OUT/'state.json',{'status':'actual_new_stock_embedding_training_or_admission','actual_service':name,'new_quality_scores':0})
        while owned(row):
            if not allowed():return
            time.sleep(15)
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed'
    write(OUT/'state.json',{'status':'actual_stock_embedding_six_fits_and_independent_full5_complete_official_scoring_pending','new_quality_scores':0})
if __name__=='__main__':main()
