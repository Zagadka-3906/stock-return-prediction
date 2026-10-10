"""Validate cross-volume prediction-file placement with the actual official scorer."""
from pathlib import Path
import hashlib
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/official_scoring_disk_placement_preflight_20261005'
SCRATCH = Path('C:/Users/esesl/.codex/contest5_compute_scratch_20261005')


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    assert read(OUT / 'capability.json')['symlink_creation_allowed'] is True
    source = ROOT / 'analysis/optimization_20261003_r60/calibrated_validation.csv'
    baseline = ROOT / 'analysis/optimization_20261003_r60/calibrated_csv_official.json'
    labels = ROOT / 'analysis/optimization_20261003_r60/scoring_validation_only'
    paths = [Path(__file__), ROOT / 'evaluate.py', ROOT / 'src/scoring.py',
             ROOT / 'analysis/locked_read_hash_cache_20261004.py', OUT / 'capability.json',
             source, baseline, labels / '测试集_X.csv', labels / '测试集_Y.csv']
    inputs = {str(path.resolve()): sha(path) for path in paths}
    assert inputs[str(source)] == read(baseline)['csv_sha256']
    create(OUT / 'frozen_before_actual_control.json', {
        'status': 'frozen_before_actual_writer_andofficial_control',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': inputs,
        'rows': 5635800, 'days': 1212, 'codes': 4650,
        'labels_are_training_validation_only': True,
        'new_quality_scores': 0, 'test_labels_read': False,
    })
    folder = OUT / 'actual_scoring'
    physical = SCRATCH / 'placement_preflight/submission.csv'
    folder.mkdir(exist_ok=False)
    physical.parent.mkdir(exist_ok=False)
    physical.touch(exist_ok=False)
    logical = folder / 'submission.csv'
    os.symlink(physical, logical)
    for name in ('测试集_X.csv', '测试集_Y.csv'):
        os.link(labels / name, folder / name)
        assert os.path.samefile(labels / name, folder / name)
    with LockedReadHashCache(inputs):
        import polars as pl
        from evaluate import evaluate
        frame = pl.read_csv(source)
        assert len(frame) == 5635800
        frame.write_csv(physical, float_precision=17)
        direct_sha = sha(physical)
        frame.write_csv(logical, float_precision=17)
        link_sha = sha(logical)
        assert logical.is_symlink() and logical.resolve() == physical.resolve()
        assert direct_sha == link_sha
        assert link_sha == inputs[str(source)], 'Actual17-digit CSV did not round-trip exactly'
        metrics = {key: float(value) for key, value in evaluate(str(logical), str(folder)).items()}
        assert metrics == read(baseline)['metrics'], 'Official eight metrics changed'
        assert sha(logical) == link_sha
    create(OUT / 'verification.json', {
        'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'rows': 5635800, 'days': 1212, 'codes': 4650,
        'actual17_digit_full_writer_bit_identical_through_logical_andphysical_path': True,
        'actual_original_training_validation_CSV_bytes_reproduced': True,
        'actual_official_eight_metrics_bit_identical': True, 'metrics': metrics,
        'csv_sha256': link_sha, 'physical_output': str(physical), 'logical_output': str(logical),
        'training_X_andY_hardlink_identity_unchanged': True,
        'logical_submission_path_remains_a_symlink_after_actual_writer': True,
        'original_scoring_sources_unchanged_andall_input_hashes_end_verified': True,
        'input_sha256': inputs, 'new_quality_scores': 0, 'new_model_fits': 0,
        'test_labels_read': False,
    })
    print(json.dumps({'status': 'passed', 'rows': 5635800, 'official_score': metrics['final_score'],
                      'logical_writer_symlink_preserved': True, 'new_quality_scores': 0}), flush=True)


if __name__ == '__main__':
    main()
