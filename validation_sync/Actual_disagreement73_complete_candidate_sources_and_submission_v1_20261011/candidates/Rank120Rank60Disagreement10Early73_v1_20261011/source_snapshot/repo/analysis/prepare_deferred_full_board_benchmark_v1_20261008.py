"""Prepare an isolated complete-report benchmark; all current model scopes are retained."""
from pathlib import Path
import ast
import json
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from deferred_full_board_serialization_v1_20261008 import SOURCE, bodies, fragment, prospective_whole_main


def main():
    qa_source = A / 'verify_lossless_ranking_display_round138_20261007.py'
    text = qa_source.read_text(encoding='utf-8-sig')
    patches = {
        'def main(number):': 'def main(number, report, report_path):',
        "    out = A / 'lossless_ranking_display_qa_v49_20261007' / f'round{number}'":
            "    assert number == 138\n    out = Path('E:/赛题五_本机临时/full_board_deferred_serialization_benchmark_v1_20261008/full_original_QA')",
        "profiles = ROOT / 'tmp/ranking_display_qa_v49_20261007' / f'round{number}'":
            "profiles = ROOT / 'tmp/full_board_deferred_QA_v1_20261008' / f'round{number}'",
        "paths = [Path(__file__), source, ROOT / 'results/all_model_rankings_20261003.json',":
            'paths = [Path(__file__), source, Path(report_path),',
        "    text = source.read_text(encoding='utf-8')":
            "    text = source.read_text(encoding='utf-8')\n    original_load = \"    report=json.loads(REPORT.read_text(encoding='utf-8'))\"\n    assert text.count(original_load) == 1\n    text = text.replace(original_load, '    report=BENCHMARK_REPORT')",
        "digest=sha, REQUESTED_ROUND=number)":
            'digest=sha, REQUESTED_ROUND=number, BENCHMARK_REPORT=report)',
    }
    for before, after in patches.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    tail = "if __name__ == '__main__':\n    main(int(sys.argv[1]))"
    assert text.count(tail) == 1
    text = text.replace(tail, '')
    target = A / 'verify_deferred_full_board_QA_v1_20261008.py'
    compile(text, str(target), 'exec')
    with target.open('x', encoding='utf-8', newline='') as stream:
        stream.write(text)
    # Compile the entire prospective main as well as the measured fragment.
    prospective_whole_main()
    before, after, *_ = bodies()
    assert len(after) == len(before) - 1
    output = Path('E:/赛题五_本机临时/full_board_deferred_AST_branch_controls_v1_20261008')
    assert not output.exists()
    output.mkdir()
    tree = ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
    page = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'PAGE' for t in n.targets)))

    class FixedDatetime:
        @staticmethod
        def now():
            return datetime(2026, 10, 8, 17, 52, 14)

    class BranchRoot:
        def __init__(self, exists):
            self.present = exists

        def __truediv__(self, name):
            assert name == 'results/validation_provenance_erratum_20261003.json'
            return self

        def exists(self):
            return self.present

    records = []
    for present in (False, True):
        pairs = []
        for deferred in (False, True):
            directory = output / f'erratum{int(present)}_deferred{int(deferred)}'
            directory.mkdir()
            rows = [{'score': .4511623376562006, 'known_restriction': False},
                    {'score': .4474065, 'known_restriction': True}]
            report = {'connected': rows, 'notes': ['中文 </script> 😀, −0.0'], 'finite_values': [0., -0., 1e-12, 1e20]}
            ns = {'ROOT': BranchRoot(present), 'OUT': directory, 'report': report,
                  'connected': rows, 'PAGE': page, 'datetime': FixedDatetime, 'json': json}
            exec(fragment(deferred), ns)
            pair = {name: sha(directory / name) for name in
                    ('all_model_rankings_20261003.json', 'all_model_rankings_20261003.html')}
            pairs.append(pair)
        assert pairs[0] == pairs[1]
        records.append({'erratum_exists': present, 'original_and_deferred_exact_bytes': pairs[0]})
    sources = [Path(__file__), SOURCE, qa_source, target,
               A / 'deferred_full_board_serialization_v1_20261008.py',
               A / 'benchmark_deferred_full_board_serialization_v1_20261008.py']
    for path in sources:
        if path.suffix == '.py':
            compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')
    result = {'status': 'passed_exact_AST_overwritten_calls_both_branch_bytes_and_prospective_whole_main_compile',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'input_sha256': {str(p): sha(p) for p in sources}, 'actual_branch_controls': records,
        'actual_full_board_benchmark_not_yet_executed': True,
        'benchmark_gate': 'round145_full_actual_terminal_pass_then_at_least24GiB_available_RAM_and30GiB_free_E',
        'all_original_QA_checks_retained_with_byte_verified_shared_report_input': True,
        'QA_wrapper_path_and_input_changes': patches, 'original_source_not_modified': True,
        'new_runtime_adoption': False, 'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}
    create(output / 'verification.json', result)
    create(A / 'deferred_full_board_benchmark_preparation_v1_20261008.json', result)
    print(json.dumps({'status': result['status'], 'output': str(output)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
