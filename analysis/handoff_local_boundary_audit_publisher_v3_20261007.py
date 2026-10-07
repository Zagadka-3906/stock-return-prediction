"""Reroute only an idle audit publisher to genuine cached cleanup proof; retain predecessors."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,stack
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    out=A/'local_boundary_audit_publisher_v3_actual_handoff_20261007';assert not out.exists();out.mkdir()
    old=A/'publish_local_boundary_audit_v2_20261007.py';new=A/'publish_local_boundary_audit_v3_20261007.py'
    text=old.read_text(encoding='utf8').replace('local_boundary_audit_v2_github_20261007','local_boundary_audit_v3_github_20261007').replace('validation_sync/local_boundary_audit_v2_20261007','validation_sync/local_boundary_audit_v3_20261007')
    text=text.replace("cleanup=A/'closed_local_score_scratch_cleanup_v2_20261007'","cleanup=A/'closed_local_score_scratch_cleanup_v3_20261007'")
    needle="    sources=list(dict.fromkeys(sources))";assert text.count(needle)==1
    text=text.replace(needle,"""    sources += [A/'bounded_frozen_SHA_bindings_v2_20261007.py',A/'prepare_cached_bounded_score_cleanup_v3_20261007.py',
        A/'plan_closed_local_score_scratch_cleanup_v3_20261007.py',A/'cached_bounded_score_cleanup_v3_source_preparation_20261007.json',
        A/'cached_bounded_SHA_bindings_actual_preflight_20261007/verification.json',
        A/'closed_local_score_scratch_cleanup_v2_20261007/read_only_path_scan_supersession.json',
        A/'ensure_round120_actual_native_proof_metadata_alias_20261007.py',A/'round120_actual_native_proof_metadata_alias_20261007/verification.json',
        A/'round120_actual_native_proof_metadata_alias_20261007/actual_original_sealer_exact_idle_guard.json',
        A/'round120_actual_native_proof_metadata_alias_20261007/original_sealer_resumed_after_actual_proof_guard.json']
"""+needle)
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    folder=A/'service_owned_workflows_20261006/local_boundary_audit_v2_main_after121';identity=read(folder/'native_launch.json');assert owned(identity)
    assert not (A/'local_boundary_audit_v2_github_20261007').exists()
    before=stack(identity['owned_worker_pid']);lines=old.read_text(encoding='utf8').splitlines()
    possible=[f'({old.name}:{i+1})' for i,line in enumerate(lines) if 'time.sleep(' in line and f'({old.name}:{i+1})' in before]
    assert len(possible)==1,(before,possible)
    parent,worker,idle=suspended_idle(identity,possible[0]);retired=False
    try:
        create(out/'actual_old_audit_publisher_exact_idle.json',idle);assert not worker.children()
        pins={str(p):sha(p) for p in [Path(__file__),old,new,A/'cached_bounded_score_cleanup_v3_source_preparation_20261007.json']}
        worker.terminate();worker.wait(timeout=15);parent.terminate();parent.wait(timeout=15);retired=True
        create(folder/'administrative_supersession_for_actual_cached_cleanup_v3_20261007.json',{'status':'administratively_retired_exact_idle_audit_publisher_before_any_publication',
            'identity':identity,'actual_publication_or_scientific_results_claimed':False,'scientific_workers_stopped':0})
        row=start_service('local_boundary_audit_v3_main_after121',new.name,[],pins)
        create(out/'verification.json',{'status':'passed_actual_idle_audit_publisher_reroute_only_to_genuine_cleanup3_and_metadata_guard_evidence',
            'input_sha256':pins,'new_identity':row,'old_identity':identity,'scientific_workers_stopped_or_restarted':0,'new_quality_scores':0})
        print({'status':'passed_actual_idle_publication_handoff','new_worker':row['owned_worker_pid']},flush=True)
    finally:
        if not retired:
            for p in (worker,parent):
                if p.is_running():p.resume()
if __name__=='__main__':main()
