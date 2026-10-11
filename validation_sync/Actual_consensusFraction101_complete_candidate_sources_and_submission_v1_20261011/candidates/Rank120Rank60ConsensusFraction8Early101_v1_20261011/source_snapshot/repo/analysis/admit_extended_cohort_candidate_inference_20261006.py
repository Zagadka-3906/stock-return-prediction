"""Wait for memory, then run the already frozen extended winner exactly once."""
from pathlib import Path
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, create, sha


def main():
    import psutil
    path = A / 'freeze_and_infer_extended_cohort_candidate_20261006.py'
    assert not (A / 'extended_cohort_rank_calibration_release_20261006').exists()
    freeze = A / 'extended_cohort_rank_calibration_source_freeze_20261006/manifest.json'
    expected = read(freeze)['files'][path.relative_to(ROOT).as_posix()]['sha256']
    while psutil.virtual_memory().available < 8.5 * 2**30:
        assert sha(path) == expected
        time.sleep(30)
    create(A / 'extended_cohort_candidate_actual_admission_20261006.json', {
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'available_RAM_GiB': psutil.virtual_memory().available/2**30,
        'driver_sha256': expected, 'source_freeze_manifest_sha256': sha(freeze),
        'original_scientific_processes_preserved': True, 'test_labels_read': False})
    runpy.run_path(str(path), run_name='__main__')


if __name__ == '__main__':
    main()
