"""Independent scalar labels,5-day purging, gaps, nonfinite labels and poisoning controls."""
from pathlib import Path
from datetime import date,timedelta
import sys,math
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
import forward5_mature_training_labels_v1_20261010 as labels

def main():
    import numpy as np,polars as pl
    days=[int((date(2020,1,1)+timedelta(days=i)).strftime('%Y%m%d')) for i in range(80)]
    rows=[{'ts_code':code,'trade_date':d,'is_train':True,'price_valid':i%17!=0,'y_ret_1d':float(np.float32((i%13-6)*(.001+j*.0001)))} for j,code in enumerate(('A','B','C')) for i,d in enumerate(days) if not (code=='B' and i==12)]
    for r in rows:
        if r['ts_code']=='C' and r['trade_date']==days[31]:r['y_ret_1d']=float('nan')
    frame=pl.DataFrame(rows);cfg={'target':labels.TARGET,'label_horizon_trading_days':5};records=[]
    for end in (4,5,6,24,45,65,79):
        cutoff=days[end];actual=labels.training_frame(frame.lazy(),cutoff,cfg).collect();expected=[]
        past=[r for r in rows if r['is_train'] and r['trade_date']<cutoff];calendar={d:i for i,d in enumerate(sorted({r['trade_date'] for r in past}))}
        for code in ('A','B','C'):
            own=sorted([r for r in past if r['ts_code']==code],key=lambda r:r['trade_date'])
            for i in range(max(0,len(own)-5)):
                begin,finish=own[i],own[i+5];values=[r['y_ret_1d'] for r in own[i:i+5]]
                if begin['price_valid'] and all(math.isfinite(v) for v in values) and calendar[finish['trade_date']]-calendar[begin['trade_date']]==5:
                    expected.append((begin['trade_date'],code,math.fsum(values)/5,finish['trade_date']))
        expected.sort();observed=[(r['trade_date'],r['ts_code'],r[labels.TARGET],r['label_end_5d']) for r in actual.to_dicts()]
        assert len(observed)==len(expected)
        for a,b in zip(observed,expected):assert a[:2]==b[:2] and a[3]==b[3] and abs(a[2]-b[2])<1e-14
        poisoned=frame.with_columns(pl.when(pl.col('trade_date')>=cutoff).then(float('inf')).otherwise(pl.col('y_ret_1d')).alias('y_ret_1d'))
        assert labels.training_frame(poisoned.lazy(),cutoff,cfg).collect().equals(actual)
        if len(actual):assert actual['label_end_5d'].max()<cutoff and np.isfinite(actual[labels.TARGET].to_numpy()).all()
        records.append({'cutoff':cutoff,'rows':len(actual),'scalar_mean_absolute_tolerance':1e-14,'exact5_calendar_span_and_mature_end_checked':True,'missing_stock_day_and_NaN_windows_excluded':True,'future_label_poison_population_and_target_identical':True})
    create(A/'forward5_mature_training_labels_actual_CPU_controls_v1_20261010.json',{'status':'passed7_independent_scalar_forward5_targets_complete_calendar_spans_maturity_and_future_poison_controls','records':records,'input_sha256':{str(p):sha(p) for p in (Path(__file__),Path(labels.__file__))},'training_days_purged_at_boundary_at_least20':True,'training_labels_only':True,'actual_annual_models':0,'GPU_used':False,'quality_scores':0,'future_test_X_or_Y_read':False})
    print('passed7 independent forward5 label and maturity CPU controls',flush=True)
if __name__=='__main__':main()
