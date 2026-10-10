"""Publish actual snapshot recovery and the live additive-handoff recovery waiter."""
from pathlib import Path
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

OUT = A / 'round95_snapshot_joint97_recovery_github_20261006'
PREFIX = Path('validation_sync/round95_snapshot_joint97_recovery_20261006')


def main():
    recovery = A / 'interrupted_round95_lossless_snapshot_recovery_20261006'
    proof = read(recovery / 'verification.json')
    assert proof['status'] == 'passed_original_exact_full10570_report_serializer_after_preserving_interrupted_gzip'
    for path, digest in proof['input_sha256'].items(): assert sha(path) == digest, path
    actual = read(A / 'joint97_handoff_waiter_actual_recovery_v2_20261006.json')
    assert owned(actual['actual_waiter']) and owned(actual['preserved_scientific_worker'])
    receipt = read(A / 'github_validation_sync_main_20261005/round95_receipt.json')
    assert receipt['status'] == 'pushed_and_remote_head_verified' and receipt['scored_records'] == 124
    assert receipt['connected_records'] == 10570
    assert not OUT.exists()
    OUT.mkdir()
    sources = [Path(__file__), A / 'recover_interrupted_round95_lossless_snapshot_20261006.py',
        A / 'recover_joint97_handoff_sources_v2_20261006.py',
        A / 'handoff_joint_goss_round97_full_execution_v2_20261006.py',
        A / 'wait_joint_goss_round97_idle_handoff_v2_20261006.py',
        A / 'joint97_handoff_source_recovery_v2_20261006.json',
        A / 'joint97_handoff_waiter_actual_recovery_v2_20261006.json',
        A / 'joint_goss_round97_actual_handoff_20261006/failure.json',
        A / 'joint_goss_round97_idle_handoff_waiter_20261006/failure.json',
        A / 'github_validation_sync_main_20261005/round95_receipt.json',
        Path(proof['preserved_interrupted_file']), *recovery.glob('*.json'),
        *(A / 'service_owned_workflows_20261006/joint97_idle_handoff_waiter_v2').glob('*.json'),
        *(A / 'joint_goss_round97_idle_handoff_waiter_v2_20261006').glob('*.json')]
    sync = helpers.sync
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for path in dict.fromkeys(sources):
        data = path.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), path
        target = path.relative_to(ROOT) if path.parent == A and path.suffix == '.py' else PREFIX / path.relative_to(ROOT)
        targets[target.as_posix()] = data
        files[path.relative_to(ROOT).as_posix()] = {'published_path': target.as_posix(),
            'raw_sha256': hashlib.sha256(data).hexdigest()}
    row = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    root, worker = helpers.owned_pair(row['pid'], Path(row['script']), row['script_args'])
    suspended = []
    restore = install()
    try:
        for _ in range(180):
            for process in (worker, root): process.suspend(); suspended.append(process)
            busy = [p for p in root.children(recursive=True)
                if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy: break
            for process in reversed(suspended): process.resume()
            suspended = []
            time.sleep(1)
        else: raise RuntimeError('Main7 still owns an active publication')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': proof['status'], 'previous_main': previous, 'at_local': sync.now(), 'files': files,
            'actual_round95_main_commit': receipt['commit'], 'new_quality_scores': 0,
            'actual_joint97_handoff_recovery_still_waiting_for_R96': True,
            'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 第95轮完整榜中断压缩恢复与第97轮后台接入恢复\n\n'
            '旧main6在本进程内压缩第95轮完整榜时被替换，子进程为空并不代表发布器空闲。'
            '孤立gzip确实缺少流结束标记，原失败与残片原样保留。恢复程序核实main7的实际原休眠'
            '调用栈，暂停前后均空闲，随后执行未改动的原完整序列化程序，解压字节SHA与原10570条'
            '完整榜SHA严格相同。main7恢复后实际发布第95轮124项与全部QA，1894个原始Git文件块'
            '已核验，main回执随附。没有改评分、预测、原排名或模型。\n\n'
            '第一次增量接入在main7未进入成功同步循环时失败，旧队列和观察器恢复，第96轮已自然'
            '启动。新恢复等待程序实际无窗口独立运行，等待原第96轮子进程树自然关闭后才接入。'
            '复用已经有效的main7及其锁，不关闭或替换发布器。原队列10全部25条路线与第67—96轮'
            '范围不变，仍只增加预先固定的第97轮151项；原分支、官方评分、完整因果及原完整QA均保留。'
            '新源码校验与实际PID/创建时间核验随附，尚不证明接入或第97轮评分已完成。\n\n'
            '新增模型训练0、选模分数0；没有停止或重启科学进程，没有读取测试标签，临时目录D盘，'
            '仅main发布。原失败记录与恢复后的真实结果分开保留。\n'
        ).encode('utf-8')
        for name, data in targets.items(): sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50): sync.git('add', '-f', '--', *selected[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '恢复第95轮中断完整榜压缩并核验实际第97轮复用发布器接入等待', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_R95_snapshot_recovery_and_joint97_waiter_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(hashes),
            'new_quality_scores': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
        print(json.dumps(read(OUT / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as exc:
        create(OUT / 'failure.json', {'status': 'failed_preserved_snapshot_and_handoff_recovery_publication',
            'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running(): process.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__': main()
