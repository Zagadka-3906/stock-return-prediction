"""Use the actual sync.git cwd contract and a fresh owned idle hold; preserve V2 failure."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'finish_API_main_exact_tree_with_file_IO_v2_20261007.py';new=A/'finish_API_main_exact_tree_with_file_IO_v3_20261007.py'
    text=old.read_text(encoding='utf8').replace('def git(*args,timeout=30):','def git(*args,cwd=None,timeout=30):').replace('cwd=helpers.sync.WORKTREE,stdin=','cwd=cwd or helpers.sync.WORKTREE,stdin=')
    text=text.replace('from handoff_ready_goss_full_execution_20261006 import pair','from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle')
    text=text.replace("row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json');parent,worker=pair(row)\n        assert parent.status()==psutil.STATUS_STOPPED and worker.status()==psutil.STATUS_STOPPED", "row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')\n        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)')")
    text=text.replace('file_IO_git','file_IO_v3_git').replace('actual_file_IO_Git_calls_v2.json','actual_file_IO_Git_calls_v3.json').replace('actual_file_backed_IO_recovery_v2','actual_file_backed_IO_recovery_v3')
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    row=start('main_publication_API_tree_recovery_lease_v3',new.name,[],{str(old):sha(old),str(new):sha(new),str(Path(__file__)):sha(Path(__file__))})
    create(A/'sparse_main_API_transport_recovery_20261007/actual_file_IO_contract_v3_hidden_launch.json',{'identity':row,'original_V2_cwd_contract_failure_retained':True,'new_quality_scores':0})

if __name__=='__main__':main()
