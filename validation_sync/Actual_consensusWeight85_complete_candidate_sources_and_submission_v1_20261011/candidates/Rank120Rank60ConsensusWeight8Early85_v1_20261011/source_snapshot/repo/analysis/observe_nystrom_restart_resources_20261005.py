"""Start a separate resource window; preserve the interrupted pretraining window."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    import observe_nystrom_ridge_resources_20261004 as observer
    from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha
    audit = ROOT / 'analysis/nystrom_restart_source_audit_20261005.json'
    proof = json.loads(audit.read_text(encoding='utf-8'))
    assert proof['status'] == 'passed_pre_execution_source_binding_correction'
    observer.OUT = ROOT / 'analysis/nystrom_ridge_resource_observations_recovery_20261005'
    observer.RUN = ROOT / 'analysis/nystrom_ridge_training_run_20261005.json'
    observer.OUT.mkdir(exist_ok=True)
    inputs = dict(proof['input_sha256'])
    for path in (audit, observer.RUN):
        inputs[str(path.resolve())] = fresh_sha(path)
    with LockedReadHashCache(inputs):
        binding = observer.OUT / 'recovery_binding.json'
        with binding.open('x', encoding='utf-8') as stream:
            json.dump({'status': 'sampling_recovery_sources_frozen_before_execution',
                       'input_sha256': inputs, 'prior_wait_samples_retained_separately': True,
                       'missing_reboot_interval_not_sampled_or_inferred': True,
                       'actual_new_annual_fits_at_start': 0, 'test_data_read': False},
                      stream, ensure_ascii=False, indent=2)
        observer.main()


if __name__ == '__main__':
    main()
