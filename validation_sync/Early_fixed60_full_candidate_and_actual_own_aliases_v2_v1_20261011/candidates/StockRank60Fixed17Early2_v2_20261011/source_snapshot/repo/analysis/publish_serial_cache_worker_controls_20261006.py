"""Publish actual serial control launch or execution, with main-only byte checks."""
from pathlib import Path
import gzip
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers


def main(phase):
    assert phase in ('launch', 'execution')
    folder = A / 'root_and_rank_cache_serial_window_20261006'
    worker = A / 'root_and_rank_cache_actual_worker_controls_20261006'
    service = A / 'service_owned_workflows_20261006/root_and_rank_cache_serial_window'
    frozen = read(folder / 'frozen_before_actual_scheduler_reservation.json')
    for path, digest in frozen['input_sha256'].items():
        assert sha(path) == digest, path
    identity = read(service / 'native_launch.json')
    if phase == 'launch':
        assert owned(identity)
        proof = read(folder / 'actual_empty_helper_before_and_after_additional_reservation.json')
        assert proof['only_empty_queue_helper_pair_held']
    else:
        proof = read(folder / 'execution.json') if (folder / 'execution.json').exists() else read(folder / 'failure.json')
        assert not owned(identity), 'Publish final execution only after natural terminal state'
    out = A / f'root_and_rank_cache_worker_{phase}_github_20261006'
    assert not out.exists()
    out.mkdir()
    prefix = Path(f'validation_sync/root_and_rank_cache_worker_{phase}_20261006')
    sources = [Path(__file__), *map(Path, frozen['input_sha256']),
        A / 'exact_rank_cache_official_worker_adapter_20261006.py',
        A / 'parallel_candidate_scoring_one_20261005.py',
        A / 'hidden_windows_child_creation_20261006.py',
        *folder.glob('*.json'), *folder.glob('*.log'),
        *service.glob('*.json'), *service.glob('*.log')]
    if phase == 'execution':
        sources.extend(worker.glob('*.json'))
        sources.extend((A / 'bounded_root_replay_full_controls_20261006').glob('*.json'))
        receipt = A / 'bounded_root_full_controls_v2_execution_github_20261006/receipt.json'
        if receipt.exists():
            sources.append(receipt)
    sync = helpers.sync
    targets = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for path in dict.fromkeys(sources):
        data = path.read_bytes()
        assert not sync.SECRET.search(data), path
        raw_sha = hashlib.sha256(data).hexdigest()
        target = path.relative_to(ROOT) if path.parent == A and path.suffix == '.py' else prefix / path.relative_to(ROOT)
        if len(data) > 5 * 1024**2:
            data = gzip.compress(data, mtime=0)
            target = Path(target.as_posix() + '.gz')
        targets[target.as_posix()] = data
        files[path.relative_to(ROOT).as_posix()] = {'published_path': target.as_posix(),
            'raw_sha256': raw_sha, 'published_sha256': hashlib.sha256(data).hexdigest()}
    main_identity = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    held = []
    restore_children = install()
    try:
        parent, process, idle = suspended_idle(main_identity,
            '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((process, parent))
        targets[(prefix / 'actual_publisher_idle.json').as_posix()] = sync.encoded(idle)
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(prefix / 'manifest.json').as_posix()] = sync.encoded({
            'phase': phase, 'actual_control': proof, 'previous_main': previous,
            'at_local': sync.now(), 'files': files, 'runtime_adopted': False,
            'new_quality_records': 0, 'new_native_fits': 0, 'test_labels_read': False,
            'only_publication_branch': 'main'})
        targets[(prefix / 'README.md').as_posix()] = (
            '# 根缓存与原排序缓存的真实 Windows 评分进程控制\n\n'
            '保持既有完整根缓存测试自然完成；在已核验休眠且子进程树为空的调度器上，'
            '延续空闲槽位预约，串行执行原基线冷/热两次及真实三用途组合配置。'
            '只有完整对照通过且实测暖预测提速时才启动第二项控制；不暂停任何科学进程。'
            '逐次核对5635800行原始预测位、最终收益率CSV字节及八项原官方指标，'
            '记录独立128MiB根载荷上限与原1GiB排序缓存；上限不表示总RSS。\n\n'
            'launch证明实际等待进程、身份和空闲预约，execution保存自然结束后的完整结果或失败。'
            '不新增选模记录或训练，不采用缓存、不读取未来标签。既有151项第97轮及所有原任务保留；'
            '第二项控制自然结束后释放自己的空闲预约。所有后台启动隐藏窗口、数据与模型留在D/E盘。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            f'记录根与排序缓存真实Windows评分进程控制的{phase}', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, hashes) == hashes
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(out / 'receipt.json', {'status': 'pushed_verified_serial_cache_worker_controls_main_only',
            'phase': phase, 'at_local': sync.now(), 'commit': commit,
            'raw_git_blobs_verified': len(hashes), 'runtime_adopted': False,
            'new_quality_records': 0, 'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
        print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    except BaseException as exc:
        create(out / 'failure.json', {'status': 'failed_preserved_serial_cache_worker_publication',
            'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for process in reversed(held):
            if process.is_running():
                process.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore_children()})


if __name__ == '__main__':
    main(sys.argv[1])
