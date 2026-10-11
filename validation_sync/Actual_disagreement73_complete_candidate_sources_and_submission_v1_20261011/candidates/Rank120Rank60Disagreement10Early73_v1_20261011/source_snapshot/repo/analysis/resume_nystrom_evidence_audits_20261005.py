"""Resume actual audits after a missing mutable progress report; preserve original proofs."""
from pathlib import Path
import importlib
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/nystrom_evidence_audit_resume_20261005'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    import run_nystrom_restart_evidence_audits_20261005 as driver
    import audit_nystrom_restart_resource_scope_20261005 as annual
    from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha
    plan_path = OUT / 'plan.json'
    run_path = OUT / 'run.json'
    while not run_path.exists():
        time.sleep(.1)
    plan = read(plan_path)
    inputs = dict(plan['input_sha256'])
    for path in [plan_path, run_path]:
        inputs[str(path.resolve())] = fresh_sha(path)
    annual_path = ROOT / 'analysis/nystrom_ridge_resource_scope_audit_20261004.json'
    annual_proof = read(annual_path)
    assert annual_proof['status'] == 'passed' and annual_proof['actual_completed_annual_fits'] == 20
    original_main, original_refresh = annual.main, driver.refresh

    def preserve_actual_annual_audit():
        assert read(annual_path) == annual_proof
        for path, digest in annual_proof['input_sha256'].items():
            assert fresh_sha(Path(path)) == digest, path
        print('Preserved actual passed20-fit resource audit and rehashed its inputs', flush=True)

    def restored_mutable_refresh(**fields):
        target = ROOT / 'analysis/nystrom_ridge_search_execution_20261004.json'
        value = read(target) if target.exists() else {
            'status': 'actual_resource_evidence_recovery_in_progress',
            'missing_mutable_report_restored': True,
            'original_failed_driver_log': plan['failed_driver_stderr'],
            'scientific_inputs_andalgorithms_unchanged': True,
            'new_quality_scores': 0, 'test_labels_read': False,
        }
        value.update(fields, updated_at_local=time.strftime('%Y-%m-%dT%H:%M:%S'))
        temporary = OUT / 'search_execution_update.tmp'
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        os.replace(temporary, target)

    with LockedReadHashCache(inputs):
        annual.main = preserve_actual_annual_audit
        driver.refresh = restored_mutable_refresh
        try:
            driver.main()
        finally:
            annual.main = original_main
            driver.refresh = original_refresh
    future = ROOT / 'analysis/nystrom_ridge_future_resource_scope_audit_20261004.json'
    complete = ROOT / 'analysis/nystrom_ridge_complete_scheme_preflight_20261004/verification.json'
    assert read(future)['status'] == 'passed' and read(complete)['status'] == 'passed'
    create(OUT / 'verification.json', {
        'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'original_passed_annual_resource_audit_preserved': True,
        'original_failed_driver_andlogs_preserved': True,
        'missing_mutable_progress_report_restored_only': True,
        'original_future_resource_andcomplete_scheme_audit_algorithms_executed': True,
        'all_recovery_inputs_end_rehashed': True, 'input_sha256': inputs,
        'annual_scope_sha256': fresh_sha(annual_path), 'future_scope_sha256': fresh_sha(future),
        'complete_scheme_sha256': fresh_sha(complete),
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
    })


if __name__ == '__main__':
    main()
