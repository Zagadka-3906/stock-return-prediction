"""A labeled throughput extrapolation from actual mature row counts; no quality or speedup claim."""
from pathlib import Path
from datetime import datetime,timedelta
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    import polars as pl
    import neural_BF16_micro8192_native_v1_20261008 as native
    from run import FEATURE_FILE,fold_cutoff
    bank=Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    info_path=bank/'2020/info.json';info=read(info_path)
    assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
    plans=[native.architecture.training_frame(pl.scan_parquet(FEATURE_FILE),fold_cutoff(y),native.CONFIG)
           .select(pl.len().alias('rows'),pl.col('trade_date').min().alias('first'),pl.col('trade_date').max().alias('last'))
           for y in range(2020,2026)]
    measured=pl.collect_all(plans)
    counts={year:frame.row(0,named=True) for year,frame in zip(range(2020,2026),measured)}
    assert counts[2020]['rows']==info['training_meta']['rows']
    for year in range(2020,2026):assert counts[year]['last']<fold_cutoff(year)
    progress=read(A/'actual_manual_resume_progress_20261008.json')
    completed={item['year'] for item in progress['new_BF16_completed_annual_models']}
    active=progress.get('new_BF16_latest_actual_epoch',{})
    seconds_per_row=info['fit_seconds_including_checkpoints_this_process']/counts[2020]['rows']
    remaining=0.
    for year,meta in counts.items():
        if year in completed:continue
        fraction=1.
        if active.get('year')==year:fraction=max(0.,(32-active['completed_epoch'])/32)
        remaining+=meta['rows']*seconds_per_row*fraction
    now=datetime.now().astimezone()
    out=A/'actual_BF16_remaining_bank_runtime_estimate_v1_20261008.json'
    paths=[Path(__file__),Path(native.__file__),Path(native.architecture.__file__),
           bank/'protocol.json',info_path,ROOT/'run.py',A/'actual_user_submission_deadline_and_priority_20261008.json']
    create(out,{'status':'actual_row_count_based_remaining_fit_extrapolation_with_explicit_assumptions',
        'at_local':now.isoformat(timespec='seconds'),'input_sha256':{str(p):sha(p) for p in paths},
        'feature_file_sha256_from_original_frozen_training_protocol':read(bank/'protocol.json')['input_sha256'][str(FEATURE_FILE)],
        'actual_mature_counts':counts,'actual_first_annual_fit_seconds':info['fit_seconds_including_checkpoints_this_process'],
        'completed_annual_years_at_snapshot':sorted(completed),'active_epoch_at_snapshot':active,
        'central_remaining_fit_hours_if_cost_scales_linearly':remaining/3600,
        'illustrative_runtime_range_hours':[remaining*.7/3600,remaining*1.4/3600],
        'illustrative_range_is_not_statistical_confidence_interval':True,
        'illustrative_fit_finish_range_local':[(now+timedelta(seconds=remaining*x)).isoformat(timespec='minutes') for x in (.7,1.4)],
        'annual_replays_independent_oracle_official_scoring_candidate_inference_and_final_delivery_extra':True,
        'unknown_later_GPU_memory_or_system_contention_can_increase_runtime':True,
        'not_global_goal_completion_or_guaranteed_speedup_estimate':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'remaining_fit_hours_central':remaining/3600,'illustrative_range_hours':[remaining*.7/3600,remaining*1.4/3600],
           'own_mature_rows':{y:r['rows'] for y,r in counts.items()}},flush=True)


if __name__=='__main__':main()
