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
OUT=A/'reverse_Bayes_actual_controls_github_20261007'

def main():
    proof_path=A/'nonflag_ReverseBayes40_actual_native3_full37_cold111_controls_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual_signed_native3_full37_independent_CDF_and111_cold_controls'
    assert proof['new_quality_scores']==0 and proof['residual_sign']==-1
    sources=[Path(__file__),proof_path,A/'prepare_reverse_Bayes_controls_main_publication_20261007.py',
      A/'prepare_reverse_empirical_Bayes_actual_controls_20261007.py',
      A/'run_reverse_empirical_Bayes_actual_controls_20261007.py',
      A/'nonflag_ReverseBayes40_control_plan_20261007.json',
      A/'nonflag_ReverseBayes40_control_source_preparation_20261007.json',
      A/'nonflag_ReverseBayes40_controls_actual_hidden_launch_20261007.json',
      A/'nonflag_residual_ReverseBayes64_native_stage_20261007.py',
      A/'run_nonflag_residual_ReverseBayes64_hook3_after_bank_20261007.py',
      A/'verify_nonflag_residual_ReverseBayes37_transform_20261007.py',
      A/'record_remaining_feasible_optimization_frontier_20261007.py',
      A/'remaining_feasible_optimization_frontier_manual_resume_20261007.json',
      A/'record_actual_single_host_resource_boundary_20261007.py',
      A/'actual_single_host_resource_boundary_after_resume_20261007.json',
      A/'nonflag_residual_ReverseBayes64_native_hook3_preflight_20261007/frozen_before_actual_controls.json',
      A/'nonflag_residual_ReverseBayes64_native_hook3_preflight_20261007/verification.json',
      A/'nonflag_residual_ReverseBayes37_transform_preflight_20261007/frozen_before_actual_full_controls.json',
      A/'nonflag_residual_ReverseBayes37_transform_preflight_20261007/verification.json',
      A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual_native3_full37_controls/job_definition.json',
      A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual_native3_full37_controls/launch_result.json',
      A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual_native3_full37_controls/native_launch.json',
      A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual_native3_full37_controls/service_execution.json',
      A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual_native3_full37_controls/verified_hidden_launch.json',
      A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual_native3_full37_controls/stderr.log',
      A/'service_owned_workflows_20261006/nonflag_ReverseBayes40_actual_native3_full37_controls/stdout.log',
    ]
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
            prefix=Path('validation_sync/reverse_Bayes_actual_controls_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for path in [*sources,OUT/'frozen_before_actual_main_publication.json']:
                data=path.read_bytes();assert not sync.SECRET.search(data),path
                target=(prefix/path.relative_to(ROOT)).as_posix();payload[target]=data
                files[path.relative_to(ROOT).as_posix()]={'published_path':target,'sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_reverse_Bayes_native3_full37_cold111_controls',
              'files':files,'previous_main':previous,'only_branch':'main','official_scores_and_full_candidate_not_yet_claimed':True,'residual_sign':-1,
              'completed_native_annual_fits_added':0,'new_quality_scores':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('反向自适应收缩实际预检查：复用已验证的标量先验、对角先验及等权均值，明确负残差方向；3项原生重载与独立解码、37项5635800行独立CDF、111项冷前缀全部通过。尚未进行40项官方比较、选中方案冻结、真实完整候选推理或完整榜登记；没有新增模型训练或官方评分。另附本机资源事实及仍可行的交叉模型集成、稀疏线性模型等方向，未宣称优化穷尽。仅main；今晚23:55停工，明早须用户实际发送继续。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','记录负向自适应收缩实际3/37/111控制与未穷尽方向和资源证据',timeout=180)
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
