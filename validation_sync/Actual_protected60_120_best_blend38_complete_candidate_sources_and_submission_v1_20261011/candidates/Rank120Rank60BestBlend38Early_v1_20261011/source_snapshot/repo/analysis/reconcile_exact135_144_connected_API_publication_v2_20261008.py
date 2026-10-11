"""Verify the actual remote tree and immutable blobs, import its exact commit, release fresh score receipts."""
from pathlib import Path
import sys,json,hashlib,datetime,subprocess,gzip,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
E=Path('E:/赛题五_本机临时/exact135_144_scores_connected_API_v1_20261008')

def main():
    b=read(E/'bundle.json');responses=read(E/'actual_connected_API_responses.json')
    raw=json.loads(responses['raw_commit']['structuredContent']['content']);ref=json.loads(responses['ref_after']['structuredContent']['content'])
    commit=raw['sha'];assert ref['object']['sha']==commit==responses['commit']['structuredContent']['sha']
    assert raw['tree']['sha']==b['expected_exact_tree_sha']==responses['tree']['structuredContent']['sha']
    assert [p['sha'] for p in raw['parents']]==[b['parent_commit']] and raw['verification']['signature'] is None
    def identity(v):
        date=datetime.datetime.fromisoformat(v['date'].replace('Z','+00:00'));return f"{v['name']} <{v['email']}> {int(date.timestamp())} +0000"
    prefix='tree '+raw['tree']['sha']+'\n'+''.join('parent '+p['sha']+'\n' for p in raw['parents'])+'author '+identity(raw['author'])+'\ncommitter '+identity(raw['committer'])+'\n\n'
    verified=(E/'actual_verified_raw_commit.bin').read_bytes()
    assert hashlib.sha1(b'commit '+str(len(verified)).encode()+b'\0'+verified).hexdigest()==commit
    assert verified.decode('utf8').split('\n\n',1)[1]==raw['message']
    assert verified.startswith(('tree '+raw['tree']['sha']+'\nparent '+b['parent_commit']+'\n').encode())
    matched=[verified]
    work=Path(b['local_worktree'])
    def git(*args,cwd=work,data=None):
        r=subprocess.run(['git',*args],cwd=cwd,input=data,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=180)
        assert r.returncode==0,(args,r.stderr.decode('utf8',errors='replace'));return r.stdout
    assert git('write-tree').decode().strip()==b['expected_exact_tree_sha']
    assert git('hash-object','-w','-t','commit','--stdin',data=matched[0]).decode().strip()==commit
    expected={p:v['sha256'] for p,v in b['files'].items()}
    paths=sorted(expected);response=git('cat-file','--batch',data=''.join(f'{commit}:{p}\n' for p in paths).encode('utf8'));offset=0
    for p in paths:
        end=response.index(b'\n',offset);header=response[offset:end].split();assert len(header)==3 and header[1]==b'blob',p
        size=int(header[2]);start=end+1;assert hashlib.sha256(response[start:start+size]).hexdigest()==expected[p],p;offset=start+size+1
    assert offset==len(response)
    for phase in b['phases'].values():
        for source,info in phase['files'].items():
            if Path(source).exists():assert sha(source)==info['raw_sha256'],source
            else:
                target=work/info['published_path'];assert target.suffix=='.gz' and hashlib.sha256(gzip.decompress(target.read_bytes())).hexdigest()==info['raw_sha256'],source
    old=git('rev-parse','refs/heads/main').decode().strip();assert old==b['parent_commit']
    git('update-ref','refs/heads/main',commit,old)
    assert not git('status','--porcelain').strip()
    git('fetch','--no-tags',str(work),'main',cwd=ROOT)
    from file_backed_hidden_git_runtime_20261007 import installed
    from watch_validations_main_v2_20261005 import advance_source_index
    with installed(E/'source_index_local_only_git_IO'):advance_source_index(commit)
    assert git('rev-parse','HEAD',cwd=ROOT).decode().strip()==commit
    proof={'status':'passed_exact140_official_score_connected_API_main_publication_and_local_commit_import','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'commit':commit,'parent':b['parent_commit'],'tree':b['expected_exact_tree_sha'],'raw_git_blobs_verified':len(expected),'official_score_records':140,'remote_API_response_sha256':sha(E/'actual_connected_API_responses.json'),'bundle_sha256':sha(E/'bundle.json'),'local_main_heads_match_remote':True,'only_branch_updated':'main','force_push':False,'test_labels_read':False,'new_quality_scores':0}
    create(E/'reconciliation_verification.json',proof)
    outputs={'135':'BF16wide40_scores_github_v3_20261008','144':'ConeRidgeAlpha100_scores_github_v2_20261008'}
    for number,name in outputs.items():
        folder=A/name;folder.mkdir(exist_ok=False);phase=b['phases'][number]
        create(folder/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':proof['at_local'],'branch':'main','commit':commit,'official_score_records':phase['official_score_records'],'raw_git_blobs_verified':sum(p.startswith(phase['prefix']+'/') for p in expected),'actual_best':phase['actual_best'],'exact_tree_sha':proof['tree'],'connected_API_publication_proof':str(E/'reconciliation_verification.json'),'connected_API_publication_proof_sha256':sha(E/'reconciliation_verification.json'),'url':'https://github.com/'+b['repository_full_name']+'/tree/main/'+phase['prefix'],'original_failed_transport_evidence_preserved':True,'new_quality_scores_by_publication':0,'test_labels_read':False})
    create(A/'exact135_144_connected_API_reconciliation_v2_20261008.json',proof)
    print(json.dumps(proof,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
