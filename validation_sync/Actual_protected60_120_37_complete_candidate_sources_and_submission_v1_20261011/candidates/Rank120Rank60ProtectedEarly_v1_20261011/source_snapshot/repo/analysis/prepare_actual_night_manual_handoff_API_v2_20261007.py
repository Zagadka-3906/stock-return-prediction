"""Prepare a small honest main backup without qualifying the failed full upload."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from handoff_ready_goss_full_execution_20261006 import pair
import publish_classifier_consensus_workflows_20261006 as helpers

OUT = A / 'actual_night_manual_handoff_API_v2_20261007'


def main():
    assert not OUT.exists()
    OUT.mkdir()
    launch = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
    parent, worker = pair(launch)
    assert parent.status() == worker.status() == psutil.STATUS_STOPPED
    guard = read(A / 'shutdown_ready_stop_until_manual_continue_20261007/guardian_status.json')
    assert guard['status'] == 'quiescing_dispatch_before_disk_stop'
    assert read(A / 'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/service_execution.json')['status'] == 'failed'
    assert not (A / 'github_validation_sync_main_20261005/round131_receipt.json').exists()
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=helpers.sync.WORKTREE, capture_output=True,
        text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW, check=True).stdout.strip()
    assert head == '328763034523f14ed3e08c3955cc1b634f0d5913'
    tree = subprocess.run(['git', 'rev-parse', 'HEAD^{tree}'], cwd=helpers.sync.WORKTREE, capture_output=True,
        text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW, check=True).stdout.strip()
    files = [Path(__file__), A / 'actual_manual_morning_optimization_handoff_20261007.json',
        A / 'record_actual_manual_morning_handoff_20261007.py',
        A / 'nonflag_RidgeMicro40_plan_20261007.json',
        A / 'lossless_ranking_display_qa_v42_20261007/round131/verification.json',
        A / 'nonflag_RidgeMicro40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json',
        A / 'optimization_20261003_r131/full_registration_failure.json',
        A / 'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/service_execution.json',
        A / 'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2/stderr.log',
        A / 'publish_round131_actual_scope_and_manual_handoff_20261007.py']
    files += [A/'prepare_actual_night_handoff_after_guard_recovery_v2_20261007.py',A/'prepare_actual_night_manual_handoff_API_20261007.py',A/'actual_night_manual_handoff_API_20261007/failed_guard_precondition.json',A/'shutdown_ready_stop_v2_20261007.py',A/'recover_actual_failed_shutdown_guard_v2_20261007.py',A/'actual_failed_shutdown_guard_recovery_v2_20261007.json',A/'service_owned_workflows_20261006/shutdown_ready_2355_manual_continue_20261007/service_execution.json',A/'service_owned_workflows_20261006/shutdown_ready_2355_manual_continue_20261007/stderr.log']
    prefix = Path('validation_sync/night_manual_handoff_20261007')
    elements = []
    hashes = {}
    for p in files:
        raw = p.read_bytes()
        assert not helpers.sync.SECRET.search(raw), p
        assert len(raw) < 200000, (p, len(raw))
        target = (prefix / p.relative_to(ROOT)).as_posix()
        elements.append({'path': target, 'mode': '100644', 'type': 'blob', 'content': raw.decode('utf8')})
        hashes[target] = {'sha256': hashlib.sha256(raw).hexdigest(), 'git_blob_sha': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}
    explanation = (
        '第131轮实际范围与停工恢复记录\n\n'
        '本轮40项比较 = 112、129、130三个锚点 + 两组Ridge及等权集成各12个幅度（36项）+ 一个消融。37项全量变换与111项冷前缀控制通过。'
        '复用原10个年度成熟Ridge模型。胜出l025残差权重0.002075，S=0.45111337697678194，比原最佳高约7.28e-9。'
        '17个原生模型的新候选已完成完整重放、独立解码、冷80检查和封存；QA42检查通过，本地完整榜13498条。\n\n'
        '40项原始官方评分已单独同步main；最后的完整榜整包上传于23:46因Git TLS错误失败，因此本轮尚未取得完整注册上传回执。'
        '完整通过全部流程的最佳仍是第128轮，S=0.45111336969856725。本包仅备份已完成状态、失败记录和明早手动恢复计划，不补写第131轮通过标记。'
        '先前准备的发布器包含沿用旧模板的轮次与数量文字，不能据此改变实际40项范围；更正发布器仅已准备，未执行。\n\n'
        '23:55停止项目工作，允许随后关机。明早仅在用户实际发送“继续”后恢复：先核对停机清单与main，补完第131轮完整榜上传并纠正说明；'
        '再完成负向Bayes、稀疏回归官方验证及GPU微批/混合精度/逐epoch恢复实测。原大网络未落盘的2022年度不能从当前epoch恢复；2020、2021已完成年度保留。'
        '新稀疏回归10个年度模型及3/37/111控制已通过，但没有新增稀疏官方分数。尚未证明所有优化方向穷尽。\n\n'
        '本API备份若推进main，原发布工作树仍在旧提交；下一次任何Git发布前必须安全取回main并同步发布器索引，不能直接推送旧HEAD。'
        '当前发布器由停工守护暂停，本次不会恢复它。\n')
    elements.append({'path': (prefix / 'README.md').as_posix(), 'mode': '100644', 'type': 'blob', 'content': explanation})
    elements.append({'path': (prefix / '.gitattributes').as_posix(), 'mode': '100644', 'type': 'blob', 'content': '* -text\n'})
    freeze = {'status': 'frozen_manual_handoff_backup_no_full131_qualification', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'expected_main_parent': head, 'base_tree_sha': tree, 'main_publisher_already_stopped_by_shutdown_guard': launch,
        'files': hashes, 'new_quality_scores': 0, 'new_native_fits': 0, 'automatic_restart_enabled': False,
        'requires_safe_main_worktree_and_source_index_adoption_after_API_commit': True,
        'full131_publication_pending': True, 'global_optimization_boundary_proven': False}
    create(OUT / 'frozen_payload.json', freeze)
    elements.append({'path': (prefix / 'manifest.json').as_posix(), 'mode': '100644', 'type': 'blob', 'content': (OUT / 'frozen_payload.json').read_text(encoding='utf8')})
    packet = {'repository_full_name': 'Zagadka-3906/stock-return-prediction', 'base_tree_sha': tree, 'tree_elements': elements}
    create(OUT / 'tree_packet.json', packet)
    print(json.dumps(packet, ensure_ascii=False))


if __name__ == '__main__':
    main()
