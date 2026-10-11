"""Publish the real deadline, actual full-training resources, and retained pretraining failure."""
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
OUT = A / 'actual_deadline_and_full_training_handoff_main_v3_20261008'
PREFIX = Path('validation_sync/actual_deadline_and_full_training_20261008')


def main():
    service = A / 'service_owned_workflows_20261006/nonflag_SparseGram40_round133_full_registration_resume_v4_20261008'
    while not (service / 'native_launch.json').exists() or owned(read(service / 'native_launch.json')): time.sleep(15)
    assert read(service / 'service_execution.json')['status'] == 'passed'
    full = A / 'optimization_20261003_r133/full_registration_execution.json'
    receipt = A / 'github_validation_sync_main_20261005/round133_receipt.json'
    assert read(full)['status'] == 'passed' and read(receipt)['status'] == 'pushed_and_remote_head_verified'
    deadline = A / 'actual_user_submission_deadline_and_priority_20261008.json'
    assert read(deadline)['deadline_local'] == '2026-10-10T23:59:00+08:00'
    resource = A / 'actual_BF16_full_annual_GPU_resource_observations_v1_20261008'
    assert read(resource / 'verification.json')['status'] == 'observed_actual_full_mature_annual_GPU_WDDM_resources_read_only'
    assert not OUT.exists()
    OUT.mkdir()
    sources = [Path(__file__), full, receipt, deadline,
        A / 'record_actual_user_deadline_and_priority_v1_20261008.py',
        A / 'sample_actual_BF16_annual_GPU_resources_v1_20261008.py',
        A / 'actual_BF16_full_annual_GPU_resource_observation_hidden_launch_20261008.json',
        A / 'recover_actual_BF16_annual_E_progress_v2_20261008.py',
        A / 'actual_BF16_annual_E_progress_recovery_v2_20261008.json',
        A / 'train_neural_BF16_micro8192_bank6_v1_20261008.py',
        A / 'train_neural_BF16_micro8192_bank6_v2_20261008.py',
        A / 'neural_BF16_micro8192_native_v1_20261008.py',
        A / 'actual_neural_BF16_micro8192_bank6_v2_20261008_hidden_launch.json',
        A / 'monitor_actual_manual_resume_v1_20261008.py', A / 'monitor_actual_manual_resume_v2_20261008.py',
        A / 'refresh_actual_progress_epoch_observer_v2_20261008.py',
        A / 'actual_progress_epoch_observer_replacement_v2_20261008.json',
        A / 'actual_progress_epoch_observer_hidden_launch_v2_20261008.json']
    sources += [A/'publish_actual_deadline_and_full_training_handoff_v1_20261008.py', A/'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json']
    sources += [A/'actual_SparseGram133_empty_E_display_resume_v4_20261008.json', A/'actual_ReverseBayesFine134_empty_E_receiver_preparation_v3_20261008.json']
    folders = [(resource, PREFIX / 'actual_full_training_resources'),
        (A / 'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v1_20261008', PREFIX / 'retained_pretraining_E_observer_failure')]
    old_bank = Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_20261008')
    bank = Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    external = [(old_bank / 'protocol.json', PREFIX / 'retained_pretraining_E_observer_failure/old_protocol.json'),
                (old_bank / '2020/frozen_training_inputs.json', PREFIX / 'retained_pretraining_E_observer_failure/old_mature_inputs.json'),
                (bank / 'protocol.json', PREFIX / 'new_BF16_annual_protocol.json'),
                (bank / '2020/frozen_training_inputs.json', PREFIX / 'new_BF16_2020_mature_inputs.json')]
    pairs = [(p, PREFIX / 'sources_and_records' / p.relative_to(ROOT)) for p in sources] + external
    for folder, prefix in folders:
        pairs += [(p, prefix / p.relative_to(folder)) for p in sorted(folder.rglob('*'))
                  if p.is_file() and p.suffix in ('.json', '.log', '.stderr')]
    targets, bindings = {}, {}
    for source, target in pairs:
        data = source.read_bytes()
        assert len(data) < 10_000_000 and not helpers.sync.SECRET.search(data), source
        targets[target.as_posix()] = data
        bindings[str(source)] = {'raw_sha256': hashlib.sha256(data).hexdigest(), 'published_path': target.as_posix()}
    observed = read(A / 'actual_manual_resume_progress_20261008.json')
    targets[(PREFIX / 'actual_live_progress_snapshot.json').as_posix()] = helpers.sync.encoded(observed)
    targets[(PREFIX / 'manifest.json').as_posix()] = helpers.sync.encoded({
        'status': 'actual_user_deadline_and_past_only_full_training_handoff_no_new_quality_claims',
        'at_local': helpers.sync.now(), 'files': bindings, 'deadline_local': read(deadline)['deadline_local'],
        'WDDM_observations_not_continuous_peaks': True,
        'new_BF16_complete_annual_count_at_observed_snapshot': len(observed['new_BF16_completed_annual_models']),
        'old_pretraining_E_path_failure_preserved_new_native_training_math_unchanged': True,
        'best_fully_qualified_at_observed_snapshot': observed['best_fully_qualified'],
        'no_new_scores_native_fits_or_inference_by_publication': True, 'test_labels_read': False,
        'goal_active_not_marked_paused_or_complete': True})
    targets[(PREFIX / '.gitattributes').as_posix()] = b'* -text\n'
    targets[(PREFIX / 'README.md').as_posix()] = (
        '# 实际截止时间与本机训练交接\n\n'
        '用户确认截止为2026年10月10日23:59（UTC+8）。优先完成新BF16六份年度模型和完整评分，以及稀疏残差133轮、反向贝叶斯幅度加密；'
        '按实际完整年度耗时决定是否增加长训练，并为提交文件复核保留时间。目标继续保持活动状态。\n\n'
        '大网络在实际1694259条2020年过去成熟训练样本上运行，保存每轮原子断点。记录实际强PID绑定的WDDM独立/共享显存和RAM观测，'
        '采样值并非连续峰值，不证明模型质量或完整年度加速倍数。模型和训练临时数据放在E盘。\n\n'
        '首次年度驱动在开始拟合前遇到旧进度写入工具只允许analysis目录的路径检查，新增拟合0次。'
        '保留失败源码、日志、协议和已冻结成熟样本信息；独立v2接收器只改为E盘内原子进度写入，原生BF16训练和预测计算保持不变。'
        '独立轻量观察器展示实际年度训练轮次和完整合格方案，所有科学训练与评分工作均继续执行。\n').encode('utf8')
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
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '记录10月10日2359实际截止与E盘BF16年度训练和显存观测交接', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            create(OUT / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'at_local': sync.now(),
                'branch': 'main', 'commit': commit, 'raw_git_blobs_verified': len(hashes), 'new_quality_scores': 0})
            print('Actual deadline and full training handoff pushed to main: ' + commit, flush=True)
    finally:
        for p in reversed(held):
            if p.is_running(): p.resume()


if __name__ == '__main__': main()
