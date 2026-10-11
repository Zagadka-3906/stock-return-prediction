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
    current=A/'service_owned_workflows_20261006/classifier_consensus_R90_root_resolution_recovery'
    identity=read(current/'native_launch.json');assert owned(identity)
    proof=read(A/'classifier_consensus_R90_root_resolution_preflight_20261007/verification.json')
    assert proof['status']=='passed_actual_six_R90_standalone_root_empty_foundation_and_exact_original_hybrid_and_negative_controls'
    folder=A/'classifier_consensus_R90_root_resolution_recovery_20261007'
    while not (folder/'frozen_before_actual_root_resolution_recovery.json').exists():
        assert owned(identity);time.sleep(1)
    frozen=read(folder/'frozen_before_actual_root_resolution_recovery.json')
    assert sha(A/'optimization_20261003_r90/protocol.json')==frozen['existing_protocol_sha256']
    assert sha(A/'optimization_20261003_r90/provenance_scope_execution_failed_location_archive_20261007.json')==frozen['original_failed_scope_sha256']
    out=A/'R90_actual_root_recovery_dispatch_github_20261007';assert not out.exists();out.mkdir()
    create(out/'actual_live_dispatch_snapshot.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_worker_identity':identity,'strong_owned_live_at_snapshot':owned(identity),'phase':read(A/'ongoing_optimization_r90_state.json'),'original_protocol_sha256':frozen['existing_protocol_sha256'],'actual_official_record_count_not_yet_qualified':sum(len(read(p)['results']) for p in (A/'optimization_20261003_r90').glob('wave*_results.json')),'available_RAM_GiB':psutil.virtual_memory().available/2**30,'full138_qualification_and_main_not_claimed':True,'test_labels_read':False})
    sources=[Path(__file__),A/'run_classifier_consensus_R90_root_resolution_recovery_20261007.py',A/'classifier_consensus_R90_root_resolution_recovery_admission_20261007.json',A/'classifier_consensus_standalone_root_resolution_runtime_20261007.py',A/'classifier_consensus_R90_root_resolution_preflight_20261007/verification.json',A/'R90_failed_scope_canonical_non_pinning_audit_20261007.json',A/'full_universe_HGB_and_R90_root_controls_github_20261007/receipt.json',A/'optimization_20261003_r90/provenance_scope_execution_failed_original_20261007.json',A/'optimization_20261003_r90/provenance_scope_execution_failed_location_archive_20261007.json',out/'actual_live_dispatch_snapshot.json']
    sources += [folder/n for n in ('effective_original_R90_bridge.txt','frozen_before_actual_root_resolution_recovery.json','actual_failed_scope_location_archival.json')]
    sources += [current/n for n in ('job_definition.json','native_launch.json','verified_hidden_launch.json')]
    pins={**frozen['input_sha256'],**{str(p.resolve()):sha(p) for p in sources}}
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
            prefix = Path('validation_sync/R90_actual_root_recovery_dispatch_20261007')
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
            manifest={'status':'actual_new_R90_root_order_recovery_dispatched_same_frozen138_grid',
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'original_protocol_bytes_unchanged':True,'old_failed_scope_archives_byte_identical':True,
                'actual_six_root_source_positive_and_negative_controls_passed':True,
                'actual_new_worker_hidden_dispatch_and_freeze_and_build_started':True,
                'original138_scientific_complete_qualification_not_yet_claimed':True,
                'new_model_selection_scores_by_this_publication':0,'new_native_fits':0,
                'remote_workers_dispatched':0,'scientific_workers_stopped_or_restarted_by_this_publication':0,
                'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 第90轮原138项验证的实际恢复启动\n\n'
                '6个真实独立方案的根模型读取顺序修复与非独立缺失目录负对照已实际通过并同步main。'
                '原第90轮协议和全部数学源字节保持不变；只有已冻结协议复用的启动条件及空独立基础模型字典的读取顺序修正。\n\n'
                '原失败记录有两份字节相同的完整归档；经固定元数据引用检查，原未被绑定的失败位置移到历史归档，新本轮最终scope待实际执行后新建。'
                '新增实际执行代码有独立的Windows只读共享锁、初末完整哈希和恢复执行元数据。\n\n'
                '新工作者已真正隐藏启动，并通过原协议复核进入build。此记录仅证明启动和检查，不声称138项评分、候选冻结推理、完整榜或main最终资格已完成。'
                '原GPU训练保持运行；官方评分、年度成熟边界、所有138项网格及全部QA保持原流程。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存第90轮原138项独立模型验证修复后实际隐藏启动与原协议复用和失败归档证据', timeout=180)
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
