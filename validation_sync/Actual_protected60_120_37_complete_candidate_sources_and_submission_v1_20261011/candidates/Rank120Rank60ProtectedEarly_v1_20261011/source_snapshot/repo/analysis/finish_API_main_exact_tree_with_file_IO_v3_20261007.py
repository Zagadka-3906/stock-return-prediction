"""Finish exact API tree adoption using file-backed Git IO, no inherited-pipe waits."""
from pathlib import Path
import sys,time,subprocess,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,create
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers
OUT=A/'sparse_main_API_transport_recovery_20261007'

def main():
    import psutil
    original=helpers.sync.git;calls=[];held=[]
    def git(*args,cwd=None,timeout=30):
        index=len(calls);stdout=OUT/f'file_IO_v3_git{index:03d}.stdout';stderr=OUT/f'file_IO_v3_git{index:03d}.stderr'
        with stdout.open('wb') as output,stderr.open('wb') as errors:
            proc=subprocess.Popen(['git','-c','http.version=HTTP/1.1',*args],cwd=cwd or helpers.sync.WORKTREE,stdin=subprocess.DEVNULL,stdout=output,stderr=errors,close_fds=True,creationflags=subprocess.CREATE_NO_WINDOW)
            try:code=proc.wait(timeout=min(timeout,90))
            except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=10);raise
        calls.append({'args':list(args),'exit_code':code,'stdout':str(stdout),'stderr':str(stderr)})
        if code:raise RuntimeError('git '+args[0]+' failed: '+stderr.read_text(encoding='utf8',errors='replace')[:1200])
        return stdout.read_text(encoding='utf8',errors='strict').strip()
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker,parent));p=read(OUT/'frozen_exact_API_tree_payload.json');r=read(OUT/'actual_API_ref_update_and_release.json');commit=r['actual_API_main_commit']
        assert git('rev-parse','HEAD')==p['original_local_commit'] and not git('status','--porcelain')
        try:git('cat-file','-e',commit+'^{commit}')
        except RuntimeError:git('fetch','--no-tags','origin','main',timeout=90)
        assert git('show','-s','--format=%T',commit)==p['expected_tree_sha']==r['verified_tree_sha']
        helpers.sync.git=git
        helpers.verify_main(commit)
        git('reset','--soft',commit);assert not git('status','--porcelain')
        helpers.watcher.advance_source_index(commit)
        create(OUT/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
          'commit':commit,'branch':'main','exact_original_tree_sha':p['expected_tree_sha'],'all_file_bytes_preserved':True,
          'actual_file_backed_IO_recovery_v3':True,'original_unpublished_commit_retained_in_local_reflog':p['original_local_commit'],
          'API_main_update_used_expected_parent_lease_and_no_force':True,'new_quality_scores':0,'new_native_fits':0})
        print('PASS exact API tree and remote main adopted; worktree bytes unchanged',flush=True)
    finally:
        helpers.sync.git=original
        for proc in reversed(held):
            if proc.is_running():proc.resume()
        create(OUT/'actual_file_IO_Git_calls_v3.json',{'calls':calls,'no_stdout_pipe_capture':True})

if __name__=='__main__':main()
