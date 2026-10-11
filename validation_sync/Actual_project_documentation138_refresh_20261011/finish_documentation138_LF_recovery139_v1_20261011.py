from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
import publish_classifier_consensus_workflows_20261006 as h
OUT=Path('E:/赛题五_本机临时/项目文档重写138_20261011')
RECOVERY=OUT/'LF_recovery139';RECOVERY.mkdir(exist_ok=False)
snapshot=read(OUT/'frozen_before_documentation_publication.json')
original=dict(snapshot['document_sha256']);names=sorted(original)
snapshot['document_sha256']={name:sha(ROOT/name) for name in names}
assert [name for name in names if original[name]!=snapshot['document_sha256'][name]]==['docs/latest_results.json']
oldraw=h.sync.git('show','e910d03f8b8ae11ca418094e8f1399440a51aa89:docs/latest_results.json')
assert read(ROOT/'docs/latest_results.json')==h.sync.json.loads(oldraw)
create(RECOVERY/'recovery_plan.json',{'status':'original_post_commit_raw_hash_check_failed_only_new_JSON_Git_LF_normalization_no_content_difference','original_unpushed_commit':'e910d03f8b8ae11ca418094e8f1399440a51aa89','old_JSON_sha256':original['docs/latest_results.json'],'normalized_JSON_sha256':snapshot['document_sha256']['docs/latest_results.json'],'actual_documentation_content_unchanged':True,'original_failure_preserved':True})
prefix=Path('validation_sync/Actual_project_documentation138_refresh_20261011')
new={str(prefix/'verification.json').replace('\\','/'):h.sync.encoded(snapshot),str(prefix/'line_ending_recovery139.json').replace('\\','/'):h.sync.encoded(read(RECOVERY/'recovery_plan.json')),str(prefix/Path(__file__).name).replace('\\','/'):Path(__file__).read_bytes()}
from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
from serial_main_publication_mutex_v1_20261009 import installed as serial
from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
os.environ['GIT_CONFIG_COUNT']=str(count+2)
controls=[read(A/f'current_user_runtime_control_202610{d}.json') for d in ('10','09')];now=datetime.now(timezone(timedelta(hours=8)))
assert all(c['status']=='project_workers_stopped_until_actual_user_manual_continue' and c['automatic_restart_enabled'] is False for c in controls)
with serial(RECOVERY/'serial_mutex.json') as mutex,safe(RECOVERY/'safe'),git_io(RECOVERY/'file_backed_git'):
    mutex.acquire();identity=read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json');assert not owned(identity)
    sync=h.sync;assert sync.git('rev-parse','HEAD')=='e910d03f8b8ae11ca418094e8f1399440a51aa89';h.verify_main('363b04accad09d792a53de06f0a3cde3dba11146');assert not sync.git('status','--porcelain')
    for name,raw in new.items():assert not sync.SECRET.search(raw);sync.atomic(sync.WORKTREE/name,raw)
    sync.git('add','-f','--',*sorted(new));assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(new)
    sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','核验文档原始字节：状态JSON采用仓库LF换行并保留恢复记录',timeout=180)
    commit=sync.git('rev-parse','HEAD');expected={**snapshot['document_sha256'],**{name:hashlib.sha256(raw).hexdigest() for name,raw in new.items()},str(prefix/'publish_project_documentation138_main_v1_20261011.py').replace('\\','/'):sha(A/'publish_project_documentation138_main_v1_20261011.py')}
    assert h.blob_hashes(commit,expected)==expected
    sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
    for name,digest in snapshot['document_sha256'].items():assert sha(ROOT/name)==digest
    receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'documents':names,'raw_git_blobs_verified':len(expected),'GitHub_About_description_read_back_verified':True,'original_line_ending_hash_failure_reconciled_without_content_changes':True,'optimization_goal_remains_paused':True,'new_training':0,'new_scoring':0,'new_inference':0,'at_local':now.isoformat(),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main'}
    create(RECOVERY/'receipt.json',receipt);create(A/'Actual_project_documentation138_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
