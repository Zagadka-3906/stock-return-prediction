"""Push the already frozen exact full135 tree via the existing local proxy; do not change any local checkout or branch."""
from pathlib import Path
import sys,subprocess,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    out=Path('E:/赛题五_本机临时/round135_connected_API_main_v1_20261008');b=read(out/'bundle.json');work=Path(b['local_worktree'])
    proofdir=out/'actual_proxy_Git_push_v1';proofdir.mkdir(exist_ok=False)
    def git(*args,data=None,timeout=180):
        i=len(list(proofdir.glob('*.stdout')));stdout=proofdir/f'git{i:02d}.stdout';stderr=proofdir/f'git{i:02d}.stderr'
        with stdout.open('wb') as o,stderr.open('wb') as e:
            p=subprocess.Popen(['git',*args],cwd=work,stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,stdout=o,stderr=e,creationflags=subprocess.CREATE_NO_WINDOW,close_fds=True)
            if data is not None:p.stdin.write(data);p.stdin.close()
            try:code=p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:p.kill();p.wait(timeout=10);raise
        result=stdout.read_text(encoding='utf8').strip();error=stderr.read_text(encoding='utf8',errors='replace');create(proofdir/f'git{i:02d}.json',{'args':list(args),'exit_code':code,'stdout':str(stdout),'stderr':str(stderr),'TLS_verification_unchanged':True,'hidden_console':True})
        assert code==0,(args[0],error[-2000:]);return result
    assert git('rev-parse','HEAD')==b['parent_commit'];assert git('write-tree')==b['expected_exact_tree_sha']
    commit=git('commit-tree',b['expected_exact_tree_sha'],'-p',b['parent_commit'],data=(b['message']+'\n').encode('utf8'))
    create(out/'actual_local_prepared_push_commit.json',{'commit':commit,'parent':b['parent_commit'],'tree':b['expected_exact_tree_sha'],'bundle_sha256':sha(out/'bundle.json'),'transport':'local_git_exact_tree_push_via_existing_proxy_then_connected_API_ref_and_commit_verification','source_sha256':sha(Path(__file__))})
    git('-c','http.proxy=http://127.0.0.1:7897','-c','http.sslBackend=openssl','-c','http.version=HTTP/1.1','push','origin',commit+':refs/heads/main',timeout=600)
    create(proofdir/'push_execution.json',{'status':'local_git_push_returned_success_connected_API_remote_commit_verification_still_required','commit':commit,'tree':b['expected_exact_tree_sha'],'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'only_remote_branch':'main','force_push':False,'local_HEAD_not_changed':git('rev-parse','HEAD')==b['parent_commit']})
    print(json.dumps({'pushed_commit':commit,'remote_API_verification_still_required':True}),flush=True)
if __name__=='__main__':main()
