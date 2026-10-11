"""Launch only frozen13 receivers after five full preflights; old failed terminal tasks remain intact."""
from pathlib import Path
import json,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    from run_dependency_queue_v3_20261006 import owned
    gate=A/'service_owned_workflows_20261006/CrossFamily94_round136_full_registration_v6_20261008'
    while not (gate/'native_launch.json').exists() or owned(read(gate/'native_launch.json')):time.sleep(10)
    assert read(gate/'service_execution.json')['status']=='passed'
    assert read(A/'optimization_20261003_r136/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round136_receipt.json')['status']=='pushed_and_remote_head_verified'
    import recover_pending137to141_registration_contracts_v14_20261008 as h
    h.initialize()
    base=A/'pending137to141_receiver_preparation_v14_20261008.json'
    controls=A/'pending137to141_collector_controls_v14_20261008.json'
    service=A/'service_owned_workflows_20261006/pending137to141_complete_prospective_controls_v14_20261008'
    assert read(service/'service_execution.json')['status']=='passed'
    proof=read(controls);assert proof['status']=='passed_all15_collectors_and_five_complete_prospective_preflights'
    assert len(proof['records'])==15
    for path,digest in read(base)['input_sha256'].items():assert sha(path)==digest,path
    audit={};jobs=[]
    for cfg in h.CONFIG:
        assert not any((A/cfg['physical_comparison']).iterdir()),cfg['round']
        for old,row in cfg['launches'].items():
            current='HuberIRLS64_49_current_parent_controls_v5_20261008' if old.startswith('HuberIRLS64_49_current_parent_controls_') else h.version12(old).replace('_v14_','_v13_')
            folder=A/'service_owned_workflows_20261006'/current
            terminal=read(folder/'service_execution.json');launch=read(folder/'native_launch.json')
            assert terminal['status']=='failed' and not owned(launch),current
            audit[current]={'terminal':terminal,'terminal_sha256':sha(folder/'service_execution.json'),'original_source':launch['original_driver'],'original_source_sha256':sha(launch['original_driver'])}
            name=h.MAPPING[old];driver=h.MAPPING[Path(row['original_driver']).stem]+'.py'
            assert (A/driver).is_file() and not (A/'service_owned_workflows_20261006'/name).exists(),name
            jobs.append((cfg['round'],name,driver,row['original_arguments']))
    assert len(jobs)==41 and len(audit)==41
    create(A/'pending137to141_failed11_terminal_audit_before_fresh13_20261008.json',{
        'status':'passed_all41_previous_workers_terminal_failed_and_not_running_before_any_fresh_launch',
        'records':audit,'old_sources_and_logs_untouched':True,'processes_stopped':0,'new_quality_scores':0})
    pins={str(p):sha(p) for p in [Path(__file__),base,controls,A/'recover_pending137to141_registration_contracts_v14_20261008.py',A/'pending137to141_closed_dependency_recovery_v14_20261008.json']}
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={};identity_races=[]
    for number,name,driver,args in jobs:
        try:row=start(name,driver,args,{**pins,str(A/driver):sha(A/driver)})
        except AssertionError as error:
            folder=A/'service_owned_workflows_20261006'/name
            for attempt in range(40):
                if (folder/'native_launch.json').exists():
                    row=read(folder/'native_launch.json')
                    if owned(row):break
                time.sleep(.25)
            else:raise
            assert row['original_driver']==str(A/driver) and row['original_arguments']==args
            identity_races.append({'service':name,'caught_identity_race':str(error),'subsequently_actual_identity_owned':True})
        launches.setdefault(str(number),{})[name]=row
        print(json.dumps({'round':number,'started':name,'worker':row['owned_worker_pid']}),flush=True)
    for cfg in h.CONFIG:
        create(A/f"round{cfg['round']}_complete_hidden_launches_v14_20261008.json",{
            'status':'started_fresh13_after_actual_full24_prospective_routes_and_terminal_failure_audit',
            'round':cfg['round'],'expected_records':cfg['count'],'QA_version':cfg['qa'],'launches':launches[str(cfg['round'])],
            'input_sha256':pins,'new_quality_scores_by_dispatch':0,'native_models_and_grid_unchanged':True})
    create(A/'pending137to141_receiver_dispatch_v14_20261008.json',{
        'status':'passed_all41_fresh_chronological_receivers_dispatched_after120_prospective_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'launches':launches,
        'identity_races':identity_races,'new_fits':0,'new_quality_scores_by_dispatch':0,
        'scientific_workers_stopped':0,'old_failed11_sources_and_logs_preserved':True,'test_labels_read':False})
if __name__=='__main__':main()
