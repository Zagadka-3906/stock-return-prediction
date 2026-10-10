"""Preserve the failed registration and the exact actual recovery in the full export."""
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
        "        A / 'register_conditional_flag_round101_artifacts_v2_20261006.py',\n"
        "        A / 'run_conditional_flag_round101_full_registration_v2_20261006.py']\n"
        "    failed_service = A / 'service_owned_workflows_20261006/conditional_flag_round101_full_registration'\n"
        "    extra += list(failed_service.glob('*.json')) + list(failed_service.glob('*.log'))\n" + before)
    namespace = {'__file__': __file__, '__name__': 'actual_conditional101_full_recovery_publication', 'SOURCE': SOURCE}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
