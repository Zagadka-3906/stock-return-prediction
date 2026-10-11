"""Repair shared-main index drift only when the entire index is a published ancestor tree."""
from pathlib import Path
from datetime import datetime
import os,subprocess,shutil,uuid
A=Path(__file__).resolve().parent;ROOT=A.parent
import verified_current_main_source_index_guard_v68_20261011 as original

def audit(index=None):
 from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
 from run_dependency_queue_v3_20261006 import read,sha,create
 index=Path(index or ROOT/'.git/index')
 if index.resolve()!=(ROOT/'.git/index').resolve():return original.audit(index)
 assert allowed()
 from serial_main_publication_mutex_v1_20261009 import MainPublicationMutex
 mutex=MainPublicationMutex();mutex.acquire();held=[]
 env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
 def git(*args,custom_env=None,data=None):
  p=subprocess.run(['git',*args],cwd=ROOT,env=custom_env or env,input=data,capture_output=True,creationflags=0x08000000)
  assert p.returncode==0,(args,p.returncode,p.stderr.decode('utf8','replace'));return p.stdout
 try:
  head=git('rev-parse','HEAD').decode().strip();assert git('branch','--show-current').strip()==b'main'
  delta=git('-c','core.quotepath=false','diff','--cached','--name-status','HEAD').decode('utf8').splitlines()
  if not delta:return original.audit(index)
  out=Path('E:/赛题五_本机临时/已发布祖先索引安全同步83_20261011')/uuid.uuid4().hex;out.mkdir(parents=True)
  before=sha(index);private=out/'original_source.index';shutil.copyfile(index,private);assert sha(private)==sha(index)==before
  privateenv=dict(env,GIT_INDEX_FILE=str(private));tree=git('write-tree',custom_env=privateenv).decode().strip()
  ancestors=[line.split('\t') for line in git('log','-n','250','--format=%H%x09%T',head).decode().splitlines()]
  matches=[commit for commit,oid in ancestors if oid==tree]
  assert matches,('Refusing staged user changes: index is not an exact published main ancestor tree',tree,head)
  ancestor=matches[0];git('merge-base','--is-ancestor',ancestor,head)
  # Hold only the existing idle publisher; science is neither suspended nor restarted.
  from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold
  p,w,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)');held=[p,w]
  assert sha(index)==before and git('rev-parse','HEAD').decode().strip()==head
  remote=git('-c','http.proxy=http://127.0.0.1:7897','-c','http.version=HTTP/1.1','ls-remote','origin','refs/heads/main').decode().split()[0];assert remote==head
  existing={}
  for line in delta:
   name=line.split('\t')[-1];path=ROOT/name
   if not name.startswith('validation_sync/') and path.is_file():existing[name]=sha(path)
  create(out/'frozen_before_metadata_alignment.json',{'status':'exact_index_tree_equals_verified_remote_main_ancestor_no_user_staged_change','at_local':datetime.now().isoformat(),'main_commit':head,'ancestor_commit':ancestor,'index_tree':tree,'original_index_sha256':before,'delta_count':len(delta),'existing_working_source_sha256':existing,'actual_idle_hold':idle})
  assert allowed();git('read-tree','--reset',head)
  files=[name for name in git('ls-files','-z').split(b'\0') if name]
  missing=[name for name in files if not (ROOT/name.decode('utf8')).exists()]
  if missing:git('update-index','--skip-worktree','-z','--stdin',data=b'\0'.join(missing)+b'\0')
  assert git('rev-parse','HEAD').decode().strip()==head
  for name,digest in existing.items():assert sha(ROOT/name)==digest,name
  proof=original.audit(index)
  create(out/'verification.json',{'status':'passed_exact_ancestor_only_metadata_sync_current_main_and_source_files_unchanged','original_index_sha256':before,'current_index_sha256':sha(index),'main_commit':head,'ancestor_commit':ancestor,'missing_archive_skip_worktree':len(missing),'working_source_files_rehashed':len(existing),'scientific_workers_not_changed':True})
  return {**proof,'actual_ancestor_only_metadata_recovery':str(out/'verification.json')}
 finally:
  for p in reversed(held):
   if p.is_running():p.resume()
  mutex.close()
