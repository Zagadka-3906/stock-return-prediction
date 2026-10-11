"""Delete only audited redundant Git exports, retain scientific data, and publish main."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,json,gzip,hashlib,subprocess,shutil,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/仓库清理140_20261011')
def git_blob(path):
    size=path.stat().st_size;digest=hashlib.sha1(b'blob '+str(size).encode()+b'\0')
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(4*1024**2),b''):digest.update(block)
    return digest.hexdigest()
def main():
    controls=[read(A/f'current_user_runtime_control_202610{d}.json') for d in ('10','09')];now=datetime.now(timezone(timedelta(hours=8)))
    assert all(c['status']=='project_workers_stopped_until_actual_user_manual_continue' and c['automatic_restart_enabled'] is False for c in controls)
    plan=read(OUT/'plan_verification.json');assert sha(OUT/'deletion_plan.jsonl.gz')==plan['plan_sha256']
    with gzip.open(OUT/'deletion_plan.jsonl.gz','rt',encoding='utf8') as f:rows=[json.loads(line) for line in f]
    before=read(OUT/'tracked_inventory.json');tree={p:(oid,size) for p,oid,size in before['files']};deleted={r['removed_path'] for r in rows}
    assert len(deleted)==plan['planned_deletions'] and all(tree[r['removed_path']]==(r['git_blob_oid'],r['bytes']) for r in rows)
    import publish_classifier_consensus_workflows_20261006 as h
    sync=h.sync;workspace=sync.WORKTREE.resolve();oldwatcher=read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json');assert not owned(oldwatcher)
    candidate_pointer=A/'alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json';delivery=read(candidate_pointer);candidate=Path(delivery['source_candidate']);native=read(candidate/'verification.json')
    bundle=read(A/'actual_fraction101_delivery_bundle137_verification_v1_20261011.json')
    pins={str(candidate_pointer):sha(candidate_pointer),str(candidate/'manifest.json'):sha(candidate/'manifest.json'),str(Path(delivery['output'])/'submission.csv'):delivery['csv_sha256'],str(Path(bundle['archive'])):bundle['archive_sha256']}
    pins.update({m['path']:m['sha256'] for m in native['models'].values()});assert len(native['models'])==37
    for path,digest in pins.items():assert sha(path)==digest,path
    for name in ['verification.json','full_report_publication_snapshot_verification.json']:
        p=sync.WORKTREE/'validation_sync/round191/complete_ranking_display/lossless_ranking_display_v2_20261006/round191'/name;proof=read(p);assert proof['connected_records']==17753 and proof['status'].startswith('passed')
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    with serial(OUT/'serial_mutex.json') as mutex,safe(OUT/'safe'),git_io(OUT/'file_backed_git'):
        mutex.acquire();assert not owned(oldwatcher);h.verify_main(plan['previous_main']);assert sync.git('rev-parse','HEAD')==plan['previous_main'] and not sync.git('status','--porcelain')
        # Resolve every deletion target inside the named Git worktree before deleting.
        canonical={r['retained_path']:r['git_blob_oid'] for r in rows if 'retained_path' in r}
        for name,oid in canonical.items():
            path=sync.WORKTREE/name;assert path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(workspace) and git_blob(path)==oid,name
        for i,row in enumerate(rows,1):
            path=sync.WORKTREE/row['removed_path'];assert path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(workspace) and git_blob(path)==row['git_blob_oid'],row['removed_path']
            if i%20000==0:print({'phase':'preflight_file_bytes_and_workspace_boundary','checked':i,'total':len(rows)},flush=True)
        create(OUT/'actual_pre_deletion_scope.json',{'status':'passed_all_deletion_targets_raw_Git_blob_bytes_and_resolved_workspace_boundaries_checked','actual_user_instruction':'整理仓库文件，删除不需要的文件','at_local':now.isoformat(),'selected_native_and_submission_SHA256':pins,'canonical_objects_checked':len(canonical),'predeclared_deletions':len(rows),'new_training':0,'new_scoring':0,'new_inference':0})
        free_before=shutil.disk_usage('E:/').free
        progress=OUT/'deletion_progress.jsonl'
        with progress.open('x',encoding='utf8') as log:
            for i,row in enumerate(rows,1):
                path=sync.WORKTREE/row['removed_path'];assert path.resolve().is_relative_to(workspace) and path.stat().st_size==row['bytes'];path.unlink()
                if i%10000==0 or i==len(rows):
                    state={'deleted':i,'total':len(rows),'at_local':datetime.now().isoformat()};log.write(json.dumps(state)+'\n');log.flush();print(state,flush=True)
        for name,oid in canonical.items():assert git_blob(sync.WORKTREE/name)==oid,name
        free_after=shutil.disk_usage('E:/').free
        # Local interpreter caches are derivatives, never candidate/source-freeze data.
        caches=[]
        for base in [ROOT/'__pycache__',ROOT/'src',ROOT/'tests',ROOT/'experiments',A]:
            if not base.exists():continue
            for folder,dirs,names in os.walk(base,followlinks=False):
                dirs[:]=[n for n in dirs if not (Path(folder)/n).is_symlink() and not (Path(folder)/n).is_junction() and n not in ['source_snapshot','repo','pre_inference_source_freeze_v1','candidates','service_owned_workflows_20261006']]
                if Path(folder).name!='__pycache__':continue
                for name in names:
                    path=Path(folder)/name
                    if path.suffix in ['.pyc','.pyo'] and not path.is_symlink() and path.resolve().is_relative_to(ROOT.resolve()):caches.append((path,path.stat().st_size))
        create(OUT/'local_cache_plan.json',{'status':'only_regenerable_python_bytecode_under_verified_ROOT_source_directories','files':[{'path':str(p),'bytes':s} for p,s in caches]})
        for path,size in caches:assert path.resolve().is_relative_to(ROOT.resolve()) and path.stat().st_size==size;path.unlink()
        for path,digest in pins.items():assert sha(path)==digest,path
        summary={'status':'passed_predeclared_redundant_exports_and_generated_views_removed_protected_candidate_scores_and_control_records_retained','previous_main':plan['previous_main'],'tracked_files_before':len(tree),'removed_tracked_files':len(rows),'removed_logical_bytes':sum(r['bytes'] for r in rows),'duplicate_export_files':plan['duplicate_export_files'],'obsolete_generated_display_files':plan['generated_display_files'],'current_original_files_retained':len(tree)-len(rows),'physical_E_free_before':free_before,'physical_E_free_after_archive_deletion':free_after,'physical_E_bytes_released_at_deletion':free_after-free_before,'local_bytecode_files_deleted':len(caches),'local_bytecode_logical_bytes_deleted':sum(s for p,s in caches),'all37_native_models_CSV_ZIP_hashes_unchanged':True,'formal191_records_retained':17753,'current_score_catalog_records_retained':18959,'Git_history_rewritten':False,'optimization_goal_remains_paused':True,'new_training':0,'new_scoring':0,'new_inference':0,'archive_index_sha256':sha(OUT/'deletion_plan.jsonl.gz')}
        catalog=ROOT/'validation_sync/archive_index_20261011.jsonl.gz';shutil.copyfile(OUT/'deletion_plan.jsonl.gz',catalog);assert sha(catalog)==summary['archive_index_sha256']
        (ROOT/'validation_sync/cleanup140_summary.json').write_bytes(sync.encoded(summary));create(OUT/'cleanup_verification.json',summary)
        payload_names=['.gitignore','docs/README.md','docs/REPOSITORY_GUIDE.md','docs/REPOSITORY_CLEANUP.md','tools/find_archive_record.py','validation_sync/README.md','validation_sync/archive_index_20261011.jsonl.gz','validation_sync/cleanup140_summary.json']
        payload={name:(ROOT/name).read_bytes() for name in payload_names}
        for p in [Path(__file__),A/'prepare_repository_cleanup140_plan_v1_20261011.py',OUT/'plan_verification.json',OUT/'actual_pre_deletion_scope.json']:
            raw=p.read_bytes();name='validation_sync/cleanup140_sources/'+p.name;payload[name]=raw
        for name,raw in payload.items():assert not sync.SECRET.search(raw) if not name.endswith('.gz') else True,name;sync.atomic(sync.WORKTREE/name,raw)
        subprocess.run(['git','update-index','--remove','-z','--stdin'],cwd=sync.WORKTREE,input=b'\0'.join(n.encode('utf8') for n in sorted(deleted))+b'\0',capture_output=True,check=True,timeout=600)
        sync.git('add','-f','--',*sorted(payload))
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged==deleted|set(payload),(len(staged),len(deleted|set(payload)))
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','整理验证归档：去除相同内容导出与旧累计展示，保留最新方案、唯一记录和历史查询索引',timeout=600)
        commit=sync.git('rev-parse','HEAD');raw=subprocess.check_output(['git','ls-tree','-r','-z',commit],cwd=sync.WORKTREE);aftertree={}
        for entry in raw.split(b'\0'):
            if entry:head,name=entry.split(b'\t',1);aftertree[name.decode('utf8')]=head.split()[2].decode()
        assert set(aftertree)==(set(tree)-deleted)|set(payload)
        for name,(oid,size) in tree.items():
            if name not in deleted and name not in payload:assert aftertree[name]==oid,name
        expected={name:hashlib.sha256(raw).hexdigest() for name,raw in payload.items()};assert h.blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=600);h.verify_main(commit);h.watcher.advance_source_index(commit)
        for path,digest in pins.items():assert sha(path)==digest,path
        assert not sync.git('status','--porcelain')
        receipt={'status':'pushed_and_remote_head_verified_all_retained_tree_blobs_unchanged','branch':'main','commit':commit,'tracked_files_after':len(aftertree),'removed_files':len(deleted),'logical_removed_bytes':summary['removed_logical_bytes'],'physical_E_bytes_released_at_deletion':summary['physical_E_bytes_released_at_deletion'],'current_candidate_CSV_ZIP_and_all37_models_unchanged':True,'all_original_retained_Git_blob_ids_checked':True,'Git_history_not_rewritten':True,'optimization_goal_remains_paused':True}
        create(OUT/'receipt.json',receipt);create(A/'Actual_repository_cleanup140_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
