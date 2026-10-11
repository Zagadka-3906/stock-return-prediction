"""Publish local throughput evidence and every completed native/official case on main."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, owned, sha
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def wait_closed(name):
    folder = A / 'service_owned_workflows_20261006' / name
    while not (folder / 'native_launch.json').exists():
        time.sleep(15)
    row = read(folder / 'native_launch.json')
    while owned(row):
        time.sleep(15)
    assert read(folder / 'service_execution.json')['status'] == 'passed', name
    return folder


def main(phase):
    assert phase in ('bank', 'scores')
    bank = A / 'cpu_full_universe_ElasticNet_bank24_recovery_v2_20261007'
    science = wait_closed('cpu_full_universe_ElasticNet_native_bank24_v2' if phase == 'bank'
        else 'full_universe_ElasticNet44_official_comparison_v2')
    if phase == 'scores':
        wait_closed('cpu_full_universe_ElasticNet24_bank_evidence_publication_v3')
    folder = bank if phase == 'bank' else A / 'full_universe_ElasticNet44_official_comparison_v2_20261007'
    proof = read(folder / 'verification.json')
    assert proof['status'] == ('passed_actual24_full_universe_CPU_ElasticNet_native_target_units_and_independent_full_prefix_controls'
        if phase == 'bank' else 'passed_actual44_full_universe_CPU_ElasticNet_CDF_full_official_comparisons')
    bank_proof = read(bank / 'verification.json')
    assert bank_proof['actual_native_fits'] == len(bank_proof['actual_models']) == 24
    for item in bank_proof['actual_models']:
        assert sha(Path(item['native_model_path'])) == item['native_model_sha256']
        assert sha(Path(item['independent_linear_state_path'])) == item['independent_linear_state_sha256']
    if phase == 'scores':
        assert len(proof['records']) == proof['new_quality_score_records'] == 44
    out = A / f'cpu_full_universe_ElasticNet24_{phase}_recovery_v2_github_20261007'
    assert not out.exists()
    out.mkdir()
    prefix = Path(f'validation_sync/cpu_full_universe_ElasticNet24_{phase}_recovery_v2_20261007')
    sources = [Path(__file__), A / 'train_cpu_full_universe_ElasticNet_bank24_recovery_v2_20261007.py',
        A / 'cpu_full_universe_ElasticNet_bank24_plan_20261007.json',
        A / 'cpu_full_universe_ElasticNet_bank24_admission_20261007.json',
        A / 'cpu_ElasticNet_independent_linear_codec_20261007.py', A / 'ElasticNet_memory_bounded_preprocessing_20261007.py', A / 'ElasticNet_memory_preprocessing_preflight_20261007/verification.json',
        A / 'verify_cpu_ElasticNet63_codec_20261007.py',
        A / 'full_universe_HGB_percentile_CDF_transform_20261007.py',
        A / 'run_full_universe_ElasticNet44_official_comparison_v2_20261007.py',
        *list((A / 'cpu_ElasticNet63_codec_preflight_20261007').glob('verification.json')),
        *[p for p in bank.rglob('*.json') if not p.name.startswith('independent_linear_state_')],
        *list(science.glob('*.json')), *list(science.glob('*.log'))]
    if phase == 'scores':
        sources += [A / 'full_universe_HGB_percentile_CDF_transform_20261007.py',
            A / 'run_full_universe_ElasticNet44_official_comparison_v2_20261007.py',
            *folder.rglob('*.json')]
        for item in proof['records']:
            capsule = Path(item['official_score_cache']['official_metrics_source'])
            assert sha(capsule) == item['official_metric_capsule_sha256']
            assert read(capsule)['metrics'] == item['metrics']
            sources.append(capsule)
    sync = helpers.sync
    payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data), source
        digest = hashlib.sha256(data).hexdigest()
        target = prefix / source.relative_to(ROOT)
        if len(data) >= 5 * 1024**2:
            data = gzip.compress(data, mtime=0)
            assert hashlib.sha256(gzip.decompress(data)).hexdigest() == digest
            target = Path(target.as_posix() + '.gz')
        payload[target.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': target.as_posix(),
            'original_sha256': digest, 'published_sha256': hashlib.sha256(data).hexdigest()}
    pins = {**bank_proof['input_sha256'], **proof['input_sha256'], **{str(p): sha(p) for p in sources}}
    for name in bank_proof['configurations']:
        path = bank / name / 'raw_oof_predictions.npy'
        expected = read(bank / name / 'oof_verification.json')['prediction_array_sha256']
        assert sha(path) == expected
        pins[str(path)] = expected
    for item in bank_proof['actual_models']:
        pins[item['native_model_path']] = item['native_model_sha256']
        pins[item['independent_linear_state_path']] = item['independent_linear_state_sha256']
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    scope = LockedReadHashCache(pins)
    scope.__enter__()
    held, retries = [], []
    restore = install()
    original_git = sync.git
    def retry_git(*args, **kwargs):
        for attempt in range(3):
            try:
                return original_git(*args, **kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote', 'push', 'fetch') or not any(
                    token in str(error).lower() for token in ('tls', 'ssl', 'connection', 'timed out', 'unable to access')):
                    raise
                retries.append({'command': args[0], 'attempt': attempt + 1, 'error': str(error)[:1200]})
                if attempt == 2:
                    raise
                time.sleep(2)
    sync.git = retry_git
    try:
        publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(publisher, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        scope.reverify()
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        manifest = {'status': proof['status'], 'phase': phase, 'at_local': sync.now(), 'files': files,
            'actual_native_model_fits': 24, 'separate_codec_diagnostic_fits': 4,
            'scored_records': 0 if phase == 'bank' else 44, 'only_branch': 'main', 'previous_main': previous,
            'execution_mode': 'local_CPU2threads_original_GPU_worker_unmodified',
            'benchmark_speedup_not_claimed_as_total_goal_speedup': True,
            'models_predictions_and_training_data_not_uploaded': True,
            'candidate_and_complete_ranking_qualification_pending': True,
            'idle_publisher_before_and_after_hold': idle, 'scientific_workers_stopped_or_restarted': 0,
            'test_labels_read': False}
        if phase == 'scores':
            manifest['best_actual_official_record'] = proof['best']
        payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
        payload[(prefix/'README.md').as_posix()]=('# 全股票池ElasticNet\n\n'
            '[ElasticNet官方文档](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html)。'
            '四种固定配置：排序/收益目标分别配alpha=.001/.01，L1比例.5，原生坐标下降最多2000轮，无验证早停。'
            '所有目标和特征缩放仅来自对应成熟过去，收益目标先按自身过去.005/.995分位限幅再标准化，预测反变换回目标单位。\n\n'
            '2020—2024逐年向前验证及2025最终拟合共24次，原生模型重载、独立系数解码、空输入、8192批次边界和实际日期前缀核对。'
            '四模型先各自转为同日百分位，再构造三个按声明顺序的均值，与106进行CDF融合，共44项完整官方评分比较。'
            '分列预处理在真实历史数据上通过统计量及训练/预测布局对照；不声称完整训练内存峰值或全局极限已被测定。\n'
            f'当前阶段：{phase}。完整候选冻结、1599600行推理和完整榜资格仍待实际完成。'
            '已有自适应选模偏差未校正，真实测试标签未读，只main，模型、预测与数据留D盘。\n').encode('utf-8')
        for name, data in payload.items():
            sync.atomic(sync.WORKTREE / name, data)
        names = sorted(payload)
        for start in range(0, len(names), 50):
            sync.git('add', '-f', '--', *names[start:start+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(names)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            f'保存本机加速及24个全股票池ElasticNet模型的实际{phase}核验', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        scope.reverify()
        create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'phase': phase,
            'at_local': sync.now(), 'commit': commit, 'branch': 'main', 'actual_native_model_fits': 24,
            'scored_records': manifest['scored_records'], 'raw_git_blobs_verified': len(hashes),
            'candidate_and_complete_ranking_qualification_pending': True,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
        print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_local_phase_publication',
            'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        scope.close()
        sync.git = original_git
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_transport_retries.json', {'attempts': retries, 'TLS_verification_unchanged': True})
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main(sys.argv[1])
