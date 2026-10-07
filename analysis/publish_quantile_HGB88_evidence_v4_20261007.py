"""Publish actual25 controls and actual28 scores separately to main."""
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
    closed('quantile_HGB_bank20_main_publication_after118_v4')
    closed('HGB_quarter_numeric28_round118_full_registration_v4')
    if phase=='scores':closed('quantile_HGB88_full85_controls_main_publication_v4')
    science=closed('quantile_HGB_full85_transform_preflight' if phase=='controls' else 'quantile_HGB88_official_comparison_v4')
    folder=A/('quantile_HGB88_transform_preflight_20261007' if phase=='controls' else 'quantile_HGB88_official_comparison_v4_20261007')
    proof=read(folder/'verification.json')
    status='passed_actual85_full5635800_quantile_HGB_independent_oracle_and_cold80_260_975_controls' if phase=='controls' else 'passed_actual88_quantile_HGB_full_official_comparisons'
    assert proof['status']==status
    assert len(proof['controls'] if phase=='controls' else proof['records'])==(85 if phase=='controls' else 88)
    sources=[Path(__file__),A/'quantile_HGB88_plan_20261007.json',
      A/'verify_quantile_HGB88_transform_20261007.py',
      A/'run_quantile_HGB88_official_comparison_v4_20261007.py',
      A/'prepare_quantile_HGB88_selected_candidate_v4_20261007.py',
      A/'seal_quantile_HGB88_selected_candidate_v4_20261007.py',
      A/'predict_refined_quantile_HGB_scheme_v2_20261007.py',
      A/'predict_quantile_HGB_residual_CDF_scheme_v2_20261007.py',
      A/'predict_lower_pool_after_quantile_HGB_scheme_v2_20261007.py',
      A/'prepare_quantile_HGB88_round119_sources_v4_20261007.py',
      A/'run_quantile_HGB88_round119_full_registration_v4_20261007.py',
      A/'verify_quantile_HGB88_round119_sources_v4_20261007.py',
      A/'refine_flagged_HGB_compatible_parent_transform_20261007.py',
      A/'all_forecast_percentile_runtime_20261007.py',A/'exact_numpy_all_forecast_percentiles_20261007.py',
      A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json',
      *folder.glob('*.json'),*science.glob('*.json'),*science.glob('*.log')]
    sources += [A/'prepare_quantile_HGB88_complete_pipeline_sources_20261007.py',A/'quantile_HGB88_complete_pipeline_source_preparation_20261007.json',A/'prepare_weighted_HGB340_round117_sources_v2_20261007.py']
    sources += [A/'cached_official_spearman_runtime_20261007.py', A/'exact_cached_official_spearman_v2_20261007.py',
      A/'exact_cached_validation_spearman_20261007.py',A/'cached_official_spearman_full_scoring_benchmark_20261007/verification.json',
      A/'exact_cached_official_spearman_v2_edge_preflight_20261007/verification.json',A/'benchmark_cached_official_spearman_full_scoring_20261007.py',
      A/'prepare_cached_official_spearman_full_benchmark_20261007.py',A/'cached_official_spearman_full_benchmark_source_preparation_20261007.json',
      A/'cached_official_spearman_full12_actual_launch_20261007.json',A/'quantile_HGB_native_hook7_preflight_20261007/verification.json',
      A/'quantile_HGB88_workflow_source_preparation_20261007.json', A/'quantile_HGB85_full_controls_source_preparation_20261007.json',
      *list((A/'service_owned_workflows_20261006/cached_official_spearman_full12_benchmark').glob('*.json')),
      *list((A/'service_owned_workflows_20261006/cached_official_spearman_full12_benchmark').glob('*.log'))]
    sources += [A/'prepare_quantile_HGB88_complete_routes_v2_20261007.py',A/'quantile_HGB88_complete_routes_source_preparation_v2_20261007.json',
      A/'prepare_quantile_HGB88_round119_sources_20261007.py',A/'verify_quantile_HGB88_round119_sources_20261007.py',
      A/'run_quantile_HGB88_round119_full_registration_v4_20261007.py',A/'publish_quantile_HGB88_evidence_20261007.py']
    sources += [A/'prepare_quantile_HGB88_routes_v3_before_scoring_20261007.py',A/'quantile_HGB88_routes_source_preparation_v3_20261007.json',
      A/'quantile_HGB88_actual_idle_waiter_handoff_v3_20261007/verification.json',
      A/'handoff_quantile_HGB88_idle_waiters_v3_20261007.py',A/'local_118_119_protocol_recovery_actual_hidden_launches_v4_20261007.json']
    if phase=='scores':
        for row in proof['records']:
            p=Path(row['official_score_cache']['official_metrics_source'])
            assert sha(p)==row['official_metric_capsule_sha256'] and read(p)['metrics']==row['metrics'];sources.append(p)
    sources=list(dict.fromkeys(sources));out=A/f'quantile_HGB88_{phase}_github_v4_20261007';assert not out.exists();out.mkdir()
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'phase':phase,'new_native_fits':0,'full119_not_yet_qualified':True})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        main7=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(main7,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path(f'validation_sync/quantile_HGB88_{phase}_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*sources,out/'frozen_before_main_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                raw=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'published_path':target,'original_sha256':raw,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_quantile_HGB88_'+phase,
              'files':files,'previous_main':previous,'only_branch':'main','actual_full_control_cases':85,'actual_cold_prefix_cases':255,
              'new_quality_score_records':88 if phase=='scores' else 0,'new_native_fits':0,'full119_not_yet_qualified':True,
              'scientific_workers_stopped':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('分位数HGB：4单模型及3等权集成各12幅度，加3个合格锚点及消融，共88项。\n'
              '本目录仅证明manifest所标记的已完成阶段；完整119资格仍需冻结、候选核对或完整推理、QA30及完整榜同步。有限网格不证明优化穷尽。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','上传分位数HGB的'+phase+'实际验证',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main','at_local':sync.now(),
              'raw_git_blobs_verified':len(hashes),'phase':phase,'new_quality_scores':88 if phase=='scores' else 0,'test_labels_read':False})
            if phase=='scores':
                target=A/'quantile_HGB88_scores_github_v4_20261007';assert not target.exists();target.mkdir()
                create(target/'receipt.json',read(out/'receipt.json'))
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})

if __name__=='__main__':main(sys.argv[1])
