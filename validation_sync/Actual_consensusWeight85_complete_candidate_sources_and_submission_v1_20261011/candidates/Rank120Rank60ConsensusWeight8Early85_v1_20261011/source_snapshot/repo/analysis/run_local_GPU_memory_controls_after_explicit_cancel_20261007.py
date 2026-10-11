"""Reviewable GPU pilot route; cannot run before an actual explicit user cancellation."""
from pathlib import Path
import sys,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
def main():
    from run_dependency_queue_v3_20261006 import read,sha,owned
    authorization=A/'original_GPU_current_fit_explicit_user_cancellation_20261007.json'
    # This marker may only be created after the real user's reply authorizes losing unsaved progress.
    assert authorization.exists(),'Await actual explicit user reply; preserve the current GPU fit'
    approval=read(authorization)
    assert approval['status']=='actual_user_authorized_current_unsaved_fit_cancellation_and_owned_processes_closed'
    assert approval['authorization_source']=='actual_user_reply_in_this_chat'
    assert approval['original_completed_2020_artifacts_preserved'] is True
    assert not owned(approval['previous_owned_gpu_identity'])
    for p,d in approval['completed_artifact_sha256'].items():assert sha(p)==d,p
    old=A/'run_memory_efficient_mlp_gpu_controls_v2_20261005.py';text=old.read_text(encoding='utf8')
    start=text.index('def original_gpu_work_closed():');end=text.index('\n\ndef main():',start)
    text=text[:start]+"""def original_gpu_work_closed():
    approval=read(A/'original_GPU_current_fit_explicit_user_cancellation_20261007.json')
    from run_dependency_queue_v3_20261006 import owned
    assert approval['status']=='actual_user_authorized_current_unsaved_fit_cancellation_and_owned_processes_closed'
    return not owned(approval['previous_owned_gpu_identity'])
"""+text[end:]
    text=text.replace("STATE = A / 'memory_efficient_mlp_gpu_control_state_v2_20261005.json'",
        "STATE = A / 'local_GPU_memory_control_state_after_user_cancel_20261007.json'")
    text=text.replace("output, scratch = Path(storage['GPU_control_directory']), Path(storage['temporary_directory'])",
        "output, scratch = A/'local_GPU_memory_controls_after_user_cancel_20261007', ROOT/'tmp/local_GPU_memory_controls_after_user_cancel_20261007'")
    text=text.replace("A / 'neural16384_full_bank_20261005/training_execution_scope.json'",
        "A / 'original_GPU_current_fit_explicit_user_cancellation_20261007.json'")
    text=text.replace("'native_original32epoch_training_untouched': True",
        "'original_scientific_sources_and_completed2020_artifacts_preserved': True, 'explicit_user_cancelled_unsaved_current_fit': True")
    text=text.replace("'waiting_for_actual_original_GPU_annual_and_final_process_closure_then14GiB_host_reserve'",
        "'actual_explicit_user_cancellation_and_owned_GPU_closure_then14GiB_host_reserve'")
    # Record the exact derived driver as well as the unchanged original code in the pilot's own freeze.
    needle="sources = [Path(__file__), RUN,";assert text.count(needle)==1
    text=text.replace(needle,"sources = [Path(__file__), A/'run_memory_efficient_mlp_gpu_controls_v2_20261005.py', RUN,")
    namespace={'__file__':str(Path(__file__)),'__name__':'actual_local_GPU_controls_after_explicit_user_cancellation'}
    exec(compile(text,str(Path(__file__)),'exec'),namespace)
    namespace['main']()
if __name__=='__main__':main()
