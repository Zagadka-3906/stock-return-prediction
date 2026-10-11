"""Defer new full native fits until the existing required workflow really closes."""
from pathlib import Path
import hashlib
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = A / 'quantile_tree_native_full_workflow_20261006'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def state(stage, **extra):
    value = {'stage': stage, 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'existing_original29_job_queue_unchanged': True,
        'new_quality_scores': 0, 'test_labels_read': False,
        'physical_resource_boundary_established': False, **extra}
    path = OUT / 'state.json'
    temporary = path.with_suffix('.next')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def main():
    run = read(OUT / 'run.json')
    for filename, digest in run['input_sha256'].items():
        assert sha(filename) == digest, filename
    service = A / 'service_owned_workflows_20261006/quantile_tree_preflight'
    while True:
        proof, terminal = A / 'quantile_tree_preflight_20261006/verification.json', service / 'service_execution.json'
        if proof.exists() and terminal.exists():
            assert read(proof)['status'] == 'passed_actual_quantile_native_maturity_reload_and_cold80_controls'
            assert read(terminal)['status'] == 'passed'
            break
        state('waiting_actual_closed_native_preflight')
        time.sleep(10)
    from run_dependency_queue_v3_20261006 import owned
    queue_plan = A / 'service_owned_dependency_queue_v4_20261006/queue_plan.json'
    while True:
        wide = read(A / 'service_owned_workflows_20261006/neural16384_annual/native_launch.json')
        queue_state = read(queue_plan.parent / 'state.json')
        active = any(owned(row) for row in queue_state['activated_jobs'].values())
        last = A / 'optimization_20261003_r90/provenance_scope_execution.json'
        future = A / 'neural16384_full_future_qa_20261005/verification.json'
        finished = (last.exists() and read(last).get('status') == 'passed'
                    and future.exists() and read(future).get('status') == 'passed'
                    and not owned(wide) and not active and not queue_state['deferred_jobs_remaining'])
        reserve = psutil.virtual_memory().available
        if finished and reserve >= 14 * 2**30:
            import qualified_round_recovery_evidence_v3_20261006 as qualification
            try:
                if all(qualification.complete_round_evidence(number) is not None
                       for number in range(67, 91)):
                    break
            finally:
                qualification.close()
        state('deferred_until_existing_required_native_and_quality_jobs_are_closed_and14GiB_available',
            original_required_rounds=list(range(67, 91)),
            wide_worker_owned_live=owned(wide), original_queue_active_children=active,
            original_jobs_remaining=len(queue_state['deferred_jobs_remaining']),
            available_host_bytes=reserve, reserved_available_host_bytes=14 * 2**30,
            actual_new_full_annual_fits=0, actual_new_full_final_fits=0)
        time.sleep(30)
    import train_quantile_tree_bank_20261006 as bank
    from frozen_provenance_execution_scope_20261004 import FrozenProvenanceExecutionScope
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    scope = FrozenProvenanceExecutionScope(bank,
        [Path(__file__), OUT / 'run.json', A / 'frozen_provenance_execution_scope_20261004.py',
         A / 'locked_read_hash_cache_20261004.py'],
        {'script': str(Path(__file__)), 'actual20_full300_round_annual_fits_required': True,
         'all_existing_required_jobs_closed_before_new_heavy_training': True}, A).install()
    recorder, failure = ResourceSampler(bank.OUT), None
    try:
        bank.OUT.mkdir(parents=True, exist_ok=True)
        recorder.start()
        bank.RESOURCE = recorder
        state('actual20_complete_mature300_round_annual_fits')
        bank.all_oof()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        resources = recorder.finish()
        bank.dump(bank.OUT / 'resource_summary.json', resources, immutable=True)
        bank.RESOURCE = None
        report = scope.close(failed=failure is not None)
        bank.dump(bank.OUT / 'training_execution_scope.json', {
            'status': 'passed' if failure is None else 'failed', 'failure': failure,
            **report, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    state('actual_four_complete_final_fits_and_full_future_native_controls', actual_new_full_annual_fits=20)
    from verify_quantile_tree_full_future_20261006 import main as future_checks
    future_checks()
    state('native_complete_full_scheme_official_quality_still_pending',
        actual_new_full_annual_fits=20, actual_new_full_final_fits=4,
        full_five_year_official_quality_and_frozen_complete_scheme_causality_and_candidate_still_pending=True)


if __name__ == '__main__':
    main()
