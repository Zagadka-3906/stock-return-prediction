"""Publish actual owned full-scope handoff and repaired observer evidence on main."""
from pathlib import Path
import hashlib
import json
import sys
import time
import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers

OUT=A/'ready_goss_reference_actual_handoff_github_20261006'
PREFIX=Path('validation_sync/ready_goss_reference_actual_handoff_20261006')


def main():
    service=A/'service_owned_workflows_20261006/ready_goss_full_execution_handoff'
    handoff=A/'ready_goss_reference_actual_handoff_20261006'
    while not (service/'service_execution.json').exists():
        assert not (handoff/'failure.json').exists(),read(handoff/'failure.json')
        if (service/'native_launch.json').exists():assert owned(read(service/'native_launch.json'))
        time.sleep(2)
    assert read(service/'service_execution.json')['status']=='passed'
    while owned(read(service/'native_launch.json')):time.sleep(.5)
    proof=read(handoff/'verification.json')
    assert proof['status']=='passed_actual_queue7_main6_monitor30_handoff_full_original_and_GOSS_scope'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    identities={key:proof[key] for key in ('actual_queue','actual_main_publisher','actual_observer')}
    assert all(owned(row) for row in identities.values())
    assert not OUT.exists();OUT.mkdir()
    generations=[]
    while len(generations)<2:
        assert owned(identities['actual_observer']) and owned(identities['actual_queue'])
        values=[read(A/name) for name in ('ongoing_optimization_state.json','resume_optimization_20261004.json','actual_optimization_monitor_state_20261005.json')]
        if len({v.get('complete_observer_generation') for v in values})==1:
            value=values[0];generation=value['complete_observer_generation']
            if value.get('actual_observer_version')==30 and value.get('actual_current_dependency_queue_identity',{}).get('owned_worker_pid')==identities['actual_queue']['owned_worker_pid'] and generation not in generations:
                assert value['gradient_sampling_actual_annual_fits']==30 and value['gradient_sampling_actual_final_fits']==6
                assert value['gradient_sampling_complete_future_controls_passed'] and value['gradient_sampling_original_routes_exposed']
                pending=set(value['pending_required_rounds']);qualified=set(value['qualified_rounds'])
                assert set((75,76,91,92,93,94,95,96))<=pending|qualified
                assert value['global_resource_exhaustion_established'] is False
                create(OUT/f'actual_complete_generation{len(generations)+1}.json',{'status':'passed_actual_monitor30_queue7_full_scope_generation','value':value,'monitor_state':values[2],'new_quality_scores':0,'test_labels_read':False})
                generations.append(generation)
        if len(generations)<2:time.sleep(2)
    sources=[Path(__file__),A/'handoff_ready_goss_full_execution_20261006.py',A/'prepare_goss_cost_schema_and_monitor30_20261006.py',A/'refresh_gradient_sampling_cost_evidence_20261005.py',A/'refresh_gradient_sampling_cost_evidence_v2_20261006.py',A/'monitor_actual_optimization_progress_v30_20261006.py',A/'GOSS_cost_schema_observer30_recovery_20261006.json',A/'GOSS_cost_schema_observer30_preflight_20261006.json',A/'service_owned_dependency_queue_v4_20261006/queue_plan_v7.json',A/'ready_goss_reference_queue_preparation_20261006/verification.json']
    sources += [A/name for name in ('run_dependency_queue_v7_20261006.py','watch_validations_main_v6_20261006.py','goss_reference_lossless_publication_adapter_20261006.py','run_goss_reference_quality_qualified_workflow_20261006.py','run_goss_reference_quality_with_exact_rank_cache_20261006.py','lossless_ranking_runtime_adapter_v4_20261006.py','build_lossless_ranking_display_v5_20261006.py')]
    for folder in (handoff,OUT):sources += sorted(folder.glob('*.json'))
    for name in ('ready_goss_full_execution_handoff','progress_monitor_v28','progress_monitor_v30','main_publisher_v5','main_publisher_v6','dependency_queue_v6','dependency_queue_v7','distribution_views_full_ranking_publisher'):
        folder=A/'service_owned_workflows_20261006'/name
        sources += sorted(folder.glob('*.json'))
        # Retain the exact observer failure, not large live progress logs.
        if name=='progress_monitor_v28':sources += [folder/'stderr.log']
    sync=helpers.sync;targets={(PREFIX/'.gitattributes').as_posix():b'* -text\n'};files={}
    for source in dict.fromkeys(sources):
        data=source.read_bytes();assert len(data)<5*1024**2 and not sync.SECRET.search(data),source
        if source.suffix=='.json':json.loads(data.decode('utf-8-sig'))
        destination=source.relative_to(ROOT) if source.parent==A and source.suffix=='.py' else PREFIX/source.relative_to(ROOT)
        targets[destination.as_posix()]=data;files[source.relative_to(ROOT).as_posix()]={'published_path':destination.as_posix(),'raw_sha256':hashlib.sha256(data).hexdigest()}
    restore=install();suspended=[]
    try:
        row=identities['actual_main_publisher'];assert owned(row)
        root,worker=helpers.owned_pair(row['pid'],Path(row['script']),row['script_args'])
        for _ in range(300):
            for p in (worker,root):p.suspend();suspended.append(p)
            busy=[p for p in root.children(recursive=True) if p.pid!=worker.pid and p.name().lower()!='conhost.exe']
            if not busy:break
            for p in reversed(suspended):p.resume()
            suspended.clear();time.sleep(1)
        else:raise RuntimeError('Main6 owns an active publication command')
        previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
        targets[(PREFIX/'manifest.json').as_posix()]=sync.encoded({'status':proof['status'],'at_local':sync.now(),'previous_main':previous,'files':files,'actual_live_identities':identities,'two_actual_complete_observer_generations':generations,'original67_through94_scope_retained':True,'additional95_96_records':262,'original_failed_observer28_preserved':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False,'only_publication_branch':'main'})
        targets[(PREFIX/'README.md').as_posix()]=('# GOSS新增完整搜索实际接管\n\n第95/96轮262条新增方案已经接入实际隐藏队列7，按合格第84/95轮为父方案。当前科学任务继续运行；新分支在当前任务释放评分位置后执行，原23条待办路由、原第67—94轮、198条分位树和262条分位组合方案均保留。每轮仍须完整连续官方评分、冻结、因果检查、全量候选和完整榜。\n\n主分支发布器6使用原完整评分发布和原始文件SHA核验，并接管93—96轮的完整不可变无损榜和全部浏览器检查。原93/94等待发布器转交后保留源代码及终止身份记录，不声称原服务自然完成。\n\n进度采集器28因旧代码要求elapsed_seconds字段而真实失败；原失败、源代码和错误日志保留。版本30已真实启动，核验两次完整更新、队列7实际进程及GOSS30/6个唯一模型。未记录的总耗时保持null，不用训练时长冒充；模型记录、预测数学和训练进程不修改。\n\n这些是实际接管和工程核验，不计新增质量分。95/96实际评分仍由后续完整运行产生。仅main发布；模型、数据和缓存保持D/E；不读取测试标签，不宣称资源边界或总目标完成。\n').encode('utf-8')
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        selected=sorted(targets)
        for offset in range(0,len(selected),50):sync.git('add','-f','--',*selected[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(selected)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','接入GOSS第95与96轮完整评分队列并修复实际进度采集与main发布',timeout=180)
        commit=sync.git('rev-parse','HEAD');expected={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
        assert helpers.blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
        receipt={'status':'pushed_actual_full_scope_handoff_main_only','at_local':sync.now(),'commit':commit,'raw_git_blobs_verified':len(expected),'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+PREFIX.as_posix()}
        create(OUT/'receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    except BaseException as error:
        create(OUT/'failure.json',{'status':'failed_preserved_handoff_publication','error':f'{type(error).__name__}: {error}'});raise
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
        create(OUT/'actual_hidden_publication_children.json',{'events':restore()})


if __name__=='__main__':main()
