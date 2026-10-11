"""Serialize audit publication after the actual117 main publisher closes."""
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
    service=A/'service_owned_workflows_20261006'/name
    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)
    assert read(service/'service_execution.json')['status']=='passed',name

def main():
    closed('weighted_HGB340_round117_full_registration_v2')
    closed('HGB_quarter_grid_numerical_coverage_audit')
    proof_path=A/'HGB_quarter_grid_numerical_coverage_20261007/verification.json';proof=read(proof_path)
    assert len(proof['forecast_controls'])==84 and len(proof['distinct_numerical_validation_paths_requiring_future_official_comparison'])==24
    sources=[Path(__file__),A/'audit_HGB_quarter_grid_numerical_coverage_20261007.py',
      A/'prepare_HGB_quarter_numeric28_plan_20261007.py',A/'HGB_quarter_numeric28_plan_20261007.json',
      A/'HGB_quarter_grid_numerical_coverage_actual_launch_20261007.json',
      A/'weighted_HGB340_complete_pipeline_actual_hidden_launches_20261007.json',
      A/'start_weighted_HGB340_complete_local_pipeline_20261007.py',
      A/'run_weighted_HGB340_admitted_official_comparison_20261007.py',
      A/'prepare_local_monitor14_weighted_pipeline_20261007.py',A/'monitor_local_only_runtime_v14_20261007.py',
      A/'handoff_local_only_monitor_v14_20261007.py',A/'local_only_monitor_v14_actual_handoff_20261007/verification.json',
      *list((A/'HGB_quarter_grid_numerical_coverage_20261007').glob('*.json')),
      *list((A/'service_owned_workflows_20261006/HGB_quarter_grid_numerical_coverage_audit').glob('*.json'))]
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    out=A/'HGB_quarter_numeric_audit_github_v5_20261007';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'full118_not_yet_qualified':True})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/HGB_quarter_numeric_audit_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in dict.fromkeys([*sources,out/'frozen_before_main_publication.json']):
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                raw=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'original_sha256':raw,'published_path':target,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual7_raw_and84_full_forecast_numerical_coverage_controls',
              'files':files,'previous_main':previous,'actual_unscored_distinct_numerical_paths':24,'new_native_fits':0,'new_quality_scores':0,
              'complete118_scoring_candidate_QA29_main_not_claimed':True,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('同样的数学系数不保证浮点输出逐位相同。实际核对7种省略比例、84条完整验证预测，找到24条未评分的数值路径。\n'
              '这些路径须按训练期完整官方总分补充比较；其余60条预测与原88轮结果逐位一致。此记录不证明未来预测完成或全局优化穷尽。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','登记HGB四份集成浮点覆盖审计及24条待评分路径',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main','raw_git_blobs_verified':len(hashes),'new_quality_scores':0})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})

if __name__=='__main__':main()
