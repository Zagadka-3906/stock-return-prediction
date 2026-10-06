"""Register completed actual pilots using the proven Win32 read-handle scope."""
from pathlib import Path
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write

NAMES={105:'robust_residual50',106:'simplex_residual47'}


def service(name):
    folder=A/'service_owned_workflows_20261006'/name
    return folder,read(folder/'native_launch.json')


def main():
    import psutil
    number=int(sys.argv[1]);assert number in NAMES
    label=NAMES[number]
    out=A/f'{label}_round{number}_registration_recovery_v4_20261006'
    assert not out.exists();out.mkdir()
    old_name=f'{label}_round{number}_full_registration'
    old_folder,old_identity=service(old_name)
    assert not owned(old_identity) and read(old_folder/'service_execution.json')['status']=='failed'
    existing_protocol = A/f'optimization_20261003_r{number}/protocol.json'
    if number == 105:
        assert existing_protocol.exists()
        assert read(A/'optimization_20261003_r105/actual_registration_preparation.json')['status'].startswith('passed_actual50')
        assert read(A/'service_owned_workflows_20261006/robust_residual50_round105_full_registration_v3/service_execution.json')['status']=='failed'
    else:
        assert not existing_protocol.exists()
    assert not (ROOT/f'results/optimization_20261003_r{number}.json').exists()
    prep=A/f'{label}_full_registration_preparation_20261006.json'
    pins=dict(read(prep)['input_sha256'])
    requirements=[f'{label}_candidate_inference',f'{label}_candidate_sealing']
    if number==105:requirements.append('longer_residual74_round104_full_registration_v2')
    else:requirements.extend(['robust_residual50_round105_full_registration_v4','residual_simplex47_scores_evidence_publication'])
    identities={}
    writer=None
    while True:
        terminal={};closed={}
        for name in requirements:
            folder=A/'service_owned_workflows_20261006'/name
            if name not in identities and (folder/'native_launch.json').exists():identities[name]=read(folder/'native_launch.json')
            closed[name]=name in identities and not owned(identities[name])
            terminal[name]=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else None
            if closed[name] and terminal[name] is not None:assert terminal[name]['status']=='passed',(name,terminal[name])
        passed=all(closed.values()) and all(row and row['status']=='passed' for row in terminal.values())
        state=read(A/'service_owned_dependency_queue_v4_20261006/state.json')
        live={name:row for name,row in state['activated_jobs'].items() if name.startswith('round') and owned(row)}
        candidate=state['activated_jobs'].get('round89')
        writer=candidate if candidate is not None else writer
        writer_closed=writer is not None and not owned(writer)
        execution=Path(writer['script_args'][0]).parent/'execution.json' if writer else None
        writer_terminal=read(execution) if execution and execution.exists() else None
        if writer_closed and writer_terminal is not None and writer_terminal['status']=='passed':
            writer_closed=(A/'github_validation_sync_main_20261005/round89_receipt.json').exists()
        available=psutil.virtual_memory().available/2**30
        write(out/'waiting_status.json',{'status':'waiting_for_actual_candidate_seals_preceding_full_registration_and_proven_terminal_original_writer',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'preceding_actual_status':terminal,'preceding_owned_handles_closed':closed,
            'original89_identity':writer,'original89_closed_and_terminal':writer_closed and writer_terminal is not None,
            'live_original_scientific_rounds':live,'available_RAM_GiB':available})
        if passed and not live and writer_closed and writer_terminal is not None and available>=9:break
        time.sleep(15)
    queue_plan=A/'service_owned_dependency_queue_bootstrap_fields_recovery_v2_20261006/queue_plan.json'
    plan=read(queue_plan)
    assert plan['complete_ranking_registration_serialization_markers']==[str(A/f'optimization_20261003_r{n}/full_registration_execution.json') for n in (105,106)]
    source=A/f'run_{label}_round{number}_full_registration_20261006.py'
    publisher=A/f'publish_{label}_round{number}_full_validation_20261006.py'
    evidence=[Path(__file__),source,publisher,prep,queue_plan,
        A/'win32_read_handle_hash_cache_20261006.py',A/'win32_read_handle_hash_cache_full104_preflight_20261006.json',
        A/'dependency_queue_v11_bootstrap_recovery_20261006/verification.json',
        A/'dependency_queue_v11_bootstrap_recovery_20261006/original89_actual_initialization_failure.json',
        old_folder/'service_execution.json',old_folder/'stderr.log',execution,Path(writer['stderr']),
        Path(writer['script_args'][0]),Path(writer['script_args'][0]).parent/'qualified_run.json',
        A/'optimization_20261003_r89/provenance_scope_execution.json']
    evidence += [A / 'win32_read_handle_hash_cache_with_filename_v2_20261006.py', A / 'full105_read_handle_denied_paths_actual_probe_20261006.json', A / 'run_residual_round105_106_registration_recovery_v4_20261006.py', A / 'frozen_controller_name_collision_restoration_20261006/source_restoration_verification.json', A / 'frozen_controller_name_collision_restoration_20261006/verification.json', A / 'run_dependency_queue_bootstrap_fields_recovery_v1_20261006.py', A / 'run_residual_round105_106_registration_recovery_v4_20261006.py']
    for prior in ('robust_residual50_round105_full_registration_v2', 'simplex_residual47_round106_full_registration_v2', 'robust_residual50_round105_full_registration_v3', 'simplex_residual47_round106_full_registration_v3'):
        old_attempt = A / 'service_owned_workflows_20261006' / prior
        evidence += list(old_attempt.glob('*.json')) + list(old_attempt.glob('*.log'))
    if number == 105:
        evidence += [A / 'optimization_20261003_r105/full_registration_failure_v2.json', A / 'optimization_20261003_r105/frozen_before_actual_full_registration_v4.json', A / 'optimization_20261003_r105/actual_main7_idle_before_and_after_hold_v4.json']
    for name in requirements:
        folder=A/'service_owned_workflows_20261006'/name
        evidence.extend([folder/'service_execution.json',folder/'native_launch.json'])
    pins.update({str(p):sha(p) for p in evidence})
    for path,digest in pins.items():assert sha(path)==digest,path
    admission={'status':'passed_actual_original_writer_terminal_and_complete_sealed_candidate_admission',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':number,'input_sha256':pins,
        'original89_actual_terminal_status':writer_terminal,'scientific_writer_ever_stopped':False,
        'full105_106_and_original_round90_quality_writers_serialized_by_queue_markers':True,
        'actual_completed_pilot_and_inference_unchanged':True,'test_labels_read':False}
    create(out/'actual_admission.json',admission)
    pins[str(out/'actual_admission.json')]=sha(out/'actual_admission.json')
    text=source.read_text(encoding='utf-8')
    replace={
        '    protocol = prepare()':"    protocol = read(A / 'optimization_20261003_r105/protocol.json') if NUMBER == 105 else prepare()\n    protocol = {**protocol, 'input_sha256': {**protocol['input_sha256'], **RECOVERY_PINS}}",
        'from locked_read_hash_cache_20261004 import LockedReadHashCache':'from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache',
        f'from publish_{label}_round{number}_full_validation_20261006 import main as github':'github = RECOVERY_PUBLISHER',
        'frozen_before_actual_full_registration.json':'frozen_before_actual_full_registration_v4.json',
        'actual_main7_idle_before_and_after_hold.json':'actual_main7_idle_before_and_after_hold_v4.json',
        'actual_hidden_registration_children.json':'actual_hidden_registration_children_v4.json',
        'full_registration_failure.json':'full_registration_failure_v4.json'}
    for before in sorted(replace,key=len,reverse=True):
        assert before in text,before
        text=text.replace(before,replace[before])
    def recovery_publisher():
        body=publisher.read_text(encoding='utf-8')
        before='    for path in extra:';assert body.count(before)==1
        paths=[*evidence,out/'actual_admission.json',A/f'optimization_20261003_r{number}/frozen_before_actual_full_registration_v4.json',
            A/f'optimization_20261003_r{number}/actual_main7_idle_before_and_after_hold_v4.json']
        paths+=list((A/'dependency_queue_v11_bootstrap_recovery_20261006').glob('*.json'))
        body=body.replace(before,'    extra += RECOVERY_EVIDENCE\n'+before)
        ns={'__file__':str(publisher),'__name__':f'actual_complete_round{number}_recovery_publication',
            'RECOVERY_EVIDENCE':list(dict.fromkeys(paths))}
        exec(compile(body,str(publisher),'exec'),ns);ns['main']()
    import publish_classifier_consensus_workflows_20261006 as helpers
    prior_git=helpers.sync.git;retries=[]
    def retry_git(*args,**kwargs):
        for attempt in range(3):
            try:return prior_git(*args,**kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote','push','fetch') or not any(word in str(error).lower() for word in ('tls','ssl','unable to access','connection','timed out')):raise
                retries.append({'command':args[0],'attempt':attempt+1,'error':str(error)[:1200]})
                if attempt==2:raise
                time.sleep(2)
    ns={'__file__':str(source),'__name__':f'actual_round{number}_native_HANDLE_registration_recovery_v2',
        'RECOVERY_PINS':pins,'RECOVERY_PUBLISHER':recovery_publisher,'NUMBER':number}
    exec(compile(text,str(source),'exec'),ns)
    helpers.sync.git=retry_git
    try:ns['main']()
    finally:
        helpers.sync.git=prior_git
        create(out/'actual_transport_retries.json',{'attempts':retries,'TLS_verification_unchanged':True})


if __name__=='__main__':main()
