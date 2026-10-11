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
    for name in ('cpu_full_universe_HGB63_codec_preflight','full_universe_HGB44_transform_route_preflight_v2','full_universe_HGB44_bad_route_idle_supersession_v2','classifier_consensus_R90_root_resolution_preflight'):
        closed(name)
    proof=read(A/'cpu_full_universe_HGB63_codec_preflight_20261007/verification.json')
    assert proof['status']=='passed_actual_four_full_universe63_feature_HGB_native_codec_prefix_and_maturity_controls'
    route=read(A/'full_universe_HGB44_transform_route_preflight_v2_20261007/verification.json')
    assert route['status']=='passed_actual_full_universe_tie_CDF_prefix_future_poisoning_and_precise109_QA20_112_QA23_prospective44_routes'
    root=read(A/'classifier_consensus_R90_root_resolution_preflight_20261007/verification.json')
    assert root['status']=='passed_actual_six_R90_standalone_root_empty_foundation_and_exact_original_hybrid_and_negative_controls'
    out=A/'full_universe_HGB_and_R90_root_controls_github_20261007';assert not out.exists();out.mkdir()
    filenames=['cpu_full_universe_HGB_bank24_plan_20261007.json','cpu_full_universe_HGB_bank24_admission_20261007.json','train_cpu_full_universe_HGB_bank24_20261007.py','verify_cpu_full_universe_HGB63_codec_20261007.py','cpu_numerical_HGB_large_batch_codec_v2_20261007.py','full_universe_HGB_percentile_CDF_transform_20261007.py','run_full_universe_HGB44_official_comparison_20261007.py','run_full_universe_HGB44_official_comparison_v2_20261007.py','full_universe_HGB44_official_comparison_admission_20261007.json','full_universe_HGB44_official_comparison_v2_admission_20261007.json','verify_full_universe_HGB44_transform_routes_20261007.py','verify_full_universe_HGB44_transform_routes_v2_20261007.py','full_universe_HGB44_route_correction_v2_20261007.json','retire_inactive_full_universe_HGB44_bad_route_20261007.py','retire_inactive_full_universe_HGB44_bad_route_v2_20261007.py','classifier_consensus_standalone_root_resolution_runtime_20261007.py','verify_classifier_consensus_R90_root_resolution_20261007.py','optimization_20261003_r90/provenance_scope_execution_failed_original_20261007.json','cpu_HGB_large_batch20_benchmark_github_20261007/receipt.json']
    sources=[Path(__file__),*[A/n for n in filenames]]
    for folder in ('cpu_full_universe_HGB63_codec_preflight_20261007','full_universe_HGB44_transform_route_preflight_20261007','full_universe_HGB44_transform_route_preflight_v2_20261007','classifier_consensus_R90_root_resolution_preflight_20261007'):
        sources += [A/folder/n for n in ('verification.json','frozen_before_actual_controls.json' if folder=='cpu_full_universe_HGB63_codec_preflight_20261007' else 'frozen_before_actual_root_controls.json' if 'R90_root' in folder else 'frozen_before_actual_controls.json')]
    sources += [A/'full_universe_HGB44_bad_route_idle_supersession_v2_20261007/verification.json']
    for name in ('cpu_full_universe_HGB63_codec_preflight','full_universe_HGB44_transform_route_preflight','full_universe_HGB44_transform_route_preflight_v2','full_universe_HGB44_bad_route_idle_supersession','full_universe_HGB44_bad_route_idle_supersession_v2','classifier_consensus_R90_root_resolution_preflight'):
        folder=A/'service_owned_workflows_20261006'/name;sources += list(folder.glob('*.json'))+list(folder.glob('*.log'))
    for name in ('cpu_full_universe_HGB_native_bank24','full_universe_HGB44_official_comparison_v2','full_universe_HGB44_official_comparison'):
        folder=A/'service_owned_workflows_20261006'/name;sources += [folder/n for n in ('job_definition.json','native_launch.json','verified_hidden_launch.json')]
    sources += [A/'service_owned_workflows_20261006/full_universe_HGB44_official_comparison/administrative_supersession_for_full_universe_HGB44_v2_20261007.json']
    folder=A/'service_owned_dependency_queue_v12_local_cache_20261007/activated_jobs/round90';sources+=list(folder.glob('*.json'))+list(folder.glob('*.log'))
    pins={}
    for inputs in (proof['input_sha256'],route['input_sha256'],root['input_sha256'],{str(p.resolve()):sha(p) for p in sources}):
        for name,digest in inputs.items():
            assert name not in pins or pins[name]==digest,name
            pins[name]=digest
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
            prefix = Path('validation_sync/full_universe_HGB_and_R90_root_controls_20261007')
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
            manifest={'status':'actual_four_global_HGB_diagnostics_and_precise44_routes_and_six_R90_root_controls',
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'actual_global63_feature_HGB_diagnostic_fits':4,'actual_global24_selection_fits':0,
                'actual_new_full_universe44_official_scores':0,'R90_actual_original_failed_attempt_scores':0,
                'R90_original_failed_scope_archived_byte_exact':True,'R90_six_root_lookup_controls_passed':True,
                'R90_138_scientific_retry_not_yet_started':True,'original_scientific_worker_termination_or_restart_by_this_publication':0,
                'known_incorrect_unstarted44_helper_only_administratively_retired':True,
                'initial_failed_administrative_guard_preserved_no_process_action_then':True,
                'native24_training_and44_scoring_admitted_but_waiting_actual112_and_RAM':True,
                'remote_workers_dispatched':0,'new_model_selection_scores_by_this_publication':0,
                'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 全股票池HGB原生检查与第90轮独立根模型读取顺序检查\n\n'
                '四种63特征全股票池配置完成了4次历史小样本诊断拟合，原生256/8192行、独立解码和前缀逐位一致；未来标签污染及负对照通过。'
                '24次完整2020至2024年度向前及2025最终训练尚未执行，44项完整官方评分尚未执行；服务等待第112轮完整验证及内存。\n\n'
                '排队评分源的第109轮QA版本号误写为24，实际应为20。旧源和首次弱静态控制保留；新V2控制同时核验109/20和112/23。'
                '仅精确空闲且零评分的旧助手被行政替换；首次替换保护因第90轮已自然失败而拒绝，记录完整保留。\n\n'
                '第90轮原尝试在独立根模型首次未来推理之前，先读取尚不存在的自身candidate verification，从而自然失败，138项评分均未开始。'
                '6个真实独立图均复现此错误；新运行实现提前返回原函数本就应返回的空基础模型字典。'
                '历史基础模型字典逐项一致，非独立图的缺失目录负对照仍拒绝，函数绑定全部恢复。'
                '原失败scope逐字节复制归档；真实138项重试尚未启动，没有候选完成或资源边界声明。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存全股票池HGB四种真实诊断和44项准备纠错及第90轮六个真实独立图读取顺序检查', timeout=180)
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
