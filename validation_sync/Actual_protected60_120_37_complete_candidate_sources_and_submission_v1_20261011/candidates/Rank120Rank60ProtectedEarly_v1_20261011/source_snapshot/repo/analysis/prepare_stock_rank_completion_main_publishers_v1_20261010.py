"""Attach main-only receipts to each completed rank native/scoring validation batch."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    # The source upload finished before its canonical-receipt filename collision.
    out=Path('E:/赛题五_本机临时/StockRankEmbedding_actual_restart_and_predeclared17_main_v36_20261010')
    receipt=read(out/'receipt.json');assert receipt['status']=='pushed_and_remote_head_verified'
    assert receipt['commit']=='017a73a2b6c0211116bb9eaad43bd9adbd997b82' and receipt['raw_git_blobs_verified']==31
    create(A/'StockRankEmbedding_actual_restart_and_predeclared17_main_receipt_v36_20261010.json',dict(receipt,administrative_receipt_filename_recovery_only=True,publication_worker_terminal_status='failed_after_verified_push_due_to_existing_old_receipt_filename'))
    for source,version in [('publish_stock_embedding_six_state_native42_completion_v50_20261010.py',54),('publish_stock_embedding_after170_completion_v53_20261010.py',55)]:
        text=(A/source).read_text(encoding='utf8').replace('stock_embedding','stock_rank_embedding').replace('StockEmbeddingSmall512','StockRankEmbeddingSmall512')
        if version==54:
            text=text.replace('v50_20261010','v54_20261010').replace('actual_stock_rank_embedding_six_state_native42_v2_20261010','actual_stock_rank_embedding_six_state_native42_v1_20261010')
            text=text.replace('stock_rank_embedding_native_stage_and_four_parent_routes_admission_v1_20261010','stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010')
            name='actual_stock_rank_embedding_native42_completion_main_v54_20261010'
        else:
            text=text.replace('v53_20261010','v55_20261010').replace('stock_rank_embedding_after170_fast17_screen_v2_20261010','stock_rank_embedding_after170_fast17_screen_v1_20261010')
            text=text.replace('stock_rank_embedding_after170_predeclared_fast17_selection_plan_v1_20261010','stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010')
            text=text.replace('run_stock_rank_embedding_after170_fast17_screen_v2_20261010','run_stock_rank_embedding_after170_fast17_screen_v1_20261010')
            start=text.index('    for admission in (');end=text.index('    bank=Path',start)
            text=text[:start]+"    for admission in ('stock_rank_embedding_own_sources_and_actual_centered_target_admission_v1_20261010.json','stock_rank_embedding_actual_priority173_runtime_admission_v2_20261010.json','stock_rank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json'):\n        paths += [A/admission,*[Path(p) for p in read(A/admission)['input_sha256'] if Path(p).suffix=='.py']]\n"+text[end:]
            name='actual_stock_rank_embedding_after170_completion_main_v55_20261010'
        dest=A/source.replace('stock_embedding','stock_rank_embedding').replace('v50_','v54_').replace('v53_','v55_')
        assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n')
        row=start_service(name,dest.name,[],{str(dest):sha(dest)})
        create(A/(name+'_activation.json'),row)
    create(A/'actual_optimization_fast_runtime_handoff_v80_20261010.json',{'status':'active_actual_rank_training_and_stock173_complete_flow_queued','deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],'best_fully_qualified_round':170,'best_fully_qualified_S':.45133118626033575,'best_actual_TRAIN_S':.4513497468277574,'stock173_actual_family':'StockEmbedding173_complete36_family_v3_20261010','rank_training_actual_queue':'actual_stock_rank_embedding_own_training_queue_v2_20261010','rank_native42_and_score17_actual_queue':'actual_stock_rank_embedding_native42_and_fast17_queue_v1_20261010','rank_new_quality_scores':0,'rank_GPU_yields_to_actual_stock173_seal':True,'progress_observer':49,'main_source_receipt':receipt,'actual_future_candidate_173_qualified':False,'remaining_work':['Complete193+main,full171;49+main,full172;stock17217+main,36+selected14,freeze/fullfuture173/QA84/main/delivery','Complete rank own6/full5/42/17 and receipts54/55; compare to fully qualified frontier before promoting','No new C models or cache; preserve root index SHA; stop at October11 11:00'],'global_optimization_boundary_proven':False})
    print({'rank_completed_validation_main_publishers':[54,55],'source_main_receipt_recovered':True},flush=True)
if __name__=='__main__':main()
