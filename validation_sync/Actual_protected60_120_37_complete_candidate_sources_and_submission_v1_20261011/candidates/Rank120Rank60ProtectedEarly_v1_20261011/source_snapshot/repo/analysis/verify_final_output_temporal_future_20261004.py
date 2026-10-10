"""Test preset final-output temporal branches on frozen future forecasts, without scores."""
from pathlib import Path
from datetime import datetime
import hashlib
import importlib.util
import json
import shutil
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
OUT=ROOT/'analysis/final_output_temporal_future_qa_20261004'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path,value):
    assert not path.exists();path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    from final_output_temporal_postprocessing_20261004 import transform
    import return_mapping
    from return_mapping import apply_mapping,daily_percentile
    preflight=ROOT/'analysis/final_output_temporal_preflight_20261004/verification.json'
    proof=read(preflight);assert proof['status']=='passed'
    for path,digest in proof['source_sha256'].items():assert sha(Path(path))==digest,path
    source=ROOT/'candidates/optimization_20261003_r25';verification=read(source/'verification.json');manifest=read(source/'manifest.json')
    assert verification['status']=='passed' and sha(source/'rank_prediction.npy')==manifest['files']['rank_prediction.npy']['sha256']
    inputs=ROOT/'deliveries/connected_topk0175_20261003/generation_inputs.parquet'
    mapping_path=ROOT/'analysis/optimization_20261003_r25/future_return_mapping.json'
    core=ROOT/'analysis/final_output_temporal_postprocessing_20261004.py'
    configs={'rank_ema':{'alpha':.9,'mix':.1,'power':1.},'curved_ema':{'alpha':.995,'mix':.025,'power':2.}}
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    sources=[Path(__file__),core,preflight,source/'rank_prediction.npy',source/'verification.json',source/'manifest.json',inputs,mapping_path,
        ROOT/'analysis/connected_validation_20261002/optimize_wave15.py',Path(return_mapping.__file__)]
    dump(OUT/'diagnostic_frozen_before_inference.json',{'status':'frozen_implementation_control','configurations':configs,
        'closed_complete_forecast_source':str(source),'mapping_scope':'FrozenR25 past-trained mapping used only to verify output mechanics; each actual selected variant requires its own past-OOF calibration.',
        'official_scores_generated':0,'new_model_selection':False,'test_labels_read':False,
        'frozen_at_local':datetime.now().isoformat(timespec='seconds'),'source_sha256':{str(p.resolve()):sha(p) for p in sources}})
    frame=pl.read_parquet(inputs,columns=['ts_code','trade_date','price_valid'])
    assert len(frame)==1599600 and frame['trade_date'].n_unique()==344
    raw=np.load(source/'rank_prediction.npy');dates=frame['trade_date'].to_numpy();valid=frame['price_valid'].to_numpy()
    symbols=frame['ts_code'].to_numpy();codes=pd.factorize(symbols,sort=True)[0];mapping=read(mapping_path)
    checks={}
    for name,cfg in configs.items():
        folder=OUT/name;folder.mkdir(exist_ok=True);shutil.copyfile(core,folder/core.name)
        spec=importlib.util.spec_from_file_location('copied_final_temporal_'+name,folder/core.name)
        copied=importlib.util.module_from_spec(spec);spec.loader.exec_module(copied)
        pred=transform(raw,dates,valid,codes,cfg);replayed=copied.transform(raw,dates,valid,codes,cfg)
        assert np.array_equal(pred,replayed)
        pct=daily_percentile(frame.select('trade_date').to_pandas(),pred);mapped=apply_mapping(mapping,pct)
        assert np.array_equal(pct,daily_percentile(frame.select('trade_date').to_pandas(),mapped))
        sub=frame.select('ts_code','trade_date').with_columns(pl.Series('pred',mapped));csv=folder/'submission.csv'
        sub.write_csv(csv,float_precision=17);parsed=pd.read_csv(csv,dtype={'ts_code':str},float_precision='round_trip')
        assert len(parsed)==1599600 and not parsed.duplicated(['ts_code','trade_date']).any() and not parsed.isna().any().any()
        assert np.isfinite(parsed['pred']).all()
        assert np.array_equal(parsed.groupby('trade_date')['pred'].rank().to_numpy(),pd.Series(mapped).groupby(parsed.trade_date.to_numpy()).rank().to_numpy())
        replay_pct=daily_percentile(frame.select('trade_date').to_pandas(),replayed);replay_mapped=apply_mapping(mapping,replay_pct)
        assert frame.select('ts_code','trade_date').with_columns(pl.Series('pred',replay_mapped)).write_csv(float_precision=17).encode('utf-8')==csv.read_bytes()
        last=int(frame['trade_date'].unique().sort()[79]);prefix=dates<=last
        prefix_codes=pd.factorize(symbols[prefix],sort=False)[0]
        assert np.array_equal(pred[prefix],copied.transform(raw[prefix],dates[prefix],valid[prefix],prefix_codes,cfg))
        assert np.array_equal(pred[~valid],raw[~valid])
        np.save(folder/'rank_prediction.npy',pred);dump(folder/'configuration.json',cfg)
        check={'status':'passed','rows':len(frame),'days':344,'validation_score':None,'copied_code_replay_bit_identical':True,
            'csv_replay_byte_identical':True,'csv_ranks_unchanged':True,'cold_first80_day_prefix_bit_identical':True,
            'test_labels_read':False,'csv_sha256':sha(csv),'rank_prediction_sha256':sha(folder/'rank_prediction.npy')}
        dump(folder/'verification.json',check);checks[name]=check
    dump(OUT/'verification.json',{'status':'passed','branches':checks,'copied_code_runs_with_frozen_project_daily_rank_dependency':True,
        'rows_per_branch':1599600,'actual_validation_score_not_generated':True,'new_model_scores':0,'test_labels_read':False,
        'diagnostic_freeze_sha256':sha(OUT/'diagnostic_frozen_before_inference.json'),'verified_at_local':datetime.now().isoformat(timespec='seconds')})
    print('Both final-output temporal future controls passed; no test scores or model selection.',flush=True)


if __name__=='__main__':main()
