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
    diagnostic=closed('full_universe_HGB_selected_hook_preflight')
    closed('full_universe_HGB113_schema_v2_actual_handoff')
    handoff=A/'full_universe_HGB113_registry_schema_v2_actual_handoff_20261007/verification.json'
    assert read(handoff)['status']=='passed_actual_idle_fullHGB113_helper_schema_correct_v2_handoff'
    folder=A/'full_universe_HGB_selected_hook_preflight_20261007'
    proof=read(folder/'verification.json')
    assert proof['status']=='passed_actual_four96_tree_diagnostic_models_and42_selected_hook_rank_CDF_full_prefix_controls'
    routes=A/'CPU_FULL_HGB44_round113_source_route_preflight_v2_20261007.json';assert read(routes)['status']=='passed_prospective_eight_source_AST_and_original_QA_reverse_routes_only'
    out=A/'full_universe_HGB_full113_route_controls_v2_github_20261007';assert not out.exists();out.mkdir()
    names=['cpu_full_universe_HGB_native_bank24','full_universe_HGB44_official_comparison_v2','cpu_full_universe_HGB24_bank_evidence_publication','cpu_full_universe_HGB24_scores_evidence_publication','CPU_FULL_HGB44_selected_candidate_preparation','CPU_FULL_HGB44_selected_candidate_sealing','CPU_FULL_HGB44_round113_full_registration_v2']
    rows={n:read(A/'service_owned_workflows_20261006'/n/'native_launch.json') for n in names};assert all(owned(r) for r in rows.values())
    create(out/'actual_hidden_workflow_dispatch_snapshot.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'identities':rows,'all_strong_owned_live_now':True,'all_console_handles_zero':all(r['actual_native_console_handle']==0 for r in rows.values()),'planned_full_native_fits':24,'planned_official_records':44,'future_inference_after_actual44_selection_only':True,'expected_round113_fullQA24':True,'actual_selection_fits':0,'actual_official_records':0,'remote_workers':0,'test_labels_read':False})
    sources=[Path(__file__),folder/'verification.json',folder/'frozen_before_actual_controls.json',routes,A/'full_universe_HGB24_44_full113_workflow_admission_20261007.json',out/'actual_hidden_workflow_dispatch_snapshot.json']
    sources += [A/n for n in ('publish_cpu_full_universe_HGB24_evidence_20261007.py','predict_full_universe_CPU_HGB_rank_CDF_scheme_20261007.py','prepare_CPU_FULL_HGB_residual44_selected_candidate_20261007.py','seal_CPU_FULL_HGB_residual44_selected_candidate_20261007.py','prepare_CPU_FULL_HGB44_round113_sources_v2_20261007.py','run_CPU_FULL_HGB44_round113_full_registration_v2_20261007.py','verify_FULL_HGB44_round113_sources_v2_20261007.py','verify_full_universe_HGB_selected_hook_20261007.py','CPU_FULL_HGB44_selected_candidate_source_admission_v2_20261007.json','CPU_FULL_HGB44_round113_full_registration_admission_v2_20261007.json','full_universe_HGB_selected_hook_preflight_admission_20261007.json')]
    for n in [*names,'full_universe_HGB_selected_hook_preflight']:
        service=A/'service_owned_workflows_20261006'/n;sources += [service/f for f in ('job_definition.json','native_launch.json','verified_hidden_launch.json')]
        if n=='full_universe_HGB_selected_hook_preflight':sources += [service/'service_execution.json',service/'stdout.log',service/'stderr.log']
    sources += [handoff,A/'handoff_full_universe_HGB113_registry_schema_v2_20261007.py',A/'full_universe_HGB113_registry_schema_v2_actual_handoff_20261007/frozen_before_handoff.json',A/'service_owned_workflows_20261006/CPU_FULL_HGB44_round113_full_registration/administrative_supersession_full_HGB113_schema_v2_20261007.json',A/'prepare_CPU_FULL_HGB44_round113_sources_20261007.py',A/'CPU_FULL_HGB44_round113_source_route_preflight_20261007.json',A/'full_universe_HGB_full113_route_controls_github_20261007/receipt.json']
    pins={**proof['input_sha256'],**read(routes)['input_sha256'],**{str(p.resolve()):sha(p) for p in sources}}
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
            prefix = Path('validation_sync/full_universe_HGB_full113_route_controls_v2_20261007')
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
            manifest={'status':proof['status'],'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main','actual_diagnostic_fits':4,'actual_diagnostic_trees_each':96,'actual_selected_hook_heads':7,'actual_selected_hook_weights_each':6,'actual_selected_hook_combinations':42,'actual_selection_fits':0,'actual_official_scores':0,'original_eight_registry_and_QA_routes_AST_and_reverse_unchanged_helpers_passed':True,'actual_publish_and_lossless_round113_call_arguments_verified':True,'all_generated_registry_measured_fields_covered_by_actual_full_pool_scorer_item_schema':True,'original_prospective_routes_did_not_check_full_pool_record_schema':True,'zero_science_old_idle_registration_helper_superseded':True,'future_actual24_training_44_scores_candidate_full1599600_and_fullQA24_not_claimed':True,'planned_future_cases':44,'all_hidden_local_dispatches_owned_now':True,'remote_workers_dispatched':0,'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded(manifest)
            payload[(prefix/'README.md').as_posix()]=('# 全股票池HGB正式候选路径及第113轮准备\n\n'
                '4个真实96轮历史小样本HGB模型实际保存重载，以原生预测和独立NumPy解码比较。实际选中推理钩子在7种单模型/均值集成、6种权重共42组配置中执行，百分位秩、CDF及完整/日期前缀逐位一致。'
                '日期上下文为显式合成未来日期，输入特征为真实历史样本，不读取实际未来特征或真实测试标签。该诊断不冒充24次完整选模训练或44项官方评分。\n\n'
                '完整候选按全部44项原官方连续向前分数选优；新方案先冻结代码、原生模型、图、校准，再执行1599600行双重重载、独立解码、冷80日和CSV复现；相同106锚点仅在全部字节、指标及封存文件核对后复用。'
                '第113轮登记44条记录，完整榜六视图、全部参数来源、45秒浏览器QA24及main同步沿用完整检查。八条生成源路由及实际113发布/榜单调用参数已核对。V2另将登记器所有measured字段与实际全股票池评分源码的记录字典交叉检查；删除原条件残差模板的非涨停不变断言，要求真实全股票池2020模型与三个冷前缀检查。原准备检查只覆盖源路由，尚未执行登记；仅把0评分的精确空闲登记辅助进程移交V2。\n\n'
                '银行、评分、发布、候选准备、封存与完整登记的7个本机隐藏服务实际已派发，仍待实际完整训练/评分完成。仅main；模型、预测及数据留D盘。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存全股票池HGB四个96轮真实模型42项推理钩子对照及完整第113轮路由', timeout=180)
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
