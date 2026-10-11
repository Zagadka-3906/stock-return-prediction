from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from serial_main_publication_mutex_v1_20261009 import MainPublicationMutex
import handoff_joint_goss_round97_full_execution_20261006 as h
assert allowed();proof=A/'actual_192_heavy_ranking_writer_memory_release94_v1_20261011.json';assert read(proof)['status']=='verified_owned_metadata_writer_stopped_no_completed_registration_claim'
mutex=MainPublicationMutex();mutex.acquire()
try:
 stopped=read(A/'actual_192_heavy_ranking_writer_interruption_for_score_priority94_v1_20261011.json');assert not owned(stopped['identity'])
 identity=read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json');assert owned(identity)
 parent,worker=h.pair(identity);before=h.stack(worker.pid);assert '(idle)' in before and 'main (watch_validations_main_v7_20261006.py:71)' in before and not worker.children()
 assert parent.status()==worker.status()=='stopped'
 import publish_classifier_consensus_workflows_20261006 as pub
 assert not pub.sync.git('status','--porcelain');head=pub.sync.git('rev-parse','HEAD');pub.verify_main(head)
 create(A/'actual_owned_main_watcher94_interrupted_hold_release_admission_v1_20261011.json',{'status':'exact_idle_owned_watcher_single_192_hold_released_under_publication_mutex_after_actual86_main_complete','identity':identity,'before':before,'main_commit':head,'interruption_proof_sha256':sha(proof)})
 parent.resume();worker.resume()
 create(A/'actual_owned_main_watcher94_interrupted_hold_release_result_v1_20261011.json',{'status':'resumed_exact_owned_idle_main_watcher','parent_status':parent.status(),'worker_status':worker.status(),'main_commit':head})
finally:mutex.close()
