"""One standard HTTPS full-pack transport attempt on the same validated local commit."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'close_actual_sparse_committed_main_after_server_error_v4_20261007.py';new=A/'close_actual_sparse_committed_main_full_pack_HTTP11_v5_20261007.py'
    text=old.read_text(encoding='utf8').replace('actual_sparse_and_isolated_scoring_controls_github_recovery_v4_20261007','actual_sparse_and_isolated_scoring_controls_github_recovery_v5_20261007')
    needle="sync.git('push','origin','HEAD:refs/heads/main',timeout=90)";assert text.count(needle)==1
    text=text.replace(needle,"sync.git('-c','http.version=HTTP/1.1','push','--no-thin','origin','HEAD:refs/heads/main',timeout=90)")
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [Path(__file__),old,new]}
    row=start('actual_sparse_committed_main_full_pack_transport_v5',new.name,[],pins)
    create(A/'actual_sparse_full_pack_HTTP11_hidden_launch_v5_20261007.json',{'status':'started_one_standard_HTTP11_full_pack_push_attempt_same_commit_without_TLS_bypass','identity':row,'input_sha256':pins,'new_quality_scores':0})

if __name__=='__main__':main()
