"""Publish the additional cleanup evidence to the existing main branch."""
from pathlib import Path
import gzip
import hashlib
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
import watch_validations_main_v2_20261005 as watcher
from finalize_main_branch_consolidation_20261005 import verify_main
from publish_main_closeout_v2_20261005 import blob_hashes

sync = watcher.sync
OUT = A / 'completed_unselected_artifact_cleanup_20261006'
PREFIX = Path('validation_sync/completed_unselected_artifact_cleanup_20261006')


def main():
    assert not (OUT / 'github_receipt.json').exists(), 'Preserve the existing publication receipt.'
    proof = sync.read(OUT / 'verification.json')
    assert proof['status'] == 'passed_additional_completed_unselected_artifact_cleanup'
    assert proof['new_missing_protected_dependencies'] == 0
    plan = sync.read(OUT / 'plan.json')
    for name, digest in plan['source_sha256'].items():
        with Path(name).open('rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest, name
    # The last observers are absent; do not create or stop a scientific process.
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            command = ' '.join(process.info['cmdline'] or [])
            if (process.info['name'] or '').lower() == 'python.exe':
                assert not any(name in command for name in (
                    'watch_validations_main_v3_20261005.py',
                    'monitor_actual_optimization_progress_v18_20261005.py')), process.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    assert sync.git('branch', '--show-current') == ''
    assert not sync.git('status', '--porcelain')
    previous = sync.git('rev-parse', 'HEAD')
    assert sync.git('rev-parse', 'HEAD', cwd=ROOT) == previous
    verify_main(previous)
    sources = [A / 'cleanup_completed_unselected_artifacts_20261006.py', Path(__file__),
               OUT / 'plan.json', OUT / 'deletions.jsonl', OUT / 'verification.json']
    targets, files = {}, {}
    for source in sources:
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A else PREFIX / source.name
        raw_digest = sync.sha(data)
        if len(data) > 5 * 1024**2:
            data = gzip.compress(data, mtime=0)
            destination = Path(destination.as_posix() + '.gz')
        targets[destination.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {
            'published_path': destination.as_posix(), 'raw_sha256': raw_digest,
            'published_sha256': sync.sha(data), 'published_bytes': len(data)}
    targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
    targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
        'status': 'completed_additional_cleanup_verified_all_retained_records',
        'at_local': sync.now(), 'previous_main': previous, 'files': files, 'verification': proof,
        'only_publication_branch': 'main', 'raw_data_weights_predictions_not_uploaded': True,
        'cleanup_did_not_restart_interrupted_scientific_workflows': True,
        'incomplete_experiments_not_reclassified_as_rejected': True,
        'test_labels_read': False, 'new_model_fits': 0, 'new_quality_scores': 0})
    targets[(PREFIX / 'README.md').as_posix()] = (
        '# 已完成验证的弃用产物追加清理\n\n'
        f"本轮直接删除 {proof['deleted_files']} 份完成验证后的缓存和评分副本，"
        f"实际D盘空闲量增加 {proof['actual_D_free_bytes_change_during_deletion']/2**30:.2f} GiB。"
        '文件包含硬链接，不能将逻辑大小当作释放空间。未创建清理备份。\n\n'
        f"加上先前清理，累计删除模型权重 {proof['cumulative_deleted_model_weights']} 份、"
        f"预测及派生缓存 {proof['cumulative_deleted_prediction_or_derived_caches']} 份。"
        f"本轮重新核对 {proof['retained_records_SHA256_unchanged']} 份记录的SHA256，"
        '分数、完整榜、日志、配置和源码均保留。当前交付方案、R65/R66候选与原始数据保留；'
        '待完成验证仍引用的冻结模型库依赖保留，未将进程中断视为模型淘汰。\n\n'
        'plan.json是删除前清单与保留记录哈希；deletions.jsonl是实际逐文件日志；'
        'verification.json是删除后的复核。较大清单无损gzip保存。'
        '原冻结验证文件继续表示当时验证事实，历史产物当前是否存在以删除日志为准。'
        '项目产物未写入C盘，GitHub仅使用main分支。\n'
    ).encode('utf-8')
    for name, data in targets.items():
        sync.atomic(sync.WORKTREE / name, data)
    paths = sorted(targets)
    for offset in range(0, len(paths), 50):
        sync.git('add', '-f', '--', *paths[offset:offset+50])
    staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
    assert staged and staged <= set(paths)
    sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
             '追加清理完成验证缓存，保留全部分数记录与未完成验证依赖', timeout=180)
    commit = sync.git('rev-parse', 'HEAD')
    expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
    assert blob_hashes(commit, expected) == expected
    sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
    verify_main(commit)
    watcher.advance_source_index(commit)
    receipt = {'status': 'pushed_verified_additional_artifact_cleanup_main_only',
        'at_local': sync.now(), 'commit': commit, 'files': len(paths),
        'raw_git_blob_sha256_verified': len(expected),
        'local_branches': ['main'], 'remote_branches': ['main'], 'default_branch': 'main',
        'url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
    with (OUT / 'github_receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
