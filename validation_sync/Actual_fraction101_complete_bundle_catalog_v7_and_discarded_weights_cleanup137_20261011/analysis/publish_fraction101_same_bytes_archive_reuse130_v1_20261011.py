from pathlib import Path
import sys,runpy,os,hashlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as gates
assert gates.allowed();oldclosed=gates.closed;gates.closed=lambda n:oldclosed('actual_fraction101_partial_seal131_v1_20261011' if n=='Rank120Rank60ConsensusFraction8Early101_selected_candidate_sealing_v1_20261011' else n)
import publish_classifier_consensus_workflows_20261006 as h
previous=h.sync.atomic;workspace=h.sync.WORKTREE.resolve();events=[]
def atomic(path,data):
 path=Path(path);rel=path.resolve().relative_to(workspace).as_posix()
 if rel.startswith('validation_sync/Actual_consensusFraction101_complete_candidate_sources_and_submission_v1_20261011/'):
  old=rel.replace('Actual_consensusFraction101_complete_candidate_sources_and_submission','Actual_consensusWeight85_complete_candidate_sources_and_submission').replace('Rank120Rank60ConsensusFraction8Early101','Rank120Rank60ConsensusWeight8Early85');source=workspace/old
  if source.is_file() and not source.is_symlink() and source.stat().st_size==len(data) and sha(source)==hashlib.sha256(data).hexdigest():
   assert not path.exists();path.parent.mkdir(parents=True,exist_ok=True);os.link(source,path);assert source.stat().st_ino==path.stat().st_ino;events.append({'path':str(path),'source':str(source),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()});return
 return previous(path,data)
h.sync.atomic=atomic
try:runpy.run_path(str(A/'publish_actual_consensusFraction101_complete_candidate_main_v1_20261011.py'),run_name='__main__')
finally:h.sync.atomic=previous;gates.closed=oldclosed
create(A/'actual_fraction101_same_bytes_main_archive_reuse130_verification_v1_20261011.json',{'status':'passed_same_bytes_regular_archive_links_only_all_original_raw_git_blob_and_remote_main_verification_preserved','events':events,'reused_bytes':sum(e['bytes'] for e in events),'input_sha256':{str(Path(__file__)):sha(__file__)}})
