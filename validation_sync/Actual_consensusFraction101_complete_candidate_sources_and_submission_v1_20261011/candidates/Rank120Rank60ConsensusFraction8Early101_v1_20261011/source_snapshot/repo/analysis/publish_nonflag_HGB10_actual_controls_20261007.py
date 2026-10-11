"""Publish genuine nonflag10 fits and37 controls; choose a verified idle main-writer window."""
from pathlib import Path
import sys,time,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers
def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(10)
    assert read(f/'service_execution.json')['status']=='passed',name
def main():
    for name in ('nonflag_residual_HGB10_training','nonflag_residual_HGB37_transform_preflight','quantile_HGB88_pre_scoring_idle_handoff_v3','local_only_monitor_v16_exact_idle_handoff'):closed(name)
    original=A/'service_owned_workflows_20261006/flagged_HGB_weighted_quarters340_official_comparison'
    stage=read(A/'flagged_HGB_weighted_quarters340_official_comparison_20261007/actual_stage.json')
    early=owned(read(original/'native_launch.json')) and stage['actual_completed_cases']<320
    if not early:closed('quantile_HGB88_round119_full_registration_v3')
    bank=A/'nonflag_residual_HGB_bank10_20261007';bankproof=read(bank/'verification.json')
    assert bankproof['status']=='passed_actual10_nonflag_residual_HGB_mature_native_reload_independent_and_prefix_controls' and bankproof['actual_native_fits']==len(bankproof['actual_models'])==10
    controls=A/'nonflag_residual_HGB37_transform_preflight_20261007';proof=read(controls/'verification.json')
    assert proof['status']=='passed_actual37_full5635800_nonflag_residual_HGB_independent_CDF_and111_cold_controls' and len(proof['controls'])==37
    paths=[Path(__file__),*[p for p in A.glob('*20261007.py') if any(t in p.name for t in ('nonflag_residual_HGB','nonflag_HGB10','quantile_HGB88_routes_v3','quantile_HGB88_idle_waiters_v3','monitor_v16','runtime_v16'))],
      *[p for p in A.glob('*20261007.json') if any(t in p.name for t in ('nonflag_residual_HGB','quantile_HGB88_v3_prospective','quantile_HGB88_pre_scoring','quantile_HGB88_routes_source_preparation_v3','quantile_HGB88_complete_pipeline_actual_hidden_launches_v3','monitor_v16'))],
      *bank.glob('*.json'),*bank.glob('*/info_*.json'),*bank.glob('*/oof_verification.json'),*controls.glob('*.json'),
      *list((A/'nonflag_residual_HGB_codec2_preflight_20261007').glob('*.json')),
      *list((A/'quantile_HGB88_actual_idle_waiter_handoff_v3_20261007').glob('*.json')),
      *list((A/'local_only_monitor_v16_actual_handoff_20261007').glob('*.json'))]
    for name in ('nonflag_residual_HGB_codec2_preflight','nonflag_residual_HGB10_training_admission','nonflag_residual_HGB10_training','nonflag_residual_HGB37_transform_preflight','quantile_HGB88_pre_scoring_idle_handoff_v3','local_only_monitor_v16_exact_idle_handoff'):
        f=A/'service_owned_workflows_20261006'/name;paths+=list(f.glob('*.json'))+list(f.glob('*.log'))
    for name in ('quantile_HGB88_round119_source_admission','quantile_HGB88_full85_controls_main_publication','quantile_HGB88_official_comparison','quantile_HGB88_scores_main_publication','quantile_HGB88_selected_candidate_preparation','quantile_HGB88_selected_candidate_sealing','quantile_HGB88_round119_full_registration'):
        paths.append(A/'service_owned_workflows_20261006'/name/'administrative_supersession_before_any119_science_v3_20261007.json')
    paths=list(dict.fromkeys(paths));pins={**bankproof['input_sha256'],**proof['input_sha256'],**{str(p):sha(p) for p in paths}}
    out=A/'nonflag_HGB10_actual_controls_github_20261007';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'early_340_worker_still_live_writer_window':early,'completed340_at_window_observation':stage['actual_completed_cases'],
      'actual_native_fits':10,'new_official_quality_scores':0,'round120_complete_future_qualification_not_claimed':True})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        parent,worker,idle=suspended_idle(read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/nonflag_HGB10_actual_controls_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*paths,out/'frozen_before_main_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                raw=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'original_sha256':raw,'published_path':target,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual10_nonflag_residual_HGB_fits_and37_full111_cold_controls',
              'files':files,'previous_main':previous,'only_branch':'main','actual_native_fits':10,'actual_diagnostic_fits':2,
              'actual_full5635800_controls':37,'actual_cold_prefix_controls':111,'new_quality_scores':0,'elapsed_training_and_native_controls_seconds':bankproof['elapsed_seconds'],
              'round120_official40_future_candidate_QA31_not_claimed':True,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('新增非涨停残差HGB：7叶平方误差、15叶绝对误差，96迭代、最小叶256；每年只训练成熟历史OOF误差，特征为63项加106当前预测秩。\n'
              '实际10年度模型，原生256/8192、重载、独立解码和历史前缀逐位通过；37项完整训练区间CDF与111项冷前缀通过。\n'
              '临时大矩阵位于E盘。官方40项比较和完整120候选资格尚未执行；保留119封存状态修正及7个零科研执行等待任务的交接证据。仅main。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','上传非涨停残差HGB10模型及37全量111冷前缀验证',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main','raw_git_blobs_verified':len(hashes),'at_local':sync.now(),
              'actual_native_fits':10,'new_quality_scores':0,'scientific_workers_stopped':0,'test_labels_read':False})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})
if __name__=='__main__':main()
