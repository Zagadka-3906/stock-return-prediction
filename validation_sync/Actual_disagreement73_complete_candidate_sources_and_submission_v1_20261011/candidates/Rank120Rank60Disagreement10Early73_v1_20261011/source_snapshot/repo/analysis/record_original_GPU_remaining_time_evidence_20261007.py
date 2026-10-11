"""Observe actual epoch throughput; distinguish extrapolation from scientific completion."""
from pathlib import Path
from datetime import datetime,timedelta
import sys,re,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    folder=A/'service_owned_workflows_20261006/neural16384_annual';identity=read(folder/'native_launch.json')
    assert owned(identity) and not (folder/'service_execution.json').exists()
    p=folder/'stdout.log';raw=p.read_bytes();text=raw.decode('utf8')
    matches=list(re.finditer(r'\[(\d\d:\d\d:\d\d)\] MLP y_rank epoch(\d+)/32 mature-training loss=([0-9.]+)',text))
    assert matches and 'fold2021: fitting 2,594,048 mature rows, 63 features' in text
    started=datetime.fromisoformat(identity['at_local']);last=started;records=[]
    for m in matches:
        observed=datetime.combine(last.date(),datetime.strptime(m[1],'%H:%M:%S').time())
        if observed<last:observed+=timedelta(days=1)
        records.append({'epoch':int(m[2]),'at_local':observed.isoformat(),'mature_training_loss':float(m[3])});last=observed
    assert records[-1]['epoch']<32
    intervals=[]
    for before,after in zip(records,records[1:]):
        n=after['epoch']-before['epoch'];assert n>0
        if n==4:
            hours=(datetime.fromisoformat(after['at_local'])-datetime.fromisoformat(before['at_local'])).total_seconds()/3600
            intervals.append({'from_epoch':before['epoch'],'to_epoch':after['epoch'],'actual_hours':hours,'hours_per_epoch':hours/n})
    assert len(intervals)>=3
    base=A/'neural_regularization_bank_20261003/rank512_drop000_e32'
    info_paths=[base/f'info_{year}.json' for year in (2021,2022,2023,2024)]
    rows={year:read(base/f'info_{year}.json')['training_meta']['rows'] for year in (2021,2022,2023,2024)}
    assert rows[2021]==2594048
    scaling=sum(rows[year]/rows[2021] for year in (2022,2023,2024))
    lower=32*scaling*min(i['hours_per_epoch'] for i in intervals)
    upper=32*scaling*max(i['hours_per_epoch'] for i in intervals)
    controls=A/'memory_efficient_mlp_preflight_20261005/verification.json'
    c=read(controls);assert c['status']=='passed_actual_gradients_saved_tensors_and_mature_CPU_pilots'
    assert c['actual_full_annual_fits']==0 and c['actual_16384_GPU_fits']==0
    paths=[Path(__file__),folder/'native_launch.json',*info_paths,controls,
        A/'memory_efficient_neural_complete_search_plan_20261005.json',
        A/'memory_efficient_neural_workflow_preflight_20261005/verification.json',
        A/'memory_efficient_neural_workflows_github_20261005/receipt.json',
        A/'neural16384_actual_shared_GPU_memory_boundary_evidence_20261006.json']
    assert owned(identity)
    destination=A/'nonflag_residual_RFFRidge_bank10_20261007/original_GPU_throughput_context_before_RFF_comparison.json'
    create(destination,{'status':'observed_actual_live_original_2021_training_and_conditional_remaining_time_estimate',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_owned_original_worker':identity,
        'mutable_stdout_observation':{'path':str(p),'captured_sha256':hashlib.sha256(raw).hexdigest(),'captured_utf8_text':text,
            'not_a_lifetime_frozen_input':True},'actual_logged_epochs':records,'actual_four_epoch_intervals':intervals,
        'matched_actual_mature_training_rows':rows,
        'conditional_remaining2022_2023_2024_training_hours':{'lower':lower,'upper':upper},
        'estimate_assumption':'future epochs take the measured range of hours per training row; this is an extrapolation, not a hardware limit or completion guarantee',
        'estimate_excludes_current_2021_remaining_epochs_final_2025_fit_future_checks_and_quality_scoring':True,
        'planned_user_five_day_window_hours':120,'all_current_extrapolated_training_estimates_exceed_five_days':lower>120,
        'prepared_memory_efficient_modes':['accumulate','checkpoint','combined'],
        'actual_memory_efficient_CPU_small_control_fits':c['actual_small_control_fits'],
        'actual_memory_efficient_full_annual_fits':0,'actual_memory_efficient16384_GPU_measurements':0,
        'no_memory_efficient_GPU_speedup_promised':True,'existing_original_2020_fit_and_current_2021_training_retained':True,
        'old_GPU_shared_memory_evidence_date':'2026-10-06; not freshly measured by this observation',
        'input_sha256':{str(p):sha(p) for p in paths},'new_native_fits':0,'new_quality_scores':0,
        'scientific_workers_stopped_or_restarted':0,'global_feasible_direction_exhaustion_not_proven':True,'test_labels_read':False})
    print({'logged_epoch':records[-1]['epoch'],'conditional_2022_2024_hours':[lower,upper],'actual_GPU_worker_live':True},flush=True)
if __name__=='__main__':main()
