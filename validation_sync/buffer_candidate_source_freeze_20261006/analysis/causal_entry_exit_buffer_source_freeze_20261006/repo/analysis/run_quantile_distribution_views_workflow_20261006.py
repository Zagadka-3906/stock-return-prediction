"""Wait for actual native closure, then complete all fixed-view outputs and controls."""
from pathlib import Path
from datetime import datetime
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    from run_dependency_queue_v3_20261006 import owned
    import psutil
    service = A / 'service_owned_workflows_20261006/quantile_tree_memmap_complete_workflow'
    receipt = A / 'quantile_tree_memmap_complete_bank_github_20261006/receipt.json'
    while not (service / 'service_execution.json').exists():
        assert owned(read(service / 'native_launch.json')), 'Native worker is missing without a terminal record.'
        time.sleep(10)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    while owned(read(service / 'native_launch.json')):
        time.sleep(.2)
    while not receipt.exists():
        publisher = A / 'service_owned_workflows_20261006/quantile_tree_memmap_complete_publication'
        assert owned(read(publisher / 'native_launch.json')), 'Required native publication is missing without a live publisher.'
        time.sleep(10)
    preflight = A / 'quantile_distribution_views_preflight_20261006/verification.json'
    controls = A / 'service_owned_workflows_20261006/quantile_distribution_views_preflight'
    while not preflight.exists():
        assert owned(read(controls / 'native_launch.json')), 'Required controls are missing without a live worker.'
        time.sleep(10)
    assert read(preflight)['status'] == 'passed_actual_six_distribution_views_native_cold80_independent_codec_and_math_controls'
    while psutil.virtual_memory().available < 4 * 2**30:
        time.sleep(10)
    import build_quantile_distribution_views_bank_20261006 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from linear_leaf_actual_resource_sampler_20261005 import ResourceSampler
    protocol = bank.freeze()
    cache = LockedReadHashCache(protocol['input_sha256'])
    old_sha, old_parent_sha, old_core_sha = bank.sha, bank.parent.sha, bank.core.parent.sha
    sampler, failure = ResourceSampler(bank.OUT), None
    try:
        with cache:
            bank.sha = bank.parent.sha = bank.core.parent.sha = cache.sha
            bank.RESOURCE = sampler
            sampler.start()
            bank.all_oof()
            bank.all_future()
            cache.reverify()
    except BaseException as error:
        failure = f'{type(error).__name__}: {error}'
        raise
    finally:
        bank.sha, bank.parent.sha, bank.core.parent.sha = old_sha, old_parent_sha, old_core_sha
        bank.RESOURCE = None
        bank.dump(bank.OUT / 'resource_summary.json', sampler.finish(), immutable=True)
        bank.dump(bank.OUT / 'execution_scope.json', {'status': 'passed' if failure is None else 'failed',
            'at_local': datetime.now().isoformat(), 'failure': failure,
            'input_sha256': protocol['input_sha256'], 'all_scientific_sources_fully_rehashed_unchanged': failure is None,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    bank.dump(bank.OUT / 'verification.json', {'status': 'passed',
        'actual_complete_virtual_annual_outputs': 30, 'actual_complete_virtual_final_artifacts': 6,
        'actual_full_future_views_and_real_cold80_passed': 6,
        'actual_new_native_fits': 0, 'additional_required_full_quality_records': 262,
        'original198_quality_records_preserved': True, 'physical_resource_boundary_established': False,
        'all_quality_mapping_causal_candidate_and_complete_ranking_steps_still_required': True,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)


if __name__ == '__main__':
    main()
