from pathlib import Path
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from scoped_user_cleanup_package134_runtime_v1_20261011 import install
gates=install()
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    assert gates.allowed();gates.closed('actual_fraction101_scoped_main134_v1_20261011')
    bundle=A/'actual_fraction101_delivery_bundle137_verification_v1_20261011.json';b=read(bundle)
    assert b['status']=='passed_complete_sealed_candidate_bundle_every_archive_entry_SHA256_verified' and sha(b['archive'])==b['archive_sha256']
    pointer=A/'complete191_plus_completed_raw_TRAIN_score_catalog_location_v7_20261011.json';catalog=Path(read(pointer)['output']);report=read(catalog/'verification.json')
    assert sha(catalog/'verification.json')==read(pointer)['verification_sha256'] and report['score_tables_bytes_unchanged_from_v5'] and report['total_score_instances']==18959
    deliverypointer=A/'alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json';directory=Path(read(deliverypointer)['output'])
    paths=[Path(__file__),bundle,pointer,deliverypointer,*catalog.glob('*.csv'),catalog/'verification.json',catalog/'说明.md',directory/'方案使用说明.md',directory/'方案包核验.json',directory/'submission_manifest.json']
    for token in ['134','135','136','137']:
        paths += [p for p in A.glob(f'*{token}*20261011*') if p.is_file() and p.suffix in ['.py','.json'] and any(t in p.name for t in ['scoped','cleanup','bundle','unadopted','unselected','matrix_same_bytes','bounded_authorization'])]
    paths += [A/n for n in ['resume_partial_fraction101_seal131_v1_20261011.py','continue_fraction101_after_disk_boundary132_v1_20261011.py','publish_fraction101_same_bytes_archive_reuse130_v1_20261011.py','actual_completed_main_publication_archives126_same_bytes_deduplication_v1_20261011.json','actual_explicit_nonadopted_medium_horizon_weights128_cleanup_plan_v1_20261011.json','actual_explicit_nonadopted_medium_horizon_weights128_cleanup_verification_v1_20261011.json','actual_user1300_final_status_and_exact_resume_manifest_v1_20261011.json']]
    for name in ['actual_fraction101_scoped_seal134_v1_20261011','actual_fraction101_scoped_main134_v1_20261011','actual_fraction101_partial_seal131_v1_20261011','actual_fraction101_disk_boundary_full_continuation132_v1_20261011']:
        folder=A/'service_owned_workflows_20261006'/name
        paths += [folder/n for n in ['native_launch.json','service_execution.json','job_definition.json'] if (folder/n).is_file()]
    for result in [read(A/'actual_unselected_banks135_cleanup_plan_v1_20261011.json'),read(A/'actual_unadopted_BF16micro134_cleanup_plan_v1_20261011.json')]:
        paths += [Path(p) for p in result['preserved_sha256'] if Path(p).suffix=='.json' and Path(p).is_file() and Path(p).stat().st_size<2000000]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/Actual_fraction101_complete_bundle_catalog_v7_and_discarded_weights_cleanup137_20261011');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'complete_higher_score_candidate_archive_checked_all_entries_latest_catalog_and_unused_model_cleanup_records','archive_weights_kept_locally_E_not_uploaded_as_binary_models':True,'S':b['official_TRAIN_internal_score'],'formal192_not_complete':True,'optimization_goal_remains_paused':True,'new_training':0,'new_scoring':0,'new_inference':0,'test_labels_read':False,'files':bindings})
    out=Path('E:/赛题五_本机临时/Actual_fraction101_bundle_catalog_cleanup137_main_v1_20261011');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    identity=read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json');assert not owned(identity)
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire();assert gates.allowed() and not owned(identity)
        sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
        for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
        names=sorted(payload)
        for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','封装S0.45146122完整37模型方案：核验ZIP全部条目、更新18959项评分明细并记录弃用权重清理',timeout=180)
        commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
        receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
        create(out/'receipt.json',receipt);create(A/'Actual_fraction101_bundle_catalog_cleanup137_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
