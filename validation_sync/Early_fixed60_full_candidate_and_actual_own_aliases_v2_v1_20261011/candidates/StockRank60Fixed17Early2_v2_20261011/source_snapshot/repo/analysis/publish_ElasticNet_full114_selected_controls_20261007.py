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
    diagnostic=closed('ElasticNet_selected_hook_preflight')
    folder=A/'ElasticNet_selected_hook_preflight_20261007';proof=read(folder/'verification.json')
    assert proof['status']=='passed_actual_four_ElasticNet_diagnostic_models_and42_selected_hook_rank_CDF_full_prefix_controls'
    routes=A/'CPU_ELASTIC44_round114_source_route_preflight_20261007.json';assert read(routes)['status']=='passed_prospective_eight_source_AST_and_original_QA_reverse_routes_only'
    out=A/'ElasticNet_full114_selected_controls_github_20261007';assert not out.exists();out.mkdir()
    names=['cpu_full_universe_ElasticNet_native_bank24','full_universe_ElasticNet44_official_comparison','cpu_full_universe_ElasticNet24_bank_evidence_publication_v2','cpu_full_universe_ElasticNet24_scores_evidence_publication_v2','CPU_ELASTIC44_selected_candidate_preparation','CPU_ELASTIC44_selected_candidate_sealing','CPU_ELASTIC44_round114_full_registration']
    rows={n:read(A/'service_owned_workflows_20261006'/n/'native_launch.json') for n in names};assert all(owned(r) for r in rows.values())
    create(out/'actual_hidden_workflow_dispatch_snapshot.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'identities':rows,'all_strong_owned_live_now':True,'all_console_handles_zero':all(r['actual_native_console_handle']==0 for r in rows.values()),'planned_full_native_fits':24,'planned_official_records':44,'future_inference_after_actual44_selection_only':True,'expected_round114_fullQA25':True,'actual_full_selection_fits':0,'actual_official_records':0,'remote_workers':0,'test_labels_read':False})
    sources=[Path(__file__),folder/'verification.json',folder/'frozen_before_actual_controls.json',routes,A/'ElasticNet44_full114_workflow_admission_20261007.json',out/'actual_hidden_workflow_dispatch_snapshot.json']
    sources += [A/n for n in ('predict_full_universe_CPU_ElasticNet_rank_CDF_scheme_20261007.py','prepare_CPU_ELASTIC_residual44_selected_candidate_20261007.py','seal_CPU_ELASTIC_residual44_selected_candidate_20261007.py','prepare_CPU_ELASTIC44_round114_sources_20261007.py','run_CPU_ELASTIC44_round114_full_registration_20261007.py','verify_ELASTIC44_round114_sources_20261007.py','verify_ElasticNet_selected_hook_20261007.py','CPU_ELASTIC44_selected_candidate_source_admission_20261007.json','CPU_ELASTIC44_round114_full_registration_admission_20261007.json','ElasticNet_selected_hook_preflight_admission_20261007.json','ElasticNet63_actual_controls_and_workflows_github_20261007/receipt.json')]
    for n in [*names,'ElasticNet_selected_hook_preflight']:
        service=A/'service_owned_workflows_20261006'/n;sources += [service/f for f in ('job_definition.json','native_launch.json','verified_hidden_launch.json')]
        if n=='ElasticNet_selected_hook_preflight':sources += [service/'service_execution.json',service/'stdout.log',service/'stderr.log']
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
            prefix = Path('validation_sync/ElasticNet_full114_selected_controls_20261007')
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
            manifest={'status':proof['status'],'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main','actual_new_selected_hook_diagnostic_fits':4,'earlier_codec_diagnostic_fits':4,'actual_diagnostic_iteration_cap':2000,'actual_selected_hook_heads':7,'actual_selected_hook_weights_each':6,'actual_selected_hook_combinations':42,'actual_full_selection_fits':0,'actual_official_scores':0,'all_generated_registry_measured_fields_covered_by_actual_full_pool_scorer_item_schema':True,'actual_publish_and_lossless_round114_call_arguments_verified':True,'original_full_QA_helpers_reverse_source_routes_exact':True,'future_actual24_training_44_scores_candidate_full1599600_and_fullQA25_not_claimed':True,'all7_hidden_local_dispatches_owned_now':True,'remote_workers_dispatched':0,'scientific_workers_stopped_or_restarted':0,'exact_idle_main_before_and_after_hold':idle,'test_labels_read':False}
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded(manifest)
            payload[(prefix/'README.md').as_posix()]=('# ElasticNet选中推理与第114轮完整榜准备\n\n'
                '另有4个真实历史512条训练诊断模型使用完整实际候选的分列预处理、目标缩放和原生ElasticNet参数。实际推理钩子在7种单模型/集成及6种权重共42组上执行：原生重载、独立系数解码、独立Pandas同日秩、按声明顺序均值和同日CDF，以及两种冷日期前缀均逐位通过。'
                '使用显式合成的未来日期上下文和实际历史特征，不读取真实未来特征或真实测试标签。弱正则诊断迭代上限及真实dual_gap/告警原样记录，不据此添加官方计分淘汰条件。\n\n'
                '八条登记/优化/发布/完整榜生成路由通过AST检查，原QA帮助代码反向恢复字节一致。登记字段已与实际44项评分记录源码字典交叉核对，publish和lossless实参均为114，完整QA25和六视图/45秒检查保留。'
                '选择44项完整历史收益映射CSV官方总分最高者，新方案先冻结所有代码、参数、模型和映射，再执行1599600行双重重载、独立解码、冷80日前缀和CSV复现；相同106锚点需完整预测位、8项指标、图和封存文件核对才复用。\n\n'
                '7个本机隐藏服务实际存活，完整24次训练及44项评分尚待前序第113轮QA24/main。候选准备、封存及第114轮完整榜登记服务已排入依赖链。此证据不宣称完整训练评分或测试推理已完成。模型、预测、数据留D盘，只main，选择偏差未校正。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '保存ElasticNet四个真实候选预处理模型42项完整推理钩子对照及第114轮完整榜路由', timeout=180)
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
