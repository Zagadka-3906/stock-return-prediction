"""Publish the actual pre-inference source freeze and live package admission evidence."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
from seal_buffer_candidate_source_package_20261006 import checked_sources
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers

OUT = A / 'buffer_candidate_source_freeze_github_20261006'
PREFIX = Path('validation_sync/buffer_candidate_source_freeze_20261006')


def main():
    sources = checked_sources()
    assert not OUT.exists()
    OUT.mkdir()
    package_waiter = read(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_package_waiter/native_launch.json')
    assert owned(package_waiter), 'This launch publication requires an actual live package waiter'
    assert package_waiter['actual_native_console_handle'] == 0 and not package_waiter['independent_launch_root_in_any_job']
    sync = helpers.sync
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    paths = [Path(__file__), A / 'freeze_buffer_candidate_source_bundle_20261006.py',
        A / 'seal_buffer_candidate_source_package_20261006.py',
        A / 'replay_sealed_buffer_candidate_20261006.py', A / 'wait_and_seal_buffer_candidate_20261006.py',
        *(A / 'causal_entry_exit_buffer_source_freeze_20261006').glob('*.json'),
        *(A / 'service_owned_workflows_20261006/causal_entry_exit_buffer_package_waiter').glob('*.json'),
        *(A / 'causal_entry_exit_buffer_package_waiter_20261006').glob('*.json')]
    paths += [A / 'causal_entry_exit_buffer_source_freeze_20261006/repo' / relative
        for relative in sources['files']]
    bindings = {}
    for path in dict.fromkeys(paths):
        data = path.read_bytes()
        assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data), path
        target = (PREFIX / path.relative_to(ROOT)).as_posix()
        targets[target] = data
        bindings[path.relative_to(ROOT).as_posix()] = {'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data), 'published_path': target}
    publisher = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    suspended = []
    restore = install()
    try:
        parent, worker, idle_proof = suspended_idle(publisher, '    main (watch_validations_main_v7_20261006.py:71)')
        suspended.extend((worker, parent))
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': 'actual_pre_inference_source_freeze_and_live_package_waiter_verified',
            'previous_main': previous, 'at_local': sync.now(), 'files': bindings,
            'source_files_frozen_before_actual_inference': len(sources['files']),
            'all_source_bytes_rechecked': True, 'actual_live_package_waiter': package_waiter,
            'publisher_idle_stack_verified_before_and_after_hold': idle_proof,
            'actual_full_candidate_and_ranking_qualification_pending': True,
            'new_quality_scores': 0, 'only_publication_branch': 'main', 'test_labels_read': False})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 成员缓冲候选的实际推理前源码冻结\n\n'
            '在原推理等待程序仍因内存准入等待、没有任何候选输出时，实际复制并逐文件核验'
            '了1930份本地Python源码、Python及依赖库版本。包含本次缓冲实现、完整模型推理图、'
            '模型编解码器、历史配方模块和来源封存程序。快照共约12.7MB，不包含模型、数据或缓存副本。\n\n'
            '真正运行的无窗口后台封存程序只会在原候选推理进程自然退出且实际执行记录为passed后'
            '封存完整输出；验证模型字节、源文件、实际模型重载、独立80日前缀及候选CSV。'
            '目前的源码冻结及等待记录不证明推理完成，不增加质量评分或完整榜资格。'
            '新的重放入口要求一个此前不存在的D/E盘输出目录，从已封存模型字节执行完整推理，'
            '不能用已存在verification文件或最终预测文件代替实际重载。\n\n'
            '原先16项训练内部官方分数及候选选择保持不变；未读取测试标签。Git写入前对实际'
            'main发布程序同时核验暂停前后均在原始空闲sleep栈，并确认没有子任务；科学训练'
            '及第96轮不会暂停或重启。完整榜登记、完整六视图检查及完成后的候选发布仍待执行。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset+50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '冻结成员缓冲候选1930份源码并记录实际无窗口封存等待', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual1930_source_freeze_and_live_package_waiter_main_only',
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(hashes),
            'source_files': len(sources['files']), 'new_quality_scores': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
        print(json.dumps(read(OUT / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_buffer_source_freeze_publication',
            'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for p in reversed(suspended):
            if p.is_running():
                p.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'events': restore()})


if __name__ == '__main__':
    main()
