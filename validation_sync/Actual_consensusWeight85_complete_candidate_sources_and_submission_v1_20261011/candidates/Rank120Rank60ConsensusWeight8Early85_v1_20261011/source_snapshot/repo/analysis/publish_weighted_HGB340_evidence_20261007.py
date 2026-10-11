"""Publish actual337 controls and actual340 scores separately to main."""
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
    assert read(f/'service_execution.json')['status']=='passed',name
    return f

def main(phase):
    assert phase in ('controls','scores')
    closed('weighted_HGB_and_percentile_controls_main_publication')
    closed('flagged_HGB88_round116_full_registration_v2')
    if phase=='scores':closed('weighted_HGB340_full337_controls_main_publication')
    science=closed('weighted_flagged_HGB_full337_transform_preflight_v3' if phase=='controls' else 'flagged_HGB_weighted_quarters340_official_comparison')
    folder=A/('flagged_HGB_weighted_quarters340_transform_preflight_20261007' if phase=='controls' else 'flagged_HGB_weighted_quarters340_official_comparison_20261007')
    proof=read(folder/'verification.json')
    status='passed_actual337_full5635800_weighted_flagged_HGB_independent_oracle_and_cold80_260_975_controls' if phase=='controls' else 'passed_actual340_weighted_flagged_HGB_full_official_comparisons'
    assert proof['status']==status
    assert len(proof['controls'] if phase=='controls' else proof['records'])==(337 if phase=='controls' else 340)
    sources=[Path(__file__),A/'flagged_HGB_weighted_quarters340_plan_20261007.json',
      A/'verify_flagged_HGB_weighted_quarters340_transform_20261007.py',
      A/'run_flagged_HGB_weighted_quarters340_official_comparison_v3_20261007.py',
      A/'prepare_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007.py',
      A/'seal_flagged_HGB_weighted_quarters340_selected_candidate_v3_20261007.py',
      A/'predict_refined_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',
      A/'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007.py',
      A/'predict_lower_pool_after_weighted_flagged_CPU_HGB_scheme_v2_20261007.py',
      A/'prepare_weighted_HGB340_round117_sources_20261007.py',
      A/'run_weighted_HGB340_round117_full_registration_20261007.py',
      A/'verify_weighted_HGB340_round117_sources_20261007.py',
      A/'refine_flagged_HGB_compatible_parent_transform_20261007.py',
      A/'all_forecast_percentile_runtime_20261007.py',A/'exact_numpy_all_forecast_percentiles_20261007.py',
      A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json',
      *folder.glob('*.json'),*science.glob('*.json'),*science.glob('*.log')]
    if phase=='scores':
        for row in proof['records']:
            p=Path(row['official_score_cache']['official_metrics_source'])
            assert sha(p)==row['official_metric_capsule_sha256'] and read(p)['metrics']==row['metrics'];sources.append(p)
    sources=list(dict.fromkeys(sources));out=A/f'weighted_HGB340_{phase}_github_20261007';assert not out.exists();out.mkdir()
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'phase':phase,'new_native_fits':0,'full117_not_yet_qualified':True})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        main7=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(main7,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path(f'validation_sync/weighted_HGB340_{phase}_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*sources,out/'frozen_before_main_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                raw=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'published_path':target,'original_sha256':raw,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_weighted_HGB340_'+phase,
              'files':files,'previous_main':previous,'only_branch':'main','actual_full_control_cases':337,'actual_cold_prefix_cases':1011,
              'new_quality_score_records':340 if phase=='scores' else 0,'new_native_fits':0,'full117_not_yet_qualified':True,
              'scientific_workers_stopped':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('加权HGB集成：28种四份组合，每种2至3个唯一原生模型，12种幅度；加3个合格锚点与移除分支，共340项。\n'
              '本目录仅证明manifest所标记的已完成阶段；完整117资格仍需冻结、候选核对或完整推理、QA28及完整榜同步。有限网格不证明优化穷尽。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','上传非等权HGB集成的'+phase+'实际验证',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main','at_local':sync.now(),
              'raw_git_blobs_verified':len(hashes),'phase':phase,'new_quality_scores':340 if phase=='scores' else 0,'test_labels_read':False})
            if phase=='scores':
                target=A/'flagged_HGB_weighted_quarters340_scores_github_20261007';assert not target.exists();target.mkdir()
                create(target/'receipt.json',read(out/'receipt.json'))
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})

if __name__=='__main__':main(sys.argv[1])
