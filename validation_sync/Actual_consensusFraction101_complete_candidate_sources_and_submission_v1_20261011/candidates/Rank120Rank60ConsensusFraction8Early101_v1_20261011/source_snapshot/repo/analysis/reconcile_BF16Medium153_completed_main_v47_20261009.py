"""Verify every committed153 blob after successful push and duplicate local receipt failure."""
from pathlib import Path
import sys,os,time,json,hashlib,gzip,subprocess
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/BF16Medium153_committed_full_QA_reconciliation_v47_20261009')
def main():
    import publish_classifier_consensus_workflows_20261006 as h
    OUT.mkdir(exist_ok=False)
    guard=Path('E:/赛题五_本机临时/BF16Medium153_completed_QA_main_safe_v43_20261009/execution.json');g=read(guard)
    assert g['research_index_bytes_unchanged'];commit=g['main_ref_updates'][-1]['main_commit']
    failure=A/'service_owned_workflows_20261006/BF16Medium78_round153_full_registration_v2_20261009/service_execution.json'
    assert read(failure)['status']=='failed' and 'round153_receipt.json' in read(failure)['failure']
    current=h.sync.git('rev-parse','HEAD');h.verify_main(current);h.sync.git('merge-base','--is-ancestor',commit,current)
    index=sha(ROOT/'.git/index');assert index=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    prefix='validation_sync/round153';manifestpath=prefix+'/manifest.json'
    manifest=json.loads(h.sync.git('show',f'{commit}:{manifestpath}'));files=manifest['exported_files']
    assert manifest['actual_complete_QA_version']==64 and manifest['immutable_all_values_lossless_display_and_complete_original_QA_published']
    assert manifest['scored_records']==78 and manifest['connected_records']==15310
    assert manifest['metrics']['final_score']==read(A/'BF16Medium78_official_comparison_v1_20261009/verification.json')['best']['connected_final_score']
    names=sorted(h.sync.git('-c','core.quotepath=false','ls-tree','-r','--name-only',commit,'--',prefix+'/').splitlines())
    assert set(names)==set(files)|{manifestpath},set(names)^(set(files)|{manifestpath})
    response=OUT/'committed_git_blobs.bin';request=''.join(f'{commit}:{p}\n' for p in names).encode('utf8')
    with response.open('xb') as writer:
        subprocess.run(['git','cat-file','--batch'],cwd=h.sync.WORKTREE,input=request,stdout=writer,stderr=subprocess.PIPE,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    with response.open('rb') as reader:
        for path in names:
            header=reader.readline().split();assert len(header)==3 and header[1]==b'blob',path
            data=reader.read(int(header[2]));assert reader.read(1)==b'\n'
            if path==manifestpath:assert json.loads(data)==manifest
            else:assert len(data)==files[path]['bytes'] and hashlib.sha256(data).hexdigest()==files[path]['sha256'],path
        assert not reader.read(1)
    # Verify the split original archive as a continuous stream as well as every
    # committed chunk; all4GB of reconstructed report bytes remain recoverable.
    for key,descriptor in g['chunked_original_artifacts'].items():
        parts=descriptor['parts'];digest=hashlib.sha256();joined=OUT/'complete_original_report.json.gz'
        with joined.open('xb') as writer:
            for part in parts:
                path=str(Path(key).parent/part['path']).replace('\\','/')
                data=h.sync.WORKTREE.joinpath(path).read_bytes()
                assert hashlib.sha256(data).hexdigest()==part['sha256'] and len(data)==part['bytes']
                assert path in files and files[path]['sha256']==part['sha256']
                writer.write(data);digest.update(data)
        assert digest.hexdigest()==descriptor['compressed_sha256'] and joined.stat().st_size==descriptor['compressed_bytes']
        with gzip.open(joined,'rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==descriptor['original_report_sha256']
    folder=A/'optimization_20261003_r153';scope=read(folder/'provenance_scope_execution.json');assert scope['status']=='passed'
    for f,d in scope['input_sha256'].items():assert sha(f)==d,f
    assert sha(ROOT/'.git/index')==index
    oldreceipt=A/'github_validation_sync_main_20261005/round153_receipt.json';old=read(oldreceipt)
    create(A/'round153_original_watcher_receipt_before_full_QA_reconciliation_v47_20261009.json',old)
    value={**old,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'commit':commit,'raw_git_blobs_verified':len(names),
        'actual_full_QA_version':64,'actual_all_committed_full_QA_and_original_archive_bytes_reverified':True,
        'original_duplicate_receipt_failure_preserved':True,'old_watcher_commit_preserved':old['commit'],
        'reconciliation_evidence':str(OUT/'verification.json')}
    proof={'status':'passed_all_committed153_blobs_QA64_original_report_stream_remote_main_and_frozen_sources',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),guard,failure,folder/'provenance_scope_execution.json')},
        'receipt':value,'actual_committed_blobs':len(names),'actual_scored_records':78,'actual_connected_records':15310,
        'original_user_index_bytes_unchanged':True,'new_quality_scores':0,'new_inference':0,'test_labels_read':False}
    create(OUT/'verification.json',proof);create(A/'BF16Medium153_committed_full_QA_main_reconciliation_v47_20261009.json',proof)
    temporary=oldreceipt.with_name(oldreceipt.name+f'.{os.getpid()}.tmp');temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(temporary,oldreceipt)
    create(folder/'full_registration_execution.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'existing_official_scores_registered':78,'full_rankings_all_original_QA_and_main_publication_completed':True,
        'actual_full_QA_version':64,'all_commit_blobs_and_reconstructed_archive_independently_reverified':True,
        'new_quality_scores_by_registration':0,'new_inference_claimed_by_registration':False,'test_labels_read':False,
        'original_full1_and_duplicate_receipt_full2_failures_preserved':True,'main_receipt':value})
    print({'passed153_full_QA_and_main':True,'verified_blobs':len(names),'commit':commit},flush=True)
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    with installed(OUT.with_name(OUT.name+'_git_IO')):main()
