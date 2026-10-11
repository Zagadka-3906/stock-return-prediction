"""Bounded adaptive verified-TLS transport retries; reuse the already frozen exact Git commit."""
from pathlib import Path
import subprocess,sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,create
def main():
    out=Path('E:/赛题五_本机临时/round135_connected_API_main_v1_20261008');info=read(out/'actual_local_prepared_push_commit.json');b=read(out/'bundle.json');folder=out/'adaptive_verified_TLS_push_v2';folder.mkdir(exist_ok=False);attempts=[]
    variants=[('openssl','HTTP/2'),('schannel','HTTP/1.1'),('openssl','HTTP/1.1'),('openssl','HTTP/2')]
    for i,(backend,version) in enumerate(variants):
        args=['git','-c','http.proxy=http://127.0.0.1:7897','-c','http.sslBackend='+backend,'-c','http.version='+version,'push','origin',info['commit']+':refs/heads/main']
        with (folder/f'push{i}.stdout').open('wb') as o,(folder/f'push{i}.stderr').open('wb') as e:
            p=subprocess.Popen(args,cwd=b['local_worktree'],stdin=subprocess.DEVNULL,stdout=o,stderr=e,creationflags=subprocess.CREATE_NO_WINDOW,close_fds=True)
            try:code=p.wait(timeout=240)
            except subprocess.TimeoutExpired:p.kill();p.wait(timeout=10);code=-1
        attempts.append({'arguments':args,'exit_code':code,'stdout':str(folder/f'push{i}.stdout'),'stderr':str(folder/f'push{i}.stderr')})
        create(folder/f'push{i}.json',attempts[-1]);print(json.dumps({'attempt':i+1,'backend':backend,'version':version,'exit_code':code}),flush=True)
        if code==0:
            create(folder/'verification.json',{'status':'actual_Git_push_succeeded_remote_API_commit_verification_still_required','commit':info['commit'],'tree':info['tree'],'attempts':attempts,'TLS_verification_not_disabled':True,'only_remote_branch':'main'});return
        time.sleep(2)
    create(folder/'verification.json',{'status':'all_four_verified_TLS_variants_failed_large_archive_API_limit_requires_chunked_transport','attempts':attempts,'original_frozen_commit_preserved':True})
    raise RuntimeError('Four distinct bounded verified TLS attempts failed; preserve exact source/data and use smaller archive transport.')
if __name__=='__main__':main()
