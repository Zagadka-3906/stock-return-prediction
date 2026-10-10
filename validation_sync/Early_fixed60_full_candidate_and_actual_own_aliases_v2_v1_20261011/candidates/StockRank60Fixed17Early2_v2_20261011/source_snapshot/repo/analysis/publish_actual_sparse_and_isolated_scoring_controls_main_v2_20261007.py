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
OUT=A/'actual_sparse_and_isolated_scoring_controls_github_20261007'

def main():
    proof_path=A/'actual_sparse_and_isolated_scoring_controls_publication_scope_20261007.json';proof=read(proof_path)
    assert proof['status']=='actual_new_sparse10_solver2_native3_full37_cold111_and_parallel4_serial4_controls_passed'
    sources=[Path(__file__),A/'prepare_actual_sparse_and_isolated_scoring_main_publication_20261007.py',proof_path,
      A/'actual_paired_serial_official_controls_hidden_launch_20261007.json',
      A/'actual_paired_serial_official_controls_source_preparation_20261007.json',
      A/'actual_paired_serial_uncached_scoring_controls_20261007/verification.json',
      A/'actual_paired_serial_uncached_scoring_controls_20261007/worker0/case0_repeat0.json',
      A/'actual_paired_serial_uncached_scoring_controls_20261007/worker0/case0_repeat1.json',
      A/'actual_paired_serial_uncached_scoring_controls_20261007/worker0/frozen_before_actual_controls.json',
      A/'actual_paired_serial_uncached_scoring_controls_20261007/worker0/verification.json',
      A/'actual_paired_serial_uncached_scoring_controls_20261007/worker1/case1_repeat0.json',
      A/'actual_paired_serial_uncached_scoring_controls_20261007/worker1/case1_repeat1.json',
      A/'actual_paired_serial_uncached_scoring_controls_20261007/worker1/frozen_before_actual_controls.json',
      A/'actual_paired_serial_uncached_scoring_controls_20261007/worker1/verification.json',
      A/'actual_two_process_uncached_scoring_controls_20261007/verification.json',
      A/'actual_two_process_uncached_scoring_controls_20261007/worker0/case0_repeat0.json',
      A/'actual_two_process_uncached_scoring_controls_20261007/worker0/case0_repeat1.json',
      A/'actual_two_process_uncached_scoring_controls_20261007/worker0/frozen_before_actual_controls.json',
      A/'actual_two_process_uncached_scoring_controls_20261007/worker0/verification.json',
      A/'actual_two_process_uncached_scoring_controls_20261007/worker1/case1_repeat0.json',
      A/'actual_two_process_uncached_scoring_controls_20261007/worker1/case1_repeat1.json',
      A/'actual_two_process_uncached_scoring_controls_20261007/worker1/frozen_before_actual_controls.json',
      A/'actual_two_process_uncached_scoring_controls_20261007/worker1/verification.json',
      A/'actual_two_process_uncached_scoring_controls_hidden_launch_20261007.json',
      A/'actual_two_process_uncached_scoring_source_preparation_20261007.json',
      A/'nonflag_residual_SparseGram37_transform_preflight_20261007/frozen_before_actual_full_controls.json',
      A/'nonflag_residual_SparseGram37_transform_preflight_20261007/verification.json',
      A/'nonflag_residual_SparseGram6410_plan_20261007.json',
      A/'nonflag_residual_SparseGram6410_source_admission_v1_20261007.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/actual_stage.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/frozen_before_actual_training.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/independent_linear_state_2021.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/independent_linear_state_2022.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/independent_linear_state_2023.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/independent_linear_state_2024.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/independent_linear_state_2025.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/info_2021.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/info_2022.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/info_2023.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/info_2024.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/info_2025.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/model_2021.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/model_2022.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/model_2023.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/model_2024.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/model_2025.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_Elastic/oof_verification.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/independent_linear_state_2021.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/independent_linear_state_2022.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/independent_linear_state_2023.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/independent_linear_state_2024.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/independent_linear_state_2025.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/info_2021.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/info_2022.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/info_2023.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/info_2024.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/info_2025.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/model_2021.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/model_2022.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/model_2023.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/model_2024.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/model_2025.joblib',
      A/'nonflag_residual_SparseGram64_bank10_20261007/nonflag_residual_sparseGram64_L1/oof_verification.json',
      A/'nonflag_residual_SparseGram64_bank10_20261007/verification.json',
      A/'nonflag_residual_SparseGram64_native_bank10_hidden_launch_20261007.json',
      A/'nonflag_residual_SparseGram64_native_hook3_preflight_20261007/frozen_before_actual_controls.json',
      A/'nonflag_residual_SparseGram64_native_hook3_preflight_20261007/verification.json',
      A/'nonflag_residual_SparseGram64_native_stage_20261007.py',
      A/'nonflag_sparse_Gram64_actual_solver_controls_20261007/verification.json',
      A/'nonflag_sparse_Gram64_codec_20261007.py',
      A/'nonflag_SparseGram64_actual_controls_hidden_launch_20261007.json',
      A/'nonflag_SparseGram64_actual_native3_full37_cold111_controls_20261007.json',
      A/'nonflag_SparseGram64_actual_native_and_transform_source_preparation_20261007.json',
      A/'nonflag_SparseGram64_residual_precheck_plan_20261007.json',
      A/'prepare_actual_two_process_uncached_scoring_controls_20261007.py',
      A/'prepare_nonflag_SparseGram64_actual_native_and_full37_controls_20261007.py',
      A/'prepare_paired_serial_official_controls_20261007.py',
      A/'run_nonflag_residual_SparseGram64_hook3_after_bank_20261007.py',
      A/'run_nonflag_SparseGram64_actual_native_and_full37_controls_20261007.py',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot0/job_definition.json',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot0/launch_result.json',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot0/native_launch.json',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot0/service_execution.json',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot0/stderr.log',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot0/stdout.log',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot0/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot1/job_definition.json',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot1/launch_result.json',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot1/native_launch.json',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot1/service_execution.json',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot1/stderr.log',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot1/stdout.log',
      A/'service_owned_workflows_20261006/actual_isolated_official_worker2_slot1/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_controls_queue/job_definition.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_controls_queue/launch_result.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_controls_queue/native_launch.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_controls_queue/service_execution.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_controls_queue/stderr.log',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_controls_queue/stdout.log',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_controls_queue/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot0/job_definition.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot0/launch_result.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot0/native_launch.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot0/service_execution.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot0/stderr.log',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot0/stdout.log',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot0/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot1/job_definition.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot1/launch_result.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot1/native_launch.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot1/service_execution.json',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot1/stderr.log',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot1/stdout.log',
      A/'service_owned_workflows_20261006/actual_paired_serial_official_worker2_slot1/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/actual_two_process_uncached_scoring_controls_queue/job_definition.json',
      A/'service_owned_workflows_20261006/actual_two_process_uncached_scoring_controls_queue/launch_result.json',
      A/'service_owned_workflows_20261006/actual_two_process_uncached_scoring_controls_queue/native_launch.json',
      A/'service_owned_workflows_20261006/actual_two_process_uncached_scoring_controls_queue/service_execution.json',
      A/'service_owned_workflows_20261006/actual_two_process_uncached_scoring_controls_queue/stderr.log',
      A/'service_owned_workflows_20261006/actual_two_process_uncached_scoring_controls_queue/stdout.log',
      A/'service_owned_workflows_20261006/actual_two_process_uncached_scoring_controls_queue/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/nonflag_residual_SparseGram64_native_bank10/job_definition.json',
      A/'service_owned_workflows_20261006/nonflag_residual_SparseGram64_native_bank10/launch_result.json',
      A/'service_owned_workflows_20261006/nonflag_residual_SparseGram64_native_bank10/native_launch.json',
      A/'service_owned_workflows_20261006/nonflag_residual_SparseGram64_native_bank10/service_execution.json',
      A/'service_owned_workflows_20261006/nonflag_residual_SparseGram64_native_bank10/stderr.log',
      A/'service_owned_workflows_20261006/nonflag_residual_SparseGram64_native_bank10/stdout.log',
      A/'service_owned_workflows_20261006/nonflag_residual_SparseGram64_native_bank10/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/nonflag_SparseGram64_actual_native3_full37_controls/job_definition.json',
      A/'service_owned_workflows_20261006/nonflag_SparseGram64_actual_native3_full37_controls/launch_result.json',
      A/'service_owned_workflows_20261006/nonflag_SparseGram64_actual_native3_full37_controls/native_launch.json',
      A/'service_owned_workflows_20261006/nonflag_SparseGram64_actual_native3_full37_controls/service_execution.json',
      A/'service_owned_workflows_20261006/nonflag_SparseGram64_actual_native3_full37_controls/stderr.log',
      A/'service_owned_workflows_20261006/nonflag_SparseGram64_actual_native3_full37_controls/stdout.log',
      A/'service_owned_workflows_20261006/nonflag_SparseGram64_actual_native3_full37_controls/verified_hidden_launch.json',
      A/'train_nonflag_residual_SparseGram64_bank10_v1_20261007.py',
      A/'verify_actual_paired_serial_official_controls_20261007.py',
      A/'verify_actual_paired_serial_official_worker2_20261007.py',
      A/'verify_actual_two_process_uncached_scoring_controls_20261007.py',
      A/'verify_nonflag_residual_SparseGram37_transform_20261007.py',
      A/'verify_nonflag_sparse_Gram64_solver_and_prepare_bank10_20261007.py',
    ]
    sources += [A/'publish_actual_sparse_and_isolated_scoring_controls_main_20261007.py',A/'prepare_actual_sparse_publication_context_v2_20261007.py',A/'record_actual_scoring_latency_limitations_20261007.py',A/'actual_two_process_scoring_latency_interpretation_20261007.json']
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
            prefix=Path('validation_sync/actual_sparse_and_isolated_scoring_controls_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for path in [*sources,OUT/'frozen_before_actual_main_publication.json']:
                data=path.read_bytes();assert not sync.SECRET.search(data),path
                target=(prefix/path.relative_to(ROOT)).as_posix();payload[target]=data
                files[path.relative_to(ROOT).as_posix()]={'published_path':target,'sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_sparse10_and_isolated_parallel4_serial4_controls',
              'files':files,'previous_main':previous,'only_branch':'main','official_scores_and_full_candidate_not_yet_claimed':True,'sparse_residual_sign':1,'actual_historical_execution_control_calls':8,
              'completed_native_annual_fits_added':10,'new_quality_scores':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('新增非涨停残差稀疏回归：L1和L1/L2两种成熟年度配方，10个真实模型均通过完整历史原生重载、独立解码及前缀检查；另有2项与sklearn的求解目标/KKT对照、3项原生CDF、37全量和111冷前缀控制。尚未完成其官方40项比较、完整未来候选或正式入选，不赋予排名。双进程隔离评分和匹配串行评分各4次，8指标、映射数值与完整CSV字节均一致；并行总耗时56.1347144000174秒，串行165.63915989999077秒。总耗时包含内存门槛等待与进程准备，串行阶段系统可用内存曾降至3.32GiB；后台GPU与完整榜检查负载会改变，不能把总耗时比视为通用或因果隔离的提速保证；跨进程共享缓存未准入，当前正式搜索保留原顺序流程。只上传源码、模型参数和证明，不重复上传大特征与预测缓存。仅main，23:55停工，明早须实际用户继续。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存稀疏残差实际10模型控制和隔离双进程串行评分对照',timeout=180)
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

if __name__=='__main__':main()
