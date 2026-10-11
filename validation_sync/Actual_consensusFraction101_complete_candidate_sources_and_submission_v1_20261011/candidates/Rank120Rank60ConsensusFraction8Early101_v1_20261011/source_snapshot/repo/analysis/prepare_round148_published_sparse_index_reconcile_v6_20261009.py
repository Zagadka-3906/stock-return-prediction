from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
old=A/'reconcile_round148_remote_verified_v5_20261009.py';new=A/'reconcile_round148_published_sparse_index_v6_20261009.py'
s=old.read_text(encoding='utf8').replace('round148_remote_verified_reconcile_v5_20261009','round148_published_sparse_index_reconcile_v6_20261009')
s=s.replace('AdaptiveJointCrossHuber242_round148_full_registration_v7_20261009','AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009')
s=s.replace("  assert value('rev-parse','HEAD')==rejected","  assert value('rev-parse','HEAD')==commit")
s=s.replace("  assert sha(original)==descriptor['compressed_sha256']","  assert not original.exists() # Private duplicate was removed after successful remote verification.")
start=s.index("  assert value('rev-parse','refs/heads/main')==parent_commit")
end=s.index("  helpers.watcher.advance_source_index(commit)",start)
replacement="""  assert value('rev-parse','refs/heads/main')==commit
  assert value('rev-parse','HEAD')==commit
  # The prior publisher intentionally omitted archived tracked files using skip-worktree.
  # read-tree cleared those private-index flags; restore flags only for unchanged, absent archives.
  deleted=git('ls-files','--deleted','-z').split(b'\\0');deleted=[p for p in deleted if p]
  for raw_name in deleted:
   name=raw_name.decode('utf8')
   assert name in previous_tree and name in actual and actual[name]==previous_tree[name],name
   assert not name.startswith('validation_sync/round148/'),name
   assert not (work/name).exists(),name
  if deleted:git('update-index','--skip-worktree','-z','--stdin',data=b'\\0'.join(deleted)+b'\\0')
  create(OUT/'restored_private_archive_skip_worktree_flags.json',{'count':len(deleted),
    'only_absent_unchanged_historical_blobs':True,'private_index_only':True,'root_index_untouched':True})
  assert not value('status','--porcelain')
"""
s=s[:start]+replacement+s[end:]
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
pins={str(p):sha(p) for p in (old,new,Path(__file__))}
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009',new.name,[],pins)
create(A/'round148_published_sparse_index_reconcile_hidden_launch_v6_20261009.json',row);print(row['owned_worker_pid'],flush=True)
