"""Place new private worker submissions on an available volume, with original paths."""
from pathlib import Path
import json
import os
import psutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha

OUT = ROOT / 'analysis/official_scoring_disk_placement_preflight_20261005'
SCRATCH = Path('C:/Users/esesl/.codex/contest5_compute_scratch_20261005')


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    proof = OUT / 'verification.json'
    value = read(proof)
    assert value['status'] == 'passed'
    assert value['actual_original_training_validation_CSV_bytes_reproduced']
    assert value['actual_official_eight_metrics_bit_identical']
    assert value['logical_submission_path_remains_a_symlink_after_actual_writer']
    assert psutil.disk_usage(str(SCRATCH)).free > 8 * 2**30
    sources = [Path(__file__), ROOT / 'analysis/verify_official_scoring_disk_placement_20261005.py',
               ROOT / 'analysis/parallel_candidate_scoring_four_20261004.py', proof,
               OUT / 'frozen_before_actual_control.json', ROOT / 'evaluate.py']
    inputs = {str(path.resolve()): fresh_sha(path) for path in sources}
    entries = []
    for number in (61, 62, 63):
        for slot in range(4):
            logical = ROOT / f'analysis/optimization_20261003_r{number}/parallel_official_workers/worker_{slot}/scoring_validation_only/submission.csv'
            physical = SCRATCH / f'round{number}/worker_{slot}/submission.csv'
            assert not logical.exists() and not logical.is_symlink()
            assert not physical.exists()
            assert logical.parent.is_relative_to(ROOT / 'analysis')
            assert physical.parent.is_relative_to(SCRATCH)
            entries.append({'round': number, 'worker_slot': slot,
                            'logical_path': str(logical), 'physical_path': str(physical)})
    decision = {'status': 'frozen_before_new_worker_file_placement',
                'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'available_D_bytes_before': psutil.disk_usage('D:/').free,
                'available_C_bytes_before': psutil.disk_usage('C:/').free,
                'observed_previous_worker_submission_bytes': 221989870,
                'expected_three_round_worker_bytes_at_observed_baseline_size': 12 * 221989870,
                'declared_new_output_aliases': entries, 'input_sha256': inputs,
                'new_quality_scores': 0, 'test_labels_read': False}
    create(OUT / 'placement_frozen_before_creation.json', decision)
    with LockedReadHashCache(inputs):
        for entry in entries:
            logical, physical = Path(entry['logical_path']), Path(entry['physical_path'])
            logical.parent.mkdir(parents=True, exist_ok=True)
            physical.parent.mkdir(parents=True, exist_ok=True)
            assert logical.parent.resolve().is_relative_to(ROOT / 'analysis')
            assert physical.parent.resolve().is_relative_to(SCRATCH)
            physical.touch(exist_ok=False)
            os.symlink(physical, logical)
            assert logical.is_symlink() and logical.resolve() == physical.resolve()
            assert os.path.samefile(logical, physical)
        create(OUT / 'placement_verification.json', {
            'status': 'passed_new_output_alias_creation_only',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'entries': entries, 'actual_aliases': len(entries),
            'all12_declared_logical_andphysical_file_identities_match': True,
            'existing_scientific_files_deleted_moved_or_rewritten': False,
            'official_scoring_input_hardlink_andworker_algorithms_unchanged': True,
            'actual_future_worker_execution_still_required': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'frozen_placement_sha256': fresh_sha(OUT / 'placement_frozen_before_creation.json'),
            'input_sha256': inputs,
        })
    print(json.dumps({'status': 'passed_new_output_alias_creation_only', 'actual_aliases': len(entries),
                      'rounds': [61, 62, 63], 'workers_per_round_unchanged': 4}), flush=True)


if __name__ == '__main__':
    main()
