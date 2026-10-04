"""Audit selected role augmentation and fresh model inference prefixes."""
from copy import deepcopy
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import objective_model_sources_20261003 as trainer
from optimize_training_round17 import OUT,MODELS,NEW_MODELS,ROLES,YEARS,baseline,prefix_controls,dump,sha,log
from finalize_training_round17 import ReleaseContext,selected


def main():
    import numpy as np
    import polars as pl
    from run import FEATURE_FILE,feature_names,to_matrix
    winner=selected()['winner'];ctx=ReleaseContext(winner);promote=ctx.promote('baseline')
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    cases=[winner]
    for role,name in zip(ROLES,NEW_MODELS):
        cfg=deepcopy(baseline());cfg['diverse_augmentation'][role]={'model':name,'weight':.15};cases.append(cfg)
    controls=[prefix_controls(ctx,promote,cfg) for cfg in cases]
    model_checks=[];features=feature_names()
    for name in NEW_MODELS:
        for year in YEARS:
            info=trainer.read(trainer.OUT/name/f'info_{year}.json')
            bundle=trainer.load_bundle(trainer.OUT/name/f'model_{year}.joblib')
            prefix=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).sort('trade_date','ts_code').head(32781).collect()
            replay=trainer.predict_arrays(bundle,to_matrix(prefix,features),dates=prefix['trade_date'].to_numpy(),valid=prefix['price_valid'].to_numpy());replay[~prefix['price_valid'].to_numpy()]=-1e6
            cached=pl.read_parquet(trainer.OUT/name/f'raw_{year}.parquet').head(len(prefix))
            assert cached.select(['ts_code','trade_date']).equals(prefix.select(['ts_code','trade_date']))
            assert np.array_equal(cached['pred_raw'].to_numpy(),replay)
            model_checks.append({'model':name,'year':year,'rows':len(prefix),'raw_inference_prefix_bit_identical':True,
                                 'last_label_end':info['training_meta']['last_label_end']})
            del bundle,prefix,replay,cached
    dump(OUT/'diverse_augmentation_causal_checks.json',{'status':'passed','controls':controls,
         'new_model_inference_prefix_checks':model_checks,'selected_output_bit_identical':True,
         'test_data_read':False,'new_scored_records':0,'verification_script_sha256':sha(Path(__file__))},immutable=True)
    log('Round17 new model inference prefixes, role augmentation, poisoned labels and date prefixes passed')


if __name__=='__main__':main()
