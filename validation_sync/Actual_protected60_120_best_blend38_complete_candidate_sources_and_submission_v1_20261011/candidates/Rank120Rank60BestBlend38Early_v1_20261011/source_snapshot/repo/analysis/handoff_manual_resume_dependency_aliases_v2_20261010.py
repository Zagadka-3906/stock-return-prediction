"""Keep the active scientific fit; correct only idle dependency followers and future child launches."""
from pathlib import Path
import sys,json,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import inventory,verified_pair,identity,exact
from shutdown_ready_stop_v2_20261007 import StableJournal
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    original=A/'manual_resume_service_alias_runtime_v1_20261010.py'
    fit='actual_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009'
    launch_path=A/'service_owned_workflows_20261006'/f'{fit}_manual_resume_v1_20261010/job_definition.json'
    assert sha(original)==read(launch_path)['input_sha256'][str(original)]
    old_alias=A/'manual_resume_service_aliases_v1_20261010.json';data=read(old_alias)
    mapping={old:(name if old==fit else name.replace('_manual_resume_v1_','_manual_resume_v2_')) for old,name in data['service_aliases'].items()}
    alias_path=A/'manual_resume_service_aliases_v2_20261010.json';create(alias_path,{**data,'service_aliases':mapping})
    evidence=A/'manual_resume_idle_dependency_handoff_v2_20261010';evidence.mkdir()
    journal=StableJournal(evidence);targets=[]
    for row in inventory(full=True):
        if row['name'] in [name for old,name in data['service_aliases'].items() if old!=fit]:
            pair=verified_pair(row['launch']);assert pair is not None
            assert not pair[0].children(), 'Scientific child must not be retired'
            journal.suspend_pair(row);targets.append(row)
    for entry in journal.data['entries']:
        if entry['phase'] in ('pending','suspended'):
            p=exact(entry['identity'])
            if p:p.terminate();p.wait(timeout=5)
            entry['phase']='idle_dependency_follower_superseded';journal.flush()
    wrapper=A/'manual_resume_service_alias_runtime_v2_20261010.py';rows={}
    stop=read(A/'user_requested_immediate_stop_20261009_214340/disk_recovery_manifest.json')
    jobs={j['name']:j for j in stop['jobs_before_stop']['jobs']}
    for old,name in mapping.items():
        if old==fit:continue
        job=jobs[old];driver=Path(job['original_driver'])
        args=['--driver',str(driver),'--aliases',str(alias_path)]
        if old=='BF16FlagAfter15217_actual_full_training_controls_v1_20261009':args+=['--wait-for','BF16Drop05_81_round156_full_registration_v1_20261009']
        pins={**job['definition']['input_sha256'],str(wrapper):sha(wrapper),str(alias_path):sha(alias_path),str(driver):sha(driver)}
        rows[old]=start_service(name,wrapper.name,args,pins)
        print(json.dumps({'follower':old,'worker':rows[old]['owned_worker_pid']},ensure_ascii=False),flush=True)
    create(evidence/'verification.json',{'status':'passed_idle_only_dependency_handoff_active_training_untouched',
        'retired_idle_names':[r['name'] for r in targets],'training_source_pin_preserved':True,
        'launches':rows,'new_quality_scores':0,'active_scientific_fits_terminated':0})

if __name__=='__main__':main()
