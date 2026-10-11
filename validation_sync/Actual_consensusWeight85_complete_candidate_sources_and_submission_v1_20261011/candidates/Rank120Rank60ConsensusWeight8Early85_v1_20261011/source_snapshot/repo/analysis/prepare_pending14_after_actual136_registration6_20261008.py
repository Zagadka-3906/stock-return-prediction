"""Preserve the13 dependency cascade; prepare new14 receivers and controls, dispatch only after actual136 qualification."""
from pathlib import Path
import sys,runpy,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(path,text):
    assert not path.exists(),path;compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')
def main():
    old=A/'verify_HuberIRLS64_49_current_parent_v4_20261008.py'
    value=old.read_text(encoding='utf8').replace('CrossFamily94_round136_full_registration_v4_20261008','CrossFamily94_round136_full_registration_v6_20261008')
    value=value.replace('current_parent_v4_20261008','current_parent_v6_20261008').replace('current_parent_full_v4_20261008','current_parent_full_v6_20261008').replace('current_parent_full_location_v4_20261008','current_parent_full_location_v6_20261008').replace('current_parent_location_v4_20261008','current_parent_location_v6_20261008')
    current=A/'verify_HuberIRLS64_49_current_parent_v6_20261008.py';save(current,value)
    source=A/'prepare_pending137to141_fresh_closed_dependencies_v13_20261008.py'
    text=source.read_text(encoding='utf8').replace('v13','v14').replace('v5_20261008','v6_20261008')
    target=A/'prepare_pending137to141_fresh_closed_dependencies_v14_20261008.py';save(target,text)
    runpy.run_path(str(target),run_name='__main__')
    old_dispatch=A/'dispatch_pending137to141_verified_fresh13_20261008.py'
    text=old_dispatch.read_text(encoding='utf8').replace('v13','v14').replace(".replace('_v14_','_v11_')", ".replace('_v14_','_v13_')")
    text=text.replace("current=old if old.startswith('HuberIRLS64_49_current_parent_controls_')", "current='HuberIRLS64_49_current_parent_controls_v5_20261008' if old.startswith('HuberIRLS64_49_current_parent_controls_')")
    needle='    import recover_pending137to141_registration_contracts_v14_20261008 as h';assert text.count(needle)==1
    text=text.replace(needle,"""    from run_dependency_queue_v3_20261006 import owned
    gate=A/'service_owned_workflows_20261006/CrossFamily94_round136_full_registration_v6_20261008'
    while not (gate/'native_launch.json').exists() or owned(read(gate/'native_launch.json')):time.sleep(10)
    assert read(gate/'service_execution.json')['status']=='passed'
    assert read(A/'optimization_20261003_r136/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round136_receipt.json')['status']=='pushed_and_remote_head_verified'
"""+needle)
    dispatch=A/'dispatch_pending137to141_verified_fresh14_20261008.py';save(dispatch,text)
    create(A/'pending14_after_actual136_registration6_preparation_20261008.json',{
        'status':'prepared_fresh14_sources_before_full_preflights_actual1366_qualification_required_before_dispatch',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target,old,current,old_dispatch,dispatch]},
        'failed13_sources_and_logs_preserved':True,'old_failed1365_never_marked_passed':True,
        'new_native_fits':0,'new_official_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    helper=A/'recover_pending137to141_registration_contracts_v14_20261008.py'
    pins={str(helper):sha(helper),str(A/'pending137to141_receiver_preparation_v14_20261008.json'):sha(A/'pending137to141_receiver_preparation_v14_20261008.json')}
    row=start('pending137to141_complete_prospective_controls_v14_20261008',helper.name,['controls'],pins)
    create(A/'pending137to141_complete_prospective_hidden_launch_v14_20261008.json',row)
    print(json.dumps({'controls_service':row['name'],'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
