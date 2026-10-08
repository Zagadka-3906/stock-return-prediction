"""Queue the isolated speed benchmark and its main-only preparation evidence."""
from pathlib import Path
import sys
import json
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    preparation = A / 'deferred_full_board_benchmark_preparation_v1_20261008.json'
    p = read(preparation)
    assert p['status'] == 'passed_exact_AST_overwritten_calls_both_branch_bytes_and_prospective_whole_main_compile'
    for path, digest in p['input_sha256'].items():
        assert sha(path) == digest, path
    text = (A / 'publish_actual145_complete_prospective_main_v27_20261008.py').read_text(encoding='utf-8-sig')
    patches = {
        "('CrossFamilyFine145_complete_prospective_controls_v1_20261008','actual138_fine145_historical_controls_main_publication_v25_20261008')":
            "('HuberCrossFamily112_round139_full_registration_v18_20261008','SpectralGram52_controls_main_publication_v18_20261008')",
        'actual145_complete_prospective_main_v27_20261008': 'actual_deferred_full_board_preparation_main_v29_20261008',
        'actual145_complete_prospective_v27_20261008': 'actual_deferred_full_board_preparation_v29_20261008',
        'actual145_complete_prospective_main_v27_receipt_20261008.json': 'actual_deferred_full_board_preparation_main_v29_receipt_20261008.json',
        'HuberCrossFamily112_scores_main_publication_v18_20261008': 'SpectralGram52_scores_main_publication_v18_20261008',
        'closed (publish_HuberCrossFamily112_evidence_v18_20261008.py:': 'closed (publish_SpectralGram52_evidence_v18_20261008.py:',
        'datetime.datetime(2026,10,8,18,15).timestamp()': 'datetime.datetime(2026,10,8,18,28).timestamp()',
        "A/'optimization_20261003_r138/full_registration_execution.json'": "A/'optimization_20261003_r139/full_registration_execution.json'",
        "'actual138_official_cases':40,'actual138_new_inference_claimed':False": "'actual139_official_cases':112,'actual139_new_inference_claimed':True",
        "'fully_qualified_best_round':136,'best_score':0.4511623376562006":
            "'fully_qualified_best_at139_round':139,'best_score_at139':0.45116512879261295,'deferred_runtime_not_adopted':True,'full_benchmark_waits_actual145_completion':True",
        '同步145轮完整125项选模流程、32路径968图控制及草稿记录': '同步139轮实际完成与完整榜重复编码隔离测试准备，保留原模型流程',
    }
    for before, after in patches.items():
        assert before in text, before
        text = text.replace(before, after)
    before = '        sources.extend(p for p in A.iterdir()'
    assert text.count(before) == 1
    text = text.replace(before, "        sources.extend([A/'deferred_full_board_benchmark_preparation_v1_20261008.json', A/'deferred_full_board_serialization_v1_20261008.py', A/'benchmark_deferred_full_board_serialization_v1_20261008.py', A/'verify_deferred_full_board_QA_v1_20261008.py', A/'prepare_deferred_full_board_benchmark_v1_20261008.py'])\n" + before)
    target = A / 'publish_actual_deferred_full_board_preparation_main_v29_20261008.py'
    compile(text, str(target), 'exec')
    with target.open('x', encoding='utf-8', newline='') as stream:
        stream.write(text)
    pins = {**p['input_sha256'], str(Path(__file__)): sha(Path(__file__)),
            str(preparation): sha(preparation), str(target): sha(target)}
    benchmark = start('actual_full_board_deferred_serialization_benchmark_v1_20261008',
                      'benchmark_deferred_full_board_serialization_v1_20261008.py', [], pins)
    publisher = start('actual_full_board_deferred_preparation_main_publication_v29_20261008', target.name, [], pins)
    create(A / 'deferred_full_board_benchmark_and_main_v29_hidden_launches_20261008.json',
           {'status': 'queued_isolated_benchmark_after145_and_main_evidence_after139_and140_controls',
            'benchmark': benchmark, 'publisher': publisher, 'input_sha256': pins,
            'new_quality_scores': 0, 'new_runtime_adoption': False, 'test_labels_read': False})
    print(json.dumps({'status': 'queued', 'benchmark_worker': benchmark['owned_worker_pid'],
                      'publisher_worker': publisher['owned_worker_pid']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
