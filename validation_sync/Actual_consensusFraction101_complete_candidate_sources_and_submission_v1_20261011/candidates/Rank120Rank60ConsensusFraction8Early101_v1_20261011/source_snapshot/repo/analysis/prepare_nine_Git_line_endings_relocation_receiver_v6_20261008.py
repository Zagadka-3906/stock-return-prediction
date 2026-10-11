"""Preserve native Git porcelain leading spaces, retaining the unused first attempt."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
def main():
    failure=A/'service_owned_workflows_20261006/Git_publisher_exact_nine_line_endings_and_E_relocation_v5_20261008/service_execution.json'
    assert read(failure)['status']=='failed'
    old=A/'reconcile_nine_Git_worktree_line_endings_and_relocate_v5_20261008.py';text=old.read_text(encoding='utf-8-sig')
    before="return git_bytes(path, *args).decode('utf-8').strip()";assert text.count(before)==1
    text=text.replace(before,"return git_bytes(path, *args).decode('utf-8').rstrip('\\r\\n')")
    text=text.replace('v5_20261008','v6_20261008')
    target=A/'reconcile_nine_Git_worktree_line_endings_and_relocate_v6_20261008.py';compile(text,str(target),'exec')
    with target.open('x',encoding='utf-8',newline='') as stream:stream.write(text)
    pins={str(p):sha(p) for p in [Path(__file__),old,target,failure]}
    row=start('Git_publisher_exact_nine_line_endings_and_E_relocation_v6_20261008',target.name,[],pins)
    create(A/'Git_publisher_line_endings_E_relocation_v6_hidden_launch_20261008.json',{'identity':row,'input_sha256':pins,'old_v5_failure_preserved':True,'no_original_D_file_modified_before_v5_failure':True,'new_quality_scores':0})
    print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
