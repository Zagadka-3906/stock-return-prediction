"""Publish the full real QA and both original failed registry attempts."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
SOURCE = A / 'publish_conditional_flag_round101_full_validation_20261006.py'


def main():
    text = SOURCE.read_text(encoding='utf-8')
    before = '    for path in extra:\n'
    assert text.count(before) == 1
    text = text.replace(before,
        "    extra += [SOURCE, Path(__file__),\n"
        "        A / 'register_conditional_flag_round101_artifacts_20261006.py',\n"
        "        A / 'register_conditional_flag_round101_artifacts_v2_20261006.py',\n"
        "        A / 'run_conditional_flag_round101_full_registration_20261006.py',\n"
        "        A / 'run_conditional_flag_round101_full_registration_v2_20261006.py',\n"
        "        A / 'run_conditional_flag_round101_full_registration_v3_20261006.py',\n"
        "        A / 'publish_conditional_flag_round101_full_validation_v2_20261006.py',\n"
        "        A / 'optimization_20261003_r101/full_registration_failure.json',\n"
        "        A / 'optimization_20261003_r101/frozen_before_actual_full_registration.json',\n"
        "        A / 'optimization_20261003_r101/frozen_before_actual_full_registration_recovery_v3.json']\n"
        "    for service_name in ('conditional_flag_round101_full_registration', 'conditional_flag_round101_full_registration_v2'):\n"
        "        failed_service = A / 'service_owned_workflows_20261006' / service_name\n"
        "        extra += list(failed_service.glob('*.json')) + list(failed_service.glob('*.log'))\n" + before)
    namespace = {'__file__': __file__, '__name__': 'actual_conditional101_full_QA_recovery_publication', 'SOURCE': SOURCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
