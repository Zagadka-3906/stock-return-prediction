"""Export the complete original R81 snapshot and both preserved recovery attempts."""
from pathlib import Path


def install(sync, qualification):
    original = sync.snapshot
    source = sync.ROOT / 'analysis/sync_validated_rounds_main_20261005.py'
    assert source.resolve().parents[1] == sync.ROOT.resolve()
    text = source.read_text(encoding='utf-8')
    before = "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'"
    after = "ROOT / 'analysis/lossless_ranking_display_qa_v3_20261006/round81/qa/interaction_result.json'"
    assert text.count(before) == 1
    text = text.replace(before, after)
    namespace = dict(sync.__dict__, __name__='actual_recovered_round81_export')
    exec(compile(text, str(source), 'exec'), namespace)
    namespace['complete_round_evidence'] = qualification.complete_round_evidence

    def snapshot(number):
        if number != 81:
            return original(number)
        manifest, payload = namespace['snapshot'](number)
        root, a = sync.ROOT, sync.ROOT / 'analysis'
        relative = Path('validation_sync/round81')
        folder = a / 'optimization_20261003_r81'
        paths = [folder / name for name in (
            'publication_recovery_execution_v2_20261006.json',
            'recovery_frozen_execution_v2_20261006.json',
            'recovery_frozen_execution_20261006.json',
            'publication_recovery_failure_20261006.json',
            'recovery_full_ranking_snapshot_v2_20261006.json.gz',
        )]
        for version in ('', '_v2'):
            service = a / f'service_owned_workflows_20261006/round81_publication_recovery{version}'
            paths += [service / name for name in ('job_definition.json', 'native_launch.json', 'service_execution.json')]
        for name in ('frozen_before_encoding.json', 'verification.json', 'complete_rankings_lossless.html'):
            paths.append(a / 'lossless_ranking_display_20261006/round81' / name)
        for version in ('', '_v3'):
            qa = a / f'lossless_ranking_display_qa{version}_20261006/round81'
            paths += [qa / name for name in ('frozen_before_actual_full_QA.json', 'verification.json',
                'qa/interaction_result.json', 'qa/ranking_report.png')]
        paths += [a / 'round81_recovered_publication_github_20261006/failure.json',
            a / 'service_owned_workflows_20261006/round81_recovered_main_publication/job_definition.json',
            a / 'service_owned_workflows_20261006/round81_recovered_main_publication/native_launch.json',
            a / 'service_owned_workflows_20261006/round81_recovered_main_publication/service_execution.json',
            a / 'launch_service_owned_windows_workflow_20261006.ps1',
            a / 'optimization_windows_status_20261006_0229.json',
            a / 'round81_failed_C_Chrome_cache_relocation_20261006.json']
        for name in ('independent_windows_background_probe_20261006', 'independent_windows_background_probe_v2_20261006'):
            paths += sorted((a / name).glob('*.json'))
        manifest['publication_recovery_QA_path_substitution'] = {'before': before, 'after': after,
            'entire_original_snapshot_and_scientific_export_checks_retained': True}
        for path in dict.fromkeys(paths):
            data = path.read_bytes()
            assert not sync.SECRET.search(data)
            destination = (relative / 'publication_recovery' / path.relative_to(a)).as_posix()
            payload[destination] = data
            manifest['local_input_source_sha256'][path.relative_to(root).as_posix()] = sync.sha(data)
            manifest['exported_files'][destination] = {'bytes': len(data), 'sha256': sync.sha(data)}
        payload[(relative / '.gitattributes').as_posix()] = b'* -text\n'
        manifest['exported_files'][(relative / '.gitattributes').as_posix()] = {
            'bytes': 8, 'sha256': sync.sha(b'* -text\n')}
        manifest['original_timeout_and_first_recovery_directory_collision_failures_preserved'] = True
        manifest['actual_closed_source_locked_full_selected_replay_and_all_original_QA_passed'] = True
        manifest['immutable_full_ranking_snapshot_and_lossless_complete_HTML_published'] = True
        payload[(relative / 'manifest.json').as_posix()] = sync.encoded(manifest)
        payload[(relative / 'README.md').as_posix()] += (
            '\n原始榜单页面因体积导致45秒浏览器验证超时，首次恢复又遇到浏览器临时目录重名。'
            '两份失败证明均保留。此次实际恢复在全部原始冻结输入的只读锁下，'
            '重新计算5,635,800条选中输出，逐位一致；完整原始榜单核验、'
            '无损页面浏览器核验及最终全量哈希复核全部通过。'
            '完整9,946条榜单的无损HTML和完整JSON压缩快照保存在 publication_recovery 中。'
            '原科学协议、分数、模型及预测保持原样；新启动与浏览器临时目录均使用D盘。\n'
        ).encode('utf-8')
        return manifest, payload

    sync.snapshot = snapshot
    return original
