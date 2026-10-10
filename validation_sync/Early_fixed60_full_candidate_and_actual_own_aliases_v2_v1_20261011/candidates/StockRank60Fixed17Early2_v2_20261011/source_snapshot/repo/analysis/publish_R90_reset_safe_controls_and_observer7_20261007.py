"""Publish measured local acceleration and strict unfinished-grid repair evidence on main."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    p = A / 'service_owned_workflows_20261006' / name
    while not (p / 'native_launch.json').exists() or owned(read(p / 'native_launch.json')):
        time.sleep(15)
    assert read(p / 'service_execution.json')['status'] == 'passed', name
    return p


def main():
    import psutil
    control_service=closed('R90_dynamic_score_context_v3_preflight')
    monitor_service=closed('local_only_observer7_actual_handoff')
    control_folder=A/'R90_dynamic_score_context_v3_preflight_20261007'
    proof=read(control_folder/'verification.json')
    assert proof['status']=='passed_actual_two_full5635800_scheme_original8_metric_bits_and_Windows_reset_safe_score_hooks'
    assert read(A/'local_only_monitor_v7_actual_handoff_20261007/verification.json')['scientific_workers_stopped_or_restarted']==0
    current=A/'service_owned_workflows_20261006/classifier_consensus_R90_root_resolution_recovery_v3'
    identity=read(current/'native_launch.json')
    out=A/'R90_reset_safe_controls_and_observer7_github_20261007';assert not out.exists();out.mkdir()
    create(out/'actual_dispatch_snapshot.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'worker_identity':identity,'strong_owned_live_at_snapshot':owned(identity),'terminal_at_snapshot':read(current/'service_execution.json') if (current/'service_execution.json').exists() else None,'actual_phase':read(A/'ongoing_optimization_r90_state.json'),'actual_written_records':sum(len(read(p)['results']) for p in (A/'optimization_20261003_r90').glob('wave*_results.json')),'full138_qualification_not_claimed':True,'test_labels_read':False})
    names=['publish_R90_reset_safe_controls_and_observer7_20261007.py','classifier_consensus_recovery_official_speed_adapter_v2_20261007.py','verify_R90_dynamic_score_context_v2_20261007.py','verify_R90_dynamic_score_context_v3_20261007.py','R90_dynamic_score_context_v2_preflight_admission_20261007.json','R90_dynamic_score_context_v3_preflight_admission_20261007.json','run_classifier_consensus_R90_root_resolution_recovery_v2_20261007.py','run_classifier_consensus_R90_root_resolution_recovery_v3_20261007.py','classifier_consensus_R90_root_resolution_recovery_v2_admission_20261007.json','classifier_consensus_R90_root_resolution_recovery_v3_admission_20261007.json','R90_failed_root_recovery_scope_non_pinning_audit_v2_20261007.json','optimization_20261003_r90/provenance_scope_execution_failed_root_recovery_20261007.json','optimization_20261003_r90/component_audit.json','monitor_local_only_runtime_v7_20261007.py','handoff_local_only_monitor_v7_20261007.py']
    sources=[A/name for name in names]+[out/'actual_dispatch_snapshot.json']
    for folder in [control_folder,A/'R90_dynamic_score_context_v2_preflight_20261007',A/'local_only_monitor_v7_actual_handoff_20261007']:
        sources += list(folder.glob('*.json'))
    for name in ['classifier_consensus_R90_root_resolution_recovery','R90_dynamic_score_context_v2_preflight','R90_dynamic_score_context_v3_preflight','classifier_consensus_R90_root_resolution_recovery_v2','classifier_consensus_R90_root_resolution_recovery_v3','local_only_observer7_actual_handoff','local_only_progress_monitor_v7']:
        service=A/'service_owned_workflows_20261006'/name
        sources += [service/n for n in ('job_definition.json','native_launch.json','verified_hidden_launch.json')]
        if name not in ('classifier_consensus_R90_root_resolution_recovery_v3','local_only_progress_monitor_v7'):
            sources += [p for p in [service/'service_execution.json',service/'stderr.log',service/'stdout.log'] if p.exists()]
    folder=A/'classifier_consensus_R90_root_resolution_recovery_v3_20261007'
    if folder.exists():sources += list(folder.glob('*.txt'))+[p for p in folder.glob('*.json') if p.name.startswith(('frozen','actual_failed'))]
    pins={**proof['input_sha256'],**{str(p.resolve()):sha(p) for p in sources}}
    create(out / 'frozen_before_main_publication.json', {'input_sha256': pins, 'test_labels_read': False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held, retries = [], []
    restore = install()
    sync = helpers.sync
    old_git = sync.git

    def retry_git(*args, **kwargs):
        for attempt in range(3):
            try:
                return old_git(*args, **kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote', 'push', 'fetch') or not any(t in str(error).lower() for t in ('tls', 'ssl', 'connection', 'timed out', 'unable to access')):
                    raise
                retries.append({'command': args[0], 'attempt': attempt + 1, 'error': str(error)[:1000]})
                if attempt == 2:
                    raise
                time.sleep(2)

    sync.git = retry_git
    try:
        row = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        with LockedReadHashCache(pins) as scope:
            prefix = Path('validation_sync/R90_reset_safe_controls_and_observer7_20261007')
            payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
            files = {}
            for p in dict.fromkeys([*sources, out / 'frozen_before_main_publication.json']):
                data = p.read_bytes()
                assert not sync.SECRET.search(data), p
                raw_sha = hashlib.sha256(data).hexdigest()
                target = (prefix / p.relative_to(ROOT)).as_posix()
                if len(data) >= 5 * 1024**2:
                    data = gzip.compress(data, mtime=0)
                    assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_sha
                    target += '.gz'
                payload[target] = data
                files[p.relative_to(ROOT).as_posix()] = {'published_path': target, 'original_sha256': raw_sha, 'published_sha256': hashlib.sha256(data).hexdigest()}
            previous = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous)
            assert not sync.git('status', '--porcelain')
            manifest={'status':'passed_actual_two_full_scheme_original8_metric_bits_and_Windows_reset_safe_context_controls','at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main','actual_original_reference_scheme_evaluations':2,'actual_windows_worker_scheme_evaluations':2,'all8_metric_uint64_bits_exact':True,'actual_full5635800_rows_each':True,'original_failed_build_and_score_hook_and_reference_alias_checks_archived':True,'actual_changed_full_future_and_cold80_component_audit_passed':True,'R90_actual138_completion_not_claimed':True,'actual_single_host_observer7_handoff_passed':True,'remote_workers_dispatched':0,'new_native_fits':0,'new_selection_score_records_by_diagnostic':0,'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded(manifest)
            payload[(prefix/'README.md').as_posix()]=('# 第90轮评分上下文修复及单机观察器更新\n\n'
                '原失败记录、完整推理检查及实际修复代码全部保存。修复后的评分钩子在切换根模型、重建上下文后重新安装；旧恢复日志使用独立的新文件名。\n\n'
                '两种真实方案分别在原评分上下文及 Windows 私有工作者中完整处理5635800行历史验证数据，8项官方指标逐位一致。诊断遵循原有全部字节指纹缓存规则，不代表138项方案已完成。\n\n'
                '单机观察器7已实际接管，展示第90轮真实部分记录、工作者身份、全股票池HGB24/44及批量推理速度。原GPU及所有科学工作者保持运行。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存第90轮两种完整历史方案评分上下文重置对照及失败记录和单机观察器7', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'commit': commit, 'at_local': sync.now(),
                'branch': 'main', 'raw_git_blobs_verified': len(hashes), 'new_quality_scores': 0,
                'all_source_inputs_initial_and_final_read_locked_full_rehash': True,
                'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
            print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    finally:
        sync.git = old_git
        for p in reversed(held):
            if p.is_running():
                p.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})
        create(out / 'transport_retries.json', {'attempts': retries, 'TLS_verification_unchanged': True})


if __name__ == '__main__':
    main()
