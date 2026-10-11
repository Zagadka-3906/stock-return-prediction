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
    bank = A / 'cpu_full_universe_HGB_bank24_recovery_v2_20261007'
    science = wait_closed('cpu_full_universe_HGB_native_bank24_v2' if phase == 'bank'
        else 'full_universe_HGB44_official_comparison_v3')
    if phase == 'scores':
        wait_closed('cpu_full_universe_HGB24_bank_evidence_publication_v2')
    folder = bank if phase == 'bank' else A / 'full_universe_HGB44_official_comparison_v3_20261007'
    proof = read(folder / 'verification.json')
    assert proof['status'] == ('passed_actual24_full_universe_CPU_HGB_native_reloads_and_original256_new8192_independent_full_prefix_controls'
        if phase == 'bank' else 'passed_actual44_full_universe_CPU_HGB_CDF_full_official_comparisons')
    bank_proof = read(bank / 'verification.json')
    assert bank_proof['actual_native_fits'] == len(bank_proof['actual_models']) == 24
    for item in bank_proof['actual_models']:
        assert sha(Path(item['native_model_path'])) == item['native_model_sha256']
        assert sha(Path(item['independent_hist_tree_state_path'])) == item['independent_hist_tree_state_sha256']
    if phase == 'scores':
        assert len(proof['records']) == proof['new_quality_score_records'] == 44
    out = A / f'cpu_full_universe_HGB24_{phase}_github_20261007'
    assert not out.exists()
    out.mkdir()
    prefix = Path(f'validation_sync/cpu_full_universe_HGB24_{phase}_20261007')
    sources = [Path(__file__), A / 'train_cpu_full_universe_HGB_bank24_recovery_v2_20261007.py',
        A / 'cpu_full_universe_HGB_bank24_plan_20261007.json',
        A / 'cpu_full_universe_HGB_bank24_admission_20261007.json',
        A / 'cpu_conditional_residual_hgb_codec_20261007.py',
        A / 'verify_cpu_full_universe_HGB63_codec_20261007.py',
        A / 'full_universe_HGB_percentile_CDF_transform_20261007.py',
        A / 'run_full_universe_HGB44_official_comparison_v3_20261007.py',
        *list((A / 'cpu_full_universe_HGB63_codec_preflight_20261007').glob('verification.json')),
        *[p for p in bank.rglob('*.json') if not p.name.startswith('independent_hist_tree_state_')],
        *list(science.glob('*.json')), *list(science.glob('*.log'))]
    if phase == 'scores':
        sources += [A / 'full_universe_HGB_percentile_CDF_transform_20261007.py',
            A / 'run_full_universe_HGB44_official_comparison_v3_20261007.py',
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
        pins[item['independent_hist_tree_state_path']] = item['independent_hist_tree_state_sha256']
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
            'execution_mode': 'local_CPU4threads_original_GPU_worker_unmodified',
            'benchmark_speedup_not_claimed_as_total_goal_speedup': True,
            'models_predictions_and_training_data_not_uploaded': True,
            'candidate_and_complete_ranking_qualification_pending': True,
            'idle_publisher_before_and_after_hold': idle, 'scientific_workers_stopped_or_restarted': 0,
            'test_labels_read': False}
        if phase == 'scores':
            manifest['best_actual_official_record'] = proof['best']
        payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
        payload[(prefix/'README.md').as_posix()]=('# 全股票池直方图梯度回归\n\n'
            '四种固定配置：排序目标7/31叶，收益目标15叶平方/绝对误差；全部96轮，CPU4线程，无验证早停。'
            '2020—2024逐年使用成熟的此前训练信息，另存2025最终模型，共24次实际拟合。'
            '原256批次、新8192批次、保存重载、独立数值树解码和80/260/975日前缀逐位核对。\n\n'
            '四个模型先各自转为同日百分位，再按声明顺序均值，避免排序/收益目标的原始单位混合。'
            '44项完整方案含100/106锚点，六种权重和七个单模型/集成头，最终收益映射CSV使用原官方评分。'
            '所有模型、集成、处理与校准只在训练期选择；真实测试标签未读取。'
            '选择偏差未校正；此阶段不声明候选冻结、完整榜资格或全局极限。\n'
            f'当前发布阶段：{phase}。权重及预测数组留在D盘，仅main。\n').encode('utf-8')
        for name, data in payload.items():
            sync.atomic(sync.WORKTREE / name, data)
        names = sorted(payload)
        for start in range(0, len(names), 50):
            sync.git('add', '-f', '--', *names[start:start+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(names)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            f'保存本机加速及24个全股票池HGB模型的实际{phase}核验', timeout=180)
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
