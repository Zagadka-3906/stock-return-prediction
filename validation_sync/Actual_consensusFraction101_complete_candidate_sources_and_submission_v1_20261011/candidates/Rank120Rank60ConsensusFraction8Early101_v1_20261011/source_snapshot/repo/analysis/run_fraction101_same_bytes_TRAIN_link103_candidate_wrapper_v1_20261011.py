from pathlib import Path
from contextlib import contextmanager
import sys,os,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
import rank120_rank60_consensusFraction8_early101_storage_v1_20261011 as storage
original=storage.installed_transfer;events=[]
approved=storage.EBASE/'selected_scoring/scoring_validation_only';canonical=A/'optimization_20261003_r95/scoring_validation_only'
@contextmanager
def linked():
 with original():
  previous=os.link
  def transfer(source,destination,*args,**kwargs):
   source,destination=Path(source),Path(destination)
   if destination.name in ('测试集_X.csv','测试集_Y.csv') and destination.parent.resolve()==approved.resolve():
    assert not args and not kwargs and source.resolve()==(canonical/destination.name).resolve() and not destination.exists() and source.is_file()
    digest=sha(source);os.symlink(source.resolve(),destination);assert destination.is_symlink() and sha(destination)==digest
    events.append({'source':str(source.resolve()),'destination':str(destination),'sha256':digest,'same_bytes_TRAIN_only_no_copy':True})
   else:previous(source,destination,*args,**kwargs)
  os.link=transfer
  try:yield
  finally:assert os.link is transfer;os.link=previous
storage.installed_transfer=linked
try:
 runpy.run_path(str(A/'run_Rank120Rank60ConsensusFraction8Early101_selected_candidate_feature_cache_v2_20261011.py'),run_name='__main__')
finally:
 storage.installed_transfer=original
 create(A/'actual_fraction101_same_bytes_TRAIN_links103_execution_v1_20261011.json',{'status':'actual_scoped_TRAIN_only_link_events_native_compute_unchanged_candidate_completion_remains_separate','events':events,'input_sha256':{str(Path(__file__)):sha(__file__),str(Path(storage.__file__)):sha(storage.__file__)},'test_labels_read':False})
