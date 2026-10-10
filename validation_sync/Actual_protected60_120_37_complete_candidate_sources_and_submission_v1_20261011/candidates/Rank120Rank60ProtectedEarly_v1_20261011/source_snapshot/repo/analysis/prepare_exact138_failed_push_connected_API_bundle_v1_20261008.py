"""Extract only the215 immutable UTF8 blobs of the failed40-score push; no new score or model choice."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
WORK=Path('D:/3.Study/数据分析/赛题五_GitHub验证同步_20261005');OUT=Path('E:/赛题五_本机临时/exact138_scores_connected_API_v1_20261008')
def git(*args,data=None):
    p=subprocess.run(['git',*args],cwd=WORK,input=data,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=60)
    assert p.returncode==0,(args,p.stderr[:1000]);return p.stdout
def main():
    assert read(A/'service_owned_workflows_20261006/BF16reverse40_scores_main_publication_v15_20261008/service_execution.json')['status']=='failed'
    assert not git('status','--porcelain')
    commit=git('rev-parse','HEAD').decode().strip();assert commit=='da13764c15b3326ea66ddb9141809d5c34521fae'
    parent=git('rev-parse','HEAD^').decode().strip();assert parent=='e473a93cfe4af9a74c7555aef03600c287a85d7b'
    tree=git('rev-parse','HEAD^{tree}').decode().strip();base=git('rev-parse','HEAD^^{tree}').decode().strip()
    paths=git('-c','core.quotepath=false','diff','--name-only',parent,commit).decode('utf8').splitlines();assert len(paths)==215
    assert all(p.startswith('validation_sync/BF16reverse40_scores_20261008/') for p in paths)
    response=git('cat-file','--batch',data=''.join(f'{commit}:{p}\n' for p in paths).encode());offset=0;elements=[];files={}
    for path in paths:
        end=response.index(b'\n',offset);header=response[offset:end].split();assert header[1]==b'blob'
        size=int(header[2]);start=end+1;data=response[start:start+size];offset=start+size+1
        content=data.decode('utf8');assert content.encode('utf8')==data
        elements.append({'path':path,'mode':'100644','type':'blob','content':content})
        files[path]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha':header[0].decode()}
    assert offset==len(response) and sum(x['bytes'] for x in files.values())==1593105
    assert not OUT.exists();OUT.mkdir()
    create(OUT/'create_tree_request.json',{'repository_full_name':'Zagadka-3906/stock-return-prediction','base_tree_sha':base,'tree_elements':elements})
    create(OUT/'bundle.json',{'status':'frozen_exact_215_UTF8_blobs_from_original_failed_push_commit',
        'repository_full_name':'Zagadka-3906/stock-return-prediction','local_worktree':str(WORK),'original_failed_push_commit':commit,
        'parent_commit':parent,'parent_tree_sha':base,'expected_exact_tree_sha':tree,'files':files,'official_score_records':40,
        'request_sha256':sha(OUT/'create_tree_request.json'),'new_quality_scores':0,'test_labels_read':False})
    create(A/'exact138_scores_connected_API_bundle_location_v1_20261008.json',{'status':'prepared_exact_failed_push_tree_before_connected_API_publish','output':str(OUT),'bundle_sha256':sha(OUT/'bundle.json')})
    print(json.dumps({'request':str(OUT/'create_tree_request.json'),'files':len(files),'tree':tree,'parent':parent}),flush=True)
if __name__=='__main__':main()
