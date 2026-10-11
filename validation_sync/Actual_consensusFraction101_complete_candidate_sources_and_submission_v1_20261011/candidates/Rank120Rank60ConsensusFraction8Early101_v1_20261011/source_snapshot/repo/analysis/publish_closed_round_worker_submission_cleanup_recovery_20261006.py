"""Publish checked scratch deletion and preserved scientific qualifications to main."""
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
import publish_classifier_consensus_workflows_20261006 as helpers

OUT = A / 'closed_round_worker_submission_cleanup_recovery_github_20261006'
PREFIX = Path('validation_sync/closed_round_worker_submission_cleanup_20261006')


def main():
    source = A / 'closed_round_worker_submission_cleanup_20261006'
    recovery = A / 'closed_round_worker_submission_cleanup_recovery_20261006'
    proof, plan = read(recovery / 'verification.json'), read(source / 'plan.json')
    assert proof['original_failure_retained'] is True
    assert proof['new_deletions_by_recovery'] == 0
    assert proof['status'] == 'passed_closed_published_round_worker_scratch_cleanup'
    assert proof['deleted_files'] == 3 and proof['original_qualification_before_and_after_identical'] is True
    assert proof['model_weights_deleted'] == proof['candidate_submissions_deleted'] == 0
    assert sha(A / 'cleanup_closed_round_worker_submissions_20261006.py') == plan['source_sha256']
    for path, digest in plan['retained_records_sha256'].items(): assert sha(path) == digest, path
    assert not OUT.exists(); OUT.mkdir()
    sync = helpers.sync
    targets, files = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}, {}
    sources = [Path(__file__), A / 'cleanup_closed_round_worker_submissions_20261006.py',
               A / 'verify_closed_round_worker_submission_cleanup_recovery_20261006.py',
               A / 'publish_closed_round_worker_submission_cleanup_20261006.py',
               *sorted(source.glob('*.json')), source / 'deletions.jsonl', *sorted(recovery.glob('*.json'))]
    for path in sources:
        data = path.read_bytes(); assert not sync.SECRET.search(data)
        target = path.relative_to(ROOT) if path.parent == A else PREFIX / path.relative_to(A)
        raw_sha = hashlib.sha256(data).hexdigest()
        if len(data) > 5 * 1024**2:
            data = gzip.compress(data, mtime=0); target = Path(target.as_posix() + '.gz')
        targets[target.as_posix()] = data
        files[path.relative_to(ROOT).as_posix()] = {'published_path': target.as_posix(), 'raw_sha256': raw_sha,
                                                   'published_sha256': hashlib.sha256(data).hexdigest()}
    row = read(A / 'service_owned_workflows_20261006/main_publisher_v6/native_launch.json'); assert owned(row)
    root, worker = helpers.owned_pair(row['pid'], Path(row['script']), row['script_args'])
    suspended, restore = [], install()
    try:
        for _ in range(300):
            for p in (worker, root): p.suspend(); suspended.append(p)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy: break
            for p in reversed(suspended): p.resume()
            suspended.clear(); time.sleep(1)
        else: raise RuntimeError('Main6 owns an active publication command')
        previous = sync.git('rev-parse', 'HEAD'); helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': proof['status'], 'previous_main': previous, 'at_local': sync.now(),
            'files': files, 'verification': proof, 'only_publication_branch': 'main',
            'raw_data_and_models_and_predictions_not_uploaded': True})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 第82—84轮临时评分CSV清理\n\n'
            f"删除三份已完成且已上传验证的工作进程临时submission.csv，逻辑大小{proof['deleted_logical_bytes']/2**30:.3f}GiB。"
            '逐文件核对路径、文件身份和SHA，扫描实际冻结输入及递归JSON来源，确认不作为后续输入；'
            '完成前后原资格检查结果一致，配置、分数、源码及日志哈希保持一致。\n\n'
            '当前方案、候选提交、模型权重、原始数据、待完成验证均保留。'
            '历史官方评分胶囊里的CSV哈希描述当时评分文件；当前临时文件删除状态以deletions.jsonl为准。'
            '首次执行已完成删除，但复核时碰到R85刷新共享完整榜而记录失败。原失败、源码及删除日志保留；'
            '独立复核排除这一可变共享榜，确认3180份冻结来源和744份记录不变，原三轮资格一致，不重复删除。'
            '这是已授权的历史缓存清理，不新增训练或评分，项目数据未写入C盘。只提交main。\n'
        ).encode('utf-8')
        for name, data in targets.items(): sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50): sync.git('add', '-f', '--', *selected[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
                 '清理已发布82至84轮临时评分CSV，保留全部分数及冻结依赖', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit); helpers.watcher.advance_source_index(commit)
        receipt = {'status': 'pushed_verified_closed_round_worker_scratch_cleanup_main_only',
                   'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected),
                   'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()}
        create(OUT / 'receipt.json', receipt); print(json.dumps(receipt, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_cleanup_publication', 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for p in reversed(suspended):
            if p.is_running(): p.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__': main()
