"""Test real ready-GOSS ownership and reject a reused-PID birth mismatch."""
from pathlib import Path
from copy import deepcopy
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
import monitor_actual_optimization_progress_v31_20261006 as observer


def main():
    out = A / 'ready_goss_observer31_ownership_preflight_20261006'
    assert not out.exists(); out.mkdir()
    sources = [Path(__file__), Path(observer.__file__), A / 'monitor_actual_optimization_progress_v30_20261006.py',
               A / 'refresh_gradient_sampling_cost_evidence_v2_20261006.py',
               A / 'optimization_20261003_r95/protocol.json']
    bindings = {str(p.resolve()): sha(p) for p in sources}
    create(out / 'frozen_before_controls.json', {'input_sha256': bindings,
        'negative_control_uses_private_copy_not_live_registry': True, 'scientific_quality_not_evaluated': True})
    queue, _ = observer.current_dependency()
    identity = read(queue)
    qstate = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
    row = qstate['activated_jobs']['round95']; assert owned(row)
    public = read(A / 'ongoing_optimization_state.json')
    assert 95 in public['pending_required_rounds']
    value, state = deepcopy(public), {}
    value.update(actual_active_quality_rounds=[], active_root_command_owned=False)
    observer.augment_ready_goss_ownership(value, state, identity, qstate)
    assert value['actual_active_quality_rounds'] == state['actual_active_quality_rounds'] == [95]
    assert value['active_root_command_owned'] is state['active_root_command_owned'] is True
    assert value['current_recovered_worker_ownership']['round95']['owned_live_now'] is True
    assert value['pending_required_rounds'] == public['pending_required_rounds']
    corrupt = deepcopy(qstate)
    corrupt['activated_jobs']['round95']['owned_worker_creation_time'] += 1.0
    value, rejected = deepcopy(public), {}
    value.update(actual_active_quality_rounds=[], active_root_command_owned=False)
    observer.augment_ready_goss_ownership(value, rejected, identity, corrupt)
    assert value['actual_active_quality_rounds'] == [] and rejected['active_root_command_owned'] is False
    assert value['current_recovered_worker_ownership']['round95']['owned_live_now'] is False
    for path, digest in bindings.items(): assert sha(path) == digest, path
    assert owned(row)
    proof = {'status': 'passed_actual_live_R95_ownership_and_private_birth_mismatch_rejection',
        'input_sha256': bindings, 'actual_live_identity': row,
        'current_pending_scope_preserved': True, 'old_observer_source_and_R95_frozen_protocol_unchanged': True,
        'private_negative_control_not_written_to_live_state': True, 'public_snapshots_written_by_control': 0,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    create(out / 'verification.json', proof)
    print(proof['status'], flush=True)


if __name__ == '__main__': main()
