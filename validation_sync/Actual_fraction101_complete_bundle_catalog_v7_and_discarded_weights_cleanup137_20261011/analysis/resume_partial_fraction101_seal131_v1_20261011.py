from pathlib import Path
import os,sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
assert allowed();closed('Rank120Rank60ConsensusFraction8Early101_selected_candidate_preparation_v1_20261011')
failed=read(A/'service_owned_workflows_20261006/Rank120Rank60ConsensusFraction8Early101_selected_candidate_sealing_v1_20261011/service_execution.json');assert failed['status']=='failed' and '112' in failed['failure']
import rank120_rank60_consensusFraction8_early101_storage_v1_20261011 as storage
candidate=A.parent/'candidates/Rank120Rank60ConsensusFraction8Early101_v1_20261011';assert not (candidate/'manifest.json').exists()
original=os.link;events=[]
def exact_resume(source,destination,*args,**kwargs):
 source,destination=Path(source),Path(destination)
 if destination.exists():
  assert not args and not kwargs and destination.resolve().is_relative_to(candidate.resolve()) and sha(source)==sha(destination);events.append(str(destination));return
 return original(source,destination,*args,**kwargs)
os.link=exact_resume
try:runpy.run_path(str(A/'seal_Rank120Rank60ConsensusFraction8Early101_selected_candidate_v2_20261011.py'),run_name='__main__')
finally:os.link=original
create(A/'actual_fraction101_partial_seal131_resume_verification_v1_20261011.json',{'status':'passed_exact_existing_partial_links_reused_original_sealer_all_source_manifest_checks_completed_no_native_inference_rerun','existing_same_bytes_links_reused':len(events),'manifest_sha256':sha(candidate/'manifest.json'),'input_sha256':{str(Path(__file__)):sha(__file__)},'test_labels_read':False})
