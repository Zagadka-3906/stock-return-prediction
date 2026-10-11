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
    bank = A / 'direct_flag_centered_rank_bank36_20261007'
    science = wait_closed('direct_flag_centered_rank_native_bank36' if phase == 'bank'
        else 'direct_flag_rank92_official_comparison')
    if phase == 'scores':
        wait_closed('single_host_rank36_bank_evidence_publication')
    wait_closed('lowalpha_huber_residual_scores50_evidence_publication')
    folder = bank if phase == 'bank' else A / 'direct_flag_rank92_official_comparison_20261007'
    proof = read(folder / 'verification.json')
    assert proof['status'] == ('passed_actual36_direct_centered_rank_native_saved_independent_and_prefix_controls'
        if phase == 'bank' else 'passed_actual92_direct_rank_CDF_full_official_comparisons')
    bank_proof = read(bank / 'verification.json')
    assert bank_proof['actual_native_fits'] == len(bank_proof['actual_models']) == 36
    for item in bank_proof['actual_models']:
        assert sha(Path(item['native_model_path'])) == item['native_model_sha256']
        assert sha(Path(item['independent_tree_dump_path'])) == item['independent_tree_dump_sha256']
    if phase == 'scores':
        assert len(proof['records']) == proof['new_quality_score_records'] == 92
    out = A / f'single_host_rank36_{phase}_github_20261007'
    assert not out.exists()
    out.mkdir()
    prefix = Path(f'validation_sync/single_host_rank36_{phase}_20261007')
    sources = [Path(__file__), A / 'benchmark_local_flag_tree_threads_20261007.py',
        A / 'train_direct_flag_centered_rank_bank36_20261007.py',
        A / 'single_host_direct_flag_rank_plan_20261007.json',
        A / 'single_host_direct_flag_rank_hidden_launch_20261007.json',
        A / 'conditional_identity_regression_tree_codec_20261006.py',
        A / 'conditional_flag_rank_codec_20261006.py',
        *list((A / 'local_flag_tree_thread_benchmark_20261007').glob('*.json')),
        *[p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')],
        *list(science.glob('*.json')), *list(science.glob('*.log'))]
    if phase == 'scores':
        sources += [A / 'direct_flag_centered_rank_CDF_transform_20261007.py',
            A / 'run_direct_flag_rank92_official_comparison_20261007.py',
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
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        manifest = {'status': proof['status'], 'phase': phase, 'at_local': sync.now(), 'files': files,
            'actual_native_model_fits': 36, 'separate_hardware_benchmark_diagnostic_fits': 6,
            'scored_records': 0 if phase == 'bank' else 92, 'only_branch': 'main', 'previous_main': previous,
            'execution_mode': 'local_CPU8threads_original_GPU_worker_unmodified',
            'measured_benchmark_speedup_over_2threads': read(A / 'local_flag_tree_thread_benchmark_20261007/verification.json')['measured_speedup_over_2_threads'],
            'benchmark_speedup_not_claimed_as_total_goal_speedup': True,
            'models_predictions_and_training_data_not_uploaded': True,
            'candidate_and_complete_ranking_qualification_pending': True,
            'idle_publisher_before_and_after_hold': idle, 'scientific_workers_stopped_or_restarted': 0,
            'test_labels_read': False}
        if phase == 'scores':
            manifest['best_actual_official_record'] = proof['best']
        payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
        payload[(prefix / 'README.md').as_posix()] = (
            '# 本机加速与直接排名模型\n\n'
            '用户取消双机协作，所有任务只在本机运行。六次训练窗口内部硬件基准仅选择线程数，'
            '两次重复均核对树结构及预测逐位一致；8线程实测约为2线程的2.41倍，不能当作整体任务加速倍数。\n\n'
            '六个固定模型为L2或Huber(alpha0.1)，叶数7/15/31，最多256棵树。'
            '2020—2024年度连续向前验证和2025最终拟合，共36次真实新拟合。'
            '每年训练窗口只构造一次分箱，供当年的六个模型复用，年度之间不共享分箱。'
            '目标为原features.py从提供训练收益生成的居中排名y_rank，并非原始CSV另行提供的字段。'
            '原生保存重载、独立树解码及80/260/975日前缀核验全部实际执行。\n\n'
            '早期64轮直接模型已覆盖2020；新方向扩展树数、损失及居中目标，不声称此前全部遗漏2020。'
            '预先声明92项最终收益率映射后的完整官方比较，包含当前合格100/106锚点，'
            '六个头及三个固定均值，各五种权重和两种当日可用预测CDF池。'
            '以原官方总分选优，完整候选冻结、推理和完整榜资格另行完成。\n\n'
            f'本阶段为{phase}。真实测试标签未读取；现有超宽网络保持运行；'
            '只提交main，上传记录和代码，权重与数据留在D盘。\n').encode('utf-8')
        for name, data in payload.items():
            sync.atomic(sync.WORKTREE / name, data)
        names = sorted(payload)
        for start in range(0, len(names), 50):
            sync.git('add', '-f', '--', *names[start:start+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(names)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            f'保存本机加速及36模型的实际{phase}核验', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'phase': phase,
            'at_local': sync.now(), 'commit': commit, 'branch': 'main', 'actual_native_model_fits': 36,
            'scored_records': manifest['scored_records'], 'raw_git_blobs_verified': len(hashes),
            'candidate_and_complete_ranking_qualification_pending': True,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
        print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_local_phase_publication',
            'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        sync.git = original_git
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_transport_retries.json', {'attempts': retries, 'TLS_verification_unchanged': True})
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main(sys.argv[1])
