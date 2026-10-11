from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from scheduled_user_pause_20261007 import write
def main():
    assert allowed()
    proof=read(A/'stock_embedding_checkpoint_yield_training_admission_v5_20261010.json')
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_stock_embedding_small512_bank6_v1_20261010','train_stock_embedding_small512_BF16_bank6_checkpoint_yield_v5_20261010.py'),('StockEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','verify_stock_embedding_small512_full5_independent_v3_20261010.py')]
    state=A/'stock_embedding_small512_own_training_queue_v1_20261010/state.json'
    for name,driver in tasks:
        assert allowed()
        if name=='StockEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009' and Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists():closed('Frontier133172_selected_candidate_sealing_v1_20261010')
        row=start_service(name,driver,[],{str(A/driver):sha(A/driver)})
        create(A/'stock_embedding_small512_own_training_queue_v1_20261010'/(name+'_launch.json'),row)
        write(state,{'status':'actual_checkpoint_yield_new_stock_embedding_training_or_full5','actual_service':name,'new_quality_scores':0})
        while owned(row):
            if not allowed():return
            time.sleep(15)
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed'
    write(state,{'status':'actual_stock_embedding_six_fits_and_independent_full5_complete_official_scoring_pending','new_quality_scores':0})
if __name__=='__main__':main()
