"""Reuse the actual registered74-case scope and finish full QA with native read handles."""
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
SOURCE=A/'run_longer_residual74_round104_full_registration_20261006.py'


def main():
    old=A/'service_owned_workflows_20261006/longer_residual74_round104_full_registration'
    assert not owned(read(old/'native_launch.json'))
    assert read(old/'service_execution.json')['status']=='failed'
    assert 'Too many open files' in read(old/'service_execution.json')['failure']
    preflight=A/'win32_read_handle_hash_cache_full104_preflight_20261006.json'
    proof=read(preflight)
    assert proof['actual_simultaneous_native_read_handles']==8240
    assert proof['actual_write_handle_denial_WinError']==32
    folder=A/'optimization_20261003_r104'
    assert sha(folder/'protocol.json')==proof['original_protocol_sha256']
    assert read(folder/'actual_registration_preparation.json')['status']=='passed_actual74_scores_controls_and_sealed_selected_model_candidate_registered'
    assert not (ROOT/'results/optimization_20261003_r104.json').exists()
    assert not (A/'github_validation_sync_main_20261005/round104_receipt.json').exists()
    recovery_paths=[Path(__file__),SOURCE,preflight,A/'win32_read_handle_hash_cache_20261006.py',
        A/'publish_longer_residual74_round104_full_validation_v2_20261006.py',
        folder/'full_registration_failure.json',old/'service_execution.json',old/'stderr.log']
    recovery_pins={str(p):sha(p) for p in recovery_paths}
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        '    protocol = prepare()':
            "    protocol = read(A / 'optimization_20261003_r104/protocol.json')\n"
            "    protocol = {**protocol, 'input_sha256': {**protocol['input_sha256'], **RECOVERY_PINS}}",
        'from locked_read_hash_cache_20261004 import LockedReadHashCache':
            'from win32_read_handle_hash_cache_20261006 import LockedReadHashCache',
        'frozen_before_actual_full_registration.json':'frozen_before_actual_full_registration_v2.json',
        'actual_main7_idle_before_and_after_hold.json':'actual_main7_idle_before_and_after_hold_v2.json',
        'actual_hidden_registration_children.json':'actual_hidden_registration_children_v2.json',
        'full_registration_failure.json':'full_registration_failure_v2.json',
        'from publish_longer_residual74_round104_full_validation_20261006 import main as github':
            'from publish_longer_residual74_round104_full_validation_v2_20261006 import main as github'}
    for before in sorted(changes,key=len,reverse=True):
        assert before in text,before
        text=text.replace(before,changes[before])
    import publish_classifier_consensus_workflows_20261006 as helpers
    previous_git=helpers.sync.git
    retries=[]
    def retry_git(*args,**kwargs):
        for attempt in range(3):
            try:return previous_git(*args,**kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote','push','fetch') or not any(word in str(error).lower() for word in ('tls','ssl','unable to access','connection','timed out')):raise
                retries.append({'command':args[0],'attempt':attempt+1,'error':str(error)[:1500]})
                if attempt==2:raise
                time.sleep(2)
    namespace={'__file__':__file__,'__name__':'actual_full104_read_handle_recovery_v2',
        'RECOVERY_PINS':recovery_pins}
    exec(compile(text,str(SOURCE),'exec'),namespace)
    helpers.sync.git=retry_git
    try:namespace['main']()
    finally:
        helpers.sync.git=previous_git
        create(folder/'actual_transport_retries_v2.json',{'attempts':retries,'TLS_verification_unchanged':True})


if __name__=='__main__':main()
