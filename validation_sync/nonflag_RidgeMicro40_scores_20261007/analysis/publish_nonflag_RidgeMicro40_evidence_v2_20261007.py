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

def actual_main(phase):
    assert phase in ('controls','scores')
    closed('nonflag_EmpiricalBayes40_round130_full_registration_v1')
    closed('nonflag_residual_Ridge_actual_hooks_and_main_after120')
    if phase=='scores':closed('nonflag_RidgeMicro40_full37_controls_main_publication_v1')
    science=closed('nonflag_residual_RidgeMicro37_transform_preflight' if phase=='controls' else 'nonflag_RidgeMicro40_official_comparison_v1')
    folder=A/('nonflag_residual_RidgeMicro37_transform_preflight_20261007' if phase=='controls' else 'nonflag_RidgeMicro40_official_comparison_v1_20261007')
    proof=read(folder/'verification.json')
    status='passed_actual37_full5635800_nonflag_residual_Ridge_independent_CDF_and111_cold_controls' if phase=='controls' else 'passed_actual40_nonflag_Ridge_full_official_comparisons'
    assert proof['status']==status
    assert len(proof['controls'] if phase=='controls' else proof['records'])==(37 if phase=='controls' else 40)
    sources=[Path(__file__),A/'nonflag_RidgeMicro40_plan_20261007.json',
      A/'prepare_nonflag_HGB40_complete_routes_v2_20261007.py',A/'nonflag_HGB40_complete_routes_source_preparation_v2_20261007.json',
      A/'run_nonflag_RidgeMicro40_official_comparison_v1_20261007.py',
      A/'prepare_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py',A/'seal_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py',
      A/'prepare_nonflag_RidgeMicro40_round131_sources_v1_20261007.py',A/'verify_nonflag_RidgeMicro40_round131_sources_v1_20261007.py',
      A/'run_nonflag_RidgeMicro40_round131_full_registration_v1_20261007.py',A/'predict_nonflag_residual_RidgeMicro_complete_scheme_20261007.py',
      A/'nonflag_residual_Ridge_native_stage_20261007.py',A/'nonflag_residual_HGB_CDF_transform_20261007.py',
      A/'nonflag_residual_HGB_preprocessing_20261007.py',A/'resolve_sealed_scientific_protocol_v2_20261007.py',
      A/'nonflag_residual_Ridge_native_hook3_preflight_20261007/verification.json',
      A/'nonflag_residual_Ridge10_actual_controls_github_20261007/receipt.json',
      *folder.glob('*.json'),*science.glob('*.json'),*science.glob('*.log'),
      *list((A/'nonflag_residual_Ridge_native_hook3_preflight_20261007').glob('*.json')),
      *list((A/'local_118_119_publication_contract_v5_actual_handoff_20261007').glob('*.json'))]
    sources += [A/'exact_native_JSON_archive_runtime_20261007.py',A/'exact_native_pretty_JSON_archive_20261007.py',A/'exact_native_JSON_full_board_benchmark_20261007/verification.json',A/'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',A/'handoff_nonflag_HGB40_archive_routes_v3_20261007.py',A/'nonflag_HGB40_archive_routes_v3_actual_handoff_20261007/verification.json',A/'resolve_sealed_scientific_protocol_v2_20261007.py']
    sources += [A/'prepare_nonflag_RidgeMicro40_science_routes_20261007.py',A/'nonflag_RidgeMicro40_science_route_preparation_v1_20261007.json',A/'prepare_nonflag_RidgeMicro40_science_routes_20261007.py',A/'nonflag_residual_Ridge_codec_20261007.py',A/'nonflag_residual_Ridge_bank10_20261007/verification.json',A/'nonflag_RidgeMicro40_science_route_preparation_v1_20261007.json']
    sources += [A/'nonflag_RidgeMicro40_round131_mapping_20261007.py',
        A/'nonflag_RidgeMicro40_science_route_preparation_v1_20261007.json',
        A/'nonflag_RidgeMicro40_round131_source_admission_v1_20261007.json',
        A/'nonflag_RidgeMicro40_prospective_routes_v2_20261007.json']
    if phase=='scores':
        for row in proof['records']:
            p=Path(row['official_score_cache']['official_metrics_source'])
            assert sha(p)==row['official_metric_capsule_sha256'] and read(p)['metrics']==row['metrics'];sources.append(p)
    sources += [A/'recover_nonflag_RidgeMicro131_after_actual_API_main_v2_20261007.py',A/'nonflag_RidgeMicro131_administrative_publication_recovery_v2_20261007.json',A/'file_backed_hidden_git_runtime_20261007.py',A/'publish_nonflag_RidgeMicro40_evidence_v2_20261007.py',A/'prepare_nonflag_RidgeMicro40_selected_candidate_v2_20261007.py',A/'seal_nonflag_RidgeMicro40_selected_candidate_v2_20261007.py',A/'run_nonflag_RidgeMicro40_round131_full_registration_v2_20261007.py']
    sources += [A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_scores_main_publication_v1/job_definition.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_scores_main_publication_v1/launch_result.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_scores_main_publication_v1/native_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_scores_main_publication_v1/service_execution.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_scores_main_publication_v1/verified_hidden_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_scores_main_publication_v1/stderr.log',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_scores_main_publication_v1/stdout.log',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_preparation_v1/job_definition.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_preparation_v1/launch_result.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_preparation_v1/native_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_preparation_v1/service_execution.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_preparation_v1/verified_hidden_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_preparation_v1/stderr.log',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_preparation_v1/stdout.log',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_sealing_v1/job_definition.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_sealing_v1/launch_result.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_sealing_v1/native_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_sealing_v1/service_execution.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_sealing_v1/verified_hidden_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_sealing_v1/stderr.log',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_sealing_v1/stdout.log',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v1/job_definition.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v1/launch_result.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v1/native_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v1/service_execution.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v1/verified_hidden_launch.json',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v1/stderr.log',A/'service_owned_workflows_20261006/nonflag_RidgeMicro40_round131_full_registration_v1/stdout.log']
    sources=list(dict.fromkeys(sources));out=A/f'nonflag_RidgeMicro40_{phase}_github_recovery_v2_20261007';assert not out.exists();out.mkdir()
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'phase':phase,'new_native_fits':0,'full131_not_yet_qualified':True})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        main7=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        import psutil
        from datetime import datetime
        deadline=datetime.fromisoformat('2026-10-07T23:45:00+08:00').timestamp()
        while any(psutil.Process(pid).status()==psutil.STATUS_STOPPED for pid in (main7['pid'],main7['owned_worker_pid'])):
            assert time.time()<deadline
            time.sleep(10)
        parent,worker,idle=suspended_idle(main7,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path(f'validation_sync/nonflag_RidgeMicro40_{phase}_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*sources,out/'frozen_before_main_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                raw=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'published_path':target,'original_sha256':raw,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_nonflag_RidgeMicro40_'+phase,
              'files':files,'previous_main':previous,'only_branch':'main','actual_full_control_cases':37,'actual_cold_prefix_cases':111,
              'new_quality_score_records':40 if phase=='scores' else 0,'new_native_fits':0,'full131_not_yet_qualified':True,
              'scientific_workers_stopped':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('非涨停残差Ridge：两组样本数归一化L2及等权集成，各12个新幅度，加三个合格锚点及消融，共40项。实际10年度成熟模型；37全量、111冷前缀和3历史原生核对。完整131候选须冻结、重放及QA42。仅main。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','上传非涨停残差Ridge的'+phase+'实际验证',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main','at_local':sync.now(),
              'raw_git_blobs_verified':len(hashes),'phase':phase,'new_quality_scores':40 if phase=='scores' else 0,'test_labels_read':False})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})

def main(phase):
    proof=A/'sparse_main_API_transport_recovery_20261007/receipt.json'
    while not proof.exists():time.sleep(2)
    assert read(proof)['status']=='pushed_and_remote_head_verified'
    from file_backed_hidden_git_runtime_20261007 import installed
    with installed(A/'RidgeMicro131_scores_file_IO_git_v2_20261007'):actual_main(phase)
    receipt=A/f'nonflag_RidgeMicro40_{phase}_github_recovery_v2_20261007/receipt.json'
    canonical=A/f'nonflag_RidgeMicro40_{phase}_github_v1_20261007/receipt.json'
    assert not canonical.exists()
    create(canonical,{**read(receipt),'actual_publication_recovery_driver':str(Path(__file__)),'original_failed_service_execution_retained':True})

if __name__=='__main__':main(sys.argv[1])
