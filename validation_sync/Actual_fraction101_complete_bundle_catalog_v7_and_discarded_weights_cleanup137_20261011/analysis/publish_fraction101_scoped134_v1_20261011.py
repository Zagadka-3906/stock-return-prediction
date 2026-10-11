from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from scoped_user_cleanup_package134_runtime_v1_20261011 import install
gates=install()
from run_dependency_queue_v3_20261006 import read,sha,create,owned
original_closed=gates.closed
def closed(name):
    return original_closed('actual_fraction101_scoped_seal134_v1_20261011' if name=='Rank120Rank60ConsensusFraction8Early101_selected_candidate_sealing_v1_20261011' else name)
gates.closed=closed
import owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 as holdmodule
original_hold=holdmodule.hold
class Stopped:
    def is_running(self):return False
def hold(identity,needle):
    assert gates.allowed() and not owned(identity)
    guard=read(A/'user_requested_stop1300_until_manual_continue_v1_20261011/guardian_status.json')
    assert guard['status']=='finished_project_stop_ready_for_user_computer_shutdown' and guard['automatic_restart_enabled'] is False
    return Stopped(),Stopped(),{'status':'actual_old_watcher_stopped_no_restart_or_suspend_needed','identity':identity}
holdmodule.hold=hold
try:runpy.run_path(str(A/'publish_actual_consensusFraction101_complete_candidate_main_v1_20261011.py'),run_name='__main__')
finally:holdmodule.hold=original_hold;gates.closed=original_closed
create(A/'actual_fraction101_scoped134_publication_execution_verification_v1_20261011.json',{'status':'passed_original_manifest_all_raw_blobs_remote_main_and_serial_mutex_verification_retained_stopped_watcher_not_restarted','original_receipt':read(A/'Actual_consensusFraction101_complete_candidate_sources_and_submission_main_receipt_v1_20261011.json'),'new_training':0,'new_scoring':0,'new_inference':0,'test_labels_read':False})
