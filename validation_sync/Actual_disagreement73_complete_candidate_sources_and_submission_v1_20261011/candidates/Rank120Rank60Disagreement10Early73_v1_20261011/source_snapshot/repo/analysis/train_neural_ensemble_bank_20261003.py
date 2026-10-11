"""Synthesize frozen seed ensembles and replay actual member models; no new OOF training."""
from pathlib import Path
import argparse
import os
import sys
import time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import neural_seed_model_sources_20261003 as members
from run import FEATURE_FILE,feature_names,to_matrix
OUT=ROOT/'analysis/neural_ensemble_bank_20261003'
read,dump,sha,log=members.read,members.dump,members.sha,members.log
YEARS=members.YEARS
KEYS=['ts_code','trade_date']
GROUPS={
    'nn512_three32':['rank512_e32','rank512_seed16_e32','rank512_seed17_e32'],
    'nn512_all4':['rank512_e32','rank512_seed16_e32','rank512_seed17_e32','rank512_seed18_e64'],
    'nn_capacity_all5':['rank512_e32','rank512_seed16_e32','rank512_seed17_e32','rank512_seed18_e64','rank1024_seed19_e32']}
CONFIGS={f'{group}_{mode}':{'kind':'neural_ensemble','target':'y_rank','members':names,'aggregation':mode,
                         'weights':[1/len(names)]*len(names)} for group,names in GROUPS.items() for mode in ('rawmean','rankmean')}


def aggregate(arrays,cfg,dates,valid):
    import numpy as np
    from optimize_wave15 import daily_ranks
    assert len(arrays)==len(cfg['weights']) and all(len(a)==len(dates)==len(valid) for a in arrays)
    if cfg['aggregation']=='rankmean':arrays=[daily_ranks(a,valid,dates) for a in arrays]
    else:assert cfg['aggregation']=='rawmean'
    result=sum(weight*array for weight,array in zip(cfg['weights'],arrays));result[~valid]=-1e6
    assert np.isfinite(result).all()
    return result


def predict_arrays(bundle,x,dates=None,valid=None):
    assert dates is not None and valid is not None,'Ensemble replay requires aligned dates and price validity'
    arrays=[members.predict_arrays(child,x,dates=dates,valid=valid) for child in bundle['member_bundles']]
    return aggregate(arrays,bundle['config'],dates,valid)


def load_bundle(path):return members.load_bundle(path)


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    members.verify();sources=[Path(__file__),Path(members.__file__),ROOT/'analysis/train_neural_seed_bank_20261003.py',
        ROOT/'analysis/train_neural_bank_20261003.py',ROOT/'analysis/train_diverse_backbones_20261003.py',
        ROOT/'analysis/catboost_model_sources_20261003.py',ROOT/'analysis/cross_section_model_sources_20261003.py',
        FEATURE_FILE,ROOT/'run.py',ROOT/'后续选模标准.md',ROOT/'analysis/neural_seed_bank_20261003/protocol.json',
        ROOT/'analysis/neural_seed_bank_20261003/oof_audit.json',ROOT/'analysis/neural_bank_20261003/protocol.json']
    for name in dict.fromkeys(name for names in GROUPS.values() for name in names):
        for year in YEARS:
            folder=members.source_dir(name)
            sources += [folder/f'model_{year}.joblib',folder/f'raw_{year}.parquet',folder/f'info_{year}.json']
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'configurations':CONFIGS,
         'features':feature_names(),'years':YEARS,'new_oof_model_training':False,'new_fold_models_trained':0,
         'ensemble_artifacts_expected':30,'method':'Equal member weights; raw-score mean or label-free current-date percentile mean. Keep invalid prices at the common sentinel.',
         'rank_pool':'Complete current-day price-valid forecast pool, never filter on label availability.',
         'causal_controls':'Poison labels; complete-date prefix assembly; actual reloaded child-model inference against assembled OOF.',
         'test_data_read':False,'input_sha256':{str(path.resolve()):sha(path) for path in dict.fromkeys(sources)}},immutable=True)
    log('Six neural seed ensembles frozen before any ensemble scores')


def train_one(name,year):
    import joblib
    import numpy as np
    import polars as pl
    verify();cfg=CONFIGS[name];folder=OUT/name;folder.mkdir(exist_ok=True)
    info_path=folder/f'info_{year}.json';model_path=folder/f'model_{year}.joblib';raw_path=folder/f'raw_{year}.parquet'
    if info_path.exists():
        info=read(info_path);assert sha(model_path)==info['model_sha256']
        if year<2025:assert sha(raw_path)==info['prediction_sha256']
        return info
    started=time.monotonic();infos={child:members.train_one(child,year) for child in cfg['members']}
    metas=[value['training_meta'] for value in infos.values()]
    for meta in metas:
        assert meta==metas[0] and meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
    bundle={'kind':'neural_ensemble','config':cfg,'member_bundles':[members.load_bundle(members.model_path(child,year)) for child in cfg['members']],
            'member_model_sha256':{child:info['model_sha256'] for child,info in infos.items()}}
    joblib.dump(bundle,model_path,compress=3)
    info={'status':'passed','model':name,'year':year,'configuration':cfg,'training_meta':metas[0],
          'model_sha256':sha(model_path),'member_model_sha256':bundle['member_model_sha256'],'new_model_fits':0,'test_data_read':False}
    if year<2025:
        features=feature_names()
        frame=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(KEYS+features+['price_valid']).sort('trade_date','ts_code').collect()
        dates=frame['trade_date'].to_numpy();valid=frame['price_valid'].to_numpy();arrays=[]
        for child in cfg['members']:
            cached=pl.read_parquet(members.source_dir(child)/f'raw_{year}.parquet')
            assert cached.select(KEYS).equals(frame.select(KEYS));arrays.append(cached['pred_raw'].to_numpy())
        raw=aggregate(arrays,cfg,dates,valid)
        replay=predict_arrays(load_bundle(model_path),to_matrix(frame,features),dates=dates,valid=valid)
        assert np.array_equal(raw,replay)
        last=frame['trade_date'].unique().sort()[79];mask=dates<=last
        prefix=aggregate([array[mask] for array in arrays],cfg,dates[mask],valid[mask]);assert np.array_equal(prefix,raw[mask])
        frame.select(KEYS).with_columns(pl.Series('pred_raw',raw)).write_parquet(raw_path)
        info.update(prediction_sha256=sha(raw_path),rows=len(frame),model_reload_bit_identical=True,
                    complete_80_day_prefix_bit_identical=True,label_independent_aggregation=True)
    else:info['fulltraining_only_test_prediction_not_generated']=True
    info['elapsed_seconds']=time.monotonic()-started;dump(info_path,info,immutable=True)
    log(f'Ensemble {name} fold{year}: assembled and actual member-model replay passed in {info["elapsed_seconds"]:.1f}s')
    return info


def all_oof():
    freeze();proofs=[]
    for name in CONFIGS:
        for year in YEARS:proofs.append(train_one(name,year))
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,'ensemble_artifacts':30,
         'models_trained':0,'member_annual_training_already_verified':True,'test_data_read':False,
         'all_actual_model_replays_bit_identical':True,'complete_day_prefix_checks':len(proofs)},immutable=True)
    log('All30 neural ensemble OOF artifacts completed; no new OOF fits')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'));parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)


if __name__=='__main__':main()
