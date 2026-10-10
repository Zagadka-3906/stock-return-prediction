"""67-parent past-OOF ridge with paired, prespecified first-year fallbacks."""
from pathlib import Path
import argparse
import gc
import importlib.util
import shutil
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
SOURCE=ROOT/'analysis/train_oof_stacking_bank_20261004.py'
spec=importlib.util.spec_from_file_location('isolated_nonlinear_stacking_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
import fourier_ridge_model_sources_20261004 as members
OUT=ROOT/'analysis/nonlinear_stacking_bank_20261004'
PREFLIGHT=ROOT/'analysis/nonlinear_stacking_preflight_20261004/verification.json'
OLD=ROOT/'analysis/expanded_stacking_bank_20261004'
MEMBERS=tuple(sorted(name for name,cfg in members.CONFIGS.items() if cfg['kind']!='past_oof_ridge'))
assert len(MEMBERS)==67
CONFIGS={f'nonlinear_oof_{name}_{policy}':{**cfg,'kind':'past_oof_ridge','fallback_model':name,
         'members':MEMBERS,'first_fold_policy':policy}
         for name,cfg in engine.linear.CONFIGS.items() for policy in ('ridge','uniform')}
BASE_CONFIGS=tuple(name for name,cfg in CONFIGS.items() if cfg['first_fold_policy']=='ridge')
engine.OUT=OUT;engine.MEMBERS=MEMBERS;engine.CONFIGS=CONFIGS;engine.members=members
original_train_one=engine.train_one
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS
KEYS=engine.KEYS
linear=engine.linear
rank_features=engine.rank_features
training_mask=engine.training_mask
load_oof_frame=engine.load_oof_frame
load_bundle=engine.load_bundle


def uniform_rank_mean(matrix,valid):
    import numpy as np
    weights=np.full(len(MEMBERS),1./len(MEMBERS),dtype=np.float64)
    raw=np.einsum('ij,j->i',matrix,weights,optimize=False,dtype=np.float64)
    raw[~valid]=-1e6
    assert np.isfinite(raw).all()
    return raw


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
                path=Path(bundle['member_model_paths'][name]);assert sha(path)==bundle['member_model_sha256'][name]
                children.append(members.load_bundle(path))
        arrays=[members.predict_arrays(child,x,dates=dates,valid=valid) for child in children]
        matrix=rank_features(arrays,dates,valid)
        raw=uniform_rank_mean(matrix,valid) if bundle['mode']=='first_fold_uniform_rank' else linear.predict_arrays(bundle['meta_bundle'],matrix)
    raw=np.asarray(raw,dtype=np.float64);raw[~valid]=-1e6
    assert np.isfinite(raw).all()
    return raw


engine.predict_arrays=predict_arrays
verify=engine.verify


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    members.verify();assert read(PREFLIGHT)['status']=='passed'
    sources=[Path(__file__),ROOT/'analysis/prepare_nonlinear_stacking_bank_20261004.py',ROOT/'analysis/nonlinear_stacking_sources_prepared_20261004.json',SOURCE,Path(members.__file__),Path(linear.__file__),engine.FEATURE_FILE,engine.MANIFEST,
             ROOT/'run.py',ROOT/'后续选模标准.md',PREFLIGHT,ROOT/'analysis/verify_nonlinear_stacking_20261004.py',
             ROOT/'analysis/nonlinear_stacking_model_sources_20261004.py',OLD/'protocol.json',OLD/'feature_audit.json',OLD/'oof_features.npy',
             ROOT/'analysis/causal_model_loading_20261004.py',
             ROOT/'analysis/current_day_input_loading_qa_20261004/verification.json',
             ROOT/'analysis/linear_bank_preflight_20261003/verification.json']
    for name in MEMBERS:
        folder=members.source_dir(name);parent=folder.parent
        sources.extend([parent/'protocol.json',parent/'oof_audit.json'])
        sources.extend(Path(p) for p in read(parent/'protocol.json')['input_sha256'])
        for year in YEARS:
            info=read(folder/f'info_{year}.json');meta=info['training_meta']
            assert info['status']=='passed' and info['model_reload_bit_identical']
            assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']<year*10000+101
            for kind,suffix in (('model','joblib'),('raw','parquet'),('info','json')):sources.append(folder/f'{kind}_{year}.{suffix}')
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'configurations':CONFIGS,'members':MEMBERS,'features':engine.feature_names(),'meta_features':MEMBERS,'years':YEARS,
         'same_validation':'2020–2024,1212 continuous dates,5635800 records; unchanged mature-label boundary',
         'meta_training':'Only mature earlier annual child-OOF forecasts and provided labels. Six distinct target/penalty fits per subsequent year; paired first-year schemes reuse these exact fitted coefficients.',
         'first_fold_policies':{'ridge':'Matching frozen raw63-feature one-day rank/return ridge fitted on mature2018–2019 data.',
             'uniform':'Fixed equal-weight daily-rank mean of all67 mature2018–2019-trained children. No learned meta weights and no2020 targets used. Ordinal output gets the same later causal one-day-return calibration.'},
         'feature_pool':'Every current-price-valid child forecast, independently of target eligibility; float32 daily percentiles minus0.5.',
         'feature_cache_reuse':'Reuse the exact frozen55 existing feature columns only after source and matrix SHA checks; compute the12 new columns under the same rule.',
         'preprocessing':'Frozen past-only ridge mean/std, imputation, clip8, past return quantiles and per-row float64 inference.',
         'new_oof_fits_expected':24,'annual_artifacts_expected':60,'fixed_first_fold_artifacts':12,
         'paired_later_fold_reuses_expected':24,'new_child_oof_fits':0,
         'fulltraining':'Fit on mature2020–2024 child OOF; train all67 children on permitted mature data and embed them before opening test feature rows. Paired schemes reuse the same full-training fit.',
         'test_data_read':False,'no_validation_epoch_stopping':True,
         'input_sha256':{str(p.resolve()):sha(p) for p in dict.fromkeys(sources)}},immutable=True)
    verify();log('Twelve67-parent stacking schemes frozen;24 new learned fits, paired fallback controls')


def build_features():
    import numpy as np
    import polars as pl
    verify();audit_path=OUT/'feature_audit.json';matrix_path=OUT/'oof_features.npy'
    if audit_path.exists():assert sha(matrix_path)==read(audit_path)['matrix_sha256'];return
    frame=load_oof_frame();assert len(frame)==5635800 and frame['trade_date'].n_unique()==1212
    old_audit=read(OLD/'feature_audit.json');assert sha(OLD/'oof_features.npy')==old_audit['matrix_sha256']
    assert linear.engine.array_hash(frame.select(KEYS).hash_rows(seed=2026).to_numpy())==old_audit['keys_sha256']
    old_names=tuple(old_audit['members']);old_matrix=np.load(OLD/'oof_features.npy',mmap_mode='r')
    assert len(old_names)==55 and set(old_names).issubset(MEMBERS) and len(set(MEMBERS)-set(old_names))==12
    matrix=np.lib.format.open_memmap(matrix_path,mode='w+',dtype=np.float32,shape=(len(frame),len(MEMBERS)))
    for name in old_names:matrix[:,MEMBERS.index(name)]=old_matrix[:,old_names.index(name)]
    del old_matrix;gc.collect();controls=[];offset=0
    for year in YEARS:
        subset=frame.filter(pl.col('trade_date')//10000==year);dates=subset['trade_date'].to_numpy();valid=subset['price_valid'].to_numpy()
        end=offset+len(subset);prefix=dates<=int(np.unique(dates)[79])
        for index,name in enumerate(MEMBERS):
            path=members.source_dir(name)/f'raw_{year}.parquet';info=read(path.with_name(f'info_{year}.json'));assert sha(path)==info['prediction_sha256']
            raw=pl.read_parquet(path);assert raw.select(KEYS).equals(subset.select(KEYS));values=raw['pred_raw'].to_numpy()
            assert np.isfinite(values[valid]).all() and (values[valid]>-9.).all()
            if name not in old_names:
                ranks=(engine.daily_ranks(values,valid,dates)-.5).astype(np.float32);ranks[~valid]=np.nan;matrix[offset:end,index]=ranks
            replay=(engine.daily_ranks(values[prefix],valid[prefix],dates[prefix])-.5).astype(np.float32);replay[~valid[prefix]]=np.nan
            assert np.array_equal(replay,matrix[offset:end,index][prefix],equal_nan=True),(name,year)
        matrix.flush();controls.append({'year':year,'members':67,'complete_first80_day_raw_rank_replay_bit_identical':True,
                  'target_independent_pool':True,'rows':len(subset)});offset=end;log(f'Expanded stacking features: fold{year},67 children aligned')
    del matrix;gc.collect()
    dump(audit_path,{'status':'passed','rows':len(frame),'days':1212,'members':MEMBERS,'dtype':'float32',
         'matrix_sha256':sha(matrix_path),'keys_sha256':old_audit['keys_sha256'],'reused_frozen_columns':55,
         'new_columns':12,'complete_day_prefix_controls':controls,'test_data_read':False},immutable=True)


def train_one(name,year,frame=None,matrix=None):
    import joblib
    import numpy as np
    import polars as pl
    if year==2025:wait_for_fit_reserve()
    verify();cfg=CONFIGS[name]
    if cfg['first_fold_policy']=='ridge':return original_train_one(name,year,frame,matrix)
    folder=OUT/name;folder.mkdir(exist_ok=True);model_path=folder/f'model_{year}.joblib';info_path=folder/f'info_{year}.json';raw_path=folder/f'raw_{year}.parquet'
    if info_path.exists():
        info=read(info_path);assert sha(model_path)==info['model_sha256']
        if year<2025:assert sha(raw_path)==info['prediction_sha256']
        return info
    started=time.monotonic();paired=name.rsplit('_',1)[0]+'_ridge'
    base_info=train_one(paired,year,frame,matrix);bundle=load_bundle(OUT/paired/f'model_{year}.joblib')
    bundle['config']=cfg
    if year==2020:
        if frame is None:frame=load_oof_frame()
        if matrix is None:matrix=np.load(OUT/'oof_features.npy',mmap_mode='r')
        mask=frame['trade_date'].to_numpy()//10000==year;subset=frame.filter(pl.Series(mask));valid=subset['price_valid'].to_numpy()
        child_infos={n:read(members.source_dir(n)/'info_2020.json') for n in MEMBERS}
        bundle={'kind':'past_oof_ridge','mode':'first_fold_uniform_rank','config':cfg,
                'member_model_paths':{n:str(members.model_path(n,2020).resolve()) for n in MEMBERS},
                'member_model_sha256':{n:info['model_sha256'] for n,info in child_infos.items()}}
        raw=uniform_rank_mean(matrix[mask],valid)
        subset.select(KEYS).with_columns(pl.Series('pred_raw',raw)).write_parquet(raw_path)
    elif year<2025:shutil.copyfile(OUT/paired/f'raw_{year}.parquet',raw_path)
    joblib.dump(bundle,model_path,compress=3);replay=load_bundle(model_path)
    info={**base_info,'model':name,'configuration':cfg,'model_sha256':sha(model_path),'fit_seconds':0.,'new_model_fits':0,
          'first_fold_is_fixed_raw_feature_fallback':False,'first_fold_is_fixed_uniform_rank_fallback':year==2020,
          'paired_fit_reused_from':str((OUT/paired/f'info_{year}.json').resolve()),'paired_info_sha256':sha(OUT/paired/f'info_{year}.json')}
    if year<2025:
        if frame is None:frame=load_oof_frame()
        if matrix is None:matrix=np.load(OUT/'oof_features.npy',mmap_mode='r')
        dates=frame['trade_date'].to_numpy();mask=dates//10000==year;valid=frame['price_valid'].to_numpy()[mask];vx=matrix[mask]
        pred=uniform_rank_mean(vx,valid) if year==2020 else linear.predict_arrays(replay['meta_bundle'],vx)
        pred[~valid]=-1e6;cached=pl.read_parquet(raw_path);assert np.array_equal(pred,cached['pred_raw'].to_numpy())
        first=dates[mask]<=int(np.unique(dates[mask])[79])
        pp=uniform_rank_mean(vx[first],valid[first]) if year==2020 else linear.predict_arrays(replay['meta_bundle'],vx[first])
        pp[~valid[first]]=-1e6;assert np.array_equal(pred[first],pp)
        info.update(prediction_sha256=sha(raw_path),rows=len(pred),model_reload_bit_identical=True,complete_80_day_prefix_bit_identical=True)
        del vx,pred,pp,cached
    info['elapsed_seconds']=time.monotonic()-started;dump(info_path,info,immutable=True);del bundle,replay;gc.collect()
    log(f'Expanded stacking {name} fold{year}: fixed/reused fitting, reload and prefix checks passed')
    return info


engine.train_one=train_one


def all_oof():
    import numpy as np
    import polars as pl
    wait_for_fit_reserve();freeze();build_features();frame=load_oof_frame();matrix=np.load(OUT/'oof_features.npy',mmap_mode='r')
    for year in (*YEARS[1:],2025):
        path=OUT/f'boundary_control_{year}.json'
        if path.exists():continue
        cutoff=engine.fold_cutoff(year);poisoned=frame.with_columns([pl.when(pl.col('trade_date')>=cutoff).then(12345.).otherwise(pl.col(c)).alias(c) for c in ('y_rank','y_ret_1d')])
        for target in ('y_rank','y_ret_1d'):
            mask=training_mask(frame,year,target);changed=training_mask(poisoned,year,target)
            assert np.array_equal(mask,changed) and np.array_equal(frame[target].to_numpy()[mask],poisoned[target].to_numpy()[changed])
        dump(path,{'status':'passed','year':year,'cutoff_exclusive':cutoff,'both_actual_meta_masks_and_targets_bit_identical_under_future_poisoning':True,
                 'feature_matrix_has_no_target_inputs':True,'test_data_read':False},immutable=True)
    proofs=[train_one(name,year,frame,matrix) for name in CONFIGS for year in YEARS]
    controls=[]
    for year in YEARS:
        path=OUT/f'actual_child_replay_{year}.json'
        if path.exists():controls.append(read(path));continue
        features=engine.feature_names();subset=frame.filter(pl.col('trade_date')//10000==year);last=int(subset['trade_date'].unique().sort()[79])
        prefix=pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)&(pl.col('trade_date')<=last)).select(KEYS+features+['price_valid']).sort('trade_date','ts_code').collect()
        x=engine.to_matrix(prefix,features);dates=prefix['trade_date'].to_numpy();valid=prefix['price_valid'].to_numpy()
        child_arrays=[members.predict_arrays(members.load_bundle(members.model_path(n,year)),x,dates=dates,valid=valid) for n in MEMBERS]
        rebuilt=rank_features(child_arrays,dates,valid);vm=(frame['trade_date'].to_numpy()//10000==year)&(frame['trade_date'].to_numpy()<=last)
        assert np.array_equal(rebuilt,matrix[vm],equal_nan=True)
        for name in CONFIGS:
            bundle=load_bundle(OUT/name/f'model_{year}.joblib')
            if bundle['mode']=='first_fold_fallback':pred=linear.predict_arrays(bundle['fallback_bundle'],x)
            elif bundle['mode']=='first_fold_uniform_rank':pred=uniform_rank_mean(rebuilt,valid)
            else:pred=linear.predict_arrays(bundle['meta_bundle'],rebuilt)
            pred[~valid]=-1e6;cached=pl.read_parquet(OUT/name/f'raw_{year}.parquet').filter(pl.col('trade_date')<=last)
            assert prefix.select(KEYS).equals(cached.select(KEYS)) and np.array_equal(pred,cached['pred_raw'].to_numpy()),(name,year)
        if year==2020:
            name=next(n for n,cfg in CONFIGS.items() if cfg['first_fold_policy']=='uniform')
            direct=predict_arrays(load_bundle(OUT/name/f'model_{year}.joblib'),x,dates=dates,valid=valid)
            assert np.array_equal(direct,uniform_rank_mean(rebuilt,valid))
        control={'status':'passed','year':year,'days':80,'rows':len(prefix),'all67_actual_children_reloaded':True,
                 'all12_raw_feature_to_output_replays_bit_identical':True,'test_data_read':False}
        dump(path,control,immutable=True);controls.append(control);log(f'Expanded stacking fold{year}:67 child and12 scheme actual replay passed')
        del x,child_arrays,rebuilt,prefix;gc.collect()
    assert sum(p['new_model_fits'] for p in proofs)==24
    for cfg in BASE_CONFIGS:
        alias=cfg.rsplit('_',1)[0]+'_uniform'
        for year in YEARS[1:]:assert read(OUT/cfg/f'info_{year}.json')['prediction_sha256']==read(OUT/alias/f'info_{year}.json')['prediction_sha256']
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,'annual_artifacts':60,'models_trained':24,
         'first_fold_fixed_artifacts':12,'paired_later_fold_reuses':24,'new_child_oof_fits':0,'actual_child_replay_controls':controls,
         'all_models_reloaded_bit_identically':True,'test_data_read':False},immutable=True)
    log('Expanded stacking completed:60 forecast artifacts,24 distinct learned fits,12 fixed first-year branches')


def wait_for_fit_reserve():
    import psutil
    while psutil.virtual_memory().available<8*2**30:
        log('Waiting for chosen8GiB free-RAM reserve; no physical exhaustion inferred');time.sleep(10)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
