from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from scheduled_user_pause_20261007 import write
OUT=A/'stock_rank_embedding_own_training_queue_v2_20261010'
def main():
    assert allowed();OUT.mkdir(exist_ok=False)
    closed('actual_stock_embedding_six_state_native42_v2_20261010')
    closed('actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010')
    for name in ('stock_rank_embedding_own_sources_and_actual_centered_target_admission_v1_20261010.json','stock_rank_embedding_actual_priority173_runtime_admission_v2_20261010.json'):
        for p,d in read(A/name)['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_stock_rank_embedding_small512_restart_v1_20261010','verify_stock_rank_embedding_small512_restart_priority173_v2_20261010.py'),('StockRankEmbeddingSmall512_independent_small_CPU_v1_20261009','verify_stock_rank_embedding_small512_small_CPU_v1_20261010.py'),('actual_stock_rank_embedding_small512_bank6_v1_20261010','train_stock_rank_embedding_small512_BF16_bank6_checkpoint_yield_priority173_v2_20261010.py'),('StockRankEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','verify_stock_rank_embedding_small512_full5_independent_v1_20261010.py')]
    for name,driver in tasks:
        if not allowed():return
        if name!='StockRankEmbeddingSmall512_independent_small_CPU_v1_20261009' and Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists():
            write(OUT/'state.json',{'status':'new_rank_recipe_checkpoint_or_GPU_phase_waiting_existing173_candidate_seal','actual_service':name,'new_quality_scores':0})
            closed('StockEmbedding173_selected_candidate_sealing_v1_20261010')
            if not allowed():return
        p=A/driver;row=start_service(name,driver,[],{str(p):sha(p)})
        create(OUT/(name+'_launch.json'),row);write(OUT/'state.json',{'status':'actual_new_centered_rank_stock_embedding_controls_or_six_fits','actual_service':name,'new_quality_scores':0})
        while owned(row):
            if not allowed():return
            time.sleep(15)
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed'
    write(OUT/'state.json',{'status':'new_rank_stock_embedding_six_models_full5_complete_exact_stage_and_official_scores_pending','new_quality_scores':0})
if __name__=='__main__':main()
