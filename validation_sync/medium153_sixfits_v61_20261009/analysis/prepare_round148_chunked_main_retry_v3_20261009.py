"""Retry only verified partial publication artifacts, with Git POSIX paths."""
from pathlib import Path
import sys,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,read,create
def verify_partial(work):
 import publish_classifier_consensus_workflows_20261006 as h
 prefix='validation_sync/round148/complete_ranking_display/lossless_ranking_display_v2_20261006/round148/'
 descriptor=read(work/(prefix+'full_report_reconstructed_for_publication.json.gz.parts.json'))
 expected={prefix+r['path'] for r in descriptor['parts']}|{prefix+'full_report_reconstructed_for_publication.json.gz.parts.json',prefix+'reconstruct_full_report.py'}
 status=h.sync.git('status','--porcelain').splitlines()
 assert {l[3:] for l in status}==expected and all(l.startswith('?? ') for l in status)
 digest=hashlib.sha256()
 for r in descriptor['parts']:
  p=work/prefix/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'];digest.update(p.read_bytes())
 assert digest.hexdigest()==descriptor['compressed_sha256']
 assert sha(A/'lossless_ranking_display_v2_20261006/round148/full_report_reconstructed_for_publication.json.gz')==descriptor['compressed_sha256']
def main():
 import publish_classifier_consensus_workflows_20261006 as h
 verify_partial(h.sync.WORKTREE)
 old=A/'recover_round148_chunked_main_publication_v1_20261009.py';s=old.read_text(encoding='utf8')
 s=s.replace('round148_chunked_main_recovery_v1_20261009','round148_chunked_main_recovery_v2_20261009')
 s=s.replace('AdaptiveJointCrossHuber242_round148_full_registration_v3_20261009','AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009')
 needle="added[str(Path(large).parent/'reconstruct_full_report.py')]";assert s.count(needle)==1
 s=s.replace(needle,"added[(Path(large).parent/'reconstruct_full_report.py').as_posix()]")
 needle="  assert not value('status','--porcelain')";assert s.count(needle)==2
 s=s.replace(needle,"  from prepare_round148_chunked_main_retry_v3_20261009 import verify_partial\n  verify_partial(work)",1)
 p=A/'recover_round148_chunked_main_publication_v2_20261009.py';compile(s,str(p),'exec')
 with p.open('x',encoding='utf8') as f:f.write(s)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 failure=A/'service_owned_workflows_20261006/AdaptiveJointCrossHuber242_round148_full_registration_v3_20261009/service_execution.json'
 row=start('AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009',p.name,[],{str(q):sha(q) for q in [Path(__file__),old,p,failure]})
 create(A/'round148_chunked_main_recovery_hidden_launch_v2_20261009.json',row)
 print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
