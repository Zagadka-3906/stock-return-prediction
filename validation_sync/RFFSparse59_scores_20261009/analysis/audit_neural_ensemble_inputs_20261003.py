"""Explicit poisoned-label inference checks for the frozen ensemble bank, complete-date prefixes only."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import train_neural_ensemble_bank_20261003 as bank


def main():
    import numpy as np
    import polars as pl
    while not (bank.OUT/'oof_audit.json').exists():time.sleep(10)
    bank.verify();features=bank.feature_names();proofs=[]
    for year in bank.YEARS:
        source=pl.scan_parquet(bank.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year))
        last=source.select('trade_date').unique().sort('trade_date').head(80).collect()['trade_date'][-1]
        frame=source.filter(pl.col('trade_date')<=last).select(bank.KEYS+features+['price_valid','y_rank','y_ret_1d']).sort('trade_date','ts_code').collect()
        poison=frame.with_columns(pl.lit(float('nan')).alias('y_rank'),pl.lit(12345.).alias('y_ret_1d'))
        x=bank.to_matrix(frame,features);px=bank.to_matrix(poison,features)
        assert np.array_equal(x,px,equal_nan=True)
        dates=poison['trade_date'].to_numpy();valid=poison['price_valid'].to_numpy()
        for name in bank.CONFIGS:
            bundle=bank.load_bundle(bank.OUT/name/f'model_{year}.joblib')
            raw=bank.predict_arrays(bundle,px,dates=dates,valid=valid)
            cached=pl.read_parquet(bank.OUT/name/f'raw_{year}.parquet').head(len(frame))
            assert cached.select(bank.KEYS).equals(frame.select(bank.KEYS)) and np.array_equal(raw,cached['pred_raw'].to_numpy())
            proofs.append({'model':name,'year':year,'rows':len(frame),'complete_days':80,
                           'poisoned_labels_reloaded_inference_bit_identical':True,'aggregation_uses_complete_current_day_pool':True})
            bank.log(f'Ensemble input audit {name}/{year}: poisoned labels and complete80-day model replay passed')
    bank.dump(bank.OUT/'input_label_poisoning_audit.json',{'status':'passed','checks':proofs,
         'new_scored_records':0,'new_model_fits':0,'test_data_read':False,'bank_protocol_sha256':bank.sha(bank.OUT/'protocol.json'),
         'audit_script_sha256':bank.sha(Path(__file__))},immutable=True)


if __name__=='__main__':main()
