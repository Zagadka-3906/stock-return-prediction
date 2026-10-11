"""Record observed owned idle RAM gates and actual diagnostic fits, without claiming exhausted resources."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import stack

def main():
    import psutil
    name_to_file={'nonflag_RFF128Low76_official_comparison_v1':'run_nonflag_RFF128Low76_official_comparison_v1_20261007.py',
        'nonflag_residual_RFF128Hi_native_bank10':'train_nonflag_residual_RFF128Hi_bank10_v1_20261007.py'}
    observations={}
    for name,source in name_to_file.items():
        row=read(A/'service_owned_workflows_20261006'/name/'native_launch.json');assert owned(row)
        observed=stack(row['owned_worker_pid'])
        observations[name]={'strong_owned_identity':row,'observed_readonly_stack':observed,
            'actual_RSS_GiB':psutil.Process(row['owned_worker_pid']).memory_info().rss/2**30,
            'RAM_gate_GiB':11 if 'official' in name else 14,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}
    external=[]
    for p in psutil.process_iter(['name','memory_info']):
        try:
            if p.info['name'] in ('qemu-system-x86_64-headless.exe','java.exe'):
                external.append({'pid':p.pid,'birth_time':p.create_time(),'name':p.info['name'],
                    'RSS_GiB':p.info['memory_info'].rss/2**30})
        except (psutil.NoSuchProcess,psutil.AccessDenied):pass
    hi=A/'nonflag_residual_RFF128Hi_bank10_20261007';low=A/'nonflag_RFF128Low76_official_comparison_v1_20261007'
    count=len(list(hi.glob('*/info_*.json')));cases=len(list(low.glob('case*_official.json')))
    diagnostic=A/'nonflag_residual_RFF128Hi_codec2_preflight_20261007/verification.json'
    assert read(diagnostic)['actual_diagnostic_fits']==2
    source_admission=A/'nonflag_RFF128Low76_round126_source_admission_v1_20261007.json'
    admission=read(source_admission)
    assert len(admission['graph_metadata_controls'])==24 and len(admission['baseline_gain_regressions'])==9
    for p,d in admission['input_sha256'].items():assert sha(p)==d,p
    receipt=A/'github_validation_sync_main_20261005/round125_receipt.json';assert read(receipt)['connected_records']==13138
    paths=[Path(__file__),diagnostic,source_admission,receipt,
        A/'nonflag_RFF128Low126_execution_gate_recovery_admission_20261007.json',
        A/'prepare_nonflag_residual_RFF128Hi_bank10_20261007.py',A/'prepare_nonflag_RFF128Hi76_controls_20261007.py',
        A/'nonflag_residual_RFF128Hi10_plan_20261007.json',A/'nonflag_RFF128Hi76_plan_20261007.json',
        *[A/n for n in name_to_file.values()]]
    out=A/'local_RAM_wait_and_next_native_recipe_context_20261007.json'
    create(out,{'status':'recorded_actual_single_host_RAM_gates_and2_stronger_L2_diagnostic_fits',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},
        'strong_owned_waiter_observations':observations,'available_RAM_GiB':psutil.virtual_memory().available/2**30,
        'external_application_resident_memory_observations':external,'external_processes_stopped':0,
        'original_GPU_and_queue_stopped':False,'actual_Hi_diagnostic_fits':2,'actual_Hi_annual_native_fits':count,
        'actual_LOW76_completed_official_scores':cases,'expected_LOW76_scores':76,
        'LOW126_native10_hooks6_full73_cold219_completed_not_future_qualification':True,
        'latest_fully_qualified_round':125,'best_fully_qualified_round':121,'best_score':read(receipt)['official_score'],
        'global_resource_and_feasible_direction_exhaustion_proven':False,'test_labels_read':False})
    print({'actual_Hi_native_fits':count,'actual_LOW_official_scores':cases,'RAM_available_GiB':psutil.virtual_memory().available/2**30},flush=True)
if __name__=='__main__':main()
