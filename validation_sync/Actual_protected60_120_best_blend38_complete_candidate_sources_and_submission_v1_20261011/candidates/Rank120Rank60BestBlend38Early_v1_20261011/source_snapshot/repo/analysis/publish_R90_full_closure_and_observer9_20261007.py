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
    closed('local_only_monitor_v9_actual_handoff')
    closed('classifier_consensus_R90_root_resolution_recovery_v3')
    closed('CPU_MLP44_round110_full_registration')
    proof = read(A / 'local_only_monitor_v9_actual_handoff_20261007/verification.json')
    assert proof['status'] == 'passed_actual_idle_observer9_complete_single_host_R90_actual_QA4_qualification_generation'
    out = A / 'R90_full_closure_and_observer9_github_20261007'
    assert not out.exists()
    out.mkdir()
    audit_path=A/'R90_full_QA4_actual_closure_receipt_20261007/verification.json'
    audit=read(audit_path)
    assert audit['status']=='passed_actual_closed_R90_138_full_QA4_candidate_causality_and_main_receipt_links'
    sources=[Path(__file__),audit_path,*[Path(p) for p in audit['input_sha256']],A/'monitor_local_only_runtime_v9_20261007.py',A/'handoff_local_only_monitor_v9_20261007.py',A/'monitor_local_only_runtime_v8_20261007.py',A/'service_owned_workflows_20261006/local_only_progress_monitor_v8/administrative_supersession_local_v9_20261007.json']
    for name in ('local_only_monitor_v9_actual_handoff_20261007','classifier_consensus_R90_root_resolution_recovery_v3_20261007'):
        sources+=list((A/name).glob('*.json'))+list((A/name).glob('*.txt'))
    for name in ('local_only_monitor_v9_actual_handoff','classifier_consensus_R90_root_resolution_recovery_v3'):
        folder=A/'service_owned_workflows_20261006'/name
        sources+=list(folder.glob('*.json'))+list(folder.glob('*.log'))
    folder=A/'service_owned_workflows_20261006/local_only_progress_monitor_v9'
    sources += [folder / n for n in ('job_definition.json','verified_hidden_launch.json','native_launch.json')]
    sources+=list((A/'optimization_20261003_r90').glob('provenance_scope_execution_failed*.json'))
    pins = {**proof['input_sha256'], **audit['input_sha256'], **{str(p): sha(p) for p in sources}}
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
            prefix = Path('validation_sync/R90_full_closure_and_observer9_20261007')
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
            manifest={'status':'published_actual_R90_recovery_closure_and_observer9_actual_QA4_qualification',
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'R90_full_validation_commit':audit['commit'],'actual_full_QA_version':4,
                'actual_scored_records':138,'full_ranking_connected_records':12076,
                'actual_candidate_rows':1599600,'actual_native_models':14,'actual_causal_cases':8,
                'best_R90_score':audit['official_score'],'no_gain_over_current_qualified106':True,
                'original_publication_receipt_not_modified':True,'failed_history_archives_preserved':True,
                'new_native_fits':0,'new_official_scores':0,'new_inference':False,
                'scientific_workers_stopped_or_restarted':0,'remote_workers_dispatched':0,
                'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 第90轮完整验证及恢复执行闭合补充\n\n'
                '原138项评分全部完成，最高官方综合分0.4510531893859833；未超过第106轮0.45110171046668335。'
                '候选1599600行、344日、4650股，14个原生模型的加载回放、管线回放、CSV和80天冷前缀检查均通过。'
                '已完成8项整方案标签污染与冷前缀检查，以及12076条完整榜的全部原核验和六种浏览器视图。\n\n'
                f"本轮完整发布提交为{audit['commit']}，2341个发布文件的原始Git内容哈希已核验。"
                '此处补传修复驱动的最终证明、执行桥文本、原冻结输入、实际隐藏子进程和全部失败历史。'
                '原完整轮收据不含QA版本字段，保持原字节；新增旁证明确链接实际QA4文件。\n\n'
                '监控九代从实际QA文件、原main收据和自然闭合服务确认资格，修正旧收据字段假设导致的错误待完成显示。'
                '监控交接仅替换精确空闲观察进程，没有停止或重启科学训练、评分或排序缓存测速。'
                '本补充没有新训练、评分或推理。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '补全第90轮实际恢复闭合与QA4证据并修正监控收据兼容', timeout=180)
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
