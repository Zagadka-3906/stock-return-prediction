"""Learn a second-stage ridge only from mature, earlier annual OOF forecasts."""
from pathlib import Path
import argparse
import gc
import os
import sys
import time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[key]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import regularization_model_sources_20261003 as members
import train_linear_bank_20261003 as linear
from run import FEATURE_FILE,MANIFEST,feature_names,fold_cutoff,to_matrix
from optimize_wave15 import daily_ranks
OUT=ROOT/'analysis/oof_stacking_bank_20261004'
read,dump,sha,log=members.read,members.dump,members.sha,members.log
YEARS=members.YEARS
KEYS=['ts_code','trade_date']
MEMBERS=tuple(sorted(members.CONFIGS))
CONFIGS={f'oof_{name}':{**cfg,'kind':'past_oof_ridge','fallback_model':name,'members':MEMBERS}
         for name,cfg in linear.CONFIGS.items()}
_verified=False


def rank_features(arrays,dates,valid):
    import numpy as np
    assert len(arrays)==len(MEMBERS)
    result=np.empty((len(dates),len(MEMBERS)),dtype=np.float32)
    for index,raw in enumerate(arrays):
        assert len(raw)==len(dates)==len(valid)
        assert np.isfinite(raw[valid]).all() and (raw[valid]>-9.).all(), 'Every price-valid child forecast must enter its daily rank pool'
        result[:,index]=daily_ranks(raw,valid,dates)-.5
    result[~valid]=np.nan
    return result


def training_mask(frame,year,target):
    import numpy as np
    dates=frame['trade_date'].to_numpy()
    return (dates<fold_cutoff(year)) & frame['price_valid'].to_numpy() & np.isfinite(frame[target].to_numpy())


def load_bundle(path):
    import joblib
    return joblib.load(path)


def predict_arrays(bundle,x,dates=None,valid=None):
    import numpy as np
    assert dates is not None and valid is not None
    if bundle['mode']=='first_fold_fallback':
        raw=linear.predict_arrays(bundle['fallback_bundle'],x)
    else:
        children=bundle.get('member_bundles')
        if children is None:
            children=[]
            for name in MEMBERS:
                source=Path(bundle['member_model_paths'][name])
                assert sha(source)==bundle['member_model_sha256'][name]
                children.append(members.load_bundle(source))
        arrays=[members.predict_arrays(child,x,dates=dates,valid=valid) for child in children]
        raw=linear.predict_arrays(bundle['meta_bundle'],rank_features(arrays,dates,valid))
    raw=np.asarray(raw,dtype=np.float64);raw[~valid]=-1e6
    assert np.isfinite(raw).all()
    return raw


def verify():
    global _verified
    protocol=read(OUT/'protocol.json')
    if not _verified:
        for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
        _verified=True
    return protocol


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    members.verify()
    proof=ROOT/'analysis/oof_stacking_preflight_20261004_v2/verification.json'
    assert read(proof)['status']=='passed'
    sources=[Path(__file__),Path(linear.__file__),Path(members.__file__),FEATURE_FILE,MANIFEST,
             ROOT/'run.py',ROOT/'后续选模标准.md',ROOT/'analysis/verify_oof_stacking_20261004_v2.py',proof,
             ROOT/'analysis/linear_bank_preflight_20261003/verification.json']
    for name in MEMBERS:
        folder=members.source_dir(name)
        parent=folder.parent
        sources += [parent/'protocol.json',parent/'oof_audit.json']
        sources.extend(Path(p) for p in read(parent/'protocol.json')['input_sha256'])
        for year in YEARS:
            info=read(folder/f'info_{year}.json');meta=info['training_meta']
            assert info['status']=='passed' and info['model_reload_bit_identical']
            assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']<year*10000+101
            for kind,suffix in (('model','joblib'),('raw','parquet'),('info','json')):
                sources.append(folder/f'{kind}_{year}.{suffix}')
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'configurations':CONFIGS,'members':MEMBERS,'features':feature_names(),'meta_features':MEMBERS,
         'years':YEARS,'same_validation':'2020–2024 annual forward OOF, 1212 continuous dates and 5635800 records',
         'meta_training':'Only mature prior annual OOF forecasts and supplied labels; date strictly below the same existing fold_cutoff. No in-sample child forecasts or current-validation-year labels.',
         'first_fold':'No prior OOF years exist for 2020. Use the fixed matching raw-feature ridge model fitted on mature 2018–2019 rows; this is a disclosed cold-start branch, not a learned 45-model ensemble.',
         'meta_inputs':'Ordered 45 model daily percentiles minus 0.5, float32. Percentile pool is every current-price-valid forecast record, independent of target availability.',
         'preprocessing':'Past meta-training mean/std, mean imputation, clip z to [-8,8], past return quantiles .005/.995; unchanged verified ridge solver and per-row float64 inference.',
         'fulltraining':'Meta fit on mature 2020–2024 OOF pairs, then embed children trained on all permitted mature data before any test-X inference.',
         'new_oof_fits_expected':24,'annual_artifacts_expected':30,'new_child_oof_fits':0,
         'test_data_read':False,'no_early_stopping_on_validation':True,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    verify();log('Six mature past-OOF stacking configurations frozen before scoring')


def load_oof_frame():
    import polars as pl
    return pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train') & pl.col('trade_date').is_between(20200101,20241231)).select(
        KEYS+['price_valid','y_rank','y_ret_1d']).sort('trade_date','ts_code').collect()


def build_features():
    import numpy as np
    import polars as pl
    verify();audit_path=OUT/'feature_audit.json';matrix_path=OUT/'oof_features.npy'
    if audit_path.exists():
        audit=read(audit_path);assert sha(matrix_path)==audit['matrix_sha256'];return
    frame=load_oof_frame();assert len(frame)==5635800 and frame['trade_date'].n_unique()==1212
    matrix=np.lib.format.open_memmap(matrix_path,mode='w+',dtype=np.float32,shape=(len(frame),len(MEMBERS)))
    controls=[];offset=0
    for year in YEARS:
        subset=frame.filter(pl.col('trade_date')//10000==year)
        dates=subset['trade_date'].to_numpy();valid=subset['price_valid'].to_numpy()
        end=offset+len(subset);last=int(np.unique(dates)[79]);prefix=dates<=last
        for index,name in enumerate(MEMBERS):
            path=members.source_dir(name)/f'raw_{year}.parquet';info=read(path.with_name(f'info_{year}.json'))
            assert sha(path)==info['prediction_sha256']
            raw=pl.read_parquet(path);assert raw.select(KEYS).equals(subset.select(KEYS))
            values=raw['pred_raw'].to_numpy();ranks=(daily_ranks(values,valid,dates)-.5).astype(np.float32)
            assert np.isfinite(values[valid]).all() and (values[valid]>-9.).all()
            ranks[~valid]=np.nan;matrix[offset:end,index]=ranks
            replay=(daily_ranks(values[prefix],valid[prefix],dates[prefix])-.5).astype(np.float32)
            replay[~valid[prefix]]=np.nan
            assert np.array_equal(replay,ranks[prefix],equal_nan=True)
        controls.append({'year':year,'members':len(MEMBERS),'complete_first_80_days_bit_identical':True,
                         'target_independent_pool':True,'rows':len(subset)})
        matrix.flush();offset=end;log(f'Stacking feature matrix: fold{year}, all45 child forecasts aligned')
    assert offset==len(frame);del matrix;gc.collect()
    dump(audit_path,{'status':'passed','rows':len(frame),'days':1212,'members':MEMBERS,'dtype':'float32',
         'matrix_sha256':sha(matrix_path),'keys_sha256':linear.engine.array_hash(frame.select(KEYS).hash_rows(seed=2026).to_numpy()),
         'complete_day_prefix_controls':controls,'test_data_read':False},immutable=True)


def train_one(name,year,frame=None,matrix=None):
    import joblib
    import numpy as np
    import polars as pl
    verify();cfg=CONFIGS[name];folder=OUT/name;folder.mkdir(exist_ok=True)
    model_path=folder/f'model_{year}.joblib';info_path=folder/f'info_{year}.json';raw_path=folder/f'raw_{year}.parquet'
    if info_path.exists():
        info=read(info_path);assert sha(model_path)==info['model_sha256']
        if year<2025:assert sha(raw_path)==info['prediction_sha256']
        return info
    started=time.monotonic();cutoff=fold_cutoff(year)
    if year==2020:
        old_info=read(linear.OUT/cfg['fallback_model']/'info_2020.json')
        fallback_path=linear.OUT/cfg['fallback_model']/'model_2020.joblib'
        assert sha(fallback_path)==old_info['model_sha256']
        bundle={'kind':'past_oof_ridge','mode':'first_fold_fallback','config':cfg,
                'fallback_bundle':load_bundle(fallback_path)}
        meta=dict(old_info['training_meta']);new_fits=0;fit_seconds=0.
        raw=pl.read_parquet(linear.OUT/cfg['fallback_model']/'raw_2020.parquet')
        assert sha(linear.OUT/cfg['fallback_model']/'raw_2020.parquet')==old_info['prediction_sha256']
        raw.write_parquet(raw_path)
    else:
        if frame is None:frame=load_oof_frame()
        if matrix is None:matrix=np.load(OUT/'oof_features.npy',mmap_mode='r')
        mask=training_mask(frame,year,cfg['target']);dates=frame['trade_date'].to_numpy()
        x=matrix[mask];y=frame[cfg['target']].to_numpy()[mask]
        all_dates=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        last=int(dates[mask][-1]);label_end=int(all_dates[np.searchsorted(all_dates,last)+1])
        assert last<cutoff and label_end<=cutoff
        past_keys=frame.filter(pl.Series(mask)).select(KEYS)
        meta={'rows':len(y),'days':int(np.unique(dates[mask]).size),'first':int(dates[mask][0]),'last':last,
              'cutoff_exclusive':cutoff,'last_label_end':label_end,'validation_year':year,
              'training_matrix_sha256':linear.engine.array_hash(x),'training_target_sha256':linear.engine.array_hash(y),
              'training_keys_sha256':linear.engine.array_hash(past_keys.hash_rows(seed=2026).to_numpy()),
              'features':feature_names(),'meta_features':MEMBERS,'meta_rows_are_child_oof':True}
        fit_start=time.monotonic();fitted=linear.fit_arrays(x,y,cfg);fit_seconds=time.monotonic()-fit_start
        del x,y,past_keys;gc.collect()
        child_infos={child:members.train_one(child,year) if year==2025 else read(members.source_dir(child)/f'info_{year}.json') for child in MEMBERS}
        for info in child_infos.values():
            child_meta=info['training_meta']
            assert child_meta['last']<child_meta['cutoff_exclusive'] and child_meta['last_label_end']<=child_meta['cutoff_exclusive']
        bundle={'kind':'past_oof_ridge','mode':'learned_past_oof','config':cfg,'meta_bundle':fitted,
                'member_model_paths':{child:str(members.model_path(child,year).resolve()) for child in MEMBERS},
                'member_model_sha256':{child:info['model_sha256'] for child,info in child_infos.items()}}
        if year==2025:
            bundle['member_bundles']=[members.load_bundle(members.model_path(child,year)) for child in MEMBERS]
        new_fits=1
        if year<2025:
            vm=dates//10000==year;vx=matrix[vm];pred=linear.predict_arrays(fitted,vx)
            pred[~frame['price_valid'].to_numpy()[vm]]=-1e6
            raw=frame.filter(pl.Series(vm)).select(KEYS).with_columns(pl.Series('pred_raw',pred))
            raw.write_parquet(raw_path);del vx,pred
    joblib.dump(bundle,model_path,compress=3)
    info={'status':'passed','model':name,'year':year,'configuration':cfg,'training_meta':meta,
          'model_sha256':sha(model_path),'fit_seconds':fit_seconds,'new_model_fits':new_fits,'test_data_read':False,
          'first_fold_is_fixed_raw_feature_fallback':year==2020}
    replay=load_bundle(model_path)
    if year<2025:
        subset=load_oof_frame().filter(pl.col('trade_date')//10000==year)
        assert raw.select(KEYS).equals(subset.select(KEYS))
        dates=subset['trade_date'].to_numpy();valid=subset['price_valid'].to_numpy()
        if year==2020:
            features=feature_names();input_frame=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(KEYS+features).sort('trade_date','ts_code').collect()
            pred=predict_arrays(replay,to_matrix(input_frame,features),dates=dates,valid=valid)
        else:
            vm=frame['trade_date'].to_numpy()//10000==year;vx=matrix[vm]
            pred=linear.predict_arrays(replay['meta_bundle'],vx);pred[~valid]=-1e6
            prefix=dates<=int(np.unique(dates)[79]);pp=linear.predict_arrays(replay['meta_bundle'],vx[prefix]);pp[~valid[prefix]]=-1e6
            assert np.array_equal(pp,pred[prefix]);del vx,pp
        assert np.array_equal(pred,raw['pred_raw'].to_numpy()) and np.isfinite(pred).all()
        info.update(prediction_sha256=sha(raw_path),rows=len(raw),model_reload_bit_identical=True,
                    complete_80_day_prefix_bit_identical=True)
    else:info['fulltraining_only_test_prediction_not_generated']=True
    info['elapsed_seconds']=time.monotonic()-started;dump(info_path,info,immutable=True)
    del bundle,replay;gc.collect();log(f'Stacking {name} fold{year}: fit/reload checks passed in {info["elapsed_seconds"]:.1f}s')
    return info


def all_oof():
    import numpy as np
    import polars as pl
    freeze();build_features();frame=load_oof_frame();matrix=np.load(OUT/'oof_features.npy',mmap_mode='r')
    for year in (*YEARS[1:],2025):
        path=OUT/f'boundary_control_{year}.json'
        if path.exists():continue
        cutoff=fold_cutoff(year)
        poisoned=frame.with_columns([pl.when(pl.col('trade_date')>=cutoff).then(12345.).otherwise(pl.col(c)).alias(c) for c in ('y_rank','y_ret_1d')])
        for target in ('y_rank','y_ret_1d'):
            mask=training_mask(frame,year,target);changed=training_mask(poisoned,year,target)
            assert np.array_equal(mask,changed)
            assert np.array_equal(frame[target].to_numpy()[mask],poisoned[target].to_numpy()[changed])
        dump(path,{'status':'passed','year':year,'cutoff_exclusive':cutoff,
             'both_actual_meta_training_masks_and_targets_bit_identical_under_future_poisoning':True,
             'feature_matrix_has_no_target_inputs':True,'test_data_read':False},immutable=True)
    proofs=[train_one(name,year,frame,matrix) for name in CONFIGS for year in YEARS]
    replay_controls=[]
    for year in YEARS[1:]:
        path=OUT/f'actual_child_replay_{year}.json'
        if path.exists():replay_controls.append(read(path));continue
        name=next(iter(CONFIGS));bundle=load_bundle(OUT/name/f'model_{year}.joblib')
        dates=frame['trade_date'].to_numpy();year_dates=np.unique(dates[dates//10000==year]);last=int(year_dates[79])
        features=feature_names()
        prefix=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)&(pl.col('trade_date')<=last)).select(KEYS+features+['price_valid']).sort('trade_date','ts_code').collect()
        pred=predict_arrays(bundle,to_matrix(prefix,features),dates=prefix['trade_date'].to_numpy(),valid=prefix['price_valid'].to_numpy())
        expected=pl.read_parquet(OUT/name/f'raw_{year}.parquet').filter(pl.col('trade_date')<=last)
        assert prefix.select(KEYS).equals(expected.select(KEYS)) and np.array_equal(pred,expected['pred_raw'].to_numpy())
        control={'status':'passed','year':year,'rows':len(prefix),'days':80,'all45_actual_child_models_reloaded':True,
                 'actual_raw_feature_to_meta_prediction_bit_identical':True,'test_data_read':False}
        dump(path,control,immutable=True);replay_controls.append(control);log(f'Stacking fold{year}: all45 actual child-model replay passed')
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'annual_artifacts':len(proofs),'models_trained':sum(p['new_model_fits'] for p in proofs),
         'first_fold_fixed_fallbacks':6,'new_child_oof_fits':0,'test_data_read':False,
         'all_models_reloaded_bit_identically':True,'actual_child_replay_controls':replay_controls},immutable=True)
    log('All30 stacking OOF artifacts completed,24 learned meta fits and6 fixed fallbacks')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
