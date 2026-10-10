"""Restore one accidental name collision and adopt the exact repair under a unique name."""
from pathlib import Path
from copy import deepcopy
import sys
import time

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service,pair
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle

OUT=A/'frozen_controller_name_collision_restoration_20261006'
QUEUE=A/'service_owned_dependency_queue_bootstrap_fields_recovery_v2_20261006'
ORIGINAL=A/'run_dependency_queue_v11_20261006.py'
UNIQUE=A/'run_dependency_queue_bootstrap_fields_recovery_v1_20261006.py'
FROZEN=A/'robust_residual50_source_freeze_20261006/repo/analysis/run_dependency_queue_v11_20261006.py'


def main():
    assert not OUT.exists() and not QUEUE.exists() and not UNIQUE.exists()
    OUT.mkdir();QUEUE.mkdir()
    expected='3b26c2d86ab37e02a6136c81e33c60730e252048f2394469ee7a6aaf43ec86cb'
    transient='eb0741235d06e24dacf07727295f0e95af1fdb76811a638595c2be2f163475af'
    assert sha(FROZEN)==expected and sha(ORIGINAL)==transient
    other=A/'simplex_residual47_source_freeze_20261006/repo/analysis/run_dependency_queue_v11_20261006.py'
    assert sha(other)==expected
    UNIQUE.write_bytes(ORIGINAL.read_bytes());assert sha(UNIQUE)==transient
    identity=read(A/'service_owned_workflows_20261006/dependency_queue_v11/native_launch.json')
    assert owned(identity)
    parent=worker=None;retired=False
    try:
        parent,worker,idle=suspended_idle(identity,'    main (run_dependency_queue_v11_shared_state_main_20261006.py:36)')
        create(OUT/'old_controller_actual_idle_before_and_after.json',idle)
        state_path=A/'service_owned_dependency_queue_v4_20261006/state.json'
        snapshot=read(state_path);assert snapshot['pid']==worker.pid
        assert not any(owned(row) for row in snapshot['activated_jobs'].values())
        prior_plan=A/'service_owned_dependency_queue_v11_recovery_20261006/queue_plan_v11.json'
        plan=read(prior_plan)
        create(OUT/'previous_controller_last_snapshot.json',snapshot)
        nn=read(A/'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
        assert owned(nn)
        old_parent,old_worker=pair(identity);assert not old_worker.children()
        old_worker.terminate();old_worker.wait(timeout=15);old_parent.terminate();old_parent.wait(timeout=15)
        retired=True
        ORIGINAL.write_bytes(FROZEN.read_bytes());assert sha(ORIGINAL)==expected
        # Verify the complete pre-inference source manifests, not just this file.
        checks=[];digests={}
        for label in ('robust_residual50','simplex_residual47'):
            manifest_path=A/f'{label}_source_freeze_20261006/manifest.json'
            manifest=read(manifest_path)
            for relative,info in manifest['files'].items():
                path=Path(info['original_source'])
                if str(path) not in digests:digests[str(path)]=sha(path)
                assert digests[str(path)]==info['sha256'],str(path)
            checks.append({'source_manifest':str(manifest_path),'sha256':sha(manifest_path),'all_files_checked':len(manifest['files'])})
        restoration={'status':'passed_exact_original_frozen_source_restoration_and_complete_both_source_manifest_reverification',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_path':str(ORIGINAL),
            'restored_SHA256':expected,'temporary_repair_source_preserved_as':str(UNIQUE),'temporary_SHA256':transient,
            'actual_verified_source_manifests':checks,'actual_unique_files_rehashed':len(digests),
            'scientific_parameters_predictions_models_or_scores_modified':False,
            'historical_handoff_pins_at_the_conflicting_path_are_historical_only':True}
        create(OUT/'source_restoration_verification.json',restoration)
        pins=deepcopy(plan['input_sha256'])
        pins[str(ORIGINAL)]=expected
        sources=[Path(__file__),UNIQUE,FROZEN,other,prior_plan,OUT/'source_restoration_verification.json',
            OUT/'old_controller_actual_idle_before_and_after.json',
            A/'service_owned_dependency_queue_v11_recovery_20261006/activated_jobs/round89/execution.json']
        pins.update({str(p):sha(p) for p in sources})
        for path,digest in pins.items():assert sha(path)==digest,path
        plan.update(status='frozen_actual_uniquely_named_bootstrap_recovery_v2_controller',input_sha256=pins,
            previously_activated_jobs=deepcopy(snapshot['activated_jobs']),prior_queue_plan=str(prior_plan),
            activation_handoff_commit_marker=str(OUT/'handoff_commit.json'),
            source_name_collision_restoration=str(OUT/'source_restoration_verification.json'))
        path=QUEUE/'queue_plan.json';create(path,plan)
        new=start_service('dependency_queue_bootstrap_fields_recovery_v2',UNIQUE.name,[str(path)],{**pins,str(path):sha(path)})
        for _ in range(120):
            assert owned(new)
            state=read(state_path)
            if state['pid']==new['owned_worker_pid']:
                assert state['activated_jobs']==snapshot['activated_jobs'];break
            time.sleep(.5)
        else:raise RuntimeError('New controller did not preserve all original shared state')
        assert owned(nn)
        create(A/'service_owned_workflows_20261006/dependency_queue_v11/administrative_supersession_unique_name_restoration_20261006.json',{
            'status':'administratively_retired_idle_helper_not_claimed_scientifically_complete',
            'old_identity':identity,'actual_new_identity':new,'scientific_workers_stopped_or_restarted':0})
        create(OUT/'handoff_commit.json',{'status':'retired_original_controller_and_preserved_scientific_workers',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_new_identity':new,'scientific_workers_stopped_or_restarted':0})
        create(OUT/'verification.json',{'status':'passed_actual_source_restoration_and_unique_controller_full_queue_handoff',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_new_identity':new,
            'all_original_deferred_routes_preserved':len(plan['deferred_jobs']),'preserved_owned_neural_worker':nn,
            'scientific_workers_stopped_or_restarted':0,'new_quality_scores':0,'test_labels_read':False})
        print('passed_actual_source_restoration_and_unique_controller_full_queue_handoff',flush=True)
    finally:
        if not retired:
            for process in (parent,worker):
                if process is not None and process.is_running():process.resume()


if __name__=='__main__':main()
