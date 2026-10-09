"""Independent scalar EMA and actual complete-OOF prefix/stock-ID controls."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import rankdata
from final_output_temporal_postprocessing_20261004 import transform
OUT=ROOT/'analysis/final_output_temporal_preflight_20261004'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def independent(raw,dates,valid,symbols,cfg):
    result=raw.copy();state={}
    for date in np.unique(dates):
        rows=np.flatnonzero((dates==date)&valid)
        ranks=rankdata(raw[rows],method='average')/len(rows)
        for row,value in zip(rows,ranks):
            now=float(value)**cfg['power'];symbol=symbols[row]
            updated=now if symbol not in state else cfg['alpha']*now+(1.-cfg['alpha'])*state[symbol]
            result[row]=(1.-cfg['mix'])*now+cfg['mix']*updated;state[symbol]=updated
    return result


def main():
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    rng=np.random.default_rng(20261004);count=11;days=np.arange(16)
    dates=np.repeat(days,count);symbols=np.tile(np.array([f'C{i:02}' for i in range(count)]),len(days))
    raw=rng.integers(-5,6,len(dates)).astype(np.float64);valid=rng.random(len(dates))>.12
    codes=pd.factorize(symbols,sort=True)[0];controls=[]
    for alpha,power,mix in ((.5,.5,.25),(.9,1.,1.),(.995,2.,.025)):
        cfg={'alpha':alpha,'power':power,'mix':mix};actual=transform(raw,dates,valid,codes,cfg)
        ref=independent(raw,dates,valid,symbols,cfg);error=float(np.max(np.abs(actual-ref)));assert error<1e-14
        for day in (1,7,12):
            prefix=dates<day;remapped=pd.factorize(symbols[prefix],sort=False)[0]
            assert np.array_equal(actual[prefix],transform(raw[prefix],dates[prefix],valid[prefix],remapped,cfg))
        # New future symbols can renumber all earlier code IDs without changing outputs.
        future_symbols=np.r_[symbols,np.array(['A_NEW','Z_NEW'])];future_dates=np.r_[dates,[16,16]]
        all_codes=pd.factorize(future_symbols,sort=True)[0]
        full=transform(np.r_[raw,[2.,3.]],future_dates,np.r_[valid,[True,True]],all_codes,cfg)
        assert np.array_equal(full[:len(raw)],actual)
        controls.append({'configuration':cfg,'independent_scalar_max_abs_error':error,'new_future_symbols_and_cold_prefix_bit_identical':True})
    source=ROOT/'analysis/optimization_20261003_r25/selected_validation.npy'
    frame_path=ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet'
    frame=pl.read_parquet(frame_path,columns=['ts_code','trade_date','price_valid'])
    raw=np.load(source);assert len(raw)==len(frame)==5635800 and frame['trade_date'].n_unique()==1212
    dates=frame['trade_date'].to_numpy();valid=frame['price_valid'].to_numpy();symbols=frame['ts_code'].to_numpy();codes=pd.factorize(symbols,sort=True)[0]
    assert np.array_equal(raw,transform(raw,dates,valid,codes,{'alpha':.9,'mix':0.,'power':1.}))
    assert np.array_equal(raw,transform(raw,dates,valid,codes,{'alpha':1.,'mix':.25,'power':1.}))
    actual_controls=[]
    for alpha,power,mix in ((.5,.5,.25),(.9,1.,.1),(.995,2.,.025)):
        cfg={'alpha':alpha,'power':power,'mix':mix};pred=transform(raw,dates,valid,codes,cfg)
        for days in (80,260):
            last=frame['trade_date'].unique().sort()[days-1];prefix=dates<=last
            remapped=pd.factorize(symbols[prefix],sort=False)[0]
            assert np.array_equal(pred[prefix],transform(raw[prefix],dates[prefix],valid[prefix],remapped,cfg))
        assert np.array_equal(pred[~valid],raw[~valid])
        actual_controls.append({'configuration':cfg,'full_validation_rows':len(raw),'cold_complete_day_prefixes':[80,260],
            'prefix_remapped_stock_ids_bit_identical':True,'invalid_current_price_forecasts_preserved':True})
    paths=[Path(__file__),ROOT/'analysis/final_output_temporal_postprocessing_20261004.py',ROOT/'analysis/connected_validation_20261002/optimize_wave15.py',source,frame_path]
    result={'status':'passed','verified_at_local':datetime.now().isoformat(timespec='seconds'),'synthetic_controls':controls,
        'actual_complete_output_controls':actual_controls,'identity_branch_bit_identical':True,
        'only_prediction_date_validity_and_symbol_inputs':True,'no_label_inputs':True,'new_model_scores':0,'test_labels_read':False,
        'source_sha256':{str(p.resolve()):sha(p) for p in paths}}
    (OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Final-output temporal controls passed: independent scalar EMA andfull5.6m-row prefixes.',flush=True)


if __name__=='__main__':main()
