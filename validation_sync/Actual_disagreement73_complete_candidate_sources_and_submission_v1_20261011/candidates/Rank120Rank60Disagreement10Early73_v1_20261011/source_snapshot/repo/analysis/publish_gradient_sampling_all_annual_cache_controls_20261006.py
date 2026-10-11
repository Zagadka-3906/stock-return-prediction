"""Publish all-five full annual cache controls and the actually dispatched original full-scope workflow."""
from pathlib import Path
import hashlib
import json
import time

import psutil
import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'gradient_sampling_all_annual_cache_controls_20261006'
OUT = A / 'gradient_sampling_all_annual_cache_controls_github_20261006'
PREFIX = Path('validation_sync/gradient_sampling_all_annual_cache_controls_20261006')


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
    assert proof['status'] == 'passed_all5_full_original_GOSS_annual_preprocessing_targets_and_maturity'
    assert len(proof['checks']) == 5 and proof['actual_native_fits'] == 0
    assert proof['new_cache_files_written'] == proof['actual_annual_fits'] == proof['new_quality_scores'] == 0
    for filename, digest in proof['input_sha256'].items():
        assert sha(filename) == digest
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_workflow'
    launch = sync.read(service / 'native_launch.json')
    assert owned(launch)
    assert launch['actual_native_console_handle'] == 0 and not launch['independent_launch_root_in_any_job']
    protocol = sync.read(A / 'gradient_sampling_memmap_capacity_20261006/protocol.json')
    assert protocol['expected_actual_full_final_fits'] == 6
    resources = sync.read(SOURCE / 'resource_summary.json')
    assert resources['status'] == 'passed' and not resources['observation_errors']
    actual_completed = sorted(p.parent.name for p in (A / 'gradient_sampling_memmap_capacity_20261006').glob('*/future_verification.json'))
    create(OUT / 'actual_launch_observation.json', {
        'at_local': sync.now(), 'actual_owned_native_launch': launch,
        'actual_complete_largest_native_and_future_models_at_observation': actual_completed,
        'actual_host_available_bytes_at_observation': psutil.virtual_memory().available,
        'largest_full_scope_remains_pending': len(actual_completed) < 6,
        'completed_backend_control_is_not_an_official_quality_result': True,
        'original30_annual_and262_quality_records_still_required': True,
        'new_quality_scores': 0, 'test_labels_read': False})
    sources = [Path(__file__), *[A / name for name in (
        'gradient_sampling_exact_memmap_20261006.py', 'verify_gradient_sampling_exact_memmap_20261006.py',
        'verify_gradient_sampling_all_annual_cache_20261006.py', 'train_gradient_sampling_memmap_bank_20261006.py',
        'run_gradient_sampling_memmap_full_workflow_20261006.py', 'verify_gradient_sampling_memmap_full_future_20261006.py',
        'prepare_gradient_sampling_memmap_full_workflow_20261006.py', 'verify_gradient_sampling_memmap_waiting_workflow_20261006.py',
        'independent_gradient_sampling_native_codec_20261006.py', 'watch_owned_scheduler_fit_lease_20261006.py',
        'owned_scheduler_native_fit_hold_20261006.py', 'verify_full2025_gradient_sampling_memmap_capacity_20261006.py',
        'prepare_gradient_sampling_memmap_capacity_20261006.py')]]
    for folder in (SOURCE, service, A / 'gradient_sampling_memmap_capacity_20261006', A / 'gradient_sampling_memmap_waiting_workflow_controls_20261006', OUT):
        for pattern in ('*.json', '*.jsonl', '*.txt', '*.log'):
            sources += sorted(folder.rglob(pattern))
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
            'status': 'passed_backend_equivalence_controls_actual_full_capacity_pending',
            'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_control_native_fits': 0, 'new_cache_files_written': 0,
            'actual_bank_annual_fits': 0, 'original30_annual_and262_quality_records_still_required': True,
            'actual_completed_full_capacity_models_at_observation': actual_completed,
            'capacity_live_logs_are_time_bounded_snapshots_not_terminal_evidence': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = '# GOSS五年完整缓存核验及完整验证流程接入\n\n2020—2024年五个成熟训练窗口分别为1,694,259、2,594,048、3,568,878、4,597,785、5,659,954行，全部63特征。\n逐窗口按原GOSS算法重新计算完整列均值、尺度和所有标准化块，逐位及SHA256均与已有缓存一致；两个目标的全部标签、矩阵、股票日期键和成熟边界均与原训练信息一致。\n缓存仅只读复用，新增缓存、模型拟合及正式质量记录均为0；69次实际资源观测错误0。\n\n完整GOSS流程已按无窗口方式实际启动并核验存活、源码绑定及原依赖范围。它先等待六个最大窗口的实际6,754,006行、300轮模型及完整1,599,600行未来输入检查全部成功，再冻结并执行原30个年度模型。\n后续每个年度模型执行原未来标签扰动控制、全年度重载、独立推理、真实80日及37日冷启动检查；最终再次核对六个原生最终模型的完整未来输入。\n原六套参数、样本、目标和迭代数保持一致，不因内存改变模型；六个最终模型复用实际拟合证据，文件复制不计新增拟合。\n\n12 GiB最大窗口启动要求仍是调度策略，不是物理资源边界；目前最大窗口实际进程仍在等待可用内存。\n年度流程的启动余量将来自六个最大窗口的实际资源观测，并增加2 GiB余量且至少6 GiB，不依据质量分数选择资源条件。\n原GPU训练、质量验证及发布进程继续运行。原第75/76轮父方案74/75、124+138共262个正式质量方案均保留；正式选模、冻结、因果检查、候选推理和完整榜更新仍待完成。\n\n新流程尚未向旧质量模型路径暴露模型或通过标记；旧待办保留，完整原生范围实际成功后另行核验接管，避免制造原执行成功记录。\n本次只证明五年缓存与实际等待流程接入，不声称30+6模型或262方案完成，不读取TestY，不宣布全局优化边界。全部代码、成功核验和实际启动快照只上传main。\n'.encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '核验GOSS五个完整年度缓存并实际接入30年模型和6最终模型验证流程', timeout=180)
        commit = sync.git('rev-parse', 'HEAD')
        expected = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
        assert helpers.blob_hashes(commit, expected) == expected
        sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
        helpers.verify_main(commit)
        helpers.watcher.advance_source_index(commit)
        create(OUT / 'receipt.json', {'status': 'pushed_actual_controls_main_only', 'at_local': sync.now(),
            'commit': commit, 'raw_git_blobs_verified': len(expected), 'new_quality_scores': 0,
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
