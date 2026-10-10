"""Only the dispatcher audit output conflicted; preserve failed15 launch, keep all admitted14 model receivers unchanged."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    old=A/'dispatch_pending137to141_verified_fresh14_after_actual15_controls_20261008.py'
    terminal=A/'service_owned_workflows_20261006/pending137to141_dispatch_verified_fresh14_after_actual15_controls_20261008/service_execution.json'
    assert read(terminal)['status']=='failed'
    assert not (A/'pending137to141_receiver_dispatch_v14_20261008.json').exists()
    import recover_pending137to141_registration_contracts_v14_20261008 as h;h.initialize()
    for cfg in h.CONFIG:
        for old_name in cfg['launches']:
            assert not (A/'service_owned_workflows_20261006'/h.MAPPING[old_name]).exists()
    text=old.read_text(encoding='utf8')
    before='pending137to141_failed11_terminal_audit_before_fresh13_20261008.json'
    after='pending137to141_failed13_terminal_audit_before_fresh14_v16_20261008.json'
    assert text.count(before)==1;text=text.replace(before,after)
    target=A/'dispatch_pending137to141_verified_fresh14_after_actual15_controls_v16_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'pending14_dispatch_exclusive_audit_name_recovery_v16_20261008.json',{
        'status':'frozen_unique_audit_output_before_fresh16_dispatch_of_unchanged14_receivers',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,terminal]},
        'actual_failed15_launch_started_no14_receivers':True,'original_full_preflight14_proofs_unchanged':True,
        'new_quality_scores':0,'scientific_workers_stopped':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('pending137to141_dispatch_verified_fresh14_after_actual15_controls_v16_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),target,A/'pending137to141_collector_controls_v14_20261008.json']})
    create(A/'pending137to141_verified_dispatch_v16_hidden_launch_20261008.json',row)
    print(json.dumps({'service':row['name'],'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
