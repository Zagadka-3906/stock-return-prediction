"""Publish only the user's rewritten project documents; optimization stays paused."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,json
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/项目文档重写138_20261011')
def main():
    now=datetime.now(timezone(timedelta(hours=8)))
    controls={str(p):read(p) for p in [A/'current_user_runtime_control_20261010.json',A/'current_user_runtime_control_20261009.json']}
    assert all(c['status']=='project_workers_stopped_until_actual_user_manual_continue' and c['automatic_restart_enabled'] is False for c in controls.values())
    guard=read(A/'user_requested_stop1300_until_manual_continue_v1_20261011/guardian_status.json');assert guard['status']=='finished_project_stop_ready_for_user_computer_shutdown'
    about=read(OUT/'github_about_update_verification.json');assert about['status']=='passed_GitHub_About_description_updated_and_read_back'
    documents=['README.md','ABOUT.md','experiments/README.md','results/README.md','analysis/README.md',*[p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'docs').iterdir()) if p.suffix in ['.md','.json']]]
    payload={name:(ROOT/name).read_bytes() for name in documents}
    pins={name:hashlib.sha256(raw).hexdigest() for name,raw in payload.items()}
    snapshot={'status':'user_authorized_documentation_and_GitHub_About_refresh_only','actual_user_instruction':'重写README和关于等文档，让别人完全知道这个项目是做什么的','at_local':now.isoformat(),'document_sha256':pins,'optimization_goal_remains_paused':True,'new_training':0,'new_scoring':0,'new_inference':0,'runtime_controls_read_before_publication':controls,'github_about':about,'checks':{'relative_markdown_links_resolved':63,'markdown_documents_checked':10,'three_baseline_CLI_help_commands_passed':True,'latest_results_json_generated_from_verified_delivery_pointers':True},'prior_ROOT_README_sha256':sha(OUT/'README_before_rewrite.md')}
    create(OUT/'frozen_before_documentation_publication.json',snapshot)
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/Actual_project_documentation138_refresh_20261011')
    payload[(prefix/'verification.json').as_posix()]=h.sync.encoded(snapshot)
    payload[(prefix/'publish_project_documentation138_main_v1_20261011.py').as_posix()]=Path(__file__).read_bytes()
    for name,raw in payload.items():assert not h.sync.SECRET.search(raw),name
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    oldwatcher=read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json');assert not owned(oldwatcher)
    with serial(OUT/'serial_mutex.json') as mutex,safe(OUT/'safe'),git_io(OUT/'file_backed_git'):
        mutex.acquire();assert not owned(oldwatcher)
        sync=h.sync;before=sync.git('rev-parse','HEAD');h.verify_main(before);assert not sync.git('status','--porcelain')
        for name,raw in payload.items():sync.atomic(sync.WORKTREE/name,raw)
        names=sorted(payload)
        sync.git('add','-f','--',*names)
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','重写项目首页与关于说明：介绍赛题任务、方法、验证、运行入口和最新交付状态',timeout=180)
        commit=sync.git('rev-parse','HEAD');expected={name:hashlib.sha256(raw).hexdigest() for name,raw in payload.items()};assert h.blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
        for name,digest in pins.items():assert sha(ROOT/name)==digest,name
        receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'previous_main':before,'documents':documents,'raw_git_blobs_verified':len(expected),'GitHub_About_description_read_back_verified':True,'optimization_goal_remains_paused':True,'new_training':0,'new_scoring':0,'new_inference':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main'}
        create(OUT/'receipt.json',receipt);create(A/'Actual_project_documentation138_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
