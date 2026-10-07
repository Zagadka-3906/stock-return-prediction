"""Publish measured GPU controls, scoped claims, and preserved failed attempts to main."""
from pathlib import Path
import hashlib
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from file_backed_hidden_git_runtime_20261007 import installed
import publish_classifier_consensus_workflows_20261006 as helpers

OUT = A / 'actual_GPU_resource_controls_main_v1_20261008'
PREFIX = Path('validation_sync/actual_GPU_resource_controls_20261008')


def main():
    full = A / 'optimization_20261003_r132/full_registration_execution.json'
    round_receipt = A / 'github_validation_sync_main_20261005/round132_receipt.json'
    for name in ('nonflag_ReverseBayes40_round132_full_registration_v1',
                 'actual_BF16_micro8192_small32_wide2_restart_control_v1_20261008'):
        folder = A / 'service_owned_workflows_20261006' / name
        while not (folder / 'native_launch.json').exists() or owned(read(folder / 'native_launch.json')):
            time.sleep(15)
        assert read(folder / 'service_execution.json')['status'] == 'passed', name
    assert read(full)['status'] == 'passed'
    assert read(round_receipt)['status'] == 'pushed_and_remote_head_verified'
    gpu32 = A / 'epoch_durable_neural_checkpoint_GPU32_preflight_v1_20261008'
    wide = Path(read(A / 'actual_wide_GPU_precision3_benchmark_location_20261008.json')['output'])
    restart = Path(read(A / 'actual_BF16_micro_restart_location_20261008.json')['output'])
    assert read(gpu32 / 'verification.json')['actual_all32_training_losses_exact']
    proof = read(wide / 'verification.json')
    assert proof['status'] == 'passed_actual_own_mature_subset_wide_GPU_precision3_resource_benchmark'
    assert len(proof['records']) == 3 and proof['new_quality_scores'] == 0
    assert read(restart / 'verification.json')['status'] == 'passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart'
    assert not OUT.exists()
    OUT.mkdir()
    sources = [Path(__file__), full, round_receipt,
        *A.glob('*actual*GPU*20261008.py'), *A.glob('*actual*GPU*20261008.json'),
        *A.glob('*neural_BF16*20261008.py'), *A.glob('*actual_BF16*20261008.json'),
        *A.glob('benchmark_actual_wide_GPU*20261008.py'),
        A / 'verify_epoch_durable_neural_checkpoint_GPU32_v1_20261008.py',
        A / 'epoch_durable_neural_checkpoint_adapter_v2_20261007.py',
        A / 'train_diverse_backbones_20261003.py']
    folders = [(gpu32, PREFIX / 'original_small_GPU32'), (wide, PREFIX / 'wide_precision3'),
               (restart, PREFIX / 'new_BF16_restart')]
    service_names = ['actual_GPU32_checkpoint_fresh_process_control_20261008',
                     'actual_wide_GPU_precision3_resource_benchmark_20261008',
                     'actual_wide_GPU_precision3_resource_benchmark_v2_20261008',
                     'actual_wide_GPU_precision3_resource_benchmark_v3_20261008',
                     'actual_BF16_micro8192_small32_wide2_restart_control_v1_20261008']
    for name in service_names:
        folder = A / 'service_owned_workflows_20261006' / name
        assert read(folder / 'service_execution.json')['status'] in ('passed', 'failed')
        folders.append((folder, PREFIX / 'actual_services' / name))
    targets = {}
    bindings = {}
    for source in dict.fromkeys(sources):
        data = source.read_bytes()
        assert not helpers.sync.SECRET.search(data), source
        target = (PREFIX / 'sources_and_pointers' / source.relative_to(ROOT)).as_posix()
        targets[target] = data
        bindings[str(source)] = {'published_path': target, 'raw_sha256': hashlib.sha256(data).hexdigest()}
    for folder, prefix in folders:
        for source in sorted(folder.rglob('*')):
            if not source.is_file() or source.suffix not in ('.json', '.log', '.stderr') or 'tmp' in source.relative_to(folder).parts:
                continue
            data = source.read_bytes()
            assert len(data) < 20_000_000 and not helpers.sync.SECRET.search(data), source
            target = (prefix / source.relative_to(folder)).as_posix()
            targets[target] = data
            bindings[str(source)] = {'published_path': target, 'raw_sha256': hashlib.sha256(data).hexdigest()}
    manifest = {'status': 'actual_GPU_measurements_and_distinct_recipe_restart_controls_only',
                'at_local': helpers.sync.now(), 'files': bindings,
                'actual_wide_timed_updates_per_recipe': 3,
                'median_update_seconds': {r['recipe']: r['median_timed_update_seconds'] for r in proof['records']},
                'actual_wide_restart_control_epochs': 2, 'actual_small_restart_control_epochs': 32,
                'original_full_FP32_annual_weights_not_reused_as_BF16': True,
                'full_annual_speedup_and_model_quality_not_established': True,
                'new_complete_annual_models': 0, 'new_quality_scores': 0,
                'failed_import_and_WDDM_codec_attempts_preserved': True, 'test_labels_read': False,
                'large_arrays_and_checkpoints_retained_on_authorized_E_with_recorded_hashes': True}
    targets[(PREFIX / 'manifest.json').as_posix()] = helpers.sync.encoded(manifest)
    targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
    targets[(PREFIX / 'README.md').as_posix()] = (
        '# 本机实际GPU资源与续训检查\n\n'
        '原FP32小网络32轮与独立进程7+25轮续训完全相同。新BF16微批方案另行完成小网络32轮和实际16384/8192/4096大网络2轮的独立进程重启检查，'
        '包含非整除批次；训练损失、全部参数位、预处理、FP32重载预测、固定8192行冷前缀和污染训练输入拒绝均通过。\n\n'
        '另在65536条过去成熟训练样本上比较FP32、BF16、TF32三种微批8192/有效批32768方案，每种1次预热和3次计时更新。'
        '中位耗时分别约2.401、1.014、1.483秒，采样所见共享显存约0.080GiB。WDDM观测并非连续峰值。'
        '原整批32768未复测，子集特征张量更小；以上不证明完整年度加速倍数，也不是年度模型质量评分。'
        '新BF16是不同的科学方案，不能继承原FP32年度权重。新年度模型及官方分数均为0。\n\n'
        '所有源码、输入哈希、实际日志和失败尝试记录同步至main；大型训练数组与续训文件保留在E盘。\n').encode('utf8')
    held = []
    try:
        row = read(A / 'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        create(OUT / 'actual_idle_main_hold.json', idle)
        with installed(OUT / 'file_backed_git'):
            sync = helpers.sync
            previous = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous)
            assert not sync.git('status', '--porcelain')
            for p, info in bindings.items(): assert sha(p) == info['raw_sha256'], p
            for name, data in targets.items(): sync.atomic(sync.WORKTREE / name, data)
            names = sorted(targets)
            for left in range(0, len(names), 50): sync.git('add', '-f', '--', *names[left:left+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) == set(names)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '同步实际GPU三精度资源实测及BF16大小网络断点续训验证', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            create(OUT / 'receipt.json', {'status': 'pushed_and_remote_head_verified',
                'commit': commit, 'at_local': sync.now(), 'branch': 'main', 'raw_git_blobs_verified': len(hashes),
                'new_quality_scores': 0, 'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + PREFIX.as_posix()})
            print('Actual GPU controls pushed to main: ' + commit, flush=True)
    finally:
        for p in reversed(held):
            if p.is_running(): p.resume()


if __name__ == '__main__': main()
