"""Import actual connector commit and verify every original publication blob before completing main receipt."""
from pathlib import Path
import argparse,sys,json,hashlib,datetime,itertools,subprocess,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main(number):
    out=Path(f'E:/赛题五_本机临时/round{number}_connected_API_main_v1_20261008');b=read(out/'bundle.json');evidence=read(out/'actual_connected_API_responses.json')
    c=json.loads(evidence['raw_commit']['structuredContent']['content']);ref=json.loads(evidence['ref_after']['structuredContent']['content']);commit=c['sha']
    assert ref['object']['sha']==commit==evidence['commit']['structuredContent']['sha'];assert c['tree']['sha']==b['expected_exact_tree_sha']==evidence['tree']['structuredContent']['sha'];assert [p['sha'] for p in c['parents']]==[b['parent_commit']]
    assert c['verification']['signature'] is None
    def identity(v):return f"{v['name']} <{v['email']}> {int(datetime.datetime.fromisoformat(v['date'].replace('Z','+00:00')).timestamp())} "
    tz=['+0800','+0000']+[('+' if m>=0 else '-')+f'{abs(m)//60:02d}{abs(m)%60:02d}' for m in range(-12*60,14*60+1,15)]
    prefix='tree '+c['tree']['sha']+'\n'+''.join('parent '+p['sha']+'\n' for p in c['parents']);matched=None
    for at,ct,end in itertools.product(tz,tz,('','\n')):
        raw=(prefix+'author '+identity(c['author'])+at+'\ncommitter '+identity(c['committer'])+ct+'\n\n'+c['message']+end).encode('utf8')
        if hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==commit:matched=raw;break
    assert matched is not None,'The imported commit must match actual remote SHA exactly'
    work=Path(b['local_worktree'])
    def git(*args,cwd=work,data=None):
        r=subprocess.run(['git',*args],cwd=cwd,input=data,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=180);assert r.returncode==0,(args,r.stderr.decode('utf8',errors='replace'));return r.stdout
    assert git('rev-parse','HEAD').decode().strip()==b['parent_commit'];assert git('write-tree').decode().strip()==b['expected_exact_tree_sha'];assert git('hash-object','-w','-t','commit','--stdin',data=matched).decode().strip()==commit
    paths=sorted(b['files']);response=git('cat-file','--batch',data=''.join(f'{commit}:{p}\n' for p in paths).encode('utf8'));offset=0
    for path in paths:
        end=response.index(b'\n',offset);header=response[offset:end].split();assert len(header)==3 and header[1]==b'blob';size=int(header[2]);start=end+1;assert hashlib.sha256(response[start:start+size]).hexdigest()==b['files'][path]['sha256'],path;offset=start+size+1
    assert offset==len(response)
    old_branch=git('rev-parse','refs/heads/main').decode().strip();git('merge-base','--is-ancestor',old_branch,commit);git('update-ref','HEAD',commit,b['parent_commit']);git('update-ref','refs/heads/main',commit,old_branch);assert not git('status','--porcelain').strip()
    git('fetch','--no-tags',str(work),'main',cwd=ROOT)
    from file_backed_hidden_git_runtime_20261007 import installed
    from watch_validations_main_v2_20261005 import advance_source_index
    with installed(out/'actual_local_source_index_git_IO'):advance_source_index(commit)
    assert git('rev-parse','HEAD',cwd=ROOT).decode().strip()==commit
    manifest=b['manifest'];qa={135:46,144:55}[number]
    receipt={'status':'pushed_and_remote_head_verified','round':number,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'commit':commit,'parent':b['parent_commit'],'exact_tree_sha':b['expected_exact_tree_sha'],'branch':'main','remote':'https://github.com/'+b['repository_full_name']+'.git','official_score':manifest['metrics']['final_score'],'scored_records':manifest['scored_records'],'connected_records':manifest['connected_records'],'raw_git_blobs_verified':len(paths),'actual_full_QA_version':qa,'full_immutable_ranking_and_all_original_QA_preserved':True,'original_official_pilot_records_registered':manifest['scored_records'],'new_quality_scores_by_registration':0,'actual_connected_API_responses_sha256':sha(out/'actual_connected_API_responses.json'),'bundle_sha256':sha(out/'bundle.json'),'force_push':False,'scheme_url':'https://github.com/'+b['repository_full_name']+f'/tree/main/validation_sync/round{number}'}
    create(out/'verified_main_publication_receipt.json',receipt)
    print(json.dumps(receipt,ensure_ascii=False),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--round',type=int,choices=(135,144),required=True);main(p.parse_args().round)
