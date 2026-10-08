"""Verify the actual API main commit via native Git when connector reads fail; preserve failed receipts."""
from pathlib import Path
import sys,json,hashlib,subprocess,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
E=Path('E:/赛题五_本机临时/exact138_scores_connected_API_v1_20261008')
def main():
    b=read(E/'bundle.json');responses=read(E/'actual_connected_API_mutation_responses.json')
    commit=responses['commit']['structuredContent']['sha'];assert responses['update_ref']['structuredContent']['success'] is True
    assert responses['tree']['structuredContent']['sha']==b['expected_exact_tree_sha']
    work=Path(b['local_worktree']);calls=[]
    def git(*args,cwd=work,data=None):
        for attempt in range(5):
            r=subprocess.run(['git',*args],cwd=cwd,input=data,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=240)
            calls.append({'args':list(args),'returncode':r.returncode,'stderr':r.stderr.decode('utf8',errors='replace')[:2000]})
            if r.returncode==0:return r.stdout
            if args[0] not in ('ls-remote','fetch') or attempt==4:raise RuntimeError(str(calls[-1]))
            time.sleep(2**attempt)
    remote=git('ls-remote','--heads','origin').decode().splitlines()
    assert remote==[commit+'\trefs/heads/main'],remote
    git('fetch','--no-tags','origin','main')
    raw=git('cat-file','commit',commit)
    assert hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==commit
    assert raw.startswith(('tree '+b['expected_exact_tree_sha']+'\nparent '+b['parent_commit']+'\n').encode())
    assert raw.split(b'\n\n',1)[1].decode()=='同步第138轮BF16宽网络实际证据 scores'
    (E/'actual_verified_raw_commit.bin').write_bytes(raw)
    assert git('write-tree').decode().strip()==b['expected_exact_tree_sha']
    paths=sorted(b['files']);data=git('cat-file','--batch',data=''.join(f'{commit}:{p}\n' for p in paths).encode());offset=0
    for p in paths:
        end=data.index(b'\n',offset);header=data[offset:end].split();assert len(header)==3 and header[1]==b'blob',p
        size=int(header[2]);start=end+1;content=data[start:start+size]
        assert hashlib.sha256(content).hexdigest()==b['files'][p]['sha256'],p
        assert header[0].decode()==b['files'][p]['git_blob_sha'],p
        offset=start+size+1
    assert offset==len(data)
    old=b['original_failed_push_commit'];assert git('rev-parse','HEAD').decode().strip()==old
    old_branch=git('rev-parse','refs/heads/main').decode().strip();assert old_branch in (old,b['parent_commit'])
    assert git('rev-parse',old+'^{tree}').decode().strip()==b['expected_exact_tree_sha']
    assert git('rev-parse',old+'^').decode().strip()==b['parent_commit']
    assert not git('branch','--show-current').strip()
    git('update-ref','HEAD',commit,old);git('update-ref','refs/heads/main',commit,old_branch)
    assert not git('status','--porcelain').strip()
    git('fetch','--no-tags',str(work),'main',cwd=ROOT)
    from file_backed_hidden_git_runtime_20261007 import installed
    from watch_validations_main_v2_20261005 import advance_source_index
    with installed(E/'source_index_local_only_git_IO_v2'):advance_source_index(commit)
    assert git('rev-parse','HEAD',cwd=ROOT).decode().strip()==commit
    create(E/'actual_native_remote_and_blob_verification_calls.json',{'calls':calls,'remote_heads':remote})
    proof={'status':'passed_exact40_official_scores_connected_API_main_publication_and_native_remote_verification','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'commit':commit,'parent':b['parent_commit'],'tree':b['expected_exact_tree_sha'],'raw_git_blobs_verified':len(paths),'official_score_records':40,
        'API_response_sha256':sha(E/'actual_connected_API_mutation_responses.json'),'actual_native_remote_verification_sha256':sha(E/'actual_native_remote_and_blob_verification_calls.json'),
        'bundle_sha256':sha(E/'bundle.json'),'local_main_heads_match_remote':True,'only_branch_updated':'main','force_push':False,'test_labels_read':False,'new_quality_scores':0,
        'original_failed_push_commit_and_logs_preserved':old,'native_remote_read_used_after_connector_transport_failure':True}
    create(E/'reconciliation_verification_v2.json',proof)
    out=A/'BF16reverse40_scores_github_v3_20261008';out.mkdir(exist_ok=False)
    pilot=read(A/'BF16reverse40_official_comparison_v1_20261008/verification.json')
    create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':proof['at_local'],'branch':'main','commit':commit,
        'official_score_records':40,'raw_git_blobs_verified':len(paths),'actual_best':pilot['best'],'exact_tree_sha':proof['tree'],
        'connected_API_publication_proof':str(E/'reconciliation_verification_v2.json'),'connected_API_publication_proof_sha256':sha(E/'reconciliation_verification_v2.json'),
        'url':'https://github.com/'+b['repository_full_name']+'/tree/main/validation_sync/BF16reverse40_scores_20261008','original_failed_transport_evidence_preserved':True,
        'new_quality_scores_by_publication':0,'test_labels_read':False})
    create(A/'exact138_connected_API_reconciliation_v2_20261008.json',proof)
    print(json.dumps(proof,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
