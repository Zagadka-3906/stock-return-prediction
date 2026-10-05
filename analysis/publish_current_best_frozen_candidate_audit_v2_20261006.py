"""Publish actual controller wiring and observed complete native scope progress on main."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'current_best_frozen_candidate_audit_20261006'
OUT = A / 'current_best_frozen_candidate_audit_github_v2_20261006'
PREFIX = Path('validation_sync/current_best_frozen_candidate_audit_20261006')


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
    assert proof['status'] == 'passed_actual_current_best_closed_candidate_frozen_bytes_audit'
    for filename, digest in proof['input_sha256'].items():
        assert sha(Path(filename)) == digest
    terminal = {'status': 'passed'}
    sources = [Path(__file__), A / 'audit_current_best_frozen_candidate_20261006.py',
        A / 'current_best_frozen_candidate.json', ROOT / 'active_release.json',
        ROOT / 'results/optimization_20261003_r65.json',
        A / 'optimization_20261003_r65/calibrated_csv_official.json']
    sources += sorted(SOURCE.glob('*.json'))
    sources += [A / 'publish_current_best_frozen_candidate_audit_20261006.py',
        A / 'current_best_frozen_candidate_audit_github_20261006/failure.json']
    candidate = Path(proof['candidate_submission']).parent
    sources += [candidate / name for name in ('manifest.json', 'selection.json', 'verification.json',
        'frozen_before_model_inference.json', 'return_mapping.json', 'market_regime_mapping.json')]
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
            'actual_current_best_closed_candidate_frozen_bytes_audit_passed': True,
            'entire_optimization_pending_required_rounds': proof['pending_required_rounds'],
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# 当前已完成验证的最高分冻结候选\n\n'
            '当前最高分来自第65轮172条完整方案评分中的胜者，2020—2024连续向前官方综合分'
            '为0.4510081068915626。第66、81、82轮保留相同最高分。'
            '原始候选在未来X推理之前已冻结，本次检查176个冻结输入、39份候选文件的实际字节、'
            '现有完整5635800行收益映射CSV官方记录及严格完整轮次合格证据。\n\n'
            '候选提交覆盖1599600行、344日、4650股票，原有完整自包含模型重载、'
            '全流程回放、实际CSV逐字节回放、80日前缀和因果控制通过且证据保持一致。'
            '本次未再次推理、重新拟合或读取测试标签，未生成新官方分数。\n\n'
            '本地analysis/current_best_frozen_candidate.json现在明确指向该已核验候选。'
            '历史正式交付仍为0.4459160901521865版本，旧报告和正式交付指针保留。'
            '仍有26轮尚未完成完整科学验证，当前最高分候选不代表优化目标已结束；'
            '之后以更高的完整训练期官方分及全部检查通过的方案更新。'
            '所有验证年份曾被反复查看，累积选择偏差仍然存在。\n'
        ).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验第65轮当前最高分冻结候选176输入39文件并保留未完成范围', timeout=180)
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
