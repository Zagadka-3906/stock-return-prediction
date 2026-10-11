from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
old=A/'recover_round148_verified_commit_transport_v4_20261009.py';new=A/'reconcile_round148_remote_verified_v5_20261009.py'
s=old.read_text(encoding='utf8').replace('round148_verified_commit_transport_v4_20261009','round148_remote_verified_reconcile_v5_20261009')
s=s.replace('AdaptiveJointCrossHuber242_round148_full_registration_v6_20261009','AdaptiveJointCrossHuber242_round148_full_registration_v7_20261009')
needle="  git('update-ref','refs/heads/main',commit,rejected);git('read-tree',commit)"
assert s.count(needle)==1
s=s.replace(needle,"  assert value('rev-parse','refs/heads/main')==parent_commit\n  assert not git('symbolic-ref','-q','HEAD') if False else True\n  git('update-ref','refs/heads/main',commit,parent_commit)\n  git('update-ref','--no-deref','HEAD',commit,rejected);git('read-tree',commit)")
# Explicitly verify detached HEAD from the filesystem before updating it.
s=s.replace("  assert not git('symbolic-ref','-q','HEAD') if False else True","  head_path=Path(value('rev-parse','--git-path','HEAD'))\n  if not head_path.is_absolute():head_path=work/head_path\n  assert head_path.read_text(encoding='ascii').strip()==rejected")
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
pins={str(p):sha(p) for p in (old,new,Path(__file__))}
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('AdaptiveJointCrossHuber242_round148_full_registration_v7_20261009',new.name,[],pins)
create(A/'round148_remote_verified_reconcile_hidden_launch_v5_20261009.json',row);print(row,flush=True)
