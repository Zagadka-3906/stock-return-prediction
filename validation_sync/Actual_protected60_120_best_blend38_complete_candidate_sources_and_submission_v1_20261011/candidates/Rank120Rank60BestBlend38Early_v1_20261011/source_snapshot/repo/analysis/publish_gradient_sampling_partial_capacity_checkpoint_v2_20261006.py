"""Publish actual completed native checkpoints and authorized unused pilot buffer cleanup."""
from pathlib import Path
import hashlib
import json
import time

import psutil
import publish_classifier_consensus_workflows_20261006 as helpers
from run_dependency_queue_v3_20261006 import owned
from hidden_windows_child_creation_20261006 import install

ROOT, A, sync = helpers.ROOT, helpers.A, helpers.sync
SOURCE = A / 'gradient_sampling_memmap_capacity_v3_20261006'
OUT = A / 'gradient_sampling_partial_capacity_checkpoint_v2_github_20261006'
PREFIX = Path('validation_sync/gradient_sampling_partial_capacity_checkpoint_v2_20261006')


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
    service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v3'
    launch = sync.read(service / 'native_launch.json')
    assert sync.read(service / "service_execution.json")["status"] == "passed" and not owned(launch)
    assert launch['actual_native_console_handle'] == 0 and not launch['independent_launch_root_in_any_job']
    completed = sorted(SOURCE.glob('*/future_verification.json'))
    assert len(completed) >= 3
    actual_completed = [p.parent.name for p in completed]
    sources = [Path(__file__), SOURCE / 'protocol.json', *[A / name for name in (
        'gradient_sampling_exact_memmap_20261006.py', 'verify_full2025_gradient_sampling_memmap_capacity_v3_20261006.py',
        'independent_gradient_sampling_native_codec_20261006.py', 'owned_scheduler_native_fit_hold_v2_20261006.py',
        'watch_owned_scheduler_fit_lease_20261006.py', 'publish_full2025_gradient_sampling_memmap_capacity_v3_20261006.py',
        'prepare_gradient_sampling_capacity_v3_publication_20261006.py',
        'prepare_gradient_sampling_capacity_v3_publication_v2_20261006.py',
        'gradient_sampling_pilot_cache_cleanup_20261006.json')]]
    checks = []
    for path in completed:
        check = sync.read(path)
        folder = path.parent
        info = sync.read(folder / 'info_2025.json')
        assert check['status'] == 'passed' and info['status'] == 'passed_actual_full_native_fit'
        assert info['actual_native_iterations'] == 300 and info['training_meta']['rows'] == 6754006
        assert sha(folder / 'model_2025.joblib') == info['model_sha256'] == check['model_sha256']
        assert sha(folder / 'future_raw.parquet') == check['future_parquet_sha256']
        assert sha(folder / 'independent_native_codec.py') == check['independent_codec_sha256']
        assert check['actual_full_future_shape'] == [1599600, 344, 4650]
        assert check['full_saved_reload_independent_codec_and_cold80_37day_predictions_bit_identical']
        hold = SOURCE / ('scheduler_fit_hold_' + check['model'])
        assert sync.read(hold / 'released.json')['scientific_workers_touched'] == 0
        assert sync.read(hold / 'independent_guard_service/service_execution.json')['status'] == 'passed'
        sources += [path, folder / 'info_2025.json', folder / 'independent_native_codec.py']
        sources += sorted(hold.rglob('*.json'))
        checks.append(check)
    cleanup = sync.read(A / 'gradient_sampling_pilot_cache_cleanup_20261006.json')
    assert cleanup['deleted_files'] == 6 and cleanup['freed_bytes'] == 49545216
    assert all(not Path(row['path']).exists() for row in cleanup['actual_cache_rows'])
    publication = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_capacity_v3_publication'
    receipt = sync.read(A / 'gradient_sampling_memmap_capacity_v3_github_20261006/receipt.json')
    assert receipt['status'] == 'pushed_actual_controls_main_only' and receipt['control_status'] == 'passed'
    bank_service = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_workflow_v3'
    assert owned(sync.read(bank_service / 'native_launch.json'))
    annual_count = len(list((A / 'gradient_sampling_memmap_complete_bank_v3_20261006').glob('*/info_202[0-4].json')))
    sources += [A / 'publish_gradient_sampling_partial_capacity_checkpoint_20261006.py',
        A / 'gradient_sampling_partial_capacity_checkpoint_github_20261006/failure.json',
        A / 'prepare_gradient_sampling_complete_bank_v3_publication_20261006.py',
        A / 'publish_gradient_sampling_memmap_complete_bank_v3_20261006.py',
        A / 'gradient_sampling_memmap_capacity_v3_github_20261006/receipt.json']
    sources += sorted((A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_bank_v3_publication').glob('*.json'))
    sources += sorted(service.glob('*.json')) + sorted(publication.glob('*.json'))
    create(OUT / 'actual_launch_observation.json', {'status': 'passed_completed_model_checkpoint_with_remaining_full_scope_live',
        'at_local': sync.now(), 'archived_successful_native_launch': launch, 'checks': checks,
        'actual_completed_largest_native_and_future_models': actual_completed,
        'remaining_largest_native_models': 6 - len(completed), 'actual_bank_annual_fits_at_observation': annual_count,
        'original30_annual_and262_quality_records_still_required': True,
        'unused_pilot_buffers_deleted_after_published_proof_bytes': cleanup['freed_bytes'],
        'completed_full_capacity_main_receipt': receipt,
        'new_quality_scores': 0, 'test_labels_read': False, 'physical_resource_boundary_established': False})
    sources += [OUT / 'actual_launch_observation.json']
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
            'status': 'passed_completed_model_checkpoint_remaining_full_scope_live',
            'at_local': sync.now(), 'files': files, 'previous_main': previous,
            'entire_actual_control_execution_preserved': True,
            'actual_completed_full_final_native_models': len(completed), 'new_native_fits_by_this_publication': 0,
            'actual_bank_annual_fits_at_observation': annual_count, 'original30_annual_and262_quality_records_still_required': True,
            'actual_completed_full_capacity_models_at_observation': actual_completed,
            'capacity_live_logs_are_time_bounded_snapshots_not_terminal_evidence': True,
            'new_quality_scores': 0, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'only_publication_branch': 'main'})
        targets[(PREFIX / 'README.md').as_posix()] = '# 六套全量GOSS控制完成、年度验证推进与弃用缓存清理\n\n六套原配置已完成全部6,754,006行、63特征、300轮原生训练，以及1,599,600行完整未来输入的重载、独立解码、真实80日和37日冷启动一致性检查。完整成功证据已自动上传main，回执另存。当前30个年度模型继续实际运行，观察时已完成数量见清单；完整年度和未来范围成功后另有存活服务自动上传。\n\n旧检查点发布器要求全量任务仍存活，而任务在检查前已完整成功并终止，因此断言失败发生在任何Git操作之前；源代码和实际失败说明保留，未将观察失败当成模型失败，也未重启已完成任务。本次根据完整原生终态、已核验主分支回执和实际存活年度进程记录状态。\n\n核对此前已上传的配对控制SHA，并扫描冻结服务输入绑定后，删除六个弃用小样本重复缓存，共49,545,216字节（47.25 MiB）。保留全部证据、当前及待办模型、共享完整训练缓冲区；未将项目数据写入C。首次完整发布准备的缺失依赖失败也完整保留，修复使用实际同步模块。\n\n六个最终模型复用实际拟合，不重复计数。第75/76轮262个完整方案及其父方案仍全部保留，尚待官方评分、冻结、因果检查、候选推理和完整榜；本次新增质量记录0，不读取TestY，不宣称物理资源上限或目标完成。全部记录仅提交main。\n'.encode('utf-8')
        for name, data in targets.items():
            sync.atomic(sync.WORKTREE / name, data)
        selected = sorted(targets)
        for offset in range(0, len(selected), 50):
            sync.git('add', '-f', '--', *selected[offset:offset + 50])
        staged = set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
        assert staged and staged <= set(selected)
        sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m',
            '同步GOSS已完成全量模型与完整推理检查并清理六个弃用试验缓存', timeout=180)
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
