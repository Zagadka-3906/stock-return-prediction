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
OUT=A/'actual_resume_new_controls_github_20261007'

def main():
    dependency=A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_full37_controls_main_publication_v1'
    while not (dependency/'native_launch.json').exists() or owned(read(dependency/'native_launch.json')):
        assert time.time()<datetime.fromisoformat('2026-10-07T23:35:00+08:00').timestamp()
        time.sleep(10)
    assert read(dependency/'service_execution.json')['status']=='passed'
    proof_path=A/'future129_130_131_administrative_count_routes_actual_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual72_prospective_sources_all_administrative_record_counts' and not proof['issues']
    sources=[Path(__file__),A/'prepare_actual_resume_new_controls_main_publication_20261007.py',
      A/'actual_user_resume_until2355_20261007.json',
      A/'future129_130_131_administrative_count_routes_actual_20261007.json',
      A/'verify_future129_130_131_administrative_count_routes_20261007.py',
      A/'actual_future_QA40_41_42_E_storage_20261007.json',
      A/'actual_new_streamed_RFF_and_empirical_Bayes_scientific_identity_20261007.json',
      A/'record_actual_new_science_and_E_QA_storage_20261007.py',
      A/'nonflag_RidgeFine52_administrative52_count_recovery_v2_20261007.json',
      A/'recover_nonflag_RidgeFine52_full128_counts_v2_20261007.py',
      A/'nonflag_RFF128StreamMid129_dependency_gate_recovery_v2_20261007.json',
      A/'recover_nonflag_RFF128StreamMid129_dependency_gate_v2_20261007.py',
      A/'nonflag_EmpiricalBayes130_parent128_gate_recovery_v4_20261007.json',
      A/'recover_nonflag_EmpiricalBayes130_parent128_gate_v4_20261007.py',
      A/'nonflag_EmpiricalBayes130_actual_admission_gate_finalization_v5_20261007.json',
      A/'finalize_nonflag_EmpiricalBayes130_actual_admission_gate_v5_20261007.py',
      A/'nonflag_EmpiricalBayes40_control_gate_recovery_v2_20261007.json',
      A/'nonflag_EmpiricalBayes40_full_control_recovery_v3_20261007.json',
      A/'nonflag_EmpiricalBayes40_partial_preparation_failure_20261007.json',
      A/'nonflag_residual_EmpiricalBayes37_transform_preflight_20261007/verification.json',
      A/'nonflag_residual_EmpiricalBayes64_native_hook3_preflight_20261007/verification.json',
      A/'nonflag_residual_RidgeMicro37_transform_preflight_20261007/verification.json',
      A/'monitor_full_actual_optimization_until2355_v28_20261007.py',
      A/'nonflag_residual_RidgeMicro_compatible_parent_20261007.py',
      A/'nonflag_RidgeMicro40_actual_controls_and_dependency_queue_hidden_launch_20261007.json',
      A/'nonflag_RidgeMicro40_plan_20261007.json',
      A/'nonflag_RidgeMicro40_prospective_routes_v2_20261007.json',
      A/'nonflag_RidgeMicro40_round131_mapping_20261007.py',
      A/'nonflag_RidgeMicro40_science_route_preparation_v1_20261007.json',
      A/'predict_nonflag_residual_RidgeMicro_complete_scheme_20261007.py',
      A/'prepare_nonflag_RidgeMicro40_round131_sources_v1_20261007.py',
      A/'prepare_nonflag_RidgeMicro40_science_routes_20261007.py',
      A/'prepare_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py',
      A/'publish_nonflag_RidgeMicro40_evidence_v1_20261007.py',
      A/'queue_nonflag_RidgeMicro131_after_actual130_20261007.py',
      A/'run_nonflag_RidgeMicro40_admitted_comparison_v1_20261007.py',
      A/'run_nonflag_RidgeMicro40_official_comparison_v1_20261007.py',
      A/'run_nonflag_RidgeMicro40_round131_full_registration_v1_20261007.py',
      A/'seal_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py',
      A/'start_nonflag_RidgeMicro40_controls_and_dependency_queue_20261007.py',
      A/'verify_nonflag_residual_RidgeMicro37_transform_20261007.py',
      A/'verify_nonflag_RidgeMicro40_prospective_routes_v2_20261007.py',
      A/'verify_nonflag_RidgeMicro40_round131_sources_v1_20261007.py',
      A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1/job_definition.json',
      A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1/launch_result.json',
      A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1/native_launch.json',
      A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1/service_execution.json',
      A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1/stderr.log',
      A/'service_owned_workflows_20261006/nonflag_RidgeFine52_round128_full_registration_v1/stdout.log',
      A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_actual129_after128_queue/job_definition.json',
      A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_actual129_after128_queue/launch_result.json',
      A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_actual129_after128_queue/native_launch.json',
      A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_actual129_after128_queue/service_execution.json',
      A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_actual129_after128_queue/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_actual129_after128_queue/stderr.log',
      A/'service_owned_workflows_20261006/nonflag_RFF128StreamMid76_actual129_after128_queue/stdout.log',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight/job_definition.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight/launch_result.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight/native_launch.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight/service_execution.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight/stderr.log',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight/stdout.log',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight_v2/job_definition.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight_v2/launch_result.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight_v2/native_launch.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight_v2/service_execution.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight_v2/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight_v2/stderr.log',
      A/'service_owned_workflows_20261006/nonflag_residual_EmpiricalBayes37_transform_preflight_v2/stdout.log',
    ]
    sources=list(dict.fromkeys(sources));pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    for p,d in pins.items():assert sha(p)==d,p
    assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_actual_main_publication.json',{'input_sha256':pins,'auxiliary_controls_not_new_official_score_records':True,'new_quality_scores':0})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        while any(psutil.Process(pid).status()==psutil.STATUS_STOPPED for pid in (row['pid'],row['owned_worker_pid'])):
            assert time.time()<datetime.fromisoformat('2026-10-07T23:45:00+08:00').timestamp()
            time.sleep(10)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/actual_resume_new_controls_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for path in [*sources,OUT/'frozen_before_actual_main_publication.json']:
                data=path.read_bytes();assert not sync.SECRET.search(data),path
                target=(prefix/path.relative_to(ROOT)).as_posix();payload[target]=data
                files[path.relative_to(ROOT).as_posix()]={'published_path':target,'sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual72_route_controls_37_full111_cold_and_explicit_new_solver_identities',
              'files':files,'previous_main':previous,'only_branch':'main','actual_administrative_failures_preserved':True,
              'completed_native_annual_fits_added':0,'new_quality_scores':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('实际恢复工作记录：遵照用户继续至23:55的答复；72份后续登记源码的项数控制、微幅Ridge37项全量与111冷前缀核对、分块RFF与自适应标量/对角先验20个成熟年度模型的明确方法身份，以及E盘QA目录核对。保留原始登记项数失败及后续依赖恢复记录；没有以此增加官方分数或宣称完整候选已合格。仅main，未读取真实测试标签。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','记录恢复优化后的实际控制验证、方法身份、E盘输出与失败恢复',timeout=180)
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
