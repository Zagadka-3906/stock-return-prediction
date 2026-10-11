"""Real tiny fit checks against an independent scalar mathematical oracle."""
from pathlib import Path
import sys,math
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
import stock_identity_excess_return_prior_native_v1_20261010 as native

def main():
    import numpy as np,polars as pl
    records=[]
    for count in (1,2,5,19):
        rows=[{'ts_code':f'S{i}','trade_date':20200101+d,'is_train':True,'price_valid':(i+d)%7!=0,'y_ret_1d':(-1.)**i*(i+d+1)/100.} for d in range(8) for i in range(count)]
        rows.append({'ts_code':'Z','trade_date':20200120,'is_train':True,'price_valid':True,'y_ret_1d':10.})
        frame=pl.DataFrame(rows);bundle=native.fit(frame,20200109)
        past=[r for r in rows if r['trade_date']<20200109 and r['price_valid']]
        means={d:math.fsum(max(-.1,min(.1,r['y_ret_1d'])) for r in past if r['trade_date']==d)/sum(r['trade_date']==d for r in past) for d in set(r['trade_date'] for r in past)}
        for code,value in zip(bundle['codes'],bundle['alpha']):
            own=[max(-.1,min(.1,r['y_ret_1d']))-means[r['trade_date']] for r in past if r['ts_code']==code]
            assert abs(float(value)-math.fsum(own)/(len(own)+252.))<1e-14
        codes=['missing',*reversed(bundle['codes']),*bundle['codes']]
        exact=lambda x,y:np.array_equal(x.view('u8'),y.view('u8'))
        actual=native.predict(bundle,codes);assert exact(actual,native.independent_predict(bundle,codes))
        assert actual[0]==0.
        poisoned=frame.with_columns(pl.when(pl.col('trade_date')>=20200109).then(float('nan')).otherwise(pl.col('y_ret_1d')).alias('y_ret_1d'))
        alternate=native.fit(poisoned,20200109);assert exact(bundle['alpha'],alternate['alpha'])
        for n in (0,1,len(codes)):assert exact(actual[:n],native.independent_predict(bundle,codes[:n]))
        records.append({'stock_count':count,'scalar_fit_absolute_tolerance':1e-14,'independent_predict_and_prefix_bits_exact':True,'future_label_poison_fit_bits_exact':True,'unseen_stock_zero':True})
    out=A/'stock_identity_excess_prior_actual_CPU_controls_v1_20261010.json'
    create(out,{'status':'passed4_actual_independent_scalar_fit_lookup_prefix_and_future_poison_controls','records':records,'input_sha256':{str(p):sha(p) for p in (Path(__file__),Path(native.__file__))},'GPU_used':False,'annual_fits':0,'quality_scores':0})
    print('passed4 actual CPU stock identity prior controls',flush=True)
if __name__=='__main__':main()
