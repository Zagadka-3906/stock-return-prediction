"""Verify parameter controls, original frozen inference and CPU label cutoffs."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import train_catboost_tuning_bank_20261004 as bank


def main():
    import numpy as np
    import polars as pl
    if bank.PREFLIGHT.exists():
        proof=bank.read(bank.PREFLIGHT);assert proof['status']=='passed'
        for path,digest in proof['input_sha256'].items():assert bank.sha(path)==digest,path
        return
    features=bank.engine.feature_names();rows={}
    for name,cfg in bank.CONFIGS.items():
        proof=bank.engine.boundary_control(2020,dict(cfg,task_type='CPU',iterations=8),features)
        proof.update(control_fit_device='CPU',gpu_retraining_bit_identity_not_claimed=True)
        rows[name]=proof
    frame=pl.scan_parquet(bank.engine.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==2024)).sort('trade_date','ts_code').select(bank.engine.KEYS+features+['price_valid']).head(32781).collect()
    x=bank.engine.to_matrix(frame,features);bundle=bank.engine.load_bundle(bank.BASELINE/'model_2024.joblib')
    raw=bank.engine.predict_arrays(bundle,x)
    for n in (1,80,32767,32768):assert np.array_equal(raw[:n],bank.engine.predict_arrays(bundle,x[:n])),n
    raw[~frame['price_valid'].to_numpy()]=-1e6
    cached=pl.read_parquet(bank.BASELINE/'raw_2024.parquet').head(len(frame))
    assert cached.select(bank.engine.KEYS).equals(frame.select(bank.engine.KEYS)) and np.array_equal(raw,cached['pred_raw'].to_numpy())
    sources=[Path(__file__),Path(bank.__file__),Path(bank.reference.__file__),bank.SOURCE,
             ROOT/'analysis/catboost_tuning_model_sources_20261004.py',
             bank.BASELINE/'model_2024.joblib',bank.BASELINE/'raw_2024.parquet',bank.BASELINE/'info_2024.json',
             bank.engine.FEATURE_FILE,bank.engine.MANIFEST]
    bank.dump(bank.PREFLIGHT,{'status':'passed','configuration_count':5,'controls':rows,
        'original_fitter_reused_without_changes':True,'original_frozen_baseline_inference_matches_oof_bit_identically':True,
        'baseline_rows':len(frame),'baseline_prefix_rows':[1,80,32767,32768],
        'gpu_refit_bit_deterministic':False,'test_data_read':False,'new_official_scores':0,
        'input_sha256':{str(p.resolve()):bank.sha(p) for p in sources}},immutable=True)
    bank.log('CatBoost tuning preflight passed: CPU maturity controls and original frozen inference')


if __name__=='__main__':main()
