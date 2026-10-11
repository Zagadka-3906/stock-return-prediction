"""Publish actual completed route repair, preserved failures, and native hook diagnostics on main."""
from pathlib import Path
import gzip
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(15)
    return read(f/'service_execution.json')


def main():
    out=A/'local_closed_dependency_recovery_v2_github_20261007';assert not out.exists();out.mkdir()
    terminal=closed('CPU_FULL_HGB44_round113_full_registration_v4')
    hook_terminal=closed('protected_upper_pool_HGB_selected_hook_preflight')
    monitor_terminal=closed('local_only_monitor_v11_actual_handoff')
    proof_path=A/'local_closed_dependency_recovery_v2_20261007.json';proof=read(proof_path)
    sources=[Path(__file__),proof_path,A/'prepare_local_closed_dependency_recovery_v2_20261007.py',
        A/'local_closed_dependency_recovery_actual14_hidden_launches_v2_20261007.json',
        A/'local_closed_dependency_recovery_resource_receipt_routes_v2_20261007.json',
        A/'CPU_FULL_HGB44_round113_source_route_preflight_v3_20261007.json',
        A/'CPU_ELASTIC44_round114_source_route_preflight_v2_20261007.json',
        *[A/n for n in [*proof['sources'],*proof['sources'].values()]],
        A/'observe_CPU_full_bank_resources_v4_20261007.py',A/'publish_CPU_full_bank_resource_observers_v4_20261007.py',
        A/'monitor_local_only_runtime_v11_20261007.py',A/'handoff_local_only_monitor_v11_20261007.py',
        A/'predict_protected_upper_pool_CPU_HGB_scheme_20261007.py',A/'verify_protected_upper_pool_HGB_selected_hook_20261007.py',
        A/'prepare_protected_upper_pool_HGB66_selected_candidate_20261007.py',A/'seal_protected_upper_pool_HGB66_selected_candidate_20261007.py',
        *list((A/'protected_upper_pool_HGB_selected_hook_preflight_20261007').glob('*.json')),
        *list((A/'local_only_monitor_v11_actual_handoff_20261007').glob('*.json')),
        *list((A/'protected_upper_pool_HGB66_score_publication_v2_actual_handoff_20261007').glob('*.json'))]
    for old,new in proof['services'].items():
        folder=A/'service_owned_workflows_20261006'/old
        assert not owned(read(folder/'native_launch.json'))
        sources += list(folder.glob('*.json'))+list(folder.glob('*.log'))
        f=A/'service_owned_workflows_20261006'/new
        sources += [f/n for n in ('job_definition.json','native_launch.json','launch_result.json','verified_hidden_launch.json')]
    for name in ('CPU_FULL_HGB44_round113_full_registration_v4','protected_upper_pool_HGB_selected_hook_preflight','local_only_monitor_v11_actual_handoff'):
        folder=A/'service_owned_workflows_20261006'/name
        sources+=list(folder.glob('*.json'))+list(folder.glob('*.log'))
    sources+=list((A/'CPU_FULL_HGB44_round113_actual_registration_v4_20261007').glob('*.json'))
    if terminal['status']=='passed':sources += [A/'optimization_20261003_r113/full_registration_execution.json',A/'github_validation_sync_main_20261005/round113_receipt.json']
    pins={str(p):sha(p) for p in dict.fromkeys(sources)}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'terminal113':terminal,'hook_terminal':hook_terminal,'monitor_terminal':monitor_terminal,'test_labels_read':False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    sync=helpers.sync;held=[];restore=install()
    try:
        main7=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(main7,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/local_closed_dependency_recovery_v2_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in dict.fromkeys([*sources,out/'frozen_before_main_publication.json']):
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                digest=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==digest;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'published_path':target,'original_sha256':digest,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_hash_route_recovery_failures_native_hook_controls_and_observer11',
                'at_local':sync.now(),'files':files,'only_branch':'main','previous_main':previous,'actual_round113_terminal':terminal,
                'preserved_old_terminal_count':len(proof['services']),'new_quality_scores_by_recovery':0,'new_native_fits_by_recovery':0,
                'original_HGB24_fits44_scores_and_anchor_inference_not_rerun':True,'actual_lower_pool_hook_terminal':hook_terminal,
                'hook603_historical_rows_not_complete_future_qualification':True,'round115_full_qualification_not_claimed':True,
                'scientific_workers_stopped_suspended_or_restarted':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('# 本机登记摘要路径修复及原生候选诊断\n\n'
                '113登记在写入首个生成文件前检测到摘要与旧预检查不同而退出。完整HGB24拟合、44项官方评分和锚点候选检查已通过，不重复执行。'
                '新版本对实际生成器的16个113/114源码重新计算并封存精确摘要，保留旧服务定义、原生身份、失败终态和日志。'
                '依赖旧登记而退出的ElasticNet尚未开始全量拟合；新服务仍需实际完成训练、评分、候选冻结、推理、完整QA和main。\n\n'
                '新增低分区候选钩子在603行历史特征、合成日期上实际运行原生HGB重载、独立解码、Pandas对照及201/402行完整日期前缀。'
                '这项诊断不代替完整父模型执行、1599600行候选或真实80日检查。资格以未来冻结后的实际结果为准。'
                '当前实际113、诊断和监控状态见manifest及原终态；不把启动检查或后续源码视为科学完成或资源穷尽。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','修复本机登记精确摘要依赖并保留失败历史及原生低分区候选诊断',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(data).hexdigest() for n,data in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'at_local':sync.now(),'branch':'main',
                'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,'all_source_inputs_initial_and_final_full_read_locked_rehash':True,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})


if __name__=='__main__':main()
