"""Independent scalar ten-day means and tied cross-sectional ranks; no GPU or score."""
from pathlib import Path
import sys,math
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha

def main():
    import polars as pl
    import recent252_rank10_mature_training_population_v2_20261011 as population
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed();rows=[]
    for j,stock in enumerate(('A','B','C','D')):
        for day in range(1,421):
            if stock=='B' and day in (44,111,276):continue
            rows.append({'ts_code':stock,'trade_date':day,'is_train':not(stock=='B' and day==173),'price_valid':day%29!=0,
                'y_ret_1d':float('nan') if stock=='A' and day==138 else ((day%7)+(j//2))*10/1024.})
    frame=pl.DataFrame(rows);cfg={'training_calendar_window':252,'target':'y_rank_10mean','label_horizon_trading_days':10};controls=[]
    for cutoff in (1,9,10,11,253,301,401):
        past=[r for r in rows if r['is_train'] and r['trade_date']<cutoff];calendar=sorted({r['trade_date'] for r in past});positions={d:i for i,d in enumerate(calendar)};window=set(calendar[-252:]);raw=[]
        for stock in ('A','B','C','D'):
            own=sorted([r for r in past if r['ts_code']==stock],key=lambda r:r['trade_date'])
            for i,origin in enumerate(own):
                if i+10>=len(own):continue
                end=own[i+10]['trade_date'];values=[r['y_ret_1d'] for r in own[i:i+10]]
                if not origin['price_valid'] or not all(math.isfinite(x) for x in values) or positions[end]-positions[origin['trade_date']]!=10:continue
                raw.append((origin['trade_date'],stock,end,math.fsum(values)/10.))
        expected=[];ties=0
        for day,stock,end,target in raw:
            if day not in window:continue
            values=[r[3] for r in raw if r[0]==day];less=sum(v<target for v in values);equal=sum(v==target for v in values)
            rank=(less+(equal+1)/2.)/len(values);ties+=equal>1
            expected.append((day,stock,end,target,rank))
        expected.sort();actual=population.training_frame(frame.lazy(),cutoff,cfg).select('trade_date','ts_code','label_end_10d','y_ret_10mean','y_rank_10mean').collect().rows()
        assert actual==expected,(cutoff,len(actual),len(expected))
        poisoned=frame.with_columns(pl.when(pl.col('trade_date')>=cutoff).then(float('inf')).otherwise(pl.col('y_ret_1d')).alias('y_ret_1d'))
        baseline=population.training_frame(frame.lazy(),cutoff,cfg).collect();assert baseline.equals(population.training_frame(poisoned.lazy(),cutoff,cfg).collect())
        assert not actual or max(r[2] for r in actual)<cutoff
        controls.append({'cutoff':cutoff,'rows':len(actual),'scalar_mean_and_tied_rank_exact':True,'tied_rank_rows':ties,'future_poison_full_frame_identical':True})
    assert controls[-1]['tied_rank_rows']>0
    create(A/'recent252_rank10_mature_population_actual_CPU_controls_v2_20261011.json',{'status':'passed7_independent_mean10_tied_daily_rank_and_recent252_maturity_CPU_controls','records':controls,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(population.__file__),A/'forward10_mature_training_labels_v2_20261011.py']},'new_native_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False})
    print({'actual_rank10_scalar_cases':7,'last_rows':controls[-1]['rows'],'tied_rank_rows':controls[-1]['tied_rank_rows']},flush=True)
if __name__=='__main__':main()
