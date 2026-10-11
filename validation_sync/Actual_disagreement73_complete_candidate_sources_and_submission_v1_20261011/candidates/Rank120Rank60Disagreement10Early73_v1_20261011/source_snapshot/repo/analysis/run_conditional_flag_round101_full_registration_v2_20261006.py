"""Run the full unchanged ranking checks after a verified terminal registry failure."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, owned
SOURCE = A / 'run_conditional_flag_round101_full_registration_20261006.py'


def main():
    import psutil
    service = A / 'service_owned_workflows_20261006/conditional_flag_round101_full_registration'
    assert not owned(read(service / 'native_launch.json'))
    failure = read(service / 'service_execution.json')
    assert failure['status'] == 'failed' and 'not in the subpath' in failure['failure']
    while psutil.virtual_memory().available < 8 * 2**30:
        time.sleep(30)
    text = SOURCE.read_text(encoding='utf-8')
    text = text.replace('register_conditional_flag_round101_artifacts_20261006', 'register_conditional_flag_round101_artifacts_v2_20261006')
    text = text.replace('publish_conditional_flag_round101_full_validation_20261006', 'publish_conditional_flag_round101_full_validation_v2_20261006')
    namespace = {'__file__': __file__, '__name__': 'actual_conditional101_full_registry_recovery'}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
