"""Verify existing pushed33 blobs and branch; complete the missing receipt without new commit."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,gzip,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def allowed():
    now=datetime.now(timezone(timedelta(hours=8)))
    return all(c['status']=='optimization_active_after_explicit_manual_resume' and now<datetime.fromisoformat(c['stop_at_local']) for c in (read(A/n) for n in ('current_user_runtime_control_20261009.json','current_user_runtime_control_20261010.json')))

def main():
    assert allowed()
    failed=A/'service_owned_workflows_20261006/actual_stock_identity_prior_screen33_completion_main_v14_20261010'
    assert not owned(read(failed/'native_launch.json')) and read(failed/'service_execution.json')['status']=='failed'
    assert 'TimeoutExpired' in read(failed/'service_execution.json')['failure']
    original=Path('E:/赛题五_本机临时/high_impact_priority_huber65_main_v14_20261010')
    bindings=read(original/'frozen_before_publication.json')['files']
    # The original push succeeded and the exception occurred at verify_main(commit).
    assert 'line 63' in (failed/'stderr.log').read_text(encoding='utf8')
    out=Path('E:/赛题五_本机临时/stock33_already_pushed_main_reconciliation_v1_20261010');out.mkdir(exist_ok=False)
    import publish_classifier_consensus_workflows_20261006 as h
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_runtime_v1_20261010 import hold
    with serial(out/'mutex.json') as mutex,safe(out/'safe'),git_io(out/'git'):
        mutex.acquire();assert allowed()
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json')
        parent,worker,idle=hold(launch,'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;commit=sync.git('rev-parse','HEAD');assert not sync.git('status','--porcelain')
            prefix=Path('validation_sync/high_impact_priority_huber65_v14_20261010')
            manifest=read(sync.WORKTREE/prefix/'manifest.json')
            assert manifest['screen_records']==33 and manifest['screen_full_and_prefix_checks']==[32,96] and manifest['files']==bindings
            hashes={}
            for source,row in bindings.items():
                assert sha(source)==row['raw_sha256'],source
                name=row['published_path'];p=sync.WORKTREE/name;data=p.read_bytes()
                assert hashlib.sha256(gzip.decompress(data) if name.endswith('.gz') else data).hexdigest()==row['raw_sha256'],name
                hashes[name]=hashlib.sha256(data).hexdigest()
            for suffix in ('manifest.json','.gitattributes'):
                name=(prefix/suffix).as_posix();hashes[name]=sha(sync.WORKTREE/name)
            assert h.blob_hashes(commit,hashes)==hashes
            h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','phase':'huber65','commit':commit,'branch':'main','raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix(),'submission_qualified':False,'original_push_reused':True,'new_commit_created':False,'new_scoring_or_inference':False}
            create(original/'receipt.json',receipt);create(A/'high_impact_priority_huber65_main_receipt_v14_20261010.json',receipt)
            create(out/'verification.json',{'status':'passed_all_original33_publication_blobs_and_remote_main_after_timeout','receipt':receipt,'original_failure_retained':True,'blob_sha256':hashes})
            print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
