"""Independently verify the already-pushed81 payload, preserving the original79 receipt."""
from pathlib import Path
import sys,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,create,sha
OUT=Path('E:/赛题五_本机临时/main81_published_receipt_reconciliation_v82_20261009')
def main():
    OUT.mkdir(exist_ok=False)
    import publish_classifier_consensus_workflows_20261006 as h
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    original=read(A/'actual154_corrected_receivers_cache_cleanup_main_v79_receipt_20261009.json');old_sha=sha(A/'actual154_corrected_receivers_cache_cleanup_main_v79_receipt_20261009.json')
    receipt=read(Path('E:/赛题五_本机临时/actual154_corrected_receivers_cache_cleanup_main_v81_20261009/receipt.json'))
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['commit']!=original['commit']
    prefix=Path('validation_sync/actual154_corrected_receivers_cache_cleanup_v81_20261009')
    with git_io(OUT/'git_read_only'):
        sync=h.sync;manifest=read(sync.WORKTREE/prefix/'manifest.json');files=manifest['files'];hashes={}
        for binding in files.values():
            p=sync.WORKTREE/binding['published_path'];raw=p.read_bytes();hashes[binding['published_path']]=hashlib.sha256(raw).hexdigest()
            decoded=gzip.decompress(raw) if p.suffix=='.gz' else raw
            assert len(decoded)==binding['original_bytes'] and hashlib.sha256(decoded).hexdigest()==binding['raw_sha256'],p
        for name in ('.gitattributes','manifest.json'):
            p=sync.WORKTREE/prefix/name;hashes[(prefix/name).as_posix()]=sha(p)
        assert len(hashes)==receipt['raw_git_blobs_verified'];assert h.blob_hashes(receipt['commit'],hashes)==hashes
        remote=sync.git('ls-remote','origin','refs/heads/main').split()[0]
        sync.git('merge-base','--is-ancestor',receipt['commit'],remote)
    assert sha(A/'actual154_corrected_receivers_cache_cleanup_main_v79_receipt_20261009.json')==old_sha
    proof={'status':'passed_all81_committed_blobs_raw_payload_hashes_and_remote_main_ancestry_after_local_receipt_collision',
        'commit':receipt['commit'],'remote_main_at_verification':remote,'actual_git_blobs_verified':len(hashes),
        'original79_receipt_preserved_sha256':old_sha,'no_new_commit_push_model_fits_or_scores':True,
        'test_labels_read':False,'input_sha256':{str(Path(__file__)):sha(__file__)}}
    create(OUT/'verification.json',proof);create(A/'main81_published_receipt_reconciliation_v82_20261009.json',proof)
    create(A/'actual154_full_import_and155_dependencies_main_v81_reconciled_receipt_20261009.json',dict(receipt,reconciliation=str(A/'main81_published_receipt_reconciliation_v82_20261009.json')))
    print(proof,flush=True)
if __name__=='__main__':
    import os
    n=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{n+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{n+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(n+2);main()
