"""Verify complete-output role augmentation, membership and new raw-model prefixes."""
from copy import deepcopy
from pathlib import Path
import numpy as np
from optimize_training_round37 import OUT,FOUNDATION,NEW_MODELS,ROLES,YEARS,Context,baseline,prefix_controls,dump,sha,log,trainer
from finalize_training_round37 import ReleaseContext,selected


def main():
    import polars as pl
    from run import FEATURE_FILE,feature_names,to_matrix
    from return_mapping import top_sets
    winner=selected()['winner'];ctx=ReleaseContext(winner);promote=ctx.promote('baseline')
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    cases=[winner];memberships=[];foundation=np.load(FOUNDATION/'selected_validation.npy');base=baseline()
    initial=top_sets(ctx.pdf,foundation)
    for role,name in zip(ROLES,NEW_MODELS):
        cfg=deepcopy(base);cfg['catboost_tuning_augmentation'][role]={'model':name,'weight':.075};cases.append(cfg)
    controls=[prefix_controls(ctx,cfg) for cfg in cases]
    for name,role in ((name,role) for name in NEW_MODELS for role in ('top','rest')):
        cfg=deepcopy(base);cfg['catboost_tuning_augmentation'][role]={'model':name,'weight':.075};ctx.configure(cfg)
        fresh,_=ctx.predict(ctx.donor(promote),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
        assert top_sets(ctx.pdf,fresh)==initial
        memberships.append({'model':name,'role':role,'foundation_top_sets_identical_every_day':True})
    inference=[];features=feature_names()
    for name in NEW_MODELS:
        for year in (2024,):
            info=trainer.read(trainer.source_dir(name)/f'info_{year}.json');bundle=trainer.load_bundle(trainer.model_path(name,year))
            prefix=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).sort('trade_date','ts_code').collect()
            last=int(prefix['trade_date'].unique().sort()[7]);prefix=prefix.filter(pl.col('trade_date')<=last)
            raw=trainer.predict_arrays(bundle,to_matrix(prefix,features),dates=prefix['trade_date'].to_numpy(),valid=prefix['price_valid'].to_numpy());raw[~prefix['price_valid'].to_numpy()]=-1e6
            cached=pl.read_parquet(trainer.source_dir(name)/f'raw_{year}.parquet').head(len(prefix))
            assert cached.select(['ts_code','trade_date']).equals(prefix.select(['ts_code','trade_date'])) and np.array_equal(cached['pred_raw'].to_numpy(),raw)
            inference.append({'model':name,'year':year,'complete_8_day_raw_inference_prefix_bit_identical':True,'last_label_end':info['training_meta']['last_label_end']})
    dump(OUT/'catboost_tuning_role_causal_checks.json',{'status':'passed','controls':controls,'ordering_only_membership_controls':memberships,
         'new_raw_model_inference_prefix_controls':inference,'selected_output_bit_identical':True,
         'new_scored_records':0,'test_data_read':False,'verification_script_sha256':sha(Path(__file__))},immutable=True)
    log('Round37 complete-output membership, raw inference, poisoned labels and prefixes passed')


if __name__=='__main__':main()
