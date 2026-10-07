"""Adopt the actual API main fast-forward and start only the unfinished publication."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from scheduled_user_pause_20261007 import inventory
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
from file_backed_hidden_git_runtime_20261007 import installed


def main():
    assert not inventory(full=True), 'Do not restart an existing owned workflow.'
    resume = A / 'actual_manual_resume_after_shutdown_20261008.json'
    sources = [Path(__file__), A / 'actual_shutdown_pause_status_20261007.json',
        A / 'shutdown_ready_stop_until_manual_continue_20261007/disk_recovery_manifest.json',
        A / 'actual_next_morning_main_transport_handoff_20261007.json',
        A / 'actual_night_manual_handoff_API_v2_20261007/receipt.json']
    assert read(sources[2])['status'] == 'project_workers_stopped_with_disk_recovery_manifest'
    import publish_classifier_consensus_workflows_20261006 as helpers
    with installed(A / 'manual_resume_main_adoption_file_IO_20261008'):
        actual = helpers.sync.git('rev-parse', 'HEAD')
        assert actual == 'dda17842b344be0b656f0db75c8ac59bf876258f'
        helpers.verify_main(actual)
        assert not helpers.sync.git('status', '--porcelain')
        assert not helpers.sync.git('diff', '--cached', '--name-only', cwd=ROOT)
        helpers.watcher.advance_source_index(actual)
        create(resume, {'status': 'actual_user_continue_after_verified_shutdown_and_safe_main_adoption',
            'actual_user_instruction': '继续', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'input_sha256': {str(p): sha(p) for p in sources}, 'main': actual,
            'actual_no_owned_project_workers_before_new_dispatch': True,
            'primary_working_files_not_reset_cleaned_or_checked_out': True,
            'old_expired_stop_and_dispatch_schedules_not_restarted': True,
            'new_quality_scores': 0, 'new_native_fits': 0})
    original = A / 'publish_nonflag_RidgeMicro40_round131_full_validation_20261007.py'
    new = A / 'publish_nonflag_RidgeMicro40_round131_full_validation_v3_20261008.py'
    text = original.read_text(encoding='utf8')
    start_marker = "    payload[(prefix / 'README.md').as_posix()] += ("
    end_marker = "    previous = sync.git('rev-parse', 'HEAD')"
    first = text.index(start_marker)
    last = text.index(end_marker, first)
    explanation = ('\n本轮实际40项完整官方比较：112、129、130三个合格锚点，两组非涨停残差Ridge及等权集成各12个幅度（36项），加一个消融。'
        '复用既有10个年度成熟Ridge模型，教师为106；37项5635800行全量变换和111项冷前缀核对通过。'
        '胜出l025残差权重0.002075，S=0.45111337697678194，较原最佳提高约7.28e-9。'
        '选中新方案已执行17个原生模型重载、独立解码、两次完整未来特征重放和冷80检查。'
        '完整榜13498条，原始六视图和45秒QA42完整保留。本次恢复昨晚失败的上传并核对全部冻结文件，不重复计入评分、拟合或推理。'
        '旧模板数量和轮次文字另作历史证据保留，不能替代本轮实际40项记录。仅main，未读取真实测试标签；不声称优化穷尽。\n')
    text = text[:first] + "    payload[(prefix / 'README.md').as_posix()] += " + repr(explanation) + ".encode('utf8')\n" + text[last:]
    old_message = '登记第119轮88项非涨停残差HGB与完整父方案组合验证并发布完整榜与全量QA'
    assert text.count(old_message) == 1
    text = text.replace(old_message, '补完第131轮40项Ridge验证完整榜与QA42并保留上传失败历史')
    needle = '    for path in extra:\n'
    assert text.count(needle) == 1
    extra = [Path(__file__), original, A / 'run_round131_preserved_QA42_main_recovery_v3_20261008.py',
        resume, A / 'actual_next_morning_main_transport_handoff_20261007.json',
        A / 'actual_night_manual_handoff_API_v2_20261007/receipt.json',
        A / 'shutdown_ready_stop_until_manual_continue_20261007/disk_recovery_manifest.json',
        A / 'optimization_20261003_r131/full_registration_failure.json',
        A / 'optimization_20261003_r131/provenance_scope_execution.json']
    service = A / 'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v2'
    extra += [*service.glob('*.json'), *service.glob('*.log')]
    text = text.replace(needle, '    extra += [' + ','.join('A/' + repr(p.relative_to(A).as_posix()) for p in extra) + ']\n' + needle)
    compile(text, str(new), 'exec')
    assert not new.exists()
    new.write_text(text, encoding='utf8', newline='\n')
    paths = [new, original, A / 'run_round131_preserved_QA42_main_recovery_v3_20261008.py', *extra]
    pins = {str(p): sha(p) for p in paths}
    row = start('round131_preserved_QA42_main_publication_recovery_v3_20261008',
        'run_round131_preserved_QA42_main_recovery_v3_20261008.py', [], pins)
    create(A / 'actual_round131_recovery_hidden_launch_v3_20261008.json', {
        'status': 'started_only_unfinished_original_QA42_main_publication', 'identity': row,
        'input_sha256': pins, 'new_quality_scores': 0, 'new_candidate_inference': 0})
    print('Actual manual resume verified; original round131 publication recovery launched hidden.', flush=True)


if __name__ == '__main__':
    main()
