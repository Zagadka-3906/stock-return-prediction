"""Persist actual new directions and next dependencies without changing active workers."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();now=datetime.now(timezone(timedelta(hours=8)))
    state=read(A/'optimization_live_progress_v64_20261010.json')
    source=A/'prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010.py'
    create(A/'actual_optimization_fast_runtime_handoff_v112_20261010.json',{'at_local':now.isoformat(),'status':'active_actual_forward5_identity_return_recipe_controls_started_rank5_48_full_pipeline_queued','deadline_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],'actual_best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),'actual_services_and_resources':state,'actual_main_source_receipts':[read(A/'StockRank5Embedding_complete48_sources_main_receipt_v51_20261010.json'),read(A/'StockForward5Embedding_actual_mature_CPU_sources_main_receipt_v52_20261010.json')],'next_steps':['Poll actual Rank5 fast17 and large29; full17748 all records with parent176 require no blind restart','Keep original full173/174/175/176 queues; full173 currently doing real parent Pandas inference, not stalled','Poll forward5-return GPU restart, independent CPU and own6; then prepare own full5 independent GPU and six-state native42 and early17 scoring with new recipe; no actual scores yet','Before every train/score/infer/publish read both controls and local time; stop20261011 11:00 guardian already active','Do not mutate pinned sources, root .git index or pending bank checkpoints; E large scratch only','Register177 copied metadata key existing_own_stock_Top10_BCE_native_bank_fits is a legacy caption; actual Bank/native CONFIG/target/epoch and plan authoritative Rank5 e64; preserve source and add explicit provenance erratum to publication rather than reinterpret as actual BCE fitting'],'source_sha256':{str(source):sha(source)},'new_full_submission_qualification_claimed':False,'test_labels_read':False})
    print({'actual_handoff112_saved':True,'goal_remains_active':True},flush=True)
if __name__=='__main__':main()
