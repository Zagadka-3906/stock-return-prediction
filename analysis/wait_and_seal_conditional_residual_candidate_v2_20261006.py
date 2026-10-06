"""Seal the unchanged scientific16 candidate with truthful successor ownership."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, owned


def main():
    service = A / 'service_owned_workflows_20261006/conditional_residual_candidate_inference_v2'
    identity = read(service / 'native_launch.json')
    driver = A / 'seal_conditional_residual_candidate_source_package_20261006.py'
    freeze = A / 'conditional_residual_source_freeze_20261006/manifest.json'
    expected = read(freeze)['files'][driver.relative_to(ROOT).as_posix()]['sha256']
    while owned(identity):
        assert sha(driver) == expected
        time.sleep(30)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    assert sha(driver) == expected
    text = driver.read_text(encoding='utf-8')
    before = 'service_owned_workflows_20261006/conditional_residual_candidate_inference'
    assert text.count(before) == 1
    text = text.replace(before, before + '_v2')
    before = '    for path in evidence:\n'
    assert text.count(before) == 1
    text = text.replace(before,
        "    evidence += [Path(__file__), A / 'admit_conditional_residual_candidate_inference_v2_20261006.py', A / 'recover_conditional_residual_admission_v2_20261006.py', A / 'conditional_residual_candidate_admission_v2_20261006/actual_admission.json', A / 'conditional_flag_round101_publication_recovery_v6_20261006/verification.json']\n"
        "    evidence += list((A / 'conditional_residual_admission_recovery_v2_20261006').glob('*.json'))\n"
        "    evidence += list(service.glob('job_definition.json'))\n" + before)
    namespace = {'__file__': str(driver), '__name__': 'actual_residual_sealer_owned_successor_v2'}
    exec(compile(text, str(driver), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
