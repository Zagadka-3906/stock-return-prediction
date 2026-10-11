"""Validate the actual portfolio bank functions without annual model or quality selection."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
OUT=ROOT/'analysis/portfolio_bank_implementation_preflight_20261004'

def main():
    import psutil
    while psutil.virtual_memory().available<8*2**30:time.sleep(10)
    import numpy as np
    import polars as pl
    import torch
    import train_portfolio_surrogate_bank_20261004 as bank
    OUT.mkdir(exist_ok=True)
    sources=[Path(__file__),Path(bank.__file__),Path(bank.proxy.__file__),bank.SOURCE,bank.PREFLIGHT,
        bank.engine.FEATURE_FILE,bank.engine.MANIFEST,ROOT/'evaluate.py',ROOT/'后续选模标准.md']
    for year in (*bank.YEARS,2025):
        sources.extend([bank.BASE/f'model_{year}.joblib',bank.BASE/f'info_{year}.json'])
        info=bank.read(bank.BASE/f'info_{year}.json')
        assert info['status']=='passed' and bank.sha(bank.BASE/f'model_{year}.joblib')==info['model_sha256']
    hashes={str(p.resolve()):bank.sha(p) for p in sources}
    bank.dump(OUT/'frozen_before_controls.json',{'status':'frozen_actual_bank_controls','input_sha256':hashes,
        'configurations':bank.CONFIGS,'controlled_fine_tuning_epochs':1,'new_quality_scores':0,
        'scope':'Actual two-date past-training pairs; not annual cross-validation or official quality scores.'},immutable=True)
    features=bank.engine.feature_names();lazy=pl.scan_parquet(bank.engine.FEATURE_FILE)
    columns=list(dict.fromkeys(bank.engine.KEYS+features+['y_rank','y_ret_1d','flag_limit_up','is_train','price_valid']))
    cutoff=bank.engine.fold_cutoff(2020)
    dates=bank.pool_filter(lazy,cutoff).select('trade_date').unique().sort('trade_date').head(2).collect()['trade_date'].to_list()
    past=bank.pool_filter(lazy,cutoff).filter(pl.col('trade_date').is_in(dates)).select(columns).sort('trade_date','ts_code').collect()
    boundaries={}
    for year in (*bank.YEARS,2025):
        edge=bank.engine.fold_cutoff(year)
        future=lazy.filter(pl.col('is_train')&(pl.col('trade_date')>=edge)).select(columns).head(16).collect()
        combined=pl.concat([past,future]);poison=combined.with_columns([
            pl.when(pl.col('trade_date')>=edge).then(pl.lit(12345.,dtype=combined.schema[c])).otherwise(pl.col(c)).alias(c)
            for c in ('y_rank','y_ret_1d')])
        assert bank.pool_filter(combined.lazy(),edge).collect().equals(bank.pool_filter(poison.lazy(),edge).collect())
        missing=combined.with_columns(pl.lit(float('nan')).alias('y_rank'),pl.lit(float('nan')).alias('y_ret_1d'))
        assert bank.pool_filter(combined.lazy(),edge).select(bank.engine.KEYS).collect().equals(bank.pool_filter(missing.lazy(),edge).select(bank.engine.KEYS).collect())
        boundaries[str(year)]={'cutoff_exclusive':edge,'actual_bank_pool_future_label_poisoning_unchanged':True,
            'actual_bank_pool_keys_independent_of_both_labels':True}
    frame=bank.pool_frame(2020);x=bank.engine.to_matrix(frame,features);rank=frame['y_rank'].to_numpy()
    supervised=np.isfinite(rank);info=bank.read(bank.BASE/'info_2020.json');meta=info['training_meta']
    assert int(supervised.sum())==meta['rows']
    for values,key in [(x,'training_matrix_sha256'),(rank,'training_target_sha256'),
        (frame.select(bank.engine.KEYS).hash_rows(seed=2026).to_numpy(),'training_keys_sha256')]:
        assert bank.subset_hash(values,supervised)==meta[key]
    import gc
    del frame,x,rank,supervised;gc.collect()
    x=bank.engine.to_matrix(past,features);bundle=bank.engine.load_bundle(bank.BASE/'model_2020.joblib')
    clean=np.clip((np.where(np.isfinite(x),x,bundle['mean'])-bundle['mean'])/bundle['scale'],-8,8).astype(np.float32)
    code_list=past['ts_code'].unique().sort().to_list()
    args=[past['trade_date'].to_numpy(),past['ts_code'].cast(pl.Enum(code_list)).to_physical().to_numpy(),
        past['flag_limit_up'].to_numpy(),past['y_rank'].to_numpy(),past['y_ret_1d'].to_numpy()]
    while psutil.virtual_memory().available<4*2**30:time.sleep(10)
    assert torch.cuda.is_available()
    zero=bank.fine_tune(bundle,clean,*args,dict(bank.COMMON,fine_tune_epochs=0))
    assert all(torch.equal(zero['state'][k],bundle['state'][k]) for k in bundle['state'])
    assert np.array_equal(bank.engine.predict_arrays(zero,x),bank.engine.predict_arrays(bundle,x))
    controls=[];first=None
    for name,cfg in bank.CONFIGS.items():
        started=time.monotonic();torch.cuda.reset_peak_memory_stats()
        actual=bank.fine_tune(bundle,clean,*args,dict(cfg,fine_tune_epochs=1))
        assert actual['fine_tuning_steps']==1 and np.isfinite(actual['fine_tuning_losses']).all()
        assert any(not torch.equal(actual['state'][k],bundle['state'][k]) for k in bundle['state'])
        assert np.array_equal(actual['mean'],bundle['mean']) and np.array_equal(actual['scale'],bundle['scale'])
        model=OUT/f'{name}.joblib';bank.engine.save_bundle(model,actual)
        full=bank.engine.predict_arrays(actual,x);replay=bank.engine.predict_arrays(bank.engine.load_bundle(model),x)
        assert np.array_equal(full,replay) and np.isfinite(full).all()
        for n in (1,80):assert np.array_equal(full[:n],bank.engine.predict_arrays(actual,x[:n]))
        if first is None:first=actual
        elif cfg['turnover_weight']>.0:
            assert any(not torch.equal(actual['state'][k],first['state'][k]) for k in first['state'])
        controls.append({'name':name,'fine_tuning_steps':1,'seconds_including_reload_andprefix':time.monotonic()-started,
            'training_proxy_loss':actual['fine_tuning_losses'][0],'own_peak_allocated_bytes':torch.cuda.max_memory_allocated(),
            'own_peak_reserved_bytes':torch.cuda.max_memory_reserved(),'model_sha256':bank.sha(model),
            'reload_andcold_prefix_bit_identical':True})
    for path,digest in hashes.items():assert bank.sha(path)==digest,path
    bank.dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':hashes,'warm_zero_step_weight_andprediction_identity':True,
        'actual_complete_2020_supervision_arrays_match_original_checkpoint_hashes':True,
        'actual_pool_boundary_controls':boundaries,'actual_two_date_rows':len(past),'controls':controls,
        'mature_normalizer_unchanged':True,'all_original_checkpoints_unchanged':True,
        'new_quality_scores':0,'official_scoring_calls':0,'test_labels_read':False,
        'scope':'Actual bank function controls on one mature pair plus complete supervised fold2020 input hashes. Annual fit quality andresource limits remain unmeasured.'},immutable=True)
    print('Actual portfolio bank implementation controls passed',flush=True)

if __name__=='__main__':main()
