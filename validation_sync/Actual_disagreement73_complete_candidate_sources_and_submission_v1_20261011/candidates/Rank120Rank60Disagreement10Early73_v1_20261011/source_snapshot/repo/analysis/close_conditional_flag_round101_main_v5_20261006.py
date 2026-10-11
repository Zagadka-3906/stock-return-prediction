"""Check the actual successful QA schema, then close the existing101 publication."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, owned
SOURCE = A / 'close_conditional_flag_round101_main_v4_20261006.py'


def main():
    previous = A / 'service_owned_workflows_20261006/conditional_flag_round101_main_closure_v4'
    assert not owned(read(previous / 'native_launch.json'))
    assert read(previous / 'service_execution.json')['status'] == 'failed'
    qa = read(A / 'lossless_ranking_display_qa_v12_20261006/round101/verification.json')
    assert qa['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    assert qa['round'] == 101 and qa['original_full_QA_result']['status'] == 'passed'
    assert qa['original_full_QA_result']['new_round_records'] == 37
    text = SOURCE.read_text(encoding='utf-8')
    text = text.replace('passed_original_full_ranking_QA_on_lossless_page',
        'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks')
    text = text.replace('publish_conditional_flag_round101_full_validation_v4_20261006',
        'publish_conditional_flag_round101_full_validation_v5_20261006')
    namespace = {'__file__': __file__, '__name__': 'actual_conditional101_QA_schema_main_closure'}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
