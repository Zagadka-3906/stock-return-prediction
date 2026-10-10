"""Publish actual controller wiring and observed complete native scope progress on main."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'neural16384_actual_training_progress_diagnostics_20261006'
OUT = A / 'neural16384_actual_training_progress_diagnostics_github_20261006'
PREFIX = Path('validation_sync/neural16384_actual_training_progress_diagnostics_20261006')


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
    proof = sync.read(SOURCE / 'verification.json')
    assert proof['status'] == 'passed_actual_nonblocking_owned_training_loop_observations'
    assert owned(proof['actual_owned_trainer'])
    frozen = sync.read(SOURCE / 'frozen_before_followup_sampling.json')
    for filename, digest in frozen['input_sha256'].items():
        assert sha(Path(filename)) == digest
    terminal = {'status': 'passed'}
    sources = [Path(__file__), *[A / name for name in (
        'prepare_readonly_pyspy_diagnostics_20261006.py',
        'sample_readonly_neural16384_stack_20261006.py',
        'verify_readonly_neural16384_training_progress_20261006.py')]]
    sources += sorted(SOURCE.glob('*.json')) + sorted(SOURCE.glob('*.txt'))
    folder = A / 'neural16384_readonly_stack_diagnostics_20261006'
    sources += sorted(folder.glob('*.json')) + sorted(folder.glob('*.txt'))
    sources += [ROOT / 'tools/readonly_pyspy_diagnostics_20261006/receipt.json']
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(ROOT)
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
            'actual_controller_wiring_control_status': terminal['status'],
            'actual_training_epoch_and_batch_positions_observed_readonly': True,
            'original198_and_additional262_official_quality_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 宽16384网络：实际训练位置的只读观察\n\n'
            '原训练日志只在第1个及每4个epoch结束时输出，不能依据最后一条epoch1日志认定训练停滞。'
            '对已核对PID、创建时间和命令身份的原训练进程执行四次只读非暂停采样，'
            '观察到2021窗口已经完成3个epoch，当前位于第4/32个epoch；'
            '批次位置从第53个推进到第55个。后续20秒观察位于反向传播，进程CPU时间增加20.375秒。\n\n'
            '本次只读取当前Python栈和整数循环变量，没有在目标进程执行代码、'
            '修改参数、暂停、重启或减少样本。训练源码和诊断工具字节核对一致。'
            '该窗口的32个epoch、完整模型、后续窗口和全部推理仍待完成；'
            '局部训练损失不是官方分数，不参与采用判断，也不计新增完整模型。\n\n'
            '使用官方PyPI py-spy0.4.2 Windows便携二进制，下载包SHA256与PyPI记录匹配，'
            '保存在D盘，没有安装或改动Python环境。可按工具receipt中的固定下载URL及SHA复现工具获取。'
            '非暂停采样不是原子读取，记录核对epoch、损失列表长度及批次范围的一致性，'
            '短时间内相同批次不能单独证明停滞；本次多次观察实际出现了位置推进。'
            '工具机制说明见https://github.com/benfred/py-spy#how-can-i-avoid-pausing-the-python-program。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '只读核验宽16384网络实际第4轮训练及批次推进并保留完整原始采样', timeout=180)
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
