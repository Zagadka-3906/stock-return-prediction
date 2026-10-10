"""Publish actual resource evidence and clearly limited experimental cache controls."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers
OUT=A/'live_profile_root_cache_controls_github_20261006'
PREFIX=Path('validation_sync/live_profile_root_cache_controls_20261006')

def main():
    actual=A/'live_scoring_and_GPU_shared_memory_profile_20261006'
    tiny=A/'bounded_root_replay_memoization_semantic_controls_20261006'
    proof=read(actual/'verification.json');controls=read(tiny/'verification.json')
    assert proof['status']=='passed_actual_owned10_stack_samples_and_process_WDDM_GPU_memory'
    assert controls['status']=='passed_tiny_root_cache_semantics_full_real_array_controls_pending'
    for item in (proof,controls):
        for p,digest in item['input_sha256'].items():assert sha(p)==digest,p
    assert controls['runtime_adopted'] is False
    assert not OUT.exists();OUT.mkdir()
    sources=[Path(__file__),A/'profile_live_scoring_and_GPU_shared_memory_20261006.py',
        A/'bounded_root_replay_memoization_20261006.py',A/'verify_bounded_root_replay_memoization_controls_20261006.py',
        A/'verify_bounded_root_replay_full_controls_20261006.py',*actual.rglob('*.json'),*actual.rglob('*.txt'),*tiny.rglob('*.json')]
    for p in sources:
        if p.suffix=='.py':compile(p.read_text(encoding='utf-8'),str(p),'exec')
    sync=helpers.sync;targets={(PREFIX/'.gitattributes').as_posix():b'* -text\n'};files={}
    for path in dict.fromkeys(sources):
        data=path.read_bytes();assert len(data)<5*1024**2 and not sync.SECRET.search(data),path
        target=path.relative_to(ROOT) if path.parent==A and path.suffix=='.py' else PREFIX/path.relative_to(ROOT)
        targets[target.as_posix()]=data;files[path.relative_to(ROOT).as_posix()]={'published_path':target.as_posix(),'raw_sha256':hashlib.sha256(data).hexdigest()}
    rows=[read(A/f'service_owned_workflows_20261006/{name}/native_launch.json') for name in ('main_publisher_v7','main_publisher_v6')
        if (A/f'service_owned_workflows_20261006/{name}/native_launch.json').exists()]
    row=next(r for r in rows if owned(r));root,worker=helpers.owned_pair(row['pid'],Path(row['script']),row['script_args'])
    suspended=[];restore=install()
    try:
        for _ in range(180):
            for p in (worker,root):p.suspend();suspended.append(p)
            busy=[p for p in root.children(recursive=True) if p.pid!=worker.pid and p.name().lower()!='conhost.exe']
            if not busy:break
            for p in reversed(suspended):p.resume()
            suspended=[];time.sleep(1)
        else:raise RuntimeError('Main publisher still owns an active publication command')
        previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous)
        assert not sync.git('status','--porcelain')
        targets[(PREFIX/'manifest.json').as_posix()]=sync.encoded({'status':'actual_live_profile_and_experimental_cache_semantics_published',
            'previous_main':previous,'at_local':sync.now(),'files':files,'full_root_cache_control_execution_pending':True,
            'runtime_cache_adopted':False,'new_quality_scores':0,'new_native_fits':0,'only_publication_branch':'main'})
        targets[(PREFIX/'README.md').as_posix()]=('''# 实际资源采样与受限历史方案缓存试验

真实第95轮评分进程在45.11秒观察窗口消耗44.67秒CPU时间；10次调用栈采样分别为历史成员排序1次、历史根预测2次、后续用途层3次、收益映射或官方评分3次、其他1次。采样比例不是精确耗时比例，也不证明缓存加速。原评分进程未改动。

独立核验神经网络PID、创建时间、命令及实际反向传播栈。两次Windows WDDM进程内存采样均为专用11728437248字节、共享5165285376字节，合计16893722624字节；同期NVML设备总显存12227MiB，使用约11803—11810MiB，GPU利用率98%。这是当前共享GPU内存占用证据，不能视为OOM、全局资源极限或模型分数。原32768批量、32轮、FP32及训练任务全部保留。累积梯度、检查点及组合模式已在原计划，不作为新方向重复登记。

试验缓存只复用相同上下文和参数下的历史根成员排序与根预测，中间值载荷上限128MiB；源证书、根参数、相关数值输入和调用参数决定键。返回值复制，日期前缀及复制后的标签污染上下文使用独立冷缓存。小规模控制通过：返回值修改不污染缓存，根参数/输入/标签修改使缓存失效，后续用途改变可复用未变的根，容量与淘汰正确，原全局类不变。未接入实际评分。

完整控制程序已准备：真实5635800行、1212日、4650股票，使用已完成的5个实际第95轮配置，逐位比较输出和8项官方指标，冷80/260日前缀、标签污染和根修改复核，再测耗时及缓存容量。当前只运行了准入探测；14GiB可用内存保护是调度规则，不是物理极限。全量控制、实际速度收益和正式接入仍待执行。新增模型训练0、新增选模分数0，不读取测试标签，所有记录仅main。
''').encode('utf-8')
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        selected=sorted(targets)
        for offset in range(0,len(selected),50):sync.git('add','-f','--',*selected[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(selected)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','记录真实GPU共享内存与评分栈采样及尚未采用的历史根缓存控制',timeout=180)
        commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
        assert helpers.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
        create(OUT/'receipt.json',{'status':'pushed_actual_profile_and_experimental_cache_controls_main_only','at_local':sync.now(),
            'commit':commit,'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,'runtime_cache_adopted':False,
            'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+PREFIX.as_posix()})
        print(json.dumps(read(OUT/'receipt.json'),ensure_ascii=False),flush=True)
    except BaseException as exc:
        create(OUT/'failure.json',{'status':'failed_preserved_profile_cache_control_publication','error':f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
        create(OUT/'actual_hidden_publication_children.json',{'events':restore()})

if __name__=='__main__':main()
