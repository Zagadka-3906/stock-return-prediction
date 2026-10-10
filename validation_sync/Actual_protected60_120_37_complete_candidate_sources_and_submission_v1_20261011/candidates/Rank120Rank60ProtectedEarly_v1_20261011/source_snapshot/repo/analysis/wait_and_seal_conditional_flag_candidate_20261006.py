"""Seal only after the exact native inference service has naturally passed."""
from pathlib import Path
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, owned


def main():
    service = A / 'service_owned_workflows_20261006/conditional_flag_rank_candidate_inference'
    identity = read(service / 'native_launch.json')
    driver = A / 'seal_conditional_flag_candidate_source_package_20261006.py'
    freeze = A / 'conditional_flag_rank_source_freeze_20261006/manifest.json'
    expected = read(freeze)['files'][driver.relative_to(ROOT).as_posix()]['sha256']
    while owned(identity):
        assert sha(driver) == expected
        time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    assert sha(driver) == expected
    runpy.run_path(str(driver), run_name='__main__')


if __name__ == '__main__':
    main()
