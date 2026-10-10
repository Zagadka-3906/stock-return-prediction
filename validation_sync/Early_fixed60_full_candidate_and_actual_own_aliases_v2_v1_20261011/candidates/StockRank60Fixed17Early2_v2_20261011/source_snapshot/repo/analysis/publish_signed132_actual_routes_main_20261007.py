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
OUT=A/'signed132_actual_routes_github_20261007'

def main():
    proof_path=A/'future132_administrative_count_routes_actual_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual24_prospective_sources_all_administrative_record_counts' and not proof['issues']
    sources=[Path(__file__),A/'prepare_signed132_actual_counts_and_main_publication_20261007.py',A/'verify_future132_administrative_count_routes_20261007.py',proof_path,
      A/'nonflag_residual_ReverseBayes64_native_stage_20261007.py',
      A/'nonflag_residual_ReverseBayes_compatible_parent_20261007.py',
      A/'nonflag_ReverseBayes40_actual_native3_full37_cold111_controls_20261007.json',
      A/'nonflag_ReverseBayes40_control_plan_20261007.json',
      A/'nonflag_ReverseBayes40_control_source_preparation_20261007.json',
      A/'nonflag_ReverseBayes40_controls_actual_hidden_launch_20261007.json',
      A/'nonflag_ReverseBayes40_full132_dependency_queue_hidden_launch_20261007.json',
      A/'nonflag_ReverseBayes40_plan_20261007.json',
      A/'nonflag_ReverseBayes40_prospective_routes_v1_20261007.json',
      A/'nonflag_ReverseBayes40_round132_mapping_20261007.py',
      A/'nonflag_ReverseBayes40_science_route_preparation_v1_20261007.json',
      A/'predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py',
      A/'prepare_nonflag_ReverseBayes40_complete_routes_20261007.py',
      A/'prepare_nonflag_ReverseBayes40_round132_sources_v1_20261007.py',
      A/'prepare_nonflag_ReverseBayes40_selected_candidate_v1_20261007.py',
      A/'publish_nonflag_ReverseBayes40_evidence_v1_20261007.py',
      A/'queue_nonflag_ReverseBayes132_after_actual131_20261007.py',
      A/'run_nonflag_residual_ReverseBayes64_hook3_after_bank_20261007.py',
      A/'run_nonflag_ReverseBayes40_admitted_comparison_v1_20261007.py',
      A/'run_nonflag_ReverseBayes40_official_comparison_v1_20261007.py',
      A/'run_nonflag_ReverseBayes40_round132_full_registration_v1_20261007.py',
      A/'seal_nonflag_ReverseBayes40_selected_candidate_v1_20261007.py',
      A/'verify_nonflag_residual_ReverseBayes37_transform_20261007.py',
      A/'verify_nonflag_ReverseBayes40_prospective_routes_v1_20261007.py',
      A/'verify_nonflag_ReverseBayes40_round132_sources_v1_20261007.py',
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
            prefix=Path('validation_sync/signed132_actual_routes_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for path in [*sources,OUT/'frozen_before_actual_main_publication.json']:
                data=path.read_bytes();assert not sync.SECRET.search(data),path
                target=(prefix/path.relative_to(ROOT)).as_posix();payload[target]=data
                files[path.relative_to(ROOT).as_posix()]={'published_path':target,'sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_signed132_24_sources12_graph_controls_and_all_record_count_guards',
              'files':files,'previous_main':previous,'only_branch':'main','official_scores_and_full_candidate_not_yet_claimed':True,'residual_sign':-1,
              'completed_native_annual_fits_added':0,'new_quality_scores':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('已实际预生成第132轮反向自适应收缩40项方案的24份完整登记源码，执行12项原生方案结构控制，并核对每一处记录项数。此前3项原生、37全量与111冷前缀控制已通过。40项官方比较仍须等待第131轮真实完整榜及main结束、再通过九项真实父分数回归与完整源码准入；23:12仍不具备条件则今晚不启动，明早等待用户继续。没有新增模型或官方分数，也没有宣称候选已正式采用。仅main。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','记录反向收缩完整132源码的实际24/12结构与全部项数检查',timeout=180)
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
