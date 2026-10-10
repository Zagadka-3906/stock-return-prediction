"""Independent Python calendar/population oracle and after-cutoff poisoning on CPU."""
from pathlib import Path
import sys,math
from datetime import datetime,timedelta
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
def main():
    import polars as pl
    import recent252_mature_training_population_v1_20261010 as helper
    rows=[];days=[int((datetime(2017,1,1)+timedelta(days=d)).strftime('%Y%m%d')) for d in range(402)]
    for day,date in enumerate(days):
        for code in ('A','B','C'):
            rows.append({'ts_code':code,'trade_date':date,'y_ret_1d':float('nan') if day%37==0 and code=='B' else .001*day,'is_train':code!='C' or day%13!=0,'price_valid':day%19!=0})
    frame=pl.DataFrame(rows);cfg={'target':'y_ret_1d','training_calendar_window':252};records=[]
    for index in (1,19,251,252,253,301,401):
        cutoff=days[index];past=[r for r in rows if r['is_train'] and r['trade_date']<cutoff]
        window=set(sorted({r['trade_date'] for r in past})[-252:])
        expected=sorted((r['trade_date'],r['ts_code']) for r in past if r['trade_date'] in window and r['price_valid'] and math.isfinite(r['y_ret_1d']))
        out=helper.training_frame(frame.lazy(),cutoff,cfg).collect()
        actual=list(zip(out['trade_date'].to_list(),out['ts_code'].to_list()));assert actual==expected
        poisoned=frame.with_columns(pl.when(pl.col('trade_date')>=cutoff).then(float('inf')).otherwise(pl.col('y_ret_1d')).alias('y_ret_1d'))
        assert out.equals(helper.training_frame(poisoned.lazy(),cutoff,cfg).collect())
        assert out['trade_date'].n_unique()<=252
        records.append({'cutoff':cutoff,'rows':len(out),'independent_population_exact':True,'future_label_poisoning_invariant':True})
    create(A/'recent252_mature_population_actual_CPU_controls_v1_20261010.json',{'status':'passed7_independent_recent252_calendar_population_and_future_label_poisoning_cases','records':records,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(helper.__file__)]},'actual_native_fits':0,'new_quality_scores':0,'GPU_used':False,'test_labels_read':False})
    print('PASS7 independent rolling252 population/cutoff/poison controls',flush=True)
if __name__=='__main__':main()
