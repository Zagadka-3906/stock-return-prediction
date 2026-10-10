"""Publish actual specialist controls and preserved recovery evidence to main."""
from pathlib import Path
import gzip
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def main():
    original = A / 'conditional_flag_rank_bank_20261006'
    bank = A / 'conditional_flag_rank_bank_v2_20261006'
    services = [A / 'service_owned_workflows_20261006' / name for name in
        ('conditional_flag_rank_native_bank', 'conditional_flag_rank_native_bank_v2')]
    for service, expected in zip(services, ('failed', 'passed')):
        assert not owned(read(service / 'native_launch.json'))
        assert read(service / 'service_execution.json')['status'] == expected
    proof = read(bank / 'verification.json')
    assert proof['status'] == 'passed_actual18_mature_flag_specialists_native_and_independent_codec_controls'
    assert proof['actual_native_fits'] == len(proof['actual_models']) == 18
    out = A / 'conditional_flag_rank_native_bank_github_20261006'
    assert not out.exists()
    out.mkdir()
    prefix = Path('validation_sync/conditional_flag_rank_native_bank_20261006')
    sources = [Path(__file__), *(A / name for name in (
        'conditional_flag_rank_codec_20261006.py',
        'conditional_flag_rank_transform_20261006.py',
        'train_conditional_flag_rank_bank_20261006.py',
        'train_conditional_flag_rank_bank_v2_20261006.py',
        'run_conditional_flag_rank_official_comparison_20261006.py',
        'run_conditional_flag_rank_official_comparison_v2_20261006.py'))]
    sources += [p for folder in (original, bank) for p in folder.rglob('*.json')
        if not p.name.startswith('model_dump_')]
    sources += [p for folder in services for pattern in ('*.json', '*.log')
        for p in folder.glob(pattern)]
    sync = helpers.sync
    payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
    records = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data), source
        raw_digest = hashlib.sha256(data).hexdigest()
        target = prefix / source.relative_to(ROOT)
        if len(data) >= 5 * 1024**2:
            data = gzip.compress(data, mtime=0)
            assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_digest
            target = Path(target.as_posix() + '.gz')
        payload[target.as_posix()] = data
        records[source.relative_to(ROOT).as_posix()] = {
            'published_path': target.as_posix(), 'original_sha256': raw_digest,
            'published_sha256': hashlib.sha256(data).hexdigest()}
    identity = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    held = []
    restore = install()
    try:
        parent, worker, idle = suspended_idle(identity,
            '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        payload[(prefix / 'manifest.json').as_posix()] = sync.encoded({
            'status': proof['status'], 'files': records, 'at_local': sync.now(),
            'actual_native_fits': 18, 'new_fits_in_recovery': 17,
            'actual_original_fit_reused_without_retraining': 1,
            'original_Unicode_native_path_failure_preserved': True,
            'actual_full_native_saved_and_independent_tree_predictions_bit_equal': True,
            'official_quality_comparison_separate_and_pending': True,
            'native_model_weights_and_data_not_uploaded': True,
            'test_labels_read': False, 'previous_main': previous,
            'idle_publisher_before_and_after_hold': idle,
            'scientific_processes_suspended_or_restarted': 0, 'only_branch': 'main'})
        payload[(prefix / 'README.md').as_posix()] = (
            '# 涨停组条件排名专用模型：实际训练与核验\n\n'
            '三个预定CPU回归配置，7/15/31叶、每个实际64棵树；'
            '各自完成2020—2024五个连续向前模型及仅以成熟训练标签拟合的2025最终模型，共18个。'
            '训练目标先在每日完整有限标签股票池计算收益排名，再取题面涨停组；'
            '沿用原fold_cutoff、一天标签成熟条件与63个因果特征。'
            '所有年度实际涨停验证行的原生预测、保存模型重载和独立树遍历逐位相等，'
            '同时保留80/260/975日冷前缀、特征与标签对齐检查及模型哈希。\n\n'
            '第一次保存的2020模型因原生库不能直接打开中文路径而加载失败。'
            '原失败、日志及已训练权重哈希完整保留；恢复通过Python读取UTF8模型文本，'
            '核验原始完整树结构相同后复用该次实际拟合，另完成17次新拟合。'
            '这里是训练与推理一致性核验，质量分数由独立37方案官方比较产生，'
            '不提前宣称方案改善或完成候选资格。\n\n'
            '本目录保留源码、原始记录、哈希、分数来源与失败证据；'
            '不上传数据、预测数组或模型权重。只使用main。\n').encode('utf-8')
        for target, data in payload.items():
            sync.atomic(sync.WORKTREE / target, data)
        names = sorted(payload)
        for start in range(0, len(names), 50):
            sync.git('add', '-f', '--', *names[start:start + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(names)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '保存18个实际涨停条件模型的核验与中文路径加载恢复证据', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified',
            'commit': commit, 'at_local': sync.now(), 'branch': 'main',
            'raw_git_blobs_verified': len(hashes), 'actual_native_fits': 18,
            'official_quality_scores_by_this_publication': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
        print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_specialist_bank_publication',
            'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
