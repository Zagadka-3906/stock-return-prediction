"""Check the historical fitter control, actual fit targets, padding and causality."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import train_neural_tuning_bank_20261004 as bank


def main():
    import numpy as np
    import polars as pl
    import torch
    out=bank.PREFLIGHT.parent
    if bank.PREFLIGHT.exists():
        proof=bank.read(bank.PREFLIGHT)
        assert proof['status']=='passed'
        for path,digest in proof['input_sha256'].items():assert bank.sha(path)==digest,path
        return
    features=bank.engine.feature_names();cfg={**bank.CONTROL,'epochs':1}
    past=bank.engine.training_frame(pl.scan_parquet(bank.engine.FEATURE_FILE),bank.engine.fold_cutoff(2020),cfg).select(bank.engine.KEYS+features+['y_rank']).sort('trade_date','ts_code').head(4096).collect()
    x=bank.engine.to_matrix(past,features);y=past['y_rank'].to_numpy()
    old=bank.original_fit_arrays(x,y,cfg);control=bank.engine.fit_arrays(x,y,cfg)
    assert all(torch.equal(old['state'][k],control['state'][k]) for k in old['state'])
    for field in ('mean','scale','training_losses'):assert np.array_equal(old[field],control[field]),field
    assert np.array_equal(bank.engine.predict_arrays(old,x),bank.engine.predict_arrays(control,x))
    assert control['actual_fit_target_sha256']==bank.engine.array_hash(y.astype(np.float32)-.5)
    rng=np.random.default_rng(20261004)
    probe=rng.normal(size=(32781,len(features))).astype(np.float32);probe[::31,::5]=np.nan
    checks={}
    for name,config in bank.CONFIGS.items():
        bundle=bank.engine.fit_arrays(x,y,{**config,'epochs':1})
        expected=y.astype(np.float32)+config['rank_training_offset']
        assert bundle['actual_fit_target_sha256']==bank.engine.array_hash(expected),name
        assert bundle['actual_fit_target_mean']==float(expected.mean(dtype=np.float64))
        full=bank.engine.predict_arrays(bundle,probe)
        for n in (1,80,32767,32768):assert np.array_equal(full[:n],bank.engine.predict_arrays(bundle,probe[:n])),(name,n)
        checks[name]={'status':'passed','actual_fit_target_sha256':bundle['actual_fit_target_sha256'],
                     'actual_fit_target_mean':bundle['actual_fit_target_mean'],
                     'rank_training_offset':config['rank_training_offset'],'learning_rate':config['learning_rate'],
                     'prefix_lengths':[1,80,32767,32768],'padded_prefix_bit_identical':True}
    boundary=bank.engine.boundary_control(2020,bank.CONTROL,features)
    paths=[Path(__file__),Path(bank.__file__),bank.SOURCE,ROOT/'analysis/neural_tuning_model_sources_20261004.py',
           bank.engine.FEATURE_FILE,bank.engine.MANIFEST]
    bank.dump(bank.PREFLIGHT,{'status':'passed','historical_fitter_control_state_bit_identical':True,
              'historical_fitter_control_predictions_bit_identical':True,'real_past_control_rows':len(past),
              'actual_float32_target_checks':checks,'future_label_poison_control':boundary,
              'test_data_read':False,'model_quality_evaluated':False,
              'input_sha256':{str(p.resolve()):bank.sha(p) for p in paths}},immutable=True)
    bank.log('Neural target-offset/lr preflight passed: exact baseline control, actual targets and padded prefixes')


if __name__=='__main__':main()
