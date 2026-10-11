from pathlib import Path
import sys,shutil,os,subprocess
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
import verified_ancestor_only_current_main_index_guard83_v1_20261011 as guard
assert allowed();root=A.parent;before=sha(root/'.git/index');positive=guard.audit()
out=Path('E:/赛题五_本机临时/祖先索引保护83实际正负检查_20261011');out.mkdir(exist_ok=False)
private=out/'deliberately_staged_negative.index';shutil.copyfile(root/'.git/index',private)
env=dict(os.environ,GIT_INDEX_FILE=str(private),GIT_OPTIONAL_LOCKS='0')
r=subprocess.run(['git','update-index','--force-remove','--','run.py'],cwd=root,env=env,capture_output=True,creationflags=0x08000000);assert r.returncode==0,r.stderr
try:guard.audit(private)
except AssertionError as error:negative={'actual_private_staged_change_rejected':True,'error':str(error)}
else:raise AssertionError('Private staged change accepted')
assert sha(root/'.git/index')==before==positive['index_sha256']
create(A/'actual_ancestor_index_guard83_positive_negative_v1_20261011.json',{'status':'passed_actual_current_main_positive_and_private_staged_negative_refused_root_index_unchanged','positive':positive,'negative':negative,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(guard.__file__)]},'root_index_unchanged':True,'working_files_changed':0})
print({'actual_positive_current_main_passed':True,'actual_private_staged_negative_rejected':True},flush=True)
