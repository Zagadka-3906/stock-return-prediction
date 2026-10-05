"""Publish the completed deletion audit to main without touching scientific jobs."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import watch_validations_main_v2_20261005 as watcher
from finalize_main_branch_consolidation_20261005 import owned_pair, verify_main
from publish_main_closeout_v2_20261005 import blob_hashes
sync = watcher.sync
OUT = A / 'rejected_artifact_cleanup_20261005'
PREFIX = Path('validation_sync/rejected_artifact_cleanup_20261005')


def main():
    assert not (OUT / 'github_receipt.json').exists()
    proof = sync.read(OUT / 'verification.json')
    assert proof['status'] == 'passed_user_authorized_rejected_artifact_cleanup'
    assert proof['new_missing_protected_dependencies'] == 0
    integrity = sync.read(OUT / 'selected_artifact_integrity.json')
    assert integrity['status'] == 'passed_selected_artifact_integrity_after_cleanup'
    plan = sync.read(OUT / 'plan.json')
    cleanup_source = A / 'cleanup_rejected_artifacts_20261005.py'
    assert sync.sha(cleanup_source.read_bytes()) == plan['source_sha256']
    launch = sync.read(sync.OUT / 'launch_v3.json')['publisher']
    publisher = owned_pair(launch['pid'], Path(launch['script']), launch['script_args'])
    assert publisher[1].pid == sync.read(sync.OUT / 'owner.lock')['pid']
    launch = sync.read(A / 'actual_optimization_monitor_launch_v16_20261005.json')
    monitor = owned_pair(launch['pid'], Path(launch['script']), launch['script_args'])
    suspended = []
    try:
        for attempt in range(12):
            for parent, child in (publisher, monitor):
                for process in (child, parent):
                    process.suspend()
                    suspended.append(process)
            busy = [p for parent, child in (publisher, monitor) for p in parent.children(recursive=True)
                    if p.pid != child.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(1)
        else:
            raise RuntimeError('Publisher or observer is still busy.')
        previous = sync.git('rev-parse', 'HEAD')
        verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets, files = {}, {}
        for source in [cleanup_source, Path(__file__), A / 'verify_selected_artifacts_after_cleanup_20261005.py',
                       A / 'artifact_cleanup_selected_roots_retention_plan_20261005.json', OUT / 'plan.json',
                       OUT / 'deletions.jsonl', OUT / 'verification.json', OUT / 'selected_artifact_integrity.json']:
            data = source.read_bytes()
            assert not sync.SECRET.search(data)
            destination = source.relative_to(ROOT) if source.parent == A else PREFIX / source.name
            raw_sha = sync.sha(data)
            if len(data) > 5 * 1024**2:
                data = gzip.compress(data, mtime=0)
                destination = Path(destination.as_posix() + '.gz')
            targets[destination.as_posix()] = data
            files[source.relative_to(ROOT).as_posix()] = {
                'published_path': destination.as_posix(), 'raw_sha256': raw_sha,
                'published_sha256': sync.sha(data), 'published_bytes': len(data)}
        targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'completed_user_authorized_artifact_deletion_audit', 'at_local': sync.now(),
            'previous_main': previous, 'files': files, 'verification': proof, 'selected_artifact_integrity': integrity,
            'raw_data_weights_and_prediction_files_not_uploaded': True,
            'historical_scores_and_configurations_preserved': True,
            'current_selected_and_live_frozen_dependencies_preserved': True,
            'only_publication_branch': 'main', 'test_labels_read': False})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 弃用模型与历史缓存清理\n\n'
            f"按用户直接删除的要求，删除 {proof['deleted_files']} 个已弃用或历史副本文件，"
            f"其中模型权重 {proof['deleted_by_kind'].get('model_weight', 0)} 个。"
            f"逻辑大小 {proof['deleted_logical_bytes']/2**30:.2f} GiB，"
            f"D盘空闲量净增加 {proof['D_free_bytes_change']/2**30:.2f} GiB。"
            '净变化同时受正在运行的训练写入和文件硬链接影响。\n\n'
            f"逐一复核 {proof['record_files_verified_unchanged']} 份记录，字节 SHA256 保持一致。"
            '分数、完整榜、配置、源码和原始数据保留；当前方案及未完成验证的冻结依赖保留。'
            '已有清理备份中的实验副本、历史实验权重与预测缓存直接删除，没有再次备份。'
            '正在训练的进程没有停止或重启；项目文件未写入C盘。\n\n'
            'plan.json为删除前路径、大小、哈希与保留依赖清单，deletions.jsonl为实际逐文件日志，'
            'verification.json为核验结果。较大清单使用无损gzip保存。'
            '旧验证清单继续作为当时的历史证据，清理后的权重是否仍存在应以本次删除日志为准。'
            '冻结验证仍引用的原模型库文件需要保留到相关任务结束，不能据此声称已经删除全部历史权重。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        paths = sorted(targets)
        for offset in range(0, len(paths), 50):
            sync.git('add', '-f', '--', *paths[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '删除弃用模型与历史缓存，保留全部记录分数及当前验证依赖', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_rejected_artifact_cleanup_main_only',
            'at_local': sync.now(), 'commit': commit, 'files': len(targets),
            'raw_git_blob_sha256_verified': len(expected),
            'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(OUT / 'github_receipt.json', sync.encoded(receipt))
        print(json.dumps(receipt, ensure_ascii=False), flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()


if __name__ == '__main__':
    main()
