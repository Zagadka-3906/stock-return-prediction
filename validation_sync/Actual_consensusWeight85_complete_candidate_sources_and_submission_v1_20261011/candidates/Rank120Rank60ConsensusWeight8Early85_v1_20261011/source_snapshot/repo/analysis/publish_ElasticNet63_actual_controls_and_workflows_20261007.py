"""Publish measured local acceleration and strict unfinished-grid repair evidence on main."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    p = A / 'service_owned_workflows_20261006' / name
    while not (p / 'native_launch.json').exists() or owned(read(p / 'native_launch.json')):
        time.sleep(15)
    assert read(p / 'service_execution.json')['status'] == 'passed', name
    return p


def main():
    import psutil
    diagnostic=closed('cpu_ElasticNet63_codec_preflight')
    memory_service=closed('ElasticNet_memory_preprocessing_preflight')
    handoff_service=closed('ElasticNet24_idle_publication_routes_v2_actual_handoff')
    folder=A/'cpu_ElasticNet63_codec_preflight_20261007';proof=read(folder/'verification.json')
    assert proof['status']=='passed_actual_four_ElasticNet63_native_target_units_decoder_batch_boundary_and_maturity_controls'
    memory=A/'ElasticNet_memory_preprocessing_preflight_20261007/verification.json';assert read(memory)['status']=='passed_actual_historical63_column_statistics_and_native_training_layout_controls'
    handoff=A/'ElasticNet24_idle_publication_routes_v2_actual_handoff_20261007/verification.json';assert read(handoff)['status']=='passed_actual_two_idle_ElasticNet_bank_score_publishers_source_route_v2_handoff'
    out=A/'ElasticNet63_actual_controls_and_workflows_github_20261007';assert not out.exists();out.mkdir()
    names=['cpu_full_universe_ElasticNet_native_bank24','full_universe_ElasticNet44_official_comparison','cpu_full_universe_ElasticNet24_bank_evidence_publication_v2','cpu_full_universe_ElasticNet24_scores_evidence_publication_v2']
    rows={n:read(A/'service_owned_workflows_20261006'/n/'native_launch.json') for n in names};assert all(owned(r) for r in rows.values())
    create(out/'actual_local_dispatch_snapshot.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'identities':rows,'all_strong_owned_live_now':True,'all_console_handles_zero':all(r['actual_native_console_handle']==0 for r in rows.values()),'planned_full_native_fits':24,'planned_official_records':44,'actual_full_fits':0,'actual_official_records':0,'full113_QA24_and_main_required_before_training':True,'future_candidate_freeze_inference_full_board_not_yet_claimed':True,'remote_workers':0,'test_labels_read':False})
    sources=[Path(__file__),folder/'verification.json',folder/'frozen_before_actual_controls.json',memory,memory.parent/'frozen_before_actual_control.json',handoff,handoff.parent/'frozen_before_actual_handoff.json',out/'actual_local_dispatch_snapshot.json']
    sources += [A/n for n in ('cpu_full_universe_ElasticNet_bank24_plan_20261007.json','cpu_full_universe_ElasticNet_bank24_admission_20261007.json','cpu_ElasticNet63_codec_preflight_admission_20261007.json','cpu_ElasticNet_independent_linear_codec_20261007.py','ElasticNet_memory_bounded_preprocessing_20261007.py','verify_cpu_ElasticNet63_codec_20261007.py','verify_ElasticNet_memory_preprocessing_20261007.py','train_cpu_full_universe_ElasticNet_bank24_20261007.py','run_full_universe_ElasticNet44_official_comparison_20261007.py','publish_cpu_full_universe_ElasticNet24_evidence_20261007.py','publish_cpu_full_universe_ElasticNet24_evidence_v2_20261007.py','handoff_ElasticNet24_idle_publication_routes_v2_20261007.py')]
    for n in [*names,'cpu_ElasticNet63_codec_preflight','ElasticNet_memory_preprocessing_preflight','ElasticNet24_idle_publication_routes_v2_actual_handoff']:
        service=A/'service_owned_workflows_20261006'/n;sources += [service/f for f in ('job_definition.json','native_launch.json','verified_hidden_launch.json')]
        if n not in names:sources += [service/'service_execution.json',service/'stdout.log',service/'stderr.log']
    for phase in ('bank','scores'):
        service=A/f'service_owned_workflows_20261006/cpu_full_universe_ElasticNet24_{phase}_evidence_publication'
        sources += [service/n for n in ('job_definition.json','native_launch.json','administrative_supersession_ElasticNet24_routes_v2_20261007.json')]
    pins={**proof['input_sha256'],**read(memory)['input_sha256'],**read(handoff)['input_sha256'],**{str(p.resolve()):sha(p) for p in sources}}
    create(out / 'frozen_before_main_publication.json', {'input_sha256': pins, 'test_labels_read': False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held, retries = [], []
    restore = install()
    sync = helpers.sync
    old_git = sync.git

    def retry_git(*args, **kwargs):
        for attempt in range(3):
            try:
                return old_git(*args, **kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote', 'push', 'fetch') or not any(t in str(error).lower() for t in ('tls', 'ssl', 'connection', 'timed out', 'unable to access')):
                    raise
                retries.append({'command': args[0], 'attempt': attempt + 1, 'error': str(error)[:1000]})
                if attempt == 2:
                    raise
                time.sleep(2)

    sync.git = retry_git
    try:
        row = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        with LockedReadHashCache(pins) as scope:
            prefix = Path('validation_sync/ElasticNet63_actual_controls_and_workflows_20261007')
            payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
            files = {}
            for p in dict.fromkeys([*sources, out / 'frozen_before_main_publication.json']):
                data = p.read_bytes()
                assert not sync.SECRET.search(data), p
                raw_sha = hashlib.sha256(data).hexdigest()
                target = (prefix / p.relative_to(ROOT)).as_posix()
                if len(data) >= 5 * 1024**2:
                    data = gzip.compress(data, mtime=0)
                    assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_sha
                    target += '.gz'
                payload[target] = data
                files[p.relative_to(ROOT).as_posix()] = {'published_path': target, 'original_sha256': raw_sha, 'published_sha256': hashlib.sha256(data).hexdigest()}
            previous = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous)
            assert not sync.git('status', '--porcelain')
            manifest={'status':proof['status'],'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main','actual_diagnostic_fits':4,'actual_selection_fits':0,'actual_official_scores':0,'actual_original63_fields_historical_model_prediction_rows_each':601,'additional_repeated_historical_matrix_rows_each':16389,'actual_native_saved_reload_and_independent_linear_decoder_full_and_empty_batch_boundary_bits_exact':True,'actual_historical_column_statistics_and_Fortran_prediction_layout_controls_passed':True,'actual_future24_training_44_scores_candidate_freeze_full1599600_and_full_board_not_claimed':True,'planned_full_native_fits':24,'planned_official_cases':44,'all4_hidden_local_dispatches_owned_now':True,'source_filename_corrected_in_exact_idle_unexecuted_bank_and_score_publication_helpers':True,'scientific_workers_stopped_or_restarted':0,'remote_workers_dispatched':0,'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded(manifest)
            payload[(prefix/'README.md').as_posix()]=('# 全股票池ElasticNet实际诊断与完整验证准备\n\n'
                '[ElasticNet官方文档](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html)。本方向补充L1与L2混合稀疏正则化。原有线性银行为Ridge、平方/Huber损失L2-SGD；此记录不把较早树L1或Ridge_lambda1解释为ElasticNet覆盖。\n\n'
                '排序/收益目标与alpha=.001/.01形成4种固定配置，L1比例.5，原生坐标下降最多2000轮。'
                '4个真实512条历史训练诊断模型已保存重载，601条历史预测及扩展16389条重复历史矩阵，空输入、8191/8192/8193边界、独立系数解码逐位通过。目标标准化及收益限幅只来自自身成熟过去；未来标签污染的训练掩码和过去标签负对照均通过。'
                '分列预处理与原统计公式在真实历史数据上按1e-12核对；相同统计量下Fortran训练矩阵与预测准备逐位一致。该控制未测量完整训练内存峰值。\n\n'
                '24次完整2020—2024年度及2025最终训练、44项完整收益映射官方比较和两阶段main发布已真正隐藏派发，仅等待已声明的完整第113轮QA24/main和RAM。'
                '候选冻结、真实1599600行推理和完整榜登记仍需后续实际完成；当前不声称获得新官方分数、候选资格或全局资源极限。'
                '已有选模偏差未校正，真实测试标签不读，仅main，数据/权重/预测留D盘。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存ElasticNet四个真实63维目标回归诊断及独立解码和内存预处理控制与24模型44评分队列', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'commit': commit, 'at_local': sync.now(),
                'branch': 'main', 'raw_git_blobs_verified': len(hashes), 'new_quality_scores': 0,
                'all_source_inputs_initial_and_final_read_locked_full_rehash': True,
                'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
            print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    finally:
        sync.git = old_git
        for p in reversed(held):
            if p.is_running():
                p.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})
        create(out / 'transport_retries.json', {'attempts': retries, 'TLS_verification_unchanged': True})


if __name__ == '__main__':
    main()
