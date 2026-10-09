"""Resolve an inherited '55' service name to the frozen152 scope: exactly25 full and75 cold cases."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    actual_name='SparseAfter14825_full_historical_controls_v2_20261009'
    service=A/'service_owned_workflows_20261006'/actual_name
    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(10)
    assert read(service/'service_execution.json')['status']=='passed'
    pointer=A/'actual_SparseAfter14825_parent148_location_v1_20261009.json';location=read(pointer)
    full=Path(location['output'])/'verification.json';assert sha(full)==location['verification_sha256']
    proof=read(full)
    assert proof['actual_stage_base_round']==148
    assert (proof['actual_full_cases_including_identity'],proof['actual_cold_cases_including_identity'])==(25,75)
    assert len(proof['records'])==25 and all(r['rows']==5635800 and len(r['cold_controls'])==3 for r in proof['records'])
    planpath=A/'SparseAfter14829_round152_plan_v1_20261009.json';plan=read(planpath)
    assert len(plan['new_cases'])==24 and plan['expected_new_full_cases']==25 and plan['expected_scored_cases']==29
    receiver=A/'verify_SparseAfter14829_round152_sources_v1_20261009.py';text=receiver.read_text(encoding='utf8')
    assert 'SparseAfter14855_full_historical_controls_v1_20261009' in text
    assert "current['actual_full_cases_including_identity']==25" in text
    assert "current['actual_cold_cases_including_identity']==75" in text
    for f,d in proof['input_sha256'].items():assert sha(f)==d,f
    import polars as pl
    frame=A/'connected_validation_20261002/combined_fold_frame.parquet'
    shape=pl.scan_parquet(frame).select(pl.len().alias('rows'),pl.col('trade_date').n_unique().alias('days'),pl.col('ts_code').n_unique().alias('stocks')).collect().row(0)
    assert shape==(5635800,1212,4650)
    sources=[Path(__file__),pointer,full,planpath,receiver,frame,service/'native_launch.json',service/'service_execution.json']
    create(A/'SparseAfter148152_legacy55_wait_gate_actual25_bridge_v40_20261009.json',{
        'status':'passed_legacy_service_name_resolved_to_actual_frozen25_full75_cold_scope',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'legacy_service_name':'SparseAfter14855_full_historical_controls_v1_20261009','actual_underlying_service':actual_name,
        'actual_complete_period_cases':25,'actual_cold_cases':75,'rows_days_stocks':[5635800,1212,4650],
        'actual152_receiver_already_requires25_not55_scientific_cases':True,
        'legacy55_name_not_a_claim_of55_executed_cases':True,'original_scientific_plan_and_full_controls_preserved':True,
        'all_original_cases_scored_by_following_receiver_still_required':29,
        'no_scientific_job_restarted_or_retired':True,'new_quality_scores':0,'test_labels_read':False})
    print({'legacy_namespace':'55','actual_verified_full_cases':25,'actual_verified_cold_cases':75,'actual_new_tests':0},flush=True)
if __name__=='__main__':main()
