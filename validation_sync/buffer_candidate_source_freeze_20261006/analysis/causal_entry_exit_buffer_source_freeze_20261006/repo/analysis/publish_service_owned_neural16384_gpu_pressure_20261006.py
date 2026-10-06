"""Publish actual current service-owned full-fit GPU resource observations."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'service_owned_neural16384_gpu_pressure_20261006'
SERVICE = A / 'service_owned_workflows_20261006/service_owned_neural16384_gpu_pressure'
OUT = A / 'service_owned_neural16384_gpu_pressure_github_20261006'
PREFIX = Path('validation_sync/service_owned_neural16384_gpu_pressure_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    assert not OUT.exists()
    OUT.mkdir()
    while not (SERVICE / 'service_execution.json').exists():
        if (SERVICE / 'native_launch.json').exists():
            assert owned(sync.read(SERVICE / 'native_launch.json')), 'Actual controls are missing without a terminal record.'
        time.sleep(10)
    terminal = sync.read(SERVICE / 'service_execution.json')
    row = sync.read(SERVICE / 'native_launch.json')
    while owned(row):
        time.sleep(.2)
    if terminal['status'] == 'passed':
        proof = sync.read(SOURCE / 'verification.json')
        assert proof['status'] == 'passed_actual_current_owned_full_fit_and_GPU_pressure_observations'
        assert proof['actual_observation_seconds'] >= 30
        assert proof['actual_process_CPU_seconds_increase'] > 0
        assert proof['new_model_fits'] == proof['new_quality_scores'] == 0
        assert proof['no_training_interruption_or_restart_or_RNG_change']
        assert proof['all_scientific_sources_full_rehash_unchanged']
        assert proof['physical_resource_boundary_established'] is False
        assert proof['test_labels_read'] is False
        for filename, digest in proof['input_sha256'].items():
            assert sha(Path(filename)) == digest
        observations = [sync.read(SOURCE / f'observation_{index}.json') for index in (1, 2)]
        for index, observation in zip((1, 2), observations):
            assert observation['owned_worker_pid'] == proof['owned_worker_pid']
            assert observation['owned_worker_creation_time'] == proof['owned_worker_creation_time']
            for channel in ('stdout', 'stderr'):
                assert sha(SOURCE / f'observation_{index}_{channel}_prefix.log') == observation[f'{channel}_snapshot_sha256']

    else:
        assert (SOURCE / 'failure.json').exists()
    sources = [Path(__file__), A / 'observe_service_owned_neural16384_gpu_pressure_20261006.py']
    sources += sorted(SOURCE.glob('*.json')) + sorted(SOURCE.glob('*.log'))
    sources += sorted(SERVICE.glob('*.json')) + sorted(SERVICE.glob('*.log'))
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(A)
        targets[destination.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {'published_path': destination.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    restore, suspended = install(), []
    try:
        pub = sync.read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
        assert owned(pub)
        root, worker = helpers.owned_pair(pub['pid'], Path(pub['script']), pub['script_args'])
        assert worker.pid == pub['owned_worker_pid'] and worker.create_time() == pub['owned_worker_creation_time']
        for attempt in range(50):
            for process in (worker, root):
                process.suspend()
                suspended.append(process)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(.2)
        else:
            raise RuntimeError('Main publisher still owns an active publication child.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': terminal['status'], 'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_owned_full_fit_resource_observation_status': terminal['status'],
            'all_original_native_fit_andquality_scopes_preserved': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 当前服务托管大网络的实际GPU资源观察\n\n'
            '通过原生进程出生时间、命令行及父子关系核对当前实际完整训练，'
            '间隔至少30秒读取两次Windows逐进程专用及共享GPU内存、设备利用率、'
            'CPU累计时间和当前服务目录内的资源采样，同时保存原生日志的精确前缀。\n\n'
            '观察没有修改训练源码、输入、随机数、32轮预算或模型，'
            '没有重启训练、额外拟合或新增官方分数。'
            '共享GPU内存本身不证明OOM或全局资源边界；'
            '没有从未打印的epoch推断进度、完成时间或五年方案优劣。'
            '全部原定完整年度训练、最终训练、未来推理和质量评分仍须完成。\n'
        ).encode('utf-8')

        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '保存当前大网络完整训练的两次实际GPU资源观察和隐藏子进程证据', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'control_status': terminal['status'],
            'at_local': sync.now(), 'commit': commit, 'raw_git_blobs_verified': len(expected), 'new_quality_scores': 0,
            'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_publication_attempt', 'error': f'{type(error).__name__}: {error}'})
        raise
    finally:
        for process in reversed(suspended):
            if process.is_running():
                process.resume()
        create(OUT / 'actual_hidden_publication_children.json', {'actual_CreateProcess_calls': restore()})


if __name__ == '__main__':
    main()
