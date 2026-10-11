"""Publish completed local speed proofs and85 quantile controls to main before340 closes."""
from pathlib import Path
import sys,gzip,hashlib,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers
def main():
    for name in ('cached_official_spearman_full12_benchmark','quantile_HGB_full85_transform_preflight','quantile_HGB_native_hook7_preflight'):
        f=A/'service_owned_workflows_20261006'/name
        assert not owned(read(f/'native_launch.json')) and read(f/'service_execution.json')['status']=='passed'
    # All later writers depend on340 closing. Publish only while its real worker is active
    # and has at least40 cases left; otherwise retain the already-queued119 publisher.
    f=A/'service_owned_workflows_20261006/flagged_HGB_weighted_quarters340_official_comparison'
    assert owned(read(f/'native_launch.json'))
    stage=read(A/'flagged_HGB_weighted_quarters340_official_comparison_20261007/actual_stage.json')
    assert stage['actual_completed_cases']<300
    paths=[Path(__file__),*[p for p in A.glob('*20261007.py') if any(t in p.name for t in ('quantile_HGB','cached_official_spearman','exact_cached_validation_spearman'))],
      *[p for p in A.glob('*20261007.json') if any(t in p.name for t in ('quantile_HGB88','quantile_HGB_full85','quantile_HGB85','quantile_HGB_native_hook7','cached_official_spearman'))]]
    folders=['cached_official_spearman_full_scoring_benchmark_20261007','exact_cached_official_spearman_v2_edge_preflight_20261007',
      'exact_cached_validation_spearman_edge_preflight_20261007','quantile_HGB88_transform_preflight_20261007',
      'quantile_HGB_native_hook7_preflight_20261007','quantile_HGB_large_batch20_benchmark_20261007']
    for folder in folders:paths += list((A/folder).glob('*.json'))
    for name in ('cached_official_spearman_full12_benchmark','quantile_HGB_full85_transform_preflight','quantile_HGB_native_hook7_preflight'):
        f=A/'service_owned_workflows_20261006'/name;paths += list(f.glob('*.json'))+list(f.glob('*.log'))
    paths=list(dict.fromkeys(paths))
    proof=read(A/'cached_official_spearman_full_scoring_benchmark_20261007/verification.json')
    controls=read(A/'quantile_HGB88_transform_preflight_20261007/verification.json')
    assert proof['actual_uncached_official_evaluation_calls']==12 and len(controls['controls'])==85
    pins={**proof['input_sha256'],**controls['input_sha256'],**{str(p):sha(p) for p in paths}}
    out=A/'local_speed_and_quantile85_controls_github_20261007';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'completed340_at_writer_start':stage['actual_completed_cases'],
      'actual_official_equivalence_calls':12,'new_model_selection_scores':0,'full119_not_qualified':True})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        parent,worker,idle=suspended_idle(read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/local_speed_and_quantile85_controls_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*paths,out/'frozen_before_main_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                raw=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'original_sha256':raw,'published_path':target,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual12_official_speed_equivalence_and85_quantile_full_controls',
              'files':files,'previous_main':previous,'only_branch':'main','phase_speedup':proof['median_full_mapping_and_official_score_phase_speedup'],
              'actual_full5635800_transform_controls':85,'actual_cold_controls':255,'new_model_selection_scores':0,
              'full119_future_inference_and_QA30_not_claimed':True,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('本机评分提速：12次真实官方评分，全部预测字节、CSV和8项指标一致；固定训练验证标签秩仅用于评分。\n'
              '分位数HGB：85项完整5635800行独立CDF及255项历史前缀检查通过；7种原生组合历史603行核对通过。\n'
              '附119轮待执行完整方案源码，正式88项评分仍等待117及118资格和实际方案准入。未声明119已经完成。仅main。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','上传本机评分提速和分位数HGB85项全量验证',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main','raw_git_blobs_verified':len(hashes),
              'at_local':sync.now(),'scientific_workers_stopped':0,'new_model_selection_scores':0,'test_labels_read':False})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})
if __name__=='__main__':main()
