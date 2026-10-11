"""Publish complete prospective or actual adoption evidence with main-only raw blobs."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers

def main(phase):
    assert phase in ('prospective','actual')
    source=A/('joint_goss_round97_queue_preparation_20261006' if phase=='prospective' else 'joint_goss_round97_actual_handoff_20261006')
    proof=read(source/'verification.json')
    expected=('passed_all_original25_routes_preserved_and_additive151_record_dispatch_and_owner_controls'
        if phase=='prospective' else 'passed_actual_queue10_main7_observer34_additive_joint97_handoff')
    assert proof['status']==expected
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    out=A/f'joint_goss_round97_{phase}_github_20261006'
    assert not out.exists();out.mkdir()
    prefix=Path(f'validation_sync/joint_goss_round97_{phase}_20261006')
    sources={p for p in A.glob('*joint_goss*20261006.py')}
    sources.update(A/f'{stem}97{suffix}.py' for stem in ('optimize_training_round','finalize_training_round') for suffix in ('','_v1','_v2','_v3'))
    sources.update(A/f'run_training_round97{suffix}_pipeline.py' for suffix in ('','_v1','_v2','_v3'))
    sources.update(A/name for name in ('lossless_ranking_runtime_adapter_v5_20261006.py',
        'build_lossless_ranking_display_v6_20261006.py','verify_lossless_ranking_display_v7_20261006.py',
        'watch_validations_main_v7_20261006.py',
        *[f'run_dependency_queue_v{v}_20261006.py' for v in (8,9,10)],
        *[f'monitor_actual_optimization_progress_v{v}_20261006.py' for v in (32,33,34)]))
    sources.update(A/f'joint_goss_membership_{name}_v{v}_20261006.json' for name in ('quality_run','round97_previous_run') for v in (1,2,3))
    folders=[A/'joint_membership_retention_scope_20261006',
        *[A/f'joint_goss_membership_generator_preflight_v{v}_20261006' for v in (1,2,3)],
        *[A/f'joint_goss_round97_full_launcher_preflight_v{v}_20261006' for v in (1,2,3,4)],
        A/'joint_goss_round97_preparation_recovery_20261006',A/'joint_goss_round97_queue_preparation_20261006']
    if phase=='actual':
        folders.append(source)
        sources.add(A/'service_owned_dependency_queue_v4_20261006/queue_plan_v10.json')
        for name in ('dependency_queue_v10','main_publisher_v7','progress_monitor_v34'):
            sources.update(A/f'service_owned_workflows_20261006/{name}/{file}' for file in ('job_definition.json','native_launch.json','verified_hidden_launch.json'))
        for name in ('dependency_queue_v7','main_publisher_v6','progress_monitor_v31'):
            sources.add(A/f'service_owned_workflows_20261006/{name}/administrative_supersession_for_joint97_20261006.json')
    for folder in folders:
        assert folder.exists(),folder
        sources.update(folder.rglob('*.json'))
    sync=helpers.sync;targets={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
    for path in sorted(sources):
        data=path.read_bytes()
        assert len(data)<5*1024**2 and not sync.SECRET.search(data),path
        target=path.relative_to(ROOT) if path.parent==A and path.suffix=='.py' else prefix/path.relative_to(ROOT)
        targets[target.as_posix()]=data
        files[path.relative_to(ROOT).as_posix()]={'published_path':target.as_posix(),'raw_sha256':hashlib.sha256(data).hexdigest()}
    live=[read(A/f'service_owned_workflows_20261006/{name}/native_launch.json') for name in ('main_publisher_v7','main_publisher_v6')
          if (A/f'service_owned_workflows_20261006/{name}/native_launch.json').exists()]
    row=next(r for r in live if owned(r))
    root,worker=helpers.owned_pair(row['pid'],Path(row['script']),row['script_args'])
    suspended=[];restore=install()
    try:
        for _ in range(180):
            for p in (worker,root):p.suspend();suspended.append(p)
            busy=[p for p in root.children(recursive=True) if p.pid!=worker.pid and p.name().lower()!='conhost.exe']
            if not busy:break
            for p in reversed(suspended):p.resume()
            suspended.clear();time.sleep(1)
        else:raise RuntimeError('Main publisher still owns an active publication command')
        previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous)
        assert not sync.git('status','--porcelain')
        targets[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':proof['status'],'phase':phase,
            'previous_main':previous,'at_local':sync.now(),'files':files,
            'full151_actual_scores_candidate_causal_full_ranking_still_pending':True,
            'new_quality_scores_by_controls':0,'new_native_fits':0,'test_labels_read':False,'only_publication_branch':'main'})
        targets[(prefix/'README.md').as_posix()]=('''# 第97轮：GOSS成员权重与高留存率联合搜索

训练集内部补测6个已完成原生训练的GOSS模型，每个模型保留非零成员权重的局部细搜起点。三阶段73、24、54条，共151条；权重0.0001、0.005、0.025，首次留存率0.984、0.99、0.995、0.998，最终留存率0.995、0.998、0.999。用途组合使用完整闭合第95轮的训练内部评分。

三种合成胜出情形的覆盖控制通过；实际共享后处理函数确认正权重时高留存率改变输出。合成控制值不是官方分数。完整启动链绑定版本3搜索、发布和候选复制，原官方缓存执行不改评分；完整榜六种视图、全部记录、45秒浏览器复核及来源检查保留。原第93—96轮完整发布路由保留，第97轮使用151条和完整QA版本7。历史候选复制路径错误、版本绑定错误、准备顺序错误及失败证据全部保留。

第97轮必须在第95轮完整闭合后执行5635800行、1212日、4650股票的连续官方验证，再冻结方案、过去成熟标签收益映射、实际CSV复评、1599600行全量候选、原生重载/冷80日前缀、方法因果检查和完整榜。此处不宣称151条已经评分，也不计入合格榜。所有原第67—96轮保留，新模型训练次数0，不读取测试标签；数据与模型D/E盘，所有上传只到main。
''').encode('utf-8')
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        selected=sorted(targets)
        for offset in range(0,len(selected),50):sync.git('add','-f','--',*selected[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert staged and staged<=set(selected)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m',
            '记录GOSS第97轮151项联合搜索及完整检查和保留失败证据' if phase=='prospective' else '接入第97轮实际完整队列并核验main发布与真实进程保留',timeout=180)
        commit=sync.git('rev-parse','HEAD')
        hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
        assert helpers.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_joint97_progress_main_only','phase':phase,'at_local':sync.now(),
            'commit':commit,'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,'new_native_fits':0,
            'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
        create(out/'receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    except BaseException as exc:
        create(out/'failure.json',{'status':'failed_preserved_joint97_progress_publication','error':f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'prospective')
