from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
 import publish_classifier_consensus_workflows_20261006 as h
 assert not h.sync.git('status','--porcelain')
 old=A/'recover_round148_chunked_main_publication_v1_20261009.py';s=old.read_text(encoding='utf8')
 s=s.replace('round148_chunked_main_recovery_v1_20261009','round148_chunked_main_recovery_v2_20261009')
 s=s.replace('AdaptiveJointCrossHuber242_round148_full_registration_v3_20261009','AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009')
 needle="added[str(Path(large).parent/'reconstruct_full_report.py')]";assert s.count(needle)==1
 s=s.replace(needle,"added[(Path(large).parent/'reconstruct_full_report.py').as_posix()]")
 p=A/'recover_round148_chunked_main_publication_v2_20261009.py';compile(s,str(p),'exec')
 with p.open('x',encoding='utf8') as f:f.write(s)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 failure=A/'service_owned_workflows_20261006/AdaptiveJointCrossHuber242_round148_full_registration_v3_20261009/service_execution.json'
 row=start('AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009',p.name,[],
  {str(q):sha(q) for q in [Path(__file__),old,p,failure]})
 create(A/'round148_chunked_main_recovery_hidden_launch_v2_20261009.json',row)
 print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
