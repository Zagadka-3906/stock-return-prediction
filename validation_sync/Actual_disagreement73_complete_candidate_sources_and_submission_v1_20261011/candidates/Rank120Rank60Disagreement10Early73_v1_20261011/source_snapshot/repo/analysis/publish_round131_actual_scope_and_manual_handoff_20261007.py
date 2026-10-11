"""Close the existing round's explanatory erratum and manual disk handoff only."""
from pathlib import Path
from datetime import datetime
import hashlib
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from handoff_ready_goss_full_execution_20261006 import pair
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from file_backed_hidden_git_runtime_20261007 import installed
import publish_classifier_consensus_workflows_20261006 as helpers

OUT = A / 'round131_actual_scope_and_manual_handoff_20261007'
LIMIT = datetime.fromisoformat('2026-10-07T23:53:00+08:00').timestamp()


def main():
    assert time.time() < LIMIT
    full = A / 'optimization_20261003_r131/full_registration_execution.json'
    receipt = A / 'github_validation_sync_main_20261005/round131_receipt.json'
    assert read(full)['status'] == 'passed'
    actual = read(receipt)
    assert actual['status'] == 'pushed_and_remote_head_verified'
    assert actual['scored_records'] == 40 and actual['connected_records'] == 13498
    plan_path = A / 'nonflag_RidgeMicro40_plan_20261007.json'
    plan = read(plan_path)
    assert len(plan['weights']) == 12 and plan['expected_full_transform_controls'] == 37
    assert plan['qualified_anchor_rounds'] == [112, 129, 130]
    selected_path = A / 'optimization_20261003_r131/selection.json'
    selected = read(selected_path)
    score = selected['winner']['metrics']['final_score']
    assert score == actual['official_score'] == 0.45111337697678194
    handoff = A / 'actual_manual_morning_optimization_handoff_20261007.json'
    if not handoff.exists():
        from record_actual_manual_morning_handoff_20261007 import main as record
        record()
    assert read(handoff)['best_fully_qualified_at_handoff']['round'] == 131
    assert not OUT.exists()
    OUT.mkdir()
    sync = helpers.sync
    held = []
    row = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    parent, worker = pair(row)
    if parent.status() == worker.status() == psutil.STATUS_STOPPED:
        journal = read(A / 'shutdown_ready_stop_until_manual_continue_20261007/suspension_journal.json')
        assert all(any(e['identity']['pid'] == p.pid and e['identity']['creation_time'] == p.create_time()
                       and e['phase'] == 'suspended' for e in journal['entries']) for p in (parent, worker))
        assert not parent.children(recursive=True) or all(p.pid == worker.pid for p in parent.children(recursive=True))
        create(OUT / 'existing_shutdown_guard_main_hold.json', {'status': 'borrowed_exact_already_quiesced_main_no_resume', 'launch': row})
    else:
        assert time.time() < datetime.fromisoformat('2026-10-07T23:45:00+08:00').timestamp()
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        create(OUT / 'actual_idle_main_hold.json', idle)
    sources = [Path(__file__), A / 'record_actual_manual_morning_handoff_20261007.py', handoff, full, receipt, plan_path, selected_path]
    pins = {str(p): sha(p) for p in sources}
    try:
        with installed(OUT / 'file_backed_git'):
            original_git = sync.git
            def bounded_git(*args, **kwargs):
                remaining = LIMIT - time.time()
                assert remaining > 5, 'Document closeout deadline reached; no new quality work.'
                kwargs['timeout'] = min(kwargs.get('timeout', 90), max(1, int((remaining - 5) / 3)))
                return original_git(*args, **kwargs)
            sync.git = bounded_git
            try:
                previous = sync.git('rev-parse', 'HEAD')
                helpers.verify_main(previous)
                assert not sync.git('status', '--porcelain')
                prefix = Path('validation_sync/round131')
                target = (prefix / 'README.md').as_posix()
                before = (sync.WORKTREE / target).read_bytes()
                original_manifest = read(sync.WORKTREE / prefix / 'manifest.json')
                assert target not in original_manifest['exported_files'], 'An existing README binding requires explicit rebinding.'
                text = before.decode('utf8')
                marker = '\n本轮52项完整官方比较：'
                assert text.count(marker) == 1
                corrected = text.split(marker, 1)[0] + (
                    '\n本轮实际为40项完整官方比较：112、129、130三个合格锚点，两组非涨停残差Ridge及等权集成各12个幅度（36项），加一个消融。'
                    '复用既有10个年度成熟Ridge模型，训练期教师为106；37项全量5635800行变换和111项冷前缀检查通过。'
                    '胜出方案为l025残差权重0.002075，官方S=0.45111337697678194，比前最佳高约7.28e-9。'
                    '候选实际重载17个原生模型，两次完整未来特征重放、独立参数解码和冷80检查通过；未读取真实测试标签。'
                    'QA42保留全部六视图、45秒浏览器超时及原始核对，完整榜共13498条记录。'
                    '本次仅纠正旧模板的说明文字并保存手动恢复记录；原始评分、模型、冻结源码和候选不变，原错误说明另行归档。'
                    '有限网格不证明优化方向穷尽；23:55停止，明早仅在用户实际发送“继续”后恢复。\n')
                correction = {'status': 'administrative_explanatory_scope_correction_no_new_scores_or_inference',
                    'round': 131, 'at_local': sync.now(), 'original_full_round_commit': actual['commit'],
                    'corrected_fields': {'official_comparisons': 40, 'anchor_rounds': [112, 129, 130], 'weights_per_head': 12,
                        'full_transform_controls': 37, 'cold_prefix_controls': 111, 'actual_new_candidate_models': 17},
                    'original_README_sha256': hashlib.sha256(before).hexdigest(),
                    'corrected_README_sha256': hashlib.sha256(corrected.encode('utf8')).hexdigest(),
                    'original_template_sources_and_old_commit_message_preserved': True,
                    'original_manifest_has_no_README_blob_binding': True,
                    'input_sha256': pins, 'new_quality_scores': 0, 'new_native_fits': 0, 'new_inference': 0,
                    'automatic_restart_enabled': False, 'global_optimization_boundary_proven': False}
                create(OUT / 'actual_scope_correction.json', correction)
                payload = {target: corrected.encode('utf8'),
                    (prefix / 'scope_correction/original_published_README.md').as_posix(): before}
                for p in [*sources, OUT / 'actual_scope_correction.json']:
                    data = p.read_bytes()
                    assert not sync.SECRET.search(data), p
                    payload[(prefix / 'scope_correction' / p.relative_to(ROOT)).as_posix()] = data
                for p, digest in pins.items(): assert sha(p) == digest, p
                for name, data in payload.items(): sync.atomic(sync.WORKTREE / name, data)
                names = sorted(payload)
                sync.git('add', '-f', '--', *names)
                assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) == set(names)
                sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '纠正第131轮实际40项验证说明并保存明早手动恢复记录')
                commit = sync.git('rev-parse', 'HEAD')
                hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
                assert helpers.blob_hashes(commit, hashes) == hashes
                sync.git('push', 'origin', 'HEAD:refs/heads/main')
                helpers.verify_main(commit)
                helpers.watcher.advance_source_index(commit)
                create(OUT / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'commit': commit,
                    'at_local': sync.now(), 'branch': 'main', 'raw_git_blobs_verified': len(hashes),
                    'original_full_round_receipt_preserved': str(receipt), 'new_quality_scores': 0})
                print('Actual scope correction and manual handoff pushed to main: ' + commit, flush=True)
            finally:
                sync.git = original_git
    finally:
        for p in reversed(held):
            if p.is_running(): p.resume()


if __name__ == '__main__':
    main()
