"""Preserve actual publisher payload and Git tree; await verified connected API main publication."""
from pathlib import Path
import sys,subprocess,hashlib,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
REPO='Zagadka-3906/stock-return-prediction'

def prepare_and_wait(number,payload,manifest):
    import publish_classifier_consensus_workflows_20261006 as helpers
    work=helpers.sync.WORKTREE;out=Path(f'E:/赛题五_本机临时/round{number}_connected_API_main_v1_20261008');out.mkdir(exist_ok=False)
    def git(*args):
        r=subprocess.run(['git',*args],cwd=work,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=180)
        assert r.returncode==0,r.stderr.decode('utf8',errors='replace');return r.stdout.decode('utf8').strip()
    assert not git('status','--porcelain');parent=git('rev-parse','HEAD');base=git('rev-parse',parent+'^{tree}')
    assert not git('branch','--show-current'), 'Keep existing detached publication clone'
    known={line.split(' ',1)[0] for line in git('rev-list','--objects',parent).splitlines()}
    for name,data in payload.items():assert not helpers.sync.SECRET.search(data);helpers.sync.atomic(work/name,data)
    paths=sorted(payload)
    for offset in range(0,len(paths),50):git('add','-f','--',*paths[offset:offset+50])
    staged=set(git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(paths)
    expected_tree=git('write-tree');entries=[];blobs=[];files={}
    for name in paths:
        data=payload[name];blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();files[name]={'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha':blob,'bytes':len(data)}
        element={'path':name,'mode':'100644','type':'blob'}
        if blob in known:element['sha']=blob
        else:
            try:
                text=data.decode('utf8');assert len(data)<2*1024**2;element['content']=text
            except (UnicodeDecodeError,AssertionError):
                target=out/'blobs'/blob;target.parent.mkdir(exist_ok=True);target.write_bytes(data)
                blobs.append({'sha':blob,'path':str(target),'bytes':len(data),'sha256':files[name]['sha256']});element['sha']=blob
        entries.append(element)
    bundle={'repository_full_name':REPO,'round':number,'parent_commit':parent,'parent_tree':base,'expected_exact_tree_sha':expected_tree,'tree_elements':entries,'binary_new_blobs':list({v['sha']:v for v in blobs}.values()),'files':files,'manifest':manifest,'local_worktree':str(work),'message':f'完成第{number}轮全部官方评分、候选推理及完整榜原始六视图QA（main连接器同步）','actual_publisher_transport_source_sha256':sha(Path(__file__))}
    create(out/'bundle.json',bundle)
    create(A/f'round{number}_connected_API_main_request_v1_20261008.json',{'status':'awaiting_actual_connected_API_main_publication_after_full_candidate_and_original_QA','bundle':str(out/'bundle.json'),'bundle_sha256':sha(out/'bundle.json'),'parent':parent,'expected_tree':expected_tree,'exported_files':len(files),'binary_new_blobs':len(bundle['binary_new_blobs']),'scored_records':manifest['scored_records'],'new_quality_scores':0})
    print(f'Round {number}: all native candidate and original full-board QA complete; exact {len(files)}-file tree ready for connected API publication.',flush=True)
    result=out/'verified_main_publication_receipt.json'
    while not result.exists():time.sleep(15)
    receipt=read(result);assert receipt['status']=='pushed_and_remote_head_verified' and receipt['exact_tree_sha']==expected_tree
    assert git('rev-parse','HEAD')==receipt['commit'] and not git('status','--porcelain')
    for name,info in files.items():assert sha(work/name)==info['sha256'],name
    create(A/f'github_validation_sync_main_20261005/round{number}_receipt.json',receipt)
    print(json.dumps(receipt,ensure_ascii=False),flush=True)

def execute_actual_publisher(number):
    name={135:'publish_BF16wide40_round135_full_validation_20261008.py',144:'publish_ConeRidgeAlpha100_round144_full_validation_20261008.py'}[number]
    source=A/name;value=source.read_text(encoding='utf8');needle="    previous = sync.git('rev-parse', 'HEAD')";assert value.count(needle)==1
    value=value[:value.index(needle)]+"    from connected_API_full_round_transport_v1_20261008 import prepare_and_wait\n    prepare_and_wait("+str(number)+",payload,manifest)\n"
    namespace={'__file__':str(source),'__name__':'actual_original_full_publisher_payload_with_connected_API_tail'}
    exec(compile(value,str(source),'exec'),namespace);namespace['main']()
