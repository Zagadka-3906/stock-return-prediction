from pathlib import Path
import os,subprocess,time,json
A=Path(__file__).resolve().parent;ROOT=A.parent

def audit(index=None):
 from run_dependency_queue_v3_20261006 import sha
 from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
 assert allowed();index=Path(index or ROOT/'.git/index');env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_INDEX_FILE=str(index))
 def git(*args):
  r=subprocess.run(['git',*args],cwd=ROOT,env=env,capture_output=True,creationflags=0x08000000);return r
 for _ in range(10):
  before=sha(index);head=git('rev-parse','HEAD');branch=git('branch','--show-current');staged=git('diff','--cached','--quiet','HEAD','--');after=sha(index);head_after=git('rev-parse','HEAD')
  assert head.returncode==branch.returncode==head_after.returncode==0
  if before!=after or head.stdout!=head_after.stdout:time.sleep(.2);continue
  assert branch.stdout.strip()==b'main'
  assert staged.returncode==0,('Unexpected staged delta against current authorized main',staged.returncode,staged.stderr.decode('utf8','replace'))
  return {'status':'passed_current_authorized_main_source_index_tree_equal_HEAD_no_staged_changes','index_sha256':before,'main_commit':head.stdout.decode().strip(),'index_path':str(index),'read_only_Git_optional_locks_disabled':True}
 raise AssertionError('Source index changed during all bounded read-only observations')
