"""Reproduce all15 frozen percentile models from complete-day raw-feature inputs."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import linear_model_sources_with_inputs_20261004 as route
import train_cross_section_bank_20261003 as cross
from run import FEATURE_FILE,feature_names,to_matrix


def main():
    import numpy as np
    import polars as pl
    controls=[];features=feature_names()
    for year in route.YEARS:
        frame=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(['ts_code','trade_date']+features+['price_valid']).sort('trade_date','ts_code').collect()
        last=int(frame['trade_date'].unique().sort()[79]);frame=frame.filter(pl.col('trade_date')<=last)
        x=to_matrix(frame,features);dates=frame['trade_date'].to_numpy();valid=frame['price_valid'].to_numpy()
        for name in cross.CONFIGS:
            path=route.model_path(name,year);bundle=route.load_bundle(path)
            assert bundle['current_day_percentile_input']
            pred=route.predict_arrays(bundle,x,dates=dates,valid=valid);pred[~valid]=-1e6
            expected=pl.read_parquet(route.source_dir(name)/f'raw_{year}.parquet').filter(pl.col('trade_date')<=last)
            assert expected.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
            assert np.array_equal(pred,expected['pred_raw'].to_numpy()),(name,year)
            original=cross.predict_arrays(cross.load_bundle(path),x,dates=dates,valid=valid);original[~valid]=-1e6
            assert np.array_equal(pred,original)
            controls.append({'model':name,'year':year,'days':80,'rows':len(frame),'cached_oof_and_original_cross_section_inference_bit_identical':True})
            print(f'Current-day input loader: {name},fold{year}, actual inference exact',flush=True)
    for name in ('rank512_e32','rank_ridge_l01','cat_rank6_e600','nn512_all4_rankmean'):
        bundle=route.load_bundle(route.model_path(name,2024));assert not bundle.get('current_day_percentile_input',False)
    sources=[Path(__file__),ROOT/'analysis/causal_model_loading_20261004.py',Path(route.__file__),Path(cross.__file__)]
    route.dump(ROOT/'analysis/current_day_input_loading_qa_20261004/verification.json',
         {'status':'passed','verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'controls':controls,
          'other_model_families_do_not_receive_extra_preprocessing':True,'test_data_read':False,'new_official_scores':0,
          'input_sha256':{str(p.resolve()):route.sha(p) for p in sources}},immutable=True)


if __name__=='__main__':main()
