"""Publish actual CPU epoch-resume controls and the preserved failed first attempt to main."""
from pathlib import Path
from datetime import datetime
import hashlib,sys,time
import psutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers
OUT=A/'actual_GPU_shared_memory_and_manual_bench_plan_github_recovery_v2_20261007'

def actual_main():
    dependency=A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v3'
    while not (dependency/'native_launch.json').exists() or owned(read(dependency/'native_launch.json')):
        assert time.time()<datetime.fromisoformat('2026-10-07T23:35:00+08:00').timestamp();time.sleep(5)
    assert read(dependency/'service_execution.json')['status']=='passed'
    proof_path=A/'actual_GPU_shared_allocation_resource_boundary_20261007.json';proof=read(proof_path)
    assert proof['status']=='measured_original16384_recipe_uses_Windows_shared_GPU_allocation_on_this_host'
    sources=[Path(__file__),
      A/'prepare_actual_GPU_resource_main_publication_20261007.py',
      A/'record_actual_GPU_memory_boundary_and_manual_bench_plan_20261007.py',
      A/'actual_neural_GPU_shared_memory_snapshot_20261007.json',
      A/'actual_GPU_shared_allocation_resource_boundary_20261007.json',
      A/'manual_next_run_GPU_speed_and_epoch_checkpoint_bench_plan_20261007.json',
      A/'actual_two_process_scoring_latency_interpretation_20261007.json',
      A/'record_actual_scoring_latency_limitations_20261007.py',
    ]
    sources += [A/'publish_actual_GPU_shared_memory_and_manual_bench_plan_main_20261007.py',A/'recover_actual_sparse_and_GPU_publications_TLS_v3_20261007.py',A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v2/job_definition.json',A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v2/launch_result.json',A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v2/native_launch.json',A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v2/service_execution.json',A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v2/verified_hidden_launch.json',A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v2/stderr.log',A/'service_owned_workflows_20261006/actual_sparse_and_isolated_scoring_controls_main_publication_v2/stdout.log',A/'service_owned_workflows_20261006/actual_GPU_shared_allocation_and_manual_bench_main_publication/job_definition.json',A/'service_owned_workflows_20261006/actual_GPU_shared_allocation_and_manual_bench_main_publication/launch_result.json',A/'service_owned_workflows_20261006/actual_GPU_shared_allocation_and_manual_bench_main_publication/native_launch.json',A/'service_owned_workflows_20261006/actual_GPU_shared_allocation_and_manual_bench_main_publication/service_execution.json',A/'service_owned_workflows_20261006/actual_GPU_shared_allocation_and_manual_bench_main_publication/verified_hidden_launch.json',A/'service_owned_workflows_20261006/actual_GPU_shared_allocation_and_manual_bench_main_publication/stderr.log',A/'service_owned_workflows_20261006/actual_GPU_shared_allocation_and_manual_bench_main_publication/stdout.log']
    sources=list(dict.fromkeys(sources));pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    for p,d in pins.items():assert sha(p)==d,p
    assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_actual_main_publication.json',{'input_sha256':pins,'signed_scheme_not_yet_officially_scored_or_adopted':True,'new_quality_scores':0})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        while any(psutil.Process(pid).status()==psutil.STATUS_STOPPED for pid in (row['pid'],row['owned_worker_pid'])):
            assert time.time()<datetime.fromisoformat('2026-10-07T23:45:00+08:00').timestamp()
            time.sleep(10)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/actual_GPU_shared_memory_and_manual_bench_plan_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for path in [*sources,OUT/'frozen_before_actual_main_publication.json']:
                data=path.read_bytes();assert not sync.SECRET.search(data),path
                target=(prefix/path.relative_to(ROOT)).as_posix();payload[target]=data
                files[path.relative_to(ROOT).as_posix()]={'published_path':target,'sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_measured_GPU_shared_allocation_and_manual_unexecuted_speed_bench_plan',
              'files':files,'previous_main':previous,'only_branch':'main','official_scores_and_full_candidate_not_yet_claimed':True,'original_training_not_modified':True,'GPU_new_recipe_qualification_not_claimed':True,
              'completed_native_annual_fits_added':0,'new_quality_scores':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('强所有权核对后采样Windows WDDM GPU进程计数：原16384/8192/4096网络使用约10.53GiB专用与5.52GiB共享GPU内存。支持当前配方已使用共享分配；未测定其造成的时间惩罚、PCIe流量或CUDA峰值。原2021成熟年度实际拟合约40小时，旧训练器仅年度末落盘；已完成2020/2021参数保留，未落盘年度关机后不能恢复。预声明明早手动GPU检查：较小微批与梯度累积、BF16、TF32及逐epoch持久化，均属于新的浮点配方，GPU等价性与速度收益尚未测试，不混作原FP32权重。后台负载变化下的双进程/串行评分总耗时也不构成保证提速证据。没有新模型分数，没有声称可行方向穷尽。仅main，23:55停工，明早用户实际继续后执行。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存原大网络GPU共享分配实测及明早手动提速检验计划',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(data).hexdigest() for n,data in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit);scope.reverify()
            create(OUT/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main',
              'at_local':sync.now(),'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,'test_labels_read':False})
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(OUT/'actual_hidden_publication_children.json',{'events':restore()})

def main():
    original_git=helpers.sync.git;attempts=[]
    def retry(*args,**kwargs):
        for trial in range(3):
            try:return original_git(*args,**kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote','push','fetch') or not any(word in str(error).lower() for word in ('tls','ssl','unable to access','connection','timed out')):raise
                attempts.append({'command':args[0],'attempt':trial+1,'error':str(error)[:1200]})
                if trial==2:raise
                time.sleep(2)
    helpers.sync.git=retry
    try:actual_main()
    finally:
        helpers.sync.git=original_git
        if OUT.exists():create(OUT/'actual_TLS_transport_retries.json',{'attempts':attempts,'TLS_verification_not_disabled':True})

if __name__=='__main__':main()
