"""Dispatch preflighted rounds only after actual preceding full QA/main qualification; preserve failed branches."""
from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
    service=A/'service_owned_workflows_20261006'/name
    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(10)
    assert read(service/'service_execution.json')['status']=='passed',name
def main():
    closed('pending139to141_complete_prospective_controls_v18_20261008')
    import recover_pending137to141_registration_contracts_v18_20261008 as h
    h.initialize();assert [c['round'] for c in h.CONFIG]==[139,140,141]
    base=A/'pending137to141_receiver_preparation_v18_20261008.json';controls=A/'pending137to141_collector_controls_v18_20261008.json'
    proof=read(base);assert len(read(controls)['records'])==9
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    pins={str(p):sha(p) for p in [Path(__file__),base,controls,A/'recover_pending137to141_registration_contracts_v18_20261008.py',A/'pending139to141_closed_dependency_recovery_v18_20261008.json']}
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    all_rows={}
    for cfg in h.CONFIG:
        n=cfg['round'];previous={139:'BF16reverse40_round138_full_registration_v17_20261008',140:'HuberCrossFamily112_round139_full_registration_v18_20261008',141:'SpectralGram52_round140_full_registration_v18_20261008'}[n]
        closed(previous)
        for p,d in proof['input_sha256'].items():assert sha(p)==d,p
        assert not any((A/cfg['physical_comparison']).iterdir()),cfg['physical_comparison']
        rows={}
        for name,row in cfg['launches'].items():
            target=h.MAPPING[name];driver=h.MAPPING[Path(row['original_driver']).stem]+'.py'
            assert not (A/'service_owned_workflows_20261006'/target).exists(),target
            rows[target]=start(target,driver,row['original_arguments'],{**pins,str(A/driver):sha(A/driver)})
        create(A/f'round{n}_complete_hidden_launches_v18_20261008.json',{'status':'started_eight_fresh_preflighted_receivers_after_actual_previous_full_qualification','round':n,
            'previous_actual_passed_service':previous,'expected_records':cfg['count'],'QA_version':cfg['qa'],'launches':rows,'input_sha256':pins,
            'native_math_and_grid_unchanged':True,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
        all_rows[str(n)]=rows
        print(json.dumps({'started_round':n,'services':list(rows),'actual_previous_service':previous},ensure_ascii=False),flush=True)
    create(A/'pending139to141_chronological_dispatch_v18_20261008.json',{'status':'passed_all24_preflighted_receivers_dispatched_on_actual_previous_full_qualification',
        'launches':all_rows,'input_sha256':pins,'old_failed_sources_and_logs_preserved':True,'training_workers_stopped':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
if __name__=='__main__':main()
