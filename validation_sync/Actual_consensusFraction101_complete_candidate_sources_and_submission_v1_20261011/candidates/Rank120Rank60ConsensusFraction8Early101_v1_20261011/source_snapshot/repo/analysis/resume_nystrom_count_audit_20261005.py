"""Resume the original waiting audit without rewriting its frozen checkpoint."""
from pathlib import Path
from datetime import datetime
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))


def main():
    import audit_four_configuration_scheme_metadata_20261004 as audit
    from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha
    checkpoint = ROOT / 'analysis/nystrom_ridge_scheme_count_metadata_audit_20261004/frozen_before_actual_proof_audit.json'
    plan_path = ROOT / 'analysis/nystrom_count_resume_20261005/plan.json'
    run_path = ROOT / 'analysis/nystrom_ridge_scheme_count_audit_run_20261005.json'
    while not run_path.exists():
        time.sleep(.1)
    plan = audit.read(plan_path)
    inputs = dict(plan['input_sha256'])
    for path in (plan_path, run_path):
        inputs[str(path.resolve())] = fresh_sha(path)
    original_create = audit.create

    def preserve_checkpoint(path, value):
        if Path(path).resolve() == checkpoint.resolve():
            saved = audit.read(checkpoint)
            assert {k: v for k, v in saved.items() if k != 'at_local'} == {k: v for k, v in value.items() if k != 'at_local'}
            return
        return original_create(path, value)

    with LockedReadHashCache(inputs):
        audit.create = preserve_checkpoint
        try:
            audit.main('nystrom_ridge')
        finally:
            audit.create = original_create
    final = checkpoint.parent / 'verification.json'
    assert audit.read(final)['status'] == 'passed_with_copied_display_label_clarified'
    original_create(plan_path.parent / 'verification.json', {
        'status': 'passed', 'at_local': datetime.now().isoformat(timespec='seconds'),
        'original_wait_checkpoint_preserved': True, 'all_recovery_inputs_end_rehashed': True,
        'completed_original_count_audit': str(final), 'count_audit_sha256': fresh_sha(final),
        'input_sha256': inputs, 'new_model_fits': 0, 'new_quality_scores': 0,
        'test_labels_read': False,
    })


if __name__ == '__main__':
    main()
