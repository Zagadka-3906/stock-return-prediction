"""Record rejected deletion honestly and reroute the idle audit publisher only."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,stack
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    cleanup=A/'closed_local_score_scratch_cleanup_v3_20261007'
    plan=read(cleanup/'plan.json')
    assert not (cleanup/'deletions.jsonl').exists()
    assert not (cleanup/'verification.json').exists()
    for row in plan['deletions']:
        p=Path(row['path']);assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    rejection=cleanup/'deletion_not_executed_policy_rejection.json'
    create(rejection,{'status':'deletion_rejected_by_automatic_approval_review_no_files_deleted',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'tool':'exec_command',
        'rejected_action':'PowerShell native single-file Remove-Item for 10 audited historical scoring scratch CSVs',
        'stated_reason':'blocked by policy','more_specific_reason_provided':False,
        'plan_sha256':sha(cleanup/'plan.json'),'actual_all_10_targets_retained_byte_exact':True,
        'deleted_files':0,'reclaimed_bytes':0,'pending_reclaimable_bytes':plan['reclaimable_single_link_bytes'],
        'scientific_workers_stopped_or_restarted':0,'test_labels_read':False})
    old=A/'publish_local_boundary_audit_v3_20261007.py';new=A/'publish_local_boundary_audit_v4_20261007.py'
    source=old.read_text(encoding='utf8').replace('local_boundary_audit_v3_github_20261007','local_boundary_audit_v4_github_20261007').replace('validation_sync/local_boundary_audit_v3_20261007','validation_sync/local_boundary_audit_v4_20261007')
    needle="    assert (cleanup/'verification.json').exists(), 'Require actual completed cleanup evidence before publication'"
    assert source.count(needle)==1
    source=source.replace(needle,"""    rejected=read(cleanup/'deletion_not_executed_policy_rejection.json')
    assert rejected['status']=='deletion_rejected_by_automatic_approval_review_no_files_deleted'
    assert rejected['deleted_files']==0 and rejected['reclaimed_bytes']==0
    assert not (cleanup/'verification.json').exists()
    for target in read(cleanup/'plan.json')['deletions']:
        assert sha(target['path'])==target['sha256'], 'Audited scratch must remain unchanged after rejected deletion'
    sources += [A/'revalidate_closed_score_cleanup_v3_20261007.py',
        A/'record_cleanup_rejection_and_reroute_audit_publication_20261007.py']""")
    source=source.replace("'global_resource_exhaustion_established':False", "'cleanup_deleted_files':0,'cleanup_reclaimed_bytes':0,'cleanup_status':rejected['status'],\n                'global_resource_exhaustion_established':False")
    source=source.replace('及有界清理验证','及未执行清理的拒绝记录')
    compile(source,str(new),'exec');assert not new.exists();new.write_text(source,encoding='utf8',newline='\n')
    folder=A/'service_owned_workflows_20261006/local_boundary_audit_v3_main_after121'
    identity=read(folder/'native_launch.json');assert owned(identity)
    assert not (A/'local_boundary_audit_v3_github_20261007').exists()
    before=stack(identity['owned_worker_pid'])
    possible=[f'({old.name}:{i+1})' for i,line in enumerate(old.read_text(encoding='utf8').splitlines()) if 'time.sleep(' in line and f'({old.name}:{i+1})' in before]
    assert len(possible)==1,(before,possible)
    parent,worker,idle=suspended_idle(identity,possible[0]);retired=False
    out=A/'local_boundary_audit_publisher_v4_actual_handoff_20261007';assert not out.exists();out.mkdir()
    try:
        assert not worker.children();create(out/'actual_old_audit_publisher_exact_idle.json',idle)
        pins={str(p):sha(p) for p in [Path(__file__),old,new,rejection]}
        worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired=True
        create(folder/'administrative_supersession_after_actual_deletion_policy_rejection.json',
            {'status':'administratively_retired_exact_idle_audit_publisher_before_any_publication',
             'identity':identity,'scientific_workers_stopped':0,'actual_publication_claimed':False})
        row=start_service('local_boundary_audit_v4_main_after121',new.name,[],pins)
        create(out/'verification.json',{'status':'passed_actual_idle_audit_publisher_handoff_to_honest_no_deletion_evidence',
            'input_sha256':pins,'new_identity':row,'old_identity':identity,
            'scientific_workers_stopped_or_restarted':0,'new_quality_scores':0,'cleanup_deleted_files':0})
        print({'status':'passed_actual_idle_publication_handoff','new_worker':row['owned_worker_pid'],'deleted_files':0},flush=True)
    finally:
        if not retired:
            for p in (worker,parent):
                if p.is_running():p.resume()

if __name__=='__main__':main()
