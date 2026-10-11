"""Publish actual rank-cache controls including the unsuccessful 512MiB capacity trial."""
from pathlib import Path
import hashlib
import json
import time

import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'exact_rank_cache_complete_scheme_v2_20261006'
OUT = A / 'exact_daily_rank_execution_controls_github_20261006'
PREFIX = Path('validation_sync/exact_rank_cache_complete_scheme_v2_20261006')


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
    assert proof['status'] == 'passed_actual_full_scheme_original_cold_warm_and_official_CSV_bytes'
    spawn = sync.read(A / 'exact_rank_cache_windows_scoring_initializer_20261006/verification.json')
    assert spawn['status'] == 'passed_actual_Windows_spawn_original_scoring_initializer_full_scheme_bits'
    for filename, digest in proof['input_sha256'].items():
        assert sha(Path(filename)) == digest
    terminal = {'status': 'passed'}
    sources = [Path(__file__), *[A / name for name in (
        'profile_round83_scoring_readonly_20261006.py',
        'exact_daily_rank_memoization_20261006.py',
        'verify_exact_daily_rank_memoization_20261006.py',
        'verify_exact_rank_cache_complete_scheme_20261006.py',
        'verify_exact_rank_cache_complete_scheme_v2_20261006.py',
        'exact_rank_cache_official_worker_adapter_20261006.py',
        'verify_exact_rank_cache_windows_scoring_initializer_20261006.py',
        'run_recovery_qualified_workflow_with_exact_rank_cache_20261006.py')]]
    for name in ('round83_readonly_scoring_bottleneck_20261006',
                 'exact_daily_rank_memoization_preflight_20261006',
                 'exact_rank_cache_complete_scheme_20261006',
                 'exact_rank_cache_complete_scheme_v2_20261006',
                 'exact_rank_cache_windows_scoring_initializer_20261006'):
        folder = A / name
        sources += sorted(folder.glob('*.json')) + sorted(folder.glob('*.txt')) + sorted(folder.glob('*.log'))
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
            'actual_complete_rank_cache_replay_and_identical_scored_CSV_verified': True,
            'unsuccessful_512MiB_capacity_trial_preserved': True,
            'production_adoption_still_pending': True,
            'original198_and_additional262_official_quality_still_pending': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        measurements = {row['mode']: row for row in proof['measurements']}
        old = sync.read(A / 'exact_rank_cache_complete_scheme_20261006/verification.json')
        lines = [
            '# 完整验证方案的按日排名复用：真实计算与字节核验', '',
            '第83轮评分子进程的三次只读采样都位于按日排名；这支持测试复用，但不单独证明全流程瓶颈。', '',
            '缓存使用全部值、有效掩码、日期、形状及dtype的SHA256；失配调用原函数。缓存按字节限制并返回独立副本。', '',
            '五组真实5635800行/1212日信号逐位相同，包含复制输入、返回值修改、阈值、并列、dtype及未来尾部变动控制。', '',
            '实际R65完整方案在独立子进程中分别以原函数、冷缓存和热缓存重算。三者所有Float64位及构造统计相同。',
            '沿用原先逐年仅历史成熟标签拟合的映射，生成的全部评分CSV字节与原始官方评分CSV完全相同。',
            '没有新增质量分数；本次没有再次运行官方评价器，引用的是同一已验证CSV的原有官方结果。', '',
            '512MiB试验只能容纳11组结果，实际23次调用在热运行仍全部失配，没有加速，因此保留记录并扩大容量另测。',
            '以下时间仅表示这一真实重复方案，不外推所有后续方案或官方评分、训练、发布的整体速度。', '',
            '| 缓存上限 | 原计算秒 | 冷运行秒 | 热运行秒 |', '| --- | ---: | ---: | ---: |']
        for label, record in (('512MiB', old), ('1GiB', proof)):
            m = {row['mode']: row['prediction_seconds'] for row in record['measurements']}
            lines.append(f"| {label} | {m['original']:.4f} | {m['memoized_cold']:.4f} | {m['memoized_warm']:.4f} |")
        lines += ['', '另外实测Windows multiprocessing spawn，调用原单评分器的完整初始化，在同一私有评分子进程内冷、热重算全部5635800行。两次预测逐位相同，热运行23组排名全部命中。',
                  '本次尚未替换任何生产评分工作流，第83轮与宽网络继续原有执行。后续接入仍需冻结新执行来源与队列交接。',
                  '模型训练0，质量分数0，不读取测试标签，不写重复模型或全量预测副本。全部验证及未获得加速的结果均保留并只上传main。', '']
        targets[(PREFIX / 'README.md').as_posix()] = '\n'.join(lines).encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验完整验证方案排名复用并保留512MiB未加速及1GiB真实控制', timeout=180)
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
