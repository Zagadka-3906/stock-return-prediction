"""Publish the measured codec control without claiming a pipeline or goal speedup."""
from pathlib import Path
import sys,time,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers
def main():
    folder=A/'service_owned_workflows_20261006/local_boundary_audit_v4_main_after121'
    while owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed'
    proof_path=A/'exact_early_string_lossless_codec_benchmark_20261007/verification.json'
    proof=read(proof_path)
    assert proof['status']=='passed_actual6_two_order_independent_report_subset_benchmarks_and_full12406_original_codebook_exact'
    out=A/'lossless_string_codec_benchmark_github_20261007';assert not out.exists();out.mkdir()
    sources=list(dict.fromkeys([Path(__file__),proof_path,proof_path.parent/'frozen_before_benchmark.json',*[Path(p) for p in proof['input_sha256']]]))
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(out/'frozen_before_publication.json',{'input_sha256':pins,'actual_pipeline_adoption':False,'new_quality_scores':0})
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/lossless_string_codec_benchmark_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*sources,out/'frozen_before_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data);raw=hashlib.sha256(data).hexdigest()
                target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[str(p.relative_to(ROOT))]={'published_path':target,'original_sha256':raw}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_codec_diagnostic_not_adopted',
                'files':files,'previous_main':previous,'branch':'main','actual_pipeline_adoption':False,
                'median_subset_speedup':proof['median_measured_subset_packing_speedup'],
                'full_old_packing_not_retimed':True,'whole_goal_speedup_not_measured':True,'new_quality_scores':0,'test_labels_read':False})
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload);sync.git('add','-f','--',*names)
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','记录完整榜编码加速对照：原始码表完全一致，未采用',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={k:hashlib.sha256(v).hexdigest() for k,v in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'actual_pipeline_adoption':False})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})
if __name__=='__main__':main()
