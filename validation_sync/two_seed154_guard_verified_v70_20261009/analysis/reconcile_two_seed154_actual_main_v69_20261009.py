"""Independently verify committed69 bytes; retain post-push duplicate-local-receipt failure."""
from pathlib import Path
import sys,os,time,json,hashlib,gzip,subprocess
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/two_seed154_actual69_committed_blob_reconciliation_v1_20261009')
def main():
    import publish_classifier_consensus_workflows_20261006 as h
    OUT.mkdir(exist_ok=False)
    original=Path('E:/赛题五_本机临时/two_seed154_synthetic_main_v69_20261009')
    receipt=read(original/'receipt.json');commit=receipt['commit'];assert receipt['status']=='pushed_and_remote_head_verified'
    failure=A/'service_owned_workflows_20261006/two_seed154_actual_complete_controls_main_publication_v69_20261009/service_execution.json'
    assert read(failure)['status']=='failed' and 'two_seed154_synthetic_main_v68_receipt' in read(failure)['failure']
    guard=Path('E:/赛题五_本机临时/two_seed154_synthetic_safe_publication_v69_20261009/execution.json')
    assert read(guard)['primary_research_index_byte_exact_after_publication']
    index=sha(ROOT/'.git/index');assert index=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    current=h.sync.git('rev-parse','HEAD');h.verify_main(current);h.sync.git('merge-base','--is-ancestor',commit,current)
    frozen=read(original/'frozen_before_main_publication.json');paths={v['published_path']:v for v in frozen['files'].values()}
    prefix='validation_sync/two_seed154_synthetic_v69_20261009';names=sorted([*paths,prefix+'/manifest.json',prefix+'/.gitattributes'])
    request=''.join(f'{commit}:{p}\n' for p in names).encode('utf8');response=OUT/'committed_git_blobs.bin'
    with response.open('xb') as writer:
        subprocess.run(['git','cat-file','--batch'],cwd=h.sync.WORKTREE,input=request,stdout=writer,stderr=subprocess.PIPE,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    with response.open('rb') as reader:
        for p in names:
            header=reader.readline().split();assert len(header)==3 and header[1]==b'blob',p
            data=reader.read(int(header[2]));assert reader.read(1)==b'\n'
            if p in paths:
                raw=gzip.decompress(data) if p.endswith('.gz') else data
                assert hashlib.sha256(raw).hexdigest()==paths[p]['raw_sha256'] and len(raw)==paths[p]['original_bytes'],p
            elif p.endswith('manifest.json'):assert json.loads(data)['files']==frozen['files']
            else:assert data==b'* -text\n'
        assert not reader.read(1)
    assert len(names)==receipt['raw_git_blobs_verified']==991 and sha(ROOT/'.git/index')==index
    value={**receipt,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original69_post_push_local_receipt_failure_preserved':True,
        'actual_independently_reverified_git_blobs':len(names),'current_verified_main_at_reconciliation':current,
        'original_user_index_unchanged':True,'reconciliation_evidence':str(OUT/'verification.json')}
    create(OUT/'verification.json',{'status':'passed_actual69_all991_committed_blobs_and_remote_main_reverified',
        'input_sha256':{str(p):sha(p) for p in (Path(__file__),original/'receipt.json',original/'frozen_before_main_publication.json',failure,guard)},
        'receipt':value,'new_quality_scores':0,'new_inference':0,'test_labels_read':False})
    create(A/'two_seed154_actual_controls_main_v69_reconciled_receipt_20261009.json',value)
    print(value,flush=True)
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    with installed(Path('E:/赛题五_本机临时/two_seed154_actual69_reconciliation_git_IO_v1_20261009')):main()
