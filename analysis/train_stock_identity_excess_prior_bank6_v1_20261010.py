"""Actual six cheap identity-prior fits, full OOF independent lookups and mature boundaries."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,gc
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
import stock_identity_excess_return_prior_native_v1_20261010 as native
OUT=Path('E:/赛题五_本机临时/stock_identity_excess_prior_bank6_v1_20261010')

def allowed():
    now=datetime.now(timezone(timedelta(hours=8)))
    for name in ('current_user_runtime_control_20261009.json','current_user_runtime_control_20261010.json'):
        c=read(A/name)
        assert c['status']=='optimization_active_after_explicit_manual_resume' and now<datetime.fromisoformat(c['stop_at_local'])

def main():
    import numpy as np,polars as pl,joblib
    from run import FEATURE_FILE,fold_cutoff
    allowed();assert not OUT.exists();OUT.mkdir()
    paths=[Path(__file__),Path(native.__file__),A/'stock_identity_excess_prior_actual_CPU_controls_v1_20261010.json',ROOT/'run.py',ROOT/'后续选模标准.md',FEATURE_FILE,A/'connected_validation_20261002/combined_fold_frame.parquet']
    pins={str(p):sha(p) for p in paths}
    assert len(read(paths[2])['records'])==4
    create(OUT/'protocol.json',{'status':'frozen_before_all6_fits_and_any_official_score','input_sha256':pins,'config':native.CONFIG,'annual_model_years':list(range(2020,2026)),'independent_fit_tolerance':1e-14,'native_lookup_vs_sorted_lookup_bits_required':True,'test_labels_read':False,'future_X_read':False})
    lazy=pl.scan_parquet(FEATURE_FILE);days=lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    oof=pl.read_parquet(paths[-1],columns=['ts_code','trade_date']);records=[];parts=[]
    exact=lambda x,y:np.array_equal(x.view('u8'),y.view('u8'))
    for year in range(2020,2026):
        allowed();cutoff=fold_cutoff(year);folder=OUT/str(year);folder.mkdir()
        frame=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)).select(['ts_code','trade_date','is_train','price_valid','y_ret_1d']).collect()
        selected=native.population(frame,cutoff)
        last=int(selected['trade_date'].max());end=int(days[np.searchsorted(days,last)+1]);assert last<cutoff and end<=cutoff
        create(folder/'frozen_before_fit.json',{'year':year,'cutoff_exclusive':cutoff,'last_label_end':end,'mature_rows':len(selected),'selected_keys_sha256':__import__('hashlib').sha256(selected.select(['ts_code','trade_date']).hash_rows(seed=2026).to_numpy().tobytes()).hexdigest()})
        bundle=native.fit(frame,cutoff);bundle['year']=year
        pd=selected.to_pandas();pd['r']=pd['y_ret_1d'].clip(-.1,.1);pd['excess']=pd['r']-pd.groupby('trade_date')['r'].transform('mean')
        sums=pd.groupby('ts_code')['excess'].agg(['sum','count']);oracle=(sums['sum']/(sums['count']+252.)).reindex(bundle['codes']).to_numpy()
        error=float(np.max(np.abs(oracle-bundle['alpha'])));assert error<1e-14
        joblib.dump(bundle,folder/'model.joblib',compress=0);reloaded=joblib.load(folder/'model.joblib')
        fixture=list(reversed(bundle['codes']))+['UNSEEN_STOCK'];raw=native.predict(bundle,fixture)
        assert exact(raw,native.independent_predict(reloaded,fixture)) and exact(raw,native.predict(reloaded,fixture))
        row={'year':year,'mature_rows':bundle['training_rows'],'cutoff_exclusive':cutoff,'last_training_date':last,'last_label_end':end,'independent_Pandas_fit_max_absolute_error':error,'independent_saved_lookup_and_reload_bits_exact':True,'unseen_stock_zero':raw[-1]==0.,'model_sha256':sha(folder/'model.joblib')}
        if year<2025:
            keys=oof.filter(pl.col('trade_date')//10000==year);codes=keys['ts_code'].to_list();value=native.predict(reloaded,codes)
            independent=native.independent_predict(reloaded,codes);assert exact(value,independent)
            prefixes=[]
            for count in (80,160,260):
                n=min(count*4650,len(keys));assert exact(value[:n],native.predict(reloaded,codes[:n])) and exact(value[:n],native.independent_predict(reloaded,codes[:n]))
                prefixes.append({'prefix_days':count,'rows':n,'native_and_independent_bits_exact':True})
            part=keys.with_columns(pl.Series('pred_raw',value));part.write_parquet(folder/'raw.parquet');parts.append(part)
            row.update(rows=len(keys),prefixes=prefixes,full_independent_bits_exact=True,raw_sha256=sha(folder/'raw.parquet'))
        create(folder/'info.json',row);records.append(row)
        print({'year':year,'mature_rows':len(selected),'fit_oracle_error':error,'status':'passed_actual_fit_and_own_independent_controls'},flush=True)
        del frame,selected,pd,sums,oracle,bundle,reloaded;gc.collect()
    combined=pl.concat(parts);assert combined.select(['ts_code','trade_date']).equals(oof)
    assert [len(combined),combined['trade_date'].n_unique(),combined['ts_code'].n_unique()]==[5635800,1212,4650]
    combined.write_parquet(OUT/'combined_raw.parquet')
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual6_mature_identity_prior_fits5_full_independent_OOF_and15_prefixes','input_sha256':pins,'records':records,'actual_native_fits':6,'rows_days_stocks':[5635800,1212,4650],'actual_full_independent_OOF_cases':5,'actual_cold_prefix_cases':15,'combined_raw_sha256':sha(OUT/'combined_raw.parquet'),'future_X_read':False,'test_labels_read':False,'quality_scores':0,'not_future_submission_qualified':True})
    create(A/'actual_stock_identity_excess_prior_bank6_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
