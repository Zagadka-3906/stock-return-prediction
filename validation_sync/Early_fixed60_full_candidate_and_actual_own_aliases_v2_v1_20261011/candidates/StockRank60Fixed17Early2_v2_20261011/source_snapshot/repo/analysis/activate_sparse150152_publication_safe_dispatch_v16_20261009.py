from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended,stack
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
import sparse150152_publication_safe_receivers_v16_20261009 as current
rows={}
for number,oldname in ((150,'HuberSparse150_complete_chronological_dispatch_v3_20261009'),(151,'RFFSparse151_complete_chronological_dispatch_v2_20261009')):
 old=read(A/'service_owned_workflows_20261006'/oldname/'native_launch.json');assert owned(old)
 dump=stack(old['owned_worker_pid']);line=next(line for line in dump.splitlines() if 'closed (' in line)
 parent,worker,idle=suspended_idle(old,line)
 try:
  name=current.CONFIG[number][2][-1];driver=current.MAP[number][name]
  row=start(('HuberSparse150' if number==150 else 'RFFSparse151')+'_complete_chronological_dispatch_publication_v16_20261009',driver,[],{str(current.META):sha(current.META),str(A/driver):sha(A/driver)})
  assert owned(row);create(A/f'actual_sparse{number}_publication_safe_handoff_v16_20261009.json',{'old_identity':old,'old_idle_boundary':idle,'new_identity':row,'scientific_workers_stopped_or_restarted':0})
  retire_suspended(old,row);rows[str(number)]=row
 except BaseException:
  if parent.is_running():parent.resume()
  if worker.is_running():worker.resume()
  raise
name=current.CONFIG[152][2][-1];driver=current.MAP[152][name]
rows['152_prospective']=start('SparseAfter148152_complete_prospective_controls_v1_20261009','verify_SparseAfter148152_existing_prospective_proof_v3_20261009.py',[],{})
rows['152_duplicate']=start('SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009','verify_SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009.py',[],{})
rows['152_dispatch']=start('SparseAfter148152_complete_chronological_dispatch_publication_v16_20261009',driver,[],{str(current.META):sha(current.META),str(A/driver):sha(A/driver)})
create(A/'actual_sparse150152_publication_safe_hidden_launches_v16_20261009.json',rows)
print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
