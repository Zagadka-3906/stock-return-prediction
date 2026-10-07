"""Show actual signed132 records, deadline defer state and main receipts."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write
from monitor_full_actual_optimization_until2355_v28_20261007 import snapshot as original

def snapshot():
    data=original();folder=A/'nonflag_ReverseBayes40_official_comparison_v1_20261007'
    rows=[read(p) for p in folder.glob('case*_official.json')]
    full=A/'optimization_20261003_r132/full_registration_execution.json';receipt=A/'github_validation_sync_main_20261005/round132_receipt.json'
    qualified=full.is_file() and receipt.is_file() and read(full)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
    deferred=A/'nonflag_ReverseBayes40_round132_dispatch_deferred_until_manual_continue_20261007.json'
    data['rounds']['132']={'family':'nonflag_ReverseBayes40','actual_completed_official_comparisons':len(rows),'expected_comparisons':40,
      'best_scored_so_far':max([r['connected_final_score'] for r in rows],default=None),'actual_full_board_and_main_closed':qualified,
      'stage':read(folder/'actual_stage.json') if (folder/'actual_stage.json').exists() else None,
      'administrative_dispatch_deferred':read(deferred) if deferred.is_file() else None,'dispatch_cutoff_at_local':'2026-10-07T23:12:00+08:00'}
    if qualified:
        score=read(A/'optimization_20261003_r132/selection.json')['winner']['metrics']['final_score'];data['latest_fully_qualified_round']=132
        if score>data['best_fully_qualified_score']:data['best_fully_qualified_round']=132;data['best_fully_qualified_score']=score
    for name in ['nonflag_ReverseBayes40_actual132_after131_dependency_queue_v2','signed132_actual_import_recovery_main_publication']:
        f=A/'service_owned_workflows_20261006'/name
        if (f/'native_launch.json').is_file():
            row=read(f/'native_launch.json');data['current_actual_recovery_and_dispatch_services'][name]={'owned_live':owned(row),'actual_execution':read(f/'service_execution.json') if (f/'service_execution.json').exists() else None}
    return data

def main():
    while True:write(A/'single_host_optimization_full_live_status_v29_20261007.json',snapshot());time.sleep(15)

if __name__=='__main__':main()
