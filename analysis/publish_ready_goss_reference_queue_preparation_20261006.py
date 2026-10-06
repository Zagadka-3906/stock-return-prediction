"""Publish successful and failed GOSS setup controls as exact blobs on main."""
from pathlib import Path
import hashlib
import json
import sys
import time
import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
OUT=A/'ready_goss_reference_queue_preparation_github_20261006'
PREFIX=Path('validation_sync/ready_goss_reference_queue_preparation_20261006')


def main():
    import publish_classifier_consensus_workflows_20261006 as helpers
    from run_dependency_queue_v3_20261006 import owned,read,create
    from hidden_windows_child_creation_20261006 import install
    sync=helpers.sync
    assert not OUT.exists()
    proofs=[A/f'ready_goss_reference_{kind}_preflight_v2_20261006/verification.json' for kind in ('generator','execution')]
    for proof in proofs:
        value=read(proof);assert value['status']=='passed'
        for path,digest in value['source_sha256'].items():
            assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    assert [r['generated_records'] for r in read(proofs[0])['controls']]==[124,138,138]
    queue_proof=A/'ready_goss_reference_queue_preparation_20261006/verification.json'
    assert read(queue_proof)['status']=='passed_actual25_original_and_additional_routes_and_exact_dispatch_expression'
    for path,digest in read(queue_proof)['source_sha256'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    for name in ('gradient_sampling_memmap_complete_bank_v3_publication','gradient_sampling_native_queue_handoff_v9_publication'):
        service=A/'service_owned_workflows_20261006'/name
        assert read(service/'service_execution.json')['status']=='passed'
        assert not owned(read(service/'native_launch.json'))
    sources=[Path(__file__),*A.glob('*ready_goss*20261006.py'),*A.glob('ready_goss_reference*20261006.json')]
    for number in (95,96):
        sources += list(A.glob(f'optimize_training_round{number}*.py'))+list(A.glob(f'finalize_training_round{number}*.py'))+list(A.glob(f'run_training_round{number}*pipeline.py'))
    for directory in ('ready_goss_reference_generator_preflight_20261006','ready_goss_reference_generator_preflight_v2_20261006','ready_goss_reference_execution_preflight_v2_20261006'):
        sources += list((A/directory).rglob('*.json'))
    sources += [A/'windows_and_work_status_20261006_095946.json']
    sources += list((A/'ready_goss_reference_queue_preparation_20261006').glob('*.json'))
    sources += [A/name for name in ('run_dependency_queue_v7_20261006.py','monitor_actual_optimization_progress_v29_20261006.py','watch_validations_main_v6_20261006.py','run_goss_reference_quality_qualified_workflow_20261006.py','run_goss_reference_quality_with_exact_rank_cache_20261006.py','lossless_ranking_runtime_adapter_v4_20261006.py','build_lossless_ranking_display_v5_20261006.py','goss_reference_lossless_publication_adapter_20261006.py')]
    targets={(PREFIX/'.gitattributes').as_posix():b'* -text\n'}; files={}
    for source in dict.fromkeys(sources):
        data=source.read_bytes();assert len(data)<5*1024**2 and not sync.SECRET.search(data),source
        if source.suffix=='.json':json.loads(data.decode('utf-8-sig'))
        destination=source.relative_to(ROOT) if source.parent==A and source.suffix=='.py' else PREFIX/source.relative_to(ROOT)
        targets[destination.as_posix()]=data
        files[source.relative_to(ROOT).as_posix()]={'published_path':destination.as_posix(),'raw_sha256':hashlib.sha256(data).hexdigest()}
    OUT.mkdir();restore=install();suspended=[]
    try:
        pub=read(A/'service_owned_workflows_20261006/main_publisher_v5/native_launch.json');assert owned(pub)
        root,worker=helpers.owned_pair(pub['pid'],Path(pub['script']),pub['script_args'])
        for attempt in range(300):
            for process in (worker,root):process.suspend();suspended.append(process)
            busy=[p for p in root.children(recursive=True) if p.pid!=worker.pid and p.name().lower()!='conhost.exe']
            if not busy:break
            for p in reversed(suspended):p.resume()
            suspended.clear();time.sleep(1)
        else:raise RuntimeError('Publisher still owns an active publication child')
        previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
        targets[(PREFIX/'manifest.json').as_posix()]=sync.encoded({'status':'passed_actual25_routes_and_prospective_queue_quality_not_yet_run','previous_main':previous,'at_local':sync.now(),'files':files,'required_additional_rounds':[95,96],'explicit_parents':[84,95],'prespecified_complete_records':[124,138],'original67_through94_retained':True,'failed_original_generator_control_preserved':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False,'only_publication_branch':'main'})
        targets[(PREFIX/'README.md').as_posix()]=('调度扩展准备：25条实际原始及新增路由和调度表达式检查通过；全部原23条待办定义与父方案保持。新队列、进度采集与main发布入口仅完成源代码准备，尚未替换当前后台服务。需完成真实接管后才能执行第95/96轮。\n\n'+'# GOSS新增完整方案比较准备检查\n\n第95轮以合格第84轮为基准比较124条用途、组合、权重及后处理；第96轮以合格第95轮为基准比较138条独立主模型及后处理。复用已有30个年度和6个最终300树模型，原第67—94轮全部保留。\n\n两轮生成控制共124/138/138条，实际驱动、版本化前序工厂、候选源码打包与原生路由检查通过。原生成声明误将84条改为编号96的失败及源代码均保留，修正版使用v3工厂。控制排序值为合成值，不计真实官方质量评分；262条完整连续验证、冻结、因果检查、全量推理及完整榜更新仍待执行。\n\n只上传源代码和记录；模型与数据保持D/E盘。使用相同2020—2024年5,635,800行、1,212连续交易日的官方综合分，未读取测试标签，未声称资源边界完成。\n').encode('utf-8')
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        selected=sorted(targets)
        for offset in range(0,len(selected),50):sync.git('add','-f','--',*selected[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(selected)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','核验GOSS第95与96轮调度及25条原始和新增路由',timeout=180)
        commit=sync.git('rev-parse','HEAD');expected={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
        assert helpers.blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
        receipt={'status':'pushed_actual_controls_main_only','at_local':sync.now(),'commit':commit,'raw_git_blobs_verified':len(expected),'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+PREFIX.as_posix()}
        create(OUT/'receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    except BaseException as error:
        create(OUT/'failure.json',{'status':'failed_preserved_publication_attempt','error':f'{type(error).__name__}: {error}'});raise
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
        create(OUT/'actual_hidden_publication_children.json',{'actual_CreateProcess_calls':restore()})


if __name__=='__main__':main()
