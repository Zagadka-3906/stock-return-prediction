"""Schedule complete146 historical metadata publication and expose the actual queues."""
from pathlib import Path
import sys
import json
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    original = A / 'publish_actual_deferred_full_board_preparation_main_v29_20261008.py'
    text = original.read_text(encoding='utf-8-sig')
    before = "('HuberCrossFamily112_round139_full_registration_v18_20261008','SpectralGram52_controls_main_publication_v18_20261008')"
    assert text.count(before) == 1
    text = text.replace(before, "('actual_full_board_deferred_preparation_main_publication_v29_20261008','HuberCrossFamilyFine30_actual_native_historical_controls_v1_20261008','HuberCrossFamilyFine121_actual_full_historical_controls_v1_20261008','CrossFamilyFine125_controls_main_publication_v1_20261008')")
    text = text.replace('actual_deferred_full_board_preparation_main_v29_20261008', 'actual_fine146_historical_controls_main_v30_20261008')
    text = text.replace('actual_deferred_full_board_preparation_v29_20261008', 'actual_fine146_historical_controls_v30_20261008')
    text = text.replace('actual_deferred_full_board_preparation_main_v29_receipt_20261008.json', 'actual_fine146_historical_controls_main_v30_receipt_20261008.json')
    text = text.replace('SpectralGram52_scores_main_publication_v18_20261008', 'CrossFamilyFine125_scores_main_publication_v1_20261008')
    text = text.replace('closed (publish_SpectralGram52_evidence_v18_20261008.py:', 'closed (publish_CrossFamilyFine125_evidence_v1_20261008.py:')
    text = text.replace("for pointer in ('actual_CrossFamilyFine30_native_hooks_location_v1_20261008.json','actual_CrossFamilyFine121_parent134_location_v1_20261008.json'):",
                        "for pointer in ('actual_CrossFamilyFine30_native_hooks_location_v1_20261008.json','actual_CrossFamilyFine121_parent134_location_v1_20261008.json','actual_HuberCrossFamilyFine30_native_hooks_location_v1_20261008.json','actual_HuberCrossFamilyFine121_parent136_location_v1_20261008.json','actual_HuberCrossFamilyFine_bank15_location_v1_20261008.json'):")
    before = "        prospective=read(A/'CrossFamilyFine125_prospective_routes_v1_20261008.json');"
    assert text.count(before) == 1
    text = text.replace(before, "        fine146=read(Path(read(A/'actual_HuberCrossFamilyFine121_parent136_location_v1_20261008.json')['output'])/'verification.json');assert fine146['actual_nonzero_full_cases']==120 and fine146['actual_nonzero_cold_cases']==360\n        native146=read(Path(read(A/'actual_HuberCrossFamilyFine30_native_hooks_location_v1_20261008.json')['output'])/'verification.json');assert native146['actual_hooks']==30 and native146['actual_cold_hooks']==30\n" + before)
    before = "'fully_qualified_best_at139_round':139,"
    assert text.count(before) == 1
    text = text.replace(before, "'actual146_full_historical_controls':121,'actual146_cold_controls':363,'actual146_native_hooks':30,'actual146_native_cold_hooks':30,'actual146_existing_native_evidence_records':15,'new146_official_scores':0,'new146_candidate_inference':0,'full146_receivers_still_required':True," + before)
    text = text.replace('同步139轮实际完成与完整榜重复编码隔离测试准备，保留原模型流程',
                        '同步146轮有符号Huber细权重完整历史控制与实际失败记录')
    target = A / 'publish_actual_fine146_historical_controls_main_v30_20261008.py'
    compile(text, str(target), 'exec')
    with target.open('x', encoding='utf-8', newline='') as stream:
        stream.write(text)
    observer_source = A / 'monitor_actual_chronological_optimization_progress_v28_20261008.py'
    observer = observer_source.read_text(encoding='utf-8-sig')
    before = "    write(A/'optimization_live_progress_v28_20261008.json'"
    assert observer.count(before) == 1
    additions = """    fine146=Path('E:/赛题五_本机临时/HuberCrossFamilyFine121_parent136_historical_v1_20261008')
    state['fine146_frontier']={'expected_quality_cases':125,'actual_native30':status('HuberCrossFamilyFine30_actual_native_historical_controls_v1_20261008'),'actual_full121':status('HuberCrossFamilyFine121_actual_full_historical_controls_v1_20261008'),'actual_full_control_records':len(list(fine146.glob('case*.json'))),'complete_quality_receivers_not_yet_prepared':True,'actual_new_official_scores':0,'new_future_inference':0,'historical_main_publication':status('actual_fine146_historical_controls_main_publication_v30_20261008')}
    state['isolated_serialization_benchmark']={'actual_service':status('actual_full_board_deferred_serialization_benchmark_v1_20261008'),'gate':'actual145_full_completion_then24GiB_available_RAM','original139_to145_runtime_retained':True,'full_measurement_not_yet_adopted':True,'preparation_main':status('actual_full_board_deferred_preparation_main_publication_v29_20261008')}
"""
    observer = observer.replace(before, additions + before)
    before = "    write(A/'optimization_live_progress_v28_20261008.md',text)"
    assert observer.count(before) == 1
    observer = observer.replace(before, "    text+=f\"\\n第146轮新方向：完整历史控制{state['fine146_frontier']['actual_full_control_records']}/121，原生复现{state['fine146_frontier']['actual_native30']['status']}；125项评分与候选流程仍需准备。\\n\"\n    text+=f\"\\n完整榜重复编码隔离基准：{state['isolated_serialization_benchmark']['actual_service']['status']}，排在145轮完成之后；尚未采用新运行方式。\\n\"\n" + before)
    observer = observer.replace('optimization_live_progress_v28_20261008', 'optimization_live_progress_v29_20261008')
    observer_target = A / 'monitor_actual_chronological_optimization_progress_v29_20261008.py'
    compile(observer, str(observer_target), 'exec')
    with observer_target.open('x', encoding='utf-8', newline='') as stream:
        stream.write(observer)
    pins = {str(p): sha(p) for p in [Path(__file__), original, target, observer_source, observer_target,
            A / 'HuberCrossFamilyFine146_historical_receiver_preparation_v1_20261008.json',
            A / 'HuberCrossFamilyFine146_historical_hidden_launches_v1_20261008.json']}
    publisher = start('actual_fine146_historical_controls_main_publication_v30_20261008', target.name, [], pins)
    monitor = start('actual_chronological_optimization_progress_observer_v29_20261008', observer_target.name, [], pins)
    create(A / 'fine146_historical_main_and_progress_v30_hidden_launches_20261008.json',
           {'status': 'started_actual_controls_publication_queue_and_compact_observer',
            'publisher': publisher, 'observer': monitor, 'input_sha256': pins,
            'new_quality_scores': 0, 'test_labels_read': False})
    create(A / 'latest_actual_optimization_progress_pointer_v29_20261008.json',
           {'path': str(A / 'optimization_live_progress_v29_20261008.json'),
            'human_readable': str(A / 'optimization_live_progress_v29_20261008.md'),
            'actual_observer_identity': monitor})
    print(json.dumps({'status': 'started', 'publisher_worker': publisher['owned_worker_pid'],
                      'observer_worker': monitor['owned_worker_pid']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
