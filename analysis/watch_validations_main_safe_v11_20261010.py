"""Keep the original idle monitor with serialized publications and exact research-index preservation."""
from pathlib import Path
import sys,os,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
def main():
    ready=A/'main_watcher_safe_handoff_and_index_restore_v34_20261009.json'
    while not ready.exists():time.sleep(1)
    assert read(ready)['status']=='passed_exact_preexisting_index_restored_and_owned_idle_watcher_replaced'
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    import verified_round_main_publication_20261006 as publisher
    import watch_validations_main_v7_20261006 as original
    from serial_main_publication_mutex_v1_20261009 import MainPublicationMutex
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    before=publisher.publish;counter=0
    def guarded(sync,number):
        nonlocal counter
        counter+=1;folder=Path('E:/赛题五_本机临时/main_watcher_safe_v11_20261010')/f'round{number}_attempt{counter}'
        # Acquiring the mutex before taking the index snapshot prevents another
        # completed publisher from invalidating that snapshot during a lock wait.
        mutex=MainPublicationMutex();mutex.acquire()
        try:
            with safe(folder/'safe_publication'),git_io(folder/'file_backed_git'):
                return before(sync,number)
        finally:
            mutex.close()
            from run_dependency_queue_v3_20261006 import create
            create(folder/'serial_publication_mutex.json',{'events':mutex.events,'research_index_snapshot_after_lock':True})
    publisher.publish=guarded
    try:original.main()
    finally:publisher.publish=before
if __name__=='__main__':main()
