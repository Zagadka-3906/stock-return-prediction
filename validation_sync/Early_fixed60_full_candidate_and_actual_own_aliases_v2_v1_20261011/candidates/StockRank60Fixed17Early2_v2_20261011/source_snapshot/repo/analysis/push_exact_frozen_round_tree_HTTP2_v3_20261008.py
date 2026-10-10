"""Publish the original exact immutable full-QA Git tree using verified working HTTP2 proxy transport."""
from pathlib import Path
import argparse,subprocess,sys,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main(number):
    out=Path(f'E:/赛题五_本机临时/round{number}_connected_API_main_v1_20261008');b=read(out/'bundle.json');folder=out/'actual_verified_HTTP2_Git_push_v3';folder.mkdir(exist_ok=False)
    env=dict(__import__('os').environ);env['GIT_TERMINAL_PROMPT']='0';env['GCM_INTERACTIVE']='Never'
    calls=[]
    def git(*args,data=None,timeout=180):
        i=len(calls);stdout=folder/f'git{i:02d}.stdout';stderr=folder/f'git{i:02d}.stderr'
        with stdout.open('wb') as o,stderr.open('wb') as e:
            p=subprocess.Popen(['git',*args],cwd=b['local_worktree'],env=env,stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,stdout=o,stderr=e,creationflags=subprocess.CREATE_NO_WINDOW,close_fds=True)
            if data is not None:p.stdin.write(data);p.stdin.close()
            try:code=p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:p.kill();p.wait(timeout=10);code=-1
        calls.append({'arguments':list(args),'exit_code':code,'stdout':str(stdout),'stderr':str(stderr)});create(folder/f'git{i:02d}.json',calls[-1]);return code,stdout.read_text(encoding='utf8').strip(),stderr.read_text(encoding='utf8',errors='replace')
    code,head,error=git('rev-parse','HEAD');assert code==0 and head==b['parent_commit']
    code,tree,error=git('write-tree');assert code==0 and tree==b['expected_exact_tree_sha']
    code,commit,error=git('commit-tree',tree,'-p',head,data=(b['message']+'\n').encode('utf8'));assert code==0,error
    create(out/'actual_local_prepared_HTTP2_push_commit_v3.json',{'commit':commit,'parent':head,'tree':tree,'bundle_sha256':sha(out/'bundle.json'),'source_sha256':sha(Path(__file__)),'transport':'actual_Git_push_verified_TLS_HTTP2_existing_proxy_and_connected_API_ref_commit_verification'})
    for attempt in range(3):
        code,message,error=git('-c','http.proxy=http://127.0.0.1:7897','-c','http.sslBackend=openssl','-c','http.version=HTTP/2','push','origin',commit+':refs/heads/main',timeout=300)
        print(json.dumps({'round':number,'attempt':attempt+1,'exit_code':code,'commit':commit}),flush=True)
        if code==0:
            create(folder/'verification.json',{'status':'actual_exact_frozen_tree_push_succeeded_connected_API_remote_verification_still_required','commit':commit,'tree':tree,'only_branch':'main','force':False,'TLS_verification_not_disabled':True,'interactive_auth_disabled':True,'calls':calls});return
        if not any(t in error.lower() for t in ('tls','ssl','connection','timed out','unable to access')):raise RuntimeError(error[-1500:])
        time.sleep(2)
    create(folder/'failure.json',{'status':'failed_preserved_three_verified_HTTP2_transport_attempts','commit':commit,'calls':calls});raise RuntimeError('Three verified HTTP2 attempts failed; actual native/QAs/tree remain frozen.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--round',type=int,choices=(135,144),required=True);main(p.parse_args().round)
