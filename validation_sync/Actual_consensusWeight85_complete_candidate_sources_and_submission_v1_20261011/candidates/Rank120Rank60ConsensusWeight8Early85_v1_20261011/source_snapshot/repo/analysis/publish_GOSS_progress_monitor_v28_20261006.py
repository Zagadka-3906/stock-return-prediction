"""Publish actual observer controls and preserved preparation failures on main."""
from pathlib import Path
import hashlib
import json
import time
import psutil
import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
OUT = A / 'GOSS_progress_monitor_github_v28_20261006'
PREFIX = Path('validation_sync/GOSS_progress_monitor_verified_v28_20261006')


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    proof = sync.read(A / 'GOSS_progress_monitor_verified_v28_20261006/verification.json')
    assert proof['status'] == 'passed_two_actual_observer28_complete_generations_GOSS_counts_and_original_scope'
    assert owned(proof['actual_owned_observer']) and len(proof['actual_complete_generation_ids']) == 2
    assert proof['actual_GOSS_final_fits'] == 6 and proof['excluded_duplicate_model_records'] >= 6
    for path, digest in proof['input_sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
    assert not OUT.exists()
    OUT.mkdir()
    sources = [Path(__file__), *[A / name for name in (
        'monitor_actual_optimization_progress_v26_20261006.py', 'monitor_actual_optimization_progress_v27_20261006.py',
        'monitor_actual_optimization_progress_v28_20261006.py', 'handoff_GOSS_progress_monitor_v26_20261006.py',
        'handoff_GOSS_progress_monitor_v27_20261006.py', 'handoff_GOSS_progress_monitor_v28_20261006.py',
        'verify_GOSS_progress_monitor_v26_20261006.py', 'verify_GOSS_progress_monitor_v27_20261006.py',
        'verify_GOSS_progress_monitor_v28_20261006.py', 'GOSS_progress_monitor27_source_generation_20261006.json',
        'GOSS_progress_monitor28_source_generation_20261006.json', 'GOSS_monitor28_unfrozen_preparation_correction_20261006.json')]]
    for name in ('GOSS_progress_monitor_handoff_v26_20261006', 'GOSS_progress_monitor_handoff_v27_20261006',
                 'GOSS_progress_monitor_handoff_v28_20261006', 'GOSS_progress_monitor_verified_v28_20261006',
                 'service_owned_workflows_20261006/progress_monitor_v26', 'service_owned_workflows_20261006/progress_monitor_v28'):
        folder = A / name
        sources += sorted(folder.glob('*.json')) + sorted(folder.glob('*.jsonl'))
        if name.endswith('v26'):
            sources += sorted(folder.glob('*.log'))
    targets = {(PREFIX / '.gitattributes').as_posix(): b'* -text\n'}
    files = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not sync.SECRET.search(data)
        destination = source.relative_to(ROOT) if source.parent == A and source.suffix == '.py' else PREFIX / source.relative_to(ROOT)
        targets[destination.as_posix()] = data
        files[source.relative_to(ROOT).as_posix()] = {
            'published_path': destination.as_posix(), 'raw_sha256': hashlib.sha256(data).hexdigest()}
    restore, suspended = install(), []
    try:
        pub = sync.read(A / 'service_owned_workflows_20261006/main_publisher_v5/native_launch.json')
        assert owned(pub)
        root, worker = helpers.owned_pair(pub['pid'], Path(pub['script']), pub['script_args'])
        assert worker.pid == pub['owned_worker_pid'] and worker.create_time() == pub['owned_worker_creation_time']
        for attempt in range(300):
            for process in (worker, root):
                process.suspend()
                suspended.append(process)
            busy = [p for p in root.children(recursive=True) if p.pid != worker.pid and p.name().lower() != 'conhost.exe']
            if not busy:
                break
            for process in reversed(suspended):
                process.resume()
            suspended.clear()
            time.sleep(1.)
        else:
            raise RuntimeError('Main publisher still owns an active publication child.')
        previous = sync.git('rev-parse', 'HEAD')
        helpers.verify_main(previous)
        assert not sync.git('status', '--porcelain')
        targets[(PREFIX / 'manifest.json').as_posix()] = sync.encoded({
            'status': proof['status'], 'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'actual_complete_generation_ids': proof['actual_complete_generation_ids'],
            'actual_GOSS_annual_fits_at_verified_snapshot': proof['actual_GOSS_annual_fits'],
            'actual_GOSS_final_fits': 6, 'copies_excluded': proof['excluded_duplicate_model_records'],
            'all_original_scientific_scope_and_current_owned_queue_retained': True,
            'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = (
            '# GOSS实际训练计数及完整进度采集验证\n\n'
            '原进度采集只读取旧GOSS目录；新版本逐模型核对配置、300轮、完整成熟训练元数据、模型与全年度预测SHA，并从实际内存映射银行及最大窗口原生记录合并计数。相同模型年份和字节仅计一次，复制及小样本控制不计新拟合。实际验证快照数量见清单；最高官方质量分、冻结候选和未完成评分不由训练计数替代。\n\n'
            '从当前共享队列状态及PID、出生时间、命令行识别实际调度器，支持原队列接管后继续观察。三份公共进度文件保持同一完整生成版本，实际观察了两轮完整更新，原262个GOSS、198个分位数、262个分布视图方案及其父方案保留。\n\n'
            '此前60秒首次更新观察不足导致准备器撤回新观察器，旧观察器恢复；后续版本的检查常量替换失败和已退休等待服务引用失败均保留。最终版以真实进程句柄及完整更新作为依据；科学训练与评分未停止。仅GOSS模型变化且其他原生模型清单完全相同时，使用单独完整核验的GOSS采集器，避免重复全历史成本扫描。所有成功与失败来源、记录和源代码同步main。\n\n'
            '本次新增训练拟合及质量记录均为0，不读取TestY，不宣布资源或全局优化边界。项目文件保留D，未新增C项目缓存。\n').encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验实际GOSS训练计数去重及完整进度更新并保留全部准备失败', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'at_local': sync.now(),
            'commit': commit, 'raw_git_blobs_verified': len(expected), 'control_status': 'passed', 'new_quality_scores': 0,
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
