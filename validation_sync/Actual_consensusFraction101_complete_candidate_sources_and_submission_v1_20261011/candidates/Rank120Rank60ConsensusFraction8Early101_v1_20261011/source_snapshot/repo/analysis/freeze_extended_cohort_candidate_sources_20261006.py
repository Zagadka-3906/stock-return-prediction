"""Freeze every local inference source before fitting and future replay."""
from pathlib import Path
import importlib.metadata
import platform
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, create, sha, owned
OUT = A / 'extended_cohort_rank_calibration_source_freeze_20261006'


def main():
    assert not OUT.exists()
    assert not (A / 'extended_cohort_rank_calibration_release_20261006').exists()
    assert not (ROOT / 'candidates/extended_cohort_rank_calibration_20261006').exists()
    service = A / 'service_owned_workflows_20261006/extended_cohort_controls_and_scores'
    assert not owned(read(service / 'native_launch.json'))
    assert read(service / 'service_execution.json')['status'] == 'passed'
    pilot = read(A / 'extended_cohort_rank_calibration_official_pilot_20261006/verification.json')
    assert len(pilot['records']) == 66
    paths = sorted(set(ROOT.glob('*.py')) | set(A.glob('*.py')) |
        set((A / 'connected_validation_20261002').glob('*.py')) |
        set((ROOT / 'src').rglob('*.py')) | set((ROOT / 'experiments').rglob('*.py')))
    OUT.mkdir()
    pins = {str(p): sha(p) for p in paths}
    create(OUT / 'frozen_before_source_copy.json', {'input_sha256': pins,
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'future_inference_not_started': True,
        'selected_official_pilot_case': pilot['best']['configuration'],
        'scientific_workers_held': 0, 'test_labels_read': False})
    files = {}
    for path, digest in pins.items():
        source = Path(path)
        target = OUT / 'repo' / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(target) == sha(source) == digest
        files[source.relative_to(ROOT).as_posix()] = {'sha256': digest,
            'bytes': target.stat().st_size, 'original_source': path}
    create(OUT / 'manifest.json', {'status': 'passed_pre_inference_local_Python_source_snapshot',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'files': files,
        'python': platform.python_version(), 'library_versions': {name: importlib.metadata.version(name)
            for name in ('numpy', 'pandas', 'polars', 'scipy', 'scikit-learn', 'joblib', 'lightgbm', 'xgboost', 'torch')},
        'actual_native_future_inference_pending': True, 'test_labels_read': False})


if __name__ == '__main__':
    main()
