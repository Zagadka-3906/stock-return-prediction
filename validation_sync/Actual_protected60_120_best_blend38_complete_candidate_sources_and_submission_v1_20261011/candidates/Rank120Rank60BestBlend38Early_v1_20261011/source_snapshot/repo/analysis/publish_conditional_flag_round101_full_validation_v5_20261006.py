"""Use the corrected101 snapshot and retain the additional pre-publication failure."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
SOURCE = A / 'publish_conditional_flag_round101_full_validation_v4_20261006.py'


def main():
    text = SOURCE.read_text(encoding='utf-8')
    # V4 already patches snapshot100 to101. Extend only its evidence list.
    before = '        "    for path in extra:\\n"'
    # Its list injection is assembled as strings; modify that assembly before
    # executing the unchanged corrected snapshot and complete collector.
    marker = '        "    for service_name in ('
    pos = text.index(marker)
    text = text[:pos] + (
        '        "    extra += [A / \'publish_conditional_flag_round101_full_validation_v4_20261006.py\',\\n"\n'
        '        "        A / \'close_conditional_flag_round101_main_v4_20261006.py\',\\n"\n'
        '        "        A / \'close_conditional_flag_round101_main_v5_20261006.py\']\\n"\n'
        '        "    old_closure = A / \'service_owned_workflows_20261006/conditional_flag_round101_main_closure_v4\'\\n"\n'
        '        "    extra += list(old_closure.glob(\'*.json\')) + list(old_closure.glob(\'*.log\'))\\n"\n'
    ) + text[pos:]
    namespace = {'__file__': __file__, '__name__': 'actual_conditional101_final_main_closure'}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
