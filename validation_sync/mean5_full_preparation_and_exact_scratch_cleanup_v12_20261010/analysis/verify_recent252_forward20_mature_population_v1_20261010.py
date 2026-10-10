"""Independent math.fsum stock-calendar oracle and future-poison invariance for the joint window/target."""
from pathlib import Path
import sys,math
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha

def main():
    import polars as pl
    import recent252_forward20_mature_training_population_v1_20261010 as population
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    rows=[]
    for stock in ('A','B'):
        for day in range(1,421):
            if stock=='B' and day in (44,111,276):continue
            rows.append({'ts_code':stock,'trade_date':day,'is_train':not(stock=='B' and day==173),'price_valid':day%29!=0,'y_ret_1d':float('nan') if stock=='A' and day==138 else math.sin(day*.17)*.03+(stock=='B')*.002})
    frame=pl.DataFrame(rows);cfg={'training_calendar_window':252,'target':'y_ret_20mean','label_horizon_trading_days':20}
    controls=[]
    for cutoff in (1,19,251,252,253,301,401):
        past=[r for r in rows if r['is_train'] and r['trade_date']<cutoff]
        calendar=sorted({r['trade_date'] for r in past});positions={d:i for i,d in enumerate(calendar)};window=set(calendar[-252:]);expected=[]
        for stock in ('A','B'):
            stockrows=sorted([r for r in past if r['ts_code']==stock],key=lambda r:r['trade_date'])
            for i,origin in enumerate(stockrows):
                if i+20>=len(stockrows):continue
                end=stockrows[i+20]['trade_date'];values=[r['y_ret_1d'] for r in stockrows[i:i+20]]
                if origin['trade_date'] not in window or not origin['price_valid'] or not all(math.isfinite(x) for x in values) or positions[end]-positions[origin['trade_date']]!=20:continue
                expected.append((origin['trade_date'],stock,end,math.fsum(values)/20.))
        expected.sort();actual=population.training_frame(frame.lazy(),cutoff,cfg).select('trade_date','ts_code','label_end_20d','y_ret_20mean').collect().rows()
        assert len(actual)==len(expected)
        error=0.
        for actualrow,expectedrow in zip(actual,expected):
            assert actualrow[:3]==expectedrow[:3]
            error=max(error,abs(actualrow[3]-expectedrow[3]));assert abs(actualrow[3]-expectedrow[3])<1e-14
        poisoned=frame.with_columns(pl.when(pl.col('trade_date')>=cutoff).then(pl.lit(float('inf'))).otherwise(pl.col('y_ret_1d')).alias('y_ret_1d'))
        baseline=population.training_frame(frame.lazy(),cutoff,cfg).collect();replayed=population.training_frame(poisoned.lazy(),cutoff,cfg).collect()
        assert baseline.equals(replayed)
        assert not actual or max(r[2] for r in actual)<cutoff
        controls.append({'cutoff':cutoff,'rows':len(actual),'independent_origin_stock_and_mature20_end_exact':True,'max_target_fsum_error':error,'after_cutoff_poison_full_frame_exact':True,'training_calendar_window':252})
    create(A/'recent252_forward20_mature_population_actual_CPU_controls_v1_20261010.json',{'status':'passed7_joint_recent252_calendar_and_mean20_strict_maturity_independent_CPU_cases','records':controls,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(population.__file__),A/'forward20_mature_training_labels_v1_20261010.py']},'GPU_training_and_official_scores_pending':True,'test_X_read':False,'test_labels_read':False,'new_native_fits':0,'new_quality_scores':0})
    print({'actual_independent_CPU_cases':len(controls),'last_case_rows':controls[-1]['rows'],'largest_target_fsum_error':max(r['max_target_fsum_error'] for r in controls)},flush=True)
if __name__=='__main__':main()
