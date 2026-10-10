"""Extend actual progress with micro131 and explicit administrative recovery stages."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from atomic_optimization_observer_writes_20261005 import write
from monitor_full_actual_optimization_until2355_v27_20261007 import snapshot as original

def snapshot():
    data=original();number=131;folder=A/'nonflag_RidgeMicro40_official_comparison_v1_20261007'
    rows=[read(p) for p in folder.glob('case*_official.json')];full=A/f'optimization_20261003_r{number}/full_registration_execution.json';receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
    qualified=full.is_file() and receipt.is_file() and read(full)['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
    data['rounds']['131']={'family':'nonflag_RidgeMicro40','actual_completed_official_comparisons':len(rows),'expected_comparisons':40,
      'best_scored_so_far':max([r['connected_final_score'] for r in rows],default=None),'actual_full_board_and_main_closed':qualified,
      'stage':read(folder/'actual_stage.json') if (folder/'actual_stage.json').exists() else None}
    if qualified:
        score=read(A/'optimization_20261003_r131/selection.json')['winner']['metrics']['final_score'];data['latest_fully_qualified_round']=131
        if score>data['best_fully_qualified_score']:data['best_fully_qualified_round']=131;data['best_fully_qualified_score']=score
    services={}
    for name in ['nonflag_RidgeFine52_round128_full_registration_v2','nonflag_RFF128StreamMid76_actual129_after128_dependency_queue_v2',
      'nonflag_EmpiricalBayes40_actual130_after129_dependency_queue_v5','nonflag_RidgeMicro40_actual131_after130_dependency_queue']:
        f=A/'service_owned_workflows_20261006'/name;row=read(f/'native_launch.json')
        services[name]={'owned_live':owned(row),'actual_execution':read(f/'service_execution.json') if (f/'service_execution.json').exists() else None}
    data['current_actual_recovery_and_dispatch_services']=services
    data['historical_admin_failure_records_retained_and_not_marked_passed']=True
    return data

def main():
    while True:
        write(A/'single_host_optimization_full_live_status_v28_20261007.json',snapshot());time.sleep(15)

if __name__=='__main__':main()
